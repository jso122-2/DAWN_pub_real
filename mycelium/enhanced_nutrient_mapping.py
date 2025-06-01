
import csv, os
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

def log_nutrient_flow(bloom, flow_strength: float):
    today = datetime.now().strftime("%Y-%m-%d")
    folder = os.path.join("mycelium_logs", today)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "nutrient_flow.csv")
    file_exists = os.path.isfile(path)
    with open(path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["timestamp", "bloom_id", "seed", "mood", "entropy_score", "bloom_factor", "lineage_depth", "flow_strength"])
        writer.writerow([datetime.now().isoformat(), bloom.bloom_id, bloom.seed, bloom.mood, bloom.entropy_score, bloom.bloom_factor, bloom.lineage_depth, flow_strength])
    print(f"[MyceliumLog] 🌱 Nutrient explicitly logged: {bloom.bloom_id}, strength: {flow_strength:.2f}")

def visualize_nutrient_map(csv_path):
    seed_totals = defaultdict(float)
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            seed_totals[row['seed']] += float(row['flow_strength'])
    seeds, strengths = zip(*seed_totals.items())
    plt.figure(figsize=(10, 5))
    plt.bar(seeds, strengths, color='green')
    plt.xlabel('Seeds')
    plt.ylabel('Total Nutrient Flow Strength')
    plt.title('🌱 Explicit Nutrient Mapping Visualization')
    plt.tight_layout()
    plt.savefig(csv_path.replace('.csv', '_visualization.png'))
    plt.close()
    print("[Visualization] 📊 Nutrient map visualization saved explicitly.")
    
if __name__ == "__main__":
    print("[Test] Enhanced Nutrient Mapping script executed explicitly.")
