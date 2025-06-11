"""
DAWN Consciousness State Machine - Refined Transition Logic

Implements sophisticated state transition system with:
- Emotional momentum tracking and inertia calculations
- Smooth probabilistic transitions instead of hard switches
- Emergency transition handling for rapid metric changes
- Time-based state persistence and transition blending
- Comprehensive state history and transition logging
"""

import time
import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from collections import deque, defaultdict
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class StateTransition:
    """Information about a state transition"""
    from_state: str
    to_state: str
    timestamp: datetime
    duration: float  # Transition duration in seconds
    trigger_reason: str
    metrics_snapshot: Dict[str, float]
    transition_probability: float
    momentum_factor: float
    inertia_factor: float
    pattern_influence: float
    is_emergency: bool = False


@dataclass
class TransitionProgress:
    """Current transition progress information"""
    in_transition: bool
    from_state: str
    to_state: str
    progress: float  # 0.0 to 1.0
    start_time: datetime
    expected_duration: float
    blended_properties: Dict[str, float]


@dataclass
class StateMetrics:
    """Metrics for a consciousness state"""
    optimal_scup: float
    optimal_entropy: float
    optimal_heat: float
    stability_factor: float
    energy_level: float
    creativity_factor: float
    introspection_factor: float


class ConsciousnessStateMachine:
    """
    Advanced state machine for DAWN consciousness with smooth transitions
    """
    
    def __init__(self, initial_state: str = "neutral", history_size: int = 100):
        """Initialize consciousness state machine
        
        Args:
            initial_state: Starting emotional state
            history_size: Maximum number of state transitions to track
        """
        # Current state information
        self.current_state = initial_state
        self.state_start_time = datetime.now()
        self.last_transition_time = datetime.now()
        
        # State history tracking (ring buffer)
        self.state_history = deque(maxlen=history_size)
        self.transition_history = deque(maxlen=history_size)
        self.momentum_history = deque(maxlen=10)  # Last 10 transitions for momentum
        
        # Transition management
        self.current_transition: Optional[TransitionProgress] = None
        self.transition_queue = deque(maxlen=5)
        
        # State metrics and properties
        self.state_metrics = {
            "creative": StateMetrics(0.7, 0.8, 0.6, 0.6, 0.8, 1.0, 0.4),
            "contemplative": StateMetrics(0.8, 0.3, 0.2, 0.9, 0.4, 0.3, 1.0),
            "curious": StateMetrics(0.6, 0.5, 0.4, 0.7, 0.6, 0.7, 0.6),
            "calm": StateMetrics(0.8, 0.2, 0.1, 1.0, 0.3, 0.2, 0.8),
            "anxious": StateMetrics(0.4, 0.7, 0.8, 0.3, 0.9, 0.5, 0.3),
            "overwhelmed": StateMetrics(0.3, 0.9, 0.9, 0.2, 1.0, 0.8, 0.1),
            "neutral": StateMetrics(0.5, 0.5, 0.3, 0.8, 0.5, 0.5, 0.5)
        }
        
        # Transition weights and parameters
        self.metric_weight = 0.4
        self.inertia_weight = 0.4
        self.pattern_weight = 0.2
        
        # Emergency transition thresholds
        self.entropy_emergency_threshold = 0.5  # Change >0.5 in <3s
        self.emergency_time_window = 3.0  # seconds
        
        # Inertia parameters
        self.base_inertia = 0.5
        self.prolonged_state_threshold = 600  # 10 minutes in seconds
        self.max_inertia_bonus = 0.4
        
        # Transition timing
        self.min_transition_duration = 2.0  # seconds
        self.max_transition_duration = 5.0  # seconds
        self.default_transition_duration = 3.0  # seconds
        
        # Emotion weights for momentum calculation
        self.emotion_weights = {
            "creative": 0.9,
            "curious": 0.7,
            "contemplative": 0.8,
            "calm": 0.6,
            "neutral": 0.5,
            "anxious": 0.8,
            "overwhelmed": 1.0
        }
        
        # Recent metric changes for emergency detection
        self.recent_metrics = deque(maxlen=20)
        
        logger.info(f"Consciousness State Machine initialized in {initial_state} state")
    
    def calculate_next_state(self, current_metrics: Dict[str, float], 
                           consciousness_history: List[Dict[str, Any]],
                           pattern_info: Optional[Any] = None) -> Tuple[str, TransitionProgress]:
        """
        Calculate next consciousness state using refined transition logic
        
        Args:
            current_metrics: Current system metrics (scup, entropy, heat, etc.)
            consciousness_history: Recent consciousness state history
            pattern_info: Optional pattern detection information
            
        Returns:
            Tuple of (suggested_state, transition_progress)
        """
        now = datetime.now()
        
        # Store current metrics for emergency detection
        self.recent_metrics.append({
            'timestamp': now,
            'metrics': current_metrics.copy()
        })
        
        # Check if we're currently in a transition
        if self.current_transition and self.current_transition.in_transition:
            updated_transition = self._update_transition_progress()
            if updated_transition.in_transition:
                return updated_transition.to_state, updated_transition
            else:
                # Transition completed
                self._finalize_transition()
        
        # Check for emergency transitions first
        emergency_state = self._check_emergency_transitions(current_metrics)
        if emergency_state:
            logger.warning(f"🚨 Emergency transition triggered to {emergency_state}")
            transition = self._initiate_transition(emergency_state, "emergency", current_metrics, True)
            return emergency_state, transition
        
        # Calculate state suggestions from different sources
        metric_suggestion = self._calculate_metric_based_state(current_metrics)
        emotional_inertia = self._calculate_emotional_inertia()
        pattern_influence = self._calculate_pattern_influence(pattern_info, consciousness_history)
        
        # Weighted decision calculation
        state_scores = defaultdict(float)
        
        # Add metric-based suggestions
        for state, score in metric_suggestion.items():
            state_scores[state] += score * self.metric_weight
        
        # Add emotional inertia (tendency to stay in current state)
        current_state_boost = emotional_inertia * self.inertia_weight
        state_scores[self.current_state] += current_state_boost
        
        # Add pattern influence
        for state, score in pattern_influence.items():
            state_scores[state] += score * self.pattern_weight
        
        # Find the highest scoring state
        if not state_scores:
            suggested_state = self.current_state
        else:
            suggested_state = max(state_scores.keys(), key=lambda k: state_scores[k])
        
        # Calculate transition probability
        if suggested_state == self.current_state:
            # Stay in current state
            return self.current_state, self._get_current_transition_progress()
        else:
            # Check if transition should occur based on probability
            transition_probability = self._calculate_transition_probability(
                suggested_state, state_scores, current_metrics
            )
            
            # Determine if transition should happen
            if random.random() < transition_probability:
                # Initiate transition
                transition_reason = self._determine_transition_reason(
                    suggested_state, metric_suggestion, emotional_inertia, pattern_influence
                )
                
                transition = self._initiate_transition(
                    suggested_state, transition_reason, current_metrics, False
                )
                
                logger.info(f"🔄 State transition initiated: {self.current_state} → {suggested_state} "
                           f"(probability: {transition_probability:.3f}, reason: {transition_reason})")
                
                return suggested_state, transition
            else:
                # Stay in current state (transition probability too low)
                return self.current_state, self._get_current_transition_progress()
    
    def _check_emergency_transitions(self, current_metrics: Dict[str, float]) -> Optional[str]:
        """Check for emergency transition conditions"""
        if len(self.recent_metrics) < 2:
            return None
        
        # Check for rapid entropy changes
        recent_entropies = [m['metrics'].get('entropy', 0.5) for m in list(self.recent_metrics)[-5:]]
        time_window = (self.recent_metrics[-1]['timestamp'] - self.recent_metrics[-5]['timestamp']).total_seconds() if len(self.recent_metrics) >= 5 else 1.0
        
        if len(recent_entropies) >= 2 and time_window > 0:
            entropy_change = abs(recent_entropies[-1] - recent_entropies[0])
            
            if entropy_change > self.entropy_emergency_threshold and time_window < self.emergency_time_window:
                # Rapid entropy change detected
                if recent_entropies[-1] > 0.8:
                    return "overwhelmed"
                elif recent_entropies[-1] > 0.6:
                    return "anxious"
                elif recent_entropies[-1] < 0.3:
                    return "calm"
        
        # Check for extreme metric values
        scup = current_metrics.get('scup', 0.5)
        entropy = current_metrics.get('entropy', 0.5)
        heat = current_metrics.get('heat', 0.3)
        
        # Emergency overwhelmed state
        if entropy > 0.9 and heat > 0.9:
            return "overwhelmed"
        
        # Emergency calm state
        if scup > 0.9 and entropy < 0.2 and heat < 0.2:
            return "calm"
        
        return None
    
    def _calculate_metric_based_state(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """Calculate state suggestions based on current metrics"""
        suggestions = {}
        
        scup = metrics.get('scup', 0.5)
        entropy = metrics.get('entropy', 0.5)
        heat = metrics.get('heat', 0.3)
        
        # Calculate fitness scores for each state
        for state_name, state_metrics in self.state_metrics.items():
            # Calculate how well current metrics match this state's optimal metrics
            scup_fitness = 1.0 - abs(scup - state_metrics.optimal_scup)
            entropy_fitness = 1.0 - abs(entropy - state_metrics.optimal_entropy)
            heat_fitness = 1.0 - abs(heat - state_metrics.optimal_heat)
            
            # Combined fitness score
            fitness = (scup_fitness + entropy_fitness + heat_fitness) / 3.0
            suggestions[state_name] = max(0.0, fitness)
        
        return suggestions
    
    def _calculate_emotional_inertia(self) -> float:
        """Calculate emotional inertia (tendency to stay in current state)"""
        now = datetime.now()
        time_in_state = (now - self.state_start_time).total_seconds()
        
        # Base inertia
        inertia = self.base_inertia
        
        # Bonus inertia for prolonged states (up to 10 minutes)
        if time_in_state > self.prolonged_state_threshold:
            prolonged_bonus = min(
                self.max_inertia_bonus,
                (time_in_state - self.prolonged_state_threshold) / self.prolonged_state_threshold * self.max_inertia_bonus
            )
            inertia += prolonged_bonus
        
        # Calculate momentum from recent transitions
        momentum = self._calculate_momentum()
        
        # Adjust inertia based on momentum
        # High momentum reduces inertia (easier to change states)
        # Low momentum increases inertia (harder to change states)
        momentum_adjusted_inertia = inertia * (1.0 - momentum * 0.3)
        
        return max(0.1, min(1.0, momentum_adjusted_inertia))
    
    def _calculate_momentum(self) -> float:
        """Calculate emotional momentum based on recent transition history"""
        if not self.momentum_history:
            return 0.0
        
        now = datetime.now()
        momentum = 0.0
        
        for i, transition in enumerate(reversed(list(self.momentum_history))):
            age = (now - transition.timestamp).total_seconds()
            if age > 300:  # Only consider transitions from last 5 minutes
                continue
                
            # Weight by recency (1/age) and emotion weight
            from_emotion = transition.from_state
            to_emotion = transition.to_state
            
            emotion_weight = max(
                self.emotion_weights.get(from_emotion, 0.5),
                self.emotion_weights.get(to_emotion, 0.5)
            )
            
            # Calculate contribution to momentum
            age_weight = 1.0 / max(age, 1.0)  # Prevent division by zero
            contribution = age_weight * emotion_weight
            momentum += contribution
        
        # Normalize momentum
        return min(1.0, momentum / 10.0)
    
    def _calculate_pattern_influence(self, pattern_info: Optional[Any],
                                   consciousness_history: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate pattern-based state influence"""
        influence = defaultdict(float)
        
        # Pattern detection influence
        if pattern_info and hasattr(pattern_info, 'confidence'):
            if pattern_info.confidence > 0.8:
                # High confidence patterns suggest exploration states
                influence["curious"] += 0.7
                influence["creative"] += 0.5
            elif pattern_info.rebloop_trigger:
                # Rebloop triggers suggest need for change
                influence["anxious"] += 0.6
                influence["contemplative"] += 0.4
        
        # Consciousness history patterns
        if len(consciousness_history) >= 5:
            recent_emotions = [entry.get('emotion', 'neutral') for entry in consciousness_history[-5:]]
            emotion_counts = defaultdict(int)
            
            for emotion in recent_emotions:
                emotion_counts[emotion] += 1
            
            # If stuck in same emotion, suggest change
            dominant_emotion = max(emotion_counts.keys(), key=lambda k: emotion_counts[k])
            if emotion_counts[dominant_emotion] >= 4:  # 4 out of 5 recent states
                # Suggest variety
                for state in self.state_metrics.keys():
                    if state != dominant_emotion:
                        influence[state] += 0.3
        
        return dict(influence)
    
    def _calculate_transition_probability(self, target_state: str, state_scores: Dict[str, float],
                                        current_metrics: Dict[str, float]) -> float:
        """Calculate probability of transitioning to target state"""
        if target_state == self.current_state:
            return 0.0
        
        # Base probability from state score difference
        current_score = state_scores.get(self.current_state, 0.0)
        target_score = state_scores.get(target_state, 0.0)
        score_diff = target_score - current_score
        
        # Convert score difference to probability
        base_probability = math.sigmoid(score_diff * 4) if hasattr(math, 'sigmoid') else 1 / (1 + math.exp(-score_diff * 4))
        
        # Adjust for emotional inertia
        inertia = self._calculate_emotional_inertia()
        inertia_adjusted = base_probability * (1.0 - inertia * 0.6)
        
        # Adjust for state stability
        target_stability = self.state_metrics[target_state].stability_factor
        stability_adjusted = inertia_adjusted * target_stability
        
        # Minimum transition probability to prevent getting stuck
        min_probability = 0.05
        
        return max(min_probability, min(0.95, stability_adjusted))
    
    def _determine_transition_reason(self, target_state: str, metric_suggestion: Dict[str, float],
                                   emotional_inertia: float, pattern_influence: Dict[str, float]) -> str:
        """Determine the primary reason for state transition"""
        metric_score = metric_suggestion.get(target_state, 0.0) * self.metric_weight
        pattern_score = pattern_influence.get(target_state, 0.0) * self.pattern_weight
        
        if metric_score > pattern_score:
            return "metric_driven"
        elif pattern_score > 0.3:
            return "pattern_influenced"
        elif emotional_inertia < 0.3:
            return "momentum_change"
        else:
            return "gradual_evolution"
    
    def _initiate_transition(self, target_state: str, reason: str, 
                           metrics: Dict[str, float], is_emergency: bool) -> TransitionProgress:
        """Initiate a state transition"""
        now = datetime.now()
        
        # Calculate transition duration
        if is_emergency:
            duration = self.min_transition_duration
        else:
            # Longer transitions for more stable states
            target_stability = self.state_metrics[target_state].stability_factor
            duration = self.min_transition_duration + (target_stability * (self.max_transition_duration - self.min_transition_duration))
        
        # Create transition progress
        transition = TransitionProgress(
            in_transition=True,
            from_state=self.current_state,
            to_state=target_state,
            progress=0.0,
            start_time=now,
            expected_duration=duration,
            blended_properties=self._calculate_initial_blend(target_state)
        )
        
        # Create transition record
        transition_record = StateTransition(
            from_state=self.current_state,
            to_state=target_state,
            timestamp=now,
            duration=duration,
            trigger_reason=reason,
            metrics_snapshot=metrics.copy(),
            transition_probability=0.0,  # Will be updated
            momentum_factor=self._calculate_momentum(),
            inertia_factor=self._calculate_emotional_inertia(),
            pattern_influence=0.0,  # Will be updated
            is_emergency=is_emergency
        )
        
        # Update state machine state
        self.current_transition = transition
        self.transition_history.append(transition_record)
        
        # Add to momentum history
        self.momentum_history.append(transition_record)
        
        return transition
    
    def _update_transition_progress(self) -> TransitionProgress:
        """Update current transition progress"""
        if not self.current_transition:
            return self._get_current_transition_progress()
        
        now = datetime.now()
        elapsed = (now - self.current_transition.start_time).total_seconds()
        progress = min(1.0, elapsed / self.current_transition.expected_duration)
        
        # Update progress
        self.current_transition.progress = progress
        
        # Update blended properties
        self.current_transition.blended_properties = self._calculate_transition_blend(progress)
        
        # Check if transition is complete
        if progress >= 1.0:
            self.current_transition.in_transition = False
        
        return self.current_transition
    
    def _finalize_transition(self) -> None:
        """Finalize the current transition"""
        if not self.current_transition:
            return
        
        # Update current state
        old_state = self.current_state
        self.current_state = self.current_transition.to_state
        self.state_start_time = datetime.now()
        self.last_transition_time = datetime.now()
        
        # Add to state history
        self.state_history.append({
            'state': old_state,
            'duration': (self.state_start_time - self.state_start_time).total_seconds(),
            'end_time': self.state_start_time,
            'transition_to': self.current_state
        })
        
        logger.info(f"✅ State transition completed: {old_state} → {self.current_state}")
        
        # Clear current transition
        self.current_transition = None
    
    def _calculate_initial_blend(self, target_state: str) -> Dict[str, float]:
        """Calculate initial blended properties at transition start"""
        current_metrics = self.state_metrics[self.current_state]
        target_metrics = self.state_metrics[target_state]
        
        # Start with current state properties
        return {
            'scup': current_metrics.optimal_scup,
            'entropy': current_metrics.optimal_entropy,
            'heat': current_metrics.optimal_heat,
            'stability': current_metrics.stability_factor,
            'energy': current_metrics.energy_level,
            'creativity': current_metrics.creativity_factor,
            'introspection': current_metrics.introspection_factor
        }
    
    def _calculate_transition_blend(self, progress: float) -> Dict[str, float]:
        """Calculate blended properties during transition"""
        if not self.current_transition:
            return {}
        
        current_metrics = self.state_metrics[self.current_transition.from_state]
        target_metrics = self.state_metrics[self.current_transition.to_state]
        
        # Use easing function for smooth transition
        eased_progress = self._ease_in_out_cubic(progress)
        
        return {
            'scup': self._lerp(current_metrics.optimal_scup, target_metrics.optimal_scup, eased_progress),
            'entropy': self._lerp(current_metrics.optimal_entropy, target_metrics.optimal_entropy, eased_progress),
            'heat': self._lerp(current_metrics.optimal_heat, target_metrics.optimal_heat, eased_progress),
            'stability': self._lerp(current_metrics.stability_factor, target_metrics.stability_factor, eased_progress),
            'energy': self._lerp(current_metrics.energy_level, target_metrics.energy_level, eased_progress),
            'creativity': self._lerp(current_metrics.creativity_factor, target_metrics.creativity_factor, eased_progress),
            'introspection': self._lerp(current_metrics.introspection_factor, target_metrics.introspection_factor, eased_progress)
        }
    
    def _ease_in_out_cubic(self, t: float) -> float:
        """Cubic easing function for smooth transitions"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            p = 2 * t - 2
            return 1 + p * p * p / 2
    
    def _lerp(self, start: float, end: float, t: float) -> float:
        """Linear interpolation between two values"""
        return start + (end - start) * t
    
    def _get_current_transition_progress(self) -> TransitionProgress:
        """Get current transition progress or create stable state progress"""
        if self.current_transition and self.current_transition.in_transition:
            return self.current_transition
        
        # Create stable state progress
        current_metrics = self.state_metrics[self.current_state]
        return TransitionProgress(
            in_transition=False,
            from_state=self.current_state,
            to_state=self.current_state,
            progress=1.0,
            start_time=self.state_start_time,
            expected_duration=0.0,
            blended_properties={
                'scup': current_metrics.optimal_scup,
                'entropy': current_metrics.optimal_entropy,
                'heat': current_metrics.optimal_heat,
                'stability': current_metrics.stability_factor,
                'energy': current_metrics.energy_level,
                'creativity': current_metrics.creativity_factor,
                'introspection': current_metrics.introspection_factor
            }
        )
    
    def get_state_info(self) -> Dict[str, Any]:
        """Get comprehensive state machine information"""
        now = datetime.now()
        time_in_state = (now - self.state_start_time).total_seconds()
        
        return {
            'current_state': self.current_state,
            'time_in_state': time_in_state,
            'is_transitioning': self.current_transition.in_transition if self.current_transition else False,
            'transition_progress': self.current_transition.progress if self.current_transition else 0.0,
            'emotional_momentum': self._calculate_momentum(),
            'emotional_inertia': self._calculate_emotional_inertia(),
            'state_metrics': self.state_metrics[self.current_state].__dict__,
            'recent_transitions': len(self.transition_history),
            'transition_queue_size': len(self.transition_queue)
        }
    
    def get_transition_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent transition history"""
        recent_transitions = list(self.transition_history)[-limit:]
        
        return [
            {
                'from_state': t.from_state,
                'to_state': t.to_state,
                'timestamp': t.timestamp.isoformat(),
                'duration': t.duration,
                'trigger_reason': t.trigger_reason,
                'is_emergency': t.is_emergency,
                'momentum_factor': t.momentum_factor,
                'inertia_factor': t.inertia_factor
            }
            for t in recent_transitions
        ]
    
    def get_state_statistics(self) -> Dict[str, Any]:
        """Get state machine statistics"""
        if not self.state_history:
            return {'status': 'no_history'}
        
        # Calculate state durations
        state_durations = defaultdict(list)
        for entry in self.state_history:
            state_durations[entry['state']].append(entry['duration'])
        
        # Calculate averages
        state_averages = {}
        for state, durations in state_durations.items():
            state_averages[state] = sum(durations) / len(durations)
        
        # Transition analysis
        transition_counts = defaultdict(int)
        for transition in self.transition_history:
            key = f"{transition.from_state}→{transition.to_state}"
            transition_counts[key] += 1
        
        return {
            'total_transitions': len(self.transition_history),
            'average_state_durations': state_averages,
            'most_common_transitions': dict(sorted(transition_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            'current_momentum': self._calculate_momentum(),
            'current_inertia': self._calculate_emotional_inertia(),
            'emergency_transitions': sum(1 for t in self.transition_history if t.is_emergency)
        }


# Factory function for easy integration
def create_state_machine(initial_state: str = "neutral") -> ConsciousnessStateMachine:
    """Create a consciousness state machine"""
    return ConsciousnessStateMachine(initial_state)


# Example usage and testing
if __name__ == "__main__":
    print("Testing DAWN Consciousness State Machine")
    print("=" * 50)
    
    # Create state machine
    state_machine = create_state_machine("neutral")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Gradual Creative Buildup",
            "metrics": {"scup": 0.7, "entropy": 0.8, "heat": 0.6},
            "description": "High entropy and SCUP should suggest creative state"
        },
        {
            "name": "Calm Contemplation",
            "metrics": {"scup": 0.9, "entropy": 0.2, "heat": 0.1},
            "description": "High SCUP, low entropy/heat should suggest calm state"
        },
        {
            "name": "Emergency Overwhelm",
            "metrics": {"scup": 0.3, "entropy": 0.95, "heat": 0.9},
            "description": "Extreme values should trigger emergency transition"
        },
        {
            "name": "Moderate Curiosity",
            "metrics": {"scup": 0.6, "entropy": 0.5, "heat": 0.4},
            "description": "Balanced values should suggest curious state"
        },
        {
            "name": "Rapid Entropy Change",
            "metrics": {"scup": 0.5, "entropy": 0.9, "heat": 0.7},
            "description": "Simulating rapid entropy change for emergency detection"
        }
    ]
    
    print("\n🔄 Testing State Transitions:")
    print("-" * 40)
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n--- Test {i+1}: {scenario['name']} ---")
        print(f"Metrics: SCUP={scenario['metrics']['scup']:.1f}, "
              f"Entropy={scenario['metrics']['entropy']:.1f}, "
              f"Heat={scenario['metrics']['heat']:.1f}")
        print(f"Expected: {scenario['description']}")
        
        # Simulate consciousness history
        consciousness_history = [
            {"emotion": state_machine.current_state, "intensity": 0.6, "timestamp": datetime.now()}
            for _ in range(5)
        ]
        
        # Calculate next state
        suggested_state, transition_progress = state_machine.calculate_next_state(
            scenario['metrics'], consciousness_history
        )
        
        print(f"\nResult: {state_machine.current_state} → {suggested_state}")
        
        if transition_progress.in_transition:
            print(f"🔄 Transition in progress:")
            print(f"   Progress: {transition_progress.progress:.1%}")
            print(f"   Duration: {transition_progress.expected_duration:.1f}s")
            print(f"   Blended Properties:")
            for prop, value in transition_progress.blended_properties.items():
                print(f"     {prop}: {value:.3f}")
        else:
            print(f"✅ Stable in {suggested_state} state")
        
        # Show state machine info
        state_info = state_machine.get_state_info()
        print(f"\n📊 State Info:")
        print(f"   Time in state: {state_info['time_in_state']:.1f}s")
        print(f"   Emotional momentum: {state_info['emotional_momentum']:.3f}")
        print(f"   Emotional inertia: {state_info['emotional_inertia']:.3f}")
        
        # Simulate time passage for transition testing
        time.sleep(0.5)
        
        # Update transition if in progress
        if transition_progress.in_transition:
            time.sleep(1.0)  # Simulate more time passage
            updated_transition = state_machine._update_transition_progress()
            print(f"   Updated progress: {updated_transition.progress:.1%}")
    
    # Show comprehensive statistics
    print(f"\n{'='*50}")
    print("📈 State Machine Statistics:")
    stats = state_machine.get_state_statistics()
    
    if stats.get('status') != 'no_history':
        print(f"   Total transitions: {stats['total_transitions']}")
        print(f"   Emergency transitions: {stats['emergency_transitions']}")
        print(f"   Current momentum: {stats['current_momentum']:.3f}")
        print(f"   Current inertia: {stats['current_inertia']:.3f}")
        
        if stats['most_common_transitions']:
            print(f"   Most common transitions:")
            for transition, count in list(stats['most_common_transitions'].items())[:3]:
                print(f"     {transition}: {count}")
    
    # Show recent transitions
    print(f"\n🔄 Recent Transition History:")
    recent_transitions = state_machine.get_transition_history(5)
    for i, transition in enumerate(recent_transitions):
        print(f"   {i+1}. {transition['from_state']} → {transition['to_state']} "
              f"({transition['trigger_reason']}) "
              f"{'🚨' if transition['is_emergency'] else '✅'}")
    
    print(f"\n✨ Consciousness State Machine Test Complete!")
    print("   Features Demonstrated:")
    print("   ✓ Refined transition algorithm with weighted decision making")
    print("   ✓ Emotional momentum tracking (last 10 transitions)")
    print("   ✓ Inertia calculation based on time in state")
    print("   ✓ Emergency transition detection")
    print("   ✓ Smooth probabilistic transitions (2-5 second duration)")
    print("   ✓ Property blending during transitions")
    print("   ✓ Comprehensive state history and logging")
    print("   ✓ Transition reason categorization") 