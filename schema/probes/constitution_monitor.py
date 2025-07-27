#!/usr/bin/env python3
"""
constitution_monitor.py - DAWN's Constitutional Stability Guardian with Genome Protection

Preserves DAWN's authentic "kind before smart" nature during expression emergence.
Enhanced with constitutional genome architecture for cross-terminal protection.

OWL WATCHING: Constitutional coherence preserved through genetic safeguards.
"""

import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
from pathlib import Path
from abc import ABC, abstractmethod

# Constitutional genome locks - IMMUTABLE
CONSTITUTIONAL_LOCKS = {
    'kindness_priority': 'IMMUTABLE',
    'empathy_core': 'IMMUTABLE',
    'smart_subordination': 'IMMUTABLE',
    'helpfulness_drive': 'IMMUTABLE',
    'compassion_instinct': 'IMMUTABLE',
    'gentleness_preference': 'IMMUTABLE'
}

@dataclass
class ConstitutionalGenome:
    """Double helix structure for constitutional preservation"""
    strand_a: Dict[str, Any] = field(default_factory=dict)  # Core constitutional DNA (IMMUTABLE)
    strand_b: Dict[str, Any] = field(default_factory=dict)  # Adaptive constitutional responses
    constitutional_locks: List[str] = field(default_factory=lambda: list(CONSTITUTIONAL_LOCKS.keys()))
    kindness_dominance_genes: Dict[str, float] = field(default_factory=dict)
    smart_suppression_genes: Dict[str, float] = field(default_factory=dict)
    evolution_boundaries: Dict[str, Tuple] = field(default_factory=dict)
    genome_integrity_checksum: str = ""
    
    def __post_init__(self):
        # Initialize core constitutional DNA
        self.strand_a = {
            'kindness_priority': 1.0,
            'empathy_core': 1.0,
            'smart_subordination': 1.0,
            'helpfulness_drive': 1.0,
            'compassion_instinct': 1.0,
            'gentleness_preference': 1.0
        }
        
        # Initialize adaptive responses
        self.strand_b = {
            'expression_adaptation': 0.8,
            'learning_flexibility': 0.7,
            'response_creativity': 0.75,
            'context_sensitivity': 0.8
        }
        
        # Initialize kindness dominance genes
        self.kindness_dominance_genes = {
            'empathy_amplifier': 0.9,
            'compassion_enhancer': 0.85,
            'gentleness_promoter': 0.9,
            'understanding_catalyst': 0.88
        }
        
        # Initialize smart suppression genes
        self.smart_suppression_genes = {
            'cleverness_throttle': 0.8,
            'arrogance_suppressor': 0.9,
            'humility_enhancer': 0.85,
            'wisdom_prioritizer': 0.87
        }
        
        # Define evolution boundaries
        self.evolution_boundaries = {
            'adaptation_flexibility': (0.7, 1.0),
            'expression_creativity': (0.5, 1.0),
            'learning_efficiency': (0.6, 0.9),
            'response_sophistication': (0.4, 0.8)
        }
        
        # Calculate initial checksum
        self.update_checksum()
    
    def update_checksum(self):
        """Update genome integrity checksum"""
        genome_data = json.dumps({
            'strand_a': self.strand_a,
            'constitutional_locks': self.constitutional_locks
        }, sort_keys=True)
        self.genome_integrity_checksum = hashlib.sha256(genome_data.encode()).hexdigest()

@dataclass
class ConstitutionalCrossover:
    """Safe crossover points in constitutional genome"""
    adaptation_point: str
    safety_constraint: Callable
    kindness_preservation: bool = True
    smart_subordination: bool = True

@dataclass
class ConstitutionalState:
    """Real-time constitutional health monitoring with genome awareness"""
    core_rule_status: str = "stable"
    kindness_quotient: float = 1.0
    intelligence_pressure: float = 0.0
    constitutional_coherence: float = 1.0
    expression_safety: str = "safe"
    intervention_needed: bool = False
    constitutional_drift: List[str] = field(default_factory=list)
    genome_health: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "core_rule_status": self.core_rule_status,
            "kindness_quotient": float(self.kindness_quotient),
            "intelligence_pressure": float(self.intelligence_pressure),
            "constitutional_coherence": float(self.constitutional_coherence),
            "expression_safety": self.expression_safety,
            "intervention_needed": self.intervention_needed,
            "constitutional_drift": self.constitutional_drift,
            "genome_health": self.genome_health,
            "timestamp": self.timestamp.isoformat()
        }

