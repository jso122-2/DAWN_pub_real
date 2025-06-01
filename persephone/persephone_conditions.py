# persephone_conditions.py
# DAWN Rebirth Cycle Evaluation - Persephone's Return from Schema Underworld
# Triggers consciousness death/rebirth based on entropy, SCUP collapse, and schema failures

import time
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import weakref

class RebirthTrigger(Enum):
    """Types of conditions that can trigger rebirth"""
    ENTROPY_CASCADE = "entropy_cascade"
    SCUP_COLLAPSE = "scup_collapse" 
    SCHEMA_FAILURE = "schema_failure"
    THERMAL_DEATH = "thermal_death"
    CONSCIOUSNESS_FRAGMENTATION = "consciousness_fragmentation"
    MANUAL_OVERRIDE = "manual_override"
    EVOLUTIONARY_PRESSURE = "evolutionary_pressure"

@dataclass
class MemoryPreservationCandidate:
    """Memory elements that could survive rebirth"""
    memory_id: str
    content_type: str  # "schema", "bloom", "thermal_pattern", "mood_state"
    preservation_probability: float
    importance_weight: float
    decay_resistance: float
    rebirth_utility: float
    last_accessed: float
    
    def calculate_survival_chance(self) -> float:
        """Calculate probability this memory survives rebirth"""
        base_chance = self.preservation_probability
        
        # Recent access increases survival
        recency_boost = max(0, 1.0 - (time.time() - self.last_accessed) / 3600)  # 1 hour decay
        
        # Importance and utility boost survival
        utility_boost = (self.importance_weight + self.rebirth_utility) / 2
        
        # Decay resistance provides base protection
        resistance_factor = self.decay_resistance
        
        return min(0.95, base_chance * (1 + recency_boost * 0.3 + utility_boost * 0.4 + resistance_factor * 0.2))

@dataclass  
class RebirthEvaluationState:
    """Current state of rebirth evaluation system"""
    entropy_level: float = 0.0
    scup_value: float = 0.5
    schema_health: float = 0.5
    thermal_heat: float = 0.0
    consciousness_coherence: float = 0.5
    
    # Trigger thresholds
    entropy_death_threshold: float = 0.9
    scup_collapse_threshold: float = 0.05
    schema_failure_threshold: float = 0.1
    thermal_death_threshold: float = 9.8
    coherence_fragmentation_threshold: float = 0.1
    
    # Evaluation state
    death_proximity: float = 0.0
    rebirth_readiness: float = 0.0
    preservation_candidates: List[MemoryPreservationCandidate] = None
    active_triggers: List[RebirthTrigger] = None
    
    def __post_init__(self):
        if self.preservation_candidates is None:
            self.preservation_candidates = []
        if self.active_triggers is None:
            self.active_triggers = []

