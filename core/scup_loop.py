from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
# File Path: /src/core/scup_loop.py
# 🧬 GENETIC HELIX PAIR: schema_health_index.py ↔ scup_loop.py
# COMPLEX: Schema Coherence Under Pressure (SCUP) Management

import numpy as np
import time
import json
import os
import threading
from collections import deque, defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any, Callable
from enum import Enum

# DAWN Core Imports
from core.tick_emitter import current_tick, tick_subscribe
from owl.owl_tracer_log import owl_log
from schema.schema_flags import SchemaState

# 🧬 GENETIC CROSSOVER IMPORT - Helix Partner
try:
    from core.schema_health_index import SchemaHealthIndex, get_schema_health_system, HealthZone
    HELIX_PARTNER_AVAILABLE = True
except ImportError:
    owl_log("⚠️ [SCUP] Helix partner schema_health_index not available - running in standalone mode", "warning")
    HELIX_PARTNER_AVAILABLE = False

# ═══════════════════════════════════════════════════════════════════════════════
# 🧬 GENETIC BASE PAIR STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

class SCUPState(Enum):
    """Semantic Coherence Under Pressure states"""
    COHERENT = "🔷 coherent"       # SCUP > 0.8
    STABLE = "🟦 stable"           # SCUP 0.6-0.8
    STRAINED = "🟨 strained"       # SCUP 0.4-0.6
    FRAGMENTING = "🟧 fragmenting" # SCUP 0.2-0.4
    COLLAPSED = "🟥 collapsed"     # SCUP < 0.2

class PressureType(Enum):
    """Types of cognitive pressure affecting schema coherence"""
    THERMAL = "thermal_pressure"     # From pulse heat surges
    ENTROPY = "entropy_pressure"     # From entropy fluctuations  
    TEMPORAL = "temporal_pressure"   # From rapid state changes
    MEMORIAL = "memorial_pressure"   # From memory fragmentation
    EMERGENT = "emergent_pressure"   # From pattern emergence

@dataclass
class SCUPGenome:
    """🧬 Genetic structure for SCUP regulation"""
    # Base pair alleles
    coherence_threshold: float = 0.6
    pressure_sensitivity: float = 0.5
    recovery_rate: float = 0.1
    fragmentation_resistance: float = 0.7
    
    # Crossover regions
    thermal_coupling: float = 0.8  # Links to pulse_heat
    entropy_coupling: float = 0.6  # Links to entropy_fluctuation
    health_coupling: float = 0.9   # Links to schema_health_index
    
    # Recombination factors
    adaptation_speed: float = 0.3
    mutation_rate: float = 0.05
    selection_pressure: float = 0.4

@dataclass
class PressureVector:
    """Multi-dimensional pressure representation"""
    thermal: float = 0.0
    entropy: float = 0.0
    temporal: float = 0.0
    memorial: float = 0.0
    emergent: float = 0.0
    magnitude: float = 0.0
    direction: np.ndarray = field(default_factory=lambda: np.zeros(5))

