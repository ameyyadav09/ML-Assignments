import pandas as pd
import numpy as np

"""
input:
converts the columns to object
df: pandas dataframe
columns: list of columns
output: new dataframe after typecasting selected columns to object
"""
def to_object(df, columns):
    # df[columns] = df[columns].apply(str)
    df[columns] = df[columns].astype(np.object)
    return df

"""
input:
df: pandas dataframe
columns: list of columns
output: new  dataframe after typecasting selected columns to int
"""
def to_int(df, columns):
    df[columns] = df[columns].apply(pd.to_numeric)
    return df

"""
input:
df: Pandas DataFrame
columns: list of columns
format: string, format to parse the date in eah cell
Ex: "%Y/%m/%d"
yearfirst(optional): If True parses dates with the year first, eg 10/11/12 is parsed as 2010-11-12.
output:
new  dataframe after typecasting selected columns to date
"""
def to_date(df, columns, yearfirst=False, forma="%d%m%Y", **kwargs):
    df[columns] = df[columns].apply(pd.to_datetime, format=forma, yearfirst=yearfirst, **kwargs)
    # df[columns] = pd.to_datetime(df[columns], format=forma, yearfirst=yearfirst)
    return df

# Test Script
# df = pd.DataFrame({'num':[15092017, 10062016,9051993]})
# print(df.dtypes)
# print(to_date(df, ['num'], True))
