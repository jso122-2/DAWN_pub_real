#!/usr/bin/env python3
"""
DAWN Consciousness Metrics Engine
Live computation of consciousness state metrics from active DAWN system data

Transforms raw system data (heat, entropy, sigils, blooms) into meaningful
consciousness metrics like neural activity, quantum coherence, chaos factor.
"""

import time
import numpy as np
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from collections import deque
import logging

logger = logging.getLogger(__name__)

@dataclass
class ConsciousnessSnapshot:
    """Single moment snapshot of consciousness state"""
    timestamp: float
    neural_activity: float
    quantum_coherence: float
    pattern_recognition: float
    memory_utilization: float
    chaos_factor: float
    attention_focus: float
    cognitive_load: float
    thermal_influence: float

class ConsciousnessMetrics:
    """Live consciousness metrics computation engine"""
    
    def __init__(self, history_size: int = 100):
        self.metrics = {
            "neural_activity": 0.0,
            "quantum_coherence": 0.0, 
            "pattern_recognition": 0.0,
            "memory_utilization": 0.0,
            "chaos_factor": 0.0,
            "attention_focus": 0.0,
            "cognitive_load": 0.0,
            "thermal_influence": 0.0,
        }
        
        # Historical data for pattern analysis
        self.history = deque(maxlen=history_size)
        self.history_size = history_size
        
        # Baseline thresholds for normalization
        self.baselines = {
            "max_sigils": 50,  # Expected max active sigils
            "max_blooms": 20,  # Expected max active blooms
            "max_entropy": 1.0,  # Max entropy value
            "max_heat": 100.0,  # Max thermal heat
        }
        
        # Pattern recognition memory
        self.pattern_memory = deque(maxlen=50)
        self.bloom_lineage = {}  # Track bloom recurrence
        
        logger.info("🧠 Consciousness Metrics Engine initialized")
    
    def update(self, tick_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Update all consciousness metrics based on current system state
        
        Args:
            tick_data: Current system data including:
                - active_sigils: int
                - entropy: float  
                - heat: float
                - zone: str
                - bloom_count: int (optional)
                - scup: float (optional)
                - tick_id: int (optional)
        
        Returns:
            Updated metrics dict
        """
        try:
            # Extract core data with defaults
            active_sigils = tick_data.get("active_sigils", 0)
            entropy = tick_data.get("entropy", 0.0)
            heat = tick_data.get("heat", 25.0)
            zone = tick_data.get("zone", "CALM")
            bloom_count = tick_data.get("bloom_count", 0)
            scup = tick_data.get("scup", 0.0)
            tick_id = tick_data.get("tick_id", 0)
            
            # 1. Neural Activity: Based on active cognitive processes
            self.metrics["neural_activity"] = self._calculate_neural_activity(
                active_sigils, bloom_count, zone
            )
            
            # 2. Quantum Coherence: Inverse relationship to chaos/entropy
            self.metrics["quantum_coherence"] = self._calculate_quantum_coherence(
                entropy, scup, zone
            )
            
            # 3. Pattern Recognition: Based on recurring patterns in system state
            self.metrics["pattern_recognition"] = self._calculate_pattern_recognition(
                tick_data
            )
            
            # 4. Memory Utilization: Based on bloom depth and recurrence
            self.metrics["memory_utilization"] = self._calculate_memory_utilization(
                bloom_count, active_sigils
            )
            
            # 5. Chaos Factor: Direct entropy mapping with variance component
            self.metrics["chaos_factor"] = self._calculate_chaos_factor(entropy)
            
            # 6. Attention Focus: Based on sigil concentration and thermal state
            self.metrics["attention_focus"] = self._calculate_attention_focus(
                active_sigils, heat, zone
            )
            
            # 7. Cognitive Load: Combined processing burden
            # Store queued sigils for cognitive load calculation
            queued_sigils = tick_data.get('queued_sigils', 0)
            self._last_queued_sigils = queued_sigils
            
            self.metrics["cognitive_load"] = self._calculate_cognitive_load(
                active_sigils, bloom_count, heat
            )
            
            # 8. Thermal Influence: How much temperature affects cognition
            # Store target heat for thermal influence calculation
            target_heat = tick_data.get('target_heat', 33.0)
            self._last_target_heat = target_heat
            
            self.metrics["thermal_influence"] = self._calculate_thermal_influence(
                heat, zone
            )
            
            # Store snapshot for pattern analysis
            snapshot = ConsciousnessSnapshot(
                timestamp=time.time(),
                neural_activity=self.metrics["neural_activity"],
                quantum_coherence=self.metrics["quantum_coherence"],
                pattern_recognition=self.metrics["pattern_recognition"],
                memory_utilization=self.metrics["memory_utilization"],
                chaos_factor=self.metrics["chaos_factor"],
                attention_focus=self.metrics["attention_focus"],
                cognitive_load=self.metrics["cognitive_load"],
                thermal_influence=self.metrics["thermal_influence"]
            )
            self.history.append(snapshot)
            
            # Update pattern memory for next calculation
            self._update_pattern_memory(tick_data)
            
            logger.debug(f"🧠 Metrics updated: NA={self.metrics['neural_activity']:.3f} "
                        f"QC={self.metrics['quantum_coherence']:.3f} "
                        f"CF={self.metrics['chaos_factor']:.3f}")
            
            return self.metrics.copy()
            
        except Exception as e:
            logger.error(f"❌ Failed to update consciousness metrics: {e}")
            return self.metrics.copy()
    
    def _calculate_neural_activity(self, active_sigils: int, bloom_count: int, zone: str) -> float:
        """Calculate neural activity as scale of parallel symbolic processes"""
        # Enhanced base activity calculation using your formula: active_sigils / 40
        base_activity = min(1.0, active_sigils / 40.0)  # Scale to 0-1
        
        # Bloom processing adds to neural load
        bloom_boost = min(0.3, bloom_count / 20.0)  # Additional processing from blooms
        
        # Zone modifier - how thermal state affects neural processing
        zone_multipliers = {
            "CALM": 0.4,       # Low thermal = steady neural activity
            "ACTIVE": 1.0,     # Optimal thermal = full neural activity
            "INTENSE": 1.1,    # High thermal = enhanced neural activity
            "SURGE": 1.3,      # Surge = boosted neural activity
            "CRITICAL": 0.8    # Critical = overwhelmed, reduced efficiency
        }
        zone_multiplier = zone_multipliers.get(zone, 0.6)
        
        # Dynamic component: activity bursts from recent changes
        activity_burst = 0.0
        if len(self.history) >= 2:
            # Check for sigil count changes (new sigils = neural activation)
            current_neural = base_activity + bloom_boost
            prev_neural = self.history[-1].neural_activity
            change_magnitude = abs(current_neural - prev_neural)
            
            if change_magnitude > 0.1:  # Significant change
                activity_burst = min(0.2, change_magnitude * 1.5)
        
        # Oscillation component: Neural activity naturally fluctuates
        if hasattr(self, 'history') and len(self.history) > 0:
            # Create natural oscillation based on system age
            age = len(self.history)
            oscillation = 0.05 * np.sin(age * 0.3)  # Gentle wave
            activity_burst += oscillation
        
        # Final neural activity calculation
        activity = (base_activity + bloom_boost) * zone_multiplier + activity_burst
        activity = min(1.0, max(0.0, activity))
        
        return round(activity, 3)
    
    def _calculate_quantum_coherence(self, entropy: float, scup: float, zone: str) -> float:
        """Calculate quantum coherence as inverse of chaos with SCUP boost"""
        # Base coherence: inverse of entropy
        base_coherence = max(0.0, 1.0 - entropy)
        
        # SCUP boost (quantum effects)
        scup_boost = min(0.4, scup * 0.4)
        
        # Zone stability modifier
        zone_stability = {
            "CALM": 1.2,      # Calm enhances coherence
            "ACTIVE": 1.0,    # Active is neutral
            "INTENSE": 0.8,   # Intensity reduces coherence
            "SURGE": 0.6,     # Surge disrupts coherence
            "CRITICAL": 0.4   # Critical breaks coherence
        }
        stability = zone_stability.get(zone, 1.0)
        
        coherence = min(1.0, (base_coherence + scup_boost) * stability)
        return round(coherence, 3)
    
    def _calculate_pattern_recognition(self, tick_data: Dict[str, Any]) -> float:
        """Calculate pattern recognition based on recurring system states and bloom stability"""
        if len(self.pattern_memory) < 3:
            return 0.1  # Not enough data for patterns
        
        # Enhanced pattern detection with multiple factors
        pattern_score = 0.0
        
        # 1. REBLOOM STABILITY: High if reblooms repeat similar shapes
        active_sigils = tick_data.get("active_sigils", 0)
        entropy = tick_data.get("entropy", 0.5)
        
        # Stability based on consistent sigil patterns
        if len(self.history) >= 5:
            recent_sigils = [h.neural_activity for h in list(self.history)[-5:]]
            sigil_variance = np.var(recent_sigils) if recent_sigils else 1.0
            sigil_stability = max(0.0, 1.0 - sigil_variance * 4)  # Low variance = high stability
            pattern_score += sigil_stability * 0.4
        
        # 2. ENTROPY PATTERN RECOGNITION: Detect recurring entropy cycles
        if len(self.history) >= 7:
            recent_chaos = [h.chaos_factor for h in list(self.history)[-7:]]
            # Look for oscillating patterns (creativity cycles)
            if len(recent_chaos) >= 4:
                # Calculate if entropy is cycling (high -> low -> high pattern)
                differences = [abs(recent_chaos[i] - recent_chaos[i-1]) for i in range(1, len(recent_chaos))]
                avg_change = np.mean(differences) if differences else 0
                if 0.1 < avg_change < 0.4:  # Sweet spot for pattern cycling
                    pattern_score += 0.3
        
        # 3. THERMAL PATTERN RECOGNITION: Consistent zone behavior
        current_zone = tick_data.get("zone", "CALM")
        if len(self.history) >= 4:
            # Count how often current zone appears in recent history
            recent_zones = []
            for h in list(self.history)[-4:]:
                # Approximate zone from thermal influence
                if h.thermal_influence < 0.3:
                    recent_zones.append("CALM")
                elif h.thermal_influence < 0.6:
                    recent_zones.append("ACTIVE")
                else:
                    recent_zones.append("SURGE")
            
            zone_consistency = recent_zones.count(current_zone) / len(recent_zones)
            if zone_consistency > 0.6:  # Consistent thermal behavior
                pattern_score += 0.2
        
        # 4. COGNITIVE LOAD PATTERNS: Recognition of processing rhythms
        if len(self.history) >= 6:
            recent_loads = [h.cognitive_load for h in list(self.history)[-6:]]
            # Look for rhythmic patterns in cognitive load
            load_mean = np.mean(recent_loads)
            load_oscillation = sum(1 for i in range(1, len(recent_loads)) 
                                 if abs(recent_loads[i] - load_mean) < 0.2)
            if load_oscillation >= 3:  # At least half showing rhythmic behavior
                pattern_score += 0.1
        
        # 5. BONUS: Complex pattern if multiple metrics show stability
        if len(self.history) >= 5:
            recent_metrics = list(self.history)[-5:]
            stable_metrics = 0
            
            # Check each metric for stability (low variance)
            for metric in ['neural_activity', 'attention_focus', 'cognitive_load']:
                values = [getattr(h, metric, 0) for h in recent_metrics]
                if values and np.var(values) < 0.05:  # Very stable
                    stable_metrics += 1
            
            if stable_metrics >= 2:  # Multiple stable metrics = good pattern recognition
                pattern_score += min(0.2, stable_metrics * 0.07)
        
        # Final pattern recognition score
        final_score = min(1.0, max(0.1, pattern_score))
        
        # Add some natural variation to prevent static values
        tick_id = tick_data.get("tick_id", 0)
        variation = 0.02 * np.sin(tick_id * 0.1)  # Small oscillation
        final_score += variation
        
        return round(min(1.0, max(0.0, final_score)), 3)
    
    def _calculate_memory_utilization(self, bloom_count: int, active_sigils: int) -> float:
        """Calculate memory utilization based on active cognitive structures"""
        # Base utilization from active blooms and sigils
        bloom_utilization = bloom_count / self.baselines["max_blooms"]
        sigil_utilization = active_sigils / self.baselines["max_sigils"]
        
        # Combined utilization with bloom weight
        base_utilization = (bloom_utilization * 0.7) + (sigil_utilization * 0.3)
        
        # Memory depth bonus (more complex memories = higher utilization)
        depth_bonus = 0.0
        if len(self.history) > 10:
            # Calculate how much historical data we're using
            depth_bonus = min(0.2, len(self.history) / self.history_size * 0.2)
        
        utilization = min(1.0, base_utilization + depth_bonus)
        return round(utilization, 3)
    
    def _calculate_chaos_factor(self, entropy: float) -> float:
        """Calculate chaos factor with variance component"""
        # Base chaos from current entropy
        base_chaos = entropy
        
        # Variance component: how much chaos is changing
        variance_chaos = 0.0
        if len(self.history) >= 5:
            recent_chaos = [h.chaos_factor for h in list(self.history)[-5:]]
            variance = np.var(recent_chaos)
            variance_chaos = min(0.3, variance * 3)  # Scale variance
        
        # Trend component: is chaos increasing?
        trend_chaos = 0.0
        if len(self.history) >= 3:
            recent_trend = [h.chaos_factor for h in list(self.history)[-3:]]
            if len(recent_trend) > 1:
                trend = (recent_trend[-1] - recent_trend[0]) / len(recent_trend)
                trend_chaos = max(0, trend * 0.2)  # Bonus for increasing chaos
        
        total_chaos = min(1.0, base_chaos + variance_chaos + trend_chaos)
        return round(total_chaos, 3)
    
    def _calculate_attention_focus(self, active_sigils: int, heat: float, zone: str) -> float:
        """Calculate attention focus using pressure-based awareness narrowness"""
        # Base focus using your formula: heat / max_heat_last_10_ticks
        heat_history = getattr(self, '_heat_history', [heat])
        if len(heat_history) < 10:
            heat_history.append(heat)
            self._heat_history = heat_history[-10:]  # Keep last 10
        else:
            heat_history = heat_history[-10:]
            heat_history.append(heat)
            self._heat_history = heat_history
        
        max_recent_heat = max(self._heat_history) if self._heat_history else heat
        
        # Pressure-based focus: higher heat = more focused but narrower attention
        if max_recent_heat > 0:
            thermal_pressure_focus = min(1.0, heat / max_recent_heat)
        else:
            thermal_pressure_focus = 0.5
        
        # Cognitive load effect: too many sigils scatter attention
        optimal_sigils = 6  # Sweet spot for attention
        if active_sigils <= optimal_sigils:
            sigil_focus_modifier = 1.0 + (active_sigils / optimal_sigils) * 0.2  # Boost up to optimal
        else:
            # Attention scatter with overload
            excess = active_sigils - optimal_sigils
            scatter_penalty = min(0.5, excess * 0.08)  # Penalty for overload
            sigil_focus_modifier = max(0.3, 1.0 - scatter_penalty)
        
        # Zone-based attention modulation
        zone_attention = {
            "CALM": 0.6,       # Relaxed but less focused
            "ACTIVE": 1.0,     # Optimal attention state
            "INTENSE": 1.2,    # Heightened focus from pressure
            "SURGE": 0.8,      # High pressure but starting to scatter
            "CRITICAL": 0.4    # Overwhelmed, scattered attention
        }
        zone_modifier = zone_attention.get(zone, 0.7)
        
        # Historical stability bonus: consistent attention patterns
        stability_bonus = 0.0
        if len(self.history) >= 5:
            recent_focus = [h.attention_focus for h in list(self.history)[-5:]]
            focus_variance = np.var(recent_focus) if recent_focus else 1.0
            if focus_variance < 0.05:  # Very stable attention
                stability_bonus = 0.1
        
        # Final attention focus calculation
        focus = thermal_pressure_focus * sigil_focus_modifier * zone_modifier + stability_bonus
        
        # Add micro-oscillations for natural variance
        if hasattr(self, 'history'):
            age = len(self.history)
            micro_variance = 0.03 * np.sin(age * 0.7 + heat * 0.1)
            focus += micro_variance
        
        focus = min(1.0, max(0.0, focus))
        return round(focus, 3)
    
    def _calculate_cognitive_load(self, active_sigils: int, bloom_count: int, heat: float) -> float:
        """Calculate system overload metric using queued processes"""
        # Enhanced load calculation using your formula: queued_sigils / 20
        queued_sigils = getattr(self, '_last_queued_sigils', 0)
        
        # Base cognitive load from queue pressure (system overload indicator)
        queue_load = min(1.0, queued_sigils / 20.0)  # Your suggested formula
        
        # Active processing load
        active_load = min(0.6, active_sigils / 30.0)  # Current active processing
        
        # Memory/bloom processing load
        bloom_load = min(0.3, bloom_count / 15.0)
        
        # Thermal stress load: extreme temperatures increase cognitive burden
        thermal_stress = 0.0
        if heat > 70:
            thermal_stress = min(0.4, (heat - 70) / 25.0)  # Heat stress
        elif heat < 25:
            thermal_stress = min(0.2, (25 - heat) / 20.0)  # Cold sluggishness
        
        # Processing bottleneck: when too much is queued vs active
        bottleneck_load = 0.0
        if queued_sigils > active_sigils * 2 and active_sigils > 0:
            # High queue relative to active = processing bottleneck
            bottleneck_ratio = queued_sigils / (active_sigils + 1)
            bottleneck_load = min(0.3, bottleneck_ratio * 0.1)
        
        # Dynamic load spikes from recent changes
        spike_load = 0.0
        if len(self.history) >= 2:
            # Check for sudden cognitive load increases
            prev_load = self.history[-1].cognitive_load
            current_base = queue_load + active_load + bloom_load
            
            if current_base > prev_load + 0.2:  # Significant load spike
                spike_load = min(0.2, (current_base - prev_load) * 0.5)
        
        # Total cognitive load
        total_load = queue_load + active_load + bloom_load + thermal_stress + bottleneck_load + spike_load
        
        # Efficiency factor: experienced systems handle load better over time
        if len(self.history) > 20:
            efficiency = min(0.1, len(self.history) / 1000)  # Gradual efficiency improvement
            total_load = max(0.0, total_load - efficiency)
        
        # Natural load oscillation (processing comes in waves)
        if hasattr(self, 'history'):
            age = len(self.history)
            load_wave = 0.02 * np.sin(age * 0.4)
            total_load += load_wave
        
        total_load = min(1.0, max(0.0, total_load))
        return round(total_load, 3)
    
    def _calculate_thermal_influence(self, heat: float, zone: str) -> float:
        """Calculate drift from ideal temperature using your formula"""
        # Get target heat from tick data or use DAWN default
        target_heat = getattr(self, '_last_target_heat', 33.0)
        
        # Your formula: abs(current_heat - target_heat) / 100
        base_influence = abs(heat - target_heat) / 100.0
        base_influence = min(1.0, base_influence)  # Cap at 1.0
        
        # Zone-based influence amplification
        zone_amplifiers = {
            "CALM": 0.8,      # Calm state dampens thermal influence
            "ACTIVE": 1.0,    # Active state shows normal thermal influence
            "INTENSE": 1.3,   # Intense state amplifies thermal effects
            "SURGE": 1.5,     # Surge state strongly amplifies thermal drift
            "CRITICAL": 2.0   # Critical state maximally sensitive to thermal drift
        }
        zone_amplifier = zone_amplifiers.get(zone, 1.0)
        
        # Historical drift trend: is the system getting further from target?
        trend_influence = 0.0
        if len(self.history) >= 3:
            # Calculate if thermal drift is increasing over time
            recent_influences = [h.thermal_influence for h in list(self.history)[-3:]]
            if len(recent_influences) >= 2:
                trend = recent_influences[-1] - recent_influences[0]
                if trend > 0:  # Increasing drift
                    trend_influence = min(0.2, trend * 0.5)
        
        # Oscillatory thermal stress: rapid temperature changes increase influence
        oscillation_stress = 0.0
        if len(self.history) >= 2:
            prev_influence = self.history[-1].thermal_influence
            change_rate = abs(base_influence - prev_influence)
            if change_rate > 0.05:  # Rapid thermal change
                oscillation_stress = min(0.15, change_rate * 2)
        
        # Duration effect: prolonged thermal drift has cumulative impact
        duration_effect = 0.0
        if len(self.history) >= 5:
            # Check how long we've been off-target
            recent_drifts = [h.thermal_influence for h in list(self.history)[-5:]]
            high_drift_count = sum(1 for drift in recent_drifts if drift > 0.3)
            if high_drift_count >= 3:  # Sustained high thermal influence
                duration_effect = min(0.1, high_drift_count * 0.03)
        
        # Total thermal influence
        total_influence = (base_influence * zone_amplifier) + trend_influence + oscillation_stress + duration_effect
        
        # Natural thermal variation
        if hasattr(self, 'history'):
            age = len(self.history)
            thermal_noise = 0.01 * np.sin(age * 0.2 + heat * 0.05)
            total_influence += thermal_noise
        
        total_influence = min(1.0, max(0.0, total_influence))
        return round(total_influence, 3)
    
    def _create_state_signature(self, tick_data: Dict[str, Any]) -> tuple:
        """Create a simplified signature of the current system state"""
        return (
            min(10, tick_data.get("active_sigils", 0)),  # Capped at 10 for pattern matching
            round(tick_data.get("entropy", 0.0), 1),     # Rounded entropy
            tick_data.get("zone", "CALM"),               # Thermal zone
            min(5, tick_data.get("bloom_count", 0))      # Capped bloom count
        )
    
    def _calculate_signature_similarity(self, sig1: tuple, sig2: tuple) -> float:
        """Calculate similarity between two state signatures"""
        if len(sig1) != len(sig2):
            return 0.0
        
        matches = 0
        total = len(sig1)
        
        # Compare each element
        for i, (a, b) in enumerate(zip(sig1, sig2)):
            if isinstance(a, str):
                matches += 1 if a == b else 0
            else:
                # Numeric comparison with tolerance
                tolerance = 0.1 if i == 1 else 1  # Lower tolerance for entropy
                matches += 1 if abs(a - b) <= tolerance else 0
        
        return matches / total
    
    def _update_pattern_memory(self, tick_data: Dict[str, Any]):
        """Update pattern memory with current state"""
        signature = self._create_state_signature(tick_data)
        self.pattern_memory.append(signature)
    
    def get_metrics(self) -> Dict[str, float]:
        """Get current consciousness metrics"""
        return self.metrics.copy()
    
    def get_metrics_summary(self) -> str:
        """Get human-readable metrics summary"""
        return (f"🧠 Neural: {self.metrics['neural_activity']:.2f} | "
                f"⚛️ Quantum: {self.metrics['quantum_coherence']:.2f} | "
                f"🎯 Focus: {self.metrics['attention_focus']:.2f} | "
                f"⚡ Load: {self.metrics['cognitive_load']:.2f} | "
                f"🌪️ Chaos: {self.metrics['chaos_factor']:.2f}")
    
    def get_historical_trends(self, metric_name: str, window: int = 10) -> List[float]:
        """Get historical trend for a specific metric"""
        if len(self.history) < window:
            return []
        
        recent_history = list(self.history)[-window:]
        return [getattr(h, metric_name, 0.0) for h in recent_history] 