import pandas as pd
import numpy as np

def cat_mode(ser):
    ser = ser.apply(str)
    values, freqs = np.unique(ser, return_counts = True)
    return values[np.argmax(freqs)]

def imputation(df):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    for column in df.columns:
        if df[column].dtype == "int64" or df[column].dtype =="float64":
            df[column].fillna(df[column].mean(), inplace = True)
        elif df[column].dtype == "object" or df[column].dtype == "bool":
            df[column].fillna(cat_mode(df[column]), inplace = True)
    return df

#TestScript
# df = pd.DataFrame({'col':['ball',np.nan,'ball','call','doll','roll']})
# df.loc[df.index %2 == 0, :] = np.nan
# print(imputation(df))
