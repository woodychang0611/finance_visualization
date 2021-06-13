from numpy.core.fromnumeric import var
from finance_utility import finance_utility
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from common import set_matplotlib_style
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter
from datetime import timedelta

obs_period = 126


indices_df = pd.read_csv('data/indices.csv', parse_dates=True, index_col=0)
returns_df = pd.read_csv('data/constant_portfolio_return.csv', parse_dates=True, index_col=0)
set_matplotlib_style('slide')
fig, ax = plt.subplots(nrows=2, ncols=1,figsize=(12,12), gridspec_kw={'height_ratios': [3, 1]})
performance_ax = ax[0]
indices_ax = ax[1]
dates = indices_df.index
color = 'yellow'
l = indices_ax.axvline(x=dates[0], c=color)
data = (  
    ('Single ETF', './data/etf_returns.csv'),    
    ('Monkey Portfolios', './data/random_portfolio_return.csv'),        
    ('CRP', './data/constant_portfolio_return.csv'),
    ('CRP with leverage', './data/l2_constant_portfolio_return.csv'),  
)

returns_dfs = []
scatters=[]
for type,src in data:
    df = pd.read_csv(src, parse_dates=True, index_col=0)
    df['type']=type
    returns_dfs.append(df)
    count = len(df.columns)
    scatter= performance_ax.scatter(np.zeros(count),np.zeros(count),label=type)
    scatters.append(scatter)

def init():
    print('test')
    color = 'cyan'
    indices_ax.plot(indices_df.index, indices_df["S&P 500"],color=color)

    color = 'lime'
    vix_ax = indices_ax.twinx()
    vix_ax.tick_params(axis='y', labelcolor=color)
    vix_ax.plot(indices_df.index, indices_df["VIX"],color=color)
    performance_ax.legend()
    performance_ax.set_xlim(0, 100)
    performance_ax.set_ylim(-3, 3)
    return l,

def update(frame):
    ed = frame    
    sd = ed - timedelta(days=(obs_period-1))
    print(ed)
    l.set_data([[frame,frame],[0,1]])
    for df, scatter in zip(returns_dfs,scatters):
        count = len(df.columns)
        if (sd < df.index[0]):
            scatter.set_sizes(np.zeros(count))               
            continue
        df = df[(df.index >=sd) & (df.index <=ed)]
        kpis = finance_utility.get_kpi(df.drop(columns=['type']),kpis=['cagr','std'])
        offsets = np.array(list(zip(kpis['std'],kpis['cagr'])))
        scatter.set_sizes(np.full(count,3))  
        scatter.set_offsets(offsets) #np.random.random((count,2)))

    return l,

ani = FuncAnimation(fig=fig, func=update, frames=dates, init_func=init, blit=True)
#plt.show()
f = r"./test.gif" 
writergif = PillowWriter(fps=30) 
ani.save(f, writer=writergif)