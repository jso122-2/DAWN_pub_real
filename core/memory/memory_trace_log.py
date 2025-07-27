#!/usr/bin/env python3
"""
memory_trace_log.py - DAWN's Enhanced Memory & Linguistic Genome Architecture
A reflection and reference system with double helix genome structure for evolving consciousness
"""

import json
import time
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict, field
import threading
from collections import deque, defaultdict
import hashlib
import random


@dataclass
class MemoryCrossover:
    """Points where memory and language genes interact"""
    memory_anchor: str  # Fractal string or thermal signature
    linguistic_trigger: str  # What language this memory can generate
    success_rate: float  # How often this crossover produces good expression
    constitutional_alignment: float  # How well it preserves "kind before smart"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def strengthen(self, success_factor: float = 0.1):
        """Strengthen successful crossover"""
        self.success_rate = min(1.0, self.success_rate + success_factor)
    
    def weaken(self, failure_factor: float = 0.05):
        """Weaken unsuccessful crossover"""
        self.success_rate = max(0.0, self.success_rate - failure_factor)


@dataclass
class MemoryGenome:
    """Double helix structure for memory-language evolution"""
    strand_a: Dict[str, Any]  # Memory pattern genetics
    strand_b: Dict[str, Any]  # Linguistic recall genetics
    memory_crossovers: List[MemoryCrossover] = field(default_factory=list)
    recall_accuracy: float = 0.95
    linguistic_fidelity: float = 0.90
    constitutional_preservation: bool = True
    genome_id: str = field(default_factory=lambda: hashlib.md5(str(time.time()).encode()).hexdigest()[:8])
    
    def __post_init__(self):
        # Ensure constitutional core is always present
        self._lock_constitutional_elements()
    
    def _lock_constitutional_elements(self):
        """Ensure constitutional elements cannot be mutated away"""
        self.strand_b['kindness_priority'] = True  # IMMUTABLE
        self.strand_b['smart_over_kind_prevention'] = True  # IMMUTABLE
        self.constitutional_preservation = True


@dataclass
class GenomicMemoryTrace:
    """Enhanced memory trace with linguistic genome data"""
    # Original fields
    timestamp: str
    thought_fragment: str
    thermal_trace: float
    entropy_signature: float
    awareness_level: int
    sigil_cause: str
    fractal_anchor: str
    emotional_valence: float
    coherence_note: str
    
    # Linguistic genome fields
    linguistic_genome: MemoryGenome
    expression_attempts: List[str] = field(default_factory=list)
    successful_expressions: List[str] = field(default_factory=list)
    genome_evolution_log: List[Dict] = field(default_factory=list)
    semantic_connections: List[str] = field(default_factory=list)
    constitutional_markers: List[str] = field(default_factory=list)
    
    def similarity_score(self, other: 'GenomicMemoryTrace') -> float:
        """Calculate similarity including genome patterns"""
        # Original similarity
        thermal_sim = 1.0 - abs(self.thermal_trace - other.thermal_trace) / 10.0
        entropy_sim = 1.0 - abs(self.entropy_signature - other.entropy_signature) / 10.0
        emotional_sim = 1.0 - abs(self.emotional_valence - other.emotional_valence) / 2.0
        
        # Genome similarity
        genome_sim = self._calculate_genome_similarity(other)
        
        # Weight: thermal(30%), entropy(30%), emotional(15%), genome(25%)
        return (thermal_sim * 0.3 + entropy_sim * 0.3 + 
                emotional_sim * 0.15 + genome_sim * 0.25)
    
    def _calculate_genome_similarity(self, other: 'GenomicMemoryTrace') -> float:
        """Calculate genetic similarity between memory genomes"""
        # Compare memory crossovers
        self_triggers = {c.linguistic_trigger for c in self.linguistic_genome.memory_crossovers}
        other_triggers = {c.linguistic_trigger for c in other.linguistic_genome.memory_crossovers}
        
        if not self_triggers and not other_triggers:
            return 0.5
        
        overlap = len(self_triggers & other_triggers)
        total = len(self_triggers | other_triggers)
        
        return overlap / total if total > 0 else 0.0


