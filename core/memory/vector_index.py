"""
DAWN Memory Vector Index - Semantic Search for Memory Chunks
Provides vector-based semantic similarity search for DAWN memory system.
Integrates with existing memory infrastructure and supports FAISS backend.
"""

import uuid
import numpy as np
import logging
import threading
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import time

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️ FAISS not available - using cosine similarity fallback")

# Simple embedder implementation for integration
class SimpleEmbedder:
    """Simple text embedder for DAWN memory chunks."""
    
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        
    def embed(self, chunk) -> List[float]:
        """Generate embedding for a memory chunk."""
        text = self._extract_text(chunk)
        return self.embed_text(text)
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text content."""
        # Simple hash-based embedding for development
        # In production, this would use a proper embedding model
        import hashlib
        
        # Create a simple hash-based vector
        hash_obj = hashlib.md5(text.lower().encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to float vector
        vector = []
        for i in range(0, len(hash_bytes), 4):
            chunk_bytes = hash_bytes[i:i+4].ljust(4, b'\x00')
            float_val = int.from_bytes(chunk_bytes, 'little') / (2**32)
            vector.append(float_val)
        
        # Pad or truncate to desired dimension
        while len(vector) < self.dimension:
            vector.extend(vector[:min(len(vector), self.dimension - len(vector))])
        
        return vector[:self.dimension]
    
    def _extract_text(self, chunk) -> str:
        """Extract text content from memory chunk."""
        if hasattr(chunk, 'content'):
            return str(chunk.content)
        elif hasattr(chunk, 'text'):
            return str(chunk.text)
        else:
            return str(chunk)


logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Result from vector similarity search"""
    chunk: Any  # MemoryChunk object
    score: float
    chunk_id: str
    rank: int


@dataclass
class IndexConfig:
    """Configuration for vector index operations"""
    use_faiss: bool = FAISS_AVAILABLE
    dimension: int = 384
    index_type: str = "flat"  # flat, ivf, hnsw
    metric: str = "cosine"  # cosine, l2, inner_product
    normalize_vectors: bool = True


class MockVectorIndex:
    """Fallback vector index using cosine similarity"""
    
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.vectors: List[np.ndarray] = []
        self.chunk_ids: List[str] = []
        
    def add(self, vectors: np.ndarray):
        """Add vectors to the mock index"""
        if len(vectors.shape) == 1:
            vectors = vectors.reshape(1, -1)
        
        for vector in vectors:
            self.vectors.append(vector)
    
    def search(self, query_vector: np.ndarray, k: int) -> Tuple[np.ndarray, np.ndarray]:
        """Search for similar vectors using cosine similarity"""
        if not self.vectors:
            return np.array([]), np.array([])
        
        # Stack all vectors
        all_vectors = np.stack(self.vectors)
        
        # Normalize query and stored vectors
        query_norm = query_vector / (np.linalg.norm(query_vector) + 1e-8)
        vectors_norm = all_vectors / (np.linalg.norm(all_vectors, axis=1, keepdims=True) + 1e-8)
        
        # Calculate cosine similarities
        similarities = np.dot(vectors_norm, query_norm)
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:k]
        top_scores = similarities[top_indices]
        
        return top_scores, top_indices


