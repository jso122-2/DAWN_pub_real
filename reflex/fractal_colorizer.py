"""
Fractal Colorizer - Bloom Mood ↔ Color Logic for DAWN System
Maps bloom states, moods, and entropy to perceptually meaningful colors
Uses HSV color space for smooth transitions and entropy-driven gradients
"""

import math
import colorsys
import logging
from typing import Dict, List, Tuple, Optional, Union
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class ColorSpace(Enum):
    """Supported color output formats"""
    HEX = "hex"
    RGB = "rgb"
    HSV = "hsv"
    HSL = "hsl"


@dataclass
class ColorProfile:
    """Color profile for a specific mood/state combination"""
    base_hue: float  # 0-360 degrees
    saturation_range: Tuple[float, float]  # (min, max) 0-1
    value_range: Tuple[float, float]  # (min, max) 0-1
    entropy_shift: float  # Hue shift per entropy unit
    thermal_sensitivity: float  # How much thermal affects brightness


class FractalColorizer:
    """
    Advanced bloom mood to color mapper with entropy gradient scaling.
    Uses perceptual color theory to create meaningful visual representations.
    """
    
    def __init__(self):
        """Initialize colorizer with mood profiles and entropy mapping"""
        
        # Core mood color profiles based on psychological color theory
        self.mood_profiles = {
            # Calm states - Cool colors (blues, greens)
            "calm": ColorProfile(210, (0.4, 0.7), (0.6, 0.9), 0, 0.3),
            "serene": ColorProfile(180, (0.3, 0.6), (0.7, 0.95), 0, 0.2),
            "peaceful": ColorProfile(120, (0.3, 0.5), (0.7, 0.9), 0, 0.25),
            "dormant": ColorProfile(240, (0.2, 0.4), (0.4, 0.7), 0, 0.4),
            "meditative": ColorProfile(270, (0.4, 0.6), (0.5, 0.8), 0, 0.3),
            
            # Active states - Warm colors (oranges, yellows)
            "active": ColorProfile(45, (0.6, 0.9), (0.7, 0.95), 15, 0.4),
            "energetic": ColorProfile(60, (0.7, 1.0), (0.8, 1.0), 20, 0.5),
            "excited": ColorProfile(30, (0.8, 1.0), (0.9, 1.0), 25, 0.6),
            "dynamic": ColorProfile(40, (0.6, 0.8), (0.7, 0.9), 18, 0.45),
            
            # Agitated states - Red spectrum
            "agitated": ColorProfile(0, (0.7, 1.0), (0.6, 0.9), 30, 0.7),
            "anxious": ColorProfile(15, (0.6, 0.9), (0.5, 0.8), 25, 0.6),
            "unstable": ColorProfile(345, (0.8, 1.0), (0.7, 0.95), 35, 0.8),
            "chaotic": ColorProfile(330, (0.9, 1.0), (0.8, 1.0), 40, 0.9),
            
            # Reflective states - Purple/violet spectrum
            "reflective": ColorProfile(280, (0.5, 0.8), (0.6, 0.85), 10, 0.35),
            "contemplative": ColorProfile(260, (0.4, 0.7), (0.5, 0.8), 8, 0.3),
            "introspective": ColorProfile(300, (0.6, 0.9), (0.7, 0.9), 12, 0.4),
            "philosophical": ColorProfile(290, (0.5, 0.7), (0.6, 0.8), 5, 0.25),
            
            # Creative states - Cyan/magenta spectrum
            "creative": ColorProfile(180, (0.6, 0.9), (0.8, 1.0), 20, 0.5),
            "inspired": ColorProfile(320, (0.7, 1.0), (0.9, 1.0), 25, 0.6),
            "imaginative": ColorProfile(200, (0.5, 0.8), (0.7, 0.95), 15, 0.4),
            "artistic": ColorProfile(310, (0.6, 0.8), (0.8, 0.95), 18, 0.45),
            
            # Curious states - Green-yellow spectrum
            "curious": ColorProfile(80, (0.6, 0.9), (0.7, 0.9), 12, 0.4),
            "inquisitive": ColorProfile(100, (0.5, 0.8), (0.6, 0.85), 10, 0.35),
            "exploratory": ColorProfile(90, (0.7, 1.0), (0.8, 0.95), 15, 0.5),
            
            # Special DAWN states
            "blooming": ColorProfile(340, (0.7, 1.0), (0.8, 1.0), 20, 0.6),
            "reblooming": ColorProfile(290, (0.8, 1.0), (0.9, 1.0), 30, 0.7),
            "thermal_peak": ColorProfile(15, (0.9, 1.0), (0.95, 1.0), 45, 1.0),
            "consciousness_flux": ColorProfile(240, (0.6, 0.9), (0.7, 0.95), 25, 0.5),
            
            # Default/neutral
            "neutral": ColorProfile(200, (0.3, 0.6), (0.5, 0.8), 5, 0.3),
            "undefined": ColorProfile(0, (0.0, 0.2), (0.3, 0.6), 0, 0.2)
        }
        
        # Entropy gradient configurations
        self.entropy_gradients = {
            "low": (0.0, 0.3),      # Stable, minimal entropy
            "moderate": (0.3, 0.6), # Normal entropy range
            "high": (0.6, 0.8),     # Elevated entropy
            "critical": (0.8, 1.0)  # Maximum entropy
        }
        
        # Thermal influence multipliers
        self.thermal_multipliers = {
            "cold": 0.7,    # Darker, muted colors
            "cool": 0.85,   # Slightly muted
            "normal": 1.0,  # No thermal influence
            "warm": 1.15,   # Brighter colors
            "hot": 1.3      # Very bright, intense colors
        }
        
        # Perceptual adjustment curves
        self.gamma_correction = 2.2
        self.perceptual_weights = {"red": 0.299, "green": 0.587, "blue": 0.114}
        
        logger.info("FractalColorizer initialized with advanced color mapping")
        
    def get_color(self, mood: str, entropy: float, 
                  thermal_state: Optional[str] = None,
                  output_format: ColorSpace = ColorSpace.HEX,
                  alpha: float = 1.0) -> str:
        """
        Return a color based on bloom mood and entropy with perceptual accuracy.
        
        Args:
            mood: Bloom mood state (e.g., 'calm', 'agitated', 'creative')
            entropy: Entropy value (0.0-1.0)
            thermal_state: Optional thermal influence ('cold', 'cool', 'normal', 'warm', 'hot')
            output_format: Color format to return
            alpha: Alpha channel value (0.0-1.0)
            
        Returns:
            Color string in requested format
        """
        # Get mood profile or use neutral as fallback
        mood_key = mood.lower() if mood else "neutral"
        profile = self.mood_profiles.get(mood_key, self.mood_profiles["neutral"])
        
        # Calculate entropy-adjusted hue
        entropy_clamped = max(0.0, min(1.0, entropy))
        hue_shift = profile.entropy_shift * entropy_clamped
        adjusted_hue = (profile.base_hue + hue_shift) % 360
        
        # Calculate saturation based on entropy
        sat_min, sat_max = profile.saturation_range
        saturation = sat_min + (sat_max - sat_min) * self._entropy_saturation_curve(entropy_clamped)
        
        # Calculate value/brightness
        val_min, val_max = profile.value_range
        base_value = val_min + (val_max - val_min) * (1.0 - entropy_clamped * 0.3)
        
        # Apply thermal influence
        thermal_multiplier = 1.0
        if thermal_state:
            thermal_multiplier = self.thermal_multipliers.get(thermal_state.lower(), 1.0)
            
        # Adjust brightness with thermal and perceptual correction
        adjusted_value = min(1.0, base_value * thermal_multiplier)
        adjusted_value = self._apply_perceptual_correction(adjusted_value, adjusted_hue)
        
        # Convert to requested format
        return self._format_color(adjusted_hue, saturation, adjusted_value, alpha, output_format)
        
    def get_entropy_gradient(self, entropy: float, 
                           base_color: Optional[str] = None,
                           steps: int = 10) -> List[str]:
        """
        Generate an entropy gradient showing color progression.
        
        Args:
            entropy: Current entropy value
            base_color: Base color to modify (hex), uses entropy-appropriate hue if None
            steps: Number of gradient steps
            
        Returns:
            List of hex colors representing entropy progression
        """
        if base_color:
            # Parse existing color and modify
            r, g, b = self._hex_to_rgb(base_color)
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            base_hue = h * 360
        else:
            # Choose hue based on entropy level
            base_hue = self._entropy_to_hue(entropy)
            
        gradient = []
        for i in range(steps):
            step_entropy = i / (steps - 1)
            
            # Shift hue towards red as entropy increases
            hue_shift = 60 * step_entropy  # Up to 60 degrees toward red
            adjusted_hue = (base_hue - hue_shift) % 360
            
            # Increase saturation and adjust brightness
            saturation = 0.3 + 0.7 * step_entropy
            value = 0.9 - 0.3 * step_entropy
            
            color = self._format_color(adjusted_hue, saturation, value, 1.0, ColorSpace.HEX)
            gradient.append(color)
            
        return gradient
        
    def get_mood_palette(self, mood: str, variations: int = 5) -> List[str]:
        """
        Generate a color palette for a specific mood.
        
        Args:
            mood: Mood to generate palette for
            variations: Number of color variations
            
        Returns:
            List of hex colors representing mood variations
        """
        profile = self.mood_profiles.get(mood.lower(), self.mood_profiles["neutral"])
        palette = []
        
        for i in range(variations):
            # Vary saturation and value within profile ranges
            sat_factor = i / (variations - 1) if variations > 1 else 0.5
            val_factor = 1.0 - i / (variations * 2)  # Slight value variation
            
            sat_min, sat_max = profile.saturation_range
            val_min, val_max = profile.value_range
            
            saturation = sat_min + (sat_max - sat_min) * sat_factor
            value = val_min + (val_max - val_min) * val_factor
            
            color = self._format_color(profile.base_hue, saturation, value, 1.0, ColorSpace.HEX)
            palette.append(color)
            
        return palette
        
    def get_thermal_visualization(self, thermal_level: float, 
                                base_mood: str = "neutral") -> str:
        """
        Get color representing thermal state overlaid on mood.
        
        Args:
            thermal_level: Thermal intensity (0.0-1.0)
            base_mood: Base mood to modify
            
        Returns:
            Hex color representing thermal state
        """
        # Use thermal-specific hue progression
        thermal_hue = 240 - (thermal_level * 240)  # Blue to red progression
        
        # High thermal = high saturation and brightness
        saturation = 0.4 + 0.6 * thermal_level
        value = 0.6 + 0.4 * thermal_level
        
        return self._format_color(thermal_hue, saturation, value, 1.0, ColorSpace.HEX)
        
    def blend_colors(self, color1: str, color2: str, 
                    blend_factor: float = 0.5) -> str:
        """
        Blend two colors with perceptual accuracy.
        
        Args:
            color1: First hex color
            color2: Second hex color
            blend_factor: Blend amount (0.0=color1, 1.0=color2)
            
        Returns:
            Blended hex color
        """
        # Convert to RGB
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)
        
        # Perceptual blending using gamma correction
        r1_linear = (r1 / 255) ** self.gamma_correction
        g1_linear = (g1 / 255) ** self.gamma_correction
        b1_linear = (b1 / 255) ** self.gamma_correction
        
        r2_linear = (r2 / 255) ** self.gamma_correction
        g2_linear = (g2 / 255) ** self.gamma_correction
        b2_linear = (b2 / 255) ** self.gamma_correction
        
        # Blend in linear space
        r_blend = r1_linear + (r2_linear - r1_linear) * blend_factor
        g_blend = g1_linear + (g2_linear - g1_linear) * blend_factor
        b_blend = b1_linear + (b2_linear - b1_linear) * blend_factor
        
        # Convert back to sRGB
        r_final = int((r_blend ** (1/self.gamma_correction)) * 255)
        g_final = int((g_blend ** (1/self.gamma_correction)) * 255)
        b_final = int((b_blend ** (1/self.gamma_correction)) * 255)
        
        return f"#{r_final:02x}{g_final:02x}{b_final:02x}"
        
    def analyze_color_harmony(self, colors: List[str]) -> Dict[str, float]:
        """
        Analyze harmony metrics for a list of colors.
        
        Args:
            colors: List of hex colors to analyze
            
        Returns:
            Dictionary of harmony metrics
        """
        if len(colors) < 2:
            return {"harmony_score": 1.0, "contrast_ratio": 0.0}
            
        # Convert to HSV for analysis
        hsv_colors = []
        for color in colors:
            r, g, b = self._hex_to_rgb(color)
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            hsv_colors.append((h * 360, s, v))
            
        # Calculate metrics
        hue_variance = self._calculate_hue_variance(hsv_colors)
        saturation_harmony = self._calculate_saturation_harmony(hsv_colors)
        brightness_balance = self._calculate_brightness_balance(hsv_colors)
        
        # Overall harmony score
        harmony_score = (saturation_harmony + brightness_balance) / 2 * (1 - hue_variance / 180)
        
        return {
            "harmony_score": max(0.0, min(1.0, harmony_score)),
            "hue_variance": hue_variance,
            "saturation_harmony": saturation_harmony,
            "brightness_balance": brightness_balance
        }
        
    def _entropy_saturation_curve(self, entropy: float) -> float:
        """Apply non-linear curve to entropy for saturation mapping"""
        # S-curve for more natural color progression
        return 1 / (1 + math.exp(-6 * (entropy - 0.5)))
        
    def _entropy_to_hue(self, entropy: float) -> float:
        """Map entropy value to appropriate hue"""
        # Low entropy = blue/green, high entropy = red/orange
        return 240 - (entropy * 200)  # 240° (blue) to 40° (orange)
        
    def _apply_perceptual_correction(self, value: float, hue: float) -> float:
        """Apply perceptual brightness correction based on hue"""
        # Human eye perceives different hues at different brightnesses
        if 45 <= hue <= 75:  # Yellow region - appears brighter
            return min(1.0, value * 0.9)
        elif 240 <= hue <= 270:  # Blue region - appears darker
            return min(1.0, value * 1.1)
        return value
        
    def _format_color(self, hue: float, saturation: float, value: float,
                     alpha: float, output_format: ColorSpace) -> str:
        """Convert HSV to requested color format"""
        # Clamp values
        hue = hue % 360
        saturation = max(0.0, min(1.0, saturation))
        value = max(0.0, min(1.0, value))
        alpha = max(0.0, min(1.0, alpha))
        
        if output_format == ColorSpace.HSV:
            return f"hsv({hue:.1f}, {saturation:.3f}, {value:.3f})"
        elif output_format == ColorSpace.HSL:
            # Convert HSV to HSL
            hsl_h = hue
            hsl_l = value * (1 - saturation / 2)
            hsl_s = 0 if hsl_l == 0 or hsl_l == 1 else (value - hsl_l) / min(hsl_l, 1 - hsl_l)
            return f"hsl({hsl_h:.1f}, {hsl_s:.3f}, {hsl_l:.3f})"
        else:
            # Convert to RGB
            r, g, b = colorsys.hsv_to_rgb(hue / 360, saturation, value)
            r_int, g_int, b_int = int(r * 255), int(g * 255), int(b * 255)
            
            if output_format == ColorSpace.RGB:
                if alpha < 1.0:
                    return f"rgba({r_int}, {g_int}, {b_int}, {alpha:.3f})"
                else:
                    return f"rgb({r_int}, {g_int}, {b_int})"
            else:  # HEX
                if alpha < 1.0:
                    alpha_hex = format(int(alpha * 255), '02x')
                    return f"#{r_int:02x}{g_int:02x}{b_int:02x}{alpha_hex}"
                else:
                    return f"#{r_int:02x}{g_int:02x}{b_int:02x}"
                    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def _calculate_hue_variance(self, hsv_colors: List[Tuple[float, float, float]]) -> float:
        """Calculate variance in hue values"""
        hues = [color[0] for color in hsv_colors]
        if len(hues) < 2:
            return 0.0
        
        # Handle circular nature of hue
        avg_hue = sum(hues) / len(hues)
        variance = sum((h - avg_hue) ** 2 for h in hues) / len(hues)
        return math.sqrt(variance)
        
    def _calculate_saturation_harmony(self, hsv_colors: List[Tuple[float, float, float]]) -> float:
        """Calculate saturation harmony score"""
        saturations = [color[1] for color in hsv_colors]
        if len(saturations) < 2:
            return 1.0
        
        # Lower variance in saturation = better harmony
        avg_sat = sum(saturations) / len(saturations)
        variance = sum((s - avg_sat) ** 2 for s in saturations) / len(saturations)
        return 1.0 - min(1.0, variance * 2)
        
    def _calculate_brightness_balance(self, hsv_colors: List[Tuple[float, float, float]]) -> float:
        """Calculate brightness balance score"""
        values = [color[2] for color in hsv_colors]
        if len(values) < 2:
            return 1.0
        
        # Good balance has values distributed across range
        value_range = max(values) - min(values)
        return min(1.0, value_range * 2)  # Reward wider value distribution
        
    def get_available_moods(self) -> List[str]:
        """Get list of all available mood profiles"""
        return list(self.mood_profiles.keys())
        
    def create_custom_mood(self, name: str, base_hue: float, 
                          saturation_range: Tuple[float, float],
                          value_range: Tuple[float, float],
                          entropy_shift: float = 10,
                          thermal_sensitivity: float = 0.5) -> None:
        """
        Create a custom mood color profile.
        
        Args:
            name: Name for the new mood profile
            base_hue: Base hue value (0-360)
            saturation_range: Min/max saturation values
            value_range: Min/max value/brightness values
            entropy_shift: Hue shift per entropy unit
            thermal_sensitivity: Thermal influence factor
        """
        self.mood_profiles[name.lower()] = ColorProfile(
            base_hue, saturation_range, value_range, 
            entropy_shift, thermal_sensitivity
        )
        logger.info(f"Created custom mood profile: {name}")


# Convenience functions for quick color generation
def quick_mood_color(mood: str, entropy: float = 0.5) -> str:
    """Quick function to get mood color"""
    colorizer = FractalColorizer()
    return colorizer.get_color(mood, entropy)


def entropy_heat_map(entropy_values: List[float]) -> List[str]:
    """Generate heat map colors for entropy values"""
    colorizer = FractalColorizer()
    return [colorizer.get_thermal_visualization(e) for e in entropy_values]


def bloom_color_sequence(mood: str, entropy_progression: List[float]) -> List[str]:
    """Generate color sequence for bloom evolution"""
    colorizer = FractalColorizer()
    return [colorizer.get_color(mood, e) for e in entropy_progression] 