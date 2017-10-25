import pandas as pd
from scipy.stats import chi2_contingency, chisquare
import numpy as np
"""
Given two columns, returns their cramer's v coeff
"""
def get_cramers_coeff(x, y, correction = False):
    contingency_matrix = pd.crosstab(np.array(x) , np.array(y))
    chi_coff = chi2_contingency(contingency_matrix, correction)[0]
    return np.sqrt(chi_coff/(x.shape[0]*(min(contingency_matrix.shape)-1)))

"""
input:
cat_df: pandas Dataframe consisting of all the categorical columns
target_val(optional): String, a target column name

output:
1. correlation between all the variables and dependent variable
2. variables combination having multicolinearity(correlation>=0.7)
return a dictionary consisting of cramer's V coeffeicients
"""
def cat_correlation(cat_df, target_val=None):
    assert(isinstance(cat_df, pd.DataFrame))
    columns = cat_df.columns
    cramer_temp = pd.DataFrame()
    res_dict = {}
    for i_col in columns:
        for j_col in columns:
            cramers_coeff = get_cramers_coeff(df[i_col], df[j_col])
            temp_df = pd.DataFrame([[i_col,j_col,cramers_coeff]], columns=['variable1', 'variable2', 'cramers_value'])
            cramer_temp = pd.concat([cramer_temp, temp_df]).reset_index(drop=True)
    cramer = cramer_temp.loc[(cramer_temp['cramers_value'] >= 0.7) & (cramer_temp['cramers_value'] != 1.0)]
    if target_val is not None:
        cramer_dependent = cramer_temp[(cramer_temp['variable1'] == target_val) & (cramer_temp['variable2'] != 'index')]
        res_dict['cramer_dependent'] = cramer_dependent
    res_dict['cramer'] = cramer
    return res_dict

# Testing
# x = ['abb','jab','cab','mab','lab','tab','abb','tab']
# y = ['skul','skul','skul','pul','kul','pul','skul','pul']
# z = ['pet','met','ret','bet','let','set','pot','pet']
# df = pd.DataFrame(np.vstack([x,y,z]).T, columns=['x','y','z']).reset_index()
# print(cat_correlation(df, 'x')['cramer'])
# print(get_cramers_coeff(df['x'], df['x']))
# contingency_matrix = min(pd.crosstab(df['x'], df['y']).shape)
