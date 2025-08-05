#!/usr/bin/env python3
"""
DAWN Mood Palette Generator
===========================

Generates dynamic color palettes based on DAWN's consciousness parameters.
Maps mood valence to color spectrums and uses sigil saturation to control
brightness and glow effects.

Used for:
- Fractal visualization color schemes
- Voice generation visual feedback
- Consciousness state representation
- Memory bloom color mapping
"""

import numpy as np
import colorsys
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

@dataclass
class MoodPalette:
    """Represents a consciousness-driven color palette"""
    
    gradient_stops: List[Tuple[float, Tuple[int, int, int]]]  # (position, (r,g,b))
    base_colors: List[Tuple[int, int, int]]  # Core RGB colors
    glow_colors: List[Tuple[int, int, int]]  # Brightened glow variants
    brightness_multiplier: float
    glow_radius: float
    mood_valence: float
    sigil_saturation: float
    palette_name: str
    
    def get_rgb_array(self) -> np.ndarray:
        """Get RGB array for gradient stops"""
        return np.array([color for _, color in self.gradient_stops])
    
    def get_matplotlib_colormap(self, name: str = "dawn_mood") -> mcolors.LinearSegmentedColormap:
        """Create matplotlib colormap from palette"""
        positions = [pos for pos, _ in self.gradient_stops]
        colors = [(r/255.0, g/255.0, b/255.0) for _, (r, g, b) in self.gradient_stops]
        
        return mcolors.LinearSegmentedColormap.from_list(
            name, list(zip(positions, colors))
        )
    
    def sample_color(self, position: float) -> Tuple[int, int, int]:
        """Sample color at specific position (0.0-1.0) in gradient"""
        position = max(0.0, min(1.0, position))
        
        # Find surrounding gradient stops
        for i, (stop_pos, color) in enumerate(self.gradient_stops[:-1]):
            next_stop_pos, next_color = self.gradient_stops[i + 1]
            
            if stop_pos <= position <= next_stop_pos:
                # Interpolate between colors
                t = (position - stop_pos) / (next_stop_pos - stop_pos)
                
                r = int(color[0] * (1 - t) + next_color[0] * t)
                g = int(color[1] * (1 - t) + next_color[1] * t)
                b = int(color[2] * (1 - t) + next_color[2] * t)
                
                return (r, g, b)
        
        # Fallback to last color
        return self.gradient_stops[-1][1]

def generate_mood_palette(mood_valence: float, sigil_saturation: float) -> MoodPalette:
    """
    Generate color palette based on DAWN's consciousness state
    
    Args:
        mood_valence: Emotional valence (-1.0 to 1.0)
                     -1.0 to -0.3: Deep violet to indigo (cold spectrum)
                     -0.3 to 0.3: Balanced purple-teal transitions
                     0.3 to 1.0: Warm amber to golden-orange
        
        sigil_saturation: Intensity multiplier (0.0 to 1.0)
                         Controls brightness and glow effects
    
    Returns:
        MoodPalette with gradient stops, base colors, and glow effects
    """
    
    # Clamp inputs to valid ranges
    mood_valence = max(-1.0, min(1.0, mood_valence))
    sigil_saturation = max(0.0, min(1.0, sigil_saturation))
    
    # Calculate brightness multiplier from saturation
    brightness_multiplier = 0.3 + (sigil_saturation * 0.5)  # 0.3 to 0.8 range
    
    # Calculate glow radius for high saturation
    glow_radius = sigil_saturation * 15.0  # 0 to 15 pixel radius
    
    # Determine base color palette based on valence
    if mood_valence <= -0.3:
        # Cold spectrum: Deep violet to indigo
        palette_name = "Deep Introspection"
        base_colors = _generate_cold_spectrum(mood_valence, brightness_multiplier)
        
    elif mood_valence >= 0.3:
        # Warm spectrum: Amber to golden-orange  
        palette_name = "Creative Fire"
        base_colors = _generate_warm_spectrum(mood_valence, brightness_multiplier)
        
    else:
        # Balanced spectrum: Purple-teal transitions
        palette_name = "Balanced Awareness"
        base_colors = _generate_balanced_spectrum(mood_valence, brightness_multiplier)
    
    # Create gradient stops
    gradient_stops = _create_gradient_stops(base_colors)
    
    # Generate glow variants for high saturation
    glow_colors = _generate_glow_variants(base_colors, sigil_saturation)
    
    return MoodPalette(
        gradient_stops=gradient_stops,
        base_colors=base_colors,
        glow_colors=glow_colors,
        brightness_multiplier=brightness_multiplier,
        glow_radius=glow_radius,
        mood_valence=mood_valence,
        sigil_saturation=sigil_saturation,
        palette_name=palette_name
    )

