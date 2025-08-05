#!/usr/bin/env python3
"""
Enhanced DAWN Autonomous Reactor - Integrated Expression System
===============================================================

Enhanced autonomous reactor that integrates voice and visual expression systems
into DAWN's main cognitive processing loop. This creates a unified cognitive system
where DAWN's internal state automatically generates both voice expressions and visual
sigil traces during real-time processing.

Features:
- Seamless integration with existing DAWN cognitive systems
- Real-time expression monitoring and generation
- Coordinated voice and visual output
- Expression archiving and retrieval
- Adaptive expression sensitivity tuning
- Performance monitoring and optimization
"""

import asyncio
import time
import threading
import logging
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json

# Import DAWN core systems
try:
    from core.dawn_autonomous_reactor import DAWNAutonomousReactor
    DAWN_REACTOR_AVAILABLE = True
except ImportError:
    DAWN_REACTOR_AVAILABLE = False
    print("⚠️ Base DAWN Autonomous Reactor not available")

try:
    from core.sigil_engine import SigilEngine
    SIGIL_ENGINE_AVAILABLE = True
except ImportError:
    SIGIL_ENGINE_AVAILABLE = False
    print("⚠️ Sigil Engine not available")

try:
    from pulse.pulse_controller import PulseController
    PULSE_CONTROLLER_AVAILABLE = True
except ImportError:
    PULSE_CONTROLLER_AVAILABLE = False
    print("⚠️ Pulse Controller not available")

# Import expression systems
try:
    from core.dawn_expression_system import (
        DAWNExpressionMonitor, DAWNExpressionArchive, 
        DAWNState, DAWNExpression
    )
    EXPRESSION_SYSTEM_AVAILABLE = True
except ImportError:
    try:
        from dawn_expression_system import (
            DAWNExpressionMonitor, DAWNExpressionArchive, 
            DAWNState, DAWNExpression
        )
        EXPRESSION_SYSTEM_AVAILABLE = True
    except ImportError:
        EXPRESSION_SYSTEM_AVAILABLE = False
        print("⚠️ DAWN Expression System not available")

try:
    from dawn_voice_core import DAWNVoiceCore
    VOICE_CORE_AVAILABLE = True
except ImportError:
    VOICE_CORE_AVAILABLE = False
    print("⚠️ DAWN Voice Core not available")

try:
    from core.sigil_visual_engine import SigilVisualEngine
    VISUAL_ENGINE_AVAILABLE = True
except ImportError:
    try:
        from sigil_visual_engine import SigilVisualEngine
        VISUAL_ENGINE_AVAILABLE = True
    except ImportError:
        VISUAL_ENGINE_AVAILABLE = False
        print("⚠️ Sigil Visual Engine not available")

try:
    from core.enhanced_dawn_pigment_dictionary import get_enhanced_dawn_pigment_dictionary
    ENHANCED_PIGMENT_AVAILABLE = True
except ImportError:
    try:
        from enhanced_dawn_pigment_dictionary import get_enhanced_dawn_pigment_dictionary
        ENHANCED_PIGMENT_AVAILABLE = True
    except ImportError:
        ENHANCED_PIGMENT_AVAILABLE = False
        print("⚠️ Enhanced Pigment Dictionary not available")

logger = logging.getLogger("enhanced_dawn_reactor")

@dataclass
class ReactorPerformanceMetrics:
    """Performance tracking for the enhanced reactor"""
    # Processing metrics
    total_cycles: int = 0
    average_cycle_time: float = 0.0
    expression_generation_time: float = 0.0
    
    # Expression metrics
    total_expressions: int = 0
    voice_expressions: int = 0
    visual_expressions: int = 0
    average_coherence: float = 0.0
    
    # Trigger statistics
    trigger_counts: Dict[str, int] = field(default_factory=dict)
    
    # Performance health
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    last_update: float = 0.0

