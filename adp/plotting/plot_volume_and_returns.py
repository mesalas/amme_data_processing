import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import pandas as pd

def plot_volume_and_returns(args):
    out = args[0]
    ins = args[1:]
    fig, ax = plt.subplots(3)
    for path in ins:
        bars = pd.read_csv(path)
        bars = bars[bars["SimTime"] >= 5]
        ax[0].plot(bars["SimTime"],bars["Close"].diff())
        ax[1].plot(bars["SimTime"],bars["Trade Volume"])
        volume = bars["Trade Volume"][1:]
        #volume = (volume - volume.mean())/volume.std()
        abs_returns = bars["Close"].diff()[1:].abs()
        #abs_returns = ((abs_returns -abs_returns.mean())/abs_returns.std())
        ax[2].plot(volume,abs_returns, '.')


def plot_intraday_volume_and_returns(args):
    out = args[0]
    ins = args[1:]
    fig, ax = plt.subplots(3)
    for path in ins:
        bars = pd.read_csv(path)
        bars = bars[bars["SimTime"] >= 5]
        bars.index = pd.to_datetime(bars["DateTime"])
        #bars = bars.between_time("9:30", "15:40")
        ax[0].plot(bars["SimTime"],bars["Close"].diff())
        ax[1].plot(bars["SimTime"],bars["Trade Volume"])
        volume = bars["Trade Volume"][1:]
        #volume = (volume - volume.mean())/volume.std()
        abs_returns = bars["Close"].diff()[1:].abs()
        #abs_returns = ((abs_returns -abs_returns.mean())/abs_returns.std())
        ax[2].plot(volume,abs_returns, '.', alpha = 0.1)

        # bars["DateTime"] = pd.to_datetime(bars["DateTime"])
        #
        # daily_grouped_bars = bars.groupby(
        #     pd.Grouper(key="DateTime",
        #                freq='B'
        #                ), sort=False
        # )
        #
        # acfs = list()
        # for name, group in daily_grouped_bars:
        #     lags = 30
        #     returns = group["Close"].diff()[1:]
        #     acf = pd.DataFrame([returns.autocorr(lag= l) for l in range(1,lags)])
        #     acfs.append(acf)
        # acfs = pd.concat(acfs, axis = 1)
        #
        # ax[3].plot(acfs,'k.',alpha = 0.1)
        # ax[3].plot(acfs.mean(axis = 1))
        #
        # acfs = list()
        # for name, group in daily_grouped_bars:
        #     lags = 30
        #     returns = group["Close"].diff()[1:].abs()
        #     acf = pd.DataFrame([returns.autocorr(lag=l) for l in range(1, lags)])
        #     acfs.append(acf)
        # acfs = pd.concat(acfs, axis=1)
        #
        # ax[4].plot(acfs, 'k.',alpha=0.1)
        # ax[4].plot(acfs.mean(axis=1))
    #
    #
    # #limit the x axis for the first 30 days
    # for a in [ax[3],ax[4]]:
    #     a.set_xlim([0,30])
    # fig.savefig(out)


if __name__ == "__main__":
    plot_price(sys.argv[1:])
