import os
import json
import matplotlib.pyplot as plt

SUMMARY_PATH = os.path.join("juliet_flowers", "cluster_report", "field_summary.json")

def visualize_field_map(summary_path=SUMMARY_PATH):
    if not os.path.exists(summary_path):
        print(f"[FieldMap] ❌ Missing summary file: {summary_path}")
        return

    with open(summary_path, "r") as f:
        summary = json.load(f)

    plt.figure(figsize=(10, 10))
    for i, (field, data) in enumerate(summary.items()):
        radius = data["avg_bloom_factor"]
        angle = i * (2 * 3.14159 / len(summary))
        x = radius * 0.8 * np.cos(angle)
        y = radius * 0.8 * np.sin(angle)
        size = data["total"] * 20
        plt.scatter(x, y, s=size, label=field, alpha=0.6)

        plt.text(x, y, field, fontsize=9, ha='center', va='center')

    plt.title("🌐 Semantic Field Map", fontsize=16)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("juliet_flowers/cluster_report/semantic_field_map.png")
    plt.close()
    print("[FieldMap] 🌐 Semantic field map saved.")