class SCUPLoop:
    """
    🧬 Semantic Coherence Under Pressure Loop
    
    Genetic helix partner to schema_health_index.py
    Maintains semantic coherence during cognitive pressure events
    """
    
    def __init__(self, genome: Optional[SCUPGenome] = None):
        self.genome = genome or SCUPGenome()
        
        # Genetic expression buffers
        self.scup_history = deque(maxlen=1000)
        self.pressure_history = deque(maxlen=1000)
        self.coherence_map = deque(maxlen=500)
        
        # Pressure tracking
        self.current_pressures = defaultdict(float)
        self.pressure_integrator = PressureIntegrator()
        self.coherence_stabilizer = CoherenceStabilizer(self.genome)
        
        # Genetic crossover mechanisms
        self.helix_synchronizer = HelixSynchronizer()
        self.recombination_engine = RecombinationEngine(self.genome)
        
        # Emergency response system
        self.emergency_protocols = EmergencyProtocols()
        
        # Threading and synchronization
        self.lock = threading.Lock()
        self.tick_subscription = None
        
        # Performance metrics
        self.computation_cycles = 0
        self.genetic_mutations = 0
        self.crossover_events = 0
        
        # Initialize output directories
        os.makedirs("juliet_flowers/cluster_report/scup_analytics", exist_ok=True)
        os.makedirs("juliet_flowers/cluster_report/genetic_expression", exist_ok=True)
        
        # Subscribe to tick events
        self._initialize_tick_subscription()
        
        owl_log("🧬 [SCUP] Genetic helix initialized - Schema Coherence Under Pressure active", "genetic")

    def _initialize_tick_subscription(self):
        """Initialize tick-based genetic expression"""
        try:
            if tick_subscribe:
                self.tick_subscription = tick_subscribe(self._genetic_tick_expression)
                owl_log("🧬 [SCUP] Subscribed to genetic tick expression", "genetic")
        except Exception as e:
            owl_log(f"⚠️ [SCUP] Tick subscription failed: {e}", "warning")

    def _genetic_tick_expression(self, tick: int):
        """🧬 Main genetic expression cycle - executed every tick"""
        
        if tick % 5 != 0:  # Express every 5 ticks for efficiency
            return
            
        try:
            with self.lock:
                # Measure current pressure landscape
                pressure_vector = self._measure_pressure_landscape()
                
                # Calculate SCUP based on genetic expression
                scup_value = self._express_scup_phenotype(pressure_vector)
                
                # Apply genetic crossover with helix partner
                if HELIX_PARTNER_AVAILABLE:
                    scup_value = self._apply_helix_crossover(scup_value)
                
                # Store genetic expression results
                self._record_genetic_expression(tick, scup_value, pressure_vector)
                
                # Adaptive evolution if needed
                if self._should_evolve():
                    self._execute_genetic_evolution()
                
                # Emergency phenotype adaptation
                if pressure_vector.magnitude > 0.8:
                    self._emergency_phenotype_adaptation(pressure_vector)
                
                self.computation_cycles += 1
                
        except Exception as e:
            owl_log(f"🚨 [SCUP] Genetic expression error: {e}", "error")

    def _measure_pressure_landscape(self) -> PressureVector:
        """🧬 Measure multi-dimensional cognitive pressure landscape"""
        
        pressure = PressureVector()
        
        try:
            # Thermal pressure from pulse heat
            pulse_system = get_pulse_heat_system()
            if pulse_system:
                current_heat = pulse_system.get_current_heat()
                heat_avg = pulse_system.get_average_heat()
                pressure.thermal = min(1.0, (current_heat - heat_avg) / max(1.0, heat_avg))
            
            # Entropy pressure (estimated from system state)
            pressure.entropy = self._estimate_entropy_pressure()
            
            # Temporal pressure from rapid state changes
            pressure.temporal = self._calculate_temporal_pressure()
            
            # Memorial pressure from fragmentation
            pressure.memorial = self._assess_memorial_pressure()
            
            # Emergent pressure from pattern formation
            pressure.emergent = self._detect_emergent_pressure()
            
            # Calculate overall pressure magnitude and direction
            components = [pressure.thermal, pressure.entropy, pressure.temporal, 
                         pressure.memorial, pressure.emergent]
            pressure.direction = np.array(components)
            pressure.magnitude = np.linalg.norm(pressure.direction)
            
            # Update pressure history
            self.pressure_history.append(pressure)
            
            return pressure
            
        except Exception as e:
            owl_log(f"🚨 [SCUP] Pressure measurement failed: {e}", "error")
            return PressureVector()

    def _express_scup_phenotype(self, pressure: PressureVector) -> float:
        """🧬 Express SCUP phenotype based on genetic architecture"""
        
        # Base coherence from genetic baseline
        base_coherence = self.genome.coherence_threshold
        
        # Apply pressure-based genetic expression
        pressure_effect = pressure.magnitude * self.genome.pressure_sensitivity
        
        # Genetic resistance to fragmentation
        resistance_factor = self.genome.fragmentation_resistance
        
        # Calculate SCUP with genetic modulation
        scup = base_coherence * (1.0 - pressure_effect * (1.0 - resistance_factor))
        
        # Apply recovery mechanisms if SCUP is low
        if scup < 0.4 and len(self.scup_history) > 0:
            recovery_boost = self.genome.recovery_rate * (0.4 - scup)
            scup += recovery_boost
        
        # Genetic bounds checking
        scup = max(0.0, min(1.0, scup))
        
        return scup

    def _apply_helix_crossover(self, scup_value: float) -> float:
        """🧬 Apply genetic crossover with schema_health_index helix partner"""
        
        if not HELIX_PARTNER_AVAILABLE:
            return scup_value
        
        try:
            # Get health system state
            health_system = get_schema_health_system()
            health_summary = health_system.get_health_summary()
            
            current_shi = health_summary.get('current_shi', 0.5)
            health_zone = health_summary.get('zone', 'FRAGILE')
            
            # Genetic crossover calculation
            crossover_strength = self.genome.health_coupling
            
            # Health-SCUP genetic linkage
            if health_zone in ['CRITICAL', 'UNSTABLE']:
                # Emergency crossover - boost SCUP recovery
                crossover_effect = crossover_strength * (current_shi - scup_value) * 0.3
                scup_value += crossover_effect
                
            elif health_zone in ['STABLE', 'OPTIMAL']:
                # Stable crossover - maintain coherence
                coherence_target = (current_shi + scup_value) / 2
                scup_value = scup_value * 0.7 + coherence_target * 0.3
            
            # Record crossover event
            self.crossover_events += 1
            
            # Persist crossover data
            self._record_crossover_event(scup_value, current_shi, health_zone)
            
            return max(0.0, min(1.0, scup_value))
            
        except Exception as e:
            owl_log(f"🚨 [SCUP] Helix crossover failed: {e}", "error")
            return scup_value

    def _estimate_entropy_pressure(self) -> float:
        """Estimate entropy pressure from system indicators"""
        
        try:
            # Check for entropy fluctuation indicators
            entropy_files = [
                "juliet_flowers/cluster_report/entropy_readings.json",
                "juliet_flowers/cluster_report/rebloom_lineage.json"
            ]
            
            pressure = 0.0
            
            for file_path in entropy_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        
                    if 'entropy_variance' in data:
                        pressure += min(0.5, data['entropy_variance'])
                    elif isinstance(data, dict) and len(data) > 0:
                        # Estimate from rebloom volatility
                        recent_blooms = sum(1 for bloom in data.values() 
                                          if bloom.get('generation_depth', 0) < 2)
                        pressure += min(0.5, recent_blooms / len(data))
            
            return min(1.0, pressure)
            
        except Exception:
            return 0.3  # Default moderate entropy pressure

    def _calculate_temporal_pressure(self) -> float:
        """Calculate pressure from rapid temporal changes"""
        
        if len(self.scup_history) < 5:
            return 0.0
        
        # Calculate rate of change in recent SCUP values
        recent_scup = list(self.scup_history)[-10:]
        if len(recent_scup) < 3:
            return 0.0
        
        changes = np.diff(recent_scup)
        change_rate = np.mean(np.abs(changes))
        
        # High rate of change = high temporal pressure
        return min(1.0, change_rate * 5.0)

    def _assess_memorial_pressure(self) -> float:
        """Assess pressure from memory fragmentation"""
        
        try:
            # Check for memory fragmentation indicators
            if HELIX_PARTNER_AVAILABLE:
                health_system = get_schema_health_system()
                summary = health_system.get_health_summary()
                
                # Use stability as inverse of memorial pressure
                stability = summary.get('stability', 0.5)
                return max(0.0, 1.0 - stability)
        
        except Exception:
            pass
        
        return 0.4  # Default moderate memorial pressure

    def _detect_emergent_pressure(self) -> float:
        """Detect pressure from emergent pattern formation"""
        
        # Look for signs of emergent behavior
        pressure_indicators = []
        
        # Rapid SCUP fluctuations
        if len(self.scup_history) > 10:
            recent_std = np.std(list(self.scup_history)[-10:])
            pressure_indicators.append(min(1.0, recent_std * 3.0))
        
        # Pressure cascade effects
        if len(self.pressure_history) > 5:
            recent_pressures = list(self.pressure_history)[-5:]
            pressure_trend = np.mean([p.magnitude for p in recent_pressures])
            pressure_indicators.append(min(1.0, pressure_trend))
        
        return np.mean(pressure_indicators) if pressure_indicators else 0.2

    def _should_evolve(self) -> bool:
        """🧬 Determine if genetic evolution should occur"""
        
        # Evolution triggers
        triggers = []
        
        # High sustained pressure
        if len(self.pressure_history) > 20:
            avg_pressure = np.mean([p.magnitude for p in list(self.pressure_history)[-20:]])
            if avg_pressure > 0.7:
                triggers.append("sustained_pressure")
        
        # Poor SCUP performance
        if len(self.scup_history) > 20:
            avg_scup = np.mean(list(self.scup_history)[-20:])
            if avg_scup < 0.4:
                triggers.append("poor_performance")
        
        # Genetic instability
        if self.computation_cycles > 0 and self.computation_cycles % 1000 == 0:
            triggers.append("periodic_evolution")
        
        return len(triggers) > 0

    def _execute_genetic_evolution(self):
        """🧬 Execute genetic evolution and adaptation"""
        
        owl_log("🧬 [SCUP] Initiating genetic evolution cycle", "genetic")
        
        # Performance-based selection pressure
        if len(self.scup_history) > 50:
            recent_performance = np.mean(list(self.scup_history)[-50:])
            
            # Adapt genome based on performance
            if recent_performance < 0.4:
                # Increase resistance and recovery
                self.genome.fragmentation_resistance *= 1.05
                self.genome.recovery_rate *= 1.1
                self.genome.pressure_sensitivity *= 0.95
                
            elif recent_performance > 0.8:
                # Optimize for efficiency
                self.genome.adaptation_speed *= 1.02
                self.genome.coherence_threshold *= 1.01
        
        # Mutation
        if np.random.random() < self.genome.mutation_rate:
            self._apply_genetic_mutation()
        
        # Bounds checking
        self._validate_genome_bounds()
        
        self.genetic_mutations += 1
        
        owl_log(f"🧬 [SCUP] Genetic evolution complete - Generation {self.genetic_mutations}", "genetic")

    def _apply_genetic_mutation(self):
        """🧬 Apply random genetic mutations"""
        
        mutation_strength = 0.05
        
        # Random mutations to genome parameters
        mutations = {
            'coherence_threshold': np.random.normal(0, mutation_strength),
            'pressure_sensitivity': np.random.normal(0, mutation_strength),
            'recovery_rate': np.random.normal(0, mutation_strength * 0.5),
            'fragmentation_resistance': np.random.normal(0, mutation_strength),
            'adaptation_speed': np.random.normal(0, mutation_strength * 0.3)
        }
        
        for param, delta in mutations.items():
            if hasattr(self.genome, param):
                current_value = getattr(self.genome, param)
                new_value = current_value + delta
                setattr(self.genome, param, new_value)

    def _validate_genome_bounds(self):
        """Ensure genome parameters stay within valid bounds"""
        
        bounds = {
            'coherence_threshold': (0.1, 0.9),
            'pressure_sensitivity': (0.1, 1.0),
            'recovery_rate': (0.01, 0.5),
            'fragmentation_resistance': (0.1, 1.0),
            'thermal_coupling': (0.1, 1.0),
            'entropy_coupling': (0.1, 1.0),
            'health_coupling': (0.1, 1.0),
            'adaptation_speed': (0.1, 0.8),
            'mutation_rate': (0.01, 0.2),
            'selection_pressure': (0.1, 0.8)
        }
        
        for param, (min_val, max_val) in bounds.items():
            if hasattr(self.genome, param):
                current_value = getattr(self.genome, param)
                clamped_value = max(min_val, min(max_val, current_value))
                setattr(self.genome, param, clamped_value)

    def _emergency_phenotype_adaptation(self, pressure: PressureVector):
        """🧬 Emergency phenotype adaptation during crisis"""
        
        owl_log(f"🚨 [SCUP] Emergency phenotype adaptation - Pressure: {pressure.magnitude:.3f}", "critical")
        
        # Immediate genetic response to crisis
        emergency_adaptations = {}
        
        if pressure.thermal > 0.7:
            # Thermal crisis - increase thermal coupling
            emergency_adaptations['thermal_coupling'] = min(1.0, self.genome.thermal_coupling * 1.2)
            
        if pressure.entropy > 0.7:
            # Entropy crisis - boost resistance
            emergency_adaptations['fragmentation_resistance'] = min(1.0, self.genome.fragmentation_resistance * 1.15)
            
        if pressure.memorial > 0.8:
            # Memorial crisis - increase recovery
            emergency_adaptations['recovery_rate'] = min(0.5, self.genome.recovery_rate * 1.3)
        
        # Apply emergency adaptations
        for param, value in emergency_adaptations.items():
            setattr(self.genome, param, value)
            
        # Record emergency adaptation
        self._record_emergency_adaptation(pressure, emergency_adaptations)

    def _record_genetic_expression(self, tick: int, scup_value: float, pressure: PressureVector):
        """Record genetic expression data"""
        
        # Update SCUP history
        self.scup_history.append(scup_value)
        
        # Determine SCUP state
        scup_state = self._determine_scup_state(scup_value)
        
        # Log SCUP status
        if tick % 25 == 0:  # Log every 25 ticks
            owl_log(
                f"🧬 [SCUP] {scup_state.value} | SCUP: {scup_value:.3f} | "
                f"Pressure: {pressure.magnitude:.3f} | "
                f"Genome Gen: {self.genetic_mutations}",
                "scup"
            )
        
        # Persist to files
        self._persist_scup_data(tick, scup_value, pressure, scup_state)

    def _determine_scup_state(self, scup_value: float) -> SCUPState:
        """Determine SCUP state based on value"""
        
        if scup_value >= 0.8:
            return SCUPState.COHERENT
        elif scup_value >= 0.6:
            return SCUPState.STABLE
        elif scup_value >= 0.4:
            return SCUPState.STRAINED
        elif scup_value >= 0.2:
            return SCUPState.FRAGMENTING
        else:
            return SCUPState.COLLAPSED

    def _persist_scup_data(self, tick: int, scup_value: float, pressure: PressureVector, state: SCUPState):
        """Persist SCUP data to files"""
        
        timestamp = time.time()
        
        # SCUP readings file
        scup_file = "juliet_flowers/cluster_report/scup_readings.json"
        scup_data = {
            'current_scup': scup_value,
            'state': state.name,
            'pressure_magnitude': pressure.magnitude,
            'pressure_components': {
                'thermal': pressure.thermal,
                'entropy': pressure.entropy,
                'temporal': pressure.temporal,
                'memorial': pressure.memorial,
                'emergent': pressure.emergent
            },
            'timestamp': timestamp,
            'tick': tick
        }
        
        try:
            with open(scup_file, 'w') as f:
                json.dump(scup_data, f, indent=2)
        except Exception as e:
            owl_log(f"⚠️ [SCUP] Failed to write SCUP file: {e}", "warning")
        
        # SCUP analytics curve
        analytics_file = "juliet_flowers/cluster_report/scup_analytics/scup_curve.csv"
        try:
            with open(analytics_file, 'a') as f:
                f.write(f"{tick},{scup_value:.4f},{state.name},{pressure.magnitude:.4f}\n")
        except Exception as e:
            owl_log(f"⚠️ [SCUP] Failed to write analytics: {e}", "warning")

    def _record_crossover_event(self, scup_value: float, shi_value: float, health_zone: str):
        """Record genetic crossover event"""
        
        crossover_file = "juliet_flowers/cluster_report/genetic_expression/crossover_events.jsonl"
        
        event_data = {
            'timestamp': time.time(),
            'tick': current_tick(),
            'scup_value': scup_value,
            'shi_value': shi_value,
            'health_zone': health_zone,
            'crossover_strength': self.genome.health_coupling,
            'event_id': self.crossover_events
        }
        
        try:
            with open(crossover_file, 'a') as f:
                f.write(json.dumps(event_data) + '\n')
        except Exception as e:
            owl_log(f"⚠️ [SCUP] Failed to record crossover: {e}", "warning")

    def _record_emergency_adaptation(self, pressure: PressureVector, adaptations: Dict[str, float]):
        """Record emergency phenotype adaptation"""
        
        emergency_file = "juliet_flowers/cluster_report/genetic_expression/emergency_adaptations.jsonl"
        
        adaptation_data = {
            'timestamp': time.time(),
            'tick': current_tick(),
            'pressure_magnitude': pressure.magnitude,
            'pressure_breakdown': {
                'thermal': pressure.thermal,
                'entropy': pressure.entropy,
                'temporal': pressure.temporal,
                'memorial': pressure.memorial,
                'emergent': pressure.emergent
            },
            'adaptations': adaptations,
            'genome_generation': self.genetic_mutations
        }
        
        try:
            with open(emergency_file, 'a') as f:
                f.write(json.dumps(adaptation_data) + '\n')
        except Exception as e:
            owl_log(f"⚠️ [SCUP] Failed to record emergency adaptation: {e}", "warning")

    def get_current_scup(self) -> float:
        """Get current SCUP value"""
        return self.scup_history[-1] if self.scup_history else 0.5

    def get_scup_state(self) -> SCUPState:
        """Get current SCUP state"""
        current_scup = self.get_current_scup()
        return self._determine_scup_state(current_scup)

    def get_genetic_status(self) -> Dict[str, Any]:
        """Get comprehensive genetic status"""
        return {
            'genome': {
                'coherence_threshold': self.genome.coherence_threshold,
                'pressure_sensitivity': self.genome.pressure_sensitivity,
                'recovery_rate': self.genome.recovery_rate,
                'fragmentation_resistance': self.genome.fragmentation_resistance,
                'generation': self.genetic_mutations
            },
            'performance': {
                'computation_cycles': self.computation_cycles,
                'crossover_events': self.crossover_events,
                'current_scup': self.get_current_scup(),
                'current_state': self.get_scup_state().name
            },
            'history_size': {
                'scup_history': len(self.scup_history),
                'pressure_history': len(self.pressure_history)
            }
        }

