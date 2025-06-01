import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib import cm
import os

from codex.sigil_probe import probe_sigil

blue_heat = probe_sigil("/blue_monday", fallback_entropy=0.0)


def animate_rhizome_glow_advanced(
    rhizome_map,
    log_path="logs/reinforcement_log.json",
    bloom_log="juliet_flowers/bloom_log.csv",
    out_gif="visual_exports/glow_animation_advanced.gif",
    pulse_mode="urgency"  # or "entropy"
):
    with open(log_path, "r") as f:
        snapshots = json.load(f)

    spark_seeds = set()
    if os.path.exists(bloom_log):
        with open(bloom_log, "r") as f:
            lines = f.readlines()[1:]  # skip header
            for line in lines:
                if "synthesis" in line:
                    parts = line.strip().split(",")
                    spark_seeds.add(parts[1])  # seed_id

    G = nx.DiGraph()
    for seed_id in rhizome_map.nodes:
        G.add_node(seed_id)

    for seed_id, node in rhizome_map.nodes.items():
        for target_id in node.edges:
            G.add_edge(seed_id, target_id)

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(10, 6))

    def update(frame):
        ax.clear()
        snapshot = snapshots[frame]
        glow_data = snapshot["reinforcement_tracker"]

        edge_colors = []
        for u, v in G.edges():
            key = f"{u}→{v}"
            glow = glow_data.get(key, 0.0)
            # 🎚️ Fade to black if low glow
            if glow < 0.05:
                edge_colors.append((0.1, 0.1, 0.1, 0.2))  # transparent black
            else:
                edge_colors.append(cm.inferno(min(glow, 1.0)))

        # 🎯 Pulse nodes by urgency or entropy
        node_colors = []
        for node in G.nodes:
            reservoir = rhizome_map.nodes[node].nutrient_reservoir
            if pulse_mode == "urgency":
                level = reservoir.get("urgency", 0.0)
                color = cm.Reds(min(level, 1.0))
            else:
                bloom = getattr(rhizome_map.nodes[node], "bloom", None)
                entropy = getattr(bloom, "entropy_score", 0.0) if bloom else 0.0
                color = cm.Blues(min(entropy, 1.0))
            # 🌱 Flash if spark
            if node in spark_seeds:
                color = (1.0, 1.0, 0.2, 1.0)  # bright yellow
            node_colors.append(color)

        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, edgecolors="black", node_size=400)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=8)
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color=edge_colors, width=2.0)

        ax.set_title(f"Advanced Glow Animation | Tick {frame} | {snapshot['timestamp']}")
        ax.axis("off")

    os.makedirs(os.path.dirname(out_gif), exist_ok=True)
    anim = FuncAnimation(fig, update, frames=len(snapshots), interval=500)
    anim.save(out_gif, writer=PillowWriter(fps=2))
    print(f"[🎥 Glow Engine+] Saved: {out_gif}")
