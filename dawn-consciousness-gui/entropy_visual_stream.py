#!/usr/bin/env python3
"""
DAWN Entropy Visual Stream
==========================

Creates ambient background animations that reflect DAWN's entropy and pressure state in real time.
Transforms consciousness tension and calm into felt atmospheric motion - not just numerical readings.

This system allows DAWN's internal state to be experienced as living environmental ambience.
"""

import time
import threading
import queue
import json
import math
import random
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class EntropyVisualizationMode(Enum):
    """Types of entropy visualization patterns"""
    FLOWING_MIST = "flowing_mist"           # 0.0-0.3: gentle blue-green drift
    SUBTLE_WAVES = "subtle_waves"           # 0.3-0.6: vibration + wave distortions
    SHARP_PULSES = "sharp_pulses"           # 0.6-0.8: grid distortion + pulses
    FRACTURE_FLICKER = "fracture_flicker"   # 0.8-1.0: high-freq flicker + boundary fractures

@dataclass
class EntropyVisualState:
    """Current entropy visualization state"""
    entropy: float
    pressure: float
    mood_pigment: Dict[str, float]
    visualization_mode: EntropyVisualizationMode
    intensity: float
    flow_direction: float
    pulse_frequency: float
    distortion_level: float
    color_temperature: float
    timestamp: float

