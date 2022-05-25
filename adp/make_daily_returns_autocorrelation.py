import pandas as pd
import sys

def make_daily_returns_autocorrelation(args):
    path, output, absolute = args
    absolute = bool(absolute)
    bars = pd.read_csv(path)
    lags = 30

    returns = bars["Close"].diff()[1:]

    if absolute == True:
        returns = returns.abs()
    acf = pd.DataFrame([returns.autocorr(lag=l) for l in range(1, lags)])
    acf.to_csv(output)


if __name__ == "__main__":
    make_daily_returns_autocorrelation(sys.argv[1:])