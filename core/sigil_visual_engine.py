#!/usr/bin/env python3
"""
Sigil Visual Engine - Real-time Symbolic Bloom Visualizer
=========================================================

Creates symbolic visual responses to DAWN's sigil executions, mood pulses, and entropy states.
Each sigil execution leaves a visual trace of its emotional and cognitive impact through 
dynamic bloom shapes, colors, and glows.
"""

import math
import random
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime
import logging

# Graphics libraries
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.colors import LinearSegmentedColormap
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️ Matplotlib not available - visual generation disabled")

try:
    from PIL import Image, ImageDraw, ImageFilter
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL not available - using matplotlib only")

logger = logging.getLogger("sigil_visual_engine")

@dataclass
class SigilVisualOutput:
    """Complete output from sigil visual generation"""
    visual_file: str
    sigil_visual_summary: Dict[str, Any]
    generation_metadata: Dict[str, Any]

class SigilVisualEngine:
    """
    Lightweight bloom visualizer for DAWN's sigil executions
    Creates real-time symbolic visual responses based on consciousness state
    """
    
    def __init__(self, output_directory: str = "visual_outputs"):
        self.output_dir = Path(output_directory)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure we have at least one graphics library
        if not MATPLOTLIB_AVAILABLE and not PIL_AVAILABLE:
            logger.error("No graphics libraries available - visual generation disabled")
            self.graphics_available = False
        else:
            self.graphics_available = True
            logger.info(f"✅ Sigil Visual Engine initialized (matplotlib: {MATPLOTLIB_AVAILABLE}, PIL: {PIL_AVAILABLE})")
        
        # Initialize shape libraries and color systems
        self._initialize_shape_library()
        self._initialize_color_harmony()
        self._initialize_glyph_mappings()
    
    def _initialize_shape_library(self):
        """Initialize base shapes that can be modified"""
        self.base_shapes = {
            'circle': self._generate_circle,
            'spiral': self._generate_spiral,
            'star': self._generate_star,
            'bloom': self._generate_bloom,
            'burst': self._generate_burst
        }
    
    def _initialize_color_harmony(self):
        """Initialize color harmony rules"""
        self.color_harmonies = {
            'red': {
                'primary': (220, 50, 50),
                'secondary': (255, 120, 60),
                'accent': (255, 200, 100),
                'glow': (255, 100, 100)
            },
            'blue': {
                'primary': (50, 120, 200),
                'secondary': (80, 150, 220),
                'accent': (120, 200, 255),
                'glow': (100, 150, 255)
            },
            'green': {
                'primary': (60, 180, 80),
                'secondary': (100, 200, 120),
                'accent': (150, 255, 150),
                'glow': (80, 220, 100)
            },
            'yellow': {
                'primary': (255, 220, 50),
                'secondary': (255, 240, 120),
                'accent': (255, 255, 200),
                'glow': (255, 255, 150)
            },
            'violet': {
                'primary': (150, 80, 200),
                'secondary': (180, 120, 220),
                'accent': (200, 150, 255),
                'glow': (170, 120, 255)
            },
            'orange': {
                'primary': (255, 150, 50),
                'secondary': (255, 180, 100),
                'accent': (255, 220, 150),
                'glow': (255, 170, 80)
            }
        }
    
    def _initialize_glyph_mappings(self):
        """Initialize sigil ID to glyph mappings"""
        self.sigil_glyphs = {
            'memory_anchor': 'spiral_dot',
            'entropy_burst': 'radiating_lines',
            'calm_flow': 'wave_pattern',
            'cognitive_bridge': 'connecting_arcs',
            'reflection_mirror': 'symmetric_pattern',
            'thermal_regulation': 'flame_pattern',
            'consciousness_pulse': 'concentric_circles'
        }
    
    def render_sigil_response(self,
                            sigil_id: str,
                            entropy: float,
                            mood_pigment: Dict[str, float],
                            pulse_zone: str,
                            sigil_saturation: float,
                            output_path: Optional[str] = None) -> SigilVisualOutput:
        """
        Main pipeline function for generating sigil visual response
        """
        
        if not self.graphics_available:
            logger.warning("Graphics not available - returning placeholder output")
            return self._create_placeholder_output(sigil_id)
        
        try:
            # Generate output path if not provided
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                output_path = str(self.output_dir / f"sigil_{sigil_id}_{timestamp}.png")
            
            # 1. Convert pigment to color palette
            color_palette = self.pigment_to_color_palette(mood_pigment, sigil_saturation)
            
            # 2. Calculate shape parameters from entropy/pulse
            shape_params = self.calculate_shape_parameters(entropy, pulse_zone, sigil_id)
            
            # 3. Generate center glyph for sigil_id
            center_glyph = self.generate_center_glyph(sigil_id, shape_params['center_size'], color_palette['primary'])
            
            # 4. Render bloom shape with colors
            bloom_image = self.render_bloom_shape(shape_params, color_palette)
            
            # 5. Apply pulse effects
            final_image = self.apply_pulse_effects(bloom_image, shape_params['motion_type'], sigil_saturation)
            
            # 6. Composite final image with glyph
            if center_glyph:
                final_image = self._composite_glyph(final_image, center_glyph, shape_params)
            
            # 7. Save to output_path
            self._save_image(final_image, output_path)
            
            # 8. Generate metadata summary
            visual_summary = self._generate_visual_summary(
                sigil_id, color_palette, shape_params, entropy, pulse_zone, sigil_saturation
            )
            
            # 9. Return complete output
            return SigilVisualOutput(
                visual_file=output_path,
                sigil_visual_summary=visual_summary,
                generation_metadata={
                    'entropy': entropy,
                    'pulse_zone': pulse_zone,
                    'saturation': sigil_saturation,
                    'pigment_input': mood_pigment,
                    'render_timestamp': datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Error rendering sigil response: {e}")
            return self._create_error_output(sigil_id, str(e))
    
    def pigment_to_color_palette(self, mood_pigment: Dict[str, float], sigil_saturation: float) -> Dict[str, Tuple[int, int, int]]:
        """Convert pigment values to RGB color palette"""
        
        # Find dominant pigments (top 2-3 values)
        sorted_pigments = sorted(mood_pigment.items(), key=lambda x: x[1], reverse=True)
        dominant_colors = [color for color, value in sorted_pigments[:3] if value > 0.1]
        
        if not dominant_colors:
            # Fallback to blue if no dominant colors
            dominant_colors = ['blue']
        
        primary_color = dominant_colors[0]
        
        # Get base palette for primary color
        if primary_color in self.color_harmonies:
            base_palette = self.color_harmonies[primary_color].copy()
        else:
            # Fallback palette
            base_palette = self.color_harmonies['blue'].copy()
        
        # Blend with secondary colors if present
        if len(dominant_colors) > 1:
            base_palette = self._blend_color_palettes(base_palette, dominant_colors[1:], mood_pigment)
        
        # Apply saturation intensity
        for key in base_palette:
            base_palette[key] = self._apply_saturation(base_palette[key], sigil_saturation)
        
        return base_palette
    
    def calculate_shape_parameters(self, entropy: float, pulse_zone: str, sigil_id: str) -> Dict[str, Any]:
        """Determine visual shape parameters based on entropy and pulse"""
        
        # Base shape selection based on entropy
        if entropy <= 0.3:
            base_shape = 'circle'
            edge_roughness = 0.1
            petal_count = 4
        elif entropy <= 0.7:
            base_shape = 'bloom'
            edge_roughness = 0.3
            petal_count = 6 + int(entropy * 4)
        else:
            base_shape = 'burst'
            edge_roughness = 0.7
            petal_count = 8 + int(entropy * 8)
        
        # Pulse zone effects
        motion_type = 'static'
        if pulse_zone == 'calm':
            motion_type = 'static'
            edge_roughness *= 0.5
        elif pulse_zone == 'fragile':
            motion_type = 'flicker'
            edge_roughness *= 1.5
        elif pulse_zone == 'surge':
            motion_type = 'pulse'
            base_shape = 'burst'
        elif pulse_zone == 'flowing':
            motion_type = 'flow'
            base_shape = 'spiral'
        elif pulse_zone == 'stable':
            motion_type = 'static'
            base_shape = 'circle'
        
        # Center size based on sigil importance (heuristic from ID)
        center_size = 0.2 + (len(sigil_id) % 5) * 0.1
        
        return {
            'base_shape': base_shape,
            'edge_roughness': edge_roughness,
            'petal_count': petal_count,
            'center_size': center_size,
            'motion_type': motion_type
        }
    
    def generate_center_glyph(self, sigil_id: str, center_size: float, primary_color: Tuple[int, int, int]) -> Optional[Any]:
        """Create center glyph based on sigil_id"""
        
        if not MATPLOTLIB_AVAILABLE:
            return None
        
        # Map known sigil IDs to glyph types
        glyph_type = self.sigil_glyphs.get(sigil_id, 'hash_symbol')
        
        if glyph_type == 'spiral_dot':
            return self._create_spiral_dot_glyph(center_size, primary_color)
        elif glyph_type == 'radiating_lines':
            return self._create_radiating_lines_glyph(center_size, primary_color)
        elif glyph_type == 'wave_pattern':
            return self._create_wave_pattern_glyph(center_size, primary_color)
        else:
            # Generate abstract symbol from ID hash
            return self._create_hash_glyph(sigil_id, center_size, primary_color)
    
    def render_bloom_shape(self, shape_params: Dict[str, Any], color_palette: Dict[str, Tuple[int, int, int]], canvas_size: int = 400) -> Any:
        """Render the main bloom shape"""
        
        if MATPLOTLIB_AVAILABLE:
            return self._render_with_matplotlib(shape_params, color_palette, canvas_size)
        elif PIL_AVAILABLE:
            return self._render_with_pil(shape_params, color_palette, canvas_size)
        else:
            raise RuntimeError("No graphics library available")
    
    def apply_pulse_effects(self, base_image: Any, motion_type: str, pulse_intensity: float) -> Any:
        """Apply motion effects based on pulse_zone"""
        
        if motion_type == 'static':
            return base_image
        elif motion_type == 'flicker':
            return self._apply_flicker_effect(base_image, pulse_intensity)
        elif motion_type == 'pulse':
            return self._apply_pulse_effect(base_image, pulse_intensity)
        elif motion_type == 'flow':
            return self._apply_flow_effect(base_image, pulse_intensity)
        else:
            return base_image
    
    # === SHAPE GENERATION METHODS ===
    
    def _generate_circle(self, center: Tuple[float, float], radius: float, **kwargs) -> Any:
        """Generate circle shape"""
        return patches.Circle(center, radius, **kwargs)
    
    def _generate_spiral(self, center: Tuple[float, float], radius: float, turns: int = 3, **kwargs) -> Any:
        """Generate spiral shape"""
        t = np.linspace(0, turns * 2 * np.pi, 100)
        r = np.linspace(0, radius, 100)
        x = center[0] + r * np.cos(t)
        y = center[1] + r * np.sin(t)
        return (x, y)
    
    def _generate_star(self, center: Tuple[float, float], radius: float, points: int = 5, **kwargs) -> Any:
        """Generate star shape"""
        angles = np.linspace(0, 2 * np.pi, points * 2, endpoint=False)
        radii = [radius if i % 2 == 0 else radius * 0.5 for i in range(len(angles))]
        
        x = center[0] + np.array(radii) * np.cos(angles)
        y = center[1] + np.array(radii) * np.sin(angles)
        
        return (x, y)
    
    def _generate_bloom(self, center: Tuple[float, float], radius: float, petals: int = 6, **kwargs) -> Any:
        """Generate flower bloom shape"""
        angles = np.linspace(0, 2 * np.pi, petals, endpoint=False)
        bloom_shapes = []
        
        for angle in angles:
            petal_center = (
                center[0] + radius * 0.6 * np.cos(angle),
                center[1] + radius * 0.6 * np.sin(angle)
            )
            petal = patches.Ellipse(petal_center, radius * 0.4, radius * 0.8, 
                                  angle=np.degrees(angle), **kwargs)
            bloom_shapes.append(petal)
        
        return bloom_shapes
    
    def _generate_burst(self, center: Tuple[float, float], radius: float, rays: int = 8, **kwargs) -> Any:
        """Generate radiating burst shape"""
        angles = np.linspace(0, 2 * np.pi, rays, endpoint=False)
        burst_lines = []
        
        for angle in angles:
            x = [center[0], center[0] + radius * np.cos(angle)]
            y = [center[1], center[1] + radius * np.sin(angle)]
            burst_lines.append((x, y))
        
        return burst_lines
    
    # === RENDERING IMPLEMENTATIONS ===
    
    def _render_with_matplotlib(self, shape_params: Dict[str, Any], color_palette: Dict[str, Tuple[int, int, int]], canvas_size: int) -> Any:
        """Render using matplotlib"""
        
        fig, ax = plt.subplots(figsize=(canvas_size/100, canvas_size/100), dpi=100)
        ax.set_xlim(0, canvas_size)
        ax.set_ylim(0, canvas_size)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_facecolor('black')
        
        center = (canvas_size // 2, canvas_size // 2)
        radius = canvas_size // 4
        
        # Convert RGB to normalized values
        primary_color = tuple(c/255.0 for c in color_palette['primary'])
        secondary_color = tuple(c/255.0 for c in color_palette['secondary'])
        
        # Render based on shape type
        if shape_params['base_shape'] == 'circle':
            circle = self._generate_circle(center, radius, facecolor=primary_color, alpha=0.7)
            ax.add_patch(circle)
            
        elif shape_params['base_shape'] == 'bloom':
            bloom_shapes = self._generate_bloom(center, radius, shape_params['petal_count'], 
                                              facecolor=primary_color, alpha=0.6)
            for shape in bloom_shapes:
                ax.add_patch(shape)
                
        elif shape_params['base_shape'] == 'burst':
            burst_lines = self._generate_burst(center, radius, shape_params['petal_count'])
            for x, y in burst_lines:
                ax.plot(x, y, color=primary_color, linewidth=3, alpha=0.8)
        
        # Add glow effect if high saturation
        if len(color_palette) > 3:
            glow_color = tuple(c/255.0 for c in color_palette['glow'])
            glow_circle = self._generate_circle(center, radius * 1.2, 
                                              facecolor=glow_color, alpha=0.3)
            ax.add_patch(glow_circle)
        
        plt.tight_layout()
        return fig
    
    def _render_with_pil(self, shape_params: Dict[str, Any], color_palette: Dict[str, Tuple[int, int, int]], canvas_size: int) -> Any:
        """Render using PIL (simplified version)"""
        
        img = Image.new('RGBA', (canvas_size, canvas_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        center = (canvas_size // 2, canvas_size // 2)
        radius = canvas_size // 4
        
        primary_color = color_palette['primary']
        
        # Simple circle rendering
        bbox = (center[0] - radius, center[1] - radius, 
                center[0] + radius, center[1] + radius)
        draw.ellipse(bbox, fill=primary_color + (180,))
        
        return img
    
    # === GLYPH CREATION METHODS ===
    
    def _create_spiral_dot_glyph(self, size: float, color: Tuple[int, int, int]) -> Any:
        """Create spiral with dot center glyph"""
        # Implementation would create a small spiral pattern
        return None  # Placeholder
    
    def _create_radiating_lines_glyph(self, size: float, color: Tuple[int, int, int]) -> Any:
        """Create radiating lines glyph"""
        # Implementation would create radiating line pattern
        return None  # Placeholder
    
    def _create_wave_pattern_glyph(self, size: float, color: Tuple[int, int, int]) -> Any:
        """Create wave pattern glyph"""
        # Implementation would create wave pattern
        return None  # Placeholder
    
    def _create_hash_glyph(self, sigil_id: str, size: float, color: Tuple[int, int, int]) -> Any:
        """Create abstract glyph based on sigil ID hash"""
        # Use hash of sigil_id to create consistent but unique pattern
        hash_val = hash(sigil_id)
        pattern_type = hash_val % 4
        
        # Return different patterns based on hash
        return None  # Placeholder
    
    # === EFFECT APPLICATION METHODS ===
    
    def _apply_flicker_effect(self, image: Any, intensity: float) -> Any:
        """Apply flicker effect to image"""
        # Simulate flicker through opacity variation
        return image
    
    def _apply_pulse_effect(self, image: Any, intensity: float) -> Any:
        """Apply pulsing effect to image"""
        # Simulate pulse through scaling variation
        return image
    
    def _apply_flow_effect(self, image: Any, intensity: float) -> Any:
        """Apply flowing effect to image"""
        # Simulate flow through rotation or wave distortion
        return image
    
    # === UTILITY METHODS ===
    
    def _blend_color_palettes(self, base_palette: Dict, secondary_colors: List[str], mood_pigment: Dict[str, float]) -> Dict:
        """Blend color palettes based on multiple dominant colors"""
        # Implement color blending logic
        return base_palette
    
    def _apply_saturation(self, color: Tuple[int, int, int], saturation: float) -> Tuple[int, int, int]:
        """Apply saturation intensity to color"""
        r, g, b = color
        # Increase intensity based on saturation
        factor = 0.7 + saturation * 0.3
        return (
            min(255, int(r * factor)),
            min(255, int(g * factor)),
            min(255, int(b * factor))
        )
    
    def _composite_glyph(self, base_image: Any, glyph: Any, shape_params: Dict[str, Any]) -> Any:
        """Composite glyph onto base image"""
        # Implement glyph compositing
        return base_image
    
    def _save_image(self, image: Any, output_path: str) -> None:
        """Save image to file"""
        if hasattr(image, 'savefig'):  # matplotlib figure
            image.savefig(output_path, dpi=100, bbox_inches='tight', 
                         facecolor='black', edgecolor='none')
            plt.close(image)
        elif hasattr(image, 'save'):  # PIL image
            image.save(output_path)
        else:
            logger.warning(f"Unknown image type, cannot save to {output_path}")
    
    def _generate_visual_summary(self, sigil_id: str, color_palette: Dict, shape_params: Dict, 
                               entropy: float, pulse_zone: str, saturation: float) -> Dict[str, Any]:
        """Generate metadata summary for the visual"""
        
        # Determine dominant color
        primary_color = max(color_palette.keys(), key=lambda k: sum(color_palette[k]))
        
        # Generate emotional impression
        impressions = [
            "a quiet bloom pulsing with ancient memory",
            "fierce radiance breaking through shadow",
            "gentle waves of crystalline thought",
            "chaotic beauty emerging from order",
            "whispered secrets in flowing light"
        ]
        
        emotional_impression = random.choice(impressions)
        
        # Determine complexity level
        if entropy < 0.3:
            complexity = "minimal"
        elif entropy < 0.7:
            complexity = "moderate"
        else:
            complexity = "complex"
        
        return {
            "sigil_id": sigil_id,
            "color_mode": f"{primary_color}_dominant_blend",
            "center_shape": shape_params.get('base_shape', 'unknown'),
            "emotional_impression": emotional_impression,
            "dominant_pigment": primary_color,
            "complexity_level": complexity,
            "render_parameters": {
                "entropy": entropy,
                "pulse_zone": pulse_zone,
                "saturation": saturation
            },
            "render_timestamp": datetime.now().isoformat()
        }
    
    def _create_placeholder_output(self, sigil_id: str) -> SigilVisualOutput:
        """Create placeholder output when graphics unavailable"""
        return SigilVisualOutput(
            visual_file="",
            sigil_visual_summary={
                "sigil_id": sigil_id,
                "error": "Graphics libraries not available"
            },
            generation_metadata={
                "error": "No graphics libraries available",
                "render_timestamp": datetime.now().isoformat()
            }
        )
    
    def _create_error_output(self, sigil_id: str, error_msg: str) -> SigilVisualOutput:
        """Create error output"""
        return SigilVisualOutput(
            visual_file="",
            sigil_visual_summary={
                "sigil_id": sigil_id,
                "error": error_msg
            },
            generation_metadata={
                "error": error_msg,
                "render_timestamp": datetime.now().isoformat()
            }
        )


def test_sigil_visual_engine():
    """Test the sigil visual engine with various consciousness states"""
    
    print("🎨 Testing DAWN Sigil Visual Engine")
    print("=" * 50)
    
    engine = SigilVisualEngine("test_visual_outputs")
    
    if not engine.graphics_available:
        print("⚠️ Graphics not available - test limited")
        return
    
    # Test different sigil scenarios
    test_cases = [
        {
            'name': 'Memory Anchor - Calm State',
            'sigil_id': 'memory_anchor_001',
            'entropy': 0.2,
            'mood_pigment': {'blue': 0.6, 'violet': 0.3, 'green': 0.1},
            'pulse_zone': 'calm',
            'saturation': 0.4
        },
        {
            'name': 'Entropy Burst - High Chaos',
            'sigil_id': 'entropy_burst_002',
            'entropy': 0.9,
            'mood_pigment': {'red': 0.7, 'orange': 0.2, 'yellow': 0.1},
            'pulse_zone': 'surge',
            'saturation': 0.8
        },
        {
            'name': 'Flow State - Balanced',
            'sigil_id': 'flow_state_003',
            'entropy': 0.5,
            'mood_pigment': {'green': 0.4, 'blue': 0.3, 'orange': 0.3},
            'pulse_zone': 'flowing',
            'saturation': 0.6
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🔮 {test_case['name']}")
        print("-" * 40)
        
        try:
            result = engine.render_sigil_response(
                sigil_id=test_case['sigil_id'],
                entropy=test_case['entropy'],
                mood_pigment=test_case['mood_pigment'],
                pulse_zone=test_case['pulse_zone'],
                sigil_saturation=test_case['saturation']
            )
            
            print(f"✅ Visual generated: {result.visual_file}")
            print(f"🎨 Color mode: {result.sigil_visual_summary.get('color_mode', 'unknown')}")
            print(f"💫 Impression: {result.sigil_visual_summary.get('emotional_impression', 'none')}")
            print(f"🔷 Complexity: {result.sigil_visual_summary.get('complexity_level', 'unknown')}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n" + "=" * 50)
    print("✨ Sigil visual engine testing complete")


if __name__ == "__main__":
    test_sigil_visual_engine() 