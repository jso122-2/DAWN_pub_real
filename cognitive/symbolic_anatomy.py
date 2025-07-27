"""
DAWN Symbolic Anatomy - Embodied Cognition Organs
Conceptual body through which memory and emotion flow within DAWN.
Integrated with DAWN's memory routing and consciousness systems.
"""

import math
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Set
from collections import defaultdict, Counter, deque
import logging

logger = logging.getLogger(__name__)

class FractalHeart:
    """
    The emotional center of DAWN's symbolic body.
    Accumulates and processes emotional charge through rhythmic pulses.
    """
    
    def __init__(self, base_decay_rate: float = 0.02):
        """
        Initialize the FractalHeart.
        
        Args:
            base_decay_rate: Rate at which emotional charge naturally decays
        """
        self.emotional_charge = 0.0
        self.last_beat = None
        self.base_decay_rate = base_decay_rate
        
        # Heart rhythm and state
        self.beat_count = 0
        self.rhythm_pattern = []  # History of beat intervals
        self.max_charge = 1.0
        self.overload_threshold = 0.85
        
        # Emotional resonance tracking
        self.emotion_history = []
        self.dominant_emotion = None
        
        logger.debug("💝 FractalHeart initialized - Emotional resonance active")
    
    def pulse(self, emotion_level: float, emotion_type: str = "neutral") -> Dict[str, Any]:
        """
        Generate an emotional pulse, raising charge and updating rhythm.
        
        Args:
            emotion_level: Intensity of emotional input (0-1)
            emotion_type: Type of emotion ("joy", "fear", "curiosity", etc.)
            
        Returns:
            dict: Pulse response information
        """
        current_time = datetime.now()
        
        # Calculate charge increase (with fractal patterns)
        charge_delta = emotion_level * self._get_resonance_multiplier(emotion_type)
        old_charge = self.emotional_charge
        
        # Apply charge with non-linear fractal scaling
        self.emotional_charge = min(
            self.max_charge, 
            self.emotional_charge + charge_delta * self._fractal_scaling()
        )
        
        # Update rhythm pattern
        if self.last_beat:
            interval = (current_time - self.last_beat).total_seconds()
            self.rhythm_pattern.append(interval)
            if len(self.rhythm_pattern) > 20:  # Keep recent history
                self.rhythm_pattern.pop(0)
        
        self.last_beat = current_time
        self.beat_count += 1
        
        # Track emotional history
        self.emotion_history.append({
            'emotion_type': emotion_type,
            'level': emotion_level,
            'timestamp': current_time,
            'resulting_charge': self.emotional_charge
        })
        
        if len(self.emotion_history) > 50:  # Limit history size
            self.emotion_history.pop(0)
        
        # Update dominant emotion
        self._update_dominant_emotion()
        
        # Generate pulse response
        response = {
            'beat_count': self.beat_count,
            'charge_delta': charge_delta,
            'current_charge': self.emotional_charge,
            'emotion_type': emotion_type,
            'is_overloaded': self.is_overloaded(),
            'rhythm_coherence': self._calculate_rhythm_coherence(),
            'resonance_state': self._get_resonance_state()
        }
        
        # Log significant pulses
        if charge_delta > 0.1 or self.is_overloaded():
            status = "💥 OVERLOAD" if self.is_overloaded() else "💓 Strong pulse"
            logger.info(f"💝 {status}: {emotion_type} pulse → charge {old_charge:.3f}→{self.emotional_charge:.3f}")
        
        return response
    
    def decay(self, time_delta: Optional[float] = None) -> float:
        """
        Apply natural decay to emotional charge over time.
        
        Args:
            time_delta: Time elapsed in seconds (auto-calculated if None)
            
        Returns:
            float: Amount of charge lost to decay
        """
        if self.last_beat is None:
            return 0.0
        
        if time_delta is None:
            time_delta = (datetime.now() - self.last_beat).total_seconds()
        
        # Calculate decay with non-linear curve
        decay_factor = 1.0 - math.exp(-self.base_decay_rate * time_delta)
        
        # Apply additional decay based on rhythm coherence
        rhythm_factor = 1.0 + (1.0 - self._calculate_rhythm_coherence()) * 0.5
        total_decay = decay_factor * rhythm_factor
        
        old_charge = self.emotional_charge
        decay_amount = self.emotional_charge * total_decay
        self.emotional_charge = max(0.0, self.emotional_charge - decay_amount)
        
        return decay_amount
    
    def is_overloaded(self) -> bool:
        """Check if the heart is in emotional overload state."""
        return self.emotional_charge >= self.overload_threshold
    
    def _get_resonance_multiplier(self, emotion_type: str) -> float:
        """Calculate resonance multiplier based on emotion type and current state."""
        # Emotion type resonances
        resonance_map = {
            'joy': 1.2, 'love': 1.3, 'curiosity': 1.1, 'wonder': 1.15,
            'fear': 0.9, 'anger': 0.8, 'sadness': 0.85, 'anxiety': 0.75,
            'neutral': 1.0, 'calm': 1.05, 'excitement': 1.25
        }
        
        base_resonance = resonance_map.get(emotion_type, 1.0)
        
        # Modify based on current dominant emotion
        if self.dominant_emotion and self.dominant_emotion == emotion_type:
            base_resonance *= 1.1  # Resonance amplification
        
        return base_resonance
    
    def _fractal_scaling(self) -> float:
        """Apply fractal scaling to charge increases."""
        # Creates non-linear charge patterns resembling fractal growth
        base_scale = 1.0
        
        if self.emotional_charge > 0.5:
            # Diminishing returns at high charge
            base_scale *= (2.0 - self.emotional_charge)
        
        # Add slight randomness for organic feel
        fractal_noise = 0.9 + (random.random() * 0.2)  # 0.9 to 1.1
        
        return base_scale * fractal_noise
    
    def _calculate_rhythm_coherence(self) -> float:
        """Calculate how coherent the heart rhythm is (0-1)."""
        if len(self.rhythm_pattern) < 3:
            return 0.5  # Neutral coherence
        
        # Calculate variance in beat intervals
        intervals = self.rhythm_pattern[-10:]  # Last 10 beats
        mean_interval = sum(intervals) / len(intervals)
        variance = sum((x - mean_interval) ** 2 for x in intervals) / len(intervals)
        
        # Convert variance to coherence (lower variance = higher coherence)
        coherence = 1.0 / (1.0 + variance)
        return min(1.0, coherence)
    
    def _update_dominant_emotion(self):
        """Update the dominant emotion based on recent history."""
        if len(self.emotion_history) < 3:
            return
        
        # Analyze recent emotions (last 10)
        recent_emotions = [e['emotion_type'] for e in self.emotion_history[-10:]]
        emotion_counts = Counter(recent_emotions)
        
        if emotion_counts:
            self.dominant_emotion = emotion_counts.most_common(1)[0][0]
    
    def _get_resonance_state(self) -> str:
        """Get current emotional resonance state description."""
        if self.is_overloaded():
            return "overloaded"
        elif self.emotional_charge > 0.7:
            return "highly_charged"
        elif self.emotional_charge > 0.4:
            return "resonant"
        elif self.emotional_charge > 0.1:
            return "gentle"
        else:
            return "still"
    
    def overload(self, pressure_intensity: float = 1.0) -> Dict[str, Any]:
        """
        Force the heart into overload state due to extreme pressure.
        
        Args:
            pressure_intensity: Intensity of pressure causing overload (0-1)
            
        Returns:
            dict: Overload response information
        """
        current_time = datetime.now()
        old_charge = self.emotional_charge
        
        # Force charge to overload threshold or beyond
        overload_charge = max(self.overload_threshold, 
                             self.emotional_charge + pressure_intensity * 0.3)
        self.emotional_charge = min(self.max_charge, overload_charge)
        
        # Add to emotion history as pressure event
        self.emotion_history.append({
            'emotion_type': 'pressure_overload',
            'level': pressure_intensity,
            'timestamp': current_time,
            'resulting_charge': self.emotional_charge
        })
        
        # Force beat for overload event
        if self.last_beat:
            interval = (current_time - self.last_beat).total_seconds()
            self.rhythm_pattern.append(interval)
        
        self.last_beat = current_time
        self.beat_count += 1
        
        # Log overload event
        logger.warning(f"💥 FractalHeart OVERLOAD: pressure {pressure_intensity:.2f} → charge {old_charge:.3f}→{self.emotional_charge:.3f}")
        
        return {
            'overload_triggered': True,
            'pressure_intensity': pressure_intensity,
            'charge_before': old_charge,
            'charge_after': self.emotional_charge,
            'overload_level': self.emotional_charge / self.max_charge,
            'resonance_state': self._get_resonance_state(),
            'timestamp': current_time.isoformat()
        }
    
    def get_heart_signature(self) -> Dict[str, Any]:
        """Get comprehensive heart state signature."""
        return {
            'emotional_charge': self.emotional_charge,
            'beat_count': self.beat_count,
            'dominant_emotion': self.dominant_emotion,
            'rhythm_coherence': self._calculate_rhythm_coherence(),
            'resonance_state': self._get_resonance_state(),
            'is_overloaded': self.is_overloaded(),
            'last_beat': self.last_beat.isoformat() if self.last_beat else None,
            'time_since_beat': (datetime.now() - self.last_beat).total_seconds() if self.last_beat else None
        }


