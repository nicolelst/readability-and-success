import pandas as pd

def getJournalsByPercentile(df, column, startPercentile, endPercentile): 
    rows, cols = df.shape
    startValue, endValue = df[column].quantile([startPercentile, endPercentile])
    data = df[df[column].between(startValue, endValue)].reset_index()
    return (startValue, endValue), data


def getPubmedJournalData(): 
    data = {"JrId": [], \
            "JournalTitle": [], \
            "MedAbbr": [], \
            "ISSN (Print)": [], \
            "ISSN (Online)": [], \
            "IsoAbbr": [], \
            "NlmId": [] \
        }
    file = open("Journal selection\\J_Medline.txt", "r")

    while True:
        line = file.readline()
        if not line: # end of file
            break
        elif "-----" in line: # end of entry
            continue
        else: # parse data in entry
            key, value = line.strip().split(":", maxsplit=1) 
            data[key].append(value.strip())
            # if key == "JournalTitle":
            #     print(value.strip())

    file.close()
    df = pd.DataFrame.from_dict(data)
    # df["search"] = df["IsoAbbr"] + "[journal]" # doesnt work, Science (1979) returns 10 results instead of 181,016 
    return df


def selectJournals(): 
    scimago_df = pd.read_csv("Journal selection\\scimagojr 2020.csv", sep = ";")
    # Rank, Sourceid, Title, Type, Issn, SJR, SJR Best Quartile, H index, Total Docs. (2020), Total Docs. (3years), Total Refs., Total Cites (3years), Citable Docs. (3years), Cites / Doc. (2years), Ref. / Doc., Country, Region, Publisher, Coverage, Categories
    pubmed_df = getPubmedJournalData()
    pubmed_df.to_csv("Journal selection\\PubmedJournals.csv", header=True, index=False) 

    data = pd.merge(scimago_df, pubmed_df, left_on="Title", right_on="JournalTitle", how="inner")
    data = data.loc[:, ["Rank", "Title", "IsoAbbr", "H index", "SJR", "Country", "Region", "Coverage"]]
    data["search"] = data.apply(lambda r: r["Title"] + "[Journal]", axis=1)
    data.to_csv("Journal selection\\FinalJournals.csv", header=True, index=False) 
    data.rename(columns = {"IsoAbbr": "journal"}, inplace = True)
    # data["search"] = data.apply(lambda r: "\"%s\"[Journal]" % r["Title"], axis=1) # has the inverted commas
    
    topRange, topJournals = getJournalsByPercentile(data, "H index", 0.9, 1)
    topJournals.loc[:, ["journal", "search"]].to_csv("Journal selection\\topJournals.csv", header=True, index=True, index_label="journalID") 

    medianRange, medianJournals = getJournalsByPercentile(data, "H index", 0.45, 0.55)
    medianJournals.loc[:, ["journal", "search"]].to_csv("Journal selection\\medianJournals.csv", header=True, index=True, index_label="journalID") 

    print("Scimago journal count:", scimago_df.shape[0]) # 32952, 3363 top 10%, 3844 median 10%
    print("Pubmed journal count:", pubmed_df.shape[0]) # 34899
    print("Final journal count:", data.shape[0]) # 1335
    print("Top journal count (>90%):", topJournals.shape[0]) # 135
    print("Top H-index range (>90%):", topRange) # 127 - 1226, vs 82 - 1226
    print("Median journal count (45-55%):", medianJournals.shape[0]) # 159
    print("Median H-index range (45-55%):", medianRange) # 26 - 36, vs 12 - 18


selectJournals()