import unittest
from adp.plotting.plot_price import plot_price,plot_intraday_bars


class TestCase(unittest.TestCase):
    def test_plot_bars(self):
        test_args = ["test_output/daily_bars.png","test_output/ABC_NYSE@0_daily_bars.csv.gz","test_output/DEF_NYSE@0_daily_bars.csv.gz", "test_output/GHI_NYSE@0_daily_bars.csv.gz"]
        plot_price(test_args)

    def test_plot_intraday_bars(self):
        test_args = ["test_output/daily_10T_bars.png","test_output/ABC_NYSE@0_10T_bars.csv.gz","test_output/DEF_NYSE@0_10T_bars.csv.gz", "test_output/GHI_NYSE@0_10T_bars.csv.gz"]
        plot_intraday_bars(test_args)


if __name__ == '__main__':
    unittest.main()
