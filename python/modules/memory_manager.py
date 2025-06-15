import asyncio
import logging
import time
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
import json
import hashlib

logger = logging.getLogger(__name__)


@dataclass
class MemoryFragment:
    """Represents a fragment of memory"""
    id: str
    content: Dict[str, Any]
    timestamp: float
    importance: float  # 0-1
    access_count: int = 0
    last_accessed: float = 0.0
    associations: List[str] = field(default_factory=list)  # IDs of related fragments
    emotional_weight: float = 0.0
    decay_rate: float = 0.01
    
    def access(self):
        """Record an access to this fragment"""
        self.access_count += 1
        self.last_accessed = time.time()
        # Strengthen importance with access
        self.importance = min(1.0, self.importance + 0.01)
    
    def decay(self, delta_time: float):
        """Apply time-based decay to the fragment"""
        decay_amount = self.decay_rate * delta_time
        self.importance = max(0.0, self.importance - decay_amount)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp,
            'importance': self.importance,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed,
            'associations': self.associations,
            'emotional_weight': self.emotional_weight
        }


@dataclass
class MemoryPattern:
    """Represents a recurring pattern in memory"""
    pattern_id: str
    pattern_type: str  # 'sequence', 'association', 'cyclic'
    elements: List[str]  # Fragment IDs
    strength: float  # 0-1
    frequency: int
    last_occurrence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'pattern_id': self.pattern_id,
            'pattern_type': self.pattern_type,
            'elements': self.elements,
            'strength': self.strength,
            'frequency': self.frequency,
            'last_occurrence': self.last_occurrence
        }


