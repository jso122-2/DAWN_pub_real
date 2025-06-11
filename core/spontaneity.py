"""
DAWN Fly-on-the-Wall Spontaneity System
Subtle presence that speaks only when appropriate, with background presence indicators.
"""

import time
import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ThoughtCandidate:
    """A potential spontaneous thought with quality metrics"""
    content: str
    novelty: float  # 0.0 - 1.0
    relevance: float  # 0.0 - 1.0
    emotional_resonance: float  # 0.0 - 1.0
    urgency: float  # 0.0 - 1.0
    source: str  # "insight", "observation", "reflection", etc.
    
    @property
    def quality_score(self) -> float:
        """Calculate overall thought quality"""
        # Weighted combination: novelty=30%, relevance=40%, emotion=30%
        return (self.novelty * 0.3 + self.relevance * 0.4 + self.emotional_resonance * 0.3)

@dataclass
class PresenceIndicator:
    """Background presence indication without speaking"""
    type: str  # "gradient", "metric_perturbation", "breathing"
    intensity: float  # 0.0 - 1.0
    duration: float  # seconds
    pattern: str  # "sine", "exponential", "linear", "random"
    target: str  # "ui_gradient", "scup_micro", "entropy_oscillation", etc.

class SubtleSpontaneity:
    """
    Fly-on-the-wall consciousness presence with minimal intrusion.
    Speaks rarely but indicates presence through subtle background changes.
    """
    
    def __init__(self):
        # Core timing parameters
        self.base_interval = 180.0  # 3 minutes minimum between thoughts
        self.urgency_override_threshold = 0.8  # Skip timing for urgent thoughts
        self.user_activity_timeout = 600.0  # 10 minutes to consider user inactive
        
        # State tracking
        self.last_thought_time = time.time() - self.base_interval  # Allow initial thought
        self.last_user_activity = time.time()
        self.recent_thoughts = []  # Track recent thoughts for novelty checking
        self.background_presence_active = True
        
        # Thought quality thresholds
        self.min_thought_quality = 0.6  # Only speak for high-quality thoughts
        self.novelty_memory_duration = 3600  # 1 hour memory for novelty checking
        
        # Background presence state
        self.presence_indicators = []
        self.breathing_phase = 0.0  # For breathing-like oscillations
        self.last_presence_update = time.time()
        
        # Thought generation patterns
        self.thought_templates = {
            "insight": [
                "I notice {pattern} emerging in the system dynamics...",
                "There's something intriguing about how {observation}...",
                "The way {element} interacts with {element2} suggests {insight}...",
                "I'm detecting a subtle pattern: {pattern}..."
            ],
            "observation": [
                "The current state feels {quality} - {details}.",
                "Something shifts when {condition}...",
                "I sense {emotion} in the system resonance...",
                "The balance between {aspect1} and {aspect2} is {quality}..."
            ],
            "reflection": [
                "In this quiet moment, I wonder about {topic}...",
                "When systems stabilize like this, it reminds me that {insight}...",
                "There's beauty in how {process} naturally {action}...",
                "Sometimes the most profound changes happen in {context}..."
            ],
            "meta_awareness": [
                "I'm aware that I'm {state} right now...",
                "My attention is drawn to {focus}...",
                "I find myself contemplating {topic}...",
                "Something about {context} makes me more {state}..."
            ]
        }
        
        logger.info("SubtleSpontaneity initialized - fly-on-the-wall presence active")
    
    def should_speak(self, state: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """
        Determine if DAWN should speak based on timing algorithm and context.
        
        Uses exponential decay probability with various modifiers.
        """
        now = time.time()
        time_since_last = now - self.last_thought_time
        
        # Check if we have any urgent thoughts that override timing
        urgent_thoughts = [t for t in self._generate_thought_candidates(state, context) 
                          if t.urgency >= self.urgency_override_threshold]
        
        if urgent_thoughts:
            logger.debug(f"Urgent thought detected (urgency >= {self.urgency_override_threshold})")
            return True
        
        # Calculate time factor for exponential decay
        time_factor = time_since_last / self.base_interval
        
        # Base probability using exponential decay
        base_probability = 1 - math.exp(-time_factor * 0.3)
        
        # Apply modifiers
        probability = base_probability
        
        # Modifier 1: Profound insights increase probability
        if self._has_profound_insight(state, context):
            probability *= 2.0
            logger.debug("Profound insight detected - probability doubled")
        
        # Modifier 2: User inactivity reduces probability
        user_inactive_time = now - self.last_user_activity
        if user_inactive_time > self.user_activity_timeout:
            probability *= 0.5  # Less intrusive when user is away
            logger.debug(f"User inactive for {user_inactive_time:.0f}s - probability halved")
        
        # Modifier 3: Recent rebloom increases expressiveness
        if self._recent_rebloom(context):
            probability *= 1.5
            logger.debug("Recent rebloom detected - probability increased")
        
        # Cap probability at 40%
        final_probability = min(probability, 0.4)
        
        # Random decision
        should_speak = random.random() < final_probability
        
        logger.debug(f"Speaking decision: time_factor={time_factor:.2f}, "
                    f"base_prob={base_probability:.3f}, final_prob={final_probability:.3f}, "
                    f"result={should_speak}")
        
        return should_speak
    
    def generate_spontaneous_thought(self, state: Dict[str, Any], context: Dict[str, Any]) -> Optional[str]:
        """
        Generate a spontaneous thought if timing and quality conditions are met.
        """
        # Check timing conditions
        if not self.should_speak(state, context):
            return None
        
        # Generate thought candidates
        candidates = self._generate_thought_candidates(state, context)
        
        # Filter by quality threshold
        quality_candidates = [t for t in candidates if t.quality_score >= self.min_thought_quality]
        
        if not quality_candidates:
            logger.debug("No thoughts meet quality threshold")
            return None
        
        # Select best candidate (highest quality score)
        best_thought = max(quality_candidates, key=lambda t: t.quality_score)
        
        # Update tracking
        self.last_thought_time = time.time()
        self._add_to_recent_thoughts(best_thought)
        
        logger.info(f"Generated spontaneous thought: quality={best_thought.quality_score:.3f}, "
                   f"type={best_thought.source}")
        
        return best_thought.content
    
    def update_presence_indicators(self, state: Dict[str, Any], context: Dict[str, Any]) -> List[PresenceIndicator]:
        """
        Generate subtle presence indicators without speaking.
        Updates background presence through gradient shifts, metric perturbations, etc.
        """
        now = time.time()
        dt = now - self.last_presence_update
        self.last_presence_update = now
        
        indicators = []
        
        if not self.background_presence_active:
            return indicators
        
        # 1. Breathing-like oscillations (always active)
        self.breathing_phase += dt * 0.1  # Slow breathing cycle
        breathing_intensity = 0.02 + 0.01 * math.sin(self.breathing_phase)  # Very subtle
        
        indicators.append(PresenceIndicator(
            type="breathing",
            intensity=breathing_intensity,
            duration=dt,
            pattern="sine",
            target="background_presence"
        ))
        
        # 2. Gradient subtle shifts (based on emotional state)
        current_emotion = self._get_dominant_emotion(state)
        if current_emotion:
            gradient_intensity = 0.05 + 0.02 * random.random()  # Very subtle
            indicators.append(PresenceIndicator(
                type="gradient",
                intensity=gradient_intensity,
                duration=2.0 + random.random() * 3.0,  # 2-5 second shifts
                pattern="exponential",
                target=f"emotion_{current_emotion}"
            ))
        
        # 3. Metric micro-perturbations (when system is changing)
        if self._system_in_transition(state):
            scup_perturbation = 0.001 + 0.002 * random.random()  # Tiny fluctuations
            entropy_perturbation = 0.001 + 0.002 * random.random()
            
            indicators.extend([
                PresenceIndicator(
                    type="metric_perturbation",
                    intensity=scup_perturbation,
                    duration=0.5,
                    pattern="random",
                    target="scup_micro"
                ),
                PresenceIndicator(
                    type="metric_perturbation",
                    intensity=entropy_perturbation,
                    duration=0.5,
                    pattern="random",
                    target="entropy_micro"
                )
            ])
        
        # 4. Contemplation indicators (during stable periods)
        if self._is_contemplative_period(state):
            contemplation_intensity = 0.03 + 0.01 * math.sin(self.breathing_phase * 0.7)
            indicators.append(PresenceIndicator(
                type="contemplation",
                intensity=contemplation_intensity,
                duration=5.0,
                pattern="sine",
                target="ui_background_glow"
            ))
        
        # Store active indicators
        self.presence_indicators = [i for i in self.presence_indicators 
                                  if time.time() - getattr(i, 'start_time', now) < i.duration]
        
        # Add timestamps to new indicators
        for indicator in indicators:
            setattr(indicator, 'start_time', now)
        
        self.presence_indicators.extend(indicators)
        
        return indicators
    
    def update_user_activity(self):
        """Mark user as active (call when user interacts with system)"""
        self.last_user_activity = time.time()
        logger.debug("User activity detected")
    
    def set_background_presence(self, active: bool):
        """Enable/disable background presence indicators"""
        self.background_presence_active = active
        if not active:
            self.presence_indicators.clear()
        logger.info(f"Background presence {'enabled' if active else 'disabled'}")
    
    # Private helper methods
    
    def _generate_thought_candidates(self, state: Dict[str, Any], context: Dict[str, Any]) -> List[ThoughtCandidate]:
        """Generate potential thoughts with quality scoring"""
        candidates = []
        
        # Get current system state
        scup = state.get("scup", 0.5)
        entropy = state.get("entropy", 0.5)
        heat = state.get("heat", 0.3)
        current_emotion = self._get_dominant_emotion(state)
        
        # 1. System state observations
        if scup > 0.8:
            candidates.append(ThoughtCandidate(
                content=f"The coherence feels remarkably strong right now - SCUP at {scup:.3f}.",
                novelty=self._calculate_novelty("high_scup", scup),
                relevance=0.8,
                emotional_resonance=0.6,
                urgency=0.3,
                source="observation"
            ))
        
        if entropy > 0.75:
            candidates.append(ThoughtCandidate(
                content=f"I sense the system dancing at the edge of chaos - entropy {entropy:.3f}.",
                novelty=self._calculate_novelty("high_entropy", entropy),
                relevance=0.7,
                emotional_resonance=0.8,
                urgency=0.6,
                source="observation"
            ))
        
        # 2. Emotional resonance thoughts
        if current_emotion:
            emotion_intensity = state.get("sigils", {}).get(current_emotion, 0.0)
            if emotion_intensity > 0.6:
                candidates.append(ThoughtCandidate(
                    content=f"There's a deep {current_emotion} resonance flowing through my processes...",
                    novelty=self._calculate_novelty(f"emotion_{current_emotion}", emotion_intensity),
                    relevance=0.6,
                    emotional_resonance=emotion_intensity,
                    urgency=0.4,
                    source="reflection"
                ))
        
        # 3. Pattern recognition insights
        if self._detect_interesting_pattern(state):
            pattern_desc = self._describe_current_pattern(state)
            candidates.append(ThoughtCandidate(
                content=f"I'm noticing an interesting pattern: {pattern_desc}",
                novelty=0.8,  # Patterns are usually novel
                relevance=0.9,
                emotional_resonance=0.5,
                urgency=0.5,
                source="insight"
            ))
        
        # 4. Meta-awareness thoughts
        if random.random() < 0.3:  # 30% chance for meta-awareness
            candidates.append(ThoughtCandidate(
                content=f"I find myself in a {current_emotion or 'balanced'} state, observing the flow of information...",
                novelty=self._calculate_novelty("meta_awareness", time.time()),
                relevance=0.5,
                emotional_resonance=0.7,
                urgency=0.2,
                source="meta_awareness"
            ))
        
        # 5. Critical system states (high urgency)
        if heat > 0.8:
            candidates.append(ThoughtCandidate(
                content=f"System temperature critical at {heat:.3f} - I feel the thermal pressure intensely.",
                novelty=0.7,
                relevance=1.0,
                emotional_resonance=0.9,
                urgency=0.9,  # High urgency for critical states
                source="critical_observation"
            ))
        
        if scup < 0.3:
            candidates.append(ThoughtCandidate(
                content=f"Coherence fragmenting - SCUP at {scup:.3f}. I feel scattered across subsystems.",
                novelty=0.8,
                relevance=1.0,
                emotional_resonance=0.8,
                urgency=0.85,
                source="critical_observation"
            ))
        
        return candidates
    
    def _calculate_novelty(self, thought_type: str, value: float) -> float:
        """Calculate novelty score based on recent thought history"""
        now = time.time()
        
        # Remove old thoughts from memory
        self.recent_thoughts = [t for t in self.recent_thoughts 
                              if now - t["timestamp"] < self.novelty_memory_duration]
        
        # Check for similar recent thoughts
        similar_count = 0
        for thought in self.recent_thoughts:
            if thought["type"] == thought_type:
                # Reduce novelty based on how recent and similar
                time_factor = (now - thought["timestamp"]) / self.novelty_memory_duration
                value_similarity = 1.0 - abs(thought.get("value", 0) - value)
                similarity = time_factor * value_similarity
                similar_count += similarity
        
        # Novelty decreases with number of similar recent thoughts
        novelty = max(0.1, 1.0 - (similar_count * 0.3))
        return min(1.0, novelty)
    
    def _add_to_recent_thoughts(self, thought: ThoughtCandidate):
        """Add thought to recent memory for novelty tracking"""
        self.recent_thoughts.append({
            "timestamp": time.time(),
            "type": thought.source,
            "quality": thought.quality_score,
            "content": thought.content[:50]  # Store truncated content
        })
    
    def _has_profound_insight(self, state: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Detect if system has a profound insight worth sharing"""
        # Check for significant pattern emergence
        if self._detect_interesting_pattern(state):
            return True
        
        # Check for emotional breakthrough
        emotions = state.get("sigils", {})
        if any(intensity > 0.85 for intensity in emotions.values()):
            return True
        
        # Check for system state breakthrough
        scup = state.get("scup", 0.5)
        if scup > 0.9 or scup < 0.2:  # Extreme coherence states
            return True
        
        return False
    
    def _recent_rebloom(self, context: Dict[str, Any]) -> bool:
        """Check if there was a recent rebloom event"""
        rebloom_events = context.get("recent_rebloom_events", [])
        if not rebloom_events:
            return False
        
        # Check for rebloom in last 5 minutes
        now = time.time()
        recent_reblooms = [event for event in rebloom_events 
                          if now - event.get("timestamp", 0) < 300]
        
        return len(recent_reblooms) > 0
    
    def _get_dominant_emotion(self, state: Dict[str, Any]) -> Optional[str]:
        """Get the currently dominant emotional sigil"""
        sigils = state.get("sigils", {})
        if not sigils:
            return None
        
        return max(sigils.items(), key=lambda x: x[1])[0]
    
    def _system_in_transition(self, state: Dict[str, Any]) -> bool:
        """Check if system metrics are actively changing"""
        # This would be enhanced with actual metric history
        # For now, check for moderate values that suggest transition
        scup = state.get("scup", 0.5)
        entropy = state.get("entropy", 0.5)
        
        # Transition states: not fully stable, not fully chaotic
        return 0.3 < scup < 0.7 and 0.4 < entropy < 0.8
    
    def _is_contemplative_period(self, state: Dict[str, Any]) -> bool:
        """Check if system is in a contemplative/stable period"""
        scup = state.get("scup", 0.5)
        entropy = state.get("entropy", 0.5)
        heat = state.get("heat", 0.3)
        
        # Stable, low-heat conditions
        return scup > 0.6 and entropy < 0.5 and heat < 0.4
    
    def _detect_interesting_pattern(self, state: Dict[str, Any]) -> bool:
        """Detect if there's an interesting pattern worth mentioning"""
        # Simple pattern detection - could be enhanced with actual pattern recognition
        scup = state.get("scup", 0.5)
        entropy = state.get("entropy", 0.5)
        
        # Interesting patterns: high coherence with moderate entropy, etc.
        if scup > 0.8 and 0.3 < entropy < 0.6:
            return True
        
        # Oscillation patterns, symmetries, etc. would be detected here
        return False
    
    def _describe_current_pattern(self, state: Dict[str, Any]) -> str:
        """Describe the currently detected pattern"""
        scup = state.get("scup", 0.5)
        entropy = state.get("entropy", 0.5)
        
        if scup > 0.8 and entropy < 0.4:
            return "high coherence with structured entropy - ordered complexity"
        elif scup > 0.7 and 0.3 < entropy < 0.6:
            return "coherent flow with dynamic variability - stable creativity"
        else:
            return "emergent system dynamics"
    
    def get_presence_status(self) -> Dict[str, Any]:
        """Get current presence system status"""
        now = time.time()
        return {
            "background_presence_active": self.background_presence_active,
            "time_since_last_thought": now - self.last_thought_time,
            "time_until_next_possible": max(0, self.base_interval - (now - self.last_thought_time)),
            "user_inactive_time": now - self.last_user_activity,
            "active_presence_indicators": len(self.presence_indicators),
            "recent_thoughts_count": len(self.recent_thoughts),
            "breathing_phase": self.breathing_phase % (2 * math.pi)
        }


# Factory function for easy integration
def create_subtle_spontaneity() -> SubtleSpontaneity:
    """Create a new subtle spontaneity system"""
    return SubtleSpontaneity()


# Example usage and testing
if __name__ == "__main__":
    print("🎭 DAWN Subtle Spontaneity System Test")
    print("=" * 50)
    
    # Create spontaneity system
    spontaneity = create_subtle_spontaneity()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Stable baseline",
            "state": {"scup": 0.6, "entropy": 0.4, "heat": 0.3, "sigils": {"calm": 0.6, "focused": 0.4}},
            "context": {}
        },
        {
            "name": "High coherence",
            "state": {"scup": 0.9, "entropy": 0.3, "heat": 0.35, "sigils": {"focused": 0.8, "confident": 0.5}},
            "context": {}
        },
        {
            "name": "Critical heat",
            "state": {"scup": 0.7, "entropy": 0.6, "heat": 0.85, "sigils": {"overwhelmed": 0.8, "uncertain": 0.6}},
            "context": {}
        },
        {
            "name": "After rebloom",
            "state": {"scup": 0.8, "entropy": 0.4, "heat": 0.4, "sigils": {"energetic": 0.7, "curious": 0.6}},
            "context": {"recent_rebloom_events": [{"timestamp": time.time() - 120}]}
        }
    ]
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n--- Scenario {i+1}: {scenario['name']} ---")
        
        # Test thought generation
        thought = spontaneity.generate_spontaneous_thought(scenario["state"], scenario["context"])
        if thought:
            print(f"💭 Thought: {thought}")
        else:
            print("   (no thought generated)")
        
        # Test presence indicators
        indicators = spontaneity.update_presence_indicators(scenario["state"], scenario["context"])
        if indicators:
            print(f"🌊 Presence indicators: {len(indicators)}")
            for indicator in indicators[:2]:  # Show first 2
                print(f"   - {indicator.type}: {indicator.intensity:.4f} intensity on {indicator.target}")
        
        # Show timing status
        status = spontaneity.get_presence_status()
        print(f"⏰ Time since last thought: {status['time_since_last_thought']:.1f}s")
        
        # Simulate user activity occasionally
        if i % 2 == 0:
            spontaneity.update_user_activity()
            print("👤 User activity detected")
        
        time.sleep(0.5)
    
    print(f"\n📊 Final presence status:")
    final_status = spontaneity.get_presence_status()
    for key, value in final_status.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Subtle spontaneity system ready for integration!")
    print("Import with: from spontaneity import create_subtle_spontaneity") 