import pandas_datareader as pdr
import pandas as pd
from datetime import datetime

sd = datetime(1999,1,1)
ed = datetime(2021,5,19)
#Get indices (S&P 500, VIX)
indices = (
    ("S&P 500","^GSPC"),
    ("VIX","^VIX")
)
indices_dataframe= pd.DataFrame(index=pd.date_range(start=sd,end=ed, freq='D'))
for name,symbol in indices:
    series = (pdr.get_data_yahoo(symbols=symbol, start=sd, end=ed)["Adj Close"]).rename(name)
    indices_dataframe[name]=series
indices_dataframe.to_csv('./data/raw_indices.csv')

etf_csv = "./data/raw/etf.csv"
df = pd.read_csv(etf_csv)

prices_dataframe= pd.DataFrame(index=pd.date_range(start=sd,end=ed, freq='D'))
for etf in df['bol']:
    print(etf)
    series = (pdr.get_data_yahoo(symbols=etf, start=sd, end=ed)["Adj Close"]).rename(etf)
    prices_dataframe[etf]=series
prices_dataframe.to_csv('./data/raw_prices.csv')
print(prices_dataframe)

