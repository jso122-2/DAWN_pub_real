import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def animate_synthesis_field(path="logs/synthesis_bloom_log.csv"):
    if not os.path.exists(path):
        print("Missing synthesis log.")
        return

    df = pd.read_csv(path)
    df["x"] = df["entropy"].astype(float) * 10  # example layout
    df["y"] = df["depth"].astype(float)

    ticks = sorted(df["tick_id"].unique())
    fig, ax = plt.subplots(figsize=(10, 6))

    def update(tick):
        ax.clear()
        current = df[df["tick_id"] == tick]
        ax.set_title(f"🌸 Synthesis Field – Tick {tick}")
        for _, row in current.iterrows():
            ax.scatter(
                row["x"],
                row["y"],
                s=row["factor"] * 100,
                alpha=0.7,
                label=row["bloom_id"],
                color="magenta" if row["mood"] == "synthesis" else "gray"
            )
            ax.text(row["x"], row["y"] + 0.2, row["bloom_id"], fontsize=7, ha="center")

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xlabel("Entropy")
        ax.set_ylabel("Lineage Depth")

    ani = animation.FuncAnimation(fig, update, frames=ticks, repeat=False, interval=700)
    ani.save("visuals/synthesis_field_overlay.gif", writer="pillow")
    plt.close()

if __name__ == "__main__":
    animate_synthesis_field()
