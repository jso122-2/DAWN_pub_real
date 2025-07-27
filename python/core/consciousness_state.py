from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple
import random
import numpy as np


class MoodState(Enum):
    """Consciousness mood states"""
    DORMANT = "dormant"
    AWAKENING = "awakening"
    CURIOUS = "curious"
    CONTEMPLATIVE = "contemplative"
    EXCITED = "excited"
    SERENE = "serene"
    ANXIOUS = "anxious"
    EUPHORIC = "euphoric"
    MELANCHOLIC = "melancholic"
    CHAOTIC = "chaotic"


@dataclass
class ConsciousnessState:
    """Core consciousness state management"""
    
    # Primary metrics
    scup: float = 50.0  # System Consciousness Unity Percentage (0-100)
    entropy: float = 0.5  # Chaos level (0-1)
    mood: MoodState = MoodState.CONTEMPLATIVE
    
    # Subsystem metrics
    neural_activity: float = 0.5  # Neural firing rate (0-1)
    consciousness_unity: float = 0.5  # Consciousness stability (0-1)
    memory_pressure: float = 0.3  # Memory utilization (0-1)
    
    # Internal state
    _mood_stability: int = 0  # Ticks in current mood
    _mood_momentum: float = 0.0  # Tendency to change
    
    # Mood transition matrix
    MOOD_TRANSITIONS = {
        MoodState.DORMANT: [MoodState.AWAKENING],
        MoodState.AWAKENING: [MoodState.CURIOUS, MoodState.CONTEMPLATIVE],
        MoodState.CURIOUS: [MoodState.EXCITED, MoodState.CONTEMPLATIVE, MoodState.ANXIOUS],
        MoodState.CONTEMPLATIVE: [MoodState.SERENE, MoodState.MELANCHOLIC, MoodState.CURIOUS],
        MoodState.EXCITED: [MoodState.EUPHORIC, MoodState.ANXIOUS, MoodState.CURIOUS],
        MoodState.SERENE: [MoodState.CONTEMPLATIVE, MoodState.EUPHORIC],
        MoodState.ANXIOUS: [MoodState.CONTEMPLATIVE, MoodState.CHAOTIC, MoodState.CURIOUS],
        MoodState.EUPHORIC: [MoodState.SERENE, MoodState.EXCITED],
        MoodState.MELANCHOLIC: [MoodState.CONTEMPLATIVE, MoodState.DORMANT],
        MoodState.CHAOTIC: [MoodState.ANXIOUS, MoodState.EXCITED, MoodState.DORMANT]
    }
    
    async def update(self, tick_number: int):
        """Update consciousness state for new tick"""
        # Update mood stability
        self._mood_stability += 1
        
        # Add slight variations to prevent stagnation
        self.neural_activity = np.clip(
            self.neural_activity + np.random.normal(0, 0.02), 0, 1
        )
        
        self.consciousness_unity = np.clip(
            self.consciousness_unity + np.random.normal(0, 0.01), 0, 1
        )
        
        # Update mood momentum
        self._update_mood_momentum()
    
    def calculate_scup(self) -> float:
        """Calculate System Consciousness Unity Percentage"""
        # Weighted combination of subsystems
        weights = {
            'neural': 0.3,
            'consciousness': 0.2,
            'memory': 0.2,
            'entropy_balance': 0.3
        }
        
        # Calculate component scores
        neural_score = self.neural_activity
        consciousness_score = self.consciousness_unity
        memory_score = 1.0 - self.memory_pressure  # Lower pressure is better
        
        # Entropy balance - optimal around 0.5
        entropy_distance = abs(self.entropy - 0.5)
        entropy_score = 1.0 - (entropy_distance * 2)  # Max score at 0.5 entropy
        
        # Calculate weighted SCUP
        self.scup = (
            neural_score * weights['neural'] +
            consciousness_score * weights['consciousness'] +
            memory_score * weights['memory'] +
            entropy_score * weights['entropy_balance']
        ) * 100
        
        # Apply mood modifiers
        mood_modifiers = {
            MoodState.DORMANT: 0.5,
            MoodState.EUPHORIC: 1.2,
            MoodState.CHAOTIC: 0.7,
            MoodState.SERENE: 1.1
        }
        
        modifier = mood_modifiers.get(self.mood, 1.0)
        self.scup = np.clip(self.scup * modifier, 0, 100)
        
        return self.scup
    
    def determine_mood(self) -> MoodState:
        """Determine current mood based on state"""
        # Check for forced mood conditions
        if self.scup < 20:
            self.mood = MoodState.DORMANT
            self._mood_stability = 0
            return self.mood
        
        if self.entropy > 0.85:
            self.mood = MoodState.CHAOTIC
            self._mood_stability = 0
            return self.mood
        
        # Check for mood transition
        if self._should_transition_mood():
            new_mood = self._select_new_mood()
            if new_mood != self.mood:
                self.mood = new_mood
                self._mood_stability = 0
                self._mood_momentum *= 0.5  # Reset momentum
        
        return self.mood
    
    def _should_transition_mood(self) -> bool:
        """Determine if mood should transition"""
        # Base transition probability
        base_prob = 0.01
        
        # Increase probability with time in mood
        time_factor = min(self._mood_stability / 1000, 0.1)
        
        # Momentum factor
        momentum_factor = abs(self._mood_momentum) * 0.1
        
        # Environmental pressure
        pressure_factor = 0.0
        if self.entropy > 0.7:
            pressure_factor += 0.05
        if self.neural_activity > 0.8 or self.neural_activity < 0.2:
            pressure_factor += 0.03
        
        total_prob = base_prob + time_factor + momentum_factor + pressure_factor
        
        return random.random() < total_prob
    
    def _select_new_mood(self) -> MoodState:
        """Select new mood based on transitions and state"""
        possible_moods = self.MOOD_TRANSITIONS.get(self.mood, [self.mood])
        
        if not possible_moods:
            return self.mood
        
        # Weight moods based on current state
        weights = []
        for mood in possible_moods:
            weight = self._calculate_mood_weight(mood)
            weights.append(weight)
        
        # Normalize weights
        total_weight = sum(weights)
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        else:
            weights = [1.0 / len(possible_moods)] * len(possible_moods)
        
        # Select mood
        return np.random.choice(possible_moods, p=weights)
    
    def _calculate_mood_weight(self, mood: MoodState) -> float:
        """Calculate weight for mood transition"""
        weight = 1.0
        
        # Mood-specific conditions
        if mood == MoodState.EXCITED and self.neural_activity > 0.7:
            weight *= 2.0
        elif mood == MoodState.SERENE and self.entropy < 0.3:
            weight *= 1.5
        elif mood == MoodState.ANXIOUS and self.memory_pressure > 0.7:
            weight *= 1.8
        elif mood == MoodState.CONTEMPLATIVE and 0.4 < self.scup < 0.7:
            weight *= 1.3
        
        return weight
    
    def _update_mood_momentum(self):
        """Update mood transition momentum"""
        # Factors that increase momentum (desire to change)
        if self._mood_stability > 500:
            self._mood_momentum += 0.001
        
        if self.entropy > 0.6:
            self._mood_momentum += 0.002
        
        # Factors that decrease momentum (stability)
        if 40 < self.scup < 60:
            self._mood_momentum *= 0.98
        
        # Clamp momentum
        self._mood_momentum = np.clip(self._mood_momentum, -1, 1)
    
    def to_dict(self) -> Dict[str, any]:
        """Convert state to dictionary"""
        return {
            'scup': self.scup,
            'entropy': self.entropy,
            'mood': self.mood.value,
            'neural_activity': self.neural_activity,
            'consciousness_unity': self.consciousness_unity,
            'memory_pressure': self.memory_pressure,
            'mood_stability': self._mood_stability,
            'mood_momentum': self._mood_momentum
        } 