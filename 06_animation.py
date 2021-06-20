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

obs_period = 126 #6 months working days
single_type_count = 100
risk_free_cagr =1  
indices_df = pd.read_csv('data/indices.csv', parse_dates=True, index_col=0)
#unzip kpis.csv.zip if needed
kpi_df = pd.read_csv('data/kpis.csv', parse_dates=['date'])
kpi_df['sharpe']=(kpi_df['cagr']-risk_free_cagr)/kpi_df['std']


#df = next(iter(kpi_df.groupby('date')))[1]


set_matplotlib_style('slide')

fig, axes = plt.subplots(nrows=2, ncols=5,figsize=(15,9), 
    gridspec_kw={'width_ratios': [7,0.2, 1,1,1],'height_ratios': [3, 1]})
#plt.subplots_adjust(left=None, bottom=None, right=0.7, top=None, wspace=None, hspace=None)
axes[0,1].remove()
axes[1,1].remove()
performance_ax = axes[0,0]
indices_ax = axes[1,0]
for ax in axes[:, 2:].flatten():
    ax.remove()
#Add span axes
gs = axes[0, 0].get_gridspec()
cagr_ax = fig.add_subplot(gs[0:, 2])
std_ax = fig.add_subplot(gs[0:, 3])
sharpe_ax = fig.add_subplot(gs[0:,4])

dates =list(kpi_df['date'].unique())
types = kpi_df['type'].unique()
type_values = {}
for i,type in enumerate(types):
    type_values[type]=i

scatters={}
for t, d in kpi_df.groupby('type', sort=False):
    count = len(d['name'].unique())
    if(t == 'Single ETF'):
        scatters[t]=performance_ax.scatter(np.zeros(count),np.zeros(count),s=100,marker="x",label=t)
        pass
    else:
        scatters[t]=performance_ax.scatter(np.zeros(count),np.zeros(count),s=2,label=t)

color = 'yellow'
ed = dates[0]
sd = ed -  np.timedelta64(obs_period,'D')
l = indices_ax.axvspan(sd, ed, alpha=0.3, color=color)
portfolio_count= single_type_count*len(type)

cmap = itertools.islice(matplotlib.rcParams['axes.prop_cycle'], len(types))
cmap = colors.ListedColormap(list((d['color'] for d in matplotlib.rcParams['axes.prop_cycle'])))
bounds=range(0,len(types)+1)
norm = colors.BoundaryNorm(bounds, len(types))
cagr_graph =cagr_ax.imshow([np.zeros((portfolio_count,1))],aspect='auto',origin='lower',
                                cmap=cmap,norm=norm)
std_graph =std_ax.imshow([np.zeros((portfolio_count,1))],aspect='auto',origin='lower',
                                cmap=cmap,norm=norm)
sharp_graph =sharpe_ax.imshow([np.zeros((portfolio_count,1))],aspect='auto',origin='lower',
                                cmap=cmap,norm=norm)
def init():
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
    performance_ax.legend()
    performance_ax.set_xlim(0, 100)
    performance_ax.set_ylim(-300, 300)
    performance_ax.set_xlabel('Std (%)')
    performance_ax.set_ylabel('CAGR (%)')

    cagr_ax.axis('off')
    cagr_ax.set_title('CAGR')
    std_ax.axis('off')
    std_ax.set_title('Std')
    sharpe_ax.axis('off')
    sharpe_ax.set_title('Sharpe Ratio') 

    return l,

def update(ed):
    print(ed)
    sd = ed -  np.timedelta64(obs_period,'D')
    sd = np.datetime64(sd, 'D')
    ed = np.datetime64(ed, 'D')
    title = f'Return (CAGR) vs Risk (Std) \n {sd}~{ed}'
    performance_ax.set_title(title)
    x0 = matplotlib.dates.date2num(sd)
    x1 = matplotlib.dates.date2num(ed)    
    l.set_xy([[x0,0],[x0,1],[x1,1],[x1,0],[x0,0]])
    df = kpi_df[kpi_df['date']==ed].groupby('type').sample(n=single_type_count,random_state=1)

    #Set Scatters
    for t, d in df.groupby('type', sort=False):
        offsets = d[['std','cagr']].to_numpy()
        scatters[t].set_offsets(offsets)

    #Set Cagr
    types = df.sort_values('cagr')['type']
    data =  np.array((list(type_values[t] for t in types),)).transpose()
    cagr_graph.set_data(data)
    types = df.sort_values('std')['type']
    data =  np.array((list(type_values[t] for t in types),)).transpose()
    std_graph.set_data(data)
    types = df.sort_values('sharpe')['type']
    data =  np.array((list(type_values[t] for t in types),)).transpose()
    sharp_graph.set_data(data)

    return l,

ani = FuncAnimation(fig=fig, func=update, frames=dates[:], init_func=init, blit=True)
f = r"./result.gif" 
writergif = PillowWriter(fps=15) 
ani.save(f, writer=writergif)
