# /core/visual_reflex_launcher.py

import subprocess
from core.visual_reflex_registry import VISUAL_REFLEXES
from core.schema_anomaly_logger import log_anomaly

def launch_reflex(name):
    path = VISUAL_REFLEXES.get(name)
    if not path:
        log_anomaly("VisualReflexFail", f"No reflex named '{name}'")
        return

    try:
        subprocess.Popen(["python", path])
        log_anomaly("VisualReflex", f"Reflex '{name}' launched → {path}")
    except Exception as e:
        log_anomaly("VisualReflexError", f"Failed to launch '{name}': {str(e)}")
