
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import defaultdict

def trigger_sigil_heatmap():
    from codex.registry import log_sigil_invocation
    log_sigil_invocation("/heat")
    print("[Sigil] 🔥 Generating sigil heatmap over time...")

    path = "juliet_flowers/synthesis/sigil_invocations.log"
    gif_output = "juliet_flowers/cluster_report/sigil_heat_timelapse.gif"

    if not os.path.exists(path):
        print("[Sigil] ❌ No entries to render heatmap.")
        return

    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                ts, symbol = line.strip().split(" | ")
                entries.append((float(ts), symbol))
            except:
                continue

    if not entries:
        return

    entries.sort()
    start_time = int(entries[0][0])
    window_size = 30

    frame_buckets = defaultdict(lambda: defaultdict(int))
    for ts, symbol in entries:
        bucket = int((ts - start_time) // window_size)
        frame_buckets[bucket][symbol] += 1

    sorted_symbols = sorted({symbol for _, symbol in entries})
    frames = [(t, [frame_buckets[t].get(sym, 0) for sym in sorted_symbols]) for t in sorted(frame_buckets.keys())]

    fig, ax = plt.subplots(figsize=(8, 4))
    bar = ax.bar(sorted_symbols, [0]*len(sorted_symbols), color="crimson")
    ax.set_ylim(0, max(max(counts) for _, counts in frames) + 1)

    def update(frame_idx):
        t, counts = frames[frame_idx]
        for rect, h in zip(bar, counts):
            rect.set_height(h)
        ax.set_title(f"Sigil Heat — t+{t * window_size}s")

    ani = FuncAnimation(fig, update, frames=len(frames), interval=800, repeat=False)
    ani.save(gif_output, writer="pillow")
    plt.close()
    print(f"[Sigil] 🎞️ Heatmap animation saved → {gif_output}")
