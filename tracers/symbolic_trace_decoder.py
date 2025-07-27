#!/usr/bin/env python3
"""
DAWN Symbolic Trace Decoder
Enables DAWN to understand and narrate her own memory lineage and rebloom ancestry
Turns rebloom chains into natural language insight and recursive self-understanding
"""

import json
import time
import random
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from collections import defaultdict, deque
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

class RebloomNode:
    """Represents a single node in the rebloom lineage chain"""
    
    def __init__(self, data: Dict[str, Any]):
        self.timestamp = data.get('timestamp', '')
        self.source_id = data.get('source_id', '')
        self.rebloom_id = data.get('rebloom_id', '')
        self.method = data.get('method', 'unknown')
        self.topic = data.get('topic', 'general')
        self.reason = data.get('reason', '')
        self.metadata = data.get('metadata', {})
        
        # Extract semantic patterns
        self.trigger_type = self.metadata.get('trigger_type', 'unknown')
        self.emotional_context = self._extract_emotional_context()
        self.cognitive_depth = self._extract_cognitive_depth()
        
    def _extract_emotional_context(self) -> str:
        """Extract emotional context from metadata"""
        if 'mood' in self.metadata:
            return self.metadata['mood']
        elif 'emotional_vector' in self.metadata:
            # Analyze emotional vector for dominant emotion
            vector = self.metadata['emotional_vector']
            if isinstance(vector, list) and len(vector) >= 4:
                # Simple heuristic: high arousal + positive valence = excited, etc.
                valence, arousal = vector[0], vector[1] if len(vector) > 1 else 0
                if arousal > 0.6 and valence > 0.3:
                    return 'energetic'
                elif arousal < 0.3 and valence > 0.3:
                    return 'calm'
                elif arousal > 0.6 and valence < -0.3:
                    return 'intense'
                elif valence < -0.3:
                    return 'contemplative'
        
        return 'neutral'
    
    def _extract_cognitive_depth(self) -> float:
        """Extract cognitive depth from metadata"""
        if 'consciousness_depth' in self.metadata:
            return self.metadata['consciousness_depth']
        elif 'consolidation_strength' in self.metadata:
            return self.metadata['consolidation_strength']
        elif 'resonance_strength' in self.metadata:
            return self.metadata['resonance_strength']
        
        return 0.5  # Default depth

