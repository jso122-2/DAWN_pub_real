import matplotlib.pyplot as plt
import networkx as nx
from lineage_tools import load_all_flowers, build_lineage_graph

def draw_lineage_tree(flowers=None, save_path="juliet_flowers/cluster_report/lineage_tree.png"):
    if flowers is None:
        flowers = load_all_flowers()

    graph, roots = build_lineage_graph(flowers)
    G = nx.DiGraph()

    for ancestor, children in graph.items():
        for child in children:
            G.add_edge(ancestor, child)

    if len(G.nodes) == 0:
        print("[LineageGraph] ❌ No rebloom links found to visualize.")
        return

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=False, node_color="lightblue", node_size=600, arrows=True)
    nx.draw_networkx_labels(G, pos, labels={n: n.split("_")[1][:6] for n in G.nodes}, font_size=7)

    plt.title("🧬 Juliet Bloom Lineage Tree")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"[LineageGraph] 🌲 Lineage tree saved to {save_path}")
