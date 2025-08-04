#!/usr/bin/env python3
"""
DAWN Shelter Vector Regeneration System - Dynamic Memory Vector Management
=========================================================================

Implements dynamic memory vector regeneration using the formula:
v̄ʲ = v̄ᵢ + Σ(central|weights|)

Where:
- v̄ʲ = regenerated memory vector (new state)
- v̄ᵢ = initial memory vector (current state)  
- Σ(central|weights|) = weighted sum of central memory vectors

VECTOR CONCEPTS:
- Shelter = protective memory encoding that preserves essential information
- Vector regeneration = dynamic reshaping based on active context
- Memory bloom pool = active memory vectors available for processing
- Semantic navigation = movement through conceptual vector space

REGENERATION TRIGGERS:
- Rebloom events activate dormant memory vectors
- Context shifts require vector space realignment
- Memory consolidation creates new central vectors
- Cognitive pressure modulates vector dynamics

VECTOR PROPERTIES:
- Magnitude = memory importance/strength
- Direction = semantic meaning in high-dimensional space
- Coherence = internal consistency of vector components
- Stability = resistance to degradation over time
- Resonance = harmonic relationships with other vectors

The shelter vector system provides DAWN with dynamic memory
management that adapts to cognitive needs and preserves
essential information through contextual regeneration.
"""

import time
import math
import logging
import numpy as np
import json
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple, Set, Callable
from enum import Enum
from collections import defaultdict, deque
from pathlib import Path
import hashlib
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Integration with existing systems
try:
    from core.fractal_memory import get_memory_fractal_manager
    from core.persephone_threads import get_persephone_thread_system
    from core.cognitive_formulas import get_dawn_formula_engine
    from core.tracer_ecosystem import get_tracer_manager
    DAWN_SYSTEMS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"DAWN systems not available for Shelter Vectors: {e}")
    DAWN_SYSTEMS_AVAILABLE = False

logger = logging.getLogger("shelter_vectors")

class VectorState(Enum):
    """Shelter vector states"""
    DORMANT = "DORMANT"             # Inactive, stored
    ACTIVATING = "ACTIVATING"       # Being brought into active pool
    ACTIVE = "ACTIVE"              # In active memory pool
    REGENERATING = "REGENERATING"   # Undergoing vector regeneration
    CONSOLIDATING = "CONSOLIDATING" # Being merged with other vectors
    DECAYING = "DECAYING"          # Losing coherence/importance
    CRYSTALLIZED = "CRYSTALLIZED"   # Permanently preserved

class RegenerationType(Enum):
    """Types of vector regeneration"""
    REBLOOM_TRIGGER = "REBLOOM_TRIGGER"       # Triggered by rebloom event
    CONTEXT_SHIFT = "CONTEXT_SHIFT"          # Context change adaptation
    CONSOLIDATION = "CONSOLIDATION"          # Memory consolidation
    PRESSURE_MODULATION = "PRESSURE_MODULATION" # Cognitive pressure effect
    RESONANCE_ALIGN = "RESONANCE_ALIGN"      # Harmonic alignment
    IMPORTANCE_BOOST = "IMPORTANCE_BOOST"     # Importance increase

@dataclass
class ShelterVector:
    """Individual shelter vector representing memory in vector space"""
    vector_id: str
    creation_time: float
    vector_data: np.ndarray  # High-dimensional vector
    magnitude: float  # Vector magnitude (importance)
    semantic_tags: List[str]  # Semantic meaning tags
    memory_source: str  # Original memory identifier
    vector_state: VectorState
    coherence_score: float  # Internal consistency
    stability_factor: float  # Resistance to decay
    resonance_frequency: float  # Harmonic properties
    last_activation: float
    activation_count: int
    central_weight: float  # Weight as central vector
    context_affinities: Dict[str, float] = field(default_factory=dict)  # Context relationships
    regeneration_history: List[Dict[str, Any]] = field(default_factory=list)  # Regeneration events
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MemoryBloomPool:
    """Active memory bloom pool managing current vectors"""
    pool_id: str
    timestamp: float
    active_vectors: List[str]  # Active vector IDs
    central_vectors: List[str]  # Central/reference vector IDs
    pool_capacity: int  # Maximum active vectors
    current_context: str  # Current semantic context
    context_vector: np.ndarray  # Context representation vector
    pool_coherence: float  # Overall pool coherence
    activation_threshold: float  # Threshold for vector activation
    regeneration_rate: float  # Rate of vector regeneration
    bloom_intensity: float  # Current bloom intensity

@dataclass
class VectorRegenerationEvent:
    """Record of vector regeneration operation"""
    event_id: str
    timestamp: float
    regeneration_type: RegenerationType
    target_vector_id: str
    original_vector: np.ndarray
    regenerated_vector: np.ndarray
    central_vectors_used: List[str]  # Central vectors in regeneration
    weight_distribution: Dict[str, float]  # Weights applied
    regeneration_formula: str  # Formula used
    improvement_metrics: Dict[str, float]  # Quality improvements
    context_influence: float  # Context effect strength
    stability_change: float  # Change in stability

