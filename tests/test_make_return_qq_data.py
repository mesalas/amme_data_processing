import unittest
from adp.make_returns_qq_data import make_returns_qq_data

class TestCase(unittest.TestCase):
    def test_daily_qq(self):
        for symbol in ["ABC", "DEF", "GHI"]:
            test_args = ["test_output/"+symbol +"_NYSE@0_daily_bars.csv.gz",
                         "test_output/"+symbol +"_NYSE@0_daily_return_qq.csv.gz"]
            make_returns_qq_data(test_args)
            test_args = ["test_output/"+symbol +"_NYSE@0_daily_bars.csv.gz",
                         "test_output/"+symbol +"_NYSE@0_daily_abs_return_qq.csv.gz"]
            make_returns_qq_data(test_args)

    def test_intraday_qq(self):
        for symbol in ["ABC", "DEF", "GHI"]:
            test_args = ["test_output/"+symbol +"_NYSE@0_10T_bars.csv.gz",
                         "test_output/"+symbol +"_NYSE@0_10T_return_qq.csv.gz"]
            make_returns_qq_data(test_args)
            test_args = ["test_output/"+symbol +"_NYSE@0_10T_bars.csv.gz",
                         "test_output/"+symbol +"_NYSE@0_10T_return_qq.csv.gz"]
            make_returns_qq_data(test_args)


if __name__ == '__main__':
    unittest.main()
