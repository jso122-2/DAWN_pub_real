import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def load_drift_sequence(log_dir):
    scores = []
    for fname in sorted(os.listdir(log_dir)):
        if fname.startswith("vector_drift_") and fname.endswith(".log"):
            with open(os.path.join(log_dir, fname), encoding="utf-8") as f:
                for line in f:
                    if "Drift Score" in line:
                        score = float(line.strip().split(": ")[-1])
                        scores.append(score)
    return scores

def animate_drift(scores, save_path):
    fig, ax = plt.subplots()
    ax.set_title("Drift Score Per Tick")
    ax.set_xlim(0, len(scores))
    ax.set_ylim(0, 1)
    line, = ax.plot([], [], "bo-")

    def update(frame):
        x = list(range(frame + 1))
        y = scores[:frame + 1]
        line.set_data(x, y)
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(scores), interval=300, repeat=False)
    ani.save(save_path, writer="pillow")
    print(f"[Animation] 🎞 Drift animation saved: {save_path}")

if __name__ == "__main__":
    drift_scores = load_drift_sequence("juliet_flowers/cluster_report")
    if drift_scores:
        animate_drift(drift_scores, "juliet_flowers/cluster_report/drift_by_tick.gif")
