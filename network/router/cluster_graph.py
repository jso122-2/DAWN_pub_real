import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from cluster_linker import link_clusters
from bloom.juliet_cluster import load_clusters
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Segoe UI Emoji"

def visualize_cluster_graph(cluster_json="juliet_flowers/cluster_report/cluster_report.json", output="juliet_flowers/cluster_report/semantic_graph.png"):
    clusters = load_clusters()
    links = link_clusters(clusters)

    G = nx.Graph()

    # Add nodes with cluster size
    for c in clusters:
        G.add_node(c["cluster_id"], size=c["size"])

    # Add edges with scores
    for link in links:
        G.add_edge(link["from"], link["to"], weight=link["score"])

    pos = nx.spring_layout(G, seed=42)

    # Draw nodes
    sizes = [G.nodes[n]["size"] * 100 for n in G.nodes]
    nx.draw_networkx_nodes(G, pos, node_size=sizes, node_color="skyblue", alpha=0.8)

    # Draw edges
    weights = [G[u][v]["weight"] for u, v in G.edges]
    nx.draw_networkx_edges(G, pos, width=[w * 0.5 for w in weights], edge_color="gray")

    # Labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    plt.title("DAWN Semantic Bloom Network", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    print(f"[Graph] 🌐 Semantic graph saved to {output}")
