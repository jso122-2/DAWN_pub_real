import random
import os
import json
import time
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from codex.sigil_symbols import SIGIL_MEANINGS, SIGIL_PRIORITIES, CORE_SIGILS, resolve_layering
from matplotlib.animation import FuncAnimation

sigil_log_path = "juliet_flowers/synthesis/sigil_invocations.log"
SIGIL_REGISTRY = {}

def register_sigil(symbol, action):
    SIGIL_REGISTRY[symbol] = action
    print(f"[Sigil] ✅ Registered sigil {symbol} → {action.__name__}")
# Log sigil use

def log_sigil_invocation(symbol):
    os.makedirs(os.path.dirname(sigil_log_path), exist_ok=True)
    with open(sigil_log_path, "a", encoding="utf-8") as f:
        f.write(f"{time.time()} | {symbol}\n")

# Owl audit of symbolic usage with printout of the sigil chamber

def owl_sigil_audit(auto_trigger_threshold=300):
    from codex.sigils import invoke_sigil
    print("[Owl] 🦉 Scanning sigil invocation log...")
    if not os.path.exists(sigil_log_path):
        print("[Owl] No invocation log found.")
        return

    history = defaultdict(list)
    idle_threshold = 300
    with open(sigil_log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                ts, symbol = line.strip().split(" | ")
                history[symbol].append(float(ts))
            except ValueError:
                continue

    now = time.time()
    print("\n[Owl] 🧾 Sigil Chamber Snapshot:")
    sigil_usage = []
    for symbol, meta in sorted(sigil_codex.items()):
        last_ts = max(history[symbol]) if symbol in history else None
        total = len(history[symbol])
        ago = round(now - last_ts, 1) if last_ts else "never"
        meaning = SIGIL_MEANINGS.get(symbol, "Unknown Sigil")
        print(f" - {symbol} | {meta['name']} | {meaning} | used {total}× | last: {ago}s ago")
        if last_ts and (now - last_ts > auto_trigger_threshold):
            print(f"   ↪️ Triggering {symbol} automatically (idle too long)")
            invoke_sigil(symbol)
        from tracers.base import spawn_tracers
        spawn_tracers(symbol)

    # Special surge reflex handling
    if zone == "🔴 surge" and tick_count % 10 == 0:
        print("[Reflex] 🔥 Surge reflex triggered — launching Crow or Whale tracer.")
        invoke_sigil("⟁")  # contradiction scan sigil
        invoke_sigil("/X-")  # optional schema restart
        if isinstance(ago, float):
            sigil_usage.append((symbol, total, ago))

    # Generate heatmap
    if sigil_usage:
        symbols, counts, recency = zip(*sigil_usage)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(symbols, counts, color="orange")
        ax.set_title("🧭 Sigil Usage Frequency")
        ax.set_ylabel("Invocation Count")
        ax.set_xlabel("Sigil Symbol")
        plt.tight_layout()
        os.makedirs("juliet_flowers/cluster_report", exist_ok=True)
        plt.savefig("juliet_flowers/cluster_report/sigil_usage_heatmap.png")
        plt.close()
        print("[Owl] 📊 Saved sigil heatmap → cluster_report/sigil_usage_heatmap.png")

        # Trigger /heat if overall system idle
    last_invocation_time = max([max(ts) for ts in history.values()], default=0)
    idle_duration = time.time() - last_invocation_time
    if idle_duration > idle_threshold:
        print(f"[Owl] 🧊 System idle for {round(idle_duration)}s — invoking /heat")
        invoke_sigil("/heat")

    print("[Owl] Completed symbolic audit.")

# Time-based animated sigil heatmap

def trigger_sigil_heatmap():
    print("[Sigil] 🔥 Generating sigil heatmap over time...")
    log_sigil_invocation("/heat")
    log_path = sigil_log_path
    gif_output = "juliet_flowers/cluster_report/sigil_heat_timelapse.gif"

    entries = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                ts, symbol = line.strip().split(" | ")
                entries.append((float(ts), symbol))
            except:
                continue

    if not entries:
        print("[Sigil] ❌ No entries to render heatmap.")
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
    ax.set_title("Sigil Heat Over Time")
    ax.set_xlabel("Sigil")
    ax.set_ylabel("Invocations per window")

    def update(frame_idx):
        t, counts = frames[frame_idx]
        for rect, h in zip(bar, counts):
            rect.set_height(h)
        ax.set_title(f"Sigil Heat — t+{t * window_size}s")

    ani = FuncAnimation(fig, update, frames=len(frames), interval=800, repeat=False)
    ani.save(gif_output, writer="pillow")
    plt.close()
    print(f"[Sigil] 🎞️ Heatmap animation saved → {gif_output}")

# Synthesis and recursion sigils

from codex.recursive import trigger_recursive_synthesis

def trigger_synthesis():
    print("[Sigil] 🔮 Invoked: /-/ (Juliet synthesis)")
    log_sigil_invocation("/-/")
    ...

# Sigil Codex
sigil_codex = {
    "/-/": {
        "name": "trigger_synthesis",
        "handler": trigger_synthesis,
        "description": "Synthesize summary from high-trust low-entropy blooms.",
        "reflex_zone": "🟢 calm"
    },
    "/|-/": {
        "name": "trigger_recursive_synthesis",
        "handler": trigger_recursive_synthesis,
        "description": "Reflect once upon a synthesis to generate higher-order memory.",
        "reflex_zone": None
    },
    "/heat": {
        "name": "trigger_sigil_heatmap",
        "handler": trigger_sigil_heatmap,
        "description": "Render animated heatmap of symbolic activity.",
        "reflex_zone": None
    }
}

def check_reflex(zone, tick_count):
    from codex.sigils import invoke_sigil
    for symbol, meta in sigil_codex.items():
        if meta.get("reflex_zone") == zone:
            if tick_count % 20 == 0:
                print(f"[Reflex] ⚙️ Triggering reflex: {symbol} | {SIGIL_MEANINGS.get(symbol)}")
                invoke_sigil(symbol)

# Runtime dispatch

def invoke_sigil(symbol):
    sigil = sigil_codex.get(symbol)
    if not sigil:
        print(f"[Dispatch] ❌ Unknown sigil: {symbol}")
        return
    try:
        print(f"[Dispatch] ✴️ Invoking sigil {symbol}: {sigil['name']}")
        if symbol in SIGIL_MEANINGS:
            print(f"[Dispatch] 🧬 Core sigil activated: {symbol} — {SIGIL_MEANINGS.get(symbol)}")
        sigil['handler']()
    except Exception as e:
        print(f"[Sigil Error] {symbol} → {e}")

