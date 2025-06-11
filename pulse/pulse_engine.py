#!/usr/bin/env python3
"""
pulse_engine.py

Unified Pulse Engine interface for DAWN cognitive system
Combines zone tracking, state timing, and overheat detection

Integration:
    Primary: dawn.pulse.diagnostics.pulse_engine
    Dependencies: zone_tracker.py, state_timer.py, overheat_detector.py
    Interfaces with: Core tick engine, thermal monitoring
    Output streams: Unified diagnostics, event streams  
    
Author: DAWN Development Team
Epoch: epoch_0601
"""

import time
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime
import logging
import yaml
import os
from pathlib import Path
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from functools import lru_cache
from collections import deque
import json
import psutil
import statistics
from typing import Deque

# Pulse engine components
from pulse.zone_tracker import PulseZoneTracker, PulseZone, PulseEvent
from pulse.state_timer import PulseStateTimer
from pulse.overheat_detector import PulseOverheatDetector, ThermalEvent, ThermalAlert

# Core DAWN components (with fallbacks for testing)
try:
    from core.tick_engine import get_current_tick
    from health.thermal_monitoring import temperature_tracker
except ImportError:
    def get_current_tick():
        return int(time.time() * 1000)
    
    class MockThermalTracker:
        def __init__(self):
            self.base_temp = 30
            self.variation = 0
            
        def get_temperature(self):
            import random
            # Simulate temperature patterns
            self.variation += random.uniform(-2, 3)
            self.variation = max(-20, min(60, self.variation))
            return self.base_temp + self.variation
            
    temperature_tracker = MockThermalTracker()

logger = logging.getLogger(__name__)

@dataclass
class PulseEngineEvent:
    """Unified pulse engine event"""
    tick: int
    zone_event: Optional[PulseEvent]
    thermal_event: Optional[ThermalEvent]
    current_state: Dict[str, Any]
    
    @property
    def is_critical(self) -> bool:
        """Check if event represents critical condition"""
        if self.thermal_event:
            return self.thermal_event.alert_level in [ThermalAlert.CRITICAL, ThermalAlert.EMERGENCY]
        return False

# Add new dataclass for zone tracking
@dataclass
class PulseZoneState:
    """Represents the current state of a pulse zone"""
    name: str
    temperature: float
    last_update: datetime
    is_active: bool = False
    transition_count: int = 0
    total_duration: float = 0.0
    
    def update(self, temperature: float) -> None:
        """Update zone state with new temperature"""
        self.temperature = temperature
        self.last_update = datetime.utcnow()
        self.total_duration += (self.last_update - self.last_update).total_seconds()
        
    def activate(self) -> None:
        """Mark zone as active"""
        if not self.is_active:
            self.is_active = True
            self.transition_count += 1
            
    def deactivate(self) -> None:
        """Mark zone as inactive"""
        if self.is_active:
            self.is_active = False
            self.transition_count += 1

