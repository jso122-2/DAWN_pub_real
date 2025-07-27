"""
DAWN View-Count Based Memory System
Simple memory system focused on view counting for memory strength determination.
Integrates with emotional sigil states for richer recall context.
"""

import json
import time
import math
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class ViewMemory:
    """Simple memory with view-count based strength"""
    memory_id: str
    content: str
    context: Dict[str, Any]
    sigil_state: Dict[str, float]  # Emotional sigil intensities when created
    view_count: int
    created_at: float
    last_accessed: float
    trigger_keywords: List[str]
    
    def get_strength(self) -> float:
        """Calculate memory strength based on view count"""
        return math.log(self.view_count + 1)

class MemoryManager:
    """View-count based memory system with sigil integration"""
    
    def __init__(self, storage_path: str = "view_memories.json"):
        self.memories: Dict[str, ViewMemory] = {}  # id -> ViewMemory
        self.storage_path = Path(storage_path)
        self.keyword_index: Dict[str, List[str]] = defaultdict(list)  # keyword -> memory_ids
        self.sigil_index: Dict[str, List[str]] = defaultdict(list)  # dominant_emotion -> memory_ids
        
        # Load existing memories
        self._load_memories()
        
        logger.info(f"View-based MemoryManager initialized with {len(self.memories)} memories")
    
    def record_memory(self, content: str, context: Dict[str, Any], 
                     sigil_state: Optional[Dict[str, float]] = None) -> str:
        """
        Create memory with view_count = 1
        Associate with current sigil state
        """
        current_time = time.time()
        
        # Generate unique memory ID
        content_hash = hashlib.md5(f"{content}:{current_time}".encode()).hexdigest()
        memory_id = f"view_mem_{int(current_time)}_{content_hash[:8]}"
        
        # Extract trigger keywords from content
        trigger_keywords = self._extract_keywords(content)
        
        # Use provided sigil state or empty dict
        if sigil_state is None:
            sigil_state = {}
        
        # Create memory with initial view count of 1
        memory = ViewMemory(
            memory_id=memory_id,
            content=content,
            context=context.copy(),
            sigil_state=sigil_state.copy(),
            view_count=1,  # Start with 1 view (creation counts as viewing)
            created_at=current_time,
            last_accessed=current_time,
            trigger_keywords=trigger_keywords
        )
        
        # Store memory
        self.memories[memory_id] = memory
        
        # Update indices
        self._update_keyword_index(memory_id, trigger_keywords)
        self._update_sigil_index(memory_id, sigil_state)
        
        # Auto-save
        self._save_memories()
        
        logger.info(f"Recorded memory {memory_id}: {content[:50]}... (sigils: {list(sigil_state.keys())})")
        
        return memory_id
    
    def recall_memory(self, trigger: str, current_sigil_state: Optional[Dict[str, float]] = None,
                     limit: int = 10) -> List[Tuple[ViewMemory, float]]:
        """
        Find relevant memories
        Increment view_count of accessed memories
        Return by strength (log(view_count + 1))
        """
        # Extract keywords from trigger
        trigger_keywords = self._extract_keywords(trigger)
        
        # Find candidate memories
        candidates = set()
        
        # Search by keyword overlap
        for keyword in trigger_keywords:
            if keyword in self.keyword_index:
                candidates.update(self.keyword_index[keyword])
        
        # Search by sigil state similarity if provided
        if current_sigil_state:
            dominant_emotion = self._get_dominant_emotion(current_sigil_state)
            if dominant_emotion and dominant_emotion in self.sigil_index:
                candidates.update(self.sigil_index[dominant_emotion])
        
        # If no candidates found, return empty
        if not candidates:
            return []
        
        # Calculate relevance scores for candidates
        scored_memories = []
        
        for memory_id in candidates:
            if memory_id not in self.memories:
                continue
                
            memory = self.memories[memory_id]
            
            # Calculate relevance score
            keyword_score = self._calculate_keyword_similarity(trigger_keywords, memory.trigger_keywords)
            sigil_score = self._calculate_sigil_similarity(current_sigil_state, memory.sigil_state)
            
            # Combined relevance (keyword matching is primary, sigil state secondary)
            relevance = keyword_score * 0.7 + sigil_score * 0.3
            
            if relevance > 0.1:  # Minimum relevance threshold
                scored_memories.append((memory, relevance))
        
        # Sort by relevance and limit results
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        recalled_memories = scored_memories[:limit]
        
        # Increment view count for accessed memories
        current_time = time.time()
        for memory, relevance in recalled_memories:
            memory.view_count += 1
            memory.last_accessed = current_time
            logger.debug(f"Memory {memory.memory_id} accessed, view_count now {memory.view_count}")
        
        # Auto-save after access
        if recalled_memories:
            self._save_memories()
        
        return recalled_memories
    
    def get_echo_strength(self, memory_id: str) -> float:
        """
        Get memory strength based purely on view count
        All memories equal - only view count determines strength
        No positive/negative weighting
        """
        if memory_id not in self.memories:
            return 0.0
        
        memory = self.memories[memory_id]
        return memory.get_strength()
    
    def get_memory_by_id(self, memory_id: str) -> Optional[ViewMemory]:
        """Get specific memory by ID without incrementing view count"""
        return self.memories.get(memory_id)
    
    def get_strongest_memories(self, limit: int = 20) -> List[ViewMemory]:
        """Get memories with highest view counts"""
        all_memories = list(self.memories.values())
        all_memories.sort(key=lambda m: m.get_strength(), reverse=True)
        return all_memories[:limit]
    
    def get_memories_by_sigil(self, dominant_emotion: str, limit: int = 10) -> List[ViewMemory]:
        """Get memories associated with a specific dominant emotion"""
        if dominant_emotion not in self.sigil_index:
            return []
        
        memory_ids = self.sigil_index[dominant_emotion][:limit]
        memories = [self.memories[mid] for mid in memory_ids if mid in self.memories]
        
        # Sort by strength
        memories.sort(key=lambda m: m.get_strength(), reverse=True)
        return memories
    
    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get comprehensive memory statistics"""
        if not self.memories:
            return {
                "total_memories": 0,
                "total_views": 0,
                "avg_views_per_memory": 0,
                "strongest_memory_views": 0,
                "dominant_emotions": {},
                "keyword_coverage": 0
            }
        
        total_views = sum(m.view_count for m in self.memories.values())
        avg_views = total_views / len(self.memories)
        strongest_views = max(m.view_count for m in self.memories.values())
        
        # Count memories by dominant emotion
        emotion_counts = defaultdict(int)
        for memory in self.memories.values():
            dominant = self._get_dominant_emotion(memory.sigil_state)
            if dominant:
                emotion_counts[dominant] += 1
        
        return {
            "total_memories": len(self.memories),
            "total_views": total_views,
            "avg_views_per_memory": avg_views,
            "strongest_memory_views": strongest_views,
            "dominant_emotions": dict(emotion_counts),
            "keyword_coverage": len(self.keyword_index),
            "sigil_coverage": len(self.sigil_index)
        }
    
    def search_memories(self, query: str, min_strength: float = 0.0) -> List[ViewMemory]:
        """Search memories by content with minimum strength filter"""
        query_lower = query.lower()
        matching_memories = []
        
        for memory in self.memories.values():
            if (query_lower in memory.content.lower() and 
                memory.get_strength() >= min_strength):
                matching_memories.append(memory)
        
        # Sort by strength
        matching_memories.sort(key=lambda m: m.get_strength(), reverse=True)
        return matching_memories
    
    def clear_weak_memories(self, min_views: int = 2) -> int:
        """Remove memories with very low view counts"""
        weak_memory_ids = [
            mid for mid, memory in self.memories.items() 
            if memory.view_count < min_views
        ]
        
        removed_count = 0
        for memory_id in weak_memory_ids:
            self._remove_memory(memory_id)
            removed_count += 1
        
        if removed_count > 0:
            self._save_memories()
            logger.info(f"Cleared {removed_count} weak memories (< {min_views} views)")
        
        return removed_count
    
    def export_memories(self, filepath: str) -> bool:
        """Export all memories to JSON file"""
        try:
            export_data = {
                "metadata": {
                    "export_time": time.time(),
                    "total_memories": len(self.memories),
                    "statistics": self.get_memory_statistics()
                },
                "memories": {
                    mid: asdict(memory) for mid, memory in self.memories.items()
                }
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Exported {len(self.memories)} memories to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export memories: {e}")
            return False
    
    def import_memories(self, filepath: str, merge: bool = True) -> bool:
        """Import memories from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if not merge:
                self.memories.clear()
                self._rebuild_indices()
            
            imported_count = 0
            for memory_id, memory_data in import_data.get("memories", {}).items():
                # Convert dict back to ViewMemory
                memory = ViewMemory(**memory_data)
                self.memories[memory_id] = memory
                
                # Update indices
                self._update_keyword_index(memory_id, memory.trigger_keywords)
                self._update_sigil_index(memory_id, memory.sigil_state)
                
                imported_count += 1
            
            self._save_memories()
            logger.info(f"Imported {imported_count} memories from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to import memories: {e}")
            return False
    
    # Private helper methods
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for indexing"""
        # Simple keyword extraction
        words = text.lower().split()
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        keywords = [word.strip('.,!?:;') for word in words if len(word) > 2 and word not in stop_words]
        
        # Remove duplicates and limit
        return list(set(keywords))[:10]
    
    def _get_dominant_emotion(self, sigil_state: Dict[str, float]) -> Optional[str]:
        """Get the dominant emotion from sigil state"""
        if not sigil_state:
            return None
        
        return max(sigil_state.items(), key=lambda x: x[1])[0] if sigil_state else None
    
    def _calculate_keyword_similarity(self, keywords1: List[str], keywords2: List[str]) -> float:
        """Calculate similarity between keyword lists"""
        if not keywords1 or not keywords2:
            return 0.0
        
        set1, set2 = set(keywords1), set(keywords2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        
        return intersection / union if union > 0 else 0.0
    
    def _calculate_sigil_similarity(self, sigil_state1: Optional[Dict[str, float]], 
                                   sigil_state2: Dict[str, float]) -> float:
        """Calculate similarity between sigil states"""
        if not sigil_state1 or not sigil_state2:
            return 0.0
        
        # Calculate cosine similarity between sigil vectors
        common_emotions = set(sigil_state1.keys()).intersection(set(sigil_state2.keys()))
        
        if not common_emotions:
            return 0.0
        
        dot_product = sum(sigil_state1[emotion] * sigil_state2[emotion] for emotion in common_emotions)
        
        magnitude1 = math.sqrt(sum(v**2 for v in sigil_state1.values()))
        magnitude2 = math.sqrt(sum(v**2 for v in sigil_state2.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _update_keyword_index(self, memory_id: str, keywords: List[str]):
        """Update keyword index"""
        for keyword in keywords:
            if memory_id not in self.keyword_index[keyword]:
                self.keyword_index[keyword].append(memory_id)
    
    def _update_sigil_index(self, memory_id: str, sigil_state: Dict[str, float]):
        """Update sigil-based index"""
        dominant_emotion = self._get_dominant_emotion(sigil_state)
        if dominant_emotion:
            if memory_id not in self.sigil_index[dominant_emotion]:
                self.sigil_index[dominant_emotion].append(memory_id)
    
    def _remove_memory(self, memory_id: str):
        """Remove memory and clean up indices"""
        if memory_id not in self.memories:
            return
        
        memory = self.memories[memory_id]
        
        # Remove from keyword index
        for keyword in memory.trigger_keywords:
            if keyword in self.keyword_index:
                if memory_id in self.keyword_index[keyword]:
                    self.keyword_index[keyword].remove(memory_id)
                if not self.keyword_index[keyword]:
                    del self.keyword_index[keyword]
        
        # Remove from sigil index
        dominant_emotion = self._get_dominant_emotion(memory.sigil_state)
        if dominant_emotion and dominant_emotion in self.sigil_index:
            if memory_id in self.sigil_index[dominant_emotion]:
                self.sigil_index[dominant_emotion].remove(memory_id)
            if not self.sigil_index[dominant_emotion]:
                del self.sigil_index[dominant_emotion]
        
        # Remove memory
        del self.memories[memory_id]
    
    def _rebuild_indices(self):
        """Rebuild all indices from current memories"""
        self.keyword_index.clear()
        self.sigil_index.clear()
        
        for memory_id, memory in self.memories.items():
            self._update_keyword_index(memory_id, memory.trigger_keywords)
            self._update_sigil_index(memory_id, memory.sigil_state)
    
    def _save_memories(self):
        """Save memories to disk"""
        try:
            save_data = {
                "metadata": {
                    "save_time": time.time(),
                    "total_memories": len(self.memories),
                    "version": "1.0"
                },
                "memories": {
                    mid: asdict(memory) for mid, memory in self.memories.items()
                }
            }
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save memories: {e}")
    
    def _load_memories(self):
        """Load memories from disk"""
        if not self.storage_path.exists():
            return
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                load_data = json.load(f)
            
            # Load memories
            for memory_id, memory_data in load_data.get("memories", {}).items():
                memory = ViewMemory(**memory_data)
                self.memories[memory_id] = memory
                
                # Update indices
                self._update_keyword_index(memory_id, memory.trigger_keywords)
                self._update_sigil_index(memory_id, memory.sigil_state)
            
            logger.info(f"Loaded {len(self.memories)} memories from {self.storage_path}")
            
        except Exception as e:
            logger.error(f"Failed to load memories: {e}")


# Global instance for easy access
view_memory_manager = MemoryManager()


def get_view_memory_manager() -> MemoryManager:
    """Get the global view-based memory manager instance"""
    return view_memory_manager


def create_view_memory_manager(storage_path: str = "view_memories.json") -> MemoryManager:
    """Create a new view-based memory manager instance"""
    return MemoryManager(storage_path) 