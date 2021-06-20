from os import replace
import numpy as np
import pandas as pd
from common import set_matplotlib_style
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
from matplotlib import colors 
from matplotlib.animation import FuncAnimation,PillowWriter
import itertools
from datetime import timedelta
import matplotlib.patches as mpatches

obs_period = 126 #6 months working days
single_type_count = 100
risk_free_cagr =1  
indices_df = pd.read_csv('data/indices.csv', parse_dates=True, index_col=0)
#unzip kpis.csv.zip if needed
kpi_df = pd.read_csv('data/kpis.csv', parse_dates=['date'])
kpi_df['sharpe']=(kpi_df['cagr']-risk_free_cagr)/kpi_df['std']
dates =list(kpi_df['date'].unique())
portfolio_types = kpi_df['type'].unique()
type_values = {}

for i,type in enumerate(portfolio_types):
    type_values[type]=i
set_matplotlib_style('slide')
axes_colors = list((d['color'] for d in matplotlib.rcParams['axes.prop_cycle']))
cmap = colors.ListedColormap(axes_colors)


bounds=range(0,len(portfolio_types)+1)
norm = colors.BoundaryNorm(bounds, len(portfolio_types))


for kpi_display_name,kpi in (('CAGR','cagr'),('Std','std'),('Sharpe Ratio','sharpe')):
    plt.close()

    fig, axes = plt.subplots(nrows=2, ncols=1,figsize=(7,9), 
        gridspec_kw={'height_ratios': [3, 1]},sharex='col')

    rank_ax = axes[0]
    indices_ax = axes[1]
    data = None
    for date in dates[:]:
        df = kpi_df[kpi_df['date']==date].groupby('type').sample(n=single_type_count,random_state=1)
        type_ranks = df.sort_values(kpi)['type']
        d = np.array(((list(type_values[t] for t in type_ranks)),)).transpose()
        if (data is None):
            data = d.copy()
        else:
            data = np.concatenate((data,d),axis=1)
    unique, counts = np.unique(data, return_counts=True)
    print(dict(zip(unique, counts)))

    offset = np.timedelta64(int(obs_period/2),'D')
    x_lims = matplotlib.dates.date2num((dates[0]-offset,dates[-1]-offset))
    rank_ax.imshow(data,aspect='auto',origin='lower',
                    extent=(*x_lims,0,100),cmap=cmap,norm=norm)
    rank_ax.xaxis.set_visible(False)
    rank_ax.set_title(f'{kpi_display_name} Rank Chart')
    rank_ax.set_yticks([])
    rank_ax.set_ylabel(f'Rank ({kpi_display_name})')
    handles=[]  
    for c,type in  zip(axes_colors,portfolio_types):
        handles.append( mpatches.Patch(color=c, label=type))
    rank_ax.legend(handles=handles,loc=7)

    color = 'cyan'
    indices_ax.plot(indices_df.index, indices_df["S&P 500"],color=color)
    indices_ax.set_ylabel('S&P 500',color=color)
    indices_ax.tick_params(axis='y', labelcolor=color)
    indices_ax.tick_params(axis='x', rotation=45)  
    color = 'lime'
    vix_ax = indices_ax.twinx()
    vix_ax.tick_params(axis='y', labelcolor=color)
    vix_ax.plot(indices_df.index, indices_df["VIX"],color=color)
    vix_ax.set_ylabel('VIX',color=color)
    plt.savefig(f'{kpi}_rank.png')          