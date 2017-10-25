import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype
from scipy.stats import boxcox
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

"""
Below method takes a pandas dataframe and filters the numeric features
applies boxcox transformation and scales the data and perform PCA and returns
a new dataframe with newly obtained features
input:
df: pandas dataframe
output: pandas dataframe containing only numeric columns after performing
PCA on the given dataframe
"""
def pca_func(df):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    is_number = [*map(lambda x:np.issubdtype(df[x], np.number), df.columns)]
    rdf = df.loc[:,is_number].copy()
    for column in rdf.columns:
        rdf[column], _ = boxcox(rdf[column])
    rdf = StandardScaler().fit(rdf).transform(rdf)
    pca = PCA()
    return pd.DataFrame(pca.fit_transform(rdf))

# Test Script
# df = pd.DataFrame({'a':[1,2,3],'b':[2,3,4],'c':['a','b','c']})
# print(pca_func(df))
