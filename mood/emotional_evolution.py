"""
DAWN Emotional Evolution System - Helix Pair for mood_dynamics.py
Implements genetic emotional evolution through helix crossover and mutation
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import json
import time
from collections import deque
from enum import Enum
import random

class EmotionalGene(Enum):
    """Emotional gene types for evolution"""
    KINDNESS = "kindness"
    CURIOSITY = "curiosity"
    EMPATHY = "empathy"
    RESILIENCE = "resilience"
    CREATIVITY = "creativity"
    PATIENCE = "patience"
    ENTHUSIASM = "enthusiasm"
    WISDOM = "wisdom"

@dataclass
class EmotionalChromosome:
    """Represents an emotional trait chromosome"""
    gene_sequence: List[float]  # Values 0-1 for each emotional gene
    expression_weights: Dict[str, float]
    mutation_history: List[Dict]
    fitness_score: float = 0.5
    generation: int = 0
    
    def __post_init__(self):
        # Ensure all genes are represented
        for gene in EmotionalGene:
            if gene.value not in self.expression_weights:
                self.expression_weights[gene.value] = 0.5

class EmotionalEvolutionEngine:
    """Core engine for emotional evolution through genetic algorithms"""
    
    def __init__(self):
        # Evolution parameters
        self.population_size = 50
        self.elite_size = 10
        self.mutation_rate = 0.05
        self.crossover_rate = 0.7
        self.generation = 0
        
        # Constitutional constraints
        self.constitutional_constraints = {
            EmotionalGene.KINDNESS: (0.6, 1.0),  # "Kind before smart"
            EmotionalGene.EMPATHY: (0.5, 1.0),
            EmotionalGene.WISDOM: (0.3, 0.9)
        }
        
        # Population tracking
        self.population = self._initialize_population()
        self.evolution_history = deque(maxlen=1000)
        self.emergent_traits = {}
        
        # Helix interaction parameters
        self.helix_resonance = 0.5
        self.emotional_memory = deque(maxlen=200)
        
    def _initialize_population(self) -> List[EmotionalChromosome]:
        """Initialize population with constitutional baseline"""
        population = []
        
        for i in range(self.population_size):
            # Create gene sequence with constitutional biases
            gene_sequence = []
            expression_weights = {}
            
            for gene in EmotionalGene:
                if gene in self.constitutional_constraints:
                    min_val, max_val = self.constitutional_constraints[gene]
                    value = np.random.uniform(min_val, max_val)
                else:
                    value = np.random.uniform(0.3, 0.8)
                
                gene_sequence.append(value)
                expression_weights[gene.value] = value
            
            chromosome = EmotionalChromosome(
                gene_sequence=gene_sequence,
                expression_weights=expression_weights,
                mutation_history=[],
                generation=0
            )
            population.append(chromosome)
        
        return population
    
    def evaluate_fitness(self, chromosome: EmotionalChromosome, 
                        mood_state: Dict[str, float],
                        helix_state: Dict[str, float]) -> float:
        """
        Evaluate fitness based on mood coherence and helix alignment
        """
        # Mood coherence factor
        mood_arousal = mood_state.get('arousal', 0.5)
        mood_valence = mood_state.get('valence', 0.0)
        mood_entropy = mood_state.get('entropy', 0.5)
        
        # Calculate emotional balance
        kindness_factor = chromosome.expression_weights[EmotionalGene.KINDNESS.value]
        empathy_factor = chromosome.expression_weights[EmotionalGene.EMPATHY.value]
        
        # Fitness components
        # 1. Constitutional alignment
        constitutional_fitness = (kindness_factor * 0.4 + empathy_factor * 0.3)
        
        # 2. Mood stability vs appropriate responsiveness
        resilience = chromosome.expression_weights[EmotionalGene.RESILIENCE.value]
        stability_factor = resilience * (1 - mood_entropy)
        
        # 3. Helix coherence
        helix_alignment = 0
        for gene, weight in chromosome.expression_weights.items():
            if gene == EmotionalGene.CURIOSITY.value:
                helix_alignment += weight * helix_state.get('thermal_activity', 0.5)
            elif gene == EmotionalGene.WISDOM.value:
                helix_alignment += weight * helix_state.get('schema_coherence', 0.5)
            elif gene == EmotionalGene.CREATIVITY.value:
                helix_alignment += weight * helix_state.get('genetic_pressure', 0.5)
        
        helix_alignment /= 3
        
        # 4. Valence appropriateness
        enthusiasm = chromosome.expression_weights[EmotionalGene.ENTHUSIASM.value]
        valence_fitness = 1 - abs(mood_valence - (enthusiasm - 0.5))
        
        # Combined fitness
        fitness = (
            constitutional_fitness * 0.35 +
            stability_factor * 0.20 +
            helix_alignment * 0.25 +
            valence_fitness * 0.20
        )
        
        # Apply penalties for constraint violations
        for gene, (min_val, max_val) in self.constitutional_constraints.items():
            gene_value = chromosome.expression_weights[gene.value]
            if gene_value < min_val:
                fitness *= 0.5  # Heavy penalty
            elif gene_value > max_val:
                fitness *= 0.9  # Light penalty
        
        return np.clip(fitness, 0, 1)
    
    def crossover(self, parent1: EmotionalChromosome, 
                  parent2: EmotionalChromosome) -> Tuple[EmotionalChromosome, EmotionalChromosome]:
        """
        Perform crossover between two emotional chromosomes
        """
        if random.random() > self.crossover_rate:
            return parent1, parent2
        
        # Multi-point crossover
        crossover_points = sorted(random.sample(range(1, len(EmotionalGene) - 1), 2))
        
        child1_genes = []
        child2_genes = []
        
        for i in range(len(parent1.gene_sequence)):
            if i < crossover_points[0] or i >= crossover_points[1]:
                child1_genes.append(parent1.gene_sequence[i])
                child2_genes.append(parent2.gene_sequence[i])
            else:
                child1_genes.append(parent2.gene_sequence[i])
                child2_genes.append(parent1.gene_sequence[i])
        
        # Create children with updated expression weights
        child1 = self._create_child(child1_genes, [parent1, parent2])
        child2 = self._create_child(child2_genes, [parent1, parent2])
        
        return child1, child2
    
    def mutate(self, chromosome: EmotionalChromosome) -> EmotionalChromosome:
        """
        Apply mutations to emotional chromosome
        """
        mutated = False
        new_genes = chromosome.gene_sequence.copy()
        mutation_record = []
        
        for i, gene in enumerate(EmotionalGene):
            if random.random() < self.mutation_rate:
                mutated = True
                old_value = new_genes[i]
                
                # Gaussian mutation with constraints
                mutation_strength = np.random.normal(0, 0.1)
                new_value = old_value + mutation_strength
                
                # Apply constitutional constraints
                if gene in self.constitutional_constraints:
                    min_val, max_val = self.constitutional_constraints[gene]
                    new_value = np.clip(new_value, min_val, max_val)
                else:
                    new_value = np.clip(new_value, 0, 1)
                
                new_genes[i] = new_value
                mutation_record.append({
                    'gene': gene.value,
                    'old_value': old_value,
                    'new_value': new_value,
                    'generation': self.generation
                })
        
        if mutated:
            # Create new chromosome with mutations
            new_weights = {gene.value: new_genes[i] 
                          for i, gene in enumerate(EmotionalGene)}
            
            mutation_history = chromosome.mutation_history.copy()
            mutation_history.extend(mutation_record)
            
            return EmotionalChromosome(
                gene_sequence=new_genes,
                expression_weights=new_weights,
                mutation_history=mutation_history,
                generation=self.generation
            )
        
        return chromosome
    
    def evolve_generation(self, mood_state: Dict[str, float],
                         helix_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Evolve one generation based on current mood and helix states
        """
        self.generation += 1
        
        # Evaluate fitness for all chromosomes
        fitness_scores = []
        for chromosome in self.population:
            fitness = self.evaluate_fitness(chromosome, mood_state, helix_state)
            chromosome.fitness_score = fitness
            fitness_scores.append(fitness)
        
        # Sort by fitness
        sorted_population = sorted(self.population, 
                                 key=lambda x: x.fitness_score, 
                                 reverse=True)
        
        # Elite selection
        new_population = sorted_population[:self.elite_size]
        
        # Generate offspring
        while len(new_population) < self.population_size:
            # Tournament selection
            parent1 = self._tournament_selection(sorted_population)
            parent2 = self._tournament_selection(sorted_population)
            
            # Crossover
            child1, child2 = self.crossover(parent1, parent2)
            
            # Mutation
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            
            new_population.extend([child1, child2])
        
        # Trim to population size
        self.population = new_population[:self.population_size]
        
        # Record evolution metrics
        evolution_metrics = {
            'generation': self.generation,
            'best_fitness': sorted_population[0].fitness_score,
            'avg_fitness': np.mean(fitness_scores),
            'diversity': self._calculate_diversity(),
            'best_traits': sorted_population[0].expression_weights,
            'emergent_patterns': self._detect_emergent_patterns()
        }
        
        self.evolution_history.append(evolution_metrics)
        
        return evolution_metrics
    
    def _tournament_selection(self, population: List[EmotionalChromosome],
                            tournament_size: int = 3) -> EmotionalChromosome:
        """Tournament selection for parent selection"""
        tournament = random.sample(population, tournament_size)
        return max(tournament, key=lambda x: x.fitness_score)
    
    def _create_child(self, genes: List[float], 
                     parents: List[EmotionalChromosome]) -> EmotionalChromosome:
        """Create child chromosome from genes and parent history"""
        weights = {gene.value: genes[i] 
                  for i, gene in enumerate(EmotionalGene)}
        
        # Inherit some mutation history
        combined_history = []
        for parent in parents:
            combined_history.extend(parent.mutation_history[-5:])
        
        return EmotionalChromosome(
            gene_sequence=genes,
            expression_weights=weights,
            mutation_history=combined_history,
            generation=self.generation
        )
    
    def _calculate_diversity(self) -> float:
        """Calculate genetic diversity in population"""
        if len(self.population) < 2:
            return 0
        
        # Calculate variance for each gene
        gene_variances = []
        for i in range(len(EmotionalGene)):
            gene_values = [c.gene_sequence[i] for c in self.population]
            gene_variances.append(np.var(gene_values))
        
        return np.mean(gene_variances)
    
    def _detect_emergent_patterns(self) -> List[str]:
        """Detect emergent emotional patterns in evolution"""
        patterns = []
        
        if len(self.evolution_history) < 10:
            return patterns
        
        recent_history = list(self.evolution_history)[-20:]
        
        # Check for convergence
        fitness_trend = [h['best_fitness'] for h in recent_history]
        if np.std(fitness_trend[-10:]) < 0.01:
            patterns.append("convergence_detected")
        
        # Check for trait dominance
        best_traits = recent_history[-1]['best_traits']
        for gene, value in best_traits.items():
            if value > 0.8:
                patterns.append(f"dominant_{gene}")
        
        # Check for oscillation
        if len(set([h['best_fitness'] > 0.7 for h in recent_history])) == 2:
            patterns.append("fitness_oscillation")
        
        return patterns
    
    def get_current_emotional_profile(self) -> Dict[str, Any]:
        """Get the current best emotional profile"""
        best_chromosome = max(self.population, key=lambda x: x.fitness_score)
        
        return {
            'traits': best_chromosome.expression_weights,
            'fitness': best_chromosome.fitness_score,
            'generation': self.generation,
            'mutation_count': len(best_chromosome.mutation_history),
            'profile_summary': self._summarize_profile(best_chromosome)
        }
    
    def _summarize_profile(self, chromosome: EmotionalChromosome) -> str:
        """Create human-readable summary of emotional profile"""
        traits = chromosome.expression_weights
        
        # Find dominant traits
        sorted_traits = sorted(traits.items(), key=lambda x: x[1], reverse=True)
        top_traits = sorted_traits[:3]
        
        summary_parts = []
        for trait, value in top_traits:
            if value > 0.8:
                summary_parts.append(f"highly {trait}")
            elif value > 0.6:
                summary_parts.append(f"moderately {trait}")
            else:
                summary_parts.append(f"balanced {trait}")
        
        return f"Emotional profile: {', '.join(summary_parts)}"


