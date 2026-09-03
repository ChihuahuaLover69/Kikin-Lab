import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def impute_missing(data_cruda, strategy='mean', columns=None):
    
    if columns:
    	data_cruda = data_cruda[columns]
    data = data_cruda.select_dtypes(include="number")
    if strategy == "mean":
        count_dictionary = {}
        dictionary = {}
        
        for k in data.index:
            for c,i in data.loc[k].items():
                if pd.notna(i):
                    dictionary[c]=dictionary.get(c,0) + i
                    count_dictionary[c]= count_dictionary.get(c,0)+1
        replacement = {}
        for i in count_dictionary.keys():
            replacement[i] = np.floor(dictionary[i]/count_dictionary[i])
    elif strategy == "median":
        replacement={}
        for i in data.columns:
            
            sorted_data = data[i].dropna()
            sorted_data = sorted_data.sort_values()
            replacement[i]=sorted_data[sorted_data.index[-1]//2]
    elif strategy == "mode":
        valuecounts =data.dropna()
        replacement={}
        for i in valuecounts.columns:
            replacement[i]=valuecounts[i].value_counts().idxmax()
        
    return data.fillna(replacement)
    
def detect_outliers(data, method='iqr', threshold=1.5):
    solution = {}
    data = data.select_dtypes(include="number")
    if method == "iqr":
        for i in data.columns:
            lower = np.percentile(data[i], 25)
            upper = np.percentile(data[i], 75)
            iqr = upper - lower
        
            lower = lower - (threshold * iqr)
            upper = upper + (threshold * iqr)
            solution[i]=(data[i] >= upper) | (data[i] <= lower)
    elif method == "zscore":
        
        count_dictionary = {}
        dictionary = {}
        means={}
        
        for k in data.index:
            for c,i in data.loc[k].items():
                if pd.notna(i):
                    dictionary[c]=dictionary.get(c,0) + i
                    count_dictionary[c]= count_dictionary.get(c,0)+1
        stds={}
        
        for z in dictionary.keys():
            
            means[z]=dictionary[z]/count_dictionary[z]
            stds[z]=sum((data[z].dropna() - means[z])**2/count_dictionary[z])
            
            if stds[z] != 0:
                solution[z] = threshold<abs((data[z]-means[z])/stds[z])
            else:
                solution[z] = data[z][1 == 2]
    return pd.DataFrame(solution)
    
def handle_outliers(data, method='iqr',action="trim", threshold=1.5):
    solution = {}
    data = data.select_dtypes(include="number")
    if method == "iqr":
        for i in data.columns:
            lower = np.percentile(data[i], 25)
            upper = np.percentile(data[i], 75)
            iqr = upper - lower
        
            lower = lower - (threshold * iqr)
            upper = upper + (threshold * iqr)
            solution[i]=(data[i] >= upper) | (data[i] <= lower)
    elif method == "zscore":
        
        count_dictionary = {}
        dictionary = {}
        means={}
        
        for k in data.index:
            for c,i in data.loc[k].items():
                if pd.notna(i):
                    dictionary[c]=dictionary.get(c,0) + i
                    count_dictionary[c]= count_dictionary.get(c,0)+1
        stds={}
        
        for z in dictionary.keys():
            
            means[z]=dictionary[z]/count_dictionary[z]
            stds[z]=sum((data[z].dropna() - means[z])**2/count_dictionary[z])
            
            if stds[z] != 0:
                solution[z] = threshold<abs((data[z]-means[z])/stds[z])
            else:
                solution[z] = data[z][1 == 2]
    outliners = pd.DataFrame(solution)
    if action == "trim":
        for c in outliners.index:
            if outliners.loc[c].any():
                data.drop(c, inplace=True)
        data.reset_index(drop=True,inplace=True)
    else:
        replacements={}
        for i in data.columns:
            lower = np.percentile(data[i], 25)
            upper = np.percentile(data[i], 75)
            iqr = upper - lower
        
            lower = lower - (threshold * iqr)
            upper = upper + (threshold * iqr)
            replacements[i] = (lower,upper)
        for column in data.columns:
            lower = replacements[column][0]
            upper = replacements[column][1]

            data[column] = data[column].clip(lower=lower,upper=upper)
        
    return data



def plot_missing(data):
    count_dictionary = {}
    
    for k in data.index:
        for c,i in data.loc[k].items():
            if not pd.notna(i):
                count_dictionary[c]= count_dictionary.get(c,0)+1
    sns.barplot(
    x=count_dictionary.keys(),
    y=count_dictionary.values())
    
    plt.xlabel("Columna")
    plt.ylabel("n de valores faltantes")
    plt.xticks(rotation=45, ha="right")
    
    plt.tight_layout()
    plt.show()
plot_missing(df)