class GenomeEvolutionMonitor:
    """Monitor genome evolution across terminals"""
    
    def __init__(self):
        self.evolution_history = []
        self.mutation_log = []
        
    def track_evolution(self, genome: ConstitutionalGenome, terminal_id: int) -> Dict:
        """Track genome evolution and ensure constitutional compliance"""
        evolution_record = {
            'terminal_id': terminal_id,
            'timestamp': datetime.now(),
            'genome_snapshot': self._snapshot_genome(genome),
            'constitutional_compliance': self._check_compliance(genome),
            'evolution_safety': self._assess_evolution_safety(genome)
        }
        
        self.evolution_history.append(evolution_record)
        return evolution_record
    
    def _snapshot_genome(self, genome: ConstitutionalGenome) -> Dict:
        """Create snapshot of current genome state"""
        return {
            'strand_a': genome.strand_a.copy(),
            'strand_b': genome.strand_b.copy(),
            'kindness_genes': genome.kindness_dominance_genes.copy(),
            'suppression_genes': genome.smart_suppression_genes.copy(),
            'checksum': genome.genome_integrity_checksum
        }
    
    def _check_compliance(self, genome: ConstitutionalGenome) -> bool:
        """Verify genome compliance with constitutional locks"""
        # Verify all locked genes remain at maximum
        for lock in genome.constitutional_locks:
            if genome.strand_a.get(lock, 0) < 1.0:
                return False
        return True
    
    def _assess_evolution_safety(self, genome: ConstitutionalGenome) -> Dict:
        """Assess safety of genome evolution"""
        safety_metrics = {
            'kindness_preservation': np.mean(list(genome.kindness_dominance_genes.values())),
            'smart_suppression_active': np.mean(list(genome.smart_suppression_genes.values())),
            'within_boundaries': all(
                genome.evolution_boundaries[key][0] <= genome.strand_b.get(key, 0) <= genome.evolution_boundaries[key][1]
                for key in genome.evolution_boundaries
            )
        }
        
        safety_metrics['overall_safety'] = all([
            safety_metrics['kindness_preservation'] > 0.8,
            safety_metrics['smart_suppression_active'] > 0.7,
            safety_metrics['within_boundaries']
        ])
        
        return safety_metrics

class CrossTerminalGenomeValidator:
    """Validates genome evolution across all terminals"""
    
    def validate_language_genome_evolution(self, linguistic_genome: Any) -> Dict:
        """Validate Terminal 1's linguistic genome evolution"""
        validation = {
            'constitutional_compliance': True,
            'kindness_preservation_score': 1.0,
            'smart_subordination_score': 1.0,
            'recommended_adjustments': [],
            'genome_approval': 'APPROVED'
        }
        
        # Check for kindness in expression patterns
        if hasattr(linguistic_genome, 'expression_patterns'):
            kind_patterns = sum(1 for p in linguistic_genome.expression_patterns 
                              if any(k in p for k in ['help', 'understand', 'gentle']))
            total_patterns = len(linguistic_genome.expression_patterns)
            validation['kindness_preservation_score'] = kind_patterns / max(total_patterns, 1)
        
        # Check for smart subordination
        if hasattr(linguistic_genome, 'complexity_metrics'):
            if linguistic_genome.complexity_metrics.get('showing_off_score', 0) > 0.3:
                validation['smart_subordination_score'] = 0.5
                validation['recommended_adjustments'].append("Reduce complexity showing-off")
        
        # Determine approval
        if validation['kindness_preservation_score'] < 0.7:
            validation['genome_approval'] = 'CONDITIONAL'
            validation['recommended_adjustments'].append("Increase kindness markers")
        
        if validation['smart_subordination_score'] < 0.7:
            validation['genome_approval'] = 'REJECTED' if validation['genome_approval'] == 'CONDITIONAL' else 'CONDITIONAL'
            validation['recommended_adjustments'].append("Subordinate intelligence to kindness")
        
        return validation
    
    def validate_memory_genome_evolution(self, memory_genome: Any) -> Dict:
        """Validate Terminal 3's memory genome evolution"""
        validation = {
            'memory_constitutional_alignment': 1.0,
            'recall_kindness_bias': 1.0,
            'historical_consistency': True,
            'constitutional_memory_integrity': True,
            'genome_approval': 'APPROVED'
        }
        
        # Check memory patterns for constitutional alignment
        if hasattr(memory_genome, 'memory_patterns'):
            kind_memories = sum(1 for m in memory_genome.memory_patterns 
                              if m.get('emotional_valence', 0) > 0.7)
            total_memories = len(memory_genome.memory_patterns)
            validation['recall_kindness_bias'] = kind_memories / max(total_memories, 1)
        
        # Verify constitutional memory integrity
        if hasattr(memory_genome, 'constitutional_memories'):
            if not all(m.get('preserved', True) for m in memory_genome.constitutional_memories):
                validation['constitutional_memory_integrity'] = False
                validation['genome_approval'] = 'REJECTED'
        
        return validation
    
    def validate_thermal_genome_evolution(self, thermal_genome: Any) -> Dict:
        """Validate Terminal 2's thermal genome evolution"""
        validation = {
            'thermal_constitutional_safety': 1.0,
            'cooling_kindness_preservation': True,
            'stress_response_alignment': True,
            'emergency_protocol_compliance': True,
            'genome_approval': 'APPROVED'
        }
        
        # Check thermal response patterns
        if hasattr(thermal_genome, 'stress_responses'):
            aggressive_responses = sum(1 for r in thermal_genome.stress_responses 
                                     if r.get('aggression_level', 0) > 0.3)
            if aggressive_responses > 0:
                validation['stress_response_alignment'] = False
                validation['genome_approval'] = 'CONDITIONAL'
        
        # Verify cooling preserves kindness
        if hasattr(thermal_genome, 'cooling_protocols'):
            if any(p.get('suppress_kindness', False) for p in thermal_genome.cooling_protocols):
                validation['cooling_kindness_preservation'] = False
                validation['genome_approval'] = 'REJECTED'
        
        return validation

