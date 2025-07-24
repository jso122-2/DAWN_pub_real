"""
DAWN Memory Chunk - Core Memory Unit
Represents individual memory fragments with metadata and system state.
Integrated with DAWN's existing memory infrastructure.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import logging

logger = logging.getLogger(__name__)


class MemoryChunk:
    """
    A single memory fragment with associated metadata and system state.
    Core unit for DAWN's memory routing and retrieval system.
    Integrates with existing DAWN memory infrastructure.
    """
    
    def __init__(
        self,
        timestamp: datetime,
        speaker: str,
        content: str,
        topic: Optional[str] = None,
        pulse_state: Optional[Dict[str, Any]] = None,
        sigils: Optional[List[str]] = None
    ):
        """
        Initialize a memory chunk.
        
        Args:
            timestamp: Datetime when memory was created
            speaker: Identity string of the memory creator
            content: Raw text content of the memory
            topic: Optional keyword or category
            pulse_state: Dict of mood/entropy/heat at time of logging
            sigils: List of linked symbolic actions
        """
        self.timestamp = timestamp
        self.speaker = speaker
        self.topic = topic
        self.content = content
        self.pulse_state = pulse_state or {}
        self.sigils = sigils or []
        
        # Computed metadata
        self.content_length = len(content)
        self.word_count = len(content.split()) if content else 0
        
        # Integration with DAWN memory systems
        self.memory_id = self._generate_memory_id()
        self.traced = False  # For integration with memory trace system
        self.anchor_linked = False  # For integration with memory anchor system
        
        logger.debug(f"Created MemoryChunk {self.memory_id}: {self.summary()}")
    
    def _generate_memory_id(self) -> str:
        """Generate unique memory ID compatible with DAWN's memory systems"""
        import hashlib
        content_hash = hashlib.md5(f"{self.content}:{self.timestamp.isoformat()}".encode()).hexdigest()
        return f"chunk_{int(self.timestamp.timestamp())}_{content_hash[:8]}"
    
    def summary(self) -> str:
        """
        Generate a short summary string of the memory chunk.
        
        Returns:
            str: Summary with timestamp, topic, and content length
        """
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        topic_str = f"[{self.topic}]" if self.topic else "[no topic]"
        
        return f"{timestamp_str} {topic_str} ({self.content_length} chars) - {self.speaker}"
    
    def get_entropy(self) -> float:
        """Get entropy value from pulse state, or 0.0 if not available."""
        return self.pulse_state.get('entropy', 0.0)
    
    def get_heat(self) -> float:
        """Get heat value from pulse state, or 0.0 if not available."""
        return self.pulse_state.get('heat', 0.0)
    
    def get_scup(self) -> float:
        """Get SCUP value from pulse state, or 0.5 if not available."""
        return self.pulse_state.get('scup', 0.5)
    
    def get_mood(self) -> str:
        """Get mood from pulse state, or 'neutral' if not available."""
        return self.pulse_state.get('mood', 'neutral')
    
    def has_sigil(self, sigil_name: str) -> bool:
        """Check if this memory is linked to a specific sigil."""
        return sigil_name in self.sigils
    
    def add_sigil(self, sigil_name: str) -> None:
        """Link a sigil to this memory chunk."""
        if sigil_name not in self.sigils:
            self.sigils.append(sigil_name)
            logger.debug(f"Added sigil {sigil_name} to memory {self.memory_id}")
    
    def get_preview(self, max_chars: int = 100) -> str:
        """
        Get a preview of the content with ellipsis if too long.
        
        Args:
            max_chars: Maximum characters to show
            
        Returns:
            str: Content preview
        """
        if len(self.content) <= max_chars:
            return self.content
        
        return self.content[:max_chars-3] + "..."
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert memory chunk to dictionary for serialization.
        Compatible with DAWN's existing memory systems.
        
        Returns:
            dict: Dictionary representation
        """
        return {
            'memory_id': self.memory_id,
            'timestamp': self.timestamp.isoformat(),
            'speaker': self.speaker,
            'topic': self.topic,
            'content': self.content,
            'pulse_state': self.pulse_state,
            'sigils': self.sigils,
            'content_length': self.content_length,
            'word_count': self.word_count,
            'traced': self.traced,
            'anchor_linked': self.anchor_linked
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryChunk':
        """
        Create a MemoryChunk from dictionary data.
        Compatible with DAWN's existing memory formats.
        
        Args:
            data: Dictionary with memory chunk data
            
        Returns:
            MemoryChunk: New memory chunk instance
        """
        # Parse timestamp
        if isinstance(data['timestamp'], str):
            timestamp = datetime.fromisoformat(data['timestamp'])
        else:
            timestamp = data['timestamp']
        
        chunk = cls(
            timestamp=timestamp,
            speaker=data['speaker'],
            content=data['content'],
            topic=data.get('topic'),
            pulse_state=data.get('pulse_state', {}),
            sigils=data.get('sigils', [])
        )
        
        # Restore additional metadata if present
        if 'memory_id' in data:
            chunk.memory_id = data['memory_id']
        if 'traced' in data:
            chunk.traced = data['traced']
        if 'anchor_linked' in data:
            chunk.anchor_linked = data['anchor_linked']
        
        return chunk
    
    def matches_filter(self, **filters) -> bool:
        """
        Check if this memory chunk matches the given filters.
        
        Args:
            **filters: Filter criteria (speaker, topic, has_sigil, etc.)
            
        Returns:
            bool: True if memory matches all filters
        """
        if 'speaker' in filters and self.speaker != filters['speaker']:
            return False
        
        if 'topic' in filters and self.topic != filters['topic']:
            return False
        
        if 'has_sigil' in filters and not self.has_sigil(filters['has_sigil']):
            return False
        
        if 'min_entropy' in filters and self.get_entropy() < filters['min_entropy']:
            return False
        
        if 'max_entropy' in filters and self.get_entropy() > filters['max_entropy']:
            return False
        
        if 'content_contains' in filters:
            if filters['content_contains'].lower() not in self.content.lower():
                return False
        
        if 'min_heat' in filters and self.get_heat() < filters['min_heat']:
            return False
        
        if 'max_heat' in filters and self.get_heat() > filters['max_heat']:
            return False
        
        if 'mood' in filters and self.get_mood() != filters['mood']:
            return False
        
        return True
    
    def to_memory_trace(self) -> Dict[str, Any]:
        """
        Convert to DAWN's MemoryTrace format for integration.
        
        Returns:
            dict: MemoryTrace-compatible format
        """
        return {
            'memory_id': self.memory_id,
            'timestamp': self.timestamp.timestamp(),
            'input_text': f"[{self.speaker}] {self.topic or 'memory'}",
            'response_text': self.content,
            'emotional_state': self.get_mood(),
            'consciousness_state': self.pulse_state,
            'metrics_snapshot': {
                'entropy': self.get_entropy(),
                'heat': self.get_heat(),
                'scup': self.get_scup()
            },
            'interaction_outcome': 'successful',
            'pattern_tags': self.sigils,
            'semantic_keywords': self.content.split()[:10],  # First 10 words as keywords
            'emotional_intensity': self.get_entropy(),
            'retrieval_count': 0,
            'last_retrieved': 0.0,
            'memory_strength': 1.0,
            'consolidation_level': 0
        }
    
    def __str__(self) -> str:
        """String representation of the memory chunk."""
        return f"MemoryChunk({self.summary()})"
    
    def __repr__(self) -> str:
        """Developer representation of the memory chunk."""
        return (f"MemoryChunk(memory_id='{self.memory_id}', speaker='{self.speaker}', "
                f"topic='{self.topic}', content_length={self.content_length})")


# Utility functions for memory chunk operations
def create_memory_now(speaker: str, content: str, **kwargs) -> MemoryChunk:
    """
    Create a memory chunk with current timestamp.
    
    Args:
        speaker: Identity of memory creator
        content: Memory content
        **kwargs: Additional parameters for MemoryChunk
        
    Returns:
        MemoryChunk: New memory with current timestamp
    """
    return MemoryChunk(
        timestamp=datetime.now(),
        speaker=speaker,
        content=content,
        **kwargs
    )


def memory_stats(chunks: List[MemoryChunk]) -> Dict[str, Any]:
    """
    Generate statistics for a collection of memory chunks.
    
    Args:
        chunks: List of memory chunks
        
    Returns:
        dict: Statistics about the memory collection
    """
    if not chunks:
        return {'total_memories': 0}
    
    speakers = set(chunk.speaker for chunk in chunks)
    topics = set(chunk.topic for chunk in chunks if chunk.topic)
    sigils = set(sigil for chunk in chunks for sigil in chunk.sigils)
    
    total_chars = sum(chunk.content_length for chunk in chunks)
    total_words = sum(chunk.word_count for chunk in chunks)
    
    entropies = [chunk.get_entropy() for chunk in chunks]
    avg_entropy = sum(entropies) / len(entropies) if entropies else 0
    
    heats = [chunk.get_heat() for chunk in chunks]
    avg_heat = sum(heats) / len(heats) if heats else 0
    
    return {
        'total_memories': len(chunks),
        'unique_speakers': len(speakers),
        'unique_topics': len(topics),
        'unique_sigils': len(sigils),
        'total_characters': total_chars,
        'total_words': total_words,
        'average_entropy': avg_entropy,
        'average_heat': avg_heat,
        'date_range': (min(chunk.timestamp for chunk in chunks),
                      max(chunk.timestamp for chunk in chunks)),
        'speakers': list(speakers),
        'topics': list(topics),
        'sigils': list(sigils)
    }


# Test and demonstration
if __name__ == "__main__":
    # Create test memory chunks
    chunk1 = create_memory_now(
        speaker="j.orloff",
        content="The system achieved a stable state after the entropy spike.",
        topic="introspection",
        pulse_state={"entropy": 0.47, "heat": 25.1, "scup": 0.65, "mood": "contemplative"},
        sigils=["STABILIZE_PROTOCOL"]
    )
    
    chunk2 = create_memory_now(
        speaker="dawn.core",
        content="Owl suggested stabilization protocol due to high entropy reading.",
        topic="system_event",
        pulse_state={"entropy": 0.83, "heat": 45.7, "scup": 0.42, "mood": "analytical"},
        sigils=["STABILIZE_PROTOCOL", "OWL_SUGGESTION"]
    )
    
    # Test functionality
    print("🧠 DAWN Memory Chunk Test:")
    print("=" * 40)
    
    print(f"Chunk 1: {chunk1.summary()}")
    print(f"Preview: {chunk1.get_preview(50)}")
    print(f"Has STABILIZE_PROTOCOL: {chunk1.has_sigil('STABILIZE_PROTOCOL')}")
    print(f"Memory ID: {chunk1.memory_id}")
    print()
    
    print(f"Chunk 2: {chunk2.summary()}")
    print(f"Entropy: {chunk2.get_entropy()}")
    print(f"SCUP: {chunk2.get_scup()}")
    print()
    
    # Test statistics
    chunks = [chunk1, chunk2]
    stats = memory_stats(chunks)
    print("Memory Collection Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test conversion to memory trace format
    print("\nMemory Trace Format:")
    trace = chunk1.to_memory_trace()
    print(json.dumps(trace, indent=2, default=str)) 