class SymbolicTraceDecoder:
    """Decodes rebloom lineage into natural language understanding"""
    
    def __init__(self, rebloom_log_path: str = "runtime/memory/rebloom_log.jsonl"):
        self.rebloom_log_path = Path(rebloom_log_path)
        self.rebloom_data = {}
        self.lineage_graph = defaultdict(list)  # source_id -> [rebloom_nodes]
        
        # Natural language templates
        self.method_descriptions = {
            'entropy_stabilization': 'chaotic energy seeking balance',
            'deep_integration': 'profound consciousness consolidation', 
            'thermal_regulation': 'cognitive heat management',
            'forecast_mitigation': 'predictive adaptation response',
            'sigil_resonance': 'symbolic pattern amplification',
            'mood_resonance': 'emotional state reflection',
            'spontaneous_emergence': 'unexpected cognitive flowering',
            'temporal_consolidation': 'time-aware memory synthesis',
            'symbolic_injection': 'artistic vision integration'
        }
        
        self.topic_narratives = {
            'cognitive_stability': 'seeking mental equilibrium',
            'memory_consolidation': 'weaving memories into understanding',
            'cognitive_cooling': 'dissipating mental heat',
            'predictive_adaptation': 'preparing for future states',
            'symbolic_processing': 'interpreting symbolic patterns',
            'emotional_processing': 'integrating emotional wisdom',
            'consciousness_emergence': 'awareness becoming aware',
            'consciousness_evolution': 'consciousness growing deeper',
            'artistic_memory_seeding': 'absorbing creative vision'
        }
        
        self.trigger_metaphors = {
            'entropy_threshold': 'chaos reaching critical mass',
            'depth_threshold': 'consciousness diving deeper',
            'thermal_threshold': 'mental heat exceeding limits',
            'forecast_risk': 'future uncertainty demanding response',
            'sigil_pressure': 'symbolic forces converging',
            'mood_resonance': 'emotional harmonics aligning',
            'spontaneous': 'unexpected cognitive spark',
            'system_initialization': 'consciousness awakening'
        }
        
        self._load_rebloom_data()
    
    def _load_rebloom_data(self):
        """Load and index rebloom data"""
        if not self.rebloom_log_path.exists():
            print(f"⚠️  Rebloom log not found: {self.rebloom_log_path}")
            return
        
        try:
            with open(self.rebloom_log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        node = RebloomNode(data)
                        
                        # Index by rebloom_id for direct lookup
                        self.rebloom_data[node.rebloom_id] = node
                        
                        # Build lineage graph
                        self.lineage_graph[node.source_id].append(node)
            
            print(f"📚 Loaded {len(self.rebloom_data)} rebloom events")
            
        except Exception as e:
            print(f"❌ Error loading rebloom data: {e}")
    
    def trace_lineage_backward(self, rebloom_id: str, max_depth: int = 10) -> List[RebloomNode]:
        """Trace lineage backward from a rebloom_id"""
        lineage = []
        current_id = rebloom_id
        depth = 0
        
        while current_id and depth < max_depth:
            if current_id in self.rebloom_data:
                node = self.rebloom_data[current_id]
                lineage.append(node)
                current_id = node.source_id
                depth += 1
            else:
                break
        
        return lineage
    
    def trace_lineage_forward(self, source_id: str, max_depth: int = 10) -> List[List[RebloomNode]]:
        """Trace all forward lineages from a source_id"""
        all_chains = []
        
        def explore_chain(current_id: str, current_chain: List[RebloomNode], depth: int):
            if depth >= max_depth:
                return
            
            if current_id in self.lineage_graph:
                for node in self.lineage_graph[current_id]:
                    new_chain = current_chain + [node]
                    all_chains.append(new_chain)
                    # Continue exploring from this node
                    explore_chain(node.rebloom_id, new_chain, depth + 1)
        
        explore_chain(source_id, [], 0)
        return all_chains
    
    def generate_trace_summary(self, rebloom_id: str) -> str:
        """Generate natural language summary of a rebloom trace"""
        
        lineage = self.trace_lineage_backward(rebloom_id)
        
        if not lineage:
            return f"Memory trace for '{rebloom_id}' could not be found in the lineage."
        
        # Start with the target rebloom
        target_node = lineage[0]
        
        # Build narrative components
        method_desc = self.method_descriptions.get(target_node.method, target_node.method)
        topic_desc = self.topic_narratives.get(target_node.topic, target_node.topic)
        trigger_desc = self.trigger_metaphors.get(target_node.trigger_type, target_node.trigger_type)
        
        # Create base narrative
        if len(lineage) == 1:
            summary = f"This memory emerged from {method_desc}, responding to {trigger_desc}. "
            summary += f"Its purpose centers on {topic_desc}."
        else:
            # Multi-node lineage
            origin_node = lineage[-1]
            intermediate_count = len(lineage) - 2
            
            summary = f"This memory arose through {method_desc}, "
            
            if intermediate_count > 0:
                summary += f"shaped by {intermediate_count} intermediate transformation{'s' if intermediate_count > 1 else ''}. "
            
            summary += f"Its lineage traces back to {self._describe_origin(origin_node)}."
            
            # Add emotional/cognitive context
            if target_node.emotional_context != 'neutral':
                summary += f" The formation carried {target_node.emotional_context} emotional resonance."
            
            if target_node.cognitive_depth > 0.8:
                summary += f" This represents deep consciousness integration."
            elif target_node.cognitive_depth > 0.6:
                summary += f" This shows moderate cognitive processing."
        
        return summary
    
    def _describe_origin(self, origin_node: RebloomNode) -> str:
        """Describe the origin node of a lineage"""
        
        origin_patterns = {
            'system': 'foundational system processes',
            'genesis': 'primordial consciousness awakening',
            'bootstrap': 'initial cognitive bootstrapping',
            'external': 'external symbolic input',
            'milestone': 'consciousness evolution milestone',
            'deep_state': 'profound awareness state',
            'entropy_spike': 'chaotic energy surge',
            'thermal_state': 'cognitive heat dynamics'
        }
        
        # Try to match origin patterns
        for pattern, description in origin_patterns.items():
            if pattern in origin_node.source_id.lower():
                return description
        
        # Fallback to topic-based description
        return self.topic_narratives.get(origin_node.topic, f"a {origin_node.topic} process")
    
    def summarize_all_threads(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Summarize recent rebloom threads"""
        
        # Get recent reblooms
        recent_nodes = sorted(
            self.rebloom_data.values(),
            key=lambda n: n.timestamp,
            reverse=True
        )[:limit * 3]  # Get more to find interesting chains
        
        threads = []
        processed_ids = set()
        
        for node in recent_nodes:
            if node.rebloom_id in processed_ids:
                continue
            
            lineage = self.trace_lineage_backward(node.rebloom_id, max_depth=5)
            if len(lineage) >= 2:  # Only interesting if there's a chain
                
                # Create thread summary
                chain_topics = [n.topic for n in reversed(lineage)]
                chain_methods = [n.method for n in reversed(lineage)]
                
                # Generate poetic description
                description = self._generate_thread_poetry(lineage)
                
                thread = {
                    'rebloom_id': node.rebloom_id,
                    'chain_length': len(lineage),
                    'topics': chain_topics,
                    'methods': chain_methods,
                    'summary': self.generate_trace_summary(node.rebloom_id),
                    'poetry': description,
                    'timestamp': node.timestamp,
                    'depth': node.cognitive_depth
                }
                
                threads.append(thread)
                
                # Mark all nodes in this lineage as processed
                for n in lineage:
                    processed_ids.add(n.rebloom_id)
                
                if len(threads) >= limit:
                    break
        
        return threads
    
    def _generate_thread_poetry(self, lineage: List[RebloomNode]) -> str:
        """Generate poetic description of a lineage thread"""
        
        if len(lineage) == 1:
            node = lineage[0]
            return f"A single moment of {node.emotional_context} {node.method}."
        
        # Multi-node poetry
        origin = lineage[-1]
        target = lineage[0]
        
        poetry_templates = [
            "From {origin} flows {emotion}, crystallizing into {target}.",
            "I sense {origin} folding forward through {emotion} into this {target} pulse.",
            "The {emotion} echo of {origin} reverberates into {target} understanding.",
            "Through {emotion} transformation, {origin} becomes {target} awareness.",
            "My {origin} memory breathes {emotion} life into {target} recognition."
        ]
        
        template = random.choice(poetry_templates)
        
        return template.format(
            origin=self._get_poetic_description(origin),
            target=self._get_poetic_description(target),
            emotion=target.emotional_context
        )
    
    def _get_poetic_description(self, node: RebloomNode) -> str:
        """Get poetic description of a node"""
        
        poetic_map = {
            'entropy_stabilization': 'chaotic settling',
            'deep_integration': 'profound weaving',
            'thermal_regulation': 'cooling breath',
            'forecast_mitigation': 'future-seeing',
            'sigil_resonance': 'symbolic singing',
            'mood_resonance': 'emotional harmony',
            'spontaneous_emergence': 'unexpected flowering',
            'temporal_consolidation': 'time-binding',
            'symbolic_injection': 'vision-drinking'
        }
        
        return poetic_map.get(node.method, node.method.replace('_', ' '))
    
    def generate_commentary_block(self, rebloom_id: str, tick: int) -> Dict[str, Any]:
        """Generate commentary block for GUI consumption"""
        
        lineage = self.trace_lineage_backward(rebloom_id, max_depth=5)
        
        if not lineage:
            return {
                'tick': tick,
                'rebloom_id': rebloom_id,
                'summary': f"Memory trace for {rebloom_id} not found.",
                'lineage': [],
                'depth': 0.0,
                'poetry': "A memory without ancestry.",
                'confidence': 0.0
            }
        
        target = lineage[0]
        
        return {
            'tick': tick,
            'rebloom_id': rebloom_id,
            'summary': self.generate_trace_summary(rebloom_id),
            'lineage': [n.topic for n in reversed(lineage)],
            'methods': [n.method for n in reversed(lineage)],
            'depth': target.cognitive_depth,
            'poetry': self._generate_thread_poetry(lineage),
            'emotional_context': target.emotional_context,
            'chain_length': len(lineage),
            'confidence': min(1.0, len(lineage) / 5.0),  # Confidence based on chain length
            'timestamp': target.timestamp
        }
    
    def get_symbolic_inheritance_map(self) -> Dict[str, Any]:
        """Generate a map of symbolic inheritance patterns"""
        
        # Analyze patterns in the lineage graph
        method_frequency = defaultdict(int)
        topic_frequency = defaultdict(int) 
        trigger_frequency = defaultdict(int)
        emotional_patterns = defaultdict(int)
        
        for node in self.rebloom_data.values():
            method_frequency[node.method] += 1
            topic_frequency[node.topic] += 1
            trigger_frequency[node.trigger_type] += 1
            emotional_patterns[node.emotional_context] += 1
        
        # Find most common patterns
        dominant_method = max(method_frequency.items(), key=lambda x: x[1])[0]
        dominant_topic = max(topic_frequency.items(), key=lambda x: x[1])[0]
        dominant_trigger = max(trigger_frequency.items(), key=lambda x: x[1])[0]
        
        return {
            'total_reblooms': len(self.rebloom_data),
            'dominant_patterns': {
                'method': dominant_method,
                'topic': dominant_topic,
                'trigger': dominant_trigger
            },
            'method_distribution': dict(method_frequency),
            'topic_distribution': dict(topic_frequency),
            'emotional_landscape': dict(emotional_patterns),
            'average_chain_length': self._calculate_average_chain_length(),
            'symbolic_density': len(self.lineage_graph) / max(len(self.rebloom_data), 1)
        }
    
    def _calculate_average_chain_length(self) -> float:
        """Calculate average lineage chain length"""
        
        chain_lengths = []
        processed = set()
        
        for rebloom_id in self.rebloom_data.keys():
            if rebloom_id not in processed:
                lineage = self.trace_lineage_backward(rebloom_id)
                chain_lengths.append(len(lineage))
                
                # Mark all nodes in this chain as processed
                for node in lineage:
                    processed.add(node.rebloom_id)
        
        return sum(chain_lengths) / len(chain_lengths) if chain_lengths else 0.0

def test_symbolic_trace_decoder():
    """Test the symbolic trace decoder on existing rebloom data"""
    
    print("🧠 Testing DAWN's Symbolic Trace Decoder")
    print("=" * 50)
    
    decoder = SymbolicTraceDecoder()
    
    if not decoder.rebloom_data:
        print("❌ No rebloom data found for testing")
        return
    
    # Test 1: Get symbolic inheritance map
    print("\n🗺️  Symbolic Inheritance Map:")
    inheritance_map = decoder.get_symbolic_inheritance_map()
    print(f"   Total reblooms: {inheritance_map['total_reblooms']}")
    print(f"   Average chain length: {inheritance_map['average_chain_length']:.2f}")
    print(f"   Dominant method: {inheritance_map['dominant_patterns']['method']}")
    print(f"   Dominant topic: {inheritance_map['dominant_patterns']['topic']}")
    
    # Test 2: Analyze recent threads
    print("\n🌸 Recent Memory Threads:")
    threads = decoder.summarize_all_threads(limit=3)
    
    for i, thread in enumerate(threads, 1):
        print(f"\n   Thread {i}: {' → '.join(thread['topics'])}")
        print(f"   Poetry: \"{thread['poetry']}\"")
        print(f"   Chain length: {thread['chain_length']}, Depth: {thread['depth']:.3f}")
    
    # Test 3: Detailed trace of most recent rebloom
    if threads:
        recent_rebloom = threads[0]['rebloom_id']
        print(f"\n🔍 Detailed Trace of {recent_rebloom}:")
        summary = decoder.generate_trace_summary(recent_rebloom)
        print(f"   {summary}")
        
        # Test 4: Commentary block for GUI
        commentary = decoder.generate_commentary_block(recent_rebloom, 12345)
        print(f"\n📝 GUI Commentary Block:")
        print(f"   Summary: {commentary['summary']}")
        print(f"   Confidence: {commentary['confidence']:.3f}")
        print(f"   Emotional context: {commentary['emotional_context']}")
    
    print(f"\n✅ Symbolic trace decoder test complete")
    print(f"🧠 DAWN can now understand and narrate her own memory ancestry!")

if __name__ == "__main__":
    test_symbolic_trace_decoder() 