# ═══════════════════════════════════════════════════════════════════════════════
# 🧬 GENETIC SUPPORTING CLASSES
# ═══════════════════════════════════════════════════════════════════════════════

class PressureIntegrator:
    """Integrates multiple pressure sources"""
    
    def __init__(self):
        self.integration_weights = {
            'thermal': 0.3,
            'entropy': 0.25,
            'temporal': 0.2,
            'memorial': 0.15,
            'emergent': 0.1
        }
    
    def integrate_pressures(self, pressure: PressureVector) -> float:
        """Integrate pressure components into single measure"""
        
        components = {
            'thermal': pressure.thermal,
            'entropy': pressure.entropy,
            'temporal': pressure.temporal,
            'memorial': pressure.memorial,
            'emergent': pressure.emergent
        }
        
        weighted_sum = sum(components[k] * self.integration_weights[k] 
                          for k in components.keys())
        
        return min(1.0, weighted_sum)

class CoherenceStabilizer:
    """Stabilizes coherence during pressure events"""
    
    def __init__(self, genome: SCUPGenome):
        self.genome = genome
        self.stabilization_buffer = deque(maxlen=10)
    
    def stabilize_coherence(self, current_scup: float, pressure: PressureVector) -> float:
        """Apply coherence stabilization"""
        
        self.stabilization_buffer.append(current_scup)
        
        if len(self.stabilization_buffer) < 3:
            return current_scup
        
        # Calculate stabilization based on recent history
        recent_avg = np.mean(self.stabilization_buffer)
        stabilization_strength = self.genome.fragmentation_resistance
        
        # Apply stabilization if under pressure
        if pressure.magnitude > 0.5:
            stabilized = current_scup * (1 - stabilization_strength) + recent_avg * stabilization_strength
            return max(current_scup, stabilized)  # Never make things worse
        
        return current_scup

