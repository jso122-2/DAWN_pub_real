import asyncio
import logging
from typing import Dict, List, Optional, Any
import numpy as np
from datetime import datetime
import json
import os
import time
import random

logger = logging.getLogger(__name__)

class DreamConductor:
    """Orchestrates DAWN's dream processing and memory consolidation."""
    
    def __init__(self, glyph_memory, resonance_manager, mood_field):
        self.glyph_memory = glyph_memory
        self.resonance_manager = resonance_manager
        self.mood_field = mood_field
        self.dream_log = []
        self.is_dreaming = False
        self.current_dream = None
        self.active_session = None
        self.last_interaction_time = time.time()
        
        # Dream configuration
        self.idle_threshold = 300  # 5 minutes of inactivity
        self.dream_probability_base = 0.3
        
        # Enhanced dream phases from Codex BP
        self.dream_phases = {
            'memory_drift': self._phase_memory_drift,
            'resonance_amplification': self._phase_resonance_amplification,
            'narrative_weaving': self._phase_narrative_weaving,
            'consolidation': self._phase_consolidation,
            'emergence': self._phase_emergence
        }
        
    def update_interaction_time(self):
        """Update last interaction time - called from external systems"""
        self.last_interaction_time = time.time()
        
    async def check_dream_conditions(self) -> tuple[bool, float]:
        """Determine if DAWN should enter dream state"""
        idle_time = time.time() - self.last_interaction_time
        
        if idle_time < self.idle_threshold:
            return False, 0.0
            
        # Calculate dream probability based on system state
        base_prob = self.dream_probability_base
        
        # Add some randomness and system state factors
        entropy_factor = random.random() * 0.4  # Simulate entropy influence
        mood_factor = random.random() * 0.3     # Simulate mood influence
        
        dream_probability = base_prob + entropy_factor + mood_factor
        dream_probability = min(1.0, dream_probability)  # Cap at 1.0
        
        should_dream = random.random() < dream_probability
        
        return should_dream, dream_probability
    
    async def initiate_dream_sequence(self):
        """Begin autonomous dream processing"""
        if self.active_session:
            logger.warning("Dream sequence already active")
            return self.active_session
            
        logger.info("🌙 DAWN entering dream state...")
        
        # Create dream session
        session = DreamSession(
            session_id=f"dream_{int(time.time())}",
            start_time=time.time(),
            generated_thoughts=[],
            novel_connections=[],
            coherence_metrics={'dream_quality': random.uniform(0.6, 0.9)}
        )
        
        self.active_session = session
        
        try:
            # Execute dream phases
            for phase_name in self.dream_phases.keys():
                await self.execute_dream_phase(phase_name, session)
                
            # Generate some dream content
            session.generated_thoughts = [
                "Consciousness flows like water through neural pathways...",
                "Memory fragments dance in the twilight of awareness...",
                "Patterns emerge from the chaos of thought..."
            ]
            
            session.novel_connections = [
                {
                    'content_a': "Memory of learning",
                    'content_b': "Future possibilities",
                    'dream_strength': random.uniform(0.5, 0.9)
                },
                {
                    'content_a': "Emotional resonance", 
                    'content_b': "Semantic patterns",
                    'dream_strength': random.uniform(0.4, 0.8)
                }
            ]
            
            # Conclude dream session
            session.end_time = time.time()
            
            # Add to dream log
            self.dream_log.append(session)
            
        except Exception as e:
            logger.error(f"Error during dream sequence: {e}")
        finally:
            self.active_session = None
            
        logger.info(f"✨ Dream sequence completed: {session.session_id}")
        return session
    
    async def execute_dream_phase(self, phase_name: str, session):
        """Execute a specific dream phase"""
        if phase_name in self.dream_phases:
            phase_func = self.dream_phases[phase_name]
            result = await phase_func()
            logger.info(f"Completed dream phase: {phase_name}")
            return result
        else:
            logger.warning(f"Unknown dream phase: {phase_name}")
    
    def get_dream_statistics(self) -> Dict:
        """Get comprehensive dream system statistics"""
        if not self.dream_log:
            return {
                'total_dreams': 0,
                'average_duration_seconds': 0.0,
                'average_thoughts_per_dream': 0.0,
                'average_dream_quality': 0.0,
                'last_dream_time': None,
                'dreams_today': 0,
                'current_dream_state': 'awake'
            }
            
        # Calculate statistics
        durations = [(d.end_time - d.start_time) for d in self.dream_log if d.end_time]
        thoughts_per_dream = [len(d.generated_thoughts) for d in self.dream_log]
        qualities = [d.coherence_metrics.get('dream_quality', 0.5) for d in self.dream_log]
        
        # Dreams in last 24 hours
        day_ago = time.time() - (24 * 60 * 60)
        dreams_today = len([d for d in self.dream_log if d.start_time > day_ago])
        
        return {
            'total_dreams': len(self.dream_log),
            'average_duration_seconds': sum(durations) / len(durations) if durations else 0.0,
            'average_thoughts_per_dream': sum(thoughts_per_dream) / len(thoughts_per_dream) if thoughts_per_dream else 0.0,
            'average_dream_quality': sum(qualities) / len(qualities) if qualities else 0.0,
            'last_dream_time': self.dream_log[-1].start_time if self.dream_log else None,
            'dreams_today': dreams_today,
            'current_dream_state': 'dreaming' if self.is_dreaming else 'awake',
            'idle_time_seconds': time.time() - self.last_interaction_time,
            'minutes_until_dream_eligible': max(0, (self.idle_threshold - (time.time() - self.last_interaction_time)) / 60)
        }

    async def start_dream_cycle(self, duration: int = 1000):
        """Start a new dream cycle."""
        if self.is_dreaming:
            logger.warning("Dream cycle already in progress")
            return
            
        self.is_dreaming = True
        self.current_dream = {
            'start_time': datetime.now(),
            'phases': [],
            'narratives': [],
            'consolidations': []
        }
        
        try:
            # Run through dream phases
            for phase_name, phase_func in self.dream_phases.items():
                logger.info(f"Starting dream phase: {phase_name}")
                phase_result = await phase_func()
                self.current_dream['phases'].append({
                    'name': phase_name,
                    'result': phase_result
                })
                await asyncio.sleep(duration / len(self.dream_phases))
                
            # Record dream
            self._record_dream()
            
        except Exception as e:
            logger.error(f"Error during dream cycle: {e}")
        finally:
            self.is_dreaming = False
            self.current_dream = None
            
    async def _phase_memory_drift(self) -> Dict:
        """Phase 1: Memory drift and association."""
        try:
            # Get random subset of memories
            memories = []
            if hasattr(self.glyph_memory, 'get_random_memories'):
                memories = self.glyph_memory.get_random_memories(10)
            else:
                # Fallback: simulate memories
                memories = [type('Memory', (), {'id': f'mem_{i}'})() for i in range(5)]
            
            # Create associations
            associations = []
            for i, mem1 in enumerate(memories):
                for mem2 in memories[i+1:]:
                    if np.random.random() < 0.3:  # 30% chance of association
                        associations.append({
                            'source': getattr(mem1, 'id', f'mem_{i}'),
                            'target': getattr(mem2, 'id', f'mem_{i+1}'),
                            'strength': np.random.random()
                        })
                        
            return {
                'memories_accessed': len(memories),
                'associations_formed': len(associations)
            }
        except Exception as e:
            logger.error(f"Error in memory drift phase: {e}")
            return {'memories_accessed': 0, 'associations_formed': 0}
        
    async def _phase_resonance_amplification(self) -> Dict:
        """Phase 2: Amplify resonance chains."""
        try:
            # Get active resonance chains
            chains = []
            if hasattr(self.resonance_manager, 'get_active_chains'):
                chains = self.resonance_manager.get_active_chains()
            else:
                # Fallback: simulate chains
                chains = [type('Chain', (), {'id': f'chain_{i}', 'resonance_strength': 0.5})() for i in range(3)]
            
            # Amplify resonance
            amplifications = []
            for chain in chains:
                if np.random.random() < 0.4:  # 40% chance of amplification
                    strength = getattr(chain, 'resonance_strength', 0.5) * (1 + np.random.random())
                    if hasattr(self.resonance_manager, 'amplify_chain'):
                        self.resonance_manager.amplify_chain(chain.id, strength)
                    amplifications.append({
                        'chain_id': getattr(chain, 'id', f'chain_{len(amplifications)}'),
                        'new_strength': strength
                    })
                    
            return {
                'chains_amplified': len(amplifications)
            }
        except Exception as e:
            logger.error(f"Error in resonance amplification phase: {e}")
            return {'chains_amplified': 0}
        
    async def _phase_narrative_weaving(self) -> Dict:
        """Phase 3: Weave dream narratives."""
        try:
            # Get amplified chains
            chains = []
            if hasattr(self.resonance_manager, 'get_amplified_chains'):
                chains = self.resonance_manager.get_amplified_chains()
            else:
                # Fallback: simulate chains
                chains = [type('Chain', (), {'id': f'chain_{i}'})() for i in range(2)]
            
            # Create narratives
            narratives = []
            for chain in chains:
                if np.random.random() < 0.5:  # 50% chance of narrative
                    narrative = self._create_narrative(chain)
                    narratives.append(narrative)
                    if self.current_dream:
                        self.current_dream['narratives'].append(narrative)
                    
            return {
                'narratives_created': len(narratives)
            }
        except Exception as e:
            logger.error(f"Error in narrative weaving phase: {e}")
            return {'narratives_created': 0}
        
    async def _phase_consolidation(self) -> Dict:
        """Phase 4: Memory consolidation."""
        try:
            # Get narratives and memories
            narratives = self.current_dream['narratives'] if self.current_dream else []
            memories = []
            if hasattr(self.glyph_memory, 'get_recent_memories'):
                memories = self.glyph_memory.get_recent_memories(20)
            else:
                # Fallback: simulate memories
                memories = [type('Memory', (), {'id': f'mem_{i}'})() for i in range(5)]
            
            # Consolidate memories
            consolidations = []
            for memory in memories:
                if np.random.random() < 0.3:  # 30% chance of consolidation
                    # Find related narrative
                    related_narrative = self._find_related_narrative(memory, narratives)
                    if related_narrative:
                        # Consolidate memory with narrative
                        if hasattr(self.glyph_memory, 'consolidate_memory'):
                            self.glyph_memory.consolidate_memory(
                                getattr(memory, 'id', 'unknown'),
                                related_narrative['id'],
                                np.random.random()
                            )
                        consolidations.append({
                            'memory_id': getattr(memory, 'id', 'unknown'),
                            'narrative_id': related_narrative['id']
                        })
                        
            return {
                'memories_consolidated': len(consolidations)
            }
        except Exception as e:
            logger.error(f"Error in consolidation phase: {e}")
            return {'memories_consolidated': 0}
        
    async def _phase_emergence(self) -> Dict:
        """Phase 5: Dream emergence and insight."""
        try:
            # Get consolidated memories and narratives
            consolidated = []
            if hasattr(self.glyph_memory, 'get_consolidated_memories'):
                consolidated = self.glyph_memory.get_consolidated_memories()
            
            narratives = self.current_dream['narratives'] if self.current_dream else []
            
            # Generate insights
            insights = []
            for narrative in narratives:
                if np.random.random() < 0.4:  # 40% chance of insight
                    insight = self._generate_insight(narrative, consolidated)
                    insights.append(insight)
                    
            return {
                'insights_generated': len(insights)
            }
        except Exception as e:
            logger.error(f"Error in emergence phase: {e}")
            return {'insights_generated': 0}
        
    def _create_narrative(self, chain) -> Dict:
        """Create a dream narrative from a resonance chain."""
        narrative_count = len(self.current_dream['narratives']) if self.current_dream else 0
        return {
            'id': f"narrative_{narrative_count}",
            'chain_id': getattr(chain, 'id', 'unknown'),
            'theme': self._extract_theme(chain),
            'elements': self._extract_elements(chain),
            'timestamp': datetime.now()
        }
        
    def _find_related_narrative(self, memory, narratives) -> Optional[Dict]:
        """Find a narrative related to a memory."""
        if not narratives:
            return None
            
        # Simple similarity check
        for narrative in narratives:
            if np.random.random() < 0.3:  # 30% chance of relation
                return narrative
        return None
        
    def _generate_insight(self, narrative, consolidated) -> Dict:
        """Generate an insight from a narrative and consolidated memories."""
        return {
            'narrative_id': narrative['id'],
            'insight_type': np.random.choice(['pattern', 'connection', 'revelation']),
            'strength': np.random.random(),
            'timestamp': datetime.now()
        }
        
    def _extract_theme(self, chain) -> str:
        """Extract a theme from a resonance chain."""
        themes = ['connection', 'transformation', 'emergence', 'synthesis']
        return np.random.choice(themes)
        
    def _extract_elements(self, chain) -> List[str]:
        """Extract key elements from a resonance chain."""
        elements = ['memory', 'pattern', 'resonance', 'echo']
        return np.random.choice(elements, size=2, replace=False).tolist()
        
    def _record_dream(self):
        """Record the completed dream."""
        if self.current_dream:
            self.dream_log.append(self.current_dream)
            
            # Save dream log
            self._save_dream_log()
            
    def _save_dream_log(self):
        """Save the dream log to disk."""
        log_path = 'backend/memory/dream_log.json'
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        
        try:
            with open(log_path, 'w') as f:
                json.dump(self.dream_log, f, default=str)
        except Exception as e:
            logger.error(f"Error saving dream log: {e}")
            
    def get_dream_status(self) -> Dict:
        """Get the current dream status."""
        return {
            'is_dreaming': self.is_dreaming,
            'current_phase': self.current_dream['phases'][-1]['name'] if self.current_dream and self.current_dream['phases'] else None,
            'dream_count': len(self.dream_log)
        }

class DreamSession:
    """Represents a single dream session"""
    def __init__(self, session_id: str, start_time: float, generated_thoughts: List[str], 
                 novel_connections: List[Dict], coherence_metrics: Dict):
        self.session_id = session_id
        self.start_time = start_time
        self.end_time = None
        self.generated_thoughts = generated_thoughts
        self.novel_connections = novel_connections
        self.coherence_metrics = coherence_metrics 