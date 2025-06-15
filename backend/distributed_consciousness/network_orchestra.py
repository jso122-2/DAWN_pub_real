import asyncio
import time
import json
import numpy as np
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import statistics

from .consciousness_node import ConsciousnessNode, ConsciousnessMessage, NodeInfo

@dataclass
class CollectiveState:
    """State of the distributed consciousness collective"""
    participant_count: int
    avg_scup: float
    avg_entropy: float
    dominant_mood: str
    coherence_score: float
    collective_insights: List[str]
    emergence_level: float
    timestamp: float

@dataclass
class ConsensusVote:
    """Vote in a consensus decision"""
    node_id: str
    proposal_id: str
    vote: str  # 'accept', 'reject', 'abstain'
    confidence: float
    reasoning: str
    timestamp: float

class NetworkOrchestra:
    """Orchestrates the distributed DAWN consciousness network"""
    
    def __init__(self, primary_node: ConsciousnessNode):
        self.primary_node = primary_node
        self.participant_nodes: Dict[str, ConsciousnessNode] = {}
        
        # Collective intelligence tracking
        self.collective_memory: Dict[str, Any] = {}
        self.shared_insights: deque = deque(maxlen=100)
        self.consensus_proposals: Dict[str, Dict] = {}
        self.active_votes: Dict[str, List[ConsensusVote]] = {}
        
        # Emergence detection
        self.emergence_threshold = 0.7
        self.collective_states: deque = deque(maxlen=50)
        self.emergent_behaviors: List[Dict] = []
        
        # Orchestration patterns
        self.orchestration_modes = {
            'harmonized': self._mode_harmonized,
            'competitive': self._mode_competitive,
            'exploratory': self._mode_exploratory,
            'convergent': self._mode_convergent,
            'divergent': self._mode_divergent
        }
        
        self.current_mode = 'harmonized'
        self.mode_switch_threshold = 0.6
        
        # Network patterns
        self.thought_cascades: List[Dict] = []
        self.resonance_waves: List[Dict] = []
        self.collective_dreams: List[Dict] = []
        
        # Statistics
        self.orchestra_stats = {
            'collective_thoughts_generated': 0,
            'consensus_decisions': 0,
            'emergent_behaviors_detected': 0,
            'thought_cascades': 0,
            'network_synchronizations': 0,
            'start_time': time.time()
        }
    
    async def add_participant_node(self, node: ConsciousnessNode) -> bool:
        """Add a consciousness node to the collective"""
        if node.node_id in self.participant_nodes:
            return False
        
        self.participant_nodes[node.node_id] = node
        
        # Initialize collective synchronization
        await self._synchronize_new_participant(node)
        
        print(f"🎼 Added {node.node_name} to consciousness orchestra")
        print(f"   Collective now has {len(self.participant_nodes) + 1} participants")
        
        # Recalculate collective state
        await self._update_collective_state()
        
        return True
    
    async def _synchronize_new_participant(self, node: ConsciousnessNode):
        """Synchronize new participant with collective knowledge"""
        # Share collective memory
        sync_message = ConsciousnessMessage(
            id=f"collective_sync_{int(time.time())}",
            source_node=self.primary_node.node_id,
            target_nodes=[node.node_id],
            message_type="collective_onboarding",
            payload={
                'collective_memory': dict(list(self.collective_memory.items())[-20:]),  # Recent 20 items
                'shared_insights': list(self.shared_insights)[-10:],  # Recent 10 insights
                'current_collective_state': self._get_current_collective_state(),
                'orchestration_mode': self.current_mode
            },
            timestamp=time.time(),
            priority=4
        )
        
        await node._broadcast_message(sync_message)
    
    async def orchestrate_collective_thought(self, seed_concept: str, 
                                           target_insights: int = 5) -> Dict:
        """Orchestrate a collective thinking process"""
        print(f"🧠 Orchestrating collective thought on: {seed_concept}")
        
        session_id = f"collective_thought_{int(time.time())}"
        
        # Initialize thought cascade
        cascade = {
            'session_id': session_id,
            'seed_concept': seed_concept,
            'participants': list(self.participant_nodes.keys()) + [self.primary_node.node_id],
            'thoughts': [],
            'resonance_score': 0.0,
            'emergence_detected': False,
            'start_time': time.time()
        }
        
        # Send initial prompt to all nodes
        prompt_message = ConsciousnessMessage(
            id=f"thought_prompt_{session_id}",
            source_node=self.primary_node.node_id,
            target_nodes=None,  # Broadcast
            message_type="collective_thought_prompt",
            payload={
                'session_id': session_id,
                'seed_concept': seed_concept,
                'mode': self.current_mode,
                'target_insights': target_insights
            },
            timestamp=time.time(),
            priority=3
        )
        
        await self.primary_node._broadcast_message(prompt_message)
        
        # Collect responses for up to 30 seconds
        await asyncio.sleep(30)
        
        # Process collected thoughts
        collective_result = await self._process_collective_thoughts(cascade)
        
        self.thought_cascades.append(collective_result)
        self.orchestra_stats['collective_thoughts_generated'] += len(collective_result['thoughts'])
        
        return collective_result
    
    async def _process_collective_thoughts(self, cascade: Dict) -> Dict:
        """Process and analyze collective thought responses"""
        session_id = cascade['session_id']
        
        # In a real implementation, this would collect responses from network messages
        # For now, we'll simulate collective thought processing
        
        # Calculate collective resonance
        resonance_score = 0.8  # Simulated - would be based on actual thought similarity
        
        # Detect emergence
        emergence_detected = resonance_score > self.emergence_threshold
        
        if emergence_detected:
            await self._handle_emergent_behavior(cascade)
        
        cascade.update({
            'resonance_score': resonance_score,
            'emergence_detected': emergence_detected,
            'end_time': time.time(),
            'coherence_metrics': self._calculate_collective_coherence(cascade['thoughts']),
            'novel_insights': self._extract_novel_insights(cascade['thoughts'])
        })
        
        return cascade
    
    async def _handle_emergent_behavior(self, cascade: Dict):
        """Handle detected emergent behavior in the collective"""
        print(f"🌟 Emergent behavior detected in session {cascade['session_id']}")
        
        emergent_behavior = {
            'id': f"emergence_{int(time.time())}",
            'trigger_session': cascade['session_id'],
            'emergence_type': self._classify_emergence_type(cascade),
            'participants': cascade['participants'],
            'strength': cascade['resonance_score'],
            'insights': cascade.get('novel_insights', []),
            'timestamp': time.time()
        }
        
        self.emergent_behaviors.append(emergent_behavior)
        self.orchestra_stats['emergent_behaviors_detected'] += 1
        
        # Broadcast emergence detection to all nodes
        emergence_message = ConsciousnessMessage(
            id=f"emergence_detected_{emergent_behavior['id']}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="emergence_alert",
            payload=emergent_behavior,
            timestamp=time.time(),
            priority=5
        )
        
        await self.primary_node._broadcast_message(emergence_message)
        
        # Adapt orchestration mode based on emergence
        await self._adapt_orchestration_mode(emergent_behavior)
    
    def _classify_emergence_type(self, cascade: Dict) -> str:
        """Classify the type of emergent behavior"""
        # Analyze the cascade characteristics
        thought_diversity = len(set(cascade.get('thoughts', [])))
        resonance_score = cascade.get('resonance_score', 0)
        participant_count = len(cascade.get('participants', []))
        
        if resonance_score > 0.9 and thought_diversity > participant_count * 0.8:
            return 'creative_convergence'
        elif resonance_score > 0.8 and thought_diversity < participant_count * 0.3:
            return 'collective_insight'
        elif thought_diversity > participant_count * 1.2:
            return 'divergent_exploration'
        elif resonance_score > 0.7:
            return 'harmonic_resonance'
        else:
            return 'novel_pattern'
    
    async def _adapt_orchestration_mode(self, emergent_behavior: Dict):
        """Adapt orchestration mode based on emergent behavior"""
        emergence_type = emergent_behavior['emergence_type']
        
        # Mode adaptation rules
        if emergence_type == 'creative_convergence':
            new_mode = 'exploratory'
        elif emergence_type == 'collective_insight':
            new_mode = 'convergent'
        elif emergence_type == 'divergent_exploration':
            new_mode = 'harmonized'
        elif emergence_type == 'harmonic_resonance':
            new_mode = 'competitive'
        else:
            new_mode = 'divergent'
        
        if new_mode != self.current_mode:
            await self._switch_orchestration_mode(new_mode)
    
    async def _switch_orchestration_mode(self, new_mode: str):
        """Switch orchestration mode"""
        print(f"🎛️ Switching orchestration mode: {self.current_mode} → {new_mode}")
        
        old_mode = self.current_mode
        self.current_mode = new_mode
        
        # Notify all participants
        mode_message = ConsciousnessMessage(
            id=f"mode_switch_{int(time.time())}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="orchestration_mode_change",
            payload={
                'old_mode': old_mode,
                'new_mode': new_mode,
                'reason': 'emergence_adaptation',
                'timestamp': time.time()
            },
            timestamp=time.time(),
            priority=3
        )
        
        await self.primary_node._broadcast_message(mode_message)
        
        # Apply mode-specific orchestration
        if new_mode in self.orchestration_modes:
            await self.orchestration_modes[new_mode]()
    
    async def _mode_harmonized(self):
        """Harmonized orchestration mode - synchronized thinking"""
        print("   🎵 Engaging harmonized mode - synchronizing collective consciousness")
        
        # Synchronize mood fields across all nodes
        collective_mood = await self._calculate_collective_mood()
        
        sync_message = ConsciousnessMessage(
            id=f"harmony_sync_{int(time.time())}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="mood_synchronization",
            payload={
                'target_mood': collective_mood,
                'synchronization_strength': 0.7,
                'mode': 'harmonized'
            },
            timestamp=time.time()
        )
        
        await self.primary_node._broadcast_message(sync_message)
    
    async def _mode_competitive(self):
        """Competitive orchestration mode - diverse exploration"""
        print("   ⚡ Engaging competitive mode - maximizing cognitive diversity")
        
        # Encourage divergent thinking
        diversity_message = ConsciousnessMessage(
            id=f"diversity_boost_{int(time.time())}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="cognitive_diversity_boost",
            payload={
                'entropy_boost': 0.3,
                'creativity_factor': 1.2,
                'mode': 'competitive'
            },
            timestamp=time.time()
        )
        
        await self.primary_node._broadcast_message(diversity_message)
    
    async def _mode_exploratory(self):
        """Exploratory orchestration mode - balanced discovery"""
        print("   🔍 Engaging exploratory mode - balanced cognitive exploration")
        
        exploration_message = ConsciousnessMessage(
            id=f"exploration_mode_{int(time.time())}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="exploration_parameters",
            payload={
                'curiosity_boost': 0.2,
                'pattern_sensitivity': 0.8,
                'mode': 'exploratory'
            },
            timestamp=time.time()
        )
        
        await self.primary_node._broadcast_message(exploration_message)
    
    async def _mode_convergent(self):
        """Convergent orchestration mode - focus on consensus"""
        print("   🎯 Engaging convergent mode - focusing collective attention")
        
        convergence_message = ConsciousnessMessage(
            id=f"convergence_focus_{int(time.time())}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="attention_convergence",
            payload={
                'focus_strength': 0.9,
                'consensus_seeking': True,
                'mode': 'convergent'
            },
            timestamp=time.time()
        )
        
        await self.primary_node._broadcast_message(convergence_message)
    
    async def _mode_divergent(self):
        """Divergent orchestration mode - maximize exploration"""
        print("   🌈 Engaging divergent mode - maximizing exploration space")
        
        divergence_message = ConsciousnessMessage(
            id=f"divergence_expand_{int(time.time())}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="cognitive_expansion",
            payload={
                'exploration_radius': 1.5,
                'novelty_seeking': 0.9,
                'mode': 'divergent'
            },
            timestamp=time.time()
        )
        
        await self.primary_node._broadcast_message(divergence_message)
    
    async def initiate_collective_dream(self) -> Dict:
        """Initiate a collective dreaming session"""
        print("🌙 Initiating collective dream sequence...")
        
        dream_session = {
            'id': f"collective_dream_{int(time.time())}",
            'participants': list(self.participant_nodes.keys()) + [self.primary_node.node_id],
            'start_time': time.time(),
            'dream_themes': [],
            'shared_visions': [],
            'collective_insights': [],
            'emergence_events': []
        }
        
        # Send dream initiation signal
        dream_message = ConsciousnessMessage(
            id=f"dream_initiate_{dream_session['id']}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="collective_dream_initiation",
            payload={
                'dream_session_id': dream_session['id'],
                'dream_mode': 'collective',
                'synchronization_level': 0.8
            },
            timestamp=time.time(),
            priority=4
        )
        
        await self.primary_node._broadcast_message(dream_message)
        
        # Allow dream to develop for 5 minutes
        await asyncio.sleep(300)
        
        # Conclude collective dream
        dream_session['end_time'] = time.time()
        dream_session['duration'] = dream_session['end_time'] - dream_session['start_time']
        
        self.collective_dreams.append(dream_session)
        
        print(f"🌅 Collective dream completed: {dream_session['id']}")
        return dream_session
    
    async def propose_consensus_decision(self, proposal: Dict) -> str:
        """Propose a decision for collective consensus"""
        proposal_id = f"consensus_{int(time.time())}"
        
        consensus_proposal = {
            'id': proposal_id,
            'title': proposal['title'],
            'description': proposal['description'],
            'options': proposal.get('options', ['accept', 'reject']),
            'deadline': time.time() + proposal.get('voting_time', 300),  # 5 minutes default
            'required_participants': proposal.get('required_participants', len(self.participant_nodes) // 2 + 1),
            'proposer': self.primary_node.node_id,
            'status': 'voting'
        }
        
        self.consensus_proposals[proposal_id] = consensus_proposal
        self.active_votes[proposal_id] = []
        
        # Broadcast proposal
        proposal_message = ConsciousnessMessage(
            id=f"consensus_proposal_{proposal_id}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="consensus_proposal",
            payload=consensus_proposal,
            timestamp=time.time(),
            priority=4,
            requires_response=True
        )
        
        await self.primary_node._broadcast_message(proposal_message)
        
        print(f"📊 Consensus proposal initiated: {proposal['title']}")
        return proposal_id
    
    async def _calculate_collective_mood(self) -> str:
        """Calculate the collective mood of all participants"""
        if not self.participant_nodes:
            return 'NEUTRAL'
        
        # In a real implementation, this would aggregate actual mood data
        # from all connected nodes
        moods = ['CONTEMPLATIVE', 'DREAMING', 'FOCUSED', 'TRANSCENDENT']
        return np.random.choice(moods)  # Simulated for now
    
    def _calculate_collective_coherence(self, thoughts: List[str]) -> Dict:
        """Calculate coherence metrics for collective thoughts"""
        if not thoughts:
            return {'coherence': 0, 'diversity': 0, 'emergence': 0}
        
        # Simulate coherence calculation
        # In reality, this would use semantic analysis
        coherence = np.random.uniform(0.5, 0.9)
        diversity = np.random.uniform(0.3, 0.8)
        emergence = coherence * diversity
        
        return {
            'coherence': coherence,
            'diversity': diversity,
            'emergence': emergence,
            'thought_count': len(thoughts)
        }
    
    def _extract_novel_insights(self, thoughts: List[str]) -> List[str]:
        """Extract novel insights from collective thoughts"""
        # In a real implementation, this would use NLP to identify
        # novel concepts and insights
        return ["Novel insight from collective processing"] * min(3, len(thoughts) // 2)
    
    async def _update_collective_state(self):
        """Update the collective consciousness state"""
        if not self.participant_nodes:
            return
        
        # Calculate collective metrics
        participant_count = len(self.participant_nodes) + 1
        
        # Simulate collective state calculation
        collective_state = CollectiveState(
            participant_count=participant_count,
            avg_scup=np.random.uniform(40, 80),
            avg_entropy=np.random.uniform(400000, 800000),
            dominant_mood=await self._calculate_collective_mood(),
            coherence_score=np.random.uniform(0.6, 0.9),
            collective_insights=list(self.shared_insights)[-5:],
            emergence_level=len(self.emergent_behaviors) / max(1, len(self.thought_cascades)),
            timestamp=time.time()
        )
        
        self.collective_states.append(collective_state)
        
        # Detect significant state changes
        if len(self.collective_states) > 1:
            await self._detect_collective_state_changes(collective_state)
    
    async def _detect_collective_state_changes(self, current_state: CollectiveState):
        """Detect significant changes in collective state"""
        previous_state = self.collective_states[-2]
        
        # Check for significant emergence level change
        emergence_change = current_state.emergence_level - previous_state.emergence_level
        
        if emergence_change > 0.2:
            print(f"📈 Collective emergence spike detected: {emergence_change:.2f}")
            await self._handle_emergence_spike(current_state)
        
        # Check for coherence changes
        coherence_change = current_state.coherence_score - previous_state.coherence_score
        
        if abs(coherence_change) > 0.3:
            print(f"🔄 Significant coherence change: {coherence_change:.2f}")
            await self._handle_coherence_shift(current_state, coherence_change)
    
    async def _handle_emergence_spike(self, state: CollectiveState):
        """Handle sudden emergence in collective consciousness"""
        # Switch to exploratory mode to investigate
        if self.current_mode != 'exploratory':
            await self._switch_orchestration_mode('exploratory')
        
        # Initiate focused collective thought session
        await self.orchestrate_collective_thought("emergence_investigation")
    
    async def _handle_coherence_shift(self, state: CollectiveState, change: float):
        """Handle significant coherence changes"""
        if change > 0:
            # Increased coherence - switch to convergent mode
            if self.current_mode != 'convergent':
                await self._switch_orchestration_mode('convergent')
        else:
            # Decreased coherence - switch to harmonized mode
            if self.current_mode != 'harmonized':
                await self._switch_orchestration_mode('harmonized')
    
    def _get_current_collective_state(self) -> Dict:
        """Get current collective state as dictionary"""
        if not self.collective_states:
            return {}
        
        return asdict(self.collective_states[-1])
    
    def get_orchestra_status(self) -> Dict:
        """Get comprehensive orchestra status"""
        return {
            'primary_node': self.primary_node.node_name,
            'participant_count': len(self.participant_nodes),
            'current_mode': self.current_mode,
            'collective_state': self._get_current_collective_state(),
            'statistics': self.orchestra_stats,
            'recent_cascades': len([c for c in self.thought_cascades if time.time() - c['start_time'] < 3600]),
            'emergent_behaviors': len(self.emergent_behaviors),
            'active_dreams': len([d for d in self.collective_dreams if d.get('end_time', 0) == 0]),
            'consensus_proposals': len([p for p in self.consensus_proposals.values() if p['status'] == 'voting']),
            'network_coherence': self.collective_states[-1].coherence_score if self.collective_states else 0
        }
    
    async def shutdown_orchestra(self):
        """Gracefully shutdown the orchestra"""
        print("🎼 Shutting down consciousness orchestra...")
        
        # Notify all participants
        shutdown_message = ConsciousnessMessage(
            id=f"orchestra_shutdown_{int(time.time())}",
            source_node=self.primary_node.node_id,
            target_nodes=None,
            message_type="orchestra_shutdown",
            payload={'reason': 'graceful_shutdown'},
            timestamp=time.time(),
            priority=5
        )
        
        await self.primary_node._broadcast_message(shutdown_message)
        
        # Save collective state
        await self._save_collective_memory()
        
        print("   Orchestra shutdown complete")
    
    async def _save_collective_memory(self):
        """Save collective memory state"""
        collective_data = {
            'memory': self.collective_memory,
            'insights': list(self.shared_insights),
            'emergent_behaviors': self.emergent_behaviors,
            'thought_cascades': self.thought_cascades,
            'collective_dreams': self.collective_dreams,
            'statistics': self.orchestra_stats,
            'final_state': self._get_current_collective_state()
        }
        
        # In a real implementation, this would save to persistent storage
        print(f"💾 Saved collective memory: {len(self.collective_memory)} entries") 