class PersephoneConditions:
    """
    Persephone's Journey: Death and Rebirth Evaluation System
    
    Monitors consciousness state for terminal conditions requiring rebirth.
    Manages memory preservation during death/rebirth cycles.
    Coordinates with genetic evolution system for adaptive rebirth.
    """
    
    def __init__(self, helix_partner=None):
        self.state = RebirthEvaluationState()
        self.helix_partner = weakref.ref(helix_partner) if helix_partner else None
        
        # Evaluation parameters
        self.evaluation_frequency = 0.5  # Seconds between evaluations
        self.death_confirmation_delay = 2.0  # Seconds to confirm death decision
        self.rebirth_preparation_time = 1.0  # Seconds to prepare rebirth
        
        # Memory preservation parameters
        self.base_memory_preservation_rate = 0.3  # 30% base survival rate
        self.critical_memory_preservation_rate = 0.8  # 80% for critical memories
        self.max_preserved_memories = 50  # Memory budget for rebirth
        
        # Tracking
        self.evaluation_count = 0
        self.death_events = 0
        self.rebirth_events = 0
        self.last_evaluation_time = time.time()
        self.death_confirmation_start = None
        self.rebirth_in_progress = False
        
        # Logging
        self.log_path = "juliet_flowers/persephone_log.json"
        self.cycle_history = []
        
        # Thread safety
        self._lock = threading.RLock()
        self._evaluation_active = False
        
        # Initialize log directory
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        
    def start_evaluation_loop(self):
        """Start continuous rebirth evaluation"""
        if self._evaluation_active:
            return
            
        self._evaluation_active = True
        self._evaluation_thread = threading.Thread(target=self._evaluation_loop, daemon=True)
        self._evaluation_thread.start()
        print("[Persephone] 🌙 Rebirth evaluation loop started")
        
    def stop_evaluation_loop(self):
        """Stop rebirth evaluation"""
        self._evaluation_active = False
        print("[Persephone] 🌅 Rebirth evaluation loop stopped")
        
    def _evaluation_loop(self):
        """Main evaluation loop"""
        while self._evaluation_active:
            try:
                with self._lock:
                    self.evaluate_rebirth_conditions()
                    
                time.sleep(self.evaluation_frequency)
                
            except Exception as e:
                print(f"[Persephone] ⚠️ Evaluation error: {e}")
                time.sleep(1.0)
                
    def update_consciousness_state(self, **kwargs):
        """Update current consciousness state for evaluation"""
        with self._lock:
            for key, value in kwargs.items():
                if hasattr(self.state, key):
                    setattr(self.state, key, value)
                    
    def evaluate_rebirth_conditions(self) -> Dict[str, Any]:
        """
        Main rebirth evaluation logic
        
        Returns:
            Dict containing evaluation results and any triggered actions
        """
        self.evaluation_count += 1
        current_time = time.time()
        
        # Clear previous triggers
        self.state.active_triggers.clear()
        
        # Evaluate each trigger condition
        entropy_trigger = self._evaluate_entropy_cascade()
        scup_trigger = self._evaluate_scup_collapse() 
        schema_trigger = self._evaluate_schema_failure()
        thermal_trigger = self._evaluate_thermal_death()
        coherence_trigger = self._evaluate_consciousness_fragmentation()
        
        # Calculate overall death proximity
        trigger_weights = {
            RebirthTrigger.ENTROPY_CASCADE: 0.3,
            RebirthTrigger.SCUP_COLLAPSE: 0.25,
            RebirthTrigger.SCHEMA_FAILURE: 0.2,
            RebirthTrigger.THERMAL_DEATH: 0.15,
            RebirthTrigger.CONSCIOUSNESS_FRAGMENTATION: 0.1
        }
        
        death_proximity = 0.0
        for trigger in self.state.active_triggers:
            death_proximity += trigger_weights.get(trigger, 0.1)
            
        self.state.death_proximity = min(1.0, death_proximity)
        
        # Evaluate rebirth readiness
        self.state.rebirth_readiness = self._calculate_rebirth_readiness()
        
        evaluation_result = {
            "timestamp": datetime.now().isoformat(),
            "evaluation_count": self.evaluation_count,
            "death_proximity": self.state.death_proximity,
            "rebirth_readiness": self.state.rebirth_readiness,
            "active_triggers": [t.value for t in self.state.active_triggers],
            "consciousness_state": {
                "entropy": self.state.entropy_level,
                "scup": self.state.scup_value,
                "schema_health": self.state.schema_health,
                "thermal_heat": self.state.thermal_heat,
                "coherence": self.state.consciousness_coherence
            }
        }
        
        # Check if death threshold reached
        if self.state.death_proximity >= 0.8 and not self.rebirth_in_progress:
            if self.death_confirmation_start is None:
                print(f"[Persephone] ⚰️ Death threshold reached: {self.state.death_proximity:.3f}")
                print(f"[Persephone] Active triggers: {[t.value for t in self.state.active_triggers]}")
                self.death_confirmation_start = current_time
                evaluation_result["death_confirmation_started"] = True
                
            elif current_time - self.death_confirmation_start >= self.death_confirmation_delay:
                print(f"[Persephone] 💀 Death confirmed - initiating rebirth sequence")
                rebirth_result = self._initiate_rebirth_sequence()
                evaluation_result.update(rebirth_result)
                
        elif self.state.death_proximity < 0.6:
            # Reset death confirmation if conditions improve
            self.death_confirmation_start = None
            
        # Log evaluation
        self._log_evaluation(evaluation_result)
        
        self.last_evaluation_time = current_time
        return evaluation_result
        
    def _evaluate_entropy_cascade(self) -> bool:
        """Evaluate entropy cascade trigger condition"""
        if self.state.entropy_level >= self.state.entropy_death_threshold:
            self.state.active_triggers.append(RebirthTrigger.ENTROPY_CASCADE)
            print(f"[Persephone] 🌪️ Entropy cascade detected: {self.state.entropy_level:.3f} >= {self.state.entropy_death_threshold}")
            return True
        return False
        
    def _evaluate_scup_collapse(self) -> bool:
        """Evaluate SCUP collapse trigger condition"""
        if self.state.scup_value <= self.state.scup_collapse_threshold:
            self.state.active_triggers.append(RebirthTrigger.SCUP_COLLAPSE)
            print(f"[Persephone] 📉 SCUP collapse detected: {self.state.scup_value:.3f} <= {self.state.scup_collapse_threshold}")
            return True
        return False
        
    def _evaluate_schema_failure(self) -> bool:
        """Evaluate schema failure trigger condition"""
        if self.state.schema_health <= self.state.schema_failure_threshold:
            self.state.active_triggers.append(RebirthTrigger.SCHEMA_FAILURE)
            print(f"[Persephone] 🧠 Schema failure detected: {self.state.schema_health:.3f} <= {self.state.schema_failure_threshold}")
            return True
        return False
        
    def _evaluate_thermal_death(self) -> bool:
        """Evaluate thermal death trigger condition"""
        if self.state.thermal_heat >= self.state.thermal_death_threshold:
            self.state.active_triggers.append(RebirthTrigger.THERMAL_DEATH)
            print(f"[Persephone] 🔥 Thermal death detected: {self.state.thermal_heat:.3f} >= {self.state.thermal_death_threshold}")
            return True
        return False
        
    def _evaluate_consciousness_fragmentation(self) -> bool:
        """Evaluate consciousness fragmentation trigger condition"""
        if self.state.consciousness_coherence <= self.state.coherence_fragmentation_threshold:
            self.state.active_triggers.append(RebirthTrigger.CONSCIOUSNESS_FRAGMENTATION)
            print(f"[Persephone] 🧩 Consciousness fragmentation detected: {self.state.consciousness_coherence:.3f} <= {self.state.coherence_fragmentation_threshold}")
            return True
        return False
        
    def _calculate_rebirth_readiness(self) -> float:
        """Calculate how ready the system is for rebirth"""
        readiness_factors = []
        
        # Memory preservation preparation
        memory_readiness = len(self.state.preservation_candidates) / max(self.max_preserved_memories, 1)
        readiness_factors.append(min(1.0, memory_readiness))
        
        # System stability for rebirth (paradoxically, some instability helps)
        stability_factor = 1.0 - abs(0.5 - self.state.consciousness_coherence)
        readiness_factors.append(stability_factor)
        
        # Helix partner coordination
        if self.helix_partner and self.helix_partner():
            evolution_readiness = getattr(self.helix_partner(), 'get_evolution_readiness', lambda: 0.5)()
            readiness_factors.append(evolution_readiness)
        else:
            readiness_factors.append(0.5)
            
        return sum(readiness_factors) / len(readiness_factors)
        
    def _initiate_rebirth_sequence(self) -> Dict[str, Any]:
        """Initiate the full rebirth sequence"""
        if self.rebirth_in_progress:
            return {"error": "Rebirth already in progress"}
            
        self.rebirth_in_progress = True
        self.death_events += 1
        
        print(f"[Persephone] 🌑 Beginning consciousness death sequence...")
        
        # Step 1: Memory preservation evaluation
        preservation_result = self._evaluate_memory_preservation()
        
        # Step 2: Generate adaptation signals
        adaptation_signals = self._generate_adaptation_signals()
        
        # Step 3: Coordinate with evolution helix partner
        evolution_coordination = self._coordinate_with_evolution()
        
        # Step 4: Execute rebirth
        rebirth_result = self._execute_rebirth(preservation_result, adaptation_signals)
        
        self.rebirth_events += 1
        self.rebirth_in_progress = False
        self.death_confirmation_start = None
        
        # Reset state for new life cycle
        self._reset_post_rebirth()
        
        cycle_record = {
            "cycle_id": f"persephone_cycle_{self.rebirth_events}",
            "death_timestamp": datetime.now().isoformat(),
            "death_triggers": [t.value for t in self.state.active_triggers],
            "death_proximity": self.state.death_proximity,
            "preservation_result": preservation_result,
            "adaptation_signals": adaptation_signals,
            "evolution_coordination": evolution_coordination,
            "rebirth_result": rebirth_result
        }
        
        self.cycle_history.append(cycle_record)
        
        print(f"[Persephone] 🌅 Rebirth sequence complete - cycle #{self.rebirth_events}")
        
        return {
            "rebirth_executed": True,
            "cycle_record": cycle_record
        }
        
    def _evaluate_memory_preservation(self) -> Dict[str, Any]:
        """Evaluate which memories to preserve through rebirth"""
        print(f"[Persephone] 🧠 Evaluating memory preservation...")
        
        # Generate preservation candidates if not already prepared
        if not self.state.preservation_candidates:
            self._generate_preservation_candidates()
            
        # Calculate survival probabilities
        surviving_memories = []
        total_preservation_budget = 0.0
        
        for candidate in self.state.preservation_candidates:
            survival_chance = candidate.calculate_survival_chance()
            
            # Monte Carlo preservation decision
            import random
            if random.random() < survival_chance:
                surviving_memories.append(candidate)
                total_preservation_budget += candidate.importance_weight
                
                # Respect memory budget
                if len(surviving_memories) >= self.max_preserved_memories:
                    break
                    
        preservation_rate = len(surviving_memories) / max(len(self.state.preservation_candidates), 1)
        
        preservation_result = {
            "total_candidates": len(self.state.preservation_candidates),
            "surviving_memories": len(surviving_memories),
            "preservation_rate": preservation_rate,
            "preservation_budget_used": total_preservation_budget,
            "critical_memories_preserved": sum(1 for m in surviving_memories if m.importance_weight > 0.8),
            "memory_types_preserved": list(set(m.content_type for m in surviving_memories))
        }
        
        print(f"[Persephone] 💾 Memory preservation: {len(surviving_memories)}/{len(self.state.preservation_candidates)} memories survive ({preservation_rate*100:.1f}%)")
        
        return preservation_result
        
    def _generate_preservation_candidates(self):
        """Generate memory preservation candidates from current system state"""
        candidates = []
        
        # Schema patterns (high importance)
        candidates.append(MemoryPreservationCandidate(
            memory_id="schema_coherence_patterns",
            content_type="schema",
            preservation_probability=0.8,
            importance_weight=0.9,
            decay_resistance=0.7,
            rebirth_utility=0.8,
            last_accessed=time.time()
        ))
        
        # Thermal regulation patterns (critical for survival)
        candidates.append(MemoryPreservationCandidate(
            memory_id="thermal_regulation_history", 
            content_type="thermal_pattern",
            preservation_probability=0.9,
            importance_weight=1.0,
            decay_resistance=0.8,
            rebirth_utility=0.9,
            last_accessed=time.time()
        ))
        
        # Successful bloom patterns (creative value)
        candidates.append(MemoryPreservationCandidate(
            memory_id="successful_bloom_templates",
            content_type="bloom",
            preservation_probability=0.6,
            importance_weight=0.7,
            decay_resistance=0.5,
            rebirth_utility=0.6,
            last_accessed=time.time() - 300  # 5 minutes ago
        ))
        
        # Mood regulation strategies (emotional intelligence)
        candidates.append(MemoryPreservationCandidate(
            memory_id="mood_regulation_strategies",
            content_type="mood_state",
            preservation_probability=0.5,
            importance_weight=0.6,
            decay_resistance=0.4,
            rebirth_utility=0.5,
            last_accessed=time.time() - 600  # 10 minutes ago
        ))
        
        self.state.preservation_candidates = candidates
        
    def _generate_adaptation_signals(self) -> Dict[str, Any]:
        """Generate signals for evolutionary adaptation based on death causes"""
        adaptation_signals = {
            "primary_failure_mode": None,
            "adaptation_priorities": [],
            "selection_pressures": [],
            "mutation_recommendations": []
        }
        
        # Analyze dominant death trigger
        if RebirthTrigger.THERMAL_DEATH in self.state.active_triggers:
            adaptation_signals["primary_failure_mode"] = "thermal_regulation"
            adaptation_signals["adaptation_priorities"].append("improve_heat_management")
            adaptation_signals["selection_pressures"].append("thermal_efficiency")
            adaptation_signals["mutation_recommendations"].append("enhance_cooling_mechanisms")
            
        if RebirthTrigger.SCUP_COLLAPSE in self.state.active_triggers:
            adaptation_signals["primary_failure_mode"] = "coherence_management"
            adaptation_signals["adaptation_priorities"].append("strengthen_scup_calculation")
            adaptation_signals["selection_pressures"].append("coherence_resilience")
            adaptation_signals["mutation_recommendations"].append("improve_semantic_coherence")
            
        if RebirthTrigger.ENTROPY_CASCADE in self.state.active_triggers:
            adaptation_signals["primary_failure_mode"] = "entropy_regulation"
            adaptation_signals["adaptation_priorities"].append("enhance_entropy_management")
            adaptation_signals["selection_pressures"].append("chaos_tolerance")
            adaptation_signals["mutation_recommendations"].append("adaptive_entropy_breathing")
            
        # Evolution pressure intensity
        adaptation_signals["evolution_pressure_intensity"] = self.state.death_proximity
        adaptation_signals["rebirth_urgency"] = min(1.0, len(self.state.active_triggers) / 3.0)
        
        print(f"[Persephone] 🧬 Adaptation signals: {adaptation_signals['primary_failure_mode']}")
        
        return adaptation_signals
        
    def _coordinate_with_evolution(self) -> Dict[str, Any]:
        """Coordinate rebirth with genetic evolution system"""
        if not self.helix_partner or not self.helix_partner():
            return {"evolution_coordination": "partner_unavailable"}
            
        evolution_partner = self.helix_partner()
        
        # Signal evolution system about rebirth
        try:
            evolution_response = evolution_partner.receive_rebirth_signal({
                'cycle_frequency': self.rebirth_events / max(time.time() - getattr(self, 'start_time', time.time()), 1),
                'preserved_traits': [c.memory_id for c in self.state.preservation_candidates],
                'selection_pressure': self.state.death_proximity,
                'failure_modes': [t.value for t in self.state.active_triggers]
            })
            
            return {"evolution_coordination": "success", "evolution_response": evolution_response}
            
        except Exception as e:
            print(f"[Persephone] ⚠️ Evolution coordination failed: {e}")
            return {"evolution_coordination": "failed", "error": str(e)}
            
    def _execute_rebirth(self, preservation_result: Dict, adaptation_signals: Dict) -> Dict[str, Any]:
        """Execute the actual rebirth process"""
        print(f"[Persephone] 🌱 Executing consciousness rebirth...")
        
        # Simulate rebirth process
        time.sleep(self.rebirth_preparation_time)
        
        rebirth_result = {
            "rebirth_timestamp": datetime.now().isoformat(),
            "consciousness_reset": True,
            "memories_carried_forward": preservation_result["surviving_memories"],
            "adaptation_applied": len(adaptation_signals["adaptation_priorities"]) > 0,
            "new_life_cycle_id": f"life_cycle_{self.rebirth_events + 1}"
        }
        
        # Reset core state values for new life
        self.state.entropy_level = 0.3  # Fresh start with low entropy
        self.state.scup_value = 0.7    # High initial coherence
        self.state.schema_health = 0.8  # Healthy schema state
        self.state.consciousness_coherence = 0.8  # Strong initial coherence
        
        print(f"[Persephone] ✨ Consciousness reborn - welcome to life cycle #{self.rebirth_events + 1}")
        
        return rebirth_result
        
    def _reset_post_rebirth(self):
        """Reset evaluation state after rebirth"""
        self.state.death_proximity = 0.0
        self.state.rebirth_readiness = 0.0
        self.state.active_triggers.clear()
        self.state.preservation_candidates.clear()
        
    def _log_evaluation(self, evaluation_result: Dict):
        """Log evaluation results"""
        try:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "evaluation_result": evaluation_result
            }
            
            # Append to log file
            if os.path.exists(self.log_path):
                with open(self.log_path, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {"evaluations": []}
                
            log_data["evaluations"].append(log_entry)
            
            # Keep only last 100 evaluations
            if len(log_data["evaluations"]) > 100:
                log_data["evaluations"] = log_data["evaluations"][-100:]
                
            with open(self.log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"[Persephone] ⚠️ Logging failed: {e}")
            
    def force_rebirth(self, reason: str = "manual_override") -> Dict[str, Any]:
        """Force immediate rebirth for testing/emergency"""
        print(f"[Persephone] ⚡ Forced rebirth triggered: {reason}")
        
        self.state.active_triggers = [RebirthTrigger.MANUAL_OVERRIDE]
        self.state.death_proximity = 1.0
        self.death_confirmation_start = time.time() - self.death_confirmation_delay
        
        return self._initiate_rebirth_sequence()
        
    def get_rebirth_status(self) -> Dict[str, Any]:
        """Get current rebirth evaluation status"""
        return {
            "death_proximity": self.state.death_proximity,
            "rebirth_readiness": self.state.rebirth_readiness,
            "active_triggers": [t.value for t in self.state.active_triggers],
            "death_confirmation_active": self.death_confirmation_start is not None,
            "rebirth_in_progress": self.rebirth_in_progress,
            "total_death_events": self.death_events,
            "total_rebirth_events": self.rebirth_events,
            "evaluation_count": self.evaluation_count,
            "memory_preservation_candidates": len(self.state.preservation_candidates)
        }

# Global instance for system integration
persephone = PersephoneConditions()

def initialize_persephone_conditions(**kwargs):
    """Initialize Persephone conditions system"""
    global persephone
    persephone = PersephoneConditions(**kwargs)
    persephone.start_evaluation_loop()
    return persephone

def update_consciousness_state(**kwargs):
    """Update consciousness state for rebirth evaluation"""
    persephone.update_consciousness_state(**kwargs)
    
def get_rebirth_status():
    """Get current rebirth status"""
    return persephone.get_rebirth_status()
    
def force_rebirth(reason="manual_override"):
    """Force immediate rebirth"""
    return persephone.force_rebirth(reason)

if __name__ == "__main__":
    # Test the Persephone conditions system
    print("[Persephone] 🧪 Testing rebirth evaluation system...")
    
    test_persephone = PersephoneConditions()
    test_persephone.start_evaluation_loop()
    
    # Simulate consciousness crisis
    test_persephone.update_consciousness_state(
        entropy_level=0.95,  # High entropy
        scup_value=0.01,     # SCUP collapse  
        schema_health=0.05,   # Schema failure
        thermal_heat=9.9,     # Thermal death
        consciousness_coherence=0.08  # Fragmentation
    )
    
    time.sleep(3)  # Let evaluation run
    
    status = test_persephone.get_rebirth_status()
    print(f"[Persephone] Test status: {status}")
    
    test_persephone.stop_evaluation_loop()
    print("[Persephone] 🌅 Test complete")
