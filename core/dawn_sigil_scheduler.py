#!/usr/bin/env python3
"""
DAWN Sigil Scheduler - Conditional Auto-Sigil Trigger
Automatically deploys stabilization protocols when entropy exceeds thresholds.
Integrated with DAWN Enhanced Entropy Analyzer for autonomous reactivity.
"""

import time
import logging
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque

# DAWN Core Integration
try:
    from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
    ENHANCED_ENTROPY_AVAILABLE = True
except ImportError:
    ENHANCED_ENTROPY_AVAILABLE = False
    EnhancedEntropyAnalyzer = None

try:
    from core.sigil_engine import SigilEngine
    SIGIL_ENGINE_AVAILABLE = True
except ImportError:
    SIGIL_ENGINE_AVAILABLE = False
    SigilEngine = None

try:
    from core.pulse_controller import PulseController
    PULSE_CONTROLLER_AVAILABLE = True
except ImportError:
    PULSE_CONTROLLER_AVAILABLE = False
    PulseController = None

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class TriggerEvent:
    """Record of a sigil trigger event"""
    timestamp: datetime
    entropy_level: float
    threshold: float
    sigil_triggered: str
    active_sigils_before: int
    thermal_context: Optional[Dict] = None
    trigger_reason: str = "entropy_threshold"


@dataclass
class CustomTrigger:
    """Custom trigger configuration"""
    name: str
    entropy_threshold: float
    sigil_name: str
    condition_func: Optional[Callable] = None
    enabled: bool = True
    trigger_count: int = 0
    last_triggered: Optional[datetime] = None


