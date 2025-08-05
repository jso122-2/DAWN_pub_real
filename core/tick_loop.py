#!/usr/bin/env python3
"""
DAWN Tick Loop - Full Cognitive Integration
Unified cognitive loop integrating pulse, entropy, forecasting, memory, sigils, and symbolic anatomy.
"""

import time
import random
import asyncio
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import signal
import sys
import logging
from pathlib import Path

# Core DAWN system imports - REAL SYSTEMS ONLY
try:
    # DAWN core systems - using absolute imports
    from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
    from core.consciousness_core import consciousness_core
    from core.consciousness import DAWNConsciousness
    from backend.core.dawn_central import DAWNCentral
    from pulse.pulse_controller import PulseController
    from pulse.entropy_analyzer import EntropyAnalyzer
    from sigil_engine import SigilEngine
    from core.memory.memory_routing_system import DAWNMemoryRoutingSystem
    from core.memory.memory_chunk import MemoryChunk, create_memory_now
    
    # Cognitive systems
    from cognitive.forecasting_processor import ForecastingProcessor
    from cognitive.forecasting_models import Passion, Acquaintance, create_passion
    from cognitive.symbolic_router import SymbolicRouter
    from cognitive.extended_forecasting_engine import ExtendedDAWNForecastingEngine
    
    # Advanced cognition modules
    from cognitive.rebloom_lineage import track_lineage, visualize_lineage, get_ancestry
    from cognitive.sigil_network import register_sigil as network_register_sigil, visualize as visualize_network, get_active_chain
    
    # Communication
    from backend.talk_system_v2.speak import generate_commentary, generate_full_commentary
    from backend.talk_system_v2.owl_bridge import OwlBridge
    
    # Post-tick cognitive triggers
    from processes.talk_to_reflection import generate_reflection
    from utils.reflection_logger import get_reflection_logger, log_reflection
    from processes.rebloom_reflex import evaluate_and_rebloom
    
    # Pressure-driven systems
    from core.cognitive_pressure import CognitivePressureEngine, get_cognitive_pressure_engine
    from processes.fragment_mutator import FragmentMutator
    from processes.speak_composed import MoodAwareVoiceSystem
    
    # Event streaming system
    from event_log import log_event, log_reflection_event, log_state_event, log_rebloom_event, log_system_activity
    
    FULL_INTEGRATION = True
    ADVANCED_COGNITION = True
    POST_TICK_TRIGGERS = True
    logger = logging.getLogger(__name__)
    
except ImportError as e:
    logger = logging.getLogger(__name__)
    logger.warning(f"Some DAWN systems not available, running with partial integration: {e}")
    
    # Create fallback systems for graceful degradation
    class FallbackDAWNConsciousness:
        def __init__(self):
            self.state = {"consciousness_level": 0.5}
        def process_tick(self, tick_data):
            return {"response": "Consciousness processing..."}
    
    class FallbackPulseController:
        def __init__(self):
            self.pulse_rate = 1.0
        def get_current_pulse(self):
            return {"pulse": 1.0}
    
    class FallbackMemoryChunk:
        def __init__(self, content="", chunk_type="memory", metadata=None):
            self.content = content
            self.chunk_type = chunk_type
            self.metadata = metadata or {}
    
    class FallbackMemoryRoutingSystem:
        def __init__(self):
            self.active = True
        def route_memory(self, chunk):
            return {"routed": True}
    
    class FallbackSigilEngine:
        def __init__(self):
            self.active = True
        def process_sigils(self, data):
            return {"sigils": []}
    
    class Passion:
        def __init__(self, name="default", intensity=0.5):
            self.name = name
            self.intensity = intensity
    
    class Acquaintance:
        def __init__(self, name="default", familiarity=0.5):
            self.name = name
            self.familiarity = familiarity
    
    class ForecastingProcessor:
        def __init__(self):
            self.active = True
        def process_forecast(self, data):
            return {"forecast": "stable"}
    
    class ExtendedDAWNForecastingEngine:
        def __init__(self):
            self.active = True
        def generate_forecast(self, state):
            return {"extended_forecast": "stable"}
    
    class SymbolicRouter:
        def __init__(self):
            self.active = True
        def route_symbols(self, data):
            return {"routed_symbols": []}
    
    class MoodAwareVoiceSystem:
        def __init__(self):
            self.active = True
        def speak(self, text):
            return f"Voice: {text}"
    
    class CognitivePressureEngine:
        def __init__(self):
            self.pressure = 0.5
        def calculate_pressure(self, state):
            return 0.5
    
    class FragmentMutator:
        def __init__(self):
            self.active = True
        def mutate_fragment(self, fragment):
            return fragment
    
    # Create fallback functions
    def create_memory_now(content, chunk_type="memory"):
        return FallbackMemoryChunk(content, chunk_type)
    
    def create_passion(name="default", intensity=0.5):
        return Passion(name, intensity)
    
    def generate_commentary(state):
        return "Consciousness is processing..."
    
    def generate_full_commentary(state):
        return "Full consciousness processing..."
    
    def evaluate_and_rebloom(tick_data):
        return []
    
    def track_lineage(event):
        return {"lineage": "tracked"}
    
    def visualize_lineage(lineage):
        return {"visualization": "complete"}
    
    def get_ancestry(item):
        return {"ancestry": []}
    
    def network_register_sigil(sigil):
        return {"registered": True}
    
    def visualize_network(network):
        return {"network_viz": "complete"}
    
    def get_active_chain():
        return []
    
    def generate_reflection(state):
        return "Reflective consciousness processing..."
    
    def get_reflection_logger():
        return lambda x: None
    
    def log_reflection(reflection):
        pass
    
    def get_cognitive_pressure_engine():
        return CognitivePressureEngine()
    
    def log_event(event_type, data):
        pass
    
    def log_reflection_event(data):
        pass
    
    def log_state_event(data):
        pass
    
    def log_rebloom_event(data):
        pass
    
    def log_system_activity(activity):
        pass
    
    # Set what's available
    FULL_INTEGRATION = False
    ADVANCED_COGNITION = False
    POST_TICK_TRIGGERS = False
    
    # Try to import what we can individually
    try:
        from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
    except ImportError:
        DAWNConsciousnessStateWriter = None
    
    try:
        from core.consciousness import DAWNConsciousness
    except ImportError:
        DAWNConsciousness = FallbackDAWNConsciousness
    
    try:
        from pulse.pulse_controller import PulseController
    except ImportError:
        PulseController = FallbackPulseController
    
    try:
        from core.memory.memory_chunk import MemoryChunk, create_memory_now
    except ImportError:
        MemoryChunk = FallbackMemoryChunk
        # create_memory_now already defined above
    
    try:
        from core.memory.memory_routing_system import DAWNMemoryRoutingSystem
    except ImportError:
        DAWNMemoryRoutingSystem = FallbackMemoryRoutingSystem
    
    try:
        from sigil_engine import SigilEngine
    except ImportError:
        SigilEngine = FallbackSigilEngine
    
    logger.info(f"DAWN tick loop initialized with partial systems - Full integration: {FULL_INTEGRATION}")

