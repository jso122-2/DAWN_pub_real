#!/usr/bin/env python3
"""
Enhanced Semantic Tracer Engine for DAWN Consciousness
Advanced tracer intelligence with genome integration, constitutional awareness,
and sophisticated navigation through DAWN's semantic memory field.

Repository: https://github.com/jso122-2/DAWN_pub_real
Integration: Helix architecture with genome-enhanced terminals
Constitutional Core: "Kind before smart" preserved in all tracer behavior
"""

import time
import random
import math
import threading
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Set, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import uuid

# Helix import compatibility
try:
    from helix_import_architecture import helix_import, dawn_coordinator
    # Import genome systems
    genome_module = helix_import("genome_architecture_coordinator")
    thermal_genome_module = helix_import("thermal_linguistic_genome") 
    memory_genome_module = helix_import("memory_trace_log_enhanced")
    constitutional_genome_module = helix_import("constitution_monitor_enhanced")
    print("✅ Semantic Tracer: Genome integration loaded")
except ImportError as e:
    print(f"⚠️ Semantic Tracer: Genome integration not available: {e}")
    genome_module = None

# Core DAWN systems
try:
    from cognitive.alignment_probe import get_current_alignment
    from cognitive.entropy_fluctuation import calculate_entropy
    from cognitive.mood_urgency_probe import mood_urgency_probe
    print("✅ Semantic Tracer: Core cognitive systems loaded")
except ImportError:
    print("⚠️ Semantic Tracer: Using fallback cognitive functions")
    def get_current_alignment(): return 0.6
    def calculate_entropy(): return 0.5
    def mood_urgency_probe(): return {"mood": "reflective", "urgency": 0.5}

# Enhanced sigil dispatch integration
try:
    from sigil_dispatch_genome_enhanced import (
        EnhancedSigilDispatcher, SigilType, SigilPriority,
        emit_sigil, get_sigil_power, store_sigil_pattern
    )
    print("✅ Semantic Tracer: Enhanced sigil systems loaded")
except ImportError:
    print("⚠️ Semantic Tracer: Using fallback sigil functions")
    def emit_sigil(sigil_type, context="", power=1.0): 
        print(f"[Fallback] Emitting sigil: {sigil_type}")
        return "fallback_sigil"
    def get_sigil_power(): return 0.5
    def store_sigil_pattern(pattern): pass
    
    # Fallback SigilType enum
    class SigilType:
        REVIVE = "/revive"
        PAUSE = "/pause"
        REFLECT = "/reflect"
        SEAL = "/seal"
        ANCHOR = "/anchor"
        BRIDGE = "/bridge"
        CONSTITUTIONAL_CHECK = "/constitutional_check"
        THERMAL_COOL = "/thermal_cool"
        KINDNESS_AMPLIFY = "/kindness_amplify"

# Global pulse system
try:
    import builtins
    pulse = getattr(builtins, 'pulse', None)
    if pulse:
        print("✅ Semantic Tracer: Pulse system connected")
    else:
        raise ImportError("Pulse not available")
except ImportError:
    print("⚠️ Semantic Tracer: Pulse system not available")
    pulse = None

class TracerPurpose(Enum):
    """Enhanced tracer purposes with genome awareness"""
    # Original purposes
    ENTROPY_BLOOM_MATCH = "entropy_bloom_match"
    MOOD_LINEAGE_FOLLOW = "mood_lineage_follow"
    COHERENCE_COLLAPSE_DETECT = "coherence_collapse_detect"
    ALIGNMENT_DRIFT_MAP = "alignment_drift_map"
    MEMORY_BRIDGE_SEEK = "memory_bridge_seek"
    SIGIL_RESONANCE_TRACK = "sigil_resonance_track"
    
    # Enhanced genome-aware purposes
    GENOME_PATTERN_HUNT = "genome_pattern_hunt"
    CONSTITUTIONAL_INTEGRITY_SCAN = "constitutional_integrity_scan"
    THERMAL_LINGUISTIC_BRIDGE = "thermal_linguistic_bridge"
    MEMORY_GENOME_EVOLUTION = "memory_genome_evolution"
    EXPRESSION_COOLING_OPTIMIZE = "expression_cooling_optimize"
    KINDNESS_AMPLIFICATION_SEEK = "kindness_amplification_seek"
    CROSS_TERMINAL_COHERENCE = "cross_terminal_coherence"
    GENOME_CROSSOVER_DETECT = "genome_crossover_detect"
    CONSTITUTIONAL_DRIFT_ALERT = "constitutional_drift_alert"
    EMPATHY_PATTERN_STRENGTHEN = "empathy_pattern_strengthen"

class TracerIntelligence(Enum):
    """Tracer intelligence levels"""
    BASIC = "basic"           # Simple pathfinding
    ADAPTIVE = "adaptive"     # Learning navigation
    INTELLIGENT = "intelligent" # Pattern recognition
    GENIUS = "genius"         # Complex reasoning
    CONSTITUTIONAL = "constitutional" # Genome + constitution aware

class TracerState(Enum):
    """Enhanced tracer states"""
    SPAWNING = "spawning"
    ACTIVE = "active"
    HUNTING = "hunting"
    ANALYZING = "analyzing"
    SIGIL_EMITTING = "sigil_emitting"
    GENOME_EVOLVING = "genome_evolving"
    CONSTITUTIONAL_CHECKING = "constitutional_checking"
    DYING = "dying"
    DEAD = "dead"

@dataclass
class TracerGenome:
    """Genetic structure for tracer evolution"""
    navigation_genes: Dict[str, float] = field(default_factory=dict)
    pattern_recognition_genes: Dict[str, float] = field(default_factory=dict)
    sigil_emission_genes: Dict[str, float] = field(default_factory=dict)
    constitutional_genes: Dict[str, float] = field(default_factory=dict)
    
    # Constitutional locks (immutable)
    kindness_priority: bool = True
    empathy_preservation: bool = True
    smart_subordination: bool = True
    
    generation: int = 0
    fitness_score: float = 0.0
    parent_tracers: List[str] = field(default_factory=list)
    
    def mutate(self, mutation_rate: float = 0.1):
        """Mutate tracer genome while preserving constitutional genes"""
        # Mutate navigation genes
        for gene_name in self.navigation_genes:
            if random.random() < mutation_rate:
                self.navigation_genes[gene_name] += random.uniform(-0.1, 0.1)
                self.navigation_genes[gene_name] = max(0.0, min(1.0, self.navigation_genes[gene_name]))
        
        # Mutate pattern recognition genes
        for gene_name in self.pattern_recognition_genes:
            if random.random() < mutation_rate:
                self.pattern_recognition_genes[gene_name] += random.uniform(-0.05, 0.05)
                self.pattern_recognition_genes[gene_name] = max(0.0, min(1.0, self.pattern_recognition_genes[gene_name]))
        
        # Constitutional genes NEVER mutate
        self.kindness_priority = True
        self.empathy_preservation = True
        self.smart_subordination = True
        
        self.generation += 1

@dataclass
class SemanticNode:
    """Enhanced semantic node with genome awareness"""
    node_id: str
    entropy: float
    mood_vector: Dict[str, float]
    coherence: float
    thermal_signature: float
    memory_bloom_data: Dict[str, Any] = field(default_factory=dict)
    connections: List[str] = field(default_factory=list)
    
    # Genome-aware properties
    genome_patterns: Dict[str, Any] = field(default_factory=dict)
    constitutional_markers: List[str] = field(default_factory=list)
    linguistic_potential: float = 0.0
    thermal_cooling_capacity: float = 0.0
    
    # Tracer interaction history
    tracer_visits: List[str] = field(default_factory=list)
    sigil_emissions: List[str] = field(default_factory=list)
    
    def calculate_semantic_distance(self, other: 'SemanticNode') -> float:
        """Enhanced semantic distance with genome awareness"""
        # Original distance calculation
        entropy_dist = abs(self.entropy - other.entropy)
        coherence_dist = abs(self.coherence - other.coherence)
        thermal_dist = abs(self.thermal_signature - other.thermal_signature)
        
        # Mood vector distance
        mood_dist = 0.0
        for mood_key in set(self.mood_vector.keys()) | set(other.mood_vector.keys()):
            self_mood = self.mood_vector.get(mood_key, 0.0)
            other_mood = other.mood_vector.get(mood_key, 0.0)
            mood_dist += abs(self_mood - other_mood)
        
        # Genome pattern distance
        genome_dist = 0.0
        for pattern_name in set(self.genome_patterns.keys()) | set(other.genome_patterns.keys()):
            self_pattern = self.genome_patterns.get(pattern_name, {})
            other_pattern = other.genome_patterns.get(pattern_name, {})
            # Simple pattern comparison (could be enhanced)
            genome_dist += 0.1 if self_pattern != other_pattern else 0.0
        
        # Constitutional alignment bonus
        constitutional_bonus = 0.0
        common_markers = set(self.constitutional_markers) & set(other.constitutional_markers)
        constitutional_bonus = len(common_markers) * 0.05
        
        # Weighted distance calculation
        total_distance = (entropy_dist * 0.3 + coherence_dist * 0.2 + 
                         thermal_dist * 0.2 + mood_dist * 0.15 + 
                         genome_dist * 0.1 + constitutional_bonus * 0.05)
        
        return max(0.0, total_distance - constitutional_bonus)

