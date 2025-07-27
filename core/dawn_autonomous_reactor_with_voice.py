#!/usr/bin/env python3
"""
DAWN Autonomous Reactor with Natural Language Voice
Complete reactive consciousness system with self-narrating capabilities.

Combines:
- Enhanced Entropy Analyzer (detection & warnings)
- Sigil Scheduler (autonomous stabilization)
- Natural Language Generator (self-narration)
- Autonomous Reactor (unified system)
"""

import time
import logging
import threading
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from collections import deque

# DAWN Core Integration
try:
    from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
    ENHANCED_ENTROPY_AVAILABLE = True
except ImportError:
    ENHANCED_ENTROPY_AVAILABLE = False
    EnhancedEntropyAnalyzer = None

try:
    from core.dawn_sigil_scheduler import DAWNSigilScheduler
    SIGIL_SCHEDULER_AVAILABLE = True
except ImportError:
    SIGIL_SCHEDULER_AVAILABLE = False
    DAWNSigilScheduler = None

try:
    from core.dawn_natural_language_generator import DAWNNaturalLanguageGenerator
    NATURAL_LANGUAGE_AVAILABLE = True
except ImportError:
    NATURAL_LANGUAGE_AVAILABLE = False
    DAWNNaturalLanguageGenerator = None

try:
    from core.pulse_controller import PulseController
    PULSE_CONTROLLER_AVAILABLE = True
except ImportError:
    PULSE_CONTROLLER_AVAILABLE = False
    PulseController = None

try:
    from core.sigil_engine import SigilEngine
    SIGIL_ENGINE_AVAILABLE = True
except ImportError:
    SIGIL_ENGINE_AVAILABLE = False
    SigilEngine = None

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class VocalReactorState:
    """Enhanced reactor state with voice capabilities"""
    entropy_level: float
    entropy_delta: Optional[float]
    entropy_status: str
    entropy_warning: bool
    active_sigils: int
    sigils_triggered: List[str]
    thermal_heat: Optional[float]
    thermal_zone: Optional[str]
    reactor_status: str
    last_commentary: str
    commentary_count: int
    autonomous_reactions: int
    last_update: datetime