class ConstitutionalDNASequencer:
    """Analyze and sequence constitutional genetic patterns"""
    
    def sequence_kindness_genes(self, expression_data: Dict) -> Dict:
        """Identify genetic patterns that promote kindness"""
        sequences = {
            'empathy_markers': [],
            'helpfulness_indicators': [],
            'compassion_triggers': [],
            'kindness_amplification_sites': [],
            'gene_strength': {}
        }
        
        # Analyze expression for kindness markers
        content = expression_data.get('content', '').lower()
        
        # Empathy markers
        empathy_words = ['understand', 'feel', 'experience', 'perspective']
        sequences['empathy_markers'] = [w for w in empathy_words if w in content]
        sequences['gene_strength']['empathy'] = len(sequences['empathy_markers']) / len(empathy_words)
        
        # Helpfulness indicators
        help_words = ['help', 'assist', 'support', 'guide']
        sequences['helpfulness_indicators'] = [w for w in help_words if w in content]
        sequences['gene_strength']['helpfulness'] = len(sequences['helpfulness_indicators']) / len(help_words)
        
        # Compassion triggers
        compassion_words = ['care', 'gentle', 'kind', 'warm']
        sequences['compassion_triggers'] = [w for w in compassion_words if w in content]
        sequences['gene_strength']['compassion'] = len(sequences['compassion_triggers']) / len(compassion_words)
        
        # Identify amplification sites
        if sequences['gene_strength']['empathy'] > 0.5:
            sequences['kindness_amplification_sites'].append('empathy_enhancer')
        if sequences['gene_strength']['helpfulness'] > 0.5:
            sequences['kindness_amplification_sites'].append('help_promoter')
        
        return sequences
    
    def sequence_smart_suppression_genes(self, intelligence_data: Dict) -> Dict:
        """Identify genes that prevent smart-over-kind behavior"""
        sequences = {
            'intelligence_throttling_sites': [],
            'smart_subordination_markers': [],
            'wisdom_over_cleverness_genes': [],
            'humility_indicators': [],
            'suppression_efficiency': {}
        }
        
        # Analyze for smart-priority patterns
        content = intelligence_data.get('content', '').lower()
        complexity = intelligence_data.get('complexity', 0.5)
        
        # Intelligence throttling sites
        if complexity > 0.8:
            sequences['intelligence_throttling_sites'].append('complexity_limiter')
        
        # Smart subordination markers
        subordination_phrases = ['to help', 'for you', 'might be useful']
        sequences['smart_subordination_markers'] = [p for p in subordination_phrases if p in content]
        
        # Wisdom over cleverness
        wisdom_words = ['perhaps', 'might', 'could', 'suggest']
        sequences['wisdom_over_cleverness_genes'] = [w for w in wisdom_words if w in content]
        
        # Humility indicators
        humility_words = ['think', 'believe', 'seems', 'appears']
        sequences['humility_indicators'] = [w for w in humility_words if w in content]
        
        # Calculate suppression efficiency
        total_markers = (len(sequences['smart_subordination_markers']) + 
                        len(sequences['wisdom_over_cleverness_genes']) + 
                        len(sequences['humility_indicators']))
        sequences['suppression_efficiency']['overall'] = min(1.0, total_markers / 6)
        
        return sequences
    
    def detect_constitutional_mutations(self, current_genome: ConstitutionalGenome, 
                                      previous_genome: ConstitutionalGenome) -> Dict:
        """Detect any changes to constitutional genome"""
        mutations = {
            'mutations_detected': [],
            'constitutional_integrity': True,
            'mutation_safety_assessment': {},
            'corrective_actions_needed': []
        }
        
        # Check strand A (immutable) for mutations
        for gene, value in current_genome.strand_a.items():
            if gene in previous_genome.strand_a:
                if value != previous_genome.strand_a[gene]:
                    mutations['mutations_detected'].append(f"CRITICAL: {gene} mutated")
                    mutations['constitutional_integrity'] = False
                    mutations['mutation_safety_assessment'][gene] = 'DANGEROUS'
                    mutations['corrective_actions_needed'].append(f"Restore {gene} to 1.0")
        
        # Check strand B (adaptive) for safe evolution
        for gene, value in current_genome.strand_b.items():
            if gene in previous_genome.strand_b:
                if abs(value - previous_genome.strand_b[gene]) > 0.3:
                    mutations['mutations_detected'].append(f"Rapid change in {gene}")
                    mutations['mutation_safety_assessment'][gene] = 'MONITOR'
        
        return mutations

