#D212 - Task 3 - Market Basket Analysis
#Kelseyann Wright


#import required libraries
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


#set display option for pandas dataframes to no max columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 150)


#Load data
df = pd.read_csv("~/Desktop/WGU/D212/teleco_market_basket.csv") #load data CSV

#preview data
df.info()
df.head()
df.shape

#remove empty rows
df = df.dropna(how='all')
df.shape

#convert dataframe into list of lists
rows = []
for i in range (0, df.shape[0]):
    rows.append([str(df.values[i,j]) for j in range (0, df.shape[1])])



#feed list to TransactionEncoder
TE = TransactionEncoder()
df_array = TE.fit(rows).transform(rows)

#make into dataframe
df_transaction = pd.DataFrame(df_array, columns = TE.columns_)
df_transaction.head()
df_transaction.shape

#remove 'nan" column
df_mba = df_transaction.drop(['nan'], axis=1)
df_mba.shape
df_mba.head()

#export cleaned dataframe to csv
df_mba.to_csv("~/Desktop/WGU/D212/teleco_market_basket_clean_T3.csv")


#create apriori object called rules
rules = apriori(df_mba, min_support = 0.05, use_colnames = True)
rules.head()
rules.shape

#create rules table
rule_table = association_rules(rules, metric = 'lift', min_threshold = 1)
rule_table.head()
rule_table.shape
rule_table.to_csv("~/Desktop/WGU/D212/ruletable_T3.csv")

#get top three rules
top_rules = rule_table.sort_values('lift', ascending=False).head(3)
print(top_rules)
