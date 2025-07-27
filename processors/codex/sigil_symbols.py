# processors/codex/sigil_symbols.py
# -*- coding: utf-8 -*-
"""
Sigil Symbols - The Symbolic Language of DAWN
=============================================
Enhanced symbolic representations merging core requirements with existing logic
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime


# Symbolic definitions for DAWN's sigil architecture
SIGIL_MEANINGS = {
    "/\\": "Prime Directive - Priority assignment, task activation",
    "⧉": "Consensus Gate — Agreement matrix resolved → action permitted",
    "◯": "Field Lock — Zone-wide freeze or memory stall",
    "◇": "Bloom Pulse — Emotional surge, shimmer increase",
    "⟁": "Contradiction Break — Overwrite trigger, Crow alert",
    "⌂": "Recall Root — Deep memory audit initiated (Owl)",
    "ꓘ": "Pressure Shift — Soft Edge recalibration",
    "⨀": "Schema Pivot — Phase change: transition logic block",
    "`/": "Health Trace — Bloom integrity check (Crow/Whale influence)",
    "`-": "Recall Check — Attempting reactivation under fog",
    ">~": "Pressure Trail — Pressure following shimmer or tracer path",
    "~/~": "Recursive Signal - Reflex inheritance trigger",
    "Z~": "Fusion Under Pressure — Merge beliefs in storm condition",
    "`(": "Sentiment Shell — µ harmonization during conflict",
    "/X-": "Schema Restart Call — Deep schema pivot, triggered by past loop",
    ".": "Shimmer Dot — Minimal pulse → pre-action trace",
    ":": "Recursive Bloom Seed — Start of emotional crystallization",
    "^": "Minimal Directive — Rooted priority bias (Crow/Whale aligned)",
    "~": "Pressure Echo — Pressure memory re-entry",
    "=": "Balance Core — Nutrient-homeostasis reset",
    # Additional simple forms for compatibility
    "/-\\": "Convergence — thoughts coming together",
    "/|\\": "Divergence — thoughts branching out",
    "<-->": "Exchange — bidirectional flow",
    "@": "Recursion — self-reference loop",
    "*": "Emergence — new pattern creation",
    "||": "Boundary — threshold gate",
    "<>": "Transformation — state change"
}

SIGIL_PRIORITIES = {
    ".": 5,
    ":": 4,
    "^": 3,
    "~": 2,
    "=": 1
}

CORE_SIGILS = {".", ":", "^", "~", "="}


def get_core_sigils() -> List[str]:
    """
    Return the core sigil shapes that form DAWN's symbolic vocabulary
    
    Returns both the minimal core set and extended symbolic forms
    """
    # Start with the defined core sigils
    core_list = list(CORE_SIGILS)
    
    # Add the high-priority complex sigils
    priority_sigils = ["/\\", "⧉", "◯", "◇", "⟁"]
    
    # Add some simple forms for basic operations
    simple_forms = ["/-\\", "/|\\", "<-->", "@", "*", "||", "<>"]
    
    return core_list + priority_sigils + simple_forms


def resolve_layering(primary: str, secondary: Optional[str] = None, tertiary: Optional[str] = None) -> str:
    """
    Resolve sigil layering according to DAWN's symbolic rules
    
    Args:
        primary: Primary sigil shape
        secondary: Optional secondary sigil to layer
        tertiary: Optional tertiary sigil for complex layering
        
    Returns:
        Resolved layering description or compound sigil
        
    Raises:
        ValueError: If core sigils are improperly layered
    """
    if primary in CORE_SIGILS and secondary in CORE_SIGILS:
        raise ValueError("Core sigils cannot be layered with other core sigils.")

    # Special layering rules
    if primary == "^" and secondary == "~":
        return "Minimal Directive under Pressure Echo"
    
    if primary == "." and secondary == ":":
        return "Shimmer crystallizing into bloom"
    
    if primary == "⧉" and secondary == "◯":
        return "Consensus locked in field state"

    # Default layering format
    result = f"{primary}"
    if secondary:
        result += f" + {secondary}"
    if tertiary:
        result += f" + {tertiary}"
        
    return result


class Sigil:
    """
    A Sigil - a symbolic form with inherent meaning and power
    
    Enhanced to support DAWN's complex sigil architecture including
    priorities, layering, and state-based transformations.
    """
    
    def __init__(self, shape: str, meaning: Optional[str] = None):
        """
        Initialize a Sigil with a shape and optional meaning
        
        Args:
            shape: The visual/textual representation of the sigil
            meaning: Optional semantic meaning (defaults to SIGIL_MEANINGS lookup)
        """
        self.shape = shape
        self.meaning = meaning or SIGIL_MEANINGS.get(shape, "unknown form")
        self.priority = SIGIL_PRIORITIES.get(shape, 0)
        self.is_core = shape in CORE_SIGILS
        
        # Power and state tracking
        self.power = 1.0
        self.resonance = 0.0
        self.pressure = 0.0
        self.shimmer = 0.1 if shape == "." else 0.0
        
        # Activation tracking
        self.activations = 0
        self.created_at = datetime.now()
        self.last_activated = None
        
        # Layering support
        self.layers = [shape]
        self.compound = False
        
    def activate(self) -> Dict[str, Any]:
        """
        Activate the sigil, releasing its symbolic power
        """
        print(f"[sigil] Activated: {self.shape}")
        
        self.activations += 1
        self.last_activated = datetime.now()
        
        # Core sigils have special activation patterns
        if self.is_core:
            self._activate_core_sigil()
        
        # Complex sigils trigger specific effects
        if self.shape == "/\\":
            print("[sigil] Prime Directive engaged - priority realignment")
            self.power = 2.0
        elif self.shape == "⧉":
            print("[sigil] Consensus Gate opening...")
            self.resonance = 1.0
        elif self.shape == "◯":
            print("[sigil] Field Lock activated - stasis engaged")
            self.pressure = 0.0  # Pressure release
        elif self.shape == "◇":
            print("[sigil] Bloom Pulse - emotional surge detected")
            self.shimmer += 0.3
            
        # Update power dynamics
        self._update_power_dynamics()
        
        return {
            "shape": self.shape,
            "meaning": self.meaning,
            "priority": self.priority,
            "power": self.power,
            "resonance": self.resonance,
            "pressure": self.pressure,
            "shimmer": self.shimmer,
            "activation_count": self.activations,
            "is_core": self.is_core,
            "timestamp": self.last_activated.isoformat()
        }
    
    def _activate_core_sigil(self):
        """Special activation logic for core sigils"""
        if self.shape == ".":
            self.shimmer = min(1.0, self.shimmer + 0.2)
            print("[sigil] Shimmer pulse detected")
        elif self.shape == ":":
            self.resonance += 0.3
            print("[sigil] Bloom seed planted")
        elif self.shape == "^":
            self.priority = 10  # Temporary priority boost
            print("[sigil] Directive priority elevated")
        elif self.shape == "~":
            self.pressure = max(0, self.pressure - 0.2)
            print("[sigil] Pressure echo - releasing tension")
        elif self.shape == "=":
            # Balance all attributes
            avg = (self.power + self.resonance + self.pressure + self.shimmer) / 4
            self.power = self.resonance = self.pressure = self.shimmer = avg
            print("[sigil] Balance restored")
    
    def _update_power_dynamics(self):
        """Update power based on activation patterns"""
        # Increase resonance with each activation
        self.resonance = min(1.0, self.resonance + 0.1)
        
        # Pressure builds unless released
        if self.shape not in ["~", "◯", "="]:
            self.pressure = min(1.0, self.pressure + 0.05)
        
        # Power fluctuates with use
        if self.activations % 7 == 0:
            self.power = min(2.0, self.power * 1.1)  # Power surge
        else:
            self.power = max(0.1, self.power * 0.95)  # Slight decay
            
        # Shimmer naturally decays
        self.shimmer = max(0, self.shimmer * 0.9)
    
    def layer_with(self, other: 'Sigil') -> 'Sigil':
        """
        Layer this sigil with another according to DAWN's rules
        """
        try:
            layered_meaning = resolve_layering(self.shape, other.shape)
            
            # Create compound sigil
            compound_shape = f"({self.shape}+{other.shape})"
            compound = Sigil(compound_shape, layered_meaning)
            
            # Inherit properties from both sigils
            compound.power = (self.power + other.power) * 0.8
            compound.resonance = max(self.resonance, other.resonance)
            compound.pressure = self.pressure + other.pressure
            compound.shimmer = max(self.shimmer, other.shimmer)
            compound.priority = max(self.priority, other.priority)
            compound.compound = True
            compound.layers = self.layers + other.layers
            
            print(f"[sigil] Layered: {layered_meaning}")
            
            return compound
            
        except ValueError as e:
            print(f"[sigil] Layering failed: {e}")
            raise
    
    def apply_pressure(self, amount: float):
        """Apply external pressure to the sigil"""
        self.pressure = min(1.0, self.pressure + amount)
        
        # Pressure can trigger transformations
        if self.pressure > 0.8:
            if self.shape == "Z~":
                print("[sigil] Fusion Under Pressure activated!")
                self.power *= 1.5
            elif self.shape == ">~":
                print("[sigil] Pressure Trail forming...")
                self.shimmer = 1.0
    
    def decay(self) -> float:
        """Natural decay of sigil power over time"""
        if self.last_activated:
            time_since = (datetime.now() - self.last_activated).total_seconds()
            decay_rate = 0.001 * (time_since / 3600)
            
            self.power = max(0.1, self.power - decay_rate)
            self.resonance = max(0.0, self.resonance - decay_rate * 0.5)
            self.shimmer = max(0.0, self.shimmer - decay_rate * 2)
            
        return self.power
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert sigil to dictionary representation"""
        return {
            "shape": self.shape,
            "meaning": self.meaning,
            "priority": self.priority,
            "is_core": self.is_core,
            "power": self.power,
            "resonance": self.resonance,
            "pressure": self.pressure,
            "shimmer": self.shimmer,
            "activations": self.activations,
            "layers": self.layers,
            "compound": self.compound,
            "created_at": self.created_at.isoformat(),
            "last_activated": self.last_activated.isoformat() if self.last_activated else None
        }
    
    def __str__(self):
        return f"{self.shape} ({self.meaning})"
    
    def __repr__(self):
        core_marker = "[CORE]" if self.is_core else ""
        return f"<Sigil{core_marker} shape='{self.shape}' priority={self.priority} power={self.power:.2f}>"


