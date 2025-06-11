"""
Unified Tick Engine - Advanced timing and event management system
"""

import asyncio
import logging
import time
import os
import json
from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import psutil
import yaml

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
        start_time = time.time()
        self._state.tick_count += 1
        
        # Calculate delta time
        delta = start_time - self._state.last_tick_time
        self._state.last_tick_time = start_time
        
        # Update thermal state
        await self._update_thermal_state(delta)
        
        # Emit tick event
        await self._emit_event("tick", {
            "tick": self._state.tick_count,
            "delta": delta,
            "interval": self._state.current_interval,
            "thermal": self._state.thermal_state,
            "performance": self._state.performance_metrics
        })
        
        # Update interval
        self._state.current_interval = self._calculate_interval()
        
        # Calculate event latency
        self._state.performance_metrics['event_latency'] = time.time() - start_time
    
    async def _update_thermal_state(self, delta: float) -> None:
        """Update thermal state based on system load"""
        # Calculate heat based on CPU usage
        cpu_heat = self._state.performance_metrics['cpu_usage'] / 100.0
        
        # Update thermal momentum
        self._state.thermal_state['momentum'] *= self._config.get('thermal_momentum_decay', 0.95)
        self._state.thermal_state['momentum'] += cpu_heat * delta
        
        # Update heat level
        self._state.thermal_state['heat'] = min(
            1.0,
            max(0.0, self._state.thermal_state['heat'] + self._state.thermal_state['momentum'])
        )
        
        # Update stability
        if self._state.thermal_state['heat'] > 0.8:
            self._state.thermal_state['stability'] *= 0.95
        else:
            self._state.thermal_state['stability'] = min(1.0, self._state.thermal_state['stability'] + 0.01)
    
    async def _process_event_queue(self) -> None:
        """Process pending events in queue"""
        while self._state.event_queue:
            event_type, data = self._state.event_queue.popleft()
            await self._emit_event(event_type, data)
    
    def _calculate_interval(self) -> float:
        """Calculate next tick interval based on system state"""
        # Base interval from config
        base_interval = self._config.get('tick_interval', 1.0)
        
        # Adjust based on thermal state
        thermal_factor = 1.0
        if self._state.thermal_state['heat'] > 0.8:
            thermal_factor = 1.5  # Slow down when hot
        elif self._state.thermal_state['heat'] < 0.2:
            thermal_factor = 0.8  # Speed up when cool
        
        # Adjust based on performance
        perf_factor = 1.0
        if self._state.performance_metrics['cpu_usage'] > 80:
            perf_factor = 1.3  # Slow down under high CPU load
        
        # Calculate final interval
        interval = base_interval * thermal_factor * perf_factor
        
        # Apply bounds
        return max(
            self._config.get('tick_interval_min', 0.1),
            min(self._config.get('tick_interval_max', 5.0), interval)
        )
    
    async def _emit_event(self, event_type: str, data: Dict) -> None:
        """Emit an event to registered handlers"""
        if event_type in self._state.event_handlers:
            for _, handler in self._state.event_handlers[event_type]:
                try:
                    await handler(data)
                except Exception as e:
                    logger.error(f"Error in event handler: {e}")
                    self._state.error_count += 1
    
    def queue_event(self, event_type: str, data: Dict) -> None:
        """Queue an event for processing"""
        self._state.event_queue.append((event_type, data))
    
    def get_state(self) -> Dict:
        """Get current tick engine state"""
        return {
            "tick_count": self._state.tick_count,
            "current_interval": self._state.current_interval,
            "target_interval": self._state.target_interval,
            "is_running": self._state.is_running,
            "last_tick_time": self._state.last_tick_time,
            "event_types": list(self._state.event_handlers.keys()),
            "thermal_state": self._state.thermal_state,
            "performance_metrics": self._state.performance_metrics,
            "error_count": self._state.error_count,
            "recovery_count": self._state.recovery_count
        }
    
    def log_tick_event(self, event_type: str, details: Dict) -> None:
        """Log a tick-related event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "details": details,
            "state": self.get_state()
        }
        
        # Write to log file
        log_file = os.path.join(self._log_dir, "tick_events.log")
        with open(log_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        logger.info(f"Logged tick event: {event_type}")
    
    def export_state(self) -> Dict:
        """Export current tick engine state"""
        return {
            "timestamp": datetime.now().isoformat(),
            "state": self.get_state(),
            "event_handlers": {
                event_type: len(handlers)
                for event_type, handlers in self._state.event_handlers.items()
            },
            "config": self._config
        }

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