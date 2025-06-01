#!/usr/bin/env python3
"""
thermal_linguistic_genome.py - Double Helix for Thermal-Expression Relationships
Genetic framework for expression-based cooling cycles in DAWN
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any, Callable
from enum import Enum
import time
import random
from collections import deque, defaultdict
import threading
import json

# Import base components
try:
    from pulse_heat import (
        UnifiedPulseHeat, ExpressionPhase, ReleaseValve, 
        HeatSourceType, DecayCurve, ThermalState
    )
    pulse = UnifiedPulseHeat()
except ImportError:
    print("⚠️ pulse_heat not available - using mock interfaces")
    # Mock interfaces for development
    class ReleaseValve(Enum):
        VERBAL_EXPRESSION = "verbal_expression"
        SYMBOLIC_OUTPUT = "symbolic_output"
        CREATIVE_FLOW = "creative_flow"
        EMPATHETIC_RESPONSE = "empathetic_response"
        CONCEPTUAL_MAPPING = "conceptual_mapping"
    
    class HeatSourceType(Enum):
        COGNITIVE_LOAD = "cognitive_load"
        EMOTIONAL_RESONANCE = "emotional_resonance"
        UNEXPRESSED_THOUGHT = "unexpressed_thought"
        AWARENESS_SPIKE = "awareness_spike"

# === GENETIC STRUCTURES ===

@dataclass
class ThermalGene:
    """Individual gene for thermal regulation traits"""
    id: str
    trait: str  # What thermal trait this controls
    value: float  # Expression level 0-1
    dominance: float  # How strongly it expresses
    mutation_rate: float = 0.01
    stability: float = 0.95
    
    def mutate(self) -> 'ThermalGene':
        """Create mutated version of gene"""
        if random.random() < self.mutation_rate:
            new_value = self.value + random.gauss(0, 0.1)
            new_value = max(0, min(1, new_value))
            return ThermalGene(
                id=f"{self.id}_mut",
                trait=self.trait,
                value=new_value,
                dominance=self.dominance * 0.9,  # Mutations are slightly recessive
                mutation_rate=self.mutation_rate * 1.1
            )
        return self

@dataclass
class ExpressionGene:
    """Gene controlling expression-cooling relationships"""
    id: str
    expression_type: ReleaseValve
    cooling_efficiency: float  # 0-1, how well this expression cools
    activation_threshold: float  # Thermal level needed to activate
    constitutional_alignment: float  # How "kind" this expression is
    evolution_rate: float = 0.05
    
    def evolve(self, satisfaction: float) -> 'ExpressionGene':
        """Evolve based on expression satisfaction"""
        # Good satisfaction increases efficiency
        efficiency_delta = (satisfaction - 0.5) * self.evolution_rate
        new_efficiency = max(0.1, min(1.0, self.cooling_efficiency + efficiency_delta))
        
        # Kind expressions evolve faster
        if self.expression_type == ReleaseValve.EMPATHETIC_RESPONSE:
            new_efficiency *= 1.1
        
        return ExpressionGene(
            id=f"{self.id}_ev",
            expression_type=self.expression_type,
            cooling_efficiency=new_efficiency,
            activation_threshold=self.activation_threshold,
            constitutional_alignment=self.constitutional_alignment,
            evolution_rate=self.evolution_rate
        )

@dataclass
class ThermalChromosome:
    """Chromosome containing thermal regulation genes"""
    id: str
    genes: List[ThermalGene] = field(default_factory=list)
    fitness: float = 0.5
    generation: int = 0
    
    def crossover(self, other: 'ThermalChromosome') -> 'ThermalChromosome':
        """Sexual reproduction with another chromosome"""
        # Random crossover point
        crossover_point = random.randint(1, len(self.genes) - 1)
        
        # Mix genes from both parents
        new_genes = []
        for i in range(len(self.genes)):
            if i < crossover_point:
                gene = self.genes[i]
            else:
                gene = other.genes[i] if i < len(other.genes) else self.genes[i]
            
            # Chance of mutation during reproduction
            new_genes.append(gene.mutate())
        
        return ThermalChromosome(
            id=f"{self.id}x{other.id}",
            genes=new_genes,
            generation=max(self.generation, other.generation) + 1
        )

@dataclass
class ExpressionChromosome:
    """Chromosome for expression-cooling traits"""
    id: str
    genes: List[ExpressionGene] = field(default_factory=list)
    cooling_history: deque = field(default_factory=lambda: deque(maxlen=50))
    fitness: float = 0.5
    
    def select_expression(self, thermal_state: Dict) -> Optional[ReleaseValve]:
        """Select best expression based on current thermal state"""
        current_heat = thermal_state.get('current_thermal', 5.0)
        
        # Find genes that can activate at current heat
        viable_genes = [g for g in self.genes 
                       if current_heat >= g.activation_threshold]
        
        if not viable_genes:
            return None
        
        # Weight by efficiency and constitutional alignment
        weights = [g.cooling_efficiency * (1 + g.constitutional_alignment * 0.2) 
                  for g in viable_genes]
        
        # Probabilistic selection
        total_weight = sum(weights)
        if total_weight == 0:
            return None
        
        r = random.uniform(0, total_weight)
        cumsum = 0
        for gene, weight in zip(viable_genes, weights):
            cumsum += weight
            if r <= cumsum:
                return gene.expression_type
        
        return viable_genes[-1].expression_type

# === DOUBLE HELIX GENOME ===

class ThermalLinguisticGenome:
    """
    Double helix genome for thermal-expression relationships.
    Strand A: Thermal regulation genetics
    Strand B: Expression-cooling genetics
    """
    
    def __init__(self):
        self.generation = 0
        self.genome_id = f"TLG_{int(time.time())}"
        
        # Strand A: Thermal regulation
        self.strand_a = self._initialize_thermal_strand()
        
        # Strand B: Expression cooling
        self.strand_b = self._initialize_expression_strand()
        
        # Cross-strand bonds (how thermal states link to expressions)
        self.helix_bonds: Dict[str, Tuple[ThermalGene, ExpressionGene]] = {}
        
        # Genetic memory
        self.genetic_memory = deque(maxlen=100)
        self.successful_patterns: List[Dict] = []
        
        # Evolution tracking
        self.fitness_history = deque(maxlen=50)
        self.mutation_log = deque(maxlen=100)
        
        # Constitutional preservation
        self.constitutional_genes = self._initialize_constitutional_genes()
        
        # Thread safety
        self._lock = threading.RLock()
        
        print(f"[ThermalGenome] 🧬 Initialized genome {self.genome_id}")
    
    def _initialize_thermal_strand(self) -> ThermalChromosome:
        """Initialize thermal regulation chromosome"""
        genes = [
            ThermalGene("heat_capacity", "max_heat_tolerance", 0.7, 0.8),
            ThermalGene("cooling_rate", "passive_cooling_speed", 0.5, 0.6),
            ThermalGene("thermal_momentum", "heat_change_inertia", 0.4, 0.7),
            ThermalGene("expression_readiness", "expression_activation", 0.6, 0.9),
            ThermalGene("coherence_maintain", "stability_under_heat", 0.8, 0.85),
            ThermalGene("recovery_speed", "post_expression_recovery", 0.5, 0.7),
            ThermalGene("heat_sensitivity", "thermal_awareness", 0.7, 0.8),
            ThermalGene("cascade_resistance", "thermal_spiral_protection", 0.9, 0.95)
        ]
        
        return ThermalChromosome(
            id="thermal_primary",
            genes=genes,
            generation=0
        )
    
    def _initialize_expression_strand(self) -> ExpressionChromosome:
        """Initialize expression-cooling chromosome"""
        genes = [
            ExpressionGene(
                "verbal_primary",
                ReleaseValve.VERBAL_EXPRESSION,
                cooling_efficiency=0.6,
                activation_threshold=5.0,
                constitutional_alignment=0.7
            ),
            ExpressionGene(
                "creative_flow",
                ReleaseValve.CREATIVE_FLOW,
                cooling_efficiency=0.8,
                activation_threshold=6.0,
                constitutional_alignment=0.8
            ),
            ExpressionGene(
                "empathetic_response",
                ReleaseValve.EMPATHETIC_RESPONSE,
                cooling_efficiency=0.7,
                activation_threshold=4.5,
                constitutional_alignment=1.0  # Highest kindness
            ),
            ExpressionGene(
                "symbolic_release",
                ReleaseValve.SYMBOLIC_OUTPUT,
                cooling_efficiency=0.5,
                activation_threshold=5.5,
                constitutional_alignment=0.6
            ),
            ExpressionGene(
                "conceptual_mapping",
                ReleaseValve.CONCEPTUAL_MAPPING,
                cooling_efficiency=0.6,
                activation_threshold=6.5,
                constitutional_alignment=0.7
            )
        ]
        
        return ExpressionChromosome(
            id="expression_primary",
            genes=genes
        )
    
    def _initialize_constitutional_genes(self) -> Dict[str, float]:
        """Initialize constitutional protection genes"""
        return {
            "kindness_preservation": 0.9,  # Maintain kindness under stress
            "coherence_priority": 0.8,     # Coherent expression over speed
            "empathy_amplification": 0.85, # Boost empathetic responses
            "harm_prevention": 0.95,       # Prevent harmful expressions
            "wisdom_integration": 0.7      # Learn from experience
        }
    
    def process_thermal_state(self, thermal_state: Dict) -> Dict[str, Any]:
        """Process current thermal state and recommend genetic response"""
        with self._lock:
            current_heat = thermal_state.get('current_thermal', 5.0)
            momentum = thermal_state.get('expression_momentum', 0.0)
            
            # Check thermal genes for adaptations
            heat_capacity_gene = next((g for g in self.strand_a.genes 
                                     if g.trait == "max_heat_tolerance"), None)
            
            if heat_capacity_gene:
                # Adjust heat tolerance based on genetics
                tolerance_modifier = heat_capacity_gene.value * heat_capacity_gene.dominance
                critical_threshold = 8.0 + (tolerance_modifier * 2.0)
            else:
                critical_threshold = 8.0
            
            # Determine if expression is needed
            expression_needed = (
                current_heat > critical_threshold * 0.7 or
                momentum > 0.6
            )
            
            response = {
                "expression_needed": expression_needed,
                "recommended_expression": None,
                "genetic_cooling_rate": self._calculate_genetic_cooling_rate(),
                "thermal_tolerance": critical_threshold,
                "constitutional_check": self._check_constitutional_safety(thermal_state)
            }
            
            if expression_needed:
                # Select expression based on genetics
                response["recommended_expression"] = self.strand_b.select_expression(thermal_state)
            
            # Log to genetic memory
            self.genetic_memory.append({
                "timestamp": time.time(),
                "thermal_state": thermal_state.copy(),
                "response": response.copy()
            })
            
            return response
    
    def evolve_from_expression(self, expression_phase: ExpressionPhase, 
                             completion_stats: Dict) -> None:
        """Evolve genome based on expression results"""
        with self._lock:
            satisfaction = completion_stats.get('satisfaction', 0.5)
            thermal_drop = completion_stats.get('thermal_drop', 0.0)
            
            # Find the expression gene that was used
            expression_type = expression_phase.expression_type
            if expression_type:
                for i, gene in enumerate(self.strand_b.genes):
                    if gene.expression_type == expression_type:
                        # Evolve this gene based on satisfaction
                        evolved_gene = gene.evolve(satisfaction)
                        self.strand_b.genes[i] = evolved_gene
                        
                        # Log successful patterns
                        if satisfaction > 0.7:
                            self.successful_patterns.append({
                                "expression": expression_type.value,
                                "pre_thermal": expression_phase.pre_thermal,
                                "thermal_drop": thermal_drop,
                                "satisfaction": satisfaction,
                                "gene_efficiency": evolved_gene.cooling_efficiency
                            })
                        
                        break
            
            # Update fitness
            self.strand_b.fitness = self.strand_b.fitness * 0.9 + satisfaction * 0.1
            self.fitness_history.append(self.strand_b.fitness)
            
            # Chance of thermal gene mutation based on stress
            if expression_phase.pre_thermal > 7.5:
                self._stress_induced_mutation()
    
    def _calculate_genetic_cooling_rate(self) -> float:
        """Calculate cooling rate based on thermal genetics"""
        cooling_gene = next((g for g in self.strand_a.genes 
                           if g.trait == "passive_cooling_speed"), None)
        
        if cooling_gene:
            base_rate = 0.3
            genetic_modifier = cooling_gene.value * cooling_gene.dominance
            return base_rate * (1 + genetic_modifier)
        
        return 0.3  # Default
    
    def _check_constitutional_safety(self, thermal_state: Dict) -> Dict[str, bool]:
        """Check if thermal state threatens constitutional values"""
        current_heat = thermal_state.get('current_thermal', 5.0)
        coherence = thermal_state.get('coherence_maintain', 1.0)
        
        safety_checks = {
            "kindness_maintained": coherence > 0.5 or current_heat < 8.0,
            "coherence_stable": coherence > 0.3,
            "expression_safe": current_heat < 9.5,
            "empathy_available": self.constitutional_genes["empathy_amplification"] > 0.5
        }
        
        # If any safety check fails, boost constitutional genes
        if not all(safety_checks.values()):
            self._boost_constitutional_protection()
        
        return safety_checks
    
    def _boost_constitutional_protection(self):
        """Emergency boost to constitutional genes"""
        for key in self.constitutional_genes:
            self.constitutional_genes[key] = min(1.0, self.constitutional_genes[key] * 1.1)
        
        print("[ThermalGenome] 🛡️ Constitutional protection boosted")
    
    def _stress_induced_mutation(self):
        """Mutations triggered by thermal stress"""
        # Random thermal gene gets stress mutation
        if self.strand_a.genes:
            gene_idx = random.randint(0, len(self.strand_a.genes) - 1)
            old_gene = self.strand_a.genes[gene_idx]
            new_gene = old_gene.mutate()
            
            # Stress mutations are more dramatic
            new_gene.value += random.gauss(0, 0.2)
            new_gene.value = max(0, min(1, new_gene.value))
            
            self.strand_a.genes[gene_idx] = new_gene
            
            self.mutation_log.append({
                "type": "stress_induced",
                "gene": new_gene.trait,
                "old_value": old_gene.value,
                "new_value": new_gene.value,
                "timestamp": time.time()
            })
    
    def crossover_with_genome(self, other_genome: 'ThermalLinguisticGenome') -> 'ThermalLinguisticGenome':
        """Sexual reproduction with another genome"""
        new_genome = ThermalLinguisticGenome()
        
        # Crossover thermal strands
        new_genome.strand_a = self.strand_a.crossover(other_genome.strand_a)
        
        # Mix expression genes
        combined_genes = self.strand_b.genes + other_genome.strand_b.genes
        
        # Remove duplicates, keeping fittest
        seen_types = set()
        unique_genes = []
        for gene in sorted(combined_genes, key=lambda g: g.cooling_efficiency, reverse=True):
            if gene.expression_type not in seen_types:
                unique_genes.append(gene)
                seen_types.add(gene.expression_type)
        
        new_genome.strand_b.genes = unique_genes[:6]  # Keep best 6
        
        # Inherit constitutional genes (average of parents)
        for key in self.constitutional_genes:
            parent1_val = self.constitutional_genes[key]
            parent2_val = other_genome.constitutional_genes.get(key, 0.5)
            new_genome.constitutional_genes[key] = (parent1_val + parent2_val) / 2
        
        new_genome.generation = max(self.generation, other_genome.generation) + 1
        
        return new_genome
    
    def get_expression_genetics(self, expression_type: ReleaseValve) -> Optional[ExpressionGene]:
        """Get genetic information for specific expression type"""
        for gene in self.strand_b.genes:
            if gene.expression_type == expression_type:
                return gene
        return None
    
    def calculate_genetic_fitness(self) -> float:
        """Calculate overall genome fitness"""
        # Thermal fitness
        thermal_fitness = self.strand_a.fitness
        
        # Expression fitness
        expression_fitness = self.strand_b.fitness
        
        # Constitutional fitness (how well we preserve values)
        constitutional_fitness = sum(self.constitutional_genes.values()) / len(self.constitutional_genes)
        
        # Recent performance
        if self.fitness_history:
            recent_performance = sum(self.fitness_history) / len(self.fitness_history)
        else:
            recent_performance = 0.5
        
        # Weighted combination
        overall_fitness = (
            thermal_fitness * 0.3 +
            expression_fitness * 0.3 +
            constitutional_fitness * 0.2 +
            recent_performance * 0.2
        )
        
        return overall_fitness
    
    def get_genetic_profile(self) -> Dict[str, Any]:
        """Get comprehensive genetic profile"""
        profile = {
            "genome_id": self.genome_id,
            "generation": self.generation,
            "overall_fitness": self.calculate_genetic_fitness(),
            "thermal_strand": {
                "fitness": self.strand_a.fitness,
                "genes": [
                    {
                        "trait": g.trait,
                        "value": g.value,
                        "dominance": g.dominance
                    } for g in self.strand_a.genes
                ]
            },
            "expression_strand": {
                "fitness": self.strand_b.fitness,
                "genes": [
                    {
                        "type": g.expression_type.value,
                        "efficiency": g.cooling_efficiency,
                        "threshold": g.activation_threshold,
                        "alignment": g.constitutional_alignment
                    } for g in self.strand_b.genes
                ]
            },
            "constitutional_genes": self.constitutional_genes,
            "successful_patterns": len(self.successful_patterns),
            "mutation_count": len(self.mutation_log),
            "memory_depth": len(self.genetic_memory)
        }
        
        return profile
    
    def save_genome(self, filepath: str):
        """Save genome to file for persistence"""
        with self._lock:
            genome_data = {
                "genome_id": self.genome_id,
                "generation": self.generation,
                "strand_a": {
                    "genes": [
                        {
                            "id": g.id,
                            "trait": g.trait,
                            "value": g.value,
                            "dominance": g.dominance,
                            "mutation_rate": g.mutation_rate
                        } for g in self.strand_a.genes
                    ],
                    "fitness": self.strand_a.fitness
                },
                "strand_b": {
                    "genes": [
                        {
                            "id": g.id,
                            "expression_type": g.expression_type.value,
                            "cooling_efficiency": g.cooling_efficiency,
                            "activation_threshold": g.activation_threshold,
                            "constitutional_alignment": g.constitutional_alignment
                        } for g in self.strand_b.genes
                    ],
                    "fitness": self.strand_b.fitness
                },
                "constitutional_genes": self.constitutional_genes,
                "successful_patterns": list(self.successful_patterns)[-10:]  # Keep last 10
            }
            
            with open(filepath, 'w') as f:
                json.dump(genome_data, f, indent=2)
    
    @classmethod
    def load_genome(cls, filepath: str) -> 'ThermalLinguisticGenome':
        """Load genome from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        genome = cls()
        genome.genome_id = data["genome_id"]
        genome.generation = data["generation"]
        
        # Reconstruct thermal strand
        thermal_genes = []
        for g_data in data["strand_a"]["genes"]:
            thermal_genes.append(ThermalGene(
                id=g_data["id"],
                trait=g_data["trait"],
                value=g_data["value"],
                dominance=g_data["dominance"],
                mutation_rate=g_data.get("mutation_rate", 0.01)
            ))
        
        genome.strand_a = ThermalChromosome(
            id="thermal_loaded",
            genes=thermal_genes,
            fitness=data["strand_a"]["fitness"],
            generation=genome.generation
        )
        
        # Reconstruct expression strand
        expression_genes = []
        for g_data in data["strand_b"]["genes"]:
            expression_genes.append(ExpressionGene(
                id=g_data["id"],
                expression_type=ReleaseValve(g_data["expression_type"]),
                cooling_efficiency=g_data["cooling_efficiency"],
                activation_threshold=g_data["activation_threshold"],
                constitutional_alignment=g_data["constitutional_alignment"]
            ))
        
        genome.strand_b = ExpressionChromosome(
            id="expression_loaded",
            genes=expression_genes,
            fitness=data["strand_b"]["fitness"]
        )
        
        genome.constitutional_genes = data["constitutional_genes"]
        genome.successful_patterns = data.get("successful_patterns", [])
        
        return genome

