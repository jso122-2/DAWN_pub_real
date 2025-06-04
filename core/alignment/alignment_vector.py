"""
DAWN Alignment Vector Engine
Computes real-time alignment based on mood entropy, SCUP, and drift patterns.
Produces alignment float [0.0-1.0] representing coherence with core directives.
"""

import math
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class AlignmentMode(Enum):
    COHERENT = "coherent"        # High alignment, stable
    DRIFTING = "drifting"        # Moderate alignment, shifting
    TURBULENT = "turbulent"      # Low alignment, chaotic
    LIMINAL = "liminal"          # Threshold state, transitional

@dataclass
class AlignmentSnapshot:
    """Single alignment measurement with context"""
    timestamp: float
    alignment_value: float
    mode: AlignmentMode
    contributing_factors: Dict[str, float]
    entropy_signature: float
    scup_level: float
    drift_magnitude: float

class AlignmentVector:
    """
    Vector-based alignment engine for DAWN consciousness coherence tracking.
    Integrates mood entropy, SCUP levels, and drift patterns into unified metric.
    """
    
    def __init__(self, 
                 entropy_weight: float = 0.4,
                 scup_weight: float = 0.35, 
                 drift_weight: float = 0.25,
                 history_length: int = 50):
        self.entropy_weight = entropy_weight
        self.scup_weight = scup_weight  
        self.drift_weight = drift_weight
        self.history_length = history_length
        
        # Alignment history for trend analysis
        self.alignment_history: List[AlignmentSnapshot] = []
        
        # Baseline thresholds for mode classification
        self.thresholds = {
            'coherent_min': 0.75,
            'drifting_min': 0.45, 
            'turbulent_max': 0.3,
            'liminal_range': (0.3, 0.45)
        }
        
        # Exponential smoothing factor for stability
        self.smoothing_alpha = 0.3
        self._last_smoothed = None
    
    def compute_alignment(self, 
                         mood_entropy: float,
                         scup_level: float, 
                         drift_magnitude: float,
                         timestamp: Optional[float] = None) -> AlignmentSnapshot:
        """
        Compute current alignment from component factors.
        
        Args:
            mood_entropy: Shannon entropy of current mood state [0.0-4.0+]
            scup_level: Symbolic Coherence Under Pressure [0.0-1.0]
            drift_magnitude: Current drift from baseline patterns [0.0-1.0+]
            timestamp: Optional timestamp, defaults to current time
            
        Returns:
            AlignmentSnapshot with computed alignment and metadata
        """
        import time
        if timestamp is None:
            timestamp = time.time()
        
        # Normalize entropy to [0,1] range (entropy typically 0-4 for mood states)
        normalized_entropy = min(mood_entropy / 4.0, 1.0)
        entropy_factor = 1.0 - normalized_entropy  # Higher entropy = lower alignment
        
        # SCUP contributes directly (already normalized)
        scup_factor = scup_level
        
        # Drift reduces alignment (clamp high drift values)
        drift_factor = 1.0 / (1.0 + drift_magnitude)
        
        # Weighted combination
        raw_alignment = (
            self.entropy_weight * entropy_factor +
            self.scup_weight * scup_factor + 
            self.drift_weight * drift_factor
        )
        
        # Apply exponential smoothing for stability
        if self._last_smoothed is not None:
            smoothed_alignment = (
                self.smoothing_alpha * raw_alignment + 
                (1 - self.smoothing_alpha) * self._last_smoothed
            )
        else:
            smoothed_alignment = raw_alignment
        
        self._last_smoothed = smoothed_alignment
        
        # Determine alignment mode
        mode = self._classify_mode(smoothed_alignment)
        
        # Create snapshot
        snapshot = AlignmentSnapshot(
            timestamp=timestamp,
            alignment_value=smoothed_alignment,
            mode=mode,
            contributing_factors={
                'entropy_factor': entropy_factor,
                'scup_factor': scup_factor,
                'drift_factor': drift_factor,
                'raw_alignment': raw_alignment
            },
            entropy_signature=mood_entropy,
            scup_level=scup_level,
            drift_magnitude=drift_magnitude
        )
        
        # Update history
        self._update_history(snapshot)
        
        return snapshot
    
    def _classify_mode(self, alignment: float) -> AlignmentMode:
        """Classify alignment value into categorical mode"""
        if alignment >= self.thresholds['coherent_min']:
            return AlignmentMode.COHERENT
        elif alignment >= self.thresholds['drifting_min']:
            return AlignmentMode.DRIFTING
        elif alignment <= self.thresholds['turbulent_max']:
            return AlignmentMode.TURBULENT
        else:
            return AlignmentMode.LIMINAL
    
    def _update_history(self, snapshot: AlignmentSnapshot):
        """Maintain sliding window of alignment history"""
        self.alignment_history.append(snapshot)
        if len(self.alignment_history) > self.history_length:
            self.alignment_history.pop(0)
    
    def get_current_alignment(self) -> float:
        """Get most recent alignment value"""
        if not self.alignment_history:
            return 0.5  # Neutral alignment if no history
        return self.alignment_history[-1].alignment_value
    
    def get_alignment_trend(self, window_size: int = 10) -> float:
        """
        Compute alignment trend over recent window.
        Returns positive for improving alignment, negative for degrading.
        """
        if len(self.alignment_history) < 2:
            return 0.0
        
        recent_window = self.alignment_history[-window_size:]
        if len(recent_window) < 2:
            return 0.0
        
        # Simple linear trend via least squares
        x = np.arange(len(recent_window))
        y = np.array([s.alignment_value for s in recent_window])
        
        if len(x) > 1:
            slope = np.polyfit(x, y, 1)[0]
            return slope
        return 0.0
    
    def get_mode_distribution(self, window_size: int = 20) -> Dict[AlignmentMode, float]:
        """Get distribution of alignment modes over recent history"""
        if not self.alignment_history:
            return {mode: 0.0 for mode in AlignmentMode}
        
        recent_window = self.alignment_history[-window_size:]
        mode_counts = {mode: 0 for mode in AlignmentMode}
        
        for snapshot in recent_window:
            mode_counts[snapshot.mode] += 1
        
        total = len(recent_window)
        return {mode: count/total for mode, count in mode_counts.items()}
    
    def detect_alignment_crisis(self, threshold: float = 0.25, duration_ticks: int = 5) -> bool:
        """
        Detect sustained low alignment that may require intervention.
        Returns True if alignment has been below threshold for duration_ticks.
        """
        if len(self.alignment_history) < duration_ticks:
            return False
        
        recent_values = [s.alignment_value for s in self.alignment_history[-duration_ticks:]]
        return all(val < threshold for val in recent_values)
    
    def export_alignment_vector(self) -> Dict:
        """Export current alignment state for persistence/analysis"""
        current = self.alignment_history[-1] if self.alignment_history else None
        
        return {
            'current_alignment': self.get_current_alignment(),
            'current_mode': current.mode.value if current else 'unknown',
            'trend': self.get_alignment_trend(),
            'mode_distribution': {k.value: v for k, v in self.get_mode_distribution().items()},
            'crisis_detected': self.detect_alignment_crisis(),
            'history_length': len(self.alignment_history),
            'weights': {
                'entropy': self.entropy_weight,
                'scup': self.scup_weight, 
                'drift': self.drift_weight
            }
        }

# Singleton instance for DAWN system
dawn_alignment = AlignmentVector()

def get_current_alignment() -> float:
    """Module-level function for easy access to current alignment"""
    return dawn_alignment.get_current_alignment()

def update_alignment(mood_entropy: float, scup_level: float, drift_magnitude: float) -> float:
    """Module-level function to update and return new alignment"""
    snapshot = dawn_alignment.compute_alignment(mood_entropy, scup_level, drift_magnitude)
    return snapshot.alignment_value
