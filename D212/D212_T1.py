#D212 - Data Mining II
#TASK 1

#import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from kneed import KneeLocator



#set display option for pandas dataframes to no max columns
pd.set_option('display.max_columns', None)

#Load and preview the data
dat = pd.read_csv("~/Desktop/WGU/D212/churn_clean.csv") #load data CSV
dat.info()
dat.head()

#select variables for research question
df = dat[["Tenure", "MonthlyCharge"]]
df.head()

#preprocessing - check for duplicates and missing values
print("number of duplicates:", df.duplicated().sum()) 
print("number of nulls:", df.isna().sum().sum())

df.to_csv("~/Desktop/WGU/D212/churn_processed_T1.csv")


#scale features using standard scalar
scaler = StandardScaler()
df_mod = pd.DataFrame(scaler.fit_transform(df), columns = df.columns)

#check scalar 
df_mod.head()
df_mod.min()
df_mod.max()
df_mod.std()

#output cleaned/prepared dataset
df_mod.to_csv("~/Desktop/WGU/D212/churn_scaled_T1.csv")


#determine number of clusters to use
ks = range(1, 11) #set range of clusters to check
inertias = [] #to store inertia values

for k in ks:
    model = KMeans(n_clusters=k, n_init='auto')
    model.fit(df_mod)
    inertias.append(model.inertia_)


plt.plot(ks, inertias, '-o')
plt.xlabel('number of clusters')
plt.ylabel('inertia')
plt.show() #assess plot to determine number of clusters to use

#use KneeLocator to determine number of clusters
kl = KneeLocator(range(1, 11), inertias, curve="convex", direction="decreasing")
nclust = kl.elbow
nclust

#create and fit model
model = KMeans(n_clusters=nclust, n_init='auto')
model.fit(df_mod)

#create table with features and labels
df_out = df_mod
df_out['Labels'] = model.labels_
df_out.head()

df_us = df.assign(clusters = model.labels_)
df_us.head()

####model analysis

# Assign the cluster centers: centroids
centroids = model.cluster_centers_

# Assign the columns of centroids: centroids_x, centroids_y
centroids_x = centroids[:,0]
centroids_y = centroids[:,1]
clust_labels = df_mod['Labels'].unique()
clust_labels.sort()


fig, ax = plt.subplots()
#make a scatter plot of all data points colored for each cluster
ax.scatter(df_mod.iloc[:,0], df_mod.iloc[:,1], c=model.labels_, alpha=0.5)

# Make a scatter plot of centroids_x and centroids_y
ax.scatter(centroids_x, centroids_y, marker='D', s=50, c='grey')

for i, txt in enumerate(clust_labels):
    ax.annotate(txt, (centroids_x[i], centroids_y[i]), weight='bold', size=12)

plt.xlabel('Standardized Tenure')
plt.ylabel('Standardized Monthly Charge')
plt.show()


#barplot of clusters using unstandardized (original) data
df_means = df_us.groupby(['clusters']).mean()
df_means['clusters'] = df_means.index.values
df_means.index.name = 'index'
df_means.iloc[:,:-1].plot.bar()
plt.xlabel('Cluster Label')
plt.ylabel('Mean Tenure and Mean Monthly Charge')
plt.show()


plt.hist(df.iloc[:,0])
plt.title('Histogram of Tenure')
plt.xlabel('Tenure')
plt.ylabel('Count of Observations')
plt.show()

plt.hist(df.iloc[:,1])
plt.title('Histogram of Monthly Charge')
plt.xlabel('Monthly Charge')
plt.ylabel('Count of Observations')
plt.show()


#scatter plot of unstandardized data (original)
plt.scatter(df_us.iloc[:,0], df_us.iloc[:,1], c=model.labels_, alpha=0.5)
plt.xlabel('Tenure (Number of Months)')
plt.ylabel('Monthly Charge (Dollars)')
plt.show()

