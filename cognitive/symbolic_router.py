"""
DAWN Symbolic Router - Embodied Memory and Emotion Routing
Coordinates symbolic organs and routes rebloom events through the body.
Integrated with DAWN's memory routing and consciousness systems.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import random
import logging

from .symbolic_anatomy import FractalHeart, SomaCoil, GlyphLung

# Integration with DAWN systems
try:
    from core.memory.memory_routing_system import get_memory_routing_system
    MEMORY_ROUTING_AVAILABLE = True
except ImportError:
    MEMORY_ROUTING_AVAILABLE = False

try:
    from core.consciousness_core import ConsciousnessCore
    CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    CONSCIOUSNESS_AVAILABLE = False

logger = logging.getLogger(__name__)


class SymbolicRouter:
    """
    Central routing system for DAWN's symbolic anatomy.
    Coordinates the flow of memory and emotion through symbolic organs.
    Integrates with DAWN's memory routing and consciousness systems.
    """
    
    def __init__(self, consciousness_core=None, memory_system=None):
        """Initialize the symbolic router with DAWN system integrations."""
        # Initialize symbolic organs
        self.heart = FractalHeart()
        self.coil = SomaCoil()
        self.lung = GlyphLung()
        
        # DAWN system integrations
        self.consciousness_core = consciousness_core
        self.memory_system = memory_system or (get_memory_routing_system() if MEMORY_ROUTING_AVAILABLE else None)
        
        # Routing state
        self.total_reblooms = 0
        self.routing_history = []
        self.organ_synergy = 0.0  # How well organs work together
        
        # Routing thresholds and rules
        self.emotion_threshold = 0.1
        self.entropy_clear_threshold = 0.6
        self.synergy_decay_rate = 0.05
        
        logger.info("🌐 SymbolicRouter initialized - Embodied routing active")
        logger.info(f"   💝 Heart: {self.heart.get_heart_signature()['resonance_state']}")
        logger.info(f"   🧬 Coil: {self.coil.get_active_glyph()} glyph active")
        logger.info(f"   🫁 Lung: {self.lung.breathing_phase} phase")
        
        if self.memory_system:
            logger.info("   🔗 Memory routing integration: ✓")
        if self.consciousness_core:
            logger.info("   🧠 Consciousness core integration: ✓")
    
    async def rebloom_trigger(self, memory_chunk, chunk_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process a rebloom event through the symbolic anatomy.
        Routes emotional charge and memory paths based on chunk characteristics.
        
        Args:
            memory_chunk: Memory chunk object with pulse_state, content, etc.
            chunk_id: Optional unique identifier for the memory
            
        Returns:
            dict: Routing response with organ activations
        """
        current_time = datetime.now()
        self.total_reblooms += 1
        
        # Extract pulse state information
        pulse_state = getattr(memory_chunk, 'pulse_state', {})
        
        # Get consciousness context if available
        consciousness_context = self._get_consciousness_context()
        
        # Initialize routing response
        routing_response = {
            'rebloom_id': self.total_reblooms,
            'timestamp': current_time.isoformat(),
            'memory_id': chunk_id,
            'organ_activations': {},
            'synergy_changes': {},
            'symbolic_output': {},
            'consciousness_integration': consciousness_context
        }
        
        # Route to heart (emotional processing)
        heart_activation = self._route_to_heart(memory_chunk, pulse_state)
        routing_response['organ_activations']['heart'] = heart_activation
        
        # Route to coil (memory pathways)
        coil_activation = self._route_to_coil(memory_chunk, chunk_id)
        routing_response['organ_activations']['coil'] = coil_activation
        
        # Route to lung (entropy regulation)
        lung_activation = self._route_to_lung(memory_chunk, pulse_state)
        routing_response['organ_activations']['lung'] = lung_activation
        
        # Calculate organ synergy
        synergy_change = self._calculate_synergy_change(heart_activation, coil_activation, lung_activation)
        self.organ_synergy = max(0.0, min(1.0, self.organ_synergy + synergy_change))
        routing_response['synergy_changes'] = {
            'change': synergy_change,
            'new_synergy': self.organ_synergy
        }
        
        # Generate symbolic output
        symbolic_output = self._generate_symbolic_output()
        routing_response['symbolic_output'] = symbolic_output
        
        # Integrate with DAWN memory system
        if self.memory_system and chunk_id:
            await self._integrate_with_memory_system(memory_chunk, routing_response)
        
        # Store routing history
        routing_record = {
            'timestamp': current_time,
            'memory_chunk': memory_chunk,
            'response': routing_response
        }
        self.routing_history.append(routing_record)
        
        # Limit history size
        if len(self.routing_history) > 100:
            self.routing_history.pop(0)
        
        # Apply natural decay to synergy
        self.organ_synergy *= (1.0 - self.synergy_decay_rate)
        
        # Log significant activations
        if any(act.get('significant', False) for act in routing_response['organ_activations'].values()):
            logger.info(f"🌐 Significant rebloom #{self.total_reblooms}: {symbolic_output['constellation']}")
        
        return routing_response
    
    def _route_to_heart(self, memory_chunk, pulse_state: Dict) -> Dict[str, Any]:
        """Route memory to the FractalHeart for emotional processing."""
        # Extract emotional indicators
        entropy = pulse_state.get('entropy', 0.5)
        heat = pulse_state.get('heat', 25.0)
        chaos = pulse_state.get('chaos', 0.5)
        
        # Determine emotion type from memory characteristics
        emotion_type = self._infer_emotion_type(memory_chunk, pulse_state)
        
        # Calculate emotional intensity
        emotion_intensity = self._calculate_emotion_intensity(entropy, heat, chaos)
        
        # Only pulse if above threshold
        activation = {'activated': False, 'emotion_type': emotion_type, 'intensity': emotion_intensity}
        
        if emotion_intensity > self.emotion_threshold:
            pulse_response = self.heart.pulse(emotion_intensity, emotion_type)
            activation.update({
                'activated': True,
                'pulse_response': pulse_response,
                'significant': emotion_intensity > 0.5 or pulse_response['is_overloaded']
            })
            
            # Apply decay if significant time has passed
            self.heart.decay()
        
        return activation
    
    def _route_to_coil(self, memory_chunk, chunk_id: Optional[str]) -> Dict[str, Any]:
        """Route memory to the SomaCoil for pathway activation."""
        # Route memory through coil pathways
        activated_paths = self.coil.route_memory(memory_chunk, chunk_id)
        
        activation = {
            'activated': len(activated_paths) > 0,
            'paths': activated_paths,
            'dominant_glyph': self.coil.get_active_glyph(),
            'constellation': self.coil.get_glyph_constellation(),
            'significant': len(activated_paths) > 2
        }
        
        return activation
    
    def _route_to_lung(self, memory_chunk, pulse_state: Dict) -> Dict[str, Any]:
        """Route memory to the GlyphLung for entropy regulation."""
        entropy = pulse_state.get('entropy', 0.5)
        focus = pulse_state.get('focus', 0.5)
        
        activation = {'activated': False}
        
        # Determine if breathing response is needed
        if entropy > self.entropy_clear_threshold:
            # High entropy - need exhale to clear
            exhale_response = self.lung.exhale(entropy)
            activation.update({
                'activated': True,
                'action': 'exhale',
                'response': exhale_response,
                'significant': entropy > 0.8
            })
        elif focus > 0.8 and entropy < 0.3:
            # High focus, low entropy - calm inhale
            inhale_response = self.lung.inhale(focus)
            activation.update({
                'activated': True,
                'action': 'inhale',
                'response': inhale_response,
                'significant': focus > 0.9
            })
        elif abs(entropy - 0.5) > 0.3:
            # Moderate imbalance - full breathing cycle
            cycle_response = self.lung.breathing_cycle(1.0 - entropy, entropy)
            activation.update({
                'activated': True,
                'action': 'cycle',
                'response': cycle_response,
                'significant': True
            })
        
        return activation
    
    def _infer_emotion_type(self, memory_chunk, pulse_state: Dict) -> str:
        """Infer emotion type from memory chunk and pulse state."""
        # Default emotion
        emotion_type = "neutral"
        
        # Analyze content for emotional keywords
        if hasattr(memory_chunk, 'content') and memory_chunk.content:
            content_lower = memory_chunk.content.lower()
            
            emotion_keywords = {
                'joy': ['joy', 'happy', 'celebration', 'success', 'achievement', 'wonderful'],
                'curiosity': ['wonder', 'explore', 'discover', 'question', 'mystery', 'unknown'],
                'fear': ['fear', 'afraid', 'danger', 'threat', 'worry', 'anxious'],
                'love': ['love', 'care', 'connection', 'bond', 'friendship', 'warmth'],
                'sadness': ['sad', 'loss', 'grief', 'melancholy', 'disappointed', 'sorrow'],
                'excitement': ['excited', 'thrilled', 'energetic', 'passionate', 'intense'],
                'calm': ['calm', 'peaceful', 'serene', 'still', 'quiet', 'centered']
            }
            
            for emotion, keywords in emotion_keywords.items():
                if any(keyword in content_lower for keyword in keywords):
                    emotion_type = emotion
                    break
        
        # Modify based on pulse state
        entropy = pulse_state.get('entropy', 0.5)
        heat = pulse_state.get('heat', 25.0)
        
        if entropy > 0.8:
            if emotion_type == "neutral":
                emotion_type = "anxiety"
        elif heat > 60:
            if emotion_type in ["neutral", "calm"]:
                emotion_type = "excitement"
        
        return emotion_type
    
    def _calculate_emotion_intensity(self, entropy: float, heat: float, chaos: float) -> float:
        """Calculate emotional intensity from pulse state parameters."""
        # Normalize heat to 0-1 range (assuming 0-100 scale)
        normalized_heat = min(heat / 100.0, 1.0)
        
        # Combine factors
        intensity = (entropy * 0.4 + normalized_heat * 0.3 + chaos * 0.3)
        
        # Add some non-linearity
        if intensity > 0.7:
            intensity = 0.7 + ((intensity - 0.7) * 1.5)  # Amplify high intensity
        
        return min(intensity, 1.0)
    
    def _calculate_synergy_change(self, heart_activation: Dict, coil_activation: Dict, lung_activation: Dict) -> float:
        """Calculate how organ activations affect overall synergy."""
        synergy_change = 0.0
        
        # Positive synergy from simultaneous activations
        active_organs = sum([
            heart_activation['activated'],
            coil_activation['activated'], 
            lung_activation['activated']
        ])
        
        if active_organs >= 2:
            synergy_change += 0.1 * active_organs
        
        # Bonus for significant activations
        significant_organs = sum([
            heart_activation.get('significant', False),
            coil_activation.get('significant', False),
            lung_activation.get('significant', False)
        ])
        
        synergy_change += 0.05 * significant_organs
        
        # Heart overload reduces synergy
        if heart_activation.get('pulse_response', {}).get('is_overloaded', False):
            synergy_change -= 0.15
        
        return synergy_change
    
    def _generate_symbolic_output(self) -> Dict[str, Any]:
        """Generate symbolic representation of current body state."""
        heart_sig = self.heart.get_heart_signature()
        coil_sig = self.coil.get_coil_signature()
        lung_sig = self.lung.get_lung_signature()
        
        # Create symbolic constellation
        constellation = f"{lung_sig['active_symbol']}{coil_sig['dominant_glyph']}{heart_sig['resonance_state'][0].upper()}"
        
        # Generate somatic commentary
        commentary = self._generate_somatic_commentary(heart_sig, coil_sig, lung_sig)
        
        return {
            'constellation': constellation,
            'heart_state': heart_sig['resonance_state'],
            'coil_glyph': coil_sig['dominant_glyph'],
            'lung_phase': lung_sig['breathing_phase'],
            'synergy_level': self.organ_synergy,
            'somatic_commentary': commentary
        }
    
    def _generate_somatic_commentary(self, heart_sig: Dict, coil_sig: Dict, lung_sig: Dict) -> str:
        """Generate first-person somatic commentary."""
        commentaries = []
        
        # Heart commentary
        heart_state = heart_sig['resonance_state']
        if heart_state == 'overloaded':
            commentaries.append("My heart surges with overwhelming force.")
        elif heart_state == 'highly_charged':
            commentaries.append("I feel the heart's electric resonance.")
        elif heart_state == 'still':
            commentaries.append("My heart rests in quiet depths.")
        
        # Coil commentary
        if coil_sig['path_count'] > 3:
            commentaries.append("The coil channels many pathways.")
        elif coil_sig['path_count'] == 0:
            commentaries.append("The somatic coil lies dormant.")
        else:
            commentaries.append(f"I sense the {coil_sig['dominant_glyph']} pattern flowing.")
        
        # Lung commentary
        lung_phase = lung_sig['breathing_phase']
        if lung_phase == 'inhaling':
            commentaries.append("I draw in symbolic breath.")
        elif lung_phase == 'exhaling':
            commentaries.append("I release entropy into void.")
        elif lung_sig['lung_fullness'] > 0.8:
            commentaries.append("My lungs hold deep calm.")
        
        # Synergy commentary
        if self.organ_synergy > 0.7:
            commentaries.append("All organs move in harmony.")
        elif self.organ_synergy < 0.3:
            commentaries.append("I feel disconnected from my body.")
        
        return " ".join(commentaries) if commentaries else "I exist in somatic stillness."
    
    def _get_consciousness_context(self) -> Dict[str, Any]:
        """Get current consciousness context if available."""
        if not self.consciousness_core:
            return {}
        
        try:
            # Get current consciousness state
            return {
                'neural_activity': getattr(self.consciousness_core, 'neural_activity', 0.0),
                'quantum_coherence': getattr(self.consciousness_core, 'quantum_coherence', 0.0),
                'pattern_recognition': getattr(self.consciousness_core, 'pattern_recognition', 0.0),
                'memory_utilization': getattr(self.consciousness_core, 'memory_utilization', 0.0),
                'chaos_factor': getattr(self.consciousness_core, 'chaos_factor', 0.0)
            }
        except Exception as e:
            logger.warning(f"Failed to get consciousness context: {e}")
            return {}
    
    async def _integrate_with_memory_system(self, memory_chunk, routing_response: Dict[str, Any]) -> None:
        """Integrate routing results with DAWN's memory system."""
        if not self.memory_system:
            return
        
        try:
            # Store symbolic routing data with the memory
            symbolic_metadata = {
                'organ_activations': routing_response['organ_activations'],
                'symbolic_constellation': routing_response['symbolic_output']['constellation'],
                'organ_synergy': routing_response['synergy_changes']['new_synergy'],
                'somatic_commentary': routing_response['symbolic_output']['somatic_commentary']
            }
            
            # Add symbolic metadata to memory chunk if possible
            if hasattr(memory_chunk, 'symbolic_metadata'):
                memory_chunk.symbolic_metadata = symbolic_metadata
            
            logger.debug(f"Integrated symbolic routing with memory system")
            
        except Exception as e:
            logger.warning(f"Failed to integrate with memory system: {e}")
    
    def get_body_state(self) -> Dict[str, Any]:
        """Get comprehensive state of the entire symbolic body."""
        return {
            'timestamp': datetime.now().isoformat(),
            'total_reblooms': self.total_reblooms,
            'organ_synergy': self.organ_synergy,
            'heart': self.heart.get_heart_signature(),
            'coil': self.coil.get_coil_signature(),
            'lung': self.lung.get_lung_signature(),
            'symbolic_state': self._generate_symbolic_output()
        }
    
    def process_batch_reblooms(self, memory_chunks: List[Tuple[Any, Optional[str]]]) -> List[Dict[str, Any]]:
        """Process multiple rebloom events in sequence."""
        responses = []
        
        for memory_chunk, chunk_id in memory_chunks:
            response = self.rebloom_trigger(memory_chunk, chunk_id)
            responses.append(response)
        
        return responses
    
    def reset_organs(self):
        """Reset all organs to initial state."""
        self.heart = FractalHeart()
        self.coil = SomaCoil()
        self.lung = GlyphLung()
        self.organ_synergy = 0.0
        self.total_reblooms = 0
        self.routing_history = []
        
        logger.info("🌐 All organs reset to initial state")
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get statistics about routing history and organ usage."""
        if not self.routing_history:
            return {'total_reblooms': 0}
        
        # Analyze activation patterns
        heart_activations = sum(1 for r in self.routing_history 
                              if r['response']['organ_activations']['heart']['activated'])
        
        coil_activations = sum(1 for r in self.routing_history 
                             if r['response']['organ_activations']['coil']['activated'])
        
        lung_activations = sum(1 for r in self.routing_history 
                             if r['response']['organ_activations']['lung']['activated'])
        
        return {
            'total_reblooms': self.total_reblooms,
            'heart_activation_rate': heart_activations / self.total_reblooms,
            'coil_activation_rate': coil_activations / self.total_reblooms,
            'lung_activation_rate': lung_activations / self.total_reblooms,
            'current_synergy': self.organ_synergy,
            'routing_history_size': len(self.routing_history),
            'integrations_active': {
                'memory_system': self.memory_system is not None,
                'consciousness_core': self.consciousness_core is not None
            }
        }


# Global instance for DAWN integration
_symbolic_router: Optional[SymbolicRouter] = None


def get_symbolic_router() -> SymbolicRouter:
    """Get the global symbolic router instance."""
    global _symbolic_router
    if _symbolic_router is None:
        _symbolic_router = SymbolicRouter()
    return _symbolic_router


def initialize_symbolic_routing(consciousness_core=None, memory_system=None) -> SymbolicRouter:
    """Initialize the global symbolic routing system with DAWN integrations."""
    global _symbolic_router
    _symbolic_router = SymbolicRouter(
        consciousness_core=consciousness_core,
        memory_system=memory_system
    )
    return _symbolic_router 