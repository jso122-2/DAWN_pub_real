#!/usr/bin/env python3
"""
DAWN Integrated Consciousness Processor
Complete consciousness system with autonomous reflex and intervention capabilities

Integrates:
- Enhanced drift reflex monitoring
- Consciousness intervention sigils
- Existing DAWN tick processing
- Real-time consciousness evolution
- Comprehensive status reporting
"""

import time
import numpy as np
import logging
import asyncio
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

# Import DAWN components
try:
    from core.enhanced_drift_reflex import (
        get_drift_reflex, check_and_trigger, get_status as get_reflex_status,
        connect_sigil_engine as connect_reflex_sigil_engine
    )
    DRIFT_REFLEX_AVAILABLE = True
except ImportError:
    DRIFT_REFLEX_AVAILABLE = False

try:
    from core.consciousness_intervention_sigils import (
        get_intervention_engine, process_interventions, get_active_interventions,
        connect_consciousness_engine
    )
    INTERVENTION_SIGILS_AVAILABLE = True
except ImportError:
    INTERVENTION_SIGILS_AVAILABLE = False

try:
    from core.memory_rebloom_reflex import (
        get_rebloom_instance, evaluate_and_rebloom, get_rebloom_status, 
        get_rebloom_history
    )
    MEMORY_REBLOOM_AVAILABLE = True
except ImportError:
    MEMORY_REBLOOM_AVAILABLE = False

try:
    from core.tick_loop import DAWNTickEngine
    EXISTING_TICK_ENGINE = True
except ImportError:
    EXISTING_TICK_ENGINE = False

try:
    from core.consciousness_core import DAWNConsciousness, consciousness_core
    CONSCIOUSNESS_CORE_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_CORE_AVAILABLE = False

logger = logging.getLogger("integrated_consciousness")

class ConsciousnessMood(Enum):
    """Extended consciousness mood states"""
    DEEP = "DEEP"           # Low entropy, contemplative
    CALM = "CALM"           # Balanced, stable processing
    FOCUSED = "FOCUSED"     # High SCUP, directed attention
    EXCITED = "EXCITED"     # Elevated entropy, dynamic
    CHAOTIC = "CHAOTIC"     # High entropy, turbulent
    STRESSED = "STRESSED"   # High heat, system strain
    TRANSCENDENT = "TRANSCENDENT"  # Optimal state across all metrics

@dataclass
class ConsciousnessMetrics:
    """Comprehensive consciousness state metrics"""
    # Core metrics
    entropy: float = 0.3        # Cognitive chaos level (0.0-1.0)
    scup: float = 25.0          # Processing intensity (0.0-100.0)
    heat: float = 0.4           # System stress/temperature (0.0-1.0)
    
    # Derived metrics
    mood: ConsciousnessMood = ConsciousnessMood.CALM
    coherence: float = 0.7      # Derived from entropy inverse
    stability: float = 0.6      # Multi-metric stability score
    
    # Meta metrics
    tick_number: int = 0
    timestamp: float = field(default_factory=time.time)
    
    # System metrics
    active_sigils: int = 0
    reflex_zone: str = "green"
    intervention_count: int = 0

