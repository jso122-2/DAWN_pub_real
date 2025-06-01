
import os
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

BLOOM_DIR = "juliet_flowers/bloom_metadata"
OUTPUT = "juliet_flowers/cluster_report/mood_transition.gif"

def load_blooms():
    entries = []
    for fname in sorted(os.listdir(BLOOM_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(BLOOM_DIR, fname), "r") as f:
                bloom = json.load(f)
                entries.append(bloom)
    return entries

def animate_mood_flow():
    data = load_blooms()
    if not data:
        print("[MoodTransition] ❌ No bloom data found.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))

    def update(frame):
        ax.clear()
        current = data[:frame+1]
        moods = [b.get("mood", "undefined") for b in current]
        ax.hist(moods, bins=len(set(moods)), color='skyblue', edgecolor='black')
        ax.set_title("🎛️ Mood Distribution Over Time")
        ax.set_ylabel("Bloom Count")
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=len(data), interval=600, repeat=False)
    ani.save(OUTPUT, writer="pillow")
    print(f"[MoodTransition] 🎛️ Saved → {OUTPUT}")