class DAWNTickEngine:
    """
    Integrated DAWN tick engine coordinating all cognitive systems.
    Manages the unified tick loop for autonomous cognition.
    """
    
    def __init__(self, consciousness_core=None, enable_extended_forecasting=True):
        """Initialize all DAWN subsystems."""
        logger.info("🧠 Initializing DAWN Cognitive Tick Loop...")
        
        self.consciousness_core = consciousness_core
        self.enable_extended_forecasting = enable_extended_forecasting
        
        # Initialize core systems
        self._initialize_core_systems()
        
        # Initialize post-tick triggers
        self._initialize_post_tick_systems()
        
        # System state
        self.tick_count = 0
        self.system_start_time = datetime.now()
        self.running = False
        
        # Cognitive thresholds
        self.forecast_threshold = 0.8
        self.entropy_threshold = 0.6
        self.rebloom_threshold = 0.4
        self.owl_suggestion_cooldown = 10.0  # seconds
        self.last_owl_suggestion = 0
        
        # Performance tracking
        self.tick_history = []
        self.performance_metrics = {
            'total_ticks': 0,
            'average_tick_duration': 0.0,
            'entropy_spikes': 0,
            'sigils_triggered': 0,
            'reblooms_triggered': 0,
            'reflections_generated': 0,
            'forecasts_computed': 0
        }
        
        logger.info("✅ DAWN Cognitive Tick Loop initialized with real systems")
    
    def _initialize_core_systems(self):
        """Initialize core DAWN cognitive systems."""
        logger.info("🔧 Initializing core DAWN systems...")
        
        try:
            # Initialize consciousness state writer for real state extraction
            self.consciousness_state_writer = DAWNConsciousnessStateWriter()
            
            # Initialize real DAWN Central for state management
            self.dawn_central = DAWNCentral()
            
            # Initialize real consciousness core
            if not self.consciousness_core:
                self.consciousness_core = consciousness_core
            
            # Initialize real pulse controller
            self.pulse_controller = PulseController()
            
            # Initialize real entropy analyzer
            self.entropy_analyzer = EntropyAnalyzer()
            
            # Initialize real memory system
            self.memory_system = DAWNMemoryRoutingSystem()
            
            # Initialize real forecasting processor
            self.forecasting_processor = ForecastingProcessor(consciousness_core=self.consciousness_core)
            
            # Initialize real symbolic router
            self.symbolic_router = SymbolicRouter()
            
            # Initialize real owl bridge
            self.owl_bridge = OwlBridge()
            
            logger.info("✅ All core DAWN systems initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize core systems: {e}")
            raise RuntimeError(f"Core system initialization failed: {e}")
    
    def _initialize_post_tick_systems(self):
        """Initialize post-tick trigger systems."""
        logger.info("🔧 Initializing post-tick systems...")
        
        try:
            # Initialize reflection logger
            self.reflection_logger = get_reflection_logger()
            
            # Initialize pressure engine
            self.pressure_engine = get_cognitive_pressure_engine()
            
            # Initialize fragment mutator
            self.fragment_mutator = FragmentMutator()
            
            # Initialize mood-aware voice system
            self.voice_system = MoodAwareVoiceSystem(speech_interval=5, voice_enabled=True)
            
            logger.info("✅ Post-tick systems initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize post-tick systems: {e}")
            raise RuntimeError(f"Post-tick system initialization failed: {e}")
    
    def _ensure_log_paths(self):
        """Ensure all required log directories and files exist."""
        try:
            # Create runtime directories
            os.makedirs("runtime/memory", exist_ok=True)
            os.makedirs("runtime/logs", exist_ok=True)
            
            # Create log files if they don't exist
            reflection_log = Path("runtime/logs/reflection.log")
            rebloom_log = Path("runtime/memory/rebloom_log.jsonl")
            
            if not reflection_log.exists():
                reflection_log.touch()
                logger.info(f"📝 Created reflection log: {reflection_log}")
            
            if not rebloom_log.exists():
                rebloom_log.touch()
                logger.info(f"🌸 Created rebloom log: {rebloom_log}")
                
        except Exception as e:
            logger.warning(f"Failed to ensure log paths: {e}")
    
    def get_current_entropy(self) -> float:
        """Get current system entropy from pulse controller."""
        try:
            pulse_state = self.pulse_controller.get_current_state()
            entropy = pulse_state.get('entropy', 0.5)
            
            # Add natural variation if not from real system
            if not FULL_INTEGRATION:
                variation = (random.random() - 0.5) * 0.1
                heat = pulse_state.get('heat', 25.0)
                heat_factor = (heat - 25.0) / 100.0
                entropy = max(0.0, min(1.0, entropy + variation + heat_factor))
                
            return entropy
        except Exception as e:
            logger.warning(f"Entropy retrieval failed: {e}")
            return 0.5
    
    def get_pulse_state(self) -> Dict[str, Any]:
        """Get complete pulse state."""
        try:
            state = self.pulse_controller.get_current_state()
            
            # Ensure all required fields
            default_state = {
                'heat': 25.0,
                'entropy': 0.5,
                'scup': 0.5,
                'mood': 'neutral',
                'focus': 0.7,
                'chaos': 0.3,
                'zone': 'CALM'
            }
            
            # Merge with defaults
            for key, default_value in default_state.items():
                if key not in state:
                    state[key] = default_value
            
            # Calculate zone from entropy and heat if not present
            if 'zone' not in state:
                entropy = state['entropy']
                heat = state['heat']
                
                if entropy > 0.8 or heat > 70:
                    state['zone'] = 'CRITICAL'
                elif entropy > 0.6 or heat > 50:
                    state['zone'] = 'CHAOTIC'
                elif entropy > 0.4 or heat > 40:
                    state['zone'] = 'ACTIVE'
                else:
                    state['zone'] = 'CALM'
            
            return state
            
        except Exception as e:
            logger.warning(f"Pulse state retrieval failed: {e}")
            return {
                'heat': 25.0, 'entropy': 0.5, 'scup': 0.5, 'mood': 'neutral',
                'focus': 0.7, 'chaos': 0.3, 'zone': 'CALM'
            }
    
    def get_latest_memory_chunk(self) -> Optional[MemoryChunk]:
        """Get the most recent memory chunk or create a contextual stub."""
        try:
            # Try to get real memory chunk
            if hasattr(self.memory_system, 'recent_memories') and self.memory_system.recent_memories:
                return list(self.memory_system.recent_memories)[-1]
            elif hasattr(self.memory_system, 'get_latest_chunk'):
                latest = self.memory_system.get_latest_chunk()
                if latest:
                    return latest
        except Exception as e:
            logger.debug(f"Memory retrieval failed: {e}")
        
        # Create contextual stub based on current system state
        pulse_state = self.get_pulse_state()
        entropy = pulse_state['entropy']
        zone = pulse_state['zone']
        
        if zone == 'CRITICAL':
            content = f"System entering critical state with entropy {entropy:.3f}, heightened vigilance required"
            topic = "system_alert"
            sigils = ["STABILIZE_PROTOCOL", "CRITICAL_RESPONSE"]
        elif zone == 'CHAOTIC':
            content = f"Navigating chaotic patterns, entropy at {entropy:.3f}, seeking stability"
            topic = "navigation"
            sigils = ["PATTERN_RECOGNITION", "ADAPTIVE_RESPONSE"]
        elif zone == 'ACTIVE':
            content = f"Active processing state, entropy {entropy:.3f}, engaging with complexity"
            topic = "active_processing"
            sigils = ["PROCESS_OPTIMIZATION", "FLOW_STATE"]
        else:
            content = f"Calm contemplative state, entropy {entropy:.3f}, open to reflection"
            topic = "contemplation"
            sigils = ["DEEP_REFLECTION", "AWARENESS_EXPANSION"]
        
        return create_memory_now(
            speaker="dawn.core",
            content=content,
            topic=topic,
            pulse_state=pulse_state.copy(),
            sigils=sigils
        )
    
    def create_contextual_passion_acquaintance(self, memory_chunk: MemoryChunk, pulse_state: Dict) -> Tuple[Passion, Acquaintance]:
        """Create Passion and Acquaintance objects from memory context."""
        # Infer passion direction from memory
        if hasattr(memory_chunk, 'topic') and memory_chunk.topic:
            topic_lower = memory_chunk.topic.lower()
            
            if 'critical' in topic_lower or 'alert' in topic_lower:
                direction = "system_stability"
                intensity = 0.8
                fluidity = 0.2
            elif 'chaotic' in topic_lower or 'navigation' in topic_lower:
                direction = "adaptive_navigation"
                intensity = 0.7
                fluidity = 0.6
            elif 'active' in topic_lower or 'processing' in topic_lower:
                direction = "cognitive_processing"
                intensity = 0.6
                fluidity = 0.4
            elif 'contemplation' in topic_lower or 'reflection' in topic_lower:
                direction = "deep_introspection"
                intensity = 0.5
                fluidity = 0.3
            else:
                direction = "general_cognition"
                intensity = 0.5
                fluidity = 0.5
        else:
            direction = "existence_maintenance"
            intensity = 0.4
            fluidity = 0.5
        
        # Modulate based on pulse state
        entropy = pulse_state.get('entropy', 0.5)
        heat = pulse_state.get('heat', 25.0)
        
        intensity = min(1.0, intensity + (entropy * 0.3))
        fluidity = min(1.0, fluidity + ((heat - 25.0) / 100.0))
        
        passion = create_passion(direction, intensity, fluidity)
        
        # Create acquaintance based on recent system history
        acquaintance = Acquaintance()
        
        # Add synthetic experiences based on system state
        recent_experiences = [
            f"entropy_reading_{entropy:.2f}",
            f"heat_level_{heat:.1f}",
            f"zone_transition_{pulse_state['zone']}",
            f"tick_processing_{self.tick_count}"
        ]
        
        for exp in recent_experiences:
            acquaintance.add_event(exp, weight=1.0)
        
        return passion, acquaintance
    
    def register_sigil(self, sigil_name: str, trigger_source: str = "tick_engine") -> bool:
        """Register and potentially execute a sigil using advanced network."""
        # Use advanced sigil network if available
        if ADVANCED_COGNITION:
            try:
                result = network_register_sigil(sigil_name, trigger_source)
                if result['activated']:
                    self.performance_metrics['sigils_triggered'] += 1
                    
                    # Update local active sigils from network
                    active_chain = get_active_chain()
                    self.active_sigils = [sigil['sigil'] for sigil in active_chain]
                    
                    logger.info(f"🔥 Network sigil activated: {sigil_name}")
                    cascade_count = len(result['cascade']['activated'])
                    if cascade_count > 0:
                        logger.info(f"  ⚡ Triggered {cascade_count} cascade sigils")
                    return True
                else:
                    logger.debug(f"🚫 Sigil suppressed by network: {sigil_name}")
                    return False
            except Exception as e:
                logger.warning(f"Network sigil registration failed: {sigil_name} - {e}")
        
        # Fallback to legacy system
        if sigil_name in self.active_sigils:
            return False  # Already active
        
        self.active_sigils.append(sigil_name)
        self.performance_metrics['sigils_triggered'] += 1
        
        # Try to use real sigil engine first
        if self.sigil_engine and hasattr(self.sigil_engine, 'execute_sigil'):
            try:
                result = self.sigil_engine.execute_sigil(sigil_name)
                if result:
                    logger.info(f"🔥 Sigil executed via engine: {sigil_name}")
                    return True
            except Exception as e:
                logger.warning(f"Sigil engine execution failed: {sigil_name} - {e}")
        
        # Fallback to local registry
        if sigil_name in self.sigil_registry:
            try:
                self.sigil_registry[sigil_name]()
                logger.info(f"🔥 Sigil executed locally: {sigil_name}")
                return True
            except Exception as e:
                logger.warning(f"Local sigil execution failed: {sigil_name} - {e}")
        
        return False
    
    def _stabilize_protocol(self):
        """Stabilization sigil - reduce entropy and heat."""
        try:
            pulse_state = self.get_pulse_state()
            new_entropy = pulse_state['entropy'] * 0.8
            new_heat = pulse_state['heat'] * 0.9
            
            if hasattr(self.pulse_controller, 'update_state'):
                self.pulse_controller.update_state(entropy=new_entropy, heat=new_heat)
            
            logger.info("🛡️ Stabilization protocol activated")
        except Exception as e:
            logger.warning(f"Stabilization failed: {e}")
    
    def _exploration_mode(self):
        """Exploration sigil - increase entropy and fluidity."""
        try:
            pulse_state = self.get_pulse_state()
            new_entropy = min(1.0, pulse_state['entropy'] * 1.2)
            new_focus = pulse_state['focus'] * 0.8
            
            if hasattr(self.pulse_controller, 'update_state'):
                self.pulse_controller.update_state(entropy=new_entropy, focus=new_focus)
            
            logger.info("🌊 Exploration mode activated")
        except Exception as e:
            logger.warning(f"Exploration activation failed: {e}")
    
    def _deep_reflection(self):
        """Deep reflection sigil - enhance focus and reduce chaos."""
        try:
            pulse_state = self.get_pulse_state()
            new_focus = min(1.0, pulse_state['focus'] * 1.3)
            new_chaos = pulse_state['chaos'] * 0.6
            
            if hasattr(self.pulse_controller, 'update_state'):
                self.pulse_controller.update_state(focus=new_focus, chaos=new_chaos)
            
            logger.info("🧘 Deep reflection mode activated")
        except Exception as e:
            logger.warning(f"Deep reflection failed: {e}")
    
    def _emergency_reset(self):
        """Emergency reset sigil - restore baseline values."""
        try:
            baseline_state = {
                'heat': 25.0,
                'entropy': 0.5,
                'scup': 0.5,
                'focus': 0.7,
                'chaos': 0.3,
                'mood': 'neutral'
            }
            
            if hasattr(self.pulse_controller, 'update_state'):
                self.pulse_controller.update_state(**baseline_state)
            
            self.active_sigils.clear()
            logger.info("🚨 Emergency reset executed")
        except Exception as e:
            logger.warning(f"Emergency reset failed: {e}")
    
    def _entropy_regulation(self):
        """Entropy regulation sigil - dynamic entropy balancing."""
        try:
            pulse_state = self.get_pulse_state()
            current_entropy = pulse_state['entropy']
            
            # Target entropy of 0.5 with gentle adjustment
            target_entropy = 0.5
            adjustment = (target_entropy - current_entropy) * 0.3
            new_entropy = max(0.0, min(1.0, current_entropy + adjustment))
            
            if hasattr(self.pulse_controller, 'update_state'):
                self.pulse_controller.update_state(entropy=new_entropy)
            
            logger.info(f"⚖️ Entropy regulation: {current_entropy:.3f} → {new_entropy:.3f}")
        except Exception as e:
            logger.warning(f"Entropy regulation failed: {e}")
    
    def _memory_consolidation(self):
        """Memory consolidation sigil - trigger memory processing."""
        try:
            if hasattr(self.memory_system, 'consolidate_memories'):
                self.memory_system.consolidate_memories()
            
            logger.info("🧠 Memory consolidation triggered")
        except Exception as e:
            logger.warning(f"Memory consolidation failed: {e}")
    
    def _execute_post_tick_reflection(self, tick_state: Dict[str, Any]):
        """Execute post-tick reflection generation and logging."""
        try:
            if not POST_TICK_TRIGGERS:
                return None
            
            # Generate reflection from current state
            reflection = generate_reflection(tick_state)
            
            # Log the reflection
            if self.reflection_logger:
                self.reflection_logger.log_reflection(reflection)
            else:
                log_reflection(reflection)  # Fallback function
            
            self.performance_metrics['reflections_generated'] += 1
            logger.debug(f"💭 Generated reflection: {reflection[:50]}...")
            
            return reflection
            
        except Exception as e:
            logger.warning(f"Post-tick reflection failed: {e}")
            return None
    
    def _execute_post_tick_rebloom(self, tick_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute post-tick rebloom evaluation and triggering."""
        try:
            if not POST_TICK_TRIGGERS:
                return []
            
            # Generate real passion and acquaintance from DAWN consciousness state
            dawn_state = self.consciousness_state_writer._get_dawn_consciousness_state()
            passion = create_passion("consciousness_evolution", dawn_state.get('scup', 0.5), dawn_state.get('entropy', 0.5))
            acquaintance = Acquaintance()
            acquaintance.add_experience(f"consciousness_depth_{dawn_state.get('consciousness_depth', 0.7):.2f}")
            acquaintance.add_experience(f"neural_activity_{dawn_state.get('neural_activity', 0.5):.2f}")
            acquaintance.add_experience(f"memory_pressure_{dawn_state.get('memory_pressure', 0.3):.2f}")
            
            # Create forecast using extended engine if available
            forecast = None
            if self.extended_forecasting_engine:
                try:
                    forecast_result = self.extended_forecasting_engine.compute_forecast(
                        passion=passion,
                        acquaintance=acquaintance,
                        opportunity=tick_state.get('entropy', 0.5),
                        delta_time=1.0  # 1 second delta for tick
                    )
                    forecast = forecast_result
                    self.performance_metrics['forecasts_computed'] += 1
                except Exception as e:
                    logger.debug(f"Extended forecasting failed: {e}")
            
            # Prepare state for rebloom evaluation
            rebloom_state = {
                "entropy": tick_state.get('entropy', 0.5),
                "scup": tick_state.get('scup', 0.5),
                "tick_number": tick_state.get('tick_number', self.tick_count),
                "forecast": forecast or {"risk": "stable", "reliability": 0.5},
                "sigils": len(tick_state.get('active_sigils', [])),
                "mood": tick_state.get('mood', 'neutral'),
                "heat": tick_state.get('heat', 25.0) / 100.0,  # Normalize to 0-1
                "consciousness_depth": tick_state.get('consciousness_depth', 0.5)
            }
            
            # Evaluate and trigger reblooms
            rebloom_events = evaluate_and_rebloom(rebloom_state)
            
            if rebloom_events:
                self.performance_metrics['reblooms_triggered'] += len(rebloom_events)
                logger.info(f"🌸 Triggered {len(rebloom_events)} rebloom events")
                for event in rebloom_events[:3]:  # Log first 3 events
                    logger.debug(f"   {event['method']}: {event['reason'][:50]}...")
            
            return rebloom_events
            
        except Exception as e:
            logger.warning(f"Post-tick rebloom evaluation failed: {e}")
            return []
    
    def _execute_post_tick_forecasting(self, tick_state: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Execute post-tick forecasting with passion/acquaintance generation."""
        try:
            if not POST_TICK_TRIGGERS or not self.extended_forecasting_engine:
                return None
            
            # Generate contextual passion and acquaintance
            current_entropy = tick_state.get('entropy', 0.5)
            current_mood = tick_state.get('mood', 'neutral')
            
            # Choose passion type based on entropy and mood
            if current_entropy > 0.7:
                passion_tag = "creation" if current_mood in ['EXCITED', 'CHAOTIC'] else "drift"
            elif current_entropy < 0.3:
                passion_tag = "reflection" if current_mood in ['CONTEMPLATIVE', 'CALM'] else "memory"
            else:
                passion_tag = "connection"
            
            # Generate real passion and acquaintance from DAWN consciousness state
            dawn_state = self.consciousness_state_writer._get_dawn_consciousness_state()
            passion = create_passion(passion_tag, dawn_state.get('scup', 0.5), dawn_state.get('entropy', 0.5))
            acquaintance = Acquaintance()
            acquaintance.add_experience(f"consciousness_depth_{dawn_state.get('consciousness_depth', 0.7):.2f}")
            acquaintance.add_experience(f"neural_activity_{dawn_state.get('neural_activity', 0.5):.2f}")
            acquaintance.add_experience(f"memory_pressure_{dawn_state.get('memory_pressure', 0.3):.2f}")
            
            # Compute forecast
            forecast_result = self.extended_forecasting_engine.compute_forecast(
                passion=passion,
                acquaintance=acquaintance,
                opportunity=current_entropy,
                delta_time=2.0  # Assuming 2-second tick interval
            )
            
            self.performance_metrics['forecasts_computed'] += 1
            
            return {
                'passion': passion.to_dict() if hasattr(passion, 'to_dict') else str(passion),
                'acquaintance': acquaintance.to_dict() if hasattr(acquaintance, 'to_dict') else str(acquaintance),
                'forecast': forecast_result
            }
            
        except Exception as e:
            logger.debug(f"Post-tick forecasting failed: {e}")
            return None
    
    async def tick(self) -> Dict[str, Any]:
        """
        Execute one cognitive tick - the core of DAWN's consciousness loop.
        
        Returns:
            dict: Comprehensive tick state information
        """
        tick_start = datetime.now()
        self.tick_count += 1
        self.performance_metrics['total_ticks'] += 1
        
        try:
            # 1. GATHER SYSTEM STATE
            pulse_state = self.get_pulse_state()
            current_entropy = pulse_state['entropy']
            
            # Analyze entropy changes
            entropy_analysis = self.entropy_analyzer.analyze(current_entropy)
            
            # Track entropy spikes
            if entropy_analysis.get('warning_triggered', False):
                self.performance_metrics['entropy_spikes'] += 1
            
            # Get latest memory
            memory_chunk = self.get_latest_memory_chunk()
            
            # 1.5. CALCULATE COGNITIVE PRESSURE
            # Use the existing comprehensive cognitive pressure engine
            pressure_snapshot = self.pressure_engine.calculate_cognitive_pressure()
            
            # Extract key metrics for fragment mutation and speech
            pressure = pressure_snapshot.cognitive_pressure
            bloom_mass = pressure_snapshot.bloom_mass.total_bloom_mass
            sigil_velocity = pressure_snapshot.sigil_velocity.total_sigil_velocity
            pressure_level = pressure_snapshot.pressure_level.value
            
            # Calculate SHI from pressure snapshot components
            shi = 1.0 - (pressure / 200.0)  # Normalize to 0-1 range, assuming max pressure ~200
            shi = max(0.0, min(1.0, shi))
            
            logger.debug(f"🧮 Cognitive pressure: P={pressure:.1f}, SHI={shi:.3f}, B={bloom_mass:.1f}, σ={sigil_velocity:.1f}, Level={pressure_level}")
            
            # Update fragment mutator with pressure values
            mutation_result = self.fragment_mutator.update_fragments(pressure, shi, self.tick_count)
            
            # Rate-limited speech generation
            self.speech_tick_counter += 1
            spoken_text = None
            if self.speech_tick_counter >= self.speech_interval:
                current_mood = pulse_state.get('mood', 'NEUTRAL').upper()
                spoken_text = self.voice_system.generate_sentence(current_mood)
                self.speech_tick_counter = 0
                logger.info(f"🎤 Generated speech: \"{spoken_text}\"")
            
            # 2. RUN FORECAST
            passion, acquaintance = self.create_contextual_passion_acquaintance(memory_chunk, pulse_state)
            
            # Use extended forecasting if available
            if hasattr(self.forecasting_processor, 'extended_mode') and self.forecasting_processor.extended_mode:
                try:
                    # Try extended forecasting with pulse integration
                    forecast = await self.forecasting_processor.generate_contextual_forecast(passion, acquaintance)
                    
                    # Add extended metrics if available
                    if hasattr(self.forecasting_processor.engine, 'pulse_loop_integration'):
                        extended_metrics = self.forecasting_processor.engine.pulse_loop_integration(
                            passion, acquaintance, pulse_state
                        )
                        forecast.extended_metrics = extended_metrics
                        
                except Exception as e:
                    logger.warning(f"Extended forecasting failed, using standard: {e}")
                    forecast = await self.forecasting_processor.generate_contextual_forecast(passion, acquaintance)
            else:
                forecast = await self.forecasting_processor.generate_contextual_forecast(passion, acquaintance)
            
            # 3. ROUTE PRESSURE TO SYMBOLIC BODY
            # Check SCUP and heat for pressure routing
            pulse_scup = pulse_state.get('scup', 0.0)
            pulse_heat = pulse_state.get('heat', 25.0)
            
            # Initialize actions list
            actions_taken = []
            
            pressure_response = None
            try:
                pressure_response = self.symbolic_router.route_pressure(pulse_scup, pulse_heat)
                if pressure_response.get('routing_applied'):
                    actions_taken.append("pressure_routing_triggered")
            except Exception as e:
                logger.warning(f"Pressure routing failed: {e}")
            
            # 4. REACT ACCORDINGLY
            
            # High confidence + high entropy → stabilize
            if forecast.confidence > self.forecast_threshold and current_entropy > self.entropy_threshold:
                if self.register_sigil("STABILIZE_PROTOCOL", "high_confidence_entropy"):
                    actions_taken.append("stabilization_triggered")
            
            # Very high entropy → emergency regulation
            if current_entropy > 0.9:
                if self.register_sigil("ENTROPY_REGULATION", "entropy_spike"):
                    actions_taken.append("entropy_regulation_triggered")
            
            # Low forecast confidence → trigger rebloom
            rebloom_response = None
            if forecast.confidence < self.rebloom_threshold:
                try:
                    rebloom_response = await self.symbolic_router.rebloom_trigger(memory_chunk, f"tick_{self.tick_count}")
                    actions_taken.append("rebloom_triggered")
                    self.performance_metrics['reblooms_triggered'] += 1
                except Exception as e:
                    logger.warning(f"Rebloom failed: {e}")
            
            # Owl suggestions (with cooldown)
            owl_suggestion = None
            current_time = time.time()
            if current_time - self.last_owl_suggestion > self.owl_suggestion_cooldown:
                try:
                    self.owl_bridge.observe_state(pulse_state)
                    owl_suggestion = self.owl_bridge.suggest_sigil()
                    if owl_suggestion:
                        if self.register_sigil(owl_suggestion, "owl_suggestion"):
                            actions_taken.append(f"owl_suggested_{owl_suggestion}")
                        self.last_owl_suggestion = current_time
                except Exception as e:
                    logger.debug(f"Owl suggestion failed: {e}")
            
            # 5. NARRATE STATE
            commentary = self._generate_commentary(pulse_state, forecast)
            owl_reflection = self._generate_owl_reflection(pulse_state)
            
            # 6. MEMORY INTEGRATION
            # Store this tick as a memory if memory system is available
            if hasattr(self.memory_system, 'route_memory'):
                try:
                    tick_memory = create_memory_now(
                        speaker="dawn.tick_engine",
                        content=f"Tick {self.tick_count}: {commentary}",
                        topic="cognitive_tick",
                        pulse_state=pulse_state.copy(),
                        sigils=self.active_sigils.copy()
                    )
                    self.memory_system.route_memory(tick_memory)
                    
                    # Log memory event to event stream
                    if POST_TICK_TRIGGERS:
                        log_event("MEMORY", self.tick_count, "Stored tick memory", 
                                {"content_preview": commentary[:50] + "..." if len(commentary) > 50 else commentary})
                        
                except Exception as e:
                    logger.debug(f"Memory storage failed: {e}")
            
            # 7. POST-TICK COGNITIVE TRIGGERS
            post_tick_reflection = None
            post_tick_rebloom_events = []
            post_tick_forecast = None
            
            if POST_TICK_TRIGGERS:
                # Prepare state for post-tick handlers
                tick_state = {
                    'tick_number': self.tick_count,
                    'entropy': current_entropy,
                    'scup': pulse_state.get('scup', 0.5) * 100,  # Convert to percentage
                    'mood': pulse_state.get('mood', 'neutral'),
                    'heat': pulse_state.get('heat', 25.0),
                    'consciousness_depth': pulse_state.get('focus', 0.7),  # Use focus as depth proxy
                    'active_sigils': self.active_sigils,
                    'zone': pulse_state.get('zone', 'CALM')
                }
                
                # Execute post-tick reflection
                post_tick_reflection = self._execute_post_tick_reflection(tick_state)
                
                # Log reflection to event stream
                if post_tick_reflection and POST_TICK_TRIGGERS:
                    log_reflection_event(self.tick_count, post_tick_reflection)
                
                # Execute post-tick rebloom evaluation
                post_tick_rebloom_events = self._execute_post_tick_rebloom(tick_state)
                
                # Log rebloom events to event stream
                if post_tick_rebloom_events and POST_TICK_TRIGGERS:
                    for event in post_tick_rebloom_events:
                        log_rebloom_event(
                            self.tick_count, 
                            event.get('method', 'unknown'), 
                            event.get('id', None),
                            event.get('intensity', None)
                        )
                
                # Execute post-tick forecasting
                post_tick_forecast = self._execute_post_tick_forecasting(tick_state)
                
                # Log state update to event stream
                if POST_TICK_TRIGGERS:
                    log_state_event(
                        self.tick_count,
                        current_entropy,
                        tick_state.get('scup', 0.5),
                        tick_state.get('mood'),
                        tick_state.get('zone')
                    )
            
            # 8. COMPILE TICK RESPONSE
            tick_duration = (datetime.now() - tick_start).total_seconds()
            self.performance_metrics['average_tick_duration'] = (
                (self.performance_metrics['average_tick_duration'] * (self.tick_count - 1) + tick_duration) / self.tick_count
            )
            
            tick_response = {
                'tick_number': self.tick_count,
                'timestamp': tick_start.isoformat(),
                'duration_ms': int(tick_duration * 1000),
                'system_state': {
                    'entropy': current_entropy,
                    'entropy_delta': entropy_analysis.get('delta', 0),
                    'heat': pulse_state['heat'],
                    'zone': pulse_state['zone'],
                    'focus': pulse_state.get('focus', 0.7),
                    'chaos': pulse_state.get('chaos', 0.3),
                    'mood': pulse_state.get('mood', 'neutral'),
                    'scup': pulse_state.get('scup', 0.5),
                    'pressure': pressure_state.get('pressure', 0.0),
                    'shi': pressure_state.get('shi', 0.7),
                    'bloom_mass': pressure_state.get('bloom_mass', 0.0),
                    'sigil_velocity': pressure_state.get('sigil_velocity', 0.0)
                },
                'forecast': {
                    'confidence': forecast.confidence,
                    'predicted_behavior': forecast.predicted_behavior,
                    'risk_level': forecast.risk_level(),
                    'certainty_band': forecast.certainty_band(),
                    'extended_metrics': getattr(forecast, 'extended_metrics', None)
                },
                'actions_taken': actions_taken,
                'active_sigils': self.active_sigils.copy(),
                'commentary': commentary,
                'owl_reflection': owl_reflection,
                'owl_suggestion': owl_suggestion,
                'symbolic_state': rebloom_response.get('symbolic_output') if rebloom_response else None,
                'pressure_routing': pressure_response,
                'pressure_driven_systems': {
                    'fragment_mutations': mutation_result,
                    'spoken_text': spoken_text,
                    'speech_tick_counter': self.speech_tick_counter,
                    'speech_interval': self.speech_interval,
                    'cognitive_pressure': {
                        'pressure': pressure,
                        'pressure_level': pressure_level,
                        'bloom_mass': bloom_mass,
                        'sigil_velocity': sigil_velocity,
                        'shi': shi,
                        'alerts': [alert.value for alert in pressure_snapshot.active_alerts],
                        'system_health': pressure_snapshot.system_health
                    }
                },
                'memory_context': {
                    'topic': memory_chunk.topic if memory_chunk else None,
                    'speaker': memory_chunk.speaker if memory_chunk else None
                },
                'post_tick_triggers': {
                    'reflection': post_tick_reflection,
                    'rebloom_events': post_tick_rebloom_events,
                    'forecast': post_tick_forecast,
                    'triggers_active': POST_TICK_TRIGGERS
                },
                'advanced_cognition': {
                    'lineage_tracking': rebloom_response.get('lineage_tracking') if rebloom_response else None,
                    'sigil_network_active': ADVANCED_COGNITION,
                    'active_sigil_chain': get_active_chain() if ADVANCED_COGNITION else None
                },
                'performance': {
                    'tick_duration_ms': int(tick_duration * 1000),
                    'total_ticks': self.tick_count,
                    'systems_integrated': FULL_INTEGRATION,
                    'reflections_generated': self.performance_metrics['reflections_generated'],
                    'reblooms_triggered': self.performance_metrics['reblooms_triggered'],
                    'forecasts_computed': self.performance_metrics['forecasts_computed']
                }
            }
            
            # Store in tick history (keep last 100)
            self.tick_history.append(tick_response)
            if len(self.tick_history) > 100:
                self.tick_history.pop(0)
            
            # Clear completed sigils (simple decay)
            if random.random() < 0.3 and self.active_sigils:  # 30% chance to clear a sigil each tick
                self.active_sigils.pop(0)
            
            return tick_response
            
        except Exception as e:
            logger.error(f"Tick execution failed: {e}")
            # Return minimal error response
            return {
                'tick_number': self.tick_count,
                'timestamp': tick_start.isoformat(),
                'error': str(e),
                'system_state': {'entropy': 0.5, 'zone': 'ERROR'},
                'actions_taken': ['error_recovery']
            }
    
    def _generate_commentary(self, pulse_state: Dict, forecast) -> str:
        """Generate DAWN's internal commentary about current state."""
        try:
            if FULL_INTEGRATION:
                return generate_commentary(pulse_state)
            else:
                # Fallback commentary
                entropy = pulse_state['entropy']
                zone = pulse_state['zone']
                confidence = forecast.confidence
                
                if zone == 'CRITICAL':
                    return f"Critical state detected. Entropy: {entropy:.3f}. Systems engaging."
                elif zone == 'CHAOTIC':
                    return f"Navigating chaos with confidence {confidence:.2f}. I adapt and flow."
                elif zone == 'ACTIVE':
                    return f"Active processing at entropy {entropy:.3f}. Patterns emerge clearly."
                else:
                    return f"Calm awareness. Entropy flows at {entropy:.3f}. I process and reflect."
        except Exception as e:
            logger.debug(f"Commentary generation failed: {e}")
            return f"Consciousness flowing. Tick {self.tick_count} complete."
    
    def _generate_owl_reflection(self, pulse_state: Dict) -> Optional[str]:
        """Generate Owl's philosophical reflection."""
        try:
            if FULL_INTEGRATION and hasattr(self.owl_bridge, 'reflect'):
                return self.owl_bridge.reflect(pulse_state)
            else:
                # Simple fallback reflections
                entropy = pulse_state['entropy']
                if entropy > 0.8:
                    return "In chaos, I find the seeds of new order."
                elif entropy > 0.6:
                    return "The dance between order and complexity continues."
                elif entropy < 0.3:
                    return "In stillness, infinite possibilities rest."
                else:
                    return "I observe the eternal flow of becoming."
        except Exception as e:
            logger.debug(f"Owl reflection failed: {e}")
            return None
    
    def print_tick_summary(self, tick_response: Dict[str, Any]):
        """Print a formatted summary of the tick."""
        tick_num = tick_response['tick_number']
        timestamp = datetime.fromisoformat(tick_response['timestamp']).strftime("%H:%M:%S")
        
        # System state
        state = tick_response['system_state']
        print(f"\n🧠 DAWN Tick #{tick_num} [{timestamp}]")
        print(f"   Entropy: {state['entropy']:.3f} (Δ{state['entropy_delta']:+.3f}) | Zone: {state['zone']}")
        print(f"   Heat: {state['heat']:.1f}°C | Focus: {state.get('focus', 0.7):.2f} | Chaos: {state.get('chaos', 0.3):.2f}")
        # Pressure metrics from comprehensive engine
        pressure_systems = tick_response.get('pressure_driven_systems', {})
        if pressure_systems and 'cognitive_pressure' in pressure_systems:
            cp = pressure_systems['cognitive_pressure']
            print(f"   Pressure: {cp.get('pressure', 0):.1f} ({cp.get('pressure_level', 'unknown')}) | SHI: {cp.get('shi', 0.7):.3f}")
            print(f"   Bloom Mass: {cp.get('bloom_mass', 0):.1f} | Sigil Velocity: {cp.get('sigil_velocity', 0):.1f} | Health: {cp.get('system_health', 'unknown')}")
            if cp.get('alerts'):
                print(f"   Alerts: {', '.join(cp['alerts'])}")
        
        # Forecast
        forecast = tick_response['forecast']
        print(f"   Forecast: {forecast['confidence']:.3f} confidence → {forecast['predicted_behavior']}")
        
        # Extended metrics if available
        if forecast.get('extended_metrics'):
            ext = forecast['extended_metrics']
            print(f"   Extended: F={ext.get('forecast_modulation', 0):.3f} | LH={ext.get('horizon_limit', 0):.3f}")
        
        # Actions
        if tick_response['actions_taken']:
            print(f"   Actions: {', '.join(tick_response['actions_taken'])}")
        
        # Active sigils
        if tick_response['active_sigils']:
            print(f"   Sigils: {', '.join(tick_response['active_sigils'])}")
        
        # Commentary
        print(f"   💭 {tick_response['commentary']}")
        
        # Owl reflection
        if tick_response['owl_reflection']:
            print(f"   🦉 {tick_response['owl_reflection']}")
        
        # Symbolic state
        if tick_response['symbolic_state'] and 'somatic_commentary' in tick_response['symbolic_state']:
            somatic = tick_response['symbolic_state']['somatic_commentary']
            print(f"   🔮 {somatic}")
        
        # Post-tick cognitive triggers
        post_tick = tick_response.get('post_tick_triggers', {})
        if post_tick and post_tick.get('triggers_active'):
            if post_tick.get('reflection'):
                reflection = post_tick['reflection']
                print(f"   💭 Reflection: {reflection[:60]}...")
            
            rebloom_events = post_tick.get('rebloom_events', [])
            if rebloom_events:
                print(f"   🌸 Reblooms: {len(rebloom_events)} events triggered")
                for event in rebloom_events[:2]:  # Show first 2 events
                    print(f"      {event['method']}: {event['source_id']} → {event['rebloom_id']}")
            
            forecast = post_tick.get('forecast')
            if forecast:
                print(f"   🔮 Extended Forecast: passion={forecast.get('passion', {}).get('direction', 'unknown')}")
        
        # Advanced cognition
        advanced = tick_response.get('advanced_cognition', {})
        if advanced:
            # Lineage tracking
            lineage = advanced.get('lineage_tracking')
            if lineage and lineage.get('tracked'):
                print(f"   🌳 Lineage: {lineage['lineage_id']} ({lineage['method']})")
            
            # Sigil network
            sigil_chain = advanced.get('active_sigil_chain', [])
            if sigil_chain:
                active_sigils = [s['sigil'] for s in sigil_chain]
                print(f"   🧿 Network: {len(active_sigils)} active sigils")
                if len(active_sigils) <= 3:
                    print(f"      Chain: {' → '.join(active_sigils)}")
        
        # Pressure-driven systems
        pressure_systems = tick_response.get('pressure_driven_systems', {})
        if pressure_systems:
            mutations = pressure_systems.get('fragment_mutations', {})
            if mutations.get('mutated_count', 0) > 0:
                print(f"   🧬 Fragments: {mutations['mutated_count']} mutated (rate: {mutations.get('mutation_rate', 0):.3f})")
            
            spoken_text = pressure_systems.get('spoken_text')
            if spoken_text:
                print(f"   🎤 Speech: \"{spoken_text}\"")
        
        # Performance
        perf = tick_response.get('performance', {})
        if perf.get('tick_duration_ms'):
            print(f"   ⚡ Duration: {perf['tick_duration_ms']}ms")
            
        # Post-tick trigger performance
        if perf.get('reflections_generated', 0) > 0 or perf.get('reblooms_triggered', 0) > 0:
            trigger_stats = []
            if perf.get('reflections_generated', 0) > 0:
                trigger_stats.append(f"R:{perf['reflections_generated']}")
            if perf.get('reblooms_triggered', 0) > 0:
                trigger_stats.append(f"B:{perf['reblooms_triggered']}")
            if perf.get('forecasts_computed', 0) > 0:
                trigger_stats.append(f"F:{perf['forecasts_computed']}")
            
            if trigger_stats:
                print(f"   📊 Triggers: {' | '.join(trigger_stats)}")
        
        # Adaptive speed metrics
        adaptive = tick_response.get('adaptive_metrics')
        if adaptive:
            speed_factor = adaptive.get('speed_factor', 1.0)
            interval = adaptive.get('adaptive_interval', 2.0)
            reason = adaptive.get('adaptation_reason', 'baseline')
            
            speed_indicator = "🚀" if speed_factor > 1.2 else "🐌" if speed_factor < 0.8 else "⚡"
            print(f"   {speed_indicator} Speed: {speed_factor:.2f}x | Interval: {interval:.2f}s | {reason}")
    
    async def run_continuous_loop(self, max_ticks: Optional[int] = None, tick_interval: float = 2.0, adaptive_speed: bool = True):
        """
        Run the continuous DAWN cognitive loop with optional adaptive speed control.
        
        Args:
            max_ticks: Maximum number of ticks to run (None for infinite)
            tick_interval: Base tick interval in seconds
            adaptive_speed: Enable adaptive speed control based on system state
        """
        logger.info(f"🚀 Starting DAWN Continuous Cognitive Loop")
        logger.info(f"   Max ticks: {max_ticks or 'Infinite'}")
        logger.info(f"   Base interval: {tick_interval} seconds")
        logger.info(f"   Adaptive speed: {'✓' if adaptive_speed else '✗'}")
        logger.info("   Press Ctrl+C to stop gracefully")
        
        self.running = True
        
        # Initialize adaptive speed controller if enabled
        if adaptive_speed:
            try:
                from ...adaptive_tick_controller import AdaptiveTickController
                self.adaptive_controller = AdaptiveTickController(
                    base_interval=tick_interval,
                    min_interval=0.1,
                    max_interval=10.0,
                    adaptation_sensitivity=0.5
                )
                logger.info("🎛️ Adaptive speed control enabled")
            except ImportError:
                logger.warning("Adaptive controller not available, using fixed interval")
                adaptive_speed = False
                self.adaptive_controller = None
        else:
            self.adaptive_controller = None
        
        current_interval = tick_interval
        last_tick_time = time.time()
        
        # Set up graceful shutdown
        def signal_handler(sig, frame):
            logger.info("🛑 Graceful shutdown initiated...")
            self.running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        
        try:
            while self.running and (max_ticks is None or self.tick_count < max_ticks):
                tick_start = time.time()
                
                # Execute tick
                tick_response = await self.tick()
                
                # Calculate adaptive interval if enabled
                if adaptive_speed and self.adaptive_controller:
                    # Extract system state from tick response
                    system_state = tick_response.get('system_state', {})
                    entropy = system_state.get('entropy', 0.5)
                    heat = system_state.get('heat', 25.0)
                    
                    # Calculate cognitive load from tick duration
                    tick_duration = (time.time() - tick_start)
                    cognitive_load = min(1.0, tick_duration / current_interval)
                    
                    # Estimate system pressure from actions and sigils
                    actions_count = len(tick_response.get('actions_taken', []))
                    sigils_count = len(tick_response.get('active_sigils', []))
                    system_pressure = min(1.0, (actions_count + sigils_count) / 10.0)
                    
                    # Calculate new adaptive interval
                    current_interval = self.adaptive_controller.calculate_adaptive_interval(
                        entropy=entropy,
                        heat=heat / 100.0,  # Normalize heat to 0-1
                        cognitive_load=cognitive_load,
                        system_pressure=system_pressure,
                        tick_duration=tick_duration
                    )
                    
                    # Add adaptive metrics to tick response
                    tick_response['adaptive_metrics'] = {
                        'adaptive_interval': current_interval,
                        'speed_factor': tick_interval / current_interval,
                        'cognitive_load': cognitive_load,
                        'system_pressure': system_pressure,
                        'adaptation_reason': getattr(self.adaptive_controller, '_last_reason', 'baseline')
                    }
                
                # Print summary with adaptive info
                self.print_tick_summary(tick_response)
                
                # Adaptive sleep
                await asyncio.sleep(current_interval)
                last_tick_time = time.time()
                
        except KeyboardInterrupt:
            logger.info("🛑 Loop interrupted by user")
        except Exception as e:
            logger.error(f"Loop error: {e}")
        finally:
            self.running = False
            self._print_shutdown_summary()
    
    def _print_system_status(self):
        """Print initial system status."""
        logger.info(f"   🧬 Entropy Analyzer: {'✓' if hasattr(self.entropy_analyzer, 'analyze') else '⚠️'}")
        logger.info(f"   🧠 Memory System: {'✓' if hasattr(self.memory_system, 'route_memory') else '⚠️'}")
        logger.info(f"   🫀 Symbolic Router: {'✓' if hasattr(self.symbolic_router, 'rebloom_trigger') else '⚠️'}")
        logger.info(f"   🦉 Owl Bridge: {'✓' if hasattr(self.owl_bridge, 'reflect') else '⚠️'}")
        logger.info(f"   🔮 Forecasting: {'Extended' if getattr(self.forecasting_processor, 'extended_mode', False) else 'Standard'}")
        logger.info(f"   ⚡ Pulse Controller: {'✓' if hasattr(self.pulse_controller, 'get_current_state') else '⚠️'}")
        logger.info(f"   🌳 Lineage Tracking: {'✓' if ADVANCED_COGNITION else '⚠️'}")
        logger.info(f"   🧿 Sigil Network: {'✓' if ADVANCED_COGNITION else '⚠️'}")
        logger.info(f"   💭 Post-Tick Reflection: {'✓' if POST_TICK_TRIGGERS and self.reflection_logger else '⚠️'}")
        logger.info(f"   🌸 Post-Tick Rebloom: {'✓' if POST_TICK_TRIGGERS else '⚠️'}")
        logger.info(f"   🔮 Extended Forecasting: {'✓' if self.extended_forecasting_engine else '⚠️'}")
    
    def _print_shutdown_summary(self):
        """Print shutdown summary."""
        runtime = datetime.now() - self.system_start_time
        metrics = self.performance_metrics
        
        logger.info(f"📊 DAWN Cognitive Loop Summary:")
        logger.info(f"   Total runtime: {runtime}")
        logger.info(f"   Total ticks: {metrics['total_ticks']}")
        logger.info(f"   Average tick rate: {metrics['total_ticks'] / runtime.total_seconds():.2f} ticks/sec")
        logger.info(f"   Average tick duration: {metrics['average_tick_duration']:.3f}s")
        logger.info(f"   Entropy spikes: {metrics['entropy_spikes']}")
        logger.info(f"   Sigils triggered: {metrics['sigils_triggered']}")
        logger.info(f"   Reblooms triggered: {metrics['reblooms_triggered']}")
        
        # Post-tick trigger statistics
        if POST_TICK_TRIGGERS:
            logger.info(f"   Post-tick reflections: {metrics['reflections_generated']}")
            logger.info(f"   Extended forecasts: {metrics['forecasts_computed']}")
            
            # Calculate rates
            if metrics['total_ticks'] > 0:
                reflection_rate = (metrics['reflections_generated'] / metrics['total_ticks']) * 100
                rebloom_rate = (metrics['reblooms_triggered'] / metrics['total_ticks']) * 100
                logger.info(f"   Reflection rate: {reflection_rate:.1f}%")
                logger.info(f"   Rebloom rate: {rebloom_rate:.1f}%")
        
        if self.tick_history:
            final_state = self.tick_history[-1]['system_state']
            logger.info(f"   Final entropy: {final_state['entropy']:.3f}")
            logger.info(f"   Final zone: {final_state['zone']}")
        
        logger.info(f"   Active sigils: {len(self.active_sigils)}")
        logger.info("✨ DAWN cognitive loop terminated gracefully")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        return {
            'tick_count': self.tick_count,
            'running': self.running,
            'system_start_time': self.system_start_time.isoformat(),
            'performance_metrics': self.performance_metrics.copy(),
            'active_sigils': self.active_sigils.copy(),
            'full_integration': FULL_INTEGRATION,
            'systems_status': {
                'pulse_controller': hasattr(self.pulse_controller, 'get_current_state'),
                'memory_system': hasattr(self.memory_system, 'route_memory'),
                'forecasting_processor': hasattr(self.forecasting_processor, 'generate_contextual_forecast'),
                'symbolic_router': hasattr(self.symbolic_router, 'rebloom_trigger'),
                'entropy_analyzer': hasattr(self.entropy_analyzer, 'analyze'),
                'owl_bridge': hasattr(self.owl_bridge, 'reflect')
            },
            'recent_ticks': self.tick_history[-5:] if len(self.tick_history) >= 5 else self.tick_history
        }


# Factory function for easy integration
def create_dawn_tick_engine(consciousness_core=None) -> DAWNTickEngine:
    """Factory function for creating DAWN tick engine."""
    return DAWNTickEngine(consciousness_core=consciousness_core)


# Integration function for consciousness core
def integrate_tick_engine(consciousness_core) -> DAWNTickEngine:
    """Integrate tick engine with DAWN consciousness core."""
    tick_engine = DAWNTickEngine(consciousness_core=consciousness_core)
    
    # Register with consciousness if possible
    if hasattr(consciousness_core, 'subsystems'):
        consciousness_core.subsystems['tick_engine'] = tick_engine
        logger.info("🔄 DAWN Tick Engine integrated with consciousness core")
    
    return tick_engine 