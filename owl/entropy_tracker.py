# owl/entropy_tracker.py

from codex.sigil_memory_ring import get_active_sigil_entropy_list
from statistics import mean
import math

def get_entropy_score(trend=None, pulse_heat=0.0, scup=0.5):
    """
    Compute a normalized entropy score based on sigil memory, mood-pressure trends, and pulse dynamics.
    
    Args:
        trend (list[float]): Rolling list of entropy values (optional).
        pulse_heat (float): Current pulse heat level.
        scup (float): Current semantic coherence under pressure.

    Returns:
        float: Normalized entropy score (0.0 to 1.0)
    """
    sigil_entropy = get_active_sigil_entropy_list()
    base_entropy = mean(sigil_entropy) if sigil_entropy else 0.0

    # Add SCUP modulation — lower SCUP = more entropy weight
    scup_penalty = (1.0 - scup) * 0.4

    # Trend-based volatility penalty
    volatility = 0.0
    if trend and len(trend) > 3:
        diffs = [abs(trend[i] - trend[i - 1]) for i in range(1, len(trend))]
        volatility = min(mean(diffs), 1.0)

    trend_mod = volatility * 0.3
    heat_mod = math.tanh(pulse_heat) * 0.2

    # Final score
    entropy_score = base_entropy + scup_penalty + trend_mod + heat_mod
    entropy_score = max(0.0, min(entropy_score, 1.0))

    print(f"[EntropyTracker] 🔎 Sigil={base_entropy:.3f} | SCUPMod={scup_penalty:.3f} | Volatility={trend_mod:.3f} | HeatMod={heat_mod:.3f} → Entropy={entropy_score:.3f}")

    return entropy_score
