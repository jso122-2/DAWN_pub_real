# /schema/mood_urgency_probe.py

from core.schema_anomaly_logger import log_anomaly
import math
from typing import Dict, Optional, Tuple

def mood_urgency_probe(mood_state: dict = None) -> float:
    """
    Computes urgency level based on dominant mood pressure with enhanced dynamics.

    Args:
        mood_state (dict): A dictionary of mood intensities, e.g.
            {'reflective': 0.32, 'resilient': 0.18, 'curious': 0.45}

    Returns:
        float: urgency level from 0.0 (calm) to 1.0 (urgent)
    """
    if not mood_state or len(mood_state) == 0:
        log_anomaly("PhantomReference", "DAWN requested 'mood_urgency' without prior definition.")
        return 0.0  # Safe fallback for now

    # Calculate mood complexity (entropy-like measure)
    total_intensity = sum(mood_state.values())
    if total_intensity == 0:
        return 0.0
    
    complexity = _calculate_mood_complexity(mood_state, total_intensity)
    dominant_mood, pressure = _get_dominant_mood(mood_state)
    
    # Base urgency from dominant mood pressure
    base_urgency = min(max(pressure, 0.0), 1.0)
    
    # Modulate based on mood type and complexity
    mood_modifier = _get_mood_urgency_modifier(dominant_mood)
    complexity_factor = _calculate_complexity_factor(complexity)
    
    # Final urgency calculation with non-linear scaling
    urgency = base_urgency * mood_modifier * complexity_factor
    urgency = _apply_urgency_curve(urgency)
    
    # Clamp to valid range
    urgency = min(max(urgency, 0.0), 1.0)
    
    print(f"[MoodUrgency] 🧠 Dominant: {dominant_mood} ({pressure:.3f}) | "
          f"Complexity: {complexity:.3f} | Urgency: {urgency:.3f}")
    
    return urgency

def _calculate_mood_complexity(mood_state: Dict[str, float], total_intensity: float) -> float:
    """Calculate Shannon entropy-like complexity of mood distribution."""
    complexity = 0.0
    for intensity in mood_state.values():
        if intensity > 0:
            normalized = intensity / total_intensity
            complexity -= normalized * math.log2(normalized)
    return complexity

def _get_dominant_mood(mood_state: Dict[str, float]) -> Tuple[str, float]:
    """Get the dominant mood and its intensity."""
    dominant_mood = max(mood_state, key=mood_state.get)
    pressure = mood_state[dominant_mood]
    return dominant_mood, pressure

def _get_mood_urgency_modifier(mood: str) -> float:
    """Get urgency modifier based on mood type."""
    urgency_modifiers = {
        'anxious': 1.4,
        'excited': 1.2,
        'curious': 1.1,
        'reflective': 0.8,
        'calm': 0.6,
        'resilient': 0.9,
        'frustrated': 1.3,
        'focused': 1.0,
        'dreamy': 0.7,
        'alert': 1.15
    }
    return urgency_modifiers.get(mood.lower(), 1.0)  # Default neutral

def _calculate_complexity_factor(complexity: float) -> float:
    """Convert complexity to urgency factor - higher complexity = higher urgency."""
    # Sigmoid-like function: complex emotional states create more urgency
    return 0.7 + 0.6 / (1 + math.exp(-2 * (complexity - 1.5)))

def _apply_urgency_curve(urgency: float) -> float:
    """Apply non-linear curve to urgency for more natural distribution."""
    # Gentle S-curve to avoid extreme values while preserving sensitivity
    return urgency * urgency * (3.0 - 2.0 * urgency)

def get_mood_urgency_definition() -> Dict[str, str]:
    """Return schema definition for mood_urgency calculation."""
    return {
        "function": "mood_urgency_probe",
        "description": "Calculates urgency from mood state complexity and dominance",
        "inputs": ["mood_state: Dict[str, float]"],
        "outputs": ["urgency: float [0.0, 1.0]"],
        "dependencies": ["core.schema_anomaly_logger"],
        "complexity_algorithm": "Shannon entropy with mood-specific modifiers",
        "curve_function": "Cubic smoothstep for natural distribution"
    }
