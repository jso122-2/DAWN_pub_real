# schema_health_index.py

import json
import os
from core.tick_emitter import current_tick


# 🔍 Load rebloom volatility from lineage log
def load_rebloom_volatility():
    lineage_log = "juliet_flowers/cluster_report/rebloom_lineage.json"
    if not os.path.exists(lineage_log):
        return 0, 0

    with open(lineage_log, "r") as f:
        try:
            lineage_data = json.load(f)
            if not isinstance(lineage_data, dict):
                print(f"[SCHEMA] ⚠️ Expected dict but got {type(lineage_data)}")
                return 0, 0
        except Exception as e:
            print(f"[SCHEMA] ⚠️ Failed to load rebloom lineage: {e}")
            return 0, 0

    total = len(lineage_data)
    volatile = sum(
        1 for bloom in lineage_data.values()
        if bloom.get("generation_depth", 0) < 2
    )

    return volatile, total



# 🩺 Compute Schema Health Index using SCUP and rebloom entropy penalties
def update_schema_health(scup_value):
    volatile, total = load_rebloom_volatility()
    volatile_ratio = (volatile / total) if total else 0

    penalty = min(0.2, volatile_ratio * 0.5)
    shi = round(max(0.0, min(1.0, scup_value * (1 - penalty))), 4)

    # 📊 Log SHI curve
    output_file = "juliet_flowers/cluster_report/schema_health_curve.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "a") as f:
        f.write(f"{current_tick()},{shi:.4f}\n")

    return shi


def calculate_SHI(pulse_avg, active_blooms, sealed_blooms, sigil_entropy_list):
    """
    Composite metric combining:
    - pulse_avg: average heat across recent ticks
    - bloom density: active / (active + sealed)
    - entropy: mean of sigil entropy scores
    """
    from statistics import mean

    if active_blooms + sealed_blooms == 0:
        density = 0
    else:
        density = active_blooms / (active_blooms + sealed_blooms)

    entropy_score = mean(sigil_entropy_list) if sigil_entropy_list else 0

    shi = (pulse_avg * 0.4) + (density * 0.3) + (entropy_score * 0.3)
    return round(shi, 4)
