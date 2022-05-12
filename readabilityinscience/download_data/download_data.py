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
#If dataframe, what is the index column (usally article or author)
dfId = 'article'
topJournalNums = list(range(0, len(topJournalInfo)))
medianJournalNums = list(range(0, len(medianJournalInfo)))

#%%
#md

"""
Download the data
"""

# #%%
# #What to get. "all" saves a txt. Otherwise the xml tags wanted (see https://www.nlm.nih.gov/bsd/licensee/elements_alphabetical.html). Seperated by a comma
# #"Trees" are possible to specify column you want. (e.g. <year> occurs) in several
# #places so pubate_year takes the <year> tag in <pubdate>
# dataOfInterest = 'abstracttext,pubdate_year,pmid,articletitle,journal_title,keyword,doi'
# folderName = 'topJournalData'
# for n in topJournalNums: 
#     searchString = topJournalInfo.search[n]
#     print(' ---[TOP] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')

#     try: 
#         numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
#     except: 
#         print("Error. Retrying...")
#         path = os.getcwd() + '/%s/abstracts/' % folderName + searchString 
#         path = path.replace(' ','_').replace('\"','')    
#         try:
#             shutil.rmtree(path)
#         except OSError as e:
#             print("Error removing %s : %s" % (path, e.strerror))
#         numArticles = -1

#     if numArticles in [-1, 0]: # if search from title fails, try IsoAbbr
#         searchString = '"%s"[Journal]' % topJournalInfo.journal[n]
#         print(">> Rerunning search:", searchString)
#         numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
    
#     print('Downloaded ' + str(numArticles) + ' articles')

# #%%
# folderName = 'medianJournalData'
# for n in medianJournalNums:
#     searchString = medianJournalInfo.search[n]
#     print(' ---[MEDIAN] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')

#     try: 
#         numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
#     except:
#         print("Error. Retrying...")
#         path = os.getcwd() + '/%s/abstracts/' % folderName + searchString 
#         path = path.replace(' ','_').replace('\"','')    
#         try:
#             shutil.rmtree(path)
#         except OSError as e:
#             print("Error removing %s : %s" % (path, e.strerror))
#         numArticles = -1

#     if numArticles in [-1, 0]: # if search from title fails, try IsoAbbr
#         searchString = '"%s"[Journal]' % medianJournalInfo.journal[n]
#         print(">> Rerunning search:", searchString)
#         numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
    
#     print('Downloaded ' + str(numArticles) + ' articles')

#%%
#md
# TODO: remove this section and add language to earlier section
"""
Download the language of each article.
"""

#%%
#with language
dataOfInterest = 'language,abstracttext,pubdate_year,pmid,articletitle,journal_title,keyword,doi'
# dataOfInterest = 'pmid,language'
#If dataframe, what is the index column (usally article or author)
dfId = 'article'

#%%
folderName = 'topJournalData'
# 108 & 109
# 111, 112
# 121, 122
# 70, 71
for n in topJournalNums:
    #Parameters needed (if left blank, get_pubmeddata asks for response)
    #What to search pubmed with
    searchString = topJournalInfo.search[n]
    print(' ---[TOP] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')
    #Run get data
    # dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore')
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

    if numArticles in [0, -1]: # if search from title fails, try IsoAbbr
        searchString = '"%s"[Journal]' % topJournalInfo.journal[n]
        print(">> Rerunning search:", searchString)
        numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
    
    print('Downloaded ' + str(numArticles) + ' articles')



#%%
folderName = 'medianJournalData'
# 9-15, 16
for n in medianJournalNums:
    #Parameters needed (if left blank, get_pubmeddata asks for response)
    #What to search pubmed with
    searchString = medianJournalInfo.search[n]
    print(' ---[MEDIAN] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')
    #Run get data
    # dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore')
    try: 
        numArticles = dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore', folderName)
    except:
        print("Error. Retrying...")
        path = os.getcwd() + '/%s/abstracts/' % folderName + searchString # TODO add data of interest
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
    if n in [71, 108, 111, 122]:
        continue
    for searchString in [topJournalInfo.search[n], \
                        '"%s"[Journal]' % topJournalInfo.journal[n]]:
        searchString = searchString.lower()
        mDir = os.getcwd() + '/%s/abstracts/' % folderName+ searchString + '/' + 'id_' + dfId + '/' + dataOfInterest + '/'
        mDir = mDir.replace(' ','_')
        mDir = mDir.replace(',','_')
        mDir = mDir.replace('\"','')
        try: 
            dat=pd.read_json(mDir + 'searchresults')
        except: 
            print("No results for (n) %s. Retrying..." % mDir)
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
print("Search complete")

#%%
folderName = 'medianJournalData'
for n in [151]: # medianJournalNums:
    if n in list(range(9, 15+1)) + [139]:
        continue
    for searchString in [medianJournalInfo.search[n], \
                        '"%s"[Journal]' % medianJournalInfo.journal[n]]:
        searchString = searchString.lower()
        mDir = os.getcwd() + '/%s/abstracts/' % folderName+ searchString + '/' + 'id_' + dfId + '/' + dataOfInterest + '/'
        mDir = mDir.replace(' ','_')
        mDir = mDir.replace(',','_')
        mDir = mDir.replace('\"','')
        try: 
            dat=pd.read_json(mDir + 'searchresults')
        except: 
            print("No results for (n) %s \nRetrying..." % mDir)
        else:
            break

    dat.sort_index(inplace=True)
    idMissing = [i for i,x in enumerate(dat.pubdate_year) if x == '']
    if len(idMissing)>0:
        #Make a list of strings
        pmidMissing=list(map(str,list(dat.pmid[idMissing])))
        print(' ---[MEDIAN] Finding missing years (' + str(len(pmidMissing)) + ' found): ' + searchString + '(%d)' % n + ' ---')
        missingYears = dmf.get_medlineyear(list(pmidMissing))
        # returns 10000 instead of 27884
        dat['pubdate_year'].loc[idMissing]=missingYears
        dat.to_json(mDir + 'searchresults')
print("Search complete")


# %%
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
folderName = 'topJournalData'
for n in topJournalNums:
    #Parameters needed (if left blank, get_pubmeddata asks for response)
    #What to search pubmed with
    searchString = topJournalInfo.search[n]
    print(' ---[TOP] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')
    #Run get data
    # dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore')
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
    #Parameters needed (if left blank, get_pubmeddata asks for response)
    #What to search pubmed with
    searchString = medianJournalInfo.search[n]
    print(' ---[MEDIAN] Running search: ' + searchString + ' (' + str(n) + ')' + ' ---')
    #Run get data
    # dmf.get_pubmeddata(searchString.lower(), dataOfInterest, dfId, email, 'ignore')
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



# %%