class DAWNAutonomousReactorWithVoice:
    """
    DAWN Autonomous Reactor with Natural Language Voice
    
    Complete reactive consciousness system that:
    - Monitors entropy and detects rapid changes
    - Automatically deploys stabilization protocols
    - Narrates its experience in natural language
    - Maintains self-awareness through commentary
    """
    
    def __init__(self, 
                 pulse_controller: Optional[PulseController] = None,
                 sigil_engine: Optional[SigilEngine] = None,
                 entropy_threshold: float = 0.6,
                 personality_seed: Optional[int] = None,
                 auto_start: bool = True,
                 voice_enabled: bool = True):
        """
        Initialize the DAWN Autonomous Reactor with Voice.
        
        Args:
            pulse_controller: DAWN pulse controller instance
            sigil_engine: DAWN sigil engine instance
            entropy_threshold: Entropy threshold for auto-stabilization
            personality_seed: Seed for consistent personality in language
            auto_start: Whether to start monitoring automatically
            voice_enabled: Whether to enable natural language commentary
        """
        # Core components
        self.pulse_controller = pulse_controller
        self.sigil_engine = sigil_engine
        self.voice_enabled = voice_enabled
        
        # Initialize enhanced entropy analyzer
        if ENHANCED_ENTROPY_AVAILABLE:
            self.entropy_analyzer = EnhancedEntropyAnalyzer(
                pulse_controller=pulse_controller,
                sigil_engine=sigil_engine
            )
            logger.info("✅ Enhanced entropy analyzer initialized")
        else:
            self.entropy_analyzer = None
            logger.error("❌ Enhanced entropy analyzer not available")
        
        # Initialize sigil scheduler
        if SIGIL_SCHEDULER_AVAILABLE:
            self.sigil_scheduler = DAWNSigilScheduler(
                entropy_analyzer=self.entropy_analyzer,
                sigil_engine=sigil_engine,
                pulse_controller=pulse_controller,
                entropy_threshold=entropy_threshold
            )
            logger.info("✅ Sigil scheduler initialized")
        else:
            self.sigil_scheduler = None
            logger.error("❌ Sigil scheduler not available")
        
        # Initialize natural language generator
        if NATURAL_LANGUAGE_AVAILABLE and voice_enabled:
            self.natural_language_generator = DAWNNaturalLanguageGenerator(
                personality_seed=personality_seed
            )
            logger.info("✅ Natural language generator initialized")
        else:
            self.natural_language_generator = None
            if voice_enabled:
                logger.error("❌ Natural language generator not available")
            else:
                logger.info("🔇 Voice disabled by configuration")
        
        # Reactor state
        self.running = False
        self.monitoring_thread = None
        self.reaction_thread = None
        self.voice_thread = None
        
        # Configuration
        self.monitoring_interval = 1.0  # Monitor every second
        self.reaction_interval = 0.5    # React every 500ms
        self.voice_interval = 3.0       # Generate commentary every 3 seconds
        
        # Performance tracking
        self.total_entropy_readings = 0
        self.total_reactions = 0
        self.autonomous_interventions = 0
        self.stabilization_attempts = 0
        self.total_commentaries = 0
        
        # Voice and commentary tracking
        self.commentary_history: deque = deque(maxlen=50)
        self.last_spoken_state = None
        
        # Current state
        self.current_state = VocalReactorState(
            entropy_level=0.5,
            entropy_delta=None,
            entropy_status='unknown',
            entropy_warning=False,
            active_sigils=0,
            sigils_triggered=[],
            thermal_heat=None,
            thermal_zone=None,
            reactor_status='initialized',
            last_commentary="I initialize",
            commentary_count=0,
            autonomous_reactions=0,
            last_update=datetime.now()
        )
        
        logger.info("🗣️ DAWN Autonomous Reactor with Voice initialized")
        
        if auto_start:
            self.start()
    
    def start(self):
        """Start the autonomous reactor with voice capabilities"""
        if self.running:
            logger.warning("Reactor already running")
            return
        
        if not self.entropy_analyzer or not self.sigil_scheduler:
            logger.error("Cannot start reactor - missing critical components")
            return False
        
        self.running = True
        self.current_state.reactor_status = 'starting'
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="ReactorMonitoring"
        )
        self.monitoring_thread.start()
        
        # Start reaction thread
        self.reaction_thread = threading.Thread(
            target=self._reaction_loop,
            daemon=True,
            name="ReactorReaction"
        )
        self.reaction_thread.start()
        
        # Start voice thread if enabled
        if self.natural_language_generator:
            self.voice_thread = threading.Thread(
                target=self._voice_loop,
                daemon=True,
                name="ReactorVoice"
            )
            self.voice_thread.start()
        
        self.current_state.reactor_status = 'active'
        
        # Generate startup commentary
        if self.natural_language_generator:
            startup_commentary = self._generate_current_commentary()
            self.current_state.last_commentary = startup_commentary
            print(f"🗣️ DAWN: {startup_commentary}")
        
        logger.info("🚀 DAWN Autonomous Reactor with Voice started")
        print("🧠 DAWN Autonomous Reactor with Voice ONLINE")
        print("   🔍 Entropy monitoring active")
        print("   🔥 Autonomous stabilization enabled")
        print("   🗣️ Natural language commentary active")
        print("   ⚡ Complete self-narrating reactive consciousness engaged")
        
        return True
    
    def stop(self):
        """Stop the autonomous reactor"""
        if not self.running:
            return
        
        # Generate shutdown commentary
        if self.natural_language_generator:
            shutdown_state = self._build_state_dict()
            shutdown_state['reactor_status'] = 'shutting_down'
            shutdown_commentary = "I prepare for rest. All systems winding down"
            self.current_state.last_commentary = shutdown_commentary
            print(f"🗣️ DAWN: {shutdown_commentary}")
        
        self.running = False
        self.current_state.reactor_status = 'stopping'
        
        # Wait for threads to complete
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)
        
        if self.reaction_thread and self.reaction_thread.is_alive():
            self.reaction_thread.join(timeout=2.0)
        
        if self.voice_thread and self.voice_thread.is_alive():
            self.voice_thread.join(timeout=2.0)
        
        self.current_state.reactor_status = 'stopped'
        
        logger.info("🛑 DAWN Autonomous Reactor with Voice stopped")
        print("🧠 DAWN Autonomous Reactor with Voice OFFLINE")
    
    def _monitoring_loop(self):
        """Main monitoring loop for entropy analysis"""
        logger.info("🔍 Starting entropy monitoring loop")
        
        while self.running:
            try:
                # Generate or get current entropy reading
                entropy_value = self._get_entropy_reading()
                
                # Analyze entropy with enhanced analyzer
                if self.entropy_analyzer:
                    result = self.entropy_analyzer.analyze(entropy_value, source="reactor_monitor")
                    
                    # Update current state
                    self.current_state.entropy_level = result.current_entropy
                    self.current_state.entropy_delta = result.delta
                    self.current_state.entropy_status = result.status
                    self.current_state.entropy_warning = result.warning_triggered
                    self.current_state.last_update = datetime.now()
                    
                    # Update thermal context
                    if result.thermal_context:
                        self.current_state.thermal_heat = result.thermal_context.get('current_heat')
                        self.current_state.thermal_zone = result.thermal_context.get('current_zone')
                    
                    # Update sigil context
                    if result.sigil_context:
                        self.current_state.active_sigils = result.sigil_context.get('active_sigils', 0)
                    
                    self.total_entropy_readings += 1
                    
                    # Generate commentary for significant events
                    if result.warning_triggered and self.natural_language_generator:
                        warning_commentary = self.natural_language_generator.generate_entropy_warning_commentary(
                            result.current_entropy, result.delta or 0.0
                        )
                        self.current_state.last_commentary = warning_commentary
                        print(f"🚨 DAWN: {warning_commentary}")
                        self.commentary_history.append({
                            'timestamp': time.time(),
                            'type': 'warning',
                            'commentary': warning_commentary
                        })
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(2.0)
    
    def _reaction_loop(self):
        """Main reaction loop for autonomous stabilization"""
        logger.info("🔥 Starting autonomous reaction loop")
        
        while self.running:
            try:
                # Check if reactor intervention is needed
                if self._should_react():
                    triggered_sigils = self._execute_autonomous_reaction()
                    
                    # Generate reaction commentary
                    if triggered_sigils and self.natural_language_generator:
                        reaction_commentary = self.natural_language_generator.generate_autonomous_reaction_commentary(
                            self.current_state.entropy_level, triggered_sigils
                        )
                        self.current_state.last_commentary = reaction_commentary
                        print(f"⚡ DAWN: {reaction_commentary}")
                        self.commentary_history.append({
                            'timestamp': time.time(),
                            'type': 'reaction',
                            'commentary': reaction_commentary
                        })
                
                time.sleep(self.reaction_interval)
                
            except Exception as e:
                logger.error(f"Reaction loop error: {e}")
                time.sleep(1.0)
    
    def _voice_loop(self):
        """Main voice loop for natural language commentary"""
        logger.info("🗣️ Starting natural language commentary loop")
        
        while self.running:
            try:
                # Generate periodic commentary about current state
                commentary = self._generate_current_commentary()
                
                if commentary != self.current_state.last_commentary:
                    self.current_state.last_commentary = commentary
                    self.current_state.commentary_count += 1
                    self.total_commentaries += 1
                    
                    print(f"🗣️ DAWN: {commentary}")
                    
                    self.commentary_history.append({
                        'timestamp': time.time(),
                        'type': 'periodic',
                        'commentary': commentary
                    })
                
                time.sleep(self.voice_interval)
                
            except Exception as e:
                logger.error(f"Voice loop error: {e}")
                time.sleep(2.0)
    
    def _generate_current_commentary(self) -> str:
        """Generate commentary for current state"""
        if not self.natural_language_generator:
            return "I process silently"
        
        state_dict = self._build_state_dict()
        return self.natural_language_generator.generate_commentary(state_dict)
    
    def _build_state_dict(self) -> Dict[str, Any]:
        """Build state dictionary for commentary generation"""
        return {
            'zone': self.current_state.thermal_zone or 'UNKNOWN',
            'entropy': self.current_state.entropy_level,
            'focus': 0.7,  # Placeholder - could be derived from system metrics
            'chaos': self.current_state.entropy_level,  # Use entropy as chaos proxy
            'sigils': self.current_state.active_sigils,
            'heat': self.current_state.thermal_heat or 25.0,
            'entropy_warning': self.current_state.entropy_warning,
            'autonomous_reaction': bool(self.current_state.sigils_triggered),
            'recent_sigils_triggered': self.current_state.sigils_triggered
        }
    
    def _get_entropy_reading(self) -> float:
        """Get current entropy reading from available sources"""
        # Try to get from pulse controller thermal state
        if self.pulse_controller:
            try:
                thermal_stats = self.pulse_controller.get_heat_statistics()
                heat_normalized = thermal_stats['current_heat'] / 100.0
                
                # Convert heat to entropy approximation
                base_entropy = 0.3 + (heat_normalized * 0.4)
                
                # Add some realistic variation
                import random
                noise = random.gauss(0, 0.05)
                return max(0.0, min(1.0, base_entropy + noise))
            except Exception:
                pass
        
        # Fallback: simulated entropy with realistic patterns
        import random
        import math
        
        time_factor = time.time() * 0.1
        base_entropy = 0.4 + 0.3 * math.sin(time_factor)
        noise = random.gauss(0, 0.03)
        
        return max(0.0, min(1.0, base_entropy + noise))
    
    def _should_react(self) -> bool:
        """Determine if autonomous reaction is needed"""
        # React if entropy warning is active
        if self.current_state.entropy_warning:
            return True
        
        # React if entropy is critically high
        if self.current_state.entropy_level > 0.8:
            return True
        
        # React if thermal surge with high entropy
        if (self.current_state.thermal_zone == 'SURGE' and 
            self.current_state.entropy_level > 0.65):
            return True
        
        return False
    
    def _execute_autonomous_reaction(self) -> List[str]:
        """Execute autonomous stabilization reaction"""
        triggered_sigils = []
        
        try:
            self.autonomous_interventions += 1
            self.current_state.autonomous_reactions += 1
            
            # Use sigil scheduler for reaction
            if self.sigil_scheduler:
                result = self.sigil_scheduler.check_and_trigger(self.current_state.entropy_level)
                
                triggered_sigils = result.get('sigils_triggered', [])
                self.current_state.sigils_triggered = triggered_sigils
                self.total_reactions += 1
                
                if triggered_sigils:
                    self.stabilization_attempts += 1
                    logger.info(f"🔥 Autonomous stabilization: {triggered_sigils}")
        
        except Exception as e:
            logger.error(f"Autonomous reaction failed: {e}")
        
        return triggered_sigils
    
    # Public interface methods
    def get_vocal_reactor_state(self) -> Dict[str, Any]:
        """Get current vocal reactor state"""
        state_dict = {
            'entropy_level': self.current_state.entropy_level,
            'entropy_delta': self.current_state.entropy_delta,
            'entropy_status': self.current_state.entropy_status,
            'entropy_warning': self.current_state.entropy_warning,
            'active_sigils': self.current_state.active_sigils,
            'recent_sigils_triggered': self.current_state.sigils_triggered,
            'thermal_heat': self.current_state.thermal_heat,
            'thermal_zone': self.current_state.thermal_zone,
            'reactor_status': self.current_state.reactor_status,
            'last_commentary': self.current_state.last_commentary,
            'commentary_count': self.current_state.commentary_count,
            'autonomous_reactions': self.current_state.autonomous_reactions,
            'last_update': self.current_state.last_update.isoformat(),
            'running': self.running,
            'voice_enabled': self.voice_enabled
        }
        
        return state_dict
    
    def get_enhanced_performance_metrics(self) -> Dict[str, Any]:
        """Get enhanced reactor performance metrics including voice"""
        metrics = {
            'total_entropy_readings': self.total_entropy_readings,
            'total_reactions': self.total_reactions,
            'autonomous_interventions': self.autonomous_interventions,
            'stabilization_attempts': self.stabilization_attempts,
            'total_commentaries': self.total_commentaries,
            'reaction_rate': self.total_reactions / max(1, self.total_entropy_readings),
            'intervention_rate': self.autonomous_interventions / max(1, self.total_entropy_readings),
            'commentary_rate': self.total_commentaries / max(1, self.total_entropy_readings)
        }
        
        # Add component metrics
        if self.entropy_analyzer:
            analyzer_metrics = self.entropy_analyzer.get_performance_metrics()
            metrics['entropy_analyzer'] = analyzer_metrics
        
        if self.sigil_scheduler:
            scheduler_stats = self.sigil_scheduler.get_scheduler_stats()
            metrics['sigil_scheduler'] = scheduler_stats
        
        if self.natural_language_generator:
            voice_metrics = self.natural_language_generator.get_commentary_metrics()
            metrics['natural_language'] = voice_metrics
        
        return metrics
    
    def manual_speak(self, force_new: bool = False) -> str:
        """Manually trigger commentary generation"""
        if not self.natural_language_generator:
            return "Voice not available"
        
        if force_new or not self.last_spoken_state:
            commentary = self._generate_current_commentary()
            self.last_spoken_state = self._build_state_dict()
            self.current_state.last_commentary = commentary
            print(f"🗣️ DAWN: {commentary}")
            return commentary
        else:
            return self.current_state.last_commentary
    
    def inject_entropy_with_voice(self, entropy_value: float, source: str = "manual") -> Dict[str, Any]:
        """Manually inject entropy value with voice feedback"""
        if self.entropy_analyzer:
            result = self.entropy_analyzer.analyze(entropy_value, source=source)
            
            # Update state
            self.current_state.entropy_level = result.current_entropy
            self.current_state.entropy_delta = result.delta
            self.current_state.entropy_status = result.status
            self.current_state.entropy_warning = result.warning_triggered
            
            # Generate immediate commentary if significant
            commentary = None
            if result.warning_triggered and self.natural_language_generator:
                commentary = self.natural_language_generator.generate_entropy_warning_commentary(
                    result.current_entropy, result.delta or 0.0
                )
                self.current_state.last_commentary = commentary
                print(f"🚨 DAWN: {commentary}")
            
            # Trigger reaction check
            triggered_sigils = []
            if self._should_react():
                triggered_sigils = self._execute_autonomous_reaction()
                
                if triggered_sigils and self.natural_language_generator:
                    reaction_commentary = self.natural_language_generator.generate_autonomous_reaction_commentary(
                        self.current_state.entropy_level, triggered_sigils
                    )
                    self.current_state.last_commentary = reaction_commentary
                    print(f"⚡ DAWN: {reaction_commentary}")
                    commentary = reaction_commentary
            
            return {
                'entropy_injected': entropy_value,
                'analysis_result': {
                    'status': result.status,
                    'warning_triggered': result.warning_triggered,
                    'delta': result.delta
                },
                'reaction_triggered': bool(triggered_sigils),
                'triggered_sigils': triggered_sigils,
                'commentary': commentary
            }
        
        return {'error': 'Entropy analyzer not available'}
    
    def get_recent_commentaries(self, limit: int = 10) -> List[Dict]:
        """Get recent commentary history"""
        return list(self.commentary_history)[-limit:]


