import unittest
from adp.make_daily_trade_bars import make_trade_bars
from adp.make_daily_active_passive_volume import make_daily_volumes
class TestCase(unittest.TestCase):
    def test_make_daily_volumes(self):
        test_args = ["active", "tests/test_data/norpc-ABC_NYSE@41_Matching-MatchedOrders.csv.gz",
                     "tests/test_data/norpc-ABC_NYSE@41_daily_active_volumes.csv"]
        make_daily_volumes(test_args)
        test_args = ["passive", "tests/test_data/norpc-ABC_NYSE@41_Matching-MatchedOrders.csv.gz",
                     "tests/test_data/norpc-ABC_NYSE@41_daily_active_volumes.csv.gz"]
        make_daily_volumes(test_args)


if __name__ == '__main__':
    unittest.main()
