# scup_loop.py

def calculate_SCUP(delta_vector, pulse_pressure, drift_variance):
    """
    Semantic Coherence Under Pressure (SCUP)
    Measures system stability based on:
    - delta_vector: semantic shift between ticks
    - pulse_pressure: schema pressure from pulse heat
    - drift_variance: mood or cluster alignment shift
    """
    weight_vector = 0.4
    weight_pressure = 0.4
    weight_drift = 0.2

    scup = 1.0 - (
        (delta_vector * weight_vector) +
        (pulse_pressure * weight_pressure) +
        (drift_variance * weight_drift)
    )

    return round(max(0.0, min(1.0, scup)), 4)
