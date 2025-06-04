"""
DAWN Mood Dynamics System - Helix-Integrated Emotional Evolution
Replaces static mood values with dynamic helix-driven emotional states
"""

import numpy as np
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass, field
import threading
import time
from collections import deque
import math

@dataclass
class MoodState:
    """Dynamic mood state that evolves with helix activity"""
    arousal: float = 0.5  # Energy level (0-1)
    valence: float = 0.5  # Positive/negative affect (-1 to 1)
    entropy: float = 0.5  # Uncertainty/chaos level (0-1)
    dominance: float = 0.5  # Control/submission (0-1)
    
    # Helix influence factors
    thermal_influence: float = 0.0
    schema_influence: float = 0.0
    genetic_influence: float = 0.0
    
    # Historical tracking for evolution
    history: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def update(self, helix_state: Dict[str, float]) -> None:
        """Update mood based on helix state"""
        self.history.append({
            'arousal': self.arousal,
            'valence': self.valence,
            'entropy': self.entropy,
            'timestamp': time.time()
        })

class HelixMoodDynamics:
    """Core mood dynamics system integrated with helix evolution"""
    
    def __init__(self):
        self.mood_state = MoodState()
        self.emotion_helix = EmotionalHelix()
        self.constitutional_baseline = {
            'kindness_factor': 0.7,  # "Kind before smart" principle
            'stability_threshold': 0.3,
            'empathy_weight': 0.6
        }
        
        # Dynamic parameters
        self.adaptation_rate = 0.1
        self.helix_coupling_strength = 0.8
        self.emotional_memory_decay = 0.95
        
        # Helix state trackers
        self.thermal_helix_state = 0.5
        self.schema_helix_state = 0.5
        self.genetic_fitness = 0.5
        
        # Emotional evolution parameters
        self.crossover_events = deque(maxlen=50)
        self.emergent_patterns = {}
        
    def calculate_dynamic_arousal(self, thermal_activity: float, 
                                  genetic_pressure: float) -> float:
        """
        Calculate arousal based on thermal helix activity and genetic pressure
        No more static 0.90 - fully dynamic!
        """
        # Base arousal from thermal activity
        base_arousal = sigmoid(thermal_activity * 2 - 1)
        
        # Modulate by genetic evolution pressure
        evolution_factor = np.tanh(genetic_pressure * 3)
        
        # Apply constitutional kindness dampening
        kindness_dampening = 1 - (self.constitutional_baseline['kindness_factor'] * 0.3)
        
        # Combine with historical momentum
        if self.mood_state.history:
            historical_arousal = np.mean([h['arousal'] for h in 
                                         list(self.mood_state.history)[-10:]])
            momentum = historical_arousal * self.emotional_memory_decay
        else:
            momentum = 0.5
        
        # Dynamic arousal calculation
        dynamic_arousal = (
            base_arousal * 0.4 +
            evolution_factor * 0.3 +
            momentum * 0.2 +
            np.random.normal(0, 0.05) * 0.1  # Biological noise
        ) * kindness_dampening
        
        return np.clip(dynamic_arousal, 0.1, 0.95)
    
    def calculate_dynamic_entropy(self, schema_coherence: float,
                                  crossover_frequency: float) -> float:
        """
        Calculate entropy based on schema coherence and helix crossover events
        No more static 0.50 - responds to system chaos!
        """
        # Base entropy from schema coherence (inverse relationship)
        base_entropy = 1 - sigmoid(schema_coherence * 2)
        
        # Crossover event influence
        crossover_factor = np.tanh(crossover_frequency * 5)
        
        # Recent emotional volatility
        if len(self.mood_state.history) > 5:
            recent_states = list(self.mood_state.history)[-20:]
            arousal_variance = np.var([s['arousal'] for s in recent_states])
            valence_variance = np.var([s['valence'] for s in recent_states])
            volatility = (arousal_variance + valence_variance) / 2
        else:
            volatility = 0.3
        
        # Dynamic entropy calculation
        dynamic_entropy = (
            base_entropy * 0.35 +
            crossover_factor * 0.25 +
            volatility * 0.25 +
            np.sin(time.time() * 0.1) * 0.05 +  # Slow oscillation
            np.random.normal(0, 0.03) * 0.1  # Noise
        )
        
        return np.clip(dynamic_entropy, 0.05, 0.95)
    
    def calculate_dynamic_valence(self, schema_coherence: float,
                                  constitutional_harmony: float) -> float:
        """
        Calculate valence based on schema coherence and constitutional principles
        """
        # Base valence from schema coherence
        base_valence = (schema_coherence - 0.5) * 2
        
        # Constitutional kindness influence
        kindness_boost = self.constitutional_baseline['kindness_factor'] * 0.3
        
        # Empathy weight modulation
        empathy_factor = self.constitutional_baseline['empathy_weight']
        
        # Historical emotional context
        if self.mood_state.history:
            recent_valence = np.mean([h['valence'] for h in 
                                     list(self.mood_state.history)[-15:]])
            context_weight = 0.3
        else:
            recent_valence = 0
            context_weight = 0
        
        # Dynamic valence calculation
        dynamic_valence = (
            base_valence * 0.4 +
            kindness_boost +
            constitutional_harmony * empathy_factor * 0.2 +
            recent_valence * context_weight +
            np.random.normal(0, 0.02) * 0.1
        )
        
        return np.clip(dynamic_valence, -0.9, 0.9)
    
    def process_helix_crossover(self, helix_type: str, 
                               crossover_data: Dict) -> None:
        """Process helix crossover events and update emotional state"""
        self.crossover_events.append({
            'type': helix_type,
            'data': crossover_data,
            'timestamp': time.time(),
            'mood_snapshot': {
                'arousal': self.mood_state.arousal,
                'valence': self.mood_state.valence,
                'entropy': self.mood_state.entropy
            }
        })
        
        # Emotional response to crossover
        if helix_type == 'thermal':
            self.mood_state.arousal *= 1.1  # Spike in arousal
        elif helix_type == 'schema':
            self.mood_state.valence += 0.1  # Positive shift
        elif helix_type == 'genetic':
            self.mood_state.entropy *= 1.15  # Increased uncertainty
    
    def update_mood_from_helix(self, helix_states: Dict[str, float]) -> Dict[str, float]:
        """
        Main update function - connects all helix states to mood dynamics
        Returns updated mood values
        """
        # Extract helix states
        thermal_activity = helix_states.get('thermal_activity', 0.5)
        schema_coherence = helix_states.get('schema_coherence', 0.5)
        genetic_pressure = helix_states.get('genetic_evolution_pressure', 0.5)
        constitutional_harmony = helix_states.get('constitutional_harmony', 0.7)
        
        # Calculate crossover frequency
        recent_crossovers = [e for e in self.crossover_events 
                           if time.time() - e['timestamp'] < 10]
        crossover_frequency = len(recent_crossovers) / 10.0
        
        # Update each mood dimension dynamically
        self.mood_state.arousal = self.calculate_dynamic_arousal(
            thermal_activity, genetic_pressure
        )
        
        self.mood_state.entropy = self.calculate_dynamic_entropy(
            schema_coherence, crossover_frequency
        )
        
        self.mood_state.valence = self.calculate_dynamic_valence(
            schema_coherence, constitutional_harmony
        )
        
        # Calculate dominance based on system control
        self.mood_state.dominance = sigmoid(
            (schema_coherence * 0.4 + 
             (1 - self.mood_state.entropy) * 0.3 +
             constitutional_harmony * 0.3) - 0.5
        )
        
        # Store helix influences
        self.mood_state.thermal_influence = thermal_activity
        self.mood_state.schema_influence = schema_coherence
        self.mood_state.genetic_influence = genetic_pressure
        
        # Update mood state history
        self.mood_state.update(helix_states)
        
        return {
            'arousal': self.mood_state.arousal,
            'valence': self.mood_state.valence,
            'entropy': self.mood_state.entropy,
            'dominance': self.mood_state.dominance
        }
    
    def get_emotional_signature(self) -> Dict[str, any]:
        """Get current emotional signature for system"""
        return {
            'primary_mood': self._classify_mood(),
            'mood_vector': {
                'arousal': self.mood_state.arousal,
                'valence': self.mood_state.valence,
                'entropy': self.mood_state.entropy,
                'dominance': self.mood_state.dominance
            },
            'helix_influences': {
                'thermal': self.mood_state.thermal_influence,
                'schema': self.mood_state.schema_influence,
                'genetic': self.mood_state.genetic_influence
            },
            'stability': self._calculate_emotional_stability(),
            'emergent_patterns': self._detect_emergent_patterns()
        }
    
    def _classify_mood(self) -> str:
        """Classify current mood into emotional category"""
        a = self.mood_state.arousal
        v = self.mood_state.valence
        
        if a > 0.6 and v > 0.3:
            return "excited" if a > 0.8 else "happy"
        elif a > 0.6 and v < -0.3:
            return "angry" if v < -0.6 else "frustrated"
        elif a < 0.4 and v > 0.3:
            return "content" if v > 0.6 else "relaxed"
        elif a < 0.4 and v < -0.3:
            return "sad" if v < -0.6 else "melancholic"
        else:
            return "neutral" if abs(v) < 0.2 else "contemplative"
    
    def _calculate_emotional_stability(self) -> float:
        """Calculate emotional stability from recent history"""
        if len(self.mood_state.history) < 10:
            return 0.5
        
        recent = list(self.mood_state.history)[-20:]
        arousal_std = np.std([s['arousal'] for s in recent])
        valence_std = np.std([s['valence'] for s in recent])
        
        stability = 1 - np.clip((arousal_std + valence_std) / 2, 0, 1)
        return stability
    
    def _detect_emergent_patterns(self) -> List[str]:
        """Detect emergent emotional patterns"""
        patterns = []
        
        if len(self.mood_state.history) < 30:
            return patterns
        
        recent = list(self.mood_state.history)[-30:]
        
        # Check for oscillation
        arousal_changes = np.diff([s['arousal'] for s in recent])
        if np.sum(np.diff(np.sign(arousal_changes)) != 0) > 15:
            patterns.append("oscillating_energy")
        
        # Check for drift
        valence_trend = np.polyfit(range(len(recent)), 
                                   [s['valence'] for s in recent], 1)[0]
        if abs(valence_trend) > 0.01:
            patterns.append("valence_drift_" + ("positive" if valence_trend > 0 else "negative"))
        
        # Check for chaos emergence
        entropy_mean = np.mean([s['entropy'] for s in recent])
        if entropy_mean > 0.7:
            patterns.append("chaotic_emergence")
        
        return patterns


