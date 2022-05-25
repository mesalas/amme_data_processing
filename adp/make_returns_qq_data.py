import pandas as pd
import sys
from scipy.stats import probplot

def make_returns_qq_data(args):
    path, output = args
    bars = pd.read_csv(path)
    returns = bars["Close"].diff()[1:]
    qq = probplot(returns.values, dist='norm')
    pd.DataFrame({"qq" : qq[0][0], "qq returns" : qq[0][1]}).to_csv(output, index=False)


if __name__ == "__main__":
    make_returns_qq_data(sys.argv[1:])