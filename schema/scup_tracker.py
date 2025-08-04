"""
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

from ...scup_math import (
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
    """Tracks SCUP state and history for the Semantic Coherence Under Pressure system.
    
    This class manages the state and computation of SCUP values, handling history tracking,
    state updates, and various computation methods. It supports vault integration for
    overrides and logging.
    
    Attributes:
        state (SCUPState): Current state of the SCUP system
        vault_path (Optional[Path]): Path to vault for overrides and logging
        
    Example:
        >>> tracker = SCUPTracker(vault_path="path/to/vault")
        >>> result = tracker.compute_scup(
        ...     alignment=0.8,
        ...     entropy=0.3,
        ...     pressure=0.5,
        ...     method="enhanced"
        ... )
        >>> print(f"SCUP: {result['scup']}, Zone: {result['zone']}")
        SCUP: 0.7500, Zone: 🟢 calm
    """
    
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
        """Compute SCUP with state tracking and optional vault integration.
        
        This is the main entry point for SCUP computation. It handles method selection,
        state updates, and optional vault integration. The method parameter determines
        which computation algorithm to use.
        
        Args:
            alignment: Semantic alignment score (0.0-1.0)
            entropy: System entropy score (0.0-1.0)
            pressure: Current pressure level (0.0-1.0)
            tp_rar: Legacy TP-RAR score (0.0-1.0)
            urgency_level: System urgency (0.0-1.0)
            sigil_entropy: Sigil entropy score (0.0-1.0)
            mood_entropy: Mood entropy score (0.0-1.0)
            bloom_entropy: Bloom entropy score (0.0-1.0)
            drift: System drift value (0.0-1.0)
            tick_id: Current tick ID for logging
            method: Computation method ('basic', 'enhanced', 'recovery', 'legacy', 'auto')
            
        Returns:
            Dict containing:
                - scup: Computed SCUP value (0.0-1.0)
                - zone: Current SCUP zone (🟢 calm, 🟡 creative, 🟠 active, 🔴 critical)
                - stability: System stability score
                - recovery_potential: Available recovery potential
                - method_used: Actual method used for computation
                
        Example:
            >>> tracker = SCUPTracker()
            >>> # Basic computation
            >>> result = tracker.compute_scup(
            ...     alignment=0.8,
            ...     entropy=0.3,
            ...     pressure=0.5
            ... )
            >>> # Enhanced computation with all parameters
            >>> result = tracker.compute_scup(
            ...     alignment=0.8,
            ...     entropy=0.3,
            ...     pressure=0.5,
            ...     mood_entropy=0.4,
            ...     sigil_entropy=0.3,
            ...     bloom_entropy=0.2,
            ...     method="enhanced"
            ... )
        """
        # Check for override first
        if self.vault_path:
            override_result = self._handle_vault_override()
            if override_result:
                return override_result
        
        # Prepare inputs and select method
        inputs = self._prepare_inputs(
            alignment, entropy, pressure, drift,
            mood_entropy, sigil_entropy, bloom_entropy,
            tp_rar, urgency_level
        )
        selected_method = self._select_computation_method(method, inputs)
        
        # Compute SCUP using selected method
        result = self._compute_scup_with_method(inputs, selected_method)
        
        # Update state and handle logging
        self._update_state(result["scup"], inputs.entropy, inputs.pressure)
        self._handle_logging(tick_id, result, inputs)
        
        return result
    
    def _handle_vault_override(self) -> Optional[Dict[str, Any]]:
        """Handle SCUP override from vault"""
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
        return None
    
    def _prepare_inputs(self, 
                       alignment: Optional[float],
                       entropy: Optional[float],
                       pressure: Optional[float],
                       drift: Optional[float],
                       mood_entropy: Optional[float],
                       sigil_entropy: Optional[float],
                       bloom_entropy: Optional[float],
                       tp_rar: Optional[float],
                       urgency_level: Optional[float]) -> SCUPInputs:
        """Prepare and validate input parameters"""
        return SCUPInputs(
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
    
    def _select_computation_method(self, method: str, inputs: SCUPInputs) -> str:
        """Select appropriate SCUP computation method based on available data"""
        if method != "auto":
            return method
            
        if inputs.alignment is not None and inputs.drift is not None:
            return "recovery"
        elif inputs.mood_entropy is not None and inputs.bloom_entropy is not None:
            return "enhanced"
        elif inputs.tp_rar is not None:
            return "legacy"
        return "basic"
    
    def _compute_scup_with_method(self, inputs: SCUPInputs, method: str) -> Dict[str, Any]:
        """Compute SCUP using the specified method"""
        if method == "basic":
            scup_value = compute_basic_scup(inputs)
            return self._create_basic_result(scup_value, method)
        elif method == "enhanced":
            result = compute_enhanced_scup(
                inputs,
                self.state.breathing_phase,
                self._calculate_stability(),
                self.state.emergency_active
            )
            return {**result.__dict__, "method_used": method}
        elif method == "recovery":
            scup_value = compute_recovery_scup(inputs)
            return self._create_basic_result(scup_value, method)
        else:  # legacy
            scup_value = compute_legacy_scup(inputs)
            return self._create_basic_result(scup_value, method)
    
    def _create_basic_result(self, scup_value: float, method: str) -> Dict[str, Any]:
        """Create result dictionary for basic computation methods"""
        return {
            "scup": scup_value,
            "zone": classify_zone(scup_value),
            "stability": self._calculate_stability(),
            "recovery_potential": 0.0,
            "method_used": method
        }
    
    def _handle_logging(self, tick_id: int, result: Dict[str, Any], inputs: SCUPInputs):
        """Handle SCUP logging to vault"""
        if self.vault_path and tick_id % 10 == 0:
            self._log_to_vault(
                result["scup"],
                result["zone"],
                inputs.drift,
                inputs.alignment,
                inputs.entropy
            )
    
    def _update_state(self, scup: float, entropy: float, pressure: float):
        """Update internal state"""
        self._update_history(scup)
        self._update_coherence_buffer(scup, entropy)
        self._update_breathing_phase()
        self._update_recovery_momentum()
    
    def _update_history(self, scup: float):
        """Update SCUP history"""
        self.state.history.append(scup)
        self.state.last_scup = scup
    
    def _update_coherence_buffer(self, scup: float, entropy: float):
        """Update coherence buffer based on current state"""
        if scup > 0.4 and entropy < 0.6:
            self.state.coherence_buffer.append(scup)
    
    def _update_breathing_phase(self):
        """Update breathing phase based on history length"""
        self.state.breathing_phase = (len(self.state.history) % 20) / 20.0
    
    def _update_recovery_momentum(self):
        """Update recovery momentum based on recent history"""
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
        """Analyze SCUP trend over time and provide insights.
        
        This method analyzes the recent SCUP history to determine trends and provide
        insights about the system's stability and direction.
        
        Returns:
            Dict containing:
                - trend: Current trend ('improving', 'declining', 'stable', 'no_data')
                - current: Most recent SCUP value
                - average: Average SCUP over history
                - min: Minimum SCUP value
                - max: Maximum SCUP value
                - stability: Current stability score
                
        Example:
            >>> tracker = SCUPTracker()
            >>> # Compute some SCUP values
            >>> tracker.compute_scup(alignment=0.8, entropy=0.3)
            >>> tracker.compute_scup(alignment=0.9, entropy=0.2)
            >>> # Analyze trend
            >>> analysis = tracker.analyze_trend()
            >>> print(f"Trend: {analysis['trend']}")
            >>> print(f"Stability: {analysis['stability']}")
            Trend: improving
            Stability: 0.850
        """
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
    """Compute SCUP using the global tracker instance.
    
    This is a convenience function that uses the global SCUP tracker instance
    to compute SCUP values. It accepts the same parameters as SCUPTracker.compute_scup().
    
    Args:
        **kwargs: Same parameters as SCUPTracker.compute_scup()
        
    Returns:
        Dict containing SCUP computation results
        
    Example:
        >>> # Basic computation
        >>> result = compute_scup(
        ...     alignment=0.8,
        ...     entropy=0.3,
        ...     pressure=0.5
        ... )
        >>> # Enhanced computation
        >>> result = compute_scup(
        ...     alignment=0.8,
        ...     entropy=0.3,
        ...     pressure=0.5,
        ...     mood_entropy=0.4,
        ...     method="enhanced"
        ... )
    """
    return scup_tracker.compute_scup(**kwargs)

def calculate_SCUP(drift: float, alignment: float, entropy: float) -> float:
    """Legacy function for simple SCUP calculation.
    
    This is a simplified version of SCUP computation that uses only the three
    core parameters. It's maintained for backward compatibility.
    
    Args:
        drift: System drift value (0.0-1.0)
        alignment: Semantic alignment score (0.0-1.0)
        entropy: System entropy score (0.0-1.0)
        
    Returns:
        float: Computed SCUP value (0.0-1.0)
        
    Example:
        >>> scup = calculate_SCUP(drift=0.2, alignment=0.8, entropy=0.3)
        >>> print(f"SCUP: {scup:.3f}")
        SCUP: 0.448
    """
    result = scup_tracker.compute_scup(
        drift=drift,
        alignment=alignment,
        entropy=entropy,
        method="recovery"
    )
    return result["scup"]

def classify_scup_zone(scup_score: float) -> str:
    """Convert SCUP score to operational zone.
    
    This function maps a SCUP score to its corresponding operational zone,
    which indicates the system's current state.
    
    Args:
        scup_score: SCUP value to classify (0.0-1.0)
        
    Returns:
        str: Zone emoji and name ('🟢 calm', '🟡 creative', '🟠 active', '🔴 critical')
        
    Example:
        >>> zone = classify_scup_zone(0.85)
        >>> print(zone)
        🟢 calm
        >>> zone = classify_scup_zone(0.25)
        >>> print(zone)
        🔴 critical
    """
    return classify_zone(scup_score)

def log_scup(tick_id: int, scup_score: float, zone: str, 
            log_path: str = "logs/scup_log.csv"):
    """Log SCUP values to a CSV file.
    
    This function writes SCUP values to a CSV log file, maintaining a history
    of SCUP computations for analysis.
    
    Args:
        tick_id: Current tick ID
        scup_score: Computed SCUP value
        zone: Current SCUP zone
        log_path: Path to log file (default: "logs/scup_log.csv")
        
    Example:
        >>> log_scup(
        ...     tick_id=42,
        ...     scup_score=0.85,
        ...     zone="🟢 calm",
        ...     log_path="custom_log.csv"
        ... )
    """
    import os
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{tick_id},{scup_score:.4f},{zone}\n") 