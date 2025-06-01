import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_rebloom_lineage(path="logs/rebloom_summary_log.csv"):
    df = pd.read_csv(path)
    G = nx.DiGraph()

    ticks = sorted(df["tick_id"].astype(str).unique())
    fig, ax = plt.subplots(figsize=(10, 7))

    def update(tick):
        ax.clear()
        partial = df[df["tick_id"] <= tick]
        G.clear()
        for _, row in partial.iterrows():
            seed = row["seed_id"]
            ancestry = row["ancestry_tag"]
            G.add_node(seed)
            if ancestry != "untagged":
                G.add_edge(ancestry, seed)

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color="lightgreen", edge_color="gray", arrows=True, ax=ax)
        ax.set_title(f"🕸 Rebloom Lineage Overlay – Tick {tick}")

    ani = animation.FuncAnimation(fig, update, frames=ticks, repeat=False, interval=500)
    ani.save("visuals/rebloom_lineage_animation.gif", writer="pillow")
    plt.close()

if __name__ == "__main__":
    animate_rebloom_lineage()