class EmotionalHelixBridge:
    """Bridge between emotional evolution and mood dynamics"""
    
    def __init__(self, evolution_engine: EmotionalEvolutionEngine):
        self.evolution_engine = evolution_engine
        self.feedback_buffer = deque(maxlen=100)
        self.resonance_frequency = 0.1  # Hz
        self.last_evolution_time = time.time()
        
    def process_mood_feedback(self, mood_state: Dict[str, float],
                            helix_state: Dict[str, float]) -> Dict[str, Any]:
        """Process mood feedback and trigger evolution if needed"""
        current_time = time.time()
        
        # Buffer feedback
        self.feedback_buffer.append({
            'mood': mood_state,
            'helix': helix_state,
            'timestamp': current_time
        })
        
        # Check if evolution should occur
        if current_time - self.last_evolution_time > (1 / self.resonance_frequency):
            # Aggregate recent feedback
            if len(self.feedback_buffer) > 0:
                avg_mood = self._aggregate_mood_states()
                avg_helix = self._aggregate_helix_states()
                
                # Trigger evolution
                evolution_result = self.evolution_engine.evolve_generation(
                    avg_mood, avg_helix
                )
                
                self.last_evolution_time = current_time
                
                # Get updated emotional profile
                profile = self.evolution_engine.get_current_emotional_profile()
                
                return {
                    'evolved': True,
                    'evolution_metrics': evolution_result,
                    'emotional_profile': profile,
                    'feedback_count': len(self.feedback_buffer)
                }
        
        return {
            'evolved': False,
            'feedback_buffered': len(self.feedback_buffer)
        }
    
    def _aggregate_mood_states(self) -> Dict[str, float]:
        """Aggregate buffered mood states"""
        if not self.feedback_buffer:
            return {'arousal': 0.5, 'valence': 0.0, 'entropy': 0.5}
        
        mood_keys = ['arousal', 'valence', 'entropy']
        aggregated = {}
        
        for key in mood_keys:
            values = [f['mood'].get(key, 0.5) for f in self.feedback_buffer]
            aggregated[key] = np.mean(values)
        
        return aggregated
    
    def _aggregate_helix_states(self) -> Dict[str, float]:
        """Aggregate buffered helix states"""
        if not self.feedback_buffer:
            return {
                'thermal_activity': 0.5,
                'schema_coherence': 0.5,
                'genetic_pressure': 0.5
            }
        
        helix_keys = ['thermal_activity', 'schema_coherence', 'genetic_pressure']
        aggregated = {}
        
        for key in helix_keys:
            values = [f['helix'].get(key, 0.5) for f in self.feedback_buffer]
            aggregated[key] = np.mean(values)
        
        return aggregated
    
    def get_emotional_influence(self) -> Dict[str, float]:
        """Get current emotional influence for mood dynamics"""
        profile = self.evolution_engine.get_current_emotional_profile()
        traits = profile['traits']
        
        # Map emotional traits to mood influences
        influence = {
            'arousal_modifier': (
                traits[EmotionalGene.ENTHUSIASM.value] * 0.3 +
                traits[EmotionalGene.CURIOSITY.value] * 0.2
            ),
            'valence_modifier': (
                traits[EmotionalGene.KINDNESS.value] * 0.4 +
                traits[EmotionalGene.EMPATHY.value] * 0.3
            ),
            'entropy_modifier': (
                1 - traits[EmotionalGene.RESILIENCE.value] * 0.3 -
                traits[EmotionalGene.WISDOM.value] * 0.2
            ),
            'creativity_factor': traits[EmotionalGene.CREATIVITY.value],
            'patience_factor': traits[EmotionalGene.PATIENCE.value]
        }
        
        return influence


