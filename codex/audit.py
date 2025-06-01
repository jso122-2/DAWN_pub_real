
import os
import time
import matplotlib.pyplot as plt
from collections import defaultdict
from codex.registry import sigil_codex, invoke_sigil

def owl_sigil_audit(auto_trigger_threshold=300):
    path = "juliet_flowers/synthesis/sigil_invocations.log"
    if not os.path.exists(path):
        print("[Owl] No invocation log found.")
        return

    history = defaultdict(list)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                ts, symbol = line.strip().split(" | ")
                history[symbol].append(float(ts))
            except:
                continue

    now = time.time()
    sigil_usage = []
    print("\n[Owl] 🧾 Sigil Chamber Snapshot:")
    for symbol, meta in sorted(sigil_codex.items()):
        last_ts = max(history[symbol]) if symbol in history else None
        total = len(history[symbol])
        ago = round(now - last_ts, 1) if last_ts else "never"
        print(f" - {symbol} | {meta['name']} | used {total}× | last: {ago}s ago")
        if last_ts and (now - last_ts > auto_trigger_threshold):
            print(f"   ↪️ Triggering {symbol} automatically (idle too long)")
            invoke_sigil(symbol)

