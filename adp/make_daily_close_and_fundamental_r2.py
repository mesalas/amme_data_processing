import pandas as pd
import sys
from scipy.stats import linregress

from adp.assign_bar_quantile import assign_percentiles
from adp.readers.trades_reader import TradesData
from adp.timemethods import date_time_to_sim_time


def make_daily_close_and_fundamental_r2(args):
    trades_path, fundamentals_path = args
    trades = TradesData(data_type="amme_matched_orders")
    trades.read_data(path=trades_path)
    daily_bars = date_time_to_sim_time(assign_percentiles(trades.resample_data(freq="b")))
    fundamentals = pd.read_csv(fundamentals_path)
    fundamentals["DateTime"] = pd.to_datetime(fundamentals["DateTime"], format="%Y-%m-%d %H:%M:%S.%f")
    dividends = fundamentals.set_index("DateTime", drop=False).resample("b").last()["dividend"]
    slope, intercept, r, p, se = linregress(daily_bars["Close"], dividends)
    print(slope,r**2)
    return r**2

if __name__ == "__main__":
    make_returns_qq_data(sys.argv[1:])