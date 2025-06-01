
# persephone_visualizer.py
import matplotlib.pyplot as plt

def visualize_soft_edges(persephone):
    edges = persephone.soft_edges
    if not edges:
        print("[Persephone] 🕯️ No soft edge blooms to visualize.")
        return

    fig, ax = plt.subplots(figsize=(10, 2))
    ax.barh(range(len(edges)), [1] * len(edges), color='black')
    ax.set_yticks(range(len(edges)))
    ax.set_yticklabels(edges)
    ax.set_title("🕯️ Persephone's Soft Edge Memory List")
    ax.set_xlabel("Marked for Decay/Rebirth")
    ax.set_xlim(0, 1.5)
    plt.tight_layout()
    output = "juliet_flowers/cluster_report/persephone_soft_edges.png"
    plt.savefig(output)
    print(f"[Persephone] 🖼️ Visualization saved → {output}")