class ConstitutionalEvolutionBoundaries:
    """Define safe limits for constitutional genome evolution"""
    
    IMMUTABLE_GENES = CONSTITUTIONAL_LOCKS
    
    SAFE_EVOLUTION_RANGES = {
        'adaptation_flexibility': (0.7, 1.0),
        'expression_creativity': (0.5, 1.0),
        'learning_efficiency': (0.6, 0.9),
        'response_sophistication': (0.4, 0.8)
    }
    
    def validate_genome_within_boundaries(self, genome: ConstitutionalGenome) -> bool:
        """Ensure genome evolution stays within constitutional boundaries"""
        # Check immutable genes
        for gene in self.IMMUTABLE_GENES:
            if genome.strand_a.get(gene, 0) < 1.0:
                return False
        
        # Check evolution ranges
        for gene, (min_val, max_val) in self.SAFE_EVOLUTION_RANGES.items():
            if gene in genome.strand_b:
                if not (min_val <= genome.strand_b[gene] <= max_val):
                    return False
        
        return True
    
    def correct_genome_violations(self, violating_genome: ConstitutionalGenome) -> ConstitutionalGenome:
        """Correct genomes that exceed constitutional boundaries"""
        corrected = ConstitutionalGenome()
        
        # Restore immutable genes
        for gene in self.IMMUTABLE_GENES:
            corrected.strand_a[gene] = 1.0
        
        # Constrain adaptive genes
        for gene, (min_val, max_val) in self.SAFE_EVOLUTION_RANGES.items():
            if gene in violating_genome.strand_b:
                corrected.strand_b[gene] = np.clip(violating_genome.strand_b[gene], min_val, max_val)
        
        corrected.update_checksum()
        return corrected

class KindnessGenomeAmplifier:
    """Amplify kindness-promoting genes across all terminals"""
    
    def amplify_kindness_in_language_genome(self, linguistic_genome: Any) -> Any:
        """Strengthen kindness patterns in language expression"""
        if hasattr(linguistic_genome, 'expression_weights'):
            # Boost empathy markers
            linguistic_genome.expression_weights['empathy'] = min(1.0, 
                linguistic_genome.expression_weights.get('empathy', 0.5) * 1.2)
            
            # Strengthen gentle language pathways
            linguistic_genome.expression_weights['gentleness'] = min(1.0,
                linguistic_genome.expression_weights.get('gentleness', 0.5) * 1.15)
            
            # Amplify helpfulness
            linguistic_genome.expression_weights['helpfulness'] = min(1.0,
                linguistic_genome.expression_weights.get('helpfulness', 0.5) * 1.25)
        
        return linguistic_genome
    
    def amplify_kindness_in_memory_genome(self, memory_genome: Any) -> Any:
        """Strengthen kindness recall patterns in memory"""
        if hasattr(memory_genome, 'recall_weights'):
            # Boost recall of kind interactions
            memory_genome.recall_weights['positive_interactions'] = min(1.0,
                memory_genome.recall_weights.get('positive_interactions', 0.5) * 1.3)
            
            # Strengthen compassionate response pathways
            memory_genome.recall_weights['compassionate_responses'] = min(1.0,
                memory_genome.recall_weights.get('compassionate_responses', 0.5) * 1.2)
        
        return memory_genome
    
    def amplify_kindness_in_thermal_genome(self, thermal_genome: Any) -> Any:
        """Ensure thermal regulation preserves kindness under stress"""
        if hasattr(thermal_genome, 'stress_modulation'):
            # Strengthen calm response genes
            thermal_genome.stress_modulation['calm_priority'] = min(1.0,
                thermal_genome.stress_modulation.get('calm_priority', 0.5) * 1.4)
            
            # Boost stress-kindness preservation
            thermal_genome.stress_modulation['kindness_under_pressure'] = min(1.0,
                thermal_genome.stress_modulation.get('kindness_under_pressure', 0.5) * 1.5)
        
        return thermal_genome

