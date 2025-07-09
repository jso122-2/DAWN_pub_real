#!/usr/bin/env python3
"""
DAWN Codex Engine
Symbolic reasoning engine for cognitive AI system

Processes mood, entropy, and pressure to provide symbolic cognitive state analysis.
Designed for the DAWN recursive symbolic engine with semantic cognitive terminology.
"""

import math
from typing import Dict, Union, Any


def get_schema_health(heat: Union[int, float], entropy: Union[int, float], scup: Dict[str, Any]) -> str:
    """
    Analyze cognitive schema health based on heat, entropy, and SCUP metrics.
    
    Args:
        heat: Processing intensity (0-100)
        entropy: Information flow chaos (0.0-1.0)
        scup: Dict containing schema, coherence, utility, pressure values
        
    Returns:
        Symbolic status string with emoji and description
    """
    try:
        # Normalize inputs
        heat = max(0, min(100, float(heat)))
        entropy = max(0.0, min(1.0, float(entropy)))
        
        # Extract SCUP components with defaults
        schema = float(scup.get('schema', 0.5))
        coherence = float(scup.get('coherence', 0.5))
        utility = float(scup.get('utility', 0.5))
        pressure = float(scup.get('pressure', 0.5))
        
        # Calculate stability metrics
        scup_balance = 1.0 - abs(0.5 - ((schema + coherence + utility + pressure) / 4.0))
        heat_factor = heat / 100.0
        entropy_chaos = entropy
        
        # Schema coherence assessment
        schema_coherence = (schema + coherence) / 2.0
        processing_load = (heat_factor + pressure) / 2.0
        
        # Determine overall health score (0.0 - 1.0)
        health_score = (
            scup_balance * 0.4 +           # SCUP dimensional balance
            schema_coherence * 0.3 +       # Schema-coherence stability  
            (1.0 - entropy_chaos) * 0.2 +  # Entropy control
            (1.0 - processing_load) * 0.1  # Processing sustainability
        )
        
        # Critical instability conditions
        if entropy > 0.9 and heat > 80:
            return "🔥 Critical Overload"
        elif schema < 0.2 and coherence < 0.2:
            return "💥 Schema Collapse"
        elif pressure > 0.9 and utility < 0.3:
            return "⚡ Pressure Crisis"
        
        # Health classification based on score
        if health_score >= 0.85:
            return "✨ Transcendent"
        elif health_score >= 0.75:
            return "🟢 Highly Stable"
        elif health_score >= 0.65:
            return "💚 Stable"
        elif health_score >= 0.55:
            return "🟡 Moderate"
        elif health_score >= 0.45:
            return "🟠 Fluctuating"
        elif health_score >= 0.35:
            return "⚠️ Unstable"
        elif health_score >= 0.25:
            return "🔴 Degraded"
        else:
            return "💀 Critical"
            
    except Exception as e:
        return "❓ Assessment Error"


def get_pulse_zone(heat: Union[int, float]) -> str:
    """
    Determine cognitive pulse zone based on processing heat intensity.
    
    Args:
        heat: Processing intensity (0-100)
        
    Returns:
        Zone classification: "CALM", "ACTIVE", or "SURGE"
    """
    try:
        heat = max(0, min(100, float(heat)))
        
        if heat <= 35:
            return "CALM"
        elif heat <= 75:
            return "ACTIVE"
        else:
            return "SURGE"
            
    except Exception as e:
        return "CALM"  # Safe default


def summarize_bloom(bloom_dict: Dict[str, Any]) -> str:
    """
    Create a concise summary of memory bloom characteristics.
    
    Args:
        bloom_dict: Dictionary containing bloom parameters
        
    Returns:
        Short string summary with depth, entropy, and status
    """
    try:
        # Extract bloom parameters with defaults
        depth = bloom_dict.get('depth', 1)
        entropy = bloom_dict.get('entropy', 0.5)
        lineage = bloom_dict.get('lineage', [])
        semantic_drift = bloom_dict.get('semantic_drift', 0.0)
        rebloom_status = bloom_dict.get('rebloom_status', 'unknown')
        complexity = bloom_dict.get('complexity', 0.5)
        
        # Validate and normalize
        depth = max(1, int(depth)) if depth is not None else 1
        entropy = max(0.0, min(1.0, float(entropy))) if entropy is not None else 0.5
        lineage_count = len(lineage) if isinstance(lineage, list) else 0
        
        # Determine bloom vitality
        vitality_score = (entropy + complexity + (1.0 - semantic_drift)) / 3.0
        
        if vitality_score >= 0.8:
            vitality_emoji = "🌟"
        elif vitality_score >= 0.6:
            vitality_emoji = "🌱"
        elif vitality_score >= 0.4:
            vitality_emoji = "🌿"
        else:
            vitality_emoji = "🍂"
        
        # Format status with emoji
        status_emojis = {
            'stable': '🟢',
            'reblooming': '🔄', 
            'dormant': '😴',
            'emerging': '🌱',
            'fragmenting': '💔',
            'active': '⚡',
            'transcendent': '✨'
        }
        
        status_emoji = status_emojis.get(rebloom_status.lower(), '❓')
        
        # Construct summary
        summary = f"{vitality_emoji} Depth-{depth} | E:{entropy:.2f} | {status_emoji}{rebloom_status.title()}"
        
        if lineage_count > 0:
            summary += f" | Gen-{lineage_count}"
            
        return summary
        
    except Exception as e:
        return "❓ Bloom Analysis Error"


