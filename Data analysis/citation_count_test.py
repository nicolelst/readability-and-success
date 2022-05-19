import csv
import json
import pandas as pd
import sys
sys.path.append("pmidcite\\src")
from pmidcite.icite.downloader import get_downloader

dnldr = get_downloader()

"""Print citation count for list of pmid"""
# pmids = [31461780, 22882545, 20050301]
# # for p in pmids:
# #     entry = dnldr.get_icite(p)
# #     print(entry.dct["pmid"], entry.dct["citation_count"])

# nih_entries = dnldr.get_icites(pmids)
# for e in nih_entries:
#     print(e.dct["pmid"], e.dct["citation_count"])
#     # for key, val in e.dct.items():
#     #     print('{KEY:>27} {VAL}'.format(KEY=key, VAL=val))

"""print citation count for searchresults"""
dataHeader = ['journal_title', 'article_ID', 'pmid', 'pubdate_year', 'language', 'abstract_text', 'citation_count']
dataFile = open('cite_test.csv', 'w', encoding='UTF8', newline='')
dataWriter = csv.writer(dataFile)
dataWriter.writerow(dataHeader) # write header row

journalHeader = ['journal_title', 'downloaded_articles', 'missing_abstracts', 'non_english_articles', 'usable_articles']
journalsFile = open('journals_test.csv', 'w', encoding='UTF8', newline='')
journalsWriter = csv.writer(journalsFile)
journalsWriter.writerow(journalHeader) # write header row

topJournalInfo = pd.read_csv('Journal selection/testJournals.csv')
# topJournals = topJournalInfo.search #['journal_of_the_european_ceramic_society[journal]', 'bulletin_of_the_american_meteorological_society[journal]']
for i in list(range(0, len(topJournalInfo))):
    journal = topJournalInfo.search[i].replace(' ','_').replace('\"','')    
    try: 
        searchResults = open('topJournalData/abstracts/%s/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % journal)
    except: 
        journal = '"%s"[Journal]' % topJournalInfo.journal[i]
        searchResults = open('topJournalData/abstracts/%s/id_article/language_abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi/searchresults' % journal)
    print(topJournalInfo.journalID[i], journal)
    
    data = json.load(searchResults)        

    pmids = list(data['pmid'].values())
    nih_entries = dnldr.get_icites(pmids)
    citation_counts = {}
    for e in nih_entries:
        citation_counts[e.dct["pmid"]] = e.dct["citation_count"]

    num_missing_abstract = 0
    num_non_eng = 0
    for index in list(data['articleID'].keys()):
        abstract_text = data['abstracttext'][index]
        if abstract_text == None or abstract_text == "": # ignore articles with no abstract
            num_missing_abstract += 1
            continue

        language = data['language'][index]
        if language != 'eng': # ignore non-english articles
            num_non_eng += 1
            continue

        journal_title = data['journal_title'][index]
        article_ID = index #data['articleID'][index]
        pmid = data['pmid'][index]
        pubdate_year = data['pubdate_year'][index]
        # fre, ndc, ndc_perc_difficult = getReadability(abstractText)
        # if not (fre == ndc == ndc_perc_difficult == nan):
        #     line = [j, index, pmid, year, 2022-year, 0, fre, ndc, ndc_perc_difficult]
        #     writer.writerow(line)
        citation_count = citation_counts[pmid] 
        line = [journal_title, article_ID, pmid, pubdate_year, language, abstract_text, citation_count]
        dataWriter.writerow(line)
    searchResults.close()

    line = [journal.rstrip("[journal]"), len(pmids), num_missing_abstract, num_non_eng, len(pmids) - num_missing_abstract - num_non_eng]
    journalsWriter.writerow(line)

dataFile.close()
journalsFile.close()