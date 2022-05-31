# readability-and-success
URECA SCI21062 
The real value of clear language: Investigating readability and success in academic journals

Python interpreter used: 3.8.5

1. Run `Journal selection/selectJournals.py`
    - For the latest version of `scimagojr 2020.csv` from [Scimago Journal Rankings](https://www.scimagojr.com/journalrank.php?order=h&ord=desc)
    - For the latest version of `J_Medline.txt` from first link on [List of Journals cited on Pubmed](https://www.nlm.nih.gov/bsd/serfile_addedinfo.html)

2. Run `readabilityinscience/download_data/download_data.py` 
    - Edit `repo_directory` in line 15
    - Edit `email` in line 17
    - i edited `dataminingfunctions.py` line 351-352, 371, 396, 401, 404
    - i edited `C:\Users\User\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\bs4\builder __init__.py` line 545-550
    - DTD for pubmed xml data found [here](https://dtd.nlm.nih.gov/ncbi/pubmed/out/pubmed_190101.dtd)

3. Run `Data analysis/get_final_data_csv.py` 

4. If the searchresults for a journal is too large to be processed (eg top journal 3), run `Data analysis/get_split_final_data_csv.py` 
    - Edit `journalID`, `journal` to reflect the affected journal in lines 115-116
    - Edit `numSplit` to reflect the number of subsets to divide the searchresults into in line 117

5. Run `Data analysis/plot_data_from_csv.py` 
