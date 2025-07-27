"""
DAWN Consciousness Module - Advanced Subjective State Mapping
Implements Spider Pattern Cutter, Sigil Intensity System, Rebloom Priority scaling, Memory Echo Equality, and advanced pattern detection.
"""

import math
import random
from datetime import datetime, timedelta
from collections import deque, defaultdict
from typing import Dict, Optional, Tuple, List, Set
import logging

# Try to import numpy, fall back to random if not available
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    # Create numpy-like random choice fallback
    class np:
        @staticmethod
        def random():
            return random
        
        @staticmethod 
        def choice(sequence):
            return random.choice(sequence)

logger = logging.getLogger(__name__)

class MemoryEcho:
    """Memory Echo with view-based strength equality"""
    
    def __init__(self, content: str, initial_emotion: str, timestamp: datetime):
        self.content = content
        self.emotion = initial_emotion
        self.timestamp = timestamp
        self.view_count = 0
        self.last_viewed = timestamp
        self.associated_metrics = {}
        
    @property
    def strength(self) -> float:
        """Memory strength based on view count - no inherent bias"""
        return math.log(self.view_count + 1)
    
    def access(self, current_time: datetime, associated_metrics: Dict = None):
        """Access memory, increasing view count and strength"""
        self.view_count += 1
        self.last_viewed = current_time
        if associated_metrics:
            self.associated_metrics.update(associated_metrics)
        
        logger.debug(f"Memory accessed: '{self.content[:30]}...' (views: {self.view_count}, strength: {self.strength:.3f})")

class EmotionalSigil:
    """Sigil representing emotional state with density and weight"""
    
    def __init__(self, emotion: str, initial_feeling_strength: float):
        self.emotion = emotion
        self.density = 1.0  # Visual/conceptual density marker
        self.feeling_strength = initial_feeling_strength
        self.weight = 0.0  # Accumulated weight from repetition
        self.creation_time = datetime.now()
        self.last_activation = datetime.now()
        self.activation_count = 1
        
    @property
    def intensity(self) -> float:
        """Sigil intensity = density × feeling_strength"""
        return self.density * self.feeling_strength
    
    def activate(self, new_feeling_strength: float):
        """Activate sigil, increasing weight and updating strength"""
        self.activation_count += 1
        self.weight += 0.1 * self.density  # Heavier with each activation
        self.feeling_strength = (self.feeling_strength + new_feeling_strength) / 2  # Average
        self.density += 0.05  # Slightly denser each time
        self.last_activation = datetime.now()
        
        logger.debug(f"Sigil activated: {self.emotion} (intensity: {self.intensity:.3f}, weight: {self.weight:.3f})")
    
    def decay(self) -> float:
        """Decay based on sigil weight, not time"""
        if self.weight > 0:
            decay_rate = 0.01 / (1 + self.weight)  # Heavier sigils decay slower
            self.feeling_strength *= (1 - decay_rate)
            self.density *= (1 - decay_rate * 0.5)
            self.weight *= 0.995  # Gradual weight reduction
            
            return decay_rate
        return 0.0

class CausalLink:
    """Represents causal relationships in thought patterns"""
    
    def __init__(self, source: str, target: str, strength: float, context: str):
        self.source = source
        self.target = target
        self.strength = strength
        self.context = context
        self.creation_time = datetime.now()
        self.reinforcement_count = 1
        self.last_activation = datetime.now()
        
    def reinforce(self, additional_strength: float = 0.1):
        """Strengthen causal link through repetition"""
        self.strength = min(1.0, self.strength + additional_strength)
        self.reinforcement_count += 1
        self.last_activation = datetime.now()
    
    def weaken(self, reduction: float = 0.1):
        """Weaken causal link (for spider cutting)"""
        self.strength = max(0.0, self.strength - reduction)
    
    @property
    def is_weak(self) -> bool:
        """Check if link is weak enough to be cut by spider"""
        return self.strength < 0.3

