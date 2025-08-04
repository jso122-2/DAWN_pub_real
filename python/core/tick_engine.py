import asyncio
import time
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Callable, Any
from collections import deque
import numpy as np
from datetime import datetime
import logging

from ...consciousness_state import ConsciousnessState, MoodState
from ...tick_broadcaster import TickBroadcaster
from ...tick_processor import TickProcessor

logger = logging.getLogger(__name__)


@dataclass
class TickData:
    """Core tick data structure"""
    tick_number: int
    timestamp: float
    scup: float  # System Consciousness Unity Percentage
    entropy: float
    mood: str
    neural_activity: float
    consciousness_unity: float
    memory_pressure: float
    active_processes: List[str]
    subsystems: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TickEngine:
    """
    DAWN's consciousness tick engine - the heartbeat of the system.
    Generates regular consciousness pulses and coordinates all subsystems.
    """
    
    def __init__(
        self,
        tick_rate: float = 10.0,  # Hz
        buffer_size: int = 1000,
        enable_owl: bool = True
    ):
        self.tick_rate = tick_rate
        self.tick_interval = 1.0 / tick_rate
        self.buffer_size = buffer_size
        
        # Core state
        self.tick_count = 0
        self.start_time = time.time()
        self.is_running = False
        
        # State management
        self.consciousness = ConsciousnessState()
        self.tick_history = deque(maxlen=buffer_size)
        
        # Components
        self.broadcaster = TickBroadcaster()
        self.processor = TickProcessor()
        
        # Subsystem modules
        self.modules: Dict[str, Any] = {}
        self.enable_owl = enable_owl
        
        # Tick callbacks
        self.tick_callbacks: List[Callable[[TickData], None]] = []
        
        # Performance tracking
        self.performance_metrics = {
            'avg_tick_time': 0.0,
            'max_tick_time': 0.0,
            'dropped_ticks': 0,
            'total_ticks': 0
        }
        
        logger.info(f"TickEngine initialized at {tick_rate}Hz")
    
    async def initialize_modules(self):
        """Initialize all subsystem modules"""
        try:
            from ..modules.neural_simulator import NeuralSimulator
            from ..modules.consciousness_state import ConsciousnessStateManager
            from ..modules.memory_manager import MemoryManager
            
            # Initialize modules with proper error handling
            self.modules['neural'] = NeuralSimulator()
            logger.info("Neural simulator initialized")
            
            self.modules['consciousness'] = ConsciousnessStateManager()
            logger.info("Consciousness state manager initialized")
            
            self.modules['memory'] = MemoryManager()
            logger.info("Memory manager initialized")
            
            # Verify memory module connection
            if hasattr(self.modules['memory'], 'get_state'):
                # Test memory state access
                test_state = await self.modules['memory'].get_state(0)
                if 'pressure' in test_state:
                    logger.info(f"✅ Memory pressure system connected: {test_state['pressure']:.3f}")
                else:
                    logger.warning("⚠️ Memory module missing pressure calculation")
            else:
                logger.error("❌ Memory module missing get_state method")
            
            if self.enable_owl:
                from ..modules.owl_integration import OwlModule
                self.modules['owl'] = OwlModule()
                logger.info("Owl module initialized")
            
            logger.info("All modules initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize modules: {e}")
            # Continue with partial initialization rather than failing completely
            logger.warning("Continuing with available modules")
            if 'neural' not in self.modules:
                logger.warning("Neural module unavailable - neural_activity will be static")
            if 'memory' not in self.modules:
                logger.warning("Memory module unavailable - memory_pressure will be static")
            if 'consciousness' not in self.modules:
                logger.warning("Consciousness module unavailable - consciousness_depth will be static")
    
    async def start(self):
        """Start the tick engine"""
        if self.is_running:
            logger.warning("Tick engine already running")
            return
        
        logger.info("Starting tick engine...")
        self.is_running = True
        self.start_time = time.time()
        
        # Initialize modules
        await self.initialize_modules()
        
        # Start tick loop
        asyncio.create_task(self._tick_loop())
        
        # Start performance monitor
        asyncio.create_task(self._performance_monitor())
        
        logger.info("Tick engine started")
    
    async def stop(self):
        """Stop the tick engine"""
        logger.info("Stopping tick engine...")
        self.is_running = False
        await asyncio.sleep(self.tick_interval * 2)  # Allow loops to finish
        logger.info("Tick engine stopped")
    
    async def _tick_loop(self):
        """Main tick loop"""
        while self.is_running:
            tick_start = time.time()
            
            try:
                # Generate tick
                tick_data = await self._generate_tick()
                
                # Store in history
                self.tick_history.append(tick_data)
                
                # Process tick through subsystems
                await self._process_tick(tick_data)
                
                # Broadcast to connected clients
                await self.broadcaster.broadcast_tick(tick_data)
                
                # Execute callbacks
                for callback in self.tick_callbacks:
                    try:
                        await asyncio.create_task(
                            asyncio.coroutine(callback)(tick_data)
                        ) if asyncio.iscoroutinefunction(callback) else callback(tick_data)
                    except Exception as e:
                        logger.error(f"Tick callback error: {e}")
                
                # Update performance metrics
                self._update_performance(tick_start)
                
            except Exception as e:
                logger.error(f"Tick loop error: {e}")
                self.performance_metrics['dropped_ticks'] += 1
            
            # Maintain tick rate
            elapsed = time.time() - tick_start
            sleep_time = max(0, self.tick_interval - elapsed)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            else:
                logger.warning(f"Tick {self.tick_count} took {elapsed:.3f}s (target: {self.tick_interval:.3f}s)")
    
    async def _generate_tick(self) -> TickData:
        """Generate a new tick with all consciousness data"""
        self.tick_count += 1
        current_time = time.time()
        
        # Update consciousness state
        await self.consciousness.update(self.tick_count)
        
        # Get subsystem states
        subsystem_states = {}
        
        # Neural state
        if 'neural' in self.modules:
            neural_state = await self.modules['neural'].get_state(self.tick_count)
            subsystem_states['neural'] = neural_state
            # Ensure neural activity is properly scaled and connected
            firing_rate = neural_state.get('firing_rate', 50.0)
            avg_activation = neural_state.get('avg_activation', 0.5)
            
            # Use both firing rate and activation for robust neural activity
            self.consciousness.neural_activity = min(1.0, max(0.0, 
                (firing_rate / 100.0) * 0.7 + avg_activation * 0.3
            ))
            
            logger.debug(f"🧠 Neural activity updated: {self.consciousness.neural_activity:.3f} "
                        f"(firing: {firing_rate:.1f}, activation: {avg_activation:.3f})")
        else:
            # Fallback with warning
            logger.warning("Neural module not available - using static neural activity")
            self.consciousness.neural_activity = 0.5
        
        # Consciousness state
        if 'consciousness' in self.modules:
            consciousness_state = await self.modules['consciousness'].get_state(self.tick_count)
            subsystem_states['consciousness'] = consciousness_state
            self.consciousness.consciousness_unity = consciousness_state['unity']
        
        # Memory state
        if 'memory' in self.modules:
            memory_state = await self.modules['memory'].get_state(self.tick_count)
            subsystem_states['memory'] = memory_state
            self.consciousness.memory_pressure = memory_state['pressure']
        
        # Chaos/Entropy calculations
        entropy = self._calculate_entropy()
        self.consciousness.entropy = entropy
        subsystem_states['chaos'] = {
            'entropy': entropy,
            'lyapunov_exponent': self._calculate_lyapunov(),
            'fractal_dimension': 1.67,  # Placeholder
            'strange_attractor': entropy > 0.7
        }
        
        # Calculate SCUP
        scup = self.consciousness.calculate_scup()
        
        # Calculate drift from stability using multiple drift sources
        drift_from_stability = self._calculate_drift_from_stability(
            entropy, scup, subsystem_states
        )
        subsystem_states['drift'] = {
            'drift_from_stability': drift_from_stability,
            'semantic_drift': self._get_semantic_drift(),
            'alignment_drift': self._get_alignment_drift(),
            'schema_drift': self._calculate_schema_drift(entropy, scup)
        }
        
        # Determine mood
        mood = self.consciousness.determine_mood()
        
        # Get active processes
        active_processes = await self.processor.get_active_processes()
        
        # Create tick data
        tick_data = TickData(
            tick_number=self.tick_count,
            timestamp=current_time,
            scup=scup,
            entropy=entropy,
            mood=mood.value,
            neural_activity=self.consciousness.neural_activity,
            consciousness_unity=self.consciousness.consciousness_unity,
            memory_pressure=self.consciousness.memory_pressure,
            active_processes=active_processes,
            subsystems=subsystem_states
        )
        
        # Add schema state data for consciousness depth calculation
        try:
            from core.schema_state import SchemaState
            if hasattr(self, '_schema_state') and self._schema_state:
                schema_info = {
                    'alignment': getattr(self._schema_state, 'alignment', 0.5),
                    'tension': getattr(self._schema_state, 'tension', 0.0),
                    'coherence': getattr(self._schema_state, 'coherence', 0.5),
                    'breathing_phase': getattr(self._schema_state, 'breathing_phase', 0.0)
                }
            else:
                # Initialize schema state if not available
                self._schema_state = SchemaState()
                schema_info = {
                    'alignment': 0.5,
                    'tension': 0.0,
                    'coherence': 0.5,
                    'breathing_phase': 0.0
                }
            
            # Add schema state to subsystems for consciousness metrics
            subsystem_states['schema_state'] = schema_info
            
        except (ImportError, Exception) as e:
            logger.debug(f"Schema state unavailable: {e}")
            # Provide fallback schema state
            subsystem_states['schema_state'] = {
                'alignment': 0.5,
                'tension': 0.0,
                'coherence': 0.5,
                'breathing_phase': 0.0
            }
        
        # Update consciousness metrics with enhanced tick data
        try:
            from core.consciousness_metrics import ConsciousnessMetrics
            if not hasattr(self, '_consciousness_metrics'):
                self._consciousness_metrics = ConsciousnessMetrics()
            
            # Create enhanced tick data for consciousness metrics
            enhanced_tick_data = {
                'active_sigils': len(active_processes),
                'entropy': entropy,
                'heat': subsystem_states.get('neural', {}).get('network_energy', 25.0) * 100,
                'zone': self._determine_zone_from_heat(subsystem_states),
                'bloom_count': self._get_bloom_count(),
                'scup': scup,
                'tick_id': self.tick_count,
                'schema_state': subsystem_states['schema_state'],
                'queued_sigils': self._get_queued_processes(),
                'target_heat': 33.0
            }
            
            # Update consciousness metrics
            consciousness_metrics = self._consciousness_metrics.update(enhanced_tick_data)
            
            # Add consciousness metrics to subsystems
            subsystem_states['consciousness_metrics'] = consciousness_metrics
            
            logger.debug(f"🧠 Consciousness metrics: "
                        f"depth={consciousness_metrics.get('consciousness_depth', 0):.3f} "
                        f"neural={consciousness_metrics.get('neural_activity', 0):.3f}")
            
        except (ImportError, Exception) as e:
            logger.warning(f"Consciousness metrics unavailable: {e}")
        
        return tick_data
    
    async def _process_tick(self, tick_data: TickData):
        """Process tick through all subsystems"""
        # Update Owl if enabled
        if self.enable_owl and 'owl' in self.modules:
            owl_observations = await self.modules['owl'].process_tick(tick_data, self.tick_history)
            
            # Check for strategic recommendations
            if owl_observations and owl_observations.get('recommendations'):
                for rec in owl_observations['recommendations']:
                    logger.info(f"Owl recommendation: {rec['description']} (priority: {rec['priority']})")
        
        # Trigger any tick-based processes
        await self.processor.process_tick_triggers(tick_data)
    
    def _calculate_entropy(self) -> float:
        """Calculate system entropy based on recent ticks"""
        if len(self.tick_history) < 10:
            return 0.5  # Default entropy
        
        # Calculate entropy from recent neural activity variance
        recent_activity = [t.neural_activity for t in list(self.tick_history)[-10:]]
        variance = np.var(recent_activity)
        
        # Add some controlled randomness
        noise = np.random.normal(0, 0.05)
        
        # Normalize to 0-1 range
        entropy = np.clip(variance * 5 + 0.5 + noise, 0, 1)
        
        return float(entropy)
    
    def _calculate_lyapunov(self) -> float:
        """Calculate Lyapunov exponent (placeholder)"""
        if len(self.tick_history) < 10:
            return 0.0
        
        recent_neural = [t.neural_activity for t in list(self.tick_history)[-10:]]
        variance = np.var(recent_neural)
        return min(1.0, variance * 10)  # Normalize
    
    def _calculate_drift_from_stability(self, entropy: float, scup: float, 
                                      subsystem_states: Dict[str, Any]) -> float:
        """
        Calculate unified drift from stability using multiple sources.
        Integrates semantic, alignment, and schema drift patterns.
        """
        # 1. SEMANTIC DRIFT: Rate of change in semantic pressure
        semantic_drift = self._get_semantic_drift()
        
        # 2. ALIGNMENT DRIFT: Deviation from target alignment
        alignment_drift = self._get_alignment_drift()
        
        # 3. SCHEMA DRIFT: Changes in schema coherence patterns
        schema_drift = self._calculate_schema_drift(entropy, scup)
        
        # 4. NEURAL DRIFT: Changes in neural activity patterns  
        neural_drift = self._calculate_neural_drift(subsystem_states)
        
        # 5. MEMORY DRIFT: Changes in memory pressure patterns
        memory_drift = self._calculate_memory_drift(subsystem_states)
        
        # 6. THERMAL DRIFT: Changes in thermal stability
        thermal_drift = self._calculate_thermal_drift()
        
        # Weighted combination of drift sources - SEMANTIC TENSION is primary
        total_drift = (
            semantic_drift * 0.40 +      # PRIMARY: Semantic tension tracking
            alignment_drift * 0.20 +     # Alignment deviation
            schema_drift * 0.15 +        # Schema coherence changes  
            neural_drift * 0.10 +        # Neural activity changes
            memory_drift * 0.10 +        # Memory pressure changes
            thermal_drift * 0.05         # Thermal stability changes
        )
        
        # SEMANTIC TENSION BOOST: Amplify when semantic pressure is high
        if semantic_drift > 0.6:  # High semantic tension
            tension_amplifier = 1.0 + (semantic_drift - 0.6) * 0.5
            total_drift *= tension_amplifier
        
        # Reduce temporal smoothing to make drift more responsive to semantic changes
        if hasattr(self, '_last_drift'):
            smoothed_drift = self._last_drift * 0.5 + total_drift * 0.5  # More responsive
        else:
            smoothed_drift = total_drift
        
        self._last_drift = smoothed_drift
        
        return min(1.0, max(0.0, smoothed_drift))
    
    def _get_semantic_drift(self) -> float:
        """Get semantic drift - tracks semantic tension and pressure buildup"""
        try:
            # PRIMARY: Track semantic tension from pressure delta
            from semantic.drift_calculator import calculate_pressure_delta
            
            # Use recent tick history to calculate semantic tension
            if len(self.tick_history) >= 5:
                recent_ticks = list(self.tick_history)[-5:]
                
                # Create semantic context from recent consciousness states  
                semantic_context = []
                for tick in recent_ticks:
                    mood_str = getattr(tick, 'mood', 'neutral')
                    scup_str = f"scup_{getattr(tick, 'scup', 0.5):.1f}"
                    neural_str = f"neural_{getattr(tick, 'neural_activity', 0.5):.1f}"
                    semantic_context.append(f"{mood_str}_{scup_str}_{neural_str}")
                
                if len(semantic_context) >= 2:
                    current_semantic = semantic_context[-1]
                    historical_semantic = semantic_context[:-1]
                    
                    # Calculate semantic pressure delta (tension indicator)
                    pressure_delta = calculate_pressure_delta(current_semantic, historical_semantic)
                    
                    # Semantic tension: Rising pressure = increasing tension
                    if pressure_delta > 1.0:  # Rising semantic pressure
                        semantic_tension = min(0.9, pressure_delta * 0.15)
                    elif pressure_delta < -1.0:  # Falling pressure (relaxing)
                        semantic_tension = max(0.1, 0.5 + (pressure_delta * 0.1))
                    else:  # Stable pressure
                        semantic_tension = 0.3 + (abs(pressure_delta) * 0.1)
                    
                    return semantic_tension
            
        except (ImportError, Exception) as e:
            logger.debug(f"Semantic pressure delta unavailable: {e}")
        
        # FALLBACK: Calculate semantic tension from SCUP/entropy variance
        if len(self.tick_history) >= 5:
            recent_scup = [getattr(t, 'scup', 0.5) for t in list(self.tick_history)[-5:]]
            recent_entropy = [getattr(t, 'entropy', 0.5) for t in list(self.tick_history)[-5:]]
            
            # Semantic tension emerges from SCUP-entropy instability
            scup_variance = np.var(recent_scup) if len(recent_scup) > 1 else 0
            entropy_variance = np.var(recent_entropy) if len(recent_entropy) > 1 else 0
            
            # High variance = high semantic tension
            semantic_tension = min(0.8, (scup_variance + entropy_variance) * 3.0)
            
            # Add current SCUP-entropy divergence as immediate tension
            current_scup = recent_scup[-1] if recent_scup else 0.5
            current_entropy = recent_entropy[-1] if recent_entropy else 0.5
            scup_entropy_divergence = abs(current_scup - current_entropy)
            
            # Strong divergence increases semantic tension
            if scup_entropy_divergence > 0.3:
                semantic_tension += (scup_entropy_divergence - 0.3) * 0.5
            
            return min(0.9, semantic_tension)
        
        return 0.2  # Default moderate tension
    
    def _get_alignment_drift(self) -> float:
        """Get alignment drift from alignment probe"""
        try:
            from core.alignment.alignment_probe import AlignmentProbe
            if hasattr(self, '_alignment_probe'):
                drift_analysis = self._alignment_probe._calculate_drift()
                return min(1.0, max(0.0, abs(drift_analysis)))
            else:
                # Initialize alignment probe
                self._alignment_probe = AlignmentProbe()
                return 0.0
                
        except (ImportError, Exception) as e:
            logger.debug(f"Alignment drift unavailable: {e}")
        
        return 0.2  # Default moderate drift
    
    def _calculate_schema_drift(self, entropy: float, scup: float) -> float:
        """Calculate schema drift from entropy and SCUP changes"""
        if len(self.tick_history) < 5:
            return 0.0
        
        # Get recent SCUP and entropy values
        recent_scup = [getattr(t, 'scup', 0.5) for t in list(self.tick_history)[-5:]]
        recent_entropy = [getattr(t, 'entropy', 0.5) for t in list(self.tick_history)[-5:]]
        
        # Calculate variance in SCUP and entropy
        scup_variance = np.var(recent_scup) if recent_scup else 0
        entropy_variance = np.var(recent_entropy) if recent_entropy else 0
        
        # Schema drift is the combined variance from stability
        schema_drift = (scup_variance + entropy_variance) * 5.0  # Scale up
        
        return min(1.0, max(0.0, schema_drift))
    
    def _calculate_neural_drift(self, subsystem_states: Dict[str, Any]) -> float:
        """Calculate neural drift from firing pattern changes"""
        if len(self.tick_history) < 3:
            return 0.0
        
        # Get recent neural activity
        recent_neural = [t.neural_activity for t in list(self.tick_history)[-5:]]
        
        if len(recent_neural) >= 3:
            # Calculate rate of change
            changes = [abs(recent_neural[i] - recent_neural[i-1]) 
                      for i in range(1, len(recent_neural))]
            avg_change = sum(changes) / len(changes) if changes else 0
            
            # High rate of change = high drift
            return min(1.0, avg_change * 3.0)
        
        return 0.0
    
    def _calculate_memory_drift(self, subsystem_states: Dict[str, Any]) -> float:
        """Calculate memory drift from memory pressure changes"""
        if len(self.tick_history) < 3:
            return 0.0
        
        # Get recent memory pressure if available
        memory_states = subsystem_states.get('memory', {})
        current_pressure = memory_states.get('pressure', 0.5)
        
        # Look for pressure in recent history
        recent_pressures = []
        for tick in list(self.tick_history)[-5:]:
            if hasattr(tick, 'subsystems') and 'memory' in tick.subsystems:
                pressure = tick.subsystems['memory'].get('pressure', 0.5)
                recent_pressures.append(pressure)
        
        if len(recent_pressures) >= 2:
            # Calculate pressure change rate
            pressure_changes = [abs(recent_pressures[i] - recent_pressures[i-1]) 
                              for i in range(1, len(recent_pressures))]
            avg_change = sum(pressure_changes) / len(pressure_changes) if pressure_changes else 0
            
            return min(1.0, avg_change * 2.0)
        
        return 0.0
    
    def _calculate_thermal_drift(self) -> float:
        """Calculate thermal drift from pulse heat changes"""
        try:
            from pulse.pulse_heat import pulse
            thermal_profile = pulse.get_thermal_profile()
            current_heat = thermal_profile.get('current_heat', 0.0)
            
            # Store heat history
            if not hasattr(self, '_heat_history'):
                self._heat_history = []
            
            self._heat_history.append(current_heat)
            if len(self._heat_history) > 10:
                self._heat_history.pop(0)
            
            # Calculate heat variance as thermal drift
            if len(self._heat_history) >= 3:
                heat_variance = np.var(self._heat_history)
                return min(1.0, heat_variance / 10.0)  # Normalize
                
        except (ImportError, Exception) as e:
            logger.debug(f"Thermal drift unavailable: {e}")
        
        return 0.0
    
    def _update_performance(self, tick_start: float):
        """Update performance metrics"""
        tick_time = time.time() - tick_start
        
        self.performance_metrics['total_ticks'] += 1
        
        # Update average (exponential moving average)
        alpha = 0.1
        self.performance_metrics['avg_tick_time'] = (
            alpha * tick_time + 
            (1 - alpha) * self.performance_metrics['avg_tick_time']
        )
        
        # Update max
        self.performance_metrics['max_tick_time'] = max(
            self.performance_metrics['max_tick_time'],
            tick_time
        )
    
    async def _performance_monitor(self):
        """Monitor and log performance metrics"""
        while self.is_running:
            await asyncio.sleep(60)  # Log every minute
            
            metrics = self.performance_metrics.copy()
            metrics['tick_rate_actual'] = self.tick_count / (time.time() - self.start_time)
            metrics['tick_rate_target'] = self.tick_rate
            metrics['efficiency'] = min(1.0, metrics['tick_rate_actual'] / metrics['tick_rate_target'])
            
            logger.info(f"Performance metrics: {json.dumps(metrics, indent=2)}")
    
    def register_callback(self, callback: Callable[[TickData], None]):
        """Register a callback to be called on each tick"""
        self.tick_callbacks.append(callback)
        logger.info(f"Registered tick callback: {callback.__name__}")
    
    def get_tick_history(self, count: int = 100) -> List[TickData]:
        """Get recent tick history"""
        return list(self.tick_history)[-count:]
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current engine state"""
        # Get semantic field drift vectors
        from semantic.semantic_field import get_current_field
        field = get_current_field()
        drift_vectors = field.get_drift_vectors() if field else {}
        
        return {
            'tick_count': self.tick_count,
            'is_running': self.is_running,
            'tick_rate': self.tick_rate,
            'consciousness': self.consciousness.to_dict(),
            'performance': self.performance_metrics,
            'modules': list(self.modules.keys()),
            'uptime': time.time() - self.start_time,
            'drift_vectors': drift_vectors
        }

    def _determine_zone_from_heat(self, subsystem_states: Dict[str, Any]) -> str:
        """Determine thermal zone from subsystem data"""
        # Try to get neural network energy as heat proxy
        neural_states = subsystem_states.get('neural', {})
        heat_proxy = neural_states.get('network_energy', 0.5) * 100
        
        # Try to get actual thermal data if available
        try:
            from pulse.pulse_heat import pulse
            thermal_profile = pulse.get_thermal_profile()
            actual_heat = thermal_profile.get('current_heat', heat_proxy)
            zone = thermal_profile.get('current_zone', None)
            if zone:
                return zone.upper()
        except (ImportError, Exception):
            actual_heat = heat_proxy
        
        # Determine zone from heat value
        if actual_heat < 20:
            return "CALM"
        elif actual_heat < 40:
            return "ACTIVE"
        elif actual_heat < 60:
            return "INTENSE"
        elif actual_heat < 80:
            return "SURGE"
        else:
            return "CRITICAL"
    
    def _get_bloom_count(self) -> int:
        """Get current bloom count from bloom system"""
        try:
            from bloom.unified_bloom_engine import get_active_bloom_count
            return get_active_bloom_count()
        except (ImportError, Exception):
            # Fallback: estimate from tick activity
            return min(5, len(self.tick_history) // 10)
    
    def _get_queued_processes(self) -> int:
        """Get number of queued processes"""
        try:
            if hasattr(self.processor, 'get_queue_size'):
                return self.processor.get_queue_size()
            else:
                # Estimate from active processes
                return max(0, len(self.processor.active_processes) - 3)
        except (AttributeError, Exception):
            return 0


# Singleton instance
tick_engine = TickEngine() 