import csv
import json
from numpy import nan
import sys

sys.path.append("C:\\Users\\User\\Desktop\\URECA CODE\\readabilityinscience")
import readabilityinscience.functions.readabilityFunctions as rf

# sys.path.append("C:\\Users\\User\\Desktop\\URECA CODE\\pmidcite\\src")
# from pmidcite.icite.downloader import get_downloader


def getReadability(text): 
    # TODO: ADD PREPROCESSING STEPS, use analyze function

    #Calculate the length of each word, sentence and syllable count
    wc, sc, sylCount, remainingText, wordLen = rf.countWordsSentSyl(text,ignoreSingleSentences=False)
    remainingText = ' '.join(remainingText)
    remainingText=remainingText.lower()
    fre = ndc = ndc_perc_difficult = nan
    #Only carry on if sentance count is greater than 0
    if wc>0 and sc>0:
        #Calc Flesh and NDC
        fre = rf.FRE(wc,sc,sylCount)
        ndc, ndc_perc_difficult, difficult_list = rf.NDC(remainingText, wc, sc)
    return (fre, ndc, ndc_perc_difficult)


def main(): 
    header = ['journal', 'index', 'pmid', 'pubdate_year', 'years_since_pub', 'citation_count', 'fre', 'ndc', 'ndc_perc_difficult']
    # C:\\Users\\User\\Desktop\\readabilityinscience\\
    journals = ['ca-cancer_j_clin[journal]', 'chem_rev[journal]', 'lancet[journal]', 'nat_biotechnol[journal]', 'new_engl_j_med[journal]']
    #journals = ['ca-cancer_j_clin[journal]']

    dataFile = open('PRELIM_DATA.csv', 'w', encoding='UTF8', newline='')
    writer = csv.writer(dataFile)
    writer.writerow(header)

    # dnldr = get_downloader()

    for j in journals:
        f = open('C:\\Users\\User\\Desktop\\URECA CODE\\readabilityinscience\\data\\abstracts\\%s\\id_article\\abstracttext_pubdate_year_pmid_articletitle_journal_title_keyword_doi\\searchresults' % j)
        data = json.load(f)            
        for index in list(data['index'].keys()):
            print(j, index)
            pmid = data['pmid'][index]
            year = data['pubdate_year'][index]
            # citations = dnldr.get_icite(pmid).dct["citation_count"] # takes forever !
            abstractText = data['abstracttext'][index]
            if abstractText != None: 
                fre, ndc, ndc_perc_difficult = getReadability(abstractText)
                if not (fre == ndc == ndc_perc_difficult == nan):
                    line = [j, index, pmid, year, 2022-year, 0, fre, ndc, ndc_perc_difficult]
                    writer.writerow(line)
        f.close()

    dataFile.close()

main()