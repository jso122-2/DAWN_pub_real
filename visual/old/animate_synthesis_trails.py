import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

def animate_synthesis_trails(path="logs/synthesis_bloom_log.csv"):
    if not os.path.exists(path):
        print("No synthesis log found.")
        return

    df = pd.read_csv(path)
    ticks = sorted(df["tick_id"].unique())

    fig, ax = plt.subplots(figsize=(10, 6))

    def update(tick):
        ax.clear()
        current = df[df["tick_id"] == tick]
        ax.set_title(f"🌸 Synthesis Trails – Tick {tick}")
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        for _, row in current.iterrows():
            path = row["path"].split("→")
            for i in range(len(path) - 1):
                ax.plot([i, i+1], [5, 5], color="magenta", linewidth=2, alpha=0.6)
                ax.text(i, 5.2, path[i], fontsize=8, ha="center")
            ax.text(len(path)-1, 5.2, path[-1], fontsize=8, ha="center", color="purple")

    ani = animation.FuncAnimation(fig, update, frames=ticks, repeat=False, interval=700)
    ani.save("visuals/synthesis_trail_animation.gif", writer="pillow")
    plt.close()

if __name__ == "__main__":
    animate_synthesis_trails()
