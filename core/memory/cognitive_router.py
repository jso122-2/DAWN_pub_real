"""
DAWN Cognitive Memory Router - Cognitive Memory Routing Core
Manages memory storage, retrieval, and relationship discovery for DAWN consciousness.
Integrated with DAWN's existing memory infrastructure.
"""

import uuid
import re
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from collections import defaultdict

from .memory_chunk import MemoryChunk


class CognitiveRouter:
    """
    Cognitive memory routing core for DAWN consciousness.
    Manages memory storage, deletion, relationship discovery, and compression.
    Enhanced with DAWN-specific pulse state and sigil integration.
    """
    
    def __init__(self):
        """Initialize the cognitive router with empty storage."""
        self.chunks: Dict[str, MemoryChunk] = {}
        self.speaker_index: Dict[str, Set[str]] = defaultdict(set)
        self.topic_index: Dict[str, Set[str]] = defaultdict(set)
        self.sigil_index: Dict[str, Set[str]] = defaultdict(set)
        self.mood_index: Dict[str, Set[str]] = defaultdict(set)
        self.entropy_index: Dict[str, Set[str]] = defaultdict(set)  # Bucketed entropy ranges
        self.creation_count = 0
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Performance tracking
        self.rebloom_requests = 0
        self.compression_requests = 0
        self.last_compression_time = None
        
        print("🧠 CognitiveRouter initialized - Cognitive routing active")
    
    def add_chunk(self, chunk: MemoryChunk) -> str:
        """
        Add a memory chunk to the router storage.
        
        Args:
            chunk: MemoryChunk to store
            
        Returns:
            str: Unique ID assigned to the chunk
        """
        with self.lock:
            # Use existing memory_id or generate new UUID
            chunk_id = chunk.memory_id if hasattr(chunk, 'memory_id') and chunk.memory_id else str(uuid.uuid4())
            
            # Store the chunk
            self.chunks[chunk_id] = chunk
            self.creation_count += 1
            
            # Update indices for fast retrieval
            self.speaker_index[chunk.speaker].add(chunk_id)
            
            if chunk.topic:
                self.topic_index[chunk.topic].add(chunk_id)
            
            for sigil in chunk.sigils:
                self.sigil_index[sigil].add(chunk_id)
            
            # Index by mood
            mood = chunk.get_mood()
            self.mood_index[mood].add(chunk_id)
            
            # Index by entropy buckets
            entropy_bucket = self._get_entropy_bucket(chunk.get_entropy())
            self.entropy_index[entropy_bucket].add(chunk_id)
            
            print(f"🧠 Memory stored: {chunk_id[:8]}... - {chunk.summary()}")
            return chunk_id
    
    def delete_chunk(self, chunk_id: str) -> bool:
        """
        Delete a memory chunk by ID.
        
        Args:
            chunk_id: Unique identifier of the chunk to delete
            
        Returns:
            bool: True if chunk was deleted, False if not found
        """
        with self.lock:
            if chunk_id not in self.chunks:
                print(f"⚠️ Memory not found for deletion: {chunk_id[:8]}...")
                return False
            
            chunk = self.chunks[chunk_id]
            
            # Remove from indices
            self.speaker_index[chunk.speaker].discard(chunk_id)
            if chunk.topic:
                self.topic_index[chunk.topic].discard(chunk_id)
            for sigil in chunk.sigils:
                self.sigil_index[sigil].discard(chunk_id)
            
            # Remove from mood and entropy indices
            mood = chunk.get_mood()
            self.mood_index[mood].discard(chunk_id)
            
            entropy_bucket = self._get_entropy_bucket(chunk.get_entropy())
            self.entropy_index[entropy_bucket].discard(chunk_id)
            
            # Remove from main storage
            del self.chunks[chunk_id]
            
            print(f"🗑️ Memory deleted: {chunk_id[:8]}... - {chunk.summary()}")
            return True
    
    def get_chunk(self, chunk_id: str) -> Optional[MemoryChunk]:
        """
        Retrieve a memory chunk by ID.
        
        Args:
            chunk_id: Unique identifier of the chunk
            
        Returns:
            MemoryChunk: The memory chunk, or None if not found
        """
        return self.chunks.get(chunk_id)
    
    def rebloom_candidates(self, query_chunk: MemoryChunk, max_candidates: int = 10) -> List[MemoryChunk]:
        """
        Find memory chunks related to the query chunk using DAWN-enhanced similarity.
        
        Args:
            query_chunk: Memory chunk to find relations for
            max_candidates: Maximum number of candidates to return
            
        Returns:
            List[MemoryChunk]: List of related memory chunks, ordered by relevance
        """
        with self.lock:
            self.rebloom_requests += 1
            
            if not self.chunks:
                return []
            
            candidates = []
            query_words = set(self._extract_keywords(query_chunk.content))
            
            print(f"🔍 Reblooming for: {query_chunk.summary()}")
            print(f"   Query keywords: {query_words}")
            
            for chunk_id, chunk in self.chunks.items():
                # Skip self-matching
                if hasattr(query_chunk, 'memory_id') and chunk_id == query_chunk.memory_id:
                    continue
                
                similarity_score = self._calculate_dawn_similarity(query_chunk, chunk, query_words)
                
                if similarity_score > 0:
                    candidates.append((similarity_score, chunk))
            
            # Sort by similarity score (descending) and limit results
            candidates.sort(key=lambda x: x[0], reverse=True)
            top_candidates = [chunk for score, chunk in candidates[:max_candidates]]
            
            print(f"   Found {len(top_candidates)} rebloom candidates")
            return top_candidates
    
    def _calculate_dawn_similarity(self, query_chunk: MemoryChunk, candidate_chunk: MemoryChunk, query_words: Set[str]) -> float:
        """
        Calculate DAWN-enhanced similarity between query and candidate chunks.
        Integrates pulse state, sigils, and DAWN-specific metrics.
        
        Args:
            query_chunk: Query memory chunk
            candidate_chunk: Candidate memory chunk
            query_words: Extracted keywords from query
            
        Returns:
            float: Similarity score (0.0 to 1.0)
        """
        score = 0.0
        
        # Same speaker boost
        if query_chunk.speaker == candidate_chunk.speaker:
            score += 0.2
        
        # Same topic boost
        if query_chunk.topic and query_chunk.topic == candidate_chunk.topic:
            score += 0.3
        
        # Shared sigils boost (DAWN-specific)
        shared_sigils = set(query_chunk.sigils) & set(candidate_chunk.sigils)
        if shared_sigils:
            score += 0.2 * min(len(shared_sigils), 3)  # Cap at 3 sigils
        
        # Content word overlap
        candidate_words = set(self._extract_keywords(candidate_chunk.content))
        word_overlap = len(query_words & candidate_words)
        if word_overlap > 0 and query_words:
            score += 0.1 * min(word_overlap / len(query_words), 0.5)
        
        # DAWN pulse state similarity
        pulse_similarity = self._calculate_pulse_similarity(query_chunk, candidate_chunk)
        score += pulse_similarity * 0.2
        
        # Mood similarity (DAWN-specific)
        if query_chunk.get_mood() == candidate_chunk.get_mood():
            score += 0.1
        
        # Time proximity (recent memories are more relevant)
        time_diff = abs((query_chunk.timestamp - candidate_chunk.timestamp).total_seconds())
        if time_diff < 3600:  # Within 1 hour
            score += 0.1 * (1 - time_diff / 3600)
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _calculate_pulse_similarity(self, chunk1: MemoryChunk, chunk2: MemoryChunk) -> float:
        """Calculate similarity based on DAWN pulse state metrics."""
        similarity = 0.0
        
        # Entropy similarity (closer entropy = higher similarity)
        entropy_diff = abs(chunk1.get_entropy() - chunk2.get_entropy())
        if entropy_diff < 0.2:
            similarity += 0.3 * (0.2 - entropy_diff) / 0.2
        
        # Heat similarity
        heat_diff = abs(chunk1.get_heat() - chunk2.get_heat())
        if heat_diff < 20.0:  # Within 20 heat units
            similarity += 0.3 * (20.0 - heat_diff) / 20.0
        
        # SCUP similarity
        scup_diff = abs(chunk1.get_scup() - chunk2.get_scup())
        if scup_diff < 0.3:
            similarity += 0.4 * (0.3 - scup_diff) / 0.3
        
        return min(similarity, 1.0)
    
    def _extract_keywords(self, content: str) -> List[str]:
        """
        Extract keywords from content for similarity matching.
        Enhanced with DAWN-specific terms and stop words.
        
        Args:
            content: Text content to extract keywords from
            
        Returns:
            List[str]: List of keywords
        """
        # Remove punctuation and convert to lowercase
        clean_content = re.sub(r'[^\w\s]', ' ', content.lower())
        words = clean_content.split()
        
        # Enhanced stop words list
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        # Keep DAWN-specific terms even if short
        dawn_terms = {'dawn', 'scup', 'owl', 'sigil', 'heat', 'mood', 'tick', 'ai'}
        
        keywords = []
        for word in words:
            if len(word) > 2 and word not in stop_words:
                keywords.append(word)
            elif word in dawn_terms:
                keywords.append(word)
        
        return keywords
    
    def _get_entropy_bucket(self, entropy: float) -> str:
        """Get entropy bucket for indexing."""
        if entropy < 0.2:
            return "very_low"
        elif entropy < 0.4:
            return "low"
        elif entropy < 0.6:
            return "medium"
        elif entropy < 0.8:
            return "high"
        else:
            return "very_high"
    
    def compress(self) -> Dict[str, Any]:
        """
        Generate a compressed representation of all stored memories.
        Enhanced with DAWN-specific metrics and pulse state analysis.
        
        Returns:
            Dict[str, Any]: Compressed memory representation
        """
        with self.lock:
            self.compression_requests += 1
            self.last_compression_time = time.time()
            
            if not self.chunks:
                return {'compressed_memories': 'No memories to compress'}
            
            # Basic compression statistics
            total_chunks = len(self.chunks)
            total_chars = sum(len(chunk.content) for chunk in self.chunks.values())
            unique_speakers = len(self.speaker_index)
            unique_topics = len([t for t in self.topic_index.keys() if t])
            unique_sigils = len(self.sigil_index)
            unique_moods = len(self.mood_index)
            
            # DAWN-specific analysis
            entropies = [chunk.get_entropy() for chunk in self.chunks.values()]
            heats = [chunk.get_heat() for chunk in self.chunks.values()]
            scups = [chunk.get_scup() for chunk in self.chunks.values()]
            
            # Calculate statistics
            avg_entropy = sum(entropies) / len(entropies) if entropies else 0
            avg_heat = sum(heats) / len(heats) if heats else 0
            avg_scup = sum(scups) / len(scups) if scups else 0
            
            # Topic and speaker frequency analysis
            topic_freq = {topic: len(chunk_ids) for topic, chunk_ids in self.topic_index.items() if topic}
            speaker_activity = {speaker: len(chunk_ids) for speaker, chunk_ids in self.speaker_index.items()}
            sigil_frequency = {sigil: len(chunk_ids) for sigil, chunk_ids in self.sigil_index.items()}
            mood_distribution = {mood: len(chunk_ids) for mood, chunk_ids in self.mood_index.items()}
            
            # Time range analysis
            timestamps = [chunk.timestamp for chunk in self.chunks.values()]
            time_range = (min(timestamps), max(timestamps)) if timestamps else None
            
            # Entropy distribution analysis
            entropy_distribution = {bucket: len(chunk_ids) for bucket, chunk_ids in self.entropy_index.items()}
            
            compressed = {
                'compression_timestamp': datetime.now().isoformat(),
                'total_memories': total_chunks,
                'total_characters': total_chars,
                'unique_speakers': unique_speakers,
                'unique_topics': unique_topics,
                'unique_sigils': unique_sigils,
                'unique_moods': unique_moods,
                'topic_frequency': topic_freq,
                'speaker_activity': speaker_activity,
                'sigil_frequency': sigil_frequency,
                'mood_distribution': mood_distribution,
                'entropy_distribution': entropy_distribution,
                'pulse_state_averages': {
                    'entropy': avg_entropy,
                    'heat': avg_heat,
                    'scup': avg_scup
                },
                'time_range': time_range,
                'performance_metrics': {
                    'creation_count': self.creation_count,
                    'rebloom_requests': self.rebloom_requests,
                    'compression_requests': self.compression_requests
                },
                'memory_summary': f"Compressed {total_chunks} memories from {unique_speakers} speakers across {unique_topics} topics with {unique_sigils} unique sigils"
            }
            
            # Add compression ratio after the dict is created
            compressed['compression_ratio'] = f"{total_chars}:{len(str(compressed))}"
            
            print(f"🗜️ Memory compressed: {total_chunks} chunks → {len(str(compressed))} chars")
            return compressed
    
    def find_by_speaker(self, speaker: str) -> List[MemoryChunk]:
        """Find all memories by a specific speaker."""
        chunk_ids = self.speaker_index.get(speaker, set())
        return [self.chunks[chunk_id] for chunk_id in chunk_ids if chunk_id in self.chunks]
    
    def find_by_topic(self, topic: str) -> List[MemoryChunk]:
        """Find all memories with a specific topic."""
        chunk_ids = self.topic_index.get(topic, set())
        return [self.chunks[chunk_id] for chunk_id in chunk_ids if chunk_id in self.chunks]
    
    def find_by_sigil(self, sigil: str) -> List[MemoryChunk]:
        """Find all memories linked to a specific sigil."""
        chunk_ids = self.sigil_index.get(sigil, set())
        return [self.chunks[chunk_id] for chunk_id in chunk_ids if chunk_id in self.chunks]
    
    def find_by_mood(self, mood: str) -> List[MemoryChunk]:
        """Find all memories with a specific mood."""
        chunk_ids = self.mood_index.get(mood, set())
        return [self.chunks[chunk_id] for chunk_id in chunk_ids if chunk_id in self.chunks]
    
    def find_by_entropy_range(self, min_entropy: float, max_entropy: float) -> List[MemoryChunk]:
        """Find all memories within an entropy range."""
        matching_chunks = []
        for chunk in self.chunks.values():
            entropy = chunk.get_entropy()
            if min_entropy <= entropy <= max_entropy:
                matching_chunks.append(chunk)
        return matching_chunks
    
    def find_similar_pulse_state(self, reference_chunk: MemoryChunk, tolerance: float = 0.2) -> List[MemoryChunk]:
        """Find memories with similar pulse state to reference chunk."""
        similar_chunks = []
        ref_entropy = reference_chunk.get_entropy()
        ref_heat = reference_chunk.get_heat()
        ref_scup = reference_chunk.get_scup()
        
        for chunk in self.chunks.values():
            # Skip self
            if hasattr(reference_chunk, 'memory_id') and hasattr(chunk, 'memory_id'):
                if reference_chunk.memory_id == chunk.memory_id:
                    continue
            
            # Check if pulse states are similar
            if (abs(chunk.get_entropy() - ref_entropy) <= tolerance and
                abs(chunk.get_heat() - ref_heat) <= tolerance * 50 and  # Scale for heat
                abs(chunk.get_scup() - ref_scup) <= tolerance):
                similar_chunks.append(chunk)
        
        return similar_chunks
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about stored memories."""
        with self.lock:
            return {
                'total_chunks': len(self.chunks),
                'creation_count': self.creation_count,
                'rebloom_requests': self.rebloom_requests,
                'compression_requests': self.compression_requests,
                'unique_speakers': len(self.speaker_index),
                'unique_topics': len([t for t in self.topic_index.keys() if t]),
                'unique_sigils': len(self.sigil_index),
                'unique_moods': len(self.mood_index),
                'entropy_buckets': len(self.entropy_index),
                'total_characters': sum(len(chunk.content) for chunk in self.chunks.values()),
                'average_entropy': sum(chunk.get_entropy() for chunk in self.chunks.values()) / max(len(self.chunks), 1),
                'average_heat': sum(chunk.get_heat() for chunk in self.chunks.values()) / max(len(self.chunks), 1),
                'average_scup': sum(chunk.get_scup() for chunk in self.chunks.values()) / max(len(self.chunks), 1),
                'memory_age_range': self._get_age_range(),
                'last_compression_time': self.last_compression_time
            }
    
    def _get_age_range(self) -> Optional[tuple]:
        """Get the age range of stored memories."""
        if not self.chunks:
            return None
        
        timestamps = [chunk.timestamp for chunk in self.chunks.values()]
        return (min(timestamps), max(timestamps))
    
    def clear_all(self) -> int:
        """
        Clear all stored memories. Use with caution.
        
        Returns:
            int: Number of memories that were cleared
        """
        with self.lock:
            count = len(self.chunks)
            self.chunks.clear()
            self.speaker_index.clear()
            self.topic_index.clear()
            self.sigil_index.clear()
            self.mood_index.clear()
            self.entropy_index.clear()
            
            print(f"🧹 Cleared {count} memories from cognitive router")
            return count


# Utility function for creating routers
def create_cognitive_router() -> CognitiveRouter:
    """Factory function for creating a new CognitiveRouter instance."""
    return CognitiveRouter()


# Integration with DAWN memory routing system
def integrate_cognitive_router(memory_routing_system):
    """Integrate cognitive router with existing memory routing system."""
    cognitive_router = CognitiveRouter()
    
    # Replace or enhance the existing router
    if hasattr(memory_routing_system, 'router'):
        # Enhance the existing router with cognitive capabilities
        memory_routing_system.cognitive_router = cognitive_router
        print("🧠 Cognitive router integrated with memory routing system")
    
    return cognitive_router 