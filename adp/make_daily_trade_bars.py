from adp.readers.trades_reader import TradesData
from adp.timemethods import date_time_to_sim_time
import sys

def make_trade_bars(args):
    path, output = args
    trades = TradesData(data_type="amme_matched_orders")
    trades.read_data(path=path)
    date_time_to_sim_time(trades.resample_data(freq = "b")).to_csv(output, index = False)

if __name__ == "__main__":
    make_trade_bars(sys.argv[1:])
