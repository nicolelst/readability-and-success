import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sympy import true


df = pd.read_csv("PRELIM_DATA.csv",sep=",",header=0)
#df.columns = ["index", "pmid", "citation_count", "fre", "ndc"]

cols = ["fre","ndc","ndc_perc_difficult","citation_count"]
df[cols] = df[cols].replace({0:np.nan})

for col in cols + ["pubdate_year", "years_since_pub"]:
    sns.displot(df, x=col, kind="kde")
    plt.savefig('kde_%s.png' % col)

sns.pairplot(df[['journal','pubdate_year', 'fre', 'ndc', 'ndc_perc_difficult']], dropna=true, hue='journal')
plt.savefig('pairplot_read_pubyear_journalhue.png')
