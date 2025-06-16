"""
DAWN Memory Management System
Persistent memory system with emotional context, pattern tracking, and intelligent retrieval.
Implements semantic similarity search, time decay, and memory consolidation.
"""

import json
import time
import math
import hashlib
import pickle
import gzip
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import re
import statistics

logger = logging.getLogger(__name__)

@dataclass
class MemoryTrace:
    """Single memory trace with full context"""
    memory_id: str
    timestamp: float
    input_text: str
    response_text: str
    emotional_state: str
    consciousness_state: Dict[str, Any]
    metrics_snapshot: Dict[str, float]
    interaction_outcome: str  # "successful", "neutral", "problematic"
    pattern_tags: List[str]
    semantic_keywords: List[str]
    emotional_intensity: float
    retrieval_count: int
    last_retrieved: float
    memory_strength: float
    consolidation_level: int  # 0=raw, 1=processed, 2=consolidated, 3=core

@dataclass
class AssociationLink:
    """Memory association between concepts"""
    from_concept: str
    to_concept: str
    strength: float
    frequency: int
    last_reinforced: float
    association_type: str  # "causal", "temporal", "semantic", "emotional"
    context_tags: List[str]

@dataclass
class PatternCluster:
    """Clustered memory patterns"""
    cluster_id: str
    pattern_signature: str
    member_memories: List[str]  # memory_ids
    frequency: int
    average_outcome: float
    dominant_emotion: str
    pattern_strength: float
    last_updated: float

@dataclass
class EchoKey:
    """Context-aware memory retrieval key"""
    current_state: Dict[str, Any]
    query_context: str
    emotional_resonance: float
    temporal_relevance: float
    pattern_match_strength: float
    retrieved_memories: List[str]  # memory_ids
    confidence_score: float

