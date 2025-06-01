# /core/scup.py

import os
from statistics import mean

def compute_scup(tp_rar, pressure_score, urgency_level, sigil_entropy, pulse, entropy_log):
    """
    Compute Semantic Coherence Under Pressure (SCUP).
    
    A composite score representing system coherence given:
    - Current pressure score (heat)
    - Urgency (mood-based)
    - Sigil entropy (semantic overload)
    - Historical entropy (recent chaos)
    - tp_rar = Thought-Priority Reflective Alignment Ratio (structural alignment snapshot)

    Returns a float between 0.0 and 1.0
    """
    # Baseline coherence
    coherence = 1.0

    # Live decay factors
    coherence -= (pressure_score * 0.3)       # Thermal strain
    coherence -= (urgency_level * 0.2)        # Time/priority strain
    coherence -= (sigil_entropy * 0.3)        # Symbolic overload

    # Historical entropy
    if entropy_log:
        recent_entropy = mean(entropy_log[-5:])
        coherence -= (recent_entropy * 0.2)    # Chaotic memory residue

    # Alignment penalty (if low or missing)
    if tp_rar is not None:
        coherence -= (1.0 - tp_rar) * 0.2      # Misaligned intent
    else:
        coherence -= 0.1                       # Default penalty if tp_rar undefined

    # Final safety clamp
    return max(0.0, min(coherence, 1.0))


def classify_scup_zone(scup_score):
    """
    Convert SCUP score into operational zones.
    """
    if scup_score >= 0.7:
        return "🟢 calm"
    elif scup_score >= 0.4:
        return "🟡 active"
    else:
        return "🔴 surge"


def log_scup(tick_id, scup_score, zone, log_path="logs/scup_log.csv"):
    """
    Append SCUP score to CSV log.
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{tick_id},{scup_score:.4f},{zone}\n")
