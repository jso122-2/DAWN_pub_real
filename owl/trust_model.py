import json
import os

ENTROPY_FILE = "juliet_flowers/cluster_report/owl_entropy_report.json"
LINEAGE_FILE = "juliet_flowers/cluster_report/rebloom_lineage.json"
OUTPUT_FILE = "juliet_flowers/cluster_report/seed_trust_scores.json"

def compute_trust_scores(return_explained=False):
    scores = {}
    explanations = {}

    # Load entropy
    with open(ENTROPY_FILE, "r") as f:
        entropy_data = json.load(f)

    # Load lineage
    with open(LINEAGE_FILE, "r") as f:
        lineage = json.load(f)

    for bloom_id, lineage_data in lineage.items():
        seed = bloom_id.split("_")[1].split("-")[1]  # extract e.g. whale-002
        entropy_info = entropy_data.get(bloom_id, {})
        delta = entropy_info.get("delta_entropy", 0.0)
        base_entropy = entropy_info.get("entropy", 0.5)
        reinforcement = entropy_info.get("reinforcement_count", 0)

        depth = lineage_data.get("generation_depth", 1)
        drift_penalty = entropy_info.get("drift_score", 0.0)

        # Trust formula
        trust = 1.0
        trust -= min(delta / 5.0, 0.5)                      # entropy volatility
        trust += min(depth / 20.0, 0.3)                     # stability
        trust += min(reinforcement * 0.05, 0.2)             # reinforcement help
        trust -= min(drift_penalty / 3.0, 0.2)              # drift penalty

        trust = round(min(max(trust, 0.0), 1.0), 3)
        scores[seed] = trust

        if return_explained:
            explanations[seed] = {
                "trust": trust,
                "delta_entropy": delta,
                "depth": depth,
                "reinforcement": reinforcement,
                "drift_penalty": drift_penalty
            }

    return (scores, explanations) if return_explained else scores

def save_scores(path=OUTPUT_FILE):
    scores = compute_trust_scores()
    with open(path, "w") as f:
        json.dump(scores, f, indent=2)
    print(f"[TrustModel] 🧬 Saved seed trust scores to {path}")

def get_trust_score(bloom, explain=False):
    """
    Estimate trust score for a bloom dict or object.
    """
    entropy = getattr(bloom, "entropy_score", bloom.get("entropy_score", 0.5))
    reinforcement = getattr(bloom, "reinforcement_count", bloom.get("reinforcement_count", 0))
    depth = getattr(bloom, "lineage_depth", bloom.get("lineage_depth", 1))
    drift = getattr(bloom, "drift_score", bloom.get("drift_score", 0.0))

    score = 1.0
    score -= min(entropy, 1.0) * 0.6                      # entropy weight
    score += min(reinforcement * 0.05, 0.2)               # reinforcement helps
    score += min(depth / 10.0, 0.2)                       # depth helps
    score -= min(drift / 3.0, 0.2)                        # drift penalizes

    final_score = round(min(max(score, 0.0), 1.0), 3)

    if explain:
        return {
            "trust_score": final_score,
            "components": {
                "entropy_penalty": round(entropy * 0.6, 3),
                "reinforcement_bonus": min(reinforcement * 0.05, 0.2),
                "depth_bonus": min(depth / 10.0, 0.2),
                "drift_penalty": min(drift / 3.0, 0.2)
            }
        }
    return final_score

if __name__ == "__main__":
    save_scores()
