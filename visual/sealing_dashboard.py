import os
import json
import matplotlib.pyplot as plt

SEALED_DIR = "juliet_flowers/sealed"
OUT = "juliet_flowers/cluster_report/sealing_dashboard.png"

def load_sealed_blooms():
    sealed = []
    for folder in os.listdir(SEALED_DIR):
        bloom_path = os.path.join(SEALED_DIR, folder)
        if not os.path.isdir(bloom_path):
            continue
        for f in os.listdir(bloom_path):
            if f.endswith(".json"):
                with open(os.path.join(bloom_path, f)) as file:
                    try:
                        data = json.load(file)
                        data["seed_id"] = folder
                        sealed.append(data)
                    except:
                        continue
    return sealed

def build_dashboard():
    data = load_sealed_blooms()
    if not data:
        print("❌ No sealed data to visualize.")
        return

    reasons = {"ash": 0, "soot": 0, "stall": 0}
    for bloom in data:
        context = bloom.get("seed_context", [])
        node = context[-1] if context else "?"
        ash, soot = bloom.get("ash", 0), bloom.get("soot", 0)
        if ash > 0.85:
            reasons["ash"] += 1
        if soot > 0.7:
            reasons["soot"] += 1
        if os.path.exists("owl/logs/crow_stall_log.json"):
            with open("owl/logs/crow_stall_log.json") as f:
                stalls = json.load(f)
                if node in stalls:
                    reasons["stall"] += 1

    labels, values = zip(*reasons.items())
    plt.figure(figsize=(7, 5))
    plt.bar(labels, values, color=["gray", "black", "crimson"])
    plt.title("📊 Sealed vs Pruned Bloom Breakdown")
    plt.ylabel("Bloom Count")
    plt.tight_layout()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.savefig(OUT)
    plt.close()
    print(f"✅ Sealing dashboard saved → {OUT}")

if __name__ == "__main__":
    build_dashboard()
