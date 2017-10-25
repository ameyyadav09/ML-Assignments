import pandas as pd

"""
input:
converts a string type column to pandas Date type and splits it into
three separate columns, Day, Month, Year

df: Pandas DataFrame
col_num: column index which needs to be split
sep:token used for separation in the string

output:
returns dataframe with three new columns nd the actual column droped
"""
def split_date(df, col_num, sep):
    assert(isinstance(df, pd.DataFrame))
    column = pd.DatetimeIndex(df.iloc[:,col_num], format="%Y{}%m{}%d".format(sep,sep))
    df['year'] = column.year
    df['month'] = column.month
    df['day'] = column.day
    df.drop(df.columns[col_num], axis=1, inplace=True)
    return df

def split_date2(column, sep):
    assert(isinstance(column, pd.Series))
    column = pd.DatetimeIndex(column, format="%Y{}%m{}%d".format(sep,sep))
    res = pd.DataFrame()
    res['date'] = column.year
    res['month'] = column.month
    res['day'] = column.day
    return res

# Test Script
# df = pd.DataFrame([["2017-02-23"], ["2017-02-22"]], columns=['date'])
# print (split_date(df, 0, "-"))
#
se = pd.Series(["2017-02-23","2017-02-22"])
print(split_date2(se, "-"))
