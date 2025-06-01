import time

cooldown_log = []

# 🚦 Suppression event triggered by PulseHeat or external schema alert
def trigger_suppression(reason="unknown", level=0.0):
    event = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "reason": reason,
        "level": round(level, 3),
        "action": "schema_cooldown"
    }
    cooldown_log.append(event)
    print(f"[Suppressor] ⛔ Triggered suppression due to {reason.upper()} | Heat={level:.2f}")
    try:
        from tick_engine.tick_engine import adjust_tick_interval
        adjust_tick_interval(multiplier=1.5)  # slow tick cycle by 50%
    except ImportError:
        print("[Suppressor] ⚠️ Tick interval adjustment failed. Fallback in place.")

# 🧪 Diagnostic access to suppression history
def get_cooldown_events():
    return cooldown_log
