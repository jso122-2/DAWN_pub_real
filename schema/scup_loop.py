from collections import deque
import matplotlib.pyplot as plt
import os
import csv
import time

# === Configurable Weights ===
SCUP_WEIGHTS = {
    "delta_vector": 0.4,
    "pulse_pressure": 0.4,
    "drift_variance": 0.2
}

# === Internal State ===
_SCUP_HISTORY = deque(maxlen=100)
_LATEST_SCUP = 0.85  # default on boot

# === Core SCUP Calculation ===
def calculate_SCUP(delta_vector, pulse_pressure, drift_variance):
    wv = SCUP_WEIGHTS["delta_vector"]
    wp = SCUP_WEIGHTS["pulse_pressure"]
    wd = SCUP_WEIGHTS["drift_variance"]

    scup = 1.0 - ((delta_vector * wv) + (pulse_pressure * wp) + (drift_variance * wd))
    clamped = round(max(0.0, min(1.0, scup)), 4)
    update_scup_history(clamped)
    return clamped

# === Adaptive Reinforcement ===
def reinforce_scup_weights(scup, feedback="positive"):
    zone, _ = get_zone_from_scup(scup)
    adjustment = 0.02 if feedback == "positive" else -0.02

    if zone == "🔴":
        SCUP_WEIGHTS["delta_vector"] = max(0.1, SCUP_WEIGHTS["delta_vector"] + adjustment)
        SCUP_WEIGHTS["pulse_pressure"] = min(0.6, SCUP_WEIGHTS["pulse_pressure"] - adjustment)
        print(f"[SCUP] 🎯 Reinforced: vector ↑, pressure ↓")
    elif zone == "🟢" and feedback == "positive":
        print(f"[SCUP] ✅ Positive feedback — stability locked.")

def print_scup_weights():
    print("[SCUP] ⚖️ Weights:", dict(SCUP_WEIGHTS))

# === History Tracking ===
def update_scup_history(value):
    global _LATEST_SCUP
    _LATEST_SCUP = value
    _SCUP_HISTORY.append(value)

def get_latest_scup():
    return _LATEST_SCUP

def get_scup_trend():
    if len(_SCUP_HISTORY) < 2:
        return _LATEST_SCUP, 0.0
    avg = round(sum(_SCUP_HISTORY) / len(_SCUP_HISTORY), 4)
    slope = round(_SCUP_HISTORY[-1] - _SCUP_HISTORY[-2], 4)
    return avg, slope

def get_scup_zone():
    score = _LATEST_SCUP
    if score >= 0.75:
        return "🟢 stable"
    elif score >= 0.4:
        return "🟡 adaptive"
    return "🔴 breakdown"

def get_zone_from_scup(scup=None):
    val = scup if scup is not None else _LATEST_SCUP
    if val >= 0.75:
        return "🟢", "stable"
    elif val >= 0.4:
        return "🟡", "adaptive"
    return "🔴", "breakdown"

def get_zone_pressure_weight(zone_emoji):
    return {
        "🟢": 0.1,
        "🟡": 0.4,
        "🔴": 0.9
    }.get(zone_emoji, 0.4)

def print_scup_summary():
    avg, slope = get_scup_trend()
    zone = get_scup_zone()
    print(f"[SCUP] 📈 Avg={avg:.4f} | Δ={slope:+.4f} | Zone={zone}")

# === Data Export & Visualization ===
def export_scup_history(path="logs/scup_history.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["index", "scup"])
        for i, val in enumerate(_SCUP_HISTORY):
            writer.writerow([i, val])
    print(f"[SCUP] 🧾 Exported history to {path}")

def plot_scup_heatmap(save_path="logs/scup_over_time.png"):
    if not _SCUP_HISTORY:
        print("[SCUP] ⚠️ No SCUP data to plot.")
        return
    fig, ax = plt.subplots(figsize=(10, 2))
    values = list(_SCUP_HISTORY)
    ax.imshow([values], cmap="viridis", aspect="auto", extent=[0, len(values), 0, 1])
    ax.set_title("🧠 SCUP Stability Over Time")
    ax.set_xlabel("Ticks")
    ax.set_yticks([])
    ax.set_xlim(0, len(values))
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
    print(f"[SCUP] 🟡 Heatmap saved to {save_path}")

# === Loop Entrypoint ===
def scup_loop():
    """
    Main SCUP loop invoked by DAWN every 25 ticks.
    Reassesses trend, logs summary, and reinforces weights if needed.
    """
    avg, slope = get_scup_trend()
    zone_emoji, zone_label = get_zone_from_scup()
    print(f"[SCUP_LOOP] 🔁 Tick | Avg={avg:.3f} | Δ={slope:+.3f} | Zone={zone_emoji} {zone_label}")
    
    if zone_emoji == "🔴" and slope < 0:
        reinforce_scup_weights(avg, feedback="negative")
    elif zone_emoji == "🟢" and slope >= 0:
        reinforce_scup_weights(avg, feedback="positive")
