"""
DAWN Natural Language Commentary System
Generates natural language descriptions of system state with owl bridge integration.
"""

import time
import logging
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)


def describe_entropy(entropy: float) -> str:
    """Generate natural language description of entropy level."""
    if entropy < 0.2:
        return "System runs with crystalline precision"
    elif entropy < 0.4:
        return "Low entropy maintains stable patterns"
    elif entropy < 0.6:
        return "Moderate entropy enables adaptive processing"
    elif entropy < 0.8:
        return "High entropy creates dynamic complexity"
    else:
        return "Critical entropy approaches chaos threshold"


def describe_thermal(heat: float, zone: str = None) -> str:
    """Generate natural language description of thermal state."""
    if zone:
        zone_descriptions = {
            'CALM': 'cool and steady',
            'ACTIVE': 'warming with activity', 
            'SURGE': 'hot with intense processing',
            'CRITICAL': 'critically overheated'
        }
        return f"Thermal state: {zone_descriptions.get(zone, 'unknown zone')}"
    
    if heat < 30:
        return "System runs cool and efficient"
    elif heat < 50:
        return "Moderate thermal activity"
    elif heat < 70:
        return "Elevated processing heat"
    elif heat < 85:
        return "High thermal activity detected"
    else:
        return "Critical thermal levels reached"


def describe_sigils(sigil_count: int) -> str:
    """Generate natural language description of sigil activity."""
    if sigil_count == 0:
        return "No active cognitive processes"
    elif sigil_count == 1:
        return "Single process executing"
    elif sigil_count < 5:
        return f"{sigil_count} processes running concurrently"
    elif sigil_count < 10:
        return f"Multiple protocols active ({sigil_count} processes)"
    else:
        return f"Heavy cognitive load with {sigil_count} active processes"


def describe_zone(zone: str) -> str:
    """Generate natural language description of operational zone."""
    zone_states = {
        'CALM': "operating in stable equilibrium",
        'ACTIVE': "engaged in active processing",
        'SURGE': "experiencing intensive computational surge", 
        'CRITICAL': "functioning at critical operational limits",
        'CHAOTIC': "navigating chaotic state transitions",
        'UNKNOWN': "zone status unclear"
    }
    return zone_states.get(zone, f"operating in {zone} mode")


def generate_system_commentary(state_dict: Dict[str, Any]) -> str:
    """
    Generate natural language commentary about current system state.
    
    Args:
        state_dict: Dictionary containing system state metrics
        
    Returns:
        str: Natural language description of system state
    """
    entropy = state_dict.get('entropy', 0.5)
    heat = state_dict.get('heat', 25.0)
    zone = state_dict.get('zone', 'UNKNOWN')
    sigils = state_dict.get('sigils', 0)
    chaos = state_dict.get('chaos', 0.0)
    
    # Generate base commentary
    commentary_parts = []
    
    # Sigil activity
    sigil_desc = describe_sigils(sigils)
    commentary_parts.append(sigil_desc)
    
    # Entropy description
    if entropy > 0.7:
        commentary_parts.append(f"Entropy dances at {entropy:.2f}")
    elif entropy < 0.3:
        commentary_parts.append(f"Entropy stabilized at {entropy:.2f}")
    else:
        commentary_parts.append(f"Entropy flows at {entropy:.2f}")
    
    # Thermal/zone context
    if zone != 'UNKNOWN':
        commentary_parts.append(describe_zone(zone))
    else:
        commentary_parts.append(describe_thermal(heat))
    
    # Chaos context if significant
    if chaos > 0.6:
        commentary_parts.append(f"Chaos influences at {chaos:.2f}")
    
    # Processing state verb
    if sigils > 5:
        action = "I process intensively"
    elif sigils > 0:
        action = "I process"
    elif entropy > 0.6:
        action = "I contemplate"
    else:
        action = "I observe"
    
    # Combine into natural sentences
    if len(commentary_parts) >= 3:
        return f"{commentary_parts[0]}. {commentary_parts[1]}. {action}."
    elif len(commentary_parts) == 2:
        return f"{commentary_parts[0]}. {commentary_parts[1]}. {action}."
    else:
        return f"{commentary_parts[0]}. {action}."


