# consolidate_scup_system.py
"""
Consolidate all SCUP-related files into unified scup_system.py
"""

from pathlib import Path
from datetime import datetime

def create_unified_scup():
    """Create unified SCUP system from multiple implementations"""
    
    # Create schema directory if it doesn't exist
    schema_dir = Path("schema")
    schema_dir.mkdir(parents=True, exist_ok=True)
    
    # Create scup_math.py
    math_content = '''"""
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
'''
    
    # Create scup_tracker.py
    tracker_content = '''"""
SCUP Tracker Module
=================
State management and history tracking for Semantic Coherence Under Pressure
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import deque
from statistics import mean, stdev
import re
import json

from .scup_math import (
    SCUPInputs, SCUPOutputs, compute_basic_scup, compute_enhanced_scup,
    compute_recovery_scup, compute_legacy_scup, classify_zone
)

@dataclass
class SCUPState:
    """Current state of the SCUP system"""
    history: deque = field(default_factory=lambda: deque(maxlen=100))
    coherence_buffer: deque = field(default_factory=lambda: deque(maxlen=20))
    recovery_momentum: float = 0.0
    breathing_phase: float = 0.0
    emergency_active: bool = False
    emergency_duration: int = 0
    last_scup: float = 0.500
    recovery_count: int = 0

class SCUPTracker:
    """Tracks SCUP state and history"""
    
    def __init__(self, vault_path: Optional[str] = None):
        self.state = SCUPState()
        self.vault_path = Path(vault_path) if vault_path else None
    
    def compute_scup(self, 
                    # Basic parameters
                    alignment: Optional[float] = None,
                    entropy: Optional[float] = None,
                    pressure: Optional[float] = None,
                    
                    # Legacy parameters
                    tp_rar: Optional[float] = None,
                    urgency_level: Optional[float] = None,
                    sigil_entropy: Optional[float] = None,
                    
                    # Enhanced parameters
                    mood_entropy: Optional[float] = None,
                    bloom_entropy: Optional[float] = None,
                    drift: Optional[float] = None,
                    
                    # Metadata
                    tick_id: int = 0,
                    method: str = "auto") -> Dict[str, Any]:
        """
        Compute SCUP with state tracking
        
        Methods:
        - 'basic': Original simple calculation
        - 'enhanced': Full recovery mechanisms
        - 'recovery': Focus on drift/alignment recovery
        - 'legacy': Old compute_scup parameters
        - 'auto': Choose best method based on available data
        """
        # Check for override
        if self.vault_path:
            override = self._check_vault_override()
            if override is not None:
                print(f"[SCUP] Override active: {override}")
                return {
                    "scup": override,
                    "zone": classify_zone(override),
                    "stability": self._calculate_stability(),
                    "recovery_potential": 0.0,
                    "method_used": "override"
                }
        
        # Prepare inputs
        inputs = SCUPInputs(
            alignment=alignment or 0.5,
            entropy=entropy or 0.5,
            pressure=pressure or 0.5,
            drift=drift or 0.0,
            mood_entropy=mood_entropy,
            sigil_entropy=sigil_entropy,
            bloom_entropy=bloom_entropy,
            tp_rar=tp_rar,
            urgency_level=urgency_level
        )
        
        # Auto-select method if needed
        if method == "auto":
            if alignment is not None and drift is not None:
                method = "recovery"
            elif mood_entropy is not None and bloom_entropy is not None:
                method = "enhanced"
            elif tp_rar is not None:
                method = "legacy"
            else:
                method = "basic"
        
        # Route to appropriate calculation
        if method == "basic":
            scup_value = compute_basic_scup(inputs)
            result = {
                "scup": scup_value,
                "zone": classify_zone(scup_value),
                "stability": self._calculate_stability(),
                "recovery_potential": 0.0,
                "method_used": method
            }
        elif method == "enhanced":
            result = compute_enhanced_scup(
                inputs,
                self.state.breathing_phase,
                self._calculate_stability(),
                self.state.emergency_active
            )
            result = result.__dict__
            result["method_used"] = method
        elif method == "recovery":
            scup_value = compute_recovery_scup(inputs)
            result = {
                "scup": scup_value,
                "zone": classify_zone(scup_value),
                "stability": self._calculate_stability(),
                "recovery_potential": 0.0,
                "method_used": method
            }
        else:  # legacy
            scup_value = compute_legacy_scup(inputs)
            result = {
                "scup": scup_value,
                "zone": classify_zone(scup_value),
                "stability": self._calculate_stability(),
                "recovery_potential": 0.0,
                "method_used": method
            }
        
        # Update state
        self._update_state(result["scup"], inputs.entropy, inputs.pressure)
        
        # Log to vault if configured
        if self.vault_path and tick_id % 10 == 0:
            self._log_to_vault(
                result["scup"],
                result["zone"],
                inputs.drift,
                inputs.alignment,
                inputs.entropy
            )
        
        return result
    
    def _update_state(self, scup: float, entropy: float, pressure: float):
        """Update internal state"""
        self.state.history.append(scup)
        self.state.last_scup = scup
        
        if scup > 0.4 and entropy < 0.6:
            self.state.coherence_buffer.append(scup)
        
        # Update breathing phase
        self.state.breathing_phase = (len(self.state.history) % 20) / 20.0
        
        # Update recovery momentum
        if len(self.state.history) > 2:
            recent = list(self.state.history)[-5:]
            if len(recent) > 2:
                trend = recent[-1] - recent[0]
                if trend > 0:
                    self.state.recovery_momentum = min(self.state.recovery_momentum + 0.05, 0.3)
                else:
                    self.state.recovery_momentum = max(self.state.recovery_momentum - 0.02, 0.0)
    
    def _calculate_stability(self) -> float:
        """Calculate system stability"""
        if len(self.state.history) < 3:
            return 0.5
        
        recent = list(self.state.history)[-10:]
        variance = stdev(recent) if len(recent) > 1 else 0.5
        avg_scup = mean(recent)
        
        stability = (1.0 - variance) * 0.5 + avg_scup * 0.5
        return round(stability, 3)
    
    def _check_vault_override(self) -> Optional[float]:
        """Check vault for SCUP override"""
        if not self.vault_path:
            return None
        
        # Priority locations
        priority_files = [
            self.vault_path / "pulse" / "scup_override.md",
            self.vault_path / "scup" / "override.md"
        ]
        
        for file_path in priority_files:
            if file_path.exists():
                override = self._extract_override_from_file(file_path)
                if override is not None:
                    return override
        
        return None
    
    def _extract_override_from_file(self, file_path: Path) -> Optional[float]:
        """Extract SCUP override from markdown frontmatter"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---'):
                end_idx = content.find('---', 3)
                if end_idx > 0:
                    frontmatter = content[3:end_idx]
                    
                    patterns = [
                        r'scup_override:\s*([0-9.]+)',
                        r'SCUP_override:\s*([0-9.]+)',
                        r'override:\s*([0-9.]+)'
                    ]
                    
                    for pattern in patterns:
                        match = re.search(pattern, frontmatter, re.IGNORECASE)
                        if match:
                            override_value = float(match.group(1))
                            override_value = max(0.0, min(1.0, override_value))
                            return override_value
        except:
            pass
        
        return None
    
    def _log_to_vault(self, scup: float, zone: str, drift: Optional[float],
                     alignment: Optional[float], entropy: Optional[float]):
        """Log SCUP to vault with context"""
        if not self.vault_path:
            return
        
        scup_dir = self.vault_path / "scup"
        scup_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now()
        filename = f"scup_log_{timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        filepath = scup_dir / filename
        
        content = f"""---
scup_value: {scup}
zone: {zone}
timestamp: {timestamp.isoformat()}
---

# SCUP Log

**Value**: {scup}  
**Zone**: {zone}
"""
        
        if drift is not None:
            content += f"\n**Drift**: {drift:.3f}"
        if alignment is not None:
            content += f"\n**Alignment**: {alignment:.3f}"
        if entropy is not None:
            content += f"\n**Entropy**: {entropy:.3f}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.state.recovery_count += 1
    
    def analyze_trend(self) -> Dict[str, Any]:
        """Analyze SCUP trend over time"""
        if not self.state.history:
            return {"trend": "no_data"}
        
        scup_values = list(self.state.history)
        
        if len(scup_values) >= 2:
            recent_avg = mean(scup_values[-3:])
            older_avg = mean(scup_values[:-3]) if len(scup_values) > 3 else scup_values[0]
            
            if recent_avg > older_avg + 0.05:
                trend = "improving"
            elif recent_avg < older_avg - 0.05:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "trend": trend,
            "current": scup_values[-1] if scup_values else 0.500,
            "average": mean(scup_values) if scup_values else 0.500,
            "min": min(scup_values) if scup_values else 0.500,
            "max": max(scup_values) if scup_values else 0.500,
            "stability": self._calculate_stability()
        }

# Global instance
scup_tracker = SCUPTracker()

# Convenience functions
def compute_scup(**kwargs) -> Dict:
    """Compute SCUP using global tracker"""
    return scup_tracker.compute_scup(**kwargs)

def calculate_SCUP(drift: float, alignment: float, entropy: float) -> float:
    """Legacy function for simple SCUP calculation"""
    result = scup_tracker.compute_scup(
        drift=drift,
        alignment=alignment,
        entropy=entropy,
        method="recovery"
    )
    return result["scup"]

def classify_scup_zone(scup_score: float) -> str:
    """Convert SCUP score to zone"""
    return classify_zone(scup_score)

def log_scup(tick_id: int, scup_score: float, zone: str, 
            log_path: str = "logs/scup_log.csv"):
    """Legacy CSV logging"""
    import os
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{tick_id},{scup_score:.4f},{zone}\n")
'''
    
    # Create scup_system.py
    system_content = '''"""
DAWN Unified SCUP System
========================
Semantic Coherence Under Pressure - The heart of schema stability
Consolidates: scup.py, scup_engine.py, scup_loop.py, scup_recovery.py
Generated: {timestamp}
"""

from .scup_math import (
    SCUPInputs, SCUPOutputs, compute_basic_scup, compute_enhanced_scup,
    compute_recovery_scup, compute_legacy_scup, classify_zone
)
from .scup_tracker import SCUPTracker, compute_scup, calculate_SCUP, log_scup

# Re-export everything for backward compatibility
__all__ = [
    'SCUPInputs',
    'SCUPOutputs',
    'compute_basic_scup',
    'compute_enhanced_scup',
    'compute_recovery_scup',
    'compute_legacy_scup',
    'classify_zone',
    'SCUPTracker',
    'compute_scup',
    'calculate_SCUP',
    'log_scup'
]
'''.format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M'))
    
    # Write files
    with open(schema_dir / "scup_math.py", 'w', encoding='utf-8') as f:
        f.write(math_content)
    
    with open(schema_dir / "scup_tracker.py", 'w', encoding='utf-8') as f:
        f.write(tracker_content)
    
    with open(schema_dir / "scup_system.py", 'w', encoding='utf-8') as f:
        f.write(system_content)
    
    print(f"✅ Created SCUP system files in {schema_dir}")
    
    # Archive originals
    archive_dir = Path("archive/schema_consolidation_20250604")
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    scup_files = ["scup.py", "scup_engine.py", "scup_loop.py", "scup_recovery.py"]
    
    for filename in scup_files:
        src = schema_dir / filename
        if src.exists():
            dst = archive_dir / filename
            src.rename(dst)
            print(f"📦 Archived {filename}")
    
    return schema_dir / "scup_system.py"

if __name__ == "__main__":
    create_unified_scup()