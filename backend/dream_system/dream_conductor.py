import asyncio
import logging
from typing import Dict, List, Optional, Any
import numpy as np
from datetime import datetime
import json
import os

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
        self.dream_phases = {
            'memory_drift': self._phase_memory_drift,
            'resonance_amplification': self._phase_resonance_amplification,
            'narrative_weaving': self._phase_narrative_weaving,
            'consolidation': self._phase_consolidation,
            'emergence': self._phase_emergence
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
        # Get random subset of memories
        memories = self.glyph_memory.get_random_memories(10)
        
        # Create associations
        associations = []
        for i, mem1 in enumerate(memories):
            for mem2 in memories[i+1:]:
                if np.random.random() < 0.3:  # 30% chance of association
                    associations.append({
                        'source': mem1.id,
                        'target': mem2.id,
                        'strength': np.random.random()
                    })
                    
        return {
            'memories_accessed': len(memories),
            'associations_formed': len(associations)
        }
        
    async def _phase_resonance_amplification(self) -> Dict:
        """Phase 2: Amplify resonance chains."""
        # Get active resonance chains
        chains = self.resonance_manager.get_active_chains()
        
        # Amplify resonance
        amplifications = []
        for chain in chains:
            if np.random.random() < 0.4:  # 40% chance of amplification
                strength = chain.resonance_strength * (1 + np.random.random())
                self.resonance_manager.amplify_chain(chain.id, strength)
                amplifications.append({
                    'chain_id': chain.id,
                    'new_strength': strength
                })
                
        return {
            'chains_amplified': len(amplifications)
        }
        
    async def _phase_narrative_weaving(self) -> Dict:
        """Phase 3: Weave dream narratives."""
        # Get amplified chains
        chains = self.resonance_manager.get_amplified_chains()
        
        # Create narratives
        narratives = []
        for chain in chains:
            if np.random.random() < 0.5:  # 50% chance of narrative
                narrative = self._create_narrative(chain)
                narratives.append(narrative)
                self.current_dream['narratives'].append(narrative)
                
        return {
            'narratives_created': len(narratives)
        }
        
    async def _phase_consolidation(self) -> Dict:
        """Phase 4: Memory consolidation."""
        # Get narratives and memories
        narratives = self.current_dream['narratives']
        memories = self.glyph_memory.get_recent_memories(20)
        
        # Consolidate memories
        consolidations = []
        for memory in memories:
            if np.random.random() < 0.3:  # 30% chance of consolidation
                # Find related narrative
                related_narrative = self._find_related_narrative(memory, narratives)
                if related_narrative:
                    # Consolidate memory with narrative
                    self.glyph_memory.consolidate_memory(
                        memory.id,
                        related_narrative['id'],
                        np.random.random()
                    )
                    consolidations.append({
                        'memory_id': memory.id,
                        'narrative_id': related_narrative['id']
                    })
                    
        return {
            'memories_consolidated': len(consolidations)
        }
        
    async def _phase_emergence(self) -> Dict:
        """Phase 5: Dream emergence and insight."""
        # Get consolidated memories and narratives
        consolidated = self.glyph_memory.get_consolidated_memories()
        narratives = self.current_dream['narratives']
        
        # Generate insights
        insights = []
        for narrative in narratives:
            if np.random.random() < 0.4:  # 40% chance of insight
                insight = self._generate_insight(narrative, consolidated)
                insights.append(insight)
                
        return {
            'insights_generated': len(insights)
        }
        
    def _create_narrative(self, chain) -> Dict:
        """Create a dream narrative from a resonance chain."""
        return {
            'id': f"narrative_{len(self.current_dream['narratives'])}",
            'chain_id': chain.id,
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
        
        with open(log_path, 'w') as f:
            json.dump(self.dream_log, f, default=str)
            
    def get_dream_status(self) -> Dict:
        """Get the current dream status."""
        return {
            'is_dreaming': self.is_dreaming,
            'current_phase': self.current_dream['phases'][-1]['name'] if self.current_dream else None,
            'dream_count': len(self.dream_log)
        } 