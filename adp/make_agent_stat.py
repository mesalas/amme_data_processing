from adp.readers.agent_stat_reader import AgentsData
from adp.timemethods import date_time_to_sim_time
import sys

def make_agent_stat(args):
    path, freq, stat, output = args
    agent_data = AgentsData(data_type="amme_agents")
    agent_data.read_data(path=path, agent_statistic= stat)
    date_time_to_sim_time(agent_data.resample(freq = freq)).to_csv(output, index = False)

if __name__ == "__main__":
    make_agent_stat(sys.argv[1:])