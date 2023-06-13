#D209 Task 1 - Classification Modeling

#import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from scipy.stats import chi2_contingency
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (accuracy_score, confusion_matrix, roc_auc_score, classification_report)

#set display option for pandas dataframes to no max columns
pd.set_option('display.max_columns', None)

#Load and preview the data
dat = pd.read_csv("~/Desktop/WGU/D209/churn_clean.csv") #load data CSV
dat.info()

#identify number of classes in each variable and remove high cardinality variables
uniqueVal = dat.nunique() #count unique values in each feature
uniqueVal 
dropcols = uniqueVal[uniqueVal>5].index #identify columns with more than 5 unique groups
dat.drop(list(dropcols), inplace=True, axis=1) 
dat.nunique() #check remaining variable lengths
dat.info() #verify that data type is object for all remaining features

#check for independence between features
datchi = dat.drop('Churn', axis = 1)
for i in datchi.columns:
    feat = datchi.drop(i,axis= 1) #feature variables
    y = np.array(datchi[i]) #dependent variable
    for f in feat.columns:
        CrosstabResult=pd.crosstab(index=y,columns=np.array(feat[f]))
        # Performing Chi-sq test
        ChiSqResult = chi2_contingency(CrosstabResult)
        if ChiSqResult[1] < 0.05:
            print(i, 'x', f)
            print(ChiSqResult[1])

colsdrop = ['OnlineBackup', 'DeviceProtection', 'Tablet', 'TechSupport']      
dat = dat.drop(colsdrop, axis=1)

#replace yes/no with 1/0
for i in dat.columns:
    dat = dat.replace({i: {'Yes': 1, 'No': 0}}) 

#get dummy variables for remaining features
obj_cols = dat.select_dtypes(include=['object']).columns #define remaining object columns
dat = pd.get_dummies(dat, columns=obj_cols) #create dummy variables

dat.head() #preview dataset

#check for balanced data
sns.countplot(x=dat["Churn"], palette="crest")#plot churn countplot
plt.show()

print(dat['Churn'].value_counts()) #check for balanced data

#need to balance churn data - use Synthetic Minority Oversampling Technique (SMOTE)
X = np.array(dat.drop('Churn',axis= 1)) #predictor (independent) variables
y = np.array(dat['Churn']) #dependent variable

os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

#columns = X_train.columns
Xmod, ymod = os.fit_resample(X_train, y_train)
Xmod = pd.DataFrame(data=Xmod,columns=dat.drop('Churn',axis= 1).columns)
ymod= pd.DataFrame(data=ymod,columns=['Churn'])
datbal = pd.concat([ymod, Xmod], axis=1)

# Check data
print(datbal['Churn'].value_counts()) #check for balanced data
datbal.info() #check final dataframe
dat.nunique() #check to make sure each feature is still binary

#export final processed dataset to CSV
datbal.to_csv("~/Desktop/WGU/D209/churn_data_processed_T1.csv")

#split data into training and test sets
X = datbal.drop('Churn', axis=1)
y = datbal['Churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
#export to csv
X_train.to_csv("~/Desktop/WGU/D209/Xtrain_T1.csv")
X_test.to_csv("~/Desktop/WGU/D209/Xtest_T1.csv")
y_train.to_csv("~/Desktop/WGU/D209/ytrain_T1.csv")
y_test.to_csv("~/Desktop/WGU/D209/ytest_T1.csv")


#Run model using training dataset
model = GaussianNB() #identify model to use (Naive Bayes Classifier)
model.fit(X_train, y_train) #train model

y_pred = model.predict(X_test) #create model predictions

confusion_matrix(y_test, y_pred) #print confusion matrix
print(classification_report(y_test, y_pred)) #print classfication report

accuracy = accuracy_score(y_pred, y_test) #calcuate model accuracy
auc_score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]) #calculate model AUC score
#print model accuracy and AUC scores
print("Accuracy:", accuracy)
print("AUC:", auc_score)