class MemoryManager:
    """Advanced memory management system for DAWN consciousness"""
    
    def __init__(self, memory_directory: str = "memories"):
        self.memory_directory = Path(memory_directory)
        self.memory_directory.mkdir(exist_ok=True)
        
        # Memory storage structures
        self.memory_traces: Dict[str, MemoryTrace] = {}
        self.association_network: Dict[str, List[AssociationLink]] = defaultdict(list)
        self.pattern_clusters: Dict[str, PatternCluster] = {}
        self.semantic_index: Dict[str, Set[str]] = defaultdict(set)  # keyword -> memory_ids
        self.emotional_index: Dict[str, List[str]] = defaultdict(list)  # emotion -> memory_ids
        
        # Memory management parameters
        self.max_active_memories = 10000  # Maximum memories in active storage
        self.consolidation_threshold = 0.7  # Threshold for memory consolidation
        self.decay_rate = 0.99  # Daily decay rate for memory strength
        self.retrieval_boost = 1.1  # Strength boost when memory is retrieved
        self.similarity_threshold = 0.6  # Minimum similarity for associations
        
        # Working memory (temporary, high-access memories)
        self.working_memory: deque = deque(maxlen=50)
        self.recent_patterns: deque = deque(maxlen=100)
        
        # Memory statistics
        self.total_memories_stored = 0
        self.total_retrievals = 0
        self.consolidation_cycles = 0
        self.last_consolidation = time.time()
        
        # Load existing memories
        self._load_memory_state()
        
        logger.info(f"Memory Manager initialized with {len(self.memory_traces)} memories")
    
    def store_interaction(self, input_text: str, response_text: str, 
                         emotional_state: str, consciousness_state: Dict[str, Any],
                         metrics_snapshot: Dict[str, float], 
                         interaction_outcome: str = "successful") -> str:
        """Store a complete interaction in memory with full context"""
        
        # Generate unique memory ID
        content_hash = hashlib.md5(f"{input_text}:{response_text}:{time.time()}".encode()).hexdigest()
        memory_id = f"mem_{int(time.time())}_{content_hash[:8]}"
        
        # Extract semantic keywords and patterns
        semantic_keywords = self._extract_semantic_keywords(input_text, response_text)
        pattern_tags = self._identify_patterns(input_text, emotional_state, consciousness_state)
        
        # Calculate emotional intensity
        emotional_intensity = self._calculate_emotional_intensity(
            emotional_state, consciousness_state, metrics_snapshot
        )
        
        # Create memory trace
        memory_trace = MemoryTrace(
            memory_id=memory_id,
            timestamp=time.time(),
            input_text=input_text,
            response_text=response_text,
            emotional_state=emotional_state,
            consciousness_state=consciousness_state.copy(),
            metrics_snapshot=metrics_snapshot.copy(),
            interaction_outcome=interaction_outcome,
            pattern_tags=pattern_tags,
            semantic_keywords=semantic_keywords,
            emotional_intensity=emotional_intensity,
            retrieval_count=0,
            last_retrieved=0.0,
            memory_strength=1.0,
            consolidation_level=0
        )
        
        # Store in active memory
        self.memory_traces[memory_id] = memory_trace
        self.working_memory.append(memory_id)
        
        # Update indices
        self._update_semantic_index(memory_id, semantic_keywords)
        self._update_emotional_index(memory_id, emotional_state)
        
        # Create associations with recent memories
        self._create_associations(memory_id, memory_trace)
        
        # Update pattern clusters
        self._update_pattern_clusters(memory_id, memory_trace)
        
        # Check if consolidation is needed
        if len(self.memory_traces) > self.max_active_memories:
            self._trigger_consolidation()
        
        self.total_memories_stored += 1
        logger.debug(f"Stored memory {memory_id}: {input_text[:50]}...")
        
        return memory_id
    
    def retrieve_similar(self, input_text: str, limit: int = 10, 
                        min_similarity: float = None) -> List[Tuple[str, float]]:
        """Retrieve memories similar to the given input with similarity scores"""
        
        if min_similarity is None:
            min_similarity = self.similarity_threshold
        
        # Extract query keywords
        query_keywords = self._extract_keywords(input_text)
        
        # Calculate similarity scores for all memories
        similarity_scores = []
        
        for memory_id, memory_trace in self.memory_traces.items():
            # Skip if memory is too weak
            if memory_trace.memory_strength < 0.1:
                continue
            
            # Calculate multiple similarity components
            semantic_sim = self._calculate_semantic_similarity(query_keywords, memory_trace.semantic_keywords)
            pattern_sim = self._calculate_pattern_similarity(input_text, memory_trace.input_text)
            temporal_relevance = self._calculate_temporal_relevance(memory_trace.timestamp)
            
            # Combined similarity score with weighting
            combined_score = (
                semantic_sim * 0.4 +
                pattern_sim * 0.3 +
                temporal_relevance * 0.2 +
                memory_trace.memory_strength * 0.1
            )
            
            if combined_score >= min_similarity:
                similarity_scores.append((memory_id, combined_score))
        
        # Sort by similarity and return top results
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Boost memory strength for retrieved memories
        for memory_id, _ in similarity_scores[:limit]:
            self._boost_memory(memory_id)
        
        self.total_retrievals += len(similarity_scores[:limit])
        return similarity_scores[:limit]
    
    def get_echo_key(self, current_state: Dict[str, Any], query_context: str = "") -> EchoKey:
        """Generate an echo key for context-aware memory retrieval"""
        
        # Analyze current emotional and consciousness state
        emotional_resonance = self._calculate_current_emotional_resonance(current_state)
        
        # Find temporally relevant memories
        temporal_relevance = self._calculate_temporal_context_relevance(current_state)
        
        # Match patterns with current state
        pattern_matches = self._find_pattern_matches(current_state, query_context)
        pattern_match_strength = max([match[1] for match in pattern_matches] + [0.0])
        
        # Retrieve most relevant memories
        if query_context:
            similar_memories = self.retrieve_similar(query_context, limit=5)
        else:
            similar_memories = self._retrieve_by_state(current_state, limit=5)
        
        retrieved_memory_ids = [mem_id for mem_id, _ in similar_memories]
        
        # Calculate confidence score
        confidence_score = min(1.0, (
            emotional_resonance * 0.3 +
            temporal_relevance * 0.2 +
            pattern_match_strength * 0.3 +
            (len(retrieved_memory_ids) / 5.0) * 0.2
        ))
        
        echo_key = EchoKey(
            current_state=current_state.copy(),
            query_context=query_context,
            emotional_resonance=emotional_resonance,
            temporal_relevance=temporal_relevance,
            pattern_match_strength=pattern_match_strength,
            retrieved_memories=retrieved_memory_ids,
            confidence_score=confidence_score
        )
        
        logger.debug(f"Generated echo key with confidence {confidence_score:.3f}")
        return echo_key
    
    def consolidate_memories(self, force: bool = False) -> Dict[str, Any]:
        """Consolidate memories to compress history and strengthen important patterns"""
        
        if not force and time.time() - self.last_consolidation < 3600:  # Once per hour
            return {"status": "skipped", "reason": "too_recent"}
        
        logger.info("Starting memory consolidation cycle...")
        
        consolidation_stats = {
            "memories_before": len(self.memory_traces),
            "patterns_before": len(self.pattern_clusters),
            "associations_before": sum(len(links) for links in self.association_network.values()),
            "memories_consolidated": 0,
            "patterns_merged": 0,
            "weak_memories_removed": 0
        }
        
        # 1. Apply time decay to all memories
        self._apply_time_decay()
        
        # 2. Remove very weak memories
        weak_memories = [
            mid for mid, mem in self.memory_traces.items() 
            if mem.memory_strength < 0.05 and mem.retrieval_count == 0
        ]
        
        for memory_id in weak_memories:
            self._remove_memory(memory_id)
            consolidation_stats["weak_memories_removed"] += 1
        
        # 3. Consolidate similar memories
        consolidated_count = self._consolidate_similar_memories()
        consolidation_stats["memories_consolidated"] = consolidated_count
        
        # 4. Merge overlapping pattern clusters
        merged_count = self._merge_pattern_clusters()
        consolidation_stats["patterns_merged"] = merged_count
        
        # 5. Strengthen important associations
        self._strengthen_important_associations()
        
        # 6. Update consolidation tracking
        self.consolidation_cycles += 1
        self.last_consolidation = time.time()
        
        consolidation_stats.update({
            "memories_after": len(self.memory_traces),
            "patterns_after": len(self.pattern_clusters),
            "associations_after": sum(len(links) for links in self.association_network.values()),
            "consolidation_cycle": self.consolidation_cycles
        })
        
        logger.info(f"Consolidation complete: {consolidation_stats}")
        return consolidation_stats
    
    def get_memory_by_id(self, memory_id: str) -> Optional[MemoryTrace]:
        """Retrieve a specific memory by ID"""
        memory = self.memory_traces.get(memory_id)
        if memory:
            self._boost_memory(memory_id)
        return memory
    
    def get_association_map(self, concept: str, depth: int = 2) -> Dict[str, Any]:
        """Get association map for a concept with specified depth"""
        
        associations = {"concept": concept, "associations": {}, "strength_total": 0.0}
        visited = set()
        
        def _explore_associations(current_concept: str, current_depth: int):
            if current_depth <= 0 or current_concept in visited:
                return
            
            visited.add(current_concept)
            
            for link in self.association_network.get(current_concept, []):
                if link.strength > 0.3:  # Only strong associations
                    associations["associations"][link.to_concept] = {
                        "strength": link.strength,
                        "frequency": link.frequency,
                        "type": link.association_type,
                        "last_reinforced": link.last_reinforced
                    }
                    associations["strength_total"] += link.strength
                    
                    if current_depth > 1:
                        _explore_associations(link.to_concept, current_depth - 1)
        
        _explore_associations(concept, depth)
        return associations
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory system statistics"""
        
        current_time = time.time()
        
        # Memory distribution by consolidation level
        consolidation_dist = defaultdict(int)
        emotion_dist = defaultdict(int)
        strength_values = []
        
        for memory in self.memory_traces.values():
            consolidation_dist[memory.consolidation_level] += 1
            emotion_dist[memory.emotional_state] += 1
            strength_values.append(memory.memory_strength)
        
        # Pattern cluster statistics
        pattern_stats = {
            "total_clusters": len(self.pattern_clusters),
            "avg_cluster_size": statistics.mean([len(cluster.member_memories) for cluster in self.pattern_clusters.values()]) if self.pattern_clusters else 0,
            "strongest_pattern": max(self.pattern_clusters.values(), key=lambda x: x.pattern_strength).pattern_signature if self.pattern_clusters else None
        }
        
        return {
            "total_memories": len(self.memory_traces),
            "total_retrievals": self.total_retrievals,
            "consolidation_cycles": self.consolidation_cycles,
            "avg_memory_strength": statistics.mean(strength_values) if strength_values else 0,
            "memory_strength_std": statistics.stdev(strength_values) if len(strength_values) > 1 else 0,
            "consolidation_distribution": dict(consolidation_dist),
            "emotion_distribution": dict(emotion_dist),
            "pattern_statistics": pattern_stats,
            "association_network_size": sum(len(links) for links in self.association_network.values()),
            "working_memory_size": len(self.working_memory),
            "last_consolidation_hours_ago": (current_time - self.last_consolidation) / 3600,
            "semantic_index_size": len(self.semantic_index),
            "memory_efficiency": len(self.memory_traces) / max(1, self.total_memories_stored)
        }
    
    def search_memories(self, query: str, filters: Dict[str, Any] = None) -> List[Tuple[str, MemoryTrace, float]]:
        """Advanced memory search with filters"""
        
        filters = filters or {}
        results = []
        
        # Get similar memories
        similar_memories = self.retrieve_similar(query, limit=50, min_similarity=0.3)
        
        for memory_id, similarity in similar_memories:
            memory = self.memory_traces[memory_id]
            
            # Apply filters
            if filters.get("emotion") and memory.emotional_state != filters["emotion"]:
                continue
            
            if filters.get("min_strength") and memory.memory_strength < filters["min_strength"]:
                continue
            
            if filters.get("pattern_tag") and filters["pattern_tag"] not in memory.pattern_tags:
                continue
            
            if filters.get("outcome") and memory.interaction_outcome != filters["outcome"]:
                continue
            
            # Time range filter
            if filters.get("time_range"):
                time_range = filters["time_range"]
                if not (time_range[0] <= memory.timestamp <= time_range[1]):
                    continue
            
            results.append((memory_id, memory, similarity))
        
        return results
    
    def save_memory_state(self, filepath: str = None) -> bool:
        """Save complete memory state to file"""
        
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = self.memory_directory / f"memory_state_{timestamp}.json"
        
        try:
            memory_state = {
                "metadata": {
                    "save_time": time.time(),
                    "total_memories": len(self.memory_traces),
                    "consolidation_cycles": self.consolidation_cycles,
                    "version": "1.0"
                },
                "memory_traces": {mid: asdict(trace) for mid, trace in self.memory_traces.items()},
                "pattern_clusters": {pid: asdict(cluster) for pid, cluster in self.pattern_clusters.items()},
                "association_network": {
                    concept: [asdict(link) for link in links] 
                    for concept, links in self.association_network.items()
                },
                "statistics": self.get_memory_statistics()
            }
            
            # Compress if large
            if len(json.dumps(memory_state, default=str)) > 5 * 1024 * 1024:  # 5MB
                with gzip.open(f"{filepath}.gz", 'wt', encoding='utf-8') as f:
                    json.dump(memory_state, f, indent=2, default=str)
                logger.info(f"Memory state saved (compressed): {filepath}.gz")
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(memory_state, f, indent=2, default=str)
                logger.info(f"Memory state saved: {filepath}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to save memory state: {e}")
            return False
    
    def load_memory_state(self, filepath: str) -> bool:
        """Load memory state from file"""
        
        filepath = Path(filepath)
        
        if not filepath.exists() and Path(f"{filepath}.gz").exists():
            filepath = Path(f"{filepath}.gz")
        
        if not filepath.exists():
            logger.warning(f"Memory state file not found: {filepath}")
            return False
        
        try:
            # Load data
            if filepath.suffix == '.gz':
                with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                    memory_state = json.load(f)
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    memory_state = json.load(f)
            
            # Restore memory traces
            self.memory_traces.clear()
            for memory_id, trace_data in memory_state.get("memory_traces", {}).items():
                memory_trace = MemoryTrace(**trace_data)
                self.memory_traces[memory_id] = memory_trace
            
            # Restore pattern clusters
            self.pattern_clusters.clear()
            for cluster_id, cluster_data in memory_state.get("pattern_clusters", {}).items():
                pattern_cluster = PatternCluster(**cluster_data)
                self.pattern_clusters[cluster_id] = pattern_cluster
            
            # Restore association network
            self.association_network.clear()
            for concept, links_data in memory_state.get("association_network", {}).items():
                links = [AssociationLink(**link_data) for link_data in links_data]
                self.association_network[concept] = links
            
            # Rebuild indices
            self._rebuild_indices()
            
            # Restore metadata
            metadata = memory_state.get("metadata", {})
            self.consolidation_cycles = metadata.get("consolidation_cycles", 0)
            
            logger.info(f"Memory state loaded: {len(self.memory_traces)} memories, {len(self.pattern_clusters)} patterns")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load memory state: {e}")
            return False
    
    # ==================== PRIVATE HELPER METHODS ====================
    
    def _load_memory_state(self):
        """Load the most recent memory state on initialization"""
        
        state_files = list(self.memory_directory.glob("memory_state_*.json*"))
        if state_files:
            latest_file = max(state_files, key=lambda f: f.stat().st_mtime)
            self.load_memory_state(str(latest_file))
    
    def _extract_semantic_keywords(self, input_text: str, response_text: str) -> List[str]:
        """Extract semantic keywords from interaction text"""
        
        combined_text = f"{input_text} {response_text}".lower()
        
        # Remove common words and extract meaningful terms
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'}
        
        # Extract words
        words = re.findall(r'\b\w+\b', combined_text)
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        # Add technical terms
        technical_terms = ['scup', 'entropy', 'heat', 'consciousness', 'thermal', 'cognitive', 'unity', 'chaos', 'metric', 'awareness']
        for term in technical_terms:
            if term in combined_text:
                keywords.append(term)
        
        # Remove duplicates and limit
        return list(set(keywords))[:20]
    
    def _identify_patterns(self, input_text: str, emotional_state: str, consciousness_state: Dict) -> List[str]:
        """Identify interaction patterns"""
        
        patterns = []
        
        # Emotional patterns
        patterns.append(f"emotion_{emotional_state}")
        
        # Consciousness state patterns
        if 'state' in consciousness_state:
            patterns.append(f"consciousness_{consciousness_state['state']}")
        
        # Input length patterns
        if len(input_text) < 20:
            patterns.append("short_input")
        elif len(input_text) > 100:
            patterns.append("long_input")
        
        # Question patterns
        if '?' in input_text:
            patterns.append("question")
        
        # Command patterns
        command_keywords = ['pause', 'stop', 'start', 'increase', 'decrease', 'set']
        if any(keyword in input_text.lower() for keyword in command_keywords):
            patterns.append("command")
        
        # Technical inquiry patterns
        technical_keywords = ['scup', 'entropy', 'heat', 'metric']
        if any(keyword in input_text.lower() for keyword in technical_keywords):
            patterns.append("technical_query")
        
        return patterns
    
    def _calculate_emotional_intensity(self, emotional_state: str, consciousness_state: Dict, 
                                     metrics_snapshot: Dict) -> float:
        """Calculate the intensity of emotional content"""
        
        base_intensity = {
            'overwhelmed': 0.9, 'energetic': 0.8, 'curious': 0.7, 'focused': 0.6,
            'content': 0.5, 'calm': 0.4, 'contemplative': 0.6, 'uncertain': 0.7
        }.get(emotional_state, 0.5)
        
        # Adjust based on metrics
        if metrics_snapshot:
            entropy = metrics_snapshot.get('entropy', 0.5)
            heat = metrics_snapshot.get('heat', 0.5)
            
            # High entropy or heat increases intensity
            intensity_modifier = (entropy + heat) / 2.0
            base_intensity = base_intensity * (1.0 + intensity_modifier * 0.5)
        
        return min(1.0, base_intensity)
    
    def _update_semantic_index(self, memory_id: str, keywords: List[str]):
        """Update semantic keyword index"""
        for keyword in keywords:
            self.semantic_index[keyword].add(memory_id)
    
    def _update_emotional_index(self, memory_id: str, emotional_state: str):
        """Update emotional state index"""
        self.emotional_index[emotional_state].append(memory_id)
    
    def _create_associations(self, memory_id: str, memory_trace: MemoryTrace):
        """Create associations with recent memories"""
        
        # Get recent memories from working memory
        recent_memory_ids = list(self.working_memory)[-10:]  # Last 10 memories
        
        for recent_id in recent_memory_ids:
            if recent_id == memory_id or recent_id not in self.memory_traces:
                continue
            
            recent_memory = self.memory_traces[recent_id]
            
            # Calculate association strength
            semantic_similarity = self._calculate_semantic_similarity(
                memory_trace.semantic_keywords, recent_memory.semantic_keywords
            )
            
            emotional_similarity = 1.0 if memory_trace.emotional_state == recent_memory.emotional_state else 0.3
            temporal_proximity = max(0.1, 1.0 - (memory_trace.timestamp - recent_memory.timestamp) / 3600)
            
            association_strength = (semantic_similarity * 0.5 + emotional_similarity * 0.3 + temporal_proximity * 0.2)
            
            if association_strength > 0.4:
                # Determine association type
                if abs(memory_trace.timestamp - recent_memory.timestamp) < 300:  # 5 minutes
                    assoc_type = "temporal"
                elif memory_trace.emotional_state == recent_memory.emotional_state:
                    assoc_type = "emotional"
                else:
                    assoc_type = "semantic"
                
                # Create bidirectional association
                self._add_association(memory_id, recent_id, association_strength, assoc_type)
                self._add_association(recent_id, memory_id, association_strength, assoc_type)
    
    def _add_association(self, from_memory: str, to_memory: str, strength: float, assoc_type: str):
        """Add an association link"""
        
        association = AssociationLink(
            from_concept=from_memory,
            to_concept=to_memory,
            strength=strength,
            frequency=1,
            last_reinforced=time.time(),
            association_type=assoc_type,
            context_tags=[]
        )
        
        self.association_network[from_memory].append(association)
    
    def _update_pattern_clusters(self, memory_id: str, memory_trace: MemoryTrace):
        """Update pattern clusters with new memory"""
        
        pattern_signature = ":".join(sorted(memory_trace.pattern_tags))
        
        # Find existing cluster or create new one
        matching_cluster = None
        for cluster in self.pattern_clusters.values():
            if cluster.pattern_signature == pattern_signature:
                matching_cluster = cluster
                break
        
        if matching_cluster:
            # Add to existing cluster
            matching_cluster.member_memories.append(memory_id)
            matching_cluster.frequency += 1
            matching_cluster.last_updated = time.time()
            
            # Update dominant emotion and average outcome
            emotions = [self.memory_traces[mid].emotional_state for mid in matching_cluster.member_memories if mid in self.memory_traces]
            if emotions:
                emotion_counts = defaultdict(int)
                for emotion in emotions:
                    emotion_counts[emotion] += 1
                matching_cluster.dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        else:
            # Create new cluster
            cluster_id = f"cluster_{len(self.pattern_clusters)}_{int(time.time())}"
            new_cluster = PatternCluster(
                cluster_id=cluster_id,
                pattern_signature=pattern_signature,
                member_memories=[memory_id],
                frequency=1,
                average_outcome=0.7,  # Default neutral outcome
                dominant_emotion=memory_trace.emotional_state,
                pattern_strength=1.0,
                last_updated=time.time()
            )
            self.pattern_clusters[cluster_id] = new_cluster
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for similarity comparison"""
        return self._extract_semantic_keywords(text, "")[:10]
    
    def _calculate_semantic_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        """Calculate semantic similarity between keyword lists"""
        
        if not keywords1 or not keywords2:
            return 0.0
        
        # Jaccard similarity
        set1, set2 = set(keywords1), set(keywords2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_pattern_similarity(self, text1: str, text2: str) -> float:
        """Calculate pattern-based similarity between texts"""
        
        # Simple length-based similarity
        len1, len2 = len(text1), len(text2)
        length_similarity = 1.0 - abs(len1 - len2) / max(len1, len2, 1)
        
        # Question pattern similarity
        q1, q2 = '?' in text1, '?' in text2
        question_similarity = 1.0 if q1 == q2 else 0.5
        
        return (length_similarity + question_similarity) / 2.0
    
    def _calculate_temporal_relevance(self, timestamp: float) -> float:
        """Calculate temporal relevance of a memory"""
        
        age_hours = (time.time() - timestamp) / 3600
        
        # Exponential decay with 24-hour half-life
        return math.exp(-age_hours / 24.0)
    
    def _boost_memory(self, memory_id: str):
        """Boost memory strength when retrieved"""
        
        if memory_id in self.memory_traces:
            memory = self.memory_traces[memory_id]
            memory.memory_strength = min(1.0, memory.memory_strength * self.retrieval_boost)
            memory.retrieval_count += 1
            memory.last_retrieved = time.time()
    
    def _calculate_current_emotional_resonance(self, current_state: Dict) -> float:
        """Calculate emotional resonance with current state"""
        
        current_emotion = current_state.get('emotion', 'calm')
        
        # Count memories with similar emotional states
        similar_emotions = len(self.emotional_index.get(current_emotion, []))
        total_memories = len(self.memory_traces)
        
        return similar_emotions / max(1, total_memories)
    
    def _calculate_temporal_context_relevance(self, current_state: Dict) -> float:
        """Calculate temporal context relevance"""
        
        current_time = time.time()
        recent_memories = [
            mem for mem in self.memory_traces.values()
            if current_time - mem.timestamp < 86400  # Last 24 hours
        ]
        
        return len(recent_memories) / max(1, len(self.memory_traces))
    
    def _find_pattern_matches(self, current_state: Dict, query_context: str) -> List[Tuple[str, float]]:
        """Find pattern matches with current state"""
        
        matches = []
        current_emotion = current_state.get('emotion', 'calm')
        
        for cluster_id, cluster in self.pattern_clusters.items():
            match_strength = 0.0
            
            # Emotional pattern match
            if cluster.dominant_emotion == current_emotion:
                match_strength += 0.5
            
            # Context keyword match
            if query_context:
                query_keywords = self._extract_keywords(query_context)
                pattern_keywords = cluster.pattern_signature.split(':')
                similarity = self._calculate_semantic_similarity(query_keywords, pattern_keywords)
                match_strength += similarity * 0.5
            
            if match_strength > 0.3:
                matches.append((cluster_id, match_strength))
        
        return sorted(matches, key=lambda x: x[1], reverse=True)
    
    def _retrieve_by_state(self, current_state: Dict, limit: int) -> List[Tuple[str, float]]:
        """Retrieve memories by current state similarity"""
        
        current_emotion = current_state.get('emotion', 'calm')
        similar_memory_ids = self.emotional_index.get(current_emotion, [])
        
        # Calculate relevance scores
        results = []
        for memory_id in similar_memory_ids[:limit*2]:  # Get more candidates
            if memory_id in self.memory_traces:
                memory = self.memory_traces[memory_id]
                
                # Combine memory strength and temporal relevance
                relevance = (
                    memory.memory_strength * 0.6 +
                    self._calculate_temporal_relevance(memory.timestamp) * 0.4
                )
                
                results.append((memory_id, relevance))
        
        return sorted(results, key=lambda x: x[1], reverse=True)[:limit]
    
    def _trigger_consolidation(self):
        """Trigger memory consolidation when needed"""
        logger.info("Memory limit reached, triggering consolidation...")
        self.consolidate_memories(force=True)
    
    def _apply_time_decay(self):
        """Apply time decay to all memories"""
        
        current_time = time.time()
        decay_factor = self.decay_rate ** ((current_time - self.last_consolidation) / 86400)  # Daily decay
        
        for memory in self.memory_traces.values():
            memory.memory_strength *= decay_factor
    
    def _consolidate_similar_memories(self) -> int:
        """Consolidate very similar memories"""
        
        consolidated_count = 0
        memory_items = list(self.memory_traces.items())
        
        for i, (mem_id1, mem1) in enumerate(memory_items):
            if mem1.consolidation_level >= 2:  # Already consolidated
                continue
            
            for j, (mem_id2, mem2) in enumerate(memory_items[i+1:], i+1):
                if mem2.consolidation_level >= 2:
                    continue
                
                # Check similarity
                semantic_sim = self._calculate_semantic_similarity(mem1.semantic_keywords, mem2.semantic_keywords)
                pattern_sim = 1.0 if set(mem1.pattern_tags) == set(mem2.pattern_tags) else 0.0
                
                if semantic_sim > 0.8 and pattern_sim > 0.5:
                    # Merge memories by strengthening the stronger one
                    if mem1.memory_strength >= mem2.memory_strength:
                        mem1.memory_strength = min(1.0, mem1.memory_strength + mem2.memory_strength * 0.3)
                        mem1.consolidation_level = 2
                        self._remove_memory(mem_id2)
                    else:
                        mem2.memory_strength = min(1.0, mem2.memory_strength + mem1.memory_strength * 0.3)
                        mem2.consolidation_level = 2
                        self._remove_memory(mem_id1)
                    
                    consolidated_count += 1
                    break
        
        return consolidated_count
    
    def _merge_pattern_clusters(self) -> int:
        """Merge overlapping pattern clusters"""
        
        merged_count = 0
        cluster_items = list(self.pattern_clusters.items())
        
        for i, (cluster_id1, cluster1) in enumerate(cluster_items):
            for j, (cluster_id2, cluster2) in enumerate(cluster_items[i+1:], i+1):
                
                # Check for pattern overlap
                pattern1_set = set(cluster1.pattern_signature.split(':'))
                pattern2_set = set(cluster2.pattern_signature.split(':'))
                overlap = len(pattern1_set.intersection(pattern2_set)) / len(pattern1_set.union(pattern2_set))
                
                if overlap > 0.7:  # High overlap
                    # Merge into the larger cluster
                    if len(cluster1.member_memories) >= len(cluster2.member_memories):
                        cluster1.member_memories.extend(cluster2.member_memories)
                        cluster1.frequency += cluster2.frequency
                        del self.pattern_clusters[cluster_id2]
                    else:
                        cluster2.member_memories.extend(cluster1.member_memories)
                        cluster2.frequency += cluster1.frequency
                        del self.pattern_clusters[cluster_id1]
                    
                    merged_count += 1
                    break
        
        return merged_count
    
    def _strengthen_important_associations(self):
        """Strengthen frequently used associations"""
        
        for concept, links in self.association_network.items():
            for link in links:
                if link.frequency > 5:  # Frequently accessed
                    link.strength = min(1.0, link.strength * 1.1)
    
    def _remove_memory(self, memory_id: str):
        """Remove a memory and clean up indices"""
        
        if memory_id not in self.memory_traces:
            return
        
        memory = self.memory_traces[memory_id]
        
        # Remove from semantic index
        for keyword in memory.semantic_keywords:
            if keyword in self.semantic_index:
                self.semantic_index[keyword].discard(memory_id)
                if not self.semantic_index[keyword]:
                    del self.semantic_index[keyword]
        
        # Remove from emotional index
        if memory.emotional_state in self.emotional_index:
            if memory_id in self.emotional_index[memory.emotional_state]:
                self.emotional_index[memory.emotional_state].remove(memory_id)
        
        # Remove from pattern clusters
        for cluster in self.pattern_clusters.values():
            if memory_id in cluster.member_memories:
                cluster.member_memories.remove(memory_id)
        
        # Remove from association network
        if memory_id in self.association_network:
            del self.association_network[memory_id]
        
        # Remove the memory itself
        del self.memory_traces[memory_id]
    
    def _rebuild_indices(self):
        """Rebuild all indices after loading from file"""
        
        self.semantic_index.clear()
        self.emotional_index.clear()
        
        for memory_id, memory in self.memory_traces.items():
            self._update_semantic_index(memory_id, memory.semantic_keywords)
            self._update_emotional_index(memory_id, memory.emotional_state)


# Global memory manager instance
memory_manager = MemoryManager()


def get_memory_manager() -> MemoryManager:
    """Get the singleton memory manager instance"""
    return initialize_memory_manager()


def initialize_memory_manager(memory_directory: str = "memories") -> MemoryManager:
    """Initialize and return a new memory manager instance"""
    return MemoryManager(memory_directory)


def create_memory_manager(memory_directory: str = "memories") -> MemoryManager:
    """Create and return a new memory manager instance (alias for initialize_memory_manager)"""
    return initialize_memory_manager(memory_directory) 