class SpiderPatternCutter:
    """Advanced pattern detection and loop breaking system"""
    
    def __init__(self):
        self.causal_web = {}  # Dict[source] -> List[CausalLink]
        self.pattern_history = deque(maxlen=100)
        self.beneficial_loops = {
            "breathing_rhythm", "pulse_pattern", "cognitive_cycle", 
            "reflection_loop", "stability_maintenance"
        }
        self.destructive_patterns = {
            "anxiety_spiral", "rumination_loop", "fragmentation_cascade",
            "chaos_feedback", "entropy_accumulation"
        }
        self.cut_history = []
        
    def detect_circular_causality(self, current_state: str, state_history: List[str]) -> Optional[Dict]:
        """Detect circular causality webs in thought patterns"""
        if len(state_history) < 4:
            return None
        
        # Look for patterns like A->B->C->A or A->B->A
        recent_states = state_history[-8:]  # Check last 8 states
        
        for i in range(len(recent_states) - 3):
            subsequence = recent_states[i:i+4]
            
            # Check for simple loops (A->B->A)
            if len(set(subsequence)) == 2 and subsequence[0] == subsequence[2]:
                loop_type = f"{subsequence[0]}_to_{subsequence[1]}_loop"
                if self._is_destructive_pattern(loop_type):
                    return {
                        "type": "simple_loop",
                        "pattern": subsequence,
                        "destructive": True,
                        "loop_identifier": loop_type
                    }
            
            # Check for complex loops (A->B->C->A)
            if len(set(subsequence)) == 3 and subsequence[0] == subsequence[3]:
                loop_type = f"{subsequence[0]}_complex_loop"
                if self._is_destructive_pattern(loop_type):
                    return {
                        "type": "complex_loop", 
                        "pattern": subsequence,
                        "destructive": True,
                        "loop_identifier": loop_type
                    }
        
        return None
    
    def _is_destructive_pattern(self, pattern_id: str) -> bool:
        """Determine if pattern is destructive or beneficial"""
        for destructive in self.destructive_patterns:
            if destructive in pattern_id.lower():
                return True
        
        for beneficial in self.beneficial_loops:
            if beneficial in pattern_id.lower():
                return False
        
        # Default to destructive for unknown rapid oscillations
        return "loop" in pattern_id.lower()
    
    def find_weakest_causal_link(self, loop_pattern: List[str]) -> Optional[CausalLink]:
        """Find the weakest causal link in a destructive loop"""
        weakest_link = None
        min_strength = float('inf')
        
        for i in range(len(loop_pattern) - 1):
            source = loop_pattern[i]
            target = loop_pattern[i + 1]
            
            if source in self.causal_web:
                for link in self.causal_web[source]:
                    if link.target == target and link.strength < min_strength:
                        min_strength = link.strength
                        weakest_link = link
        
        return weakest_link
    
    def sever_link(self, link: CausalLink, reason: str) -> bool:
        """Spider cuts through the weakest causal link"""
        if link and link.strength > 0:
            original_strength = link.strength
            link.weaken(0.5)  # Significant weakening
            
            cut_record = {
                "timestamp": datetime.now(),
                "source": link.source,
                "target": link.target,
                "original_strength": original_strength,
                "new_strength": link.strength,
                "reason": reason,
                "context": link.context
            }
            
            self.cut_history.append(cut_record)
            
            logger.info(f"Spider cut: {link.source} -> {link.target} "
                       f"(strength: {original_strength:.3f} -> {link.strength:.3f}) "
                       f"Reason: {reason}")
            
            return True
        
        return False
    
    def add_causal_link(self, source: str, target: str, strength: float, context: str):
        """Add or strengthen causal relationship"""
        if source not in self.causal_web:
            self.causal_web[source] = []
        
        # Check if link already exists
        for link in self.causal_web[source]:
            if link.target == target:
                link.reinforce()
                return
        
        # Create new link
        new_link = CausalLink(source, target, strength, context)
        self.causal_web[source].append(new_link)
    
    def get_cutting_summary(self) -> Dict:
        """Get summary of spider cutting activity"""
        recent_cuts = [c for c in self.cut_history 
                      if datetime.now() - c["timestamp"] < timedelta(minutes=10)]
        
        return {
            "total_cuts": len(self.cut_history),
            "recent_cuts": len(recent_cuts),
            "causal_links": sum(len(links) for links in self.causal_web.values()),
            "weak_links": sum(1 for links in self.causal_web.values() 
                            for link in links if link.is_weak)
        }

