import unittest
from adp.make_daily_returns_autocorrelation import make_daily_returns_autocorrelation
from adp.make_intraday_returns_autocorrelation import make_intraday_returns_autocorrelation
class TestCase(unittest.TestCase):
    def test_daily_autocorr(self):
        for symbol in ["ABC", "DEF", "GHI"]:
            test_args = ["test_output/"+symbol +"_NYSE@0_daily_bars.csv.gz",
                         "test_output/"+symbol +"_NYSE@0_daily_autocorr.csv.gz", False]
            make_daily_returns_autocorrelation(test_args)
            test_args = ["test_output/"+symbol +"_NYSE@0_daily_bars.csv.gz",
                         "test_output/"+symbol +"_NYSE@0_daily_abs_autocorr.csv.gz", True]
            make_daily_returns_autocorrelation(test_args)

    def test_intraday_autocorr(self):
        for symbol in ["ABC", "DEF", "GHI"]:
            test_args = ["test_output/"+symbol +"_NYSE@0_10T_bars.csv.gz",
                         "test_output/"+symbol +"_NYSE@0_10T_autocorr.csv.gz", False]
            make_intraday_returns_autocorrelation(test_args)
            test_args = ["test_output/"+symbol +"_NYSE@0_10T_bars.csv.gz",
                         "test_output/"+symbol +"_NYSE@0_10T_abs_autocorr.csv.gz", True]
            make_intraday_returns_autocorrelation(test_args)


if __name__ == '__main__':
    unittest.main()
