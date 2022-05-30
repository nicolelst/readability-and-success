import csv
from datetime import date
import json
import os
from numpy import nan
import pandas as pd
import sys

sys.path.append("./readabilityinscience")
import functions.readabilityFunctions as rf
sys.path.append("./pmidcite/src")
from pmidcite.icite.downloader import get_downloader


def init_final_data_csv(outputDataFileName, outputJournalFileName, journalListFileName, dataFolderName):
    '''
    Initializes final output files, returns list of pmids
    Function parameters:
    - outputDataFileName: name of data file (output), with data regarding each article
    - outputJournalFileName: name of journal file (output), with data regarding each journal
    - journalListFileName: name of file with list of journals 
    - dataFolderName: name of folder where journal data is stored
    '''
    # initialise file for article data
    dataHeader = ['journal_ID', 'article_ID', 'pmid', 'pubdate_year', 'citation_count', 'citation_count_per_year', 'fre', 'ndc', 'ndc_perc_difficult', 'sentence_count', 'word_count']
    dataFile = open(outputDataFileName, 'w', encoding='UTF8', newline='')
    dataWriter = csv.writer(dataFile)
    dataWriter.writerow(dataHeader) # write header row

    # initialise file for journal data
    journalHeader = ['journal_ID', 'journal', 'journal_full_title', 'downloaded_articles', 'missing_abstracts', 'non_english_articles', 'usable_articles', 'final_article_count']
    journalsFile = open(outputJournalFileName, 'w', encoding='UTF8', newline='')
    journalsWriter = csv.writer(journalsFile)
    journalsWriter.writerow(journalHeader) # write header row

    # iterate list of journals
    journalInfo = pd.read_csv(journalListFileName, index_col="journalID")
    for journal_ID in journalInfo.index.values: #list(range(0, len(journalInfo))):
        # find search results for journal
        journal = journalInfo.search[journal_ID].replace(' ','_').replace('\"','').lower()
        try: 
            searchResults = open('%s/abstracts/%s/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % (dataFolderName, journal))
        except: 
            journal = '%s[Journal]' % journalInfo.journal[journal_ID]
            journal = journal.replace(' ','_').replace('\"','').lower()
            searchResults = open('%s/abstracts/%s/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % (dataFolderName, journal))
        journal = journal.replace("[journal]", "")

        print("INITIALIZING...\t", journal_ID, journal)
        data = json.load(searchResults)        
        num_missing_abstract = 0 # to track number of articles with no abstracts
        num_non_eng = 0 # to track number of non-english articles
        for articleID in list(data['articleID'].keys()):
            abstract_text = data['abstracttext'][articleID]
            if abstract_text == None or abstract_text == "": # ignore articles with no abstract
                num_missing_abstract += 1
                continue

            language = data['language'][articleID]
            if language != 'eng': # ignore non-english articles
                num_non_eng += 1
                continue

            article_ID = articleID 
            pmid = data['pmid'][articleID]
            pubdate_year = data['pubdate_year'][articleID]

            # record article data 
            line = [journal_ID, article_ID, pmid, pubdate_year] + [nan] * 7
            dataWriter.writerow(line)
        searchResults.close()
        # record journal data
        line = [journal_ID, journal, list(data['journal_title'].values())[0], len(list(data['articleID'].keys())), num_missing_abstract, num_non_eng, len(list(data['articleID'].keys())) - num_missing_abstract - num_non_eng] + [nan]
        journalsWriter.writerow(line)

    dataFile.close()
    journalsFile.close()


def remove_repeated_articles(outputDataFileName, outputJournalFileName):
    '''
    Removes articles which appear in multiple journals from output data file, 
    and updates final article count for each journal in output journal file.
    Only the first occurence of each pmid is preserved.
    '''
    outputData = pd.read_csv(outputDataFileName, index_col=['journal_ID', 'article_ID'])
    outputData = outputData.drop_duplicates(subset=['pmid'], keep='first')
    outputData.to_csv(outputDataFileName, index=True)

    journalData = pd.read_csv(outputJournalFileName, index_col=['journal_ID'])
    for journal_ID in journalData.index.values:
        journalData.loc[journal_ID, 'final_article_count'] = (outputData.index.get_level_values(0)==journal_ID).sum()
    journalData.to_csv(outputJournalFileName, index=True)


def get_readability(journalID, journalName, outputDataFileName, dataFolderName):
    '''
    Function parameters:
    - journalName: name of journal
    - outputDataFileName: name of data file (output), with data regarding each article
    - dataFolderName: name of folder where journal data is stored
    ''' 
    searchresults_path = '%s/abstracts/%s[journal]/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % (dataFolderName, journalName)
    readability_path = 'Data analysis/readabilityTemp.json'
    rf.analyze(path = searchresults_path,\
            spath = readability_path, \
            textType = 'abstracttext', \
            columnList = {'journal_title','articleID','pmid','pubdate_year'}, \
            doPreprocessing = 1)
    readability = open(readability_path)
    readabilityData = json.load(readability)
    outputData = pd.read_csv(outputDataFileName, index_col=['journal_ID', 'article_ID'])
    selectedData = outputData[outputData.index.get_level_values(0)==journalID] # get only rows with matching journalID
    for index in selectedData.index.values: # get only for this journal
        outputData.loc[index, 'fre'] = readabilityData['flesch'][str(index[1])]
        outputData.loc[index, 'ndc'] = readabilityData['NDC'][str(index[1])]
        outputData.loc[index, 'ndc_perc_difficult'] = readabilityData['PercDiffWord'][str(index[1])]
        outputData.loc[index, 'sentence_count'] = readabilityData['sentenceCount'][str(index[1])]
        outputData.loc[index, 'word_count'] = readabilityData['wordCount'][str(index[1])]
    outputData.to_csv(outputDataFileName, index=True)
    readability.close()
    os.remove(readability_path)


def get_citations(outputDataFileName, outputJournalFileName):
    '''
    Get citations for articles listed in output data file
    Function parameters:
    - outputDataFileName: name of data file (output), with data regarding each article
    - outputJournalFileName: name of journal file (output), with data regarding each journal
    ''' 
    outputData = pd.read_csv(outputDataFileName, index_col=['journal_ID', 'article_ID'])

    dnldr = get_downloader() # use pmidcite for citation counts
    citation_counts = {}
    try: 
        pmids = outputData['pmid'].astype('int64').tolist()
        nih_entries = dnldr.get_icites(pmids)
    except: 
        print("Failed to get citations, retrying journal by journal...")
        journalData = pd.read_csv(outputJournalFileName, index_col="journal_ID")
        for journal_ID, journal in journalData['journal'].iteritems(): 
            print("> Getting citations for", journal_ID, journal)
            selectedData = outputData[outputData.index.get_level_values(0)==journal_ID] # get only rows with matching journalID
            pmids = selectedData['pmid'].astype('int64').tolist()
            nih_entries = dnldr.get_icites(pmids)
            for e in nih_entries:
                citation_counts[e.dct["pmid"]] = e.dct["citation_count"]
    else: 
        for e in nih_entries:
            citation_counts[e.dct["pmid"]] = e.dct["citation_count"]
    
    # with open("pmids_citation_dict.json", "w") as outfile:
    #     json.dump(citation_counts, outfile)

    # f = open('pmids_citation_dict.json')
    # citation_counts = json.load(f)
    for index in outputData.index.values:
        pmid = str(int(outputData.loc[index]['pmid']))
        pubdate_year = outputData.loc[index]['pubdate_year']
        outputData.loc[index, 'citation_count'] = citation_counts[pmid] 
        outputData.loc[index, 'citation_count_per_year'] = citation_counts[pmid] / (date.today().year - pubdate_year)  
    outputData.to_csv(outputDataFileName, index=True)


def get_final_data_csv(outputDataFileName, outputJournalFileName, journalListFileName, dataFolderName):
    '''
    Outputs two csv files:
    - data file: data about each article (journal, article id, pmid, readability measures, citation counts)
        - journal, article_ID, pmid: information for identifying article
        - pubdate_year: year of publishing
        - citation_count: number of citations
        - citation_count_per_year: average number of citations per year since publishing
        - fre, ndc, ndc_perc_difficult: readability measures based on abstract 
        - sentence_count, word_count: number of sentences/words in abstract
    - journal file: data about each journal (number of articles downloaded / used for analysis)
        - journal: string used to identify journal, name of folder for this journal
        - full_journal_title: full title of journal
        - downloaded_articles: number of articles downloaded from querying this journal on pubmed
        - missing_abstracts: number of articles without abstracts
        - non_english_articles: number of articles with abstracts but not in english
        - usable_articles: final number of articles used for analysis
    
    Function parameters:
    - outputDataFileName: name of data file (output)
    - outputJournalFileName: name of journal file (output)
    - journalListFileName: name of file with list of journals 
    - dataFolderName: name of folder where journal data is stored
    '''

    # TODO print total counts after each section?
    # TODO why top pmid are floats
    # init_final_data_csv(outputDataFileName, outputJournalFileName, journalListFileName, dataFolderName)
    # print("REMOVING REPEATED ARTICLES...")
    # remove_repeated_articles(outputDataFileName, outputJournalFileName)
    # TODO redo top journal 3 memory error
    print("GETTING CITATIONS...")
    get_citations(outputDataFileName, outputJournalFileName)
    # TODO TODO REDO COUNT PER YEAR TODO TODO 
    # 0 citations, 0 years (2022 pub), no pubdate, nan(?)
    print("CALCULATING READABILITY...")
    journalData = pd.read_csv(outputJournalFileName, index_col="journal_ID")
    for journal_ID, journal in journalData['journal'].iteritems(): 
        # TODO get readability for 3
        print("analysing", journal_ID)
        journal = journalData.loc[journal_ID, 'journal']
        if journalData.loc[journal_ID, 'final_article_count'] == 0: # TODO test?
            continue
        get_readability(journal_ID, journal, outputDataFileName, dataFolderName)
        print("ANALYSIS COMPLETED!\t", journal_ID, journal)


def main(): 
    # get_final_data_csv(outputDataFileName = 'Data analysis/articles_test.csv', \
    #                     outputJournalFileName = 'Data analysis/journals_test.csv', \
    #                     journalListFileName = 'Journal selection/testJournals.csv', \
    #                     dataFolderName = 'topJournalData')

    print("============== MEDIAN JOURNALS ==============") # 71422 articles 
    get_final_data_csv(outputDataFileName = 'Data analysis/median_journals_articles.csv', \
                        outputJournalFileName = 'Data analysis/median_journals_info.csv', \
                        journalListFileName = 'Journal selection/medianJournals.csv', \
                        dataFolderName = 'medianJournalData')

    print("============== TOP JOURNALS ==============") # 259,000 of 1,253,545
    get_final_data_csv(outputDataFileName = 'Data analysis/top_journals_articles.csv', \
                        outputJournalFileName = 'Data analysis/top_journals_info.csv', \
                        journalListFileName = 'Journal selection/topJournals.csv', \
                        dataFolderName = 'topJournalData')


main()

