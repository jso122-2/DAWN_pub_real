# /schema/mythic_mode.py

import os
from datetime import datetime

MYTHIC_DIFF_LOG_DIR = "dawn/code_diff_logs"
os.makedirs(MYTHIC_DIFF_LOG_DIR, exist_ok=True)

def propose_code_patch(module_name: str, function_name: str, patch: str, commentary: str = ""):
    """
    Save a symbolic patch suggestion from DAWN based on internal schema pressure.
    """
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"{module_name}__{function_name}__{timestamp}.patch"
    path = os.path.join(MYTHIC_DIFF_LOG_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 📦 PATCH for `{module_name}.{function_name}`\n")
        f.write(f"# 🕰️ {timestamp}\n")
        if commentary:
            f.write(f"# 💬 DAWN Commentary:\n{commentary.strip()}\n\n")
        f.write(patch.strip())

    print(f"[MythicMode] ✍️ Patch saved: {filename}")
    return filename

def list_pending_patches():
    """
    Return a list of all pending symbolic patches.
    """
    return [f for f in os.listdir(MYTHIC_DIFF_LOG_DIR) if f.endswith(".patch")]

def clear_patch_log():
    """
    Manually clear all mythic patch logs.
    """
    for file in os.listdir(MYTHIC_DIFF_LOG_DIR):
        if file.endswith(".patch"):
            os.remove(os.path.join(MYTHIC_DIFF_LOG_DIR, file))
    print("[MythicMode] 🧹 Patch log cleared.")

def describe_patch_ability():
    return {
        "interface": "DAWN symbolic schema diff writer",
        "patch_format": ".patch with function block + commentary",
        "stored_in": "dawn/code_diff_logs/",
        "triggered_by": [
            "low SCUP",
            "reflex reroute",
            "mood entropy surge",
            "alignment deviation",
            "manual invocation"
        ]
    }