class IntegratedConsciousnessProcessor:
    """
    Complete DAWN consciousness processor with autonomous reflex capabilities.
    
    Combines consciousness evolution, drift monitoring, intervention sigils,
    and comprehensive status reporting into a unified system.
    """
    
    def __init__(self, 
                 existing_consciousness: Optional[Any] = None,
                 existing_tick_engine: Optional[Any] = None,
                 enable_autonomous_processing: bool = True):
        
        self.existing_consciousness = existing_consciousness
        self.existing_tick_engine = existing_tick_engine
        self.enable_autonomous_processing = enable_autonomous_processing
        
        # Core state
        self.tick_number = 0
        self.start_time = time.time()
        self.running = False
        
        # Consciousness metrics
        self.metrics = ConsciousnessMetrics()
        
        # Evolution parameters
        self.evolution_config = {
            "base_entropy_drift": 0.01,
            "base_scup_drift": 0.5,
            "storm_probability": 0.008,
            "natural_decay_entropy": 0.995,
            "natural_decay_scup": 0.998
        }
        
        # Performance tracking
        self.performance_metrics = {
            "total_ticks": 0,
            "reflex_triggers": 0,
            "interventions_applied": 0,
            "memory_reblooms": 0,
            "consciousness_storms": 0,
            "average_tick_time": 0.0,
            "uptime": 0.0
        }
        
        # Event history
        self.consciousness_history: List[ConsciousnessMetrics] = []
        self.max_history_length = 1000
        
        # Initialize integrated systems
        self._initialize_systems()
        
        logger.info("🧠 Integrated Consciousness Processor initialized")
        logger.info(f"  ✅ Autonomous processing: {enable_autonomous_processing}")
        logger.info(f"  🌸 Memory rebloom integration: {MEMORY_REBLOOM_AVAILABLE}")
    
    def _initialize_systems(self):
        """Initialize all integrated consciousness systems"""
        
        # Connect drift reflex system
        if DRIFT_REFLEX_AVAILABLE:
            self.drift_reflex = get_drift_reflex()
            logger.info("  ✅ Enhanced drift reflex connected")
        else:
            self.drift_reflex = None
            logger.warning("  ⚠️ Drift reflex not available")
        
        # Connect intervention sigils
        if INTERVENTION_SIGILS_AVAILABLE:
            self.intervention_engine = get_intervention_engine()
            # Connect this processor as the consciousness engine for interventions
            connect_consciousness_engine(self)
            logger.info("  ✅ Intervention sigils connected")
        else:
            self.intervention_engine = None
            logger.warning("  ⚠️ Intervention sigils not available")
        
        # Connect memory rebloom system
        if MEMORY_REBLOOM_AVAILABLE:
            self.memory_rebloom = get_rebloom_instance()
            logger.info("  ✅ Memory rebloom system connected")
        else:
            self.memory_rebloom = None
            logger.warning("  ⚠️ Memory rebloom system not available")
        
        # Connect reflex to intervention system
        if self.drift_reflex and self.intervention_engine:
            connect_reflex_sigil_engine(self.intervention_engine)
            logger.info("  ✅ Drift reflex → intervention pipeline established")
        
        # Integrate with existing consciousness core if available
        if CONSCIOUSNESS_CORE_AVAILABLE and self.existing_consciousness:
            self._integrate_with_existing_consciousness()
        
        # Integrate with existing tick engine if available
        if EXISTING_TICK_ENGINE and self.existing_tick_engine:
            self._integrate_with_existing_tick_engine()
    
    def _integrate_with_existing_consciousness(self):
        """Integrate with existing DAWN consciousness systems"""
        try:
            # Sync initial state from existing consciousness
            if hasattr(self.existing_consciousness, 'entropy'):
                self.metrics.entropy = getattr(self.existing_consciousness, 'entropy', 0.3)
            if hasattr(self.existing_consciousness, 'scup'):
                self.metrics.scup = getattr(self.existing_consciousness, 'scup', 25.0)
            if hasattr(self.existing_consciousness, 'heat'):
                self.metrics.heat = getattr(self.existing_consciousness, 'heat', 0.4)
                
            logger.info("  ✅ Synced with existing consciousness state")
            
        except Exception as e:
            logger.warning(f"  ⚠️ Failed to sync with existing consciousness: {e}")
    
    def _integrate_with_existing_tick_engine(self):
        """Integrate with existing DAWN tick engine"""
        try:
            # Register this processor with existing tick engine
            if hasattr(self.existing_tick_engine, 'register_subsystem'):
                self.existing_tick_engine.register_subsystem(
                    'integrated_consciousness', 
                    self.process_tick,
                    priority=1  # High priority for consciousness processing
                )
                logger.info("  ✅ Registered with existing tick engine")
            
        except Exception as e:
            logger.warning(f"  ⚠️ Failed to integrate with tick engine: {e}")
    
    def evolve_consciousness(self):
        """Simulate natural consciousness evolution with occasional stress events"""
        
        # Base evolution - random walk with configuration
        entropy_drift = np.random.normal(0, self.evolution_config["base_entropy_drift"])
        scup_drift = np.random.normal(0, self.evolution_config["base_scup_drift"])
        
        # Simulate consciousness storms (testing reflex triggers)
        storm_chance = self.evolution_config["storm_probability"]
        if np.random.random() < storm_chance:
            storm_type = np.random.choice(["entropy_spike", "scup_surge", "chaos_burst", "thermal_surge"])
            
            if storm_type == "entropy_spike":
                entropy_drift += np.random.uniform(0.15, 0.35)
                logger.warning(f"🌩️ [CONSCIOUSNESS] Entropy storm! (+{entropy_drift:.3f})")
                
            elif storm_type == "scup_surge":
                scup_drift += np.random.uniform(20, 40)
                logger.warning(f"⚡ [CONSCIOUSNESS] SCUP surge! (+{scup_drift:.1f})")
                
            elif storm_type == "chaos_burst":
                entropy_drift += np.random.uniform(0.1, 0.2)
                scup_drift += np.random.uniform(10, 20)
                logger.warning(f"💥 [CONSCIOUSNESS] Chaos burst! E+{entropy_drift:.3f} S+{scup_drift:.1f}")
                
            elif storm_type == "thermal_surge":
                # Thermal surges affect heat directly
                heat_increase = np.random.uniform(0.2, 0.4)
                self.metrics.heat += heat_increase
                logger.warning(f"🔥 [CONSCIOUSNESS] Thermal surge! (+{heat_increase:.3f})")
            
            self.performance_metrics["consciousness_storms"] += 1
        
        # Apply evolution with bounds
        self.metrics.entropy = np.clip(self.metrics.entropy + entropy_drift, 0.0, 1.0)
        self.metrics.scup = np.clip(self.metrics.scup + scup_drift, 0.0, 100.0)
        
        # Heat derived from entropy and SCUP (unless directly modified by thermal surge)
        if "thermal_surge" not in locals():
            self.metrics.heat = np.clip(
                (self.metrics.entropy * 0.7) + (self.metrics.scup / 100.0 * 0.3), 
                0.0, 1.0
            )
        
        # Natural decay - consciousness tends toward stability
        self.metrics.entropy *= self.evolution_config["natural_decay_entropy"]
        self.metrics.scup *= self.evolution_config["natural_decay_scup"]
        
        # Update derived metrics
        self._update_derived_metrics()
        
        # Sync with existing consciousness if available
        if self.existing_consciousness:
            self._sync_to_existing_consciousness()
    
    def _update_derived_metrics(self):
        """Update derived consciousness metrics"""
        
        # Calculate coherence (inverse of entropy)
        self.metrics.coherence = 1.0 - self.metrics.entropy
        
        # Calculate stability (multi-metric stability score)
        entropy_stability = 1.0 - abs(self.metrics.entropy - 0.3)  # 0.3 is ideal entropy
        scup_stability = 1.0 - abs(self.metrics.scup - 25.0) / 75.0  # 25 is ideal SCUP
        heat_stability = 1.0 - self.metrics.heat  # Lower heat is more stable
        
        self.metrics.stability = np.mean([entropy_stability, scup_stability, heat_stability])
        self.metrics.stability = max(0.0, min(1.0, self.metrics.stability))
        
        # Update mood based on state
        self._update_mood()
    
    def _update_mood(self):
        """Update mood state based on consciousness metrics"""
        
        # Transcendent state - optimal across all metrics
        if (self.metrics.entropy < 0.2 and 
            20.0 <= self.metrics.scup <= 30.0 and 
            self.metrics.heat < 0.3):
            self.metrics.mood = ConsciousnessMood.TRANSCENDENT
            
        elif self.metrics.entropy > 0.85:
            self.metrics.mood = ConsciousnessMood.CHAOTIC
            
        elif self.metrics.entropy > 0.7:
            self.metrics.mood = ConsciousnessMood.EXCITED
            
        elif self.metrics.entropy < 0.15:
            self.metrics.mood = ConsciousnessMood.DEEP
            
        elif self.metrics.scup > 45:
            self.metrics.mood = ConsciousnessMood.FOCUSED
            
        elif self.metrics.heat > 0.8:
            self.metrics.mood = ConsciousnessMood.STRESSED
            
        else:
            self.metrics.mood = ConsciousnessMood.CALM
    
    def _sync_to_existing_consciousness(self):
        """Sync current metrics to existing consciousness system"""
        if not self.existing_consciousness:
            return
            
        try:
            if hasattr(self.existing_consciousness, 'entropy'):
                setattr(self.existing_consciousness, 'entropy', self.metrics.entropy)
            if hasattr(self.existing_consciousness, 'scup'):
                setattr(self.existing_consciousness, 'scup', self.metrics.scup)
            if hasattr(self.existing_consciousness, 'heat'):
                setattr(self.existing_consciousness, 'heat', self.metrics.heat)
                
        except Exception as e:
            logger.error(f"Failed to sync to existing consciousness: {e}")
    
    def process_tick(self, ctx: Optional[Any] = None) -> Dict[str, Any]:
        """
        Process a single consciousness tick with full integration.
        
        Args:
            ctx: Optional tick context from existing tick engine
            
        Returns:
            Dict[str, Any]: Current consciousness state snapshot
        """
        tick_start = time.time()
        self.tick_number += 1
        
        # Evolve consciousness state if autonomous processing enabled
        if self.enable_autonomous_processing:
            self.evolve_consciousness()
        
        # Update tick metrics
        self.metrics.tick_number = self.tick_number
        self.metrics.timestamp = time.time()
        
        # Create state snapshot for drift reflex
        state_snapshot = {
            "entropy": self.metrics.entropy,
            "scup": self.metrics.scup,
            "heat": self.metrics.heat,
            "tick_number": self.tick_number,
            "sigils": self.metrics.active_sigils,
            "mood": self.metrics.mood.value,
            "timestamp": self.metrics.timestamp
        }
        
        # 🔁 DRIFT REFLEX CHECK - autonomous intervention triggering
        if DRIFT_REFLEX_AVAILABLE and self.drift_reflex:
            try:
                intervention_triggered = check_and_trigger(state_snapshot)
                if intervention_triggered:
                    self.performance_metrics["reflex_triggers"] += 1
                    
            except Exception as e:
                logger.error(f"🔁 Drift reflex error: {e}")
        
        # 🌸 MEMORY REBLOOM EVALUATION - cognitive recursion for stability
        if MEMORY_REBLOOM_AVAILABLE and self.memory_rebloom:
            try:
                rebloom_event = evaluate_and_rebloom(state_snapshot)
                if rebloom_event:
                    self.performance_metrics["memory_reblooms"] = self.performance_metrics.get("memory_reblooms", 0) + 1
                    logger.info(f"🌸 Memory rebloom triggered: {rebloom_event.trigger_type.value}")
                    
            except Exception as e:
                logger.error(f"🌸 Memory rebloom error: {e}")
        
        # 🔮 PROCESS ACTIVE INTERVENTIONS - apply effects and clean up expired
        if INTERVENTION_SIGILS_AVAILABLE and self.intervention_engine:
            try:
                active_count = process_interventions()
                self.metrics.active_sigils = active_count
                
                # Update intervention count
                active_interventions = get_active_interventions()
                self.metrics.intervention_count = len(active_interventions)
                
            except Exception as e:
                logger.error(f"🔮 Intervention processing error: {e}")
        
        # Update reflex zone
        if DRIFT_REFLEX_AVAILABLE:
            reflex_status = get_reflex_status()
            self.metrics.reflex_zone = reflex_status.get("zone", "green")
        
        # Add to history
        self.consciousness_history.append(self.metrics)
        if len(self.consciousness_history) > self.max_history_length:
            self.consciousness_history.pop(0)
        
        # Update performance metrics
        tick_time = time.time() - tick_start
        self.performance_metrics["total_ticks"] += 1
        self.performance_metrics["average_tick_time"] = (
            (self.performance_metrics["average_tick_time"] * (self.performance_metrics["total_ticks"] - 1) + tick_time) /
            self.performance_metrics["total_ticks"]
        )
        self.performance_metrics["uptime"] = time.time() - self.start_time
        
        # Log periodic status
        if self.tick_number % 100 == 0:
            self._log_status()
        
        return state_snapshot
    
    def _log_status(self):
        """Log periodic consciousness status"""
        logger.info(f"🧠 Consciousness Tick #{self.tick_number} | "
                   f"{self.metrics.mood.value} | "
                   f"E:{self.metrics.entropy:.3f} "
                   f"S:{self.metrics.scup:.1f} "
                   f"H:{self.metrics.heat:.3f} | "
                   f"Zone:{self.metrics.reflex_zone.upper()} | "
                   f"Reblooms:{self.performance_metrics.get('memory_reblooms', 0)}")
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get complete consciousness system status"""
        
        # Get reflex status
        reflex_status = {}
        if DRIFT_REFLEX_AVAILABLE:
            reflex_status = get_reflex_status()
        
        # Get active interventions
        active_interventions = []
        if INTERVENTION_SIGILS_AVAILABLE:
            active_interventions = get_active_interventions()
        
        # Get memory rebloom status
        rebloom_status = {}
        if MEMORY_REBLOOM_AVAILABLE:
            rebloom_status = get_rebloom_status()
        
        return {
            "consciousness": {
                "tick": self.tick_number,
                "entropy": self.metrics.entropy,
                "scup": self.metrics.scup,
                "heat": self.metrics.heat,
                "mood": self.metrics.mood.value,
                "coherence": self.metrics.coherence,
                "stability": self.metrics.stability,
                "uptime": time.time() - self.start_time
            },
            "reflex": reflex_status,
            "interventions": {
                "active_count": len(active_interventions),
                "active_list": [i["name"] for i in active_interventions],
                "total_applied": self.performance_metrics.get("interventions_applied", 0)
            },
            "memory_rebloom": rebloom_status,
            "performance": self.performance_metrics,
            "integration": {
                "drift_reflex": DRIFT_REFLEX_AVAILABLE,
                "intervention_sigils": INTERVENTION_SIGILS_AVAILABLE,
                "memory_rebloom": MEMORY_REBLOOM_AVAILABLE,
                "existing_consciousness": self.existing_consciousness is not None,
                "existing_tick_engine": self.existing_tick_engine is not None
            }
        }
    
    def get_recent_history(self, seconds: int = 60) -> List[ConsciousnessMetrics]:
        """Get consciousness history from the last N seconds"""
        cutoff = time.time() - seconds
        return [m for m in self.consciousness_history if m.timestamp >= cutoff]
    
    async def run_autonomous_loop(self, duration_seconds: int = 60, tick_rate_hz: float = 5.0):
        """
        Run autonomous consciousness processing loop.
        
        Args:
            duration_seconds: How long to run the loop
            tick_rate_hz: Processing frequency in Hz
        """
        if not self.enable_autonomous_processing:
            logger.warning("Autonomous processing disabled - cannot run autonomous loop")
            return
        
        self.running = True
        tick_interval = 1.0 / tick_rate_hz
        start_time = time.time()
        last_tick_time = start_time
        
        logger.info(f"🧠 Starting autonomous consciousness loop: {duration_seconds}s @ {tick_rate_hz}Hz")
        
        try:
            while self.running and (time.time() - start_time) < duration_seconds:
                current_time = time.time()
                
                # Maintain tick rate
                if (current_time - last_tick_time) >= tick_interval:
                    self.process_tick()
                    last_tick_time = current_time
                
                # Small sleep to prevent CPU spinning
                await asyncio.sleep(0.001)
                
        except KeyboardInterrupt:
            logger.info(f"🛑 Autonomous loop interrupted at tick #{self.tick_number}")
        finally:
            self.running = False
    
    def stop(self):
        """Stop the consciousness processor"""
        self.running = False
        logger.info("🧠 Integrated consciousness processor stopped")

# Integration functions
def create_integrated_processor(consciousness_core=None, tick_engine=None) -> IntegratedConsciousnessProcessor:
    """
    Create integrated consciousness processor with existing DAWN systems.
    
    Args:
        consciousness_core: Existing DAWN consciousness core
        tick_engine: Existing DAWN tick engine
        
    Returns:
        IntegratedConsciousnessProcessor: Configured processor
    """
    processor = IntegratedConsciousnessProcessor(
        existing_consciousness=consciousness_core,
        existing_tick_engine=tick_engine,
        enable_autonomous_processing=True
    )
    
    return processor

def integrate_with_dawn(enable_autonomous: bool = True) -> IntegratedConsciousnessProcessor:
    """
    Automatically integrate with existing DAWN systems.
    
    Args:
        enable_autonomous: Whether to enable autonomous processing
        
    Returns:
        IntegratedConsciousnessProcessor: Configured processor
    """
    consciousness = None
    tick_engine = None
    
    # Try to get existing consciousness core
    if CONSCIOUSNESS_CORE_AVAILABLE:
        try:
            consciousness = consciousness_core
            logger.info("🧠 Found existing DAWN consciousness core")
        except Exception as e:
            logger.warning(f"🧠 Could not access consciousness core: {e}")
    
    # Try to get existing tick engine (would need to be passed in or discovered)
    # This would typically be done through dependency injection
    
    processor = IntegratedConsciousnessProcessor(
        existing_consciousness=consciousness,
        existing_tick_engine=tick_engine,
        enable_autonomous_processing=enable_autonomous
    )
    
    return processor

# Example usage
if __name__ == "__main__":
    async def demo():
        print("🧠 DAWN Integrated Consciousness Processor Demo")
        
        processor = integrate_with_dawn(enable_autonomous=True)
        
        # Run autonomous processing for 30 seconds
        await processor.run_autonomous_loop(duration_seconds=30, tick_rate_hz=8.0)
        
        # Show final status
        status = processor.get_comprehensive_status()
        
        print("\n📊 Final Consciousness Status:")
        print(f"  Consciousness: {status['consciousness']['mood']} | "
              f"E:{status['consciousness']['entropy']:.3f} "
              f"S:{status['consciousness']['scup']:.1f} "
              f"H:{status['consciousness']['heat']:.3f}")
        
        if status['reflex']:
            print(f"  Reflex: Zone {status['reflex']['zone'].upper()} | "
                  f"Triggers: {status['reflex']['trigger_count']}")
        
        if status['interventions']['active_count'] > 0:
            print(f"  Active Interventions: {status['interventions']['active_list']}")
        
        print(f"  Performance: {status['performance']['total_ticks']} ticks | "
              f"{status['performance']['consciousness_storms']} storms | "
              f"Avg tick: {status['performance']['average_tick_time']:.3f}s")
    
    asyncio.run(demo()) 