# Add configuration dataclass
@dataclass
class PulseConfig:
    """Configuration for pulse engine"""
    pressure_limit: float = 0.85
    cooldown_ms: int = 1000
    zone_alert_level: float = 0.75
    thermal_thresholds: Dict[str, float] = field(default_factory=lambda: {
        'warning': 0.7,
        'critical': 0.85,
        'emergency': 0.95
    })
    zone_thresholds: Dict[str, float] = field(default_factory=lambda: {
        'calm': 0.3,
        'active': 0.7,
        'surge': 0.9
    })
    monitoring: Dict[str, Any] = field(default_factory=lambda: {
        'interval': 1.0,
        'history_size': 100,
        'log_level': 'INFO'
    })
    
    @classmethod
    def from_yaml(cls, path: str) -> 'PulseConfig':
        """Load configuration from YAML file"""
        try:
            with open(path, 'r') as f:
                config_data = yaml.safe_load(f)
            return cls(**config_data)
        except Exception as e:
            logger.warning(f"Failed to load config from {path}: {e}")
            return cls()  # Return default config
            
    def to_yaml(self, path: str) -> None:
        """Save configuration to YAML file"""
        try:
            config_data = {
                'pressure_limit': self.pressure_limit,
                'cooldown_ms': self.cooldown_ms,
                'zone_alert_level': self.zone_alert_level,
                'thermal_thresholds': self.thermal_thresholds,
                'zone_thresholds': self.zone_thresholds,
                'monitoring': self.monitoring
            }
            with open(path, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Failed to save config to {path}: {e}")

class ConfigWatcher(FileSystemEventHandler):
    """Watch for configuration file changes"""
    def __init__(self, pulse_engine):
        self.pulse_engine = pulse_engine
        
    def on_modified(self, event):
        if event.src_path.endswith('pulse_config.yaml'):
            logger.info("Configuration file changed, reloading...")
            self.pulse_engine.reload_config()

# Add batch processing support
@dataclass
class ZoneBatch:
    """Batch of zone updates to process"""
    temperatures: List[float]
    burn_rates: List[float]
    timestamps: List[datetime]
    
    def __post_init__(self):
        if not (len(self.temperatures) == len(self.burn_rates) == len(self.timestamps)):
            raise ValueError("All batch lists must have the same length")

# Add metrics tracking
@dataclass
class PulseMetrics:
    """Metrics for pulse engine performance"""
    timestamp: datetime
    system_pressure: float
    active_zones: int
    avg_tick_duration: float
    memory_usage_mb: float
    batch_size: int
    event_count: int
    thermal_stats: Dict[str, float]
    zone_stats: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for JSON serialization"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'system_pressure': self.system_pressure,
            'active_zones': self.active_zones,
            'avg_tick_duration': self.avg_tick_duration,
            'memory_usage_mb': self.memory_usage_mb,
            'batch_size': self.batch_size,
            'event_count': self.event_count,
            'thermal_stats': self.thermal_stats,
            'zone_stats': self.zone_stats
        }