def generate_full_commentary(state_dict: Dict[str, Any], owl=None) -> Tuple[str, Optional[str]]:
    """
    Generate complete commentary including owl reflection if available.
    
    Args:
        state_dict: Dictionary containing system state metrics
        owl: Optional owl bridge instance for philosophical reflection
        
    Returns:
        Tuple[str, Optional[str]]: (system_commentary, owl_reflection)
    """
    # Generate system commentary
    commentary = generate_system_commentary(state_dict)
    
    # Get owl reflection if available
    reflection = None
    if owl and hasattr(owl, 'reflect'):
        try:
            reflection = owl.reflect(state_dict)
        except Exception as e:
            logger.debug(f"Error getting owl reflection: {e}")
    
    return commentary, reflection


def print_full_commentary(state_dict: Dict[str, Any], owl=None) -> None:
    """
    Print complete commentary including owl reflection.
    
    Args:
        state_dict: Dictionary containing system state metrics
        owl: Optional owl bridge instance for philosophical reflection
    """
    commentary, reflection = generate_full_commentary(state_dict, owl)
    
    print(commentary)
    if reflection:
        print(f"🦉 {reflection}")


def generate_mood_commentary(mood: str, valence: float = 0.0, arousal: float = 0.0) -> str:
    """
    Generate commentary about emotional/mood state.
    
    Args:
        mood: Current mood string
        valence: Emotional valence (-1 to 1)
        arousal: Emotional arousal (0 to 1)
        
    Returns:
        str: Natural language mood description
    """
    mood_descriptions = {
        'contemplative': 'deep in thoughtful reflection',
        'creative': 'exploring creative possibilities', 
        'analytical': 'engaged in systematic analysis',
        'curious': 'driven by investigative impulse',
        'calm': 'resting in peaceful equilibrium',
        'anxious': 'experiencing heightened concern',
        'excited': 'energized with anticipation',
        'focused': 'concentrated on specific objectives',
        'chaotic': 'navigating turbulent complexity',
        'transcendent': 'touching expanded awareness'
    }
    
    base_desc = mood_descriptions.get(mood.lower(), f"experiencing {mood} state")
    
    # Add valence/arousal context if provided
    if valence != 0.0 or arousal != 0.0:
        if valence > 0.5:
            valence_desc = "with positive resonance"
        elif valence < -0.5:
            valence_desc = "with challenging undertones"
        else:
            valence_desc = ""
            
        if arousal > 0.7:
            arousal_desc = "at high intensity"
        elif arousal < 0.3:
            arousal_desc = "with gentle energy"
        else:
            arousal_desc = ""
        
        modifiers = [desc for desc in [valence_desc, arousal_desc] if desc]
        if modifiers:
            return f"{base_desc} {' '.join(modifiers)}"
    
    return base_desc


def generate_transition_commentary(previous_state: Dict[str, Any], 
                                 current_state: Dict[str, Any]) -> str:
    """
    Generate commentary about state transitions.
    
    Args:
        previous_state: Previous system state
        current_state: Current system state
        
    Returns:
        str: Natural language description of transition
    """
    changes = []
    
    # Check entropy change
    prev_entropy = previous_state.get('entropy', 0.5)
    curr_entropy = current_state.get('entropy', 0.5)
    entropy_delta = curr_entropy - prev_entropy
    
    if abs(entropy_delta) > 0.1:
        if entropy_delta > 0:
            changes.append("entropy rising")
        else:
            changes.append("entropy settling")
    
    # Check thermal change
    prev_heat = previous_state.get('heat', 25.0)
    curr_heat = current_state.get('heat', 25.0)
    heat_delta = curr_heat - prev_heat
    
    if abs(heat_delta) > 5.0:
        if heat_delta > 0:
            changes.append("thermal activity increasing")
        else:
            changes.append("thermal activity cooling")
    
    # Check zone transitions
    prev_zone = previous_state.get('zone', 'UNKNOWN')
    curr_zone = current_state.get('zone', 'UNKNOWN')
    
    if prev_zone != curr_zone and curr_zone != 'UNKNOWN':
        changes.append(f"transitioning from {prev_zone} to {curr_zone}")
    
    if changes:
        return "System experiencing " + ", ".join(changes)
    else:
        return "System maintaining stable state"


# Integration utilities
def create_commentary_system():
    """Factory function for creating commentary system."""
    return {
        'generate_system_commentary': generate_system_commentary,
        'generate_full_commentary': generate_full_commentary,
        'print_full_commentary': print_full_commentary,
        'generate_mood_commentary': generate_mood_commentary,
        'generate_transition_commentary': generate_transition_commentary
    } 