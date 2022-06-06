from doctest import OutputChecker
import pandas as pd
import researchpy as rp
import scipy.stats as stats
from datetime import datetime

def anova_by_quintiles(dataFile, factor, response, outputFile):
    # https://www.pythonfordatascience.org/anova-python/

    # load dataset
    df = pd.read_csv(dataFile)

    # divide data into quintiles by factor values 
    df.sort_values(by = factor, inplace = True)
    df['quintile_rank']= pd.qcut(df[factor],
                             q = 5, labels = False)

    # ANOVA in response variable for each quintile of factor values 
    F_stat, p_value = stats.f_oneway(df[response][df['quintile_rank'] == 0],
                df[response][df['quintile_rank'] == 1],
                df[response][df['quintile_rank'] == 2],
                df[response][df['quintile_rank'] == 3],
                df[response][df['quintile_rank'] == 4])

    with open(outputFile, 'a') as f:
        print("\n" + "=" * 40, file=f)
        print("Data:", dataFile, file=f)
        print("Factor:", factor, file=f)
        print("Response variable:", response, file=f)
        print("", file=f)
        print(rp.summary_cont(df[response]), file=f)
        print("", file=f)
        print(rp.summary_cont(df[response].groupby(df['quintile_rank'])), file=f)
        print("\nF-statistic:", F_stat, file=f)
        print("p-value:", p_value, file=f)

def main():
    # anova_by_quintiles(dataFile = "https://raw.githubusercontent.com/researchpy/Data-sets/master/difficile.csv",
    #                 factor = 'dose', 
    #                 response = 'libido')

    outputFile = 'Data analysis/ANOVA_results.txt'

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(outputFile, 'w') as f:
        print("ANOVA RESULTS (last updated: %s)" % dt_string, file=f)
        

    for dataFile in ['Data analysis/top_journals_articles.csv', 
                    'Data analysis/median_journals_articles.csv']:
        for factor in ['fre', 'ndc', 'pubdate_year', 'sentence_count', 'word_count']:
            anova_by_quintiles(dataFile = dataFile,
                            factor = factor, 
                            response = 'citation_count', 
                            outputFile = outputFile)

main()