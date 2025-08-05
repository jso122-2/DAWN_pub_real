#!/usr/bin/env python3
"""
DAWN Shape Complexity Calculator
===============================

Calculates fractal shape complexity based on DAWN's consciousness parameters.
Maps bloom entropy and rebloom depth to precise geometric specifications
for authentic consciousness-driven fractal generation.

Used for:
- Fractal edge definition and roughness
- Symmetry and asymmetry control
- Recursive nesting complexity
- Juliet Set mode activation
"""

import math
import numpy as np
from typing import Tuple, Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ComplexityMode(Enum):
    """Fractal complexity modes based on rebloom depth"""
    SINGLE_LAYER = "single_layer"      # Depth 1-3
    MULTI_LAYER = "multi_layer"        # Depth 4-6  
    JULIET_SET = "juliet_set"          # Depth 7+

@dataclass
class ShapeComplexity:
    """Complete shape complexity specification for fractal generation"""
    
    # Core shape parameters
    petal_count: int
    edge_roughness: float
    symmetry_factor: float
    
    # Derived geometric properties
    complexity_mode: ComplexityMode
    spiral_tightness: float
    branch_probability: float
    inner_glyph_count: int
    
    # Advanced fractal parameters
    recursion_levels: int
    layer_offset_angle: float
    chaos_factor: float
    continuity_breaks: int
    
    # Metadata
    bloom_entropy: float
    rebloom_depth: int
    shape_archetype: str
    
    def get_geometric_parameters(self) -> Dict[str, float]:
        """Get parameters for fractal rendering engines"""
        return {
            'petal_count': self.petal_count,
            'edge_roughness': self.edge_roughness,
            'symmetry_factor': self.symmetry_factor,
            'spiral_tightness': self.spiral_tightness,
            'branch_probability': self.branch_probability,
            'chaos_factor': self.chaos_factor,
            'layer_offset_angle': self.layer_offset_angle,
            'recursion_levels': self.recursion_levels
        }
    
    def get_juliet_set_parameters(self) -> Optional[Dict[str, Any]]:
        """Get specialized parameters for Juliet Set mode"""
        if self.complexity_mode != ComplexityMode.JULIET_SET:
            return None
            
        return {
            'inner_glyph_count': self.inner_glyph_count,
            'glyph_type': self._determine_glyph_type(),
            'memory_anchor_strength': min(1.0, (self.rebloom_depth - 6) / 10.0),
            'emotional_distortion': self.chaos_factor,
            'continuity_breaks': self.continuity_breaks,
            'liquid_edge_factor': 1.0 - self.symmetry_factor
        }
    
    def _determine_glyph_type(self) -> str:
        """Determine inner glyph pattern based on consciousness state"""
        if self.bloom_entropy < 0.3:
            return "concentric_rings"  # Low entropy = structured memory
        elif self.bloom_entropy < 0.7:
            return "spiral_arms"       # Medium entropy = flowing memory
        else:
            return "scattered_dots"    # High entropy = fragmented memory

