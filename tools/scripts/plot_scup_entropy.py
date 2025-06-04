import pandas as pd
import matplotlib.pyplot as plt

def plot_scup_vs_entropy(scup_log_path="logs/scup_tick_log.csv", entropy_path="juliet_flowers/cluster_report/drift_compass_log.csv"):
    scup_df = pd.read_csv(scup_log_path)
    ent_df = pd.read_csv(entropy_path, names=["tick_id", "angle", "magnitude", "entropy"])

    df = pd.merge(scup_df, ent_df[["tick_id", "entropy"]], on="tick_id", how="inner")
    df["tick_id"] = pd.to_numeric(df["tick_id"])

    plt.figure(figsize=(12, 6))
    plt.plot(df["tick_id"], df["scup"], label="SCUP", color="green")
    plt.plot(df["tick_id"], df["entropy"], label="Entropy", color="red", alpha=0.7)
    plt.title("📈 SCUP vs Entropy Over Time")
    plt.xlabel("Tick")
    plt.ylabel("Signal Strength")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("visuals/scup_entropy_trend.png")
    plt.show()

if __name__ == "__main__":
    plot_scup_vs_entropy()
