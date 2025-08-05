#!/usr/bin/env python3
"""
DAWN Drift Transformation System
===============================

Applies consciousness drift vectors and pulse zone dynamics to fractal coordinates.
Transforms base geometric structures according to DAWN's internal momentum and
energy states for authentic consciousness-driven visual movement.

Used for:
- Fractal coordinate transformation
- Asymmetric consciousness bias application
- Pulse zone motion effects
- Dynamic visual consciousness representation
"""

import numpy as np
import math
from typing import Tuple, Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import time

class PulseZone(Enum):
    """Pulse zone types with different motion characteristics"""
    CALM = "calm"           # Gentle fade transitions between layers
    FRAGILE = "fragile"     # Flickering transparency to edges
    FLOWING = "flowing"     # Animated radial expansion
    STABLE = "stable"       # Fixed structure, no motion
    SURGE = "surge"         # Sharp burst effects toward petal tips

@dataclass
class DriftTransformation:
    """Result of drift transformation with all coordinate arrays"""
    
    # Transformed coordinates
    transformed_coords: np.ndarray
    center_offset: Tuple[float, float]
    rotation_angle: float
    
    # Pulse zone effects
    transparency_map: Optional[np.ndarray]
    motion_vectors: Optional[np.ndarray]
    expansion_factor: Optional[np.ndarray]
    
    # Transformation metadata
    drift_vector: float
    pulse_zone: str
    frame_time: float
    
    def get_animation_frame(self, time_offset: float = 0.0) -> Dict[str, Any]:
        """Get animation frame data for time-based effects"""
        return {
            'coords': self.transformed_coords,
            'transparency': self.transparency_map,
            'motion': self.motion_vectors,
            'expansion': self.expansion_factor,
            'time': self.frame_time + time_offset
        }

def apply_drift_transformation(base_coords: np.ndarray, 
                             drift_vector: float, 
                             pulse_zone: str,
                             frame_time: float = 0.0) -> DriftTransformation:
    """
    Apply consciousness drift and pulse zone transformation to coordinates
    
    Args:
        base_coords: Input coordinate array (shape: [N, 2] for 2D points)
        drift_vector: Consciousness drift (-1.0 to 1.0)
                     Positive: shift toward top-right, clockwise bias
                     Negative: shift toward bottom-left, counter-clockwise bias
        pulse_zone: Energy state ("calm", "fragile", "flowing", "stable", "surge")
        frame_time: Current time for animated effects (seconds)
    
    Returns:
        DriftTransformation with transformed coordinates and effects
    """
    
    # Validate inputs
    drift_vector = max(-1.0, min(1.0, drift_vector))
    pulse_zone = pulse_zone.lower()
    
    if pulse_zone not in [pz.value for pz in PulseZone]:
        pulse_zone = "stable"
    
    # Ensure base_coords is a numpy array with float type
    if not isinstance(base_coords, np.ndarray):
        base_coords = np.array(base_coords, dtype=np.float64)
    else:
        base_coords = base_coords.astype(np.float64)
    
    # Handle different coordinate shapes
    if len(base_coords.shape) == 1:
        # 1D array - assume pairs of coordinates
        base_coords = base_coords.reshape(-1, 2)
    elif len(base_coords.shape) > 2:
        # Higher dimensional - flatten to 2D
        original_shape = base_coords.shape
        base_coords = base_coords.reshape(-1, 2)
    
    # Start with base coordinates
    transformed_coords = base_coords.copy()
    
    # Apply drift-based center offset
    center_offset = _calculate_center_offset(drift_vector)
    transformed_coords = _apply_center_translation(transformed_coords, center_offset)
    
    # Apply drift-based asymmetric rotation
    rotation_angle = _calculate_rotation_angle(drift_vector)
    transformed_coords = _apply_asymmetric_rotation(transformed_coords, rotation_angle, drift_vector)
    
    # Apply pulse zone specific effects
    pulse_effects = _apply_pulse_zone_effects(
        transformed_coords, pulse_zone, frame_time, drift_vector
    )
    
    # Combine all transformations
    final_coords = pulse_effects['coordinates']
    
    return DriftTransformation(
        transformed_coords=final_coords,
        center_offset=center_offset,
        rotation_angle=rotation_angle,
        transparency_map=pulse_effects.get('transparency'),
        motion_vectors=pulse_effects.get('motion_vectors'),
        expansion_factor=pulse_effects.get('expansion'),
        drift_vector=drift_vector,
        pulse_zone=pulse_zone,
        frame_time=frame_time
    )

