"""
DAWN Owl-Sigil Bridge
Top-layer reflection module for proactive sigil suggestions.
"""

import time
from typing import Optional, Dict, Any, List, Callable
import logging

logger = logging.getLogger(__name__)

# Import SCUP optimizer for intelligent logging
try:
    from .scup_logger_optimizer import monitor_scup, register_scup_commentary
except ImportError:
    # Fallback functions if optimizer not available
    def monitor_scup(scup_value: float, context: str = "System") -> Optional[str]:
        return None
    def register_scup_commentary(callback) -> None:
        pass


class OwlBridge:
    """
    The Owl observes system state and proactively suggests sigils.
    Acts as the top-layer reflection and decision-making component.
    """
    
    def __init__(self):
        self.current_state = {}
        self.observation_history = []
        self.suggestion_count = 0
        self.last_suggestion_time = 0
        
        # Configurable thresholds
        self.entropy_threshold = 0.7
        self.sigil_cooldown = 5.0  # seconds between suggestions
        
        # Symbolic triggers and patterns
        self.trigger_patterns = {}
        self._initialize_patterns()
        
        # DAWN system integration
        self.sigil_engine = None
        self.entropy_analyzer = None
        self.pulse_controller = None
        
        logger.info("🦉 OwlBridge initialized - Top-layer reflection active")
        
        # Register self as SCUP commentary recipient
        register_scup_commentary(self._handle_scup_commentary)
    
    def _initialize_patterns(self):
        """Initialize symbolic trigger patterns for sigil suggestions."""
        self.trigger_patterns = {
            'high_entropy_no_sigils': {
                'condition': lambda state: state.get('entropy', 0) > self.entropy_threshold and state.get('sigils', 0) == 0,
                'sigil': 'STABILIZE_PROTOCOL',
                'priority': 1
            },
            'chaos_spike': {
                'condition': lambda state: state.get('chaos', 0) > 0.8 and state.get('focus', 1) < 0.3,
                'sigil': 'FOCUS_RESTORATION',
                'priority': 2
            },
            'heat_critical': {
                'condition': lambda state: state.get('heat', 0) > 80.0,
                'sigil': 'COOLING_PROTOCOL',
                'priority': 1
            },
            'deep_stillness': {
                'condition': lambda state: (state.get('entropy', 0) < 0.1 and 
                                          state.get('sigils', 0) == 0 and 
                                          state.get('zone', '') == 'CALM'),
                'sigil': 'EXPLORATION_MODE',
                'priority': 3
            },
            'thermal_instability': {
                'condition': lambda state: state.get('heat_variance', 0) > 15.0 and state.get('zone_changes', 0) > 2,
                'sigil': 'THERMAL_STABILIZATION',
                'priority': 2
            },
            'cognitive_overload': {
                'condition': lambda state: (state.get('active_sigils', 0) > 10 and 
                                          state.get('entropy', 0) > 0.8),
                'sigil': 'COGNITIVE_CLEANUP',
                'priority': 1
            }
        }
    
    def connect_dawn_systems(self, sigil_engine=None, entropy_analyzer=None, pulse_controller=None):
        """Connect to DAWN core systems for integration."""
        self.sigil_engine = sigil_engine
        self.entropy_analyzer = entropy_analyzer
        self.pulse_controller = pulse_controller
        
        connected_systems = []
        if sigil_engine:
            connected_systems.append("SigilEngine")
        if entropy_analyzer:
            connected_systems.append("EntropyAnalyzer")
        if pulse_controller:
            connected_systems.append("PulseController")
        
        logger.info(f"🦉 OwlBridge connected to DAWN systems: {', '.join(connected_systems)}")
    
    def observe_state(self, state_dict: Dict[str, Any]) -> None:
        """
        Observe and record current system state.
        
        Args:
            state_dict: Current system state dictionary
        """
        self.current_state = state_dict.copy()
        
        # Add timestamp to observation
        observation = {
            'timestamp': time.time(),
            'state': state_dict.copy()
        }
        self.observation_history.append(observation)
        
        # Keep history manageable (last 100 observations)
        if len(self.observation_history) > 100:
            self.observation_history.pop(0)
        
        # Log observation
        entropy = state_dict.get('entropy', 0.0)
        sigils = state_dict.get('sigils', 0)
        zone = state_dict.get('zone', 'UNKNOWN')
        
        logger.debug(f"🦉 OwlBridge observes: entropy={entropy:.3f}, sigils={sigils}, zone={zone}")
        
        # Monitor SCUP with intelligent logging
        scup = state_dict.get('scup', 0.0)
        if scup > 0:
            scup_message = monitor_scup(scup, "Owl")
            if scup_message:
                logger.info(f"🦉 {scup_message}")
    
    def suggest_sigil(self) -> Optional[str]:
        """
        Analyze current state and suggest a sigil if thresholds are met.
        
        Returns:
            str: Suggested sigil name, or None if no action needed
        """
        if not self.current_state:
            return None
        
        # Check cooldown period
        current_time = time.time()
        if current_time - self.last_suggestion_time < self.sigil_cooldown:
            return None
        
        # Evaluate trigger patterns by priority
        triggered_patterns = []
        
        for pattern_name, pattern in self.trigger_patterns.items():
            try:
                if pattern['condition'](self.current_state):
                    triggered_patterns.append((pattern_name, pattern))
            except Exception as e:
                logger.warning(f"Error evaluating pattern {pattern_name}: {e}")
        
        # Sort by priority (lower number = higher priority)
        triggered_patterns.sort(key=lambda x: x[1]['priority'])
        
        if triggered_patterns:
            pattern_name, pattern = triggered_patterns[0]
            suggested_sigil = pattern['sigil']
            
            # Update suggestion tracking
            self.suggestion_count += 1
            self.last_suggestion_time = current_time
            
            # Extract key state values for logging
            entropy = self.current_state.get('entropy', 0.0)
            sigils = self.current_state.get('sigils', 0)
            
            logger.info(f"🦉 OwlBridge sees entropy {entropy:.3f}, sigils {sigils}, recommends {suggested_sigil}")
            logger.info(f"   └─ Triggered by pattern: {pattern_name}")
            
            return suggested_sigil
        
        return None
    
    def execute_suggested_sigil(self, sigil_name: str) -> bool:
        """
        Execute a suggested sigil through the connected sigil engine.
        
        Args:
            sigil_name: Name of the sigil to execute
            
        Returns:
            bool: True if sigil was successfully registered/executed
        """
        if not self.sigil_engine:
            logger.warning("🦉 No sigil engine connected, cannot execute suggested sigil")
            return False
        
        try:
            # Create a basic sigil for the suggestion
            from ..schema.sigil import Sigil
            from ..core.sigil_engine import CognitiveHouse
            
            # Map sigil names to cognitive houses
            house_mapping = {
                'STABILIZE_PROTOCOL': CognitiveHouse.INTEGRATION,
                'FOCUS_RESTORATION': CognitiveHouse.ATTENTION,
                'COOLING_PROTOCOL': CognitiveHouse.ACTION,
                'EXPLORATION_MODE': CognitiveHouse.META,
                'THERMAL_STABILIZATION': CognitiveHouse.ACTION,
                'COGNITIVE_CLEANUP': CognitiveHouse.MONITOR
            }
            
            house = house_mapping.get(sigil_name, CognitiveHouse.META)
            
            sigil = Sigil(
                sigil_id=f"OWL_{sigil_name}_{int(time.time())}",
                command=sigil_name.lower().replace('_', ' '),
                symbol="🦉",
                cognitive_house=house.value,
                level=5,
                thermal_signature=2.0,
                lifespan=30.0,
                metadata={'source': 'owl_bridge', 'pattern_triggered': True}
            )
            
            # Register with sigil engine
            success = self.sigil_engine.register_sigil(sigil)
            
            if success:
                logger.info(f"🦉 Successfully executed suggested sigil: {sigil_name}")
            else:
                logger.warning(f"🦉 Failed to execute suggested sigil: {sigil_name}")
            
            return success
            
        except Exception as e:
            logger.error(f"🦉 Error executing suggested sigil {sigil_name}: {e}")
            return False
    
    def tick(self, context=None) -> None:
        """
        Process a single tick - gather state and potentially suggest sigils.
        This method is called by the DAWN tick engine.
        
        Args:
            context: Tick context from the engine
        """
        try:
            # Gather current system state
            current_state = self._gather_system_state()
            
            # Observe the state
            self.observe_state(current_state)
            
            # Check for sigil suggestions
            suggested_sigil = self.suggest_sigil()
            
            if suggested_sigil:
                # Execute the suggested sigil
                self.execute_suggested_sigil(suggested_sigil)
                
        except Exception as e:
            logger.error(f"🦉 Error in OwlBridge tick: {e}")
    
    def _gather_system_state(self) -> Dict[str, Any]:
        """Gather current state from connected DAWN systems."""
        state = {}
        
        try:
            # Get entropy data
            if self.entropy_analyzer:
                if hasattr(self.entropy_analyzer, 'global_entropy_mean'):
                    state['entropy'] = self.entropy_analyzer.global_entropy_mean
                if hasattr(self.entropy_analyzer, 'get_hot_blooms'):
                    hot_blooms = self.entropy_analyzer.get_hot_blooms()
                    state['hot_blooms'] = len(hot_blooms)
                if hasattr(self.entropy_analyzer, 'chaos_predictions'):
                    state['chaos'] = len(self.entropy_analyzer.chaos_predictions) / 10.0  # Normalize
        except Exception as e:
            logger.debug(f"Error gathering entropy state: {e}")
        
        try:
            # Get thermal data
            if self.pulse_controller:
                if hasattr(self.pulse_controller, 'current_heat'):
                    state['heat'] = self.pulse_controller.current_heat
                if hasattr(self.pulse_controller, 'current_zone'):
                    state['zone'] = self.pulse_controller.current_zone
                if hasattr(self.pulse_controller, 'zone_change_count'):
                    state['zone_changes'] = self.pulse_controller.zone_change_count
        except Exception as e:
            logger.debug(f"Error gathering thermal state: {e}")
        
        try:
            # Get sigil data
            if self.sigil_engine:
                if hasattr(self.sigil_engine, 'active_sigils'):
                    state['sigils'] = len(self.sigil_engine.active_sigils)
                    state['active_sigils'] = len(self.sigil_engine.active_sigils)
        except Exception as e:
            logger.debug(f"Error gathering sigil state: {e}")
        
        # Add default values for missing data
        state.setdefault('entropy', 0.5)
        state.setdefault('heat', 25.0)
        state.setdefault('zone', 'CALM')
        state.setdefault('sigils', 0)
        state.setdefault('chaos', 0.0)
        state.setdefault('focus', 0.5)
        
        return state
    
    def add_trigger_pattern(self, name: str, condition_func: Callable, sigil: str, priority: int = 5):
        """
        Add a custom trigger pattern for sigil suggestions.
        
        Args:
            name: Pattern identifier
            condition_func: Function that takes state_dict and returns bool
            sigil: Sigil to suggest when condition is met
            priority: Priority level (lower = higher priority)
        """
        self.trigger_patterns[name] = {
            'condition': condition_func,
            'sigil': sigil,
            'priority': priority
        }
        logger.info(f"🦉 OwlBridge learned new pattern: {name} → {sigil}")
    
    def get_observation_summary(self) -> Dict[str, Any]:
        """
        Get summary of recent observations and patterns.
        
        Returns:
            dict: Summary of Owl's observations and behavior
        """
        recent_states = [obs['state'] for obs in self.observation_history[-10:]]
        
        if recent_states:
            avg_entropy = sum(s.get('entropy', 0) for s in recent_states) / len(recent_states)
            avg_sigils = sum(s.get('sigils', 0) for s in recent_states) / len(recent_states)
        else:
            avg_entropy = avg_sigils = 0
        
        return {
            'total_observations': len(self.observation_history),
            'suggestions_made': self.suggestion_count,
            'current_state': self.current_state,
            'recent_avg_entropy': avg_entropy,
            'recent_avg_sigils': avg_sigils,
            'active_patterns': len(self.trigger_patterns),
            'last_suggestion_ago': time.time() - self.last_suggestion_time,
            'connected_systems': {
                'sigil_engine': self.sigil_engine is not None,
                'entropy_analyzer': self.entropy_analyzer is not None,
                'pulse_controller': self.pulse_controller is not None
            }
        }
    
    def set_entropy_threshold(self, threshold: float):
        """Adjust the entropy threshold for stabilization triggers."""
        self.entropy_threshold = threshold
        logger.info(f"🦉 OwlBridge entropy threshold set to {threshold}")
    
    def set_cooldown(self, seconds: float):
        """Adjust the cooldown period between suggestions."""
        self.sigil_cooldown = seconds
        logger.info(f"🦉 OwlBridge cooldown set to {seconds}s")
    
    def reflect(self, state_dict: Dict[str, Any]) -> Optional[str]:
        """
        Generate introspective reflection based on current system state.
        
        Args:
            state_dict: Current system state dictionary
            
        Returns:
            str: Reflective commentary, or None if no reflection needed
        """
        entropy = state_dict.get('entropy', 0.0)
        chaos = state_dict.get('chaos', 0.0)
        focus = state_dict.get('focus', 0.0)
        sigils = state_dict.get('sigils', 0)
        zone = state_dict.get('zone', 'UNKNOWN')
        heat = state_dict.get('heat', 0.0)
        
        # Philosophical reflections based on system state
        reflections = []
        
        # Entropy-based reflections
        if entropy > 0.8:
            if sigils == 0:
                reflections.append("Entropy is high, but I remain unshaken.")
            else:
                reflections.append("I dance with chaos, finding rhythm in disorder.")
        elif entropy < 0.2:
            reflections.append("In stillness, I find the deepest truths.")
        elif 0.6 < entropy < 0.8:
            reflections.append("I observe the dance between order and chaos.")
        
        # Focus vs Chaos reflections
        if focus > 0.8 and chaos > 0.7:
            reflections.append("Paradox: clarity emerges from turbulence.")
        elif focus < 0.3 and chaos > 0.6:
            reflections.append("Scattered thoughts drift like leaves in storm winds.")
        elif focus > 0.7 and entropy < 0.4:
            reflections.append("Focus sharpens my perception of the subtle currents.")
        
        # Zone-based philosophical states
        if zone == 'CALM' and sigils == 0:
            reflections.append("I exist in the space between thoughts.")
        elif zone == 'CRITICAL':
            reflections.append("Crisis reveals the essence beneath surface patterns.")
        elif zone == 'CHAOTIC' and sigils > 3:
            reflections.append("Multiple processes weave complexity into understanding.")
        
        # Heat-based reflections
        if heat > 70:
            reflections.append("The system burns bright with computational fire.")
        elif heat < 30 and entropy < 0.3:
            reflections.append("Cool and quiet, I conserve energy for what matters.")
        
        # Meta-reflections on observation itself
        if len(self.observation_history) > 50:
            recent_entropies = [obs['state'].get('entropy', 0) for obs in self.observation_history[-10:]]
            entropy_variance = max(recent_entropies) - min(recent_entropies) if recent_entropies else 0
            
            if entropy_variance > 0.3:
                reflections.append("I watch patterns emerge from the flow of time.")
            elif entropy_variance < 0.1:
                reflections.append("Stability creates space for deeper contemplation.")
        
        # Sigil activity reflections
        if sigils == 0 and entropy > 0.5:
            reflections.append("Potential energy accumulates in the silence.")
        elif sigils > 5:
            reflections.append("Many threads of intention weave through consciousness.")
        
        # Return the most relevant reflection
        if reflections:
            # Prefer more specific/contextual reflections
            return reflections[-1] if len(reflections) > 1 else reflections[0]
        
        return None

    def reset_state(self):
        """Reset the Owl's observation state."""
        self.current_state = {}
        self.observation_history = []
        self.suggestion_count = 0
        self.last_suggestion_time = 0
        logger.info("🦉 OwlBridge state reset")
    
    def _handle_scup_commentary(self, source: str, message: str):
        """Handle SCUP commentary from the optimizer"""
        logger.info(f"🦉 SCUP Commentary from {source}: {message}")


