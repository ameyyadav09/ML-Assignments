import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

"""
Given a Series object CountVectorizer is used to obtain a csr matrix
and then it is converted as a pandas DataFrame and returned
input:
ser:Pandas Series
output:
Pandas DataFrame obtained after vectorizing
"""
def _vectorize(ser):
    column = ser.name
    # initializing countVectorizer
    vectorizer = CountVectorizer()
    # transforming the required feature vector into csr_matrix
    vectorizer.fit(ser)
    cdf = vectorizer.transform(ser)
    #create a dictionary to change the column names
    vals = {val: column+"_"+ val for val in np.unique(ser)}
    # replacing the column names into more redable format
    vals = [column+"_"+val for val in vectorizer.get_feature_names()]
    #converting csr_matrix to pandas DataFrame
    return pd.DataFrame(cdf.todense(), columns=vals)

"""
Given a Pandas DataFrame categorical features are identified and dummy
encoding is performed on each individual feature and resultant DataFrame
is returned
input:
df: Pandas DataFrame
output:
Pandas DataFrame after performing Dummy encoding
"""
def dummy_encoding(df):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    num_df = df.select_dtypes(include=["object"])
    df.drop(num_df.columns, axis = 1, inplace = True)

    for column in num_df.columns:
        temp_df = _vectorize(num_df[column])
        num_df = pd.concat([num_df, temp_df], axis = 1)
        num_df.drop(column, axis = 1, inplace = True)
    df = pd.concat([df, num_df], axis = 1)
    return df

"""
input:
Given a Pandas Dataframe categorical columns are identified and label
encoding is applied on each individual column and resultant dataframe
is returned
df:Pandas DataFrame
output:
Pandas DataFrame after performing
"""
def cat_encoding(df):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    cat_df = df.select_dtypes(include=["object"])
    df.drop(cat_df.columns, axis = 1, inplace = True)

    res_df = pd.DataFrame()
    for column in cat_df.columns:
        uniq_dict = {i:val for val,i in enumerate(np.unique(cat_df[column]))}
        cat_df[column] = cat_df[column].map(uniq_dict)
    df = pd.concat([df, cat_df], axis = 1)
    return df

# Test Script
# df = pd.DataFrame({"a":["sss","bam","lam"],"b":[2,4,3],"c":[1,5,6],"d":["44a","asd","56asf7567"]})
# print(df)
# print(cat_encoding(df))