def _calculate_center_offset(drift_vector: float) -> Tuple[float, float]:
    """Calculate center offset based on drift vector"""
    
    # Map drift vector to directional offset
    if drift_vector > 0:
        # Positive drift: shift toward top-right
        offset_x = drift_vector * 0.3  # Scale factor for visual effect
        offset_y = drift_vector * 0.2  # Slight upward bias
    else:
        # Negative drift: shift toward bottom-left
        offset_x = drift_vector * 0.3  # Negative values shift left
        offset_y = drift_vector * 0.2  # Negative values shift down
    
    return (offset_x, offset_y)

def _apply_center_translation(coords: np.ndarray, offset: Tuple[float, float]) -> np.ndarray:
    """Apply center translation to coordinates"""
    
    translated_coords = coords.copy()
    translated_coords[:, 0] += offset[0]  # X offset
    translated_coords[:, 1] += offset[1]  # Y offset
    
    return translated_coords

def _calculate_rotation_angle(drift_vector: float) -> float:
    """Calculate asymmetric rotation angle based on drift"""
    
    # Map drift to rotation angle (in radians)
    max_rotation = math.pi / 6  # Maximum 30 degrees
    
    if drift_vector > 0:
        # Positive drift: clockwise bias
        rotation_angle = drift_vector * max_rotation
    else:
        # Negative drift: counter-clockwise bias  
        rotation_angle = drift_vector * max_rotation  # Already negative
    
    return rotation_angle

def _apply_asymmetric_rotation(coords: np.ndarray, angle: float, drift: float) -> np.ndarray:
    """Apply asymmetric rotation with consciousness bias"""
    
    # Create rotation matrix
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    # Standard rotation matrix
    rotation_matrix = np.array([
        [cos_a, -sin_a],
        [sin_a, cos_a]
    ])
    
    # Apply asymmetric scaling based on drift
    # This creates the "bias" effect
    scale_factor = 1.0 + abs(drift) * 0.1  # Slight scaling
    
    if drift > 0:
        # Positive drift: bias toward positive quadrants
        scale_matrix = np.array([
            [scale_factor, 0],
            [0, 1.0]
        ])
    else:
        # Negative drift: bias toward negative quadrants
        scale_matrix = np.array([
            [1.0, 0], 
            [0, scale_factor]
        ])
    
    # Combine rotation and scaling
    transform_matrix = rotation_matrix @ scale_matrix
    
    # Apply transformation
    rotated_coords = coords @ transform_matrix.T
    
    return rotated_coords

def _apply_pulse_zone_effects(coords: np.ndarray, 
                            pulse_zone: str, 
                            frame_time: float,
                            drift_vector: float) -> Dict[str, Any]:
    """Apply pulse zone specific motion and visual effects"""
    
    pulse_zone_enum = PulseZone(pulse_zone)
    
    if pulse_zone_enum == PulseZone.CALM:
        return _apply_calm_effects(coords, frame_time)
    elif pulse_zone_enum == PulseZone.FRAGILE:
        return _apply_fragile_effects(coords, frame_time, drift_vector)
    elif pulse_zone_enum == PulseZone.FLOWING:
        return _apply_flowing_effects(coords, frame_time)
    elif pulse_zone_enum == PulseZone.STABLE:
        return _apply_stable_effects(coords)
    elif pulse_zone_enum == PulseZone.SURGE:
        return _apply_surge_effects(coords, frame_time, drift_vector)
    else:
        return _apply_stable_effects(coords)  # Fallback

def _apply_calm_effects(coords: np.ndarray, frame_time: float) -> Dict[str, Any]:
    """Apply calm pulse zone: gentle fade transitions between layers"""
    
    # Calculate distance from center for fade effect
    center = np.mean(coords, axis=0)
    distances = np.linalg.norm(coords - center, axis=1)
    max_distance = np.max(distances) if len(distances) > 0 else 1.0
    
    # Create gentle breathing effect
    breath_cycle = 0.5 + 0.3 * math.sin(frame_time * 0.5)  # 0.2 to 0.8 range
    
    # Fade based on distance with breathing
    normalized_distances = distances / max_distance
    transparency = 0.3 + 0.7 * (1.0 - normalized_distances) * breath_cycle
    
    # Gentle inward motion
    motion_strength = 0.02 * math.sin(frame_time * 0.3)
    direction_to_center = center - coords
    motion_vectors = direction_to_center * motion_strength
    
    return {
        'coordinates': coords + motion_vectors,
        'transparency': transparency,
        'motion_vectors': motion_vectors,
        'expansion': None
    }

