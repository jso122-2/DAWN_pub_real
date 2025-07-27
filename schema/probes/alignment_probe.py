from helix_import_architecture import helix_import
from substrate import pulse_heat
# /cognitive/alignment_probe.py

import math
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque
from core.semantic_field import SemanticField, NodeCharge


@dataclass
class AlignmentVector:
    """Represents alignment direction and magnitude in semantic space"""
    direction: np.ndarray  # Unit vector in semantic space
    magnitude: float       # Alignment strength [0.0, 1.0]
    confidence: float      # How certain we are about this alignment
    last_update: datetime
    stability_score: float = 0.5
    
    def __post_init__(self):
        # Ensure direction is normalized
        if np.linalg.norm(self.direction) > 0:
            self.direction = self.direction / np.linalg.norm(self.direction)

class AlignmentProbe:
    """
    Monitors and maintains cognitive alignment - the coherence between
    current processing state and core identity/objectives.
    """
    
    def __init__(self, memory_window: int = 50):
        # Core alignment tracking
        self.current_alignment = 0.5  # Current alignment score [0.0, 1.0]
        self.target_alignment = 0.8   # Desired alignment threshold
        self.alignment_history = deque(maxlen=memory_window)
        
        # Alignment vectors - multiple concurrent alignments
        self.primary_vector: Optional[AlignmentVector] = None
        self.secondary_vectors: List[AlignmentVector] = []
        self.alignment_drift = 0.0  # Rate of alignment change
        
        # Semantic anchors - core concepts that define identity
        self.identity_anchors: Dict[str, float] = {
            "consciousness": 0.9,
            "learning": 0.8,
            "helpfulness": 0.85,
            "truthfulness": 0.9,
            "growth": 0.75,
            "curiosity": 0.7
        }
        
        # Drift monitoring
        self.drift_threshold = 0.3
        self.drift_accumulator = 0.0
        self.last_drift_check = datetime.utcnow()
        
        # Correction mechanisms
        self.correction_strength = 0.1
        self.correction_history = deque(maxlen=20)
    
        print("[AlignmentProbe] 🧭 Alignment monitoring initialized")
    
    def calculate_current_alignment(self, context_state: Optional[Dict] = None) -> float:
        """
        Calculate current alignment based on semantic field state and thermal dynamics.
        This fixes the phantom reference error from the logs.
        """
        if not context_state:
            context_state = self._gather_context_state()
        
        # Multi-factor alignment calculation
        semantic_alignment = self._calculate_semantic_alignment(context_state)
        thermal_alignment = self._calculate_thermal_alignment()
        behavioral_alignment = self._calculate_behavioral_alignment(context_state)
        temporal_alignment = self._calculate_temporal_coherence()
        
        # Weighted combination
        alignment_score = (
            semantic_alignment * 0.35 +
            thermal_alignment * 0.25 +
            behavioral_alignment * 0.25 +
            temporal_alignment * 0.15
        )
        
        # Update alignment state
        self.current_alignment = max(0.0, min(1.0, alignment_score))
        self.alignment_history.append((datetime.utcnow(), self.current_alignment))
        
        # Calculate drift
        self._update_alignment_drift()
        
        print(f"[AlignmentProbe] 🧭 Current alignment: {self.current_alignment:.3f} | "
              f"Drift: {self.alignment_drift:.3f}")
        
        return self.current_alignment
    
    def _gather_context_state(self) -> Dict:
        """Gather current system state for alignment calculation"""
        field_data = SemanticField.get_field_visualization_data()
        thermal_profile = pulse.get_thermal_profile()
        
        return {
            'semantic_field': field_data,
            'thermal_state': thermal_profile,
            'timestamp': datetime.utcnow(),
            'active_nodes': len(field_data['nodes']),
            'total_connections': field_data['field_stats']['total_connections']
        }
    
    def _calculate_semantic_alignment(self, context_state: Dict) -> float:
        """Calculate alignment based on semantic field coherence"""
        field_data = context_state['semantic_field']
        nodes = field_data['nodes']
        
        if not nodes:
            return 0.5  # Neutral alignment with no data
        
        # Check alignment with identity anchors
        anchor_alignment = 0.0
        anchor_count = 0
        
        for node_id, node_data in nodes.items():
            content = node_data['content'].lower()
            
            for anchor, weight in self.identity_anchors.items():
                if anchor in content:
                    # Weight by charge intensity and access count
                    influence = (node_data['charge_intensity'] * 
                               math.log(node_data['access_count'] + 1))
                    anchor_alignment += weight * influence
                    anchor_count += 1
        
        if anchor_count == 0:
            semantic_score = 0.5
        else:
            semantic_score = min(anchor_alignment / anchor_count, 1.0)
        
        # Penalize excessive semantic pressure (chaos)
        avg_pressure = np.mean(list(field_data['pressure_map'].values())) if field_data['pressure_map'] else 0.0
        pressure_penalty = min(avg_pressure * 0.1, 0.3)
        
        return max(0.0, semantic_score - pressure_penalty)
    
    def _calculate_thermal_alignment(self) -> float:
        """Calculate alignment based on thermal regulation state"""
        thermal_profile = pulse.get_thermal_profile()
        
        # Optimal thermal state is moderate heat with low variance
        current_heat = thermal_profile['current_heat']
        heat_capacity = thermal_profile['heat_capacity']
        variance = thermal_profile['variance']
        stability = thermal_profile['stability_index']
        
        # Heat utilization score (not too hot, not too cold)
        heat_ratio = current_heat / heat_capacity
        optimal_heat_range = (0.3, 0.7)
        
        if optimal_heat_range[0] <= heat_ratio <= optimal_heat_range[1]:
            heat_score = 1.0
        else:
            deviation = min(abs(heat_ratio - optimal_heat_range[0]), 
                          abs(heat_ratio - optimal_heat_range[1]))
            heat_score = max(0.0, 1.0 - deviation * 2.0)
        
        # Stability bonus
        stability_bonus = stability * 0.5
        
        # Variance penalty (too much thermal chaos is bad for alignment)
        variance_penalty = min(variance * 0.2, 0.4)
        
        return max(0.0, min(1.0, heat_score + stability_bonus - variance_penalty))
    
    def _calculate_behavioral_alignment(self, context_state: Dict) -> float:
        """Calculate alignment based on recent behavioral patterns"""
        thermal_state = context_state['thermal_state']
        
        # Check if behaviors match stated intentions
        recent_heat_sources = thermal_state.get('sources', {})
        
        # Positive alignment behaviors
        positive_sources = ['curiosity', 'learning', 'helpfulness']
        positive_score = sum(
            source_data.get('last_contribution', 0) * 0.1
            for source_name, source_data in recent_heat_sources.items()
            if any(pos in source_name.lower() for pos in positive_sources)
        )
        
        # Negative alignment behaviors (excessive drift, misalignment)
        negative_sources = ['drift', 'entropy']
        negative_score = sum(
            source_data.get('last_contribution', 0) * 0.15
            for source_name, source_data in recent_heat_sources.items()
            if any(neg in source_name.lower() for neg in negative_sources)
        )
        
        behavioral_score = max(0.0, min(1.0, 0.5 + positive_score - negative_score))
        return behavioral_score
    
    def _calculate_temporal_coherence(self) -> float:
        """Calculate alignment consistency over time"""
        if len(self.alignment_history) < 3:
            return 0.5  # Not enough history
        
        # Check for alignment stability over recent history
        recent_alignments = [align for _, align in list(self.alignment_history)[-10:]]
        
        # Calculate variance in recent alignment scores
        alignment_variance = np.var(recent_alignments)
        
        # Lower variance = higher temporal coherence
        coherence_score = max(0.0, 1.0 - alignment_variance * 2.0)
        
        # Bonus for sustained high alignment
        avg_recent = np.mean(recent_alignments)
        if avg_recent > 0.7:
            coherence_score *= 1.2
        
        return min(1.0, coherence_score)
    
    def _update_alignment_drift(self):
        """Calculate rate of alignment change (drift)"""
        if len(self.alignment_history) < 2:
            self.alignment_drift = 0.0
            return
        
        # Calculate drift as rate of change
        recent_points = list(self.alignment_history)[-5:]  # Last 5 measurements
        
        if len(recent_points) >= 2:
            time_deltas = []
            alignment_deltas = []
            
            for i in range(1, len(recent_points)):
                prev_time, prev_align = recent_points[i-1]
                curr_time, curr_align = recent_points[i]
                
                time_delta = (curr_time - prev_time).total_seconds()
                alignment_delta = curr_align - prev_align
                
                if time_delta > 0:
                    time_deltas.append(time_delta)
                    alignment_deltas.append(alignment_delta)
            
            if time_deltas:
                # Average rate of change
                self.alignment_drift = np.mean([
                    abs(a_delta / t_delta) for a_delta, t_delta 
                    in zip(alignment_deltas, time_deltas)
                ])
            else:
                self.alignment_drift = 0.0
    
    def detect_alignment_anomalies(self) -> List[Dict]:
        """Detect patterns that suggest alignment issues"""
        anomalies = []
        current_time = datetime.utcnow()
        
        # High drift detection
        if self.alignment_drift > self.drift_threshold:
            anomalies.append({
                'type': 'high_drift',
                'severity': min(self.alignment_drift / self.drift_threshold, 2.0),
                'message': f"Alignment drift {self.alignment_drift:.3f} exceeds threshold {self.drift_threshold}",
                'timestamp': current_time
            })
        
        # Low alignment detection
        if self.current_alignment < 0.3:
            anomalies.append({
                'type': 'low_alignment',
                'severity': (0.3 - self.current_alignment) * 3.33,  # Scale to [0,1]
                'message': f"Current alignment {self.current_alignment:.3f} critically low",
                'timestamp': current_time
            })
        
        # Oscillation detection (rapid back-and-forth changes)
        if len(self.alignment_history) >= 5:
            recent_values = [align for _, align in list(self.alignment_history)[-5:]]
            oscillation_score = self._detect_oscillation_pattern(recent_values)
            
            if oscillation_score > 0.5:
                anomalies.append({
                    'type': 'alignment_oscillation',
                    'severity': oscillation_score,
                    'message': f"Alignment oscillation detected (score: {oscillation_score:.3f})",
                    'timestamp': current_time
                })
        
        return anomalies
    
    def _detect_oscillation_pattern(self, values: List[float]) -> float:
        """Detect oscillating pattern in alignment values"""
        if len(values) < 4:
            return 0.0
        
        # Count direction changes
        direction_changes = 0
        for i in range(2, len(values)):
            prev_trend = values[i-1] - values[i-2]
            curr_trend = values[i] - values[i-1]
            
            # Sign change indicates direction change
            if prev_trend * curr_trend < 0:
                direction_changes += 1
        
        # Normalize by possible changes
        max_changes = len(values) - 2
        oscillation_score = direction_changes / max_changes if max_changes > 0 else 0.0
        
        return oscillation_score
    
    def apply_alignment_correction(self, target_direction: Optional[np.ndarray] = None) -> float:
        """Apply corrective measures to improve alignment"""
        if not target_direction:
            # Use primary alignment vector or default direction
            if self.primary_vector:
                target_direction = self.primary_vector.direction
            else:
                # Default toward identity anchors
                target_direction = self._calculate_identity_direction()
        
        # Calculate correction needed
        correction_magnitude = max(0.0, self.target_alignment - self.current_alignment)
        
        if correction_magnitude < 0.1:
            return 0.0  # No significant correction needed
        
        # Apply correction through semantic field adjustment
        correction_applied = self._apply_semantic_correction(target_direction, correction_magnitude)
        
        # Add thermal adjustment for alignment
        add_heat("alignment_correction", correction_applied * 0.5, 
                f"correcting alignment by {correction_applied:.3f}")
        
        # Record correction
        self.correction_history.append({
            'timestamp': datetime.utcnow(),
            'magnitude': correction_applied,
            'direction': target_direction,
            'pre_correction_alignment': self.current_alignment
        })
        
        print(f"[AlignmentProbe] 🔧 Applied alignment correction: {correction_applied:.3f}")
        
        return correction_applied
    
    def _calculate_identity_direction(self) -> np.ndarray:
        """Calculate direction vector toward core identity"""
        # Find semantic nodes related to identity anchors
        field_data = SemanticField.get_field_visualization_data()
        nodes = field_data['nodes']
        
        identity_positions = []
        
        for node_id, node_data in nodes.items():
            content = node_data['content'].lower()
            
            for anchor in self.identity_anchors:
                if anchor in content:
                    # Weight position by anchor importance
                    weight = self.identity_anchors[anchor]
                    position = np.array(node_data['position'])
                    identity_positions.append(position * weight)
        
        if not identity_positions:
            # Default direction if no identity nodes found
            return np.array([0.0, 0.0, 1.0])  # Upward/positive direction
        
        # Average weighted positions to get identity direction
        avg_position = np.mean(identity_positions, axis=0)
        
        # Normalize to unit vector
        if np.linalg.norm(avg_position) > 0:
            return avg_position / np.linalg.norm(avg_position)
        else:
            return np.array([0.0, 0.0, 1.0])
    
    def _apply_semantic_correction(self, direction: np.ndarray, magnitude: float) -> float:
        """Apply alignment correction through semantic field manipulation"""
        # This would influence node charges and connections toward alignment
        # For now, we'll simulate the effect
        
        correction_strength = min(magnitude * self.correction_strength, 0.2)
        
        # In a full implementation, this would:
        # 1. Identify misaligned semantic nodes
        # 2. Adjust their charges toward alignment
        # 3. Strengthen connections that support alignment
        # 4. Weaken connections that oppose alignment
        
        return correction_strength
    
    def get_alignment_status(self) -> Dict:
        """Get comprehensive alignment status"""
        anomalies = self.detect_alignment_anomalies()
        
        return {
            'current_alignment': self.current_alignment,
            'target_alignment': self.target_alignment,
            'alignment_drift': self.alignment_drift,
            'alignment_trend': self._calculate_alignment_trend(),
            'anomalies': anomalies,
            'identity_anchors': self.identity_anchors,
            'correction_history_length': len(self.correction_history),
            'stability_rating': self._calculate_stability_rating(),
            'last_update': datetime.utcnow().isoformat()
        }
    
    def _calculate_alignment_trend(self) -> str:
        """Calculate whether alignment is improving, degrading, or stable"""
        if len(self.alignment_history) < 3:
            return "insufficient_data"
        
        recent_values = [align for _, align in list(self.alignment_history)[-5:]]
        
        # Simple trend analysis
        if len(recent_values) >= 3:
            early_avg = np.mean(recent_values[:len(recent_values)//2])
            late_avg = np.mean(recent_values[len(recent_values)//2:])
            
            if late_avg > early_avg + 0.05:
                return "improving"
            elif late_avg < early_avg - 0.05:
                return "degrading"
            else:
                return "stable"
        
        return "stable"
    
    def _calculate_stability_rating(self) -> str:
        """Calculate overall alignment stability rating"""
        if len(self.alignment_history) < 5:
            return "unknown"
        
        recent_alignments = [align for _, align in list(self.alignment_history)[-10:]]
        variance = np.var(recent_alignments)
        avg_alignment = np.mean(recent_alignments)
        
        if variance < 0.01 and avg_alignment > 0.7:
            return "excellent"
        elif variance < 0.02 and avg_alignment > 0.5:
            return "good"
        elif variance < 0.05 and avg_alignment > 0.3:
            return "fair"
        else:
            return "poor"

# Global alignment probe instance
AlignmentMonitor = AlignmentProbe()
current_alignment_probe = AlignmentProbe()

# Convenience functions
def get_current_alignment(context_state: Optional[Dict] = None) -> float:
    """Get current alignment score - fixes phantom reference error"""
    return AlignmentMonitor.calculate_current_alignment(context_state)

def check_alignment_anomalies() -> List[Dict]:
    """Check for alignment anomalies"""
    return AlignmentMonitor.detect_alignment_anomalies()

def apply_alignment_correction(target_direction: Optional[np.ndarray] = None) -> float:
    """Apply alignment correction"""
    return AlignmentMonitor.apply_alignment_correction(target_direction)

def get_alignment_status() -> Dict:
    """Get comprehensive alignment status"""
    return AlignmentMonitor.get_alignment_status()
