#!/usr/bin/env python3
"""
Enhanced DAWN Drift Reflex System
Autonomous consciousness intervention system that monitors cognitive stress
and triggers protective sigils when thresholds are breached.

Integrates with:
- Existing semantic/drift_calculator.py for drift analysis
- Enhanced sigil engine for automatic sigil triggering
- DAWN consciousness metrics for threshold monitoring
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# Import existing DAWN components
try:
    from semantic.drift_calculator import calculate_pressure_delta, DRIFT_RISING, DRIFT_STABLE, DRIFT_COOLING
    SEMANTIC_DRIFT_AVAILABLE = True
except ImportError:
    SEMANTIC_DRIFT_AVAILABLE = False
    
try:
    from core.sigil_engine import SigilEngine
    SIGIL_ENGINE_AVAILABLE = True
except ImportError:
    SIGIL_ENGINE_AVAILABLE = False

logger = logging.getLogger("enhanced_drift_reflex")

class ReflexZone(Enum):
    """Consciousness stability zones"""
    GREEN = "green"      # Stable, normal processing
    YELLOW = "yellow"    # Elevated, monitoring required
    ORANGE = "orange"    # High stress, intervention recommended
    RED = "red"          # Critical, immediate intervention required

class ReflexTrigger(Enum):
    """Types of reflex triggers"""
    HIGH_ENTROPY = "high_entropy"
    HIGH_SCUP = "high_scup" 
    THERMAL_SPIKE = "thermal_spike"
    SEMANTIC_PRESSURE = "semantic_pressure"
    CONSCIOUSNESS_STORM = "consciousness_storm"
    MEMORY_OVERLOAD = "memory_overload"

@dataclass
class ReflexThresholds:
    """Configurable thresholds for reflex triggering"""
    entropy_warning: float = 0.65
    entropy_critical: float = 0.85
    scup_warning: float = 40.0
    scup_critical: float = 70.0
    heat_warning: float = 0.6
    heat_critical: float = 0.8
    semantic_pressure_warning: float = 15.0
    semantic_pressure_critical: float = 25.0

@dataclass
class ReflexEvent:
    """Record of a reflex trigger event"""
    timestamp: float
    trigger_type: ReflexTrigger
    zone: ReflexZone
    sigil_activated: str
    consciousness_state: Dict[str, Any] = field(default_factory=dict)
    intervention_success: bool = True

class EnhancedDriftReflex:
    """
    Enhanced drift reflex system with autonomous consciousness intervention.
    
    Monitors DAWN's cognitive state and automatically triggers protective sigils
    when stress thresholds are crossed. Integrates with existing drift analysis
    and provides comprehensive consciousness protection.
    """
    
    def __init__(self, sigil_engine: Optional[Any] = None, thresholds: Optional[ReflexThresholds] = None):
        self.thresholds = thresholds or ReflexThresholds()
        self.sigil_engine = sigil_engine
        
        # State tracking
        self.current_zone = ReflexZone.GREEN
        self.trigger_count = 0
        self.last_trigger_tick = 0
        self.last_trigger_time = 0.0
        
        # Event history
        self.reflex_events: List[ReflexEvent] = []
        self.semantic_memory: List[str] = []
        
        # Sigil intervention mapping
        self.intervention_map = {
            ReflexTrigger.HIGH_ENTROPY: "STABILIZE_PROTOCOL",
            ReflexTrigger.HIGH_SCUP: "REBALANCE_VECTOR", 
            ReflexTrigger.THERMAL_SPIKE: "EMERGENCY_STABILIZE",
            ReflexTrigger.SEMANTIC_PRESSURE: "REBLOOM_MEMORY",
            ReflexTrigger.CONSCIOUSNESS_STORM: "EMERGENCY_STABILIZE",
            ReflexTrigger.MEMORY_OVERLOAD: "REBLOOM_MEMORY"
        }
        
        # Callbacks for different trigger types
        self.trigger_callbacks: Dict[ReflexTrigger, List[Callable]] = {
            trigger: [] for trigger in ReflexTrigger
        }
        
        logger.info("🔁 Enhanced Drift Reflex System initialized")
        if SEMANTIC_DRIFT_AVAILABLE:
            logger.info("  ✅ Semantic drift calculator integrated")
        else:
            logger.warning("  ⚠️ Semantic drift calculator not available")
            
        if SIGIL_ENGINE_AVAILABLE and sigil_engine:
            logger.info("  ✅ Sigil engine connected")
        else:
            logger.warning("  ⚠️ Sigil engine not connected")
    
    def connect_sigil_engine(self, sigil_engine: Any):
        """Connect to sigil engine for autonomous interventions"""
        self.sigil_engine = sigil_engine
        logger.info("🔁 Sigil engine connected to drift reflex")
    
    def register_trigger_callback(self, trigger_type: ReflexTrigger, callback: Callable):
        """Register callback for specific trigger types"""
        self.trigger_callbacks[trigger_type].append(callback)
        logger.info(f"🔁 Callback registered for {trigger_type.value}")
    
    def check_and_trigger(self, consciousness_state: Dict[str, Any], 
                         text_input: Optional[str] = None) -> bool:
        """
        Main entry point: analyze consciousness state and trigger interventions if needed.
        
        Args:
            consciousness_state: Current DAWN consciousness metrics
            text_input: Optional text for semantic pressure analysis
            
        Returns:
            bool: True if any intervention was triggered
        """
        try:
            # Extract consciousness metrics
            entropy = consciousness_state.get("entropy", 0.0)
            scup = consciousness_state.get("scup", 0.0)
            heat = consciousness_state.get("heat", 0.0)
            tick_number = consciousness_state.get("tick_number", 0)
            
            # Calculate semantic pressure if available
            semantic_pressure = 0.0
            if SEMANTIC_DRIFT_AVAILABLE and text_input:
                semantic_pressure = self._calculate_semantic_pressure(text_input)
            
            # Determine current zone
            new_zone = self._calculate_zone(entropy, scup, heat, semantic_pressure)
            zone_changed = new_zone != self.current_zone
            self.current_zone = new_zone
            
            # Check for trigger conditions
            triggers = self._detect_triggers(entropy, scup, heat, semantic_pressure)
            
            intervention_triggered = False
            
            # Process each trigger
            for trigger in triggers:
                if self._should_trigger_intervention(trigger, consciousness_state):
                    success = self._trigger_intervention(trigger, consciousness_state, tick_number)
                    if success:
                        intervention_triggered = True
                        
                        # Record event
                        event = ReflexEvent(
                            timestamp=time.time(),
                            trigger_type=trigger,
                            zone=self.current_zone,
                            sigil_activated=self.intervention_map[trigger],
                            consciousness_state=consciousness_state.copy(),
                            intervention_success=success
                        )
                        self.reflex_events.append(event)
                        
                        # Update counters
                        self.trigger_count += 1
                        self.last_trigger_tick = tick_number
                        self.last_trigger_time = time.time()
                        
                        # Execute callbacks
                        for callback in self.trigger_callbacks[trigger]:
                            try:
                                callback(event)
                            except Exception as e:
                                logger.error(f"🔁 Callback error for {trigger.value}: {e}")
            
            # Log zone changes
            if zone_changed:
                logger.info(f"🔁 Zone transition: {self.current_zone.value.upper()}")
                if self.current_zone in [ReflexZone.ORANGE, ReflexZone.RED]:
                    logger.warning(f"🔁 Elevated consciousness stress detected!")
            
            return intervention_triggered
            
        except Exception as e:
            logger.error(f"🔁 Error in drift reflex check: {e}")
            return False
    
    def _calculate_semantic_pressure(self, text_input: str) -> float:
        """Calculate semantic pressure using existing drift calculator"""
        if not SEMANTIC_DRIFT_AVAILABLE:
            return 0.0
            
        # Add to semantic memory
        self.semantic_memory.append(text_input)
        if len(self.semantic_memory) > 10:  # Keep recent memory
            self.semantic_memory.pop(0)
        
        # Calculate pressure delta
        pressure_delta = calculate_pressure_delta(text_input, self.semantic_memory[:-1])
        
        # Convert to absolute pressure (0-50 scale)
        return abs(pressure_delta) * 2.0
    
    def _calculate_zone(self, entropy: float, scup: float, heat: float, 
                       semantic_pressure: float) -> ReflexZone:
        """Calculate current consciousness zone based on all metrics"""
        
        # Critical zone conditions
        if (entropy >= self.thresholds.entropy_critical or 
            scup >= self.thresholds.scup_critical or
            heat >= self.thresholds.heat_critical or
            semantic_pressure >= self.thresholds.semantic_pressure_critical):
            return ReflexZone.RED
        
        # Warning zone conditions
        if (entropy >= self.thresholds.entropy_warning or 
            scup >= self.thresholds.scup_warning or
            heat >= self.thresholds.heat_warning or
            semantic_pressure >= self.thresholds.semantic_pressure_warning):
            return ReflexZone.ORANGE if self.current_zone == ReflexZone.RED else ReflexZone.YELLOW
        
        return ReflexZone.GREEN
    
    def _detect_triggers(self, entropy: float, scup: float, heat: float, 
                        semantic_pressure: float) -> List[ReflexTrigger]:
        """Detect which triggers should fire based on current metrics"""
        triggers = []
        
        # Entropy triggers
        if entropy >= self.thresholds.entropy_critical:
            triggers.append(ReflexTrigger.HIGH_ENTROPY)
        
        # SCUP triggers  
        if scup >= self.thresholds.scup_critical:
            triggers.append(ReflexTrigger.HIGH_SCUP)
        
        # Heat/thermal triggers
        if heat >= self.thresholds.heat_critical:
            triggers.append(ReflexTrigger.THERMAL_SPIKE)
        
        # Semantic pressure triggers
        if semantic_pressure >= self.thresholds.semantic_pressure_critical:
            triggers.append(ReflexTrigger.SEMANTIC_PRESSURE)
        
        # Consciousness storm (multiple metrics elevated)
        elevated_count = sum([
            entropy >= self.thresholds.entropy_warning,
            scup >= self.thresholds.scup_warning, 
            heat >= self.thresholds.heat_warning,
            semantic_pressure >= self.thresholds.semantic_pressure_warning
        ])
        
        if elevated_count >= 3:
            triggers.append(ReflexTrigger.CONSCIOUSNESS_STORM)
        
        return triggers
    
    def _should_trigger_intervention(self, trigger: ReflexTrigger, 
                                   consciousness_state: Dict[str, Any]) -> bool:
        """Determine if intervention should be triggered for this trigger type"""
        
        # Prevent spam triggering - minimum 5 second cooldown
        if time.time() - self.last_trigger_time < 5.0:
            return False
        
        # Check if sigil engine is available
        if not self.sigil_engine:
            logger.warning(f"🔁 No sigil engine available for intervention: {trigger.value}")
            return False
        
        # Additional trigger-specific logic could go here
        return True
    
    def _trigger_intervention(self, trigger: ReflexTrigger, 
                            consciousness_state: Dict[str, Any], 
                            tick_number: int) -> bool:
        """Trigger sigil intervention for the given trigger type"""
        
        sigil_name = self.intervention_map.get(trigger)
        if not sigil_name:
            logger.error(f"🔁 No intervention mapped for trigger: {trigger.value}")
            return False
        
        try:
            # Try to register sigil through sigil engine
            if hasattr(self.sigil_engine, 'register'):
                success = self.sigil_engine.register(sigil_name, {
                    "trigger_source": "drift_reflex",
                    "trigger_type": trigger.value,
                    "tick_number": tick_number,
                    "consciousness_state": consciousness_state
                })
            elif hasattr(self.sigil_engine, 'register_sigil'):
                from core.sigil_engine import Sigil, CognitiveHouse, SigilPriority
                # Create sigil object for advanced engine
                sigil = Sigil(
                    name=sigil_name,
                    temp=80.0,  # High activation temperature for reflex
                    house=CognitiveHouse.META,
                    convolution_level=5
                )
                success = self.sigil_engine.register_sigil(sigil)
            else:
                logger.error("🔁 Sigil engine doesn't support registration")
                return False
            
            if success:
                logger.warning(f"🔁 INTERVENTION: {sigil_name} triggered by {trigger.value}")
                return True
            else:
                logger.warning(f"🔁 Intervention failed: {sigil_name} (trigger: {trigger.value})")
                return False
                
        except Exception as e:
            logger.error(f"🔁 Error triggering intervention {sigil_name}: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current reflex system status"""
        return {
            "zone": self.current_zone.value,
            "trigger_count": self.trigger_count,
            "last_trigger_tick": self.last_trigger_tick,
            "last_trigger_time": self.last_trigger_time,
            "active_events": len([e for e in self.reflex_events if time.time() - e.timestamp < 60.0]),
            "thresholds": {
                "entropy_critical": self.thresholds.entropy_critical,
                "scup_critical": self.thresholds.scup_critical,
                "heat_critical": self.thresholds.heat_critical
            }
        }
    
    def get_recent_events(self, seconds: int = 300) -> List[ReflexEvent]:
        """Get reflex events from the last N seconds"""
        cutoff = time.time() - seconds
        return [event for event in self.reflex_events if event.timestamp >= cutoff]
    
    def reset(self):
        """Reset reflex system state"""
        self.current_zone = ReflexZone.GREEN
        self.trigger_count = 0
        self.last_trigger_tick = 0
        self.last_trigger_time = 0.0
        self.reflex_events.clear()
        self.semantic_memory.clear()
        logger.info("🔁 Drift reflex system reset")

