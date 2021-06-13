import pandas as pd
from finance_utility import finance_utility

df = pd.read_csv('data/raw_prices.csv', parse_dates=True, index_col=0)
min_date = pd.Timestamp(0)
print(min_date)
for etf in df.columns:
    s = df[etf].dropna()
    sd = s.index[0]
    min_date = max(min_date,sd)
print(min_date)
df = df[(df.index>=min_date)]
df = df[df.index.dayofweek < 5]
df =df.fillna(method='ffill')
df.to_csv('./data/etf_prices.csv')
finance_utility.price_to_return(df).to_csv('./data/etf_returns.csv')