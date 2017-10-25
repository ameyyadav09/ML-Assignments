import numpy as np
import pandas as pd
from scipy.stats import skew, boxcox

"""
Given a Dataframe/Series/numpy ndarray/python list and a threshould value,
this function applies boxcox transformation only to those columns whose
skewness is greaterthan the spicified threshould.
input:
df -> Pandas Dataframe/Series/numpy ndarray/python list
cutoff -> Integer/float
output: returns a pandas DataFrame after applying boxcox transformation
on selected columns of given DataFrame.
"""
def boxcox_(df, cutoff):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    # nums = df.select_dtypes(include= ['int16', 'int32', 'int64', 'float16', 'float32', 'float64'])
    nums = df.select_dtypes(exclude=['object'])
    # nums = df._get_numeric_data()
    res = pd.DataFrame()
    for column in nums.columns:
        temp_skew = skew(nums[column])
        if temp_skew > cutoff:
            res[column], _ = boxcox(nums[column])
        else:
            res[column] = nums[column]
    return res

def boxcox_2(df, cutoff):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    res = pd.DataFrame()
    for column in df.columns:
        if df[column].dtype == np.int64 or df[column].dtype == np.float64:
            if skew(df[column]) > cutoff:
                res[column], _ = boxcox(df[column])
            else:
                res[column] = df[column]
    return res

# print(boxcox_([['a',2],[3,4]], -1))
