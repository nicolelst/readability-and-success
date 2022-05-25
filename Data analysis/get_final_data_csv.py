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
    journalHeader = ['journal_ID', 'journal', 'journal_full_title', 'downloaded_articles', 'missing_abstracts', 'non_english_articles', 'usable_articles']
    journalsFile = open(outputJournalFileName, 'w', encoding='UTF8', newline='')
    journalsWriter = csv.writer(journalsFile)
    journalsWriter.writerow(journalHeader) # write header row

    # iterate list of journals
    journalInfo = pd.read_csv(journalListFileName, index_col="journalID")
    pmids = []
    for journal_ID in journalInfo.index.values: #list(range(0, len(journalInfo))):
        # find search results for journal
        journal = journalInfo.search[journal_ID].replace(' ','_').replace('\"','').lower()
        try: 
            searchResults = open('%s/abstracts/%s/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % (dataFolderName, journal))
        except: 
            journal = '%s[Journal]' % journalInfo.journal[journal_ID]
            journal = journal.replace(' ','_').replace('\"','').lower()
            searchResults = open('%s/abstracts/%s/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % (dataFolderName, journal))
        journal = journal.rstrip("[journal]")

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
            pmids.append(pmid)
            pubdate_year = data['pubdate_year'][articleID]

            # record article data 
            line = [journal_ID, article_ID, pmid, pubdate_year] + [nan] * 7
            dataWriter.writerow(line)
        searchResults.close()
        # record journal data
        line = [journal_ID, journal, list(data['journal_title'].values())[0], len(list(data['articleID'].keys())), num_missing_abstract, num_non_eng, len(list(data['articleID'].keys())) - num_missing_abstract - num_non_eng]
        journalsWriter.writerow(line)

    dataFile.close()
    journalsFile.close()
    return pmids


def get_readability(journalID, journalName, outputDataFileName, dataFolderName):
    '''
    Function parameters:
    - journalName: name of journal
    - outputDataFileName: name of data file (output), with data regarding each article
    - dataFolderName: name of folder where journal data is stored
    ''' # TODO
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


def get_citations(pmids, outputDataFileName):
    '''
    Function parameters:
    - pmids: list of pmids
    - outputDataFileName: name of data file (output), with data regarding each article
    ''' # TODO
    dnldr = get_downloader() # for citation counts
    # get citation count for each article in journal
    nih_entries = dnldr.get_icites(pmids)
    citation_counts = {}
    for e in nih_entries:
        citation_counts[e.dct["pmid"]] = e.dct["citation_count"]
    
    outputData = pd.read_csv(outputDataFileName, index_col=['journal_ID', 'article_ID'])
    for index in outputData.index.values:
        pmid = outputData.loc[index]['pmid']
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

    pmids = init_final_data_csv(outputDataFileName, outputJournalFileName, journalListFileName, dataFolderName)
    print("GETTING CITATIONS...")
    get_citations(pmids, outputDataFileName)
    print("CALCULATING READABILITY...")
    journalData = pd.read_csv(outputJournalFileName, index_col="journal_ID")
    for journal_ID, journal in journalData['journal'].iteritems(): 
        get_readability(journal_ID, journal, outputDataFileName, dataFolderName)
        print("ANALYSIS COMPLETED!\t", journal_ID, journal)


def main(): 
    get_final_data_csv(outputDataFileName = 'Data analysis/articles_test.csv', \
                        outputJournalFileName = 'Data analysis/journals_test.csv', \
                        journalListFileName = 'Journal selection/testJournals.csv', \
                        dataFolderName = 'topJournalData')

    # get_final_data_csv(dataFileName = 'Data analysis/top_journals_articles.csv', \ 
    #                     journalFileName = 'Data analysis/top_journals_info.csv', \
    #                     journalInfoFileName = 'Journal selection/topJournals.csv', \
    #                     dataFolderName = 'topJournalData')
    
    # get_final_data_csv(dataFileName = 'Data analysis/median_journals_articles.csv', \ 
    #                     journalFileName = 'Data analysis/median_journals_info.csv', \
    #                     journalInfoFileName = 'Journal selection/medianJournals.csv', \
    #                     dataFolderName = 'medianJournalData')

main()

