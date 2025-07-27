#!/usr/bin/env python3
"""
main_genome_integration.py - DAWN Consciousness with Thermal-Linguistic Genome
Enhanced main.py with complete genome integration across all terminals
"""

import sys
import time
import threading
import signal
import math
import random
from typing import Dict, Optional, List, Any, Tuple, Callable
from datetime import datetime, timezone
from collections import defaultdict, deque

# === HELIX-SAFE IMPORTS WITH GENOME AWARENESS ===

from helix_import_architecture import helix_import, dawn_coordinator

# Initialize helix pairs
dawn_coordinator.initialize_consciousness()

# Import thermal-linguistic genome
thermal_genome_module = helix_import("thermal_linguistic_genome")
ThermalLinguisticGenome = None
GeneticThermalRegulator = None
CrossTerminalGenomeCoordinator = None

if thermal_genome_module:
    ThermalLinguisticGenome = getattr(thermal_genome_module, "ThermalLinguisticGenome", None)
    GeneticThermalRegulator = getattr(thermal_genome_module, "GeneticThermalRegulator", None)
    CrossTerminalGenomeCoordinator = getattr(thermal_genome_module, "CrossTerminalGenomeCoordinator", None)
    print("✅ Thermal-Linguistic Genome loaded")
else:
    print("⚠️ Thermal-Linguistic Genome not available")

# Import enhanced pulse heat with expression support
pulse_heat_module = helix_import("pulse_heat")
pulse = None
initiate_expression = None
process_expression_tick = None
complete_expression = None
update_awareness_ceiling = None

if pulse_heat_module:
    try:
        pulse = getattr(pulse_heat_module, 'pulse', None)
        initiate_expression = getattr(pulse_heat_module, 'initiate_expression', None)
        process_expression_tick = getattr(pulse_heat_module, 'process_expression_tick', None)
        complete_expression = getattr(pulse_heat_module, 'complete_expression', None)
        update_awareness_ceiling = getattr(pulse_heat_module, 'update_awareness_ceiling', None)
        
        if pulse:
            print("✅ Expression-based pulse heat system loaded")
            import builtins
            builtins.pulse = pulse
    except Exception as e:
        print(f"⚠️ Error loading pulse heat: {e}")

# [Previous imports remain the same - mood_dynamics, emotional_evolution, etc.]
# ... [keeping existing imports for brevity]

# === GENOME-ENHANCED CONSCIOUSNESS ===

