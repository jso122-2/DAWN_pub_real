#!/usr/bin/env python3
"""
DAWN Consciousness Intervention Sigils
Autonomous consciousness stabilization through symbolic interventions

These sigils are triggered by the drift reflex system when cognitive
stress thresholds are crossed. They apply specific effects to
consciousness state to maintain cognitive stability.
"""

import time
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

# Import existing sigil components if available
try:
    from core.sigil_engine import Sigil, CognitiveHouse, SigilPriority
    ADVANCED_SIGIL_ENGINE = True
except ImportError:
    ADVANCED_SIGIL_ENGINE = False

logger = logging.getLogger("consciousness_intervention")

class InterventionSigil(Enum):
    """Built-in consciousness intervention sigils"""
    STABILIZE_PROTOCOL = "STABILIZE_PROTOCOL"
    REBALANCE_VECTOR = "REBALANCE_VECTOR"
    REBLOOM_MEMORY = "REBLOOM_MEMORY"
    EMERGENCY_STABILIZE = "EMERGENCY_STABILIZE"
    THERMAL_REGULATION = "THERMAL_REGULATION"
    ENTROPY_DAMPING = "ENTROPY_DAMPING"
    SCUP_MODULATION = "SCUP_MODULATION"

@dataclass
class SigilEffect:
    """Define the effects a sigil has on consciousness state"""
    name: str
    duration: float = 10.0
    priority: int = 2  # 1=low, 2=normal, 3=high, 4=critical
    
    # Multiplicative effects (applied as: value *= effect)
    entropy_multiplier: Optional[float] = None
    scup_multiplier: Optional[float] = None
    heat_multiplier: Optional[float] = None
    
    # Additive effects (applied as: value += effect)
    entropy_additive: Optional[float] = None
    scup_additive: Optional[float] = None
    heat_additive: Optional[float] = None
    
    # Special effects
    memory_boost: bool = False
    heat_reduction: Optional[float] = None
    description: str = "Consciousness intervention"

@dataclass
class ActiveInterventionSigil:
    """An active consciousness intervention sigil"""
    sigil: InterventionSigil
    effect: SigilEffect
    activation_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_expired(self) -> bool:
        """Check if sigil has expired"""
        return time.time() > (self.activation_time + self.effect.duration)
    
    @property
    def time_remaining(self) -> float:
        """Get remaining time for this sigil"""
        return max(0, (self.activation_time + self.effect.duration) - time.time())

