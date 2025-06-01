def predict_next_synthesis(rhizome_map, top_n=3):
    predictions = []

    for node in rhizome_map.nodes.values():
        reinforcement_sum = 0.0
        for neighbor_id, edge in node.edges.items():
            if isinstance(edge, dict):
                reinforcement_sum += edge.get("reinforcement_score", 0.0)

        entropy = getattr(node, "entropy_score", 0.5)
        depth = getattr(node, "lineage_depth", 0)
        mood = getattr(node, "mood", "neutral")

        # Score = reinforcement - entropy penalty + depth weight
        score = reinforcement_sum - (entropy * 0.5) + (0.1 * depth)
        if score > 1.5:  # threshold filter
            predictions.append((node.seed_id, round(score, 3)))

    predictions.sort(key=lambda x: x[1], reverse=True)

    print("[Owl] 🔮 Predicted Synthesis Candidates:")
    for seed, score in predictions[:top_n]:
        print(f"  • {seed}: score={score}")

    return predictions[:top_n]
