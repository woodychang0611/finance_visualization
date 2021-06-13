import pandas as pd
import pandas_datareader as pdr
from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib
import math
import numpy as np

class finance_utility:
    @staticmethod
    def drawdown(x: pd.core.series.Series):
        return finance_utility._drawdown(x, False)

    @staticmethod
    def plot_drawdown(x: pd.core.series.Series):
        return finance_utility._drawdown(x, True)

    @staticmethod
    def _drawdown(x: pd.core.series.Series, display):
        if (not isinstance(x, (pd.core.series.Series))):
            raise TypeError(f'type {type(x)} not supported')
        e = ((np.maximum.accumulate(x) - x)/np.maximum.accumulate(x)).idxmax()  # end of the period
        if (isinstance(e, float) and math.isnan(e)):
            e = x.index[0]
        s = e if (e == x.index[0]) else (x[:e]).idxmax()
        if (display):
            plt.plot(x)
            plt.plot([e, s], [x[e], x[s]], 'o', color='Red', markersize=10)
            plt.show()
            return
        else:
            return min(0, (x[e]-x[s])/x[s])

    @staticmethod
    def cagr(start, end, len):
        return math.pow(end/start, 365/len)-1

    @staticmethod
    def price_to_return(df):
        ret= df.copy()
        for col in ret.columns:
            ret[col] = ret[col].rolling(2).apply(lambda s:s[1]/s[0]-1)
        return ret
    
    @staticmethod
    def return_to_price(df,init_price=1):
        price_df= df.copy()
        
        for col in df.columns:
            returns = df[col].sort_index().fillna(0)
            array = returns.to_numpy()
            price = init_price
            for i in range(len(array)):
                price = array[i] = price*(array[i]+1)
            price_df[col] =  pd.Series(array, index=returns.index)
            
        return price_df