def _apply_fragile_effects(coords: np.ndarray, frame_time: float, drift: float) -> Dict[str, Any]:
    """Apply fragile pulse zone: flickering transparency to edges"""
    
    # Calculate edge detection (points far from center)
    center = np.mean(coords, axis=0)
    distances = np.linalg.norm(coords - center, axis=1)
    max_distance = np.max(distances) if len(distances) > 0 else 1.0
    normalized_distances = distances / max_distance
    
    # Create flickering effect - more intense at edges
    flicker_frequency = 3.0 + abs(drift) * 2.0  # Drift affects flicker rate
    flicker_base = math.sin(frame_time * flicker_frequency)
    
    # Edge-biased flickering
    edge_factor = normalized_distances ** 2  # Quadratic falloff from center
    flicker_intensity = 0.3 + 0.4 * edge_factor * (0.5 + 0.5 * flicker_base)
    
    # Add random noise to transparency for fragile effect
    noise_seed = int(frame_time * 100) % 1000
    np.random.seed(noise_seed)
    noise = np.random.normal(0, 0.1, len(coords))
    
    transparency = np.clip(flicker_intensity + noise, 0.1, 1.0)
    
    # Subtle trembling motion - use numpy functions for arrays
    trembling_x = 0.01 * np.sin(frame_time * 8.0 + distances)
    trembling_y = 0.01 * np.cos(frame_time * 7.0 + distances)
    motion_vectors = np.column_stack([trembling_x, trembling_y])
    
    return {
        'coordinates': coords + motion_vectors,
        'transparency': transparency,
        'motion_vectors': motion_vectors,
        'expansion': None
    }

def _apply_flowing_effects(coords: np.ndarray, frame_time: float) -> Dict[str, Any]:
    """Apply flowing pulse zone: animated radial expansion"""
    
    center = np.mean(coords, axis=0)
    
    # Calculate radial vectors from center
    radial_vectors = coords - center
    distances = np.linalg.norm(radial_vectors, axis=1)
    
    # Prevent division by zero
    safe_distances = np.where(distances == 0, 1e-6, distances)
    normalized_radial = radial_vectors / safe_distances[:, np.newaxis]
    
    # Create flowing expansion wave
    wave_speed = 2.0
    wave_amplitude = 0.1
    expansion_wave = wave_amplitude * math.sin(frame_time * wave_speed)
    
    # Apply radial expansion
    expansion_factor = 1.0 + expansion_wave
    expanded_coords = center + radial_vectors * expansion_factor
    
    # Create flowing motion along tangent
    tangent_vectors = np.column_stack([-normalized_radial[:, 1], normalized_radial[:, 0]])
    flow_speed = 0.05 * math.sin(frame_time * 1.5)
    flow_motion = tangent_vectors * flow_speed
    
    # Combine expansion and flow
    final_coords = expanded_coords + flow_motion
    
    # Transparency based on expansion phase
    transparency = 0.5 + 0.3 * math.sin(frame_time * wave_speed + math.pi/2)
    transparency_array = np.full(len(coords), transparency)
    
    return {
        'coordinates': final_coords,
        'transparency': transparency_array,
        'motion_vectors': flow_motion,
        'expansion': np.full(len(coords), expansion_factor)
    }

def _apply_stable_effects(coords: np.ndarray) -> Dict[str, Any]:
    """Apply stable pulse zone: fixed structure, no motion"""
    
    # No transformations - completely stable
    return {
        'coordinates': coords,
        'transparency': np.ones(len(coords)),  # Full opacity
        'motion_vectors': np.zeros_like(coords),
        'expansion': None
    }