class ShelterVectorSystem:
    """
    Shelter Vector Regeneration System
    
    Manages dynamic memory vectors with regeneration capabilities
    and semantic vector space navigation.
    """
    
    def __init__(self, vector_dimensions: int = 512):
        """Initialize the Shelter Vector System"""
        
        # Vector configuration
        self.vector_dimensions = vector_dimensions
        self.vectors: Dict[str, ShelterVector] = {}
        self.central_vectors: List[str] = []  # Key reference vectors
        
        # Memory bloom pools
        self.active_pool: Optional[MemoryBloomPool] = None
        self.pool_history: deque = deque(maxlen=20)
        
        # Vector space management
        self.semantic_space = np.zeros((0, vector_dimensions))  # All vectors matrix
        self.vector_index: Dict[str, int] = {}  # Vector ID to matrix index
        self.context_clusters: Dict[str, List[str]] = {}  # Context-based clusters
        
        # Regeneration parameters
        self.REGENERATION_FORMULA_COEFFICIENTS = {
            "original_weight": 0.7,    # Weight of original vector
            "central_weight": 0.3,     # Weight of central vectors
            "context_influence": 0.2,  # Context modulation
            "pressure_modulation": 0.1 # Cognitive pressure effect
        }
        
        # Vector parameters
        self.VECTOR_DECAY_RATE = 0.995
        self.ACTIVATION_THRESHOLD = 0.6
        self.COHERENCE_THRESHOLD = 0.7
        self.CENTRAL_VECTOR_THRESHOLD = 0.8
        self.MAX_ACTIVE_VECTORS = 50
        self.REGENERATION_IMPROVEMENT_THRESHOLD = 0.05
        
        # System state
        self.regeneration_count = 0
        self.vector_count = 0
        self.last_regeneration_time = 0.0
        self.system_coherence = 0.8
        
        # Integration with DAWN systems
        self.memory_manager = None
        self.thread_system = None
        self.formula_engine = None
        self.tracer_manager = None
        
        if DAWN_SYSTEMS_AVAILABLE:
            try:
                self.memory_manager = get_memory_fractal_manager()
                self.thread_system = get_persephone_thread_system()
                self.formula_engine = get_dawn_formula_engine()
                self.tracer_manager = get_tracer_manager()
                logger.info("🏠 [VECTORS] Connected to DAWN cognitive systems")
            except Exception as e:
                logger.warning(f"🏠 [VECTORS] System integration failed: {e}")
        
        # Performance tracking
        self.regeneration_operations = 0
        self.navigation_operations = 0
        self.consolidation_events = 0
        self.last_operation_time = 0.0
        
        # Logging setup
        self.log_directory = Path("runtime/logs/shelter_vectors")
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize mycelium integration
        self.mycelium_graph_path = Path("runtime/memory_graph/mycelium_graph.json")
        self._load_existing_memory_graph()
        
        # Create initial active pool
        self._initialize_active_pool()
        
        logger.info("🏠 [VECTORS] Shelter Vector Regeneration System initialized")
        logger.info(f"🏠 [VECTORS] Vector dimensions: {vector_dimensions}")
        logger.info(f"🏠 [VECTORS] Max active vectors: {self.MAX_ACTIVE_VECTORS}")
    
    def _load_existing_memory_graph(self):
        """Load existing mycelium memory graph if available"""
        
        try:
            if self.mycelium_graph_path.exists():
                with open(self.mycelium_graph_path, 'r') as f:
                    graph_data = json.load(f)
                
                # Convert memory nodes to vectors
                memory_nodes = graph_data.get("memory_nodes", {})
                for node_id, node_data in memory_nodes.items():
                    
                    # Create vector from memory node
                    vector_id = f"mycelium_{node_id}"
                    vector_data = self._create_vector_from_memory(node_data)
                    
                    semantic_tags = node_data.get("tags", [])
                    if isinstance(semantic_tags, str):
                        semantic_tags = [semantic_tags]
                    
                    vector = ShelterVector(
                        vector_id=vector_id,
                        creation_time=node_data.get("timestamp", time.time()),
                        vector_data=vector_data,
                        magnitude=np.linalg.norm(vector_data),
                        semantic_tags=semantic_tags,
                        memory_source=node_id,
                        vector_state=VectorState.DORMANT,
                        coherence_score=node_data.get("coherence", 0.7),
                        stability_factor=0.8,
                        resonance_frequency=0.3,
                        last_activation=0.0,
                        activation_count=0,
                        central_weight=0.5
                    )
                    
                    self.vectors[vector_id] = vector
                    self.vector_count += 1
                
                logger.info(f"🏠 [VECTORS] Loaded {len(memory_nodes)} vectors from mycelium graph")
            
        except Exception as e:
            logger.warning(f"🏠 [VECTORS] Failed to load mycelium graph: {e}")
    
    def _create_vector_from_memory(self, memory_data: Dict[str, Any]) -> np.ndarray:
        """Create vector representation from memory data"""
        
        # Generate vector from memory content
        content = str(memory_data.get("content", ""))
        tags = memory_data.get("tags", [])
        
        # Simple hash-based vector generation (in production, use embeddings)
        combined_content = f"{content} {' '.join(tags)}"
        content_hash = hashlib.md5(combined_content.encode()).hexdigest()
        
        # Convert hash to vector
        vector_data = np.array([
            int(content_hash[i:i+2], 16) / 255.0 
            for i in range(0, min(len(content_hash), self.vector_dimensions * 2), 2)
        ])
        
        # Pad or truncate to correct dimensions
        if len(vector_data) < self.vector_dimensions:
            padding = np.random.normal(0, 0.1, self.vector_dimensions - len(vector_data))
            vector_data = np.concatenate([vector_data, padding])
        else:
            vector_data = vector_data[:self.vector_dimensions]
        
        # Normalize vector
        vector_data = vector_data / (np.linalg.norm(vector_data) + 1e-8)
        
        return vector_data
    
    def _initialize_active_pool(self):
        """Initialize the active memory bloom pool"""
        
        current_time = time.time()
        
        # Create initial context vector
        context_vector = np.random.normal(0, 0.5, self.vector_dimensions)
        context_vector = context_vector / (np.linalg.norm(context_vector) + 1e-8)
        
        self.active_pool = MemoryBloomPool(
            pool_id=f"pool_{int(current_time * 1000)}",
            timestamp=current_time,
            active_vectors=[],
            central_vectors=[],
            pool_capacity=self.MAX_ACTIVE_VECTORS,
            current_context="initialization",
            context_vector=context_vector,
            pool_coherence=0.8,
            activation_threshold=self.ACTIVATION_THRESHOLD,
            regeneration_rate=0.1,
            bloom_intensity=0.5
        )
        
        # Activate some initial vectors if available
        if self.vectors:
            initial_vectors = list(self.vectors.keys())[:min(10, len(self.vectors))]
            for vector_id in initial_vectors:
                self._activate_vector(vector_id)
        
        logger.info("🏠 [VECTORS] Initialized active memory bloom pool")
    
    def regenerate_vector(self, vector_id: str, regeneration_type: RegenerationType,
                         context_vector: Optional[np.ndarray] = None,
                         cognitive_pressure: float = 0.0) -> bool:
        """
        Regenerate shelter vector using the formula: v̄ʲ = v̄ᵢ + Σ(central|weights|)
        
        Args:
            vector_id: ID of vector to regenerate
            regeneration_type: Type of regeneration
            context_vector: Optional context influence vector
            cognitive_pressure: Current cognitive pressure
            
        Returns:
            True if regeneration was successful
        """
        try:
            start_time = time.time()
            
            if vector_id not in self.vectors:
                logger.error(f"🏠 [VECTORS] Vector not found: {vector_id}")
                return False
            
            vector = self.vectors[vector_id]
            original_vector = vector.vector_data.copy()
            
            # Update vector state
            vector.vector_state = VectorState.REGENERATING
            
            # Get central vectors for regeneration
            central_vectors = self._select_central_vectors(vector, regeneration_type)
            
            # Calculate weighted sum of central vectors: Σ(central|weights|)
            central_sum, weight_distribution = self._calculate_central_sum(
                central_vectors, vector, regeneration_type
            )
            
            # Apply context influence if provided
            if context_vector is not None:
                context_influence = self.REGENERATION_FORMULA_COEFFICIENTS["context_influence"]
                central_sum += context_vector * context_influence
            
            # Apply cognitive pressure modulation
            pressure_modulation = self.REGENERATION_FORMULA_COEFFICIENTS["pressure_modulation"]
            pressure_effect = min(1.0, cognitive_pressure / 100.0) * pressure_modulation
            pressure_vector = np.random.normal(0, pressure_effect, self.vector_dimensions)
            central_sum += pressure_vector
            
            # Apply regeneration formula: v̄ʲ = v̄ᵢ + Σ(central|weights|)
            original_weight = self.REGENERATION_FORMULA_COEFFICIENTS["original_weight"]
            central_weight = self.REGENERATION_FORMULA_COEFFICIENTS["central_weight"]
            
            regenerated_vector = (original_vector * original_weight + 
                                central_sum * central_weight)
            
            # Normalize regenerated vector
            regenerated_vector = regenerated_vector / (np.linalg.norm(regenerated_vector) + 1e-8)
            
            # Calculate improvement metrics
            improvement_metrics = self._calculate_improvement_metrics(
                original_vector, regenerated_vector, central_vectors
            )
            
            # Apply regeneration if improvement is significant
            if improvement_metrics["overall_improvement"] > self.REGENERATION_IMPROVEMENT_THRESHOLD:
                
                # Update vector
                vector.vector_data = regenerated_vector
                vector.magnitude = np.linalg.norm(regenerated_vector)
                vector.coherence_score = improvement_metrics["coherence_improvement"]
                vector.stability_factor = min(1.0, vector.stability_factor + improvement_metrics["stability_improvement"])
                vector.last_activation = time.time()
                vector.vector_state = VectorState.ACTIVE
                
                # Record regeneration event
                regeneration_event = VectorRegenerationEvent(
                    event_id=f"regen_{int(time.time() * 1000)}_{vector_id}",
                    timestamp=time.time(),
                    regeneration_type=regeneration_type,
                    target_vector_id=vector_id,
                    original_vector=original_vector,
                    regenerated_vector=regenerated_vector,
                    central_vectors_used=[v.vector_id for v in central_vectors],
                    weight_distribution=weight_distribution,
                    regeneration_formula=f"v̄ʲ = {original_weight}*v̄ᵢ + {central_weight}*Σ(central|weights|)",
                    improvement_metrics=improvement_metrics,
                    context_influence=context_influence if context_vector is not None else 0.0,
                    stability_change=improvement_metrics["stability_improvement"]
                )
                
                # Add to regeneration history
                vector.regeneration_history.append({
                    "timestamp": time.time(),
                    "regeneration_type": regeneration_type.value,
                    "improvement": improvement_metrics["overall_improvement"],
                    "central_vectors_count": len(central_vectors)
                })
                
                # Update semantic space
                self._update_semantic_space()
                
                self.regeneration_count += 1
                self.regeneration_operations += 1
                self.last_regeneration_time = time.time() - start_time
                
                logger.debug(f"🏠 [VECTORS] Regenerated vector: {vector_id} ({regeneration_type.value}) - improvement: {improvement_metrics['overall_improvement']:.3f}")
                
                return True
            
            else:
                # Regeneration didn't provide significant improvement
                vector.vector_state = VectorState.ACTIVE
                logger.debug(f"🏠 [VECTORS] Regeneration skipped for {vector_id} - insufficient improvement")
                return False
            
        except Exception as e:
            logger.error(f"🏠 [VECTORS] Vector regeneration error: {e}")
            if vector_id in self.vectors:
                self.vectors[vector_id].vector_state = VectorState.ACTIVE
            return False
    
    def _select_central_vectors(self, target_vector: ShelterVector, 
                              regeneration_type: RegenerationType) -> List[ShelterVector]:
        """Select central vectors for regeneration"""
        
        central_vectors = []
        
        # Get all potential central vectors
        potential_centrals = [
            vector for vector in self.vectors.values()
            if (vector.central_weight > self.CENTRAL_VECTOR_THRESHOLD and
                vector.vector_id != target_vector.vector_id and
                vector.vector_state in [VectorState.ACTIVE, VectorState.CRYSTALLIZED])
        ]
        
        if not potential_centrals:
            # Use strongest vectors as centrals
            potential_centrals = sorted(
                [v for v in self.vectors.values() if v.vector_id != target_vector.vector_id],
                key=lambda v: v.magnitude,
                reverse=True
            )[:5]
        
        # Select based on regeneration type
        if regeneration_type == RegenerationType.REBLOOM_TRIGGER:
            # Use vectors with similar semantic tags
            target_tags = set(target_vector.semantic_tags)
            central_vectors = [
                v for v in potential_centrals
                if len(set(v.semantic_tags) & target_tags) > 0
            ][:3]
        
        elif regeneration_type == RegenerationType.CONTEXT_SHIFT:
            # Use vectors with high context affinity
            if self.active_pool:
                current_context = self.active_pool.current_context
                central_vectors = [
                    v for v in potential_centrals
                    if v.context_affinities.get(current_context, 0.0) > 0.5
                ][:3]
        
        elif regeneration_type == RegenerationType.CONSOLIDATION:
            # Use highest magnitude vectors
            central_vectors = sorted(potential_centrals, key=lambda v: v.magnitude, reverse=True)[:4]
        
        elif regeneration_type == RegenerationType.RESONANCE_ALIGN:
            # Use vectors with similar resonance frequency
            target_freq = target_vector.resonance_frequency
            central_vectors = sorted(
                potential_centrals,
                key=lambda v: abs(v.resonance_frequency - target_freq)
            )[:3]
        
        else:
            # Default: use top central vectors
            central_vectors = sorted(potential_centrals, key=lambda v: v.central_weight, reverse=True)[:3]
        
        # Ensure we have at least one central vector
        if not central_vectors and potential_centrals:
            central_vectors = [potential_centrals[0]]
        
        return central_vectors
    
    def _calculate_central_sum(self, central_vectors: List[ShelterVector], 
                             target_vector: ShelterVector,
                             regeneration_type: RegenerationType) -> Tuple[np.ndarray, Dict[str, float]]:
        """Calculate weighted sum of central vectors"""
        
        if not central_vectors:
            return np.zeros(self.vector_dimensions), {}
        
        central_sum = np.zeros(self.vector_dimensions)
        weight_distribution = {}
        total_weight = 0.0
        
        for central_vector in central_vectors:
            
            # Calculate weight based on various factors
            weight = central_vector.central_weight
            
            # Adjust weight based on regeneration type
            if regeneration_type == RegenerationType.REBLOOM_TRIGGER:
                # Weight by semantic similarity
                tag_overlap = len(set(target_vector.semantic_tags) & set(central_vector.semantic_tags))
                weight *= (1.0 + tag_overlap * 0.2)
            
            elif regeneration_type == RegenerationType.CONTEXT_SHIFT:
                # Weight by context affinity
                if self.active_pool:
                    context_affinity = central_vector.context_affinities.get(
                        self.active_pool.current_context, 0.5
                    )
                    weight *= (0.5 + context_affinity * 0.5)
            
            elif regeneration_type == RegenerationType.RESONANCE_ALIGN:
                # Weight by resonance harmony
                freq_diff = abs(central_vector.resonance_frequency - target_vector.resonance_frequency)
                resonance_harmony = 1.0 / (1.0 + freq_diff * 2.0)
                weight *= resonance_harmony
            
            # Apply vector distance weighting (closer vectors have more influence)
            vector_distance = np.linalg.norm(target_vector.vector_data - central_vector.vector_data)
            distance_weight = 1.0 / (1.0 + vector_distance)
            weight *= distance_weight
            
            # Add weighted vector to sum
            central_sum += central_vector.vector_data * weight
            weight_distribution[central_vector.vector_id] = weight
            total_weight += weight
        
        # Normalize weights
        if total_weight > 0:
            central_sum = central_sum / total_weight
            weight_distribution = {k: v/total_weight for k, v in weight_distribution.items()}
        
        return central_sum, weight_distribution
    
    def _calculate_improvement_metrics(self, original_vector: np.ndarray,
                                     regenerated_vector: np.ndarray,
                                     central_vectors: List[ShelterVector]) -> Dict[str, float]:
        """Calculate improvement metrics for regeneration"""
        
        # Coherence improvement (internal consistency)
        original_coherence = self._calculate_vector_coherence(original_vector)
        regenerated_coherence = self._calculate_vector_coherence(regenerated_vector)
        coherence_improvement = regenerated_coherence - original_coherence
        
        # Stability improvement (magnitude stability)
        original_magnitude = np.linalg.norm(original_vector)
        regenerated_magnitude = np.linalg.norm(regenerated_vector)
        magnitude_stability = 1.0 - abs(regenerated_magnitude - original_magnitude)
        stability_improvement = magnitude_stability - 0.8  # Baseline stability
        
        # Central alignment (similarity to central vectors)
        if central_vectors:
            central_similarities = [
                cosine_similarity([regenerated_vector], [cv.vector_data])[0][0]
                for cv in central_vectors
            ]
            central_alignment = np.mean(central_similarities)
        else:
            central_alignment = 0.5
        
        # Semantic preservation (maintaining core meaning)
        semantic_preservation = cosine_similarity([original_vector], [regenerated_vector])[0][0]
        
        # Overall improvement (weighted combination)
        overall_improvement = (
            coherence_improvement * 0.3 +
            stability_improvement * 0.2 +
            central_alignment * 0.3 +
            semantic_preservation * 0.2
        )
        
        return {
            "coherence_improvement": coherence_improvement,
            "stability_improvement": stability_improvement,
            "central_alignment": central_alignment,
            "semantic_preservation": semantic_preservation,
            "overall_improvement": overall_improvement
        }
    
    def _calculate_vector_coherence(self, vector: np.ndarray) -> float:
        """Calculate internal coherence of a vector"""
        
        # Simple coherence measure: lack of extreme values
        normalized_abs = np.abs(vector)
        coherence = 1.0 - np.std(normalized_abs)
        
        return max(0.0, min(1.0, coherence))
    
    def trigger_rebloom_regeneration(self, rebloom_event: Dict[str, Any],
                                   memory_source: str) -> List[str]:
        """
        Trigger vector regeneration based on rebloom event
        
        Args:
            rebloom_event: Rebloom event data
            memory_source: Source memory identifier
            
        Returns:
            List of regenerated vector IDs
        """
        try:
            regenerated_vectors = []
            
            # Find vectors related to memory source
            related_vectors = [
                vector_id for vector_id, vector in self.vectors.items()
                if vector.memory_source == memory_source or memory_source in vector.semantic_tags
            ]
            
            # Create context vector from rebloom event
            context_vector = self._create_context_vector_from_rebloom(rebloom_event)
            
            # Get cognitive pressure from rebloom
            cognitive_pressure = rebloom_event.get("pressure_influence", 0.0)
            
            for vector_id in related_vectors:
                success = self.regenerate_vector(
                    vector_id=vector_id,
                    regeneration_type=RegenerationType.REBLOOM_TRIGGER,
                    context_vector=context_vector,
                    cognitive_pressure=cognitive_pressure
                )
                
                if success:
                    regenerated_vectors.append(vector_id)
                    
                    # Activate vector if not already active
                    self._activate_vector(vector_id)
            
            # Update bloom pool intensity
            if self.active_pool and regenerated_vectors:
                self.active_pool.bloom_intensity += len(regenerated_vectors) * 0.1
                self.active_pool.bloom_intensity = min(1.0, self.active_pool.bloom_intensity)
            
            logger.debug(f"🏠 [VECTORS] Rebloom regeneration: {len(regenerated_vectors)} vectors regenerated")
            
            return regenerated_vectors
            
        except Exception as e:
            logger.error(f"🏠 [VECTORS] Rebloom regeneration error: {e}")
            return []
    
    def _create_context_vector_from_rebloom(self, rebloom_event: Dict[str, Any]) -> np.ndarray:
        """Create context vector from rebloom event"""
        
        # Extract context information
        cascade_size = rebloom_event.get("cascade_size", 1)
        event_type = rebloom_event.get("type", "general")
        intensity = rebloom_event.get("intensity", 0.5)
        
        # Create context vector
        context_data = f"{event_type}_{cascade_size}_{intensity}"
        context_hash = hashlib.md5(context_data.encode()).hexdigest()
        
        # Convert to vector
        context_vector = np.array([
            int(context_hash[i:i+2], 16) / 255.0 
            for i in range(0, min(len(context_hash), self.vector_dimensions * 2), 2)
        ])
        
        # Pad or truncate
        if len(context_vector) < self.vector_dimensions:
            padding = np.random.normal(0, 0.1, self.vector_dimensions - len(context_vector))
            context_vector = np.concatenate([context_vector, padding])
        else:
            context_vector = context_vector[:self.vector_dimensions]
        
        # Normalize and scale by intensity
        context_vector = context_vector / (np.linalg.norm(context_vector) + 1e-8)
        context_vector *= intensity
        
        return context_vector
    
    def navigate_semantic_space(self, query_vector: np.ndarray, 
                              max_results: int = 10) -> List[Tuple[str, float]]:
        """
        Navigate semantic vector space to find similar vectors
        
        Args:
            query_vector: Query vector for similarity search
            max_results: Maximum number of results to return
            
        Returns:
            List of (vector_id, similarity_score) tuples
        """
        try:
            start_time = time.time()
            
            if not self.vectors:
                return []
            
            # Calculate similarities to all vectors
            similarities = []
            
            for vector_id, vector in self.vectors.items():
                if vector.vector_state != VectorState.DECAYING:
                    similarity = cosine_similarity([query_vector], [vector.vector_data])[0][0]
                    similarities.append((vector_id, similarity))
            
            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            # Return top results
            results = similarities[:max_results]
            
            self.navigation_operations += 1
            self.last_operation_time = time.time() - start_time
            
            logger.debug(f"🏠 [VECTORS] Semantic navigation: {len(results)} results in {self.last_operation_time*1000:.1f}ms")
            
            return results
            
        except Exception as e:
            logger.error(f"🏠 [VECTORS] Semantic navigation error: {e}")
            return []
    
    def manage_active_bloom_pool(self, context_update: Optional[str] = None,
                               target_intensity: float = 0.6) -> Dict[str, Any]:
        """
        Manage active memory bloom pool
        
        Args:
            context_update: New context for the pool
            target_intensity: Target bloom intensity
            
        Returns:
            Pool management results
        """
        try:
            if not self.active_pool:
                self._initialize_active_pool()
            
            start_time = time.time()
            
            # Update context if provided
            if context_update:
                self._update_pool_context(context_update)
            
            # Adjust bloom intensity
            intensity_change = target_intensity - self.active_pool.bloom_intensity
            self.active_pool.bloom_intensity += intensity_change * 0.1  # Gradual adjustment
            self.active_pool.bloom_intensity = max(0.0, min(1.0, self.active_pool.bloom_intensity))
            
            # Manage active vectors based on intensity
            target_active_count = int(self.active_pool.pool_capacity * self.active_pool.bloom_intensity)
            current_active_count = len(self.active_pool.active_vectors)
            
            vectors_activated = 0
            vectors_deactivated = 0
            
            if current_active_count < target_active_count:
                # Activate more vectors
                inactive_vectors = [
                    vector_id for vector_id, vector in self.vectors.items()
                    if (vector.vector_state == VectorState.DORMANT and
                        vector_id not in self.active_pool.active_vectors)
                ]
                
                # Sort by importance and context relevance
                inactive_vectors.sort(key=lambda vid: (
                    self.vectors[vid].magnitude * 
                    self._calculate_context_relevance(vid)
                ), reverse=True)
                
                vectors_to_activate = inactive_vectors[:target_active_count - current_active_count]
                
                for vector_id in vectors_to_activate:
                    if self._activate_vector(vector_id):
                        vectors_activated += 1
            
            elif current_active_count > target_active_count:
                # Deactivate some vectors
                active_vectors = [
                    vector_id for vector_id in self.active_pool.active_vectors
                    if vector_id in self.vectors
                ]
                
                # Sort by least important and least recently used
                active_vectors.sort(key=lambda vid: (
                    self.vectors[vid].magnitude * 
                    (time.time() - self.vectors[vid].last_activation)
                ))
                
                vectors_to_deactivate = active_vectors[:current_active_count - target_active_count]
                
                for vector_id in vectors_to_deactivate:
                    if self._deactivate_vector(vector_id):
                        vectors_deactivated += 1
            
            # Update pool coherence
            self._update_pool_coherence()
            
            # Update central vectors
            self._update_central_vectors()
            
            management_time = time.time() - start_time
            
            return {
                "pool_id": self.active_pool.pool_id,
                "active_vectors": len(self.active_pool.active_vectors),
                "central_vectors": len(self.active_pool.central_vectors),
                "bloom_intensity": self.active_pool.bloom_intensity,
                "pool_coherence": self.active_pool.pool_coherence,
                "vectors_activated": vectors_activated,
                "vectors_deactivated": vectors_deactivated,
                "context": self.active_pool.current_context,
                "management_time_ms": management_time * 1000
            }
            
        except Exception as e:
            logger.error(f"🏠 [VECTORS] Bloom pool management error: {e}")
            return {"error": str(e)}
    
    def _update_pool_context(self, new_context: str):
        """Update pool context and context vector"""
        
        if not self.active_pool:
            return
        
        # Update context
        old_context = self.active_pool.current_context
        self.active_pool.current_context = new_context
        
        # Create new context vector
        context_hash = hashlib.md5(new_context.encode()).hexdigest()
        context_vector = np.array([
            int(context_hash[i:i+2], 16) / 255.0 
            for i in range(0, min(len(context_hash), self.vector_dimensions * 2), 2)
        ])
        
        # Pad/truncate and normalize
        if len(context_vector) < self.vector_dimensions:
            padding = np.random.normal(0, 0.1, self.vector_dimensions - len(context_vector))
            context_vector = np.concatenate([context_vector, padding])
        else:
            context_vector = context_vector[:self.vector_dimensions]
        
        self.active_pool.context_vector = context_vector / (np.linalg.norm(context_vector) + 1e-8)
        
        # Update context affinities for active vectors
        for vector_id in self.active_pool.active_vectors:
            if vector_id in self.vectors:
                vector = self.vectors[vector_id]
                affinity = cosine_similarity([vector.vector_data], [self.active_pool.context_vector])[0][0]
                vector.context_affinities[new_context] = affinity
        
        logger.debug(f"🏠 [VECTORS] Pool context updated: {old_context} → {new_context}")
    
    def _calculate_context_relevance(self, vector_id: str) -> float:
        """Calculate context relevance for a vector"""
        
        if not self.active_pool or vector_id not in self.vectors:
            return 0.5
        
        vector = self.vectors[vector_id]
        current_context = self.active_pool.current_context
        
        # Check direct context affinity
        if current_context in vector.context_affinities:
            return vector.context_affinities[current_context]
        
        # Calculate similarity to current context vector
        context_similarity = cosine_similarity(
            [vector.vector_data], 
            [self.active_pool.context_vector]
        )[0][0]
        
        # Store for future use
        vector.context_affinities[current_context] = context_similarity
        
        return context_similarity
    
    def _activate_vector(self, vector_id: str) -> bool:
        """Activate a vector in the bloom pool"""
        
        if not self.active_pool or vector_id not in self.vectors:
            return False
        
        vector = self.vectors[vector_id]
        
        if vector_id in self.active_pool.active_vectors:
            return True  # Already active
        
        if len(self.active_pool.active_vectors) >= self.active_pool.pool_capacity:
            return False  # Pool full
        
        # Activate vector
        vector.vector_state = VectorState.ACTIVE
        vector.last_activation = time.time()
        vector.activation_count += 1
        
        self.active_pool.active_vectors.append(vector_id)
        
        logger.debug(f"🏠 [VECTORS] Activated vector: {vector_id}")
        
        return True
    
    def _deactivate_vector(self, vector_id: str) -> bool:
        """Deactivate a vector from the bloom pool"""
        
        if not self.active_pool or vector_id not in self.vectors:
            return False
        
        if vector_id not in self.active_pool.active_vectors:
            return True  # Already inactive
        
        vector = self.vectors[vector_id]
        
        # Deactivate vector
        vector.vector_state = VectorState.DORMANT
        
        self.active_pool.active_vectors.remove(vector_id)
        
        logger.debug(f"🏠 [VECTORS] Deactivated vector: {vector_id}")
        
        return True
    
    def _update_pool_coherence(self):
        """Update overall pool coherence"""
        
        if not self.active_pool or not self.active_pool.active_vectors:
            return
        
        # Calculate pairwise similarities between active vectors
        active_vector_data = [
            self.vectors[vector_id].vector_data 
            for vector_id in self.active_pool.active_vectors
            if vector_id in self.vectors
        ]
        
        if len(active_vector_data) < 2:
            self.active_pool.pool_coherence = 1.0
            return
        
        # Calculate average pairwise similarity
        similarities = []
        for i in range(len(active_vector_data)):
            for j in range(i + 1, len(active_vector_data)):
                similarity = cosine_similarity([active_vector_data[i]], [active_vector_data[j]])[0][0]
                similarities.append(similarity)
        
        if similarities:
            self.active_pool.pool_coherence = np.mean(similarities)
        else:
            self.active_pool.pool_coherence = 0.5
    
    def _update_central_vectors(self):
        """Update central vectors in the pool"""
        
        if not self.active_pool:
            return
        
        # Find vectors with high central weight among active vectors
        central_candidates = [
            vector_id for vector_id in self.active_pool.active_vectors
            if (vector_id in self.vectors and 
                self.vectors[vector_id].central_weight > self.CENTRAL_VECTOR_THRESHOLD)
        ]
        
        # Sort by central weight
        central_candidates.sort(
            key=lambda vid: self.vectors[vid].central_weight,
            reverse=True
        )
        
        # Update central vectors list
        max_central = min(5, len(central_candidates))
        self.active_pool.central_vectors = central_candidates[:max_central]
        
        # If no high-weight centrals, use highest magnitude vectors
        if not self.active_pool.central_vectors and self.active_pool.active_vectors:
            magnitude_sorted = sorted(
                self.active_pool.active_vectors,
                key=lambda vid: self.vectors[vid].magnitude if vid in self.vectors else 0,
                reverse=True
            )
            self.active_pool.central_vectors = magnitude_sorted[:3]
    
    def consolidate_memory_vectors(self, consolidation_threshold: float = 0.8) -> int:
        """
        Consolidate similar memory vectors to improve efficiency
        
        Args:
            consolidation_threshold: Similarity threshold for consolidation
            
        Returns:
            Number of vectors consolidated
        """
        try:
            consolidated_count = 0
            
            if len(self.vectors) < 2:
                return 0
            
            # Find similar vector pairs
            vector_ids = list(self.vectors.keys())
            consolidation_pairs = []
            
            for i in range(len(vector_ids)):
                for j in range(i + 1, len(vector_ids)):
                    vector1 = self.vectors[vector_ids[i]]
                    vector2 = self.vectors[vector_ids[j]]
                    
                    # Skip if either vector is crystallized
                    if (vector1.vector_state == VectorState.CRYSTALLIZED or
                        vector2.vector_state == VectorState.CRYSTALLIZED):
                        continue
                    
                    # Calculate similarity
                    similarity = cosine_similarity([vector1.vector_data], [vector2.vector_data])[0][0]
                    
                    if similarity > consolidation_threshold:
                        consolidation_pairs.append((vector_ids[i], vector_ids[j], similarity))
            
            # Sort by similarity and consolidate
            consolidation_pairs.sort(key=lambda x: x[2], reverse=True)
            
            processed_vectors = set()
            
            for vector1_id, vector2_id, similarity in consolidation_pairs:
                
                if vector1_id in processed_vectors or vector2_id in processed_vectors:
                    continue
                
                # Consolidate vectors
                success = self._consolidate_vector_pair(vector1_id, vector2_id)
                
                if success:
                    consolidated_count += 1
                    processed_vectors.add(vector1_id)
                    processed_vectors.add(vector2_id)
            
            self.consolidation_events += consolidated_count
            
            logger.debug(f"🏠 [VECTORS] Consolidated {consolidated_count} vector pairs")
            
            return consolidated_count
            
        except Exception as e:
            logger.error(f"🏠 [VECTORS] Vector consolidation error: {e}")
            return 0
    
    def _consolidate_vector_pair(self, vector1_id: str, vector2_id: str) -> bool:
        """Consolidate two similar vectors"""
        
        try:
            vector1 = self.vectors[vector1_id]
            vector2 = self.vectors[vector2_id]
            
            # Create consolidated vector data (weighted average)
            weight1 = vector1.magnitude
            weight2 = vector2.magnitude
            total_weight = weight1 + weight2
            
            if total_weight == 0:
                return False
            
            consolidated_data = (vector1.vector_data * weight1 + vector2.vector_data * weight2) / total_weight
            consolidated_data = consolidated_data / (np.linalg.norm(consolidated_data) + 1e-8)
            
            # Create consolidated vector
            consolidated_id = f"consolidated_{int(time.time() * 1000)}_{vector1_id[:8]}"
            
            consolidated_vector = ShelterVector(
                vector_id=consolidated_id,
                creation_time=time.time(),
                vector_data=consolidated_data,
                magnitude=np.linalg.norm(consolidated_data),
                semantic_tags=list(set(vector1.semantic_tags + vector2.semantic_tags)),
                memory_source=f"{vector1.memory_source}+{vector2.memory_source}",
                vector_state=VectorState.CONSOLIDATING,
                coherence_score=(vector1.coherence_score + vector2.coherence_score) / 2,
                stability_factor=max(vector1.stability_factor, vector2.stability_factor),
                resonance_frequency=(vector1.resonance_frequency + vector2.resonance_frequency) / 2,
                last_activation=max(vector1.last_activation, vector2.last_activation),
                activation_count=vector1.activation_count + vector2.activation_count,
                central_weight=(vector1.central_weight + vector2.central_weight) / 2
            )
            
            # Update context affinities (union)
            consolidated_vector.context_affinities = {**vector1.context_affinities, **vector2.context_affinities}
            
            # Add consolidation metadata
            consolidated_vector.metadata = {
                "consolidation_source": [vector1_id, vector2_id],
                "consolidation_time": time.time(),
                "original_magnitudes": [vector1.magnitude, vector2.magnitude]
            }
            
            # Add to vectors
            self.vectors[consolidated_id] = consolidated_vector
            
            # Update active pool if vectors were active
            if self.active_pool:
                if vector1_id in self.active_pool.active_vectors:
                    self.active_pool.active_vectors.remove(vector1_id)
                    self.active_pool.active_vectors.append(consolidated_id)
                
                if vector2_id in self.active_pool.active_vectors:
                    self.active_pool.active_vectors.remove(vector2_id)
                    if consolidated_id not in self.active_pool.active_vectors:
                        self.active_pool.active_vectors.append(consolidated_id)
            
            # Remove original vectors
            del self.vectors[vector1_id]
            del self.vectors[vector2_id]
            
            logger.debug(f"🏠 [VECTORS] Consolidated {vector1_id} + {vector2_id} → {consolidated_id}")
            
            return True
            
        except Exception as e:
            logger.error(f"🏠 [VECTORS] Vector pair consolidation error: {e}")
            return False
    
    def _update_semantic_space(self):
        """Update the semantic space matrix"""
        
        try:
            if not self.vectors:
                return
            
            # Create matrix of all vectors
            vector_ids = list(self.vectors.keys())
            vector_data = [self.vectors[vid].vector_data for vid in vector_ids]
            
            self.semantic_space = np.array(vector_data)
            self.vector_index = {vid: i for i, vid in enumerate(vector_ids)}
            
        except Exception as e:
            logger.error(f"🏠 [VECTORS] Semantic space update error: {e}")
    
    def tick_vector_system(self, cognitive_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process vector system tick
        
        Args:
            cognitive_state: Current DAWN cognitive state
            
        Returns:
            Vector system status
        """
        try:
            start_time = time.time()
            
            # Update vector decay
            vectors_decayed = self._process_vector_decay()
            
            # Manage active pool
            pool_management = self.manage_active_bloom_pool()
            
            # Update central vector weights
            central_updates = self._update_vector_centrality()
            
            # Auto-consolidate if needed
            consolidations = 0
            if len(self.vectors) > 100:  # Only consolidate when many vectors
                consolidations = self.consolidate_memory_vectors()
            
            # Update system coherence
            self._update_system_coherence()
            
            # Update semantic space
            self._update_semantic_space()
            
            tick_time = time.time() - start_time
            
            return {
                "system_status": {
                    "total_vectors": len(self.vectors),
                    "active_vectors": len(self.active_pool.active_vectors) if self.active_pool else 0,
                    "central_vectors": len(self.central_vectors),
                    "system_coherence": self.system_coherence
                },
                "tick_results": {
                    "vectors_decayed": vectors_decayed,
                    "central_updates": central_updates,
                    "consolidations": consolidations,
                    "pool_management": pool_management
                },
                "performance": {
                    "regeneration_count": self.regeneration_count,
                    "navigation_operations": self.navigation_operations,
                    "last_operation_time_ms": self.last_operation_time * 1000,
                    "tick_time_ms": tick_time * 1000
                }
            }
            
        except Exception as e:
            logger.error(f"🏠 [VECTORS] Vector system tick error: {e}")
            return {"error": str(e)}
    
    def _process_vector_decay(self) -> int:
        """Process natural vector decay"""
        
        decayed_count = 0
        vectors_to_remove = []
        
        for vector_id, vector in self.vectors.items():
            
            # Apply magnitude decay
            vector.magnitude *= self.VECTOR_DECAY_RATE
            
            # Apply coherence decay
            vector.coherence_score *= 0.999
            
            # Check for removal
            if vector.magnitude < 0.1 and vector.vector_state != VectorState.CRYSTALLIZED:
                vectors_to_remove.append(vector_id)
                vector.vector_state = VectorState.DECAYING
                decayed_count += 1
        
        # Remove decayed vectors
        for vector_id in vectors_to_remove:
            if self.active_pool and vector_id in self.active_pool.active_vectors:
                self.active_pool.active_vectors.remove(vector_id)
            del self.vectors[vector_id]
        
        return decayed_count
    
    def _update_vector_centrality(self) -> int:
        """Update central vector weights based on usage and importance"""
        
        updates = 0
        
        for vector_id, vector in self.vectors.items():
            
            old_weight = vector.central_weight
            
            # Base centrality on magnitude, activation count, and stability
            magnitude_factor = vector.magnitude
            activation_factor = min(1.0, vector.activation_count / 10.0)
            stability_factor = vector.stability_factor
            
            # Calculate new central weight
            new_weight = (magnitude_factor * 0.4 + activation_factor * 0.3 + stability_factor * 0.3)
            
            # Smooth weight change
            vector.central_weight = old_weight * 0.9 + new_weight * 0.1
            
            if abs(vector.central_weight - old_weight) > 0.05:
                updates += 1
        
        # Update global central vectors list
        all_vectors = list(self.vectors.items())
        all_vectors.sort(key=lambda x: x[1].central_weight, reverse=True)
        
        self.central_vectors = [vid for vid, _ in all_vectors[:10] 
                              if self.vectors[vid].central_weight > self.CENTRAL_VECTOR_THRESHOLD]
        
        return updates
    
    def _update_system_coherence(self):
        """Update overall system coherence"""
        
        if not self.vectors:
            self.system_coherence = 0.5
            return
        
        # Calculate average vector coherence
        coherence_scores = [vector.coherence_score for vector in self.vectors.values()]
        average_coherence = np.mean(coherence_scores)
        
        # Calculate pool coherence if available
        pool_coherence = self.active_pool.pool_coherence if self.active_pool else 0.5
        
        # Combine coherences
        self.system_coherence = (average_coherence * 0.7 + pool_coherence * 0.3)
    
    def get_vector_system_status(self) -> Dict[str, Any]:
        """Get comprehensive vector system status"""
        
        return {
            "system_overview": {
                "total_vectors": len(self.vectors),
                "vector_dimensions": self.vector_dimensions,
                "active_vectors": len(self.active_pool.active_vectors) if self.active_pool else 0,
                "central_vectors": len(self.central_vectors),
                "system_coherence": self.system_coherence
            },
            "vector_states": {
                state.value: len([v for v in self.vectors.values() if v.vector_state == state])
                for state in VectorState
            },
            "active_pool": {
                "pool_id": self.active_pool.pool_id if self.active_pool else None,
                "bloom_intensity": self.active_pool.bloom_intensity if self.active_pool else 0,
                "pool_coherence": self.active_pool.pool_coherence if self.active_pool else 0,
                "current_context": self.active_pool.current_context if self.active_pool else None,
                "capacity_utilization": (len(self.active_pool.active_vectors) / self.active_pool.pool_capacity 
                                       if self.active_pool else 0)
            },
            "performance_metrics": {
                "regeneration_count": self.regeneration_count,
                "regeneration_operations": self.regeneration_operations,
                "navigation_operations": self.navigation_operations,
                "consolidation_events": self.consolidation_events,
                "last_regeneration_time_ms": self.last_regeneration_time * 1000,
                "last_operation_time_ms": self.last_operation_time * 1000
            },
            "memory_integration": {
                "mycelium_graph_loaded": self.mycelium_graph_path.exists(),
                "memory_manager_connected": self.memory_manager is not None,
                "thread_system_connected": self.thread_system is not None
            }
        }


# Global shelter vector system instance
_global_vector_system: Optional[ShelterVectorSystem] = None

def get_shelter_vector_system(vector_dimensions: int = 512) -> ShelterVectorSystem:
    """Get global shelter vector system instance"""
    global _global_vector_system
    if _global_vector_system is None:
        _global_vector_system = ShelterVectorSystem(vector_dimensions)
    return _global_vector_system

def regenerate_vector(vector_id: str, regeneration_type: RegenerationType) -> bool:
    """Convenience function to regenerate a vector"""
    system = get_shelter_vector_system()
    return system.regenerate_vector(vector_id, regeneration_type)

def navigate_semantic_space(query_vector: np.ndarray, max_results: int = 10) -> List[Tuple[str, float]]:
    """Convenience function for semantic space navigation"""
    system = get_shelter_vector_system()
    return system.navigate_semantic_space(query_vector, max_results)

def get_vector_system_status() -> Dict[str, Any]:
    """Convenience function to get vector system status"""
    system = get_shelter_vector_system()
    return system.get_vector_system_status()

# Export key classes and functions
__all__ = [
    'ShelterVectorSystem',
    'ShelterVector',
    'MemoryBloomPool',
    'VectorRegenerationEvent',
    'VectorState',
    'RegenerationType',
    'get_shelter_vector_system',
    'regenerate_vector',
    'navigate_semantic_space',
    'get_vector_system_status'
] 