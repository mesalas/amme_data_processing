import pandas as pd
import sys

def make_intraday_returns_autocorrelation(args):
    path, output, absolute = args
    absolute = bool(absolute)
    bars = pd.read_csv(path)
    lags = 30
    bars["DateTime"] = pd.to_datetime(bars["DateTime"])
    daily_grouped_bars = bars.groupby(
        pd.Grouper(key="DateTime",
                   freq='B'
                   ), sort=False
    )
    try:
        acfs = list()
        for name, group in daily_grouped_bars:
            if absolute == True:
                returns = group["Close"].diff().abs()[1:]
            else:
                returns = group["Close"].diff()[1:]

            acf = pd.DataFrame([returns.autocorr(lag=l) for l in range(1, lags)])
            acfs.append(acf)
        acfs = pd.concat(acfs, axis=1)
    except:
        print("error when making auto correlations")

    acfs.mean(axis=1).to_csv(output)



if __name__ == "__main__":
    make_intraday_returns_autocorrelation(sys.argv[1:])