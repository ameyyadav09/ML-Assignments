import numpy as np
from scipy.stats import iqr
import matplotlib.pyplot as plt
import pandas as pd
"""
This function detects  outliers based on boxplots distribution  and imputes
outliers using capping method. It caps the values which are below first
quantile into first quantile and above fourth quantile into fourth quantile
input:
df: pandas DataFrame or a numpy array
output:
pandas Dataframe obtained after eliminating outliers
"""
def outlier_rem(df):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    outlier_imputed = pd.DataFrame(columns=df.columns)
    for column in df.columns:
        outlier_values = plt.boxplot(df[column])["fliers"][0].get_data()[1]
        if len(outlier_values) > 0:
            temp_df = df[column]
            qnt = temp_df.quantile([0.25, 0.75]).values
            caps = temp_df.quantile([0.05, 0.95]).values
            H = 1.5 * iqr(temp_df, nan_policy='omit')
            temp_df[temp_df < (qnt[0]-H)] = caps[0]
            temp_df[temp_df > (qnt[1]-H)] = caps[1]
            outlier_imputed[column] = temp_df
        else:
            outlier_imputed[column] = df[column]
    return outlier_imputed

# Test Script
# np.random.seed(0)
# df = pd.DataFrame(np.random.randn(100, 5), columns=list('ABCDE'))
# df.iloc[::10] += np.random.randn() * 2
# print (df.head(10))
# df = outlier_rem(df)
# print (df.head(10))