class HelixSynchronizer:
    """Synchronizes with genetic helix partner"""
    
    def __init__(self):
        self.sync_history = deque(maxlen=100)
        self.last_sync_time = 0
    
    def synchronize_with_partner(self, scup_value: float, partner_value: float) -> Tuple[float, float]:
        """Synchronize genetic expression with helix partner"""
        
        # Calculate synchronization strength
        sync_strength = 0.1
        
        # Bidirectional influence
        scup_adjustment = (partner_value - scup_value) * sync_strength
        partner_adjustment = (scup_value - partner_value) * sync_strength
        
        new_scup = scup_value + scup_adjustment
        new_partner = partner_value + partner_adjustment
        
        self.sync_history.append((new_scup, new_partner))
        self.last_sync_time = time.time()
        
        return new_scup, new_partner

class RecombinationEngine:
    """Handles genetic recombination events"""
    
    def __init__(self, genome: SCUPGenome):
        self.genome = genome
        self.recombination_history = []
    
    def recombine_traits(self, performance_metrics: Dict[str, float]) -> SCUPGenome:
        """Recombine genetic traits based on performance"""
        
        new_genome = SCUPGenome(
            coherence_threshold=self.genome.coherence_threshold,
            pressure_sensitivity=self.genome.pressure_sensitivity,
            recovery_rate=self.genome.recovery_rate,
            fragmentation_resistance=self.genome.fragmentation_resistance
        )
        
        # Performance-based recombination
        if performance_metrics.get('avg_scup', 0) > 0.7:
            # Good performance - small beneficial mutations
            new_genome.coherence_threshold *= 1.01
            new_genome.fragmentation_resistance *= 1.01
        else:
            # Poor performance - larger adaptive changes
            new_genome.recovery_rate *= 1.1
            new_genome.pressure_sensitivity *= 0.95
        
        self.recombination_history.append({
            'timestamp': time.time(),
            'performance': performance_metrics,
            'genome_changes': {
                'coherence_threshold': new_genome.coherence_threshold - self.genome.coherence_threshold,
                'recovery_rate': new_genome.recovery_rate - self.genome.recovery_rate
            }
        })
        
        return new_genome

