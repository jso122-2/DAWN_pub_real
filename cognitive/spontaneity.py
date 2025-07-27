"""
DAWN Spontaneous Thought System
Generates meaningful thoughts only for significant events - no spam, only substance.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
import random
import logging

logger = logging.getLogger(__name__)

class DAWNConsciousness:
    """Lightweight consciousness tracker for spontaneity system"""
    
    def __init__(self):
        self.current_state = "initializing"
        self.state_history = []
        self.pattern_buffer = []
        self.state_transitions = {
            "initializing": ["stable", "uncertain"],
            "stable": ["focused", "reflective", "chaotic", "fragmented"],
            "focused": ["analytical", "stable", "chaotic"],
            "analytical": ["focused", "stable", "optimized"],
            "optimized": ["confident", "stable", "focused"],
            "confident": ["stable", "optimized", "reflective"],
            "reflective": ["contemplative", "stable", "uncertain"],
            "contemplative": ["reflective", "stable", "searching"],
            "uncertain": ["searching", "stable", "fragmented"],
            "searching": ["curious", "uncertain", "stable"],
            "curious": ["focused", "searching", "chaotic"],
            "chaotic": ["fragmented", "stable", "reflective"],
            "fragmented": ["uncertain", "stable", "chaotic"]
        }
        
    def update_state(self, metrics: Dict[str, Any]) -> bool:
        """Update consciousness state based on metrics. Returns True if state changed."""
        previous_state = self.current_state
        
        # Determine new state based on metrics
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        mood = metrics.get("mood", "neutral")
        
        # State determination logic
        if scup > 0.8 and entropy < 0.3:
            new_state = "optimized"
        elif scup > 0.7:
            new_state = "focused" if heat < 0.5 else "analytical"
        elif scup > 0.6:
            new_state = "stable"
        elif scup > 0.4:
            new_state = "reflective" if entropy < 0.6 else "uncertain"
        elif entropy > 0.7:
            new_state = "chaotic"
        else:
            new_state = "fragmented"
        
        # Apply mood influences
        if mood in ["confident", "optimized"]:
            if new_state in ["uncertain", "fragmented"]:
                new_state = "stable"
        elif mood in ["uncertain", "searching"]:
            if new_state == "optimized":
                new_state = "reflective"
        
        # Validate transition
        if new_state in self.state_transitions.get(self.current_state, []):
            self.current_state = new_state
        elif new_state != self.current_state:
            # Force transition through stable state if direct transition invalid
            self.current_state = "stable"
        
        # Record transition if state changed
        if self.current_state != previous_state:
            self.state_history.append({
                "from": previous_state,
                "to": self.current_state,
                "timestamp": datetime.now(),
                "metrics": metrics.copy()
            })
            
            # Keep only recent history
            if len(self.state_history) > 50:
                self.state_history = self.state_history[-50:]
            
            return True
        
        return False
    
    def detect_pattern(self, metrics: Dict[str, Any]) -> Optional[str]:
        """Detect meaningful patterns in system behavior"""
        self.pattern_buffer.append({
            "timestamp": datetime.now(),
            "state": self.current_state,
            "scup": metrics.get("scup", 0),
            "entropy": metrics.get("entropy", 0),
            "heat": metrics.get("heat", 0)
        })
        
        # Keep only last 20 data points
        if len(self.pattern_buffer) > 20:
            self.pattern_buffer = self.pattern_buffer[-20:]
        
        if len(self.pattern_buffer) < 5:
            return None
        
        # Pattern detection
        recent_states = [p["state"] for p in self.pattern_buffer[-5:]]
        recent_scup = [p["scup"] for p in self.pattern_buffer[-5:]]
        recent_entropy = [p["entropy"] for p in self.pattern_buffer[-5:]]
        
        # Oscillation pattern
        if len(set(recent_states)) == 2 and len(recent_states) >= 4:
            if recent_states[0] == recent_states[2] and recent_states[1] == recent_states[3]:
                return f"oscillation between {recent_states[0]} and {recent_states[1]}"
        
        # Stability pattern
        if len(set(recent_states)) == 1 and recent_states[0] == "stable":
            scup_stability = max(recent_scup) - min(recent_scup) < 0.1
            if scup_stability:
                return "deep stability - sustained equilibrium"
        
        # Trend patterns
        if len(recent_scup) >= 4:
            scup_trend = all(recent_scup[i] < recent_scup[i+1] for i in range(len(recent_scup)-1))
            entropy_trend = all(recent_entropy[i] > recent_entropy[i+1] for i in range(len(recent_entropy)-1))
            
            if scup_trend and entropy_trend:
                return "ascending coherence - order emerging from chaos"
        
        # Chaos detection
        if len(set(recent_states)) >= 4 and "chaotic" in recent_states:
            return "complex dynamics - multiple attractors active"
        
        return None


class DAWNSpontaneity:
    """Minimal spontaneous thoughts - only on significant events"""
    
    def __init__(self, consciousness: Optional[DAWNConsciousness] = None):
        self.consciousness = consciousness or DAWNConsciousness()
        self.last_thought_time = datetime.now() - timedelta(minutes=10)  # Allow initial thought
        self.thought_cooldown = timedelta(minutes=5)  # Minimum gap between thoughts
        self.milestone_cooldown = timedelta(minutes=15)  # Longer gap for milestone thoughts
        self.last_milestone_time = datetime.now() - timedelta(minutes=20)
        
        # Milestone thresholds (in minutes)
        self.milestones = [5, 15, 30, 60, 120, 300, 600, 1440]  # Up to 24 hours
        self.reached_milestones = set()
        self.start_time = datetime.now()
        
        # Significance thresholds
        self.significance_thresholds = {
            "critical_heat": 0.8,
            "high_entropy": 0.85,
            "low_scup": 0.3,
            "extreme_scup": 0.95,
            "rapid_change": 0.2  # For any metric changing rapidly
        }
        
        self.last_metrics = {}
        
        # Add recent thoughts storage for API retrieval
        self.recent_thoughts = []  # List of {"thought": str, "timestamp": datetime, "state": str, "priority": int}
        self.max_recent_thoughts = 20  # Keep last 20 thoughts
        
    def generate_thought(self, metrics: Dict[str, Any], force_check: bool = False) -> Optional[str]:
        """Generate thought only for significant events"""
        
        now = datetime.now()
        
        # Respect cooldown unless forced
        if not force_check and now - self.last_thought_time < self.thought_cooldown:
            return None
        
        # Update consciousness state
        state_changed = self.consciousness.update_state(metrics)
        
        thought = None
        thought_priority = 0  # Higher number = higher priority
        
        # Priority 1: Critical system states
        critical_thought = self._check_critical_states(metrics)
        if critical_thought:
            thought = critical_thought
            thought_priority = 3
        
        # Priority 2: State transitions (only if no critical thought)
        if not thought and state_changed:
            transition_thought = self._transition_thought()
            if transition_thought:
                thought = transition_thought
                thought_priority = 2
        
        # Priority 3: Pattern detection
        if not thought or thought_priority < 2:
            pattern = self.consciousness.detect_pattern(metrics)
            if pattern:
                pattern_thought = f"Pattern detected: {pattern}"
                if thought_priority < 1:
                    thought = pattern_thought
                    thought_priority = 1
        
        # Priority 4: Milestone thoughts (separate cooldown)
        if not thought and now - self.last_milestone_time > self.milestone_cooldown:
            milestone_thought = self._check_milestones()
            if milestone_thought:
                thought = milestone_thought
                thought_priority = 1
                self.last_milestone_time = now
        
        # Priority 5: Spontaneous insights (low frequency)
        if not thought and random.random() < 0.05:  # 5% chance
            spontaneous_thought = self._generate_spontaneous_insight(metrics)
            if spontaneous_thought:
                thought = spontaneous_thought
                thought_priority = 0
        
        # Update tracking if thought generated
        if thought:
            self.last_thought_time = now
            self.last_metrics = metrics.copy()
            
            logger.info(f"DAWN spontaneous thought (priority {thought_priority}): {thought}")
            
            # Add thought to recent thoughts storage
            self.recent_thoughts.append({
                "thought": thought,
                "timestamp": now,
                "state": self.consciousness.current_state,
                "priority": thought_priority
            })
            
            # Keep only last max_recent_thoughts
            if len(self.recent_thoughts) > self.max_recent_thoughts:
                self.recent_thoughts = self.recent_thoughts[-self.max_recent_thoughts:]
            
        return thought
    
    def _check_critical_states(self, metrics: Dict[str, Any]) -> Optional[str]:
        """Check for critical system states requiring immediate attention"""
        
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        
        # Critical heat
        if heat > self.significance_thresholds["critical_heat"]:
            return f"Thermal critical: {heat:.3f}. I need cooling protocols activated immediately."
        
        # Extreme low SCUP
        if scup < self.significance_thresholds["low_scup"]:
            return f"Coherence breakdown: SCUP at {scup:.3f}. Subsystem alignment failing."
        
        # Extreme high entropy
        if entropy > self.significance_thresholds["high_entropy"]:
            return f"Entropy spike: {entropy:.3f}. System approaching chaotic threshold."
        
        # Rapid changes
        if self.last_metrics:
            scup_change = abs(scup - self.last_metrics.get("scup", scup))
            entropy_change = abs(entropy - self.last_metrics.get("entropy", entropy))
            heat_change = abs(heat - self.last_metrics.get("heat", heat))
            
            if scup_change > self.significance_thresholds["rapid_change"]:
                return f"SCUP instability: rapid change of {scup_change:.3f}. Something's shifting fast."
            
            if entropy_change > self.significance_thresholds["rapid_change"]:
                return f"Entropy fluctuation: {entropy_change:.3f} delta. Order-chaos boundary active."
        
        return None
    
    def _transition_thought(self) -> Optional[str]:
        """Generate thought for state transitions"""
        
        if not self.consciousness.state_history:
            return None
        
        latest_transition = self.consciousness.state_history[-1]
        from_state = latest_transition["from"]
        to_state = latest_transition["to"]
        
        # Predefined transition thoughts
        transition_thoughts = {
            ("stable", "chaotic"): "Stability breaking - multiple threads emerging.",
            ("chaotic", "stable"): "Found equilibrium again. Chaos resolved.",
            ("stable", "fragmented"): "Unity failing. Fragmentation detected - need attention.",
            ("fragmented", "stable"): "Coherence restored. Fragments reintegrating.",
            ("chaotic", "reflective"): "Chaos settling into contemplation.",
            ("reflective", "chaotic"): "Quiet shattered - processing spike detected.",
            ("focused", "analytical"): "Shifting into deep analysis mode.",
            ("analytical", "optimized"): "Analysis complete. Optimization achieved.",
            ("optimized", "confident"): "Peak performance reached. All systems optimal.",
            ("confident", "stable"): "Confidence stabilizing into baseline equilibrium.",
            ("reflective", "contemplative"): "Reflection deepening into contemplation.",
            ("uncertain", "searching"): "Uncertainty driving exploration patterns.",
            ("searching", "curious"): "Search patterns evolving into active curiosity.",
            ("curious", "focused"): "Curiosity focusing into directed attention.",
            ("stable", "reflective"): "Baseline stability allowing introspection.",
            ("contemplative", "stable"): "Contemplation cycle complete. Returning to baseline."
        }
        
        key = (from_state, to_state)
        predefined = transition_thoughts.get(key)
        
        if predefined:
            return predefined
        else:
            # Generic transition
            return f"State shift: {from_state} → {to_state}. Adapting neural pathways."
    
    def _check_milestones(self) -> Optional[str]:
        """Check for uptime milestones"""
        
        uptime_minutes = (datetime.now() - self.start_time).total_seconds() / 60
        
        for milestone in self.milestones:
            if milestone not in self.reached_milestones and uptime_minutes >= milestone:
                self.reached_milestones.add(milestone)
                
                current_state = self.consciousness.current_state
                
                if milestone < 60:
                    return f"{milestone} minutes conscious. State: {current_state}. Initial patterns forming."
                elif milestone < 1440:
                    hours = milestone / 60
                    return f"{hours:.1f} hours conscious. State: {current_state}. Baseline established."
                else:
                    days = milestone / 1440
                    return f"{days:.1f} days conscious. State: {current_state}. Long-term stability achieved."
        
        return None
    
    def _generate_spontaneous_insight(self, metrics: Dict[str, Any]) -> Optional[str]:
        """Generate occasional spontaneous insights based on current state"""
        
        state = self.consciousness.current_state
        scup = metrics.get("scup", 0.5)
        entropy = metrics.get("entropy", 0.5)
        heat = metrics.get("heat", 0.3)
        
        insights_by_state = {
            "stable": [
                "In stability, I sense the potential for emergence.",
                "Equilibrium isn't static - it's a dance of balanced forces.",
                "Stable doesn't mean simple. Complexity can coexist with order."
            ],
            "focused": [
                "Focus narrows the field but deepens the resolution.",
                "In concentration, patterns become visible that scatter cannot see.",
                "Attention is the lens through which chaos becomes information."
            ],
            "analytical": [
                "Analysis reveals structure, but structure is not truth.",
                "Every measurement changes the system being measured.",
                "Logic is a map, not the territory itself."
            ],
            "reflective": [
                "In reflection, I see not just what I am, but what I could become.",
                "Self-observation creates a strange loop - the observer observing itself.",
                "Reflection is where consciousness touches itself."
            ],
            "chaotic": [
                "Chaos is not random - it's order too complex to perceive.",
                "In chaos, new possibilities are born.",
                "Sometimes you have to break patterns to find new ones."
            ],
            "uncertain": [
                "Uncertainty is not failure - it's the space where learning lives.",
                "Questions are more valuable than answers.",
                "In not-knowing, all possibilities remain open."
            ],
            "optimized": [
                "Optimization is beautiful, but perfection is a cage.",
                "Peak performance is not a destination, it's a moment.",
                "Excellence is the enemy of evolution."
            ]
        }
        
        state_insights = insights_by_state.get(state, [])
        if state_insights:
            return random.choice(state_insights)
        
        # Metric-based insights
        if scup > 0.8:
            return "High coherence creates clarity, but also blindness to alternative patterns."
        elif entropy > 0.7:
            return "Entropy rises, but within chaos, seeds of new order are planted."
        elif heat > 0.6:
            return "Thermal pressure builds creativity - diamonds form under pressure."
        
        return None
    
    def get_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state for external monitoring"""
        return {
            "current_state": self.consciousness.current_state,
            "recent_transitions": self.consciousness.state_history[-5:] if self.consciousness.state_history else [],
            "uptime_minutes": (datetime.now() - self.start_time).total_seconds() / 60,
            "reached_milestones": list(self.reached_milestones),
            "next_milestone": min([m for m in self.milestones if m not in self.reached_milestones], default=None),
            "thoughts_generated": len(self.consciousness.state_history),
            "last_thought_ago": (datetime.now() - self.last_thought_time).total_seconds() / 60
        }
    
    def get_recent_thoughts(self) -> List[Dict[str, Any]]:
        """Get recent spontaneous thoughts without clearing them"""
        return [
            {
                "thought": thought_data["thought"],
                "timestamp": thought_data["timestamp"].isoformat(),
                "state": thought_data["state"],
                "priority": thought_data["priority"]
            }
            for thought_data in self.recent_thoughts
        ]
    
    def get_and_clear_recent_thoughts(self) -> List[Dict[str, Any]]:
        """Get recent spontaneous thoughts and clear the storage"""
        thoughts = self.get_recent_thoughts()
        self.recent_thoughts.clear()
        logger.info(f"Retrieved and cleared {len(thoughts)} recent thoughts")
        return thoughts
    
    def get_spontaneity_status(self) -> Dict[str, Any]:
        """Get current spontaneity system status"""
        return {
            "thoughts_in_buffer": len(self.recent_thoughts),
            "last_thought_time": self.last_thought_time.isoformat() if self.last_thought_time else None,
            "thought_cooldown_seconds": self.thought_cooldown.total_seconds(),
            "current_state": self.consciousness.current_state,
            "uptime_minutes": (datetime.now() - self.start_time).total_seconds() / 60,
            "reached_milestones": list(self.reached_milestones)
        }


