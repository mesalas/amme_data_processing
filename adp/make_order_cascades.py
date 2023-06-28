import sys

import pandas as pd
import networkx as nx
import numpy as np
from adp.timemethods import date_time_to_sim_time

def get_nodes(df: pd.DataFrame):
    nodes_df = df[["SimTime", "active_id", "active_orderQty", "active_avgPrice", 'active_agent', 'passive_fillQty', 'passive_fillPrice']].groupby(by = ["active_id"]).agg(simTime = pd.NamedAgg(column="SimTime", aggfunc="first"),
    averagePrice = pd.NamedAgg(column="active_avgPrice", aggfunc="first"),
    size = pd.NamedAgg(column='passive_fillQty', aggfunc="sum"),
    agent = pd.NamedAgg(column='active_agent', aggfunc="first"),
    trades = pd.NamedAgg(column='active_agent', aggfunc="count"),
    price_low = pd.NamedAgg(column='passive_fillPrice', aggfunc="min"),
    price_high = pd.NamedAgg(column='passive_fillPrice', aggfunc="max"))
    return nodes_df

def get_edges(df: pd.DataFrame):
    matches_of_intrest = df[(df["triggering order"] != "none") &
    (df["triggering order"] != "zi trigger") &
    (df["trigger"] != "eod2")&
    (df["trigger"] != "eod1")&
    (df["triggering order"] != "passive trigger") & (df["triggering order"].notna())]
    return matches_of_intrest

def make_node_to_group_map(S):
    group_no = 0
    node_to_group_map = dict()
    for subgraph in S:
        [node_to_group_map.update({node : group_no}) for node in subgraph.nodes]
        group_no += 1
    return node_to_group_map

def assign_group(row,node_to_group_map):
    try:
        group = node_to_group_map[row["active_id"]]
    except:
        group = np.NaN
    return group
def assign_order_to_group(df: pd.DataFrame):
    nodes_df = get_nodes(df)
    G = nx.Graph()
    G.add_nodes_from([(i, nodes_df.loc[i].to_dict()) for i in nodes_df.index])
    matches_of_intrest = get_edges(df)
    G.add_edges_from( list(matches_of_intrest[["active_id", "triggering order"]].to_records(index=False)))
    # Make sub graphs of connected orders. Each subgraph is a cluster of orders
    S = [G.subgraph(c).copy() for c in nx.connected_components(G) if len(c) > 1]

    node_to_group_map = make_node_to_group_map(S)
    df["group"] = np.NaN
    df["group"] = df.apply(lambda row : assign_group(row,node_to_group_map), axis=1)
def MergeMatchedOrdersAndMarketOrders(matched_orders, market_orders):
    """
    This function merges two DataFrames: matched_orders and market_orders, which represent logs of matched orders and all orders
    sent to a simulated stock market respectively. It combines information to identify if an order in the matched_orders log was
    triggered by a previous trade from the market_orders log. If an order does not have a corresponding trigger in the market_orders log,
    it is labeled as 'no trigger'.

    Parameters:
    matched_orders (pd.DataFrame): DataFrame containing the matched orders log.
    market_orders (pd.DataFrame): DataFrame containing the all orders log.

    Returns:
    pd.DataFrame: The updated matched_orders DataFrame after merging with relevant information from market_orders.
    """

    market_orders = market_orders.rename(columns={"OrderID": "active_id"})
    market_orders = market_orders[market_orders["Action"] == "NEW"]
    matched_orders = matched_orders.merge(
        market_orders[["active_id", "trigger", "triggering order", "OrderPrice", "OrderQty", "Method"]], on='active_id',
        how='left')

    # Fill NaN values with "no trigger"
    #matched_orders["trigger"].fillna("no trigger", inplace=True)
    #matched_orders["triggering order"].fillna("no trigger", inplace=True)

    return matched_orders.rename(columns=lambda x: x.lstrip()) #strip any leading whitespaces from columns

