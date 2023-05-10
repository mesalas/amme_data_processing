from adp.readers.trades_reader import TradesData
from adp.timemethods import date_to_sim_time
from adp.assign_bar_quantile import assign_percentiles
import sys

def make_daily_volumes(args):
    side, path, output = args
    trades = TradesData(data_type="amme_matched_orders")
    trades.read_data(path=path)
    if side == "active":
        date_to_sim_time(trades.make_daily_active_volume()).to_csv(output, index = False)
    elif side == "passive":
        date_to_sim_time(trades.make_daily_passive_volume()).to_csv(output, index = False)


if __name__ == "__main__":
    make_daily_volumes(sys.argv[1:])
