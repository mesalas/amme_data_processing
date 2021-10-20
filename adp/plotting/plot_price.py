import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import pandas as pd

def plot_price(args):
    out = args[0]
    ins = args[1:]
    fig, ax = plt.subplots(5, figsize=(7, 15))
    for path in ins:
        bars = pd.read_csv(path)
        bars.plot( x = "SimTime", y = "Close", ax = ax[0])
        ax[1].plot(bars["SimTime"],bars["Close"].diff())
        bars.plot(x="SimTime", y="Trade Volume", ax=ax[2])
        pd.plotting.autocorrelation_plot(bars["Close"].diff()[1:], ax = ax[3])
        pd.plotting.autocorrelation_plot(bars["Close"].diff()[1:].abs(), ax=ax[4])

    #limit the x axis for the first 30 days
    for a in [ax[3],ax[4]]:
        a.set_xlim([0,30])
    fig.savefig(out)

def plot_intraday_bars(args):
    out = args[0]
    ins = args[1:]
    fig, ax = plt.subplots(5, figsize=(7, 15))
    for path in ins:
        bars = pd.read_csv(path)
        bars.plot( x = "SimTime", y = "Close", ax = ax[0])
        ax[1].plot(bars["SimTime"], bars["Close"].diff())
        bars.plot(x="SimTime", y="Trade Volume", ax=ax[2])

        bars["DateTime"] = pd.to_datetime(bars["DateTime"])

        daily_grouped_bars = bars.groupby(
            pd.Grouper(key="DateTime",
                       freq='B'
                       ), sort=False
        )
        try:
            acfs = list()
            for name, group in daily_grouped_bars:
                lags = 30
                returns = group["Close"].diff()[1:]
                acf = pd.DataFrame([returns.autocorr(lag= l) for l in range(1,lags)])
                acfs.append(acf)
            acfs = pd.concat(acfs, axis = 1)

            ax[3].plot(acfs,'k.',alpha = 0.1)
            ax[3].plot(acfs.mean(axis = 1))

            acfs = list()
            for name, group in daily_grouped_bars:
                lags = 30
                returns = group["Close"].diff()[1:].abs()
                acf = pd.DataFrame([returns.autocorr(lag=l) for l in range(1, lags)])
                acfs.append(acf)
            acfs = pd.concat(acfs, axis=1)

            ax[4].plot(acfs, 'k.',alpha=0.1)
            ax[4].plot(acfs.mean(axis=1))
        except:
            print("error when making auto correlations")


    #limit the x axis for the first 30 days
    for a in [ax[3],ax[4]]:
        a.set_xlim([0,30])
    fig.savefig(out)


if __name__ == "__main__":
    plot_price(sys.argv[1:])
