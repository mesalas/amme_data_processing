import unittest
from adp.assign_bar_quantile import assign_percentiles
from adp.readers.trades_reader import TradesData
import pandas as pd


class TestCase(unittest.TestCase):
    def test_assign_bar_quantile(self):
        file_path = "tests/test_data/ABC_NYSE@0_10T_bars.csv.gz"
        bars = pd.read_csv(file_path)
        bars = assign_percentiles(bars, quantiles=20)
        print(bars.head().to_markdown())
        

if __name__ == '__main__':
    unittest.main()