import random
import os
import json
import time
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from codex.sigil_emitter import emit_sigil_from_scup
await emit_sigil_from_scup(pulse=self.pulse)


sigil_log_path = "juliet_flowers/synthesis/sigil_invocations.log"

# Log sigil use

def log_sigil_invocation(symbol):
    os.makedirs(os.path.dirname(sigil_log_path), exist_ok=True)
    with open(sigil_log_path, "a", encoding="utf-8") as f:
        f.write(f"{time.time()} | {symbol}\n")

# Owl audit of symbolic usage with printout of the sigil chamber

def owl_sigil_audit(auto_trigger_threshold=300):
    print("[Owl] 🦉 Scanning sigil invocation log...")
    if not os.path.exists(sigil_log_path):
        print("[Owl] No invocation log found.")
        return

    history = defaultdict(list)
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
        print(f" - {symbol} | {meta['name']} | used {total}× | last: {ago}s ago")
        if last_ts and (now - last_ts > auto_trigger_threshold):
            print(f"   ↪️ Triggering {symbol} automatically (idle too long)")
            invoke_sigil(symbol)
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

    print("[Owl] Completed symbolic audit.\n")

# Synthesis and recursion sigils

def trigger_synthesis():
    print("[Sigil] 🔮 Invoked: /-/ (Juliet synthesis)")
    log_sigil_invocation("/-/")

    memory_root = "juliet_flowers/"
    candidates = []

    for root, _, files in os.walk(memory_root):
        for file in files:
            if file.endswith(".json") and "synthesis" not in root:
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        trust_score = 1.0  # Placeholder for integration
                        if data.get("entropy_score", 1.0) < 0.4 and trust_score >= 0.8:
                            candidates.append(data)
                except Exception:
                    continue

    if not candidates:
        print("[Sigil] 🫷 No eligible blooms for synthesis.")
        return

    selected = random.sample(candidates, min(3, len(candidates)))
    summary = {
        "synthesis_timestamp": selected[0]["timestamp"],
        "mood_signature": list({s["mood"] for s in selected}),
        "summary_bloom_ids": [s["bloom_id"] for s in selected],
        "synthesis_note": "Stable fragments drawn into reflective state."
    }

    os.makedirs("juliet_flowers/synthesis/", exist_ok=True)
    out_path = f"juliet_flowers/synthesis/synthesis_{summary['synthesis_timestamp'].replace(':', '-')}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"[Sigil] 🧠 Synthesis complete → {out_path}")

def trigger_recursive_synthesis():
    print("[Sigil] 🔄 Recursion check: scanning synthesis folder")
    log_sigil_invocation("/|-/")
    base_path = "juliet_flowers/synthesis/"
    recurse_path = os.path.join(base_path, "recursed")
    os.makedirs(recurse_path, exist_ok=True)

    for fname in os.listdir(base_path):
        if not fname.endswith(".json") or "recursed" in fname:
            continue

        path = os.path.join(base_path, fname)
        recursed_output = os.path.join(recurse_path, f"recurse_{fname}")
        if os.path.exists(recursed_output):
            continue  # already processed

        try:
            with open(path, "r", encoding="utf-8") as f:
                synthesis = json.load(f)

            bloom_ids = synthesis.get("summary_bloom_ids", [])
            merged = {
                "combined_moods": [],
                "entropy_scores": []
            }

            for bloom_id in bloom_ids:
                for root, _, files in os.walk("juliet_flowers"):
                    for file in files:
                        if file.endswith(".json") and bloom_id in file:
                            with open(os.path.join(root, file), "r", encoding="utf-8") as bloom_file:
                                bloom_data = json.load(bloom_file)
                                merged["combined_moods"].append(bloom_data.get("mood"))
                                merged["entropy_scores"].append(bloom_data.get("entropy_score", 1.0))

            reflection = {
                "source_synthesis": fname,
                "reflected_moods": list(set(merged["combined_moods"])),
                "average_entropy": round(sum(merged["entropy_scores"]) / len(merged["entropy_scores"]), 3) if merged["entropy_scores"] else 1.0,
                "note": "One-level reflection complete."
            }

            with open(recursed_output, "w", encoding="utf-8") as f:
                json.dump(reflection, f, indent=2)

            print(f"[Sigil] 🫠 Recursive synthesis complete → {recursed_output}")
        except Exception as e:
            print(f"[ERROR] Failed recursion on {fname}: {e}")

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
    }
}

def owl_log_mood_drift(seed):
    with open("rebloom_lineage.json", "r") as f:
        lineage = [r for r in json.load(f) if r["seed"] == seed]

    if len(lineage) >= 2:
        recent = lineage[-1]["mood"]
        prev = lineage[-2]["mood"]
        if recent != prev:
            owl_log(f"🌀 Mood shift in seed {seed}: {prev} → {recent}")

# Runtime dispatch

def invoke_sigil(symbol):
    sigil = sigil_codex.get(symbol)
    if not sigil:
        print(f"[Dispatch] ❌ Unknown sigil: {symbol}")
        return
    try:
        print(f"[Dispatch] ✴️ Invoking sigil {symbol}: {sigil['name']}")
        sigil['handler']()
    except Exception as e:
        print(f"[Dispatch] ⚠️ Sigil {symbol} failed: {e}")