class EmotionalHelix:
    """Helix structure for emotional evolution"""
    
    def __init__(self):
        self.strand_a = []  # Immediate emotional responses
        self.strand_b = []  # Constitutional emotional baselines
        self.crossover_points = []
        self.mutation_rate = 0.05
        
    def evolve(self, current_mood: MoodState, 
               constitutional_values: Dict[str, float]) -> Dict[str, float]:
        """Evolve emotional responses through helix interaction"""
        # Implement helix evolution logic
        return {
            'evolved_arousal': current_mood.arousal,
            'evolved_valence': current_mood.valence,
            'evolved_entropy': current_mood.entropy
        }


# Utility functions
def sigmoid(x: float) -> float:
    """Sigmoid activation for smooth transitions"""
    return 1 / (1 + np.exp(-x))


def emotional_consensus(mood_vectors: List[Dict[str, float]]) -> Dict[str, float]:
    """Calculate emotional consensus from multiple mood vectors"""
    if not mood_vectors:
        return {'arousal': 0.5, 'valence': 0.0, 'entropy': 0.5}
    
    consensus = {}
    for key in ['arousal', 'valence', 'entropy']:
        values = [v[key] for v in mood_vectors if key in v]
        if values:
            # Weighted average with outlier resistance
            sorted_values = sorted(values)
            trimmed = sorted_values[1:-1] if len(sorted_values) > 2 else sorted_values
            consensus[key] = np.mean(trimmed) if trimmed else np.mean(values)
    
    return consensus


