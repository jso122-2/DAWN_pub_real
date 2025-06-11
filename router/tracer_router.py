"""
Tracer Router with Decision Spine Logic
Implements structured decision-making framework for tracers based on pressure and semantic relationships.
"""

import json
import os
from typing import Dict, List, Tuple, Optional, Set, Any
from collections import deque, defaultdict
import numpy as np
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class TracerPayload:
    """Structured payload for tracer routing with signal and context."""
    
    signal: str
    origin: str
    urgency: float
    mood_context: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate and normalize payload data."""
        # Ensure urgency is between 0 and 1
        self.urgency = max(0.0, min(1.0, self.urgency))
        
        # Normalize signal
        self.signal = self.signal.strip().lower()
        
        # Ensure origin is a valid module name
        self.origin = self.origin.replace(" ", "_").lower()
        
        # Set default mood if not provided
        if self.mood_context is None:
            self.mood_context = "neutral"
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert payload to dictionary format."""
        return {
            "signal": self.signal,
            "origin": self.origin,
            "urgency": self.urgency,
            "mood_context": self.mood_context,
            "metadata": self.metadata
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TracerPayload':
        """Create payload from dictionary data."""
        return cls(
            signal=data["signal"],
            origin=data["origin"],
            urgency=data["urgency"],
            mood_context=data.get("mood_context"),
            metadata=data.get("metadata", {})
        )
        
    def get_signal_type(self) -> str:
        """Determine the type of signal for routing."""
        signal_lower = self.signal.lower()
        
        if "entropy" in signal_lower or "risk" in signal_lower:
            return "entropy_signal"
        elif "bloom" in signal_lower or "fractal" in signal_lower:
            return "bloom_signal"
        elif "sigil" in signal_lower or "pattern" in signal_lower:
            return "sigil_signal"
        elif "claude" in signal_lower:
            return "claude_signal"
        else:
            return "general_signal"
            
    def get_priority_boost(self) -> float:
        """Calculate priority boost based on signal content and urgency."""
        boost = 0.0
        
        # Base boost from urgency
        boost += self.urgency * 0.1
        
        # Additional boost for specific signal types
        signal_type = self.get_signal_type()
        if signal_type == "entropy_signal" and self.urgency > 0.7:
            boost += 0.2
        elif signal_type == "bloom_signal" and "critical" in self.signal:
            boost += 0.15
        elif signal_type == "sigil_signal" and "anomaly" in self.signal:
            boost += 0.15
            
        return min(0.3, boost)  # Cap total boost at 0.3

class ClaudeSignal:
    """Helper class for managing Claude signal priorities."""
    
    PRIORITY_TERMS_FILE = "priority_terms.txt"
    CLAUDE_TRACE_FILE = "logs/claude_trace.json"
    PRIORITY_BOOST = 0.05
    
    @classmethod
    def get_priority_terms(cls) -> List[str]:
        """Load priority terms from file or return defaults."""
        try:
            if os.path.exists(cls.PRIORITY_TERMS_FILE):
                with open(cls.PRIORITY_TERMS_FILE, 'r') as f:
                    return [line.strip() for line in f if line.strip()]
            else:
                # Create default priority terms
                default_terms = [
                    "schema drift",
                    "operator offline",
                    "fail-safe trigger",
                    "critical path",
                    "system stress",
                    "anomaly detected"
                ]
                with open(cls.PRIORITY_TERMS_FILE, 'w') as f:
                    f.write('\n'.join(default_terms))
                return default_terms
        except Exception as e:
            print(f"[ClaudeSignal] Error loading priority terms: {e}")
            return []
            
    @classmethod
    def get_recent_signals(cls, max_age_seconds: int = 300) -> List[Dict]:
        """Get recent signals from Claude trace."""
        try:
            if not os.path.exists(cls.CLAUDE_TRACE_FILE):
                return []
                
            with open(cls.CLAUDE_TRACE_FILE, 'r') as f:
                signals = json.load(f)
                
            # Filter for recent signals
            current_time = datetime.now()
            recent_signals = []
            
            for signal in signals:
                try:
                    signal_time = datetime.fromisoformat(signal.get('timestamp', ''))
                    age = (current_time - signal_time).total_seconds()
                    if age <= max_age_seconds:
                        recent_signals.append(signal)
                except (ValueError, TypeError):
                    continue
                    
            return recent_signals
        except Exception as e:
            print(f"[ClaudeSignal] Error loading recent signals: {e}")
            return []
            
    @classmethod
    def has_priority_match(cls, signal_text: str) -> bool:
        """Check if signal text matches any priority terms."""
        priority_terms = cls.get_priority_terms()
        return any(term.lower() in signal_text.lower() for term in priority_terms)

class TracerTypeRegistry:
    """Registry for tracer type configurations and behaviors."""
    
    def __init__(self):
        self.registry = {
            "OwlTracer": {
                "urgency_modifier": 1.2,  # Higher urgency for entropy risks
                "preferred_targets": {"entropy_monitor", "risk_analyzer", "whisper_log"},
                "avoided_targets": set(),
                "special_logic": self._owl_tracer_logic
            },
            "BloomTracer": {
                "urgency_modifier": 1.0,
                "preferred_targets": {"bloom_engine", "memory_weaver", "fractal_decoder"},
                "avoided_targets": {"risk_analyzer", "entropy_monitor"},
                "special_logic": self._bloom_tracer_logic
            },
            "SigilTracer": {
                "urgency_modifier": 0.8,  # More cautious with high pressure
                "preferred_targets": {"sigil_generator", "pattern_matcher"},
                "avoided_targets": {"rebloom_zone", "entropy_monitor"},
                "special_logic": self._sigil_tracer_logic
            }
        }
        
    def get_tracer_config(self, tracer_type: str) -> Dict:
        """Get configuration for a specific tracer type."""
        return self.registry.get(tracer_type, {
            "urgency_modifier": 1.0,
            "preferred_targets": set(),
            "avoided_targets": set(),
            "special_logic": None
        })
        
    def _owl_tracer_logic(self, route_data: Dict) -> float:
        """Special routing logic for OwlTracer."""
        # Boost score if target is in preferred targets
        if route_data["target"] in self.registry["OwlTracer"]["preferred_targets"]:
            return 1.2
            
        # Check for high entropy risk
        if route_data.get("entropy", 0.0) > 0.7:
            return 1.3  # Significant boost for high entropy
            
        return 1.0
        
    def _bloom_tracer_logic(self, route_data: Dict) -> float:
        """Special routing logic for BloomTracer."""
        # Boost score for bloom-related targets
        if route_data["target"] in self.registry["BloomTracer"]["preferred_targets"]:
            return 1.2
            
        # Reduce score for risk-related targets
        if route_data["target"] in self.registry["BloomTracer"]["avoided_targets"]:
            return 0.7
            
        return 1.0
        
    def _sigil_tracer_logic(self, route_data: Dict) -> float:
        """Special routing logic for SigilTracer."""
        # Avoid rebloom zones if pressure is high
        if (route_data["target"] in self.registry["SigilTracer"]["avoided_targets"] and 
            route_data.get("pressure", 0.0) > 0.6):
            return 0.0  # Block route
            
        # Boost score for sigil-related targets
        if route_data["target"] in self.registry["SigilTracer"]["preferred_targets"]:
            return 1.1
            
        return 1.0

class TracerAttentionManager:
    """Manages attention budgets for tracers."""
    
    def __init__(self):
        self.attention_levels: Dict[str, float] = defaultdict(lambda: 1.0)
        self.last_replenish: Dict[str, datetime] = defaultdict(datetime.now)
        self.replenish_rate = 0.05  # Attention points per tick
        self.min_attention = 0.1    # Minimum attention to process requests
        self.max_attention = 1.0    # Maximum attention level
        
    def get_attention(self, tracer_id: str) -> float:
        """Get current attention level for a tracer."""
        self._replenish_attention(tracer_id)
        return self.attention_levels[tracer_id]
        
    def _replenish_attention(self, tracer_id: str) -> None:
        """Replenish attention based on time elapsed."""
        now = datetime.now()
        last = self.last_replenish[tracer_id]
        ticks_elapsed = (now - last).total_seconds() / 5.0  # Assuming 5-second ticks
        
        if ticks_elapsed > 0:
            replenish_amount = min(
                self.replenish_rate * ticks_elapsed,
                self.max_attention - self.attention_levels[tracer_id]
            )
            self.attention_levels[tracer_id] += replenish_amount
            self.last_replenish[tracer_id] = now
            
    def consume_attention(self, tracer_id: str, route_score: float) -> bool:
        """
        Consume attention for a route.
        
        Args:
            tracer_id: ID of the tracer
            route_score: Score of the route being taken
            
        Returns:
            bool: True if enough attention available, False otherwise
        """
        self._replenish_attention(tracer_id)
        
        # Calculate attention cost
        attention_cost = route_score / 10.0
        
        # Check if enough attention available
        if self.attention_levels[tracer_id] < attention_cost:
            print(f"[TracerAttention] {tracer_id} has insufficient attention: "
                  f"{self.attention_levels[tracer_id]:.2f} < {attention_cost:.2f}")
            return False
            
        # Consume attention
        self.attention_levels[tracer_id] -= attention_cost
        print(f"[TracerAttention] {tracer_id} consumed {attention_cost:.2f} attention, "
              f"remaining: {self.attention_levels[tracer_id]:.2f}")
        return True
        
    def can_process_request(self, tracer_id: str) -> bool:
        """Check if tracer has enough attention to process a request."""
        return self.get_attention(tracer_id) >= self.min_attention
        
    def get_attention_status(self, tracer_id: str) -> Dict[str, float]:
        """Get detailed attention status for a tracer."""
        return {
            "current_attention": self.attention_levels[tracer_id],
            "replenish_rate": self.replenish_rate,
            "min_attention": self.min_attention,
            "max_attention": self.max_attention
        }

class TracerRouter:
    """Core router implementing Decision Spine Logic for tracers."""
    
    def __init__(self, semantic_field=None, agreement_matrix=None, log_file: str = "tracer_paths.json"):
        # Decision thresholds
        self.pressure_threshold = 0.7
        self.trust_threshold = 0.6
        self.semantic_threshold = 0.5
        self.hold_timeout = 300  # 5 minutes
        
        # State tracking
        self.last_decision = None
        self.hold_start_time = None
        self.pressure_history = deque(maxlen=100)
        self.trust_history = deque(maxlen=100)
        self.route_history = deque(maxlen=50)
        self.current_tick = 0
        
        # Dependencies
        self.semantic_field = semantic_field
        self.agreement_matrix = agreement_matrix
        
        # Initialize tracer type registry
        self.tracer_registry = TracerTypeRegistry()
        
        # Initialize attention manager
        self.attention_manager = TracerAttentionManager()
        
        # Logging
        self.log_file = log_file
        self.path_log = []
        self.load_path_log()
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Pressure sources
        self.pressure_sources = {
            'pulse': self._get_pulse_pressure,
            'bloom': self._get_bloom_entropy,
            'claude': self._get_claude_signal
        }
        
        # Initialize route registry
        self.route_registry = {}
        
        # Initialize memory trail log
        self.memory_trail_file = "logs/tracer_memory.json"
        self._init_memory_trail()
        
        # Initialize Claude signal handler
        self.claude_signal = ClaudeSignal()
        
    def _init_memory_trail(self) -> None:
        """Initialize memory trail log file if it doesn't exist."""
        if not os.path.exists(self.memory_trail_file):
            with open(self.memory_trail_file, 'w') as f:
                json.dump([], f)
                
    def log_memory_trail(self, source: str, target: str, path: List[str], 
                        score: float, entropy: float, signal: str, 
                        mood_context: str) -> None:
        """
        Log a memory trail entry for a completed route.
        
        Args:
            source: Source component
            target: Target component
            path: List of components in the path
            score: Route score
            entropy: Entropy at start of route
            signal: Signal type (e.g., 'rebloom risk')
            mood_context: Current mood context
        """
        # Generate tracer ID
        tracer_id = f"OwlTracer-{self.current_tick:03d}"
        
        # Create memory trail entry
        memory_entry = {
            "tick": self.current_tick,
            "tracer": tracer_id,
            "source": source,
            "target": target,
            "path": path,
            "score": score,
            "entropy_at_start": entropy,
            "signal": signal,
            "mood_context": mood_context
        }
        
        # Load existing memory trail
        try:
            with open(self.memory_trail_file, 'r') as f:
                memory_trail = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            memory_trail = []
            
        # Append new entry
        memory_trail.append(memory_entry)
        
        # Write updated memory trail
        with open(self.memory_trail_file, 'w') as f:
            json.dump(memory_trail, f, indent=2)
            
        print(f"[TracerRouter] Logged memory trail for {tracer_id}")
        
    def load_path_log(self) -> None:
        """Load path log from file."""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    self.path_log = json.load(f)
                print(f"[TracerRouter] Loaded {len(self.path_log)} path logs")
            else:
                print("[TracerRouter] No existing path log found, starting fresh")
                self.path_log = []
        except Exception as e:
            print(f"[TracerRouter] Error loading path log: {e}")
            self.path_log = []

    def save_path_log(self) -> None:
        """Save path log to file."""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.path_log, f, indent=2)
            print(f"[TracerRouter] Saved {len(self.path_log)} path logs")
        except Exception as e:
            print(f"[TracerRouter] Error saving path log: {e}")

    def log_path(self, source: str, target: str, path: List[str], 
                confidence: float, semantic_distance: float) -> None:
        """Log a tracer path."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'target': target,
            'path': path,
            'confidence': confidence,
            'semantic_distance': semantic_distance
        }
        self.path_log.append(log_entry)
        self.save_path_log()

    def log_route_trace(self, source: str, target: str, path: List[str], 
                       score: float, semantic_distance: float) -> None:
        """Record route decision in logs/tracer_path_trace.json."""
        trace_entry = {
            "tick": self.current_tick,
            "source": source,
            "target": target,
            "path": path,
            "score": score,
            "semantic_distance": semantic_distance
        }
        
        trace_file = "logs/tracer_path_trace.json"
        
        # Load existing traces if file exists
        traces = []
        if os.path.exists(trace_file):
            try:
                with open(trace_file, 'r') as f:
                    traces = json.load(f)
            except json.JSONDecodeError:
                traces = []
        
        # Append new trace
        traces.append(trace_entry)
        
        # Write updated traces
        with open(trace_file, 'w') as f:
            json.dump(traces, f, indent=2)

    def evaluate_need(self, tracer_type: str, context: Dict) -> Tuple[bool, str]:
        """
        Decision Point 1: Am I needed?
        
        Args:
            tracer_type: Type of tracer (memory/command/mood)
            context: Dict containing:
                - triggered: bool (explicit trigger)
                - ambient_pressure: float
                - urgency: float
                
        Returns:
            Tuple of (is_needed: bool, reason: str)
        """
        # Explicit trigger always activates
        if context.get('triggered', False):
            return True, "Explicit trigger received"
            
        # Check ambient pressure
        ambient_pressure = context.get('ambient_pressure', 0.0)
        if ambient_pressure > self.pressure_threshold:
            return True, f"High ambient pressure: {ambient_pressure:.2f}"
            
        # Type-specific activation
        if self._check_type_specific_need(tracer_type, context):
            return True, f"Type-specific need detected for {tracer_type}"
            
        return False, "No current need"
        
    def find_pressure_peak(self, pressure_map: Dict[str, float]) -> Tuple[str, float]:
        """
        Decision Point 2: Where is pressure highest?
        
        Args:
            pressure_map: Dict mapping component names to pressure values
            
        Returns:
            Tuple of (component_name, pressure_value)
        """
        if not pressure_map:
            return None, 0.0
            
        # Find highest pressure component
        max_component = max(pressure_map.items(), key=lambda x: x[1])
        
        # Update pressure history
        self.pressure_history.append(max_component[1])
        
        return max_component
        
    def evaluate_path(self, source: str, target: str, 
                     trust_matrix: Dict[str, float],
                     semantic_field: 'SemanticField') -> Tuple[bool, float, str]:
        """
        Decision Point 3: What path is most trusted and semantically proximate?
        
        Args:
            source: Source component
            target: Target component
            trust_matrix: Component trust scores
            semantic_field: Semantic field instance
            
        Returns:
            Tuple of (path_exists: bool, path_score: float, path: str)
        """
        # Get semantic distance
        semantic_distance = semantic_field.calculate_semantic_distance(source, target)
        
        # Get trust score
        trust_score = trust_matrix.get(f"{source}→{target}", 0.5)
        
        # Update trust history
        self.trust_history.append(trust_score)
        
        # Calculate path score
        path_score = (1 - semantic_distance) * trust_score
        
        # Check if path is viable
        if semantic_distance < self.semantic_threshold and trust_score > self.trust_threshold:
            return True, path_score, f"{source}→{target}"
            
        return False, path_score, None
        
    def determine_payload_type(self, tracer_type: str, context: Dict) -> str:
        """
        Decision Point 4: What type of payload do I carry?
        
        Args:
            tracer_type: Type of tracer
            context: Dict containing:
                - source_component: str
                - target_component: str
                - pressure_type: str
                - semantic_field: SemanticField
                
        Returns:
            str: 'memory', 'command', or 'mood'
        """
        # Type-specific payload determination
        if tracer_type == 'memory_tracer':
            return 'memory'
        elif tracer_type == 'command_tracer':
            return 'command'
        elif tracer_type == 'mood_tracer':
            return 'mood'
            
        # Default determination based on components and pressure
        source = context['source_component']
        target = context['target_component']
        
        if 'memory' in source.lower() or 'memory' in target.lower():
            return 'memory'
        elif 'mood' in source.lower() or 'mood' in target.lower():
            return 'mood'
        else:
            return 'command'
            
    def handle_no_path(self, context: Dict) -> Tuple[str, str]:
        """
        Decision Point 5: What to do when no path exists?
        
        Args:
            context: Dict containing:
                - pressure: float
                - trust_history: List[float]
                - semantic_field: SemanticField
                
        Returns:
            Tuple of (action: str, reason: str)
        """
        pressure = context.get('pressure', 0.0)
        trust_trend = np.mean(list(self.trust_history)[-10:]) if self.trust_history else 0.5
        
        # Check if we should hold
        if pressure > 0.8 and trust_trend > 0.6:
            if not self.hold_start_time:
                self.hold_start_time = time.time()
            elif time.time() - self.hold_start_time > self.hold_timeout:
                return 'decay', "Hold timeout exceeded"
            return 'hold', "High pressure with good trust trend"
            
        # Check if we should decay
        if pressure < 0.3 or trust_trend < 0.3:
            return 'decay', f"Low pressure ({pressure:.2f}) or trust ({trust_trend:.2f})"
            
        # Default to return
        return 'return', "No viable path, returning to source"
        
    def _check_type_specific_need(self, tracer_type: str, context: Dict) -> bool:
        """Check if tracer is needed based on its specific type."""
        if tracer_type == 'memory_tracer':
            return context.get('memory_pressure', 0.0) > 0.6
        elif tracer_type == 'command_tracer':
            return context.get('command_urgency', 0.0) > 0.7
        elif tracer_type == 'mood_tracer':
            return context.get('mood_volatility', 0.0) > 0.5
        return False
        
    def _get_pulse_pressure(self) -> float:
        """Get pressure from pulse_state.json"""
        try:
            with open("pulse_state.json", "r") as f:
                pulse_data = json.load(f)
                return min(1.0, pulse_data.get("heat", 0.0) / 10.0)
        except Exception:
            return 0.0
            
    def _get_bloom_entropy(self) -> float:
        """Get pressure from bloom entropy"""
        try:
            bloom_count = len([f for f in os.listdir("blooms") 
                              if f.endswith(".json")]) if os.path.exists("blooms") else 0
            return min(1.0, bloom_count / 20.0)
        except Exception:
            return 0.0
            
    def _get_claude_signal(self) -> float:
        """Get pressure from Claude signal input"""
        try:
            if os.path.exists("claude_trigger.py"):
                with open("claude_trigger.py", "r") as f:
                    content = f.read()
                    return min(1.0, content.count("claude") / 10.0)
            return 0.0
        except Exception:
            return 0.0
            
    def register_route(self, route_id: str, route_data: Dict):
        """Register a new route in the registry."""
        self.route_registry[route_id] = {
            'data': route_data,
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'success_count': 0,
            'failure_count': 0
        }
        
    def update_route_stats(self, route_id: str, success: bool):
        """Update route statistics after use."""
        if route_id in self.route_registry:
            route = self.route_registry[route_id]
            route['last_used'] = datetime.now().isoformat()
            if success:
                route['success_count'] += 1
            else:
                route['failure_count'] += 1
                
    def get_route_reliability(self, route_id: str) -> float:
        """Calculate route reliability score."""
        if route_id in self.route_registry:
            route = self.route_registry[route_id]
            total = route['success_count'] + route['failure_count']
            if total > 0:
                return route['success_count'] / total
        return 0.5  # Default reliability for unknown routes 

    def evaluate_route(self, source: str, target: str, 
                      payload: TracerPayload,
                      current_pressure: float,
                      tracer_type: str = "OwlTracer") -> Dict:
        """
        Evaluate a route between source and target components.
        
        Args:
            source: Source component
            target: Target component
            payload: TracerPayload containing signal and context
            current_pressure: Current system pressure
            tracer_type: Type of tracer making the request
            
        Returns:
            Dict containing route evaluation results
        """
        # Generate tracer ID
        tracer_id = f"{tracer_type}-{self.current_tick:03d}"
        
        # Check attention budget
        if not self.attention_manager.can_process_request(tracer_id):
            print(f"[TracerRouter] {tracer_id} has insufficient attention, delaying request")
            return {
                "success": False,
                "status": "delayed",
                "reason": "insufficient_attention",
                "tracer_id": tracer_id,
                "attention_status": self.attention_manager.get_attention_status(tracer_id)
            }
            
        # Get tracer configuration
        tracer_config = self.tracer_registry.get_tracer_config(tracer_type)
        
        # Get base agreement score
        agreement_score = self.agreement_matrix.get_route_score(f"{source}→{target}")
        
        # Get signal-based priority boost
        priority_boost = payload.get_priority_boost()
        if priority_boost > 0:
            print(f"[TracerRouter] Applying signal priority boost of {priority_boost:.2f}")
        
        # Apply priority boost to agreement score
        boosted_score = min(1.0, agreement_score + priority_boost)
        
        # Get semantic distance
        semantic_distance = self.semantic_field.calculate_semantic_distance(source, target)
        
        # Get current mood and apply mood-based modifiers
        current_mood = payload.mood_context or self._get_current_mood()
        mood_modifier = 1.0
        
        if current_mood == "submerged":
            mood_modifier = 0.9
            print(f"[TracerRouter] Submerged mood: reducing route scores by 10%")
        elif current_mood == "reflective":
            if semantic_distance > 0.5:
                mood_modifier = 1.2
                print(f"[TracerRouter] Reflective mood: boosting longer semantic paths by 20%")
            else:
                mood_modifier = 0.9
                print(f"[TracerRouter] Reflective mood: reducing shorter paths by 10%")
        elif current_mood == "anxious":
            if boosted_score < 0.5:
                mood_modifier = 0.0
                print(f"[TracerRouter] Anxious mood: blocking low-confidence path ({boosted_score:.2f})")
            else:
                mood_modifier = 1.1
                print(f"[TracerRouter] Anxious mood: boosting high-confidence path by 10%")
        
        # Apply mood modifier to boosted score
        mood_adjusted_score = boosted_score * mood_modifier
        
        # Apply tracer-specific logic
        route_data = {
            "source": source,
            "target": target,
            "pressure": current_pressure,
            "entropy": self._get_bloom_entropy(),
            "score": mood_adjusted_score,
            "signal": payload.signal,
            "signal_type": payload.get_signal_type()
        }
        
        if tracer_config["special_logic"]:
            tracer_modifier = tracer_config["special_logic"](route_data)
            mood_adjusted_score *= tracer_modifier
            print(f"[TracerRouter] Applied {tracer_type} modifier: {tracer_modifier:.2f}")
        
        # Apply tracer urgency modifier
        urgency_adjusted_score = mood_adjusted_score * tracer_config["urgency_modifier"]
        
        # Calculate final score
        final_score = (1 - semantic_distance) * urgency_adjusted_score
        
        # Check for preferred/avoided targets
        if target in tracer_config["preferred_targets"]:
            final_score *= 1.2
            print(f"[TracerRouter] Target {target} is preferred for {tracer_type}")
        elif target in tracer_config["avoided_targets"]:
            final_score *= 0.7
            print(f"[TracerRouter] Target {target} is avoided for {tracer_type}")
        
        # Determine route viability
        is_viable = (semantic_distance < self.semantic_threshold and 
                    urgency_adjusted_score > self.trust_threshold)
                    
        # Check if enough attention available for the route
        if is_viable and not self.attention_manager.consume_attention(tracer_id, final_score):
            is_viable = False
            print(f"[TracerRouter] Route viable but insufficient attention for {tracer_id}")
        
        # Create evaluation result
        eval_result = {
            "success": is_viable,
            "route": f"{source}→{target}",
            "score": final_score,
            "semantic_distance": semantic_distance,
            "agreement_score": agreement_score,
            "priority_boost": priority_boost,
            "boosted_score": boosted_score,
            "mood": current_mood,
            "mood_modifier": mood_modifier,
            "mood_adjusted_score": mood_adjusted_score,
            "tracer_type": tracer_type,
            "tracer_id": tracer_id,
            "urgency_modifier": tracer_config["urgency_modifier"],
            "final_adjusted_score": urgency_adjusted_score,
            "signal_type": payload.get_signal_type(),
            "payload_urgency": payload.urgency,
            "attention_status": self.attention_manager.get_attention_status(tracer_id)
        }
        
        # Update agreement matrix if route is viable
        if is_viable:
            self._update_agreement_matrix(source, target, final_score)
            
            # Log memory trail
            self.log_memory_trail(
                source=source,
                target=target,
                path=[source, target],
                score=final_score,
                entropy=current_pressure,
                signal=payload.signal,
                mood_context=current_mood
            )
            
        return eval_result

    def _get_risk_zones(self) -> Dict[str, float]:
        """Get risk zones from owl_registry.json."""
        try:
            with open('owl_registry.json', 'r') as f:
                registry = json.load(f)
                return registry.get('risk_zones', {})
        except Exception as e:
            print(f"[TracerRouter] Error reading owl registry: {str(e)}")
            return {}

    def _get_priority_terms(self) -> Dict[str, float]:
        """Get priority terms from claude_trace.json."""
        try:
            with open('claude_trace.json', 'r') as f:
                trace = json.load(f)
                return trace.get('priority_terms', {})
        except Exception as e:
            print(f"[TracerRouter] Error reading claude trace: {str(e)}")
            return {}

    def _update_agreement_matrix(self, source: str, target: str, score: float) -> None:
        """Update agreement matrix with new route score."""
        try:
            if not self.agreement_matrix:
                self.agreement_matrix = {}
                
            key = f"{source}→{target}"
            if key not in self.agreement_matrix:
                self.agreement_matrix[key] = {
                    'score': score,
                    'count': 1,
                    'last_updated': datetime.now().isoformat()
                }
            else:
                # Update with exponential moving average
                old_score = self.agreement_matrix[key]['score']
                new_score = 0.7 * old_score + 0.3 * score
                self.agreement_matrix[key].update({
                    'score': new_score,
                    'count': self.agreement_matrix[key]['count'] + 1,
                    'last_updated': datetime.now().isoformat()
                })
                
            # Save updated matrix
            with open('agreement_matrix.json', 'w') as f:
                json.dump(self.agreement_matrix, f, indent=2)
                
        except Exception as e:
            print(f"[TracerRouter] Error updating agreement matrix: {str(e)}")

    def _get_current_mood(self) -> str:
        """Get current mood context from system state."""
        try:
            with open("mood_state.json", 'r') as f:
                mood_state = json.load(f)
                return mood_state.get("current_mood", "neutral")
        except (FileNotFoundError, json.JSONDecodeError):
            return "neutral" 

    def _find_nearest_reachable(self, source: str, target: str, 
                              semantic_field: 'SemanticField') -> Tuple[str, float]:
        """
        Find the nearest reachable node to the target.
        
        Args:
            source: Source component
            target: Target component
            semantic_field: Semantic field for distance calculation
            
        Returns:
            Tuple of (nearest_node, distance_score)
        """
        # Get all known components
        all_components = set(self.route_registry.keys())
        all_components.add(source)
        all_components.add(target)
        
        # Calculate distances to target
        distances = []
        for component in all_components:
            if component != target:
                try:
                    distance = semantic_field.calculate_semantic_distance(component, target)
                    trust_score = self.agreement_matrix.get_route_score(f"{source}→{component}")
                    combined_score = (1 - distance) * trust_score
                    distances.append((component, combined_score))
                except Exception:
                    continue
                    
        if not distances:
            return source, 0.0
            
        # Return the component with highest combined score
        return max(distances, key=lambda x: x[1])
        
    def _log_fallback_handoff(self, source: str, target: str, 
                            fallback_node: str, score: float,
                            payload: TracerPayload) -> None:
        """
        Log fallback handoff information.
        
        Args:
            source: Original source
            target: Original target
            fallback_node: Node where handoff occurred
            score: Handoff confidence score
            payload: Original tracer payload
        """
        fallback_data = {
            "timestamp": datetime.now().isoformat(),
            "original_route": f"{source}→{target}",
            "fallback_node": fallback_node,
            "confidence_score": score,
            "payload": payload.to_dict(),
            "system_state": {
                "pressure": self._get_pulse_pressure(),
                "mood": self._get_current_mood(),
                "tick": self.current_tick
            }
        }
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Load existing fallback log
        fallback_file = "logs/route_fallback.json"
        try:
            if os.path.exists(fallback_file):
                with open(fallback_file, 'r') as f:
                    fallback_log = json.load(f)
            else:
                fallback_log = []
        except Exception:
            fallback_log = []
            
        # Append new fallback entry
        fallback_log.append(fallback_data)
        
        # Save updated log
        try:
            with open(fallback_file, 'w') as f:
                json.dump(fallback_log, f, indent=2)
            print(f"[TracerRouter] Logged fallback handoff to {fallback_node}")
        except Exception as e:
            print(f"[TracerRouter] Error logging fallback: {e}")
            
    def handle_route_failure(self, source: str, target: str,
                           payload: TracerPayload) -> Dict:
        """
        Handle route failure by finding nearest reachable node.
        
        Args:
            source: Original source
            target: Original target
            payload: Tracer payload
            
        Returns:
            Dict containing fallback route information
        """
        # Find nearest reachable node
        fallback_node, fallback_score = self._find_nearest_reachable(
            source, target, self.semantic_field
        )
        
        # Log the fallback handoff
        self._log_fallback_handoff(
            source=source,
            target=target,
            fallback_node=fallback_node,
            score=fallback_score,
            payload=payload
        )
        
        # Create fallback result
        fallback_result = {
            "success": True,  # Degraded success
            "status": "fallback",
            "original_route": f"{source}→{target}",
            "fallback_node": fallback_node,
            "confidence_score": fallback_score,
            "handoff_timestamp": datetime.now().isoformat(),
            "payload": payload.to_dict()
        }
        
        print(f"[TracerRouter] Route failure handled: {source}→{target} → {fallback_node}")
        return fallback_result

def main():
    """Example usage of TracerPayload and route evaluation."""
    # Create sample payloads
    entropy_payload = TracerPayload(
        signal="High entropy risk detected in bloom_engine",
        origin="entropy_monitor",
        urgency=0.8,
        mood_context="anxious",
        metadata={"risk_level": "high", "affected_components": ["bloom_engine"]}
    )
    
    bloom_payload = TracerPayload(
        signal="Critical bloom pattern detected",
        origin="bloom_analyzer",
        urgency=0.6,
        metadata={"pattern_type": "fractal", "confidence": 0.85}
    )
    
    # Initialize router
    router = TracerRouter()
    
    # Evaluate routes with different payloads
    entropy_route = router.evaluate_route(
        source="entropy_monitor",
        target="risk_analyzer",
        payload=entropy_payload,
        current_pressure=0.7,
        tracer_type="OwlTracer"
    )
    
    bloom_route = router.evaluate_route(
        source="bloom_analyzer",
        target="memory_weaver",
        payload=bloom_payload,
        current_pressure=0.5,
        tracer_type="BloomTracer"
    )
    
    print("\nEntropy Route Evaluation:")
    print(json.dumps(entropy_route, indent=2))
    
    print("\nBloom Route Evaluation:")
    print(json.dumps(bloom_route, indent=2))

if __name__ == "__main__":
    main() 