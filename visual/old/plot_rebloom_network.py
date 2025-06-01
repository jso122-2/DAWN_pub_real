import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def plot_rebloom_network(path="logs/rebloom_summary_log.csv"):
    df = pd.read_csv(path)
    G = nx.DiGraph()

    for _, row in df.iterrows():
        seed = row["seed_id"]
        ancestry = row["ancestry_tag"]
        G.add_node(seed)
        if ancestry != "untagged":
            G.add_edge(ancestry, seed)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=600, node_color="skyblue", edge_color="gray", arrows=True)
    plt.title("🌱 Rebloom Lineage Network")
    plt.tight_layout()
    plt.savefig("visuals/rebloom_network.png")
    plt.show()

if __name__ == "__main__":
    plot_rebloom_network()
