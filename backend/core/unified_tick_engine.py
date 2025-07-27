"""
Unified Tick Engine - Advanced timing and event management system
"""

import asyncio
import logging
import time
import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import psutil
import yaml

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add backend directory to Python path
backend_dir = str(Path(__file__).parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from semantic.field_initializer import get_current_field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TickState:
    """Current state of the tick engine"""
    tick_count: int = 0
    last_tick_time: float = field(default_factory=time.time)
    current_interval: float = 1.0
    target_interval: float = 1.0
    event_handlers: Dict[str, List[Callable]] = field(default_factory=dict)
    event_queue: deque = field(default_factory=lambda: deque(maxlen=1000))
    is_running: bool = False
    stop_event: asyncio.Event = field(default_factory=asyncio.Event)
    thermal_state: Dict[str, float] = field(default_factory=lambda: {
        'heat': 0.0,
        'momentum': 0.0,
        'stability': 1.0
    })
    performance_metrics: Dict[str, float] = field(default_factory=lambda: {
        'cpu_usage': 0.0,
        'memory_usage': 0.0,
        'event_latency': 0.0
    })
    error_count: int = 0
    recovery_count: int = 0
    last_recovery_time: float = field(default_factory=time.time)

    def __post_init__(self):
        if self.event_handlers is None:
            self.event_handlers = {}
        if self.stop_event is None:
            self.stop_event = asyncio.Event()
        if self.event_queue is None:
            self.event_queue = deque(maxlen=1000)

class UnifiedTickEngine:
    """
    Advanced timing and event management system.
    Provides comprehensive tick processing, event handling, and system monitoring.
    """
    
    def __init__(self, config_path: str = "config/tick_config.yaml"):
        """Initialize tick engine with configuration"""
        self._state = TickState()
        self._subsystems = {}  # Dictionary to store subsystems
        
        # Resolve config path relative to project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, config_path)
        
        self._config = self._load_config(config_path)
        self._log_dir = os.path.join(project_root, 'logs')
        self._metrics_dir = os.path.join(self._log_dir, 'metrics')
        os.makedirs(self._log_dir, exist_ok=True)
        os.makedirs(self._metrics_dir, exist_ok=True)
        
        # Initialize monitoring
        self._process = psutil.Process()
        self._monitor_task = None
        
        self.current_tick = 0
        self.tick_interval = 0.1  # 100ms between ticks
        self.tick_history = []
        self.max_history_size = 1000
        self.tick_callbacks = []
        self.tick_metrics = {
            "tick_rate": 0,
            "subsystem_times": {},
            "total_time": 0
        }
        self.event_queue = []
        
        logger.info("Initialized UnifiedTickEngine")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load engine configuration"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}
    
    async def start(self) -> None:
        """Start the tick engine"""
        if self._state.is_running:
            logger.warning("Tick engine already running")
            return
            
        self._state.is_running = True
        self._state.stop_event.clear()
        
        # Start monitoring
        self._monitor_task = asyncio.create_task(self._monitor_system())
        
        logger.info("Starting tick engine")
        
        try:
            while not self._state.stop_event.is_set():
                # Process tick
                await self._process_tick()
                
                # Process event queue
                await self._process_event_queue()
                
                # Calculate next interval
                next_interval = self._calculate_interval()
                
                # Wait for next tick
                await asyncio.sleep(next_interval)
                
        except Exception as e:
            logger.error(f"Error in tick engine: {e}")
            await self._handle_error(e)
        finally:
            self._state.is_running = False
            if self._monitor_task:
                self._monitor_task.cancel()
                try:
                    await self._monitor_task
                except asyncio.CancelledError:
                    pass
            logger.info("Tick engine stopped")
    
    async def _monitor_system(self):
        """Monitor system resources and performance"""
        while not self._state.stop_event.is_set():
            try:
                # Update CPU usage
                self._state.performance_metrics['cpu_usage'] = self._process.cpu_percent()
                
                # Update memory usage
                memory_info = self._process.memory_info()
                self._state.performance_metrics['memory_usage'] = memory_info.rss / 1024 / 1024  # MB
                
                # Log metrics
                self._log_metrics()
                
                await asyncio.sleep(1.0)  # Update every second
            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
    
    def _log_metrics(self):
        """Log current metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'tick_count': self._state.tick_count,
            'performance': self._state.performance_metrics,
            'thermal': self._state.thermal_state
        }
        
        metrics_file = os.path.join(self._metrics_dir, f"metrics_{datetime.now().strftime('%Y%m%d')}.json")
        with open(metrics_file, 'a') as f:
            f.write(json.dumps(metrics) + "\n")
    
    async def _handle_error(self, error: Exception):
        """Handle engine errors"""
        self._state.error_count += 1
        
        # Check if recovery is needed
        if self._state.error_count >= self._config.get('max_errors', 3):
            await self._attempt_recovery()
        
        # Log error
        self.log_tick_event('error', {
            'error': str(error),
            'error_count': self._state.error_count,
            'recovery_count': self._state.recovery_count
        })
    
    async def _attempt_recovery(self):
        """Attempt system recovery"""
        if (self._state.recovery_count >= self._config.get('max_recoveries', 3) or
            time.time() - self._state.last_recovery_time < self._config.get('recovery_cooldown', 300)):
            logger.error("Max recoveries reached or cooldown active")
            await self.stop()
            return
        
        logger.info("Attempting system recovery")
        self._state.recovery_count += 1
        self._state.last_recovery_time = time.time()
        self._state.error_count = 0
        
        # Reset thermal state
        self._state.thermal_state = {
            'heat': 0.0,
            'momentum': 0.0,
            'stability': 1.0
        }
        
        # Clear event queue
        self._state.event_queue.clear()
        
        # Log recovery
        self.log_tick_event('recovery', {
            'recovery_count': self._state.recovery_count,
            'timestamp': datetime.now().isoformat()
        })
    
    async def stop(self) -> None:
        """Stop the tick engine"""
        if not self._state.is_running:
            return
            
        self._state.stop_event.set()
        logger.info("Stopping tick engine")
        
        # Stop monitoring
        if hasattr(self, '_monitor_task'):
            self._monitor_task.cancel()
    
    def register_handler(self, event_type: str, handler: Callable, priority: int = 0) -> None:
        """Register an event handler with priority"""
        if event_type not in self._state.event_handlers:
            self._state.event_handlers[event_type] = []
        
        # Add handler with priority
        self._state.event_handlers[event_type].append((priority, handler))
        # Sort by priority
        self._state.event_handlers[event_type].sort(key=lambda x: x[0], reverse=True)
        
        logger.info(f"Registered handler for {event_type} with priority {priority}")
    
    def unregister_handler(self, event_type: str, handler: Callable) -> None:
        """Unregister an event handler"""
        if event_type in self._state.event_handlers:
            self._state.event_handlers[event_type] = [
                (p, h) for p, h in self._state.event_handlers[event_type] if h != handler
            ]
            logger.info(f"Unregistered handler for {event_type}")
    
    async def _process_tick(self) -> None:
        """Process a single tick"""
        try:
            # Record start time
            start_time = time.time()
            
            # Process subsystems
            for name, subsystem in self._subsystems.items():
                try:
                    subsystem_start = time.time()
                    if hasattr(subsystem, 'process_tick'):
                        await subsystem.process_tick()
                    elif hasattr(subsystem, 'tick'):
                        await subsystem.tick()
                    subsystem_time = time.time() - subsystem_start
                    self._state.performance_metrics[f"{name}_time"] = subsystem_time
                except Exception as e:
                    logger.error(f"Error processing subsystem {name}: {e}")
            
            # Calculate tick metrics
            total_time = time.time() - start_time
            self._state.performance_metrics["total_time"] = total_time
            self._state.performance_metrics["tick_rate"] = 1.0 / total_time if total_time > 0 else 0
            
            # Update tick count
            self._state.tick_count += 1
            
            # Output tick data to stdout for visualizer scripts
            tick_data = {
                "tick": self._state.tick_count,
                "timestamp": time.time(),
                "metrics": self._state.performance_metrics,
                "subsystems": {
                    name: {
                        "active": True,
                        "metrics": self._state.performance_metrics.get(f"{name}_time", 0)
                    }
                    for name in self._subsystems.keys()
                },
                "thermal_state": self._state.thermal_state,
                "scup": getattr(self, 'scup_tracker', {}).get_scup() if hasattr(self, 'scup_tracker') else 0.5,
                "mood": getattr(self, 'mood_probe', {}).get_mood() if hasattr(self, 'mood_probe') else {"base_level": 0.5},
                "entropy": 0.5  # Default entropy value
            }
            self.output_tick_data_to_stdout(tick_data)
            
            # Broadcast tick state
            await self._broadcast_tick_state()
            
        except Exception as e:
            logger.error(f"Error processing tick: {e}")
    
    async def _broadcast_tick_state(self):
        """Broadcast current tick state to all subscribers"""
        try:
            state = {
                "tick": self._state.tick_count,
                "timestamp": time.time(),
                "metrics": self._state.performance_metrics,
                "subsystems": {
                    name: {
                        "active": True,
                        "metrics": self._state.performance_metrics.get(f"{name}_time", 0)
                    }
                    for name in self._subsystems.keys()
                }
            }
            
            # Broadcast to all subscribers
            for callback in self._state.event_handlers.get('tick', []):
                try:
                    await callback(state)
                except Exception as e:
                    logger.error(f"Error broadcasting tick state: {e}")
                    
        except Exception as e:
            logger.error(f"Error broadcasting tick state: {e}")
    
    def register_subsystem(self, name: str, subsystem: Any, priority: int = 0) -> None:
        """Register a subsystem with the tick engine"""
        self._subsystems[name] = subsystem
        logger.info(f"Registered subsystem {name} with priority {priority}")
        
        # Register tick handler for the subsystem
        if hasattr(subsystem, 'on_tick'):
            self.register_handler('tick', subsystem.on_tick, priority)
            
        # Register event handler if available
        if hasattr(subsystem, 'on_event'):
            self.register_handler('event', subsystem.on_event, priority)

    def get_subsystem(self, name: str) -> Optional[Any]:
        """Get a registered subsystem by name"""
        return self._subsystems.get(name)

    def get_active_processes(self) -> List[str]:
        """Get list of active subsystem processes"""
        return [name for name, subsystem in self._subsystems.items() 
                if hasattr(subsystem, 'is_active') and subsystem.is_active()]

    def add_tick_callback(self, callback):
        """Add a callback to be called on each tick"""
        self.tick_callbacks.append(callback)
    
    def remove_tick_callback(self, callback):
        """Remove a tick callback"""
        if callback in self.tick_callbacks:
            self.tick_callbacks.remove(callback)
    
    async def shutdown(self):
        """Shutdown the tick engine"""
        self._state.is_running = False
        logger.info("Shutting down tick engine")
        
        # Wait for any pending ticks to complete
        await asyncio.sleep(self.tick_interval * 2)
        
        # Clear all callbacks and subsystems
        self.tick_callbacks.clear()
        self._subsystems.clear()
        self.tick_history.clear()
        self.event_queue.clear()

    async def _process_event_queue(self):
        """Process events in the queue"""
        while self.event_queue:
            event = self.event_queue.pop(0)
            try:
                event_type, data = event
                # Process event based on type
                if event_type == "tick":
                    await self._process_tick()
                elif event_type == "subsystem":
                    subsystem_name = data.get("name")
                    if subsystem_name in self._subsystems:
                        await self._subsystems[subsystem_name].process_tick()
                # Add more event types as needed
            except Exception as e:
                logger.error(f"Error processing event: {e}")

    def _calculate_interval(self) -> float:
        """Calculate the next tick interval based on system state and performance"""
        try:
            # Base interval from config or default
            base_interval = self._config.get('base_interval', 0.1)
            
            # Adjust based on system load
            cpu_usage = self._state.performance_metrics['cpu_usage']
            memory_usage = self._state.performance_metrics['memory_usage']
            
            # Calculate load factor (0.5 to 2.0)
            load_factor = 1.0
            if cpu_usage > 80 or memory_usage > 80:
                load_factor = 2.0  # Slow down under high load
            elif cpu_usage < 20 and memory_usage < 20:
                load_factor = 0.5  # Speed up under low load
            
            # Adjust based on thermal state
            thermal_factor = 1.0
            if self._state.thermal_state['heat'] > 0.8:
                thermal_factor = 1.5  # Slow down when hot
            elif self._state.thermal_state['heat'] < 0.2:
                thermal_factor = 0.8  # Speed up when cool
            
            # Calculate final interval
            interval = base_interval * load_factor * thermal_factor
            
            # Ensure interval stays within bounds
            min_interval = self._config.get('min_interval', 0.05)
            max_interval = self._config.get('max_interval', 0.5)
            interval = max(min_interval, min(max_interval, interval))
            
            return interval
            
        except Exception as e:
            logger.error(f"Error calculating interval: {e}")
            return 0.1  # Default to 100ms on error

    def output_tick_data_to_stdout(self, tick_data: Dict[str, Any]) -> None:
        """Output tick data as JSON to stdout for visualizer scripts"""
        try:
            # Ensure the data is JSON serializable
            json_data = json.dumps(tick_data, default=str)
            print(json_data, flush=True)
        except BrokenPipeError:
            # Visualizer scripts are not running or not reading from stdin
            # This is normal when running backend standalone
            pass
        except Exception as e:
            logger.error(f"Error outputting tick data to stdout: {e}")

# Global instance
tick_engine = UnifiedTickEngine()

def register_handler(event_type: str, handler: Callable, priority: int = 0) -> None:
    """Register an event handler"""
    return tick_engine.register_handler(event_type, handler, priority)

def unregister_handler(event_type: str, handler: Callable) -> None:
    """Unregister an event handler"""
    return tick_engine.unregister_handler(event_type, handler)

def patch_tick_engine(handler: Callable, event_type: str = 'tick', priority: int = 0) -> None:
    """
    Patch the tick engine with a custom handler.
    
    Args:
        handler: The handler function to register
        event_type: The type of event to handle (default: 'tick')
        priority: Handler priority (default: 0)
    """
    tick_engine.register_handler(event_type, handler, priority)
    logger.info(f"Patched tick engine with handler for {event_type}")

# Export key functions
__all__ = [
    'tick_engine',
    'register_handler',
    'unregister_handler',
    'patch_tick_engine'
] 