class DAWNVectorIndex:
    """Vector index for semantic search of DAWN memory chunks"""
    
    def __init__(self, config: Optional[IndexConfig] = None, embedder: Optional[SimpleEmbedder] = None):
        self.config = config or IndexConfig()
        self.embedder = embedder or SimpleEmbedder(dimension=self.config.dimension)
        
        # Storage for chunks and metadata
        self.chunks: Dict[str, Any] = {}  # chunk_id -> MemoryChunk
        self.chunk_metadata: Dict[str, Dict] = {}  # chunk_id -> metadata
        self.id_to_index: Dict[str, int] = {}  # chunk_id -> vector index position
        self.index_to_id: Dict[int, str] = {}  # vector index position -> chunk_id
        
        # Initialize vector index
        self.vector_index = None
        self.vector_count = 0
        
        # Thread safety
        self.lock = threading.RLock()
        
        # Integration with DAWN memory systems
        self.dawn_integration_enabled = True
        
        self._initialize_index()
        
        logger.info(f"🔍 DAWN Vector Index initialized")
        logger.info(f"   Backend: {'FAISS' if self.config.use_faiss else 'Mock'}")
        logger.info(f"   Dimensions: {self.config.dimension}")
        logger.info(f"   Metric: {self.config.metric}")
    
    def _initialize_index(self):
        """Initialize the vector index backend"""
        if self.config.use_faiss and FAISS_AVAILABLE:
            # Initialize FAISS index
            if self.config.index_type == "flat":
                if self.config.metric == "cosine":
                    self.vector_index = faiss.IndexFlatIP(self.config.dimension)  # Inner product for cosine
                elif self.config.metric == "l2":
                    self.vector_index = faiss.IndexFlatL2(self.config.dimension)
                else:
                    self.vector_index = faiss.IndexFlatIP(self.config.dimension)
            else:
                # Default to flat index
                self.vector_index = faiss.IndexFlatIP(self.config.dimension)
        else:
            # Use mock index
            self.vector_index = MockVectorIndex(self.config.dimension)
            self.config.use_faiss = False
    
    def add(self, chunk: Any, vector: Optional[List[float]] = None):
        """
        Add a memory chunk to the vector index.
        
        Args:
            chunk: MemoryChunk object to add
            vector: Pre-computed embedding vector (optional)
        """
        with self.lock:
            # Generate or get chunk ID
            chunk_id = self._get_chunk_id(chunk)
            
            # Generate embedding if not provided
            if vector is None:
                vector = self.embedder.embed(chunk)
            
            # Ensure vector is the right size
            if len(vector) != self.config.dimension:
                logger.warning(f"Vector dimension mismatch: expected {self.config.dimension}, got {len(vector)}")
                # Pad or truncate
                if len(vector) < self.config.dimension:
                    vector.extend([0.0] * (self.config.dimension - len(vector)))
                else:
                    vector = vector[:self.config.dimension]
            
            # Normalize vector if configured
            if self.config.normalize_vectors:
                vector_array = np.array(vector, dtype=np.float32)
                norm = np.linalg.norm(vector_array)
                if norm > 0:
                    vector_array = vector_array / norm
            else:
                vector_array = np.array(vector, dtype=np.float32)
            
            # Add to index mappings
            current_index = self.vector_count
            self.id_to_index[chunk_id] = current_index
            self.index_to_id[current_index] = chunk_id
            
            # Store chunk and metadata
            self.chunks[chunk_id] = chunk
            self.chunk_metadata[chunk_id] = self._extract_metadata(chunk)
            
            # Add to vector index
            if self.config.use_faiss:
                self.vector_index.add(vector_array.reshape(1, -1))
            else:
                self.vector_index.add(vector_array)
                self.vector_index.chunk_ids.append(chunk_id)
            
            self.vector_count += 1
            
            logger.debug(f"📚 Added chunk {chunk_id[:8]}... to vector index (total: {self.vector_count})")
    
    def search(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """
        Search for similar memory chunks using semantic similarity.
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            
        Returns:
            List[SearchResult]: Ranked search results
        """
        with self.lock:
            if self.vector_count == 0:
                return []
            
            # Generate query embedding
            query_vector = self.embedder.embed_text(query)
            query_array = np.array(query_vector, dtype=np.float32)
            
            # Normalize query vector if configured
            if self.config.normalize_vectors:
                norm = np.linalg.norm(query_array)
                if norm > 0:
                    query_array = query_array / norm
            
            # Perform search
            if self.config.use_faiss:
                scores, indices = self.vector_index.search(query_array.reshape(1, -1), min(top_k, self.vector_count))
                scores = scores[0]  # Remove batch dimension
                indices = indices[0]
            else:
                scores, indices = self.vector_index.search(query_array, min(top_k, self.vector_count))
            
            # Build results
            results = []
            for rank, (score, idx) in enumerate(zip(scores, indices)):
                if idx < 0 or idx >= self.vector_count:  # FAISS can return -1 for empty slots
                    continue
                    
                chunk_id = self.index_to_id.get(idx)
                if chunk_id and chunk_id in self.chunks:
                    result = SearchResult(
                        chunk=self.chunks[chunk_id],
                        score=float(score),
                        chunk_id=chunk_id,
                        rank=rank
                    )
                    results.append(result)
            
            logger.debug(f"🔍 Vector search for '{query[:30]}...' returned {len(results)} results")
            return results
    
    def search_by_chunk(self, chunk: Any, top_k: int = 3) -> List[SearchResult]:
        """
        Find similar chunks to a given memory chunk.
        
        Args:
            chunk: MemoryChunk to find similarities for
            top_k: Number of top results to return
            
        Returns:
            List[SearchResult]: Ranked search results
        """
        # Get chunk text content
        chunk_text = self._extract_text(chunk)
        results = self.search(chunk_text, top_k + 1)  # +1 to account for self-match
        
        # Filter out self-match if present
        chunk_id = self._get_chunk_id(chunk)
        filtered_results = [r for r in results if r.chunk_id != chunk_id]
        
        return filtered_results[:top_k]
    
    def search_with_pulse_state(self, query: str, pulse_state: Dict, top_k: int = 3) -> List[SearchResult]:
        """
        Hybrid scoring with pulse state integration (DAWN-specific).
        
        Args:
            query: Search query string
            pulse_state: Current pulse state for relevance weighting
            top_k: Number of top results to return
            
        Returns:
            List[SearchResult]: Ranked search results with pulse state weighting
        """
        # Get base semantic results
        base_results = self.search(query, top_k * 2)  # Get more to allow for reranking
        
        # Apply pulse state weighting
        weighted_results = []
        for result in base_results:
            chunk = result.chunk
            
            # Calculate pulse state similarity bonus
            pulse_bonus = 0.0
            
            if hasattr(chunk, 'pulse_state') and chunk.pulse_state:
                chunk_pulse = chunk.pulse_state
                
                # Heat level boost for urgent memories
                if 'heat' in pulse_state and 'heat' in chunk_pulse:
                    heat_similarity = 1.0 - abs(pulse_state['heat'] - chunk_pulse['heat']) / 100.0
                    pulse_bonus += max(0, heat_similarity) * 0.2
                
                # Mood-based relevance weighting
                if 'mood' in pulse_state and 'mood' in chunk_pulse:
                    if pulse_state['mood'] == chunk_pulse['mood']:
                        pulse_bonus += 0.3
                
                # Entropy state similarity
                if 'entropy' in pulse_state and 'entropy' in chunk_pulse:
                    entropy_similarity = 1.0 - abs(pulse_state['entropy'] - chunk_pulse['entropy'])
                    pulse_bonus += max(0, entropy_similarity) * 0.2
            
            # Create new result with adjusted score
            adjusted_result = SearchResult(
                chunk=result.chunk,
                score=result.score + pulse_bonus,
                chunk_id=result.chunk_id,
                rank=result.rank
            )
            weighted_results.append(adjusted_result)
        
        # Re-sort by adjusted score and limit results
        weighted_results.sort(key=lambda x: x.score, reverse=True)
        
        # Update ranks
        for i, result in enumerate(weighted_results[:top_k]):
            result.rank = i
        
        logger.debug(f"🌡️ Pulse-weighted search returned {len(weighted_results[:top_k])} results")
        return weighted_results[:top_k]
    
    def search_with_filters(self, query: str, speaker: str = None, topic: str = None, mood: str = None, top_k: int = 3) -> List[SearchResult]:
        """
        Filtered search by speaker, topic, or mood (DAWN-specific).
        
        Args:
            query: Search query string
            speaker: Filter by speaker identity
            topic: Filter by topic
            mood: Filter by mood state
            top_k: Number of top results to return
            
        Returns:
            List[SearchResult]: Filtered search results
        """
        # Get all semantic results
        all_results = self.search(query, self.vector_count)
        
        # Apply filters
        filtered_results = []
        for result in all_results:
            chunk = result.chunk
            
            # Apply speaker filter
            if speaker and hasattr(chunk, 'speaker') and chunk.speaker != speaker:
                continue
            
            # Apply topic filter
            if topic and hasattr(chunk, 'topic') and chunk.topic != topic:
                continue
            
            # Apply mood filter
            if mood:
                chunk_mood = getattr(chunk, 'get_mood', lambda: None)()
                if chunk_mood != mood:
                    continue
            
            filtered_results.append(result)
            
            if len(filtered_results) >= top_k:
                break
        
        # Update ranks
        for i, result in enumerate(filtered_results):
            result.rank = i
        
        logger.debug(f"🔍 Filtered search returned {len(filtered_results)} results")
        return filtered_results
    
    def get_chunk(self, chunk_id: str) -> Optional[Any]:
        """Get a specific chunk by ID"""
        return self.chunks.get(chunk_id)
    
    def remove_chunk(self, chunk_id: str) -> bool:
        """
        Remove a chunk from the index.
        Note: FAISS doesn't support efficient removal, so this is a logical removal.
        """
        with self.lock:
            if chunk_id not in self.chunks:
                return False
            
            # Remove from storage
            del self.chunks[chunk_id]
            del self.chunk_metadata[chunk_id]
            
            # Note: Actual vector removal from FAISS would require rebuilding the index
            # For now, we just mark it as removed in our metadata
            logger.debug(f"🗑️ Marked chunk {chunk_id[:8]}... for removal (index rebuild needed)")
            return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        with self.lock:
            return {
                'total_chunks': len(self.chunks),
                'vector_count': self.vector_count,
                'backend': 'faiss' if self.config.use_faiss else 'mock',
                'dimension': self.config.dimension,
                'metric': self.config.metric,
                'memory_usage_mb': self._estimate_memory_usage(),
                'dawn_integration_enabled': self.dawn_integration_enabled
            }
    
    def _get_chunk_id(self, chunk: Any) -> str:
        """Get or generate chunk ID"""
        if hasattr(chunk, 'memory_id') and chunk.memory_id:
            return str(chunk.memory_id)
        elif hasattr(chunk, 'id') and chunk.id:
            return str(chunk.id)
        elif hasattr(chunk, 'chunk_id') and chunk.chunk_id:
            return str(chunk.chunk_id)
        else:
            # Generate new UUID
            new_id = str(uuid.uuid4())
            # Try to set it on the chunk if possible
            if hasattr(chunk, 'memory_id'):
                chunk.memory_id = new_id
            elif hasattr(chunk, 'id'):
                chunk.id = new_id
            return new_id
    
    def _extract_text(self, chunk: Any) -> str:
        """Extract text content from memory chunk"""
        if hasattr(chunk, 'content'):
            return str(chunk.content)
        elif hasattr(chunk, 'text'):
            return str(chunk.text)
        elif hasattr(chunk, 'data'):
            return str(chunk.data)
        else:
            return str(chunk)
    
    def _extract_metadata(self, chunk: Any) -> Dict[str, Any]:
        """Extract metadata from memory chunk for filtering and analysis"""
        metadata = {
            'added_timestamp': time.time(),
            'chunk_type': type(chunk).__name__
        }
        
        # Extract DAWN-specific attributes
        if hasattr(chunk, 'speaker'):
            metadata['speaker'] = chunk.speaker
        if hasattr(chunk, 'topic'):
            metadata['topic'] = chunk.topic
        if hasattr(chunk, 'timestamp'):
            metadata['created_at'] = chunk.timestamp
        if hasattr(chunk, 'sigils'):
            metadata['sigils'] = chunk.sigils
        if hasattr(chunk, 'get_mood'):
            metadata['mood'] = chunk.get_mood()
        if hasattr(chunk, 'get_entropy'):
            metadata['entropy'] = chunk.get_entropy()
        if hasattr(chunk, 'get_heat'):
            metadata['heat'] = chunk.get_heat()
        if hasattr(chunk, 'get_scup'):
            metadata['scup'] = chunk.get_scup()
        
        return metadata
    
    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage in MB"""
        # Rough estimation
        vector_size = self.vector_count * self.config.dimension * 4  # 4 bytes per float32
        metadata_size = len(self.chunks) * 1000  # Rough estimate
        return (vector_size + metadata_size) / (1024 * 1024)
    
    def log_search_to_rebloom(self, query: str, results: List[SearchResult]):
        """Integration with rebloom lineage log (future feature)"""
        # TODO: Log search operations to rebloom_logger for:
        # - Search pattern analysis
        # - Memory access tracking
        # - Rebloom trigger correlation
        # - Performance optimization insights
        logger.debug(f"📊 Logged search '{query[:30]}...' with {len(results)} results to rebloom system")


# Factory function for creating DAWN vector index
def create_dawn_vector_index(config: Optional[IndexConfig] = None) -> DAWNVectorIndex:
    """Factory function for creating a new DAWNVectorIndex instance."""
    return DAWNVectorIndex(config=config)


# Integration with DAWN memory routing system
def integrate_vector_index(memory_routing_system):
    """Integrate vector index with existing memory routing system."""
    vector_index = DAWNVectorIndex()
    
    # Add vector index to the memory routing system
    if hasattr(memory_routing_system, 'router'):
        memory_routing_system.vector_index = vector_index
        logger.info("🔍 Vector index integrated with memory routing system")
    
    return vector_index 