class MemoryManager:
    """
    Manages memory fragments, patterns, and pressure for consciousness simulation.
    Handles memory formation, retrieval, and consolidation.
    """
    
    def __init__(self, max_fragments: int = 10000):
        self.max_fragments = max_fragments
        self.fragments: Dict[str, MemoryFragment] = {}
        self.patterns: Dict[str, MemoryPattern] = {}
        
        # Memory organization
        self.short_term_memory = deque(maxlen=100)  # Recent fragments
        self.long_term_memory = []  # Important/consolidated fragments
        self.working_memory = deque(maxlen=20)  # Currently active fragments
        
        # Memory pressure and metrics
        self.memory_pressure = 0.3
        self.consolidation_threshold = 0.7
        self.forgetting_threshold = 0.1
        
        # Pattern detection
        self.pattern_window = 50
        self.pattern_threshold = 0.6
        
        # Access patterns for analysis
        self.access_history = deque(maxlen=1000)
        self.consolidation_events = []
        
        # Performance metrics
        self.retrieval_times = []
        self.compression_ratio = 1.0
        
        logger.info(f"Memory manager initialized with capacity for {max_fragments} fragments")
    
    async def get_state(self, tick_number: int) -> Dict[str, Any]:
        """Get current memory state"""
        # Update memory dynamics
        await self._update_memory_dynamics(tick_number)
        
        # Calculate metrics
        pressure = self._calculate_memory_pressure()
        consolidation_rate = self._calculate_consolidation_rate()
        fragmentation = self._calculate_fragmentation()
        
        return {
            'pressure': pressure,
            'total_fragments': len(self.fragments),
            'short_term_count': len(self.short_term_memory),
            'long_term_count': len(self.long_term_memory),
            'working_memory_count': len(self.working_memory),
            'consolidation_rate': consolidation_rate,
            'fragmentation': fragmentation,
            'pattern_count': len(self.patterns),
            'avg_fragment_importance': self._calculate_avg_importance(),
            'memory_efficiency': self._calculate_memory_efficiency(),
            'retrieval_performance': self._calculate_retrieval_performance(),
            'compression_ratio': self.compression_ratio
        }
    
    async def _update_memory_dynamics(self, tick_number: int):
        """Update memory system dynamics"""
        current_time = time.time()
        
        # Apply decay to all fragments
        await self._apply_memory_decay(current_time)
        
        # Check for consolidation opportunities
        await self._consolidate_memories()
        
        # Detect new patterns
        await self._detect_patterns()
        
        # Manage memory pressure
        await self._manage_memory_pressure()
        
        # Update working memory
        await self._update_working_memory(tick_number)
    
    async def _apply_memory_decay(self, current_time: float):
        """Apply time-based decay to memory fragments"""
        to_remove = []
        
        for fragment_id, fragment in self.fragments.items():
            # Calculate time since last access
            time_since_access = current_time - fragment.last_accessed
            
            # Apply decay
            fragment.decay(time_since_access / 3600)  # Convert to hours
            
            # Mark for removal if importance too low
            if fragment.importance < self.forgetting_threshold:
                to_remove.append(fragment_id)
        
        # Remove forgotten fragments
        for fragment_id in to_remove:
            await self._forget_fragment(fragment_id)
    
    async def _consolidate_memories(self):
        """Consolidate important short-term memories to long-term"""
        consolidation_candidates = []
        
        # Find high-importance fragments in short-term memory
        for fragment_id in self.short_term_memory:
            if fragment_id in self.fragments:
                fragment = self.fragments[fragment_id]
                if fragment.importance > self.consolidation_threshold:
                    consolidation_candidates.append(fragment)
        
        # Consolidate candidates
        for fragment in consolidation_candidates:
            await self._consolidate_fragment(fragment)
    
    async def _consolidate_fragment(self, fragment: MemoryFragment):
        """Consolidate a fragment to long-term memory"""
        if fragment.id not in [f.id for f in self.long_term_memory]:
            self.long_term_memory.append(fragment)
            
            # Strengthen associations
            await self._strengthen_associations(fragment)
            
            # Record consolidation event
            self.consolidation_events.append({
                'fragment_id': fragment.id,
                'timestamp': time.time(),
                'importance': fragment.importance
            })
            
            logger.debug(f"Consolidated fragment {fragment.id} to long-term memory")
    
    async def _detect_patterns(self):
        """Detect patterns in memory access and content"""
        if len(self.access_history) < self.pattern_window:
            return
        
        recent_accesses = list(self.access_history)[-self.pattern_window:]
        
        # Detect sequence patterns
        await self._detect_sequence_patterns(recent_accesses)
        
        # Detect association patterns
        await self._detect_association_patterns()
        
        # Detect cyclic patterns
        await self._detect_cyclic_patterns(recent_accesses)
    
    async def _detect_sequence_patterns(self, accesses: List[str]):
        """Detect sequential access patterns"""
        sequence_length = 3
        
        for i in range(len(accesses) - sequence_length + 1):
            sequence = accesses[i:i + sequence_length]
            
            # Create pattern ID
            pattern_id = hashlib.md5('_'.join(sequence).encode()).hexdigest()[:8]
            
            if pattern_id in self.patterns:
                # Update existing pattern
                pattern = self.patterns[pattern_id]
                pattern.frequency += 1
                pattern.strength = min(1.0, pattern.strength + 0.1)
                pattern.last_occurrence = time.time()
            else:
                # Create new pattern
                pattern = MemoryPattern(
                    pattern_id=pattern_id,
                    pattern_type='sequence',
                    elements=sequence,
                    strength=0.3,
                    frequency=1,
                    last_occurrence=time.time()
                )
                self.patterns[pattern_id] = pattern
    
    async def _detect_association_patterns(self):
        """Detect association patterns between fragments"""
        for fragment in self.fragments.values():
            if fragment.associations:
                # Analyze co-occurrence of associated fragments
                for assoc_id in fragment.associations:
                    if assoc_id in self.fragments:
                        # Check if these fragments are accessed together
                        pattern_strength = self._calculate_association_strength(fragment.id, assoc_id)
                        
                        if pattern_strength > self.pattern_threshold:
                            pattern_id = f"assoc_{fragment.id}_{assoc_id}"
                            
                            if pattern_id not in self.patterns:
                                pattern = MemoryPattern(
                                    pattern_id=pattern_id,
                                    pattern_type='association',
                                    elements=[fragment.id, assoc_id],
                                    strength=pattern_strength,
                                    frequency=1,
                                    last_occurrence=time.time()
                                )
                                self.patterns[pattern_id] = pattern
    
    async def _detect_cyclic_patterns(self, accesses: List[str]):
        """Detect cyclic patterns in memory access"""
        # Look for repeating subsequences
        for cycle_length in range(2, 10):
            if len(accesses) < cycle_length * 2:
                continue
            
            for start in range(len(accesses) - cycle_length * 2):
                cycle1 = accesses[start:start + cycle_length]
                cycle2 = accesses[start + cycle_length:start + cycle_length * 2]
                
                if cycle1 == cycle2:
                    pattern_id = f"cycle_{hashlib.md5('_'.join(cycle1).encode()).hexdigest()[:8]}"
                    
                    if pattern_id in self.patterns:
                        self.patterns[pattern_id].frequency += 1
                        self.patterns[pattern_id].strength = min(1.0, self.patterns[pattern_id].strength + 0.05)
                    else:
                        pattern = MemoryPattern(
                            pattern_id=pattern_id,
                            pattern_type='cyclic',
                            elements=cycle1,
                            strength=0.4,
                            frequency=1,
                            last_occurrence=time.time()
                        )
                        self.patterns[pattern_id] = pattern
    
    async def _manage_memory_pressure(self):
        """Manage memory pressure by removing low-importance fragments"""
        self.memory_pressure = len(self.fragments) / self.max_fragments
        
        if self.memory_pressure > 0.9:
            # Emergency cleanup
            await self._emergency_cleanup()
        elif self.memory_pressure > 0.7:
            # Gentle cleanup
            await self._gentle_cleanup()
    
    async def _emergency_cleanup(self):
        """Emergency memory cleanup when pressure is critical"""
        # Remove fragments with lowest importance
        fragments_by_importance = sorted(
            self.fragments.values(),
            key=lambda f: f.importance
        )
        
        to_remove = fragments_by_importance[:len(fragments_by_importance) // 4]
        
        for fragment in to_remove:
            await self._forget_fragment(fragment.id)
        
        logger.warning(f"Emergency cleanup removed {len(to_remove)} fragments")
    
    async def _gentle_cleanup(self):
        """Gentle memory cleanup for normal pressure relief"""
        current_time = time.time()
        to_remove = []
        
        for fragment in self.fragments.values():
            # Remove old, unimportant, rarely accessed fragments
            age = current_time - fragment.timestamp
            if (age > 3600 and  # Older than 1 hour
                fragment.importance < 0.3 and
                fragment.access_count < 3):
                to_remove.append(fragment.id)
        
        for fragment_id in to_remove:
            await self._forget_fragment(fragment_id)
        
        if to_remove:
            logger.debug(f"Gentle cleanup removed {len(to_remove)} fragments")
    
    async def _update_working_memory(self, tick_number: int):
        """Update working memory with currently relevant fragments"""
        # Add recently accessed fragments to working memory
        recent_access_threshold = time.time() - 60  # Last minute
        
        for fragment in self.fragments.values():
            if (fragment.last_accessed > recent_access_threshold and
                fragment.id not in self.working_memory):
                self.working_memory.append(fragment.id)
    
    def store_fragment(self, content: Dict[str, Any], importance: float = 0.5) -> str:
        """Store a new memory fragment"""
        fragment_id = hashlib.md5(json.dumps(content, sort_keys=True).encode()).hexdigest()[:16]
        
        fragment = MemoryFragment(
            id=fragment_id,
            content=content,
            timestamp=time.time(),
            importance=importance,
            last_accessed=time.time()
        )
        
        self.fragments[fragment_id] = fragment
        self.short_term_memory.append(fragment_id)
        
        logger.debug(f"Stored memory fragment {fragment_id}")
        return fragment_id
    
    def retrieve_fragment(self, fragment_id: str) -> Optional[MemoryFragment]:
        """Retrieve a memory fragment by ID"""
        if fragment_id in self.fragments:
            fragment = self.fragments[fragment_id]
            fragment.access()
            self.access_history.append(fragment_id)
            
            return fragment
        
        return None
    
    def search_fragments(self, query: Dict[str, Any], limit: int = 10) -> List[MemoryFragment]:
        """Search for fragments matching a query"""
        matches = []
        
        for fragment in self.fragments.values():
            similarity = self._calculate_similarity(fragment.content, query)
            if similarity > 0.5:
                matches.append((fragment, similarity))
        
        # Sort by similarity and return top matches
        matches.sort(key=lambda x: x[1], reverse=True)
        return [match[0] for match in matches[:limit]]
    
    def create_association(self, fragment_id1: str, fragment_id2: str, strength: float = 0.5):
        """Create an association between two fragments"""
        if fragment_id1 in self.fragments and fragment_id2 in self.fragments:
            frag1 = self.fragments[fragment_id1]
            frag2 = self.fragments[fragment_id2]
            
            if fragment_id2 not in frag1.associations:
                frag1.associations.append(fragment_id2)
            if fragment_id1 not in frag2.associations:
                frag2.associations.append(fragment_id1)
            
            logger.debug(f"Created association between {fragment_id1} and {fragment_id2}")
    
    async def _forget_fragment(self, fragment_id: str):
        """Remove a fragment from memory"""
        if fragment_id in self.fragments:
            # Remove from all memory stores
            if fragment_id in self.fragments:
                del self.fragments[fragment_id]
            
            # Remove from memory stores
            if fragment_id in self.short_term_memory:
                self.short_term_memory.remove(fragment_id)
            
            self.long_term_memory = [f for f in self.long_term_memory if f.id != fragment_id]
            
            if fragment_id in self.working_memory:
                self.working_memory.remove(fragment_id)
            
            # Remove associations
            for fragment in self.fragments.values():
                if fragment_id in fragment.associations:
                    fragment.associations.remove(fragment_id)
            
            logger.debug(f"Forgot fragment {fragment_id}")
    
    async def _strengthen_associations(self, fragment: MemoryFragment):
        """Strengthen associations for a consolidated fragment"""
        for assoc_id in fragment.associations:
            if assoc_id in self.fragments:
                assoc_fragment = self.fragments[assoc_id]
                assoc_fragment.importance = min(1.0, assoc_fragment.importance + 0.05)
    
    def _calculate_memory_pressure(self) -> float:
        """Calculate current memory pressure"""
        return len(self.fragments) / self.max_fragments
    
    def _calculate_consolidation_rate(self) -> float:
        """Calculate rate of memory consolidation"""
        recent_consolidations = [
            event for event in self.consolidation_events
            if time.time() - event['timestamp'] < 3600  # Last hour
        ]
        
        return len(recent_consolidations) / 60  # Per minute
    
    def _calculate_fragmentation(self) -> float:
        """Calculate memory fragmentation level"""
        if not self.fragments:
            return 0.0
        
        # Fragmentation based on importance distribution
        importances = [f.importance for f in self.fragments.values()]
        std_dev = np.std(importances)
        
        return min(1.0, std_dev * 2)  # Normalize to 0-1
    
    def _calculate_avg_importance(self) -> float:
        """Calculate average fragment importance"""
        if not self.fragments:
            return 0.0
        
        return sum(f.importance for f in self.fragments.values()) / len(self.fragments)
    
    def _calculate_memory_efficiency(self) -> float:
        """Calculate memory system efficiency"""
        if not self.fragments:
            return 1.0
        
        # Efficiency based on ratio of important to total fragments
        important_fragments = sum(1 for f in self.fragments.values() if f.importance > 0.5)
        return important_fragments / len(self.fragments)
    
    def _calculate_retrieval_performance(self) -> float:
        """Calculate average retrieval performance"""
        if not self.retrieval_times:
            return 1.0
        
        avg_time = sum(self.retrieval_times) / len(self.retrieval_times)
        return max(0.0, 1.0 - avg_time)  # Lower time = better performance
    
    def _calculate_similarity(self, content1: Dict[str, Any], content2: Dict[str, Any]) -> float:
        """Calculate similarity between two content dictionaries"""
        # Simple similarity based on matching keys and values
        keys1 = set(content1.keys())
        keys2 = set(content2.keys())
        
        common_keys = keys1.intersection(keys2)
        if not common_keys:
            return 0.0
        
        matches = sum(1 for key in common_keys if content1[key] == content2[key])
        return matches / len(keys1.union(keys2))
    
    def _calculate_association_strength(self, fragment_id1: str, fragment_id2: str) -> float:
        """Calculate strength of association between two fragments"""
        # Count co-occurrences in access history
        recent_accesses = list(self.access_history)[-100:]
        
        cooccurrences = 0
        window_size = 5
        
        for i in range(len(recent_accesses) - window_size):
            window = recent_accesses[i:i + window_size]
            if fragment_id1 in window and fragment_id2 in window:
                cooccurrences += 1
        
        return min(1.0, cooccurrences / 10)  # Normalize
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get a summary of memory system state"""
        return {
            'total_fragments': len(self.fragments),
            'memory_stores': {
                'short_term': len(self.short_term_memory),
                'long_term': len(self.long_term_memory),
                'working_memory': len(self.working_memory)
            },
            'patterns': {
                'total': len(self.patterns),
                'by_type': {
                    ptype: sum(1 for p in self.patterns.values() if p.pattern_type == ptype)
                    for ptype in ['sequence', 'association', 'cyclic']
                }
            },
            'pressure': self.memory_pressure,
            'efficiency': self._calculate_memory_efficiency(),
            'recent_activity': len(self.access_history)
        } 