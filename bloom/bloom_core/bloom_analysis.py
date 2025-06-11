import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# === BLOOM SHAPE EVOLUTION ===

def lock_bloom_evolution(bloom):
    """
    Finalizes bloom shape based on recursive dynamics.
    Applies stability logic using bloom_factor, lineage_depth, and entropy.
    Handles edge cases and locks in final shape state.
    Returns locked shape or 'unstable'.
    """
    try:
        factor = getattr(bloom, "bloom_factor", 1.0)
        depth = getattr(bloom, "lineage_depth", 0)
        entropy = getattr(bloom, "entropy_score", 0.5)

        # Edge case: extreme entropy or recursion
        if entropy > 0.95:
            bloom.shape_state = "chaotic"
            bloom.evolution_locked = False
            bloom.activity_log.append(f"⚠️ Bloom entropy too high → chaotic shape")
            return bloom.shape_state

        if depth > 15:
            bloom.shape_state = "collapsed"
            bloom.evolution_locked = False
            bloom.activity_log.append(f"⚠️ Bloom lineage too deep → collapsed shape")
            return bloom.shape_state

        # Stability score
        stability = (factor * 0.6) + ((1 / (1 + depth)) * 0.3) + ((1 - entropy) * 0.1)
        bloom.stability_index = round(stability, 3)

        # Shape decision
        if stability > 0.85:
            shape = "crystal"
        elif stability > 0.6:
            shape = "spiral"
        elif stability > 0.4:
            shape = "wave"
        else:
            shape = "unstable"

        bloom.shape_state = shape
        bloom.evolution_locked = True if shape != "unstable" else False
        bloom.activity_log.append(
            f"🔒 Evolution locked as '{shape}' | stability={bloom.stability_index} | entropy={entropy:.2f} | depth={depth}"
        )
        return shape

    except Exception as e:
        bloom.shape_state = "undefined"
        bloom.evolution_locked = False
        bloom.activity_log.append(f"❌ Evolution failed due to: {str(e)}")
        return "error"


# === SCUP VS ENTROPY VISUALIZATION ===

def plot_scup_vs_entropy(
    scup_log_path="logs/scup_tick_log.csv",
    entropy_path="juliet_flowers/cluster_report/drift_compass_log.csv"
):
    """
    Plot SCUP vs entropy over time for schema coherence diagnostics.
    """
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
    os.makedirs("visuals", exist_ok=True)
    plt.savefig("visuals/scup_entropy_trend.png")
    plt.show()


# === ENTRY POINT ===

if __name__ == "__main__":
    plot_scup_vs_entropy()