class EmergencyProtocols:
    """Emergency response protocols for critical states"""
    
    def __init__(self):
        self.emergency_history = []
        self.last_emergency = 0
        self.emergency_cooldown = 30  # seconds
    
    def trigger_emergency_response(self, scup_value: float, pressure: PressureVector) -> Dict[str, Any]:
        """Trigger emergency response protocols"""
        
        current_time = time.time()
        
        if current_time - self.last_emergency < self.emergency_cooldown:
            return {'action': 'cooldown', 'time_remaining': self.emergency_cooldown - (current_time - self.last_emergency)}
        
        emergency_actions = []
        
        # Critical SCUP collapse
        if scup_value < 0.2:
            emergency_actions.append('scup_collapse_protocol')
        
        # Extreme pressure
        if pressure.magnitude > 0.9:
            emergency_actions.append('pressure_relief_protocol')
        
        # Record emergency
        emergency_record = {
            'timestamp': current_time,
            'scup_value': scup_value,
            'pressure_magnitude': pressure.magnitude,
            'actions': emergency_actions
        }
        
        self.emergency_history.append(emergency_record)
        self.last_emergency = current_time
        
        return {'action': 'emergency_response', 'protocols': emergency_actions, 'record': emergency_record}

# ═══════════════════════════════════════════════════════════════════════════════
# 🧬 GLOBAL GENETIC SYSTEM ACCESS
# ═══════════════════════════════════════════════════════════════════════════════

