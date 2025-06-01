import os
import matplotlib.pyplot as plt

def parse_logs_with_mood(path="juliet_flowers/cluster_report"):
    points = []
    for fname in os.listdir(path):
        if fname.startswith("vector_drift_") and fname.endswith(".log"):
            full_path = os.path.join(path, fname)
            with open(full_path, encoding="utf-8") as f:
                drift = None
                for line in f:
                    if "Drift Score" in line:
                        drift = float(line.strip().split(": ")[-1])
                if drift is not None:
                    mood = "unknown"
                    if "_anxious" in fname:
                        mood = "anxious"
                    elif "_curious" in fname:
                        mood = "curious"
                    elif "_calm" in fname:
                        mood = "calm"
                    elif "_reflective" in fname:
                        mood = "reflective"
                    points.append((drift, mood))
    return points

def mood_to_color(mood):
    return {
        "anxious": "red",
        "curious": "orange",
        "calm": "blue",
        "reflective": "green",
        "unknown": "gray"
    }.get(mood, "black")

def render_entropy_gradient_overlay(points, save_path="juliet_flowers/cluster_report/entropy_overlay_gradient.png"):
    plt.figure(figsize=(10, 5))
    for idx, (score, mood) in enumerate(points):
        plt.scatter(idx, score, color=mood_to_color(mood), label=mood if idx == 0 else "", s=60)
    plt.title("Drift Entropy Overlay (Colored by Mood)")
    plt.xlabel("Bloom Index")
    plt.ylabel("Drift Score")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
    print(f"[Render] Drift gradient saved → {save_path}")

if __name__ == "__main__":
    data = parse_logs_with_mood()
    render_entropy_gradient_overlay(data)
