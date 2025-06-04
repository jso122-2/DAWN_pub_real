
import os
import time

def log_sigil_invocation(symbol):
    log_path = "juliet_flowers/synthesis/sigil_invocations.log"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{time.time()} | {symbol}\n")

from codex.core_synthesis import trigger_synthesis
from codex.recursive import trigger_recursive_synthesis
from codex.visualization import trigger_sigil_heatmap

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
