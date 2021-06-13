import pandas as pd
import numpy as np

def constant_weight(weight):
    def F():
        return weight
    return F

def random_weight(len,leverage=1):
    def F():    
        rand = np.random.random(len)
        rand = np.exp(rand*30)
        n= 0
        threshold = np.sort(rand)[-n]
        func =lambda s:s if (s>=threshold) else 0
        rand = np.array(list(func(i) for i in rand))
        a = leverage*rand / rand.sum()
        return a
    return F

def new_portfolio_returns(weight_func,df_return):
    series = pd.Series(index = df_return.index,dtype=float)
    for i in series.index:
        returns = df_return.loc[i].to_numpy()
        if (np.isnan(returns).any()):
            series[i] = np.NAN
        else:
            series[i] = np.dot(returns,weight_func())
    return series

returns_df = pd.read_csv('./data/etf_returns.csv', parse_dates=True, index_col=0)
inv_len = len(returns_df.columns)

random_weight_func = random_weight(inv_len)
generate_count = 500

df_constant_portfolio_return = pd.DataFrame(index = returns_df.index) 
for i in range(generate_count):
    constant_weight_func = constant_weight(random_weight(inv_len,leverage=2)())
    s= new_portfolio_returns(constant_weight_func,returns_df)
    df_constant_portfolio_return[f'p_{i}'] =s
    if ((i+1)%10 ==0):
        print (f'{i+1}/{generate_count} Done')
        df_constant_portfolio_return.to_csv('./data/l2_constant_portfolio_return.csv')
df_constant_portfolio_return.to_csv('./data/l2_constant_portfolio_return.csv')


df_random_portfolio_return = pd.DataFrame(index = returns_df.index) 
for i in range(generate_count):
    s= new_portfolio_returns(random_weight_func,returns_df)
    df_random_portfolio_return[f'p_{i}'] =s
    if ((i+1)%10 ==0):
        print (f'{i+1}/{generate_count} Done')
        df_random_portfolio_return.to_csv('./data/random_portfolio_return.csv')
df_random_portfolio_return.to_csv('./data/random_portfolio_return.csv')


df_constant_portfolio_return = pd.DataFrame(index = returns_df.index) 
for i in range(generate_count):
    constant_weight_func = constant_weight(random_weight(inv_len,leverage=2)())
    s= new_portfolio_returns(constant_weight_func,returns_df)
    df_constant_portfolio_return[f'p_{i}'] =s
    if ((i+1)%10 ==0):
        print (f'{i+1}/{generate_count} Done')
        df_constant_portfolio_return.to_csv('./data/l2_constant_portfolio_return.csv')
df_constant_portfolio_return.to_csv('./data/l2_constant_portfolio_return.csv')

exit()