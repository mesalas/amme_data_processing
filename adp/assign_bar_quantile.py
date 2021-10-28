import pandas as pd

def assign_percentiles(bars : pd.DataFrame, quantiles = 20, statistic = "range") -> pd.DataFrame:
    ''' Method for assigning a quantile to a row in data frame. Assignmen is based on the statistic 
    '''
    if statistic == "range":
        stat = bars["High"] - bars["Low"]
    else:
        raise Exception()

    bars["quantile"] = pd.qcut(stat.rank(method='first'), quantiles,
                               labels=[i for i in range(1, quantiles + 1)])
    return bars
def make_quantile_windows(bars, target_quant):
    bars = bars[bars["quantile"] == target_quant].reset_index()
    windows = list()
    for i in range(len(bars)-1):
        windows.append([bars["First"].loc[i],bars["Last"].loc[i]])
    return windows