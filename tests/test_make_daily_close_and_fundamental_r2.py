import unittest
from adp.make_daily_close_and_fundamental_r2 import make_daily_close_and_fundamental_r2
class TestCase(unittest.TestCase):
    def test_read_trades_write_bars(self):
        test_args = ["tests/test_data/norpc-ABC_NYSE@250_Matching-MatchedOrders.csv.gz",
                     "tests/test_data/norpc-ABC_NYSE@250_Matching-FundamentalInstsLog.csv.gz"]
        make_daily_close_and_fundamental_r2(test_args)

        test_args = ["tests/test_data/norpc-ABC_NYSE@41_Matching-MatchedOrders.csv.gz",
                     "tests/test_data/norpc-ABC_NYSE@41_Matching-FundamentalInstsLog.csv.gz"]
        make_daily_close_and_fundamental_r2(test_args)



if __name__ == '__main__':
    unittest.main()