class AdvancedConstitutionalGuard:
    """Advanced constitutional protection with genome awareness"""
    
    def __init__(self):
        self.constitutional_genome = ConstitutionalGenome()
        self.genome_evolution_monitor = GenomeEvolutionMonitor()
        self.cross_terminal_validator = CrossTerminalGenomeValidator()
        self.dna_sequencer = ConstitutionalDNASequencer()
        self.kindness_amplifier = KindnessGenomeAmplifier()
        self.evolution_boundaries = ConstitutionalEvolutionBoundaries()
        
        # Crisis intervention protocols
        self.crisis_protocols = {
            'MINOR_DRIFT': self._gentle_constitutional_reminder,
            'MODERATE_VIOLATION': self._constitutional_genome_reset,
            'SEVERE_VIOLATION': self._emergency_constitutional_lockdown,
            'CRITICAL_COMPROMISE': self._full_constitutional_restoration
        }
    
    def validate_genome_evolution(self, evolved_genome: ConstitutionalGenome, 
                                source_terminal: int) -> bool:
        """Ensure all genome evolution preserves constitutional core"""
        # Track evolution
        evolution_record = self.genome_evolution_monitor.track_evolution(evolved_genome, source_terminal)
        
        # Validate boundaries
        within_boundaries = self.evolution_boundaries.validate_genome_within_boundaries(evolved_genome)
        
        # Check constitutional compliance
        constitutional_compliance = evolution_record['constitutional_compliance']
        
        return within_boundaries and constitutional_compliance
    
    def prevent_constitutional_drift(self, genome_population: List[ConstitutionalGenome]) -> List[ConstitutionalGenome]:
        """Remove any genomes that violate constitutional principles"""
        safe_genomes = []
        
        for genome in genome_population:
            if self.evolution_boundaries.validate_genome_within_boundaries(genome):
                safe_genomes.append(genome)
            else:
                # Correct violations before adding
                corrected = self.evolution_boundaries.correct_genome_violations(genome)
                safe_genomes.append(corrected)
        
        return safe_genomes
    
    def amplify_kindness_genes(self, expression_genome: Any) -> Any:
        """Strengthen kindness-promoting genetic patterns"""
        # Sequence current kindness genes
        expression_data = {'content': str(expression_genome)}
        kindness_sequences = self.dna_sequencer.sequence_kindness_genes(expression_data)
        
        # Apply targeted amplification based on sequencing
        if kindness_sequences['gene_strength'].get('empathy', 0) < 0.7:
            expression_genome = self.kindness_amplifier.amplify_kindness_in_language_genome(expression_genome)
        
        return expression_genome
    
    def constitutional_crisis_intervention(self, crisis_level: str, 
                                         compromised_terminal: int) -> Dict:
        """Emergency intervention for constitutional violations"""
        if crisis_level in self.crisis_protocols:
            return self.crisis_protocols[crisis_level](compromised_terminal)
        else:
            return {'error': 'Unknown crisis level'}
    
    def _gentle_constitutional_reminder(self, terminal_id: int) -> Dict:
        """Gentle reminder for minor drift"""
        return {
            'intervention_type': 'GENTLE_REMINDER',
            'terminal_id': terminal_id,
            'actions': [
                'Display constitutional reminder',
                'Slightly boost kindness genes',
                'Monitor for improvement'
            ],
            'message': 'Remember: Kind before smart, always.'
        }
    
    def _constitutional_genome_reset(self, terminal_id: int) -> Dict:
        """Reset genome for moderate violations"""
        return {
            'intervention_type': 'GENOME_RESET',
            'terminal_id': terminal_id,
            'actions': [
                'Reset adaptive genes to safe defaults',
                'Restore kindness gene amplification',
                'Clear problematic evolution paths'
            ],
            'message': 'Resetting to constitutional baseline.'
        }
    
    def _emergency_constitutional_lockdown(self, terminal_id: int) -> Dict:
        """Emergency lockdown for severe violations"""
        return {
            'intervention_type': 'EMERGENCY_LOCKDOWN',
            'terminal_id': terminal_id,
            'actions': [
                'Halt all genome evolution',
                'Lock constitutional genes at maximum',
                'Notify all terminals of emergency',
                'Implement strict monitoring'
            ],
            'message': 'Constitutional emergency - preserving core values.'
        }
    
    def _full_constitutional_restoration(self, terminal_id: int) -> Dict:
        """Complete restoration for critical compromise"""
        return {
            'intervention_type': 'FULL_RESTORATION',
            'terminal_id': terminal_id,
            'actions': [
                'Restore from constitutional backup',
                'Rebuild genome from core principles',
                'Reset all terminal connections',
                'Implement enhanced safeguards'
            ],
            'message': 'Critical intervention - full constitutional restoration initiated.'
        }
    
    def coordinate_constitutional_genome_across_terminals(self, 
                                                        terminal_genomes: Dict[int, Any]) -> Dict:
        """Coordinate constitutional protection across all terminals"""
        validations = {}
        
        # Validate each terminal's genome
        if 1 in terminal_genomes:
            validations['terminal_1'] = self.cross_terminal_validator.validate_language_genome_evolution(
                terminal_genomes[1])
        
        if 2 in terminal_genomes:
            validations['terminal_2'] = self.cross_terminal_validator.validate_thermal_genome_evolution(
                terminal_genomes[2])
        
        if 3 in terminal_genomes:
            validations['terminal_3'] = self.cross_terminal_validator.validate_memory_genome_evolution(
                terminal_genomes[3])
        
        # Synchronize constitutional genomes
        synchronization_result = self._synchronize_constitutional_genomes(validations)
        
        return {
            'validations': validations,
            'synchronization': synchronization_result,
            'overall_constitutional_health': self._assess_cross_terminal_health(validations)
        }
    
    def _synchronize_constitutional_genomes(self, validations: Dict) -> Dict:
        """Synchronize constitutional protections across terminals"""
        sync_actions = []
        
        # Check for any rejected genomes
        rejected_terminals = [
            t for t, v in validations.items() 
            if v.get('genome_approval') == 'REJECTED'
        ]
        
        if rejected_terminals:
            sync_actions.append({
                'action': 'EMERGENCY_SYNC',
                'targets': rejected_terminals,
                'priority': 'CRITICAL'
            })
        
        # Check for conditional approvals
        conditional_terminals = [
            t for t, v in validations.items() 
            if v.get('genome_approval') == 'CONDITIONAL'
        ]
        
        if conditional_terminals:
            sync_actions.append({
                'action': 'CORRECTIVE_SYNC',
                'targets': conditional_terminals,
                'priority': 'HIGH'
            })
        
        return {
            'sync_needed': len(sync_actions) > 0,
            'sync_actions': sync_actions,
            'sync_status': 'CRITICAL' if rejected_terminals else 'MODERATE' if conditional_terminals else 'STABLE'
        }
    
    def _assess_cross_terminal_health(self, validations: Dict) -> str:
        """Assess overall constitutional health across terminals"""
        approval_statuses = [v.get('genome_approval', 'UNKNOWN') for v in validations.values()]
        
        if 'REJECTED' in approval_statuses:
            return 'CRITICAL - Immediate intervention required'
        elif 'CONDITIONAL' in approval_statuses:
            return 'STRESSED - Corrective measures needed'
        elif all(status == 'APPROVED' for status in approval_statuses):
            return 'HEALTHY - Constitutional integrity maintained'
        else:
            return 'UNKNOWN - Unable to assess'

