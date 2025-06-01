import os
import json
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import matplotlib.colors as mcolors

def generate_nutrient_map(
    log_root="juliet_flowers/mycelium_log",
    output="juliet_flowers/cluster_report/nutrient_map.png",
    show_top_k=None,
    annotate=True,
    save_json_summary=True
):
    """
    Visualize nutrient activity (log density) per seed across the mycelium log structure.
    Optionally limits to top-k active seeds and saves a JSON summary for downstream agents.
    """
    seed_counts = defaultdict(int)

    if not os.path.exists(log_root):
        print(f"[Owl] 🕸️ No nutrient logs found at {log_root}.")
        return

    for folder in os.listdir(log_root):
        full_path = os.path.join(log_root, folder)
        if not os.path.isdir(full_path):
            continue
        for fname in os.listdir(full_path):
            if fname.endswith(".log"):
                seed = fname.replace(".log", "")
                log_path = os.path.join(full_path, fname)
                try:
                    with open(log_path, "r", encoding="utf-8") as f:
                        line_count = len(f.readlines())
                        seed_counts[seed] += line_count
                except Exception as e:
                    print(f"[Owl] ⚠️ Failed to parse {fname}: {e}")

    if not seed_counts:
        print("[NutrientMap] ❌ No data available to visualize.")
        return

    # Sort by activity
    sorted_seeds = sorted(seed_counts.items(), key=lambda x: x[1], reverse=True)

    if show_top_k:
        sorted_seeds = sorted_seeds[:show_top_k]

    seeds, values = zip(*sorted_seeds)

    # Color normalization
    norm = mcolors.Normalize(vmin=min(values), vmax=max(values))
    cmap = plt.cm.YlGnBu
    colors = cmap(norm(values))

    # Plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(seeds, values, color=colors)
    plt.title("🌱 Mycelium Nutrient Density by Seed")
    plt.xlabel("Seed")
    plt.ylabel("Root Activity (Log Line Count)")
    plt.xticks(rotation=45)

    if annotate:
        for bar, val in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width() / 2, val + 1, str(val),
                     ha='center', va='bottom', fontsize=8, alpha=0.7)

    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.set_label("Nutrient Intensity")

    os.makedirs(os.path.dirname(output), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output)
    print(f"[NutrientMap] ✅ Saved map to → {output}")
    plt.close()

    # Optional summary output
    if save_json_summary:
        json_out = output.replace(".png", "_summary.json")
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(dict(sorted_seeds), f, indent=2)
        print(f"[NutrientMap] 🧾 Saved JSON summary to → {json_out}")
