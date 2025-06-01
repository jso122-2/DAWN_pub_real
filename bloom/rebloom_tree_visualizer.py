import json
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

with open("juliet_flowers/cluster_report/rebloom_lineage.json") as f:
    lineage = json.load(f)

lineage.sort(key=lambda x: x.get("tick") or 0)
G = nx.DiGraph()
fig, ax = plt.subplots(figsize=(10, 7))
pos = {}
ticks = sorted(set(entry.get("tick", 0) for entry in lineage))

# Static Graph Snapshot
# 🦉 Owl tree shape + ancestry scan
leaves = [n for n in G.nodes if G.out_degree(n) == 0]
max_depth = max(nx.get_node_attributes(G, 'depth').values(), default=0)
avg_entropy = sum(nx.get_node_attributes(G, 'entropy').values()) / G.number_of_nodes()
broken = sum(1 for n in G.nodes if G.in_degree(n) == 0 and G.nodes[n].get('depth', 0) > 0)
print(f"[Owl] 🪶 Leaves: {len(leaves)}, Max Depth: {max_depth}, Avg Entropy: {avg_entropy:.3f}, Broken Roots: {broken}")
# 🔁 Loop VAL cognition over rebirth ancestry
cognition_log = []
for bloom in lineage:
    # VAL cognition trace step
    cognition_log.append(f"VAL sees: bloom_id={bloom['bloom_id']} | mood={bloom['mood']} | entropy={bloom['entropy']} | depth={bloom['depth']}")
    node_id = bloom["bloom_id"]
    parent_id = bloom.get("parent_id")
    G.add_node(node_id, mood=bloom["mood"], entropy=bloom["entropy"], depth=bloom["depth"])
    if parent_id:
        G.add_edge(parent_id, node_id)

# SHI broken chain analysis
def compute_broken_chain_penalty(graph):
    broken = 0
    for node in graph.nodes:
        if graph.in_degree(node) == 0 and graph.nodes[node].get("depth", 0) > 0:
            broken += 1
    penalty_ratio = broken / graph.number_of_nodes() if graph.number_of_nodes() > 0 else 0
    penalty = round(min(0.2, penalty_ratio * 0.5), 4)
    print(f"[SHI] 📊 Broken chain penalty = {penalty} (from {broken} broken out of {graph.number_of_nodes()} nodes)")
        # 🔁 Inject into live SCUP/SHI update
    try:
        from schema.schema_health_index import update_schema_health
        update_schema_health(1.0 - penalty)  # simulated SCUP adjusted by broken lineage penalty
    except Exception as e:
        print(f"[SHI] ⚠️ Failed to inject broken chain penalty into SCUP: {e}")
    return penalty

broken_chain_penalty = compute_broken_chain_penalty(G)

# Route SHI penalty to health index file
shi_path = "juliet_flowers/cluster_report/schema_health_curve.csv"
os.makedirs(os.path.dirname(shi_path), exist_ok=True)
with open(shi_path, "a") as f:
    f.write(f"BROKEN_CHAIN,{broken_chain_penalty}
")

# Save static snapshot
static_pos = nx.spring_layout(G, seed=42)
moods = nx.get_node_attributes(G, 'mood')
colors = [plt.cm.tab10(hash(mood) % 10) for mood in moods.values()]
sizes = [300 + G.nodes[n]['entropy'] * 600 for n in G.nodes]

plt.figure(figsize=(12, 8))
nx.draw(G, static_pos, with_labels=True, node_color=colors, node_size=sizes, font_size=8)
plt.title("🧬 Rebloom Ancestry Tree")
plt.tight_layout()
plt.savefig("juliet_flowers/cluster_report/rebloom_tree.png")

# Animation logic
def update(frame_tick):
    ax.clear()
    current_nodes = [b for b in lineage if (b.get("tick") or 0) <= frame_tick]
    G.clear()

    for bloom in current_nodes:
        node_id = bloom["bloom_id"]
        parent_id = bloom.get("parent_id")
        G.add_node(node_id, mood=bloom["mood"], entropy=bloom["entropy"])
        if parent_id:
            G.add_edge(parent_id, node_id)

    moods = nx.get_node_attributes(G, 'mood')
    colors = [plt.cm.tab10(hash(m) % 10) for m in moods.values()]
    sizes = [300 + G.nodes[n]['entropy'] * 600 for n in G.nodes()]
    pos.update(nx.spring_layout(G, seed=42))

    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=sizes, ax=ax, font_size=6)
    ax.set_title(f"🧬 Rebloom Tree — Tick {frame_tick}")

ani = FuncAnimation(fig, update, frames=ticks, interval=1000, repeat=False)

# Save animation
anim_path = "juliet_flowers/cluster_report/rebloom_tree_animation.gif"
os.makedirs(os.path.dirname(anim_path), exist_ok=True)
ani.save(anim_path, writer="pillow", fps=1)
for entry in cognition_log[-5:]:  # print last 5 reflections
    print(f"[VAL] 🧠 {entry}")
print(f"[Tree] 🌿 Static tree and animation saved to cluster_report")