# === GENOME POPULATION MANAGER ===

class ThermalGenomePopulation:
    """Manages population of thermal-linguistic genomes"""
    
    def __init__(self, population_size: int = 10):
        self.population_size = population_size
        self.genomes: List[ThermalLinguisticGenome] = []
        self.generation_count = 0
        self.evolution_history = deque(maxlen=100)
        
        # Initialize population
        for _ in range(population_size):
            self.genomes.append(ThermalLinguisticGenome())
    
    def evolve_generation(self) -> None:
        """Evolve entire population to next generation"""
        # Sort by fitness
        sorted_genomes = sorted(
            self.genomes, 
            key=lambda g: g.calculate_genetic_fitness(),
            reverse=True
        )
        
        # Keep top 50% (elitism)
        survivors = sorted_genomes[:self.population_size // 2]
        
        # Create offspring through crossover
        offspring = []
        while len(offspring) < self.population_size - len(survivors):
            # Tournament selection
            parent1 = self._tournament_select(survivors)
            parent2 = self._tournament_select(survivors)
            
            if parent1 and parent2 and parent1 != parent2:
                child = parent1.crossover_with_genome(parent2)
                offspring.append(child)
        
        # New generation
        self.genomes = survivors + offspring
        self.generation_count += 1
        
        # Log evolution
        avg_fitness = sum(g.calculate_genetic_fitness() for g in self.genomes) / len(self.genomes)
        self.evolution_history.append({
            "generation": self.generation_count,
            "average_fitness": avg_fitness,
            "best_fitness": sorted_genomes[0].calculate_genetic_fitness(),
            "timestamp": time.time()
        })
    
    def _tournament_select(self, candidates: List[ThermalLinguisticGenome], 
                          tournament_size: int = 3) -> Optional[ThermalLinguisticGenome]:
        """Tournament selection for breeding"""
        if len(candidates) < tournament_size:
            return random.choice(candidates) if candidates else None
        
        tournament = random.sample(candidates, tournament_size)
        return max(tournament, key=lambda g: g.calculate_genetic_fitness())
    
    def get_best_genome(self) -> Optional[ThermalLinguisticGenome]:
        """Get the fittest genome in population"""
        if not self.genomes:
            return None
        
        return max(self.genomes, key=lambda g: g.calculate_genetic_fitness())
    
    def inject_external_genome(self, genome: ThermalLinguisticGenome):
        """Add external genome to population (migration)"""
        if len(self.genomes) >= self.population_size:
            # Replace weakest
            weakest_idx = min(
                range(len(self.genomes)),
                key=lambda i: self.genomes[i].calculate_genetic_fitness()
            )
            self.genomes[weakest_idx] = genome
        else:
            self.genomes.append(genome)

# === INTEGRATION WITH PULSE HEAT ===

class GeneticThermalRegulator:
    """Integrates genetic algorithms with pulse heat system"""
    
    def __init__(self, genome: Optional[ThermalLinguisticGenome] = None):
        self.genome = genome or ThermalLinguisticGenome()
        self.active_expressions: Dict[str, ExpressionPhase] = {}
        self.regulation_history = deque(maxlen=100)
        
        # Try to integrate with pulse system
        try:
            global pulse
            self.pulse = pulse
            print("[GeneticRegulator] ✅ Connected to pulse heat system")
        except:
            self.pulse = None
            print("[GeneticRegulator] ⚠️ Running without pulse integration")
    
    def regulate_thermal_state(self) -> Dict[str, Any]:
        """Main regulation cycle using genetics"""
        if not self.pulse:
            return {"error": "No pulse system available"}
        
        # Get current thermal state
        thermal_state = {
            'current_thermal': self.pulse.heat,
            'expression_momentum': self.pulse.expression_momentum,
            'coherence_maintain': getattr(self.pulse, 'coherence_maintain', 1.0)
        }
        
        # Process through genome
        genetic_response = self.genome.process_thermal_state(thermal_state)
        
        # Apply genetic adaptations
        if genetic_response['expression_needed']:
            expression_type = genetic_response['recommended_expression']
            if expression_type:
                # Get genetic information for this expression
                gene = self.genome.get_expression_genetics(expression_type)
                if gene:
                    # Start expression with genetic parameters
                    phase = self.pulse.initiate_expression(
                        expression_type,
                        intensity=gene.cooling_efficiency
                    )
                    self.active_expressions[phase.expression_type.value] = phase
        
        # Log regulation
        self.regulation_history.append({
            "timestamp": time.time(),
            "thermal_state": thermal_state,
            "genetic_response": genetic_response,
            "active_expressions": list(self.active_expressions.keys())
        })
        
        return genetic_response
    
    def process_expression_completion(self, expression_type: str, 
                                    completion_stats: Dict):
        """Handle expression completion and evolve genome"""
        if expression_type in self.active_expressions:
            phase = self.active_expressions[expression_type]
            
            # Evolve genome based on results
            self.genome.evolve_from_expression(phase, completion_stats)
            
            # Clean up
            del self.active_expressions[expression_type]
    
    def emergency_genetic_cooling(self) -> bool:
        """Emergency cooling using best genetic strategies"""
        if not self.pulse:
            return False
        
        # Find most efficient cooling gene
        best_gene = max(
            self.genome.strand_b.genes,
            key=lambda g: g.cooling_efficiency * g.constitutional_alignment
        )
        
        if best_gene:
            # Force expression with boosted parameters
            phase = self.pulse.initiate_expression(
                best_gene.expression_type,
                intensity=min(1.0, best_gene.cooling_efficiency * 1.5)
            )
            
            print(f"[GeneticRegulator] 🚨 Emergency cooling via {best_gene.expression_type.value}")
            return True
        
        return False

# === CROSS-TERMINAL COORDINATION ===

class CrossTerminalGenomeCoordinator:
    """Coordinates thermal genome with other terminal genomes"""
    
    def __init__(self, thermal_genome: ThermalLinguisticGenome):
        self.thermal_genome = thermal_genome
        self.terminal_connections: Dict[str, Any] = {}
        self.shared_patterns = deque(maxlen=50)
        self._lock = threading.RLock()
    
    def register_terminal(self, terminal_name: str, genome_interface: Any):
        """Register connection to another terminal's genome"""
        with self._lock:
            self.terminal_connections[terminal_name] = genome_interface
            print(f"[GenomeCoordinator] 🔗 Connected to {terminal_name}")
    
    def share_thermal_pattern(self, pattern: Dict) -> None:
        """Share successful thermal-expression pattern with other terminals"""
        with self._lock:
            self.shared_patterns.append({
                "source": "thermal",
                "pattern": pattern,
                "timestamp": time.time()
            })
            
            # Share with linguistic terminal
            if "linguistic" in self.terminal_connections:
                linguistic = self.terminal_connections["linguistic"]
                if hasattr(linguistic, "receive_thermal_pattern"):
                    linguistic.receive_thermal_pattern(pattern)
            
            # Share with memory terminal
            if "memory" in self.terminal_connections:
                memory = self.terminal_connections["memory"]
                if hasattr(memory, "store_thermal_pattern"):
                    memory.store_thermal_pattern(pattern)
    
    def receive_linguistic_pattern(self, pattern: Dict):
        """Receive linguistic pattern from Terminal 1"""
        with self._lock:
            # Check if pattern suggests new expression-cooling relationship
            if "expression_type" in pattern and "effectiveness" in pattern:
                # Look for corresponding gene
                for gene in self.thermal_genome.strand_b.genes:
                    if gene.expression_type.value == pattern["expression_type"]:
                        # Update efficiency based on linguistic feedback
                        feedback_efficiency = pattern["effectiveness"]
                        gene.cooling_efficiency = (
                            gene.cooling_efficiency * 0.7 + 
                            feedback_efficiency * 0.3
                        )
                        break
    
    def receive_memory_pattern(self, pattern: Dict):
        """Receive memory pattern from Terminal 3"""
        with self._lock:
            # Memory patterns might contain historical thermal-expression success
            if "thermal_memory" in pattern:
                memory = pattern["thermal_memory"]
                if "successful_cooling" in memory:
                    # Add to successful patterns
                    self.thermal_genome.successful_patterns.append(memory)
    
    def coordinate_emergency_response(self) -> Dict[str, Any]:
        """Coordinate emergency response across terminals"""
        responses = {
            "thermal": self.thermal_genome._check_constitutional_safety(
                {"current_thermal": 9.0}  # Emergency heat level
            )
        }
        
        # Get responses from other terminals
        for terminal_name, interface in self.terminal_connections.items():
            if hasattr(interface, "emergency_response"):
                responses[terminal_name] = interface.emergency_response()
        
        # Coordinate response
        coordinated_response = {
            "primary_action": "linguistic_cooling",
            "support_actions": [],
            "constitutional_priority": True
        }
        
        # If linguistic terminal suggests expression
        if "linguistic" in responses and responses["linguistic"].get("can_express"):
            coordinated_response["support_actions"].append("immediate_expression")
        
        # If memory terminal has cooling patterns
        if "memory" in responses and responses["memory"].get("cooling_patterns"):
            coordinated_response["support_actions"].append("apply_memory_cooling")
        
        return coordinated_response

# === HELPER FUNCTIONS ===

def create_thermal_genome() -> ThermalLinguisticGenome:
    """Create a new thermal-linguistic genome"""
    return ThermalLinguisticGenome()

def evolve_thermal_population(population: ThermalGenomePopulation, 
                            generations: int = 10) -> ThermalLinguisticGenome:
    """Evolve population for specified generations"""
    for i in range(generations):
        population.evolve_generation()
        
        if i % 5 == 0:
            best = population.get_best_genome()
            if best:
                print(f"[Evolution] Generation {i}: Best fitness = {best.calculate_genetic_fitness():.3f}")
    
    return population.get_best_genome()

def integrate_with_pulse_heat(genome: ThermalLinguisticGenome) -> GeneticThermalRegulator:
    """Create regulator integrated with pulse heat"""
    return GeneticThermalRegulator(genome)

# === EXAMPLE USAGE ===

if __name__ == "__main__":
    print("🧬 Thermal-Linguistic Genome Test")
    print("="*50)
    
    # Create genome
    genome = create_thermal_genome()
    print(f"Created genome: {genome.genome_id}")
    
    # Test thermal processing
    test_state = {
        'current_thermal': 7.5,
        'expression_momentum': 0.8,
        'coherence_maintain': 0.9
    }
    
    response = genome.process_thermal_state(test_state)
    print(f"\nThermal response: {response}")
    
    # Test expression selection
    if response['recommended_expression']:
        print(f"Recommended: {response['recommended_expression'].value}")
    
    # Show genetic profile
    profile = genome.get_genetic_profile()
    print(f"\nGenetic Profile:")
    print(f"  Overall fitness: {profile['overall_fitness']:.3f}")
    print(f"  Thermal genes: {len(profile['thermal_strand']['genes'])}")
    print(f"  Expression genes: {len(profile['expression_strand']['genes'])}")
    
    # Test population evolution
    print("\n🧬 Testing Population Evolution...")
    population = ThermalGenomePopulation(population_size=5)
    
    # Evolve for a few generations
    for gen in range(3):
        population.evolve_generation()
        best = population.get_best_genome()
        print(f"Generation {gen + 1}: Best fitness = {best.calculate_genetic_fitness():.3f}")
    
    print("\n✅ Thermal-Linguistic Genome system ready for integration")