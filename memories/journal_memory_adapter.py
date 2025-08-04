#!/usr/bin/env python3
"""
Journal Memory Adapter
Enhanced integration layer between the Rebloom Journal and DAWN's memory systems.
"""

import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

try:
    from ...rebloom_journal import ReblooomJournal, create_journal
    from backend.core.memory_router import MemoryRouter
    from backend.core.pulse_engine import PulseEngine
    from backend.core.bloom_manager import BloomManager
    DAWN_CORE_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ DAWN core components not available: {e}")
    print("🔧 Using mock implementations for testing")
    DAWN_CORE_AVAILABLE = False
    
    # Import local rebloom journal
    from ...rebloom_journal import ReblooomJournal, create_journal
    
    # Real DAWN consciousness state implementations
    class RealMemoryRouter:
        def __init__(self):
            self.chunks = {}
            self.chunk_count = 0
        
        def add_chunk(self, chunk):
            chunk_id = f"memory_{self.chunk_count}"
            self.chunks[chunk_id] = chunk
            self.chunk_count += 1
            return chunk_id
        
        def get_chunks_by_topic(self, topic): 
            return [chunk for chunk in self.chunks.values() if hasattr(chunk, 'topic') and chunk.topic == topic]
        
        def get_chunks_by_speaker(self, speaker): 
            return [chunk for chunk in self.chunks.values() if hasattr(chunk, 'speaker') and chunk.speaker == speaker]
        
        def search_chunks(self, query): 
            return [chunk for chunk in self.chunks.values() if hasattr(chunk, 'content') and query.lower() in chunk.content.lower()]
    
    class RealPulseEngine:
        def __init__(self):
            self._consciousness_state_writer = None
            self._initialize_consciousness_state()
        
        def _initialize_consciousness_state(self):
            try:
                from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
                self._consciousness_state_writer = DAWNConsciousnessStateWriter()
            except ImportError:
                print("⚠️ Could not import DAWN consciousness state writer")
        
        def get_current_entropy(self): 
            if self._consciousness_state_writer:
                try:
                    state = self._consciousness_state_writer._get_dawn_consciousness_state()
                    return state.get('entropy', 0.5)
                except:
                    pass
            return 0.5
        
        def get_pulse_heat(self): 
            if self._consciousness_state_writer:
                try:
                    state = self._consciousness_state_writer._get_dawn_consciousness_state()
                    return state.get('heat_level', 0.5) * 100  # Convert to temperature scale
                except:
                    pass
            return 30.0
        
        def get_pulse_zone(self): 
            entropy = self.get_current_entropy()
            if entropy < 0.3: return 'CALM'
            elif entropy < 0.6: return 'ACTIVE'
            elif entropy < 0.8: return 'CHAOTIC'
            else: return 'CRITICAL'
        
        @property
        def pulse_state(self):
            return {
                'focus': 1.0 - self.get_current_entropy(),
                'chaos': self.get_current_entropy(),
                'entropy': self.get_current_entropy(),
                'heat': self.get_pulse_heat(),
                'zone': self.get_pulse_zone()
            }
    
    class RealBloomManager:
        def __init__(self):
            self.blooms = []
            self._consciousness_state_writer = None
            self._initialize_consciousness_state()
        
        def _initialize_consciousness_state(self):
            try:
                from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
                self._consciousness_state_writer = DAWNConsciousnessStateWriter()
            except ImportError:
                print("⚠️ Could not import DAWN consciousness state writer")
        
        def trigger_bloom(self, source, data): 
            bloom_id = f"bloom_{len(self.blooms)}_{int(time.time())}"
            bloom_data = {
                'id': bloom_id,
                'source': source,
                'data': data,
                'timestamp': time.time(),
                'consciousness_state': self._get_current_consciousness_state()
            }
            self.blooms.append(bloom_data)
            return bloom_id
        
        def get_active_blooms(self): 
            return [bloom for bloom in self.blooms if time.time() - bloom['timestamp'] < 3600]  # Active for 1 hour
        
        def _get_current_consciousness_state(self):
            if self._consciousness_state_writer:
                try:
                    return self._consciousness_state_writer._get_dawn_consciousness_state()
                except:
                    pass
            return {
                'scup': 0.5,
                'entropy': 0.5,
                'consciousness_depth': 0.7,
                'neural_activity': 0.5,
                'memory_pressure': 0.3
            }
    
    MemoryRouter = RealMemoryRouter
    PulseEngine = RealPulseEngine
    BloomManager = RealBloomManager