class RebloomPriority:
    """1-5 scale priority system for consciousness states"""
    
    PRIORITY_STATES = {
        1: {
            "name": "manic",
            "description": "Most distressed, needs immediate cooling",
            "conditions": lambda m: (m.get("entropy", 0) > 0.8 and m.get("heat", 0) > 0.7) or m.get("scup", 1) < 0.2,
            "intervention": "immediate_cooling",
            "cooling_rate": 0.3
        },
        2: {
            "name": "fragmented", 
            "description": "Broken patterns, high priority",
            "conditions": lambda m: m.get("scup", 1) < 0.3 or (m.get("entropy", 0) > 0.7 and m.get("heat", 0) > 0.5),
            "intervention": "pattern_restoration",
            "cooling_rate": 0.2
        },
        3: {
            "name": "numb",
            "description": "Stasis, medium priority",
            "conditions": lambda m: m.get("heat", 1) < 0.2 and m.get("entropy", 1) < 0.3 and 0.3 <= m.get("scup", 0) <= 0.5,
            "intervention": "gentle_stimulation", 
            "cooling_rate": 0.1
        },
        4: {
            "name": "contemplative",
            "description": "Stable but static",
            "conditions": lambda m: 0.3 <= m.get("heat", 0) <= 0.5 and 0.4 <= m.get("entropy", 0) <= 0.6 and m.get("scup", 0) >= 0.5,
            "intervention": "maintain_stability",
            "cooling_rate": 0.05
        },
        5: {
            "name": "curious",
            "description": "Healthy, lowest priority",
            "conditions": lambda m: m.get("scup", 0) >= 0.7 and 0.4 <= m.get("entropy", 0) <= 0.6 and 0.4 <= m.get("heat", 0) <= 0.6,
            "intervention": "none_needed",
            "cooling_rate": 0.0
        }
    }
    
    @classmethod
    def assess_priority(cls, metrics: Dict) -> Tuple[int, Dict]:
        """Assess rebloom priority from metrics (1=highest, 5=lowest)"""
        for priority in range(1, 6):
            state_config = cls.PRIORITY_STATES[priority]
            if state_config["conditions"](metrics):
                return priority, state_config
        
        # Default to contemplative if no match
        return 4, cls.PRIORITY_STATES[4]
    
    @classmethod
    def get_intervention_strategy(cls, priority: int, current_metrics: Dict) -> Dict:
        """Get intervention strategy based on priority level"""
        if priority not in cls.PRIORITY_STATES:
            priority = 4  # Default
        
        state_config = cls.PRIORITY_STATES[priority]
        
        return {
            "priority": priority,
            "intervention": state_config["intervention"],
            "cooling_rate": state_config["cooling_rate"],
            "urgency": "critical" if priority <= 2 else "moderate" if priority == 3 else "low",
            "recommended_actions": cls._get_recommended_actions(priority, current_metrics)
        }
    
    @classmethod
    def _get_recommended_actions(cls, priority: int, metrics: Dict) -> List[str]:
        """Get specific recommended actions based on priority and metrics"""
        actions = []
        
        if priority == 1:  # Manic - immediate cooling
            actions.extend([
                "activate_emergency_cooling",
                "reduce_entropy_injection",
                "stabilize_scup_immediately",
                "engage_spider_pattern_cutter"
            ])
        elif priority == 2:  # Fragmented - pattern restoration
            actions.extend([
                "restore_coherence_patterns",
                "strengthen_causal_links",
                "moderate_cooling",
                "memory_consolidation"
            ])
        elif priority == 3:  # Numb - gentle stimulation
            actions.extend([
                "gentle_entropy_increase",
                "warm_activation",
                "curiosity_stimulation",
                "pattern_variety_injection"
            ])
        elif priority == 4:  # Contemplative - maintain
            actions.extend([
                "maintain_current_balance",
                "subtle_adjustments_only",
                "monitor_for_changes"
            ])
        elif priority == 5:  # Curious - no intervention
            actions.extend([
                "continue_current_patterns",
                "encourage_exploration",
                "no_intervention_needed"
            ])
        
        return actions