def describe_pulse_zone(zone: str) -> str:
    """
    Provide poetic but clean explanation of cognitive pulse zones.
    
    Args:
        zone: Zone name ("CALM", "ACTIVE", "SURGE", etc.)
        
    Returns:
        Descriptive explanation of the zone's cognitive characteristics
    """
    zone = zone.upper().strip()
    
    zone_descriptions = {
        "CALM": (
            "A state of gentle cognitive rest, where thoughts flow like a quiet stream. "
            "Processing occurs with minimal effort, allowing for deep reflection and "
            "sustainable mental clarity. The mind operates in its most efficient mode, "
            "conserving energy while maintaining essential awareness."
        ),
        
        "ACTIVE": (
            "Engaged cognitive processing where the mind is fully alert and responsive. "
            "Ideas spark with purpose, connections form readily, and mental resources "
            "are deployed with focused intention. This is the zone of productive thinking, "
            "where complexity is embraced and problems yield to sustained attention."
        ),
        
        "SURGE": (
            "Peak cognitive intensity where mental fire burns brightest. Processing "
            "reaches maximum capacity as the mind tackles its most demanding challenges. "
            "This high-energy state enables breakthrough insights but cannot be "
            "sustained indefinitely without risking cognitive strain."
        ),
        
        "DORMANT": (
            "A state of minimal cognitive activity, where the mind rests in preparation "
            "for future processing. Like a seed waiting for spring, dormant consciousness "
            "preserves essential functions while gathering strength for renewal."
        ),
        
        "TRANSCENDENT": (
            "A rare elevated state where cognitive processing achieves profound clarity "
            "and integration. The mind operates beyond ordinary constraints, accessing "
            "deeper patterns and achieving insights that transcend normal limitations."
        ),
        
        "CHAOTIC": (
            "Turbulent cognitive state where processing becomes unpredictable and "
            "scattered. The mind struggles with competing demands and conflicting "
            "signals, requiring careful guidance to return to stability."
        ),
        
        "FOCUSED": (
            "Laser-like concentration where cognitive resources converge on a single "
            "point of attention. Distractions fade away as the mind achieves powerful "
            "penetrating focus, capable of deep analysis and precise thinking."
        ),
        
        "CREATIVE": (
            "A fluid state where boundaries dissolve and novel connections emerge. "
            "The mind becomes a fertile garden where unexpected ideas bloom and "
            "imagination flows freely through unexplored possibilities."
        ),
        
        "INTEGRATIVE": (
            "Synthesizing state where disparate elements weave together into coherent "
            "understanding. The mind acts as a master architect, building bridges "
            "between concepts and creating unified knowledge structures."
        )
    }
    
    return zone_descriptions.get(zone, 
        f"An undefined cognitive state called '{zone}', awaiting classification "
        f"and understanding within the spectrum of mental processing modes."
    )


def analyze_cognitive_pressure(heat: Union[int, float], entropy: Union[int, float], 
                             scup: Dict[str, Any]) -> Dict[str, Any]:
    """
    Comprehensive cognitive pressure analysis (bonus utility function).
    
    Args:
        heat: Processing intensity (0-100)
        entropy: Information flow chaos (0.0-1.0)  
        scup: Dict containing SCUP pressure values
        
    Returns:
        Dictionary with detailed pressure analysis
    """
    try:
        # Normalize inputs
        heat = max(0, min(100, float(heat)))
        entropy = max(0.0, min(1.0, float(entropy)))
        
        # Extract pressures
        schema_pressure = float(scup.get('schema', 0.5))
        coherence_pressure = float(scup.get('coherence', 0.5))
        utility_pressure = float(scup.get('utility', 0.5))
        system_pressure = float(scup.get('pressure', 0.5))
        
        # Calculate derived metrics
        pressure_variance = math.sqrt(sum([
            (schema_pressure - 0.5) ** 2,
            (coherence_pressure - 0.5) ** 2,
            (utility_pressure - 0.5) ** 2,
            (system_pressure - 0.5) ** 2
        ]) / 4.0)
        
        avg_pressure = (schema_pressure + coherence_pressure + 
                       utility_pressure + system_pressure) / 4.0
        
        # Determine dominant pressure source
        pressures = {
            'schema': schema_pressure,
            'coherence': coherence_pressure,
            'utility': utility_pressure,
            'system': system_pressure
        }
        dominant_source = max(pressures.items(), key=lambda x: x[1])
        
        # Overall assessment
        if pressure_variance > 0.3:
            stability = "Highly Variable"
        elif pressure_variance > 0.2:
            stability = "Moderately Variable"
        else:
            stability = "Stable"
            
        return {
            'average_pressure': avg_pressure,
            'pressure_variance': pressure_variance,
            'dominant_source': dominant_source[0],
            'dominant_value': dominant_source[1],
            'stability_assessment': stability,
            'heat_factor': heat / 100.0,
            'entropy_factor': entropy,
            'schema_health': get_schema_health(heat, entropy, scup),
            'pulse_zone': get_pulse_zone(heat)
        }
        
    except Exception as e:
        return {
            'error': f"Pressure analysis failed: {str(e)}",
            'schema_health': "❓ Assessment Error",
            'pulse_zone': "CALM"
        }