def MatchOrdersAndVolatilityQuantile(matched_orders, bars):
    bar_length = len(bars)
    bar_row_no = 1 #starting row
    matched_orders["quantile"] = 0
    for row_no,row in enumerate(matched_orders.itertuples()):
        while row.SimTime >= bars.at[bar_row_no, "SimTime"]:
            if bar_row_no == bar_length -1 :
                matched_orders.at[row_no, "quantile"] = bars.at[bar_length -1,"quantile"]
                #print("reached end")
                break
            else:
                bar_row_no += 1

        if row.SimTime < bars.at[bar_row_no,"SimTime"]:
            #print("matched row {} with bar row {}".format(row_no,bar_row_no))
            matched_orders.at[row_no, "quantile"] = bars.at[bar_row_no,"quantile"]
def ReadMatchedOrders(path):
    matched_orders = pd.read_csv(path)
    matched_orders["DateTime"] = pd.to_datetime(matched_orders["DateTime"], format="%Y-%m-%d %H:%M:%S.%f")
    matched_orders = date_time_to_sim_time(matched_orders)
    return matched_orders
def ReadMarketOrders(path):
    market_orders = pd.read_csv(path)
    market_orders["DateTime"] = pd.to_datetime(market_orders["DateTime"], format="%Y-%m-%d %H:%M:%S.%f")
    market_orders = date_time_to_sim_time(market_orders)
    market_orders[["trigger", "triggering order"]] = market_orders["Comment"].str.split(":", expand = True)
    market_orders.loc[market_orders["triggering order"] == "", "triggering order"] = "none"
    return market_orders

def get_max_order_generation(orders,first_order_id):
    group_lenght = 1
    for idx,order in orders.iterrows():
        if idx == first_order_id:
            continue

        n = 1
        triggering_order = order["triggering order"]
        while triggering_order != first_order_id:
            triggering_order = orders.loc[triggering_order]["triggering order"]
            n += 1
        if n > group_lenght:
            group_lenght = n
    return group_lenght
