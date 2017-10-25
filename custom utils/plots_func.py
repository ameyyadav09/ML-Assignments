import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use("ggplot")
"""
input:
df: pandas DataFrame
path: Location where the plots need to be saved
Takes a python DataFrame and plots histograms and bar graphs for numeric
and categorical columns respectively and saves them in the specified path
with their respective column names
"""
def plotter(df, path, show=False):
    assert(isinstance(df, pd.DataFrame))
    for column in df.columns:
        if df[column].dtype != "datetime64[ns]":
            if df[column].dtype == "int64":
                plt.hist(df[column], histtype="step")
                plt.title(column)
            elif df[column].dtype == "object" or df[column].dtype == "bool":
                values, freqs = np.unique(df[column], return_counts = True)
                y_pos = np.arange(values.shape[0])
                plt.bar(y_pos, freqs)
                plt.xticks(y_pos, values)
                plt.title(column)
            plt.savefig(os.path.join(path, "column.png"))
            if show:
                plt.show()

# Test Script
# df = pd.DataFrame([['red',1,True],['blue',2,True],['white',3,False]], columns=['colors','val','flag'])
# plotter(df, "<>", True)
