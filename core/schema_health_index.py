# File Path: /src/core/schema_health_index.py

import numpy as np
from schema.schema_state import get_current_zone  # Assuming this is for schema's current zone state
from owl.owl_tracer_log import owl_log

# Function to calculate schema entropy based on bloom state
def get_schema_entropy(active_blooms):
    """
    Calculate the schema's entropy based on the entropy scores of active blooms.
    Entropy can be defined as a measure of uncertainty or disorder in the schema.
    """
    if not active_blooms:
        return 0.0

    # Calculate entropy as the average of the entropy scores of active blooms
    avg_entropy = np.mean([b.entropy_score for b in active_blooms])
    return min(1.0, avg_entropy / 1.5)

# Compute the overall Schema Health Index (SHI)
def compute_shi(
    recent_pulse_heat,             # List of floats
    active_blooms,                 # List of bloom objects
    tracer_diplomacy_log,          # List of tuples (tick, seed_id, action)
    nutrient_flow_report           # Dict: seed_id → total flow value
):
    """
    Compute overall Schema Health Index (SHI) in range [0.0, 1.0].
    SHI considers pulse volatility, bloom entropy, tracer diplomacy, and nutrient flow.
    """

    # 1. 🔥 Pulse Volatility Penalty
    if len(recent_pulse_heat) < 2:
        pulse_penalty = 0.0
    else:
        heat_std = np.std(recent_pulse_heat)
        pulse_penalty = min(1.0, heat_std / 5.0)  # Scaled penalty based on pulse volatility

    # 2. 🌸 Bloom Entropy Penalty
    entropy_penalty = get_schema_entropy(active_blooms)  # Using the get_schema_entropy function
    if not active_blooms:
        entropy_penalty = 0.0

    # 3. 🕸️ Tracer Friction Penalty
    hybrid_count = sum(1 for _, _, action in tracer_diplomacy_log if "+" in action)
    total_count = len(tracer_diplomacy_log) or 1
    friction_penalty = hybrid_count / total_count  # Proportion of diplomatic actions

    # 4. 🌱 Nutrient Density Bonus
    if not nutrient_flow_report:
        nutrient_bonus = 0.0
    else:
        avg_nutrient = np.mean(list(nutrient_flow_report.values()))
        nutrient_bonus = min(1.0, avg_nutrient / 5.0)  # Normalize the nutrient flow value

    # Final SHI Score
    penalty = (pulse_penalty + entropy_penalty + friction_penalty) / 3.0
    shi = max(0.0, min(1.0, nutrient_bonus * (1.0 - penalty)))

    # Optional: Log the SHI calculation for audit purposes
    owl_log(f"[SHI] Calculated SHI: {shi} | Pulse Penalty: {pulse_penalty} | "
            f"Entropy Penalty: {entropy_penalty} | Friction Penalty: {friction_penalty} | "
            f"Nutrient Bonus: {nutrient_bonus}")

    return round(shi, 4)

