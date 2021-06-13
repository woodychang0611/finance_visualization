from finance_utility import finance_utility
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import timedelta

data = (  
    ('Single ETF', './data/etf_returns.csv'),    
    ('Monkey Portfolios', './data/random_portfolio_return.csv'),        
    #('CRP', './data/constant_portfolio_return.csv'),
    #('CRP with leverage', './data/l2_constant_portfolio_return.csv'),  
)
obs_period = 126 #6 months working days


result_df = pd.DataFrame()
for type,src in data:
    df = pd.read_csv(src, parse_dates=True, index_col=0)
    dates = list(d for d in df.index if (( d-df.index[0]).days >= obs_period))

    for date in dates[:2]:
        ed = date
        sd = date - timedelta(days=obs_period)
        df = df[(df.index >=sd) & (df.index <=ed)]
        kpi_df = finance_utility.get_kpi(df,kpis=['cagr','std'])
        kpi_df['date'] = date
        kpi_df['type']=type
        kpi_df.set_index(['date','type','name'],inplace=True)  
        result_df =pd.concat([result_df, kpi_df])

        print(kpi_df)
      
print(result_df.index)
result_df.to_csv('./data/kpis.csv')
    
