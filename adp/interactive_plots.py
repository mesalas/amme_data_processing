import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
from plot_price import plot_price, plot_intraday_bars
from plot_volume_and_returns import plot_volume_and_returns, plot_intraday_volume_and_returns

# test_args = ["test_data/daily_bars.png","test_data/ABC_NYSE@0_daily_bars.csv","test_data/DEF_NYSE@0_daily_bars.csv"]
# plot_price(test_args)
#
# test_args = ["test_data/daily_5T_bars.png","test_data/ABC_NYSE@0_5T_bars.csv","test_data/DEF_NYSE@0_5T_bars.csv"]
# plot_intraday_bars(test_args)

test_args = ["test_data/daily_bars.png","test_data/ABC_NYSE@0_daily_bars.csv.gz","test_data/DEF_NYSE@0_daily_bars.csv.gz"]
plot_volume_and_returns(test_args)

test_args = ["test_data/daily_10T_bars.png","test_data/ABC_NYSE@0_10T_bars.csv.gz","test_data/DEF_NYSE@0_10T_bars.csv.gz"]
plot_intraday_volume_and_returns(test_args)

plt.show()