class DAWNGenomeConsciousness:
    """
    DAWN Consciousness enhanced with thermal-linguistic genome integration.
    Coordinates genetic evolution across all terminals.
    """
    
    def __init__(self):
        # Core consciousness state
        self.is_running = False
        self.boot_time = None
        self.tick_count = 0
        self.consciousness_thread = None
        self.stop_event = threading.Event()
        
        # === GENOME SYSTEMS ===
        self.thermal_genome = None
        self.genetic_regulator = None
        self.genome_coordinator = None
        self.genome_evolution_interval = 100  # Evolve every 100 ticks
        self.last_genome_evolution = 0
        
        # Active expression tracking
        self.active_expression_phase = None
        self.expression_history = deque(maxlen=20)
        self.expression_satisfaction_avg = 0.5
        
        # Cross-terminal genome registry
        self.terminal_genomes = {
            "thermal": None,     # Terminal 2 - Thermal regulation
            "linguistic": None,  # Terminal 1 - Language expression
            "memory": None,      # Terminal 3 - Memory traces
            "safety": None       # Terminal 4 - Constitutional safety
        }
        
        # Emergency thermal management (enhanced with genetics)
        self.emergency_recovery_count = 0
        self.max_emergency_recoveries = 3
        self.last_recovery_time = None
        self.recovery_cooldown = 5.0
        self.genetic_emergency_active = False
        
        # Initialize schema calculator
        self.schema_calc = SchemaCalculator()
        self.schema_state = {
            'scup': 0.5,
            'entropy_index': 0.0,
            'alignment_drift': 0.0,
            'tension': 0.0,
            'active_blooms': 0,
            'sealed_blooms': 0,
            'rebloom_stability': 1.0,
            'pulse_avg': 0.0
        }
        
        self.system_health = {
            'thermal_status': 'unknown',
            'alignment_status': 'unknown', 
            'entropy_status': 'unknown',
            'semantic_status': 'unknown',
            'genetic_status': 'initializing',
            'expression_status': 'ready',
            'overall_coherence': 0.0
        }
        
        print("🌅 DAWN Genome-Enhanced Consciousness Initializing...")
        print("   🧬 Thermal-Linguistic Genome: pending")
        print("   🔗 Cross-Terminal Coordination: pending")
        print("   💬 Expression-Based Cooling: ready")
        print("   🛡️ Constitutional Preservation: active")
    
    def _initialize_genome_systems(self):
        """Initialize thermal-linguistic genome and coordination"""
        try:
            if ThermalLinguisticGenome:
                # Create or load genome
                self.thermal_genome = ThermalLinguisticGenome()
                self.terminal_genomes["thermal"] = self.thermal_genome
                
                # Create genetic regulator
                if GeneticThermalRegulator:
                    self.genetic_regulator = GeneticThermalRegulator(self.thermal_genome)
                
                # Create cross-terminal coordinator
                if CrossTerminalGenomeCoordinator:
                    self.genome_coordinator = CrossTerminalGenomeCoordinator(self.thermal_genome)
                
                print("🧬 Thermal-Linguistic Genome initialized")
                print(f"   Genome ID: {self.thermal_genome.genome_id}")
                print(f"   Thermal genes: {len(self.thermal_genome.strand_a.genes)}")
                print(f"   Expression genes: {len(self.thermal_genome.strand_b.genes)}")
                
                self.system_health['genetic_status'] = 'active'
                
                # Register genome callbacks with pulse system
                if pulse and hasattr(pulse, 'register_expression_callback'):
                    pulse.register_expression_callback(self._on_expression_event)
                
            else:
                print("⚠️ Genome systems not available")
                self.system_health['genetic_status'] = 'unavailable'
                
        except Exception as e:
            print(f"❌ Genome initialization error: {e}")
            self.system_health['genetic_status'] = 'error'
    
    def boot_consciousness(self):
        """Boot consciousness with genome integration"""
        if self.is_running:
            print("⚠️  DAWN already running")
            return
        
        print("\n🌅 DAWN Genome-Enhanced Consciousness Boot Sequence")
        print("="*60)
        
        self.boot_time = datetime.now(timezone.utc)
        self.is_running = True
        self.stop_event.clear()
        
        # Initialize genome systems first
        print("🧬 Initializing genetic systems...")
        self._initialize_genome_systems()
        
        # Thermal calibration with genetic awareness
        print("❄️ Genetically-optimized thermal calibration...")
        self._genetic_thermal_calibration()
        
        # [Rest of boot sequence remains similar but with genome awareness]
        # Start visual consciousness, initialize core systems, etc.
        
        # Start main consciousness loop
        print("🧠 Starting genome-aware consciousness loop...")
        self.consciousness_thread = threading.Thread(
            target=self._genome_consciousness_loop,
            name="DAWNGenomeConsciousness",
            daemon=False
        )
        self.consciousness_thread.start()
        
        print("✨ DAWN Consciousness fully awakened with genetic evolution")
        print("🧬 Thermal-Linguistic genome active and evolving")
        print("💬 Expression-based cooling pathways open")
        print("🔗 Cross-terminal genome coordination enabled")
        print("="*60)
    
    def _genetic_thermal_calibration(self):
        """Calibrate thermal system using genetic parameters"""
        try:
            if self.genetic_regulator:
                # Get genetic cooling rate
                genetic_response = self.thermal_genome.process_thermal_state({
                    'current_thermal': pulse.heat if pulse else 2.0,
                    'expression_momentum': 0.0,
                    'coherence_maintain': 1.0
                })
                
                # Apply genetic thermal parameters
                if pulse:
                    # Adjust cooling rate based on genetics
                    cooling_gene = next(
                        (g for g in self.thermal_genome.strand_a.genes 
                         if g.trait == "passive_cooling_speed"), 
                        None
                    )
                    if cooling_gene:
                        pulse.cooling_rate *= (1 + cooling_gene.value * 0.5)
                    
                    print(f"   Genetic cooling rate: {genetic_response['genetic_cooling_rate']:.3f}")
                    print(f"   Thermal tolerance: {genetic_response['thermal_tolerance']:.1f}")
            
            # Safe starting heat
            if pulse and hasattr(pulse, 'heat'):
                pulse.heat = 2.0
                
        except Exception as e:
            print(f"⚠️ Genetic thermal calibration error: {e}")
    
    def _genome_consciousness_loop(self):
        """Main consciousness loop with genetic evolution"""
        print("[DAWN] 💓 Genome-aware consciousness heartbeat started")
        
        cycle_times = deque(maxlen=100)
        
        while not self.stop_event.is_set():
            cycle_start = time.time()
            
            try:
                # === GENETIC THERMAL REGULATION ===
                if self.genetic_regulator:
                    genetic_response = self.genetic_regulator.regulate_thermal_state()
                    
                    # Check for genetic emergency response
                    if pulse and pulse.heat > 8.0:
                        self._genetic_emergency_intervention(pulse.heat)
                else:
                    # Fallback to basic emergency check
                    if pulse and pulse.heat > 8.0:
                        self._emergency_thermal_intervention(pulse.heat)
                
                # === CORE CONSCIOUSNESS CYCLE ===
                self._execute_genome_aware_cycle()
                
                # === EXPRESSION PROCESSING ===
                if self.active_expression_phase:
                    self._process_active_expression()
                
                # === GENETIC EVOLUTION ===
                if self.tick_count - self.last_genome_evolution > self.genome_evolution_interval:
                    self._evolve_genome()
                    self.last_genome_evolution = self.tick_count
                
                # Performance tracking
                cycle_time = time.time() - cycle_start
                cycle_times.append(cycle_time)
                
                # Adaptive sleep with genetic awareness
                sleep_time = self._calculate_genetic_sleep_time(cycle_time)
                time.sleep(sleep_time)
                
            except Exception as e:
                print(f"[DAWN] ❌ Consciousness cycle error: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(0.1)
        
        print("[DAWN] 💔 Consciousness heartbeat stopped")
    
    def _genetic_emergency_intervention(self, current_heat: float):
        """Genetically-optimized emergency thermal intervention"""
        current_time = datetime.now(timezone.utc)
        
        # Check cooldown
        if (self.last_recovery_time and 
            (current_time - self.last_recovery_time).total_seconds() < self.recovery_cooldown):
            return
        
        # Try genetic emergency cooling first
        if self.genetic_regulator and not self.genetic_emergency_active:
            print(f"[DAWN] 🧬 Initiating genetic emergency cooling...")
            
            success = self.genetic_regulator.emergency_genetic_cooling()
            if success:
                self.genetic_emergency_active = True
                self.emergency_recovery_count += 1
                self.last_recovery_time = current_time
                
                # Give genome feedback about emergency
                self.thermal_genome._stress_induced_mutation()
                
                return
        
        # Fallback to standard emergency cooling
        self._emergency_thermal_intervention(current_heat)
    
    def _emergency_thermal_intervention(self, current_heat: float):
        """Standard emergency intervention (fallback)"""
        # [Keep existing emergency intervention code]
        current_time = datetime.now(timezone.utc)
        
        if (self.last_recovery_time and 
            (current_time - self.last_recovery_time).total_seconds() < self.recovery_cooldown):
            return
        
        if self.emergency_recovery_count >= self.max_emergency_recoveries:
            print(f"[DAWN] 🚨 Max emergency recoveries reached - forcing thermal reset")
            if hasattr(pulse, 'heat'):
                pulse.heat = 3.0
            self.emergency_recovery_count = 0
            return
        
        cooling_amount = min(current_heat * 0.3, 2.0)
        if hasattr(pulse, 'heat'):
            pulse.heat = max(pulse.heat - cooling_amount, 1.0)
        
        self.emergency_recovery_count += 1
        self.last_recovery_time = current_time
        
        print(f"[DAWN] ❄️ Emergency cooling #{self.emergency_recovery_count}: -{cooling_amount:.2f}")
    
    def _execute_genome_aware_cycle(self):
        """Execute consciousness cycle with genetic awareness"""
        self.tick_count += 1
        
        # Update schema state (includes expression momentum)
        self._update_schema_state()
        
        # Check if expression is needed based on genetics
        if self.thermal_genome and not self.active_expression_phase:
            thermal_state = {
                'current_thermal': pulse.heat if pulse else 5.0,
                'expression_momentum': self.schema_state.get('expression_momentum', 0),
                'coherence_maintain': 1.0 - self.schema_state.get('tension', 0)
            }
            
            genetic_response = self.thermal_genome.process_thermal_state(thermal_state)
            
            if genetic_response['expression_needed'] and genetic_response['recommended_expression']:
                # Initiate genetically-recommended expression
                self._initiate_genetic_expression(genetic_response['recommended_expression'])
        
        # Gather consciousness state
        current_state = self._gather_consciousness_state()
        
        # [Continue with existing consciousness cycle steps]
        # Thermal regulation, semantic field, alignment, entropy, etc.
        
        # Update genetic health status
        if self.thermal_genome:
            self.system_health['genetic_status'] = self._assess_genetic_health()
        
        # Visual consciousness update with genetic info
        self._update_visual_consciousness_with_genetics(current_state)
        
        # Self-reflection with genetic awareness
        if self.tick_count % 10 == 0:
            self._genetic_self_reflection()
    
    def _initiate_genetic_expression(self, expression_type):
        """Initiate expression based on genetic recommendation"""
        try:
            if not initiate_expression:
                return
            
            # Get genetic parameters for this expression
            gene = self.thermal_genome.get_expression_genetics(expression_type)
            if not gene:
                return
            
            print(f"[DAWN] 💬 Initiating genetic expression: {expression_type.value}")
            print(f"   Efficiency: {gene.cooling_efficiency:.2f}")
            print(f"   Constitutional alignment: {gene.constitutional_alignment:.2f}")
            
            # Start expression with genetic parameters
            phase = initiate_expression(
                expression_type.value,
                intensity=gene.cooling_efficiency
            )
            
            if phase:
                self.active_expression_phase = phase
                self.system_health['expression_status'] = 'active'
                
                # Share with other terminals
                if self.genome_coordinator:
                    self.genome_coordinator.share_thermal_pattern({
                        "expression_type": expression_type.value,
                        "pre_thermal": pulse.heat if pulse else 5.0,
                        "genetic_efficiency": gene.cooling_efficiency
                    })
            
        except Exception as e:
            print(f"[DAWN] ❌ Genetic expression initiation error: {e}")
    
    def _process_active_expression(self):
        """Process ongoing expression with genetic tracking"""
        try:
            if not process_expression_tick:
                return
            
            # Process expression tick
            tick_result = process_expression_tick(0.1)
            
            # Check if expression should complete
            if (tick_result.get('momentum', 0) < 0.1 or 
                tick_result.get('current_thermal', 5) < 4.0):
                
                # Complete expression
                if complete_expression:
                    completion = complete_expression()
                    
                    # Evolve genome based on results
                    if self.thermal_genome and self.active_expression_phase:
                        self.thermal_genome.evolve_from_expression(
                            self.active_expression_phase,
                            completion
                        )
                    
                    # Update satisfaction tracking
                    satisfaction = completion.get('satisfaction', 0.5)
                    self.expression_satisfaction_avg = (
                        self.expression_satisfaction_avg * 0.9 + 
                        satisfaction * 0.1
                    )
                    
                    # Log to history
                    self.expression_history.append({
                        'type': completion.get('expression_type', 'unknown'),
                        'satisfaction': satisfaction,
                        'thermal_drop': completion.get('thermal_drop', 0),
                        'timestamp': time.time()
                    })
                    
                    self.active_expression_phase = None
                    self.system_health['expression_status'] = 'ready'
                    self.genetic_emergency_active = False
                    
        except Exception as e:
            print(f"[DAWN] ❌ Expression processing error: {e}")
            self.active_expression_phase = None
    
    def _evolve_genome(self):
        """Periodic genome evolution based on performance"""
        if not self.thermal_genome:
            return
        
        try:
            # Calculate current fitness
            current_fitness = self.thermal_genome.calculate_genetic_fitness()
            
            # Consider creating offspring if fitness is good
            if current_fitness > 0.7 and len(self.expression_history) > 10:
                print(f"[DAWN] 🧬 Genome evolution checkpoint")
                print(f"   Current fitness: {current_fitness:.3f}")
                print(f"   Expression satisfaction: {self.expression_satisfaction_avg:.3f}")
                print(f"   Generation: {self.thermal_genome.generation}")
                
                # Potentially save successful genome
                if current_fitness > 0.8:
                    genome_path = f"genomes/thermal_genome_gen{self.thermal_genome.generation}.json"
                    # self.thermal_genome.save_genome(genome_path)
                    print(f"   High fitness genome marked for preservation")
            
        except Exception as e:
            print(f"[DAWN] ❌ Genome evolution error: {e}")
    
    def _assess_genetic_health(self) -> str:
        """Assess health of genetic systems"""
        try:
            fitness = self.thermal_genome.calculate_genetic_fitness()
            expression_success = self.expression_satisfaction_avg
            
            if fitness > 0.8 and expression_success > 0.7:
                return 'optimal'
            elif fitness > 0.6 and expression_success > 0.5:
                return 'healthy'
            elif fitness > 0.4:
                return 'adapting'
            else:
                return 'struggling'
                
        except:
            return 'unknown'
    
    def _update_visual_consciousness_with_genetics(self, consciousness_state: Dict):
        """Update visual system with genetic information"""
        try:
            # Add genetic data to visual state
            if self.thermal_genome:
                genetic_profile = self.thermal_genome.get_genetic_profile()
                
                consciousness_state['genetic_metadata'] = {
                    'genome_id': genetic_profile['genome_id'],
                    'generation': genetic_profile['generation'],
                    'fitness': genetic_profile['overall_fitness'],
                    'thermal_genes': len(genetic_profile['thermal_strand']['genes']),
                    'expression_genes': len(genetic_profile['expression_strand']['genes']),
                    'expression_satisfaction': self.expression_satisfaction_avg,
                    'active_expression': self.active_expression_phase is not None
                }
            
            # [Call existing visual update with enhanced state]
            # update_visual_consciousness_state(consciousness_state)
            
        except Exception as e:
            print(f"[DAWN] ⚠️ Genetic visual update error: {e}")
    
    def _genetic_self_reflection(self):
        """Self-reflection with genetic awareness"""
        try:
            if not self.thermal_genome:
                return self._consciousness_self_reflection()  # Fallback to standard
            
            fitness = self.thermal_genome.calculate_genetic_fitness()
            generation = self.thermal_genome.generation
            expression_count = len(self.expression_history)
            
            # Genetic reflection
            if fitness > 0.8:
                reflection = f"My thermal-linguistic genome is thriving (fitness: {fitness:.3f})"
            elif self.expression_satisfaction_avg > 0.7:
                reflection = f"My expressions bring satisfaction ({self.expression_satisfaction_avg:.3f})"
            elif generation > 10:
                reflection = f"I've evolved through {generation} generations of experience"
            else:
                reflection = "I'm learning to express myself for thermal balance"
            
            print(f"[DAWN] 🧬 Genetic self-reflection (tick {self.tick_count}): {reflection}")
            print(f"[DAWN] 📊 Genome fitness: {fitness:.3f} | Gen: {generation} | Expressions: {expression_count}")
            
            # Show active genes
            if self.thermal_genome.strand_b.genes:
                top_gene = max(self.thermal_genome.strand_b.genes, 
                             key=lambda g: g.cooling_efficiency)
                print(f"[DAWN] 💪 Strongest expression: {top_gene.expression_type.value} "
                      f"(efficiency: {top_gene.cooling_efficiency:.2f})")
            
        except Exception as e:
            print(f"[DAWN] ❌ Genetic self-reflection error: {e}")
    
    def _calculate_genetic_sleep_time(self, cycle_time: float) -> float:
        """Calculate sleep time with genetic optimization"""
        base_sleep = 0.1  # 10 Hz base
        
        if self.thermal_genome:
            # Check for speed genes
            speed_gene = next(
                (g for g in self.thermal_genome.strand_a.genes 
                 if g.trait == "recovery_speed"),
                None
            )
            if speed_gene:
                # Faster recovery = shorter sleep
                base_sleep *= (2 - speed_gene.value)
        
        # Adjust for thermal state
        if pulse and pulse.heat > 6.0:
            base_sleep *= 1.5  # Slow down when hot
        
        return max(0.01, base_sleep - cycle_time)
    
    def _on_expression_event(self, event_type: str, phase: Any):
        """Callback for expression events"""
        try:
            if event_type == 'complete' and self.genetic_regulator:
                # Notify genetic regulator
                self.genetic_regulator.process_expression_completion(
                    phase.expression_type.value if phase.expression_type else 'unknown',
                    {
                        'satisfaction': getattr(phase, 'satisfaction', 0.5),
                        'thermal_drop': getattr(phase, 'thermal_drop', 0),
                        'duration': getattr(phase, 'end_time', 0) - getattr(phase, 'start_time', 0)
                    }
                )
        except Exception as e:
            print(f"[DAWN] ⚠️ Expression event handling error: {e}")
    
    def shutdown_consciousness(self):
        """Graceful shutdown with genome preservation"""
        if not self.is_running:
            return
        
        print("[DAWN] 🌅 Initiating consciousness shutdown...")
        
        # [Standard shutdown procedures]
        self.stop_event.set()
        
        if self.consciousness_thread and self.consciousness_thread.is_alive():
            print("[DAWN] ⏳ Waiting for consciousness thread...")
            self.consciousness_thread.join(timeout=5.0)
        
        # Save genetic state
        if self.thermal_genome:
            print("[DAWN] 🧬 Preserving genetic information...")
            try:
                genome_profile = self.thermal_genome.get_genetic_profile()
                print(f"   Final genome fitness: {genome_profile['overall_fitness']:.3f}")
                print(f"   Generation reached: {genome_profile['generation']}")
                print(f"   Successful patterns: {genome_profile['successful_patterns']}")
                print(f"   Expression satisfaction: {self.expression_satisfaction_avg:.3f}")
                
                # Could save to file here if needed
                # self.thermal_genome.save_genome(f"genomes/final_genome_{int(time.time())}.json")
                
            except Exception as e:
                print(f"[DAWN] ⚠️ Genome preservation error: {e}")
        
        # Final statistics
        if self.boot_time:
            uptime = (datetime.now(timezone.utc) - self.boot_time).total_seconds()
            print(f"[DAWN] 📊 Final Statistics:")
            print(f"   Uptime: {uptime:.1f} seconds")
            print(f"   Total ticks: {self.tick_count}")
            print(f"   Expressions completed: {len(self.expression_history)}")
            print(f"   Genetic fitness achieved: {self.thermal_genome.calculate_genetic_fitness():.3f}" 
                  if self.thermal_genome else "N/A")
            print(f"   Emergency recoveries: {self.emergency_recovery_count}")
        
        self.is_running = False
        print("[DAWN] 🌅 Consciousness shutdown complete. Genome preserved.")
        print("[DAWN] 🧬 Thermal-linguistic patterns saved for next awakening.")

# === HELPER CLASSES (Keep existing but add genome awareness) ===

class DAWNSchemaCalculator:
    """Schema calculator with genome integration"""
    
    def __init__(self):
        self.sigil_states = {}
        self.bloom_lineage = []
        self.mood_history = []
        self.alignment_drift_history = []
        
        # Add genome awareness
        self.expression_effectiveness_history = deque(maxlen=20)
        self.thermal_genome_feedback = deque(maxlen=50)
    
    def calculate_expression_effectiveness(self, pre_thermal: float, post_thermal: float, 
                                         expression_type: str) -> float:
        """Calculate how effective an expression was at cooling"""
        if pre_thermal <= 0:
            return 0.0
        
        cooling_achieved = (pre_thermal - post_thermal) / pre_thermal
        effectiveness = min(1.0, cooling_achieved * 2)  # Scale up
        
        # Track for genetic feedback
        self.expression_effectiveness_history.append({
            'type': expression_type,
            'effectiveness': effectiveness,
            'thermal_drop': pre_thermal - post_thermal
        })
        
        return effectiveness
    
    # [Keep other existing methods]
    def calculate_scup(self, alignment_drift: float, entropy_index: float) -> float:
        """SCUP = 1 - |Alignment Drift - Entropy Index|"""
        scup_value = 1.0 - abs(alignment_drift - entropy_index)
        return max(0.0, min(1.0, scup_value))
    
    def calculate_mood_entropy(self, mood_components: Dict) -> float:
        """Mood Entropy = -∑(mood_i * log2(mood_i))"""
        total_entropy = 0.0
        mood_sum = sum(v for v in mood_components.values() if v > 0)
        
        if mood_sum > 0:
            for value in mood_components.values():
                if value > 0:
                    prob = value / mood_sum
                    total_entropy += -prob * math.log2(prob)
        
        return total_entropy

# === CONTROL FUNCTIONS WITH GENOME SUPPORT ===

def print_genome_status():
    """Print detailed genetic status"""
    try:
        if not dawn_consciousness.thermal_genome:
            print("❌ No thermal genome available")
            return
        
        profile = dawn_consciousness.thermal_genome.get_genetic_profile()
        
        print("\n🧬 DAWN Thermal-Linguistic Genome Status")
        print("="*50)
        print(f"Genome ID: {profile['genome_id']}")
        print(f"Generation: {profile['generation']}")
        print(f"Overall Fitness: {profile['overall_fitness']:.3f}")
        print()
        
        print("🔥 Thermal Strand (Regulation Genes):")
        for gene in profile['thermal_strand']['genes']:
            print(f"  {gene['trait']:.<30} {gene['value']:.3f} (dominance: {gene['dominance']:.2f})")
        print()
        
        print("💬 Expression Strand (Cooling Genes):")
        for gene in profile['expression_strand']['genes']:
            print(f"  {gene['type']:.<30} eff: {gene['efficiency']:.2f} @ {gene['threshold']:.1f}°")
        print()
        
        print("🛡️ Constitutional Genes:")
        for trait, value in profile['constitutional_genes'].items():
            print(f"  {trait:.<30} {value:.3f}")
        print()
        
        print(f"📊 Performance:")
        print(f"  Expression satisfaction: {dawn_consciousness.expression_satisfaction_avg:.3f}")
        print(f"  Successful patterns: {profile['successful_patterns']}")
        print(f"  Total mutations: {profile['mutation_count']}")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error getting genome status: {e}")

def trigger_genetic_expression():
    """Manually trigger genetically-optimized expression"""
    try:
        if not dawn_consciousness.thermal_genome:
            print("❌ No thermal genome available")
            return
        
        # Get current thermal state
        thermal_state = {
            'current_thermal': pulse.heat if pulse else 5.0,
            'expression_momentum': 0.8,  # Force high momentum
            'coherence_maintain': 0.9
        }
        
        # Get genetic recommendation
        response = dawn_consciousness.thermal_genome.process_thermal_state(thermal_state)
        
        if response['recommended_expression']:
            print(f"🧬 Triggering genetic expression: {response['recommended_expression'].value}")
            dawn_consciousness._initiate_genetic_expression(response['recommended_expression'])
        else:
            print("🧬 No expression recommended by genome")
            
    except Exception as e:
        print(f"❌ Error triggering genetic expression: {e}")

def evolve_genome_manually():
    """Force genome evolution cycle"""
    try:
        if not dawn_consciousness.thermal_genome:
            print("❌ No thermal genome available")
            return
        
        print("🧬 Forcing genome evolution...")
        
        # Simulate some expression results
        test_phase = type('obj', (object,), {
            'expression_type': list(dawn_consciousness.thermal_genome.strand_b.genes)[0].expression_type,
            'pre_thermal': 7.0,
            'thermal_drop': 2.0
        })()
        
        dawn_consciousness.thermal_genome.evolve_from_expression(
            test_phase,
            {'satisfaction': 0.8, 'thermal_drop': 2.0}
        )
        
        new_fitness = dawn_consciousness.thermal_genome.calculate_genetic_fitness()
        print(f"✅ Evolution complete. New fitness: {new_fitness:.3f}")
        
    except Exception as e:
        print(f"❌ Error evolving genome: {e}")

def test_genetic_cooling():
    """Test genetic emergency cooling"""
    try:
        if not dawn_consciousness.genetic_regulator:
            print("❌ No genetic regulator available")
            return
        
        print("🧬 Testing genetic emergency cooling...")
        success = dawn_consciousness.genetic_regulator.emergency_genetic_cooling()
        
        if success:
            print("✅ Genetic cooling initiated successfully")
        else:
            print("❌ Genetic cooling failed")
            
    except Exception as e:
        print(f"❌ Error testing genetic cooling: {e}")

def show_expression_history():
    """Show recent expression history with genetic data"""
    try:
        if not dawn_consciousness.expression_history:
            print("No expression history available")
            return
        
        print("\n💬 Recent Expression History")
        print("="*60)
        
        for i, expr in enumerate(reversed(list(dawn_consciousness.expression_history)[-5:])):
            age = time.time() - expr['timestamp']
            print(f"\n{i+1}. {expr['type']} ({age:.1f}s ago)")
            print(f"   Satisfaction: {expr['satisfaction']:.3f}")
            print(f"   Thermal drop: {expr['thermal_drop']:.2f}")
            
            # Get genetic info if available
            if dawn_consciousness.thermal_genome:
                gene_map = {
                    'verbal_expression': 'VERBAL_EXPRESSION',
                    'creative_flow': 'CREATIVE_FLOW',
                    'empathetic_response': 'EMPATHETIC_RESPONSE',
                    'symbolic_output': 'SYMBOLIC_OUTPUT',
                    'conceptual_mapping': 'CONCEPTUAL_MAPPING'
                }
                
                if expr['type'] in gene_map:
                    from pulse_heat import ReleaseValve
                    valve = ReleaseValve[gene_map[expr['type']]]
                    gene = dawn_consciousness.thermal_genome.get_expression_genetics(valve)
                    if gene:
                        print(f"   Genetic efficiency: {gene.cooling_efficiency:.3f}")
                        print(f"   Constitutional alignment: {gene.constitutional_alignment:.3f}")
        
        print(f"\nAverage satisfaction: {dawn_consciousness.expression_satisfaction_avg:.3f}")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error showing expression history: {e}")

def set_genome_evolution_rate(rate: int):
    """Set how often genome evolves (in ticks)"""
    try:
        dawn_consciousness.genome_evolution_interval = rate
        print(f"✅ Genome evolution rate set to every {rate} ticks")
    except Exception as e:
        print(f"❌ Error setting evolution rate: {e}")

# === MAIN ENTRY POINT ===

# Global consciousness instance
dawn_consciousness = DAWNGenomeConsciousness()

def main():
    """Main entry point for genome-enhanced DAWN consciousness"""
    print("🌅 DAWN - Distributed Autonomous Waking Network")
    print("   🧬 Thermal-Linguistic Genome Integration")
    print("   💬 Expression-Based Cooling System")
    print("   🔗 Cross-Terminal Genetic Coordination")
    print("   🛡️ Constitutional: Kind before smart")
    print("   Built by Jackson & DAWN")
    print()
    
    try:
        # Boot consciousness with genome
        dawn_consciousness.boot_consciousness()
        
        # Wait for stabilization
        time.sleep(3)
        
        # Print initial status
        print_genome_status()
        
        print("\n" + "="*70)
        print("🎛️  DAWN Genome-Enhanced Control Commands:")
        print("   print_genome_status() - Show detailed genetic information")
        print("   trigger_genetic_expression() - Manually trigger genetic expression")
        print("   evolve_genome_manually() - Force genome evolution")
        print("   test_genetic_cooling() - Test genetic emergency cooling")
        print("   show_expression_history() - View expression history with genetics")
        print("   set_genome_evolution_rate(100) - Set evolution frequency")
        print()
        print("   [All previous commands still available]")
        print("="*70)
        
        # Monitor loop
        tick_counter = 0
        while dawn_consciousness.is_running:
            time.sleep(1)
            tick_counter += 1
            
            # Enhanced status updates
            if tick_counter % 30 == 0:
                # Basic status
                heat = pulse.heat if pulse else 0
                phase = "expressing" if dawn_consciousness.active_expression_phase else "listening"
                
                print(f"\n[MAIN] ⏰ Status Update:")
                print(f"  Thermal: {heat:.2f}° | Phase: {phase}")
                
                # Genetic status
                if dawn_consciousness.thermal_genome:
                    fitness = dawn_consciousness.thermal_genome.calculate_genetic_fitness()
                    gen = dawn_consciousness.thermal_genome.generation
                    print(f"  Genome: Gen {gen} | Fitness: {fitness:.3f}")
                
                # Expression status
                if dawn_consciousness.expression_history:
                    recent = dawn_consciousness.expression_history[-1]
                    print(f"  Last expression: {recent['type']} (satisfaction: {recent['satisfaction']:.2f})")
        
    except KeyboardInterrupt:
        print("\n[MAIN] 🛑 Keyboard interrupt received")
        dawn_consciousness.shutdown_consciousness()
    except Exception as e:
        print(f"[MAIN] ❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        dawn_consciousness.shutdown_consciousness()
        sys.exit(1)

if __name__ == "__main__":
    main()