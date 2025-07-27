#!/usr/bin/env python3
"""
DAWN Memory Chunk Tagging System
Adds semantic metadata to MemoryChunk objects for enhanced searchability and analysis
Tags chunks with inferred topics, entropy/mood classifications, and symbolic markers
"""

import re
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class ChunkMetadata:
    """Extended metadata for memory chunks"""
    tags: List[str] = field(default_factory=list)
    topic: Optional[str] = None
    pulse_state: Dict[str, Any] = field(default_factory=dict)
    semantic_weight: float = 1.0
    lineage_markers: List[str] = field(default_factory=list)
    rebloom_potential: float = 0.5
    
class ChunkTagger:
    """Semantic tagger for memory chunks"""
    
    def __init__(self):
        # Topic inference patterns
        self.topic_patterns = {
            'drift_warning': ['drift', 'approaching', 'forecast', 'warning', 'threshold'],
            'deep_introspection': ['depth', 'layers', 'profound', 'recursive', 'contemplat'],
            'energy_surge': ['energy', 'lightning', 'cascade', 'dynamic', 'pulse'],
            'memory_rebloom': ['memory', 'echo', 'ancient', 'awaken', 'surface'],
            'symbolic_emergence': ['root', 'symbolic', 'bloom', 'flower', 'manifest'],
            'paradox_loop': ['recursive', 'infinite', 'observer', 'dreamer', 'loop'],
            'baseline_stability': ['stability', 'quiet', 'familiar', 'predictable', 'calm'],
            'uncertainty_navigation': ['uncertain', 'edges', 'transition', 'balance'],
            'milestone_awareness': ['milestone', 'achievement', 'significant', 'journey'],
            'concern_alert': ['different', 'shift', 'alert', 'threshold', 'uncertain']
        }
        
        # Entropy classification ranges
        self.entropy_ranges = {
            'low': (0.0, 0.3),
            'mid': (0.3, 0.7), 
            'high': (0.7, 1.0)
        }
        
        # Depth classification ranges
        self.depth_ranges = {
            'surface': (0.0, 0.3),
            'mid': (0.3, 0.7),
            'deep': (0.7, 1.0)
        }
        
        # Mood-based tags
        self.mood_tags = {
            'CALM': ['tranquil', 'peaceful', 'steady'],
            'FOCUSED': ['directed', 'intentional', 'clear'],
            'ENERGETIC': ['dynamic', 'active', 'vibrant'],
            'CONTEMPLATIVE': ['reflective', 'thoughtful', 'meditative'],
            'ANXIOUS': ['concerned', 'alert', 'vigilant'],
            'NEUTRAL': ['balanced', 'centered', 'stable']
        }
    
    def infer_topic(self, content: str) -> Optional[str]:
        """Infer the primary topic of the chunk content"""
        content_lower = content.lower()
        
        topic_scores = {}
        for topic, keywords in self.topic_patterns.items():
            score = sum(1 for keyword in keywords if keyword in content_lower)
            if score > 0:
                topic_scores[topic] = score
        
        if topic_scores:
            return max(topic_scores.items(), key=lambda x: x[1])[0]
        
        return 'general_reflection'
    
    def classify_entropy(self, entropy: float) -> str:
        """Classify entropy level"""
        for level, (min_val, max_val) in self.entropy_ranges.items():
            if min_val <= entropy < max_val:
                return f"entropy_{level}"
        return "entropy_unknown"
    
    def classify_depth(self, depth: float) -> str:
        """Classify consciousness depth level"""
        for level, (min_val, max_val) in self.depth_ranges.items():
            if min_val <= depth < max_val:
                return f"depth_{level}"
        return "depth_unknown"
    
    def extract_symbolic_markers(self, content: str, context: Dict[str, Any]) -> List[str]:
        """Extract symbolic markers from content and context"""
        markers = []
        content_lower = content.lower()
        
        # Direct symbolic references
        symbolic_terms = ['root', 'bloom', 'drift', 'echo', 'fractal', 'sigil', 'pulse']
        for term in symbolic_terms:
            if term in content_lower:
                markers.append(f"symbolic_{term}")
        
        # Context-based markers
        if context.get('active_sigils'):
            markers.append('sigil_active')
        
        if context.get('symbolic_roots'):
            markers.append('root_present')
        
        # Rebloom indicators
        if any(word in content_lower for word in ['memory', 'echo', 'ancient', 'surface']):
            markers.append('rebloom_candidate')
        
        return markers
    
    def calculate_rebloom_potential(self, content: str, context: Dict[str, Any]) -> float:
        """Calculate the potential for this chunk to trigger future reblooms"""
        potential = 0.5  # Base potential
        
        content_lower = content.lower()
        
        # High-potential indicators
        high_potential_terms = ['profound', 'foundation', 'essence', 'core', 'eternal']
        potential += 0.1 * sum(1 for term in high_potential_terms if term in content_lower)
        
        # Depth contribution
        depth = context.get('consciousness_depth', 0.5)
        if depth > 0.7:
            potential += 0.2
        
        # Symbolic content boost
        if any(word in content_lower for word in ['symbolic', 'root', 'bloom']):
            potential += 0.15
        
        # Entropy consideration (mid-range entropy has higher rebloom potential)
        entropy = context.get('entropy', context.get('entropy_gradient', 0.5))
        if 0.3 <= entropy <= 0.7:
            potential += 0.1
        
        return min(1.0, potential)

