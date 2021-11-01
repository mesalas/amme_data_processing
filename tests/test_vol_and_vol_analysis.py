import unittest
from adp.make_volatility_and_volume_analysis import match_bars_and_trades
from adp.readers.trades_reader import TradesData
import pandas as pd


class TestCase(unittest.TestCase):
    def test_assign_bar_quantile(self):
        bars_file_path = "tests/test_data/ABC_NYSE@0_10T_bars.csv.gz"
        matched_orders_file_path = "tests/test_data/ABC_NYSE@0_Matching-MatchedOrders.csv.gz"
        match_bars_and_trades(matched_orders_file_path,
                          bars_file_path,
                          "tests/test_data/10T_heatmap_full.png",
                          "tests/test_data/10T_heatmap_full.csv",
                          0,
                          n_quantiles = 0)
        match_bars_and_trades(matched_orders_file_path,
                          bars_file_path,
                          "tests/test_data/10T_heatmap_1.png",
                          "tests/test_data/10T_heatmap_1.csv",
                          1,
                          n_quantiles = 20)
        
        match_bars_and_trades(matched_orders_file_path,
                          bars_file_path,
                          "tests/test_data/10T_heatmap_q20.png",
                          "tests/test_data/10T_heatmap_q20.csv",
                          20,
                          n_quantiles = 20)
        
        bars_file_path = "tests/test_data/ABC_NYSE@0_daily_bars.csv.gz"
        match_bars_and_trades(matched_orders_file_path,
                          bars_file_path,
                          "tests/test_data/daily_heatmap_full.png",
                          "tests/test_data/daily_heatmap_full.csv",
                          0,
                          n_quantiles = 0)

        match_bars_and_trades(matched_orders_file_path,
                          bars_file_path,
                          "tests/test_data/daily_heatmap_1.png",
                          "tests/test_data/daily_heatmap_1.csv",
                          1,
                          n_quantiles = 20)
        
        match_bars_and_trades(matched_orders_file_path,
                          bars_file_path,
                          "tests/test_data/daily_heatmap_q20.png",
                          "tests/test_data/daily_heatmap_q20.csv",
                          20,
                          n_quantiles = 20)
        

if __name__ == '__main__':
    unittest.main()