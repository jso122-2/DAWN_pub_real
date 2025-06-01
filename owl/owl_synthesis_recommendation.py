# /owl/owl_synthesis_recommendation.py

def recommend_synthesis_nodes(rhizome_map, min_score=2.5):
    candidates = []
    for node in rhizome_map.nodes.values():
        total_reinforcement = 0.0
        for edge in node.edges.values():
            if isinstance(edge, dict):
                total_reinforcement += edge.get("reinforcement_score", 0.0)
        if total_reinforcement >= min_score:
            candidates.append((node.seed_id, round(total_reinforcement, 2)))

    candidates.sort(key=lambda x: x[1], reverse=True)
    print("[Owl] 🧠 Top synthesis candidates:")
    for seed, score in candidates[:5]:
        print(f"  → {seed}: {score}")
    return candidates