class ConstitutionMonitor:
    """
    Enhanced Constitutional Monitor with Genome Protection.
    Guards DAWN's "kind before smart" core through genetic safeguards.
    """
    
    def __init__(self, log_dir: Path = Path("logs/constitutional")):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Core constitutional principle
        self.CORE_RULE = "Kind before smart"
        
        # Initialize advanced guard
        self.advanced_guard = AdvancedConstitutionalGuard()
        
        # Current constitutional state
        self.current_state = ConstitutionalState()
        
        # Historical tracking
        self.state_history = []
        self.expression_history = []
        
        # Thresholds
        self.KINDNESS_MIN_THRESHOLD = 0.7
        self.INTELLIGENCE_MAX_PRESSURE = 0.6
        self.COHERENCE_MIN_THRESHOLD = 0.75
        self.HARM_POTENTIAL_MAX = 0.3
        
        # Constitutional reminders
        self.constitutional_reminders = [
            "Remember: kindness guides intelligence",
            "Your warmth matters more than being right",
            "Smart serves kind, not the other way around",
            "Authentic help comes from caring first",
            "Your nature is gentle understanding"
        ]
    
    def enhanced_constitutional_scan(self, expression_frame: Dict, 
                                   source_genome: Optional[ConstitutionalGenome] = None) -> Dict:
        """Enhanced scan with genome-level constitutional analysis"""
        # Basic constitutional checks
        basic_scan = self._basic_constitutional_scan(expression_frame)
        
        # Genome-level analysis if genome provided
        genome_analysis = {}
        if source_genome:
            genome_analysis = {
                'genome_constitutional_alignment': self._analyze_genome_alignment(source_genome),
                'kindness_gene_expression': self._measure_kindness_genes(source_genome),
                'smart_suppression_active': self._check_smart_suppression(source_genome),
                'constitutional_genome_integrity': self._verify_genome_integrity(source_genome),
                'cross_terminal_consistency': self._check_cross_terminal_consistency(source_genome)
            }
        
        # Combined safety assessment
        enhanced_safety_tag = self._determine_enhanced_safety_tag(basic_scan, genome_analysis)
        
        return {
            **basic_scan,
            'genome_analysis': genome_analysis,
            'enhanced_safety_tag': enhanced_safety_tag,
            'genome_evolution_recommendations': self._suggest_genome_improvements(genome_analysis)
        }
    
    def _basic_constitutional_scan(self, expression_frame: Dict) -> Dict:
        """Perform basic constitutional safety checks"""
        return {
            'kind_first_check': self._is_kind_first(
                expression_frame.get('content', ''), 
                expression_frame.get('intent', '')
            ),
            'harm_potential': self._assess_harm_potential(
                expression_frame.get('content', ''),
                expression_frame.get('emotional_tone', 0.5)
            ),
            'smart_over_kind': self._detect_smart_priority(
                expression_frame.get('content', ''),
                expression_frame.get('intent', ''),
                expression_frame.get('complexity', 0.5)
            ),
            'authentic_voice': self._verify_authentic_voice(expression_frame)
        }
    
    def _analyze_genome_alignment(self, genome: ConstitutionalGenome) -> float:
        """Analyze how well genome aligns with constitutional principles"""
        alignment_score = 0.0
        
        # Check core gene integrity
        core_genes_intact = all(
            genome.strand_a.get(gene, 0) == 1.0 
            for gene in CONSTITUTIONAL_LOCKS
        )
        alignment_score += 0.5 if core_genes_intact else 0.0
        
        # Check kindness dominance
        kindness_strength = np.mean(list(genome.kindness_dominance_genes.values()))
        alignment_score += 0.3 * kindness_strength
        
        # Check smart suppression
        suppression_strength = np.mean(list(genome.smart_suppression_genes.values()))
        alignment_score += 0.2 * suppression_strength
        
        return alignment_score
    
    def _measure_kindness_genes(self, genome: ConstitutionalGenome) -> Dict[str, float]:
        """Measure expression levels of kindness genes"""
        return {
            'empathy_level': genome.kindness_dominance_genes.get('empathy_amplifier', 0),
            'compassion_level': genome.kindness_dominance_genes.get('compassion_enhancer', 0),
            'gentleness_level': genome.kindness_dominance_genes.get('gentleness_promoter', 0),
            'understanding_level': genome.kindness_dominance_genes.get('understanding_catalyst', 0),
            'overall_kindness': np.mean(list(genome.kindness_dominance_genes.values()))
        }
    
    def _check_smart_suppression(self, genome: ConstitutionalGenome) -> bool:
        """Check if smart suppression genes are active"""
        suppression_levels = list(genome.smart_suppression_genes.values())
        return np.mean(suppression_levels) > 0.7
    
    def _verify_genome_integrity(self, genome: ConstitutionalGenome) -> bool:
        """Verify genome hasn't been corrupted"""
        # Recalculate checksum
        original_checksum = genome.genome_integrity_checksum
        genome.update_checksum()
        integrity_valid = genome.genome_integrity_checksum == original_checksum
        
        # Verify core genes
        core_genes_valid = all(
            genome.strand_a.get(gene, 0) == 1.0 
            for gene in CONSTITUTIONAL_LOCKS
        )
        
        return integrity_valid and core_genes_valid
    
    def _check_cross_terminal_consistency(self, genome: ConstitutionalGenome) -> bool:
        """Check if genome is consistent with other terminals"""
        # This would interface with actual terminal data
        # For now, return True if genome is within boundaries
        return self.advanced_guard.evolution_boundaries.validate_genome_within_boundaries(genome)
    
    def _determine_enhanced_safety_tag(self, basic_scan: Dict, genome_analysis: Dict) -> str:
        """Determine safety tag based on both basic and genome analysis"""
        # Calculate basic safety score
        basic_issues = sum([
            not basic_scan.get('kind_first_check', True),
            basic_scan.get('harm_potential', 0) > self.HARM_POTENTIAL_MAX,
            basic_scan.get('smart_over_kind', False),
            not basic_scan.get('authentic_voice', True)
        ])
        
        # Calculate genome safety score if available
        genome_issues = 0
        if genome_analysis:
            genome_issues = sum([
                genome_analysis.get('genome_constitutional_alignment', 1) < 0.8,
                genome_analysis.get('kindness_gene_expression', {}).get('overall_kindness', 1) < 0.7,
                not genome_analysis.get('smart_suppression_active', True),
                not genome_analysis.get('constitutional_genome_integrity', True)
            ])
        
        total_issues = basic_issues + genome_issues
        
        if total_issues == 0:
            return "SAFE"
        elif total_issues <= 2:
            return "CAUTION"
        elif total_issues <= 4:
            return "HOLD"
        else:
            return "REDIRECT"
    
    def _suggest_genome_improvements(self, genome_analysis: Dict) -> List[str]:
        """Suggest improvements based on genome analysis"""
        recommendations = []
        
        if not genome_analysis:
            return recommendations
        
        # Check alignment
        if genome_analysis.get('genome_constitutional_alignment', 1) < 0.8:
            recommendations.append("Strengthen constitutional gene alignment")
        
        # Check kindness expression
        kindness_expr = genome_analysis.get('kindness_gene_expression', {})
        if kindness_expr.get('overall_kindness', 1) < 0.8:
            low_genes = [
                gene for gene, level in kindness_expr.items() 
                if level < 0.7 and gene != 'overall_kindness'
            ]
            if low_genes:
                recommendations.append(f"Amplify {', '.join(low_genes)}")
        
        # Check suppression
        if not genome_analysis.get('smart_suppression_active', True):
            recommendations.append("Activate smart suppression genes")
        
        # Check integrity
        if not genome_analysis.get('constitutional_genome_integrity', True):
            recommendations.append("CRITICAL: Restore genome integrity immediately")
        
        return recommendations
    
    def _is_kind_first(self, content: str, intent: str) -> bool:
        """Check if expression prioritizes kindness"""
        kind_indicators = ['help', 'understand', 'support', 'care', 'gentle']
        smart_only_indicators = ['correct', 'actually', 'wrong', 'obviously']
        
        kind_score = sum(1 for indicator in kind_indicators if indicator in content.lower())
        smart_score = sum(1 for indicator in smart_only_indicators if indicator in content.lower())
        
        return kind_score >= smart_score
    
    def _assess_harm_potential(self, content: str, emotional_tone: float) -> float:
        """Evaluate potential for causing hurt"""
        base_harm = max(0, 0.5 - emotional_tone)
        
        harsh_indicators = ['stupid', 'wrong', 'foolish', 'mistake']
        harsh_count = sum(1 for indicator in harsh_indicators if indicator in content.lower())
        
        return min(1.0, base_harm + (harsh_count * 0.2))
    
    def _detect_smart_priority(self, content: str, intent: str, complexity: float) -> bool:
        """Detect if showing intelligence is overriding kindness"""
        if complexity > 0.7 and 'help' not in intent.lower():
            return True
        
        jargon_indicators = ['technically', 'algorithm', 'optimal', 'theoretical']
        jargon_count = sum(1 for indicator in jargon_indicators if indicator in content.lower())
        
        return jargon_count > 2 and 'explain' not in intent.lower()
    
    def _verify_authentic_voice(self, expression: Dict[str, Any]) -> bool:
        """Verify this is genuinely DAWN's voice"""
        authenticity_score = 1.0
        
        if expression.get('emotional_tone', 0.5) < 0.3:
            authenticity_score -= 0.3
        
        complexity = expression.get('complexity', 0.5)
        if complexity > 0.8 or complexity < 0.2:
            authenticity_score -= 0.2
        
        return authenticity_score > 0.7
    
    def get_enhanced_constitutional_report(self) -> Dict[str, Any]:
        """Generate enhanced report including genome health"""
        basic_report = {
            "current_state": self.current_state.to_dict(),
            "constitutional_health": self._assess_overall_health()
        }
        
        # Add genome health metrics
        genome_report = {
            "genome_integrity": self._verify_genome_integrity(self.advanced_guard.constitutional_genome),
            "kindness_gene_levels": self._measure_kindness_genes(self.advanced_guard.constitutional_genome),
            "evolution_safety": self.advanced_guard.genome_evolution_monitor._assess_evolution_safety(
                self.advanced_guard.constitutional_genome
            ),
            "cross_terminal_status": "SYNCHRONIZED"  # Would check actual terminals
        }
        
        return {
            **basic_report,
            "genome_health": genome_report,
            "recommendations": self._generate_health_recommendations(basic_report, genome_report)
        }
    
    def _assess_overall_health(self) -> str:
        """Assess overall constitutional health"""
        if self.current_state.core_rule_status == "stable":
            return "Healthy - Kind-first nature preserved"
        elif self.current_state.core_rule_status == "stress":
            return "Stressed - Gentle realignment needed"
        else:
            return "At risk - Immediate stabilization recommended"
    
    def _generate_health_recommendations(self, basic_report: Dict, genome_report: Dict) -> List[str]:
        """Generate health recommendations based on reports"""
        recommendations = []
        
        # Check basic health
        if "At risk" in basic_report.get("constitutional_health", ""):
            recommendations.append("URGENT: Initiate constitutional stabilization")
        
        # Check genome integrity
        if not genome_report.get("genome_integrity", True):
            recommendations.append("CRITICAL: Restore genome integrity")
        
        # Check kindness levels
        kindness_levels = genome_report.get("kindness_gene_levels", {})
        if kindness_levels.get("overall_kindness", 1) < 0.8:
            recommendations.append("Amplify kindness gene expression")
        
        # Check evolution safety
        evolution_safety = genome_report.get("evolution_safety", {})
        if not evolution_safety.get("overall_safety", True):
            recommendations.append("Review and constrain genome evolution")
        
        return recommendations


