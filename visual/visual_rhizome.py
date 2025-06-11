import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
import networkx as nx
from matplotlib import cm

def visualize_rhizome_map(rhizome_map, nutrient_type="attention", glow_threshold=0.1):
    """
    Visualizes the RhizomeMap as a force-directed graph with nutrient trails and glow.
    Nodes = seeds, Edges = nutrient flow
    """
    G = nx.DiGraph()

    # Step 1: Add nodes
    for seed_id in rhizome_map.nodes:
        G.add_node(seed_id)

    # Step 2: Add edges with glow weight
    for seed_id, node in rhizome_map.nodes.items():
        for target_id, edge_data in node.edges.items():
            if isinstance(edge_data, dict):
                glow = edge_data.get("reinforcement_score", 0.0)
                nutrient_flow = node.nutrient_reservoir.get(nutrient_type, 0.0)
                if glow >= glow_threshold:
                    G.add_edge(seed_id, target_id, glow=glow, flow=nutrient_flow)

    pos = nx.spring_layout(G, seed=42)  # Force-directed layout

    # Step 3: Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="lightblue", edgecolors="black")

    # Step 4: Draw labels
    nx.draw_networkx_labels(G, pos, font_size=8)

    # Step 5: Draw edges with glow intensity as color
    edges = G.edges(data=True)
    flows = [d["glow"] for (_, _, d) in edges]
    edge_colors = cm.inferno([min(f, 1.0) for f in flows])  # Normalize to [0,1]

    nx.draw_networkx_edges(
        G, pos,
        edgelist=[(u, v) for u, v, _ in edges],
        edge_color=edge_colors,
        width=2.0
    )

    plt.title(f"Rhizome Nutrient Map – Highlighting '{nutrient_type}' Flow")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
