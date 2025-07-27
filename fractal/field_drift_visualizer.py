import os
import json
import matplotlib.pyplot as plt

def plot_field_drift(folder="juliet_flowers/cluster_report", output="juliet_flowers/cluster_report/field_drift.png"):
    snapshots = sorted([
        f for f in os.listdir(folder)
        if f.startswith("field_summary_") and f.endswith(".json")
    ])

    if len(snapshots) < 2:
        print("[FieldDrift] ⚠️ Not enough snapshots to visualize drift.")
        return

    field_history = {}

    for snap in snapshots:
        with open(os.path.join(folder, snap), "r") as f:
            summary = json.load(f)
            for field, data in summary.items():
                field_history.setdefault(field, []).append(data["avg_bloom_factor"])

    plt.figure(figsize=(12, 6))
    for field, factors in field_history.items():
        plt.plot(factors, label=field)

    plt.title("📈 Field Bloom Drift Over Time", fontsize=14)
    plt.xlabel("Snapshot Index")
    plt.ylabel("Avg Bloom Factor")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    print(f"[FieldDrift] 📈 Drift graph saved to {output}")
