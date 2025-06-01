import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

LOG_PATH = "logs/decay_loss_log.csv"

def animate_decay_trails():
    if not os.path.exists(LOG_PATH):
        print("No decay_loss_log.csv found.")
        return

    df = pd.read_csv(LOG_PATH)
    df["tick_id"] = df["tick_id"].astype(str)

    fig, ax = plt.subplots(figsize=(10, 6))
    nodes = set(df["from"]) | set(df["to"])
    pos = {node: (i, 0) for i, node in enumerate(sorted(nodes))}

    def update(tick):
        ax.clear()
        current = df[df["tick_id"] == tick]

        for _, row in current.iterrows():
            x1, y1 = pos[row["from"]]
            x2, y2 = pos[row["to"]]
            width = row["total_decay"] * 5
            ax.plot([x1, x2], [y1, y2], color="red", linewidth=width, alpha=0.6)
            ax.text(x1, y1 + 0.1, row["from"], ha="center", fontsize=8)
            ax.text(x2, y2 + 0.1, row["to"], ha="center", fontsize=8)

        ax.set_title(f"Decay Trails at Tick {tick}")
        ax.set_ylim(-1, 2)
        ax.set_xticks([])
        ax.set_yticks([])

    ticks = sorted(df["tick_id"].unique())
    ani = animation.FuncAnimation(fig, update, frames=ticks, repeat=False, interval=500)
    ani.save("visuals/decay_trail_animation.gif", writer="pillow")
    plt.close()

if __name__ == "__main__":
    animate_decay_trails()