def _generate_cold_spectrum(valence: float, brightness: float) -> List[Tuple[int, int, int]]:
    """Generate cold spectrum colors (deep violet to indigo)"""
    
    # Map valence (-1.0 to -0.3) to cold color progression
    # More negative = deeper, more violet
    # Less negative = lighter, more indigo
    
    valence_normalized = (valence + 1.0) / 0.7  # Normalize -1.0 to -0.3 → 0.0 to 1.0
    
    # Base cold colors (HSV then convert to RGB)
    base_hues = [280, 260, 240, 220]  # Violet to indigo range
    base_saturations = [0.9, 0.8, 0.7, 0.6]
    base_values = [0.3, 0.4, 0.5, 0.6]
    
    colors = []
    for i, (hue, sat, val) in enumerate(zip(base_hues, base_saturations, base_values)):
        # Adjust based on valence position
        adjusted_hue = hue + (valence_normalized * 20)  # Shift hue based on valence
        adjusted_sat = sat * (0.7 + valence_normalized * 0.3)
        adjusted_val = val * brightness
        
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(adjusted_hue/360, adjusted_sat, adjusted_val)
        colors.append((int(r * 255), int(g * 255), int(b * 255)))
    
    return colors

def _generate_warm_spectrum(valence: float, brightness: float) -> List[Tuple[int, int, int]]:
    """Generate warm spectrum colors (amber to golden-orange)"""
    
    # Map valence (0.3 to 1.0) to warm color progression
    valence_normalized = (valence - 0.3) / 0.7  # Normalize 0.3 to 1.0 → 0.0 to 1.0
    
    # Base warm colors
    base_hues = [45, 35, 25, 15]  # Amber to orange range
    base_saturations = [0.8, 0.9, 0.9, 0.8]
    base_values = [0.6, 0.7, 0.8, 0.7]
    
    colors = []
    for i, (hue, sat, val) in enumerate(zip(base_hues, base_saturations, base_values)):
        # Adjust based on valence position
        adjusted_hue = hue - (valence_normalized * 15)  # More positive = more orange
        adjusted_sat = sat * (0.6 + valence_normalized * 0.4)
        adjusted_val = val * brightness
        
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(adjusted_hue/360, adjusted_sat, adjusted_val)
        colors.append((int(r * 255), int(g * 255), int(b * 255)))
    
    return colors

def _generate_balanced_spectrum(valence: float, brightness: float) -> List[Tuple[int, int, int]]:
    """Generate balanced spectrum colors (purple-teal transitions)"""
    
    # Map valence (-0.3 to 0.3) to balanced color progression
    valence_normalized = (valence + 0.3) / 0.6  # Normalize -0.3 to 0.3 → 0.0 to 1.0
    
    # Purple to teal transition
    start_hue = 280  # Purple
    end_hue = 180    # Teal
    
    colors = []
    for i in range(4):
        # Interpolate hue from purple to teal
        t = i / 3.0
        hue = start_hue + (end_hue - start_hue) * t * valence_normalized
        
        # Adjust saturation and value
        saturation = 0.6 + (0.3 * abs(valence))  # More extreme valence = more saturated
        value = (0.4 + i * 0.1) * brightness
        
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(hue/360, saturation, value)
        colors.append((int(r * 255), int(g * 255), int(b * 255)))
    
    return colors