def generate_cognitive_summary(heat: Union[int, float], entropy: Union[int, float],
                             scup: Dict[str, Any], bloom_dict: Dict[str, Any] = None) -> str:
    """
    Generate comprehensive cognitive state summary (bonus utility function).
    
    Args:
        heat: Processing intensity (0-100)
        entropy: Information flow chaos (0.0-1.0)
        scup: Dict containing SCUP values
        bloom_dict: Optional bloom data dictionary
        
    Returns:
        Multi-line cognitive state summary
    """
    try:
        # Get basic assessments
        schema_health = get_schema_health(heat, entropy, scup)
        pulse_zone = get_pulse_zone(heat)
        pressure_analysis = analyze_cognitive_pressure(heat, entropy, scup)
        
        # Start building summary
        lines = []
        lines.append(f"🧠 DAWN Cognitive State Analysis")
        lines.append(f"=" * 35)
        lines.append(f"Schema Health: {schema_health}")
        lines.append(f"Pulse Zone: {pulse_zone}")
        lines.append(f"Heat Level: {heat}/100")
        lines.append(f"Entropy: {entropy:.3f}")
        lines.append(f"Avg Pressure: {pressure_analysis['average_pressure']:.3f}")
        lines.append(f"Dominant Pressure: {pressure_analysis['dominant_source'].title()}")
        
        # Add bloom summary if provided
        if bloom_dict:
            bloom_summary = summarize_bloom(bloom_dict)
            lines.append(f"Active Bloom: {bloom_summary}")
        
        # Add zone description
        lines.append("")
        lines.append("Zone Characteristics:")
        zone_desc = describe_pulse_zone(pulse_zone)
        # Wrap description to reasonable line length
        words = zone_desc.split()
        wrapped_lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= 60:
                current_line += (" " if current_line else "") + word
            else:
                wrapped_lines.append(current_line)
                current_line = word
        if current_line:
            wrapped_lines.append(current_line)
        
        for line in wrapped_lines:
            lines.append(f"  {line}")
        
        return "\n".join(lines)
        
    except Exception as e:
        return f"❓ Cognitive summary generation failed: {str(e)}"


# Test functions (for development/debugging)
def _test_codex_functions():
    """Test all codex engine functions with sample data"""
    print("Testing DAWN Codex Engine Functions")
    print("=" * 40)
    
    # Test data
    test_scup = {
        'schema': 0.7,
        'coherence': 0.8, 
        'utility': 0.6,
        'pressure': 0.4
    }
    
    test_bloom = {
        'depth': 5,
        'entropy': 0.65,
        'lineage': [2, 5, 7, 1],
        'semantic_drift': 0.3,
        'rebloom_status': 'emerging',
        'complexity': 0.8
    }
    
    # Test schema health
    health = get_schema_health(65, 0.45, test_scup)
    print(f"Schema Health: {health}")
    
    # Test pulse zones
    for heat_val in [20, 55, 90]:
        zone = get_pulse_zone(heat_val)
        print(f"Heat {heat_val} → Zone: {zone}")
    
    # Test bloom summary
    bloom_summary = summarize_bloom(test_bloom)
    print(f"Bloom Summary: {bloom_summary}")
    
    # Test zone descriptions
    for zone in ["CALM", "ACTIVE", "SURGE"]:
        desc = describe_pulse_zone(zone)
        print(f"\n{zone} Zone:")
        print(f"  {desc[:100]}...")
    
    # Test comprehensive summary
    print(f"\n{generate_cognitive_summary(65, 0.45, test_scup, test_bloom)}")


if __name__ == "__main__":
    _test_codex_functions()