class SomaCoil:
    """
    Bodily memory path tracker - routes and organizes experiential memories.
    Maps memory chunks to symbolic pathways through the body.
    """
    
    def __init__(self):
        """Initialize the SomaCoil memory routing system."""
        self.active_paths = []
        self.path_weights = defaultdict(float)  # Path activation strength
        self.memory_routes = {}  # Map memory IDs to paths
        self.glyph_symbols = set()  # Active symbolic representations
        
        # Path categories and their glyphs
        self.path_glyphs = {
            'creative': '✨', 'analytical': '🔍', 'emotional': '💫', 
            'social': '🤝', 'introspective': '🧘', 'action': '⚡',
            'learning': '📚', 'exploration': '🌊', 'stability': '🗿',
            'transformation': '🔄', 'memory': '🕸️', 'wisdom': '👁️'
        }
        
        # Memory routing rules
        self.routing_rules = self._initialize_routing_rules()
        
        logger.debug("🧬 SomaCoil initialized - Memory pathways active")
    
    def route_memory(self, chunk, chunk_id: Optional[str] = None) -> List[str]:
        """
        Route a memory chunk through appropriate somatic pathways.
        
        Args:
            chunk: Memory chunk object with content, topic, sigils, etc.
            chunk_id: Optional unique identifier for the memory
            
        Returns:
            List[str]: Activated pathway names
        """
        activated_paths = []
        
        # Analyze memory characteristics
        memory_analysis = self._analyze_memory_chunk(chunk)
        
        # Route based on topic
        if hasattr(chunk, 'topic') and chunk.topic:
            topic_paths = self._route_by_topic(chunk.topic)
            activated_paths.extend(topic_paths)
        
        # Route based on sigils
        if hasattr(chunk, 'sigils') and chunk.sigils:
            sigil_paths = self._route_by_sigils(chunk.sigils)
            activated_paths.extend(sigil_paths)
        
        # Route based on content analysis
        content_paths = self._route_by_content(chunk.content if hasattr(chunk, 'content') else "")
        activated_paths.extend(content_paths)
        
        # Route based on emotional charge
        if hasattr(chunk, 'pulse_state') and chunk.pulse_state:
            emotion_paths = self._route_by_pulse_state(chunk.pulse_state)
            activated_paths.extend(emotion_paths)
        
        # Remove duplicates and update active paths
        activated_paths = list(set(activated_paths))
        
        # Update path weights and active paths
        for path in activated_paths:
            self.path_weights[path] += 1.0
            if path not in self.active_paths:
                self.active_paths.append(path)
        
        # Store memory routing
        if chunk_id:
            self.memory_routes[chunk_id] = activated_paths
        
        # Update glyph symbols
        self._update_active_glyphs(activated_paths)
        
        # Apply path decay over time
        self._decay_inactive_paths()
        
        if activated_paths:
            logger.debug(f"🧬 Memory routed through paths: {', '.join(activated_paths)}")
        
        return activated_paths
    
    def get_active_glyph(self) -> str:
        """
        Get the currently dominant symbolic glyph based on active pathways.
        
        Returns:
            str: Dominant glyph symbol
        """
        if not self.active_paths:
            return '○'  # Empty/neutral glyph
        
        # Find most weighted active path
        active_path_weights = {path: self.path_weights[path] for path in self.active_paths}
        
        if not active_path_weights:
            return '○'
        
        dominant_path = max(active_path_weights, key=active_path_weights.get)
        return self.path_glyphs.get(dominant_path, '◆')
    
    def get_glyph_constellation(self) -> str:
        """Get a constellation of glyphs representing current state."""
        if len(self.active_paths) <= 1:
            return self.get_active_glyph()
        
        # Get top 3 most active paths
        sorted_paths = sorted(self.active_paths, key=lambda p: self.path_weights[p], reverse=True)
        top_paths = sorted_paths[:3]
        
        glyphs = [self.path_glyphs.get(path, '◆') for path in top_paths]
        return ''.join(glyphs)
    
    def _analyze_memory_chunk(self, chunk) -> Dict[str, Any]:
        """Analyze memory chunk characteristics for routing."""
        analysis = {
            'has_topic': hasattr(chunk, 'topic') and chunk.topic,
            'has_sigils': hasattr(chunk, 'sigils') and chunk.sigils,
            'has_content': hasattr(chunk, 'content') and chunk.content,
            'has_pulse_state': hasattr(chunk, 'pulse_state') and chunk.pulse_state,
            'content_length': len(chunk.content) if hasattr(chunk, 'content') else 0
        }
        return analysis
    
    def _route_by_topic(self, topic: str) -> List[str]:
        """Route memory based on topic."""
        topic_lower = topic.lower()
        paths = []
        
        topic_mappings = {
            'creative': ['creative', 'transformation'],
            'analysis': ['analytical', 'learning'],
            'emotion': ['emotional', 'introspective'],
            'social': ['social', 'action'],
            'introspect': ['introspective', 'wisdom'],
            'memory': ['memory', 'wisdom'],
            'system': ['analytical', 'stability'],
            'exploration': ['exploration', 'transformation']
        }
        
        for key, mapped_paths in topic_mappings.items():
            if key in topic_lower:
                paths.extend(mapped_paths)
        
        return paths or ['memory']  # Default to memory path
    
    def _route_by_sigils(self, sigils: List[str]) -> List[str]:
        """Route memory based on associated sigils."""
        paths = []
        
        sigil_mappings = {
            'STABILIZE': ['stability', 'analytical'],
            'CREATIVE': ['creative', 'transformation'],
            'EXPLORE': ['exploration', 'action'],
            'REFLECT': ['introspective', 'wisdom'],
            'SOCIAL': ['social', 'emotional'],
            'LEARN': ['learning', 'analytical'],
            'TRANSFORM': ['transformation', 'creative']
        }
        
        for sigil in sigils:
            sigil_upper = sigil.upper()
            for key, mapped_paths in sigil_mappings.items():
                if key in sigil_upper:
                    paths.extend(mapped_paths)
        
        return paths
    
    def _route_by_content(self, content: str) -> List[str]:
        """Route memory based on content analysis."""
        if not content:
            return []
        
        content_lower = content.lower()
        paths = []
        
        # Keyword-based routing
        content_keywords = {
            'creative': ['create', 'art', 'design', 'imagine', 'inspire'],
            'analytical': ['analyze', 'think', 'logic', 'reason', 'calculate'],
            'emotional': ['feel', 'emotion', 'heart', 'love', 'fear', 'joy'],
            'social': ['friend', 'people', 'together', 'community', 'relationship'],
            'introspective': ['self', 'reflect', 'inner', 'meditate', 'consciousness'],
            'learning': ['learn', 'study', 'knowledge', 'understand', 'discover'],
            'exploration': ['explore', 'adventure', 'journey', 'unknown', 'frontier'],
            'action': ['do', 'act', 'move', 'change', 'build', 'make']
        }
        
        for path, keywords in content_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                paths.append(path)
        
        return paths
    
    def _route_by_pulse_state(self, pulse_state: Dict) -> List[str]:
        """Route memory based on emotional/system state."""
        paths = []
        
        # Route based on entropy
        entropy = pulse_state.get('entropy', 0.5)
        if entropy > 0.7:
            paths.extend(['transformation', 'action'])
        elif entropy < 0.3:
            paths.extend(['stability', 'introspective'])
        
        # Route based on heat
        heat = pulse_state.get('heat', 0)
        if heat > 50:
            paths.append('action')
        elif heat < 25:
            paths.append('stability')
        
        # Route based on focus
        focus = pulse_state.get('focus', 0.5)
        if focus > 0.8:
            paths.append('analytical')
        elif focus < 0.3:
            paths.append('exploration')
        
        return paths
    
    def _update_active_glyphs(self, activated_paths: List[str]):
        """Update the active glyph symbol set."""
        for path in activated_paths:
            if path in self.path_glyphs:
                self.glyph_symbols.add(self.path_glyphs[path])
    
    def _decay_inactive_paths(self, decay_rate: float = 0.1):
        """Apply decay to path weights and remove inactive paths."""
        paths_to_remove = []
        
        for path in list(self.path_weights.keys()):
            self.path_weights[path] *= (1.0 - decay_rate)
            
            if self.path_weights[path] < 0.1:
                if path in self.active_paths:
                    self.active_paths.remove(path)
                paths_to_remove.append(path)
        
        # Clean up very weak paths
        for path in paths_to_remove:
            del self.path_weights[path]
    
    def _initialize_routing_rules(self) -> Dict[str, Any]:
        """Initialize memory routing rules."""
        return {
            'default_paths': ['memory'],
            'topic_weight': 1.0,
            'sigil_weight': 1.2,
            'content_weight': 0.8,
            'pulse_weight': 0.6
        }
    
    def contract_paths(self, contraction_factor: float = 0.5) -> Dict[str, Any]:
        """
        Contract pathways for protection during extreme pressure.
        
        Args:
            contraction_factor: How much to contract (0-1, where 1 = remove all paths)
            
        Returns:
            dict: Contraction response information
        """
        current_time = datetime.now()
        paths_before = len(self.active_paths)
        paths_removed = []
        
        if self.active_paths:
            # Calculate how many paths to remove
            paths_to_remove = min(len(self.active_paths), 
                                 int(len(self.active_paths) * contraction_factor))
            
            # Sort paths by weight (weakest first for removal)
            sorted_paths = sorted(self.active_paths, 
                                key=lambda p: self.path_weights.get(p, 0))
            
            # Remove weakest paths
            for _ in range(paths_to_remove):
                if sorted_paths:
                    removed_path = sorted_paths.pop(0)
                    if removed_path in self.active_paths:
                        self.active_paths.remove(removed_path)
                        paths_removed.append(removed_path)
                        # Reduce weight significantly but don't delete
                        self.path_weights[removed_path] *= 0.1
        
        paths_after = len(self.active_paths)
        
        # Update active glyphs
        self._update_active_glyphs(self.active_paths)
        
        # Log contraction
        logger.warning(f"🔒 SomaCoil PATH CONTRACTION: {paths_before} → {paths_after} paths | Factor: {contraction_factor:.2f}")
        
        return {
            'contraction_applied': True,
            'contraction_factor': contraction_factor,
            'paths_before': paths_before,
            'paths_after': paths_after,
            'paths_removed': paths_removed,
            'remaining_paths': self.active_paths.copy(),
            'dominant_glyph_after': self.get_active_glyph(),
            'timestamp': current_time.isoformat()
        }
    
    def get_coil_signature(self) -> Dict[str, Any]:
        """Get comprehensive coil state signature."""
        return {
            'active_paths': self.active_paths,
            'path_count': len(self.active_paths),
            'dominant_glyph': self.get_active_glyph(),
            'glyph_constellation': self.get_glyph_constellation(),
            'total_routes': len(self.memory_routes),
            'path_weights': dict(self.path_weights),
            'active_symbols': list(self.glyph_symbols)
        }