class EnhancedDAWNAutonomousReactor:
    """
    Enhanced DAWN autonomous reactor with integrated expression system
    
    Extends the base autonomous reactor with coordinated voice and visual expression
    capabilities while maintaining seamless integration with existing systems.
    """
    
    def __init__(self, 
                 expression_config: Optional[Dict] = None,
                 performance_monitoring: bool = True,
                 archive_expressions: bool = True):
        
        # Initialize base systems
        self.running = False
        self.performance_monitoring = performance_monitoring
        self.archive_expressions = archive_expressions
        
        # Core DAWN components
        self.pulse_controller: Optional[PulseController] = None
        self.sigil_engine: Optional[SigilEngine] = None
        self.entropy_analyzer = None
        self.schema_processor = None
        
        # Expression system components
        self.expression_monitor: Optional[DAWNExpressionMonitor] = None
        self.expression_archive: Optional[DAWNExpressionArchive] = None
        self.voice_core: Optional[DAWNVoiceCore] = None
        self.visual_engine: Optional[SigilVisualEngine] = None
        
        # State tracking
        self.current_dawn_state: Optional[DAWNState] = None
        self.current_expression: Optional[DAWNExpression] = None
        self.expression_history: List[DAWNExpression] = []
        
        # Performance monitoring
        self.performance_metrics = ReactorPerformanceMetrics()
        self.cycle_times = []
        
        # Threading
        self.main_thread: Optional[threading.Thread] = None
        self.expression_thread: Optional[threading.Thread] = None
        
        # Initialize all systems
        self._initialize_systems(expression_config)
        
        logger.info("🧠✨ Enhanced DAWN Autonomous Reactor initialized")
    
    def _initialize_systems(self, expression_config: Optional[Dict]):
        """Initialize all DAWN subsystems and expression components"""
        
        try:
            # Initialize core DAWN systems
            if PULSE_CONTROLLER_AVAILABLE:
                self.pulse_controller = PulseController(initial_heat=25.0)
                logger.info("🔥 Pulse Controller initialized")
            
            if SIGIL_ENGINE_AVAILABLE:
                self.sigil_engine = SigilEngine()
                logger.info("🔮 Sigil Engine initialized")
            
            # Initialize expression systems
            if EXPRESSION_SYSTEM_AVAILABLE:
                self.expression_monitor = DAWNExpressionMonitor(expression_config)
                logger.info("🎭 Expression Monitor initialized")
                
                if self.archive_expressions:
                    self.expression_archive = DAWNExpressionArchive()
                    logger.info("📚 Expression Archive initialized")
            
            if VOICE_CORE_AVAILABLE:
                self.voice_core = DAWNVoiceCore()
                logger.info("🗣️ Voice Core initialized")
            
            if VISUAL_ENGINE_AVAILABLE:
                self.visual_engine = SigilVisualEngine()
                logger.info("🎨 Visual Engine initialized")
            
            # Check system readiness
            self._validate_system_readiness()
            
        except Exception as e:
            logger.error(f"Failed to initialize systems: {e}")
            raise
    
    def _validate_system_readiness(self):
        """Validate that essential systems are ready"""
        
        essential_systems = [
            (self.pulse_controller, "Pulse Controller"),
            (self.sigil_engine, "Sigil Engine"),
            (self.expression_monitor, "Expression Monitor")
        ]
        
        missing_systems = []
        for system, name in essential_systems:
            if system is None:
                missing_systems.append(name)
        
        if missing_systems:
            logger.warning(f"Missing essential systems: {', '.join(missing_systems)}")
            logger.warning("Reactor will run with limited capabilities")
        else:
            logger.info("✅ All essential systems ready")
    
    async def start(self):
        """Start the enhanced autonomous reactor"""
        
        if self.running:
            logger.warning("Enhanced reactor already running")
            return False
        
        self.running = True
        logger.info("🚀 Starting Enhanced DAWN Autonomous Reactor...")
        
        try:
            # Start the main processing loop
            await self.enhanced_autonomous_cycle_loop()
            
        except Exception as e:
            logger.error(f"Error in reactor main loop: {e}")
            self.running = False
            raise
        
        return True
    
    def stop(self):
        """Stop the enhanced autonomous reactor"""
        
        self.running = False
        logger.info("🛑 Stopping Enhanced DAWN Autonomous Reactor...")
        
        # Stop any background threads
        if self.main_thread and self.main_thread.is_alive():
            self.main_thread.join(timeout=5.0)
        
        if self.expression_thread and self.expression_thread.is_alive():
            self.expression_thread.join(timeout=5.0)
        
        logger.info("✅ Enhanced reactor stopped")
    
    async def enhanced_autonomous_cycle_loop(self):
        """Main processing loop with expression integration"""
        
        logger.info("🔄 Enhanced autonomous cycle loop started")
        
        while self.running:
            try:
                cycle_start = time.time()
                
                # Execute enhanced cognitive cycle
                cycle_result = await self.enhanced_autonomous_cycle()
                
                # Update performance metrics
                cycle_duration = time.time() - cycle_start
                self._update_performance_metrics(cycle_duration, cycle_result)
                
                # Log periodic status
                if self.performance_metrics.total_cycles % 10 == 0:
                    self._log_reactor_status()
                
                # Dynamic sleep based on system load and expression activity
                sleep_time = self._calculate_dynamic_sleep_time(cycle_duration, cycle_result)
                await asyncio.sleep(sleep_time)
                
            except Exception as e:
                logger.error(f"Error in enhanced cycle loop: {e}")
                await asyncio.sleep(1.0)  # Brief pause before retry
        
        logger.info("🔄 Enhanced autonomous cycle loop stopped")
    
    async def enhanced_autonomous_cycle(self) -> Dict[str, Any]:
        """
        Enhanced autonomous processing cycle with expression integration
        
        This is the core method that integrates expression generation with
        standard DAWN cognitive processing.
        """
        
        cycle_start = time.time()
        
        # 1. Execute standard DAWN cognitive processing
        schema_state = await self._process_schema_updates()
        sigil_results = await self._execute_pending_sigils()
        entropy_state = await self._calculate_entropy_drift()
        
        # 2. Prepare DAWN state for expression system
        current_dawn_state = self._prepare_dawn_state(
            schema_state, sigil_results, entropy_state
        )
        
        # 3. Check expression triggers and generate if needed
        expression_result = None
        if self.expression_monitor:
            expression_result = self.expression_monitor.update_state(current_dawn_state)
        
        # 4. Handle expression generation (if triggered)
        if expression_result:
            await self._handle_expression_generation(expression_result, current_dawn_state)
        
        # 5. Update reactor state
        self.current_dawn_state = current_dawn_state
        self.current_expression = expression_result
        
        # 6. Return enhanced cycle results
        return {
            'schema_state': schema_state,
            'sigil_results': sigil_results,
            'entropy_state': entropy_state,
            'dawn_state': current_dawn_state,
            'expression': expression_result,
            'cycle_time': time.time() - cycle_start,
            'cognitive_coherence': self._calculate_overall_coherence(current_dawn_state, expression_result)
        }
    
    async def _process_schema_updates(self) -> Dict[str, Any]:
        """Process schema updates (placeholder for integration with actual schema system)"""
        
        # This would integrate with DAWN's actual schema processing system
        # For now, return mock schema state
        return {
            'pigment': self._get_current_mood_pigment(),
            'pulse_zone': self._get_current_pulse_zone(),
            'saturation': self._get_current_saturation(),
            'rebloom_depth': self._get_current_rebloom_depth()
        }
    
    async def _execute_pending_sigils(self) -> Dict[str, Any]:
        """Execute pending sigils and collect results"""
        
        if not self.sigil_engine:
            return {
                'active': [],
                'completed': [],
                'heat': {'heat': 0.0, 'friction': 0.0, 'recasion': 0.0}
            }
        
        try:
            # Execute sigils using the sigil engine
            execution_results = []
            
            # Get active sigils (this would integrate with actual sigil engine)
            active_sigils = []
            completed_sigils = []
            
            # Calculate sigil heat metrics
            sigil_heat = self._calculate_sigil_heat()
            
            return {
                'active': active_sigils,
                'completed': completed_sigils,
                'heat': sigil_heat
            }
            
        except Exception as e:
            logger.error(f"Error executing sigils: {e}")
            return {'active': [], 'completed': [], 'heat': {}}
    
    async def _calculate_entropy_drift(self) -> Dict[str, Any]:
        """Calculate entropy and drift state"""
        
        # This would integrate with DAWN's actual entropy analyzer
        # For now, simulate entropy based on system state
        
        current_time = time.time()
        
        # Simulate entropy based on various factors
        base_entropy = 0.5
        time_factor = (current_time % 60) / 60  # Oscillates with time
        
        if self.pulse_controller:
            # Get actual heat from pulse controller if available
            heat_factor = min(1.0, getattr(self.pulse_controller, 'current_heat', 25.0) / 100.0)
            base_entropy += heat_factor * 0.3
        
        entropy = min(1.0, base_entropy + time_factor * 0.2)
        drift = (time_factor - 0.5) * 2.0  # Range from -1 to 1
        
        return {
            'entropy': entropy,
            'drift': drift,
            'heat_contribution': getattr(self.pulse_controller, 'current_heat', 25.0) if self.pulse_controller else 25.0
        }
    
    def _prepare_dawn_state(self, schema_state: Dict, sigil_results: Dict, entropy_state: Dict) -> DAWNState:
        """Prepare DAWNState object from processing results"""
        
        return DAWNState(
            entropy=entropy_state.get('entropy', 0.0),
            drift_vector=entropy_state.get('drift', 0.0),
            mood_pigment=schema_state.get('pigment', {}),
            active_sigils=sigil_results.get('active', []),
            completed_sigils=sigil_results.get('completed', []),
            sigil_heat=sigil_results.get('heat', {}),
            pulse_zone=schema_state.get('pulse_zone', 'calm'),
            sigil_saturation=schema_state.get('saturation', 0.0),
            rebloom_depth=schema_state.get('rebloom_depth', 0),
            last_voice_generation=getattr(self.current_dawn_state, 'last_voice_generation', 0.0) if self.current_dawn_state else 0.0,
            last_visual_generation=getattr(self.current_dawn_state, 'last_visual_generation', 0.0) if self.current_dawn_state else 0.0,
            expression_threshold=self._calculate_expression_threshold(entropy_state, schema_state)
        )
    
    async def _handle_expression_generation(self, expression: DAWNExpression, dawn_state: DAWNState):
        """Handle expression generation and archiving"""
        
        try:
            # Update expression history
            self.expression_history.append(expression)
            
            # Archive expression if enabled
            if self.expression_archive and self.archive_expressions:
                archive_result = self.expression_archive.archive_expression(expression, dawn_state)
                logger.debug(f"Archived expression: {archive_result.get('expression_id', 'unknown')}")
            
            # Log expression generation
            logger.info(f"🎭 Expression generated: {expression.trigger_reason} (coherence: {expression.cognitive_coherence:.3f})")
            
            if expression.utterance:
                logger.info(f"🗣️ DAWN speaks: \"{expression.utterance}\"")
            
            if expression.visual_path:
                logger.info(f"🎨 Visual created: {expression.visual_path}")
            
            # Update performance metrics
            self.performance_metrics.total_expressions += 1
            if expression.utterance:
                self.performance_metrics.voice_expressions += 1
            if expression.visual_path:
                self.performance_metrics.visual_expressions += 1
            
            # Update trigger statistics
            trigger = expression.trigger_reason
            self.performance_metrics.trigger_counts[trigger] = self.performance_metrics.trigger_counts.get(trigger, 0) + 1
            
        except Exception as e:
            logger.error(f"Error handling expression generation: {e}")
    
    def _calculate_overall_coherence(self, dawn_state: DAWNState, expression: Optional[DAWNExpression]) -> float:
        """Calculate overall system cognitive coherence"""
        
        coherence_factors = []
        
        # Base cognitive coherence (entropy vs stability)
        entropy_coherence = 1.0 - abs(dawn_state.entropy - 0.5) * 2  # Peak at 0.5 entropy
        coherence_factors.append(entropy_coherence)
        
        # Pigment coherence (how well-defined the pigment state is)
        if dawn_state.mood_pigment:
            pigment_values = list(dawn_state.mood_pigment.values())
            pigment_coherence = max(pigment_values) if pigment_values else 0.0
            coherence_factors.append(pigment_coherence)
        
        # Expression coherence (if expression was generated)
        if expression:
            coherence_factors.append(expression.cognitive_coherence)
        
        # Sigil coherence (activity level)
        sigil_activity = len(dawn_state.active_sigils) + len(dawn_state.completed_sigils)
        sigil_coherence = min(1.0, sigil_activity * 0.2)
        coherence_factors.append(sigil_coherence)
        
        return sum(coherence_factors) / len(coherence_factors) if coherence_factors else 0.0
    
    def _update_performance_metrics(self, cycle_duration: float, cycle_result: Dict):
        """Update performance tracking metrics"""
        
        if not self.performance_monitoring:
            return
        
        self.performance_metrics.total_cycles += 1
        
        # Update cycle time tracking
        self.cycle_times.append(cycle_duration)
        if len(self.cycle_times) > 100:  # Keep last 100 cycles
            self.cycle_times.pop(0)
        
        self.performance_metrics.average_cycle_time = sum(self.cycle_times) / len(self.cycle_times)
        
        # Update coherence tracking
        if cycle_result.get('cognitive_coherence'):
            current_avg = self.performance_metrics.average_coherence
            total = self.performance_metrics.total_cycles
            self.performance_metrics.average_coherence = (
                (current_avg * (total - 1) + cycle_result['cognitive_coherence']) / total
            )
        
        self.performance_metrics.last_update = time.time()
    
    def _log_reactor_status(self):
        """Log periodic reactor status"""
        
        metrics = self.performance_metrics
        
        logger.info(f"🧠 Reactor Status - Cycles: {metrics.total_cycles}, "
                   f"Avg Time: {metrics.average_cycle_time:.3f}s, "
                   f"Expressions: {metrics.total_expressions}, "
                   f"Avg Coherence: {metrics.average_coherence:.3f}")
        
        if metrics.trigger_counts:
            top_triggers = sorted(metrics.trigger_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            trigger_summary = ", ".join([f"{trigger}: {count}" for trigger, count in top_triggers])
            logger.info(f"🎯 Top Triggers: {trigger_summary}")
    
    def _calculate_dynamic_sleep_time(self, cycle_duration: float, cycle_result: Dict) -> float:
        """Calculate dynamic sleep time based on system state"""
        
        base_sleep = 0.1  # Base 100ms
        
        # Adjust based on cycle performance
        if cycle_duration > 0.2:  # Slow cycle
            sleep_adjustment = -0.05  # Sleep less to catch up
        elif cycle_duration < 0.05:  # Fast cycle
            sleep_adjustment = 0.05  # Sleep more to conserve resources
        else:
            sleep_adjustment = 0.0
        
        # Adjust based on expression activity
        if cycle_result.get('expression'):
            sleep_adjustment += 0.02  # Brief pause after expression
        
        # Adjust based on entropy (higher entropy = more active processing)
        entropy = cycle_result.get('entropy_state', {}).get('entropy', 0.5)
        entropy_adjustment = (0.5 - entropy) * 0.1  # Higher entropy = less sleep
        
        total_sleep = max(0.01, base_sleep + sleep_adjustment + entropy_adjustment)
        return total_sleep
    
    # === HELPER METHODS FOR SYSTEM INTEGRATION ===
    
    def _get_current_mood_pigment(self) -> Dict[str, float]:
        """Get current mood pigment state"""
        # This would integrate with actual DAWN pigment system
        # For now, simulate based on system state
        
        current_time = time.time()
        time_factor = (current_time % 120) / 120  # 2-minute cycle
        
        # Simulate different pigment dominances over time
        if time_factor < 0.2:
            return {'blue': 0.6, 'violet': 0.3, 'green': 0.1}
        elif time_factor < 0.4:
            return {'green': 0.5, 'blue': 0.3, 'yellow': 0.2}
        elif time_factor < 0.6:
            return {'red': 0.5, 'orange': 0.3, 'yellow': 0.2}
        elif time_factor < 0.8:
            return {'violet': 0.4, 'blue': 0.3, 'red': 0.3}
        else:
            return {'orange': 0.4, 'yellow': 0.3, 'green': 0.3}
    
    def _get_current_pulse_zone(self) -> str:
        """Get current pulse zone"""
        # This would integrate with actual pulse controller
        if self.pulse_controller:
            heat = getattr(self.pulse_controller, 'current_heat', 25.0)
            if heat < 20:
                return 'calm'
            elif heat < 40:
                return 'stable'
            elif heat < 60:
                return 'flowing'
            elif heat < 80:
                return 'surge'
            else:
                return 'fragile'
        return 'calm'
    
    def _get_current_saturation(self) -> float:
        """Get current sigil saturation"""
        if self.sigil_engine:
            # Calculate based on active sigils
            active_count = len(getattr(self.sigil_engine, 'active_sigils', {}))
            return min(1.0, active_count * 0.2)
        return 0.0
    
    def _get_current_rebloom_depth(self) -> int:
        """Get current rebloom depth"""
        # This would integrate with actual rebloom system
        return 0
    
    def _calculate_sigil_heat(self) -> Dict[str, float]:
        """Calculate sigil heat metrics"""
        if self.pulse_controller:
            heat = getattr(self.pulse_controller, 'current_heat', 25.0)
            normalized_heat = heat / 100.0
            
            return {
                'heat': normalized_heat,
                'friction': normalized_heat * 0.7,
                'recasion': normalized_heat * 0.3
            }
        
        return {'heat': 0.25, 'friction': 0.1, 'recasion': 0.05}
    
    def _calculate_expression_threshold(self, entropy_state: Dict, schema_state: Dict) -> float:
        """Calculate dynamic expression threshold"""
        base_threshold = 0.5
        
        # Increase threshold with higher entropy
        entropy_factor = entropy_state.get('entropy', 0.5) * 0.3
        
        # Increase threshold with higher heat
        heat_factor = entropy_state.get('heat_contribution', 25.0) / 100.0 * 0.2
        
        return min(1.0, base_threshold + entropy_factor + heat_factor)
    
    # === PUBLIC API METHODS ===
    
    def get_current_state(self) -> Optional[DAWNState]:
        """Get current DAWN state"""
        return self.current_dawn_state
    
    def get_current_expression(self) -> Optional[DAWNExpression]:
        """Get current expression"""
        return self.current_expression
    
    def get_recent_expressions(self, limit: int = 10) -> List[DAWNExpression]:
        """Get recent expressions"""
        return self.expression_history[-limit:] if self.expression_history else []
    
    def get_performance_metrics(self) -> ReactorPerformanceMetrics:
        """Get current performance metrics"""
        return self.performance_metrics
    
    def trigger_manual_expression(self, reason: str = "manual_trigger") -> Optional[DAWNExpression]:
        """Manually trigger expression generation"""
        if not self.expression_monitor or not self.current_dawn_state:
            return None
        
        # Temporarily override threshold
        original_threshold = self.current_dawn_state.expression_threshold
        self.current_dawn_state.expression_threshold = 1.0
        
        # Force expression generation
        expression = self.expression_monitor._generate_coordinated_expression(
            self.current_dawn_state, reason
        )
        
        # Restore original threshold
        self.current_dawn_state.expression_threshold = original_threshold
        
        if expression:
            self.expression_history.append(expression)
            
        return expression
    
    def configure_expression_settings(self, config: Dict) -> bool:
        """Configure expression settings"""
        try:
            if self.expression_monitor:
                self.expression_monitor.expression_config.update(config)
                logger.info(f"Updated expression configuration: {config}")
                return True
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")
        
        return False


def test_enhanced_reactor():
    """Test the enhanced DAWN autonomous reactor"""
    
    print("🧠✨ Testing Enhanced DAWN Autonomous Reactor")
    print("=" * 60)
    
    async def run_test():
        # Initialize reactor
        reactor = EnhancedDAWNAutonomousReactor(
            expression_config={
                'entropy_trigger_threshold': 0.6,  # Lower threshold for testing
                'time_between_expressions': 2.0    # Faster expressions for testing
            },
            performance_monitoring=True,
            archive_expressions=True
        )
        
        # Start reactor for a short test period
        print("🚀 Starting enhanced reactor...")
        
        # Run for 30 seconds
        start_time = time.time()
        await asyncio.wait_for(reactor.start(), timeout=30.0)
        
        print("✅ Test completed")
        
        # Print results
        metrics = reactor.get_performance_metrics()
        print(f"\n📊 Performance Metrics:")
        print(f"  Cycles: {metrics.total_cycles}")
        print(f"  Average cycle time: {metrics.average_cycle_time:.3f}s")
        print(f"  Total expressions: {metrics.total_expressions}")
        print(f"  Voice expressions: {metrics.voice_expressions}")
        print(f"  Visual expressions: {metrics.visual_expressions}")
        print(f"  Average coherence: {metrics.average_coherence:.3f}")
        
        expressions = reactor.get_recent_expressions(5)
        print(f"\n🎭 Recent Expressions:")
        for expr in expressions[-3:]:  # Show last 3
            print(f"  - {expr.trigger_reason}: coherence {expr.cognitive_coherence:.3f}")
            if expr.utterance:
                print(f"    Voice: \"{expr.utterance}\"")
        
        reactor.stop()
    
    try:
        asyncio.run(run_test())
    except asyncio.TimeoutError:
        print("⏰ Test completed (timeout reached)")
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    print("=" * 60)
    print("✨ Enhanced reactor testing complete")


if __name__ == "__main__":
    test_enhanced_reactor() 