import matplotlib
from cycler import cycler

def set_matplotlib_style(mode=None):
    matplotlib.rcParams.update(matplotlib.rcParamsDefault)
    matplotlib.rcParams.update({'font.size': 15})
    matplotlib.rcParams['lines.linewidth'] = 2
    #matplotlib.rcParams["text.usetex"] = True

    if(mode=='slide'):
        matplotlib.rcParams['axes.prop_cycle']=  cycler(color= ['#66FF99','#66CCFF','#FFD9CD','#FF99FF'])
        for name in matplotlib.rcParams:
            if matplotlib.rcParams[name]=='black':
                matplotlib.rcParams[name] ='#B9CAFF'
            if matplotlib.rcParams[name]=='white':
                matplotlib.rcParams[name] ='#0C0C3A'