class DAWNSigilScheduler:
    """
    DAWN Sigil Scheduler - Conditional Auto-Sigil Trigger
    
    Automatically deploys stabilization protocols when entropy exceeds thresholds.
    Integrated with Enhanced Entropy Analyzer and existing DAWN components.
    """
    
    def __init__(self, 
                 entropy_analyzer: Optional[EnhancedEntropyAnalyzer] = None,
                 sigil_engine: Optional[SigilEngine] = None,
                 pulse_controller: Optional[PulseController] = None,
                 entropy_threshold: float = 0.6,
                 stabilize_sigil: str = "STABILIZE_PROTOCOL"):
        """
        Initialize the DAWN Sigil Scheduler.
        
        Args:
            entropy_analyzer: Enhanced entropy analyzer instance
            sigil_engine: DAWN sigil engine instance
            pulse_controller: DAWN pulse controller instance
            entropy_threshold: Default entropy threshold for auto-triggers
            stabilize_sigil: Default stabilization sigil to execute
        """
        # Core configuration
        self.entropy_threshold = entropy_threshold
        self.stabilize_sigil = stabilize_sigil
        
        # DAWN Integration
        self.entropy_analyzer = entropy_analyzer
        self.sigil_engine = sigil_engine
        self.pulse_controller = pulse_controller
        
        # State tracking
        self.last_trigger_tick = 0
        self.total_triggers = 0
        self.debug_mode = False
        
        # Advanced features
        self.custom_triggers: Dict[str, CustomTrigger] = {}
        self.trigger_history: deque = deque(maxlen=100)
        self.trigger_cooldown = 5.0  # Minimum seconds between triggers
        
        # Performance metrics
        self.successful_triggers = 0
        self.failed_triggers = 0
        self.entropy_readings = 0
        self.threshold_breaches = 0
        
        # Initialize entropy monitoring if analyzer available
        self.current_entropy = 0.5
        self.entropy_source = "scheduler_internal"
        
        logger.info("🔥 DAWN Sigil Scheduler initialized")
        
        # Register default stabilization triggers
        self._register_default_triggers()
    
    def _register_default_triggers(self):
        """Register default stabilization triggers"""
        # High entropy stabilization
        self.register_custom_trigger(
            name="high_entropy_stabilize",
            entropy_threshold=self.entropy_threshold,
            sigil_name=self.stabilize_sigil,
            condition_func=self._check_no_active_sigils
        )
        
        # Critical entropy emergency protocol
        self.register_custom_trigger(
            name="critical_entropy_emergency",
            entropy_threshold=0.85,
            sigil_name="EMERGENCY_STABILIZE",
            condition_func=self._check_critical_conditions
        )
        
        # Thermal correlation stabilization
        if self.pulse_controller:
            self.register_custom_trigger(
                name="thermal_entropy_correlation",
                entropy_threshold=0.7,
                sigil_name="THERMAL_STABILIZE",
                condition_func=self._check_thermal_surge_correlation
            )
    
    def check_and_trigger(self, external_entropy: Optional[float] = None) -> Dict[str, Any]:
        """
        Main scheduler function - runs on every system tick.
        Checks entropy levels and automatically triggers stabilization sigils.
        
        Args:
            external_entropy: Optional external entropy reading
            
        Returns:
            dict: Trigger status and system state information
        """
        # Get current entropy from various sources
        current_entropy = self._get_current_entropy(external_entropy)
        active_sigils = self._get_active_sigil_count()
        
        self.entropy_readings += 1
        
        # Build result structure
        result = {
            'tick_executed': True,
            'entropy_level': current_entropy,
            'active_sigils': active_sigils,
            'threshold_exceeded': current_entropy > self.entropy_threshold,
            'sigils_triggered': [],
            'total_triggers': self.total_triggers,
            'scheduler_status': 'active'
        }
        
        # Check if entropy exceeds threshold
        if current_entropy > self.entropy_threshold:
            self.threshold_breaches += 1
            
            # Check all custom triggers
            triggered_sigils = self._check_all_triggers(current_entropy, active_sigils)
            result['sigils_triggered'] = triggered_sigils
            
            if triggered_sigils:
                result['scheduler_status'] = 'triggered'
                self.total_triggers += len(triggered_sigils)
                self.last_trigger_tick = self._get_current_tick()
        
        # Debug output
        if self.debug_mode:
            self._debug_output(current_entropy, active_sigils, result)
        
        return result
    
    def _get_current_entropy(self, external_entropy: Optional[float] = None) -> float:
        """Get current entropy from available sources"""
        if external_entropy is not None:
            self.current_entropy = external_entropy
            self.entropy_source = "external"
            return external_entropy
        
        # Try to get from enhanced entropy analyzer
        if self.entropy_analyzer and hasattr(self.entropy_analyzer, 'entropy_history'):
            if self.entropy_analyzer.entropy_history:
                self.current_entropy = self.entropy_analyzer.entropy_history[-1]
                self.entropy_source = "enhanced_analyzer"
                return self.current_entropy
        
        # Try to get from sigil engine entropy tracking
        if self.sigil_engine and hasattr(self.sigil_engine, 'get_system_entropy'):
            try:
                self.current_entropy = self.sigil_engine.get_system_entropy()
                self.entropy_source = "sigil_engine"
                return self.current_entropy
            except Exception:
                pass
        
        # Fallback: use internal tracking
        self.entropy_source = "internal_fallback"
        return self.current_entropy
    
    def _get_active_sigil_count(self) -> int:
        """Get count of active sigils"""
        if self.sigil_engine and hasattr(self.sigil_engine, 'active_sigils'):
            return len(self.sigil_engine.active_sigils)
        return 0
    
    def _check_all_triggers(self, entropy: float, active_sigils: int) -> List[str]:
        """Check all registered triggers and execute qualifying ones"""
        triggered_sigils = []
        current_time = datetime.now()
        
        for trigger_name, trigger in self.custom_triggers.items():
            if not trigger.enabled:
                continue
            
            # Check cooldown
            if (trigger.last_triggered and 
                (current_time - trigger.last_triggered).total_seconds() < self.trigger_cooldown):
                continue
            
            # Check entropy threshold
            if entropy <= trigger.entropy_threshold:
                continue
            
            # Check custom condition if provided
            if trigger.condition_func and not trigger.condition_func(entropy, active_sigils):
                continue
            
            # Execute trigger
            if self._execute_sigil_trigger(trigger.sigil_name, entropy, trigger_name):
                triggered_sigils.append(trigger.sigil_name)
                trigger.trigger_count += 1
                trigger.last_triggered = current_time
                
                # Record trigger event
                self._record_trigger_event(entropy, trigger, active_sigils)
        
        return triggered_sigils
    
    def _execute_sigil_trigger(self, sigil_name: str, entropy: float, trigger_name: str) -> bool:
        """Execute a sigil trigger"""
        try:
            if self.sigil_engine and SIGIL_ENGINE_AVAILABLE:
                # Use actual sigil engine
                success = self._execute_with_sigil_engine(sigil_name)
                if success:
                    self.successful_triggers += 1
                    if self.debug_mode:
                        print(f"🔥 DAWN: Auto-triggered {sigil_name} | Entropy: {entropy:.3f} | Trigger: {trigger_name}")
                else:
                    self.failed_triggers += 1
                return success
            else:
                # Simulation mode
                self.successful_triggers += 1
                if self.debug_mode:
                    print(f"🔥 DAWN: [SIM] Auto-triggered {sigil_name} | Entropy: {entropy:.3f} | Trigger: {trigger_name}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to execute sigil trigger {sigil_name}: {e}")
            self.failed_triggers += 1
            return False
    
    def _execute_with_sigil_engine(self, sigil_name: str) -> bool:
        """Execute sigil using the DAWN sigil engine"""
        try:
            # Register sigil with engine
            self.sigil_engine.register_sigil(sigil_name)
            
            # Execute next sigil in queue
            result = self.sigil_engine.execute_next_sigil()
            
            return result is not None and getattr(result, 'success', True)
        except Exception as e:
            logger.error(f"Sigil engine execution failed: {e}")
            return False
    
    def _record_trigger_event(self, entropy: float, trigger: CustomTrigger, active_sigils: int):
        """Record a trigger event for history tracking"""
        thermal_context = None
        if self.pulse_controller:
            try:
                thermal_stats = self.pulse_controller.get_heat_statistics()
                thermal_context = {
                    'heat': thermal_stats['current_heat'],
                    'zone': thermal_stats['current_zone']
                }
            except Exception:
                pass
        
        event = TriggerEvent(
            timestamp=datetime.now(),
            entropy_level=entropy,
            threshold=trigger.entropy_threshold,
            sigil_triggered=trigger.sigil_name,
            active_sigils_before=active_sigils,
            thermal_context=thermal_context,
            trigger_reason=trigger.name
        )
        
        self.trigger_history.append(event)
    
    # Condition functions for default triggers
    def _check_no_active_sigils(self, entropy: float, active_sigils: int) -> bool:
        """Check if no sigils are currently active"""
        return active_sigils == 0
    
    def _check_critical_conditions(self, entropy: float, active_sigils: int) -> bool:
        """Check for critical system conditions"""
        # Critical if very high entropy regardless of active sigils
        return entropy > 0.85
    
    def _check_thermal_surge_correlation(self, entropy: float, active_sigils: int) -> bool:
        """Check for thermal surge correlation with entropy"""
        if not self.pulse_controller:
            return False
        
        try:
            thermal_stats = self.pulse_controller.get_heat_statistics()
            return (thermal_stats['current_zone'] == 'SURGE' and 
                   thermal_stats['current_heat'] > 75.0)
        except Exception:
            return False
    
    def _debug_output(self, entropy: float, active_sigils: int, result: Dict):
        """Output debug information"""
        if entropy > self.entropy_threshold:
            if active_sigils > 0 and not result['sigils_triggered']:
                print(f"⏳ DAWN: High entropy ({entropy:.3f}) but {active_sigils} sigils active")
            elif result['sigils_triggered']:
                print(f"🚀 DAWN: Triggered {len(result['sigils_triggered'])} sigils for entropy {entropy:.3f}")
    
    def _get_current_tick(self) -> int:
        """Get current system tick"""
        return int(time.time() * 1000)
    
    # Public configuration methods
    def set_entropy_threshold(self, new_threshold: float):
        """Dynamically adjust entropy threshold for stabilization triggers."""
        self.entropy_threshold = new_threshold
        
        # Update default trigger
        if "high_entropy_stabilize" in self.custom_triggers:
            self.custom_triggers["high_entropy_stabilize"].entropy_threshold = new_threshold
        
        print(f"🎛️ DAWN: Entropy threshold updated to {new_threshold}")
        logger.info(f"Entropy threshold updated to {new_threshold}")
    
    def enable_debug_mode(self, enabled: bool = True):
        """Enable/disable debug output for scheduler monitoring."""
        self.debug_mode = enabled
        status = "enabled" if enabled else "disabled"
        print(f"🔍 DAWN: Sigil scheduler debug mode {status}")
        logger.info(f"Debug mode {status}")
    
    def register_custom_trigger(self, name: str, entropy_threshold: float, 
                              sigil_name: str, condition_func: Optional[Callable] = None):
        """
        Register custom trigger conditions.
        
        Args:
            name: Unique name for the trigger
            entropy_threshold: Entropy level to trigger at
            sigil_name: Name of sigil to execute
            condition_func: Optional additional condition function
        """
        trigger = CustomTrigger(
            name=name,
            entropy_threshold=entropy_threshold,
            sigil_name=sigil_name,
            condition_func=condition_func
        )
        
        self.custom_triggers[name] = trigger
        print(f"📋 DAWN: Custom trigger registered - {sigil_name} at entropy {entropy_threshold}")
        logger.info(f"Custom trigger registered: {name} -> {sigil_name} @ {entropy_threshold}")
    
    def get_scheduler_stats(self) -> Dict[str, Any]:
        """Get comprehensive scheduler statistics for system monitoring."""
        return {
            'entropy_threshold': self.entropy_threshold,
            'total_triggers': self.total_triggers,
            'successful_triggers': self.successful_triggers,
            'failed_triggers': self.failed_triggers,
            'last_trigger_tick': self.last_trigger_tick,
            'debug_mode': self.debug_mode,
            'stabilize_sigil': self.stabilize_sigil,
            'current_entropy': self.current_entropy,
            'entropy_source': self.entropy_source,
            'active_sigils': self._get_active_sigil_count(),
            'entropy_readings': self.entropy_readings,
            'threshold_breaches': self.threshold_breaches,
            'custom_triggers_count': len(self.custom_triggers),
            'enabled_triggers': sum(1 for t in self.custom_triggers.values() if t.enabled),
            'recent_triggers': len(self.trigger_history)
        }
    
    def get_trigger_history(self, limit: int = 10) -> List[Dict]:
        """Get recent trigger history"""
        recent_events = list(self.trigger_history)[-limit:]
        return [
            {
                'timestamp': event.timestamp.isoformat(),
                'entropy_level': event.entropy_level,
                'threshold': event.threshold,
                'sigil_triggered': event.sigil_triggered,
                'active_sigils_before': event.active_sigils_before,
                'thermal_context': event.thermal_context,
                'trigger_reason': event.trigger_reason
            }
            for event in recent_events
        ]
    
    def reset_scheduler(self):
        """Reset scheduler state - useful for system restarts."""
        self.last_trigger_tick = 0
        self.total_triggers = 0
        self.successful_triggers = 0
        self.failed_triggers = 0
        self.entropy_readings = 0
        self.threshold_breaches = 0
        self.trigger_history.clear()
        
        # Reset custom trigger states
        for trigger in self.custom_triggers.values():
            trigger.trigger_count = 0
            trigger.last_triggered = None
        
        print("🔄 DAWN: Sigil scheduler reset")
        logger.info("Scheduler state reset")
    
    def enable_trigger(self, trigger_name: str, enabled: bool = True):
        """Enable/disable a specific trigger"""
        if trigger_name in self.custom_triggers:
            self.custom_triggers[trigger_name].enabled = enabled
            status = "enabled" if enabled else "disabled"
            print(f"🔧 DAWN: Trigger '{trigger_name}' {status}")
        else:
            print(f"⚠️ DAWN: Unknown trigger '{trigger_name}'")
    
    def test_scheduler(self, test_entropy: float = 0.7) -> Dict[str, Any]:
        """Test the scheduler with simulated conditions."""
        print("🧪 Testing DAWN Sigil Scheduler...")
        
        # Enable debug for testing
        original_debug = self.debug_mode
        self.enable_debug_mode(True)
        
        print(f"Test entropy: {test_entropy}")
        print(f"Current entropy: {self.current_entropy}")
        print(f"Active sigils: {self._get_active_sigil_count()}")
        
        # Run scheduler check
        result = self.check_and_trigger(test_entropy)
        print(f"Scheduler result: {result}")
        
        # Restore debug mode
        self.enable_debug_mode(original_debug)
        
        return result


# Integration interface for DAWN system
def create_dawn_sigil_scheduler(entropy_analyzer: Optional[EnhancedEntropyAnalyzer] = None,
                               sigil_engine: Optional[SigilEngine] = None,
                               pulse_controller: Optional[PulseController] = None) -> DAWNSigilScheduler:
    """Factory function for DAWN integration."""
    return DAWNSigilScheduler(
        entropy_analyzer=entropy_analyzer,
        sigil_engine=sigil_engine,
        pulse_controller=pulse_controller
    )


# Backward compatibility with original interface
class SigilScheduler(DAWNSigilScheduler):
    """Backward compatibility wrapper for the original interface"""
    
    def __init__(self):
        super().__init__()
        print("🔥 DAWN: Using enhanced sigil scheduler with backward compatibility")


# Example usage for testing
if __name__ == "__main__":
    print("🚀 DAWN Sigil Scheduler - Direct Execution Mode")
    
    # Create scheduler
    scheduler = DAWNSigilScheduler()
    
    # Run test
    scheduler.test_scheduler()
    
    # Show statistics
    stats = scheduler.get_scheduler_stats()
    print("\n📊 Scheduler Statistics:")
    for key, value in stats.items():
        print(f"  {key.replace('_', ' ').title()}: {value}") 