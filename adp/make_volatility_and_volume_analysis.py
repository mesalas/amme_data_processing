import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from adp.readers.trades_reader import TradesData
from adp.assign_bar_quantile import assign_percentiles,make_quantile_windows
#from make_network import make_traded_volume_matrix,make_directed_graph,save_directed_graph
#from make_micro_network_analysis import calculate_total_node_volume,normalize_directional_graph
import networkx as nx
import seaborn as sns
#import community
#from nxviz.plots import CircosPlot
import copy
import sys

def make_traded_volume_matrix(agents_log, cutoff):

    #agents_log  # Read matched orders files

    # Make matrix of trades between agents and list of agent names. The number of trades will be used as the strength of the connections
    # The names will be the nodes
    agent_volumes = agents_log.make_directional_agent_pair_volumes()
    groups = agent_volumes.groupby("active_agent")
    total_volume_for_first_agent = groups.transform(np.sum)
    #if normalize == True:
    #    agent_volumes["volume"] = agent_volumes["volume"] / total_volume_for_first_agent["volume"]

    nodes = agent_volumes["active_agent"].append(agent_volumes["passive_agent"]).unique()
    edges = [t for t,total in zip(agent_volumes.itertuples(index=False, name=None),total_volume_for_first_agent["volume"]) if t[2] > cutoff*total]# and t[0] != t[1]]

    return nodes,edges

def match_bars_and_trades(trades_path, bars_path, active_passive_table_path, heatmap_path,heatmap_csv_path,target_quant,n_quantiles = 20):
    matched_orders = TradesData("amme_matched_orders")
    matched_orders.read_data(trades_path)
    
    # we want to calculate network properties in different "regimes" these are found by assigning quantiles to each bar
    
    bars = pd.read_csv(bars_path) # Read Bars

    # Assign Quantiles and make windows
    bars = assign_percentiles(bars, n_quantiles)
    windows = make_quantile_windows(bars, target_quant)

    matched_orders_copy = copy.deepcopy(matched_orders) # We copy the trades data objet so we can modify it

        # Read trades
    matched_orders_copy.trades.index = matched_orders_copy.trades["DateTime"] # make datetime index



    #select trades in windows define by quantiles
    matched_orders_copy.select_data_in_windows(windows)
    
    #TODO: passive active stats. Are we using this?
    #passive_active_stat = matched_orders_copy.passive_active_stat()
    #passive_active_stat.to_csv(active_passive_table_path)

    #community.best_partition()
    # aggregate on agent classes
    matched_orders_copy.strip_agent_numbers()

    nodes,edges = make_traded_volume_matrix(matched_orders_copy, cutoff = 0.0)

    directed_graph = nx.DiGraph()  # Rows are the active agent
    directed_graph.add_nodes_from(nodes)
    directed_graph.add_weighted_edges_from(edges)




    volume_table = nx.to_pandas_adjacency(directed_graph, weight="weight")
    volume_table.to_csv(heatmap_csv_path)
    fig,ax = plt.subplots()
    ax = sns.heatmap(volume_table.apply(np.log10).replace([np.inf, -np.inf], np.nan).fillna(0), linewidths=.5, ax = ax)
    fig.tight_layout()
    fig.savefig(heatmap_path)

        #TODO: impliment
        # Calculate the total volume traded by each node
        #calculate_total_node_volume(directed_graph)
        #normalize_directional_graph(directed_graph)

if __name__ == "__main__":
    trades_path = sys.argv[1]
    bars_path = sys.argv[2]
    active_passive_table_path = sys.argv[3]
    heatmap_path = sys.argv[4]
    heatmap_csv_path = sys.argv[5]
    write_quantiles = int(sys.argv[6])
    match_bars_and_trades(trades_path,
                          bars_path,
                          active_passive_table_path,
                          heatmap_path,
                          heatmap_csv_path,
                          write_quantiles,
                          n_quantiles = 20)