class ConsciousnessInterventionEngine:
    """
    Consciousness intervention system using symbolic sigils.
    
    Manages intervention sigils that are triggered by the drift reflex
    to stabilize consciousness during periods of cognitive stress.
    """
    
    def __init__(self, consciousness_engine: Optional[Any] = None):
        self.consciousness_engine = consciousness_engine
        self.active_sigils: List[ActiveInterventionSigil] = []
        self.total_activations = 0
        
        # Define built-in intervention sigils
        self.intervention_effects = self._create_intervention_effects()
        
        logger.info("🔮 Consciousness Intervention Engine initialized")
        logger.info(f"  ✅ {len(self.intervention_effects)} intervention sigils loaded")
    
    def _create_intervention_effects(self) -> Dict[InterventionSigil, SigilEffect]:
        """Create the built-in consciousness intervention sigils"""
        return {
            InterventionSigil.STABILIZE_PROTOCOL: SigilEffect(
                name="Stabilize Protocol",
                duration=15.0,
                priority=3,
                entropy_multiplier=0.7,
                scup_multiplier=0.9,
                description="Reduces cognitive chaos and processing load"
            ),
            
            InterventionSigil.REBALANCE_VECTOR: SigilEffect(
                name="Rebalance Vector",
                duration=12.0,
                priority=2,
                entropy_multiplier=0.8,
                scup_multiplier=0.85,
                description="Rebalances processing vector and entropy"
            ),
            
            InterventionSigil.REBLOOM_MEMORY: SigilEffect(
                name="Rebloom Memory",
                duration=8.0,
                priority=2,
                entropy_multiplier=0.9,
                scup_additive=5.0,  # Temporary processing increase
                memory_boost=True,
                description="Triggers memory rebloom process"
            ),
            
            InterventionSigil.EMERGENCY_STABILIZE: SigilEffect(
                name="Emergency Stabilize",
                duration=20.0,
                priority=4,
                entropy_multiplier=0.5,
                scup_multiplier=0.7,
                heat_reduction=0.3,
                description="Emergency consciousness stabilization"
            ),
            
            InterventionSigil.THERMAL_REGULATION: SigilEffect(
                name="Thermal Regulation",
                duration=10.0,
                priority=3,
                heat_multiplier=0.8,
                entropy_multiplier=0.9,
                description="Regulates thermal consciousness state"
            ),
            
            InterventionSigil.ENTROPY_DAMPING: SigilEffect(
                name="Entropy Damping",
                duration=12.0,
                priority=3,
                entropy_multiplier=0.6,
                description="Targeted entropy reduction for stability"
            ),
            
            InterventionSigil.SCUP_MODULATION: SigilEffect(
                name="SCUP Modulation",
                duration=8.0,
                priority=2,
                scup_multiplier=0.75,
                description="Modulates processing intensity"
            )
        }
    
    def register(self, sigil_name: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        Register and activate a consciousness intervention sigil.
        
        Args:
            sigil_name: Name of the intervention sigil to activate
            metadata: Optional metadata for this activation
            
        Returns:
            bool: True if sigil was successfully registered and activated
        """
        # Convert string name to enum
        try:
            sigil_enum = InterventionSigil(sigil_name)
        except ValueError:
            logger.error(f"🔮 Unknown intervention sigil: {sigil_name}")
            return False
        
        # Get sigil effect
        effect = self.intervention_effects.get(sigil_enum)
        if not effect:
            logger.error(f"🔮 No effect defined for sigil: {sigil_name}")
            return False
        
        # Check if this sigil is already active
        for active in self.active_sigils:
            if active.sigil == sigil_enum and not active.is_expired:
                logger.warning(f"🔮 {sigil_name} already active, extending duration")
                active.activation_time = time.time()  # Reset timer
                return True
        
        # Create new active sigil
        new_sigil = ActiveInterventionSigil(
            sigil=sigil_enum,
            effect=effect,
            activation_time=time.time(),
            metadata=metadata or {}
        )
        
        # Insert in priority order
        self.active_sigils.append(new_sigil)
        self.active_sigils.sort(key=lambda s: s.effect.priority, reverse=True)
        
        self.total_activations += 1
        
        # Apply immediate effects if consciousness engine is available
        if self.consciousness_engine:
            self._apply_sigil_effects(new_sigil)
        
        logger.warning(f"🔮 INTERVENTION ACTIVATED: {sigil_name} | "
                      f"Priority: {effect.priority} | Duration: {effect.duration}s")
        
        return True
    
    def _apply_sigil_effects(self, active_sigil: ActiveInterventionSigil):
        """Apply a sigil's effects to the consciousness engine"""
        if not self.consciousness_engine:
            return
        
        effect = active_sigil.effect
        
        # Apply multiplicative effects
        if effect.entropy_multiplier is not None:
            old_entropy = getattr(self.consciousness_engine, 'entropy', 0.0)
            new_entropy = old_entropy * effect.entropy_multiplier
            setattr(self.consciousness_engine, 'entropy', new_entropy)
            logger.debug(f"🔮 Entropy: {old_entropy:.3f} → {new_entropy:.3f}")
        
        if effect.scup_multiplier is not None:
            old_scup = getattr(self.consciousness_engine, 'scup', 0.0)
            new_scup = old_scup * effect.scup_multiplier
            setattr(self.consciousness_engine, 'scup', new_scup)
            logger.debug(f"🔮 SCUP: {old_scup:.1f} → {new_scup:.1f}")
        
        if effect.heat_multiplier is not None:
            old_heat = getattr(self.consciousness_engine, 'heat', 0.0)
            new_heat = old_heat * effect.heat_multiplier
            setattr(self.consciousness_engine, 'heat', new_heat)
            logger.debug(f"🔮 Heat: {old_heat:.3f} → {new_heat:.3f}")
        
        # Apply additive effects
        if effect.entropy_additive is not None:
            current = getattr(self.consciousness_engine, 'entropy', 0.0)
            setattr(self.consciousness_engine, 'entropy', current + effect.entropy_additive)
        
        if effect.scup_additive is not None:
            current = getattr(self.consciousness_engine, 'scup', 0.0)
            setattr(self.consciousness_engine, 'scup', current + effect.scup_additive)
        
        if effect.heat_additive is not None:
            current = getattr(self.consciousness_engine, 'heat', 0.0)
            setattr(self.consciousness_engine, 'heat', current + effect.heat_additive)
        
        # Apply special effects
        if effect.heat_reduction is not None:
            current_heat = getattr(self.consciousness_engine, 'heat', 0.0)
            new_heat = max(0, current_heat - effect.heat_reduction)
            setattr(self.consciousness_engine, 'heat', new_heat)
        
        if effect.memory_boost:
            logger.info("🔮 Memory rebloom intervention initiated")
            # Trigger memory rebloom if available
            if hasattr(self.consciousness_engine, 'trigger_rebloom'):
                self.consciousness_engine.trigger_rebloom()
        
        # Ensure consciousness values stay within bounds
        self._enforce_consciousness_bounds()
    
    def _enforce_consciousness_bounds(self):
        """Ensure consciousness values stay within valid ranges"""
        if not self.consciousness_engine:
            return
        
        # Entropy: 0.0 - 1.0
        if hasattr(self.consciousness_engine, 'entropy'):
            entropy = getattr(self.consciousness_engine, 'entropy')
            setattr(self.consciousness_engine, 'entropy', max(0.0, min(1.0, entropy)))
        
        # SCUP: 0.0 - 100.0
        if hasattr(self.consciousness_engine, 'scup'):
            scup = getattr(self.consciousness_engine, 'scup')
            setattr(self.consciousness_engine, 'scup', max(0.0, min(100.0, scup)))
        
        # Heat: 0.0 - 1.0
        if hasattr(self.consciousness_engine, 'heat'):
            heat = getattr(self.consciousness_engine, 'heat')
            setattr(self.consciousness_engine, 'heat', max(0.0, min(1.0, heat)))
    
    def process_active_sigils(self) -> int:
        """
        Process all active sigils and remove expired ones
        
        Returns:
            int: Number of currently active sigils
        """
        # Remove expired sigils
        before_count = len(self.active_sigils)
        self.active_sigils = [s for s in self.active_sigils if not s.is_expired]
        
        if len(self.active_sigils) < before_count:
            expired_count = before_count - len(self.active_sigils)
            logger.info(f"🔮 {expired_count} intervention sigil(s) expired")
        
        return len(self.active_sigils)
    
    def get_active_sigils(self) -> List[Dict[str, Any]]:
        """Get information about currently active intervention sigils"""
        return [
            {
                "name": sigil.sigil.value,
                "effect_name": sigil.effect.name,
                "priority": sigil.effect.priority,
                "time_remaining": sigil.time_remaining,
                "description": sigil.effect.description
            }
            for sigil in self.active_sigils
            if not sigil.is_expired
        ]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get intervention system statistics"""
        active_count = len([s for s in self.active_sigils if not s.is_expired])
        
        return {
            "total_activations": self.total_activations,
            "active_count": active_count,
            "available_sigils": [s.value for s in InterventionSigil],
            "active_sigils": [s.sigil.value for s in self.active_sigils if not s.is_expired]
        }
    
    def set_consciousness_engine(self, engine: Any):
        """Connect consciousness engine for applying effects"""
        self.consciousness_engine = engine
        logger.info("🔮 Consciousness engine connected to intervention system")
    
    def clear_all_sigils(self):
        """Clear all active intervention sigils - emergency reset"""
        count = len(self.active_sigils)
        self.active_sigils.clear()
        logger.warning(f"🔮 Emergency clear: {count} intervention sigils deactivated")

# Integration with existing sigil engine
def integrate_with_sigil_engine(sigil_engine: Any, consciousness_engine: Any) -> ConsciousnessInterventionEngine:
    """
    Integrate consciousness intervention sigils with existing sigil engine.
    
    Args:
        sigil_engine: Existing DAWN sigil engine
        consciousness_engine: DAWN consciousness engine
        
    Returns:
        ConsciousnessInterventionEngine: Configured intervention engine
    """
    intervention_engine = ConsciousnessInterventionEngine(consciousness_engine)
    
    # If using advanced sigil engine, register intervention sigils
    if ADVANCED_SIGIL_ENGINE and hasattr(sigil_engine, 'register_sigil'):
        logger.info("🔮 Registering intervention sigils with advanced sigil engine")
        
        for sigil_enum, effect in intervention_engine.intervention_effects.items():
            try:
                # Create advanced sigil object
                advanced_sigil = Sigil(
                    name=sigil_enum.value,
                    temp=75.0,  # High activation temperature for interventions
                    house=CognitiveHouse.META,
                    convolution_level=effect.priority + 2
                )
                
                sigil_engine.register_sigil(advanced_sigil)
                logger.debug(f"  ✅ Registered {sigil_enum.value}")
                
            except Exception as e:
                logger.warning(f"  ⚠️ Failed to register {sigil_enum.value}: {e}")
    
    # Connect intervention engine to main sigil engine
    if hasattr(sigil_engine, 'register_processor'):
        sigil_engine.register_processor('intervention', intervention_engine.register)
    
    return intervention_engine

# Global instance management
_global_intervention_engine = None

def get_intervention_engine() -> ConsciousnessInterventionEngine:
    """Get the global consciousness intervention engine"""
    global _global_intervention_engine
    if _global_intervention_engine is None:
        _global_intervention_engine = ConsciousnessInterventionEngine()
    return _global_intervention_engine

def register_intervention(sigil_name: str, metadata: Optional[Dict[str, Any]] = None) -> bool:
    """
    Register a consciousness intervention sigil
    Called by drift reflex system when intervention is needed
    """
    engine = get_intervention_engine()
    return engine.register(sigil_name, metadata)

def process_interventions() -> int:
    """Process active intervention sigils - call regularly from tick loop"""
    engine = get_intervention_engine()
    return engine.process_active_sigils()

def get_active_interventions() -> List[Dict[str, Any]]:
    """Get list of currently active intervention sigils"""
    engine = get_intervention_engine()
    return engine.get_active_sigils()

def connect_consciousness_engine(engine: Any):
    """Connect consciousness engine for intervention effects"""
    intervention_engine = get_intervention_engine()
    intervention_engine.set_consciousness_engine(engine)

# Example usage
if __name__ == "__main__":
    print("🔮 Testing DAWN Consciousness Intervention System")
    
    # Create mock consciousness engine
    class MockConsciousness:
        def __init__(self):
            self.entropy = 0.8
            self.scup = 60.0
            self.heat = 0.7
    
    mock_consciousness = MockConsciousness()
    intervention_engine = ConsciousnessInterventionEngine(mock_consciousness)
    
    print(f"Initial state: E={mock_consciousness.entropy} S={mock_consciousness.scup} H={mock_consciousness.heat}")
    
    # Test intervention
    success = intervention_engine.register("EMERGENCY_STABILIZE")
    print(f"Emergency stabilize triggered: {success}")
    
    print(f"After intervention: E={mock_consciousness.entropy:.3f} S={mock_consciousness.scup:.1f} H={mock_consciousness.heat:.3f}")
    
    # Show active sigils
    active = intervention_engine.get_active_sigils()
    print(f"Active interventions: {active}")
    
    print("✅ Consciousness intervention test complete") 