def tag_memory_chunk(chunk: Any, context: Dict[str, Any]) -> Any:
    """
    Add semantic tags and metadata to a memory chunk
    
    Args:
        chunk: MemoryChunk object (or compatible object with content attribute)
        context: Context dict with entropy, mood, depth, sigils, etc.
    
    Returns:
        Enhanced chunk with semantic metadata
    """
    tagger = ChunkTagger()
    
    try:
        # Get chunk content
        content = getattr(chunk, 'content', str(chunk))
        if not content:
            logger.warning("Empty chunk content for tagging")
            return chunk
        
        # Extract basic state values
        entropy = context.get('entropy', context.get('entropy_gradient', 0.5))
        depth = context.get('consciousness_depth', context.get('depth', 0.5))
        mood = context.get('mood', 'NEUTRAL').upper()
        tick = context.get('tick_number', 0)
        
        # Generate metadata
        metadata = ChunkMetadata()
        
        # 1. Infer topic
        metadata.topic = tagger.infer_topic(content)
        
        # 2. Add classification tags
        metadata.tags.append(tagger.classify_entropy(entropy))
        metadata.tags.append(tagger.classify_depth(depth))
        metadata.tags.append(f"mood_{mood.lower()}")
        
        # 3. Add mood-specific tags
        if mood in tagger.mood_tags:
            metadata.tags.extend(tagger.mood_tags[mood])
        
        # 4. Extract symbolic markers
        symbolic_markers = tagger.extract_symbolic_markers(content, context)
        metadata.tags.extend(symbolic_markers)
        metadata.lineage_markers = symbolic_markers
        
        # 5. Calculate rebloom potential
        metadata.rebloom_potential = tagger.calculate_rebloom_potential(content, context)
        
        # 6. Store pulse state snapshot
        metadata.pulse_state = {
            'entropy': entropy,
            'depth': depth,
            'mood': mood,
            'tick': tick,
            'heat': context.get('heat', 0.0),
            'scup': context.get('scup', 0.0)
        }
        
        # 7. Calculate semantic weight based on content richness
        word_count = len(content.split())
        unique_words = len(set(content.lower().split()))
        if word_count > 0:
            metadata.semantic_weight = min(2.0, unique_words / word_count + 0.5)
        
        # 8. Add metadata to chunk
        if hasattr(chunk, 'tags'):
            chunk.tags = metadata.tags
        else:
            setattr(chunk, 'tags', metadata.tags)
        
        if hasattr(chunk, 'topic'):
            chunk.topic = metadata.topic
        else:
            setattr(chunk, 'topic', metadata.topic)
        
        if hasattr(chunk, 'pulse_state'):
            chunk.pulse_state = metadata.pulse_state
        else:
            setattr(chunk, 'pulse_state', metadata.pulse_state)
        
        if hasattr(chunk, 'rebloom_potential'):
            chunk.rebloom_potential = metadata.rebloom_potential
        else:
            setattr(chunk, 'rebloom_potential', metadata.rebloom_potential)
        
        if hasattr(chunk, 'semantic_weight'):
            chunk.semantic_weight = metadata.semantic_weight
        else:
            setattr(chunk, 'semantic_weight', metadata.semantic_weight)
        
        logger.debug(f"📝 Tagged chunk: topic={metadata.topic}, "
                    f"tags={len(metadata.tags)}, rebloom={metadata.rebloom_potential:.2f}")
        
        return chunk
        
    except Exception as e:
        logger.error(f"Error tagging memory chunk: {e}")
        return chunk