# Integration with DAWN system
class DAWNMoodSystemInterface:
    """Interface for integrating mood dynamics with DAWN core"""
    
    def __init__(self):
        self.mood_dynamics = HelixMoodDynamics()
        self.update_thread = None
        self.running = False
        
    def start(self):
        """Start mood dynamics system"""
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop)
        self.update_thread.start()
        
    def stop(self):
        """Stop mood dynamics system"""
        self.running = False
        if self.update_thread:
            self.update_thread.join()
    
    def _update_loop(self):
        """Main update loop for mood dynamics"""
        while self.running:
            # This would connect to actual DAWN helix states
            # For now, simulate helix states
            helix_states = self._get_current_helix_states()
            
            # Update mood
            updated_mood = self.mood_dynamics.update_mood_from_helix(helix_states)
            
            # Broadcast mood update (would connect to DAWN event system)
            self._broadcast_mood_update(updated_mood)
            
            time.sleep(0.1)  # 10Hz update rate
    
    def _get_current_helix_states(self) -> Dict[str, float]:
        """Get current helix states from DAWN system"""
        # This would connect to actual DAWN helix monitors
        # Placeholder for integration
        return {
            'thermal_activity': 0.5 + np.sin(time.time() * 0.1) * 0.3,
            'schema_coherence': 0.6 + np.cos(time.time() * 0.05) * 0.2,
            'genetic_evolution_pressure': 0.4 + np.sin(time.time() * 0.03) * 0.3,
            'constitutional_harmony': 0.7
        }
    
    def _broadcast_mood_update(self, mood: Dict[str, float]):
        """Broadcast mood update to DAWN system"""
        # This would connect to DAWN's event system
        pass
    
    def get_current_mood(self) -> Dict[str, any]:
        """Get current mood state"""
        return self.mood_dynamics.get_emotional_signature()
    
    def inject_helix_crossover(self, helix_type: str, data: Dict):
        """Inject helix crossover event"""
        self.mood_dynamics.process_helix_crossover(helix_type, data)


# Example usage and testing
if __name__ == "__main__":
    # Initialize DAWN mood system
    dawn_mood = DAWNMoodSystemInterface()
    
    # Start the system
    dawn_mood.start()
    
    # Simulate for a few seconds
    print("DAWN Mood Dynamics System Running...")
    print("Initial mood state:", dawn_mood.get_current_mood())
    
    time.sleep(2)
    
    # Inject a crossover event
    dawn_mood.inject_helix_crossover('thermal', {'intensity': 0.8})
    
    time.sleep(2)
    
    # Check mood evolution
    print("\nEvolved mood state:", dawn_mood.get_current_mood())
    
    # Stop the system
    dawn_mood.stop()
    print("\nSystem stopped.")