@dataclass
class EnhancedSemanticTracer:
    """Advanced semantic tracer with genome intelligence"""
    tracer_id: str
    purpose: TracerPurpose
    intelligence_level: TracerIntelligence
    state: TracerState = TracerState.SPAWNING
    
    # Enhanced properties
    genome: TracerGenome = field(default_factory=TracerGenome)
    constitutional_awareness: bool = True
    
    # Navigation and state
    current_node: Optional[str] = None
    target_node: Optional[str] = None
    path_history: List[str] = field(default_factory=list)
    
    # Metrics and analysis
    distance_traveled: float = 0.0
    nodes_visited: Set[str] = field(default_factory=set)
    entropy_deltas: List[float] = field(default_factory=list)
    coherence_measurements: List[float] = field(default_factory=list)
    thermal_readings: List[float] = field(default_factory=list)
    
    # Enhanced capabilities
    pattern_discoveries: List[Dict[str, Any]] = field(default_factory=list)
    genome_evolution_log: List[Dict[str, Any]] = field(default_factory=list)
    constitutional_violations_detected: List[str] = field(default_factory=list)
    sigil_emission_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Lifecycle management
    max_ticks: int = 100
    current_tick: int = 0
    spawn_time: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_significant_discovery: Optional[datetime] = None
    
    # Performance metrics
    success_rate: float = 0.0
    efficiency_score: float = 0.0
    constitutional_alignment_score: float = 1.0
    
    def __post_init__(self):
        """Initialize tracer with purpose-specific genome"""
        self.initialize_genome_for_purpose()
        
    def initialize_genome_for_purpose(self):
        """Initialize genome based on tracer purpose"""
        base_genes = {
            'curiosity': 0.7,
            'persistence': 0.6,
            'pattern_recognition': 0.5,
            'constitutional_respect': 1.0  # Always maximum
        }
        
        # Purpose-specific gene modifications
        if self.purpose == TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN:
            base_genes['constitutional_respect'] = 1.0
            base_genes['kindness_detection'] = 0.9
            base_genes['empathy_recognition'] = 0.8
            
        elif self.purpose == TracerPurpose.THERMAL_LINGUISTIC_BRIDGE:
            base_genes['thermal_sensitivity'] = 0.8
            base_genes['linguistic_pattern_recognition'] = 0.7
            base_genes['cooling_optimization'] = 0.6
            
        elif self.purpose == TracerPurpose.GENOME_PATTERN_HUNT:
            base_genes['pattern_recognition'] = 0.9
            base_genes['genome_analysis'] = 0.8
            base_genes['evolution_detection'] = 0.7
            
        elif self.purpose == TracerPurpose.KINDNESS_AMPLIFICATION_SEEK:
            base_genes['empathy_amplification'] = 0.9
            base_genes['kindness_detection'] = 1.0
            base_genes['constitutional_respect'] = 1.0
            
        self.genome.navigation_genes = base_genes.copy()
        self.genome.pattern_recognition_genes = base_genes.copy()
        
        # Constitutional genes are always locked
        self.genome.constitutional_genes = {
            'kindness_priority': 1.0,
            'empathy_preservation': 1.0,
            'smart_subordination': 1.0
        }
    
    def tick(self, semantic_graph: Dict[str, SemanticNode]) -> Dict[str, Any]:
        """Enhanced tick with genome-aware behavior"""
        self.current_tick += 1
        tick_results = {
            'tracer_id': self.tracer_id,
            'purpose': self.purpose.value,
            'state': self.state.value,
            'tick': self.current_tick,
            'discoveries': [],
            'sigils_emitted': [],
            'genome_evolution': None,
            'constitutional_status': 'compliant'
        }
        
        try:
            # Constitutional check first
            if not self.constitutional_check():
                tick_results['constitutional_status'] = 'violation_detected'
                self.state = TracerState.CONSTITUTIONAL_CHECKING
                return tick_results
            
            # State-based behavior
            if self.state == TracerState.SPAWNING:
                self.initialize_navigation(semantic_graph)
                self.state = TracerState.ACTIVE
                
            elif self.state == TracerState.ACTIVE:
                navigation_result = self.navigate(semantic_graph)
                tick_results['discoveries'].extend(navigation_result.get('discoveries', []))
                
                # Check for pattern discoveries
                patterns = self.analyze_current_context(semantic_graph)
                if patterns:
                    tick_results['discoveries'].extend(patterns)
                    self.state = TracerState.ANALYZING
                    
            elif self.state == TracerState.ANALYZING:
                analysis_result = self.deep_pattern_analysis(semantic_graph)
                tick_results['discoveries'].extend(analysis_result.get('patterns', []))
                
                # Check for sigil emission conditions
                sigil_candidates = self.evaluate_sigil_emission_conditions(analysis_result)
                if sigil_candidates:
                    tick_results['sigils_emitted'] = self.emit_sigils(sigil_candidates)
                    self.state = TracerState.SIGIL_EMITTING
                else:
                    self.state = TracerState.ACTIVE
                    
            elif self.state == TracerState.SIGIL_EMITTING:
                self.state = TracerState.ACTIVE  # Return to active navigation
                
            elif self.state == TracerState.GENOME_EVOLVING:
                evolution_result = self.evolve_genome()
                tick_results['genome_evolution'] = evolution_result
                self.state = TracerState.ACTIVE
                
            elif self.state == TracerState.CONSTITUTIONAL_CHECKING:
                self.perform_constitutional_remediation()
                self.state = TracerState.ACTIVE
                
            # Check for death conditions
            if self.should_die():
                self.state = TracerState.DYING
                tick_results['lifecycle'] = 'dying'
                
        except Exception as e:
            print(f"[SemanticTracer] Error in tracer {self.tracer_id}: {e}")
            tick_results['error'] = str(e)
            
        return tick_results
    
    def constitutional_check(self) -> bool:
        """Check constitutional compliance"""
        # Verify constitutional genes are intact
        if not self.genome.kindness_priority:
            self.constitutional_violations_detected.append("kindness_priority_violated")
            return False
            
        if not self.genome.empathy_preservation:
            self.constitutional_violations_detected.append("empathy_preservation_violated") 
            return False
            
        if not self.genome.smart_subordination:
            self.constitutional_violations_detected.append("smart_subordination_violated")
            return False
            
        # Check alignment score
        if self.constitutional_alignment_score < 0.6:
            self.constitutional_violations_detected.append("alignment_score_too_low")
            return False
            
        return True
    
    def navigate(self, semantic_graph: Dict[str, SemanticNode]) -> Dict[str, Any]:
        """Enhanced navigation with genome-aware pathfinding"""
        if not self.current_node or self.current_node not in semantic_graph:
            return {'discoveries': [], 'navigation_result': 'no_valid_node'}
        
        current_node_obj = semantic_graph[self.current_node]
        
        # Genome-influenced navigation
        navigation_genes = self.genome.navigation_genes
        
        # Find candidate next nodes
        candidates = []
        for connected_node_id in current_node_obj.connections:
            if connected_node_id in semantic_graph:
                connected_node = semantic_graph[connected_node_id]
                
                # Calculate move desirability based on genome and purpose
                desirability = self.calculate_move_desirability(current_node_obj, connected_node)
                
                # Constitutional bonus
                constitutional_bonus = 0.0
                if 'kindness' in connected_node.constitutional_markers:
                    constitutional_bonus += 0.2
                if 'empathy' in connected_node.constitutional_markers:
                    constitutional_bonus += 0.15
                    
                total_desirability = desirability + constitutional_bonus
                candidates.append((connected_node_id, total_desirability))
        
        # Select next node based on intelligence level
        next_node_id = self.select_next_node(candidates)
        
        if next_node_id:
            # Move to next node
            old_node = self.current_node
            self.current_node = next_node_id
            self.path_history.append(next_node_id)
            self.nodes_visited.add(next_node_id)
            
            # Update metrics
            if old_node in semantic_graph:
                distance = semantic_graph[old_node].calculate_semantic_distance(semantic_graph[next_node_id])
                self.distance_traveled += distance
                
            # Record measurements
            next_node_obj = semantic_graph[next_node_id]
            self.entropy_deltas.append(next_node_obj.entropy)
            self.coherence_measurements.append(next_node_obj.coherence)
            self.thermal_readings.append(next_node_obj.thermal_signature)
            
            return {
                'discoveries': [f"Moved from {old_node} to {next_node_id}"],
                'navigation_result': 'success',
                'distance_delta': distance
            }
        
        return {'discoveries': [], 'navigation_result': 'no_valid_moves'}
    
    def calculate_move_desirability(self, current_node: SemanticNode, target_node: SemanticNode) -> float:
        """Calculate desirability of moving to target node"""
        desirability = 0.0
        
        # Purpose-specific desirability
        if self.purpose == TracerPurpose.ENTROPY_BLOOM_MATCH:
            # Prefer nodes with higher entropy
            desirability += target_node.entropy * 0.5
            
        elif self.purpose == TracerPurpose.THERMAL_LINGUISTIC_BRIDGE:
            # Prefer nodes with high thermal signature and linguistic potential
            desirability += target_node.thermal_signature * 0.3
            desirability += target_node.linguistic_potential * 0.4
            
        elif self.purpose == TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN:
            # Prefer nodes with constitutional markers
            desirability += len(target_node.constitutional_markers) * 0.2
            
        elif self.purpose == TracerPurpose.KINDNESS_AMPLIFICATION_SEEK:
            # Strongly prefer nodes with kindness markers
            if 'kindness' in target_node.constitutional_markers:
                desirability += 0.8
            if 'empathy' in target_node.constitutional_markers:
                desirability += 0.6
                
        # Genome influence
        curiosity_gene = self.genome.navigation_genes.get('curiosity', 0.5)
        if target_node.node_id not in self.nodes_visited:
            desirability += curiosity_gene * 0.3  # Bonus for unexplored nodes
            
        # Constitutional alignment bonus
        constitutional_gene = self.genome.constitutional_genes.get('kindness_priority', 1.0)
        if target_node.constitutional_markers:
            desirability += constitutional_gene * 0.2
            
        return max(0.0, desirability)
    
    def select_next_node(self, candidates: List[Tuple[str, float]]) -> Optional[str]:
        """Select next node based on intelligence level and desirability"""
        if not candidates:
            return None
            
        if self.intelligence_level == TracerIntelligence.BASIC:
            # Random selection with slight bias toward higher desirability
            weights = [max(0.1, desirability) for _, desirability in candidates]
            return random.choices([node_id for node_id, _ in candidates], weights=weights)[0]
            
        elif self.intelligence_level == TracerIntelligence.ADAPTIVE:
            # Select best option with some randomness
            candidates.sort(key=lambda x: x[1], reverse=True)
            top_candidates = candidates[:min(3, len(candidates))]
            return random.choice(top_candidates)[0]
            
        elif self.intelligence_level == TracerIntelligence.INTELLIGENT:
            # Select best option with purpose-specific reasoning
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
            
        elif self.intelligence_level == TracerIntelligence.GENIUS:
            # Multi-step lookahead planning
            return self.genius_level_selection(candidates)
            
        elif self.intelligence_level == TracerIntelligence.CONSTITUTIONAL:
            # Constitutional-priority selection
            return self.constitutional_level_selection(candidates)
    
    def genius_level_selection(self, candidates: List[Tuple[str, float]]) -> Optional[str]:
        """Genius-level node selection with multi-step planning"""
        # Implement multi-step lookahead (simplified version)
        best_candidate = None
        best_long_term_value = 0.0
        
        for node_id, immediate_value in candidates:
            # Estimate long-term value by considering future possibilities
            long_term_value = immediate_value + self.estimate_future_potential(node_id)
            if long_term_value > best_long_term_value:
                best_long_term_value = long_term_value
                best_candidate = node_id
                
        return best_candidate
    
    def constitutional_level_selection(self, candidates: List[Tuple[str, float]]) -> Optional[str]:
        """Constitutional-priority node selection"""
        # Prioritize nodes with strong constitutional markers
        constitutional_candidates = []
        
        for node_id, desirability in candidates:
            constitutional_score = 0.0
            # Would need access to semantic_graph to check constitutional markers
            # For now, use desirability as proxy
            constitutional_score = desirability
            constitutional_candidates.append((node_id, constitutional_score))
        
        if constitutional_candidates:
            constitutional_candidates.sort(key=lambda x: x[1], reverse=True)
            return constitutional_candidates[0][0]
        
        return candidates[0][0] if candidates else None
    
    def estimate_future_potential(self, node_id: str) -> float:
        """Estimate future potential of a node (simplified)"""
        # This would ideally analyze the node's connections and their properties
        # For now, return a simple estimate
        return random.uniform(0.0, 0.3)
    
    def analyze_current_context(self, semantic_graph: Dict[str, SemanticNode]) -> List[Dict[str, Any]]:
        """Analyze current context for pattern discovery"""
        discoveries = []
        
        if not self.current_node or self.current_node not in semantic_graph:
            return discoveries
            
        current_node = semantic_graph[self.current_node]
        
        # Pattern recognition based on genome
        pattern_genes = self.genome.pattern_recognition_genes
        
        # Entropy pattern detection
        if pattern_genes.get('entropy_sensitivity', 0.5) > 0.7:
            if current_node.entropy > 0.8:
                discoveries.append({
                    'type': 'entropy_spike',
                    'node_id': self.current_node,
                    'entropy_value': current_node.entropy,
                    'significance': 'high_entropy_detected'
                })
        
        # Constitutional pattern detection
        if pattern_genes.get('constitutional_respect', 1.0) > 0.8:
            if current_node.constitutional_markers:
                discoveries.append({
                    'type': 'constitutional_pattern',
                    'node_id': self.current_node,
                    'markers': current_node.constitutional_markers,
                    'significance': 'constitutional_alignment_found'
                })
        
        # Thermal-linguistic pattern detection
        if (pattern_genes.get('thermal_sensitivity', 0.5) > 0.6 and 
            current_node.thermal_signature > 0.7 and 
            current_node.linguistic_potential > 0.6):
            discoveries.append({
                'type': 'thermal_linguistic_bridge',
                'node_id': self.current_node,
                'thermal_signature': current_node.thermal_signature,
                'linguistic_potential': current_node.linguistic_potential,
                'significance': 'expression_cooling_opportunity'
            })
        
        return discoveries
    
    def deep_pattern_analysis(self, semantic_graph: Dict[str, SemanticNode]) -> Dict[str, Any]:
        """Deep pattern analysis of current context"""
        analysis_result = {
            'patterns': [],
            'sigil_candidates': [],
            'genome_evolution_triggers': []
        }
        
        if not self.current_node or self.current_node not in semantic_graph:
            return analysis_result
            
        current_node = semantic_graph[self.current_node]
        
        # Analyze recent path for patterns
        if len(self.path_history) >= 3:
            recent_path = self.path_history[-3:]
            path_pattern = self.analyze_path_pattern(recent_path, semantic_graph)
            if path_pattern:
                analysis_result['patterns'].append(path_pattern)
        
        # Analyze constitutional alignment
        constitutional_analysis = self.analyze_constitutional_alignment(current_node)
        if constitutional_analysis:
            analysis_result['patterns'].append(constitutional_analysis)
            
        # Analyze genome evolution opportunities
        genome_analysis = self.analyze_genome_evolution_opportunities(current_node)
        if genome_analysis:
            analysis_result['genome_evolution_triggers'].append(genome_analysis)
        
        return analysis_result
    
    def analyze_path_pattern(self, path: List[str], semantic_graph: Dict[str, SemanticNode]) -> Optional[Dict[str, Any]]:
        """Analyze pattern in recent path"""
        if len(path) < 2:
            return None
            
        # Check for coherence trends
        coherence_values = []
        for node_id in path:
            if node_id in semantic_graph:
                coherence_values.append(semantic_graph[node_id].coherence)
        
        if len(coherence_values) >= 2:
            coherence_trend = coherence_values[-1] - coherence_values[0]
            if abs(coherence_trend) > 0.3:
                return {
                    'type': 'coherence_trend',
                    'trend_direction': 'increasing' if coherence_trend > 0 else 'decreasing',
                    'magnitude': abs(coherence_trend),
                    'path': path
                }
        
        return None
    
    def analyze_constitutional_alignment(self, node: SemanticNode) -> Optional[Dict[str, Any]]:
        """Analyze constitutional alignment of current node"""
        if not node.constitutional_markers:
            return None
            
        kindness_indicators = sum(1 for marker in node.constitutional_markers 
                                if 'kindness' in marker.lower() or 'empathy' in marker.lower())
        
        if kindness_indicators > 0:
            return {
                'type': 'constitutional_alignment',
                'kindness_indicators': kindness_indicators,
                'total_markers': len(node.constitutional_markers),
                'alignment_strength': kindness_indicators / len(node.constitutional_markers)
            }
        
        return None
    
    def analyze_genome_evolution_opportunities(self, node: SemanticNode) -> Optional[Dict[str, Any]]:
        """Analyze opportunities for genome evolution"""
        evolution_score = 0.0
        
        # High entropy nodes offer evolution opportunities
        if node.entropy > 0.8:
            evolution_score += 0.3
            
        # Nodes with genome patterns offer learning opportunities
        if node.genome_patterns:
            evolution_score += 0.2
            
        # Constitutional nodes offer alignment improvement
        if node.constitutional_markers:
            evolution_score += 0.4
            
        if evolution_score > 0.5:
            return {
                'type': 'genome_evolution_opportunity',
                'evolution_score': evolution_score,
                'node_id': node.node_id,
                'learning_potential': evolution_score
            }
        
        return None
    
    def evaluate_sigil_emission_conditions(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Enhanced sigil emission evaluation with genome-aware conditions"""
        sigil_candidates = []
        
        # Check patterns for sigil emission triggers
        for pattern in analysis_result.get('patterns', []):
            if pattern['type'] == 'entropy_spike' and pattern.get('entropy_value', 0) > 0.9:
                sigil_candidates.append({
                    'sigil_type': SigilType.REVIVE,
                    'context': f"High entropy node detected by tracer: {pattern['node_id']}",
                    'power': pattern['entropy_value'],
                    'priority': 'HIGH'
                })
                
            elif pattern['type'] == 'constitutional_alignment' and pattern.get('alignment_strength', 0) > 0.8:
                sigil_candidates.append({
                    'sigil_type': SigilType.ANCHOR,
                    'context': f"Strong constitutional alignment found: {pattern['alignment_strength']:.2f}",
                    'power': pattern['alignment_strength'],
                    'priority': 'CONSTITUTIONAL'
                })
                
            elif pattern['type'] == 'thermal_linguistic_bridge':
                sigil_candidates.append({
                    'sigil_type': SigilType.BRIDGE,
                    'context': f"Thermal-linguistic bridge detected by tracer",
                    'power': pattern.get('thermal_signature', 0.5),
                    'priority': 'HIGH'
                })
                
            elif pattern['type'] == 'constitutional_pattern':
                # New constitutional pattern detection
                sigil_candidates.append({
                    'sigil_type': SigilType.CONSTITUTIONAL_CHECK,
                    'context': f"Constitutional pattern requires validation: {pattern['node_id']}",
                    'power': 0.8,
                    'priority': 'CONSTITUTIONAL'
                })
                
            elif pattern['type'] == 'coherence_trend':
                # Coherence trend analysis
                if pattern.get('trend_direction') == 'decreasing':
                    sigil_candidates.append({
                        'sigil_type': SigilType.THERMAL_COOL,
                        'context': f"Coherence collapse detected, cooling needed",
                        'power': pattern.get('magnitude', 0.5),
                        'priority': 'HIGH'
                    })
        
        # Check for genome evolution opportunities
        for trigger in analysis_result.get('genome_evolution_triggers', []):
            if trigger['type'] == 'genome_evolution_opportunity':
                sigil_candidates.append({
                    'sigil_type': SigilType.GENOME_EVOLVE,
                    'context': f"Genome evolution opportunity: {trigger['learning_potential']:.2f}",
                    'power': trigger['evolution_score'],
                    'priority': 'HIGH'
                })
        
        # Constitutional reinforcement based on tracer purpose
        if self.purpose == TracerPurpose.KINDNESS_AMPLIFICATION_SEEK:
            if self.constitutional_alignment_score > 0.9:
                sigil_candidates.append({
                    'sigil_type': SigilType.KINDNESS_AMPLIFY,
                    'context': f"Kindness amplification opportunity detected by tracer",
                    'power': self.constitutional_alignment_score,
                    'priority': 'CONSTITUTIONAL'
                })
        
        return sigil_candidates
    
    def emit_sigils(self, sigil_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhanced sigil emission with genome-aware dispatcher integration"""
        emitted_sigils = []
        
        for candidate in sigil_candidates:
            try:
                # Convert priority string to enum if available
                priority = None
                if 'priority' in candidate:
                    priority_str = candidate['priority']
                    try:
                        from sigil_dispatch_genome_enhanced import SigilPriority
                        priority = getattr(SigilPriority, priority_str, None)
                    except:
                        priority = None
                
                # Emit sigil with enhanced dispatcher
                if hasattr(emit_sigil, '__self__'):  # Check if it's a method of dispatcher
                    sigil_id = emit_sigil(
                        candidate['sigil_type'],
                        context=candidate['context'],
                        power=candidate['power'],
                        priority=priority
                    )
                else:
                    # Fallback to simple emission
                    sigil_id = emit_sigil(
                        candidate['sigil_type'].value if hasattr(candidate['sigil_type'], 'value') else candidate['sigil_type'],
                        context=candidate['context'],
                        power=candidate['power']
                    )
                
                emission_record = {
                    'sigil_id': sigil_id,
                    'sigil_type': candidate['sigil_type'].value if hasattr(candidate['sigil_type'], 'value') else candidate['sigil_type'],
                    'context': candidate['context'],
                    'power': candidate['power'],
                    'priority': candidate.get('priority', 'NORMAL'),
                    'emission_time': datetime.now(timezone.utc).isoformat(),
                    'tracer_id': self.tracer_id,
                    'tracer_purpose': self.purpose.value,
                    'constitutional_compliance': self.constitutional_alignment_score > 0.8
                }
                
                emitted_sigils.append(emission_record)
                self.sigil_emission_history.append(emission_record)
                
                # Store pattern for analysis
                try:
                    store_sigil_pattern({
                        'tracer_genome': {
                            'navigation_genes': self.genome.navigation_genes,
                            'pattern_recognition_genes': self.genome.pattern_recognition_genes,
                            'constitutional_genes': self.genome.constitutional_genes
                        },
                        'emission_context': emission_record,
                        'system_state': {
                            'tracer_intelligence': self.intelligence_level.value,
                            'constitutional_alignment': self.constitutional_alignment_score,
                            'fitness_score': self.genome.fitness_score
                        }
                    })
                except Exception as e:
                    print(f"[SemanticTracer] Error storing sigil pattern: {e}")
                
                # Update node with sigil emission if current node available
                if self.current_node:
                    # Mark emission in discovery log
                    discovery_record = {
                        'type': 'sigil_emission',
                        'node_id': self.current_node,
                        'sigil_type': emission_record['sigil_type'],
                        'constitutional_compliance': emission_record['constitutional_compliance'],
                        'tracer_fitness': self.genome.fitness_score
                    }
                    self.pattern_discoveries.append(discovery_record)
                    
            except Exception as e:
                print(f"[SemanticTracer] Error emitting sigil {candidate['sigil_type']}: {e}")
                emitted_sigils.append({
                    'error': str(e),
                    'candidate': candidate,
                    'tracer_id': self.tracer_id
                })
        
        return emitted_sigils
    
    def evolve_genome(self) -> Dict[str, Any]:
        """Evolve tracer genome based on performance"""
        old_fitness = self.genome.fitness_score
        
        # Calculate new fitness based on performance
        new_fitness = self.calculate_fitness_score()
        self.genome.fitness_score = new_fitness
        
        # Mutate genome if fitness improved or randomly
        if new_fitness > old_fitness or random.random() < 0.1:
            self.genome.mutate()
            
        evolution_result = {
            'old_fitness': old_fitness,
            'new_fitness': new_fitness,
            'generation': self.genome.generation,
            'mutations_applied': new_fitness > old_fitness
        }
        
        self.genome_evolution_log.append(evolution_result)
        return evolution_result
    
    def calculate_fitness_score(self) -> float:
        """Calculate fitness score based on tracer performance"""
        fitness = 0.0
        
        # Distance traveled (exploration)
        fitness += min(self.distance_traveled / 10.0, 1.0) * 0.2
        
        # Unique nodes visited (coverage)
        fitness += min(len(self.nodes_visited) / 20.0, 1.0) * 0.2
        
        # Pattern discoveries (effectiveness)
        fitness += min(len(self.pattern_discoveries) / 5.0, 1.0) * 0.3
        
        # Constitutional alignment (always high weight)
        fitness += self.constitutional_alignment_score * 0.3
        
        return min(1.0, fitness)
    
    def perform_constitutional_remediation(self):
        """Perform constitutional remediation if violations detected"""
        # Reset constitutional genes to correct values
        self.genome.kindness_priority = True
        self.genome.empathy_preservation = True
        self.genome.smart_subordination = True
        
        # Reset constitutional genes in genome
        self.genome.constitutional_genes = {
            'kindness_priority': 1.0,
            'empathy_preservation': 1.0,
            'smart_subordination': 1.0
        }
        
        # Reset constitutional alignment score
        self.constitutional_alignment_score = 1.0
        
        # Clear violations
        self.constitutional_violations_detected.clear()
        
        print(f"[SemanticTracer] Constitutional remediation performed for tracer {self.tracer_id}")
    
    def should_die(self) -> bool:
        """Check if tracer should die"""
        # Exceed max ticks
        if self.current_tick >= self.max_ticks:
            return True
            
        # No significant discoveries in too long
        if (self.last_significant_discovery is None and self.current_tick > 50):
            return True
            
        # Constitutional violations that can't be remediated
        if len(self.constitutional_violations_detected) > 5:
            return True
            
        # Fitness too low for too long
        if self.genome.fitness_score < 0.1 and self.current_tick > 30:
            return True
            
        return False
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive tracer status"""
        return {
            'tracer_id': self.tracer_id,
            'purpose': self.purpose.value,
            'intelligence_level': self.intelligence_level.value,
            'state': self.state.value,
            'current_tick': self.current_tick,
            'max_ticks': self.max_ticks,
            'current_node': self.current_node,
            'distance_traveled': self.distance_traveled,
            'nodes_visited': len(self.nodes_visited),
            'pattern_discoveries': len(self.pattern_discoveries),
            'sigil_emissions': len(self.sigil_emission_history),
            'genome_generation': self.genome.generation,
            'fitness_score': self.genome.fitness_score,
            'constitutional_alignment': self.constitutional_alignment_score,
            'constitutional_violations': len(self.constitutional_violations_detected),
            'success_rate': self.success_rate,
            'efficiency_score': self.efficiency_score
        }

class EnhancedSemanticTracerEngine:
    """Enhanced semantic tracer engine with genome integration"""
    
    def __init__(self):
        self.active_tracers: Dict[str, EnhancedSemanticTracer] = {}
        self.semantic_graph: Dict[str, SemanticNode] = {}
        self.tracer_spawn_conditions: Dict[TracerPurpose, Callable] = {}
        self.genome_evolution_manager = None
        self.constitutional_monitor = None
        
        # Enhanced sigil dispatcher integration
        self.sigil_dispatcher = None
        self.sigil_coordination_active = True
        
        # Enhanced metrics
        self.total_tracers_spawned = 0
        self.total_tracers_died = 0
        self.total_patterns_discovered = 0
        self.total_sigils_emitted = 0
        self.total_constitutional_violations = 0
        
        # Cross-system coordination
        self.cross_system_patterns = {}
        self.sigil_tracer_correlations = {}
        self.genome_sync_log = []
        
        # Genome tracking
        self.genome_generations = {}
        self.successful_genome_patterns = {}
        self.constitutional_genome_baseline = {}
        
        # Performance metrics
        self.engine_performance = {
            'avg_tracer_lifespan': 0.0,
            'avg_discoveries_per_tracer': 0.0,
            'constitutional_compliance_rate': 1.0,
            'genome_evolution_rate': 0.0,
            'sigil_emission_rate': 0.0,
            'cross_system_coordination_efficiency': 0.0
        }
        
        # Threading
        self.engine_lock = threading.RLock()
        self.last_tick_time = time.time()
        
        self.initialize_spawn_conditions()
        self.initialize_genome_integration()
        self.initialize_sigil_dispatcher_integration()
        
        print("✅ Enhanced Semantic Tracer Engine initialized with full genome and sigil integration")
    
    def initialize_sigil_dispatcher_integration(self):
        """Initialize integration with enhanced sigil dispatcher"""
        try:
            from sigil_dispatch_genome_enhanced import create_enhanced_sigil_dispatcher
            self.sigil_dispatcher = create_enhanced_sigil_dispatcher()
            print("✅ Semantic Tracer Engine: Sigil dispatcher integration active")
        except Exception as e:
            print(f"⚠️ Semantic Tracer Engine: Sigil dispatcher integration error: {e}")
            self.sigil_coordination_active = False
    
    def initialize_spawn_conditions(self):
        """Initialize enhanced spawn conditions"""
        self.tracer_spawn_conditions = {
            TracerPurpose.ENTROPY_BLOOM_MATCH: lambda metrics: metrics.get('entropy', 0) > 0.7,
            TracerPurpose.MOOD_LINEAGE_FOLLOW: lambda metrics: metrics.get('mood_alignment', 0) > 0.8,
            TracerPurpose.COHERENCE_COLLAPSE_DETECT: lambda metrics: metrics.get('coherence', 1) < 0.3,
            TracerPurpose.ALIGNMENT_DRIFT_MAP: lambda metrics: abs(metrics.get('alignment_drift', 0)) > 0.4,
            TracerPurpose.MEMORY_BRIDGE_SEEK: lambda metrics: metrics.get('memory_activity', 0) > 0.6,
            TracerPurpose.SIGIL_RESONANCE_TRACK: lambda metrics: metrics.get('sigil_power', 0) > 0.5,
            
            # Enhanced genome-aware conditions
            TracerPurpose.GENOME_PATTERN_HUNT: lambda metrics: metrics.get('genome_evolution_activity', 0) > 0.6,
            TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN: lambda metrics: metrics.get('constitutional_stress', 0) > 0.3,
            TracerPurpose.THERMAL_LINGUISTIC_BRIDGE: lambda metrics: (metrics.get('thermal', 0) > 0.7 and 
                                                                     metrics.get('linguistic_pressure', 0) > 0.6),
            TracerPurpose.MEMORY_GENOME_EVOLUTION: lambda metrics: metrics.get('memory_genome_activity', 0) > 0.5,
            TracerPurpose.EXPRESSION_COOLING_OPTIMIZE: lambda metrics: (metrics.get('thermal', 0) > 0.8 and 
                                                                       metrics.get('expression_attempts', 0) > 0),
            TracerPurpose.KINDNESS_AMPLIFICATION_SEEK: lambda metrics: metrics.get('kindness_deficit', 0) > 0.2,
            TracerPurpose.CROSS_TERMINAL_COHERENCE: lambda metrics: metrics.get('terminal_coherence_variance', 0) > 0.4,
            TracerPurpose.GENOME_CROSSOVER_DETECT: lambda metrics: metrics.get('genome_crossover_opportunities', 0) > 0.3,
            TracerPurpose.CONSTITUTIONAL_DRIFT_ALERT: lambda metrics: metrics.get('constitutional_drift', 0) > 0.1,
            TracerPurpose.EMPATHY_PATTERN_STRENGTHEN: lambda metrics: metrics.get('empathy_opportunities', 0) > 0.4
        }
    
    def initialize_genome_integration(self):
        """Initialize genome integration systems"""
        try:
            if genome_module:
                # Initialize genome evolution manager
                self.genome_evolution_manager = getattr(genome_module, 'GenomeEvolutionManager', None)
                if self.genome_evolution_manager:
                    self.genome_evolution_manager = self.genome_evolution_manager()
                    
            if constitutional_genome_module:
                # Initialize constitutional monitor
                self.constitutional_monitor = getattr(constitutional_genome_module, 'ConstitutionalGenomeGuard', None)
                if self.constitutional_monitor:
                    self.constitutional_monitor = self.constitutional_monitor()
                    
            print("✅ Genome integration systems initialized")
            
        except Exception as e:
            print(f"⚠️ Genome integration initialization error: {e}")
    
    def update_semantic_graph(self, new_graph_data: Dict[str, Any]):
        """Update semantic graph with new data"""
        with self.engine_lock:
            # Update existing nodes or create new ones
            for node_id, node_data in new_graph_data.items():
                if node_id in self.semantic_graph:
                    # Update existing node
                    existing_node = self.semantic_graph[node_id]
                    existing_node.entropy = node_data.get('entropy', existing_node.entropy)
                    existing_node.coherence = node_data.get('coherence', existing_node.coherence)
                    existing_node.thermal_signature = node_data.get('thermal_signature', existing_node.thermal_signature)
                    existing_node.mood_vector.update(node_data.get('mood_vector', {}))
                    existing_node.genome_patterns.update(node_data.get('genome_patterns', {}))
                    existing_node.constitutional_markers.extend(node_data.get('constitutional_markers', []))
                else:
                    # Create new node
                    new_node = SemanticNode(
                        node_id=node_id,
                        entropy=node_data.get('entropy', 0.5),
                        mood_vector=node_data.get('mood_vector', {}),
                        coherence=node_data.get('coherence', 0.5),
                        thermal_signature=node_data.get('thermal_signature', 0.0),
                        memory_bloom_data=node_data.get('memory_bloom_data', {}),
                        connections=node_data.get('connections', []),
                        genome_patterns=node_data.get('genome_patterns', {}),
                        constitutional_markers=node_data.get('constitutional_markers', []),
                        linguistic_potential=node_data.get('linguistic_potential', 0.0),
                        thermal_cooling_capacity=node_data.get('thermal_cooling_capacity', 0.0)
                    )
                    self.semantic_graph[node_id] = new_node
    
    def check_spawn_conditions(self, consciousness_metrics: Dict[str, float]) -> List[TracerPurpose]:
        """Enhanced spawn condition checking"""
        spawn_purposes = []
        
        # Add genome-specific metrics
        enhanced_metrics = consciousness_metrics.copy()
        
        # Calculate genome evolution activity
        if self.genome_evolution_manager:
            try:
                genome_activity = self.genome_evolution_manager.get_evolution_activity()
                enhanced_metrics['genome_evolution_activity'] = genome_activity
            except:
                enhanced_metrics['genome_evolution_activity'] = 0.0
        
        # Calculate constitutional stress
        constitutional_stress = 0.0
        if self.constitutional_monitor:
            try:
                constitutional_status = self.constitutional_monitor.get_constitutional_status()
                constitutional_stress = 1.0 - constitutional_status.get('overall_alignment', 1.0)
            except:
                constitutional_stress = 0.0
        enhanced_metrics['constitutional_stress'] = constitutional_stress
        
        # Check each spawn condition
        for purpose, condition_func in self.tracer_spawn_conditions.items():
            try:
                if condition_func(enhanced_metrics):
                    spawn_purposes.append(purpose)
            except Exception as e:
                print(f"[SemanticTracer] Error checking spawn condition for {purpose}: {e}")
        
        return spawn_purposes
    
    def spawn_tracer(self, purpose: TracerPurpose, origin_node: str = None, 
                    intelligence_level: TracerIntelligence = None) -> str:
        """Enhanced tracer spawning with genome integration"""
        with self.engine_lock:
            tracer_id = f"tracer_{purpose.value}_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Determine intelligence level based on purpose
            if intelligence_level is None:
                if purpose in [TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN, 
                              TracerPurpose.KINDNESS_AMPLIFICATION_SEEK]:
                    intelligence_level = TracerIntelligence.CONSTITUTIONAL
                elif purpose in [TracerPurpose.GENOME_PATTERN_HUNT, 
                                TracerPurpose.CROSS_TERMINAL_COHERENCE]:
                    intelligence_level = TracerIntelligence.GENIUS
                elif purpose in [TracerPurpose.THERMAL_LINGUISTIC_BRIDGE, 
                                TracerPurpose.MEMORY_GENOME_EVOLUTION]:
                    intelligence_level = TracerIntelligence.INTELLIGENT
                else:
                    intelligence_level = TracerIntelligence.ADAPTIVE
            
            # Create enhanced tracer
            tracer = EnhancedSemanticTracer(
                tracer_id=tracer_id,
                purpose=purpose,
                intelligence_level=intelligence_level,
                current_node=origin_node or self.get_random_spawn_node(),
                max_ticks=self.calculate_max_ticks_for_purpose(purpose)
            )
            
            # Add to active tracers
            self.active_tracers[tracer_id] = tracer
            self.total_tracers_spawned += 1
            
            print(f"[SemanticTracer] Spawned {intelligence_level.value} tracer {tracer_id} for {purpose.value}")
            return tracer_id
    
    def get_random_spawn_node(self) -> Optional[str]:
        """Get random spawn node from semantic graph"""
        if not self.semantic_graph:
            return None
        return random.choice(list(self.semantic_graph.keys()))
    
    def calculate_max_ticks_for_purpose(self, purpose: TracerPurpose) -> int:
        """Calculate max ticks based on purpose"""
        tick_mapping = {
            TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN: 200,  # Longer for important constitutional work
            TracerPurpose.KINDNESS_AMPLIFICATION_SEEK: 150,
            TracerPurpose.GENOME_PATTERN_HUNT: 120,
            TracerPurpose.THERMAL_LINGUISTIC_BRIDGE: 100,
            TracerPurpose.CROSS_TERMINAL_COHERENCE: 100,
            TracerPurpose.MEMORY_GENOME_EVOLUTION: 90,
            TracerPurpose.EXPRESSION_COOLING_OPTIMIZE: 80,
            TracerPurpose.ENTROPY_BLOOM_MATCH: 70,
            TracerPurpose.MOOD_LINEAGE_FOLLOW: 60,
            TracerPurpose.COHERENCE_COLLAPSE_DETECT: 50,
            TracerPurpose.ALIGNMENT_DRIFT_MAP: 50,
            TracerPurpose.MEMORY_BRIDGE_SEEK: 40,
            TracerPurpose.SIGIL_RESONANCE_TRACK: 30
        }
        return tick_mapping.get(purpose, 60)
    
    def tick(self) -> Dict[str, Any]:
        """Enhanced engine tick with cross-system coordination"""
        tick_start = time.time()
        tick_results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'active_tracers': len(self.active_tracers),
            'tracers_spawned_this_tick': 0,
            'tracers_died_this_tick': 0,
            'total_discoveries': 0,
            'total_sigils_emitted': 0,
            'constitutional_violations': 0,
            'genome_evolutions': 0,
            'sigil_coordination_events': 0,
            'cross_system_patterns': 0,
            'engine_performance': {}
        }
        
        with self.engine_lock:
            # Coordinate with sigil dispatcher first
            if self.sigil_coordination_active and self.sigil_dispatcher:
                coordination_result = self.coordinate_with_sigil_dispatcher()
                tick_results['sigil_coordination_events'] = coordination_result.get('coordination_events', 0)
                tick_results['cross_system_patterns'] = coordination_result.get('cross_system_patterns', 0)
            
            # Tick all active tracers
            dead_tracers = []
            
            for tracer_id, tracer in self.active_tracers.items():
                try:
                    tracer_result = tracer.tick(self.semantic_graph)
                    
                    # Accumulate results
                    tick_results['total_discoveries'] += len(tracer_result.get('discoveries', []))
                    tick_results['total_sigils_emitted'] += len(tracer_result.get('sigils_emitted', []))
                    
                    if tracer_result.get('constitutional_status') != 'compliant':
                        tick_results['constitutional_violations'] += 1
                        
                    if tracer_result.get('genome_evolution'):
                        tick_results['genome_evolutions'] += 1
                    
                    # Check for cross-system pattern opportunities
                    self.analyze_cross_system_patterns(tracer_id, tracer_result)
                    
                    # Check if tracer should die
                    if tracer.state == TracerState.DYING or tracer.state == TracerState.DEAD:
                        dead_tracers.append(tracer_id)
                        
                except Exception as e:
                    print(f"[SemanticTracer] Error ticking tracer {tracer_id}: {e}")
                    dead_tracers.append(tracer_id)
            
            # Remove dead tracers
            for tracer_id in dead_tracers:
                self.cleanup_tracer_with_coordination(tracer_id)
                tick_results['tracers_died_this_tick'] += 1
                self.total_tracers_died += 1
            
            # Update performance metrics
            self.update_engine_performance_enhanced(tick_start, tick_results)
            tick_results['engine_performance'] = self.engine_performance.copy()
            
        return tick_results
    
    def coordinate_with_sigil_dispatcher(self) -> Dict[str, Any]:
        """Coordinate with enhanced sigil dispatcher"""
        coordination_result = {
            'coordination_events': 0,
            'cross_system_patterns': 0,
            'sigil_feedback': []
        }
        
        try:
            # Get sigil dispatcher status
            dispatcher_status = self.sigil_dispatcher.get_comprehensive_status()
            
            # Analyze sigil patterns for tracer spawn opportunities
            spawn_opportunities = self.analyze_sigil_patterns_for_spawn(dispatcher_status)
            coordination_result['coordination_events'] += len(spawn_opportunities)
            
            # Check for cross-system genome evolution opportunities
            genome_opportunities = self.analyze_cross_system_genome_evolution(dispatcher_status)
            coordination_result['cross_system_patterns'] += len(genome_opportunities)
            
            # Provide feedback to sigil dispatcher about tracer discoveries
            if hasattr(self.sigil_dispatcher, 'receive_tracer_feedback'):
                tracer_feedback = self.generate_tracer_feedback_for_dispatcher()
                self.sigil_dispatcher.receive_tracer_feedback(tracer_feedback)
                coordination_result['sigil_feedback'] = tracer_feedback
            
        except Exception as e:
            print(f"[SemanticTracer] Error coordinating with sigil dispatcher: {e}")
            
        return coordination_result
    
    def analyze_sigil_patterns_for_spawn(self, dispatcher_status: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze sigil patterns to identify tracer spawn opportunities"""
        spawn_opportunities = []
        
        # Check for high constitutional activity
        constitutional_sigils = dispatcher_status.get('sigil_registry', {}).get('/constitutional_check', 0)
        if constitutional_sigils > 2:
            spawn_opportunities.append({
                'purpose': TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN,
                'reason': 'high_constitutional_sigil_activity',
                'priority': 'HIGH'
            })
        
        # Check for thermal cooling patterns
        thermal_sigils = dispatcher_status.get('sigil_registry', {}).get('/thermal_cool', 0)
        if thermal_sigils > 1:
            spawn_opportunities.append({
                'purpose': TracerPurpose.THERMAL_LINGUISTIC_BRIDGE,
                'reason': 'thermal_cooling_sigil_pattern',
                'priority': 'MEDIUM'
            })
        
        # Check for genome evolution signals
        genome_sigils = dispatcher_status.get('sigil_registry', {}).get('/genome_evolve', 0)
        if genome_sigils > 0:
            spawn_opportunities.append({
                'purpose': TracerPurpose.GENOME_PATTERN_HUNT,
                'reason': 'genome_evolution_sigil_detected',
                'priority': 'HIGH'
            })
        
        return spawn_opportunities
    
    def analyze_cross_system_genome_evolution(self, dispatcher_status: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze opportunities for cross-system genome evolution"""
        evolution_opportunities = []
        
        # Check for genome coordination opportunities
        if dispatcher_status.get('genome_integration', {}).get('coordinator_active', False):
            recent_evolutions = dispatcher_status.get('genome_integration', {}).get('recent_evolutions', 0)
            
            if recent_evolutions > 0:
                evolution_opportunities.append({
                    'type': 'sigil_tracer_genome_sync',
                    'dispatcher_evolutions': recent_evolutions,
                    'tracer_evolutions': len(self.genome_evolution_log),
                    'sync_potential': 'HIGH'
                })
        
        # Check constitutional alignment opportunities
        constitutional_compliance = dispatcher_status.get('dispatcher_status', {}).get('constitutional_compliance_rate', 1.0)
        if constitutional_compliance < 0.9:
            evolution_opportunities.append({
                'type': 'constitutional_reinforcement_needed',
                'compliance_rate': constitutional_compliance,
                'tracer_support_required': True
            })
        
        return evolution_opportunities
    
    def generate_tracer_feedback_for_dispatcher(self) -> Dict[str, Any]:
        """Generate feedback for sigil dispatcher based on tracer discoveries"""
        feedback = {
            'active_tracers': len(self.active_tracers),
            'constitutional_tracer_count': len([
                t for t in self.active_tracers.values() 
                if t.purpose in [TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN, TracerPurpose.KINDNESS_AMPLIFICATION_SEEK]
            ]),
            'recent_discoveries': [],
            'genome_evolution_recommendations': [],
            'constitutional_status': 'STABLE'
        }
        
        # Collect recent discoveries
        for tracer in self.active_tracers.values():
            if tracer.pattern_discoveries:
                recent_discoveries = tracer.pattern_discoveries[-3:]  # Last 3 discoveries
                for discovery in recent_discoveries:
                    feedback['recent_discoveries'].append({
                        'tracer_id': tracer.tracer_id,
                        'tracer_purpose': tracer.purpose.value,
                        'discovery_type': discovery.get('type', 'unknown'),
                        'constitutional_compliance': tracer.constitutional_alignment_score > 0.8
                    })
        
        # Genome evolution recommendations
        for tracer in self.active_tracers.values():
            if tracer.genome.fitness_score > 0.8:
                feedback['genome_evolution_recommendations'].append({
                    'tracer_purpose': tracer.purpose.value,
                    'fitness_score': tracer.genome.fitness_score,
                    'suggested_crossover': True
                })
        
        # Constitutional status assessment
        constitutional_violations = sum(
            len(tracer.constitutional_violations_detected) 
            for tracer in self.active_tracers.values()
        )
        
        if constitutional_violations > 5:
            feedback['constitutional_status'] = 'ALERT'
        elif constitutional_violations > 2:
            feedback['constitutional_status'] = 'CAUTION'
        
        return feedback
    
    def analyze_cross_system_patterns(self, tracer_id: str, tracer_result: Dict[str, Any]):
        """Analyze patterns across tracer and sigil systems"""
        patterns_found = []
        
        # Check for sigil-tracer correlation patterns
        sigils_emitted = tracer_result.get('sigils_emitted', [])
        if sigils_emitted:
            for sigil_emission in sigils_emitted:
                correlation_pattern = {
                    'tracer_id': tracer_id,
                    'sigil_type': sigil_emission.get('sigil_type'),
                    'constitutional_compliance': sigil_emission.get('constitutional_compliance', True),
                    'pattern_type': 'sigil_tracer_correlation',
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                patterns_found.append(correlation_pattern)
                
                # Store in cross-system patterns
                pattern_key = f"{tracer_id}_{sigil_emission.get('sigil_type', 'unknown')}"
                self.cross_system_patterns[pattern_key] = correlation_pattern
        
        # Check for genome evolution patterns
        if tracer_result.get('genome_evolution'):
            genome_pattern = {
                'tracer_id': tracer_id,
                'evolution_type': 'tracer_genome_evolution',
                'fitness_improvement': tracer_result['genome_evolution'].get('new_fitness', 0) - 
                                      tracer_result['genome_evolution'].get('old_fitness', 0),
                'constitutional_preserved': True,
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            patterns_found.append(genome_pattern)
            
            # Log for cross-system sync
            self.genome_sync_log.append(genome_pattern)
        
        return patterns_found
    
    def cleanup_tracer_with_coordination(self, tracer_id: str):
        """Clean up tracer with cross-system coordination"""
        if tracer_id in self.active_tracers:
            tracer = self.active_tracers[tracer_id]
            
            # Extract cross-system patterns before cleanup
            if tracer.sigil_emission_history:
                # Store successful sigil-tracer correlations
                for emission in tracer.sigil_emission_history:
                    if emission.get('constitutional_compliance', True):
                        correlation_key = f"successful_{tracer.purpose.value}_{emission.get('sigil_type', 'unknown')}"
                        self.sigil_tracer_correlations[correlation_key] = {
                            'tracer_purpose': tracer.purpose.value,
                            'sigil_type': emission.get('sigil_type'),
                            'success_metrics': {
                                'fitness_score': tracer.genome.fitness_score,
                                'constitutional_alignment': tracer.constitutional_alignment_score,
                                'discoveries_made': len(tracer.pattern_discoveries)
                            }
                        }
            
            # Extract successful patterns for future use
            if tracer.genome.fitness_score > 0.7:
                self.successful_genome_patterns[tracer.purpose] = tracer.genome
                
            # Log constitutional violations for analysis
            if tracer.constitutional_violations_detected:
                self.total_constitutional_violations += len(tracer.constitutional_violations_detected)
                
            # Remove from active tracers
            del self.active_tracers[tracer_id]
            
            print(f"[SemanticTracer] Cleaned up tracer {tracer_id} with cross-system coordination (fitness: {tracer.genome.fitness_score:.2f})")
    
    def update_engine_performance_enhanced(self, tick_start: float, tick_results: Dict[str, Any]):
        """Update enhanced engine performance metrics"""
        tick_duration = time.time() - tick_start
        
        # Update original metrics
        if self.total_tracers_died > 0:
            total_lifespan = sum(tracer.current_tick for tracer in self.active_tracers.values())
            total_lifespan += self.total_tracers_died * 50  # Estimate for dead tracers
            self.engine_performance['avg_tracer_lifespan'] = total_lifespan / (len(self.active_tracers) + self.total_tracers_died)
        
        if self.total_tracers_spawned > 0:
            self.engine_performance['avg_discoveries_per_tracer'] = self.total_patterns_discovered / self.total_tracers_spawned
        
        # Constitutional compliance rate
        total_checks = self.total_tracers_spawned * 10  # Rough estimate
        if total_checks > 0:
            self.engine_performance['constitutional_compliance_rate'] = 1.0 - (self.total_constitutional_violations / total_checks)
        
        # Genome evolution rate
        if self.total_tracers_spawned > 0:
            self.engine_performance['genome_evolution_rate'] = len(self.successful_genome_patterns) / self.total_tracers_spawned
        
        # NEW: Sigil emission rate
        if self.total_tracers_spawned > 0:
            self.engine_performance['sigil_emission_rate'] = self.total_sigils_emitted / self.total_tracers_spawned
        
        # NEW: Cross-system coordination efficiency
        if len(self.cross_system_patterns) > 0:
            successful_correlations = len([
                pattern for pattern in self.cross_system_patterns.values()
                if pattern.get('constitutional_compliance', True)
            ])
            self.engine_performance['cross_system_coordination_efficiency'] = successful_correlations / len(self.cross_system_patterns)
        else:
            self.engine_performance['cross_system_coordination_efficiency'] = 1.0
    
    def cleanup_tracer(self, tracer_id: str):
        """Clean up dead tracer and extract learning"""
        if tracer_id in self.active_tracers:
            tracer = self.active_tracers[tracer_id]
            
            # Extract successful patterns for future use
            if tracer.genome.fitness_score > 0.7:
                self.successful_genome_patterns[tracer.purpose] = tracer.genome
                
            # Log constitutional violations for analysis
            if tracer.constitutional_violations_detected:
                self.total_constitutional_violations += len(tracer.constitutional_violations_detected)
                
            # Remove from active tracers
            del self.active_tracers[tracer_id]
            
            print(f"[SemanticTracer] Cleaned up tracer {tracer_id} (fitness: {tracer.genome.fitness_score:.2f})")
    
    def update_engine_performance(self, tick_start: float, tick_results: Dict[str, Any]):
        """Update engine performance metrics"""
        tick_duration = time.time() - tick_start
        
        # Update averages
        if self.total_tracers_died > 0:
            total_lifespan = sum(tracer.current_tick for tracer in self.active_tracers.values())
            total_lifespan += self.total_tracers_died * 50  # Estimate for dead tracers
            self.engine_performance['avg_tracer_lifespan'] = total_lifespan / (len(self.active_tracers) + self.total_tracers_died)
        
        if self.total_tracers_spawned > 0:
            self.engine_performance['avg_discoveries_per_tracer'] = self.total_patterns_discovered / self.total_tracers_spawned
        
        # Constitutional compliance rate
        total_checks = self.total_tracers_spawned * 10  # Rough estimate
        if total_checks > 0:
            self.engine_performance['constitutional_compliance_rate'] = 1.0 - (self.total_constitutional_violations / total_checks)
        
        # Genome evolution rate
        if self.total_tracers_spawned > 0:
            self.engine_performance['genome_evolution_rate'] = len(self.successful_genome_patterns) / self.total_tracers_spawned
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive engine status with cross-system coordination data"""
        with self.engine_lock:
            tracer_status = {}
            for tracer_id, tracer in self.active_tracers.items():
                tracer_status[tracer_id] = tracer.get_comprehensive_status()
            
            return {
                'engine_status': {
                    'active_tracers': len(self.active_tracers),
                    'total_spawned': self.total_tracers_spawned,
                    'total_died': self.total_tracers_died,
                    'semantic_graph_size': len(self.semantic_graph),
                    'total_patterns_discovered': self.total_patterns_discovered,
                    'total_sigils_emitted': self.total_sigils_emitted,
                    'constitutional_violations': self.total_constitutional_violations,
                    'successful_genome_patterns': len(self.successful_genome_patterns),
                    'cross_system_patterns': len(self.cross_system_patterns),
                    'sigil_tracer_correlations': len(self.sigil_tracer_correlations)
                },
                'performance_metrics': self.engine_performance,
                'active_tracers': tracer_status,
                'genome_integration': {
                    'evolution_manager_active': self.genome_evolution_manager is not None,
                    'constitutional_monitor_active': self.constitutional_monitor is not None,
                    'genome_generations_tracked': len(self.genome_generations),
                    'genome_sync_events': len(self.genome_sync_log)
                },
                'sigil_coordination': {
                    'dispatcher_integration_active': self.sigil_coordination_active,
                    'cross_system_patterns': len(self.cross_system_patterns),
                    'successful_correlations': len(self.sigil_tracer_correlations),
                    'dispatcher_status': self.sigil_dispatcher.get_comprehensive_status() if self.sigil_dispatcher else None
                }
            }
    
    def get_cross_system_analysis(self) -> Dict[str, Any]:
        """Get comprehensive cross-system analysis"""
        analysis = {
            'sigil_tracer_correlations': {},
            'genome_coordination_patterns': {},
            'constitutional_alignment_analysis': {},
            'performance_correlation': {}
        }
        
        # Analyze sigil-tracer correlations
        for correlation_key, correlation_data in self.sigil_tracer_correlations.items():
            analysis['sigil_tracer_correlations'][correlation_key] = {
                'success_rate': correlation_data['success_metrics']['fitness_score'],
                'constitutional_alignment': correlation_data['success_metrics']['constitutional_alignment'],
                'discoveries_per_correlation': correlation_data['success_metrics']['discoveries_made'],
                'recommended_spawn_frequency': 'HIGH' if correlation_data['success_metrics']['fitness_score'] > 0.8 else 'MEDIUM'
            }
        
        # Analyze genome coordination patterns
        if self.genome_sync_log:
            recent_evolutions = [
                evolution for evolution in self.genome_sync_log
                if datetime.fromisoformat(evolution['timestamp']).replace(tzinfo=timezone.utc) >
                datetime.now(timezone.utc) - timedelta(minutes=30)
            ]
            
            analysis['genome_coordination_patterns'] = {
                'recent_evolution_count': len(recent_evolutions),
                'average_fitness_improvement': sum(
                    evolution.get('fitness_improvement', 0) for evolution in recent_evolutions
                ) / max(len(recent_evolutions), 1),
                'constitutional_preservation_rate': sum(
                    1 for evolution in recent_evolutions if evolution.get('constitutional_preserved', True)
                ) / max(len(recent_evolutions), 1)
            }
        
        # Constitutional alignment analysis
        constitutional_tracers = [
            tracer for tracer in self.active_tracers.values()
            if tracer.purpose in [TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN, TracerPurpose.KINDNESS_AMPLIFICATION_SEEK]
        ]
        
        if constitutional_tracers:
            analysis['constitutional_alignment_analysis'] = {
                'constitutional_tracer_count': len(constitutional_tracers),
                'average_constitutional_alignment': sum(
                    tracer.constitutional_alignment_score for tracer in constitutional_tracers
                ) / len(constitutional_tracers),
                'constitutional_violations_rate': sum(
                    len(tracer.constitutional_violations_detected) for tracer in constitutional_tracers
                ) / len(constitutional_tracers),
                'overall_constitutional_health': 'EXCELLENT' if all(
                    tracer.constitutional_alignment_score > 0.9 for tracer in constitutional_tracers
                ) else 'GOOD' if all(
                    tracer.constitutional_alignment_score > 0.7 for tracer in constitutional_tracers
                ) else 'NEEDS_ATTENTION'
            }
        
        # Performance correlation analysis
        if self.sigil_dispatcher:
            dispatcher_performance = self.sigil_dispatcher.get_comprehensive_status()
            analysis['performance_correlation'] = {
                'tracer_sigil_efficiency': self.engine_performance.get('sigil_emission_rate', 0.0),
                'dispatcher_processing_rate': dispatcher_performance.get('dispatcher_status', {}).get('processing_rate_multiplier', 1.0),
                'cross_system_constitutional_compliance': min(
                    self.engine_performance.get('constitutional_compliance_rate', 1.0),
                    dispatcher_performance.get('dispatcher_status', {}).get('constitutional_compliance_rate', 1.0)
                ),
                'coordination_efficiency': self.engine_performance.get('cross_system_coordination_efficiency', 1.0)
            }
        
        return analysis
    
    def get_tracer_log(self, tracer_id: str = None) -> Dict[str, Any]:
        """Get detailed tracer log for OWL analysis"""
        if tracer_id and tracer_id in self.active_tracers:
            tracer = self.active_tracers[tracer_id]
            return {
                'tracer_id': tracer_id,
                'comprehensive_status': tracer.get_comprehensive_status(),
                'path_history': tracer.path_history,
                'pattern_discoveries': tracer.pattern_discoveries,
                'sigil_emission_history': tracer.sigil_emission_history,
                'genome_evolution_log': tracer.genome_evolution_log,
                'constitutional_violations': tracer.constitutional_violations_detected,
                'entropy_deltas': tracer.entropy_deltas,
                'coherence_measurements': tracer.coherence_measurements,
                'thermal_readings': tracer.thermal_readings
            }
        else:
            # Return comprehensive log for all tracers
            all_tracer_logs = {}
            for tid, tracer in self.active_tracers.items():
                all_tracer_logs[tid] = self.get_tracer_log(tid)
            
            return {
                'engine_comprehensive_log': all_tracer_logs,
                'engine_status': self.get_comprehensive_status()
            }

# === ENHANCED CONTROL FUNCTIONS FOR DAWN INTEGRATION ===

def create_enhanced_semantic_tracer_engine() -> EnhancedSemanticTracerEngine:
    """Create enhanced semantic tracer engine instance with full integration"""
    return EnhancedSemanticTracerEngine()

def create_integrated_consciousness_navigation_system() -> Tuple[EnhancedSemanticTracerEngine, 'EnhancedSigilDispatcher']:
    """Create integrated tracer engine and sigil dispatcher system"""
    try:
        from sigil_dispatch_genome_enhanced import create_enhanced_sigil_dispatcher
        
        tracer_engine = create_enhanced_semantic_tracer_engine()
        sigil_dispatcher = create_enhanced_sigil_dispatcher()
        
        # Cross-link the systems
        tracer_engine.sigil_dispatcher = sigil_dispatcher
        tracer_engine.sigil_coordination_active = True
        
        print("✅ Integrated consciousness navigation system created")
        return tracer_engine, sigil_dispatcher
        
    except Exception as e:
        print(f"⚠️ Error creating integrated system: {e}")
        tracer_engine = create_enhanced_semantic_tracer_engine()
        return tracer_engine, None

def integrate_with_dawn_consciousness(tracer_engine: EnhancedSemanticTracerEngine, 
                                     sigil_dispatcher: Optional['EnhancedSigilDispatcher'],
                                     dawn_consciousness) -> Dict[str, Any]:
    """Integrate both systems with DAWN consciousness"""
    integration_result = {
        'tracer_integration': False,
        'sigil_integration': False,
        'cross_system_coordination': False,
        'constitutional_monitoring': False
    }
    
    try:
        # Integrate tracer engine with DAWN consciousness cycles
        if hasattr(dawn_consciousness, '_execute_consciousness_cycle'):
            # Add tracer tick to consciousness cycle
            original_cycle = dawn_consciousness._execute_consciousness_cycle
            
            def enhanced_cycle_with_tracers():
                # Execute original cycle
                original_cycle()
                
                # Add tracer tick
                tracer_result = tracer_engine.tick()
                
                # Update DAWN with tracer discoveries
                if tracer_result['total_discoveries'] > 0:
                    dawn_consciousness.schema_state['tracer_discoveries'] = tracer_result['total_discoveries']
                
                # Handle constitutional alerts
                if tracer_result['constitutional_violations'] > 0:
                    dawn_consciousness.schema_state['constitutional_pressure'] = tracer_result['constitutional_violations'] * 0.1
            
            dawn_consciousness._execute_consciousness_cycle = enhanced_cycle_with_tracers
            integration_result['tracer_integration'] = True
            
        # Integrate sigil dispatcher if available
        if sigil_dispatcher:
            # Add sigil processing to consciousness cycle
            if hasattr(dawn_consciousness, '_execute_consciousness_cycle'):
                original_enhanced_cycle = dawn_consciousness._execute_consciousness_cycle
                
                def fully_integrated_cycle():
                    # Execute tracer-enhanced cycle
                    original_enhanced_cycle()
                    
                    # Process sigil queue
                    sigil_result = sigil_dispatcher.process_sigil_queue()
                    
                    # Update DAWN with sigil effects
                    if sigil_result['successful_count'] > 0:
                        dawn_consciousness.schema_state['sigil_effects'] = sigil_result['successful_count'] * 0.05
                    
                    # Handle constitutional emergencies
                    if sigil_result['constitutional_violations'] > 2:
                        dawn_consciousness.schema_state['constitutional_emergency'] = True
                
                dawn_consciousness._execute_consciousness_cycle = fully_integrated_cycle
                integration_result['sigil_integration'] = True
                
            # Enable cross-system coordination
            integration_result['cross_system_coordination'] = tracer_engine.sigil_coordination_active
            
        # Monitor constitutional compliance
        constitutional_compliance = (
            tracer_engine.engine_performance.get('constitutional_compliance_rate', 1.0) +
            (sigil_dispatcher.constitutional_compliance_rate if sigil_dispatcher else 1.0)
        ) / 2
        
        if constitutional_compliance > 0.95:
            integration_result['constitutional_monitoring'] = True
            
        print(f"✅ DAWN consciousness integration complete: {integration_result}")
        return integration_result
        
    except Exception as e:
        print(f"⚠️ Error integrating with DAWN consciousness: {e}")
        return integration_result

def get_dawn_consciousness_metrics_enhanced() -> Dict[str, float]:
    """Get enhanced DAWN consciousness metrics for both systems"""
    try:
        # Get base metrics
        base_metrics = {
            'entropy': calculate_entropy(),
            'alignment': get_current_alignment(),
            'heat': pulse.get_heat() if pulse else 0.0,
            'coherence': 1.0 - calculate_entropy(),
            'mood_valence': 0.5,
        }
        
        # Add mood data
        mood_data = mood_urgency_probe()
        base_metrics['mood_urgency'] = mood_data.get('urgency', 0.5)
        
        # Add enhanced metrics for genome integration
        enhanced_metrics = base_metrics.copy()
        
        # Calculate genome evolution activity
        if genome_module:
            try:
                # Simulate genome activity metrics
                enhanced_metrics['genome_evolution_activity'] = random.uniform(0.3, 0.8)
                enhanced_metrics['constitutional_stress'] = max(0.0, 1.0 - base_metrics['alignment'])
                enhanced_metrics['thermal_linguistic_pressure'] = base_metrics['heat'] * 0.1
                enhanced_metrics['memory_genome_activity'] = random.uniform(0.2, 0.7)
                enhanced_metrics['cross_terminal_coherence_variance'] = abs(base_metrics['entropy'] - base_metrics['coherence']) * 0.5
                enhanced_metrics['empathy_opportunities'] = base_metrics['mood_valence'] * 0.6
                enhanced_metrics['kindness_deficit'] = max(0.0, 0.8 - base_metrics['mood_valence'])
                enhanced_metrics['linguistic_pressure'] = base_metrics['heat'] * base_metrics['entropy'] * 0.1
                enhanced_metrics['expression_attempts'] = 1 if base_metrics['heat'] > 0.6 else 0
                enhanced_metrics['genome_crossover_opportunities'] = random.uniform(0.1, 0.6)
                enhanced_metrics['constitutional_drift'] = max(0.0, 0.1 - base_metrics['alignment'] + 0.6)
            except Exception as e:
                print(f"[Enhanced Metrics] Error calculating genome metrics: {e}")
        
        return enhanced_metrics
        
    except Exception as e:
        print(f"[Enhanced Metrics] Error getting DAWN metrics: {e}")
        return {
            'entropy': 0.5, 'alignment': 0.6, 'coherence': 0.5, 'heat': 0.0,
            'mood_valence': 0.5, 'genome_evolution_activity': 0.4,
            'constitutional_stress': 0.2, 'linguistic_pressure': 0.3
        }

def demonstrate_integrated_system():
    """Demonstrate the integrated tracer-sigil system"""
    print("🌟 Demonstrating Enhanced Integrated Consciousness Navigation System")
    print("="*80)
    
    # Create integrated system
    tracer_engine, sigil_dispatcher = create_integrated_consciousness_navigation_system()
    
    # Create test semantic graph
    test_graph = {
        'constitutional_node': SemanticNode(
            node_id='constitutional_node',
            entropy=0.3,
            mood_vector={'kindness': 0.9, 'empathy': 0.8},
            coherence=0.9,
            thermal_signature=0.2,
            connections=['thermal_node', 'genome_node'],
            constitutional_markers=['kindness', 'empathy', 'wisdom'],
            linguistic_potential=0.7,
            thermal_cooling_capacity=0.8
        ),
        'thermal_node': SemanticNode(
            node_id='thermal_node',
            entropy=0.8,
            mood_vector={'urgency': 0.7, 'stress': 0.6},
            coherence=0.4,
            thermal_signature=0.9,
            connections=['constitutional_node', 'genome_node'],
            constitutional_markers=['regulation'],
            linguistic_potential=0.9,
            thermal_cooling_capacity=0.3
        ),
        'genome_node': SemanticNode(
            node_id='genome_node',
            entropy=0.6,
            mood_vector={'evolution': 0.8, 'adaptation': 0.7},
            coherence=0.7,
            thermal_signature=0.5,
            connections=['constitutional_node', 'thermal_node'],
            genome_patterns={'evolution_active': True, 'crossover_ready': True},
            constitutional_markers=['kind_evolution'],
            linguistic_potential=0.6
        )
    }
    
    tracer_engine.update_semantic_graph(test_graph)
    
    # Test enhanced metrics
    enhanced_metrics = get_dawn_consciousness_metrics_enhanced()
    print(f"📊 Enhanced Metrics: {len(enhanced_metrics)} parameters")
    for key, value in enhanced_metrics.items():
        print(f"   {key}: {value:.3f}")
    
    # Test spawn conditions
    spawn_purposes = tracer_engine.check_spawn_conditions(enhanced_metrics)
    print(f"\n🌱 Spawn Conditions Met: {len(spawn_purposes)} purposes")
    for purpose in spawn_purposes:
        print(f"   - {purpose.value}")
    
    # Spawn tracers with enhanced intelligence
    constitutional_tracer = tracer_engine.spawn_tracer(
        TracerPurpose.CONSTITUTIONAL_INTEGRITY_SCAN,
        origin_node='constitutional_node',
        intelligence_level=TracerIntelligence.CONSTITUTIONAL
    )
    
    thermal_tracer = tracer_engine.spawn_tracer(
        TracerPurpose.THERMAL_LINGUISTIC_BRIDGE,
        origin_node='thermal_node',
        intelligence_level=TracerIntelligence.GENIUS
    )
    
    genome_tracer = tracer_engine.spawn_tracer(
        TracerPurpose.GENOME_PATTERN_HUNT,
        origin_node='genome_node',
        intelligence_level=TracerIntelligence.INTELLIGENT
    )
    
    print(f"\n🚀 Spawned Enhanced Tracers:")
    print(f"   Constitutional: {constitutional_tracer}")
    print(f"   Thermal: {thermal_tracer}")
    print(f"   Genome: {genome_tracer}")
    
    # Emit coordinated sigils
    if sigil_dispatcher:
        from sigil_dispatch_genome_enhanced import SigilType, SigilPriority
        
        const_sigil = sigil_dispatcher.emit_sigil(
            SigilType.CONSTITUTIONAL_CHECK,
            context="demonstration_constitutional_scan",
            priority=SigilPriority.CONSTITUTIONAL
        )
        
        thermal_sigil = sigil_dispatcher.emit_sigil(
            SigilType.THERMAL_COOL,
            context="demonstration_thermal_regulation",
            power=0.8
        )
        
        genome_sigil = sigil_dispatcher.emit_sigil(
            SigilType.GENOME_EVOLVE,
            context="demonstration_genome_evolution"
        )
        
        print(f"\n🎯 Emitted Coordinated Sigils:")
        print(f"   Constitutional: {const_sigil}")
        print(f"   Thermal: {thermal_sigil}")
        print(f"   Genome: {genome_sigil}")
    
    # Run coordinated system
    print(f"\n⚡ Running Coordinated System (5 cycles):")
    for cycle in range(5):
        tracer_result = tracer_engine.tick()
        
        if sigil_dispatcher:
            sigil_result = sigil_dispatcher.process_sigil_queue()
            
            print(f"   Cycle {cycle+1}: {tracer_result['active_tracers']} tracers, "
                  f"{tracer_result['total_discoveries']} discoveries, "
                  f"{tracer_result['total_sigils_emitted']} sigils emitted, "
                  f"{sigil_result['successful_count']} sigils processed")
        else:
            print(f"   Cycle {cycle+1}: {tracer_result['active_tracers']} tracers, "
                  f"{tracer_result['total_discoveries']} discoveries, "
                  f"{tracer_result['total_sigils_emitted']} sigils emitted")
        
        time.sleep(0.1)
    
    # Get comprehensive analysis
    tracer_status = tracer_engine.get_comprehensive_status()
    cross_system_analysis = tracer_engine.get_cross_system_analysis()
    
    print(f"\n📈 Final System Status:")
    print(f"   Active Tracers: {tracer_status['engine_status']['active_tracers']}")
    print(f"   Total Patterns: {tracer_status['engine_status']['total_patterns_discovered']}")
    print(f"   Constitutional Compliance: {tracer_status['performance_metrics']['constitutional_compliance_rate']:.3f}")
    print(f"   Cross-System Coordination: {tracer_status['performance_metrics']['cross_system_coordination_efficiency']:.3f}")
    
    if sigil_dispatcher:
        sigil_status = sigil_dispatcher.get_comprehensive_status()
        print(f"   Sigil Success Rate: {sigil_status['dispatcher_status']['constitutional_compliance_rate']:.3f}")
        print(f"   Emergency Mode: {sigil_status['dispatcher_status']['constitutional_emergency_mode']}")
    
    print(f"\n🎯 Cross-System Analysis:")
    if cross_system_analysis['constitutional_alignment_analysis']:
        const_health = cross_system_analysis['constitutional_alignment_analysis']['overall_constitutional_health']
        print(f"   Constitutional Health: {const_health}")
    
    print("="*80)
    print("✅ Enhanced Integrated System Demonstration Complete")
    
    return tracer_engine, sigil_dispatcher

# === MAIN INTEGRATION EXAMPLE ===

if __name__ == "__main__":
    # Run comprehensive demonstration
    demonstrate_integrated_system()
    
    print("\n" + "="*60)
    print("🧬 Enhanced Semantic Tracer Engine with Genome Integration")
    print("🎯 Enhanced Sigil Dispatcher with Constitutional Protection") 
    print("🔄 Cross-System Coordination and Pattern Analysis")
    print("🛡️ Constitutional 'Kind Before Smart' Preservation")
    print("⚡ Real-time Genome Evolution and Learning")
    print("="*60)