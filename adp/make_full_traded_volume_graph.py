from adp.readers.trades_reader import TradesData
import networkx as nx


def make_traded_volume_matrix(agents_log, cutoff):

    #agents_log  # Read matched orders files

    # Make matrix of trades between agents and list of agent names. The number of trades will be used as the strength of the connections
    # The names will be the nodes
    agent_volumes = agents_log.make_directional_agent_pair_volumes()
    #if normalize == True:
    #    agent_volumes["volume"] = agent_volumes["volume"] / total_volume_for_first_agent["volume"]

    nodes = agent_volumes["active_agent"].append(agent_volumes["passive_agent"]).unique()
    edges = [t for t,total in zip(agent_volumes.itertuples(index=False, name=None),total_volume_for_first_agent["volume"]) if t[2] > cutoff*total]# and t[0] != t[1]]

    return nodes,edges

def make_full_traded_volume_graph(trades_path : str, full_traded_graph_path: str) -> None:
    matched_orders = TradesData("amme_matched_orders")
    matched_orders.read_data(trades_path)
    
    nodes,edges = make_traded_volume_matrix(matched_orders, cutoff = 0.0)

    directed_graph = nx.DiGraph()  # Rows are the active agent
    directed_graph.add_nodes_from(nodes)
    directed_graph.add_weighted_edges_from(edges)

    nx.write_gexf(directed_graph, full_traded_graph_path)

if __name__ == "__main__":
    trades_path = sys.argv[1]
    full_graph_out_path = sys.argv[2]
    make_full_traded_volume_graph(trades_path,
                          full_graph_out_path)