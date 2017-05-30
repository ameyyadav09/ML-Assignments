from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import pandas_datareader as web
from bs4 import BeautifulSoup
import requests
import pickle

def process_data_for_labels(ticker):
	hm_days = 7
	df = pd.read_csv('sp500_joined_closes.csv', index_col = 0)
	tickers = df.columns.values.tolist()
	df.fillna(0, inplace = True)

	for i in range(1, hm_days+1):
		df['{}_{}d'.format(ticker, i)] = ((df[ticker].shift(-i) - df[ticker])/df[ticker])*100
	df.fillna(0, inplace = True)
	return tickers,df
# print process_data_for_labels("XOM").head()

def buy_sell_hold(*args):
	cols = [c for c in args]
	requirement = 2
	for col in cols:
		if col > requirement:
			return 1
		elif col < -requirement:
			return -1
	return 0

def extract_featuresets(ticker):
	tickers, df = process_data_for_labels(ticker)
	df['{}_target'.format(ticker)] = list(map(buy_sell_hold, *[df['{}_{}d'.format(ticker, j)] for j in range(1, 8)]))

	vals = df['{}_target'.format(ticker)].map(str)
	print 'Data Spread:', Counter(vals)
	df.fillna(0, inplace = True)
	df = df.replace([np.inf, -np.inf], np.nan)
	df.dropna(inplace = True)

	df_vals = df[[tticker for tticker in tickers]].pct_change()
	df_vals = df_vals.replace([np.inf, -np.inf], 0)
	df_vals.dropna(inplace = True)

	X = df_vals.values
	y =  df['{}_target'.format(ticker)].values

	return X, y, df
X, y, df = extract_featuresets('AAPL')