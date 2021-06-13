from finance_utility import finance_utility
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from common import set_matplotlib_style

set_matplotlib_style('slide')

def get_kpi(input_df,var=True):
    df = pd.DataFrame()
    for name in input_df.columns:
        prices = input_df[name]
        ret = returns_df[name]
        trade_days = (prices.index[-1] - prices.index[0]).days
        mdd =finance_utility.drawdown(prices)
        cagr = finance_utility.cagr(prices[0],prices[-1],trade_days)
        if(var):
            dd = prices.rolling(126).apply(func=finance_utility.drawdown,raw=False)
            var = dd.quantile(0.05)
        else:
            var=0
        std = ret.std()
        result_dict = {
            'name' :name,
            'mdd' :-mdd*100,
            'var': -var*100,
            'cagr' : cagr,
            'std':std*100*math.sqrt(252),
        }
        df = df.append(result_dict, ignore_index=True)
    return df





data = (  
    ('Single ETF', './data/etf_returns.csv'),    
    ('Monkey Portfolios', './data/random_portfolio_return.csv'),        
    ('CRP', './data/constant_portfolio_return.csv'),
    ('CRP with leverage', './data/l2_constant_portfolio_return.csv'),  
)
fig,ax = plt.subplots()
for type,src in data:
    returns_df = pd.read_csv(src, parse_dates=True, index_col=0)
    prices_df = finance_utility.return_to_price(returns_df)
    df = get_kpi(prices_df,var=False)
    size = 2
    marker=None
    if (type == 'Single ETF'):
        print("qqqqqqqqqqq")
        size = 50
        marker ="x"
    else:
        print(type)
    print(f'size:{size}')
    ax.scatter(df['std'],df['cagr'],s=size,marker=marker,label=type)
    ax.set_xlabel('Std (%)')
    ax.set_ylabel('CAGR (%)')
plt.legend()
plt.tight_layout()
plt.show()
exit()
data = (
 #   ('random', './data/random_portfolio_return.csv'),        
  #  ('constant', './data/constant_portfolio_return.csv'),
  #  ('l2', './data/l2_constant_portfolio_return.csv'),    
    ('etf', './data/etf_returns.csv'),
)
fig, axes = plt.subplots(1,3, figsize=(12, 4))
for type,src in data:
    returns_df = pd.read_csv(src, parse_dates=True, index_col=0)
    prices_df = finance_utility.return_to_price(returns_df)
    df = get_kpi(prices_df)
    axes[0].scatter(df['std'],df['mdd'],s=2,label=type)
    axes[0].set_xlabel('Std (%)')
    axes[0].set_ylabel('MDD (%)')
    axes[1].scatter(df['std'],df['var'],s=2,label=type)
    axes[1].set_xlabel('Std (%)')
    axes[1].set_ylabel('Var (%)')
    axes[2].scatter(df['mdd'],df['var'],s=2,label=type)
    axes[2].set_xlabel('MDD (%)')
    axes[2].set_ylabel('VaR (%)')
    fig.suptitle('Comparison between risk indicators')   
#plt.legend()
plt.tight_layout()
plt.show()