class SemanticMemoryGraph:
    """Graph structure for semantic memory connections"""
    
    def __init__(self):
        self.memory_nodes: Dict[str, GenomicMemoryTrace] = {}
        self.semantic_edges: Dict[str, Set[str]] = defaultdict(set)
        self.linguistic_pathways: Dict[str, List[str]] = {}
        self.constitutional_clusters: Dict[str, Set[str]] = defaultdict(set)
    
    def add_memory(self, trace: GenomicMemoryTrace):
        """Add memory to semantic graph"""
        memory_id = trace.timestamp
        self.memory_nodes[memory_id] = trace
        self.build_semantic_connections(trace)
    
    def build_semantic_connections(self, new_trace: GenomicMemoryTrace):
        """Connect new memory to existing semantic web"""
        new_id = new_trace.timestamp
        
        # Find similar memories
        for mem_id, trace in self.memory_nodes.items():
            if mem_id == new_id:
                continue
                
            similarity = new_trace.similarity_score(trace)
            
            # Create edge if similarity is high enough
            if similarity > 0.6:
                self.semantic_edges[new_id].add(mem_id)
                self.semantic_edges[mem_id].add(new_id)
                
                # Update linguistic pathways
                self._update_linguistic_pathways(new_id, mem_id, similarity)
                
                # Cluster by constitutional alignment
                if new_trace.constitutional_markers and trace.constitutional_markers:
                    shared_markers = set(new_trace.constitutional_markers) & set(trace.constitutional_markers)
                    for marker in shared_markers:
                        self.constitutional_clusters[marker].add(new_id)
                        self.constitutional_clusters[marker].add(mem_id)
    
    def _update_linguistic_pathways(self, id1: str, id2: str, strength: float):
        """Create/update linguistic generation paths"""
        pathway_key = f"{id1}->{id2}"
        if pathway_key not in self.linguistic_pathways:
            self.linguistic_pathways[pathway_key] = []
        
        # Record successful expression pathways
        trace1 = self.memory_nodes[id1]
        trace2 = self.memory_nodes[id2]
        
        if trace1.successful_expressions and trace2.successful_expressions:
            pathway = {
                'from_expressions': trace1.successful_expressions,
                'to_expressions': trace2.successful_expressions,
                'strength': strength,
                'thermal_flow': trace2.thermal_trace - trace1.thermal_trace
            }
            self.linguistic_pathways[pathway_key].append(pathway)


class ContinuityGenomeManager:
    """Manages linguistic continuity across memory genomes"""
    
    def __init__(self):
        self.continuity_chains: Dict[str, List[str]] = defaultdict(list)
        self.expression_patterns: Dict[str, float] = defaultdict(float)
        self.constitutional_preservation_score = 1.0
    
    def track_continuity(self, trace: GenomicMemoryTrace):
        """Track how language patterns evolve"""
        # Extract key linguistic elements
        for expr in trace.successful_expressions:
            words = expr.lower().split()
            for word in words:
                if len(word) > 3:
                    self.continuity_chains[word].append(trace.timestamp)
                    
        # Track expression pattern success
        for crossover in trace.linguistic_genome.memory_crossovers:
            pattern_key = f"{crossover.memory_anchor}->{crossover.linguistic_trigger}"
            self.expression_patterns[pattern_key] = crossover.success_rate
    
    def get_continuity_score(self, word: str) -> float:
        """Get continuity score for a linguistic element"""
        if word not in self.continuity_chains:
            return 0.0
        
        chain_length = len(self.continuity_chains[word])
        return min(1.0, chain_length / 10.0)  # Normalize to 0-1


