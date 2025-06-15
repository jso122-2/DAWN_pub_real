import asyncio
import time
import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Callable, Any
from collections import deque
import numpy as np
from datetime import datetime
import logging

from .consciousness_state import ConsciousnessState, MoodState
from .tick_broadcaster import TickBroadcaster
from .tick_processor import TickProcessor

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
            
            self.modules['neural'] = NeuralSimulator()
            self.modules['consciousness'] = ConsciousnessStateManager()
            self.modules['memory'] = MemoryManager()
            
            if self.enable_owl:
                from ..modules.owl_integration import OwlModule
                self.modules['owl'] = OwlModule()
                logger.info("Owl module initialized")
            
            logger.info("All modules initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize modules: {e}")
            raise
    
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
            self.consciousness.neural_activity = neural_state['firing_rate'] / 100.0
        
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
        """Calculate Lyapunov exponent for chaos measurement"""
        if len(self.tick_history) < 20:
            return 0.0
        
        # Simplified Lyapunov calculation
        recent_scup = [t.scup for t in list(self.tick_history)[-20:]]
        differences = np.diff(recent_scup)
        
        if len(differences) > 0 and np.std(differences) > 0:
            lyapunov = np.mean(np.abs(differences)) / np.std(differences)
        else:
            lyapunov = 0.0
        
        return float(np.clip(lyapunov * 0.1, -1, 1))
    
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


# Singleton instance
tick_engine = TickEngine() 