import math
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np

def get_pairplot(outputDataFileName, cols, imageName, hue=None):
    df = pd.read_csv(outputDataFileName, sep=",", header=0)
    #df.columns = ["index", "pmid", "citation_count", "fre", "ndc"]

    # df[cols] = df[cols].replace({0:np.nan})
    plot = sns.pairplot(df[cols], dropna=True, hue=hue)
    fig = plot.get_figure()
    fig.savefig(imageName)


def get_histograms(outputDataFileName, cols, discrete, imageNamePrefix = ''):
    if len(cols) != len(discrete):
        print("Error: difference in length of cols and discrete array.")
        return

    df = pd.read_csv(outputDataFileName, sep=",", header=0)
    fig = plt.figure()
    for i in range(len(cols)):
        col = cols[i]
        disc = discrete[i]
        print(imageNamePrefix, col, disc)
        plt.clf()
        plot = sns.histplot(df, x = col, discrete = disc, kde=True)
        fig = plot.get_figure()
        fig.savefig(imageNamePrefix + 'hist_%s.png' % col)


def get_scatterplots(outputDataFileName, x_cols, y_col, imageNamePrefix = ''):
    df = pd.read_csv(outputDataFileName, sep=",", header=0)
    fig = plt.figure()
    for x_col in x_cols:
        print(imageNamePrefix, x_col, y_col)
        plt.clf()
        plot = sns.scatterplot(data=df, x=x_col, y=y_col)
        fig = plot.get_figure()
        fig.savefig(imageNamePrefix + 'scatter_%s_%s.png' % (x_col, y_col))


def get_jointplots(outputDataFileName, x_cols, y_col, imageNamePrefix = ''):
    df = pd.read_csv(outputDataFileName, sep=",", header=0)
    fig = plt.figure()
    for x_col in x_cols:
        print(imageNamePrefix, x_col, y_col)
        plt.clf()
        plot = sns.jointplot(data=df, x=x_col, y=y_col)
        fig = plot.fig
        fig.savefig(imageNamePrefix + 'joint_%s_%s.png' % (x_col, y_col))


def get_correlation_heatmap(outputDataFileName, cols, imageNamePrefix = ''):
    df = pd.read_csv(outputDataFileName, sep=",", header=0)
    corr = df[cols].corr()
    plt.clf()
    plot = sns.heatmap(corr, annot=True, fmt='.1g') #, center=0)
    fig = plot.get_figure()
    fig.savefig(imageNamePrefix + 'correlation.png')

def roundup(num):
    return int(math.ceil(num / 10.0) * 10)
def rounddown(num):
    return int(math.floor(num / 10.0) * 10)


# TODO UGLY, DECADE BINS ARE WRONG
def get_boxplots(outputDataFileName, values, groupby, imageNamePrefix = ''):
    df = pd.read_csv(outputDataFileName, sep=",", header=0)
    df.dropna(axis=0, subset=[values, groupby])
    # plot = sns.boxplot(data=df, x=groupby, y=values, fliersize=2)
    # dlong = df.melt(var_name=groupby, value_name=values)
    # dlong['bins'] = pd.cut(dlong[values], 10)
    df.sort_values(groupby, inplace=True)
    numBins = (roundup(df[groupby].max()) - rounddown(df[groupby].min())) // 10
    print(df[groupby].min(), df[groupby].max(), numBins)
    df['bin'] = pd.cut(df[groupby], numBins, include_lowest = True)
    plot = sns.boxplot(data=df, x='bin', y=values)
    plot.set_xticklabels(plot.get_xticklabels(),rotation = 20)
    fig = plot.get_figure()
    fig.savefig(imageNamePrefix + 'boxplot_%s_by_%s.png' % (values, groupby))


def main():
    try: 
        os.mkdir('Figures')
    except: 
        pass

    
    # cols = ['journal_ID','pubdate_year','citation_count','citation_count_per_year','fre','ndc','ndc_perc_difficult','sentence_count','word_count']
    # get_pairplot('Data analysis/median_journals_articles.csv', cols, 'Figures/median_pairplot_all.png', hue='journal_ID')
    # get_pairplot('Data analysis/top_journals_articles.csv', cols, 'Figures/top_pairplot_all.png', hue='journal_ID')

    # cols = ['pubdate_year','citation_count','fre','ndc','ndc_perc_difficult']
    # get_pairplot('Data analysis/median_journals_articles.csv', cols, 'Figures/median_pairplot.png')
    # get_pairplot('Data analysis/top_journals_articles.csv', cols, 'Figures/top_pairplot.png')
    
    cols = ['pubdate_year','citation_count','fre','ndc','ndc_perc_difficult', 'sentence_count', 'word_count']
    # discrete = [True,True,False,False,False,True,True]
    # get_histograms('Data analysis/median_journals_articles.csv', cols, discrete, 'Figures/median_')
    # get_histograms('Data analysis/top_journals_articles.csv', cols, discrete, 'Figures/top_')
    
    # x_cols = ['fre','ndc','ndc_perc_difficult', 'sentence_count', 'word_count']
    # y_col = 'citation_count'
    # get_scatterplots('Data analysis/median_journals_articles.csv', \
    #                 x_cols, y_col, \
    #                 'Figures/median_')
    # get_scatterplots('Data analysis/top_journals_articles.csv', \
    #                 x_cols, y_col, \
    #                 'Figures/top_')

    # get_jointplots('Data analysis/median_journals_articles.csv', \
    #                 x_cols, y_col, \
    #                 'Figures/median_')
    # get_jointplots('Data analysis/top_journals_articles.csv', \
    #                 x_cols, y_col, \
    #                 'Figures/top_')

    get_correlation_heatmap('Data analysis/median_journals_articles.csv', cols, 'Figures/median_')
    get_correlation_heatmap('Data analysis/top_journals_articles.csv', cols, 'Figures/top_')

    # TODO UGLY
    # get_boxplots(outputDataFileName='Data analysis/median_journals_articles.csv', \
    #                 values='citation_count', \
    #                 groupby='pubdate_year', \
    #                 imageNamePrefix='Figures/median_')
    # get_boxplots(outputDataFileName='Data analysis/top_journals_articles.csv', \
    #                 values='citation_count', \
    #                 groupby='pubdate_year', \
    #                 imageNamePrefix='Figures/top_')

    # TODO journal stats: get avg readability for each journal ?


main()