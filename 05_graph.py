from finance_utility import finance_utility
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from common import set_matplotlib_style

set_matplotlib_style('slide')


data = (  
    ('Single ETF', './data/etf_returns.csv'),    
    ('Monkey Portfolios', './data/random_portfolio_return.csv'),        
    ('CRP', './data/constant_portfolio_return.csv'),
    ('CRP with leverage', './data/l2_constant_portfolio_return.csv'),  
)
fig,ax = plt.subplots()
for type,src in data:
    returns_df = pd.read_csv(src, parse_dates=True, index_col=0)
    df = finance_utility.get_kpi(returns_df=returns_df,kpis=['cagr','std'])
    size = 2
    marker=None
    if (type == 'Single ETF'):
        size = 50
        marker ="x"
    else:
        print(type)
    ax.scatter(df['std'],df['cagr'],s=size,marker=marker,label=type)
    ax.set_xlabel('Std (%)')
    ax.set_ylabel('CAGR (%)')
plt.legend()
plt.tight_layout()
plt.show()
#exit()
data = (
 #   ('random', './data/random_portfolio_return.csv'),        
  #  ('constant', './data/constant_portfolio_return.csv'),
  #  ('l2', './data/l2_constant_portfolio_return.csv'),    
    ('etf', './data/etf_returns.csv'),
)
fig, axes = plt.subplots(1,3, figsize=(12, 4))
for type,src in data:
    returns_df = pd.read_csv(src, parse_dates=True, index_col=0)
    df = finance_utility.get_kpi(returns_df,kpis=['mdd','var','cagr','std'])
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