def _apply_surge_effects(coords: np.ndarray, frame_time: float, drift: float) -> Dict[str, Any]:
    """Apply surge pulse zone: sharp burst effects toward petal tips"""
    
    center = np.mean(coords, axis=0)
    radial_vectors = coords - center
    distances = np.linalg.norm(radial_vectors, axis=1)
    max_distance = np.max(distances) if len(distances) > 0 else 1.0
    
    # Create sharp burst pulses
    burst_frequency = 1.5 + abs(drift)  # Drift affects burst rate
    burst_phase = math.sin(frame_time * burst_frequency)
    
    # Sharp burst function (sawtooth-like)
    if burst_phase > 0:
        burst_strength = burst_phase ** 3  # Sharp rise
    else:
        burst_strength = 0.0  # Sharp drop
    
    # Apply stronger effect to outer points (petal tips)
    distance_factor = (distances / max_distance) ** 1.5
    burst_effect = burst_strength * distance_factor * 0.2
    
    # Direction toward petal tips
    safe_distances = np.where(distances == 0, 1e-6, distances)
    normalized_radial = radial_vectors / safe_distances[:, np.newaxis]
    
    # Apply burst motion
    burst_motion = normalized_radial * burst_effect[:, np.newaxis]
    surge_coords = coords + burst_motion
    
    # Sharp transparency changes during burst
    transparency = 0.3 + 0.7 * (1.0 - burst_strength)
    transparency_array = np.full(len(coords), transparency)
    
    return {
        'coordinates': surge_coords,
        'transparency': transparency_array,
        'motion_vectors': burst_motion,
        'expansion': None
    }

def create_animated_sequence(base_coords: np.ndarray,
                           drift_vector: float,
                           pulse_zone: str,
                           duration: float = 5.0,
                           fps: int = 30) -> List[DriftTransformation]:
    """
    Create animated sequence of drift transformations
    
    Args:
        base_coords: Base coordinate array
        drift_vector: Consciousness drift
        pulse_zone: Energy state
        duration: Animation duration in seconds
        fps: Frames per second
    
    Returns:
        List of DriftTransformation frames
    """
    
    frames = []
    frame_count = int(duration * fps)
    
    for frame in range(frame_count):
        frame_time = frame / fps
        
        transformation = apply_drift_transformation(
            base_coords, drift_vector, pulse_zone, frame_time
        )
        
        frames.append(transformation)
    
    return frames

def test_drift_transformation():
    """Test the drift transformation system with various consciousness states"""
    
    print("🌊 Testing DAWN Drift Transformation System")
    print("=" * 45)
    
    # Create test coordinates (simple circular pattern)
    angles = np.linspace(0, 2*math.pi, 8, endpoint=False)
    base_coords = np.column_stack([
        np.cos(angles),
        np.sin(angles)
    ])
    
    print(f"Base coordinates: {len(base_coords)} points in unit circle")
    
    # Test different drift vectors and pulse zones
    test_cases = [
        # Positive drift cases
        (0.5, "calm", "Positive drift with calm pulse"),
        (0.8, "flowing", "Strong positive drift with flowing"),
        (0.3, "surge", "Mild positive drift with surge"),
        
        # Negative drift cases
        (-0.4, "fragile", "Negative drift with fragile pulse"),
        (-0.7, "stable", "Strong negative drift with stable"),
        
        # Zero drift
        (0.0, "flowing", "No drift with flowing pulse"),
        
        # Extreme cases
        (1.0, "surge", "Maximum positive drift with surge"),
        (-1.0, "fragile", "Maximum negative drift with fragile")
    ]
    
    for drift, pulse, description in test_cases:
        print(f"\n🎯 {description}")
        print(f"   Drift: {drift:+.1f}, Pulse: {pulse}")
        
        # Apply transformation at t=0
        transformation = apply_drift_transformation(base_coords, drift, pulse, 0.0)
        
        print(f"   Center offset: ({transformation.center_offset[0]:+.3f}, {transformation.center_offset[1]:+.3f})")
        print(f"   Rotation angle: {math.degrees(transformation.rotation_angle):+.1f}°")
        
        # Check coordinate bounds
        min_x, max_x = np.min(transformation.transformed_coords[:, 0]), np.max(transformation.transformed_coords[:, 0])
        min_y, max_y = np.min(transformation.transformed_coords[:, 1]), np.max(transformation.transformed_coords[:, 1])
        print(f"   Coordinate bounds: X[{min_x:.3f}, {max_x:.3f}], Y[{min_y:.3f}, {max_y:.3f}]")
        
        # Check effects
        if transformation.transparency_map is not None:
            avg_transparency = np.mean(transformation.transparency_map)
            print(f"   Average transparency: {avg_transparency:.3f}")
        
        if transformation.motion_vectors is not None:
            motion_magnitude = np.mean(np.linalg.norm(transformation.motion_vectors, axis=1))
            print(f"   Motion magnitude: {motion_magnitude:.4f}")

