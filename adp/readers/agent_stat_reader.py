import pandas as pd
import numpy as np

class AgentsData:
    def __init__(self, data_type):
        if data_type == "amme_agents":
            self.timestamp_col_name = "Nanos"
            self.timestamp_units = "ns"

            self.read_data = self.read_amme_agents_data
            #self.resample_data = self.resample_amme_agents_data
            self.market_open = "9:30:00"
            self.agent_data_labels =["Pos","PL","Vol","CashValue"]
        # elif data_type == "trades":
        #     self.read_data = self.read_nyse_trades_data
        #     self.resample_data = self.resample_trades_data

        else:
            print("{}: unknown data type".format(data_type))

    def read_amme_agents_data(self, path, agent_statistic):
        if agent_statistic in self.agent_data_labels:
            load_csv_kw_args = {"filepath_or_buffer" : path,
                                "usecols" : ["DateTime", "AgentName",agent_statistic]}
            self.agent_statistic = agent_statistic
            self.agent_statistic = pd.read_csv(**load_csv_kw_args)

            try:
                self.agent_statistic["DateTime"] = pd.to_datetime(self.agent_statistic["DateTime"],
                                                                  format="%Y-%m-%d %H:%M:%S.%f")  # convert datetime string to datetime object
            except ValueError:
                print("Got value error converting time")
                try:
                    print("trying to skip last line")
                    self.agent_statistic = pd.read_csv(**load_csv_kw_args, skipfooter=1)
                    self.agent_statistic["DateTime"] = pd.to_datetime(self.agent_statistic["DateTime"],
                                                                      format="%Y-%m-%d %H:%M:%S.%f")
                except:
                    raise Exception("Error reading")

    def _resample_agent_stat(self, freq):
        daily_grouped_agent_stat = self.agent_statistic.groupby(
            pd.Grouper(key="DateTime",
                       freq='B'
                       ), sort=False
        )

        result_df = pd.DataFrame()
        for name, group in daily_grouped_agent_stat:
            pivot_pos = group.pivot_table(values = self.agent_statistic, index="DateTime", columns="AgentName", aggfunc = "last").ffill().resample(freq).last()
            pivot_pos.columns = pivot_pos.columns.droplevel()
            result_df = pd.concat([result_df, pivot_pos])
        return result_df.ffill().fillna(0.0)

    def _resample_agent_stat_daily(self):
        daily_grouped_agent_stat = self.agent_statistic.groupby(
            pd.Grouper(key="DateTime",
                       freq='B'
                       ), sort=False
        )

        result_df = pd.DataFrame()
        for name, group in daily_grouped_agent_stat:
            pivot_pos = group.pivot_table(values = self.agent_statistic, index="DateTime", columns="AgentName", aggfunc = "last").ffill().tail(1) 
            pivot_pos.columns = pivot_pos.columns.droplevel()
            result_df = pd.concat([result_df, pivot_pos])
        return result_df.ffill().fillna(0.0)


    def resample(self, freq):
        agent_statistics = self._resample_agent_stat(freq)
        agent_statistics["DateTime"] = agent_statistics.index
        return agent_statistics.reset_index(drop=True)
    
    def resample_daily(self):
        
        agent_statistics = self._resample_agent_stat_daily()
        agent_statistics["DateTime"] = agent_statistics.index
        return agent_statistics.reset_index(drop=True)