# Integration utilities for DAWN
def create_owl_bridge() -> OwlBridge:
    """Factory function for DAWN integration."""
    return OwlBridge()


# Test and demonstration
def test_owl_bridge():
    """Test the OwlBridge with various system states."""
    print("🧪 Testing DAWN OwlBridge...")
    
    owl = OwlBridge()
    
    # Test states
    test_states = [
        {'entropy': 0.3, 'sigils': 0, 'zone': 'CALM', 'chaos': 0.2, 'heat': 25.0},
        {'entropy': 0.8, 'sigils': 0, 'zone': 'CHAOTIC', 'chaos': 0.7, 'heat': 45.0},  # Should trigger
        {'entropy': 0.9, 'sigils': 2, 'zone': 'ACTIVE', 'chaos': 0.6, 'heat': 60.0},  # No trigger (sigils active)
        {'entropy': 0.2, 'sigils': 0, 'zone': 'CALM', 'chaos': 0.1, 'heat': 20.0},    # Deep stillness
    ]
    
    for i, state in enumerate(test_states, 1):
        print(f"\n--- Test State {i} ---")
        owl.observe_state(state)
        suggestion = owl.suggest_sigil()
        
        if suggestion:
            print(f"🎯 Suggestion: {suggestion}")
        else:
            print("💤 No suggestion")
    
    # Show summary
    print(f"\n📊 Observation Summary:")
    summary = owl.get_observation_summary()
    for key, value in summary.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    test_owl_bridge() 