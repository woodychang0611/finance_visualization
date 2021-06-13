import pandas_datareader as pdr
import pandas as pd
from datetime import datetime
etf_csv = "./data/raw/etf.csv"
df = pd.read_csv(etf_csv)

sd = datetime(1999,1,1)
ed = datetime(2021,5,19)
prices_dataframe= pd.DataFrame(index=pd.date_range(start=sd,end=ed, freq='D'))
for etf in df['bol']:
    print(etf)
    series = (pdr.get_data_yahoo(symbols=etf, start=sd, end=ed)["Adj Close"]).rename(etf)
    prices_dataframe[etf]=series
prices_dataframe.to_csv('./data/raw_prices.csv')
print(prices_dataframe)