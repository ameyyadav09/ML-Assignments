import pandas as pd
import numpy as np
data = pd.read_csv("movie.csv")

#checking null values in each column
# print data.isnull().sum()

#checking unique values 
# print data.select_dtypes(include = ['O']).apply(pd.Series.nunique)
data.dropna(inplace = True)

#find the average rank of the 10 most popular movies between 2000-2009 (inclusive)
# temp_df = data[['movie_title', 'title_year', 'imdb_score']]
# print temp_df[temp_df['title_year'].isin(range(2000, 2010) )].sort_values(['imdb_score'], ascending = False).head(10)['imdb_score'].mean()

# find the year in the 1900s when the average rank increased the most, compared to the previous year. (Ignore movies with votes < 1000)
# data = data[data.num_voted_users > 1000]
# temp_df = data[data['title_year'].isin(range(1900, 2001))]
# temp_df = temp_df[['title_year', 'imdb_score']].sort_values(['title_year'], ascending = False)
# s = temp_df['imdb_score'].groupby(temp_df['title_year']).mean()
# year = s.index.get_level_values(0).tolist()
# m = (0,0)
# print len(s)
# for i in range(1, len(s)):
#     if s.iloc[i] > s.iloc[i-1] and s.iloc[i]-s.iloc[i-1] > m[0]:
#         m = (s.iloc[i], year[i])
# print m


#predicting average score per year using Linear Regression
# from sklearn.linear_model import LinearRegression
# from sklearn.cross_validation import train_test_split
# temp_df = data[['title_year', 'imdb_score']].groupby('title_year').mean().reset_index()
# # temp_df.reset_index(inplace = True)
# y_data = temp_df['imdb_score']
# temp_df.drop('imdb_score', axis = 'columns', inplace = True)
# x_tr, x_te, y_tr, y_te = train_test_split(temp_df, y_data)
# lenreg = LinearRegression()
# lenreg.fit(x_tr, y_tr)
# y_pred = lenreg.predict(x_te)
# from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
# print "mean_squared_error:",mean_squared_error(y_te, y_pred)
# print "mean_absolute_error:",mean_absolute_error(y_te, y_pred)
# print "r2_score:", r2_score(y_te, y_pred)

#find correlation between columns
data = data[ (data['title_year'] > 1900) & (data['title_year'] < 2000) ]
coe = []
for each in data['title_year'].unique():
    temp_df = data[data['title_year'] == each]
    temp_df = temp_df[['num_voted_users', 'imdb_score']]
    # temp_df.drop('title_year', axis = 'columns', inplace = True)
    x = temp_df['num_voted_users'].corr(temp_df['imdb_score'])
    # print x
    if not np.isnan(x):
        coe.append(x)
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
plt.plot(coe, 'g', label = 'coeff', linewidth = 2)
plt.legend()
plt.show()