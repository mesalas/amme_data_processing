import numpy as np
import pandas as pd
def date_time_to_sim_time(data_frame: pd.DataFrame, open_time: str = "9:30:00", length_of_trading_day: str = "6:30:00") -> pd.DataFrame:
    """

    :rtype: pd.DataFrame
    """
    business_day_number = data_frame.groupby(pd.Grouper(key = "DateTime",freq = 'B')).ngroup()

    data_frame["SimTime"] = business_day_number + (
                data_frame["DateTime"] - data_frame["DateTime"].dt.floor("D") - pd.Timedelta(
            open_time)).values.astype(np.float64) * 1e-9 / pd.Timedelta(length_of_trading_day).seconds
    return data_frame