#D212 Task 2 - PCA
#Kelseyann Wright


#import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA 


#set display option for pandas dataframes to no max columns
pd.set_option('display.max_columns', None)

#Load data
df = pd.read_csv("~/Desktop/WGU/D212/churn_clean.csv") #load data CSV

#check for duplicates and missing values
print("number of duplicates:", df.duplicated().sum()) 
print("number of nulls:", df.isna().sum().sum())

#preview data
df.info()

#pull out continuous data
df_cont = df.select_dtypes(include=float)
df_cont.info()
df_cont.describe()

#scale the data for PCA
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_cont), columns = df_cont.columns)

#check scalar 
df_scaled.describe()

#output prepared dataset
df_scaled.to_csv("~/Desktop/WGU/D212/churn_processed_T2.csv")

#fit PCA to the data
pca = PCA(n_components=df_scaled.shape[1])
pca_model = pca.fit_transform(df_scaled)

#create column labels for PCA
nums = list(range(len(df_scaled.columns)+1))
nums.remove(0)
nums = [str(x) for x in nums]
names = ['PC' + x for x in nums]
names

#make pca dataframe
df_pca = pd.DataFrame(pca_model, columns=names)
df_pca

#output loadings
loadings = pd.DataFrame(pca.components_.T, columns=names, index=df_scaled.columns)
loadings

#scree plot
plt.plot(pca.explained_variance_ratio_)
plt.xlabel('number of components')
plt.ylabel('explained variance')
plt.title('Scree Plot')
plt.show()

#plot with eigenvalues
cov_matrix = np.dot(df_scaled.T, df_scaled) / df_scaled.shape[0]
eigenvalues = [np.dot(eigenvector.T, np.dot(cov_matrix, eigenvector)) for eigenvector in pca.components_]

plt.plot(eigenvalues)
plt.xlabel('number of components')
plt.ylabel('eigenvalue')
plt.title('Kaiser Criterion')
plt.axhline(y=1, color='r', linestyle='-')
plt.show() 


#Variance of each component
exp_var = pca.explained_variance_
exp_var[0:3]
exp_var[0:3].sum()

exp_var_perc = pca.explained_variance_ratio_*100
exp_var_perc[0:3]
exp_var_perc[0:3].sum()