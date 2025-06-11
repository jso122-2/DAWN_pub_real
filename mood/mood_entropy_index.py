
import os
import json
import pandas as pd

def scan_bloom_memory(root="juliet_flowers"):
    records = []

    for subdir, _, files in os.walk(root):
        for file in files:
            if file.endswith(".json"):
                try:
                    path = os.path.join(subdir, file)
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        records.append({
                            "bloom_id": data.get("bloom_id"),
                            "mood": data.get("mood"),
                            "entropy_score": data.get("entropy_score"),
                            "bloom_factor": data.get("bloom_factor"),
                            "lineage_depth": data.get("lineage_depth"),
                            "timestamp": data.get("timestamp")
                        })
                except Exception as e:
                    print(f"⚠️ Error loading {file}: {e}")

    return pd.DataFrame(records)

def generate_mood_entropy_index(df):
    if df.empty:
        print("No bloom data found.")
        return None

    # Clean NaNs
    df = df.dropna(subset=["entropy_score", "bloom_factor", "lineage_depth"])
    grouped = df.groupby("mood")[["entropy_score", "bloom_factor", "lineage_depth"]].mean().sort_values("entropy_score", ascending=False)
    print("📊 Mood Entropy Index:")
    print(grouped.round(3))
    return grouped

if __name__ == "__main__":
    df = scan_bloom_memory()
    generate_mood_entropy_index(df)

