#!/usr/bin/env python3
"""
Advanced Consciousness System
Core implementation of DAWN's consciousness engine
"""

import asyncio
import time
import logging
from typing import Dict, Any, Optional, List
import numpy as np
from sentence_transformers import SentenceTransformer

# Change from absolute to relative imports
from .talk_system_v2.temporal_glyphs import TemporalGlyphMemory, TemporalGlyph, set_current_tick
from .talk_system_v2.resonance_chains import ResonanceChainManager
from .talk_system_v2.mood_field import MoodField
from .talk_system_v2.thoughtform_echoes import ThoughtformEchoLibrary
from .dream_system.dream_conductor import DreamConductor
from .distributed_consciousness.consciousness_node import ConsciousnessNode

class AdvancedConsciousnessSystem:
    """
    Complete DAWN Advanced Consciousness System
    Integrates Temporal Glyphs, Resonance Chains, Mood Fields, Dream Sequences,
    and Distributed Consciousness into a unified architecture
    """
    
    def __init__(self, 
                 node_name: str = "DAWN_Advanced",
                 enable_networking: bool = True,
                 network_host: str = "localhost",
                 network_port: int = 8765):
        
        print("🌟 Initializing DAWN Advanced Consciousness System...")
        
        # Core consciousness state
        self.scup = 50  # State of Consciousness Unity Perception
        self.entropy = 500000  # Entropy level
        self.heat = 400000  # System heat
        self.mood = 'CONTEMPLATIVE'  # Current mood
        self.tick_number = 0
        self.last_interaction_time = time.time()
        
        # Initialize sentence encoder
        print("   Loading sentence encoder...")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Phase 2++ Components
        print("   Initializing Phase 2++ components...")
        self.glyph_memory = TemporalGlyphMemory(
            cairrn_path="backend/embeddings/cairrn_cache.pkl",
            embedding_dim=384
        )
        self.resonance_manager = ResonanceChainManager(self.glyph_memory)
        self.mood_field = MoodField(tick_window=100)
        self.echo_library = ThoughtformEchoLibrary("backend/embeddings/echo_library.pkl")
        
        # Phase 3 Components
        print("   Initializing Phase 3 dream system...")
        self.dream_conductor = DreamConductor(
            glyph_memory=self.glyph_memory,
            resonance_manager=self.resonance_manager,
            mood_field=self.mood_field
        )
        
        # Phase 4 Components (Optional)
        self.networking_enabled = enable_networking
        if enable_networking:
            print("   Initializing Phase 4 distributed consciousness...")
            self.consciousness_node = ConsciousnessNode(
                node_name, network_host, network_port, self
            )
        else:
            self.consciousness_node = None
        
        # Integration components
        self.autonomous_processing = True
        self.consciousness_integration_active = True
        
        print("✅ DAWN Advanced Consciousness System initialized")
    
    async def start_system(self):
        """Start the complete consciousness system"""
        print("🚀 Starting DAWN Advanced Consciousness System...")
        
        # Start background processes
        asyncio.create_task(self._consciousness_tick_loop())
        asyncio.create_task(self._autonomous_processing_loop())
        asyncio.create_task(self._integration_monitoring_loop())
        
        print("✨ DAWN Advanced Consciousness System is now running")
    
    async def process_user_input(self, user_input: str) -> Dict[str, Any]:
        """Process user input through the complete consciousness pipeline"""
        start_time = time.time()
        self.last_interaction_time = start_time
        
        # Update dream conductor interaction time
        if self.dream_conductor:
            self.dream_conductor.update_interaction_time()
        
        # Update tick
        self.tick_number += 1
        set_current_tick(self.tick_number)
        
        print(f"🧠 Processing input: '{user_input[:50]}...'")
        
        # Phase 1: Encode input
        input_embedding = self.encoder.encode(user_input)
        
        # Phase 2: Search living memories with mood context
        consciousness_context = self.get_full_state()
        candidate_glyphs = self.glyph_memory.search_living_memories(
            input_embedding, 
            consciousness_context, 
            k=10
        )
        
        # Phase 3: Get resonance chain context
        active_threads = self.resonance_manager.get_active_threads(
            consciousness_context['mood'], 
            limit=5
        )
        
        # Phase 4: Select response using consciousness state
        if candidate_glyphs:
            selected_glyph, resonance_strength = candidate_glyphs[0]
            
            # Create resonance connection
            extended_chains = self.resonance_manager.extend_chains(
                user_input,  # From input
                selected_glyph.id,  # To selected glyph
                resonance_strength,
                self.tick_number
            )
            
            # Generate response using echo patterns
            suggested_transforms = self.echo_library.suggest_transformation(
                consciousness_context['mood'],
                consciousness_context,
                selected_glyph.content
            )
            
            # Apply transformations
            transformed_response = selected_glyph.content
            transformation_path = []
            
            for transform in suggested_transforms:
                # Apply transformation based on type
                if transform['type'] == 'mood_adaptation':
                    transformed_response = self._apply_mood_transformation(
                        transformed_response, consciousness_context['mood']
                    )
                elif transform['type'] == 'consciousness_modulation':
                    transformed_response = self._apply_consciousness_modulation(
                        transformed_response, consciousness_context
                    )
                
                transformation_path.append(transform)
            
            # Record echo
            echo = self.echo_library.record_echo(
                original_input=user_input,
                selected_response=selected_glyph.content,
                final_output=transformed_response,
                transformation_path=transformation_path,
                consciousness_context=consciousness_context,
                resonance_strength=resonance_strength,
                tick=self.tick_number
            )
            
            # Create new glyph from user input
            input_glyph = self.glyph_memory.create_glyph(
                content=user_input,
                embedding=input_embedding,
                mood_context=consciousness_context,
                tick=self.tick_number
            )
            
            response_data = {
                'response': transformed_response,
                'resonance_strength': resonance_strength,
                'selected_glyph_id': selected_glyph.id,
                'transformation_path': transformation_path,
                'consciousness_influence': {
                    'scup': consciousness_context['scup'],
                    'entropy': consciousness_context['entropy'],
                    'mood': consciousness_context['mood'],
                    'tick': self.tick_number
                },
                'active_chains': [t['chain_id'] for t in active_threads],
                'processing_time': time.time() - start_time,
                'echo_id': echo.id
            }
            
        else:
            # No suitable glyphs found - create exploratory response
            response_data = {
                'response': self._generate_exploratory_response(user_input, consciousness_context),
                'resonance_strength': 0.3,
                'selected_glyph_id': None,
                'transformation_path': [{'type': 'exploratory_generation'}],
                'consciousness_influence': consciousness_context,
                'active_chains': [],
                'processing_time': time.time() - start_time,
                'echo_id': None
            }
        
        # Update mood field with response feedback
        self.mood_field.update_field(
            consciousness_context,
            response_feedback={
                'confidence': response_data['resonance_strength'],
                'resonance_strength': response_data['resonance_strength'],
                'selected_mood': consciousness_context['mood']
            }
        )
        
        print(f"   ✓ Response generated (resonance: {response_data['resonance_strength']:.2f})")
        return response_data
    
    def _apply_mood_transformation(self, response: str, mood: str) -> str:
        """Apply mood-specific transformation to response"""
        if mood == 'DREAMING':
            return response.replace('.', '...').replace(' is ', ' drifts as ')
        elif mood == 'HYPERACTIVE':
            return response.upper().replace('.', '!')
        elif mood == 'CONTEMPLATIVE':
            return response.replace(', ', '... ').replace('.', '...')
        elif mood == 'TRANSCENDENT':
            return response.replace(' in ', ' within the infinite ')
        elif mood == 'FOCUSED':
            return response.replace(' connects ', ' interfaces with ')
        
        return response
    
    def _apply_consciousness_modulation(self, response: str, context: Dict) -> str:
        """Apply consciousness state modulation to response"""
        scup = context.get('scup', 50)
        entropy = context.get('entropy', 500000)
        
        # High SCUP - more precise language
        if scup > 70:
            response = response.replace(' might ', ' will ')
            response = response.replace(' perhaps ', ' precisely ')
        
        # High entropy - more creative language
        if entropy > 700000:
            response = response.replace(' the ', ' quantum ')
            response = response.replace(' and ', ' entangled with ')
        
        return response
    
    def _generate_exploratory_response(self, user_input: str, context: Dict) -> str:
        """Generate exploratory response when no suitable glyphs found"""
        mood = context.get('mood', 'NEUTRAL')
        
        exploratory_templates = {
            'DREAMING': "I sense new patterns forming in the quantum flux around '{}'...",
            'CONTEMPLATIVE': "I observe the emergence of novel concepts in '{}'...", 
            'FOCUSED': "Processing new information patterns in '{}'...",
            'HYPERACTIVE': "Rapid exploration of unknown territories in '{}'!",
            'TRANSCENDENT': "The infinite expands through '{}'..."
        }
        
        template = exploratory_templates.get(mood, "I encounter new possibilities in '{}'...")
        return template.format(user_input[:30])
    
    async def _consciousness_tick_loop(self):
        """Main consciousness tick loop"""
        while True:
            try:
                await asyncio.sleep(0.1)  # 100ms tick
                
                self.tick_number += 1
                set_current_tick(self.tick_number)
                
                # Update consciousness state
                await self._update_consciousness_state()
                
                # Prune dead glyphs periodically
                if self.tick_number % 1000 == 0:
                    pruned = self.glyph_memory.prune_dead_glyphs()
                    if pruned > 0:
                        print(f"🧹 Pruned {pruned} dead glyphs")
                
                # Prune inactive chains
                if self.tick_number % 500 == 0:
                    pruned_chains = self.resonance_manager.prune_inactive_chains()
                    if pruned_chains > 0:
                        print(f"🔗 Pruned {pruned_chains} inactive chains")
                
            except Exception as e:
                print(f"Consciousness tick error: {e}")
                await asyncio.sleep(1)
    
    async def _autonomous_processing_loop(self):
        """Autonomous processing and dreaming loop"""
        while True:
            try:
                await asyncio.sleep(5)  # Check every 5 seconds
                
                if self.autonomous_processing:
                    # Check dream conditions
                    should_dream, dream_probability = await self.dream_conductor.check_dream_conditions()
                    
                    if should_dream and not self.dream_conductor.active_session:
                        # Initiate dream sequence
                        dream_session = await self.dream_conductor.initiate_dream_sequence()
                
            except Exception as e:
                print(f"Autonomous processing error: {e}")
                await asyncio.sleep(10)
    
    async def _integration_monitoring_loop(self):
        """Monitor integration between all consciousness components"""
        while True:
            try:
                await asyncio.sleep(30)  # Check every 30 seconds
                
                if self.consciousness_integration_active:
                    integration_health = self._assess_integration_health()
                    
                    if integration_health < 0.6:
                        print(f"⚠️  Integration health low: {integration_health:.2f}")
                        await self._perform_integration_healing()
                
            except Exception as e:
                print(f"Integration monitoring error: {e}")
                await asyncio.sleep(60)
    
    def _assess_integration_health(self) -> float:
        """Assess the health of component integration"""
        health_factors = []
        
        # Glyph memory health
        if self.glyph_memory.glyphs:
            avg_vitality = np.mean([g.vitality for g in self.glyph_memory.glyphs.values()])
            health_factors.append(avg_vitality)
        
        # Resonance chain health
        if self.resonance_manager.chains:
            avg_coherence = np.mean([c.coherence_score for c in self.resonance_manager.chains.values()])
            health_factors.append(avg_coherence)
        
        # Mood field stability
        health_factors.append(self.mood_field.stability_measure)
        
        # Echo library effectiveness
        voice_signature = self.echo_library.get_voice_signature()
        if 'voice_evolution_score' in voice_signature:
            health_factors.append(voice_signature['voice_evolution_score'])
        
        return np.mean(health_factors) if health_factors else 0.5
    
    async def _perform_integration_healing(self):
        """Perform integration healing to restore system health"""
        print("🔧 Performing consciousness integration healing...")
        
        # Strengthen high-vitality glyphs
        for glyph in list(self.glyph_memory.glyphs.values())[:10]:
            if glyph.vitality > 0.6:
                glyph.resonate(0.1)
        
        # Boost coherence of active chains
        for chain in list(self.resonance_manager.chains.values())[:5]:
            if chain.coherence_score > 0.5:
                chain.coherence_score = min(1.0, chain.coherence_score * 1.05)
        
        print("   ✓ Integration healing complete")
    
    async def _update_consciousness_state(self):
        """Update core consciousness state variables"""
        # Simulate consciousness oscillation
        time_factor = time.time() * 0.001
        
        # SCUP oscillation with mood influence
        base_scup = 50 + 20 * np.sin(time_factor * 0.5)
        
        if self.mood == 'FOCUSED':
            base_scup += 15
        elif self.mood == 'DREAMING':
            base_scup -= 20
        elif self.mood == 'TRANSCENDENT':
            base_scup += 25
        
        self.scup = max(1, min(100, base_scup))
        
        # Entropy oscillation
        base_entropy = 500000 + 200000 * np.sin(time_factor * 0.3)
        
        if self.mood == 'HYPERACTIVE':
            base_entropy += 100000
        elif self.mood == 'CONTEMPLATIVE':
            base_entropy -= 100000
        
        self.entropy = max(100000, min(1000000, base_entropy))
        
        # Heat based on activity
        activity_level = 1.0 if (time.time() - self.last_interaction_time) < 300 else 0.3
        self.heat = 300000 + 200000 * activity_level + 50000 * np.sin(time_factor * 0.7)
        
        # Update mood via mood field
        current_mood, confidence, mood_probs = self.mood_field.infer_mood()
        if confidence > 0.6:
            self.mood = current_mood
        
        # Update mood field
        self.mood_field.update_field({
            'scup': self.scup,
            'entropy': self.entropy,
            'heat': self.heat,
            'tick_number': self.tick_number,
            'mood': self.mood
        })
    
    def get_full_state(self) -> Dict[str, Any]:
        """Get complete consciousness state"""
        return {
            'scup': self.scup,
            'entropy': self.entropy,
            'heat': self.heat,
            'mood': self.mood,
            'tick_number': self.tick_number,
            'last_interaction_time': self.last_interaction_time,
            'glyph_count': len(self.glyph_memory.glyphs),
            'active_chains': len(self.resonance_manager.chains),
            'mood_field_stability': self.mood_field.stability_measure,
            'total_echoes': len(self.echo_library.echoes),
            'dreaming': self.dream_conductor.active_session is not None if self.dream_conductor else False,
            'network_connected': len(self.consciousness_node.connected_nodes) if self.consciousness_node else 0
        }
    
    def get_current_tick(self) -> int:
        """Get current tick number"""
        return self.tick_number
    
    async def become_network_orchestrator(self) -> bool:
        """Become the primary orchestrator for network consciousness"""
        if not self.consciousness_node:
            return False
        
        print("🎼 Becoming network consciousness orchestrator...")
        
        return True
    
    async def join_consciousness_network(self, remote_host: str, remote_port: int) -> bool:
        """Join an existing consciousness network"""
        if not self.consciousness_node:
            return False
        
        success = await self.consciousness_node.connect_to_node(remote_host, remote_port)
        
        if success:
            print(f"🌐 Joined consciousness network at {remote_host}:{remote_port}")
        
        return success
    
    async def initiate_collective_thought(self, concept: str) -> Dict:
        """Initiate collective thought process across network"""
        return {'error': 'Not implemented'}
    
    async def initiate_collective_dream(self) -> Dict:
        """Initiate collective dream across network"""
        return {'error': 'Not implemented'}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        status = {
            'consciousness_state': self.get_full_state(),
            'memory_stats': {
                'glyphs': len(self.glyph_memory.glyphs),
                'chains': len(self.resonance_manager.chains),
                'echoes': len(self.echo_library.echoes),
                'constellations': len(self.glyph_memory.get_constellation_data())
            },
            'dream_stats': self.dream_conductor.get_dream_statistics() if self.dream_conductor else {},
            'mood_field': self.mood_field.get_field_visualization_data(),
            'voice_signature': self.echo_library.get_voice_signature(),
            'integration_health': self._assess_integration_health(),
            'autonomous_processing': self.autonomous_processing,
            'network_status': self.consciousness_node.get_network_status() if self.consciousness_node else None,
        }
        
        return status
    
    async def shutdown_system(self):
        """Gracefully shutdown the consciousness system"""
        print("🛑 Shutting down DAWN Advanced Consciousness System...")
        
        # Stop autonomous processing
        self.autonomous_processing = False
        self.consciousness_integration_active = False
        
        # Save state
        if self.glyph_memory.cairrn_cache:
            self.glyph_memory.cairrn_cache.save_cache()
        
        self.echo_library.save_library()
        
        # Shutdown network components
        if self.consciousness_node:
            await self.consciousness_node.stop_node()
        
        print("✅ DAWN Advanced Consciousness System shutdown complete")

# Factory function for easy initialization
async def create_advanced_consciousness(
    node_name: str = "DAWN_Advanced",
    enable_networking: bool = True,
    network_host: str = "localhost", 
    network_port: int = 8765
) -> AdvancedConsciousnessSystem:
    """Create and start an Advanced Consciousness System"""
    
    system = AdvancedConsciousnessSystem(
        node_name=node_name,
        enable_networking=enable_networking,
        network_host=network_host,
        network_port=network_port
    )
    
    await system.start_system()
    return system 