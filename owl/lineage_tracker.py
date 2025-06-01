import os
import json
from collections import defaultdict
from lineage_tree_visualizer import draw_lineage_tree
draw_lineage_tree()


def load_all_flowers(base_dir="juliet_flowers"):
    flowers = {}
    for seed in os.listdir(base_dir):
        seed_path = os.path.join(base_dir, seed)
        if not os.path.isdir(seed_path) or seed in ["cluster_report", "sealed", "mycelium_log"]:
            continue
        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
        for fname in os.listdir(mood_path):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(mood_path, fname)
            try:
                with open(fpath, "r") as f:
                    data = json.load(f)
                    flowers[data["id"]] = data
            except Exception as e:
                print(f"[Lineage] ⚠️ Skipped {fname}: {e}")

    return flowers

def build_lineage_graph(flowers):
    graph = defaultdict(list)
    roots = []

    for fid, flower in flowers.items():
        ancestor = flower.get("ancestor_id")
        if ancestor:
            graph[ancestor].append(fid)
        else:
            roots.append(fid)

    return graph, roots

def trace_lineages(flowers, graph, roots):
    lineages = []

    def dfs(path):
        current = path[-1]
        if current not in graph:
            lineages.append(list(path))
            return
        for child in graph[current]:
            dfs(path + [child])

    for root in roots:
        dfs([root])

    return lineages

if __name__ == "__main__":
    flowers = load_all_flowers()
    graph, roots = build_lineage_graph(flowers)
    lineages = trace_lineages(flowers, graph, roots)

    for i, chain in enumerate(lineages):
        print(f"\n🧬 Lineage {i+1} (length {len(chain)}):")
        for fid in chain:
            f = flowers[fid]
            print(f"  - {fid} | mood: {f['mood']} | seed: {f['seed_context'][0]}")
