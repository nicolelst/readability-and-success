import pandas as pd
import researchpy as rp
import statsmodels.api as sm
from statsmodels.formula.api import ols
from datetime import datetime

def anova_table(aov):
    aov['mean_sq'] = aov[:]['sum_sq']/aov[:]['df']

    aov['eta_sq'] = aov[:-1]['sum_sq']/sum(aov['sum_sq'])

    aov['omega_sq'] = (aov[:-1]['sum_sq']-(aov[:-1]['df']*aov['mean_sq'][-1]))/(sum(aov['sum_sq'])+aov['mean_sq'][-1])

    cols = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
    aov = aov[cols]
    return aov


def anova_by_quintiles(dataFile, factor, response, outputFile):
    # https://www.pythonfordatascience.org/anova-python/

    # load dataset
    df = pd.read_csv(dataFile)

    # divide data into quintiles by factor values 
    df.sort_values(by = factor, inplace = True)
    df['quintile_rank']= pd.qcut(df[factor],
                             q = 5, labels = False)

    # ANOVA in response variable for each quintile of factor values 
    formula = '%s ~ C(%s)' % (response, 'quintile_rank')
    model = ols(formula, data=df).fit()
    aov_table = sm.stats.anova_lm(model, typ=2)

    with open(outputFile, 'a') as f:
        print("\n" + "=" * 40, file=f)
        print("Data:", dataFile, file=f)
        print("Factor:", factor, file=f)
        print("Response variable:", response, file=f)
        print("", file=f)
        print(rp.summary_cont(df[response]), file=f)
        print("", file=f)
        print(rp.summary_cont(df[response].groupby(df['quintile_rank'])), file=f)
        print("", file=f)
        print(anova_table(aov_table), file=f)

def main():
    outputFile = 'Data analysis/ANOVA_results_quintiles.txt'

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(outputFile, 'w') as f:
        print("ANOVA RESULTS (last updated: %s)" % dt_string, file=f)
        print("sum_sq: sum of squares for model terms\n" + 
                "df: degrees of freedom for model terms\n" + 
                "mean_sq: sum_sq / df\n"
                "F: F statistic value for significance of adding model terms\n" +
                "PR(>F): p-value for significance of adding model terms\n" + 
                "eta_sq: measure of effect size, proportion of variance associated with each main effect and interaction effect\n" +
                "omega_sq: measure of effect size, estimate of how much variance in the response variables are accounted for by the explanatory variables", 
                file=f)
        

    for dataFile in ['Data analysis/top_journals_articles.csv', 
                    'Data analysis/median_journals_articles.csv']:
        for factor in ['fre', 'ndc', 'pubdate_year', 'sentence_count', 'word_count']:
            anova_by_quintiles(dataFile = dataFile,
                            factor = factor, 
                            response = 'citation_count', 
                            outputFile = outputFile)

main()