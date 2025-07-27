"""
Helix Bridge - Threading Module for DAWN System Components
=========================================================
Manages communication and coordination between helix components
Integrates with DAWN's live tick, bloom, and pulse cycles
"""

import logging
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import time
import json
from pathlib import Path
import asyncio
from datetime import datetime
from collections import deque

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('helix_bridge')

class ComponentStatus(Enum):
    """Status of helix components"""
    UNKNOWN = "unknown"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    ERROR = "error"
    STUB = "stub"
    DEPRECATED = "deprecated"
    DORMANT = "dormant"

class CyclePhase(Enum):
    """Phase of DAWN's operational cycles"""
    TICK = "tick"
    BLOOM = "bloom"
    PULSE = "pulse"
    COOLDOWN = "cooldown"
    EMERGENCY = "emergency"

@dataclass
class ComponentInfo:
    """Information about a helix component"""
    name: str
    version: str
    status: ComponentStatus
    dependencies: List[str]
    last_health_check: float
    health_status: bool
    error_message: Optional[str] = None
    last_activity: float = 0.0
    entropy_drift: float = 0.0
    cycle_phase: CyclePhase = CyclePhase.COOLDOWN
    cycle_count: int = 0

class HelixBridge:
    """Bridge for coordinating helix components"""
    
    def __init__(self):
        self.components: Dict[str, ComponentInfo] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
        self._last_signal_time = time.time()
        self._signal_history = []
        self._helix_thread: Optional[threading.Thread] = None
        self._stop_helix = threading.Event()
        self._tick_state = 0
        self._last_status_log = 0.0
        self._status_log_interval = 300  # 5 minutes
        
        # Cycle tracking
        self._current_phase = CyclePhase.COOLDOWN
        self._cycle_history = deque(maxlen=1000)
        self._phase_start_time = time.time()
        self._tick_handlers: List[Callable] = []
        self._bloom_handlers: List[Callable] = []
        self._pulse_handlers: List[Callable] = []
        
    def bridge_components(self) -> Dict[str, bool]:
        """Manages handoffs between genome_loader, bloom_engine, pulse_heat"""
        try:
            # Import helix import architecture
            from helix_import_architecture import helix_import
            
            # Key components to bridge
            components_to_check = [
                "genome_loader",
                "bloom_engine",
                "pulse_heat",
                "thermal_linguistic_genome"
            ]
            
            results = {}
            
            for component_name in components_to_check:
                try:
                    module = helix_import(component_name)
                    is_stub = module is None or getattr(module, '__stub__', False)
                    
                    # Check if component is dormant
                    is_dormant = False
                    if hasattr(module, 'get_state'):
                        state = module.get_state()
                        is_dormant = state.get('dormant', False)
                    
                    status = ComponentStatus.DORMANT if is_dormant else (
                        ComponentStatus.STUB if is_stub else ComponentStatus.ACTIVE
                    )
                    
                    self.components[component_name] = ComponentInfo(
                        name=component_name,
                        version=getattr(module, '__version__', 'unknown'),
                        status=status,
                        dependencies=getattr(module, '__dependencies__', []),
                        last_health_check=time.time(),
                        health_status=not (is_stub or is_dormant),
                        last_activity=time.time(),
                        cycle_phase=self._current_phase
                    )
                    
                    # Register cycle handlers
                    if not is_stub and not is_dormant:
                        self._register_cycle_handlers(module, component_name)
                    
                    results[component_name] = not (is_stub or is_dormant)
                    logger.info(f"Component {component_name} status: {status.value}")
                    
                except Exception as e:
                    logger.error(f"Error importing {component_name}: {str(e)}")
                    self.components[component_name] = ComponentInfo(
                        name=component_name,
                        version='unknown',
                        status=ComponentStatus.ERROR,
                        dependencies=[],
                        last_health_check=time.time(),
                        health_status=False,
                        error_message=str(e)
                    )
                    results[component_name] = False
            
            return results
            
        except Exception as e:
            logger.error(f"Error in bridge_components: {str(e)}")
            return {}
    
    def _register_cycle_handlers(self, module: Any, component_name: str):
        """Register cycle handlers for a component"""
        try:
            if hasattr(module, 'on_tick'):
                self._tick_handlers.append(module.on_tick)
            if hasattr(module, 'on_bloom'):
                self._bloom_handlers.append(module.on_bloom)
            if hasattr(module, 'on_pulse'):
                self._pulse_handlers.append(module.on_pulse)
        except Exception as e:
            logger.error(f"Error registering handlers for {component_name}: {str(e)}")
    
    def route_signal(self, event: str) -> bool:
        """Dynamically dispatches Claude events to helix modules"""
        with self._lock:
            current_time = time.time()
            self._signal_history.append({
                'event': event,
                'timestamp': current_time
            })
            
            # Keep only last 100 signals
            if len(self._signal_history) > 100:
                self._signal_history.pop(0)
            
            self._last_signal_time = current_time
            
            try:
                # Handle different event types
                if event == 'evolve_bloom':
                    return self._handle_evolve_bloom()
                elif event == 'halt_sequence':
                    return self._handle_halt_sequence()
                elif event == 'thermal_emergency':
                    return self._handle_thermal_emergency()
                elif event == 'genome_sync':
                    return self._handle_genome_sync()
                elif event == 'claude_adaptation':
                    return self._handle_claude_adaptation()
                else:
                    logger.warning(f"Unknown event type: {event}")
                    return False
                    
            except Exception as e:
                logger.error(f"Error routing signal {event}: {str(e)}")
                return False
    
    def init_helix_thread(self) -> bool:
        """Creates a long-running helix loop that checks tick state or entropy drift"""
        if self._helix_thread and self._helix_thread.is_alive():
            logger.warning("Helix thread already running")
            return False
            
        self._stop_helix.clear()
        self._helix_thread = threading.Thread(
            target=self._helix_loop,
            name="HelixMonitor",
            daemon=True
        )
        self._helix_thread.start()
        logger.info("Helix monitoring thread started")
        return True
    
    def _helix_loop(self):
        """Main helix monitoring loop"""
        while not self._stop_helix.is_set():
            try:
                # Check tick state
                self._check_tick_state()
                
                # Check entropy drift
                self._check_entropy_drift()
                
                # Process current cycle phase
                self._process_cycle_phase()
                
                # Log status periodically
                self.log_bridge_status()
                
                # Sleep briefly
                time.sleep(1.0)
                
            except Exception as e:
                logger.error(f"Error in helix loop: {str(e)}")
                time.sleep(5.0)  # Longer sleep on error
    
    def _check_tick_state(self):
        """Check and update tick state"""
        try:
            from core.tick_emitter import current_tick
            new_tick = current_tick()
            if new_tick != self._tick_state:
                self._tick_state = new_tick
                logger.debug(f"Tick state updated: {new_tick}")
        except Exception as e:
            logger.error(f"Error checking tick state: {str(e)}")
    
    def _check_entropy_drift(self):
        """Check entropy drift in components"""
        try:
            from owl.entropy_tracker import get_entropy_score
            for component_name, info in self.components.items():
                if info.status == ComponentStatus.ACTIVE:
                    drift = get_entropy_score(component_name)
                    info.entropy_drift = drift
                    if drift > 0.8:  # High drift threshold
                        logger.warning(f"High entropy drift in {component_name}: {drift}")
        except Exception as e:
            logger.error(f"Error checking entropy drift: {str(e)}")
    
    def log_bridge_status(self):
        """Periodically logs what helix components are active, stubbed, or dormant"""
        current_time = time.time()
        if current_time - self._last_status_log < self._status_log_interval:
            return
            
        self._last_status_log = current_time
        
        status_summary = {
            'active': [],
            'stub': [],
            'dormant': [],
            'error': []
        }
        
        for name, info in self.components.items():
            if info.status == ComponentStatus.ACTIVE:
                status_summary['active'].append(name)
            elif info.status == ComponentStatus.STUB:
                status_summary['stub'].append(name)
            elif info.status == ComponentStatus.DORMANT:
                status_summary['dormant'].append(name)
            elif info.status == ComponentStatus.ERROR:
                status_summary['error'].append(name)
        
        logger.info("Helix Bridge Status:")
        logger.info(f"Active components: {', '.join(status_summary['active']) or 'none'}")
        logger.info(f"Stub components: {', '.join(status_summary['stub']) or 'none'}")
        logger.info(f"Dormant components: {', '.join(status_summary['dormant']) or 'none'}")
        logger.info(f"Error components: {', '.join(status_summary['error']) or 'none'}")
        
        # Log to file
        try:
            log_dir = Path("logs/helix")
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / f"helix_status_{datetime.now().strftime('%Y%m%d')}.log"
            
            with open(log_file, "a") as f:
                f.write(f"\n=== Helix Status {datetime.now().isoformat()} ===\n")
                f.write(json.dumps(status_summary, indent=2))
                f.write("\n")
        except Exception as e:
            logger.error(f"Error writing status log: {str(e)}")
    
    def _handle_claude_adaptation(self) -> bool:
        """Handle Claude-driven system adaptation"""
        try:
            # Import Claude trigger system
            from claude_trigger import ClaudeTrigger
            trigger = ClaudeTrigger()
            
            # Get current system state
            state = self.get_integration_status()
            
            # Request adaptation
            return trigger.adapt_system(state)
        except Exception as e:
            logger.error(f"Error in Claude adaptation: {str(e)}")
            return False
    
    def _handle_evolve_bloom(self) -> bool:
        """Handle bloom evolution signal"""
        try:
            if 'bloom_engine' in self.components:
                # Import and call bloom evolution
                from helix_import_architecture import helix_import
                bloom_module = helix_import("bloom_engine")
                if bloom_module and hasattr(bloom_module, 'evolve_bloom'):
                    return bloom_module.evolve_bloom()
            return False
        except Exception as e:
            logger.error(f"Error in evolve_bloom: {str(e)}")
            return False
    
    def _handle_halt_sequence(self) -> bool:
        """Handle sequence halt signal"""
        try:
            # Notify all components of halt
            for component_name, info in self.components.items():
                if info.status == ComponentStatus.ACTIVE:
                    logger.info(f"Halting component: {component_name}")
            return True
        except Exception as e:
            logger.error(f"Error in halt_sequence: {str(e)}")
            return False
    
    def _handle_thermal_emergency(self) -> bool:
        """Handle thermal emergency signal"""
        try:
            if 'pulse_heat' in self.components:
                # Import and handle thermal emergency
                from helix_import_architecture import helix_import
                pulse_module = helix_import("pulse_heat")
                if pulse_module and hasattr(pulse_module, 'handle_thermal_emergency'):
                    return pulse_module.handle_thermal_emergency()
            return False
        except Exception as e:
            logger.error(f"Error in thermal_emergency: {str(e)}")
            return False
    
    def _handle_genome_sync(self) -> bool:
        """Handle genome synchronization signal"""
        try:
            if 'genome_loader' in self.components:
                # Import and sync genome
                from helix_import_architecture import helix_import
                genome_module = helix_import("genome_loader")
                if genome_module and hasattr(genome_module, 'sync_genome'):
                    return genome_module.sync_genome()
            return False
        except Exception as e:
            logger.error(f"Error in genome_sync: {str(e)}")
            return False
    
    def _process_cycle_phase(self):
        """Process the current cycle phase"""
        current_time = time.time()
        phase_duration = current_time - self._phase_start_time
        
        try:
            if self._current_phase == CyclePhase.TICK:
                # Process tick phase
                for handler in self._tick_handlers:
                    handler(self._tick_state)
                
                # Check if should transition to bloom
                if phase_duration >= 1.0:  # 1 second per tick
                    self._transition_phase(CyclePhase.BLOOM)
                    
            elif self._current_phase == CyclePhase.BLOOM:
                # Process bloom phase
                for handler in self._bloom_handlers:
                    handler()
                
                # Check if should transition to pulse
                if phase_duration >= 0.5:  # 0.5 seconds per bloom
                    self._transition_phase(CyclePhase.PULSE)
                    
            elif self._current_phase == CyclePhase.PULSE:
                # Process pulse phase
                for handler in self._pulse_handlers:
                    handler()
                
                # Check if should transition to cooldown
                if phase_duration >= 0.2:  # 0.2 seconds per pulse
                    self._transition_phase(CyclePhase.COOLDOWN)
                    
            elif self._current_phase == CyclePhase.COOLDOWN:
                # Process cooldown phase
                if phase_duration >= 0.1:  # 0.1 seconds cooldown
                    self._transition_phase(CyclePhase.TICK)
                    
            elif self._current_phase == CyclePhase.EMERGENCY:
                # Emergency handling
                self._handle_emergency_phase()
                
        except Exception as e:
            logger.error(f"Error processing cycle phase: {str(e)}")
            self._transition_phase(CyclePhase.EMERGENCY)
    
    def _transition_phase(self, new_phase: CyclePhase):
        """Transition to a new cycle phase"""
        old_phase = self._current_phase
        self._current_phase = new_phase
        self._phase_start_time = time.time()
        
        # Record phase transition
        self._cycle_history.append({
            'timestamp': time.time(),
            'from_phase': old_phase.value,
            'to_phase': new_phase.value
        })
        
        # Update component phases
        for component in self.components.values():
            if component.status == ComponentStatus.ACTIVE:
                component.cycle_phase = new_phase
                component.cycle_count += 1
        
        logger.debug(f"Phase transition: {old_phase.value} -> {new_phase.value}")
    
    def _handle_emergency_phase(self):
        """Handle emergency phase"""
        try:
            # Check thermal state
            if 'pulse_heat' in self.components:
                from helix_import_architecture import helix_import
                pulse_module = helix_import("pulse_heat")
                if pulse_module and hasattr(pulse_module, 'get_thermal_state'):
                    thermal_state = pulse_module.get_thermal_state()
                    if thermal_state.get('emergency', False):
                        # Stay in emergency phase
                        return
            
            # If no emergency, transition to cooldown
            self._transition_phase(CyclePhase.COOLDOWN)
            
        except Exception as e:
            logger.error(f"Error in emergency phase: {str(e)}")
    
    def get_cycle_status(self) -> Dict[str, Any]:
        """Get current cycle status"""
        return {
            'current_phase': self._current_phase.value,
            'phase_duration': time.time() - self._phase_start_time,
            'cycle_history': list(self._cycle_history),
            'component_phases': {
                name: info.cycle_phase.value 
                for name, info in self.components.items()
            }
        }
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status"""
        status = {
            'components': {name: info.__dict__ for name, info in self.components.items()},
            'last_signal_time': self._last_signal_time,
            'signal_count': len(self._signal_history),
            'tick_state': self._tick_state
        }
        status.update(self.get_cycle_status())
        return status

# Create global instance
HELIX_BRIDGE = HelixBridge()