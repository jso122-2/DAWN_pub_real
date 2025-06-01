import json
from datetime import datetime
import os

LOG_PATH = "owl/owl_log.json"

def load_logs(path=LOG_PATH):
    if not os.path.exists(path):
        print("❌ No owl_log.json found.")
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def summarize_logs(logs):
    if not logs:
        print("🕊️ No entries to summarize.")
        return

    timestamps = [datetime.fromisoformat(log["timestamp"]) for log in logs]
    messages = [log["message"] for log in logs]

    print(f"📅 Log Timeline: {min(timestamps)} → {max(timestamps)}")
    print(f"📜 Total Entries: {len(messages)}")

    # 🧭 Drift Summary
    drift_lines = [m for m in messages if "Δ =" in m or "drift" in m.lower()]
    if drift_lines:
        print(f"🧭 Drift Events: {len(drift_lines)}")
        for line in drift_lines[-3:]:
            print(f"   • {line}")

    # 🧬 Entropy Summary
    entropy_lines = [m for m in messages if "Entropy" in m or "entropy" in m.lower()]
    if entropy_lines:
        print(f"🧬 Entropy Mentions: {len(entropy_lines)}")
        for line in entropy_lines[-3:]:
            print(f"   • {line}")

    # 🧠 SCUP & Pressure
    scup_alerts = [m for m in messages if "SCUP" in m or "pressure" in m.lower()]
    if scup_alerts:
        print(f"🧠 SCUP/Pressure Events: {len(scup_alerts)}")
        for line in scup_alerts[-3:]:
            print(f"   • {line}")

def run_analyzer():
    logs = load_logs()
    summarize_logs(logs)

if __name__ == "__main__":
    run_analyzer()
