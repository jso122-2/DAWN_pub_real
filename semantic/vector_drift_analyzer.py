# semantic/vector_drift_analyzer.py

import math

def compute_drift_score(vec1, vec2):
    """
    Compute angular and Euclidean drift between two semantic vectors.

    Args:
        vec1 (list[float]): Prior semantic state vector
        vec2 (list[float]): Current semantic state vector

    Returns:
        tuple[float, float]: angle (radians), magnitude (0–1 normalized drift)
    """
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0, 0.0

    dot = sum(a * b for a, b in zip(vec1, vec2))
    mag1 = math.sqrt(sum(a * a for a in vec1))
    mag2 = math.sqrt(sum(b * b for b in vec2))

    angle = math.acos(min(max(dot / (mag1 * mag2 + 1e-8), -1.0), 1.0))  # radians
    magnitude = math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))
    normalized_magnitude = min(magnitude / len(vec1), 1.0)

    print(f"[DriftAnalyzer] ↔︎ Angle: {angle:.3f} rad | Magnitude: {normalized_magnitude:.3f}")
    return angle, normalized_magnitude
