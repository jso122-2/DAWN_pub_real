import json
import os

def compute_weight(seed, metrics, coeffs):
    return round(
        coeffs["alpha"] * metrics.get("entropy", 0.0) +
        coeffs["beta"]  * metrics.get("trust", 0.0) +
        coeffs["gamma"] * metrics.get("scup", 0.0) +
        coeffs["delta"] * metrics.get("mood", 0.0) +
        coeffs["epsilon"] * metrics.get("depth", 0.0) +
        coeffs["zeta"] * metrics.get("gravity", 0.0) +
        coeffs["eta"]  * metrics.get("central", 0.0), 4
    )

def load_seed_metrics(path="juliet_flowers/index/seed_metrics.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_weight_map(weight_map, path="juliet_flowers/index/weight_map.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(weight_map, f, indent=2)

def run_weight_engine():
    metrics = load_seed_metrics()
    coeffs = {
        "alpha": 0.2,
        "beta":  0.3,
        "gamma": 0.1,
        "delta": 0.1,
        "epsilon": 0.1,
        "zeta": 0.1,
        "eta":  0.1
    }

    weight_map = {}
    for seed, dims in metrics.items():
        weight_map[seed] = compute_weight(seed, dims, coeffs)

    save_weight_map(weight_map)
    print("[WeightEngine] 🧠 Semantic weights saved to weight_map.json")

if __name__ == "__main__":
    run_weight_engine()