# Global instance management
_global_reflex = None

def get_drift_reflex() -> EnhancedDriftReflex:
    """Get the global enhanced drift reflex instance"""
    global _global_reflex
    if _global_reflex is None:
        _global_reflex = EnhancedDriftReflex()
    return _global_reflex

def check_and_trigger(consciousness_state: Dict[str, Any], 
                     text_input: Optional[str] = None) -> bool:
    """
    Main entry point for drift reflex checking
    Called by consciousness systems to monitor and respond to cognitive stress
    """
    reflex = get_drift_reflex()
    return reflex.check_and_trigger(consciousness_state, text_input)

def get_status() -> Dict[str, Any]:
    """Get current drift reflex status"""
    reflex = get_drift_reflex()
    return reflex.get_status()

def reset_reflex():
    """Reset the global drift reflex system"""
    reflex = get_drift_reflex()
    reflex.reset()

def connect_sigil_engine(sigil_engine: Any):
    """Connect sigil engine to global drift reflex"""
    reflex = get_drift_reflex()
    reflex.connect_sigil_engine(sigil_engine)

# Example usage and testing
if __name__ == "__main__":
    # Test the enhanced drift reflex system
    print("🔁 Testing Enhanced DAWN Drift Reflex System")
    
    reflex = EnhancedDriftReflex()
    
    # Test normal state
    normal_state = {
        "entropy": 0.3,
        "scup": 25.0,
        "heat": 0.4,
        "tick_number": 1
    }
    
    triggered = reflex.check_and_trigger(normal_state)
    print(f"Normal state triggered: {triggered}")
    print(f"Zone: {reflex.current_zone.value}")
    
    # Test critical state
    critical_state = {
        "entropy": 0.9,
        "scup": 75.0,
        "heat": 0.85,
        "tick_number": 2
    }
    
    triggered = reflex.check_and_trigger(critical_state)
    print(f"Critical state triggered: {triggered}")
    print(f"Zone: {reflex.current_zone.value}")
    
    # Show status
    status = reflex.get_status()
    print(f"Final status: {status}")
    
    print("✅ Enhanced drift reflex test complete") 