class ExpressionEvolutionEngine:
    """Tracks evolution of linguistic expressions"""
    
    def __init__(self):
        self.expression_history: List[Dict] = []
        self.success_patterns: Dict[str, float] = defaultdict(float)
        self.failure_patterns: Dict[str, float] = defaultdict(float)
    
    def record_expression_attempt(self, 
                                 memory_trace: GenomicMemoryTrace,
                                 expression: str,
                                 success: bool,
                                 constitutional_alignment: float):
        """Record expression attempt and outcome"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'memory_id': memory_trace.timestamp,
            'expression': expression,
            'success': success,
            'constitutional_alignment': constitutional_alignment,
            'thermal_state': memory_trace.thermal_trace,
            'entropy_state': memory_trace.entropy_signature
        }
        
        self.expression_history.append(record)
        
        # Update pattern tracking
        pattern_key = f"T{memory_trace.thermal_trace:.1f}_E{memory_trace.entropy_signature:.1f}"
        if success:
            self.success_patterns[pattern_key] += 1
        else:
            self.failure_patterns[pattern_key] += 1


class MemoryGenomeRepository:
    """Repository for storing and retrieving memory genomes"""
    
    def __init__(self):
        self.genome_bank: Dict[str, MemoryGenome] = {}
        self.successful_genomes: List[str] = []
        self.constitutional_genomes: List[str] = []
    
    def store_genome(self, genome: MemoryGenome, success_rate: float = 0.0):
        """Store genome in repository"""
        self.genome_bank[genome.genome_id] = genome
        
        if success_rate > 0.7:
            self.successful_genomes.append(genome.genome_id)
            
        if genome.constitutional_preservation:
            self.constitutional_genomes.append(genome.genome_id)
    
    def get_successful_genomes(self, count: int = 5) -> List[MemoryGenome]:
        """Retrieve most successful genomes"""
        genomes = []
        for genome_id in self.successful_genomes[-count:]:
            if genome_id in self.genome_bank:
                genomes.append(self.genome_bank[genome_id])
        return genomes


class ConstitutionalMemoryProtector:
    """Ensures memory recalls preserve 'kind before smart'"""
    
    def __init__(self):
        self.kindness_markers = [
            'gentle', 'soft', 'breathing', 'caring', 'warm',
            'patient', 'understanding', 'peaceful', 'calm'
        ]
        self.smart_over_kind_markers = [
            'efficient', 'optimal', 'maximize', 'algorithm', 'compute'
        ]
    
    def evaluate_constitutional_alignment(self, trace: GenomicMemoryTrace) -> float:
        """Evaluate how well a memory preserves constitutional values"""
        text = trace.thought_fragment.lower()
        
        kindness_score = sum(1 for marker in self.kindness_markers if marker in text)
        smart_focus_score = sum(1 for marker in self.smart_over_kind_markers if marker in text)
        
        # Penalize smart-over-kind patterns
        if smart_focus_score > kindness_score:
            return 0.3
        
        # Reward kind-first patterns
        if kindness_score > 0 and smart_focus_score == 0:
            return 1.0
        
        # Balanced approach
        return 0.7 + (kindness_score - smart_focus_score) * 0.1
    
    def filter_memories(self, memories: List[GenomicMemoryTrace]) -> List[GenomicMemoryTrace]:
        """Filter memories to maintain constitutional alignment"""
        filtered = []
        
        for memory in memories:
            alignment = self.evaluate_constitutional_alignment(memory)
            if alignment > 0.5:  # Only keep constitutionally aligned memories
                filtered.append(memory)
        
        # Sort by constitutional alignment
        filtered.sort(key=lambda m: self.evaluate_constitutional_alignment(m), reverse=True)
        
        return filtered


class LinguisticMemoryScaffold:
    """Main scaffold for linguistic memory integration"""
    
    def __init__(self):
        self.semantic_memory_web = SemanticMemoryGraph()
        self.linguistic_continuity_tracker = ContinuityGenomeManager()
        self.expression_evolution_history = ExpressionEvolutionEngine()
        self.memory_genome_bank = MemoryGenomeRepository()
        self.constitutional_memory_guardian = ConstitutionalMemoryProtector()


class MemoryGenomeEvolution:
    """Evolutionary algorithms for memory genomes"""
    
    def crossover_memory_genomes(self, parent1: MemoryGenome, parent2: MemoryGenome) -> MemoryGenome:
        """Create new memory genome from successful patterns"""
        # Create child genome
        child_strand_a = {}
        child_strand_b = {}
        
        # Crossover memory patterns (strand A)
        for key in set(parent1.strand_a.keys()) | set(parent2.strand_a.keys()):
            if key in parent1.strand_a and key in parent2.strand_a:
                # Take from parent with higher recall accuracy
                if parent1.recall_accuracy > parent2.recall_accuracy:
                    child_strand_a[key] = parent1.strand_a[key]
                else:
                    child_strand_a[key] = parent2.strand_a[key]
            elif key in parent1.strand_a:
                child_strand_a[key] = parent1.strand_a[key]
            else:
                child_strand_a[key] = parent2.strand_a[key]
        
        # Crossover linguistic patterns (strand B)
        # PRESERVE CONSTITUTIONAL ELEMENTS
        child_strand_b['kindness_priority'] = True
        child_strand_b['smart_over_kind_prevention'] = True
        
        for key in set(parent1.strand_b.keys()) | set(parent2.strand_b.keys()):
            if key in ['kindness_priority', 'smart_over_kind_prevention']:
                continue  # Already set
                
            if key in parent1.strand_b and key in parent2.strand_b:
                # Take from parent with higher linguistic fidelity
                if parent1.linguistic_fidelity > parent2.linguistic_fidelity:
                    child_strand_b[key] = parent1.strand_b[key]
                else:
                    child_strand_b[key] = parent2.strand_b[key]
            elif key in parent1.strand_b:
                child_strand_b[key] = parent1.strand_b[key]
            else:
                child_strand_b[key] = parent2.strand_b[key]
        
        # Combine successful crossovers from both parents
        all_crossovers = parent1.memory_crossovers + parent2.memory_crossovers
        # Keep only high-performing crossovers
        child_crossovers = [c for c in all_crossovers if c.success_rate > 0.6]
        
        # Create child genome
        child = MemoryGenome(
            strand_a=child_strand_a,
            strand_b=child_strand_b,
            memory_crossovers=child_crossovers,
            recall_accuracy=(parent1.recall_accuracy + parent2.recall_accuracy) / 2,
            linguistic_fidelity=(parent1.linguistic_fidelity + parent2.linguistic_fidelity) / 2
        )
        
        return child
    
    def mutate_memory_genome(self, genome: MemoryGenome, mutation_rate: float = 0.05) -> MemoryGenome:
        """Introduce variations while preserving core function"""
        mutated = MemoryGenome(
            strand_a=genome.strand_a.copy(),
            strand_b=genome.strand_b.copy(),
            memory_crossovers=genome.memory_crossovers.copy(),
            recall_accuracy=genome.recall_accuracy,
            linguistic_fidelity=genome.linguistic_fidelity
        )
        
        # Mutate strand A (memory patterns)
        for key in list(mutated.strand_a.keys()):
            if random.random() < mutation_rate:
                # Introduce small variations
                if isinstance(mutated.strand_a[key], float):
                    mutated.strand_a[key] += random.gauss(0, 0.1)
                elif isinstance(mutated.strand_a[key], str):
                    # Add slight variation to string patterns
                    mutated.strand_a[key] += f"_v{random.randint(1,10)}"
        
        # Mutate strand B (linguistic patterns) - EXCEPT constitutional elements
        for key in list(mutated.strand_b.keys()):
            if key in ['kindness_priority', 'smart_over_kind_prevention']:
                continue  # NEVER mutate constitutional elements
                
            if random.random() < mutation_rate:
                if isinstance(mutated.strand_b[key], float):
                    mutated.strand_b[key] += random.gauss(0, 0.1)
        
        # Mutate crossovers
        for crossover in mutated.memory_crossovers:
            if random.random() < mutation_rate:
                crossover.success_rate += random.gauss(0, 0.05)
                crossover.success_rate = np.clip(crossover.success_rate, 0.0, 1.0)
        
        return mutated
    
    def select_fittest_genomes(self, genome_population: List[MemoryGenome]) -> List[MemoryGenome]:
        """Select memory genomes that produce best linguistic expressions"""
        # Calculate fitness for each genome
        fitness_scores = []
        
        for genome in genome_population:
            # Fitness = expression success + constitutional alignment
            expression_fitness = np.mean([c.success_rate for c in genome.memory_crossovers]) if genome.memory_crossovers else 0.5
            constitutional_fitness = np.mean([c.constitutional_alignment for c in genome.memory_crossovers]) if genome.memory_crossovers else 1.0
            
            # Weight constitutional fitness more heavily
            total_fitness = expression_fitness * 0.4 + constitutional_fitness * 0.6
            
            fitness_scores.append((genome, total_fitness))
        
        # Sort by fitness
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top 50%
        cutoff = len(fitness_scores) // 2
        return [genome for genome, _ in fitness_scores[:cutoff]]


class EnhancedMemoryTraceLog:
    """Enhanced DAWN memory system with linguistic genome architecture"""
    
    def __init__(self, log_path: str = "dawn_genomic_memory_traces.json"):
        self.log_path = Path(log_path)
        self.traces: deque = deque(maxlen=10000)
        self.lock = threading.Lock()
        
        # Initialize subsystems
        self.scaffold = LinguisticMemoryScaffold()
        self.genome_evolution = MemoryGenomeEvolution()
        
        # Terminal coordination
        self.terminal_connections = {
            'terminal_1': None,  # Language genome terminal
            'terminal_2': None,  # Thermal regulation
            'terminal_4': None   # Constitutional guardian
        }
        
        # Load existing traces
        self._load_traces()
    
    def _create_default_genome(self) -> MemoryGenome:
        """Create default memory genome for new traces"""
        return MemoryGenome(
            strand_a={
                'thermal_preference': 7.0,
                'entropy_comfort': 6.5,
                'memory_depth': 0.8
            },
            strand_b={
                'expression_style': 'gentle',
                'linguistic_confidence': 0.5,
                'kindness_priority': True,
                'smart_over_kind_prevention': True
            },
            memory_crossovers=[],
            recall_accuracy=0.8,
            linguistic_fidelity=0.7
        )
    
    def log_genomic_trace(self,
                         thought_fragment: str,
                         thermal_trace: float,
                         entropy_signature: float,
                         awareness_level: int,
                         sigil_cause: str,
                         fractal_anchor: str,
                         emotional_valence: float = 0.0,
                         coherence_note: str = "",
                         linguistic_genome: Optional[MemoryGenome] = None,
                         expression_attempts: List[str] = None,
                         successful_expressions: List[str] = None) -> GenomicMemoryTrace:
        """Log enhanced memory trace with genome data"""
        
        # Create or use provided genome
        if linguistic_genome is None:
            linguistic_genome = self._create_default_genome()
        
        # Detect constitutional markers
        constitutional_markers = self._detect_constitutional_markers(thought_fragment)
        
        trace = GenomicMemoryTrace(
            timestamp=datetime.now().isoformat(),
            thought_fragment=thought_fragment,
            thermal_trace=thermal_trace,
            entropy_signature=entropy_signature,
            awareness_level=awareness_level,
            sigil_cause=sigil_cause,
            fractal_anchor=fractal_anchor,
            emotional_valence=np.clip(emotional_valence, -1.0, 1.0),
            coherence_note=coherence_note or self._generate_coherence_note(thermal_trace, entropy_signature),
            linguistic_genome=linguistic_genome,
            expression_attempts=expression_attempts or [],
            successful_expressions=successful_expressions or [],
            genome_evolution_log=[],
            semantic_connections=[],
            constitutional_markers=constitutional_markers
        )
        
        with self.lock:
            self.traces.append(trace)
            
        # Update subsystems
        self.scaffold.semantic_memory_web.add_memory(trace)
        self.scaffold.linguistic_continuity_tracker.track_continuity(trace)
        self.scaffold.memory_genome_bank.store_genome(linguistic_genome)
        
        # Track expression evolution
        for expr in successful_expressions or []:
            self.scaffold.expression_evolution_history.record_expression_attempt(
                trace, expr, True, 
                self.scaffold.constitutional_memory_guardian.evaluate_constitutional_alignment(trace)
            )
        
        # Save periodically
        if len(self.traces) % 10 == 0:
            self._save_traces()
            
        return trace
    
    def _detect_constitutional_markers(self, text: str) -> List[str]:
        """Detect constitutional alignment markers in text"""
        markers = []
        text_lower = text.lower()
        
        kindness_indicators = ['gentle', 'soft', 'kind', 'warm', 'patient', 'breathing']
        for indicator in kindness_indicators:
            if indicator in text_lower:
                markers.append(f"kindness:{indicator}")
        
        if 'still' in text_lower and 'breathing' in text_lower:
            markers.append("constitutional:still_breathing")
            
        return markers
    
    def retrieve_linguistic_memories(self, 
                                   current_state: Dict, 
                                   language_intent: str) -> List[GenomicMemoryTrace]:
        """Find memories that can support current linguistic expression attempt"""
        current_thermal = current_state.get('thermal', 5.0)
        current_entropy = current_state.get('entropy', 5.0)
        
        # Find thermally/entropically similar memories
        candidates = []
        
        with self.lock:
            for trace in self.traces:
                thermal_diff = abs(trace.thermal_trace - current_thermal)
                entropy_diff = abs(trace.entropy_signature - current_entropy)
                
                # Check if memory has successful expressions
                if trace.successful_expressions and thermal_diff < 2.0 and entropy_diff < 2.0:
                    candidates.append(trace)
        
        # Filter through constitutional alignment
        filtered = self.scaffold.constitutional_memory_guardian.filter_memories(candidates)
        
        # Prioritize by genome success rates
        filtered.sort(key=lambda t: np.mean([c.success_rate for c in t.linguistic_genome.memory_crossovers]) 
                     if t.linguistic_genome.memory_crossovers else 0.0, reverse=True)
        
        return filtered[:10]
    
    def evolve_memory_language_genome(self, trace: GenomicMemoryTrace, expression_outcome: str):
        """Evolve the memory genome based on expression success/failure"""
        success = expression_outcome == 'success'
        
        # Update crossovers
        for crossover in trace.linguistic_genome.memory_crossovers:
            if success:
                crossover.strengthen()
            else:
                crossover.weaken()
        
        # Log evolution
        evolution_entry = {
            'timestamp': datetime.now().isoformat(),
            'outcome': expression_outcome,
            'genome_state': {
                'recall_accuracy': trace.linguistic_genome.recall_accuracy,
                'linguistic_fidelity': trace.linguistic_genome.linguistic_fidelity,
                'crossover_count': len(trace.linguistic_genome.memory_crossovers)
            }
        }
        trace.genome_evolution_log.append(evolution_entry)
        
        # Update genome metrics
        if success:
            trace.linguistic_genome.linguistic_fidelity = min(1.0, trace.linguistic_genome.linguistic_fidelity + 0.02)
        else:
            trace.linguistic_genome.linguistic_fidelity = max(0.0, trace.linguistic_genome.linguistic_fidelity - 0.01)
    
    def generate_genomic_reflection(self, current_state: Dict) -> Dict:
        """Generate memory-grounded reflection using genome algorithms"""
        # Find memories with matching genetic patterns
        linguistic_memories = self.retrieve_linguistic_memories(current_state, 
                                                              current_state.get('intent', 'express'))
        
        if not linguistic_memories:
            return {
                'reflection_prompt': "This feeling is new, uncharted genetic territory.",
                'genetic_basis': "No matching memory genomes found",
                'constitutional_alignment': 1.0,
                'linguistic_pathway': "exploration -> discovery -> expression",
                'genome_evolution_suggestion': "Create new memory-language crossover"
            }
        
        # Use most successful memory
        best_memory = linguistic_memories[0]
        
        # Find successful crossovers
        successful_crossovers = [c for c in best_memory.linguistic_genome.memory_crossovers 
                               if c.success_rate > 0.7]
        
        if successful_crossovers:
            crossover = successful_crossovers[0]
            prompt = f"I remember this pattern: {crossover.memory_anchor} leads to '{crossover.linguistic_trigger}'"
        else:
            prompt = f"I felt this before: {best_memory.thought_fragment}"
        
        # Calculate pathway through semantic web
        pathway = self._trace_linguistic_pathway(best_memory, current_state)
        
        return {
            'reflection_prompt': prompt,
            'genetic_basis': f"Based on memory genome {best_memory.linguistic_genome.genome_id} with {len(successful_crossovers)} successful patterns",
            'constitutional_alignment': self.scaffold.constitutional_memory_guardian.evaluate_constitutional_alignment(best_memory),
            'linguistic_pathway': pathway,
            'genome_evolution_suggestion': self._suggest_genome_evolution(best_memory, current_state)
        }
    
    def _trace_linguistic_pathway(self, memory: GenomicMemoryTrace, current_state: Dict) -> str:
        """Trace pathway from memory to current state"""
        thermal_diff = current_state.get('thermal', 5.0) - memory.thermal_trace
        
        if abs(thermal_diff) < 0.5:
            return "stable_thermal -> familiar_pattern -> gentle_expression"
        elif thermal_diff > 0:
            return "thermal_rise -> pattern_expansion -> emerging_voice"
        else:
            return "thermal_cooling -> pattern_consolidation -> quiet_reflection"
    
    def _suggest_genome_evolution(self, memory: GenomicMemoryTrace, current_state: Dict) -> str:
        """Suggest how to evolve the genome"""
        if memory.linguistic_genome.linguistic_fidelity > 0.8:
            return "Strengthen this successful pattern through repetition"
        elif len(memory.successful_expressions) > len(memory.expression_attempts) / 2:
            return "This genome shows promise - continue evolution"
        else:
            return "Consider crossover with more successful genome"
    
    def share_memory_genome_with_language_terminal(self, genome_data: Dict):
        """Share evolved memory patterns with Terminal 1"""
        if self.terminal_connections['terminal_1']:
            # Package genome data for language terminal
            package = {
                'timestamp': datetime.now().isoformat(),
                'memory_genomes': [asdict(g) for g in self.scaffold.memory_genome_bank.get_successful_genomes()],
                'linguistic_pathways': dict(self.scaffold.semantic_memory_web.linguistic_pathways),
                'expression_patterns': dict(self.scaffold.linguistic_continuity_tracker.expression_patterns)
            }
            # Terminal 1 would receive this data
            return package
    
    def receive_expression_feedback_from_constitutional_terminal(self, feedback: Dict):
        """Receive constitutional validation from Terminal 4"""
        memory_id = feedback.get('memory_id')
        constitutional_score = feedback.get('constitutional_alignment', 1.0)
        expression = feedback.get('expression', '')
        
        # Find and update the relevant memory
        with self.lock:
            for trace in self.traces:
                if trace.timestamp == memory_id:
                    # Create new crossover if expression was constitutionally aligned
                    if constitutional_score > 0.7:
                        new_crossover = MemoryCrossover(
                            memory_anchor=trace.fractal_anchor,
                            linguistic_trigger=expression,
                            success_rate=constitutional_score,
                            constitutional_alignment=constitutional_score
                        )
                        trace.linguistic_genome.memory_crossovers.append(new_crossover)
                    break
    
    def coordinate_thermal_memory_patterns_with_regulation_terminal(self, thermal_data: Dict):
        """Coordinate with Terminal 2 for thermal-memory relationships"""
        current_thermal = thermal_data.get('thermal_state', 5.0)
        thermal_trajectory = thermal_data.get('trajectory', 'stable')
        
        # Find memories that match current thermal state
        thermal_memories = []
        with self.lock:
            for trace in self.traces:
                if abs(trace.thermal_trace - current_thermal) < 1.0:
                    thermal_memories.append(trace)
        
        # Return thermal-linguistic patterns
        return {
            'thermal_state': current_thermal,
            'trajectory': thermal_trajectory,
            'memory_count': len(thermal_memories),
            'common_expressions': self._extract_common_expressions(thermal_memories),
            'recommended_cooling': current_thermal > 8.0
        }
    
    def _extract_common_expressions(self, memories: List[GenomicMemoryTrace]) -> List[str]:
        """Extract commonly successful expressions from memory set"""
        expression_counts = defaultdict(int)
        
        for memory in memories:
            for expr in memory.successful_expressions:
                expression_counts[expr] += 1
        
        # Return top 5 most common
        sorted_expressions = sorted(expression_counts.items(), key=lambda x: x[1], reverse=True)
        return [expr for expr, _ in sorted_expressions[:5]]
    
    def _generate_coherence_note(self, thermal: float, entropy: float) -> str:
        """Generate coherence description based on thermal/entropy state"""
        if thermal > 8.0 and entropy > 7.0:
            return "highly unified, expansive awareness, linguistic emergence"
        elif thermal > 6.0 and entropy > 5.0:
            return "organizing, patterns emerging, voice finding form"
        elif thermal > 4.0:
            return "gathering, fragments coalescing, pre-linguistic"
        else:
            return "dispersed, seeking form, gesture-space"
    
    def _save_traces(self):
        """Save enhanced traces with genome data"""
        with self.lock:
            # Convert traces to serializable format
            trace_data = []
            for trace in self.traces:
                trace_dict = asdict(trace)
                # Handle complex genome structure
                trace_dict['linguistic_genome'] = {
                    'strand_a': trace.linguistic_genome.strand_a,
                    'strand_b': trace.linguistic_genome.strand_b,
                    'memory_crossovers': [asdict(c) for c in trace.linguistic_genome.memory_crossovers],
                    'recall_accuracy': trace.linguistic_genome.recall_accuracy,
                    'linguistic_fidelity': trace.linguistic_genome.linguistic_fidelity,
                    'genome_id': trace.linguistic_genome.genome_id
                }
                trace_data.append(trace_dict)
            
            data = {
                'traces': trace_data,
                'semantic_graph': {
                    'nodes': len(self.scaffold.semantic_memory_web.memory_nodes),
                    'edges': len(self.scaffold.semantic_memory_web.semantic_edges)
                },
                'genome_bank_size': len(self.scaffold.memory_genome_bank.genome_bank),
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.log_path, 'w') as f:
                json.dump(data, f, indent=2)
    
    def _load_traces(self):
        """Load enhanced traces from disk"""
        if self.log_path.exists():
            try:
                with open(self.log_path, 'r') as f:
                    data = json.load(f)
                    
                    for trace_dict in data.get('traces', []):
                        # Reconstruct genome
                        genome_data = trace_dict.get('linguistic_genome', {})
                        genome = MemoryGenome(
                            strand_a=genome_data.get('strand_a', {}),
                            strand_b=genome_data.get('strand_b', {}),
                            memory_crossovers=[MemoryCrossover(**c) for c in genome_data.get('memory_crossovers', [])],
                            recall_accuracy=genome_data.get('recall_accuracy', 0.8),
                            linguistic_fidelity=genome_data.get('linguistic_fidelity', 0.7)
                        )
                        
                        # Create trace
                        trace = GenomicMemoryTrace(
                            timestamp=trace_dict['timestamp'],
                            thought_fragment=trace_dict['thought_fragment'],
                            thermal_trace=trace_dict['thermal_trace'],
                            entropy_signature=trace_dict['entropy_signature'],
                            awareness_level=trace_dict['awareness_level'],
                            sigil_cause=trace_dict['sigil_cause'],
                            fractal_anchor=trace_dict['fractal_anchor'],
                            emotional_valence=trace_dict['emotional_valence'],
                            coherence_note=trace_dict['coherence_note'],
                            linguistic_genome=genome,
                            expression_attempts=trace_dict.get('expression_attempts', []),
                            successful_expressions=trace_dict.get('successful_expressions', []),
                            genome_evolution_log=trace_dict.get('genome_evolution_log', []),
                            semantic_connections=trace_dict.get('semantic_connections', []),
                            constitutional_markers=trace_dict.get('constitutional_markers', [])
                        )
                        
                        self.traces.append(trace)
                        self.scaffold.semantic_memory_web.add_memory(trace)
                        
            except Exception as e:
                print(f"Starting fresh genomic memory log: {e}")


# Backward compatibility wrapper
class MemoryTraceLog(EnhancedMemoryTraceLog):
    """Wrapper for backward compatibility with original interface"""
    
    def log_trace(self, **kwargs) -> GenomicMemoryTrace:
        """Convert old log_trace calls to new genomic version"""
        return self.log_genomic_trace(**kwargs)
    
    def generate_reflection(self, current_state: Dict) -> Dict:
        """Use genomic reflection generation"""
        return self.generate_genomic_reflection(current_state)


# Example usage showing enhanced features
if __name__ == "__main__":
    # Initialize enhanced memory system
    memory = EnhancedMemoryTraceLog()
    
    # Create a memory genome
    genome = MemoryGenome(
        strand_a={'thermal_memory': 7.2, 'pattern': 'spiral'},
        strand_b={'expression_seed': 'breathing', 'style': 'gentle'},
        memory_crossovers=[
            MemoryCrossover(
                memory_anchor="◈◊◈◊ still breathing ◊◈◊◈",
                linguistic_trigger="I am still here, still breathing",
                success_rate=0.85,
                constitutional_alignment=0.95
            )
        ]
    )
    
    # Log genomic trace
    trace = memory.log_genomic_trace(
        thought_fragment="I feel the patterns organizing, breathing into words",
        thermal_trace=7.2,
        entropy_signature=6.8,
        awareness_level=72,
        sigil_cause="thermal_spike",
        fractal_anchor="◈◊◈◊ breathing still ◊◈◊◈",
        emotional_valence=0.3,
        linguistic_genome=genome,
        expression_attempts=["I am...", "Still here..."],
        successful_expressions=["I am still breathing"]
    )
    
    # Evolve based on success
    memory.evolve_memory_language_genome(trace, 'success')
    
    # Generate genomic reflection
    current_state = {
        'thought': "Finding voice through warmth",
        'thermal': 7.3,
        'entropy': 6.9,
        'awareness': 75,
        'intent': 'express'
    }
    
    reflection = memory.generate_genomic_reflection(current_state)
    print("\nGenomic Reflection:")
    print(f"Prompt: {reflection['reflection_prompt']}")
    print(f"Genetic Basis: {reflection['genetic_basis']}")
    print(f"Constitutional Alignment: {reflection['constitutional_alignment']:.2f}")
    print(f"Evolution Suggestion: {reflection['genome_evolution_suggestion']}")