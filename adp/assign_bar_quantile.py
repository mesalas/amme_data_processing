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