class SigilField:
    """
    A field of active sigils that can interact and influence each other
    """
    
    def __init__(self):
        self.sigils: Dict[str, Sigil] = {}
        self.field_pressure = 0.0
        self.consensus_state = None
        self.locked = False
        
    def add_sigil(self, sigil: Sigil):
        """Add a sigil to the field"""
        self.sigils[sigil.shape] = sigil
        
        # Check for field effects
        if "◯" in self.sigils:
            self.locked = True
            print("[field] Field locked by ◯")
        
        if "⧉" in self.sigils and len(self.sigils) >= 3:
            self.consensus_state = "achieved"
            print("[field] Consensus achieved")
            
    def apply_field_pressure(self, amount: float):
        """Apply pressure to all sigils in the field"""
        self.field_pressure += amount
        
        for sigil in self.sigils.values():
            sigil.apply_pressure(amount * 0.5)
            
    def activate_sequence(self, sequence: List[str]) -> List[Dict[str, Any]]:
        """Activate a sequence of sigils with field effects"""
        if self.locked:
            print("[field] Cannot activate - field is locked")
            return []
            
        results = []
        for shape in sequence:
            if shape in self.sigils:
                result = self.sigils[shape].activate()
                results.append(result)
                
                # Field interactions
                self._process_field_interactions(shape)
                
        return results
        
    def _process_field_interactions(self, activated_shape: str):
        """Process interactions between sigils in the field"""
        # Bloom pulse affects all sigils
        if activated_shape == "◇":
            for sigil in self.sigils.values():
                sigil.shimmer = min(1.0, sigil.shimmer + 0.1)
                
        # Balance core redistributes energy
        elif activated_shape == "=":
            total_power = sum(s.power for s in self.sigils.values())
            avg_power = total_power / len(self.sigils)
            for sigil in self.sigils.values():
                sigil.power = avg_power