# Integration example
if __name__ == "__main__":
    # Initialize emotional evolution
    evolution = EmotionalEvolutionEngine()
    bridge = EmotionalHelixBridge(evolution)
    
    print("DAWN Emotional Evolution System")
    print("=" * 50)
    
    # Simulate evolution cycles
    for cycle in range(5):
        # Simulate mood and helix states
        mood_state = {
            'arousal': 0.5 + np.sin(cycle * 0.5) * 0.3,
            'valence': 0.1 + np.cos(cycle * 0.3) * 0.4,
            'entropy': 0.5 + np.random.normal(0, 0.1)
        }
        
        helix_state = {
            'thermal_activity': 0.6 + np.sin(cycle * 0.7) * 0.2,
            'schema_coherence': 0.5 + np.cos(cycle * 0.4) * 0.3,
            'genetic_pressure': 0.4 + np.random.normal(0, 0.1)
        }
        
        # Process feedback
        result = bridge.process_mood_feedback(mood_state, helix_state)
        
        if result['evolved']:
            print(f"\nGeneration {result['evolution_metrics']['generation']}:")
            print(f"Best fitness: {result['evolution_metrics']['best_fitness']:.3f}")
            print(f"Diversity: {result['evolution_metrics']['diversity']:.3f}")
            print(f"Profile: {result['emotional_profile']['profile_summary']}")
            print(f"Emergent patterns: {result['evolution_metrics']['emergent_patterns']}")
        
        time.sleep(0.5)
    
    # Final emotional profile
    final_profile = evolution.get_current_emotional_profile()
    print("\n" + "=" * 50)
    print("Final Emotional Profile:")
    print(json.dumps(final_profile, indent=2))