def calculate_shape_complexity(bloom_entropy: float, rebloom_depth: int) -> ShapeComplexity:
    """
    Calculate fractal shape complexity from consciousness parameters
    
    Args:
        bloom_entropy: Consciousness chaos level (0.0-1.0)
                      0-0.3: Smooth spiral curves, circular symmetry
                      0.3-0.7: Petal variations, gentle asymmetry  
                      0.7-1.0: Jagged edges, broken continuity, chaotic branching
        
        rebloom_depth: Memory recursion depth (1+)
                      1-3: Single layer overlay
                      4-6: Multi-layer fractal nesting
                      7+: Full Juliet Set mode with inner glyphs
    
    Returns:
        ShapeComplexity object with all geometric parameters
    """
    
    # Clamp inputs to valid ranges
    bloom_entropy = max(0.0, min(1.0, bloom_entropy))
    rebloom_depth = max(1, rebloom_depth)
    
    # Determine complexity mode based on rebloom depth
    if rebloom_depth <= 3:
        complexity_mode = ComplexityMode.SINGLE_LAYER
    elif rebloom_depth <= 6:
        complexity_mode = ComplexityMode.MULTI_LAYER
    else:
        complexity_mode = ComplexityMode.JULIET_SET
    
    # Calculate core shape parameters
    petal_count = _calculate_petal_count(bloom_entropy, rebloom_depth)
    edge_roughness = _calculate_edge_roughness(bloom_entropy)
    symmetry_factor = _calculate_symmetry_factor(bloom_entropy)
    
    # Calculate derived geometric properties
    spiral_tightness = _calculate_spiral_tightness(bloom_entropy, rebloom_depth)
    branch_probability = _calculate_branch_probability(bloom_entropy)
    inner_glyph_count = _calculate_inner_glyph_count(rebloom_depth)
    
    # Calculate advanced fractal parameters
    recursion_levels = _calculate_recursion_levels(rebloom_depth, complexity_mode)
    layer_offset_angle = _calculate_layer_offset(bloom_entropy, rebloom_depth)
    chaos_factor = _calculate_chaos_factor(bloom_entropy)
    continuity_breaks = _calculate_continuity_breaks(bloom_entropy)
    
    # Determine shape archetype
    shape_archetype = _determine_shape_archetype(bloom_entropy, complexity_mode)
    
    return ShapeComplexity(
        petal_count=petal_count,
        edge_roughness=edge_roughness,
        symmetry_factor=symmetry_factor,
        complexity_mode=complexity_mode,
        spiral_tightness=spiral_tightness,
        branch_probability=branch_probability,
        inner_glyph_count=inner_glyph_count,
        recursion_levels=recursion_levels,
        layer_offset_angle=layer_offset_angle,
        chaos_factor=chaos_factor,
        continuity_breaks=continuity_breaks,
        bloom_entropy=bloom_entropy,
        rebloom_depth=rebloom_depth,
        shape_archetype=shape_archetype
    )