def get_grouped_trades(df: pd.DataFrame):
    # Aggregate Groups and calculate parameters
    grouped_trades = df[~df["group"].isna()].groupby(by="group")
    groups_list = list()
    for name, group in grouped_trades:
        orders = group.groupby(by="active_id").last()
        first_order_id = group["active_id"].iloc[0]
        max_order_gen = get_max_order_generation(orders, first_order_id)

        sim_time = group["SimTime"].iloc[0]
        last_sim_time = group["SimTime"].iloc[-1]
        trades = len(group["SimTime"])
        n_orders = len(group['active_id'].unique())
        mean_price = group['active_fillPrice'].mean()
        high_price = group['active_fillPrice'].max()
        low_price = group['active_fillPrice'].min()

        first_price = group['active_fillPrice'].iloc[0]
        last_price = group['active_fillPrice'].iloc[-1]
        volume_traded = group['passive_fillQty'].sum()
        # Order types
        orders_of_interest = group[group["trigger"] == "momentum entry"]
        momentum_fraction = float(len(orders_of_interest)) / float(trades)

        orders_of_interest = group[group["trigger"] == "reversion entry"]
        reversion_fraction = float(len(orders_of_interest)) / float(trades)

        orders_of_interest = group[group["trigger"] == "stop loss"]
        stoploss_fraction = float(len(orders_of_interest)) / float(trades)

        orders_of_interest = group[group["trigger"] == "take profit"]
        takeprofit_fraction = float(len(orders_of_interest)) / float(trades)
        # Buy side stats
        select_buy = group[group['active_side'] == "BUY"]
        buy_volume = select_buy['passive_fillQty'].sum()
        buy_avg_price = select_buy['active_fillPrice'].mean()
        if len(select_buy) > 0:
            first_buy_price = select_buy['active_fillPrice'].iloc[0]
            last_buy_price = select_buy['active_fillPrice'].iloc[-1]
        else:
            first_buy_price = np.NaN
            last_buy_price = np.NaN
        # Sell side stats
        select_sell = group[group['active_side'] == "SELL"]
        sell_volume = select_sell['passive_fillQty'].sum()
        sell_avg_price = select_sell['active_fillPrice'].mean()
        if len(select_sell) > 0:
            first_sell_price = select_sell['active_fillPrice'].iloc[0]
            last_sell_price = select_sell['active_fillPrice'].iloc[-1]
        else:
            first_sell_price = np.NaN
            last_sell_price = np.NaN

        # First order stats
        first_order_id = group['active_id'].unique()[0]
        first_order_side = group[group['active_id'] == first_order_id]['active_side'].iloc[0]
        first_order_quantile = group[group['active_id'] == first_order_id]['quantile'].iloc[0]

        first_order_first_price = group[group['active_id'] == first_order_id]['active_fillPrice'].iloc[0]
        first_order_last_price = group[group['active_id'] == first_order_id]['active_fillPrice'].iloc[-1]
        first_order_total_trade_volume = group[group['active_id'] == first_order_id]['passive_fillQty'].sum()
        first_order_total_trades = len(group[group['active_id'] == first_order_id]["SimTime"])
        first_order_size = group[group['active_id'] == first_order_id]['active_orderQty'].iloc[0]

        groups_list.append(pd.DataFrame({"group": name,
                                         "SimTime": sim_time,
                                         "last SimTime": last_sim_time,
                                         "duration": last_sim_time - sim_time,
                                         "trades": trades,
                                         "number of orders": n_orders,
                                         "mean price": mean_price,
                                         "low price": low_price,
                                         "high price": high_price,
                                         "first price": first_price,
                                         "last price": last_price,
                                         "price diff": high_price - low_price,
                                         "first last price diff": last_price - first_price,
                                         "volume": volume_traded,
                                         "buy volume": buy_volume,
                                         "sell volume": sell_volume,
                                         "mean buy price": buy_avg_price,
                                         "first buy price": first_buy_price,
                                         "last buy price": last_buy_price,
                                         "first last buy diff": (last_buy_price - first_buy_price),
                                         "mean sell price": sell_avg_price,
                                         "first sell price": first_sell_price,
                                         "last sell price": last_sell_price,
                                         "first last sell diff": (last_sell_price - first_sell_price),
                                         "first order size": first_order_size,
                                         "first order traded volume": first_order_total_trade_volume,
                                         "first order number of trades": first_order_total_trades,
                                         "first order first price": first_order_first_price,
                                         "first order last price": first_order_last_price,
                                         "first order price diff": first_order_last_price - first_order_first_price,
                                         "momentum entry fraction": momentum_fraction,
                                         "reversion entry fraction": reversion_fraction,
                                         "stoploss fraction": stoploss_fraction,
                                         "takeprofit fraction": takeprofit_fraction,
                                         "first order side": first_order_side,
                                         "first order quantile": first_order_quantile,
                                         "cascade length": max_order_gen}, index=[name]))

    return pd.concat(groups_list)
def make_order_cascades(args):
    # inputs are:
    # matched orders
    # market orders
    # trade bars
    # output file name
    matched_orders_name_and_path, market_orders_name_and_path, trade_bars_name_and_path, out_put_file_name_and_path = args
    matched_orders = MergeMatchedOrdersAndMarketOrders(
        matched_orders = ReadMatchedOrders(matched_orders_name_and_path),
        market_orders=ReadMarketOrders(market_orders_name_and_path)
                                                       )
    MatchOrdersAndVolatilityQuantile(matched_orders,pd.read_csv(trade_bars_name_and_path))
    assign_order_to_group(matched_orders)
    get_grouped_trades(matched_orders).to_csv(out_put_file_name_and_path)

if __name__ == "__main__":
    make_order_cascades(sys.argv[1:])
