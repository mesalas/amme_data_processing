import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys
import pandas as pd
import seaborn as sns


def plot_average_agent_pos(args):
    out_file = args[0]
    in_file = args[1]
    agent_pos = pd.read_csv(in_file)
    agent_names = agent_pos.columns[agent_pos.columns != "DateTime"]
    agent_names = agent_names[agent_names != "SimTime"]
    agent_types = pd.Series([s.split('-')[0] for s in agent_names]).unique()
    fig,ax = plt.subplots()
    for agent_type in agent_types:
        average_pos = agent_pos[[col for col in agent_pos.columns if col.startswith(agent_type)]].sum(axis = 1)
        ax.plot(average_pos.groupby(average_pos.index // 120).mean())
    plt.show()

def plot_agent_pos_correlation(args):
    out_file = args[0]
    in_file = args[1]
    agent_pos = pd.read_csv(in_file)
    agent_names = agent_pos.columns[agent_pos.columns != "DateTime"]
    agent_names = agent_names[agent_names != "SimTime"]
    agent_types = pd.Series([s.split('-')[0] for s in agent_names]).unique()

    agent_classes = [["MarketMaker", "ZeroInfo", "LongShort", "SectorRotate"],
                     ["MarketMaker", "ZeroInfo","Aggressor", "OpeningRange", "Breakout"]]
    for agent_class in agent_classes:

        average_pos = pd.DataFrame({agent_type : agent_pos[[col for col in agent_pos.columns if col.startswith(agent_type)]].sum(axis = 1) for agent_type in agent_class})
        sns.pairplot(average_pos.groupby(average_pos.index // 120).mean(), kind = "reg",corner= True, plot_kws=dict(marker=".", scatter_kws={"alpha" :0.1}))
    plt.show()
plot_agent_pos_correlation(["dum", "test_data/DEF_NYSE@0_Agent_Pos.csv.gz"])

plot_average_agent_pos(["dum", "test_data/DEF_NYSE@0_Agent_Pos.csv.gz"])