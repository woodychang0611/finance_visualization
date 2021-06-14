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

indices_df = pd.read_csv('data/indices.csv', parse_dates=True, index_col=0)
kpi_df = pd.read_csv('data/kpis.csv', parse_dates=['date'])
kpi_df['cagr']=kpi_df['cagr']*100
set_matplotlib_style('slide')

fig, ax = plt.subplots(nrows=2, ncols=1,figsize=(12,12), gridspec_kw={'height_ratios': [3, 1]})
performance_ax = ax[0]
indices_ax = ax[1]
dates =list(kpi_df['date'].unique())
scatters={}
for t, d in kpi_df.groupby('type', sort=False):
    print(t)
    count = len(d['name'].unique())
    if(t == 'Single ETF'):
        scatters[t]=performance_ax.scatter(np.zeros(count),np.zeros(count),s=150,marker="x",label=t)
        pass
    else:
        scatters[t]=performance_ax.scatter(np.zeros(count),np.zeros(count),s=2,label=t)

color = 'yellow'

l = indices_ax.axvline(x=dates[0], c=color)
def init():
    print('test')
    color = 'cyan'
    indices_ax.plot(indices_df.index, indices_df["S&P 500"],color=color)
    indices_ax.set_ylabel('S&P 500')
    color = 'lime'
    vix_ax = indices_ax.twinx()
    vix_ax.tick_params(axis='y', labelcolor=color)
    vix_ax.plot(indices_df.index, indices_df["VIX"],color=color)
    vix_ax.set_ylabel('VIX',color=color)
    performance_ax.legend()
    performance_ax.set_xlim(0, 100)
    performance_ax.set_ylim(-300, 300)
    performance_ax.set_xlabel('Std (%)')
    performance_ax.set_ylabel('CAGR (%)')
    return l,

def update(frame):
    ed = frame
    print(ed)
    l.set_data([[ed,ed],[0,1]])
    df = kpi_df[kpi_df['date']==ed]

    for t, d in df.groupby('type', sort=False):
        offsets = d[['std','cagr']].to_numpy()
        scatters[t].set_offsets(offsets)

    return l,

ani = FuncAnimation(fig=fig, func=update, frames=dates[:], init_func=init, blit=True)
f = r"./test.gif" 
writergif = PillowWriter(fps=30) 
ani.save(f, writer=writergif)