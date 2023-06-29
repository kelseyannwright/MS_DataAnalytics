#D209 Task 2 - Predictive Modeling with Random Forest Regressor

#import required libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error as MSE
from sklearn.metrics import r2_score



#set display option for pandas dataframes to no max columns
pd.set_option('display.max_columns', None)

#Load and preview the data
dat = pd.read_csv("~/Desktop/WGU/D209/churn_clean.csv") #load data CSV
dat.info()

#identify number of classes in each variable and remove high cardinality variables
uniqueVal = dat.select_dtypes(include=['object', 'integer']).nunique()
dropcols = uniqueVal[uniqueVal>5].index #identify columns with more than 5 unique groups
dat.drop(list(dropcols), inplace=True, axis=1) 
dat.nunique() #check remaining features and variable lengths

#replace yes/no with 1/0
for i in dat.columns:
    dat = dat.replace({i: {'Yes': 1, 'No': 0}}) 
    
#get dummy variables for remaining features
obj_cols = dat.select_dtypes(include=['object']).columns #define remaining object columns
dat = pd.get_dummies(dat, columns=obj_cols) #create dummy variables


#preview dataset
dat.head()
dat.info()

#export final processed dataset to CSV
dat.to_csv("~/Desktop/WGU/D209/churn_data_processed_T2.csv")

#split data into training and test sets
X = dat.drop('Tenure', axis=1)
y = dat['Tenure']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

#export to csv
X_train.to_csv("~/Desktop/WGU/D209/Xtrain_T2.csv")
X_test.to_csv("~/Desktop/WGU/D209/Xtest_T2.csv")
y_train.to_csv("~/Desktop/WGU/D209/ytrain_T2.csv")
y_test.to_csv("~/Desktop/WGU/D209/ytest_T2.csv")


#Run model using training dataset
rf = RandomForestRegressor(n_estimators=100, random_state=1) #set up random forest classifer
rf.fit(X_train, y_train) #train model

y_pred = rf.predict(X_test) #create model predictions


#Assess model performance
mse_calc = MSE(y_test, y_pred) #check MSE
r2 = r2_score(y_test, y_pred) #check R squared

#calculate errors 
errors = abs(y_pred - y_test)

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / y_test)

# Calculate accuracy using MAPE
accuracy = 100 - np.mean(mape)

print('MSE:', round(mse_calc, 2)) #MSE
print('R2: ', round(r2, 3)) #R squared
print('Accuracy:', round(accuracy, 2), '%.')