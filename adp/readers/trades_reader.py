import pandas as pd
import numpy as np

class TradesData:
    def __init__(self, data_type):
        if data_type == "amme_matched_orders":
            self.active_fill_price_col = " active_fillPrice"  # note theres a leading space
            self.passive_fill_qty_col = " passive_fillQty"
            self.timestamp_col_name = "Nanos"
            self.timestamp_units = "ns"
            self.active_agent_col = "active_agent"
            self.passive_agent_col = "passive_agent"

            self.read_data = self.read_amme_matched_orders_data
            self.resample_data = self.resample_amme_matched_orders_data
            self.market_open = "9:30:00"
        # elif data_type == "trades":
        #     self.read_data = self.read_nyse_trades_data
        #     self.resample_data = self.resample_trades_data

        else:
            print("{}: unknown data type".format(data_type))

    def read_amme_matched_orders_data(self, path):
        load_csv_kw_args = {"filepath_or_buffer" : path,
                            "usecols" : ["DateTime",
                                         self.active_fill_price_col,
                                         self.passive_fill_qty_col,
                                         self.active_agent_col,
                                         self.passive_agent_col]
                            }

        self.trades = pd.read_csv(**load_csv_kw_args)



        try:
            self.trades["DateTime"] = pd.to_datetime(self.trades["DateTime"], format="%Y-%m-%d %H:%M:%S.%f") # convert datetime string to datetime object
        except ValueError:
            print("Got value error converting time")
            try:
                print("trying to skip last line")
                self.trades = pd.read_csv(**load_csv_kw_args, skipfooter=1)
                self.trades["DateTime"] = pd.to_datetime(self.trades["DateTime"], format="%Y-%m-%d %H:%M:%S.%f")
            except:
                raise Exception("Error reading")
    def make_intraday_bars(self,freq):
        #group on days

        daily_grouped_trade_price = self.trades.groupby(
            pd.Grouper(key="DateTime",
                       freq='B'
                       ), sort=False
        )

        bars = list()
        for name, group in daily_grouped_trade_price:
            group = group.set_index("DateTime", drop=False)
            group = group.resample(freq
                                   )

            bars.append(self._make_bars_from_agg(group))
        bars = pd.concat(bars)
        bars["DateTime"] = bars.index
        return bars.reset_index(drop = True)

    def _make_bars_from_agg(self, resampled):
        price = self.active_fill_price_col
        volume = self.passive_fill_qty_col
        resampled_data = resampled.agg({
            "DateTime": "last"})
        #   "Symbol": "last",
        resampled_data["Mean"] = resampled.agg({
            price: "mean"})
        resampled_data["High"] = resampled.agg({
            price: lambda x: x.max()})
        resampled_data["Low"] = resampled.agg({
            price: lambda x: x.min()})
        resampled_data["Open"] = resampled.agg({
            price: "first"})
        resampled_data["Close"] = resampled.agg({
            price: "last"})
        resampled_data["Trade Volume"] = resampled.agg({volume: "sum"})
        resampled_data["Trades"] = resampled.agg({
            volume: "count"})
        resampled_data["First"] = resampled.agg({
            "DateTime": "first"})
        resampled_data["Last"] = resampled.agg({
            "DateTime": "last"})
        return resampled_data

    def resample_amme_matched_orders_data(self,freq):

        resampled = self.trades.set_index("DateTime", drop = False).resample(freq)
        resampled_data = self._make_bars_from_agg(resampled)
        resampled_data["DateTime"] = resampled_data.index + pd.Timedelta(self.market_open)
        return resampled_data.reset_index(drop = True)

        #resampled_data["Dollar Volume"] = resampled.agg({"Dollar Volume": "sum"})

    
#     def read_nyse_trades_data(self,path, symbol = None, compression = "gzip"):
#         """
#         Method for reading NYSE TAQ data
#         It is assumed that the data is compressed
#         """
#         chunks = pd.read_csv(path, sep="|", compression=compression, usecols = ["Time","Symbol", "Trade Price", "Trade Volume", "Exchange"], chunksize=10000000)
#         self.data = pd.concat([chunk[chunk["Symbol"] == symbol] for chunk in chunks])
#         self.data["Dollar Volume"] = self.data["Trade Volume"] * self.data["Trade Price"]
#         self.date_str = self.get_date(path)
#         self.convert_time_stamps()
#
#
#     def convert_time_stamps(self):
#         #Convert timestamp to datetime and index
#         self.data.index = pd.DatetimeIndex(
#             pd.to_datetime(
#                 self.data.Time.apply(lambda x : self.date_str + " " + str(x)),
#                  format = "%Y%m%d %H%M%S%f"),
#                  name = "DateTime"
#                  )
#
#         one_sec_time_delta = pd.Timedelta(1,"s")
#         day_time_stamp = pd.to_datetime(self.date_str)
#
#         self.data.Time = ((self.data.index-day_time_stamp)/one_sec_time_delta).values
#
#     def get_date(self, path_string):
#         return path_string.split("_")[-1].split(".")[0]
#
#     def select_between_open_and_close(self,start,end):
#         self.data = self.data.between_time(start,end)
#     def resample_nbbo_data(self, freq):
#         resampled_data = self.data.resample(freq).last().ffill()
#         one_sec_time_delta = pd.Timedelta(1,"s")
#         day_time_stamp = pd.to_datetime(self.date_str)
#
#         resampled_data.Time = ((resampled_data.index-day_time_stamp)/one_sec_time_delta).values
#         return resampled_data
#
#     def resample_trades_data(self,freq):
#         resampled = self.data.resample(freq)
#         resampled_data =resampled.agg({
#             "Time" : "last"})
#           #   "Symbol": "last",
#         resampled_data["Trade Price"] = resampled.agg({
#             "Trade Price": "mean"})
#         resampled_data["High"] = resampled.agg({
#             "Trade Price": lambda x : x.max()})
#         resampled_data["Low"]= resampled.agg({
#             "Trade Price": lambda x: x.min()})
#         resampled_data["Open"] = resampled.agg({
#             "Trade Price": "first"})
#         resampled_data["Close"] = resampled.agg({
#             "Trade Price": "last"})
#         resampled_data["Trade Volume"] =  resampled.agg({"Trade Volume": "sum"})
#         resampled_data["Trades"] = resampled.agg({
#             "Trade Price": "count"})
#         resampled_data["Dollar Volume"] = resampled.agg({"Dollar Volume": "sum"})
#
#         one_sec_time_delta = pd.Timedelta(1,"s")
#         day_time_stamp = pd.to_datetime(self.date_str)
#
#         resampled_data.Time = ((resampled_data.index-day_time_stamp)/one_sec_time_delta).values
#
#         return resampled_data
#
# def convert_taq(data_type,path,symbol):
#     taq_data = DailyTaqData(data_type)
#     taq_data.read_data(path, symbol)
#     taq_data.select_between_open_and_close("9:30:00", "16:00:00")
#     taq_data.data.to_csv("test_out/" + taq_data.date_str + "_"+ symbol + "_" + data_type + ".csv")
#
#     resample_freqs = {"1min" : "1T", "1sec": "1s"}
#
#     for time, freq in resample_freqs.items():
#         taq_data.resample_data(freq).to_csv("test_out/" + taq_data.date_str + "_"+ symbol + "_" + data_type + "_" + time +".csv")
