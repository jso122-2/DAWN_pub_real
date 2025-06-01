import os
import json
import pandas as pd
import matplotlib.pyplot as plt

SPIDER_LOG = "owl/logs/visual_use_log.json"
SCUP_LOG = "juliet_flowers/scup_bloom_correlation.csv"

def load_spider_actions():
    if not os.path.exists(SPIDER_LOG):
        return []
    with open(SPIDER_LOG, "r") as f:
        return json.load(f)

def load_scup_values():
    if not os.path.exists(SCUP_LOG):
        return pd.DataFrame()
    return pd.read_csv(SCUP_LOG, parse_dates=["timestamp"])

def build_correlation():
    spider_data = load_spider_actions()
    scup_data = load_scup_values()

    # extract only Spider-triggered visuals
    spider_df = pd.DataFrame([
        {
            "timestamp": entry["timestamp"],
            "visual": entry["visual"]
        } for entry in spider_data
        if "Spider" in entry.get("visual", "") or "spider" in entry.get("visual", "")
    ])

    spider_df["timestamp"] = pd.to_datetime(spider_df["timestamp"])
    scup_data["timestamp"] = pd.to_datetime(scup_data["timestamp"])

    merged = pd.merge_asof(spider_df.sort_values("timestamp"),
                           scup_data.sort_values("timestamp"),
                           on="timestamp",
                           tolerance=pd.Timedelta("5m"),
                           direction="backward")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(merged["timestamp"], merged["scup"], c="red", label="SCUP at Spider action")
    plt.plot(scup_data["timestamp"], scup_data["scup"], alpha=0.4, label="Full SCUP")
    plt.title("📈 Spider Visual Actions vs SCUP Stability")
    plt.ylabel("SCUP")
    plt.xlabel("Timestamp")
    plt.legend()
    plt.grid(True)
    out_path = "juliet_flowers/cluster_report/spider_scup_correlation.png"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path)
    plt.close()
    print(f"✅ Correlation plot saved: {out_path}")

if __name__ == "__main__":
    build_correlation()