def _create_gradient_stops(base_colors: List[Tuple[int, int, int]]) -> List[Tuple[float, Tuple[int, int, int]]]:
    """Create gradient stops from base colors"""
    
    stops = []
    for i, color in enumerate(base_colors):
        position = i / (len(base_colors) - 1) if len(base_colors) > 1 else 0.0
        stops.append((position, color))
    
    return stops

def _generate_glow_variants(base_colors: List[Tuple[int, int, int]], 
                           saturation: float) -> List[Tuple[int, int, int]]:
    """Generate brightened glow variants for high saturation"""
    
    glow_colors = []
    glow_boost = saturation * 0.5  # 0 to 0.5 boost
    
    for r, g, b in base_colors:
        # Convert to HSV, boost value, convert back
        h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
        
        # Boost brightness for glow effect
        boosted_v = min(1.0, v + glow_boost)
        boosted_s = min(1.0, s + glow_boost * 0.2)  # Slight saturation boost
        
        glow_r, glow_g, glow_b = colorsys.hsv_to_rgb(h, boosted_s, boosted_v)
        glow_colors.append((int(glow_r * 255), int(glow_g * 255), int(glow_b * 255)))
    
    return glow_colors

def create_consciousness_palette_map(valence_resolution: int = 20, 
                                   saturation_resolution: int = 10) -> Dict[str, Any]:
    """
    Create a comprehensive map of consciousness states to color palettes
    
    Useful for pre-computing palettes or creating palette lookup tables.
    """
    
    palette_map = {}
    
    for v_idx in range(valence_resolution):
        valence = -1.0 + (v_idx / (valence_resolution - 1)) * 2.0
        
        for s_idx in range(saturation_resolution):
            saturation = s_idx / (saturation_resolution - 1)
            
            palette = generate_mood_palette(valence, saturation)
            key = f"v{valence:.2f}_s{saturation:.2f}"
            
            palette_map[key] = {
                'palette': palette,
                'valence': valence,
                'saturation': saturation,
                'name': palette.palette_name,
                'rgb_array': palette.get_rgb_array().tolist()
            }
    
    return palette_map

