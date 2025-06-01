from datetime import datetime
import os
import matplotlib.pyplot as plt




def get_visual_output_folder(base_dir="C:/Users/Admin/OneDrive/Desktop/DAWN/juliet_flowers/cluster_report/owl_visuals"):
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    folder = os.path.join(base_dir, timestamp)
    os.makedirs(folder, exist_ok=True)
    return folder

def plot_drift_consistency(owl_data, output_dir):
    consistency_by_seed = {}
    for entry in owl_data:
        ts = entry["timestamp"]
        for drift in entry.get("drift", []):
            seed = drift["seed"]
            if seed not in consistency_by_seed:
                consistency_by_seed[seed] = []
            consistency_by_seed[seed].append((ts, drift["consistency"]))
    for seed, values in consistency_by_seed.items():
        x = [datetime.fromisoformat(v[0]) for v in values]
        y = [v[1] for v in values]
        plt.figure()
        plt.plot(x, y, marker='o', label=seed)
        plt.xlabel("Time")
        plt.ylabel("Drift Consistency")
        plt.title(f"🧭 Drift Consistency – {seed}")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{seed}_drift_plot.png"))
        plt.close()

def plot_stale_rates(owl_data, output_dir):
    from collections import defaultdict
    stale_count_by_tick = defaultdict(int)
    for entry in owl_data:
        ts = datetime.fromisoformat(entry["timestamp"])
        for _ in entry.get("stale", []):
            stale_count_by_tick[ts] += 1
    sorted_stale = sorted(stale_count_by_tick.items())
    x = [v[0] for v in sorted_stale]
    y = [v[1] for v in sorted_stale]
    plt.figure()
    plt.plot(x, y, marker='s', color='firebrick')
    plt.xlabel("Time")
    plt.ylabel("Stale Seeds Count")
    plt.title("📁 Stale Rates Over Time")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "stale_rates_plot.png"))
    plt.close()

def plot_loop_moods(owl_data, output_dir):
    from collections import defaultdict
    import matplotlib.pyplot as plt

    loop_moods_by_seed = defaultdict(lambda: defaultdict(int))
    for entry in owl_data:
        for loop in entry.get("loops", []):
            seed = loop["seed"]
            for mood in loop.get("moods", []):
                loop_moods_by_seed[seed][mood] += 1

    for seed, mood_counts in loop_moods_by_seed.items():
        moods = list(mood_counts.keys())
        counts = [mood_counts[m] for m in moods]
        plt.figure(figsize=(6, 4))
        plt.bar(moods, counts, color="teal")
        plt.xlabel("Mood")
        plt.ylabel("Loop Count")
        plt.title(f"🧠 Mood Loop Count – {seed}")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{seed}_mood_loop_chart.png"))
        plt.close()