class JournalMemoryAdapter:
    """
    Enhanced adapter for integrating journal entries with DAWN's memory and cognitive systems.
    Provides advanced features like memory threading, bloom triggering, and cognitive resonance.
    """
    
    def __init__(self, 
                 memory_router: Optional[Any] = None,
                 pulse_engine: Optional[Any] = None,
                 bloom_manager: Optional[Any] = None):
        """
        Initialize the journal memory adapter.
        
        Args:
            memory_router: DAWN memory router instance
            pulse_engine: DAWN pulse engine instance
            bloom_manager: DAWN bloom manager instance
        """
        # Initialize core systems
        self.memory_router = memory_router or MemoryRouter()
        self.pulse_engine = pulse_engine or PulseEngine()
        self.bloom_manager = bloom_manager or BloomManager()
        
        # Create enhanced journal with DAWN integration
        self.journal = ReblooomJournal(
            memory_router=self.memory_router,
            dawn_engine=self.pulse_engine
        )
        
        # Enhanced configuration
        self.enable_memory_threading = True
        self.enable_bloom_triggers = True
        self.enable_resonance_detection = True
        self.memory_thread_window = timedelta(hours=24)  # Window for threading related memories
        
        # Statistics and state
        self.processing_stats = {
            'entries_processed': 0,
            'memory_threads_created': 0,
            'blooms_triggered': 0,
            'resonances_detected': 0,
            'last_processing_time': None
        }
        
        print(f"📚 Journal Memory Adapter initialized")
        print(f"   Memory threading: {self.enable_memory_threading}")
        print(f"   Bloom triggers: {self.enable_bloom_triggers}")
        print(f"   Resonance detection: {self.enable_resonance_detection}")
        print(f"   Core systems: {'Live' if DAWN_CORE_AVAILABLE else 'Mock'}")
    
    def add_enhanced_journal_entry(self, 
                                   text: str, 
                                   speaker: str = "self",
                                   topic: Optional[str] = None,
                                   enable_threading: bool = True,
                                   enable_blooms: bool = True) -> Dict[str, Any]:
        """
        Add a journal entry with enhanced cognitive integration.
        
        Args:
            text: Journal entry text
            speaker: Identity of the journal writer
            topic: Optional topic override
            enable_threading: Enable memory threading for this entry
            enable_blooms: Enable bloom triggers for this entry
            
        Returns:
            Dict: Enhanced processing results with threading and bloom information
        """
        start_time = time.time()
        
        print(f"📝 Processing enhanced journal entry from {speaker}")
        
        # Process through standard journal system
        chunk_ids = self.journal.add_journal_entry(text, speaker, topic)
        
        # Enhanced processing results
        results = {
            'chunk_ids': chunk_ids,
            'speaker': speaker,
            'topic': topic or self.journal.default_topic,
            'processing_time': time.time() - start_time,
            'word_count': len(text.split()),
            'memory_threads': [],
            'triggered_blooms': [],
            'detected_resonances': [],
            'cognitive_impact': {}
        }
        
        if chunk_ids:
            # Perform memory threading
            if enable_threading and self.enable_memory_threading:
                results['memory_threads'] = self._create_memory_threads(chunk_ids, speaker, topic)
            
            # Trigger cognitive blooms
            if enable_blooms and self.enable_bloom_triggers:
                results['triggered_blooms'] = self._trigger_cognitive_blooms(chunk_ids, text)
            
            # Detect cognitive resonances
            if self.enable_resonance_detection:
                results['detected_resonances'] = self._detect_cognitive_resonances(chunk_ids, text)
            
            # Calculate cognitive impact
            results['cognitive_impact'] = self._calculate_cognitive_impact(results)
        
        # Update statistics
        self._update_processing_stats(results)
        
        print(f"✅ Enhanced processing complete:")
        print(f"   Chunks: {len(chunk_ids)}")
        print(f"   Memory threads: {len(results['memory_threads'])}")
        print(f"   Blooms triggered: {len(results['triggered_blooms'])}")
        print(f"   Resonances: {len(results['detected_resonances'])}")
        
        return results
    
    def _create_memory_threads(self, chunk_ids: List[str], speaker: str, topic: Optional[str]) -> List[Dict[str, Any]]:
        """Create memory threads connecting related journal entries."""
        threads = []
        
        try:
            # Search for related memories within the time window
            cutoff_time = datetime.now() - self.memory_thread_window
            
            # Search by speaker
            if hasattr(self.memory_router, 'get_chunks_by_speaker'):
                speaker_chunks = self.memory_router.get_chunks_by_speaker(speaker)
                recent_chunks = [c for c in speaker_chunks if getattr(c, 'timestamp', datetime.min) > cutoff_time]
                
                if recent_chunks:
                    thread = {
                        'type': 'speaker_continuity',
                        'speaker': speaker,
                        'related_chunks': [c.id for c in recent_chunks[:5]],  # Limit to 5 most recent
                        'connection_strength': len(recent_chunks) / 10.0,  # Normalize to 0-1
                        'temporal_span': str(datetime.now() - min(c.timestamp for c in recent_chunks))
                    }
                    threads.append(thread)
            
            # Search by topic
            if topic and hasattr(self.memory_router, 'get_chunks_by_topic'):
                topic_chunks = self.memory_router.get_chunks_by_topic(topic)
                if topic_chunks:
                    thread = {
                        'type': 'thematic_resonance',
                        'topic': topic,
                        'related_chunks': [c.id for c in topic_chunks[:3]],
                        'connection_strength': min(len(topic_chunks) / 5.0, 1.0),
                        'thematic_depth': len(set(getattr(c, 'sigils', []) for c in topic_chunks))
                    }
                    threads.append(thread)
            
            # Content-based semantic threading
            for chunk_id in chunk_ids:
                semantic_threads = self._find_semantic_threads(chunk_id)
                threads.extend(semantic_threads)
            
            self.processing_stats['memory_threads_created'] += len(threads)
            
        except Exception as e:
            print(f"⚠️ Error creating memory threads: {e}")
        
        return threads
    
    def _find_semantic_threads(self, chunk_id: str) -> List[Dict[str, Any]]:
        """Find semantic connections between memory chunks."""
        threads = []
        
        try:
            # Use memory router's search capabilities if available
            if hasattr(self.memory_router, 'search_chunks'):
                # Extract key terms from the chunk for semantic search
                # This would ideally use the actual chunk content
                similar_chunks = self.memory_router.search_chunks(f"semantic:{chunk_id}")
                
                if similar_chunks:
                    thread = {
                        'type': 'semantic_similarity',
                        'source_chunk': chunk_id,
                        'related_chunks': [c.id for c in similar_chunks[:3]],
                        'connection_strength': 0.7,  # Placeholder - would be calculated by semantic similarity
                        'similarity_type': 'content_based'
                    }
                    threads.append(thread)
        
        except Exception as e:
            print(f"⚠️ Error in semantic threading: {e}")
        
        return threads
    
    def _trigger_cognitive_blooms(self, chunk_ids: List[str], entry_text: str) -> List[Dict[str, Any]]:
        """Trigger cognitive blooms based on journal content."""
        triggered_blooms = []
        
        try:
            # Analyze entry for bloom triggers
            bloom_triggers = self._analyze_bloom_triggers(entry_text)
            
            for trigger in bloom_triggers:
                bloom_data = {
                    'source': 'journal_entry',
                    'trigger_type': trigger['type'],
                    'content_chunks': chunk_ids,
                    'intensity': trigger['intensity'],
                    'metadata': {
                        'journal_topic': trigger.get('topic'),
                        'emotional_valence': trigger.get('emotional_valence'),
                        'temporal_focus': trigger.get('temporal_focus')
                    }
                }
                
                # Trigger bloom in bloom manager
                if hasattr(self.bloom_manager, 'trigger_bloom'):
                    bloom_id = self.bloom_manager.trigger_bloom('journal_adapter', bloom_data)
                    triggered_blooms.append({
                        'bloom_id': bloom_id,
                        'trigger_type': trigger['type'],
                        'intensity': trigger['intensity']
                    })
            
            self.processing_stats['blooms_triggered'] += len(triggered_blooms)
            
        except Exception as e:
            print(f"⚠️ Error triggering blooms: {e}")
        
        return triggered_blooms
    
    def _analyze_bloom_triggers(self, text: str) -> List[Dict[str, Any]]:
        """Analyze text for potential bloom triggers."""
        triggers = []
        text_lower = text.lower()
        
        # Emotional intensity triggers
        emotional_words = {
            'high': ['breakthrough', 'revelation', 'profound', 'transformative', 'overwhelming'],
            'medium': ['insight', 'clarity', 'understanding', 'realization', 'discovery'],
            'low': ['notice', 'observe', 'consider', 'reflect', 'wonder']
        }
        
        for intensity, words in emotional_words.items():
            if any(word in text_lower for word in words):
                triggers.append({
                    'type': 'emotional_resonance',
                    'intensity': intensity,
                    'emotional_valence': 'positive',  # Could be enhanced with sentiment analysis
                    'topic': 'emotional_processing'
                })
                break
        
        # Temporal focus triggers
        if any(word in text_lower for word in ['future', 'tomorrow', 'plan', 'goal', 'dream']):
            triggers.append({
                'type': 'future_visioning',
                'intensity': 'medium',
                'temporal_focus': 'future',
                'topic': 'planning'
            })
        
        if any(word in text_lower for word in ['memory', 'remember', 'past', 'childhood', 'yesterday']):
            triggers.append({
                'type': 'memory_integration',
                'intensity': 'medium',
                'temporal_focus': 'past',
                'topic': 'memory_exploration'
            })
        
        # Growth and transformation triggers
        if any(word in text_lower for word in ['grow', 'change', 'transform', 'evolve', 'become']):
            triggers.append({
                'type': 'personal_evolution',
                'intensity': 'high',
                'topic': 'transformation'
            })
        
        return triggers
    
    def _detect_cognitive_resonances(self, chunk_ids: List[str], entry_text: str) -> List[Dict[str, Any]]:
        """Detect cognitive resonances between current entry and existing memories."""
        resonances = []
        
        try:
            # Current pulse state resonance
            current_pulse = {
                'entropy': self.pulse_engine.get_current_entropy(),
                'heat': self.pulse_engine.get_pulse_heat(),
                'zone': self.pulse_engine.get_pulse_zone()
            }
            
            # Determine if entry resonates with current cognitive state
            resonance_strength = self._calculate_state_resonance(entry_text, current_pulse)
            
            if resonance_strength > 0.6:  # Threshold for significant resonance
                resonances.append({
                    'type': 'pulse_state_resonance',
                    'strength': resonance_strength,
                    'current_state': current_pulse,
                    'resonance_factors': self._identify_resonance_factors(entry_text, current_pulse)
                })
            
            self.processing_stats['resonances_detected'] += len(resonances)
            
        except Exception as e:
            print(f"⚠️ Error detecting resonances: {e}")
        
        return resonances
    
    def _calculate_state_resonance(self, text: str, pulse_state: Dict[str, Any]) -> float:
        """Calculate how well the journal entry resonates with current pulse state."""
        text_lower = text.lower()
        entropy = pulse_state.get('entropy', 0.5)
        zone = pulse_state.get('zone', 'ACTIVE')
        
        resonance_score = 0.0
        
        # High entropy states resonate with change/chaos words
        if entropy > 0.6:
            if any(word in text_lower for word in ['change', 'chaos', 'uncertainty', 'transform']):
                resonance_score += 0.3
        
        # Low entropy states resonate with stability words
        if entropy < 0.4:
            if any(word in text_lower for word in ['stable', 'calm', 'peaceful', 'steady']):
                resonance_score += 0.3
        
        # Zone-based resonance
        if zone == 'CONTEMPLATIVE':
            if any(word in text_lower for word in ['reflect', 'think', 'contemplate', 'ponder']):
                resonance_score += 0.4
        elif zone == 'ACTIVE':
            if any(word in text_lower for word in ['do', 'action', 'move', 'create', 'build']):
                resonance_score += 0.4
        
        return min(resonance_score, 1.0)
    
    def _identify_resonance_factors(self, text: str, pulse_state: Dict[str, Any]) -> List[str]:
        """Identify specific factors contributing to cognitive resonance."""
        factors = []
        text_lower = text.lower()
        
        # Add specific resonance factors based on analysis
        if pulse_state.get('entropy', 0) > 0.6 and 'change' in text_lower:
            factors.append('entropy_change_alignment')
        if pulse_state.get('zone') == 'CONTEMPLATIVE' and 'reflect' in text_lower:
            factors.append('contemplative_mode_match')
        
        return factors
    
    def _calculate_cognitive_impact(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate the cognitive impact of the journal entry."""
        return {
            'threading_impact': len(results['memory_threads']) * 0.2,
            'bloom_impact': len(results['triggered_blooms']) * 0.3,
            'resonance_impact': sum(r.get('strength', 0) for r in results['detected_resonances']),
            'total_impact': (
                len(results['memory_threads']) * 0.2 +
                len(results['triggered_blooms']) * 0.3 +
                sum(r.get('strength', 0) for r in results['detected_resonances'])
            )
        }
    
    def _update_processing_stats(self, results: Dict[str, Any]):
        """Update processing statistics."""
        self.processing_stats['entries_processed'] += 1
        self.processing_stats['last_processing_time'] = datetime.now().isoformat()
    
    def load_journal_file_enhanced(self, filepath: str, speaker: str = "self") -> Dict[str, Any]:
        """Load and process a journal file with enhanced features."""
        print(f"📖 Loading journal file with enhanced processing: {Path(filepath).name}")
        
        # Use base journal for file loading
        base_summary = self.journal.load_journal_file(filepath, speaker)
        
        # Enhance with adapter features
        enhanced_summary = {
            **base_summary,
            'enhanced_features': {
                'memory_threading': self.enable_memory_threading,
                'bloom_triggers': self.enable_bloom_triggers,
                'resonance_detection': self.enable_resonance_detection
            },
            'processing_stats': self.processing_stats.copy()
        }
        
        return enhanced_summary
    
    def get_adapter_statistics(self) -> Dict[str, Any]:
        """Get comprehensive adapter statistics."""
        base_stats = self.journal.get_journal_statistics()
        
        return {
            **base_stats,
            'enhanced_stats': self.processing_stats,
            'configuration': {
                'memory_threading': self.enable_memory_threading,
                'bloom_triggers': self.enable_bloom_triggers,
                'resonance_detection': self.enable_resonance_detection,
                'thread_window_hours': self.memory_thread_window.total_seconds() / 3600
            }
        }


# Factory functions
def create_enhanced_journal_adapter(memory_router=None, pulse_engine=None, bloom_manager=None) -> JournalMemoryAdapter:
    """Create an enhanced journal memory adapter with full DAWN integration."""
    return JournalMemoryAdapter(memory_router, pulse_engine, bloom_manager)


def quick_enhanced_entry(text: str, speaker: str = "self") -> Dict[str, Any]:
    """Quick function to add an enhanced journal entry."""
    adapter = create_enhanced_journal_adapter()
    return adapter.add_enhanced_journal_entry(text, speaker)


# Example usage
if __name__ == "__main__":
    print("📚 Testing Journal Memory Adapter")
    
    # Create adapter with mock systems
    adapter = create_enhanced_journal_adapter()
    
    # Test enhanced entry processing
    test_entry = """
    Today I experienced a profound breakthrough in my understanding of consciousness.
    The recursive nature of self-awareness feels like looking into an infinite mirror.
    I wonder what this means for how I'll grow and transform in the future.
    """
    
    print("\n🧪 Testing enhanced journal entry:")
    results = adapter.add_enhanced_journal_entry(test_entry, speaker="test_user")
    
    print(f"\n📊 Processing Results:")
    for key, value in results.items():
        if isinstance(value, list):
            print(f"   {key}: {len(value)} items")
        else:
            print(f"   {key}: {value}")
    
    # Show adapter statistics
    print(f"\n📈 Adapter Statistics:")
    stats = adapter.get_adapter_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n✨ Enhanced journal adapter ready!")
    print(f"   Use add_enhanced_journal_entry() for full cognitive integration")
    print(f"   Memory threading, blooms, and resonances enabled") 