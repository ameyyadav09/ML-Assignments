import numpy as np
import pandas as pd

train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

# print train_data.shape, test_data.shape

#check missing values
train_NaNs = train_data.shape[0] - train_data.dropna().shape[0]

test_NaNs = test_data.shape[0] - test_data.dropna().shape[0]

#checking which columns have missing values
train_cols = train_data.isnull().sum()

#counting unique values in each column
uniqs = train_data.select_dtypes(include = ['O'])
values = uniqs.apply(pd.Series.nunique)

#handling NaNs
#workclass - imputing values Domain specifically
train_data.workclass.value_counts(sort = True)
train_data.workclass.fillna('Private', inplace = True)

#Occupation
train_data.occupation.value_counts(sort = True)
train_data.occupation.fillna('Prof-speciality', inplace = True)

#Native Country
train_data['native.country'].value_counts(sort = True)
train_data['native.country'].fillna('United-States', inplace = True)

#checking again if NaNs still persisting
train_cols = train_data.isnull().sum()

#chekcing proportion of target variable
prop = train_data.target.value_counts()/train_data.shape[0]
#for above prop with rough estimate we can get 75% accuracy

#checking influence of education on target by creating a cross tab of target
cross = pd.crosstab(train_data['education'], train_data['target'], margins = True)/train_data.shape[0]

#importing sklearn for model building
from sklearn import preprocessing

for column in train_data.columns:
	if train_data[column].dtype == 'object':
		lable = preprocessing.LabelEncoder()
		lable.fit(list(train_data[column].values))
		train_data[column] = lable.transform(list(train_data[column].values))

#Build a Random Forest
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score

y = train_data['target']
train_data.drop('target',axis='columns',inplace=True)
X = train_data

X_train, X_test, y_train, y_test = \
train_test_split(X, y, test_size = 0.3, random_state = 1, stratify = y)

#train RandomForestClassifier
randClassifier = RandomForestClassifier(n_estimators = 500, max_depth = 6)
randClassifier.fit(X_train, y_train)
y_pred = randClassifier.predict(X_test)

print "Accuracy-score:", accuracy_score(np.array(y_test), y_pred)