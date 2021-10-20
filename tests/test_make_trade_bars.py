import unittest
from adp.make_daily_trade_bars import make_trade_bars
from adp.make_intraday_trade_bars import make_intraday_trade_bars
class TestCase(unittest.TestCase):
    def test_read_trades_write_bars(self):
        for symbol in ["ABC", "DEF", "GHI"]:
            test_args = ["tests/test_data/"+symbol +"_NYSE@0_Matching-MatchedOrders.csv.gz",
                         "tests/test_data/"+symbol +"_NYSE@0_daily_bars.csv.gz"]
            make_trade_bars(test_args)

    def test_read_trades_write_intraday_bars(self):
        for symbol in ["ABC", "DEF", "GHI" ]:
            test_args = ["10T",
                         "tests/test_data/" + symbol + "_NYSE@0_Matching-MatchedOrders.csv.gz",
                         "tests/test_data/" + symbol + "_NYSE@0_10T_bars.csv.gz"]
            make_intraday_trade_bars(test_args)


if __name__ == '__main__':
    unittest.main()