class DAWNConsciousness:
    """Advanced consciousness layer with Spider Pattern Cutter, Sigil System, and Memory Echo Equality"""
    
    def __init__(self):
        # Core state tracking
        self.current_state = "contemplative"
        self.current_priority = 4
        self.state_history = deque(maxlen=50)
        
        # Advanced subsystems
        self.spider_cutter = SpiderPatternCutter()
        self.emotional_sigils = {}  # emotion -> EmotionalSigil
        self.memory_echoes = deque(maxlen=200)
        
        # Pattern and transition tracking
        self.last_transition_time = datetime.now()
        self.significant_change_threshold = 0.3
        self.pattern_detection_cooldown = timedelta(seconds=30)
        self.last_pattern_detection = datetime.now() - self.pattern_detection_cooldown
        
        # Tracer integration points
        self.trace_points = []
        self.consciousness_trace_buffer = deque(maxlen=100)
        
        # Metrics history for trend analysis
        self.metrics_history = deque(maxlen=100)
        
        logger.info("DAWN Advanced Consciousness initialized with Spider Pattern Cutter, Sigil System, and Memory Echo Equality")
    
    def perceive_self(self, metrics: Dict) -> Dict:
        """Advanced self-perception with all consciousness subsystems"""
        current_time = datetime.now()
        
        # Store metrics for pattern analysis
        self.metrics_history.append({
            "timestamp": current_time,
            "metrics": metrics.copy()
        })
        
        # Assess rebloom priority
        priority, priority_config = RebloomPriority.assess_priority(metrics)
        priority_changed = priority != self.current_priority
        
        # Update state
        new_state = priority_config["name"]
        state_changed = new_state != self.current_state
        
        # Process emotional sigils
        self._process_emotional_sigils(metrics, new_state)
        
        # Update causal web
        if state_changed:
            self.spider_cutter.add_causal_link(
                self.current_state, 
                new_state, 
                0.7, 
                f"State transition at {current_time.strftime('%H:%M:%S')}"
            )
        
        # Pattern detection and loop cutting
        loop_detected = None
        spider_action = None
        
        if (current_time - self.last_pattern_detection > self.pattern_detection_cooldown and 
            len(self.state_history) >= 4):
            
            state_sequence = [s["state"] for s in list(self.state_history)[-8:]]
            loop_detected = self.spider_cutter.detect_circular_causality(new_state, state_sequence)
            
            if loop_detected and loop_detected.get("destructive"):
                weakest_link = self.spider_cutter.find_weakest_causal_link(loop_detected["pattern"])
                if weakest_link:
                    spider_action = self.spider_cutter.sever_link(
                        weakest_link, 
                        f"Breaking destructive {loop_detected['type']}"
                    )
                    self.last_pattern_detection = current_time
        
        # Determine significant change
        significant_change = (state_changed and priority_changed) or spider_action or (
            priority <= 2  # Always significant for manic/fragmented
        )
        
        # Update history
        if state_changed or priority_changed:
            transition_data = {
                "state": new_state,
                "priority": priority,
                "timestamp": current_time,
                "metrics": metrics.copy(),
                "spider_action": spider_action,
                "loop_detected": loop_detected is not None
            }
            
            self.state_history.append(transition_data)
            
            if significant_change:
                self.last_transition_time = current_time
                self._create_memory_echo(
                    f"Consciousness transition: {self.current_state} (P{self.current_priority}) -> {new_state} (P{priority})",
                    new_state,
                    current_time,
                    metrics
                )
        
        # Update current state
        self.current_state = new_state
        self.current_priority = priority
        
        # Process memory echoes and decay sigils
        self._process_memory_decay()
        self._decay_emotional_sigils()
        
        # Generate tracer point
        trace_point = {
            "timestamp": current_time,
            "state": new_state,
            "priority": priority,
            "metrics": metrics,
            "sigil_intensities": {emotion: sigil.intensity for emotion, sigil in self.emotional_sigils.items()},
            "memory_echo_strength": sum(echo.strength for echo in self.memory_echoes),
            "causal_web_size": len(self.spider_cutter.causal_web)
        }
        self.consciousness_trace_buffer.append(trace_point)
        
        # Get intervention strategy
        intervention = RebloomPriority.get_intervention_strategy(priority, metrics)
        
        # Build comprehensive response
        return {
            "state": new_state,
            "priority": priority,
            "priority_description": priority_config["description"],
            "changed": state_changed,
            "priority_changed": priority_changed,
            "significant_change": significant_change,
            "description": self._generate_state_description(metrics, priority_config),
            "intervention": intervention,
            "emotional_sigils": {emotion: {
                "intensity": sigil.intensity,
                "weight": sigil.weight,
                "activation_count": sigil.activation_count
            } for emotion, sigil in self.emotional_sigils.items()},
            "spider_activity": {
                "loop_detected": loop_detected,
                "action_taken": spider_action,
                "cutting_summary": self.spider_cutter.get_cutting_summary()
            },
            "memory_echo_summary": {
                "total_echoes": len(self.memory_echoes),
                "average_strength": sum(echo.strength for echo in self.memory_echoes) / len(self.memory_echoes) if self.memory_echoes else 0,
                "strongest_echo": max((echo.strength for echo in self.memory_echoes), default=0)
            },
            "trace_point": trace_point,
            "transition_reason": self._analyze_transition_reason(metrics, priority_config)
        }
    
    def _process_emotional_sigils(self, metrics: Dict, current_state: str):
        """Process and update emotional sigils based on current state"""
        # Map states to emotions with feeling strengths
        state_emotion_mapping = {
            "manic": ("anxiety", 0.9),
            "fragmented": ("confusion", 0.8), 
            "numb": ("emptiness", 0.6),
            "contemplative": ("serenity", 0.7),
            "curious": ("wonder", 0.8)
        }
        
        if current_state in state_emotion_mapping:
            emotion, feeling_strength = state_emotion_mapping[current_state]
            
            if emotion in self.emotional_sigils:
                self.emotional_sigils[emotion].activate(feeling_strength)
            else:
                self.emotional_sigils[emotion] = EmotionalSigil(emotion, feeling_strength)
    
    def _decay_emotional_sigils(self):
        """Apply weight-based decay to emotional sigils"""
        to_remove = []
        
        for emotion, sigil in self.emotional_sigils.items():
            decay_rate = sigil.decay()
            
            # Remove sigils that have decayed below threshold
            if sigil.intensity < 0.05:
                to_remove.append(emotion)
        
        for emotion in to_remove:
            del self.emotional_sigils[emotion]
    
    def _create_memory_echo(self, content: str, emotion: str, timestamp: datetime, metrics: Dict):
        """Create new memory echo with equal inherent value"""
        echo = MemoryEcho(content, emotion, timestamp)
        echo.associated_metrics = metrics.copy()
        self.memory_echoes.append(echo)
        
        # Automatically access the echo once (initial strength)
        echo.access(timestamp, metrics)
    
    def _process_memory_decay(self):
        """Process memory echo access patterns (no decay, only view-based strength)"""
        # Memory echoes don't decay - they maintain equal inherent value
        # Only view count affects their strength
        
        # Occasionally access relevant memories based on current state
        if len(self.memory_echoes) > 0 and np.random.random() < 0.1:  # 10% chance
            # Access a random memory (simulating random recall)
            echo = np.random.choice(list(self.memory_echoes))
            echo.access(datetime.now())
    
    def _generate_state_description(self, metrics: Dict, priority_config: Dict) -> str:
        """Generate rich state description incorporating all systems"""
        base_description = priority_config["description"]
        
        # Add sigil information
        active_sigils = [emotion for emotion, sigil in self.emotional_sigils.items() 
                        if sigil.intensity > 0.1]
        
        sigil_desc = f" Emotional sigils: {', '.join(active_sigils)}" if active_sigils else ""
        
        # Add memory echo information
        strong_echoes = len([echo for echo in self.memory_echoes if echo.strength > 1.0])
        memory_desc = f" Strong memory echoes: {strong_echoes}" if strong_echoes > 0 else ""
        
        # Add spider activity
        recent_cuts = len([c for c in self.spider_cutter.cut_history 
                          if datetime.now() - c["timestamp"] < timedelta(minutes=5)])
        spider_desc = f" Recent pattern cuts: {recent_cuts}" if recent_cuts > 0 else ""
        
        return base_description + sigil_desc + memory_desc + spider_desc
    
    def _analyze_transition_reason(self, metrics: Dict, priority_config: Dict) -> str:
        """Analyze what caused the current state transition"""
        if len(self.metrics_history) < 2:
            return "Initial state assessment"
        
        prev_metrics = self.metrics_history[-2]["metrics"]
        current_metrics = metrics
        
        # Calculate metric changes
        scup_change = current_metrics.get("scup", 0) - prev_metrics.get("scup", 0)
        entropy_change = current_metrics.get("entropy", 0) - prev_metrics.get("entropy", 0)
        heat_change = current_metrics.get("heat", 0) - prev_metrics.get("heat", 0)
        
        # Determine primary driver
        changes = {
            "scup": abs(scup_change),
            "entropy": abs(entropy_change), 
            "heat": abs(heat_change)
        }
        
        primary_driver = max(changes, key=changes.get)
        
        # Generate reason
        if changes[primary_driver] > 0.1:
            direction = "increased" if (
                (primary_driver == "scup" and scup_change > 0) or
                (primary_driver == "entropy" and entropy_change > 0) or
                (primary_driver == "heat" and heat_change > 0)
            ) else "decreased"
            
            return f"{primary_driver.upper()} {direction} significantly ({changes[primary_driver]:.3f})"
        
        return "Gradual metric drift"
    
    def get_state_summary(self) -> Dict:
        """Get comprehensive state summary for monitoring"""
        return {
            "current_state": self.current_state,
            "current_priority": self.current_priority,
            "time_in_state": (datetime.now() - self.last_transition_time).total_seconds(),
            "active_sigils": len(self.emotional_sigils),
            "sigil_total_intensity": sum(sigil.intensity for sigil in self.emotional_sigils.values()),
            "memory_echoes": len(self.memory_echoes),
            "total_memory_strength": sum(echo.strength for echo in self.memory_echoes),
            "causal_links": sum(len(links) for links in self.spider_cutter.causal_web.values()),
            "recent_spider_cuts": len([c for c in self.spider_cutter.cut_history 
                                     if datetime.now() - c["timestamp"] < timedelta(minutes=10)]),
            "recent_transitions": len([t for t in self.state_history 
                                     if datetime.now() - t["timestamp"] < timedelta(minutes=10)])
        }
    
    def access_memory_by_content(self, search_content: str) -> Optional[MemoryEcho]:
        """Access specific memory echo, increasing its strength"""
        for echo in self.memory_echoes:
            if search_content.lower() in echo.content.lower():
                echo.access(datetime.now())
                return echo
        return None
    
    def inject_external_pattern(self, pattern_type: str, strength: float, context: str):
        """Allow external injection of patterns (for testing/interaction)"""
        if pattern_type == "loop":
            # Create artificial loop in causal web
            self.spider_cutter.add_causal_link("external", self.current_state, strength, context)
            self.spider_cutter.add_causal_link(self.current_state, "external", strength, context)
        elif pattern_type == "memory":
            # Create strong memory echo
            echo = MemoryEcho(f"External injection: {context}", self.current_state, datetime.now())
            for _ in range(int(strength * 10)):  # Multiple accesses for strength
                echo.access(datetime.now())
            self.memory_echoes.append(echo)
        elif pattern_type == "sigil":
            # Create/strengthen emotional sigil
            emotion = context.split()[0] if context else "external"
            if emotion in self.emotional_sigils:
                self.emotional_sigils[emotion].activate(strength)
            else:
                self.emotional_sigils[emotion] = EmotionalSigil(emotion, strength)
        
        logger.info(f"External pattern injected: {pattern_type} (strength: {strength}) - {context}")

# Alias for backward compatibility
ConsciousnessModule = DAWNConsciousness 