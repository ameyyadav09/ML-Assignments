import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold
def get_nzv_cols(df, threshold = 0.0):
    sel = VarianceThreshold(threshold)
    sel.fit(df)
    nzv_cols = df.columns[sel.get_support()]
    res_dict = {"nzv_cols":nzv_cols}
    zv_cols = df.columns[sel.variances_ <= threshold]
    res_dict['zeroVar']=zv_cols
    return res_dict

#Test script
# X = pd.DataFrame([[0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 1, 1], [0, 1, 0], [0, 1, 1]], columns=['a','b','c'])
# threshold = .8*(1-.8)
# print(get_nzv_cols(X, threshold))
