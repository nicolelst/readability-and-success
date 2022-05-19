import csv
import json
import pandas as pd
import sys
sys.path.append("pmidcite\\src")
from pmidcite.icite.downloader import get_downloader

dnldr = get_downloader()

def get_final_data_csv(dataFileName, journalFileName, journalInfoFileName, folderName):
    '''
    Outputs two csv files:
    - data file: data about each article (journal, article id, pmid, readability measures, citation counts)
        - journal, article_ID, pmid: information for identifying article
        - pubdate_year: year of publishing
        - language
        - abstract_text
        - citation_count
        - TODO readability measures
    - journal file: data about each journal (number of articles downloaded / used for analysis)
        - journal: string used to identify journal, name of folder for this journal
        - full_journal_title: full title of journal
        - downloaded_articles: number of articles downloaded from querying this journal on pubmed
        - missing_abstracts: number of articles without abstracts
        - non_english_articles: number of articles with abstracts but not in english
        - usable_articles: final number of articles used for analysis
    
    Function parameters:
    - dataFileName: name of data file
    - journalFileName: name of journal file
    - journalInfoFileName: name of file with list of journals 
    - folderName: name of folder where journal data is stored
    '''
    # initialise file for article data
    dataHeader = ['journal', 'article_ID', 'pmid', 'pubdate_year', 'language', 'abstract_text', 'citation_count']
    dataFile = open(dataFileName, 'w', encoding='UTF8', newline='')
    dataWriter = csv.writer(dataFile)
    dataWriter.writerow(dataHeader) # write header row

    # initialise file for journal data
    journalHeader = ['journal', 'full_journal_title', 'downloaded_articles', 'missing_abstracts', 'non_english_articles', 'usable_articles']
    journalsFile = open(journalFileName, 'w', encoding='UTF8', newline='')
    journalsWriter = csv.writer(journalsFile)
    journalsWriter.writerow(journalHeader) # write header row

    # iterate list of journals
    journalInfo = pd.read_csv(journalInfoFileName)
    for i in list(range(0, len(journalInfo))):
        # find search results for journal
        journal = journalInfo.search[i].replace(' ','_').replace('\"','').lower()
        try: 
            searchResults = open('%s/abstracts/%s/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % (folderName, journal))
        except: 
            journal = '%s[Journal]' % journalInfo.journal[i]
            journal = journal.replace(' ','_').replace('\"','').lower()
            searchResults = open('%s/abstracts/%s/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % (folderName, journal))
        journal = journal.rstrip("[journal]")
        print(journalInfo.journalID[i], journal)
        data = json.load(searchResults)        

        # get citation count for each article in journal
        pmids = list(data['pmid'].values())
        nih_entries = dnldr.get_icites(pmids)
        citation_counts = {}
        for e in nih_entries:
            citation_counts[e.dct["pmid"]] = e.dct["citation_count"]

        num_missing_abstract = 0 # to track number of articles with no abstracts
        num_non_eng = 0 # to track number of non-english articles
        for index in list(data['articleID'].keys()):
            abstract_text = data['abstracttext'][index]
            if abstract_text == None or abstract_text == "": # ignore articles with no abstract
                num_missing_abstract += 1
                continue

            language = data['language'][index]
            if language != 'eng': # ignore non-english articles
                num_non_eng += 1
                continue

            article_ID = index 
            pmid = data['pmid'][index]
            pubdate_year = data['pubdate_year'][index]

            citation_count = citation_counts[pmid] 

            # fre, ndc, ndc_perc_difficult = getReadability(abstractText)
            # if not (fre == ndc == ndc_perc_difficult == nan):
            #     line = [j, index, pmid, year, 2022-year, 0, fre, ndc, ndc_perc_difficult]
            #     writer.writerow(line)

            # record article data 
            line = [journal, article_ID, pmid, pubdate_year, language, abstract_text, citation_count]
            dataWriter.writerow(line)
        searchResults.close()
        # record journal data
        line = [journal, list(data['journal_title'].values())[0], len(pmids), num_missing_abstract, num_non_eng, len(pmids) - num_missing_abstract - num_non_eng]
        journalsWriter.writerow(line)

    dataFile.close()
    journalsFile.close()

get_final_data_csv(dataFileName = 'Data analysis/cite_test.csv', \
                    journalFileName = 'Data analysis/journals_test.csv', \
                    journalInfoFileName = 'Journal selection/testJournals.csv', \
                    folderName = 'topJournalData')

# get_final_data_csv(dataFileName = 'Data analysis/top_journals_article_data.csv', \ 
#                     journalFileName = 'Data analysis/top_journals_data.csv', \
#                     journalInfoFileName = 'Journal selection/topJournals.csv', \
#                     folderName = 'topJournalData')