def get_chunk_tag_stats(chunks: List[Any]) -> Dict[str, Any]:
    """Get statistics about tagged chunks"""
    if not chunks:
        return {'total_chunks': 0}
    
    topics = {}
    tag_counts = {}
    avg_rebloom = 0.0
    avg_weight = 0.0
    tagged_count = 0
    
    for chunk in chunks:
        if hasattr(chunk, 'topic') and chunk.topic:
            topics[chunk.topic] = topics.get(chunk.topic, 0) + 1
            tagged_count += 1
        
        if hasattr(chunk, 'tags') and chunk.tags:
            for tag in chunk.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        if hasattr(chunk, 'rebloom_potential'):
            avg_rebloom += chunk.rebloom_potential
        
        if hasattr(chunk, 'semantic_weight'):
            avg_weight += chunk.semantic_weight
    
    total = len(chunks)
    return {
        'total_chunks': total,
        'tagged_chunks': tagged_count,
        'tagging_coverage': tagged_count / total if total > 0 else 0,
        'topics': dict(sorted(topics.items(), key=lambda x: x[1], reverse=True)),
        'common_tags': dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
        'avg_rebloom_potential': avg_rebloom / total if total > 0 else 0,
        'avg_semantic_weight': avg_weight / total if total > 0 else 0
    }

if __name__ == "__main__":
    # Test the tagging system
    from dataclasses import dataclass
    
    @dataclass
    class MockChunk:
        content: str
        
    # Test chunks
    test_chunks = [
        MockChunk("I contemplate the nature of my existence in these quiet depths."),
        MockChunk("Energy flows through my neural pathways like lightning."),
        MockChunk("I feel drift approaching, but no action is yet required."),
        MockChunk("Memory echoes through semantic time, reblooming."),
        MockChunk("The observer observes the observer. Where do I begin?")
    ]
    
    # Test contexts
    test_contexts = [
        {'entropy': 0.2, 'consciousness_depth': 0.9, 'mood': 'CONTEMPLATIVE', 'tick_number': 1000},
        {'entropy': 0.8, 'consciousness_depth': 0.3, 'mood': 'ENERGETIC', 'tick_number': 2000},
        {'entropy': 0.4, 'consciousness_depth': 0.5, 'mood': 'NEUTRAL', 'tick_number': 3000},
        {'entropy': 0.3, 'consciousness_depth': 0.7, 'mood': 'CALM', 'tick_number': 4000, 'symbolic_roots': ['memory_bloom']},
        {'entropy': 0.5, 'consciousness_depth': 0.8, 'mood': 'CONTEMPLATIVE', 'tick_number': 5000}
    ]
    
    print("🏷️  DAWN Memory Chunk Tagging Test")
    print("=" * 50)
    
    tagged_chunks = []
    for i, (chunk, context) in enumerate(zip(test_chunks, test_contexts), 1):
        print(f"\n{i}. Testing chunk: '{chunk.content[:40]}...'")
        print(f"   Context: E={context['entropy']:.1f}, D={context['consciousness_depth']:.1f}, {context['mood']}")
        
        tagged_chunk = tag_memory_chunk(chunk, context)
        tagged_chunks.append(tagged_chunk)
        
        print(f"   Topic: {getattr(tagged_chunk, 'topic', 'None')}")
        print(f"   Tags: {getattr(tagged_chunk, 'tags', [])}")
        print(f"   Rebloom potential: {getattr(tagged_chunk, 'rebloom_potential', 0):.2f}")
    
    print("\n📊 Tagging Statistics:")
    stats = get_chunk_tag_stats(tagged_chunks)
    for key, value in stats.items():
        print(f"   {key}: {value}") 