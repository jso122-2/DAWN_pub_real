# File Path: /src/core/schema_health_index.py

import numpy as np
from schema.schema_state import get_current_zone  # Assuming this is for schema's current zone state
from owl.owl_tracer_log import owl_log
from codex import get_schema_health, get_pulse_zone, analyze_cognitive_pressure

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


def compute_enhanced_shi_with_codex(
    recent_pulse_heat,             # List of floats
    active_blooms,                 # List of bloom objects
    tracer_diplomacy_log,          # List of tuples (tick, seed_id, action)
    nutrient_flow_report,          # Dict: seed_id → total flow value
    current_entropy=0.5,           # Current system entropy
    current_scup=0.5              # Current SCUP value
):
    """
    Enhanced Schema Health Index computation integrating DAWN Codex Engine analysis.
    
    Returns:
        Dict containing both traditional SHI and enhanced codex-based analysis
    """
    
    # Calculate traditional SHI
    traditional_shi = compute_shi(
        recent_pulse_heat, active_blooms, tracer_diplomacy_log, nutrient_flow_report
    )
    
    # Calculate average heat for codex analysis
    avg_heat = np.mean(recent_pulse_heat) if recent_pulse_heat else 0.3
    heat_scaled = avg_heat * 100  # Convert to 0-100 scale
    
    # Build SCUP dictionary for codex analysis
    scup_dict = {
        'schema': current_scup,
        'coherence': traditional_shi,  # Use SHI as coherence measure
        'utility': min(1.0, len(active_blooms) / 10.0) if active_blooms else 0.5,  # Bloom utility
        'pressure': avg_heat  # Heat as pressure indicator
    }
    
    # Get codex engine analysis
    schema_health_symbolic = get_schema_health(heat_scaled, current_entropy, scup_dict)
    pulse_zone = get_pulse_zone(heat_scaled)
    pressure_analysis = analyze_cognitive_pressure(heat_scaled, current_entropy, scup_dict)
    
    # Create enhanced SHI report
    enhanced_shi = {
        'traditional_shi': traditional_shi,
        'symbolic_health': schema_health_symbolic,
        'pulse_zone': pulse_zone,
        'entropy_level': current_entropy,
        'average_heat': avg_heat,
        'active_bloom_count': len(active_blooms) if active_blooms else 0,
        'pressure_analysis': pressure_analysis,
        'health_score': traditional_shi,  # Traditional SHI as base health score
        'recommendations': _generate_shi_recommendations(schema_health_symbolic, pulse_zone, pressure_analysis)
    }
    
    # Enhanced logging
    owl_log(f"[Enhanced SHI] Traditional: {traditional_shi:.4f} | "
            f"Symbolic: {schema_health_symbolic} | Zone: {pulse_zone} | "
            f"Entropy: {current_entropy:.3f} | Blooms: {len(active_blooms) if active_blooms else 0}")
    
    return enhanced_shi


def _generate_shi_recommendations(symbolic_health: str, pulse_zone: str, pressure_analysis: dict) -> list:
    """Generate actionable recommendations based on codex analysis"""
    
    recommendations = []
    
    # Schema health based recommendations
    if "Critical" in symbolic_health or "Degraded" in symbolic_health:
        recommendations.extend([
            "Emergency schema stabilization required",
            "Reduce cognitive load immediately",
            "Activate coherence recovery protocols"
        ])
    elif "Unstable" in symbolic_health or "Fluctuating" in symbolic_health:
        recommendations.extend([
            "Monitor schema coherence patterns",
            "Consider gentle parameter adjustments",
            "Increase observation frequency"
        ])
    elif "Transcendent" in symbolic_health:
        recommendations.extend([
            "Optimal cognitive state - maintain current parameters",
            "Consider exploring advanced capabilities",
            "Document successful configuration"
        ])
    
    # Pulse zone based recommendations
    if pulse_zone == "SURGE" and "Critical" in symbolic_health:
        recommendations.append("High-energy state with instability - reduce heat immediately")
    elif pulse_zone == "CALM" and "Stable" in symbolic_health:
        recommendations.append("Excellent foundation state - safe for exploration")
    elif pulse_zone == "ACTIVE":
        recommendations.append("Balanced processing state - monitor for optimization opportunities")
    
    # Pressure analysis recommendations
    if pressure_analysis.get('stability_assessment') == "Highly Variable":
        recommendations.append("Address pressure variance - investigate source instability")
    
    dominant_pressure = pressure_analysis.get('dominant_source', 'unknown')
    if dominant_pressure == 'system' and pressure_analysis.get('dominant_value', 0) > 0.8:
        recommendations.append("High system pressure detected - consider load balancing")
    
    return recommendations[:5]  # Limit to top 5 recommendations


def get_current_schema_health_status():
    """
    Convenience function to get current schema health status using codex engine.
    Returns a simplified status for quick checks.
    """
    try:
        # This would be called with actual system values
        # For now, return a template that shows the integration pattern
        return {
            'status': 'Integration Ready',
            'message': 'DAWN Codex Engine successfully integrated with Schema Health Index',
            'functions_available': [
                'compute_enhanced_shi_with_codex',
                '_generate_shi_recommendations',
                'get_current_schema_health_status'
            ]
        }
    except Exception as e:
        owl_log(f"[Schema Health] Error getting status: {e}", "error")
        return {'status': 'Error', 'message': str(e)}

