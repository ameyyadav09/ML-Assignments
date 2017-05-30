from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import numpy as np

def scrape_companies():
	response = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
	soup = BeautifulSoup(response.text, 'html.parser')
	table = soup.findAll('table', {'class':'wikitable'})[0]
	tickers = []
	for row in table.findAll('tr')[1:]:
		ticker = row.findAll('td')[0].text
		tickers.append(ticker)
	with open("sp500.pickle", "wb") as fp:
		pickle.dump(tickers, fp)
	return tickers
# print scrape_companies()

def get_data_from_yahoo(reload_sp500 = False):
	if reload_sp500:
		tickers = scrape_companies()
	else:
		with open("sp500.pickle", 'rb') as fp:
			tickers = pickle.load(fp)
	if not os.path.exists('stock_dfs'):
		os.mkdir('stock_dfs')

	start = dt.datetime(2000,1,1)
	end = dt.datetime(2016,12,31)
	for ticker in tickers:
		try:
			print ticker
			if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
				df = web.DataReader(ticker, 'google', start, end)
				df.to_csv('stock_dfs/{}.csv'.format(ticker))
			else:
				print "Already have {}".format(ticker)
		except Exception as e:
			continue
# get_data_from_yahoo()

def compile_data():
	with open("sp500.pickle", "rb") as fp:
		tickers = pickle.load(fp)
	main_df = pd.DataFrame()
	for count, ticker in enumerate(tickers):
		try:
			df = pd.read_csv("stock_dfs/{}.csv".format(ticker))
			df.set_index('Date', inplace = True)
			df.rename (columns = {'Close' : ticker}, inplace = True)
			df.drop(['Volume','Open', 'High','Low'], 1, inplace = True)
			if main_df.empty:
				main_df = df
			else:
				main_df = main_df.join(df, how = 'outer')

			if count %10 == 0:
				print count
		except Exception:
			continue

	print main_df.head()
	main_df.to_csv('sp500_joined_closes.csv')
# compile_data()

def visualize_data():
	df = pd.read_csv('sp500_joined_closes.csv')
	df_corr = df.corr()
	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	
	headmap = ax.pcolor(df_corr, cmap = plt.cm.RdYlGn)
	fig.colorbar(headmap)

	ax.set_xticks(np.arange(df.shape[0]+0.5), minor = False)
	ax.set_yticks(np.arange(df.shape[1]+0.5), minor = False)

	#inverts the axis
	ax.invert_yaxis()

	#xaxis labels appear on top of graph but not at bottom
	ax.xaxis.tick_top()

	#both are actually similar
	column_labels = df_corr.columns
	row_labels = df_corr.index

	#assigning axis labels
	ax.set_xticklabels(column_labels)
	ax.set_yticklabels(row_labels)

	plt.xticks(rotation = 90)
	headmap.set_clim(-1, 1)
	plt.tight_layout()
	plt.show()
visualize_data()