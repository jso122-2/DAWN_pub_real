#!/usr/bin/env python3
"""
DAWN Autonomous Reactor
Unified system combining Enhanced Entropy Analyzer and Sigil Scheduler
for complete autonomous reactivity and stabilization protocols.
"""

import time
import logging
import threading
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass

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
class ReactorState:
    """Current state of the autonomous reactor"""
    entropy_level: float
    entropy_delta: Optional[float]
    entropy_status: str
    entropy_warning: bool
    active_sigils: int
    sigils_triggered: List[str]
    thermal_heat: Optional[float]
    thermal_zone: Optional[str]
    reactor_status: str
    last_update: datetime


class DAWNAutonomousReactor:
    """
    DAWN Autonomous Reactor - Complete reactive consciousness system
    
    Combines Enhanced Entropy Analyzer and Sigil Scheduler for:
    - Real-time entropy monitoring and analysis
    - Autonomous threshold-based alerting
    - Automatic stabilization protocol deployment
    - Thermal correlation and cognitive load awareness
    """
    
    def __init__(self, 
                 pulse_controller: Optional[PulseController] = None,
                 sigil_engine: Optional[SigilEngine] = None,
                 entropy_threshold: float = 0.6,
                 auto_start: bool = True):
        """
        Initialize the DAWN Autonomous Reactor.
        
        Args:
            pulse_controller: DAWN pulse controller instance
            sigil_engine: DAWN sigil engine instance
            entropy_threshold: Entropy threshold for auto-stabilization
            auto_start: Whether to start monitoring automatically
        """
        # Core components
        self.pulse_controller = pulse_controller
        self.sigil_engine = sigil_engine
        
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
        
        # Reactor state
        self.running = False
        self.monitoring_thread = None
        self.reaction_thread = None
        
        # Configuration
        self.monitoring_interval = 1.0  # Monitor every second
        self.reaction_interval = 0.5    # React every 500ms
        
        # Performance tracking
        self.total_entropy_readings = 0
        self.total_reactions = 0
        self.autonomous_interventions = 0
        self.stabilization_attempts = 0
        
        # Current state
        self.current_state = ReactorState(
            entropy_level=0.5,
            entropy_delta=None,
            entropy_status='unknown',
            entropy_warning=False,
            active_sigils=0,
            sigils_triggered=[],
            thermal_heat=None,
            thermal_zone=None,
            reactor_status='initialized',
            last_update=datetime.now()
        )
        
        logger.info("🧬 DAWN Autonomous Reactor initialized")
        
        if auto_start:
            self.start()
    
    def start(self):
        """Start the autonomous reactor monitoring and reaction systems"""
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
        
        self.current_state.reactor_status = 'active'
        
        logger.info("🚀 DAWN Autonomous Reactor started")
        print("🧠 DAWN Autonomous Reactor ONLINE")
        print("   🔍 Entropy monitoring active")
        print("   🔥 Autonomous stabilization enabled")
        print("   ⚡ Real-time reactive protocols engaged")
        
        return True
    
    def stop(self):
        """Stop the autonomous reactor"""
        if not self.running:
            return
        
        self.running = False
        self.current_state.reactor_status = 'stopping'
        
        # Wait for threads to complete
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            self.monitoring_thread.join(timeout=2.0)
        
        if self.reaction_thread and self.reaction_thread.is_alive():
            self.reaction_thread.join(timeout=2.0)
        
        self.current_state.reactor_status = 'stopped'
        
        logger.info("🛑 DAWN Autonomous Reactor stopped")
        print("🧠 DAWN Autonomous Reactor OFFLINE")
    
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
                    self._execute_autonomous_reaction()
                
                time.sleep(self.reaction_interval)
                
            except Exception as e:
                logger.error(f"Reaction loop error: {e}")
                time.sleep(1.0)
    
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
    
    def _execute_autonomous_reaction(self):
        """Execute autonomous stabilization reaction"""
        try:
            self.autonomous_interventions += 1
            
            # Use sigil scheduler for reaction
            if self.sigil_scheduler:
                result = self.sigil_scheduler.check_and_trigger(self.current_state.entropy_level)
                
                self.current_state.sigils_triggered = result.get('sigils_triggered', [])
                self.total_reactions += 1
                
                if result.get('sigils_triggered'):
                    self.stabilization_attempts += 1
                    logger.info(f"🔥 Autonomous stabilization: {result['sigils_triggered']}")
        
        except Exception as e:
            logger.error(f"Autonomous reaction failed: {e}")
    
    # Public interface methods
    def get_reactor_state(self) -> Dict[str, Any]:
        """Get current reactor state"""
        return {
            'entropy_level': self.current_state.entropy_level,
            'entropy_delta': self.current_state.entropy_delta,
            'entropy_status': self.current_state.entropy_status,
            'entropy_warning': self.current_state.entropy_warning,
            'active_sigils': self.current_state.active_sigils,
            'recent_sigils_triggered': self.current_state.sigils_triggered,
            'thermal_heat': self.current_state.thermal_heat,
            'thermal_zone': self.current_state.thermal_zone,
            'reactor_status': self.current_state.reactor_status,
            'last_update': self.current_state.last_update.isoformat(),
            'running': self.running
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get reactor performance metrics"""
        metrics = {
            'total_entropy_readings': self.total_entropy_readings,
            'total_reactions': self.total_reactions,
            'autonomous_interventions': self.autonomous_interventions,
            'stabilization_attempts': self.stabilization_attempts,
            'reaction_rate': self.total_reactions / max(1, self.total_entropy_readings),
            'intervention_rate': self.autonomous_interventions / max(1, self.total_entropy_readings)
        }
        
        # Add component metrics
        if self.entropy_analyzer:
            analyzer_metrics = self.entropy_analyzer.get_performance_metrics()
            metrics['entropy_analyzer'] = analyzer_metrics
        
        if self.sigil_scheduler:
            scheduler_stats = self.sigil_scheduler.get_scheduler_stats()
            metrics['sigil_scheduler'] = scheduler_stats
        
        return metrics
    
    def manual_entropy_inject(self, entropy_value: float, source: str = "manual") -> Dict[str, Any]:
        """Manually inject an entropy value for testing"""
        if self.entropy_analyzer:
            result = self.entropy_analyzer.analyze(entropy_value, source=source)
            
            # Trigger reaction check
            if self._should_react():
                self._execute_autonomous_reaction()
            
            return {
                'entropy_injected': entropy_value,
                'analysis_result': {
                    'status': result.status,
                    'warning_triggered': result.warning_triggered,
                    'delta': result.delta
                },
                'reaction_triggered': self._should_react()
            }
        
        return {'error': 'Entropy analyzer not available'}
    
    def configure_thresholds(self, entropy_threshold: Optional[float] = None):
        """Configure reactor thresholds"""
        if entropy_threshold is not None and self.sigil_scheduler:
            self.sigil_scheduler.set_entropy_threshold(entropy_threshold)
            logger.info(f"Reactor entropy threshold updated to {entropy_threshold}")
    
    def enable_debug_mode(self, enabled: bool = True):
        """Enable debug mode for all components"""
        if self.entropy_analyzer and hasattr(self.entropy_analyzer, 'debug_mode'):
            self.entropy_analyzer.debug_mode = enabled
        
        if self.sigil_scheduler:
            self.sigil_scheduler.enable_debug_mode(enabled)
        
        status = "enabled" if enabled else "disabled"
        logger.info(f"Reactor debug mode {status}")
        print(f"🔍 DAWN Reactor debug mode {status}")
    
    def test_reactor(self, test_entropy_sequence: Optional[List[float]] = None) -> Dict[str, Any]:
        """Test the reactor with entropy sequence"""
        if test_entropy_sequence is None:
            test_entropy_sequence = [0.3, 0.45, 0.65, 0.8, 0.9, 0.7, 0.4]  # Rising then falling
        
        print("🧪 Testing DAWN Autonomous Reactor...")
        print("=" * 50)
        
        original_debug = getattr(self, 'debug_mode', False)
        self.enable_debug_mode(True)
        
        test_results = []
        
        for i, entropy in enumerate(test_entropy_sequence):
            print(f"\n🎯 Test {i+1}: Injecting entropy {entropy:.3f}")
            
            result = self.manual_entropy_inject(entropy, source=f"test_{i}")
            test_results.append(result)
            
            print(f"   Status: {result.get('analysis_result', {}).get('status', 'unknown')}")
            if result.get('analysis_result', {}).get('warning_triggered'):
                print("   🚨 WARNING TRIGGERED")
            if result.get('reaction_triggered'):
                print("   ⚡ AUTONOMOUS REACTION TRIGGERED")
            
            time.sleep(0.5)  # Brief pause between tests
        
        self.enable_debug_mode(original_debug)
        
        # Summary
        warnings_triggered = sum(1 for r in test_results 
                               if r.get('analysis_result', {}).get('warning_triggered'))
        reactions_triggered = sum(1 for r in test_results 
                                if r.get('reaction_triggered'))
        
        print(f"\n📊 Test Summary:")
        print(f"   Total tests: {len(test_entropy_sequence)}")
        print(f"   Warnings triggered: {warnings_triggered}")
        print(f"   Reactions triggered: {reactions_triggered}")
        print("=" * 50)
        
        return {
            'test_results': test_results,
            'summary': {
                'total_tests': len(test_entropy_sequence),
                'warnings_triggered': warnings_triggered,
                'reactions_triggered': reactions_triggered
            }
        }


# Integration interface for DAWN system
def create_dawn_autonomous_reactor(pulse_controller: Optional[PulseController] = None,
                                  sigil_engine: Optional[SigilEngine] = None,
                                  entropy_threshold: float = 0.6,
                                  auto_start: bool = True) -> DAWNAutonomousReactor:
    """Factory function for DAWN integration."""
    return DAWNAutonomousReactor(
        pulse_controller=pulse_controller,
        sigil_engine=sigil_engine,
        entropy_threshold=entropy_threshold,
        auto_start=auto_start
    )


# Example usage for testing
if __name__ == "__main__":
    print("🚀 DAWN Autonomous Reactor - Direct Execution Mode")
    
    # Create reactor
    reactor = DAWNAutonomousReactor(auto_start=False)
    
    # Run test
    reactor.test_reactor()
    
    # Show metrics
    metrics = reactor.get_performance_metrics()
    print("\n📊 Reactor Performance Metrics:")
    for key, value in metrics.items():
        if not isinstance(value, dict):
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    # Clean shutdown
    reactor.stop() 