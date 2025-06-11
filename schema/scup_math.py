"""
SCUP Math Module
===============
Pure mathematical calculations for Semantic Coherence Under Pressure
"""

from dataclasses import dataclass
from typing import Dict, Optional
import math

# Constants
ZONE_CALM_THRESHOLD = 0.8
ZONE_CREATIVE_THRESHOLD = 0.5
ZONE_CRITICAL_THRESHOLD = 0.3
ZONE_EMERGENCY_THRESHOLD = 0.1

# Recovery seeds for stability
COHERENCE_SEEDS = {
    "baseline": 0.15,
    "breath": 0.05,
    "memory": 0.10,
    "self": 0.08
}

@dataclass
class SCUPInputs:
    """Immutable input parameters for SCUP calculation"""
    alignment: float = 0.5
    entropy: float = 0.5
    pressure: float = 0.5
    drift: float = 0.0
    mood_entropy: Optional[float] = None
    sigil_entropy: Optional[float] = None
    bloom_entropy: Optional[float] = None
    tp_rar: Optional[float] = None
    urgency_level: Optional[float] = None

@dataclass
class SCUPOutputs:
    """Immutable output values from SCUP calculation"""
    scup: float
    zone: str
    tension: float
    stability: float
    recovery_potential: float
    breathing_phase: float
    emergency_active: bool

def compute_basic_scup(inputs: SCUPInputs) -> float:
    """Basic SCUP calculation with pressure, entropy, and drift"""
    weight_pressure = 0.4
    weight_entropy = 0.4
    weight_drift = 0.2
    
    scup = 1.0 - (
        (inputs.pressure * weight_pressure) +
        (inputs.entropy * weight_entropy) +
        (inputs.drift * weight_drift)
    )
    
    return max(0.0, min(1.0, scup))

def compute_enhanced_scup(inputs: SCUPInputs, 
                         breathing_phase: float,
                         stability_factor: float,
                         emergency_active: bool) -> SCUPOutputs:
    """Enhanced SCUP with full recovery mechanisms"""
    # Core formula
    raw_scup = 1.0 - abs(inputs.alignment - inputs.entropy)
    
    # Pressure modulation
    pressure_factor = compute_pressure_factor(inputs.pressure)
    
    # Total entropy
    total_entropy = compute_weighted_entropy(
        inputs.mood_entropy or 0.5,
        inputs.sigil_entropy or 0.5,
        inputs.bloom_entropy or 0.5
    )
    
    # Coherence floor
    coherence_floor = compute_coherence_floor(raw_scup, total_entropy)
    
    # Breathing bonus
    breathing_bonus = compute_breathing_bonus(breathing_phase, emergency_active)
    
    # Composite SCUP
    composite_scup = (
        raw_scup * pressure_factor * 0.4 +
        coherence_floor * 0.2 +
        breathing_bonus * 0.1 +
        stability_factor * 0.2 +
        (inputs.tp_rar or 0.5) * 0.1
    )
    
    # Emergency recovery
    if composite_scup < ZONE_EMERGENCY_THRESHOLD:
        composite_scup = compute_emergency_recovery(composite_scup)
        emergency_active = True
    else:
        emergency_active = False
    
    # Calculate tension
    tension = abs(composite_scup - total_entropy)
    
    # Zone classification
    zone = classify_zone(composite_scup)
    
    return SCUPOutputs(
        scup=round(composite_scup, 4),
        zone=zone,
        tension=round(tension, 4),
        stability=round(stability_factor, 3),
        recovery_potential=compute_recovery_potential(composite_scup),
        breathing_phase=round(breathing_phase, 2),
        emergency_active=emergency_active
    )

def compute_recovery_scup(inputs: SCUPInputs) -> float:
    """Recovery-focused SCUP calculation"""
    # Validate inputs
    drift = max(0.0, min(1.0, inputs.drift))
    alignment = max(0.0, min(1.0, inputs.alignment))
    entropy = max(0.0, min(1.0, inputs.entropy))
    
    # Recovery formula
    scup = alignment * (1 - drift) * (1 - entropy)
    
    return round(scup, 3)

def compute_legacy_scup(inputs: SCUPInputs) -> float:
    """Legacy SCUP calculation"""
    coherence = 1.0
    
    # Apply decay factors
    coherence -= (inputs.pressure * 0.3)
    coherence -= (inputs.urgency_level or 0.5) * 0.2
    coherence -= (inputs.sigil_entropy or 0.5) * 0.3
    coherence -= (inputs.entropy * 0.2)
    
    # Alignment penalty
    if inputs.tp_rar is not None:
        coherence -= (1.0 - inputs.tp_rar) * 0.2
    else:
        coherence -= 0.1
    
    return max(0.0, min(coherence, 1.0))

def compute_pressure_factor(pressure: float) -> float:
    """Modulate based on pressure"""
    if pressure > 0.9:
        return 0.7 - (pressure - 0.9) * 0.5
    elif pressure < 0.2:
        return 1.1 + (0.2 - pressure) * 0.5
    else:
        return 1.0 - pressure * 0.3

def compute_weighted_entropy(mood: float, sigil: float, bloom: float) -> float:
    """Calculate weighted total entropy"""
    mood_weight = 0.4
    sigil_weight = 0.4
    bloom_weight = 0.2
    return (mood * mood_weight + sigil * sigil_weight + bloom * bloom_weight)

def compute_coherence_floor(raw_scup: float, entropy: float) -> float:
    """Ensure minimum coherence"""
    floor = COHERENCE_SEEDS["baseline"]
    
    if entropy < 0.5:
        floor += COHERENCE_SEEDS["breath"]
    if raw_scup > 0:
        floor += COHERENCE_SEEDS["self"]
    
    return min(floor, 0.4)

def compute_breathing_bonus(phase: float, emergency_active: bool) -> float:
    """Natural breathing rhythm for stability"""
    breath_value = (math.sin(phase * 2 * math.pi) + 1) * 0.5
    return breath_value * (0.3 if emergency_active else 0.1)

def compute_emergency_recovery(scup: float) -> float:
    """Emergency coherence injection"""
    recovery_boost = 0.3
    recovered_scup = scup + recovery_boost
    return min(recovered_scup, 0.5)

def compute_recovery_potential(current_scup: float) -> float:
    """Recovery potential calculation"""
    base_potential = sum(COHERENCE_SEEDS.values())
    total_potential = base_potential + 0.2
    headroom = 1.0 - current_scup
    return round(min(total_potential, headroom), 3)

def classify_zone(scup: float) -> str:
    """Classify SCUP into operational zones"""
    if scup >= ZONE_CALM_THRESHOLD:
        return "🟢 calm"
    elif scup >= ZONE_CREATIVE_THRESHOLD:
        return "🟡 creative"  
    elif scup >= ZONE_CRITICAL_THRESHOLD:
        return "🟠 active"
    else:
        return "🔴 critical" 