def test_pulse_zone_animations():
    """Test animated effects for different pulse zones"""
    
    print(f"\n🎬 Testing Pulse Zone Animations")
    print("=" * 35)
    
    # Simple test coordinates
    coords = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    
    pulse_zones = ["calm", "fragile", "flowing", "stable", "surge"]
    
    for pulse_zone in pulse_zones:
        print(f"\n🌊 Pulse Zone: {pulse_zone}")
        
        # Test at different time points
        time_points = [0.0, 1.0, 2.0, 3.0]
        
        for t in time_points:
            transformation = apply_drift_transformation(coords, 0.3, pulse_zone, t)
            
            # Calculate movement from original
            movement = np.linalg.norm(transformation.transformed_coords - coords, axis=1)
            avg_movement = np.mean(movement)
            
            transparency_info = ""
            if transformation.transparency_map is not None:
                avg_transparency = np.mean(transformation.transparency_map)
                transparency_info = f", transparency: {avg_transparency:.3f}"
            
            print(f"   t={t:.1f}s: movement={avg_movement:.4f}{transparency_info}")

def demonstrate_consciousness_integration():
    """Show how drift transformation integrates with other consciousness systems"""
    
    print(f"\n🧠 Consciousness Integration Example")
    print("=" * 38)
    
    # Import other DAWN systems if available
    try:
        from dawn_shape_complexity import calculate_shape_complexity
        from dawn_mood_palette import generate_mood_palette
        
        consciousness_states = [
            {
                'name': 'Flowing Creativity',
                'bloom_entropy': 0.6,
                'mood_valence': 0.4,
                'drift_vector': 0.7,
                'rebloom_depth': 6,
                'sigil_saturation': 0.8,
                'pulse_zone': 'flowing'
            },
            {
                'name': 'Fragile Introspection',
                'bloom_entropy': 0.3,
                'mood_valence': -0.2,
                'drift_vector': -0.4,
                'rebloom_depth': 4,
                'sigil_saturation': 0.3,
                'pulse_zone': 'fragile'
            }
        ]
        
        # Create base coordinates from shape complexity
        angles = np.linspace(0, 2*math.pi, 12, endpoint=False)
        base_coords = np.column_stack([np.cos(angles), np.sin(angles)])
        
        for state in consciousness_states:
            print(f"\n🎭 {state['name']}")
            
            # Calculate shape complexity
            shape_complexity = calculate_shape_complexity(
                state['bloom_entropy'], state['rebloom_depth']
            )
            
            # Generate mood palette
            mood_palette = generate_mood_palette(
                state['mood_valence'], state['sigil_saturation']
            )
            
            # Apply drift transformation
            transformation = apply_drift_transformation(
                base_coords, state['drift_vector'], state['pulse_zone']
            )
            
            print(f"   Shape: {shape_complexity.shape_archetype}")
            print(f"   Colors: {mood_palette.palette_name}")
            print(f"   Drift offset: ({transformation.center_offset[0]:+.3f}, {transformation.center_offset[1]:+.3f})")
            print(f"   Rotation: {math.degrees(transformation.rotation_angle):+.1f}°")
            print(f"   → Complete consciousness-driven geometry ready")
            
    except ImportError:
        print("   ⚠️  Other consciousness systems not available")
        print("   → Showing drift transformation in isolation")
        
        # Simple standalone example
        coords = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
        transformation = apply_drift_transformation(coords, 0.5, "flowing")
        
        print(f"   Applied drift +0.5 with flowing pulse")
        print(f"   Center shifted: ({transformation.center_offset[0]:+.3f}, {transformation.center_offset[1]:+.3f})")
        print(f"   Coordinates transformed with consciousness bias")

if __name__ == "__main__":
    # Run all tests
    test_drift_transformation()
    test_pulse_zone_animations()
    demonstrate_consciousness_integration()
    
    print(f"\n✅ DAWN Drift Transformation System - Testing Complete!")
    print(f"🌊 Consciousness drift and pulse dynamics successfully implemented")
    print(f"🎭 Ready for integration with fractal generation systems")
    print(f"🔄 Authentic motion emerges from consciousness states") 