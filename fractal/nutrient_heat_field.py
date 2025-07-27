import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

def generate_nutrient_heatfield(log_root="juliet_flowers/mycelium_log", output="juliet_flowers/cluster_report/nutrient_heat_field.png"):
    total_counts = defaultdict(int)

    for folder in os.listdir(log_root):
        full_path = os.path.join(log_root, folder)
        if not os.path.isdir(full_path):
            continue
        for fname in os.listdir(full_path):
            if fname.endswith(".log"):
                seed = fname.replace(".log", "")
                with open(os.path.join(full_path, fname), "r") as f:
                    total_counts[seed] += len(f.readlines())

    seed_pos = {
        "A1": (0, 1),
        "B2": (1, 0),
        "C3": (0, -1),
        "D4": (-1, 0)
    }

    plt.figure(figsize=(8, 8))
    for seed, count in total_counts.items():
        x, y = seed_pos.get(seed, (0, 0))
        color = "green"
        if count > 60:
            color = "red"
        elif count > 30:
            color = "orange"
        elif count > 10:
            color = "yellow"

        plt.scatter(x, y, s=count * 30, color=color, alpha=0.7)
        plt.text(x, y, f"{seed}\n{count}", fontsize=10, ha="center", va="center")

    plt.title("🌱 Semantic Nutrient Heat Field")
    plt.axis("off")
    plt.savefig(output)
    plt.close()
    print(f"[HeatField] ✅ Saved to {output}")
