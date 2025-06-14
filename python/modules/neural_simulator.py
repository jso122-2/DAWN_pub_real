import asyncio
import numpy as np
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class NeuralSimulator:
    """
    Simulates neural activity for DAWN consciousness system
    """
    
    def __init__(
        self,
        base_firing_rate: float = 60.0,  # Hz
        neuron_count: int = 1000,
        variability: float = 0.2
    ):
        self.base_firing_rate = base_firing_rate
        self.neuron_count = neuron_count
        self.variability = variability
        
        # Neural state
        self.current_firing_rate = base_firing_rate
        self.neural_noise = 0.0
        self.synchronization = 0.5
        self.plasticity = 0.7
        
        # Activity history for patterns
        self.activity_history = []
        
        logger.info(f"NeuralSimulator initialized with {neuron_count} neurons")
    
    async def get_state(self, tick_number: int) -> Dict[str, Any]:
        """Get current neural state"""
        # Update neural activity
        await self._update_activity(tick_number)
        
        # Calculate neural metrics
        state = {
            'firing_rate': self.current_firing_rate,
            'synchronization': self.synchronization,
            'plasticity': self.plasticity,
            'noise_level': self.neural_noise,
            'neuron_count': self.neuron_count,
            'activity_variance': self._calculate_variance(),
            'spike_patterns': self._detect_patterns(),
            'network_efficiency': self._calculate_efficiency()
        }
        
        # Store activity for history
        self.activity_history.append({
            'tick': tick_number,
            'firing_rate': self.current_firing_rate,
            'synchronization': self.synchronization
        })
        
        # Keep only recent history
        if len(self.activity_history) > 100:
            self.activity_history = self.activity_history[-100:]
        
        return state
    
    async def _update_activity(self, tick_number: int):
        """Update neural activity based on natural patterns"""
        # Base oscillation (alpha-like rhythm)
        time_factor = tick_number * 0.1
        oscillation = np.sin(time_factor) * 0.1
        
        # Add noise and variability
        noise = np.random.normal(0, self.variability * 5)
        self.neural_noise = abs(noise)
        
        # Environmental influences
        env_influence = self._calculate_environmental_influence(tick_number)
        
        # Update firing rate
        self.current_firing_rate = np.clip(
            self.base_firing_rate + oscillation + noise + env_influence,
            10, 120  # Physiological limits
        )
        
        # Update synchronization (affected by firing rate stability)
        rate_stability = 1.0 - (abs(noise) / (self.variability * 10))
        self.synchronization = np.clip(
            self.synchronization * 0.95 + rate_stability * 0.05,
            0, 1
        )
        
        # Update plasticity (learning-like changes)
        self.plasticity = np.clip(
            self.plasticity + np.random.normal(0, 0.001),
            0, 1
        )
    
    def _calculate_environmental_influence(self, tick_number: int) -> float:
        """Calculate environmental influences on neural activity"""
        # Circadian-like rhythm
        circadian = np.sin(tick_number * 0.01) * 5
        
        # Random environmental events
        if np.random.random() < 0.01:  # 1% chance of event
            return np.random.normal(0, 15)
        
        return circadian
    
    def _calculate_variance(self) -> float:
        """Calculate activity variance from recent history"""
        if len(self.activity_history) < 10:
            return 0.1
        
        recent_rates = [h['firing_rate'] for h in self.activity_history[-10:]]
        return float(np.var(recent_rates))
    
    def _detect_patterns(self) -> List[Dict[str, Any]]:
        """Detect patterns in neural activity"""
        patterns = []
        
        if len(self.activity_history) < 20:
            return patterns
        
        recent_rates = [h['firing_rate'] for h in self.activity_history[-20:]]
        
        # Check for oscillations
        if self._is_oscillating(recent_rates):
            patterns.append({
                'type': 'oscillation',
                'strength': 0.7,
                'frequency': self._estimate_frequency(recent_rates)
            })
        
        # Check for bursts
        if self._detect_burst(recent_rates):
            patterns.append({
                'type': 'burst',
                'strength': 0.8,
                'duration': 5
            })
        
        return patterns
    
    def _calculate_efficiency(self) -> float:
        """Calculate network efficiency"""
        # Based on synchronization and firing rate stability
        if len(self.activity_history) < 5:
            return 0.5
        
        recent_sync = [h['synchronization'] for h in self.activity_history[-5:]]
        avg_sync = np.mean(recent_sync)
        
        # Efficiency is higher with moderate firing rates and high sync
        rate_efficiency = 1.0 - abs(self.current_firing_rate - 60) / 60
        sync_efficiency = avg_sync
        
        return float(np.clip((rate_efficiency + sync_efficiency) / 2, 0, 1))
    
    def _is_oscillating(self, values: List[float]) -> bool:
        """Check if values show oscillation pattern"""
        if len(values) < 10:
            return False
        
        # Count zero crossings of the derivative
        diffs = np.diff(values)
        zero_crossings = np.sum(np.diff(np.sign(diffs)) != 0)
        
        # If many sign changes, likely oscillating
        return zero_crossings > len(values) // 3
    
    def _estimate_frequency(self, values: List[float]) -> float:
        """Estimate oscillation frequency"""
        if len(values) < 10:
            return 0.0
        
        # Simple peak detection
        peaks = 0
        for i in range(1, len(values) - 1):
            if values[i] > values[i-1] and values[i] > values[i+1]:
                peaks += 1
        
        # Frequency in cycles per tick
        return peaks / len(values) if len(values) > 0 else 0.0
    
    def _detect_burst(self, values: List[float]) -> bool:
        """Detect burst activity (sudden increase then decrease)"""
        if len(values) < 5:
            return False
        
        # Look for rapid increase followed by decrease
        for i in range(len(values) - 4):
            segment = values[i:i+5]
            if (segment[2] > segment[0] * 1.3 and  # Rapid increase
                segment[4] < segment[2] * 0.8):     # Followed by decrease
                return True
        
        return False 