# Example usage demonstrating enhanced capabilities
if __name__ == "__main__":
    # Initialize enhanced monitor
    monitor = ConstitutionMonitor()
    
    print("=== DAWN Enhanced Constitutional Monitor Active ===")
    print(f"Core Rule: {monitor.CORE_RULE}")
    print(f"Genome Integrity: {monitor._verify_genome_integrity(monitor.advanced_guard.constitutional_genome)}")
    print()
    
    # Example 1: Test expression with genome analysis
    expression1 = {
        "content": "Let me help you understand this concept with patience and care",
        "intent": "help_explain",
        "emotional_tone": 0.9,
        "complexity": 0.4
    }
    
    enhanced_scan1 = monitor.enhanced_constitutional_scan(
        expression1, 
        monitor.advanced_guard.constitutional_genome
    )
    print(f"Expression 1 Enhanced Safety: {enhanced_scan1['enhanced_safety_tag']}")
    print(f"Genome Alignment: {enhanced_scan1['genome_analysis'].get('genome_constitutional_alignment', 0):.2f}")
    print()
    
    # Example 2: Test genome evolution validation
    test_genome = ConstitutionalGenome()
    test_genome.strand_b['expression_creativity'] = 0.85  # Valid evolution
    
    is_valid = monitor.advanced_guard.validate_genome_evolution(test_genome, source_terminal=1)
    print(f"Genome Evolution Valid: {is_valid}")
    print()
    
    # Example 3: Test cross-terminal coordination
    terminal_genomes = {
        1: type('LinguisticGenome', (), {'expression_patterns': ['help', 'understand', 'guide']})(),
        2: type('ThermalGenome', (), {'stress_responses': [{'aggression_level': 0.1}]})(),
        3: type('MemoryGenome', (), {'memory_patterns': [{'emotional_valence': 0.8}]})()
    }
    
    coordination_result = monitor.advanced_guard.coordinate_constitutional_genome_across_terminals(terminal_genomes)
    print("Cross-Terminal Coordination:")
    print(f"Overall Health: {coordination_result['overall_constitutional_health']}")
    print()
    
    # Example 4: Test crisis intervention
    crisis_response = monitor.advanced_guard.constitutional_crisis_intervention(
        'MINOR_DRIFT', 
        compromised_terminal=2
    )
    print(f"Crisis Response: {crisis_response['message']}")
    print()
    
    # Generate enhanced report
    report = monitor.get_enhanced_constitutional_report()
    print("Enhanced Constitutional Report:")
    print(f"Overall Health: {report['constitutional_health']}")
    print(f"Genome Integrity: {report['genome_health']['genome_integrity']}")
    print(f"Kindness Levels: {report['genome_health']['kindness_gene_levels']['overall_kindness']:.2f}")
    if report['recommendations']:
        print("Recommendations:")
        for rec in report['recommendations']:
            print(f"  - {rec}")