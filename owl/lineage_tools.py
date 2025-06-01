import os
import json
from collections import defaultdict

def load_all_flowers(base_dir="juliet_flowers"):
    flowers = {}
    for seed in os.listdir(base_dir):
        seed_path = os.path.join(base_dir, seed)
        if not os.path.isdir(seed_path) or seed in ["sealed", "cluster_report", "mycelium_log"]:
            continue
        for mood in os.listdir(seed_path):
            mood_path = os.path.join(seed_path, mood)
            if not os.path.isdir(mood_path):
                continue
            for fname in os.listdir(mood_path):
                if not fname.endswith(".json"):
                    continue
                try:
                    with open(os.path.join(mood_path, fname), "r") as f:
                        data = json.load(f)
                        flowers[data["id"]] = data
                except Exception as e:
                    print(f"[LineageTools] ⚠️ Skipped {fname}: {e}")
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

def check_lineage_contradictions(bloom, flower_dict):
    """
    Scans bloom's lineage for logical or mood-based contradictions.
    Returns a list of issues if found, else an empty list.
    """
    contradictions = []
    lineage = resolve_bloom_lineage(bloom["id"], flower_dict)

    for ancestor in lineage:
        if ancestor.get("mood") != bloom.get("mood"):
            if semantic_conflict(bloom.get("sentences", []), ancestor.get("sentences", [])):
                contradictions.append(
                    f"Mood shift ({ancestor.get('mood')} → {bloom.get('mood')}) with semantic clash"
                )

    return contradictions


def resolve_bloom_lineage(bloom_id, flower_dict):
    """
    Reconstructs a bloom's lineage by traversing ancestor_id chain.
    """
    lineage = []
    current = flower_dict.get(bloom_id)
    while current and current.get("ancestor_id"):
        if ancestor.get("mood") != bloom.get("mood"):
            ancestor = flower_dict.get(ancestor_id)
        if ancestor:
            lineage.append(ancestor)
            current = ancestor
        else:
            break
    return lineage


def semantic_conflict(current_sentences, ancestor_sentences):
    """
    Basic placeholder: checks for keyword contradiction or lexical inversion.
    """
    # TODO: Replace with embedding similarity + antonym detector later
    for sent in current_sentences:
        for ancestor_sent in ancestor_sentences:
            if "not" in sent and "always" in ancestor_sent:
                return True
    return False


if __name__ == "__main__":
    flowers = load_all_flowers()
    graph, roots = build_lineage_graph(flowers)
    for fid, bloom in flowers.items():
        issues = check_lineage_contradictions(bloom, flowers)
        if issues:
            print(f"[Owl] 🧪 {fid} → {issues}")
