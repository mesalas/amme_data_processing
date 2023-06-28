import unittest
from adp.make_order_cascades import make_order_cascades

class TestCase(unittest.TestCase):
    def test_make_order_cascades(self):

        test_args = ["test_data/cascades_data/ABC_NYSE@0_Matching-MatchedOrders.csv.gz",
                     "test_data/cascades_data/ABC_NYSE@0_Matching-MarketOrders.csv.gz",
                     "test_data/cascades_data/0_ABC_5T_bars.csv.gz",
                     "test_data/cascades_data/0_ABC_NYSE_cascades.csv.gz"]
        make_order_cascades(test_args)


if __name__ == '__main__':
    unittest.main()