class PulseEngine:
    """Manages system rhythms and patterns"""
    
    # Cache static zone definitions
    _ZONE_DEFINITIONS = {
        '🟢 calm': {'color': 'green', 'emoji': '🟢', 'base_threshold': 0.3},
        '🟡 active': {'color': 'yellow', 'emoji': '🟡', 'base_threshold': 0.7},
        '🔴 surge': {'color': 'red', 'emoji': '🔴', 'base_threshold': 0.9}
    }
    
    def __init__(self, config_path: str = 'config/pulse_config.yaml'):
        self.config_path = config_path
        self.config = PulseConfig.from_yaml(config_path)
        self.config_lock = threading.RLock()
        
        # Initialize components with config
        self.active = False
        self.current_zone = None
        self.pulse_count = 0
        self.zone_tracker = PulseZoneTracker()
        self.state_timer = PulseStateTimer()
        self.overheat_detector = PulseOverheatDetector()
        self.heat_history = []
        self.last_update = time.time()
        self.thermal_stats = {
            'min_temp': float('inf'),
            'max_temp': float('-inf'),
            'avg_temp': 0.0,
            'total_updates': 0
        }
        
        # Initialize zone tracking with config thresholds
        self.zones: Dict[str, PulseZoneState] = {
            '🟢 calm': PulseZoneState('🟢 calm', 0.0, datetime.utcnow()),
            '🟡 active': PulseZoneState('🟡 active', 0.0, datetime.utcnow()),
            '🔴 surge': PulseZoneState('🔴 surge', 0.0, datetime.utcnow())
        }
        
        # Event bus integration
        self.event_bus = None
        self.event_count = 0
        self.last_event_time = None
        
        # Add batch processing buffers
        self.batch_buffer = deque(maxlen=100)  # Store recent updates
        self.last_batch_time = time.time()
        self.batch_size = 10  # Default batch size
        
        # Add metrics tracking
        self.tick_durations: Deque[float] = deque(maxlen=100)  # Store last 100 tick durations
        self.last_tick_time = time.time()
        self.metrics_log_path = Path('logs/pulse_metrics.json')
        self.metrics_log_path.parent.mkdir(exist_ok=True)
        self.metrics_interval = 10  # Log metrics every 10 ticks
        
        # Start config watcher
        self._start_config_watcher()
        
    def _start_config_watcher(self):
        """Start watching for config file changes"""
        try:
            observer = Observer()
            observer.schedule(ConfigWatcher(self), 
                            path=os.path.dirname(self.config_path),
                            recursive=False)
            observer.start()
            logger.info(f"Started watching {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to start config watcher: {e}")
            
    def reload_config(self):
        """Reload configuration from file"""
        with self.config_lock:
            new_config = PulseConfig.from_yaml(self.config_path)
            self.config = new_config
            logger.info("Configuration reloaded")
            
            # Update components with new config
            self._update_component_configs()
            
    def _update_component_configs(self):
        """Update all components with new configuration"""
        # Update zone thresholds
        for zone_name, threshold in self.config.zone_thresholds.items():
            if zone_name in self.zones:
                self.zones[zone_name].threshold = threshold
                
        # Update thermal thresholds
        if hasattr(self.overheat_detector, 'update_thresholds'):
            self.overheat_detector.update_thresholds(self.config.thermal_thresholds)
            
        # Update monitoring settings
        if hasattr(self, 'run_diagnostic_loop'):
            self.monitoring_interval = self.config.monitoring['interval']
            
    def wire(self, orchestrator):
        """Wire into the system"""
        self.event_bus = orchestrator.event_bus
        self.zone_tracker.wire(orchestrator)
        self.state_timer.wire(orchestrator)
        self.overheat_detector.wire(orchestrator)
        self.active = True
        logger.info("Pulse engine wired")
        
    def wire_to_event_bus(self, event_bus) -> None:
        """
        Wire the pulse engine to the event bus system
        
        Args:
            event_bus: Event bus instance to wire to
        """
        self.event_bus = event_bus
        
        # Subscribe to pulse events
        self.event_bus.subscribe('pulse_event', self._handle_pulse_event)
        self.event_bus.subscribe('thermal_event', self._handle_thermal_event)
        self.event_bus.subscribe('zone_transition', self._handle_zone_transition)
        
        logger.info("Pulse engine wired to event bus")
        
    def _handle_pulse_event(self, event: PulseEngineEvent) -> None:
        """Handle incoming pulse events"""
        self.event_count += 1
        self.last_event_time = datetime.utcnow()
        
        # Update engine state
        if event.thermal_event:
            self.update(event.thermal_event.temperature, event.thermal_event.burn_rate)
            
        # Log event processing
        if self.event_count % 100 == 0:
            logger.info(f"Processed {self.event_count} events")
            
    def _handle_thermal_event(self, event: ThermalEvent) -> None:
        """Handle thermal events"""
        if event.alert_level in [ThermalAlert.CRITICAL, ThermalAlert.EMERGENCY]:
            logger.warning(f"Critical thermal event: {event.alert_level}")
            # Trigger emergency cooling if needed
            self._trigger_emergency_cooling()
            
    def _handle_zone_transition(self, event: Dict[str, Any]) -> None:
        """Handle zone transition events"""
        from_zone = event.get('from_zone')
        to_zone = event.get('to_zone')
        
        if from_zone in self.zones:
            self.zones[from_zone].deactivate()
        if to_zone in self.zones:
            self.zones[to_zone].activate()
            
        logger.info(f"Zone transition: {from_zone} → {to_zone}")
        
    def _trigger_emergency_cooling(self) -> None:
        """Trigger emergency cooling procedures"""
        logger.warning("Triggering emergency cooling")
        # Implement emergency cooling logic here
        
    def get_active_zones(self) -> Dict[str, Dict[str, Any]]:
        """
        Get current state of all registered zones
        
        Returns:
            Dict mapping zone names to their current state
        """
        current_time = datetime.utcnow()
        active_zones = {}
        
        for name, zone in self.zones.items():
            # Calculate time since last update
            time_since_update = (current_time - zone.last_update).total_seconds()
            
            active_zones[name] = {
                'name': zone.name,
                'temperature': zone.temperature,
                'last_update': zone.last_update.isoformat(),
                'is_active': zone.is_active,
                'time_since_update': time_since_update,
                'transition_count': zone.transition_count,
                'total_duration': zone.total_duration
            }
            
        return active_zones
        
    def update_zone_state(self, zone_name: str, temperature: float) -> None:
        """
        Update the state of a specific zone
        
        Args:
            zone_name: Name of the zone to update
            temperature: New temperature reading
        """
        if zone_name in self.zones:
            self.zones[zone_name].update(temperature)
            
            # Emit zone update event if wired
            if self.event_bus:
                self.event_bus.emit('zone_update', {
                    'zone': zone_name,
                    'temperature': temperature,
                    'timestamp': datetime.utcnow().isoformat()
                })
        
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        return {
            "active": self.active,
            "current_zone": self.current_zone,
            "pulse_count": self.pulse_count,
            "zone_tracker": self.zone_tracker.get_status(),
            "state_timer": self.state_timer.get_status(),
            "overheat_detector": self.overheat_detector.get_status()
        }
        
    @lru_cache(maxsize=128)
    def _normalize_temperature(self, temp: float) -> float:
        """Normalize temperature to 0-1 range"""
        return max(0.0, min(1.0, temp / 100.0))
        
    @lru_cache(maxsize=128)
    def _calculate_pressure(self, temp: float, burn_rate: float) -> float:
        """Calculate system pressure from temperature and burn rate"""
        return self._normalize_temperature(temp) * burn_rate
        
    @lru_cache(maxsize=32)
    def _get_zone_threshold(self, zone_name: str) -> float:
        """Get threshold for a specific zone"""
        return self._ZONE_DEFINITIONS.get(zone_name, {}).get('base_threshold', 0.5)
        
    def _log_metrics(self) -> None:
        """Log current metrics to JSON file"""
        try:
            metrics = self.get_metrics()
            
            # Load existing metrics if file exists
            existing_metrics = []
            if self.metrics_log_path.exists():
                with open(self.metrics_log_path, 'r') as f:
                    existing_metrics = json.load(f)
            
            # Add new metrics
            existing_metrics.append(metrics.to_dict())
            
            # Keep only last 1000 entries
            if len(existing_metrics) > 1000:
                existing_metrics = existing_metrics[-1000:]
            
            # Write updated metrics
            with open(self.metrics_log_path, 'w') as f:
                json.dump(existing_metrics, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to log metrics: {e}")
            
    def get_metrics(self) -> PulseMetrics:
        """
        Get current engine metrics
        
        Returns:
            PulseMetrics object containing current performance metrics
        """
        # Calculate tick duration
        current_time = time.time()
        tick_duration = current_time - self.last_tick_time
        self.tick_durations.append(tick_duration)
        self.last_tick_time = current_time
        
        # Calculate average tick duration
        avg_tick_duration = statistics.mean(self.tick_durations) if self.tick_durations else 0.0
        
        # Get memory usage
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_usage_mb = memory_info.rss / (1024 * 1024)  # Convert to MB
        
        # Calculate system pressure
        current_pressure = 0.0
        if self.batch_buffer:
            pressures = [self._calculate_pressure(t, b) 
                        for t, b in zip([x[0] for x in self.batch_buffer], 
                                      [x[1] for x in self.batch_buffer])]
            current_pressure = max(pressures) if pressures else 0.0
            
        # Count active zones
        active_zones = sum(1 for zone in self.zones.values() if zone.is_active)
        
        # Get zone statistics
        zone_stats = {
            name: {
                'is_active': zone.is_active,
                'temperature': zone.temperature,
                'transition_count': zone.transition_count,
                'total_duration': zone.total_duration
            }
            for name, zone in self.zones.items()
        }
        
        return PulseMetrics(
            timestamp=datetime.utcnow(),
            system_pressure=current_pressure,
            active_zones=active_zones,
            avg_tick_duration=avg_tick_duration,
            memory_usage_mb=memory_usage_mb,
            batch_size=len(self.batch_buffer),
            event_count=self.event_count,
            thermal_stats={
                'min_temp': self.thermal_stats['min_temp'],
                'max_temp': self.thermal_stats['max_temp'],
                'avg_temp': self.thermal_stats['avg_temp'],
                'total_updates': self.thermal_stats['total_updates']
            },
            zone_stats=zone_stats
        )
        
    def update(self, temperature: float, burn_rate: float) -> PulseEngineEvent:
        """Update engine state with new temperature and burn rate"""
        if not self.active:
            return None
            
        with self.config_lock:
            # Add to batch buffer
            self.batch_buffer.append((temperature, burn_rate, datetime.utcnow()))
            
            # Process batch if buffer is full or enough time has passed
            current_time = time.time()
            if (len(self.batch_buffer) >= self.batch_size or 
                current_time - self.last_batch_time >= 1.0):
                event = self._process_batch()
            else:
                event = self._process_single_update(temperature, burn_rate)
                
            # Log metrics periodically
            if self.pulse_count % self.metrics_interval == 0:
                self._log_metrics()
                
            return event
            
    def _process_batch(self) -> PulseEngineEvent:
        """Process a batch of updates"""
        if not self.batch_buffer:
            return None
            
        # Create batch
        batch = ZoneBatch(
            temperatures=[t[0] for t in self.batch_buffer],
            burn_rates=[t[1] for t in self.batch_buffer],
            timestamps=[t[2] for t in self.batch_buffer]
        )
        
        # Calculate batch metrics
        avg_temp = sum(batch.temperatures) / len(batch.temperatures)
        avg_burn = sum(batch.burn_rates) / len(batch.burn_rates)
        max_pressure = max(self._calculate_pressure(t, b) 
                         for t, b in zip(batch.temperatures, batch.burn_rates))
        
        # Process the batch
        current_tick = get_current_tick()
        self.pulse_count += len(batch.temperatures)
        
        # Update thermal stats
        self.thermal_stats['min_temp'] = min(self.thermal_stats['min_temp'], min(batch.temperatures))
        self.thermal_stats['max_temp'] = max(self.thermal_stats['max_temp'], max(batch.temperatures))
        self.thermal_stats['total_updates'] += len(batch.temperatures)
        
        # Calculate new average
        total_temp = self.thermal_stats['avg_temp'] * (self.thermal_stats['total_updates'] - len(batch.temperatures))
        total_temp += sum(batch.temperatures)
        self.thermal_stats['avg_temp'] = total_temp / self.thermal_stats['total_updates']
        
        # Update components
        zone_event = self.zone_tracker.update(avg_temp, avg_burn)
        thermal_event = self.overheat_detector.check_temperature(avg_temp)
        self.state_timer.update(current_tick)
        
        # Create unified event
        event = PulseEngineEvent(
            tick=current_tick,
            zone_event=zone_event,
            thermal_event=thermal_event,
            current_state=self.get_status()
        )
        
        # Check for critical conditions
        if max_pressure > self.config.pressure_limit:
            logger.warning(f"Batch max pressure {max_pressure:.2f} exceeds limit {self.config.pressure_limit}")
            if hasattr(self, 'event_bus'):
                self.event_bus.emit('pulse_critical', event)
                
        # Clear buffer and update time
        self.batch_buffer.clear()
        self.last_batch_time = time.time()
        
        return event
        
    def _process_single_update(self, temperature: float, burn_rate: float) -> PulseEngineEvent:
        """Process a single update"""
        current_tick = get_current_tick()
        self.pulse_count += 1
        
        # Calculate pressure
        system_pressure = self._calculate_pressure(temperature, burn_rate)
        
        # Update thermal stats
        self.thermal_stats['min_temp'] = min(self.thermal_stats['min_temp'], temperature)
        self.thermal_stats['max_temp'] = max(self.thermal_stats['max_temp'], temperature)
        self.thermal_stats['total_updates'] += 1
        self.thermal_stats['avg_temp'] = (
            (self.thermal_stats['avg_temp'] * (self.thermal_stats['total_updates'] - 1) + temperature) /
            self.thermal_stats['total_updates']
        )
        
        # Update components
        zone_event = self.zone_tracker.update(temperature, burn_rate)
        thermal_event = self.overheat_detector.check_temperature(temperature)
        self.state_timer.update(current_tick)
        
        # Create unified event
        event = PulseEngineEvent(
            tick=current_tick,
            zone_event=zone_event,
            thermal_event=thermal_event,
            current_state=self.get_status()
        )
        
        # Check pressure threshold
        if system_pressure > self.config.pressure_limit:
            logger.warning(f"System pressure {system_pressure:.2f} exceeds limit {self.config.pressure_limit}")
            if hasattr(self, 'event_bus'):
                self.event_bus.emit('pulse_critical', event)
                
        return event
        
    def run_diagnostic_loop(self, duration: int = 60, interval: float = 1.0, pressure_threshold: float = 0.85):
        """
        Run diagnostic loop with self-monitoring capabilities
        
        Args:
            duration: Total runtime in seconds
            interval: Time between diagnostics in seconds
            pressure_threshold: Warning threshold for system pressure
        """
        start_time = time.time()
        end_time = start_time + duration
        last_diagnostic = start_time
        
        # Initialize monitoring state
        monitoring_state = {
            'pressure_history': [],
            'zone_transitions': [],
            'warning_count': 0,
            'last_warning': None,
            'max_pressure': 0.0,
            'zone_duration': {'🟢 calm': 0, '🟡 active': 0, '🔴 surge': 0}
        }
        
        logger.info(f"Starting diagnostic loop for {duration}s (interval: {interval}s)")
        logger.info(f"Pressure threshold set to {pressure_threshold}")
        
        try:
            while time.time() < end_time:
                current_time = time.time()
                
                # Check if it's time for a diagnostic
                if current_time - last_diagnostic >= interval:
                    # Get current system state
                    temp = temperature_tracker.get_temperature()
                    burn_rate = min(1.0, temp / 100 * 1.2)
                    system_pressure = burn_rate * (temp / 100)
                    
                    # Update engine
                    event = self.update(temp, burn_rate)
                    
                    # Track pressure history
                    monitoring_state['pressure_history'].append(system_pressure)
                    monitoring_state['max_pressure'] = max(monitoring_state['max_pressure'], system_pressure)
                    
                    # Track zone duration
                    current_zone = event.current_state['current_zone'] if event else '🟢 calm'
                    monitoring_state['zone_duration'][current_zone] += interval
                    
                    # Check for zone transitions
                    if event and event.zone_event:
                        monitoring_state['zone_transitions'].append({
                            'time': current_time,
                            'from_zone': event.zone_event.previous_zone,
                            'to_zone': event.zone_event.new_zone
                        })
                        logger.info(f"Zone transition: {event.zone_event.previous_zone} → {event.zone_event.new_zone}")
                    
                    # Check pressure threshold
                    if system_pressure > pressure_threshold:
                        warning_msg = f"⚠️ High system pressure: {system_pressure:.2f} (threshold: {pressure_threshold})"
                        logger.warning(warning_msg)
                        monitoring_state['warning_count'] += 1
                        monitoring_state['last_warning'] = current_time
                        
                        # Log detailed state during high pressure
                        logger.warning(f"Current state: Zone={current_zone}, Temp={temp:.1f}°C, Burn={burn_rate:.2f}")
                    
                    # Log periodic summary
                    if len(monitoring_state['pressure_history']) % 10 == 0:
                        logger.info(
                            f"Diagnostic Summary:\n"
                            f"  Runtime: {current_time - start_time:.1f}s\n"
                            f"  Current Pressure: {system_pressure:.2f}\n"
                            f"  Max Pressure: {monitoring_state['max_pressure']:.2f}\n"
                            f"  Warnings: {monitoring_state['warning_count']}\n"
                            f"  Zone Durations: {monitoring_state['zone_duration']}"
                        )
                    
                    last_diagnostic = current_time
                
                time.sleep(0.1)  # Small sleep to prevent CPU overuse
                
        except KeyboardInterrupt:
            logger.info("Diagnostic loop interrupted by user")
        except Exception as e:
            logger.error(f"Error in diagnostic loop: {str(e)}")
        finally:
            # Final summary
            logger.info("\n=== Diagnostic Loop Complete ===")
            logger.info(f"Total runtime: {time.time() - start_time:.1f}s")
            logger.info(f"Total warnings: {monitoring_state['warning_count']}")
            logger.info(f"Max pressure reached: {monitoring_state['max_pressure']:.2f}")
            logger.info("Zone duration summary:")
            for zone, duration in monitoring_state['zone_duration'].items():
                logger.info(f"  {zone}: {duration:.1f}s")
            
            # Calculate stability metrics
            if monitoring_state['pressure_history']:
                avg_pressure = sum(monitoring_state['pressure_history']) / len(monitoring_state['pressure_history'])
                pressure_variance = sum((p - avg_pressure) ** 2 for p in monitoring_state['pressure_history']) / len(monitoring_state['pressure_history'])
                logger.info(f"Average pressure: {avg_pressure:.2f}")
                logger.info(f"Pressure variance: {pressure_variance:.2f}")
            
            logger.info(f"Zone transitions: {len(monitoring_state['zone_transitions'])}")
            
            return monitoring_state
        
    def get_unified_display(self) -> str:
        """Get unified status display"""
        status = self.get_status()
        thermal = self.thermal_stats
        
        display = [
            "=== PULSE ENGINE STATUS ===",
            f"Active: {'✅' if status['active'] else '❌'}",
            f"Current Zone: {status['current_zone']}",
            f"Pulse Count: {status['pulse_count']}",
            "\nThermal Stats:",
            f"  Temperature: {thermal['avg_temp']:.1f}°C",
            f"  Range: {thermal['min_temp']:.1f}°C - {thermal['max_temp']:.1f}°C",
            f"  Updates: {thermal['total_updates']}",
            "\nComponent Status:",
            f"  Zone Tracker: {status['zone_tracker']['active']}",
            f"  State Timer: {status['state_timer']['active']}",
            f"  Overheat Detector: {status['overheat_detector']['active']}"
        ]
        
        return "\n".join(display)
        
    def get_diagnostics(self) -> Dict[str, Any]:
        """Get comprehensive diagnostics"""
        return {
            'status': self.get_status(),
            'thermal_stats': self.thermal_stats,
            'heat_history': self.heat_history[-100:],  # Last 100 readings
            'uptime': time.time() - self.last_update,
            'pulse_count': self.pulse_count,
            'metrics': {
                'avg_pulse_rate': self.pulse_count / (time.time() - self.last_update) if self.last_update else 0,
                'thermal_stability': 1.0 - (self.thermal_stats['max_temp'] - self.thermal_stats['min_temp']) / 100,
                'zone_stability': len(set(self.heat_history[-10:])) / 10 if self.heat_history else 1.0
            }
        }
        
    def shutdown(self):
        """Shutdown the engine"""
        self.active = False
        self.current_zone = None
        self.zone_tracker.shutdown()
        self.state_timer.shutdown()
        self.overheat_detector.shutdown()
        logger.info("Pulse engine shut down")


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    print("=== DAWN PULSE ENGINE TEST ===")
    print("Unified diagnostics interface")
    print("="*50 + "\n")
    
    # Create pulse engine
    engine = PulseEngine()
    
    # Run test scenarios
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        # Run diagnostic loop
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        engine.run_diagnostic_loop(duration=duration)
    else:
        # Run quick test
        print("Running quick test sequence...\n")
        
        # Simulate temperature patterns
        test_temps = [
            30, 35, 40, 45, 50,  # Gradual rise
            55, 60, 65, 70, 75,  # Into surge
            80, 85, 80, 75, 70,  # Critical and recovery
            65, 60, 55, 50, 45,  # Cool down
            40, 35, 30, 25, 20   # Return to calm
        ]
        
        for i, temp in enumerate(test_temps):
            # Calculate burn rate based on temperature
            burn_rate = min(1.0, temp / 100 * 1.2)
            
            # Update engine
            event = engine.update(temp, burn_rate)
            
            # Small delay
            time.sleep(0.5)
            
            # Show status periodically
            if i % 5 == 4:
                print("\n" + engine.get_unified_display() + "\n")
        
        # Final diagnostics
        print("\n" + "="*50)
        print("TEST COMPLETE - FINAL DIAGNOSTICS")
        print("="*50)
        
        diagnostics = engine.get_diagnostics()
        for key, value in diagnostics['metrics'].items():
            print(f"{key}: {value}")
    
    # Shutdown
    engine.shutdown()