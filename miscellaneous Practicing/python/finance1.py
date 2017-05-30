import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

style.use('ggplot')

# start = dt.datetime(2000,1,1)
# end = dt.datetime(2016,12,31)

# #getting dataframe
df = web.DataReader('TSLA', 'google', start, end)
print df.head()
df.to_csv('tsla.csv')

#reading data
df = pd.read_csv('tsla.csv', parse_dates = True, index_col = 0)

# todays price and 100 days prior days price and find average - 100ma
df['100ma'] = df['Close'].rolling(window = 100).mean()
df.dropna(inplace = True)

#creating subplots
ax1 = plt.subplot2grid((5,1), (0,0), rowspan = 4, colspan = 1)
ax2 = plt.subplot2grid((5,1), (4, 0), rowspan = 1, colspan = 1, sharex = ax1)
ax1.plot(df.index, df['Close'])
ax1.plot(df.index, df['100ma'])
ax2.bar(df.index, df['Volume'])
plt.show() 

#ohlc = open high low close
df_ohlc = df['Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

#making the date as a column by resetting the index
df_ohlc.reset_index(inplace = True)
print df_ohlc.head()

# df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
print df_ohlc.head()
ax1 = plt.subplot2grid((5,1), (0,0), rowspan = 4, colspan = 1)
ax2 = plt.subplot2grid((5,1), (4, 0), rowspan = 1, colspan = 1, sharex = ax1)
takes mdates and displays them as beautiful dates
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width = 2, colorup = 'g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()