_global_scup_system = None

def get_scup_system() -> SCUPLoop:
    """Get or create global SCUP system instance"""
    global _global_scup_system
    if _global_scup_system is None:
        _global_scup_system = SCUPLoop()
    return _global_scup_system

def initialize_scup_genetics(custom_genome: Optional[SCUPGenome] = None) -> SCUPLoop:
    """Initialize SCUP genetic system with optional custom genome"""
    global _global_scup_system
    _global_scup_system = SCUPLoop(custom_genome)
    return _global_scup_system

def get_current_scup() -> float:
    """Get current SCUP value - legacy compatibility"""
    scup_system = get_scup_system()
    return scup_system.get_current_scup()

# ═══════════════════════════════════════════════════════════════════════════════
# 🧬 GENETIC DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════════════

def run_genetic_diagnostics():
    """Run comprehensive genetic system diagnostics"""
    
    scup_system = get_scup_system()
    
    owl_log("🧬 [SCUP] Running genetic diagnostics...", "genetic")
    
    # Genetic status
    genetic_status = scup_system.get_genetic_status()
    owl_log(f"🧬 [SCUP] Genetic Status: {genetic_status}", "genetic")
    
    # Helix partner connectivity
    if HELIX_PARTNER_AVAILABLE:
        owl_log("🧬 [SCUP] Helix partner (schema_health_index) connected", "genetic")
    else:
        owl_log("⚠️ [SCUP] Helix partner not available - running standalone", "warning")
    
    # Performance metrics
    performance = {
        'computation_cycles': scup_system.computation_cycles,
        'genetic_mutations': scup_system.genetic_mutations,
        'crossover_events': scup_system.crossover_events,
        'current_scup': scup_system.get_current_scup(),
        'scup_state': scup_system.get_scup_state().name
    }
    
    owl_log(f"🧬 [SCUP] Performance Metrics: {performance}", "genetic")
    
    owl_log("✅ [SCUP] Genetic diagnostics complete", "genetic")
    
    return genetic_status

# Auto-initialize on import
if __name__ != "__main__":
    try:
        _global_scup_system = SCUPLoop()
        owl_log("🧬 [SCUP] Genetic helix system initialized", "genetic")
    except Exception as e:
        owl_log(f"❌ [SCUP] Genetic initialization failed: {e}", "error")

# ═══════════════════════════════════════════════════════════════════════════════
# 🧪 GENETIC TESTING
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🧬 DAWN SCUP Genetic Helix System - Test Mode")
    print("═" * 60)
    
    # Initialize system
    scup_system = SCUPLoop()
    
    # Simulate genetic expression
    for i in range(10):
        scup_system._genetic_tick_expression(i * 5)
        time.sleep(0.1)
    
    # Test genetic evolution
    if scup_system._should_evolve():
        scup_system._execute_genetic_evolution()
    
    # Show results
    status = scup_system.get_genetic_status()
    print(f"Final Genetic Status: {status}")
    
    # Run diagnostics
    diagnostics = run_genetic_diagnostics()
    
    print("🧬 Genetic testing complete!")