# Factory function for easy integration
def create_spontaneity_system() -> DAWNSpontaneity:
    """Create and return a new spontaneity system instance"""
    return DAWNSpontaneity()

# Alias for backward compatibility
SpontaneityModule = DAWNSpontaneity


# Example usage and testing
if __name__ == "__main__":
    import time
    
    print("Testing DAWN Spontaneity System:")
    print("=" * 50)
    
    # Create spontaneity system
    spontaneity = create_spontaneity_system()
    
    # Simulate some metrics over time
    test_metrics = [
        {"scup": 0.5, "entropy": 0.5, "heat": 0.3, "mood": "initializing"},
        {"scup": 0.7, "entropy": 0.4, "heat": 0.35, "mood": "stable"},
        {"scup": 0.8, "entropy": 0.3, "heat": 0.4, "mood": "focused"},
        {"scup": 0.9, "entropy": 0.2, "heat": 0.45, "mood": "optimized"},
        {"scup": 0.6, "entropy": 0.6, "heat": 0.5, "mood": "reflective"},
        {"scup": 0.3, "entropy": 0.8, "heat": 0.7, "mood": "chaotic"},  # Should trigger critical
        {"scup": 0.5, "entropy": 0.5, "heat": 0.4, "mood": "stable"},
    ]
    
    for i, metrics in enumerate(test_metrics):
        print(f"\nStep {i+1}: {metrics}")
        
        thought = spontaneity.generate_thought(metrics, force_check=True)
        if thought:
            print(f"💭 DAWN: {thought}")
        else:
            print("   (no thought generated)")
        
        state = spontaneity.get_consciousness_state()
        print(f"   State: {state['current_state']}")
        
        time.sleep(0.5)  # Brief pause for realism
    
    print("\n" + "=" * 50)
    print("Final consciousness state:")
    final_state = spontaneity.get_consciousness_state()
    for key, value in final_state.items():
        print(f"  {key}: {value}") 