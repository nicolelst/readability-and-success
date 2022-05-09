#%%
#md

"""
This script downloads the dataset use in the analysis.

__It requires 2 inputs to be specified__

repo_directory and email (see first cell block).
"""

#%%

# Where is the main directory of the repo
repo_directory = 'C:\\Users\\User\\Desktop\\readability-and-success' 
# Pubmed requires you to identify with an email addreesss
email = 'nicolelim2608@gmail.com'

#%%
import os
os.chdir(repo_directory)

import shutil

import numpy as np
import pandas as pd
# import sys
# sys.path.append(repo_directory)
import readabilityinscience.functions.dataminingfunctions as dmf
import readabilityinscience.functions.readabilityFunctions as rf



#%%

#Load journal info
# journalInfo=pd.read_csv('./JournalSelection/JournalSelection.csv')
topJournalInfo=pd.read_csv('./Journal selection/topJournals.csv')
medianJournalInfo=pd.read_csv('./Journal selection/medianJournals.csv')


#%%
#md

"""
Specify the search data that you want to get from pubmeddata
"""

#%%

#What to get. "all" saves a txt. Otherwise the xml tags wanted (see https://www.nlm.nih.gov/bsd/licensee/elements_alphabetical.html). Seperated by a comma
#"Trees" are possible to specify column you want. (e.g. <year> occurs) in several
#places so pubate_year takes the <year> tag in <pubdate>
dataOfInterest = 'abstracttext,pubdate_year,pmid,articletitle,journal_title,keyword,doi'
#If dataframe, what is the index column (usally article or author)
dfId = 'article'
topJournalNums = list(range(0, len(topJournalInfo)))
medianJournalNums = list(range(0, len(medianJournalInfo)))

#%%
#md

"""
Download the data
"""

#%%
folderName = 'topJournalData'
for n in topJournalNums: 
    searchString = topJournalInfo.search[n]
    print(' ---[TOP] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')

    try: 
        numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
    except: 
        print("Error. Retrying...")
        path = os.getcwd() + '/%s/abstracts/' % folderName + searchString 
        path = path.replace(' ','_').replace('\"','')    
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error removing %s : %s" % (path, e.strerror))
        numArticles = -1

    if numArticles == 0: # if search from title fails, try IsoAbbr
        searchString = '"%s"[Journal]' % topJournalInfo.journal[n]
        print(">> Rerunning search:", searchString)
        numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
    
    print('Downloaded ' + str(numArticles) + ' articles')

#%%
folderName = 'medianJournalData'
for n in medianJournalNums:
    searchString = medianJournalInfo.search[n]
    print(' ---[MEDIAN] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')

    try: 
        numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
    except:
        print("Error. Retrying...")
        path = os.getcwd() + '/%s/abstracts/' % folderName + searchString 
        path = path.replace(' ','_').replace('\"','')    
        try:
            shutil.rmtree(path)
        except OSError as e:
            print("Error removing %s : %s" % (path, e.strerror))
        numArticles = -1

    if numArticles in [-1, 0]: # if search from title fails, try IsoAbbr
        searchString = '"%s"[Journal]' % medianJournalInfo.journal[n]
        print(">> Rerunning search:", searchString)
        numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
    
    print('Downloaded ' + str(numArticles) + ' articles')


#%%
#md

"""
Sometimes the pubdate, year tags were missing in articles. The next cell finds those instances and
"""

#%%
folderName = 'topJournalData'
for n in topJournalNums:
    for searchString in [topJournalInfo.search[n], \
                        '"%s"[Journal]' % medianJournalInfo.journal[n]]:
        searchString = searchString.lower()
        mDir = os.getcwd() + '/%s/abstracts/' % folderName+ searchString + '/' + 'id_' + dfId + '/' + dataOfInterest + '/'
        mDir = mDir.replace(' ','_')
        mDir = mDir.replace(',','_')
        mDir = mDir.replace('\"','')
        try: 
            dat=pd.read_json(mDir + 'searchresults')
        except: 
            print("No results for %s. Retrying..." % searchString)
        else:
            break

    dat.sort_index(inplace=True)
    idMissing = [i for i,x in enumerate(dat.pubdate_year) if x == '']
    if len(idMissing)>0:
        #Make a list of strings
        pmidMissing=list(map(str,list(dat.pmid[idMissing])))
        print(' ---[TOP] Finding missing years (' + str(len(pmidMissing)) + ' found): ' + searchString + '(%d)' % n + ' ---')
        missingYears = dmf.get_medlineyear(list(pmidMissing))
        dat['pubdate_year'].loc[idMissing]=missingYears
        dat.to_json(mDir + 'searchresults')

#%%
for n in medianJournalNums:
    searchString = medianJournalInfo.search[n].lower()
    #make path to data (always this, if dataframe)
    mDir = os.getcwd() + '/data/abstracts/' + searchString + '/' + 'id_' + dfId + '/' + dataOfInterest + '/'
    mDir = mDir.replace(' ','_')
    mDir = mDir.replace(',','_')
    mDir = mDir.replace('\"','')
    dat=pd.read_json(mDir + 'searchresults')
    dat.sort_index(inplace=True)
    idMissing = [i for i,x in enumerate(dat.pubdate_year) if x == '']
    if len(idMissing)>0:
        #Make a list of strings
        pmidMissing=list(map(str,list(dat.pmid[idMissing])))
        print(' ---[MEDIAN] Finding missing years (' + str(len(pmidMissing)) + ' found): ' + searchString + '. term: ' + str(n) + ' ---')
        missingYears = dmf.get_medlineyear(list(pmidMissing))
        dat['pubdate_year'].loc[idMissing]=missingYears
        dat.to_json(mDir + 'searchresults')

#%%
#md

"""
For the "nr authors" the author info also has to be download.
"""

#%%
#What to get. "all" saves a txt. Otherwise the xml tags wanted (see https://www.nlm.nih.gov/bsd/licensee/elements_alphabetical.html). Seperated by a comma
#"Trees" are possible to specify column you want. (e.g. <year> occurs) in several
#places so pubate_year takes the <year> tag in <pubdate>
dataOfInterest = 'forename,lastname,affiliation'
#If dataframe, what is the index column (usally article or author)
dfId = 'author'

#%%
for n in topJournalNums:
    #Parameters needed (if left blank, get_pubmeddata asks for response)
    #What to search pubmed with
    searchString = topJournalInfo.search[n]
    print(' ---[TOP] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')
    #Run get data
    dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore')

#%%
for n in medianJournalNums:
    #Parameters needed (if left blank, get_pubmeddata asks for response)
    #What to search pubmed with
    searchString = medianJournalInfo.search[n]
    print(' ---[MEDIAN] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')
    #Run get data
    dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore')

# %%
