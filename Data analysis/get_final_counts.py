import pandas as pd


def main(): 
    scimago_df = pd.read_csv("Journal selection\\scimagojr 2020.csv", sep = ";")
    print("Scimago journal count:", scimago_df.shape[0]) # 32952, 3363 top 10%, 3844 median 10%
    print()

    pubmed_df = pd.read_csv("Journal selection\\PubmedJournals.csv")
    print("Pubmed journal count:", pubmed_df.shape[0]) # 34899
    print()
    
    final_df = pd.read_csv("Journal selection\\FinalJournals.csv")
    print("Final journal count:", final_df.shape[0]) # 1335
    print()

    top_df = pd.read_csv("Data analysis\\top_journals_info.csv")
    count = top_df.shape[0]
    print("Top journal count (>90%):", count) # 135
    # print("Top H-index range (>90%):", topRange) # 127 - 1226, vs 82 - 1226
    min_journal = top_df['journal_full_title'].iat[count-1]
    print("Min H index:", final_df.loc[final_df['Title'] == min_journal, 'H index'].values)
    max_journal = top_df['journal_full_title'].iat[0]
    print("Max H index:", final_df.loc[final_df['Title'] == max_journal, 'H index'].values)
    print("Total downloaded articles:", top_df['downloaded_articles'].sum())
    print("Articles with missing abstracts:", top_df['missing_abstracts'].sum())
    print("Non-English articles:", top_df['non_english_articles'].sum())
    print("Usable articles:", top_df['usable_articles'].sum()) 
    print("Final article count after removing duplicates:", top_df['final_article_count'].sum())
    print()

    median_df = pd.read_csv("Data analysis\\median_journals_info.csv")
    count = median_df.shape[0]
    print("Median journal count (45-55%):", count) # 159
    # print("Median H-index range (45-55%):", medianRange) # 26 - 36, vs 12 - 18
    min_journal = median_df['journal_full_title'].iat[count-1]
    print("Min H index:", final_df.loc[final_df['Title'] == min_journal, 'H index'].values)
    max_journal = median_df['journal_full_title'].iat[0]
    print("Max H index:", final_df.loc[final_df['Title'] == max_journal, 'H index'].values)
    print("Total downloaded articles:", median_df['downloaded_articles'].sum())
    print("Articles with missing abstracts:", median_df['missing_abstracts'].sum())
    print("Non-English articles:", median_df['non_english_articles'].sum())
    print("Usable articles:", median_df['usable_articles'].sum()) 
    print("Final article count after removing duplicates:", median_df['final_article_count'].sum())
    print()


main()

"""
Scimago journal count: 32952

Pubmed journal count: 34899

Final journal count: 1335

Top journal count (>90%): 135
Min H index: [127]
Max H index: [1226]
Total downloaded articles: 2184583
Articles with missing abstracts: 903898
Non-English articles: 1061
Usable articles: 1279624
Final article count after removing duplicates: 1253545.0

Median journal count (45-55%): 159
Min H index: [26]
Max H index: [179  35]
Total downloaded articles: 367203
Articles with missing abstracts: 219036
Non-English articles: 74625
Usable articles: 73542
Final article count after removing duplicates: 71422.0
"""