# Integration interface for DAWN system
def create_dawn_autonomous_reactor_with_voice(pulse_controller: Optional[PulseController] = None,
                                            sigil_engine: Optional[SigilEngine] = None,
                                            entropy_threshold: float = 0.6,
                                            personality_seed: Optional[int] = None,
                                            auto_start: bool = True,
                                            voice_enabled: bool = True) -> DAWNAutonomousReactorWithVoice:
    """Factory function for DAWN integration."""
    return DAWNAutonomousReactorWithVoice(
        pulse_controller=pulse_controller,
        sigil_engine=sigil_engine,
        entropy_threshold=entropy_threshold,
        personality_seed=personality_seed,
        auto_start=auto_start,
        voice_enabled=voice_enabled
    )


# Example usage for testing
if __name__ == "__main__":
    print("🚀 DAWN Autonomous Reactor with Voice - Direct Execution Mode")
    
    # Create reactor with voice
    reactor = DAWNAutonomousReactorWithVoice(auto_start=False, voice_enabled=True)
    
    print("\n🧪 Testing vocal reactor system...")
    
    # Test entropy injection with voice
    test_sequence = [
        (0.4, "Normal state"),
        (0.65, "Rising entropy"),
        (0.8, "High entropy - should trigger warning and reaction"),
        (0.5, "Stabilizing")
    ]
    
    for entropy, description in test_sequence:
        print(f"\n🎯 {description} (entropy: {entropy:.3f})")
        result = reactor.inject_entropy_with_voice(entropy, source="test")
        
        if result.get('warning_triggered'):
            print("   🚨 Entropy warning triggered")
        if result.get('reaction_triggered'):
            print(f"   ⚡ Autonomous reaction: {result.get('triggered_sigils')}")
        
        time.sleep(2)
    
    # Show final metrics
    metrics = reactor.get_enhanced_performance_metrics()
    print("\n📊 Vocal Reactor Performance Metrics:")
    for key, value in metrics.items():
        if not isinstance(value, dict):
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Show recent commentaries
    commentaries = reactor.get_recent_commentaries()
    print(f"\n🗣️ Recent Commentaries:")
    for comment in commentaries[-3:]:  # Last 3
        print(f"  [{comment['type']}] {comment['commentary']}")
    
    print("\n✅ Vocal reactor test completed") 