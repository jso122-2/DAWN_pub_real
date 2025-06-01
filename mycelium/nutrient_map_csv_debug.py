
import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

def generate_nutrient_map_csv(log_root="mycelium_logs", output="juliet_flowers/cluster_report/nutrient_map.png"):
    seed_totals = defaultdict(float)

    if not os.path.exists(log_root):
        print(f"[Owl] ❌ No mycelium log directory found at {log_root}")
        return

    print(f"[DEBUG] Scanning log directory: {log_root}")

    for folder in os.listdir(log_root):
        folder_path = os.path.join(log_root, folder)
        if not os.path.isdir(folder_path):
            continue
        csv_path = os.path.join(folder_path, "nutrient_flow.csv")
        if not os.path.isfile(csv_path):
            print(f"[DEBUG] No nutrient_flow.csv in {folder_path}")
            continue

        print(f"[DEBUG] Reading: {csv_path}")
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    seed = row.get("seed")
                    try:
                        strength = float(row.get("flow_strength", 0))
                        seed_totals[seed] += strength
                    except ValueError:
                        print(f"[WARN] Bad flow_strength in row: {row}")
        except Exception as e:
            print(f"[Error] Failed to read {csv_path}: {e}")

    if not seed_totals:
        print("[NutrientMap] ❌ No data to visualize.")
        return

    print(f"[DEBUG] Seeds collected: {len(seed_totals)}")
    for seed, strength in seed_totals.items():
        print(f" - {seed}: {strength:.2f}")

    os.makedirs(os.path.dirname(output), exist_ok=True)
    print(f"[DEBUG] Saving to: {output}")

    plt.figure(figsize=(10, 6))
    seeds = list(seed_totals.keys())
    values = [seed_totals[s] for s in seeds]

    plt.bar(seeds, values, color="green")
    plt.title("🧠 Mycelium Nutrient Density (by Seed)")
    plt.xlabel("Seed")
    plt.ylabel("Total Flow Strength")
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    print(f"[NutrientMap] 📊 Saved to {output}")
