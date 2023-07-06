#D210 - Data Visualization

#The goal of this script is to load, check, and clean datasets
#kaggle dataset source: https://www.kaggle.com/datasets/thedevastator/us-broadband-usage-across-counties-and-zip-codes

#import required libraries
import pandas as pd
import numpy as np

#set display option for pandas dataframes to no max columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


#start with broadband dataset from kaggle
#Load and preview the data
df_broadband = pd.read_csv("~/Desktop/WGU/D210/broadband_data_2020October_ORIGINAL.csv") #load data CSV
df_broadband.info()
df_broadband.head()

#drop metadata columns and check
df_broadband = df_broadband.drop(columns=df_broadband.columns[0:2])
df_broadband.info()
df_broadband

#drop rows with na's and check
df_broadband = df_broadband.dropna(axis=0)
df_broadband.head()

#rename columns and check
df_broadband.columns = ['CountyID', 'CountyName', 'BroadbandAvailPerFCC', 'BroadbandUsage']
df_broadband = df_broadband.drop(17)
df_broadband.head()

#redo index and delete old inex
df_broadband= df_broadband.reset_index()
df_broadband = df_broadband.drop(columns=df_broadband.columns[0])


#check for nans and duplicates
print("number of duplicates:", df_broadband.duplicated().sum()) #count and print number of duplicates
print("number of nulls:", df_broadband.isna().sum().sum())


###Load churn dataset
df_churn = pd.read_csv("~/Desktop/WGU/D210/churn_original.csv") #load data CSV
df_churn.info()
df_churn.head()

df_churn[df_churn['Region'].isna()]


#check county names for matches
df_churn['County'].nunique()
df_broadband['CountyName'].nunique()

#remove strings from broadband dataset that will not match the churn dataset from county column
df_broadband['CountyName'] = df_broadband['CountyName'].str.replace(' County', '')
df_broadband['CountyName'] = df_broadband['CountyName'].str.replace(' Parish', '')
df_broadband['CountyName'] = df_broadband['CountyName'].str.replace(' Borough', '')
df_broadband['CountyName'] = df_broadband['CountyName'].str.replace(' Census Area', '')
df_broadband['CountyName'] = df_broadband['CountyName'].str.replace(' city', '')
df_broadband['CountyName'] = df_broadband['CountyName'].str.replace(' Municipality', '')
df_broadband['CountyName'] = df_broadband['CountyName'].str.replace(' City and', '')


#check which counties in the churn dataset do not have matches in the broadband dataset
missing = df_churn['County'].isin(df_broadband['CountyName']) == False
df_churn[missing]['State']
df_churn[missing]['County']

#make changes to counties to match
df_churn['County'] = df_churn['County'].str.replace('Wade Hampton', 'Greenville')
df_churn['County'] = df_churn['County'].str.replace('Doña Ana', 'Dona Ana')
df_churn['County'] = df_churn['County'].str.replace('Oglala Lakota', 'Oglala')


#add region to churn dataset
state_region_mapping = {
    "Northeast": ["CT", "DE", "ME", "MD", "MA", "NH", "NJ", "NY", "PA", "RI", "VT"],
    "Midwest": ["IL", "IN", "IA", "KS", "MI", "MN", "MO", "NE", "ND", "OH", "SD", "WI"],
    "South": ["AL", "AR", "FL", "GA", "KY", "LA", "MS", "NC", "OK", "SC", "TN", "TX", "VA", "WV", "PR", "DC"],
    "West": ["AK", "AZ", "CA", "CO", "HI", "ID", "MT", "NV", "NM", "OR", "UT", "WA", "WY"]
}

df_churn["Region"] = df_churn["State"].map(
    {state: region for region, states in state_region_mapping.items() for state in states}
)

df_churn.info()
df_churn.head()

df_churn= df_churn.drop(columns=df_churn.columns[0]) #drop extra index column

#export datasets
df_broadband.to_csv("~/Desktop/WGU/D210/broadband_data_clean.csv")
df_churn.to_csv("~/Desktop/WGU/D210/churn_clean.csv")