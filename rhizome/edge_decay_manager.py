# /rhizome/edge_decay_manager.py

def decay_edge_weights(rhizome_map, min_flow_threshold=0.05, decay_rate=0.9):
    """
    Reduce edge weights for connections with low nutrient flow.

    Parameters:
    - rhizome_map: the full RhizomeMap structure containing nodes and edges
    - min_flow_threshold: the minimal reinforcement score to avoid decay
    - decay_rate: multiplier applied to weight (e.g., 0.9 = 10% decay)
    """
    for node in rhizome_map.nodes.values():
        for target, data in node.edges.items():
            reinforcement = data.get("reinforcement_score", 0)
            if reinforcement < min_flow_threshold:
                old_weight = data.get("weight", 1.0)
                new_weight = old_weight * decay_rate
                data["weight"] = new_weight

                if hasattr(node, "activity_log"):
                    node.activity_log.append(
                        f"🪓 Edge to {target} decayed: {old_weight:.4f} → {new_weight:.4f}"
                    )
