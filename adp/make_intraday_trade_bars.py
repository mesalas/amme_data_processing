from adp.readers.trades_reader import TradesData
from adp.timemethods import date_time_to_sim_time
import sys

def make_intraday_trade_bars(args):
    freq,path, output = args
    trades = TradesData(data_type="amme_matched_orders")
    trades.read_data(path=path)
    date_time_to_sim_time(trades.make_intraday_bars(freq = freq)).to_csv(output, index = False)

if __name__ == "__main__":
    make_intraday_trade_bars(sys.argv[1:])
