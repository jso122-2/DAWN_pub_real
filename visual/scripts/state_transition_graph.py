import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path
import sys

def main(*args, **kwargs):
    input_path = Path("data/state_transitions.npy")
    output_dir = Path("visual/outputs/state_transition_graph")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "state_transition_graph.png"

    if not input_path.exists():
        print(f"ERROR: Input data not found: {input_path}")
        sys.exit(1)

    transitions = np.load(input_path, allow_pickle=True)
    if transitions.size == 0:
        print(f"ERROR: Input data is empty: {input_path}")
        sys.exit(1)

    G = nx.DiGraph()
    for src, dst, weight in transitions:
        G.add_edge(str(src), str(dst), weight=weight)
    fig, ax = plt.subplots(figsize=(10, 8))
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=3000, ax=ax)
    edges = G.edges()
    weights = [G[u][v]['weight'] for u, v in edges]
    nx.draw_networkx_edges(G, pos, width=[w*3 for w in weights], alpha=0.6, edge_color='gray', connectionstyle='arc3,rad=0.1', ax=ax, arrowsize=20, arrowstyle='->')
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    edge_labels = {k: f'{v:.1f}' for k, v in edge_labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8, ax=ax)
    ax.set_title('State Transition Graph')
    ax.axis('off')
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"SUCCESS: State transition graph saved to {output_path}")
    return str(output_path)

if __name__ == "__main__":
    main() 