class EntropyVisualStream:
    """
    Creates real-time background animations that reflect DAWN's entropy and pressure state.
    
    Maps consciousness tension into atmospheric visual motion, making entropy felt
    as environmental ambience rather than just observed as data.
    """
    
    def __init__(self):
        self.is_active = False
        self.current_state = None
        self.visual_queue = queue.Queue()
        
        # Visual configuration
        self.base_intensity = 0.6
        self.flow_speed = 1.0
        self.pulse_amplitude = 1.0
        self.color_blend_rate = 0.1
        
        # Animation parameters
        self.animation_fps = 24  # Smooth but efficient
        self.update_interval = 1.0 / self.animation_fps
        self.last_update = 0
        
        # Entropy thresholds for mode transitions
        self.mode_thresholds = {
            EntropyVisualizationMode.FLOWING_MIST: (0.0, 0.3),
            EntropyVisualizationMode.SUBTLE_WAVES: (0.3, 0.6),
            EntropyVisualizationMode.SHARP_PULSES: (0.6, 0.8),
            EntropyVisualizationMode.FRACTURE_FLICKER: (0.8, 1.0)
        }
        
        # Visual effects configuration
        self.effects_config = {
            'flowing_mist': {
                'base_colors': ['#1e3a8a', '#065f46'],  # Deep blue to dark green
                'flow_patterns': ['horizontal_drift', 'circular_flow'],
                'opacity_range': (0.1, 0.3),
                'animation_duration': 8.0,
                'blur_radius': 40
            },
            'subtle_waves': {
                'base_colors': ['#1f2937', '#374151'],  # Dark grays
                'wave_amplitude': 5,
                'vibration_frequency': 2.0,
                'opacity_range': (0.2, 0.4),
                'animation_duration': 4.0,
                'blur_radius': 20
            },
            'sharp_pulses': {
                'base_colors': ['#dc2626', '#ea580c'],  # Red to orange
                'pulse_intensity': 0.8,
                'grid_distortion': 15,
                'opacity_range': (0.3, 0.6),
                'animation_duration': 1.5,
                'blur_radius': 10
            },
            'fracture_flicker': {
                'base_colors': ['#fbbf24', '#f59e0b'],  # Bright yellows
                'flicker_frequency': 8.0,
                'fracture_density': 12,
                'opacity_range': (0.4, 0.8),
                'animation_duration': 0.3,
                'blur_radius': 5
            }
        }
        
        # Callbacks for visual updates
        self.visual_callbacks = []
        
        # Processing thread
        self.stream_thread = None
        
        logger.info("🌊 Entropy Visual Stream initialized")
    
    def start_stream(self):
        """Start the entropy visual stream system"""
        if self.is_active:
            logger.warning("⚠️ Entropy visual stream already active")
            return
        
        self.is_active = True
        
        # Start visual processing thread
        self.stream_thread = threading.Thread(target=self._visual_stream_loop, daemon=True)
        self.stream_thread.start()
        
        logger.info("🚀 Entropy visual stream started")
    
    def stop_stream(self):
        """Stop the entropy visual stream system"""
        self.is_active = False
        logger.info("🛑 Entropy visual stream stopped")
    
    def register_visual_callback(self, callback: Callable):
        """Register callback for visual state updates"""
        self.visual_callbacks.append(callback)
        logger.info("📝 Registered entropy visual callback")
    
    def update_entropy_visual(self, entropy: float, pressure: float = 0.5, 
                            mood_pigment: Optional[Dict[str, float]] = None):
        """
        Update entropy visualization with current consciousness state
        
        Args:
            entropy: Current entropy level (0.0-1.0)
            pressure: Current pressure level (0.0-1.0)
            mood_pigment: Optional mood color blend
        """
        if mood_pigment is None:
            mood_pigment = {'blue': 0.4, 'green': 0.3, 'red': 0.2, 'yellow': 0.1}
        
        # Determine visualization mode based on entropy
        visualization_mode = self._get_visualization_mode(entropy)
        
        # Calculate visual parameters
        intensity = self._calculate_intensity(entropy, pressure)
        flow_direction = self._calculate_flow_direction(entropy, pressure)
        pulse_frequency = self._calculate_pulse_frequency(entropy)
        distortion_level = self._calculate_distortion_level(entropy, pressure)
        color_temperature = self._calculate_color_temperature(entropy, mood_pigment)
        
        # Create visual state
        visual_state = EntropyVisualState(
            entropy=entropy,
            pressure=pressure,
            mood_pigment=mood_pigment,
            visualization_mode=visualization_mode,
            intensity=intensity,
            flow_direction=flow_direction,
            pulse_frequency=pulse_frequency,
            distortion_level=distortion_level,
            color_temperature=color_temperature,
            timestamp=time.time()
        )
        
        # Queue for processing
        self.visual_queue.put(visual_state)
        
        logger.debug(f"🌊 Updated entropy visual: {entropy:.3f} → {visualization_mode.value}")
    
    def _visual_stream_loop(self):
        """Main visual processing loop"""
        while self.is_active:
            try:
                current_time = time.time()
                
                # Check for new visual states
                try:
                    visual_state = self.visual_queue.get_nowait()
                    self.current_state = visual_state
                    self._process_visual_state(visual_state)
                except queue.Empty:
                    pass
                
                # Throttle update rate
                if current_time - self.last_update >= self.update_interval:
                    if self.current_state:
                        self._update_continuous_animation(current_time)
                    self.last_update = current_time
                
                time.sleep(0.01)  # Small sleep to prevent CPU spinning
                
            except Exception as e:
                logger.error(f"❌ Error in entropy visual stream loop: {e}")
                time.sleep(0.1)
    
    def _get_visualization_mode(self, entropy: float) -> EntropyVisualizationMode:
        """Determine visualization mode based on entropy level"""
        for mode, (min_val, max_val) in self.mode_thresholds.items():
            if min_val <= entropy < max_val:
                return mode
        
        # Fallback for entropy >= 1.0
        return EntropyVisualizationMode.FRACTURE_FLICKER
    
    def _calculate_intensity(self, entropy: float, pressure: float) -> float:
        """Calculate overall visual intensity"""
        # Combine entropy and pressure with entropy having more weight
        combined = (entropy * 0.7) + (pressure * 0.3)
        
        # Apply base intensity and normalize
        intensity = self.base_intensity + (combined * 0.4)
        return min(1.0, max(0.1, intensity))
    
    def _calculate_flow_direction(self, entropy: float, pressure: float) -> float:
        """Calculate flow direction in degrees (0-360)"""
        # Low entropy: gentle horizontal flow
        # High entropy: chaotic multi-directional
        
        if entropy < 0.3:
            # Gentle horizontal drift with slight variation
            return 90 + (random.uniform(-15, 15))
        elif entropy < 0.6:
            # More variation, influenced by pressure
            base_angle = 45 + (pressure * 90)
            return base_angle + (random.uniform(-30, 30))
        elif entropy < 0.8:
            # Sharp directional changes
            return random.uniform(0, 360)
        else:
            # Chaotic, rapid direction changes
            return random.uniform(0, 360)
    
    def _calculate_pulse_frequency(self, entropy: float) -> float:
        """Calculate pulse frequency in Hz"""
        if entropy < 0.3:
            return 0.5  # Very slow, breathing-like
        elif entropy < 0.6:
            return 1.0 + (entropy * 2)  # Gradual increase
        elif entropy < 0.8:
            return 3.0 + (entropy * 4)  # Sharp pulses
        else:
            return 6.0 + (entropy * 6)  # High-frequency flicker
    
    def _calculate_distortion_level(self, entropy: float, pressure: float) -> float:
        """Calculate visual distortion level"""
        # Higher entropy and pressure create more distortion
        base_distortion = entropy * 0.6 + pressure * 0.4
        
        # Apply threshold effects
        if entropy < 0.3:
            return base_distortion * 0.2  # Minimal distortion
        elif entropy < 0.6:
            return base_distortion * 0.5  # Subtle distortion
        elif entropy < 0.8:
            return base_distortion * 0.8  # Noticeable distortion
        else:
            return min(1.0, base_distortion * 1.2)  # Maximum distortion
    
    def _calculate_color_temperature(self, entropy: float, mood_pigment: Dict[str, float]) -> float:
        """Calculate color temperature (0.0 = cool, 1.0 = warm)"""
        # Base temperature from entropy
        entropy_temp = entropy
        
        # Influence from mood pigment
        warm_colors = mood_pigment.get('red', 0) + mood_pigment.get('orange', 0) + mood_pigment.get('yellow', 0)
        cool_colors = mood_pigment.get('blue', 0) + mood_pigment.get('green', 0) + mood_pigment.get('violet', 0)
        
        pigment_temp = warm_colors - cool_colors
        
        # Blend entropy and pigment influence
        final_temp = (entropy_temp * 0.7) + (pigment_temp * 0.3)
        
        return max(0.0, min(1.0, final_temp))
    
    def _process_visual_state(self, visual_state: EntropyVisualState):
        """Process a new visual state and trigger callbacks"""
        # Generate visual configuration for GUI
        visual_config = self._generate_visual_config(visual_state)
        
        # Trigger callbacks with visual data
        for callback in self.visual_callbacks:
            try:
                callback(visual_config)
            except Exception as e:
                logger.error(f"❌ Error in entropy visual callback: {e}")
    
    def _update_continuous_animation(self, current_time: float):
        """Update continuous animation parameters"""
        if not self.current_state:
            return
        
        # Calculate animation phase based on time and frequency
        phase = (current_time * self.current_state.pulse_frequency) % (2 * math.pi)
        
        # Generate time-based visual updates
        animation_update = {
            'animation_phase': phase,
            'flow_offset': (current_time * self.flow_speed) % 360,
            'distortion_phase': (current_time * 2.0) % (2 * math.pi),
            'timestamp': current_time
        }
        
        # Trigger animation callbacks
        for callback in self.visual_callbacks:
            try:
                callback({'animation_update': animation_update})
            except Exception as e:
                logger.error(f"❌ Error in animation callback: {e}")
    
    def _generate_visual_config(self, visual_state: EntropyVisualState) -> Dict[str, Any]:
        """Generate complete visual configuration for GUI"""
        mode_key = visual_state.visualization_mode.value
        base_config = self.effects_config.get(mode_key, self.effects_config['flowing_mist'])
        
        # Apply mood pigment color modulation
        modulated_colors = self._modulate_colors_with_pigment(
            base_config['base_colors'], 
            visual_state.mood_pigment,
            visual_state.color_temperature
        )
        
        # Calculate opacity range based on intensity
        min_opacity, max_opacity = base_config['opacity_range']
        intensity_opacity = min_opacity + (visual_state.intensity * (max_opacity - min_opacity))
        
        visual_config = {
            'mode': mode_key,
            'entropy': visual_state.entropy,
            'pressure': visual_state.pressure,
            'intensity': visual_state.intensity,
            'colors': modulated_colors,
            'opacity': intensity_opacity,
            'flow_direction': visual_state.flow_direction,
            'pulse_frequency': visual_state.pulse_frequency,
            'distortion_level': visual_state.distortion_level,
            'animation_duration': base_config['animation_duration'],
            'blur_radius': base_config['blur_radius'],
            'timestamp': visual_state.timestamp,
            
            # Mode-specific parameters
            **self._get_mode_specific_params(visual_state, base_config)
        }
        
        return visual_config
    
    def _modulate_colors_with_pigment(self, base_colors: List[str], 
                                    mood_pigment: Dict[str, float],
                                    color_temperature: float) -> List[str]:
        """Modulate base colors with mood pigment and temperature"""
        modulated_colors = []
        
        for color_hex in base_colors:
            # Convert hex to RGB
            rgb = self._hex_to_rgb(color_hex)
            
            # Apply mood pigment influence
            pigmented_rgb = self._apply_pigment_to_rgb(rgb, mood_pigment)
            
            # Apply color temperature
            temperature_rgb = self._apply_color_temperature(pigmented_rgb, color_temperature)
            
            # Convert back to hex
            modulated_hex = self._rgb_to_hex(temperature_rgb)
            modulated_colors.append(modulated_hex)
        
        return modulated_colors
    
    def _get_mode_specific_params(self, visual_state: EntropyVisualState, 
                                base_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get mode-specific visual parameters"""
        mode = visual_state.visualization_mode
        
        if mode == EntropyVisualizationMode.FLOWING_MIST:
            return {
                'flow_pattern': random.choice(base_config['flow_patterns']),
                'mist_density': visual_state.intensity * 0.8
            }
        elif mode == EntropyVisualizationMode.SUBTLE_WAVES:
            return {
                'wave_amplitude': base_config['wave_amplitude'] * visual_state.distortion_level,
                'vibration_frequency': base_config['vibration_frequency'] * visual_state.intensity
            }
        elif mode == EntropyVisualizationMode.SHARP_PULSES:
            return {
                'pulse_intensity': base_config['pulse_intensity'] * visual_state.intensity,
                'grid_distortion': base_config['grid_distortion'] * visual_state.distortion_level
            }
        elif mode == EntropyVisualizationMode.FRACTURE_FLICKER:
            return {
                'flicker_frequency': base_config['flicker_frequency'] * visual_state.intensity,
                'fracture_density': base_config['fracture_density'] * visual_state.distortion_level
            }
        
        return {}
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex color"""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    
    def _apply_pigment_to_rgb(self, rgb: Tuple[int, int, int], 
                            mood_pigment: Dict[str, float]) -> Tuple[int, int, int]:
        """Apply mood pigment influence to RGB color"""
        r, g, b = rgb
        
        # Extract pigment influences
        red_influence = mood_pigment.get('red', 0) + mood_pigment.get('orange', 0) * 0.5
        green_influence = mood_pigment.get('green', 0)
        blue_influence = mood_pigment.get('blue', 0) + mood_pigment.get('violet', 0) * 0.5
        
        # Apply influences (subtle modulation)
        influence_strength = 0.3
        r = int(r + (red_influence * 50 * influence_strength))
        g = int(g + (green_influence * 50 * influence_strength))
        b = int(b + (blue_influence * 50 * influence_strength))
        
        # Clamp to valid range
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    def _apply_color_temperature(self, rgb: Tuple[int, int, int], 
                               temperature: float) -> Tuple[int, int, int]:
        """Apply color temperature to RGB (0.0 = cool, 1.0 = warm)"""
        r, g, b = rgb
        
        if temperature > 0.5:
            # Warm: enhance reds and yellows
            warm_factor = (temperature - 0.5) * 2
            r = int(r + (warm_factor * 30))
            g = int(g + (warm_factor * 15))
        else:
            # Cool: enhance blues
            cool_factor = (0.5 - temperature) * 2
            b = int(b + (cool_factor * 30))
            g = int(g + (cool_factor * 10))
        
        # Clamp to valid range
        return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    # Public interface methods
    
    def get_current_visual_state(self) -> Optional[Dict[str, Any]]:
        """Get current visual state for GUI"""
        if not self.current_state:
            return None
        
        return self._generate_visual_config(self.current_state)
    
    def set_visual_parameters(self, **params):
        """Update visual parameters"""
        if 'base_intensity' in params:
            self.base_intensity = max(0.1, min(1.0, params['base_intensity']))
        if 'flow_speed' in params:
            self.flow_speed = max(0.1, min(3.0, params['flow_speed']))
        if 'pulse_amplitude' in params:
            self.pulse_amplitude = max(0.1, min(2.0, params['pulse_amplitude']))
        
        logger.info(f"🎚️ Updated visual parameters: {params}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        return {
            'is_active': self.is_active,
            'current_mode': self.current_state.visualization_mode.value if self.current_state else None,
            'current_entropy': self.current_state.entropy if self.current_state else None,
            'current_intensity': self.current_state.intensity if self.current_state else None,
            'animation_fps': self.animation_fps,
            'registered_callbacks': len(self.visual_callbacks),
            'base_intensity': self.base_intensity,
            'flow_speed': self.flow_speed
        }

# Global entropy visual stream instance
entropy_stream = EntropyVisualStream()

def get_entropy_stream() -> EntropyVisualStream:
    """Get the global entropy visual stream"""
    return entropy_stream

def start_entropy_stream():
    """Start the entropy visual stream system"""
    entropy_stream.start_stream()

def stop_entropy_stream():
    """Stop the entropy visual stream system"""
    entropy_stream.stop_stream()

def update_entropy_visual(entropy: float, pressure: float = 0.5, 
                         mood_pigment: Optional[Dict[str, float]] = None):
    """Update entropy visualization (convenience function)"""
    entropy_stream.update_entropy_visual(entropy, pressure, mood_pigment)

if __name__ == "__main__":
    # Test the entropy visual stream system
    print("🌊 Testing DAWN Entropy Visual Stream...")
    
    stream = EntropyVisualStream()
    
    # Register test callback
    def test_visual_callback(visual_data):
        if 'mode' in visual_data:
            mode = visual_data['mode']
            entropy = visual_data.get('entropy', 0)
            intensity = visual_data.get('intensity', 0)
            print(f"🌊 Visual update: {mode} (entropy: {entropy:.2f}, intensity: {intensity:.2f})")
    
    stream.register_visual_callback(test_visual_callback)
    
    # Start stream
    stream.start_stream()
    
    print("✅ Entropy visual stream started")
    print("🌊 Testing entropy progression...")
    
    # Test progression through entropy levels
    test_entropies = [0.1, 0.25, 0.4, 0.55, 0.7, 0.85, 0.95]
    
    for entropy in test_entropies:
        print(f"\n🎯 Testing entropy: {entropy}")
        
        # Test with different mood pigments
        mood_pigments = [
            {'blue': 0.6, 'green': 0.3, 'red': 0.1},    # Cool
            {'red': 0.5, 'orange': 0.3, 'yellow': 0.2}, # Warm
            {'violet': 0.4, 'blue': 0.4, 'green': 0.2}  # Mystical
        ]
        
        for i, pigment in enumerate(mood_pigments):
            stream.update_entropy_visual(entropy, pressure=0.5 + (i * 0.2), mood_pigment=pigment)
            time.sleep(0.5)
    
    print(f"\n📊 System Status:")
    status = stream.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print(f"\n⏳ Running visual stream for 5 seconds...")
    time.sleep(5)
    
    print(f"\n🛑 Stopping entropy visual stream...")
    stream.stop_stream()
    print("✅ Entropy visual stream test complete") 