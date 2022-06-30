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


def anova_by_threshold(dataFile, factor, response, threshold, outputFile):
    # https://www.pythonfordatascience.org/anova-python/

    # load dataset
    df = pd.read_csv(dataFile)

    # divide data into two groups, based on whether value of response is above the threshold
    df['above_threshold'] = df[response] > threshold
    # df.loc[df['c1'] == 'Value', 'c2'] = 10

    # ANOVA in factor variable for each group
    formula = '%s ~ C(%s)' % (factor, 'above_threshold')
    model = ols(formula, data=df).fit()
    aov_table = sm.stats.anova_lm(model, typ=2)

    with open(outputFile, 'a') as f:
        print("\n" + "=" * 40, file=f)
        print("Data:", dataFile, file=f)
        print("Factor:", factor, file=f)
        print("Response variable:", response, file=f)
        print("Response variable threshold:", threshold, file=f)
        print("", file=f)
        print(rp.summary_cont(df[factor]), file=f)
        print("", file=f)
        print(rp.summary_cont(df[factor].groupby(df['above_threshold'])), file=f)
        print("", file=f)
        print(anova_table(aov_table), file=f)

def main():
    for threshold in [0, 1, 5, 10, 20, 50, 100, 200, 500, 1000]:
        outputFile = 'Data analysis/ANOVA_results_citations_above_%d.txt' % threshold
        
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        with open(outputFile, 'w') as f:
            print("ANOVA RESULTS (last updated: %s)\n" % dt_string, file=f)
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
                anova_by_threshold(dataFile = dataFile,
                    factor = factor, 
                    response = 'citation_count', 
                    threshold = threshold,
                    outputFile = outputFile)

main()