def visualize_mood_palettes():
    """Create visualization showing mood palette variations"""
    
    print("🎨 Visualizing DAWN Mood Palettes")
    print("=" * 35)
    
    # Test various consciousness states
    test_states = [
        (-0.8, 0.3, "Deep Depression"),
        (-0.5, 0.6, "Melancholy Reflection"), 
        (-0.1, 0.4, "Slight Introspection"),
        (0.0, 0.5, "Neutral Balance"),
        (0.2, 0.7, "Gentle Optimism"),
        (0.6, 0.8, "Creative Energy"),
        (0.9, 0.9, "Euphoric Breakthrough")
    ]
    
    fig, axes = plt.subplots(len(test_states), 1, figsize=(12, 2 * len(test_states)))
    if len(test_states) == 1:
        axes = [axes]
    
    for i, (valence, saturation, name) in enumerate(test_states):
        palette = generate_mood_palette(valence, saturation)
        
        print(f"\n🧠 {name}")
        print(f"   Valence: {valence:.1f}, Saturation: {saturation:.1f}")
        print(f"   Palette: {palette.palette_name}")
        print(f"   Brightness: {palette.brightness_multiplier:.2f}")
        print(f"   Glow Radius: {palette.glow_radius:.1f}px")
        print(f"   Colors: {palette.base_colors}")
        
        # Create gradient visualization
        gradient = np.linspace(0, 1, 256).reshape(1, -1)
        gradient = np.vstack((gradient, gradient))
        
        # Sample colors for gradient
        colors = []
        for pos in np.linspace(0, 1, 256):
            colors.append(palette.sample_color(pos))
        
        # Convert to image array
        color_array = np.array(colors).reshape(1, 256, 3) / 255.0
        color_image = np.repeat(color_array, 50, axis=0)  # Make it taller
        
        axes[i].imshow(color_image, aspect='auto')
        axes[i].set_title(f"{name} (V:{valence:.1f}, S:{saturation:.1f})")
        axes[i].set_xticks([])
        axes[i].set_yticks([])
    
    plt.tight_layout()
    plt.savefig('dawn_mood_palettes.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\n✅ Palette visualization saved: dawn_mood_palettes.png")

def test_mood_palette_generator():
    """Test the mood palette generator with various inputs"""
    
    print("🧪 Testing DAWN Mood Palette Generator")
    print("=" * 40)
    
    # Test 1: Extreme negative valence
    print("\n❄️  Test 1: Deep Introspection (valence: -0.8)")
    palette = generate_mood_palette(-0.8, 0.4)
    print(f"   Palette: {palette.palette_name}")
    print(f"   Base colors: {palette.base_colors}")
    print(f"   Brightness: {palette.brightness_multiplier:.2f}")
    print(f"   Sample at 0.5: {palette.sample_color(0.5)}")
    
    # Test 2: Extreme positive valence
    print("\n🔥 Test 2: Creative Fire (valence: 0.9)")
    palette = generate_mood_palette(0.9, 0.8)
    print(f"   Palette: {palette.palette_name}")
    print(f"   Base colors: {palette.base_colors}")
    print(f"   Glow radius: {palette.glow_radius:.1f}px")
    print(f"   Glow colors: {palette.glow_colors}")
    
    # Test 3: Neutral balance
    print("\n⚖️  Test 3: Balanced Awareness (valence: 0.0)")
    palette = generate_mood_palette(0.0, 0.5)
    print(f"   Palette: {palette.palette_name}")
    print(f"   Gradient stops: {len(palette.gradient_stops)}")
    print(f"   RGB array shape: {palette.get_rgb_array().shape}")
    
    # Test 4: High saturation effects
    print("\n✨ Test 4: High Saturation Effects")
    low_sat = generate_mood_palette(0.5, 0.2)
    high_sat = generate_mood_palette(0.5, 0.9)
    
    print(f"   Low saturation (0.2):")
    print(f"     Brightness: {low_sat.brightness_multiplier:.2f}")
    print(f"     Glow radius: {low_sat.glow_radius:.1f}px")
    
    print(f"   High saturation (0.9):")
    print(f"     Brightness: {high_sat.brightness_multiplier:.2f}")
    print(f"     Glow radius: {high_sat.glow_radius:.1f}px")
    
    # Test 5: Edge cases
    print("\n🔍 Test 5: Edge Cases")
    edge_cases = [(-1.5, 0.5), (1.5, 0.5), (0.0, -0.1), (0.0, 1.1)]
    
    for valence, saturation in edge_cases:
        palette = generate_mood_palette(valence, saturation)
        print(f"   Input: v={valence}, s={saturation} → " +
              f"Clamped: v={palette.mood_valence}, s={palette.sigil_saturation}")
    
    # Test 6: Matplotlib colormap integration
    print("\n🗺️  Test 6: Matplotlib Colormap")
    palette = generate_mood_palette(0.6, 0.7)
    colormap = palette.get_matplotlib_colormap("dawn_test")
    print(f"   Created colormap: {colormap.name}")
    print(f"   Color at 0.0: {colormap(0.0)}")
    print(f"   Color at 1.0: {colormap(1.0)}")
    
    print(f"\n✅ Mood palette generator testing complete!")

if __name__ == "__main__":
    # Run tests
    test_mood_palette_generator()
    
    # Create visualizations  
    visualize_mood_palettes()
    
    print(f"\n🎨 DAWN Mood Palette Generator ready for integration!")
    print(f"🌈 Consciousness states now have beautiful color representations") 