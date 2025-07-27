from typing import Dict, Any, List, Optional, Tuple
import numpy as np
from datetime import datetime
import math
from collections import defaultdict
import heapq
from scipy.spatial.distance import cosine

class Memory:
    def __init__(self, data: Dict[str, Any], importance: float = 0.0):
        self.data = data
        self.importance = importance
        self.timestamp = datetime.now()
        self.access_count = 0
        self.last_access = self.timestamp
        self.associations = set()
        self.embedding = None
        self.decay_rate = 0.1
        self.recency_score = 1.0
    
    def update_recency(self) -> None:
        """Update recency score based on time decay"""
        time_diff = (datetime.now() - self.timestamp).total_seconds()
        self.recency_score = math.exp(-self.decay_rate * time_diff)
    
    def get_relevance_score(self) -> float:
        """Calculate overall relevance score"""
        return (self.importance * 0.4 + 
                self.recency_score * 0.3 + 
                (self.access_count / 100) * 0.3)

class MemoryManager:
    def __init__(self, max_memories: int = 1000):
        self.memories = []
        self.max_memories = max_memories
        self.last_update = datetime.now()
        self.memory_index = defaultdict(set)
        self.association_graph = defaultdict(set)
        self.importance_threshold = 0.3
        self.consolidation_threshold = 0.7
        self.consolidation_interval = 3600  # 1 hour
        self.last_consolidation = datetime.now()
    
    def _update_memory_scores(self) -> None:
        """Update scores for all memories"""
        for memory in self.memories:
            memory.update_recency()
    
    def _consolidate_memories(self) -> None:
        """Consolidate and prune memories based on relevance"""
        self._update_memory_scores()
        
        # Sort memories by relevance
        self.memories.sort(key=lambda m: m.get_relevance_score(), reverse=True)
        
        # Keep only the most relevant memories
        if len(self.memories) > self.max_memories:
            self.memories = self.memories[:self.max_memories]
        
        # Update memory index
        self.memory_index.clear()
        for memory in self.memories:
            for key, value in memory.data.items():
                if isinstance(value, (str, int, float)):
                    self.memory_index[value].add(memory)
        
        self.last_consolidation = datetime.now()
    
    def _find_similar_memories(self, memory: Memory, threshold: float = 0.8) -> List[Memory]:
        """Find memories similar to the given memory"""
        if not memory.embedding:
            return []
        
        similar_memories = []
        for other in self.memories:
            if other.embedding and other != memory:
                similarity = 1 - cosine(memory.embedding, other.embedding)
                if similarity >= threshold:
                    similar_memories.append((other, similarity))
        
        return [m for m, _ in sorted(similar_memories, key=lambda x: x[1], reverse=True)]
    
    def _update_associations(self, memory: Memory) -> None:
        """Update memory associations based on similarity"""
        similar_memories = self._find_similar_memories(memory)
        for similar, _ in similar_memories:
            memory.associations.add(similar)
            similar.associations.add(memory)
            self.association_graph[memory].add(similar)
            self.association_graph[similar].add(memory)
    
    def add_memory(self, data: Dict[str, Any], importance: float = 0.0, 
                  embedding: Optional[np.ndarray] = None) -> Memory:
        """Add a new memory"""
        memory = Memory(data, importance)
        memory.embedding = embedding
        
        self.memories.append(memory)
        self._update_associations(memory)
        
        # Update memory index
        for key, value in data.items():
            if isinstance(value, (str, int, float)):
                self.memory_index[value].add(memory)
        
        # Check if consolidation is needed
        if (datetime.now() - self.last_consolidation).total_seconds() > self.consolidation_interval:
            self._consolidate_memories()
        
        self.last_update = datetime.now()
        return memory
    
    def get_memory(self, memory_id: int) -> Optional[Memory]:
        """Get a specific memory by ID"""
        if 0 <= memory_id < len(self.memories):
            memory = self.memories[memory_id]
            memory.access_count += 1
            memory.last_access = datetime.now()
            return memory
        return None
    
    def search_memories(self, query: str, limit: int = 10) -> List[Memory]:
        """Search memories by query"""
        # Update memory scores
        self._update_memory_scores()
        
        # Find memories containing the query
        matching_memories = set()
        for value, memories in self.memory_index.items():
            if query.lower() in str(value).lower():
                matching_memories.update(memories)
        
        # Sort by relevance
        sorted_memories = sorted(
            matching_memories,
            key=lambda m: m.get_relevance_score(),
            reverse=True
        )
        
        return sorted_memories[:limit]
    
    def get_associated_memories(self, memory: Memory, limit: int = 5) -> List[Memory]:
        """Get memories associated with the given memory"""
        return list(memory.associations)[:limit]
    
    def update_memory_importance(self, memory: Memory, importance: float) -> None:
        """Update the importance of a memory"""
        memory.importance = max(0.0, min(1.0, importance))
        self.last_update = datetime.now()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        total_importance = sum(m.importance for m in self.memories)
        avg_importance = total_importance / len(self.memories) if self.memories else 0
        
        return {
            'total_memories': len(self.memories),
            'average_importance': avg_importance,
            'memory_distribution': {
                'high_importance': len([m for m in self.memories if m.importance > 0.7]),
                'medium_importance': len([m for m in self.memories if 0.3 <= m.importance <= 0.7]),
                'low_importance': len([m for m in self.memories if m.importance < 0.3])
            },
            'association_density': len(self.association_graph) / (len(self.memories) * (len(self.memories) - 1)) if len(self.memories) > 1 else 0
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get memory manager metrics"""
        return {
            'total_memories': len(self.memories),
            'memory_stats': self.get_memory_stats(),
            'last_consolidation': self.last_consolidation.isoformat(),
            'last_update': self.last_update.isoformat()
        }

def create_memory_manager(max_memories: int = 1000) -> MemoryManager:
    """Create and return a new memory manager instance"""
    return MemoryManager(max_memories)

# Singleton instance
_memory_manager = None

def get_memory_manager() -> MemoryManager:
    """Get or create the singleton memory manager instance"""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = create_memory_manager()
    return _memory_manager 