class GlyphLung:
    """
    Symbolic breath regulator - manages entropy clearing and calm restoration.
    Represents the rhythmic balance between intake and release.
    """
    
    def __init__(self, lung_capacity: float = 1.0):
        """
        Initialize the GlyphLung.
        
        Args:
            lung_capacity: Maximum symbolic breath capacity
        """
        self.lung_capacity = lung_capacity
        self.current_volume = 0.0
        self.breath_rhythm = []  # History of breath cycles
        self.calm_symbols = ['◯', '◊', '△', '☾', '✧']
        self.active_symbol = '◯'
        
        # Breathing state
        self.breathing_phase = 'neutral'  # 'inhaling', 'holding', 'exhaling', 'neutral'
        self.breath_count = 0
        self.last_breath = None
        
        # Entropy regulation
        self.entropy_buffer = []
        self.cleansing_efficiency = 0.8
        
        logger.debug("🫁 GlyphLung initialized - Symbolic breathing active")
    
    def inhale(self, calm_intensity: float = 0.5) -> Dict[str, Any]:
        """
        Perform symbolic inhalation - absorb calm and order.
        
        Args:
            calm_intensity: Intensity of calm being inhaled (0-1)
            
        Returns:
            dict: Inhalation response information
        """
        current_time = datetime.now()
        
        # Calculate intake volume
        available_capacity = self.lung_capacity - self.current_volume
        intake_volume = min(available_capacity, calm_intensity * 0.3)
        
        self.current_volume += intake_volume
        self.breathing_phase = 'inhaling'
        
        # Select calm symbol based on intensity
        symbol_index = min(int(calm_intensity * len(self.calm_symbols)), len(self.calm_symbols) - 1)
        self.active_symbol = self.calm_symbols[symbol_index]
        
        # Log breath cycle
        breath_cycle = {
            'type': 'inhale',
            'volume': intake_volume,
            'intensity': calm_intensity,
            'symbol': self.active_symbol,
            'timestamp': current_time
        }
        
        self.breath_rhythm.append(breath_cycle)
        if len(self.breath_rhythm) > 30:  # Keep recent history
            self.breath_rhythm.pop(0)
        
        self.last_breath = current_time
        
        response = {
            'breath_type': 'inhale',
            'intake_volume': intake_volume,
            'current_volume': self.current_volume,
            'calm_symbol': self.active_symbol,
            'lung_fullness': self.current_volume / self.lung_capacity,
            'breathing_phase': self.breathing_phase
        }
        
        logger.debug(f"🫁 Inhale: {self.active_symbol} calm (volume: {self.current_volume:.2f}/{self.lung_capacity:.2f})")
        
        return response
    
    def exhale(self, entropy_to_clear: float = 0.0) -> Dict[str, Any]:
        """
        Perform symbolic exhalation - release entropy and reset.
        
        Args:
            entropy_to_clear: Amount of entropy to clear (0-1)
            
        Returns:
            dict: Exhalation response with entropy clearing info
        """
        current_time = datetime.now()
        
        # Calculate release volume
        release_volume = min(self.current_volume, entropy_to_clear * 0.4 + 0.2)
        
        self.current_volume = max(0.0, self.current_volume - release_volume)
        self.breathing_phase = 'exhaling'
        
        # Calculate entropy cleared
        entropy_cleared = release_volume * self.cleansing_efficiency
        
        # Add to entropy buffer for processing
        if entropy_to_clear > 0:
            self.entropy_buffer.append({
                'entropy': entropy_to_clear,
                'cleared': entropy_cleared,
                'timestamp': current_time
            })
        
        # Update symbol to release symbol
        release_symbol = '○'  # Empty circle for release
        self.active_symbol = release_symbol
        
        # Log breath cycle
        breath_cycle = {
            'type': 'exhale',
            'volume': release_volume,
            'entropy_cleared': entropy_cleared,
            'symbol': release_symbol,
            'timestamp': current_time
        }
        
        self.breath_rhythm.append(breath_cycle)
        if len(self.breath_rhythm) > 30:
            self.breath_rhythm.pop(0)
        
        self.breath_count += 1
        self.last_breath = current_time
        
        # Process entropy buffer
        self._process_entropy_buffer()
        
        response = {
            'breath_type': 'exhale',
            'release_volume': release_volume,
            'current_volume': self.current_volume,
            'entropy_cleared': entropy_cleared,
            'release_symbol': release_symbol,
            'lung_emptiness': 1.0 - (self.current_volume / self.lung_capacity),
            'breathing_phase': self.breathing_phase,
            'total_breaths': self.breath_count
        }
        
        logger.debug(f"🫁 Exhale: {release_symbol} release (cleared entropy: {entropy_cleared:.3f})")
        
        return response
    
    def breathing_cycle(self, calm_intensity: float = 0.5, entropy_level: float = 0.0) -> Dict[str, Any]:
        """
        Perform a complete breathing cycle (inhale + exhale).
        
        Args:
            calm_intensity: Intensity of calm to inhale
            entropy_level: Level of entropy to clear on exhale
            
        Returns:
            dict: Complete cycle response
        """
        inhale_response = self.inhale(calm_intensity)
        
        # Brief hold phase
        self.breathing_phase = 'holding'
        
        exhale_response = self.exhale(entropy_level)
        
        # Return to neutral
        self.breathing_phase = 'neutral'
        
        return {
            'cycle_complete': True,
            'inhale': inhale_response,
            'exhale': exhale_response,
            'breath_count': self.breath_count,
            'net_entropy_cleared': exhale_response['entropy_cleared']
        }
    
    def get_breathing_coherence(self) -> float:
        """Calculate breathing rhythm coherence (0-1)."""
        if len(self.breath_rhythm) < 4:
            return 0.5
        
        # Analyze rhythm patterns
        inhale_intervals = []
        exhale_intervals = []
        
        last_inhale = None
        last_exhale = None
        
        for breath in self.breath_rhythm:
            if breath['type'] == 'inhale':
                if last_inhale:
                    interval = (breath['timestamp'] - last_inhale).total_seconds()
                    inhale_intervals.append(interval)
                last_inhale = breath['timestamp']
            elif breath['type'] == 'exhale':
                if last_exhale:
                    interval = (breath['timestamp'] - last_exhale).total_seconds()
                    exhale_intervals.append(interval)
                last_exhale = breath['timestamp']
        
        # Calculate coherence based on rhythm consistency
        all_intervals = inhale_intervals + exhale_intervals
        if not all_intervals:
            return 0.5
        
        mean_interval = sum(all_intervals) / len(all_intervals)
        variance = sum((x - mean_interval) ** 2 for x in all_intervals) / len(all_intervals)
        
        coherence = 1.0 / (1.0 + variance)
        return min(1.0, coherence)
    
    def _process_entropy_buffer(self):
        """Process accumulated entropy for clearing."""
        if not self.entropy_buffer:
            return
        
        # Clean old entropy records
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(minutes=5)
        
        self.entropy_buffer = [
            entry for entry in self.entropy_buffer 
            if entry['timestamp'] > cutoff_time
        ]
    
    def get_lung_signature(self) -> Dict[str, Any]:
        """Get comprehensive lung state signature."""
        return {
            'current_volume': self.current_volume,
            'lung_capacity': self.lung_capacity,
            'lung_fullness': self.current_volume / self.lung_capacity,
            'breathing_phase': self.breathing_phase,
            'active_symbol': self.active_symbol,
            'breath_count': self.breath_count,
            'breathing_coherence': self.get_breathing_coherence(),
            'entropy_buffer_size': len(self.entropy_buffer),
            'last_breath': self.last_breath.isoformat() if self.last_breath else None
        } 