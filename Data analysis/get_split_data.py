import csv
from datetime import date
import json
import os
from numpy import nan
import pandas as pd
import sys

from pyparsing import nums

sys.path.append("./readabilityinscience")
import functions.readabilityFunctions as rf
sys.path.append("./pmidcite/src")
from pmidcite.icite.downloader import get_downloader


def split_searchresults(numSplit, journal, dataFolderName):
    '''
    Splits large searchresults file into smaller subsets for easier processing.
    Function parameters:
    - numSplit: number of subsets to divide the searchresults into
    - journalName: name of journal
    - dataFolderName: name of folder where journal data is stored
    ''' 
    searchresults_path = '%s/abstracts/%s[journal]/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % (dataFolderName, journal)
    f = open(searchresults_path)
    searchresults = json.load(f)
    searchTerms = list(searchresults.keys())
    
    numResults = len(searchresults[searchTerms[0]].keys()) 
    subsetSize = numResults // numSplit

    for i in range(1, numSplit+1):
        start = subsetSize * (i-1)
        if i == numSplit:
            end = numResults
        else: 
            end = subsetSize * i

        subset = {}
        for search in searchTerms: 
            subsection = dict(list(searchresults[search].items())[start:end])
            subset[search] = subsection
            print("split %d (%s): %d items" % (i, search, len(subsection.keys())))

        filepath = searchresults_path + "_split" + str(i) + ".json"        
        with open(filepath, "w") as outfile:
            json.dump(subset, outfile)

def get_split_readability(searchresults_path, indices, outputDataFileName):
    readability_path = 'Data analysis/readabilityTemp.json'
    rf.analyze(path = searchresults_path,\
            spath = readability_path, \
            textType = 'abstracttext', \
            columnList = {'journal_title','articleID','pmid','pubdate_year'}, \
            doPreprocessing = 1)
    readability = open(readability_path)
    readabilityData = json.load(readability)

    outputData = pd.read_csv(outputDataFileName, index_col=['journal_ID', 'article_ID'])

    for index in indices: 
        outputData.loc[index, 'fre'] = readabilityData['flesch'][str(index[1])]
        outputData.loc[index, 'ndc'] = readabilityData['NDC'][str(index[1])]
        outputData.loc[index, 'ndc_perc_difficult'] = readabilityData['PercDiffWord'][str(index[1])]
        outputData.loc[index, 'sentence_count'] = readabilityData['sentenceCount'][str(index[1])]
        outputData.loc[index, 'word_count'] = readabilityData['wordCount'][str(index[1])]
    outputData.to_csv(outputDataFileName, index=True)
    readability.close()
    os.remove(readability_path)


def get_split_citations(indices, outputDataFileName):
    outputData = pd.read_csv(outputDataFileName, index_col=['journal_ID', 'article_ID'])
    selectedData = outputData.loc[indices]

    dnldr = get_downloader() # use pmidcite for citation counts
    citation_counts = {}

    pmids = selectedData['pmid'].astype('int64').tolist()
    nih_entries = dnldr.get_icites(pmids)
    for e in nih_entries:
        citation_counts[e.dct["pmid"]] = e.dct["citation_count"]
    
    for index in indices:
        pmid = int(outputData.loc[index]['pmid'])
        pubdate_year = outputData.loc[index]['pubdate_year']
        outputData.loc[index, 'citation_count'] = citation_counts[pmid] 
        outputData.loc[index, 'citation_count_per_year'] = citation_counts[pmid] / (date.today().year - pubdate_year)  
    outputData.to_csv(outputDataFileName, index=True)


def get_split_final_data_csv(numSplits, journalID, journal, outputDataFileName, dataFolderName):
    outputData = pd.read_csv(outputDataFileName, index_col=['journal_ID', 'article_ID'])
    selectedData = outputData.loc[outputData.index.get_level_values(0) == journalID]

    for splitNo in range(1, numSplits+1):
        print("> analyzing split %d ..." % splitNo)
        searchresults_path = '%s/abstracts/%s[journal]/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults_split%d.json' % (dataFolderName, journal, splitNo)
        f = open(searchresults_path)
        searchresults = json.load(f) 

        splitArticleIDs = list(map(int, list(searchresults['index'].keys())))
        indices = [index for index in selectedData.index.values if (index[1] in splitArticleIDs)]
        print(len(indices), "results for", len(splitArticleIDs), "article IDs in split") # TODO DEL

        # print("GETTING CITATIONS...")
        # get_split_citations(indices, outputDataFileName)
        
        # TODO
        print("CALCULATING READABILITY...")
        get_split_readability(searchresults_path, indices, outputDataFileName)

    print("ANALYSIS COMPLETED!\t", journalID, journal)
    


def main():
    journalID = 3
    journal = 'proc_natl_acad_sci_u_s_a'
    numSplit = 4
    '''
    Run init_final_data_csv and remove_repeated_articles first
    '''
    # split_searchresults(numSplit=numSplit, \
    #         journalName = journal, \
    #         dataFolderName = 'topJournalData')
    # split 1: 0 to 37143, split 2: 37143 to 74287, split 3: 74287 to 111430, split 4: 111430 to 148574
    """
    split 1 (index): 37143 items
    split 1 (articleID): 37143 items
    split 1 (abstracttext): 37143 items
    split 1 (articletitle): 37143 items
    split 1 (doi): 37143 items
    split 1 (journal_title): 37143 items
    split 1 (keyword): 37143 items
    split 1 (language): 37143 items
    split 1 (pmid): 37143 items
    split 1 (pubdate_year): 37143 items
    split 2 (index): 37143 items
    split 2 (articleID): 37143 items
    split 2 (abstracttext): 37143 items
    split 2 (articletitle): 37143 items
    split 2 (doi): 37143 items
    split 2 (journal_title): 37143 items
    split 2 (keyword): 37143 items
    split 2 (language): 37143 items
    split 2 (pmid): 37143 items
    split 2 (pubdate_year): 37143 items
    split 3 (index): 37143 items
    split 3 (articleID): 37143 items
    split 3 (abstracttext): 37143 items
    split 3 (articletitle): 37143 items
    split 3 (doi): 37143 items
    split 3 (journal_title): 37143 items
    split 3 (keyword): 37143 items
    split 3 (language): 37143 items
    split 3 (pmid): 37143 items
    split 3 (pubdate_year): 37143 items
    split 4 (index): 37145 items
    split 4 (articleID): 37145 items
    split 4 (abstracttext): 37145 items
    split 4 (articletitle): 37145 items
    split 4 (doi): 37145 items
    split 4 (journal_title): 37145 items
    split 4 (keyword): 37145 items
    split 4 (language): 37145 items
    split 4 (pmid): 37145 items
    split 4 (pubdate_year): 37145 items
    """
    get_split_final_data_csv(numSplits = numSplit, \
                        journalID = journalID, journal = journal, \
                        outputDataFileName = 'Data analysis/top_journals_articles.csv', \
                        # outputJournalFileName = 'Data analysis/top_journals_info.csv', \
                        # journalListFileName = 'Journal selection/topJournals.csv', \
                        dataFolderName = 'topJournalData')
    """
    # line 98013 in article data
    split 1: 22,587 results / 37,143 article IDs 
    split 2: 31,318 results / 37,143 article IDs 
    split 3: 35,788 results / 37,143 article IDs 
    split 4: 26,105 results / 37,145 article IDs 
    total: 115,798 final article count / 14,8574 total downloaded articles
    """      

main()