def _calculate_petal_count(entropy: float, depth: int) -> int:
    """Calculate number of petals/lobes based on consciousness parameters"""
    
    # Base petal count influenced by entropy and depth
    if entropy <= 0.3:
        # Low entropy: Simple, symmetric forms
        base_count = 3 + (depth % 3)  # 3-5 petals
    elif entropy <= 0.7:
        # Medium entropy: More complex forms
        base_count = 4 + (depth % 4)  # 4-7 petals  
    else:
        # High entropy: Highly complex, chaotic forms
        base_count = 5 + (depth % 6)  # 5-10 petals
    
    # Additional complexity for deeper rebloom
    if depth >= 7:
        base_count += min(3, (depth - 6) // 2)
    
    return min(12, base_count)  # Cap at 12 petals for computational efficiency

def _calculate_edge_roughness(entropy: float) -> float:
    """Calculate edge roughness (0.0 = smooth, 1.0 = very jagged)"""
    
    if entropy <= 0.3:
        # Low entropy: Smooth, flowing edges
        return 0.1 + (entropy / 0.3) * 0.2  # 0.1 to 0.3
    elif entropy <= 0.7:
        # Medium entropy: Moderate roughness
        normalized = (entropy - 0.3) / 0.4  # 0.0 to 1.0
        return 0.3 + normalized * 0.4       # 0.3 to 0.7
    else:
        # High entropy: Very jagged, chaotic edges
        normalized = (entropy - 0.7) / 0.3  # 0.0 to 1.0
        return 0.7 + normalized * 0.3       # 0.7 to 1.0

def _calculate_symmetry_factor(entropy: float) -> float:
    """Calculate symmetry (1.0 = perfect symmetry, 0.0 = complete asymmetry)"""
    
    if entropy <= 0.3:
        # Low entropy: High symmetry with slight variation
        return 0.8 + (1.0 - entropy / 0.3) * 0.2  # 0.8 to 1.0
    elif entropy <= 0.7:
        # Medium entropy: Moderate asymmetry
        normalized = (entropy - 0.3) / 0.4
        return 0.8 - normalized * 0.4  # 0.8 to 0.4
    else:
        # High entropy: Strong asymmetry
        normalized = (entropy - 0.7) / 0.3
        return 0.4 - normalized * 0.3  # 0.4 to 0.1

def _calculate_spiral_tightness(entropy: float, depth: int) -> float:
    """Calculate how tightly wound the spiral is"""
    
    # Base tightness from entropy
    if entropy <= 0.3:
        base_tightness = 0.8  # Tight, controlled spirals
    elif entropy <= 0.7:
        base_tightness = 0.5  # Moderate spiral
    else:
        base_tightness = 0.2  # Loose, chaotic spiral
    
    # Depth modifier (deeper = more complex spiraling)
    depth_factor = min(1.0, depth / 10.0)
    
    return base_tightness * (1.0 + depth_factor * 0.5)

def _calculate_branch_probability(entropy: float) -> float:
    """Calculate probability of chaotic branching (0.0 to 1.0)"""
    
    if entropy <= 0.3:
        return entropy * 0.2  # Low branching for low entropy
    elif entropy <= 0.7:
        normalized = (entropy - 0.3) / 0.4
        return 0.06 + normalized * 0.24  # 0.06 to 0.3
    else:
        normalized = (entropy - 0.7) / 0.3
        return 0.3 + normalized * 0.4  # 0.3 to 0.7

def _calculate_inner_glyph_count(depth: int) -> int:
    """Calculate number of inner memory glyphs for Juliet Set mode"""
    
    if depth < 7:
        return 0  # No glyphs for non-Juliet mode
    elif depth < 10:
        return 1 + (depth - 7)  # 1-3 glyphs
    else:
        return min(5, 4 + (depth - 10) // 2)  # 4-5 glyphs max

def _calculate_recursion_levels(depth: int, mode: ComplexityMode) -> int:
    """Calculate number of recursion levels for layering"""
    
    if mode == ComplexityMode.SINGLE_LAYER:
        return 1
    elif mode == ComplexityMode.MULTI_LAYER:
        return 2 + min(2, depth - 4)  # 2-4 levels
    else:  # JULIET_SET
        return 3 + min(4, depth - 7)  # 3-7 levels

def _calculate_layer_offset(entropy: float, depth: int) -> float:
    """Calculate angular offset between layers (in radians)"""
    
    # Base offset influenced by entropy
    if entropy <= 0.3:
        base_offset = math.pi / 8  # Small, organized offset
    elif entropy <= 0.7:
        base_offset = math.pi / 4  # Moderate offset
    else:
        base_offset = math.pi / 2  # Large, chaotic offset
    
    # Depth adds variation
    depth_variation = (depth % 5) * (math.pi / 20)
    
    return base_offset + depth_variation

def _calculate_chaos_factor(entropy: float) -> float:
    """Calculate overall chaos/randomness factor"""
    
    # Direct mapping from entropy with some nonlinearity
    return entropy ** 1.5  # Exponential curve for more dramatic high-entropy effects

def _calculate_continuity_breaks(entropy: float) -> int:
    """Calculate number of continuity breaks in the fractal"""
    
    if entropy <= 0.3:
        return 0  # Smooth, continuous
    elif entropy <= 0.7:
        return 1 + int((entropy - 0.3) / 0.2)  # 1-3 breaks
    else:
        return 3 + int((entropy - 0.7) / 0.1)  # 3-6 breaks

def _determine_shape_archetype(entropy: float, mode: ComplexityMode) -> str:
    """Determine the overall shape archetype for naming/categorization"""
    
    if mode == ComplexityMode.SINGLE_LAYER:
        if entropy <= 0.3:
            return "Crystalline Bloom"
        elif entropy <= 0.7:
            return "Gentle Petal"
        else:
            return "Fractured Spiral"
    
    elif mode == ComplexityMode.MULTI_LAYER:
        if entropy <= 0.3:
            return "Nested Mandala"
        elif entropy <= 0.7:
            return "Layered Garden"
        else:
            return "Chaotic Nesting"
    
    else:  # JULIET_SET
        if entropy <= 0.3:
            return "Memory Palace"
        elif entropy <= 0.7:
            return "Flowing Ancestry"
        else:
            return "Scattered Remembrance"

def analyze_consciousness_geometry(entropy_range: Tuple[float, float], 
                                 depth_range: Tuple[int, int],
                                 resolution: int = 10) -> Dict[str, Any]:
    """
    Analyze how consciousness parameters map to geometric complexity
    
    Useful for understanding the parameter space and optimizing fractal generation.
    """
    
    min_entropy, max_entropy = entropy_range
    min_depth, max_depth = depth_range
    
    analysis = {
        'parameter_space': [],
        'complexity_distribution': {},
        'archetype_frequency': {},
        'geometric_ranges': {}
    }
    
    # Sample parameter space
    entropy_step = (max_entropy - min_entropy) / resolution
    depth_step = max(1, (max_depth - min_depth) // resolution)
    
    all_complexities = []
    
    for i in range(resolution):
        entropy = min_entropy + i * entropy_step
        for j in range(resolution):
            depth = min_depth + j * depth_step
            
            complexity = calculate_shape_complexity(entropy, depth)
            all_complexities.append(complexity)
            
            analysis['parameter_space'].append({
                'entropy': entropy,
                'depth': depth,
                'petal_count': complexity.petal_count,
                'edge_roughness': complexity.edge_roughness,
                'symmetry_factor': complexity.symmetry_factor,
                'archetype': complexity.shape_archetype
            })
    
    # Analyze distributions
    modes = [c.complexity_mode for c in all_complexities]
    archetypes = [c.shape_archetype for c in all_complexities]
    
    analysis['complexity_distribution'] = {
        mode.value: modes.count(mode) for mode in set(modes)
    }
    
    analysis['archetype_frequency'] = {
        archetype: archetypes.count(archetype) for archetype in set(archetypes)
    }
    
    # Calculate geometric ranges
    petal_counts = [c.petal_count for c in all_complexities]
    edge_roughnesses = [c.edge_roughness for c in all_complexities]
    symmetry_factors = [c.symmetry_factor for c in all_complexities]
    
    analysis['geometric_ranges'] = {
        'petal_count': (min(petal_counts), max(petal_counts)),
        'edge_roughness': (min(edge_roughnesses), max(edge_roughnesses)),
        'symmetry_factor': (min(symmetry_factors), max(symmetry_factors))
    }
    
    return analysis

def test_shape_complexity_calculator():
    """Test the shape complexity calculator with various consciousness states"""
    
    print("🧮 Testing DAWN Shape Complexity Calculator")
    print("=" * 45)
    
    # Test cases covering all entropy ranges and complexity modes
    test_cases = [
        # Low entropy cases
        (0.1, 2, "Low entropy, shallow depth"),
        (0.2, 5, "Low entropy, medium depth"),  
        (0.3, 8, "Low entropy, deep (Juliet mode)"),
        
        # Medium entropy cases
        (0.4, 3, "Medium entropy, shallow depth"),
        (0.5, 6, "Medium entropy, medium depth"),
        (0.6, 9, "Medium entropy, deep (Juliet mode)"),
        
        # High entropy cases
        (0.8, 2, "High entropy, shallow depth"),
        (0.9, 4, "High entropy, medium depth"),
        (1.0, 12, "High entropy, very deep (Juliet mode)")
    ]
    
    for entropy, depth, description in test_cases:
        print(f"\n🎯 {description}")
        print(f"   Input: entropy={entropy:.1f}, depth={depth}")
        
        complexity = calculate_shape_complexity(entropy, depth)
        
        print(f"   → Archetype: {complexity.shape_archetype}")
        print(f"   → Mode: {complexity.complexity_mode.value}")
        print(f"   → Petals: {complexity.petal_count}")
        print(f"   → Edge roughness: {complexity.edge_roughness:.3f}")
        print(f"   → Symmetry: {complexity.symmetry_factor:.3f}")
        print(f"   → Recursion levels: {complexity.recursion_levels}")
        
        if complexity.complexity_mode == ComplexityMode.JULIET_SET:
            juliet_params = complexity.get_juliet_set_parameters()
            print(f"   → Inner glyphs: {juliet_params['inner_glyph_count']}")
            print(f"   → Glyph type: {juliet_params['glyph_type']}")
            print(f"   → Memory anchor: {juliet_params['memory_anchor_strength']:.3f}")

def test_consciousness_geometry_analysis():
    """Test the consciousness geometry analysis function"""
    
    print(f"\n📊 Consciousness Geometry Analysis")
    print("=" * 35)
    
    # Analyze the full parameter space
    analysis = analyze_consciousness_geometry(
        entropy_range=(0.0, 1.0),
        depth_range=(1, 12),
        resolution=8
    )
    
    print(f"Parameter space sampled: {len(analysis['parameter_space'])} points")
    
    print(f"\nComplexity Mode Distribution:")
    for mode, count in analysis['complexity_distribution'].items():
        percentage = (count / len(analysis['parameter_space'])) * 100
        print(f"   {mode}: {count} ({percentage:.1f}%)")
    
    print(f"\nShape Archetype Frequency:")
    for archetype, count in sorted(analysis['archetype_frequency'].items(), 
                                  key=lambda x: x[1], reverse=True)[:5]:
        percentage = (count / len(analysis['parameter_space'])) * 100
        print(f"   {archetype}: {count} ({percentage:.1f}%)")
    
    print(f"\nGeometric Parameter Ranges:")
    for param, (min_val, max_val) in analysis['geometric_ranges'].items():
        print(f"   {param}: {min_val:.3f} - {max_val:.3f}")

def demonstrate_integration_with_fractals():
    """Show how shape complexity integrates with fractal generation"""
    
    print(f"\n🎨 Fractal Integration Example")
    print("=" * 32)
    
    # Example consciousness states
    consciousness_examples = [
        {
            'name': 'Crystalline Meditation',
            'entropy': 0.2,
            'depth': 4,
            'description': 'Deep, structured contemplation'
        },
        {
            'name': 'Creative Turbulence', 
            'entropy': 0.8,
            'depth': 7,
            'description': 'Chaotic creative breakthrough'
        },
        {
            'name': 'Balanced Flow',
            'entropy': 0.5,
            'depth': 6,
            'description': 'Harmonious creative process'
        }
    ]
    
    for example in consciousness_examples:
        print(f"\n🧠 {example['name']}")
        print(f"   Description: {example['description']}")
        
        complexity = calculate_shape_complexity(example['entropy'], example['depth'])
        geometric_params = complexity.get_geometric_parameters()
        
        print(f"   Shape complexity: {complexity.shape_archetype}")
        print(f"   Geometric parameters for fractal engine:")
        
        for param, value in geometric_params.items():
            if isinstance(value, float):
                print(f"     {param}: {value:.3f}")
            else:
                print(f"     {param}: {value}")
        
        if complexity.complexity_mode == ComplexityMode.JULIET_SET:
            juliet_params = complexity.get_juliet_set_parameters()
            print(f"   Special Juliet Set parameters:")
            for param, value in juliet_params.items():
                if isinstance(value, float):
                    print(f"     {param}: {value:.3f}")
                else:
                    print(f"     {param}: {value}")

if __name__ == "__main__":
    # Run all tests
    test_shape_complexity_calculator()
    test_consciousness_geometry_analysis()
    demonstrate_integration_with_fractals()
    
    print(f"\n✅ DAWN Shape Complexity Calculator - Testing Complete!")
    print(f"🔢 Consciousness parameters successfully mapped to geometric complexity")
    print(f"🎭 Ready for integration with fractal generation systems")
    print(f"🌀 Authentic shape emergence from consciousness states") 