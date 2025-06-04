# /core/pulse.py

MOOD_PULSE_MAP = {
    "joyful":     1.1,
    "focused":    1.0,
    "reflective": 0.9,
    "curious":    1.2,
    "anxious":    1.5,
    "angry":      1.7,
    "sad":        1.3
}

def mood_to_pulse(mood, base_heat=1.0):
    """
    Adjust pulse strength based on mood.
    Returns updated pulse heat multiplier.
    """
    mood_factor = MOOD_PULSE_MAP.get(mood, 1.0)
    adjusted_heat = base_heat * mood_factor
    return adjusted_heat
