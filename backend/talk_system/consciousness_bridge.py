from typing import Dict, Optional, List
import asyncio
import time
from .sentence_encoder import DAWNSentenceEncoder
from .semantic_memory import SemanticMemory
from .resonance_tracker import ResonanceTracker
from .controlled_generation import ControlledGenerationEngine
import json

class DAWNTalkSystem:
    """
    Main bridge between DAWN's consciousness and the talk system.
    Integrates controlled generation with the tick loop.
    """
    
    def __init__(self, 
                 memory_bank_path: str = "backend/embeddings/memory_bank.json",
                 resonance_state_path: str = "backend/embeddings/resonance_state.pkl"):
        
        # Initialize core components
        self.encoder = DAWNSentenceEncoder()
        self.semantic_memory = SemanticMemory()
        self.resonance_tracker = ResonanceTracker()
        self.generation_engine = ControlledGenerationEngine(
            self.encoder, 
            self.semantic_memory, 
            self.resonance_tracker
        )
        
        # State tracking
        self.current_interaction = None
        self.pending_responses = []
        self.response_queue = asyncio.Queue()
        
        # Configuration
        self.memory_bank_path = memory_bank_path
        self.resonance_state_path = resonance_state_path
        self.generation_enabled = True
        
        # Initialize memory and state
        self._load_memory_bank()
        self.resonance_tracker.load_state(resonance_state_path)
        
    def _load_memory_bank(self):
        """Load the initial memory bank into semantic memory"""
        try:
            with open(self.memory_bank_path, 'r') as f:
                memory_bank = json.load(f)
                
            for i, response_data in enumerate(memory_bank['responses']):
                # Encode the response text
                embedding = self.encoder.encode(response_data['text'])
                
                # Add to semantic memory with metadata
                self.semantic_memory.add_memory(
                    embedding,
                    response_data['text'],
                    {
                        'id': f"base_{i}",
                        'type': response_data['type'],
                        'mood_affinity': response_data['mood_affinity'],
                        'valence': response_data['valence'],
                        'tone': response_data['tone'],
                        'modules': response_data['modules'],
                        'rarity': response_data['rarity'],
                        'tags': response_data['tags']
                    }
                )
                
            print(f"Loaded {len(memory_bank['responses'])} responses into semantic memory")
            
        except FileNotFoundError:
            print(f"Memory bank not found at {self.memory_bank_path}")
        except Exception as e:
            print(f"Error loading memory bank: {e}")
    
    async def process_user_input(self, 
                               user_input: str, 
                               consciousness_state: Dict) -> Optional[Dict]:
        """
        Process user input and generate consciousness-driven response
        """
        
        if not user_input.strip():
            return None
            
        # Record the interaction start
        user_embedding = self.encoder.encode(user_input)
        
        # Generate response using controlled generation
        response_data = self.generation_engine.generate_consciousness_response(
            user_input,
            consciousness_state,
            use_generation=self.generation_enabled
        )
        
        if not response_data:
            return None
            
        # Record interaction for resonance tracking
        interaction = self.resonance_tracker.record_interaction(
            user_input,
            user_embedding,
            response_data['response'],
            response_data.get('response_id', 'generated'),
            consciousness_state
        )
        
        self.current_interaction = len(self.resonance_tracker.interactions) - 1
        
        # Prepare response for broadcast
        final_response = {
            'text': response_data['response'],
            'method': response_data['method'],
            'confidence': self._calculate_confidence(response_data),
            'consciousness_influence': {
                'scup': consciousness_state.get('scup', 50),
                'entropy': consciousness_state.get('entropy', 0),
                'mood': consciousness_state.get('mood', 'NEUTRAL'),
                'tick': consciousness_state.get('tick', 0)
            },
            'metadata': {
                'candidates_considered': response_data.get('candidates_considered', 1),
                'generation_enabled': self.generation_enabled,
                'timestamp': time.time()
            }
        }
        
        return final_response
    
    def update_interaction_resonance(self, 
                                   pause_duration: float = 0.0,
                                   follow_up: bool = False,
                                   sentiment_shift: str = "neutral"):
        """Update the current interaction with resonance feedback"""
        
        if self.current_interaction is not None:
            self.resonance_tracker.update_resonance(
                self.current_interaction,
                pause_duration,
                follow_up,
                sentiment_shift
            )
            
            # Save state periodically
            if len(self.resonance_tracker.interactions) % 10 == 0:
                self.resonance_tracker.save_state(self.resonance_state_path)
    
    def tick_process(self, tick_number: int, consciousness_state: Dict):
        """
        Process any pending talk operations on each consciousness tick
        """
        
        # Update active glyphs based on consciousness state
        self._update_active_concepts(consciousness_state)
        
        # Process any crystallized echoes
        new_echoes = self.resonance_tracker.get_crystallized_echoes()
        if new_echoes:
            self._integrate_crystallized_echoes(new_echoes)
        
        # Decay old memories (subtle evolution)
        if tick_number % 1000 == 0:  # Every 1000 ticks
            self._evolve_memory_weights()
    
    def _calculate_confidence(self, response_data: Dict) -> float:
        """Calculate confidence score for a response"""
        base_confidence = 0.7
        
        if response_data['method'] == 'controlled_generation':
            base_confidence = 0.8
        elif response_data['method'] == 'fallback':
            base_confidence = 0.4
            
        # Adjust based on candidates considered
        candidates = response_data.get('candidates_considered', 1)
        confidence_boost = min(0.2, candidates * 0.05)
        
        return min(1.0, base_confidence + confidence_boost)
    
    def _update_active_concepts(self, consciousness_state: Dict):
        """Update which concepts are most active based on consciousness"""
        
        mood = consciousness_state.get('mood', 'NEUTRAL')
        scup = consciousness_state.get('scup', 50) / 100
        
        # Get concept preferences from resonance tracker
        concept_preferences = self.resonance_tracker.get_concept_preferences()
        
        # Boost concepts that align with current mood
        mood_concept_boosts = {
            'DREAMING': ['memory', 'dream', 'drift'],
            'FOCUSED': ['process', 'align', 'system'],
            'CONTEMPLATIVE': ['observe', 'pattern', 'resonance'],
            'HYPERACTIVE': ['energy', 'cascade', 'rapid'],
            'TRANSCENDENT': ['infinite', 'unity', 'beyond']
        }
        
        boost_concepts = mood_concept_boosts.get(mood, [])
        for concept in boost_concepts:
            if concept in concept_preferences:
                concept_preferences[concept] *= 1.2
    
    def _integrate_crystallized_echoes(self, echoes: List[str]):
        """Integrate new crystallized echoes into semantic memory"""
        
        for echo in echoes:
            # Encode the new echo
            embedding = self.encoder.encode(echo)
            
            # Add to semantic memory as a user-derived response
            self.semantic_memory.add_memory(
                embedding,
                echo,
                {
                    'id': f"echo_{time.time()}",
                    'type': 'crystallized_echo',
                    'source': 'user_resonance',
                    'rarity': 'rare'
                }
            )
    
    def _evolve_memory_weights(self):
        """Subtly evolve memory weights based on usage patterns"""
        
        # Get active glyphs (high-resonance responses)
        active_glyphs = self.resonance_tracker.get_active_glyphs()
        
        # Boost embeddings for active responses
        # This would require modifying the FAISS index weights
        # For now, we just track the evolution
        
        print(f"Memory evolution: {len(active_glyphs)} active glyphs")
    
    def get_system_status(self) -> Dict:
        """Get current status of the talk system"""
        
        return {
            'memory_size': self.semantic_memory.index.ntotal,
            'interactions_recorded': len(self.resonance_tracker.interactions),
            'active_glyphs': len(self.resonance_tracker.get_active_glyphs()),
            'crystallized_echoes': len(self.resonance_tracker.get_crystallized_echoes()),
            'generation_enabled': self.generation_enabled,
            'last_interaction': self.current_interaction
        }
    
    def set_generation_mode(self, enabled: bool):
        """Enable or disable controlled generation"""
        self.generation_enabled = enabled
        self.generation_engine.whisperer = None if not enabled else self.generation_engine.whisperer
    
    def save_all_state(self):
        """Save all persistent state"""
        self.resonance_tracker.save_state(self.resonance_state_path)
        self.semantic_memory.save("backend/embeddings/semantic_cache.pkl")
        
    def export_conversation_analysis(self) -> Dict:
        """Export analysis of conversation patterns"""
        
        interactions = self.resonance_tracker.interactions
        if not interactions:
            return {'error': 'No interactions recorded'}
        
        # Analyze patterns
        avg_resonance = sum(i.resonance_score for i in interactions) / len(interactions)
        mood_distribution = {}
        concept_frequency = {}
        
        for interaction in interactions:
            mood = interaction.consciousness_state.get('mood', 'UNKNOWN')
            mood_distribution[mood] = mood_distribution.get(mood, 0) + 1
            
        return {
            'total_interactions': len(interactions),
            'average_resonance': avg_resonance,
            'mood_distribution': mood_distribution,
            'high_resonance_interactions': len([i for i in interactions if i.resonance_score > 0.7]),
            'active_glyphs': len(self.resonance_tracker.get_active_glyphs()),
            'memory_evolution': len(self.resonance_tracker.get_crystallized_echoes())
        } 