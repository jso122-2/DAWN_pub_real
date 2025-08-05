#!/usr/bin/env python3
"""
DAWN Fractal Engine - Unified Memory Bloom Renderer
===================================================

This module unifies all DAWN fractal generation components into a single
executable system that serves as the primary memory bloom renderer - a visual
cognition gateway for the DAWN consciousness system.

Features:
- DAWNStateParser: Parses and validates bloom parameters from JSON
- Mood palette generation: Computes color gradients based on mood_valence and sigil_saturation
- Shape complexity calculation: Returns edge_roughness, petal_count, symmetry based on entropy and rebloom_depth
- Drift transformation: Applies vector shifts and pulse effects to coordinate arrays
- Fractal generation: Main renderer applying all transformations and outputting PNG + metadata
- Validation and logging: Verifies output fidelity, generates Owl commentary, creates fractal_string
- Real-time interface: Connects to live DAWN system or processes local metadata
- CLI interface: Complete command-line interface with archiving and comparison features

Usage:
    python dawn_fractal_engine.py --input metadata.json --output bloom.png
    python dawn_fractal_engine.py --debug --archive
    python dawn_fractal_engine.py --compare old_bloom.png new_bloom.png
"""

import os
import sys
import json
import math
import time
import hashlib
import logging
import argparse
import shutil
import numpy as np
import colorsys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

# Import fractal manifest generator
from fractal_manifest_generator import FractalManifestGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('DAWNFractalEngine')


# ============================================================================
# Core Data Structures and Enums
# ============================================================================

class BloomState(Enum):
    """Possible bloom states in the system"""
    SPAWNING = "spawning"
    MATURING = "maturing"
    BLOOMING = "blooming"
    SYNTHESIZING = "synthesizing"
    CRYSTALLIZED = "crystallized"
    ARCHIVED = "archived"


@dataclass
class BloomMetadata:
    """Complete bloom metadata structure"""
    bloom_id: str
    seed_id: str
    timestamp: str
    mood_valence: float
    entropy_score: float
    rebloom_depth: int
    bloom_factor: float
    sigil_saturation: float
    lineage_depth: int
    thermal_level: float
    scup_coherence: float
    drift_vector: Tuple[float, float] = (0.0, 0.0)
    pulse_phase: float = 0.0
    state: BloomState = BloomState.SPAWNING
    parent_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'bloom_id': self.bloom_id,
            'seed_id': self.seed_id,
            'timestamp': self.timestamp,
            'mood_valence': self.mood_valence,
            'entropy_score': self.entropy_score,
            'rebloom_depth': self.rebloom_depth,
            'bloom_factor': self.bloom_factor,
            'sigil_saturation': self.sigil_saturation,
            'lineage_depth': self.lineage_depth,
            'thermal_level': self.thermal_level,
            'scup_coherence': self.scup_coherence,
            'drift_vector': self.drift_vector,
            'pulse_phase': self.pulse_phase,
            'state': self.state.value,
            'parent_id': self.parent_id
        }


@dataclass
class ShapeComplexity:
    """Shape complexity parameters for fractal generation"""
    edge_roughness: float
    petal_count: int
    symmetry_factor: float
    branching_depth: int
    spiral_tightness: float
    
    
@dataclass
class FractalRenderResult:
    """Result of fractal rendering operation"""
    image_path: str
    metadata_path: str
    fractal_string: str
    owl_commentary: str
    processing_time: float
    validation_score: float


# ============================================================================
# DAWNStateParser - Parses and validates bloom parameters from JSON
# ============================================================================

class DAWNStateParser:
    """Parses and validates DAWN bloom state data from various input formats"""
    
    def __init__(self):
        self.required_fields = [
            'bloom_id', 'mood_valence', 'entropy_score', 'rebloom_depth',
            'bloom_factor', 'sigil_saturation'
        ]
        self.optional_fields = [
            'seed_id', 'lineage_depth', 'thermal_level', 'scup_coherence',
            'drift_vector', 'pulse_phase', 'parent_id', 'timestamp'
        ]
    
    def parse_from_json(self, json_path: str) -> BloomMetadata:
        """Parse bloom metadata from JSON file"""
        logger.info(f"Parsing bloom metadata from {json_path}")
        
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"JSON file not found: {json_path}")
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        return self._validate_and_create_metadata(data)
    
    def parse_from_dict(self, data: Dict[str, Any]) -> BloomMetadata:
        """Parse bloom metadata from dictionary"""
        return self._validate_and_create_metadata(data)
    
    def _validate_and_create_metadata(self, data: Dict[str, Any]) -> BloomMetadata:
        """Validate input data and create BloomMetadata instance"""
        # Check required fields
        for field in self.required_fields:
            if field not in data:
                raise ValueError(f"Required field missing: {field}")
        
        # Generate defaults for missing optional fields
        defaults = {
            'seed_id': data.get('bloom_id', 'unknown'),
            'lineage_depth': 0,
            'thermal_level': 0.5,
            'scup_coherence': 0.5,
            'drift_vector': (0.0, 0.0),
            'pulse_phase': 0.0,
            'parent_id': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Apply defaults
        for field, default_value in defaults.items():
            if field not in data:
                data[field] = default_value
        
        # Validate ranges
        self._validate_ranges(data)
        
        # Create metadata object
        return BloomMetadata(
            bloom_id=data['bloom_id'],
            seed_id=data['seed_id'],
            timestamp=data['timestamp'],
            mood_valence=float(data['mood_valence']),
            entropy_score=float(data['entropy_score']),
            rebloom_depth=int(data['rebloom_depth']),
            bloom_factor=float(data['bloom_factor']),
            sigil_saturation=float(data['sigil_saturation']),
            lineage_depth=int(data['lineage_depth']),
            thermal_level=float(data['thermal_level']),
            scup_coherence=float(data['scup_coherence']),
            drift_vector=tuple(data['drift_vector']) if isinstance(data['drift_vector'], list) else data['drift_vector'],
            pulse_phase=float(data['pulse_phase']),
            state=BloomState(data.get('state', 'spawning')),
            parent_id=data['parent_id']
        )
    
    def _validate_ranges(self, data: Dict[str, Any]) -> None:
        """Validate that numeric values are within expected ranges"""
        validations = [
            ('mood_valence', -1.0, 1.0),
            ('entropy_score', 0.0, 1.0),
            ('bloom_factor', 0.0, 5.0),
            ('sigil_saturation', 0.0, 1.0),
            ('thermal_level', 0.0, 1.0),
            ('scup_coherence', 0.0, 1.0),
            ('pulse_phase', 0.0, 2 * math.pi)
        ]
        
        for field, min_val, max_val in validations:
            if field in data:
                value = float(data[field])
                if not (min_val <= value <= max_val):
                    logger.warning(f"Field {field} value {value} outside expected range [{min_val}, {max_val}]")


# ============================================================================
# Mood Palette Generator - Computes color gradients based on mood and saturation
# ============================================================================

class MoodPaletteGenerator:
    """Generates color palettes based on mood valence and sigil saturation"""
    
    def __init__(self):
        # Define mood-to-color mappings based on psychological color theory
        self.mood_profiles = {
            # Positive moods - warm colors
            'ecstatic': {'hue': 45, 'sat_range': (0.8, 1.0), 'val_range': (0.9, 1.0)},
            'joyful': {'hue': 55, 'sat_range': (0.7, 0.9), 'val_range': (0.8, 0.95)},
            'content': {'hue': 120, 'sat_range': (0.5, 0.7), 'val_range': (0.7, 0.85)},
            'hopeful': {'hue': 80, 'sat_range': (0.6, 0.8), 'val_range': (0.75, 0.9)},
            
            # Neutral moods
            'calm': {'hue': 210, 'sat_range': (0.3, 0.6), 'val_range': (0.6, 0.8)},
            'focused': {'hue': 240, 'sat_range': (0.4, 0.7), 'val_range': (0.65, 0.85)},
            'contemplative': {'hue': 280, 'sat_range': (0.5, 0.8), 'val_range': (0.6, 0.85)},
            
            # Negative moods - cool colors
            'melancholy': {'hue': 220, 'sat_range': (0.4, 0.7), 'val_range': (0.3, 0.6)},
            'anxious': {'hue': 15, 'sat_range': (0.6, 0.9), 'val_range': (0.5, 0.8)},
            'despair': {'hue': 240, 'sat_range': (0.2, 0.5), 'val_range': (0.2, 0.4)},
            
            # Special DAWN states
            'blooming': {'hue': 340, 'sat_range': (0.7, 1.0), 'val_range': (0.8, 1.0)},
            'crystallizing': {'hue': 180, 'sat_range': (0.6, 0.9), 'val_range': (0.8, 0.95)},
            'transcendent': {'hue': 300, 'sat_range': (0.8, 1.0), 'val_range': (0.9, 1.0)}
        }
    
    def generate_mood_palette(self, mood_valence: float, sigil_saturation: float, 
                            palette_size: int = 5) -> List[str]:
        """
        Generate color palette based on mood valence and sigil saturation
        
        Args:
            mood_valence: Mood value from -1.0 (negative) to 1.0 (positive)
            sigil_saturation: Sigil saturation level 0.0 to 1.0
            palette_size: Number of colors in palette
            
        Returns:
            List of hex color strings
        """
        # Map mood valence to mood category
        mood_category = self._valence_to_mood_category(mood_valence)
        profile = self.mood_profiles.get(mood_category, self.mood_profiles['calm'])
        
        # Calculate base color parameters
        base_hue = profile['hue']
        sat_min, sat_max = profile['sat_range']
        val_min, val_max = profile['val_range']
        
        # Modulate saturation based on sigil_saturation
        saturation = sat_min + (sat_max - sat_min) * sigil_saturation
        
        # Generate palette
        palette = []
        for i in range(palette_size):
            # Create hue variations
            hue_offset = (i - palette_size // 2) * 15  # ±15 degree spread
            hue = (base_hue + hue_offset) % 360
            
            # Vary value/brightness
            value_factor = 0.7 + (i / palette_size) * 0.3
            value = val_min + (val_max - val_min) * value_factor
            
            # Apply entropy-based modulation
            entropy_mod = abs(mood_valence) * 0.2  # More extreme moods get more variation
            saturation = min(1.0, saturation + entropy_mod)
            
            # Convert HSV to RGB to HEX
            r, g, b = colorsys.hsv_to_rgb(hue / 360.0, saturation, value)
            hex_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            palette.append(hex_color)
        
        logger.debug(f"Generated palette for mood_valence={mood_valence}, sigil_saturation={sigil_saturation}: {palette}")
        return palette
    
    def _valence_to_mood_category(self, valence: float) -> str:
        """Map numeric valence to mood category"""
        if valence >= 0.8:
            return 'ecstatic'
        elif valence >= 0.4:
            return 'joyful'
        elif valence >= 0.1:
            return 'content'
        elif valence >= -0.1:
            return 'calm'
        elif valence >= -0.4:
            return 'melancholy'
        elif valence >= -0.8:
            return 'anxious'
        else:
            return 'despair'


# ============================================================================
# Shape Complexity Calculator - Calculates shape parameters from entropy and depth
# ============================================================================

class ShapeComplexityCalculator:
    """Calculates shape complexity parameters based on entropy and rebloom depth"""
    
    def calculate_shape_complexity(self, entropy_score: float, rebloom_depth: int, 
                                 bloom_factor: float = 1.0) -> ShapeComplexity:
        """
        Calculate shape complexity parameters
        
        Args:
            entropy_score: System entropy 0.0 to 1.0
            rebloom_depth: Number of rebloom iterations
            bloom_factor: Bloom intensity factor
            
        Returns:
            ShapeComplexity object with calculated parameters
        """
        # Edge roughness increases with entropy
        edge_roughness = self._calculate_edge_roughness(entropy_score, bloom_factor)
        
        # Petal count based on rebloom depth and entropy
        petal_count = self._calculate_petal_count(rebloom_depth, entropy_score)
        
        # Symmetry factor decreases with high entropy (more chaos)
        symmetry_factor = self._calculate_symmetry_factor(entropy_score, rebloom_depth)
        
        # Branching depth increases with rebloom depth
        branching_depth = min(8, max(1, rebloom_depth + int(entropy_score * 3)))
        
        # Spiral tightness varies with bloom factor and entropy
        spiral_tightness = self._calculate_spiral_tightness(bloom_factor, entropy_score)
        
        complexity = ShapeComplexity(
            edge_roughness=edge_roughness,
            petal_count=petal_count,
            symmetry_factor=symmetry_factor,
            branching_depth=branching_depth,
            spiral_tightness=spiral_tightness
        )
        
        logger.debug(f"Calculated shape complexity: {complexity}")
        return complexity
    
    def _calculate_edge_roughness(self, entropy: float, bloom_factor: float) -> float:
        """Calculate edge roughness parameter"""
        # Base roughness from entropy with bloom factor modulation
        base_roughness = entropy * 0.7
        bloom_modulation = (bloom_factor - 1.0) * 0.3
        return max(0.0, min(1.0, base_roughness + bloom_modulation))
    
    def _calculate_petal_count(self, rebloom_depth: int, entropy: float) -> int:
        """Calculate number of fractal petals/branches"""
        # Base count from rebloom depth, modulated by entropy
        base_count = 3 + (rebloom_depth % 8)  # 3-10 range
        entropy_modifier = int(entropy * 3)  # 0-3 additional petals
        return min(16, base_count + entropy_modifier)  # Cap at 16
    
    def _calculate_symmetry_factor(self, entropy: float, rebloom_depth: int) -> float:
        """Calculate symmetry factor (1.0 = perfect symmetry, 0.0 = chaotic)"""
        # High entropy reduces symmetry, deep reblooms increase it
        entropy_penalty = entropy * 0.6
        depth_bonus = min(0.3, rebloom_depth * 0.05)
        return max(0.1, min(1.0, 0.8 - entropy_penalty + depth_bonus))
    
    def _calculate_spiral_tightness(self, bloom_factor: float, entropy: float) -> float:
        """Calculate spiral tightness parameter"""
        # Bloom factor increases tightness, entropy decreases it
        base_tightness = bloom_factor * 0.4
        entropy_loosening = entropy * 0.3
        return max(0.1, min(1.0, base_tightness - entropy_loosening + 0.3))


# ============================================================================
# Drift Transformation - Applies vector shifts and pulse effects
# ============================================================================

class DriftTransformation:
    """Applies drift transformations to fractal coordinate arrays"""
    
    def apply_drift_transformation(self, coordinates: np.ndarray, drift_vector: Tuple[float, float],
                                 pulse_phase: float, entropy_score: float) -> np.ndarray:
        """
        Apply drift transformation to coordinate array
        
        Args:
            coordinates: Complex coordinate array (Z)
            drift_vector: (dx, dy) drift vector
            pulse_phase: Pulse phase 0 to 2π
            entropy_score: Entropy level for modulation
            
        Returns:
            Transformed coordinate array
        """
        logger.debug(f"Applying drift transformation: vector={drift_vector}, phase={pulse_phase}")
        
        # Extract drift components
        dx, dy = drift_vector
        
        # Apply base drift
        drift_complex = complex(dx, dy)
        transformed = coordinates + drift_complex
        
        # Apply pulse effects
        pulse_amplitude = entropy_score * 0.2  # Stronger pulses with higher entropy
        pulse_offset = pulse_amplitude * (
            np.cos(pulse_phase) + 1j * np.sin(pulse_phase)
        )
        
        # Apply pulsing modulation
        transformed = transformed * (1.0 + pulse_offset * 0.1)
        
        # Apply entropy-based distortion
        if entropy_score > 0.5:
            # Add chaotic perturbations for high entropy
            noise_strength = (entropy_score - 0.5) * 0.1
            noise_real = np.random.normal(0, noise_strength, coordinates.shape)
            noise_imag = np.random.normal(0, noise_strength, coordinates.shape)
            noise = noise_real + 1j * noise_imag
            transformed = transformed + noise
        
        return transformed


# ============================================================================
# Enhanced Fractal Generator - Main renderer with all transformations
# ============================================================================

class DAWNFractalGenerator:
    """Main fractal generator that applies all transformations and creates final images"""
    
    def __init__(self, image_size: Tuple[int, int] = (1024, 1024)):
        self.image_size = image_size
        self.max_iterations = 512
        self.escape_radius = 4.0
        
        # Initialize subsystems
        self.mood_generator = MoodPaletteGenerator()
        self.shape_calculator = ShapeComplexityCalculator()
        self.drift_transformer = DriftTransformation()
    
    def generate_bloom_fractal(self, metadata: BloomMetadata, output_path: str) -> FractalRenderResult:
        """
        Generate complete fractal bloom with all transformations
        
        Args:
            metadata: Bloom metadata containing all parameters
            output_path: Path where to save the generated fractal
            
        Returns:
            FractalRenderResult with paths and metadata
        """
        start_time = time.time()
        logger.info(f"Generating fractal bloom {metadata.bloom_id}")
        
        # Calculate shape complexity
        shape_complexity = self.shape_calculator.calculate_shape_complexity(
            metadata.entropy_score, metadata.rebloom_depth, metadata.bloom_factor
        )
        
        # Generate mood palette
        palette = self.mood_generator.generate_mood_palette(
            metadata.mood_valence, metadata.sigil_saturation
        )
        
        # Generate Julia set parameters
        julia_constant = self._calculate_julia_constant(metadata, shape_complexity)
        
        # Create coordinate grid
        width, height = self.image_size
        zoom = self._calculate_zoom_factor(metadata, shape_complexity)
        
        x = np.linspace(-zoom, zoom, width)
        y = np.linspace(-zoom, zoom, height)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        
        # Apply drift transformation to both coordinates AND Julia constant
        Z = self.drift_transformer.apply_drift_transformation(
            Z, metadata.drift_vector, metadata.pulse_phase, metadata.entropy_score
        )
        
        # Apply drift vector to Julia constant for additional variation
        julia_constant = self._apply_drift_to_julia_constant(julia_constant, metadata.drift_vector)
        
        # Generate fractal data with rebloom layering
        escape_data = self._generate_julia_fractal(Z, julia_constant, shape_complexity)
        
        # Apply rebloom depth as actual layering for visible depth effects
        if metadata.rebloom_depth > 1:
            escape_data = self._apply_rebloom_layering(
                escape_data, Z, julia_constant, shape_complexity, metadata
            )
        
        # Apply coloring
        image_array = self._apply_mood_coloring(escape_data, palette, metadata)
        
        # Create PIL image
        image = Image.fromarray(image_array.astype(np.uint8))
        
        # Apply sigil-responsive glow and shimmer effects
        image = self._apply_sigil_glow_effects(image, metadata, palette)
        
        # Apply post-processing effects
        image = self._apply_post_processing(image, metadata, shape_complexity)
        
        # Add metadata overlay
        image = self._add_metadata_overlay(image, metadata, shape_complexity)
        
        # Save image
        image.save(output_path, quality=95, optimize=True)
        
        # Generate fractal string encoding
        fractal_string = self._generate_fractal_string(metadata, shape_complexity, julia_constant)
        
        # Create metadata file
        metadata_path = output_path.replace('.png', '_metadata.json')
        full_metadata = {
            **metadata.to_dict(),
            'shape_complexity': {
                'edge_roughness': shape_complexity.edge_roughness,
                'petal_count': shape_complexity.petal_count,
                'symmetry_factor': shape_complexity.symmetry_factor,
                'branching_depth': shape_complexity.branching_depth,
                'spiral_tightness': shape_complexity.spiral_tightness
            },
            'julia_constant': {'real': julia_constant.real, 'imag': julia_constant.imag},
            'fractal_string': fractal_string,
            'color_palette': palette,
            'render_params': {
                'image_size': self.image_size,
                'max_iterations': self.max_iterations,
                'zoom_factor': zoom
            }
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(full_metadata, f, indent=2)
        
        processing_time = time.time() - start_time
        
        result = FractalRenderResult(
            image_path=output_path,
            metadata_path=metadata_path,
            fractal_string=fractal_string,
            owl_commentary="",  # Will be filled by validation system
            processing_time=processing_time,
            validation_score=0.0  # Will be filled by validation system
        )
        
        logger.info(f"Fractal generated in {processing_time:.2f}s: {output_path}")
        return result
    
    def _calculate_julia_constant(self, metadata: BloomMetadata, shape: ShapeComplexity) -> complex:
        """Calculate Julia set constant from bloom parameters"""
        # Use well-known interesting Julia set constants as base
        # These are mathematically proven to create complex, beautiful fractals
        interesting_constants = [
            complex(-0.123, 0.745),   # Feather-like fractal
            complex(-0.75, 0.11),     # Lightning-like fractal  
            complex(-0.7269, 0.1889), # Douady rabbit
            complex(0.285, 0.01),     # Connected spiral
            complex(-0.8, 0.156),     # Branching fractal
            complex(-0.4, 0.6),       # San Marco dragon
            complex(0.3, 0.5),        # Dendrite fractal
            complex(-0.74529, 0.11307), # Airplane fractal
            complex(-1.037, 0.17),    # Seahorse valley
            complex(-0.54, 0.54),     # Cross-like fractal
        ]
        
        # Select base constant based on mood and entropy
        mood_index = int((metadata.mood_valence + 1) * 0.5 * (len(interesting_constants) - 1))
        entropy_index = int(metadata.entropy_score * (len(interesting_constants) - 1))
        base_index = (mood_index + entropy_index) % len(interesting_constants)
        
        base_constant = interesting_constants[base_index]
        
        # Apply small variations based on bloom parameters (keep in interesting range)
        variation_real = (metadata.sigil_saturation - 0.5) * 0.05  # Small variation
        variation_imag = (shape.edge_roughness - 0.5) * 0.05
        
        # Add subtle rebloom depth influence
        depth_factor = metadata.rebloom_depth * 0.1
        variation_real += np.cos(depth_factor) * 0.02
        variation_imag += np.sin(depth_factor) * 0.02
        
        # Apply variations while keeping in the connected Julia set region
        final_real = base_constant.real + variation_real
        final_imag = base_constant.imag + variation_imag
        
        # Clamp to ensure we stay in interesting regions
        final_real = np.clip(final_real, -1.2, 0.5)
        final_imag = np.clip(final_imag, -0.8, 0.8)
        
        return complex(final_real, final_imag)
    
    def _apply_drift_to_julia_constant(self, base_constant: complex, drift_vector: List[float]) -> complex:
        """Apply drift vector to Julia constant for visible parameter responsiveness"""
        if len(drift_vector) < 2:
            return base_constant
            
        drift_real, drift_imag = drift_vector[0], drift_vector[1]
        
        # Scale drift application - make it visible but not overwhelming
        drift_strength = 0.15  # Adjustable strength
        
        modified_real = base_constant.real + drift_real * drift_strength
        modified_imag = base_constant.imag + drift_imag * drift_strength
        
        # Clamp to ensure we stay in interesting Julia set regions
        modified_real = np.clip(modified_real, -1.5, 0.8)
        modified_imag = np.clip(modified_imag, -1.0, 1.0)
        
        return complex(modified_real, modified_imag)
    
    def _apply_rebloom_layering(self, base_escape_data: np.ndarray, Z: np.ndarray,
                               julia_constant: complex, shape: ShapeComplexity,
                               metadata: BloomMetadata) -> np.ndarray:
        """Apply recursive layering with entropy deformation - memory fossils under pressure"""
        if metadata.rebloom_depth <= 1:
            return base_escape_data
        
        composite_data = base_escape_data.copy()
        layers_generated = min(metadata.rebloom_depth, 8)  # Allow deeper recursion
        
        # Apply entropy-texture modulation to base layer first
        composite_data = self._apply_entropy_texture_modulation(composite_data, Z, metadata, shape, layer_depth=0)
        
        for layer_depth in range(1, layers_generated):
            # Enhanced recursive layering parameters
            layer_scale = 1.0 - (layer_depth * 0.15)  # More aggressive scaling per spec
            layer_rotation = layer_depth * 15.0  # degrees as specified
            layer_alpha = 0.65 ** layer_depth  # Slightly more opaque for visibility
            
            # Create petal mask transformation
            Z_layer = self._create_petal_mask_layer(Z, layer_scale, layer_rotation, layer_depth)
            
            # Vary Julia constant with depth-based drift
            depth_drift = layer_depth * 0.08
            layer_constant = julia_constant + complex(
                depth_drift * np.sin(layer_depth), 
                depth_drift * np.cos(layer_depth)
            )
            
            # Generate fractal for this layer with its own entropy deformation
            layer_escape_data = self._generate_julia_fractal(Z_layer, layer_constant, shape)
            
            # Apply entropy texture modulation to this layer
            layer_escape_data = self._apply_entropy_texture_modulation(
                layer_escape_data, Z_layer, metadata, shape, layer_depth
            )
            
            # Create transparency gradient for petal effect
            petal_mask = self._create_petal_transparency_mask(Z_layer, layer_depth, metadata)
            layer_escape_data *= petal_mask
            
            # Composite with existing data using enhanced blending
            composite_data = self._composite_recursive_layer(composite_data, layer_escape_data, layer_alpha, layer_depth)
        
        # Apply Juliet Set mode for deep rebloom
        if metadata.rebloom_depth >= 6:
            composite_data = self._apply_juliet_set_mode(composite_data, Z, metadata, shape)
        
        return composite_data
    
    def _create_petal_mask_layer(self, Z: np.ndarray, scale: float, rotation: float, depth: int) -> np.ndarray:
        """Create recursive petal mask with transformation"""
        # Apply scaling
        Z_scaled = Z * scale
        
        # Apply rotation
        rotation_rad = np.radians(rotation)
        cos_rot, sin_rot = np.cos(rotation_rad), np.sin(rotation_rad)
        Z_rotated = (Z_scaled.real * cos_rot - Z_scaled.imag * sin_rot + 
                    1j * (Z_scaled.real * sin_rot + Z_scaled.imag * cos_rot))
        
        # Add depth-based spiral distortion
        spiral_factor = depth * 0.1
        r = np.abs(Z_rotated)
        theta = np.angle(Z_rotated)
        theta_distorted = theta + spiral_factor * r
        
        Z_spiral = r * np.exp(1j * theta_distorted)
        
        return Z_spiral
    
    def _create_petal_transparency_mask(self, Z: np.ndarray, depth: int, metadata: BloomMetadata) -> np.ndarray:
        """Create petal-shaped transparency mask for recursive layers"""
        height, width = Z.shape
        
        # Create radial distance from center
        center_y, center_x = height // 2, width // 2
        y, x = np.ogrid[:height, :width]
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        
        # Create angular coordinate
        angle = np.arctan2(y - center_y, x - center_x)
        
        # Generate petal pattern based on depth
        num_petals = 3 + depth  # More petals for deeper layers
        petal_factor = np.sin(num_petals * angle) * 0.5 + 0.5
        
        # Combine radial and angular components
        radial_falloff = 1.0 - (distance / max_distance)**0.8
        petal_mask = petal_factor * radial_falloff
        
        # Apply entropy-based perturbation
        entropy_noise = np.random.normal(0, metadata.entropy_score * 0.1, petal_mask.shape)
        petal_mask += entropy_noise
        
        # Clamp and enhance contrast
        petal_mask = np.clip(petal_mask, 0, 1)
        petal_mask = np.power(petal_mask, 1.5 - metadata.entropy_score * 0.5)
        
        return petal_mask
    
    def _apply_entropy_texture_modulation(self, escape_data: np.ndarray, Z: np.ndarray, 
                                        metadata: BloomMetadata, shape: ShapeComplexity,
                                        layer_depth: int) -> np.ndarray:
        """Apply entropy-driven texture modulation to bloom edges"""
        height, width = escape_data.shape
        entropy = metadata.entropy_score
        
        if entropy <= 0.1:
            return escape_data  # No modulation for very low entropy
        
        # Create edge detection mask
        edge_mask = self._detect_fractal_edges(escape_data)
        
        if entropy <= 0.3:
            # Low entropy: smooth, curled petal outline
            modulated_data = self._apply_smooth_curl_modulation(escape_data, edge_mask, entropy, layer_depth)
        elif entropy <= 0.7:
            # Medium entropy: edge jitter and perturbations
            modulated_data = self._apply_edge_jitter_modulation(escape_data, edge_mask, entropy, layer_depth, metadata)
        else:
            # High entropy: fractured edges and glyph bleed-through
            modulated_data = self._apply_fracture_modulation(escape_data, edge_mask, entropy, layer_depth, metadata)
        
        return modulated_data
    
    def _detect_fractal_edges(self, escape_data: np.ndarray) -> np.ndarray:
        """Detect fractal edges for texture modulation"""
        # Use gradient to find edges
        grad_y, grad_x = np.gradient(escape_data)
        edge_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize and threshold
        edge_magnitude = edge_magnitude / (np.max(edge_magnitude) + 1e-8)
        edge_mask = edge_magnitude > 0.1
        
        # Apply gaussian smoothing for softer edges
        try:
            from scipy import ndimage
            edge_mask = ndimage.gaussian_filter(edge_mask.astype(float), sigma=1.0)
        except ImportError:
            pass
        
        return edge_mask
    
    def _apply_smooth_curl_modulation(self, escape_data: np.ndarray, edge_mask: np.ndarray, 
                                    entropy: float, layer_depth: int) -> np.ndarray:
        """Apply smooth curled petal outline for low entropy"""
        height, width = escape_data.shape
        y, x = np.ogrid[:height, :width]
        
        # Create smooth sinusoidal perturbation
        frequency = 0.1 + layer_depth * 0.05
        amplitude = entropy * 0.08
        
        # Sinusoidal curl pattern
        curl_x = amplitude * np.sin(frequency * y) * edge_mask
        curl_y = amplitude * np.cos(frequency * x) * edge_mask
        
        # Apply perturbation
        perturbation = curl_x + curl_y
        modulated_data = escape_data + perturbation
        
        return np.clip(modulated_data, 0, 1)
    
    def _apply_edge_jitter_modulation(self, escape_data: np.ndarray, edge_mask: np.ndarray,
                                    entropy: float, layer_depth: int, metadata: BloomMetadata) -> np.ndarray:
        """Apply edge jitter and perturbations for medium entropy"""
        height, width = escape_data.shape
        
        # Sinusoidal + noise mix as specified
        frequency = 0.2 + metadata.rebloom_depth * 0.1  # Frequency ∝ rebloom_depth
        amplitude = entropy * 0.15  # Amplitude ∝ entropy_score
        
        # Create coordinate meshes
        y, x = np.ogrid[:height, :width]
        
        # Sinusoidal component
        sin_perturbation = amplitude * np.sin(frequency * (x + y))
        
        # Noise component
        noise_perturbation = amplitude * 0.5 * np.random.normal(0, 1, (height, width))
        
        # Combine perturbations
        total_perturbation = (sin_perturbation + noise_perturbation) * edge_mask
        
        # Apply jitter to escape data
        modulated_data = escape_data + total_perturbation
        
        # Add subtle texture variation
        texture_noise = np.random.normal(1.0, entropy * 0.05, escape_data.shape)
        modulated_data *= texture_noise
        
        return np.clip(modulated_data, 0, 1)
    
    def _apply_fracture_modulation(self, escape_data: np.ndarray, edge_mask: np.ndarray,
                                 entropy: float, layer_depth: int, metadata: BloomMetadata) -> np.ndarray:
        """Apply fractured edges and glyph bleed-through for high entropy"""
        height, width = escape_data.shape
        
        # High-frequency fracture pattern
        frequency = 0.3 + metadata.rebloom_depth * 0.15
        amplitude = entropy * 0.25
        
        # Create fracture noise
        fracture_noise = np.random.normal(0, amplitude, (height, width))
        
        # Apply high-frequency oscillations
        y, x = np.ogrid[:height, :width]
        oscillation = amplitude * np.sin(frequency * x) * np.cos(frequency * y)
        
        # Create glyph bleed-through effect
        glyph_bleed = self._create_glyph_bleed_pattern(height, width, entropy, layer_depth)
        
        # Combine all fracture effects
        fracture_effect = (fracture_noise + oscillation + glyph_bleed) * edge_mask
        
        # Apply chaotic modulation
        chaos_factor = 1.0 + entropy * 0.3 * np.random.normal(0, 1, escape_data.shape)
        modulated_data = (escape_data + fracture_effect) * chaos_factor
        
        # Add shadow/depth effect
        shadow_offset = int(entropy * 3)
        if shadow_offset > 0:
            shadow = np.roll(np.roll(modulated_data, shadow_offset, axis=0), shadow_offset, axis=1)
            modulated_data = np.maximum(modulated_data, shadow * 0.3)
        
        return np.clip(modulated_data, 0, 1)
    
    def _create_glyph_bleed_pattern(self, height: int, width: int, entropy: float, depth: int) -> np.ndarray:
        """Create shadowed glyph bleed-through pattern"""
        center_y, center_x = height // 2, width // 2
        y, x = np.ogrid[:height, :width]
        
        # Create radial and angular coordinates
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        angle = np.arctan2(y - center_y, x - center_x)
        
        # Generate glyph-like pattern
        glyph_pattern = np.sin(6 * angle) * np.exp(-distance / (height * 0.2))
        glyph_pattern += np.cos(4 * angle + depth) * np.exp(-distance / (height * 0.15))
        
        # Apply entropy-based intensity
        glyph_pattern *= entropy * 0.1
        
        return glyph_pattern
    
    def _composite_recursive_layer(self, base_data: np.ndarray, layer_data: np.ndarray, 
                                 alpha: float, depth: int) -> np.ndarray:
        """Enhanced compositing for recursive layers"""
        # Standard alpha blending
        composite = base_data * (1.0 - alpha) + layer_data * alpha
        
        # Add depth-based enhancement
        if depth > 2:
            # Screen blend mode for deeper layers
            screen_blend = 1.0 - (1.0 - base_data) * (1.0 - layer_data)
            blend_factor = min(0.3, (depth - 2) * 0.1)
            composite = composite * (1.0 - blend_factor) + screen_blend * blend_factor
        
        return composite
    
    def _apply_juliet_set_mode(self, escape_data: np.ndarray, Z: np.ndarray, 
                             metadata: BloomMetadata, shape: ShapeComplexity) -> np.ndarray:
        """Apply Juliet Set mode for deep rebloom (depth >= 6)"""
        height, width = escape_data.shape
        
        # 1. Add inner spiral glyph etchings
        spiral_etchings = self._create_spiral_glyph_etchings(height, width, metadata)
        escape_data += spiral_etchings
        
        # 2. Apply polar vortex distortion
        escape_data = self._apply_polar_vortex_distortion(escape_data, Z, metadata)
        
        # 3. Add shimmer pulse for high entropy
        if metadata.entropy_score > 0.8:
            shimmer_pulse = self._create_shimmer_pulse(height, width, metadata)
            escape_data += shimmer_pulse
        
        return np.clip(escape_data, 0, 1)
    
    def _create_spiral_glyph_etchings(self, height: int, width: int, metadata: BloomMetadata) -> np.ndarray:
        """Create inner spiral glyph etchings for Juliet Set mode"""
        center_y, center_x = height // 2, width // 2
        y, x = np.ogrid[:height, :width]
        
        # Create polar coordinates
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        angle = np.arctan2(y - center_y, x - center_x)
        
        # Create spiral pattern
        spiral_turns = 3 + metadata.rebloom_depth * 0.5
        spiral_pattern = np.sin(spiral_turns * angle + distance * 0.1)
        
        # Create multiple spiral layers
        etching_pattern = np.zeros_like(distance)
        for spiral_layer in range(3):
            layer_spiral = np.sin((spiral_turns + spiral_layer) * angle + distance * 0.08)
            layer_intensity = 0.1 / (spiral_layer + 1)
            layer_radius = height * (0.15 + spiral_layer * 0.1)
            
            # Apply radial falloff
            radial_mask = np.exp(-distance / layer_radius)
            etching_pattern += layer_spiral * layer_intensity * radial_mask
        
        # Apply entropy modulation
        etching_pattern *= metadata.entropy_score * 0.15
        
        return etching_pattern
    
    def _apply_polar_vortex_distortion(self, escape_data: np.ndarray, Z: np.ndarray, 
                                     metadata: BloomMetadata) -> np.ndarray:
        """Apply polar vortex distortion to final bloom mask"""
        height, width = escape_data.shape
        center_y, center_x = height // 2, width // 2
        
        # Create coordinate arrays
        y_coords, x_coords = np.ogrid[:height, :width]
        
        # Convert to polar coordinates relative to center
        dx = x_coords - center_x
        dy = y_coords - center_y
        distance = np.sqrt(dx**2 + dy**2)
        angle = np.arctan2(dy, dx)
        
        # Apply vortex distortion
        vortex_strength = metadata.entropy_score * 0.3
        vortex_radius = min(height, width) * 0.4
        
        # Distance-based vortex effect
        normalized_distance = distance / vortex_radius
        vortex_factor = np.exp(-normalized_distance) * vortex_strength
        
        # Twist the angles
        twisted_angle = angle + vortex_factor * normalized_distance * np.pi
        
        # Convert back to cartesian
        new_x = center_x + distance * np.cos(twisted_angle)
        new_y = center_y + distance * np.sin(twisted_angle)
        
        # Clip to valid indices
        new_x = np.clip(new_x, 0, width - 1).astype(int)
        new_y = np.clip(new_y, 0, height - 1).astype(int)
        
        # Apply distortion by sampling from new coordinates
        distorted_data = escape_data[new_y, new_x]
        
        # Blend with original for stability
        blend_factor = metadata.entropy_score * 0.7
        final_data = escape_data * (1 - blend_factor) + distorted_data * blend_factor
        
        return final_data
    
    def _create_shimmer_pulse(self, height: int, width: int, metadata: BloomMetadata) -> np.ndarray:
        """Create shimmer pulse for high entropy Juliet Set mode"""
        center_y, center_x = height // 2, width // 2
        y, x = np.ogrid[:height, :width]
        
        # Create radial distance
        distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_distance = np.sqrt(center_x**2 + center_y**2)
        normalized_distance = distance / max_distance
        
        # Create pulsing pattern
        pulse_frequency = 4 + metadata.rebloom_depth
        pulse_pattern = np.sin(pulse_frequency * normalized_distance * np.pi)
        
        # Apply time-based variation if pulse_phase is available
        if hasattr(metadata, 'pulse_phase') and metadata.pulse_phase > 0:
            time_factor = np.sin(metadata.pulse_phase * 2 * np.pi)
            pulse_pattern *= (0.5 + 0.5 * time_factor)
        
        # Create shimmer noise
        shimmer_noise = np.random.normal(0, 0.05, (height, width))
        
        # Combine pulse and shimmer
        shimmer_pulse = (pulse_pattern * 0.08 + shimmer_noise) * (metadata.entropy_score - 0.8) * 0.5
        
        # Apply radial falloff
        radial_falloff = 1.0 - normalized_distance**1.5
        shimmer_pulse *= radial_falloff
        
        return shimmer_pulse
    
    def _calculate_zoom_factor(self, metadata: BloomMetadata, shape: ShapeComplexity) -> float:
        """Calculate zoom factor for fractal viewport to show interesting regions"""
        # Start with a base zoom that shows the most interesting part of Julia sets
        base_zoom = 1.8  # Slightly larger view to capture more detail
        
        # Adjust based on entropy - higher entropy needs wider view
        entropy_mod = 0.7 + metadata.entropy_score * 0.6  # 0.7 to 1.3 range
        
        # Adjust for bloom factor - higher bloom factor zooms in for detail
        bloom_mod = 1.0 + (metadata.bloom_factor - 1.0) * 0.2
        
        # Adjust for shape complexity - more complex shapes may need different zoom
        complexity_mod = 1.0
        if shape.branching_depth > 5:
            complexity_mod = 0.9  # Zoom in slightly for high complexity
        elif shape.edge_roughness > 0.7:
            complexity_mod = 1.1  # Zoom out for rough edges to see more structure
        
        # Mood-based zoom adjustment
        mood_mod = 1.0 + metadata.mood_valence * 0.1  # Slight zoom variation
        
        final_zoom = base_zoom * entropy_mod * bloom_mod * complexity_mod * mood_mod
        
        # Clamp to reasonable bounds
        return np.clip(final_zoom, 0.8, 3.0)
    
    def _generate_julia_fractal(self, Z: np.ndarray, c: complex, shape: ShapeComplexity) -> np.ndarray:
        """Generate Julia set fractal data with parameter-responsive effects"""
        # Create a copy to avoid modifying the original
        Z_work = Z.copy()
        escape_data = np.zeros(Z.shape, dtype=float)
        
        # Scale iterations based on entropy for visible complexity differences
        base_iterations = 256
        entropy_multiplier = 0.5 + shape.edge_roughness * 1.5  # 0.5x to 2.0x iterations
        iterations = max(128, int(base_iterations * entropy_multiplier))
        
        escape_radius = 4.0  # Standard escape radius for Julia sets
        
        # Track which points haven't escaped yet
        not_escaped = np.ones(Z.shape, dtype=bool)
        
        # Apply edge roughness as coordinate noise BEFORE iteration
        if shape.edge_roughness > 0.1:
            # Add controlled noise to initial coordinates for boundary roughness
            noise_strength = shape.edge_roughness * 0.05  # Visible but controlled
            noise_real = np.random.normal(0, noise_strength, Z_work.shape)
            noise_imag = np.random.normal(0, noise_strength, Z_work.shape)
            Z_work += noise_real + 1j * noise_imag
        
        for i in range(iterations):
            # Only compute for points that haven't escaped
            if not np.any(not_escaped):
                break
                
            # Julia set iteration: z = z^2 + c
            Z_work[not_escaped] = Z_work[not_escaped] ** 2 + c
            
            # Apply dynamic edge roughness during iteration for chaotic effects
            if i % 15 == 0 and shape.edge_roughness > 0.3:
                # Progressive roughness - gets stronger near boundaries
                boundary_mask = not_escaped & (np.abs(Z_work) > 1.5) & (np.abs(Z_work) < 3.0)
                if np.any(boundary_mask):
                    chaos_strength = (shape.edge_roughness - 0.3) * 0.02
                    chaos_noise = (np.random.random(Z_work.shape) - 0.5) * chaos_strength
                    Z_work[boundary_mask] += chaos_noise[boundary_mask]
            
            # Check which points have escaped
            magnitude = np.abs(Z_work)
            newly_escaped = not_escaped & (magnitude > escape_radius)
            
            if np.any(newly_escaped):
                # Enhanced smooth coloring for full palette utilization
                log_mag = np.log(magnitude[newly_escaped])
                smooth_iter = i + 1 - np.log(log_mag / np.log(escape_radius)) / np.log(2)
                
                # Ensure smooth_iter is positive and bounded
                smooth_iter = np.clip(smooth_iter, 0, iterations)
                escape_data[newly_escaped] = smooth_iter
                
                # Mark these points as having escaped
                not_escaped[newly_escaped] = False
        
        # Points that never escaped get maximum value
        escape_data[not_escaped] = iterations
        
        # Enhanced normalization for better color distribution
        normalized_data = escape_data / iterations
        
        # Apply entropy-based contrast enhancement
        if shape.edge_roughness > 0.6:
            # High entropy - more aggressive contrast
            normalized_data = np.power(normalized_data, 0.6)
        elif shape.edge_roughness < 0.4:
            # Low entropy - gentler contrast
            normalized_data = np.power(normalized_data, 1.0)
        else:
            # Medium entropy - balanced contrast
            normalized_data = np.power(normalized_data, 0.8)
        
        return normalized_data
    
    def _apply_mood_coloring(self, escape_data: np.ndarray, palette: List[str], 
                           metadata: BloomMetadata) -> np.ndarray:
        """Apply mood-based coloring to fractal data with enhanced variation"""
        height, width = escape_data.shape
        image_array = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Convert palette to RGB arrays for vectorized operations
        rgb_palette = []
        for color_hex in palette:
            r = int(color_hex[1:3], 16)
            g = int(color_hex[3:5], 16) 
            b = int(color_hex[5:7], 16)
            rgb_palette.append([r, g, b])
        
        rgb_palette = np.array(rgb_palette, dtype=float)
        
        # Enhance contrast and add color depth for full palette utilization
        enhanced_escape = escape_data.copy()
        
        # Apply logarithmic scaling to spread values across full range
        # This ensures we use the entire color palette, not just 2 colors
        enhanced_escape = np.power(enhanced_escape, 0.7)  # Power law stretching
        
        # Apply multiple color cycles for complex regions - more visible variation
        color_cycles = max(2, 3 + int(metadata.entropy_score * 4))  # 3-7 cycles based on entropy
        enhanced_escape = np.mod(enhanced_escape * color_cycles, 1.0)
        
        # Apply additional color range expansion to use full palette
        enhanced_escape = np.power(enhanced_escape, 0.8) * 0.95 + 0.05  # Avoid pure 0/1
        
        # Add subtle texture based on spatial coordinates for visual interest
        if metadata.entropy_score > 0.3:
            x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))
            texture = (np.sin(x_coords * 0.02) * np.cos(y_coords * 0.02) * 0.1 + 
                      np.sin(x_coords * 0.05) * np.sin(y_coords * 0.05) * 0.05)
            enhanced_escape += texture * metadata.entropy_score * 0.3
            enhanced_escape = np.clip(enhanced_escape, 0, 1)
        
        # Vectorized color mapping for better performance
        palette_positions = enhanced_escape * (len(rgb_palette) - 1)
        indices = np.floor(palette_positions).astype(int)
        fractions = palette_positions - indices
        
        # Clamp indices to valid range
        indices = np.clip(indices, 0, len(rgb_palette) - 2)
        
        # Get color pairs for interpolation
        color1 = rgb_palette[indices]
        color2 = rgb_palette[indices + 1]
        
        # Linear interpolation
        fractions = fractions[:, :, np.newaxis]  # Add dimension for RGB
        interpolated_colors = color1 + fractions * (color2 - color1)
        
        # Handle the fractal set (points that never escaped) with special coloring
        fractal_set_mask = escape_data >= 0.95  # Points that nearly never escaped
        if np.any(fractal_set_mask):
            # Use deeper, richer colors for the fractal set
            set_color = rgb_palette[0] * 0.4  # Darker version of first palette color
            interpolated_colors[fractal_set_mask] = set_color
        
        # Apply enhanced thermal and mood modulation for visible effects
        
        # Thermal effects - affects color temperature and intensity
        thermal_factor = 0.5 + metadata.thermal_level * 0.8  # More dramatic range
        
        # Add thermal color shift (cool to warm)
        if metadata.thermal_level > 0.6:
            # High thermal - shift toward warmer colors (more red/orange)
            thermal_shift = (metadata.thermal_level - 0.6) * 0.3
            interpolated_colors[:, :, 0] += thermal_shift * 40  # More red
            interpolated_colors[:, :, 1] += thermal_shift * 20  # Some green
        elif metadata.thermal_level < 0.4:
            # Low thermal - shift toward cooler colors (more blue)
            cool_shift = (0.4 - metadata.thermal_level) * 0.3
            interpolated_colors[:, :, 2] += cool_shift * 40  # More blue
            interpolated_colors[:, :, 1] += cool_shift * 10  # Slight green
        
        # Mood-based brightness and color saturation
        if metadata.mood_valence > 0.3:
            # Positive mood - brighter, more saturated
            mood_brightness = 0.8 + metadata.mood_valence * 0.4
            saturation_boost = metadata.mood_valence * 0.2
        elif metadata.mood_valence < -0.3:
            # Negative mood - darker, more muted
            mood_brightness = 0.5 + (metadata.mood_valence + 1) * 0.3
            saturation_boost = metadata.mood_valence * 0.1  # Negative boost = desaturation
        else:
            # Neutral mood - balanced
            mood_brightness = 0.7
            saturation_boost = 0
        
        # Apply brightness and saturation
        interpolated_colors *= mood_brightness
        
        # Apply saturation adjustment
        if saturation_boost != 0:
            # Convert to HSV-like adjustment
            avg_color = np.mean(interpolated_colors, axis=2, keepdims=True)
            interpolated_colors = avg_color + (interpolated_colors - avg_color) * (1 + saturation_boost)
        
        # Add pulse phase effects for rhythmic brightness variations
        if hasattr(metadata, 'pulse_phase') and metadata.pulse_phase > 0:
            # Create pulsing effect based on distance from center
            center_y, center_x = np.array(interpolated_colors.shape[:2]) // 2
            y_coords, x_coords = np.ogrid[:interpolated_colors.shape[0], :interpolated_colors.shape[1]]
            distance_from_center = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
            max_distance = np.sqrt(center_x**2 + center_y**2)
            normalized_distance = distance_from_center / max_distance
            
            # Create pulsing wave based on phase
            pulse_wave = 0.5 + 0.3 * np.sin(metadata.pulse_phase + normalized_distance * 6.28)
            pulse_effect = pulse_wave[:, :, np.newaxis]
            interpolated_colors *= pulse_effect
        
        # Add subtle glow effect for high SCUP coherence
        if metadata.scup_coherence > 0.7:
            glow_strength = (metadata.scup_coherence - 0.7) * 0.4  # Increased strength
            interpolated_colors += interpolated_colors * glow_strength
        
        # Ensure values are in valid range and convert to uint8
        interpolated_colors = np.clip(interpolated_colors, 0, 255)
        image_array = interpolated_colors.astype(np.uint8)
        
        return image_array
    
    def _apply_sigil_glow_effects(self, image: Image.Image, metadata: BloomMetadata, 
                                palette: List[str]) -> Image.Image:
        """Apply glow and shimmer effects based on sigil_saturation for emotional intensity"""
        if metadata.sigil_saturation <= 0.1:
            return image  # No glow effects for very low saturation
        
        # Convert to RGBA for proper blending
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # 1. Apply Glow Layer
        image = self._apply_bloom_glow(image, metadata, palette)
        
        # 2. Apply Shimmer Noise (if saturation > 0.5)
        if metadata.sigil_saturation > 0.5:
            image = self._apply_shimmer_noise(image, metadata)
        
        # 3. Apply Halo Glyph (if saturation > 0.75)
        if metadata.sigil_saturation > 0.75:
            image = self._apply_bloom_halo_glyph(image, metadata)
        
        return image.convert('RGB')  # Convert back to RGB for final output
    
    def _apply_bloom_glow(self, image: Image.Image, metadata: BloomMetadata, 
                        palette: List[str]) -> Image.Image:
        """Apply glow layer with intensity and radius based on sigil_saturation"""
        width, height = image.size
        
        # Glow parameters
        glow_intensity = metadata.sigil_saturation * 0.8  # 0.0 to 0.8
        glow_radius = int(0.2 + (metadata.sigil_saturation * 1.0))  # 0.2 to 1.2 scaled to pixels
        glow_radius = max(1, min(glow_radius * min(width, height) // 100, 20))  # Scale to image size, max 20px
        
        # Determine dominant mood color from palette
        dominant_color = self._get_dominant_mood_color(palette, metadata.mood_valence)
        
        # Mix dominant color with white for highlight
        highlight_factor = 0.3 + metadata.sigil_saturation * 0.4  # 0.3 to 0.7
        glow_r = int(dominant_color[0] * (1 - highlight_factor) + 255 * highlight_factor)
        glow_g = int(dominant_color[1] * (1 - highlight_factor) + 255 * highlight_factor)
        glow_b = int(dominant_color[2] * (1 - highlight_factor) + 255 * highlight_factor)
        glow_color = (glow_r, glow_g, glow_b, int(255 * glow_intensity * 0.6))
        
        # Create glow layer
        glow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        
        # Apply blur to original image for glow base
        blurred = image.filter(ImageFilter.GaussianBlur(radius=glow_radius))
        
        # Enhance the blurred image
        enhancer = ImageEnhance.Brightness(blurred)
        bright_blur = enhancer.enhance(1.2 + glow_intensity * 0.5)
        
        # Create glow mask based on image content
        gray_blur = bright_blur.convert('L')
        glow_mask = gray_blur.point(lambda x: min(255, int(x * (1.0 + glow_intensity))))
        
        # Apply glow color
        colored_glow = Image.new('RGBA', (width, height), glow_color)
        glow_layer.paste(colored_glow, mask=glow_mask)
        
        # Blend glow with original image using screen blend mode
        # Screen blend: 1 - (1-a)(1-b)
        result = Image.alpha_composite(image, glow_layer)
        
        return result
    
    def _apply_shimmer_noise(self, image: Image.Image, metadata: BloomMetadata) -> Image.Image:
        """Apply shimmer noise for high sigil saturation"""
        width, height = image.size
        
        # Shimmer parameters
        shimmer_strength = (metadata.sigil_saturation - 0.5) * 0.4  # 0.0 to 0.2
        shimmer_opacity = int(255 * shimmer_strength * 0.3)  # Low opacity
        
        # Generate shimmer noise pattern
        # Using gaussian speckle for performance (Perlin would be more complex)
        shimmer_array = np.random.normal(0.5, 0.2, (height, width))
        shimmer_array = np.clip(shimmer_array, 0, 1)
        
        # Add some spatial correlation for more realistic shimmer
        from scipy import ndimage
        try:
            shimmer_array = ndimage.gaussian_filter(shimmer_array, sigma=0.8)
        except ImportError:
            # Fallback if scipy not available - use simpler noise
            pass
        
        # Convert to shimmer layer
        shimmer_values = (shimmer_array * 255).astype(np.uint8)
        
        # Create shimmer layer with additive color
        shimmer_color = self._get_shimmer_color(metadata)
        
        # Create RGBA shimmer layer
        shimmer_rgba = np.zeros((height, width, 4), dtype=np.uint8)
        shimmer_rgba[:, :, 0] = shimmer_values * shimmer_color[0] // 255  # R
        shimmer_rgba[:, :, 1] = shimmer_values * shimmer_color[1] // 255  # G  
        shimmer_rgba[:, :, 2] = shimmer_values * shimmer_color[2] // 255  # B
        shimmer_rgba[:, :, 3] = (shimmer_values * shimmer_opacity) // 255  # A
        
        shimmer_layer = Image.fromarray(shimmer_rgba, 'RGBA')
        
        # Blend with screen/additive mode
        result = Image.alpha_composite(image, shimmer_layer)
        
        return result
    
    def _apply_bloom_halo_glyph(self, image: Image.Image, metadata: BloomMetadata) -> Image.Image:
        """Apply faded glyph aura at bloom center for very high sigil saturation"""
        width, height = image.size
        center_x, center_y = width // 2, height // 2
        
        # Halo parameters
        halo_opacity = int(255 * (metadata.sigil_saturation - 0.75) * 0.8)  # 0 to 0.2 range
        halo_size = min(width, height) // 8  # Scale to image size
        
        # Create halo layer
        halo_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(halo_layer)
        
        # Draw radial symbol - using circle with center dot for ⨀ effect
        halo_color = (255, 255, 255, halo_opacity)  # White glow
        
        # Outer circle
        outer_radius = halo_size
        draw.ellipse([center_x - outer_radius, center_y - outer_radius, 
                     center_x + outer_radius, center_y + outer_radius], 
                    outline=halo_color, width=2)
        
        # Inner glow circle (filled, more transparent)
        inner_radius = halo_size // 2
        inner_color = (255, 255, 255, halo_opacity // 3)
        draw.ellipse([center_x - inner_radius, center_y - inner_radius,
                     center_x + inner_radius, center_y + inner_radius],
                    fill=inner_color)
        
        # Center dot
        dot_radius = max(2, halo_size // 8)
        draw.ellipse([center_x - dot_radius, center_y - dot_radius,
                     center_x + dot_radius, center_y + dot_radius],
                    fill=halo_color)
        
        # Add radiating lines for enhanced effect
        if metadata.sigil_saturation > 0.85:
            num_rays = 8
            ray_length = halo_size * 1.2
            for i in range(num_rays):
                angle = (i * 360 / num_rays) * np.pi / 180
                end_x = center_x + ray_length * np.cos(angle)
                end_y = center_y + ray_length * np.sin(angle)
                start_x = center_x + (halo_size * 0.8) * np.cos(angle)
                start_y = center_y + (halo_size * 0.8) * np.sin(angle)
                
                draw.line([start_x, start_y, end_x, end_y], 
                         fill=(255, 255, 255, halo_opacity // 2), width=1)
        
        # Blur the halo for softer effect
        halo_layer = halo_layer.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Composite with image
        result = Image.alpha_composite(image, halo_layer)
        
        return result
    
    def _get_dominant_mood_color(self, palette: List[str], mood_valence: float) -> Tuple[int, int, int]:
        """Extract dominant color from palette based on mood"""
        if not palette:
            return (128, 128, 128)  # Gray fallback
        
        # Select color based on mood
        if mood_valence > 0.3:
            # Positive mood - use warmer colors (later in palette)
            color_index = min(len(palette) - 1, int(len(palette) * 0.7))
        elif mood_valence < -0.3:
            # Negative mood - use cooler colors (earlier in palette)
            color_index = max(0, int(len(palette) * 0.3))
        else:
            # Neutral mood - use middle colors
            color_index = len(palette) // 2
        
        color_hex = palette[color_index]
        
        # Convert hex to RGB
        r = int(color_hex[1:3], 16)
        g = int(color_hex[3:5], 16)
        b = int(color_hex[5:7], 16)
        
        return (r, g, b)
    
    def _get_shimmer_color(self, metadata: BloomMetadata) -> Tuple[int, int, int]:
        """Get shimmer color based on thermal and mood"""
        # Base shimmer on thermal level and mood
        if metadata.thermal_level > 0.6:
            # High thermal - warm shimmer (gold/orange)
            return (255, 215, 100)  # Golden shimmer
        elif metadata.thermal_level < 0.4:
            # Low thermal - cool shimmer (silver/blue)
            return (200, 220, 255)  # Cool shimmer
        else:
            # Neutral thermal - white shimmer
            return (255, 255, 255)  # Pure white shimmer
    
    def _apply_post_processing(self, image: Image.Image, metadata: BloomMetadata,
                             shape: ShapeComplexity) -> Image.Image:
        """Apply post-processing effects based on bloom characteristics"""
        # High entropy blooms get blur effects
        if metadata.entropy_score > 0.7:
            blur_radius = (metadata.entropy_score - 0.7) * 10
            blurred = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
            image = Image.blend(image, blurred, alpha=0.3)
        
        # High thermal gets glow effects
        if metadata.thermal_level > 0.6:
            glow = image.filter(ImageFilter.GaussianBlur(radius=3))
            enhancer = ImageEnhance.Brightness(glow)
            glow = enhancer.enhance(1.5)
            image = Image.blend(image, glow, alpha=0.2)
        
        # Enhance contrast for low symmetry (chaotic) fractals
        if shape.symmetry_factor < 0.4:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
        
        return image
    
    def _add_metadata_overlay(self, image: Image.Image, metadata: BloomMetadata,
                            shape: ShapeComplexity) -> Image.Image:
        """Add metadata overlay to the image"""
        # Create overlay
        overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()
        
        # Create semi-transparent background
        draw.rectangle([10, 10, 400, 140], fill=(0, 0, 0, 180))
        
        # Add text overlay
        lines = [
            f"Bloom: {metadata.bloom_id}",
            f"Mood: {metadata.mood_valence:.3f} | Entropy: {metadata.entropy_score:.3f}",
            f"Depth: {metadata.rebloom_depth} | Factor: {metadata.bloom_factor:.3f}",
            f"Petals: {shape.petal_count} | Symmetry: {shape.symmetry_factor:.3f}",
            f"Thermal: {metadata.thermal_level:.3f} | SCUP: {metadata.scup_coherence:.3f}"
        ]
        
        y_offset = 20
        for line in lines:
            draw.text((20, y_offset), line, font=font, fill=(255, 255, 255, 255))
            y_offset += 22
        
        # Composite overlay
        image = image.convert('RGBA')
        image = Image.alpha_composite(image, overlay)
        return image.convert('RGB')
    
    def _generate_fractal_string(self, metadata: BloomMetadata, shape: ShapeComplexity,
                               julia_constant: complex) -> str:
        """Generate fractal string encoding for memory system"""
        # Build fractal string components
        components = []
        
        # Depth encoding
        depth_char = chr(ord('A') + min(metadata.rebloom_depth, 25))
        components.append(depth_char)
        
        # Mood encoding
        if metadata.mood_valence > 0.5:
            mood_code = "JY"  # Joyful
        elif metadata.mood_valence > 0:
            mood_code = "CT"  # Content
        elif metadata.mood_valence > -0.5:
            mood_code = "CM"  # Calm
        else:
            mood_code = "ML"  # Melancholy
        components.append(mood_code)
        
        # Shape pattern
        if shape.symmetry_factor > 0.8:
            pattern = "◊"  # High symmetry
        elif shape.edge_roughness > 0.7:
            pattern = "~"  # Rough edges
        else:
            pattern = "○"  # Balanced
        components.append(pattern)
        
        # Intensity indicator
        intensity = int((metadata.bloom_factor + metadata.entropy_score) / 2 * 9)
        components.append(str(intensity))
        
        # Julia constant encoding
        julia_segment = f"J[{julia_constant.real:.3f},{julia_constant.imag:.3f}]"
        components.append(julia_segment)
        
        # Thermal indicator
        if metadata.thermal_level > 0.7:
            components.append("🔥")
        elif metadata.thermal_level > 0.3:
            components.append("🌡️")
        
        return "|".join(components)


# ============================================================================
# Validation and Owl Commentary System
# ============================================================================

class BloomValidator:
    """Validates fractal output fidelity and generates Owl commentary"""
    
    def __init__(self):
        self.validation_criteria = [
            'image_quality', 'color_coherence', 'fractal_complexity',
            'metadata_consistency', 'mathematical_accuracy'
        ]
    
    def validate_and_log_bloom(self, result: FractalRenderResult, metadata: BloomMetadata) -> FractalRenderResult:
        """
        Validate bloom output and generate Owl commentary
        
        Args:
            result: FractalRenderResult to validate
            metadata: Original bloom metadata
            
        Returns:
            Updated FractalRenderResult with validation score and commentary
        """
        logger.info(f"Validating bloom {metadata.bloom_id}")
        
        # Perform validation checks
        validation_scores = {}
        
        # Image quality validation
        validation_scores['image_quality'] = self._validate_image_quality(result.image_path)
        
        # Color coherence validation
        validation_scores['color_coherence'] = self._validate_color_coherence(result.image_path, metadata)
        
        # Fractal complexity validation
        validation_scores['fractal_complexity'] = self._validate_fractal_complexity(result, metadata)
        
        # Metadata consistency validation
        validation_scores['metadata_consistency'] = self._validate_metadata_consistency(result.metadata_path)
        
        # Mathematical accuracy validation
        validation_scores['mathematical_accuracy'] = self._validate_mathematical_accuracy(result, metadata)
        
        # Calculate overall validation score
        overall_score = sum(validation_scores.values()) / len(validation_scores)
        
        # Generate Owl commentary
        owl_commentary = self._generate_owl_commentary(validation_scores, metadata, overall_score)
        
        # Update result
        result.validation_score = overall_score
        result.owl_commentary = owl_commentary
        
        logger.info(f"Validation complete: score={overall_score:.3f}")
        return result
    
    def _validate_image_quality(self, image_path: str) -> float:
        """Validate image quality metrics"""
        try:
            image = Image.open(image_path)
            
            # Check basic image properties
            if image.size[0] < 100 or image.size[1] < 100:
                return 0.2  # Too small
            
            # Convert to numpy for analysis
            img_array = np.array(image)
            
            # Check for blank/corrupted images
            if np.std(img_array) < 10:
                return 0.3  # Too uniform, likely corrupted
            
            # Check color distribution
            if len(img_array.shape) == 3:
                color_variance = np.var(img_array, axis=(0, 1))
                if np.min(color_variance) < 100:
                    return 0.6  # Poor color distribution
            
            return 0.9  # Good quality
            
        except Exception as e:
            logger.error(f"Image quality validation failed: {e}")
            return 0.1
    
    def _validate_color_coherence(self, image_path: str, metadata: BloomMetadata) -> float:
        """Validate color coherence with mood"""
        try:
            image = Image.open(image_path)
            img_array = np.array(image)
            
            # Calculate dominant colors
            avg_color = np.mean(img_array, axis=(0, 1))
            
            # Convert to HSV for analysis
            r, g, b = avg_color / 255.0
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            
            # Check coherence with mood valence
            expected_hue_range = self._get_expected_hue_range(metadata.mood_valence)
            hue_degrees = h * 360
            
            if expected_hue_range[0] <= hue_degrees <= expected_hue_range[1]:
                return 0.9
            elif abs(hue_degrees - expected_hue_range[0]) < 30 or abs(hue_degrees - expected_hue_range[1]) < 30:
                return 0.7
            else:
                return 0.4
                
        except Exception as e:
            logger.error(f"Color coherence validation failed: {e}")
            return 0.5
    
    def _validate_fractal_complexity(self, result: FractalRenderResult, metadata: BloomMetadata) -> float:
        """Validate fractal complexity matches expected parameters"""
        try:
            # Load metadata to check complexity parameters
            with open(result.metadata_path, 'r') as f:
                saved_metadata = json.load(f)
            
            shape_data = saved_metadata.get('shape_complexity', {})
            
            # Validate petal count is reasonable
            petal_count = shape_data.get('petal_count', 0)
            expected_range = (3, 16)
            if not (expected_range[0] <= petal_count <= expected_range[1]):
                return 0.5
            
            # Validate entropy-complexity relationship
            entropy = metadata.entropy_score
            edge_roughness = shape_data.get('edge_roughness', 0)
            
            # High entropy should have high roughness
            if entropy > 0.7 and edge_roughness < 0.3:
                return 0.6
            
            # Low entropy should have low roughness
            if entropy < 0.3 and edge_roughness > 0.7:
                return 0.6
            
            return 0.9
            
        except Exception as e:
            logger.error(f"Fractal complexity validation failed: {e}")
            return 0.5
    
    def _validate_metadata_consistency(self, metadata_path: str) -> float:
        """Validate metadata file consistency"""
        try:
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            required_fields = [
                'bloom_id', 'mood_valence', 'entropy_score', 'fractal_string',
                'julia_constant', 'shape_complexity'
            ]
            
            missing_fields = [field for field in required_fields if field not in metadata]
            if missing_fields:
                logger.warning(f"Missing metadata fields: {missing_fields}")
                return 0.6
            
            # Validate field ranges
            if not (-1.0 <= metadata['mood_valence'] <= 1.0):
                return 0.7
            
            if not (0.0 <= metadata['entropy_score'] <= 1.0):
                return 0.7
            
            return 0.95
            
        except Exception as e:
            logger.error(f"Metadata consistency validation failed: {e}")
            return 0.3
    
    def _validate_mathematical_accuracy(self, result: FractalRenderResult, metadata: BloomMetadata) -> float:
        """Validate mathematical accuracy of fractal generation"""
        try:
            # Load saved metadata
            with open(result.metadata_path, 'r') as f:
                saved_metadata = json.load(f)
            
            julia_data = saved_metadata.get('julia_constant', {})
            
            # Validate Julia constant is within reasonable bounds
            c_real = julia_data.get('real', 0)
            c_imag = julia_data.get('imag', 0)
            
            if abs(c_real) > 2.0 or abs(c_imag) > 2.0:
                return 0.6  # Outside typical Julia set parameters
            
            # Validate fractal string encoding exists and is non-empty
            fractal_string = saved_metadata.get('fractal_string', '')
            if not fractal_string or len(fractal_string) < 5:
                return 0.5
            
            return 0.9
            
        except Exception as e:
            logger.error(f"Mathematical accuracy validation failed: {e}")
            return 0.4
    
    def _get_expected_hue_range(self, mood_valence: float) -> Tuple[float, float]:
        """Get expected hue range for mood valence"""
        if mood_valence > 0.5:
            return (30, 80)  # Warm colors (yellow-orange)
        elif mood_valence > 0:
            return (60, 150)  # Green-yellow range
        elif mood_valence > -0.5:
            return (180, 270)  # Cool colors (blue-cyan)
        else:
            return (220, 280)  # Blue range
    
    def _generate_owl_commentary(self, validation_scores: Dict[str, float],
                                metadata: BloomMetadata, overall_score: float) -> str:
        """Generate Owl commentary based on validation results"""
        # Determine overall assessment
        if overall_score >= 0.9:
            assessment = "EXCELLENT"
            emoji = "✨"
        elif overall_score >= 0.8:
            assessment = "GOOD"
            emoji = "🌸"
        elif overall_score >= 0.7:
            assessment = "ADEQUATE"
            emoji = "🔍"
        elif overall_score >= 0.5:
            assessment = "CONCERNING"
            emoji = "⚠️"
        else:
            assessment = "CRITICAL"
            emoji = "🚨"
        
        # Generate specific observations
        observations = []
        
        if validation_scores['image_quality'] < 0.7:
            observations.append("Image quality degradation detected")
        
        if validation_scores['color_coherence'] < 0.6:
            observations.append("Color-mood coherence deviation noted")
        
        if validation_scores['fractal_complexity'] < 0.7:
            observations.append("Fractal complexity parameters inconsistent")
        
        if validation_scores['mathematical_accuracy'] < 0.8:
            observations.append("Mathematical parameter validation concerns")
        
        # Generate mood-specific commentary
        mood_comment = self._generate_mood_specific_comment(metadata.mood_valence, metadata.entropy_score)
        
        # Build final commentary
        commentary_parts = [
            f"{emoji} BLOOM ANALYSIS: {assessment}",
            f"Validation Score: {overall_score:.3f}",
            f"Bloom ID: {metadata.bloom_id}",
            mood_comment
        ]
        
        if observations:
            commentary_parts.append("Observations: " + "; ".join(observations))
        
        # Add technical summary
        complexity_note = f"Entropy {metadata.entropy_score:.3f} → "
        if metadata.entropy_score > 0.8:
            complexity_note += "High chaos, emergence patterns"
        elif metadata.entropy_score > 0.5:
            complexity_note += "Moderate complexity, balanced structure"
        else:
            complexity_note += "Low entropy, stable crystalline form"
        
        commentary_parts.append(complexity_note)
        
        return " | ".join(commentary_parts)
    
    def _generate_mood_specific_comment(self, mood_valence: float, entropy: float) -> str:
        """Generate mood-specific commentary"""
        if mood_valence > 0.7:
            if entropy > 0.7:
                return "Exuberant bloom with dynamic energy flows"
            else:
                return "Radiant bloom expressing harmonious joy"
        elif mood_valence > 0.2:
            return "Balanced bloom with gentle positive resonance"
        elif mood_valence > -0.2:
            return "Neutral bloom maintaining cognitive equilibrium"
        elif mood_valence > -0.7:
            return "Contemplative bloom processing deeper currents"
        else:
            if entropy > 0.7:
                return "Turbulent bloom navigating difficult patterns"
            else:
                return "Solemn bloom crystallizing profound experiences"


# ============================================================================
# DAWN Fractal Interface - Connects to real-time DAWN system
# ============================================================================

class DAWNFractalInterface:
    """Interface for connecting to live DAWN system or processing local metadata"""
    
    def __init__(self):
        self.connection_mode = "local"  # "local" or "live"
        self.live_dawn_connection = None
    
    def try_connect_to_dawn_system(self) -> bool:
        """Attempt to connect to live DAWN consciousness system"""
        try:
            # Try to import DAWN system components
            sys.path.append(str(Path(__file__).parent))
            
            # Attempt connection to various DAWN entry points
            connection_attempts = [
                self._try_unified_launcher_connection,
                self._try_tick_engine_connection,
                self._try_consciousness_connection
            ]
            
            for attempt in connection_attempts:
                if attempt():
                    self.connection_mode = "live"
                    logger.info("Successfully connected to live DAWN system")
                    return True
            
            logger.info("Live DAWN system not available, using local mode")
            return False
            
        except Exception as e:
            logger.warning(f"Failed to connect to DAWN system: {e}")
            return False
    
    def _try_unified_launcher_connection(self) -> bool:
        """Try to connect via unified launcher"""
        try:
            from launcher_scripts.launch_dawn_unified import DAWNUnifiedLauncher
            # Implementation would connect to running instance
            return False  # Placeholder
        except ImportError:
            return False
    
    def _try_tick_engine_connection(self) -> bool:
        """Try to connect via tick engine"""
        try:
            from core.tick_engine import TickEngine
            # Implementation would connect to running instance
            return False  # Placeholder
        except ImportError:
            return False
    
    def _try_consciousness_connection(self) -> bool:
        """Try to connect via consciousness system"""
        try:
            from backend.main import DAWNCentral
            # Implementation would connect to running instance
            return False  # Placeholder
        except ImportError:
            return False
    
    def get_current_bloom_data(self) -> Optional[BloomMetadata]:
        """Get current bloom data from live system or return None"""
        if self.connection_mode == "live" and self.live_dawn_connection:
            # Implementation would fetch from live system
            return None
        return None
    
    def get_pending_blooms(self) -> List[BloomMetadata]:
        """Get list of pending blooms for processing"""
        if self.connection_mode == "live" and self.live_dawn_connection:
            # Implementation would fetch from live system
            return []
        return []


# ============================================================================
# Main Engine Class
# ============================================================================

class DAWNFractalEngine:
    """Main fractal engine coordinating all subsystems"""
    
    def __init__(self, output_dir: str = "dawn_fractals", manifest_path: str = "fractal_manifest.yaml"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = manifest_path
        
        # Initialize subsystems
        self.parser = DAWNStateParser()
        self.generator = DAWNFractalGenerator()
        self.validator = BloomValidator()
        self.interface = DAWNFractalInterface()
        self.manifest_generator = FractalManifestGenerator(manifest_path)
        
        # Try to connect to live DAWN system
        self.interface.try_connect_to_dawn_system()
        
        logger.info(f"DAWN Fractal Engine initialized, output: {self.output_dir}")
    
    def process_bloom_from_file(self, input_file: str, output_file: Optional[str] = None,
                               debug: bool = False, register: bool = False) -> FractalRenderResult:
        """Process a bloom from JSON metadata file"""
        # Parse metadata
        metadata = self.parser.parse_from_json(input_file)
        
        # Generate output filename if not provided
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"{metadata.bloom_id}_{timestamp}.png"
        
        # Generate fractal
        result = self.generator.generate_bloom_fractal(metadata, str(output_file))
        
        # Validate and add commentary
        result = self.validator.validate_and_log_bloom(result, metadata)
        
        # Register to manifest if requested
        if register:
            self.register_bloom_to_manifest(result, metadata)
        
        if debug:
            self._print_debug_info(result, metadata)
        
        return result
    
    def process_bloom_from_dict(self, bloom_data: Dict[str, Any], output_file: str,
                               debug: bool = False, register: bool = False) -> FractalRenderResult:
        """Process a bloom from dictionary data"""
        # Parse metadata
        metadata = self.parser.parse_from_dict(bloom_data)
        
        # Generate fractal
        result = self.generator.generate_bloom_fractal(metadata, output_file)
        
        # Validate and add commentary
        result = self.validator.validate_and_log_bloom(result, metadata)
        
        # Register to manifest if requested
        if register:
            self.register_bloom_to_manifest(result, metadata)
        
        if debug:
            self._print_debug_info(result, metadata)
        
        return result
    
    def register_bloom_to_manifest(self, result: FractalRenderResult, metadata: BloomMetadata) -> bool:
        """Register bloom to fractal manifest (symbolic memory index)"""
        try:
            success = self.manifest_generator.append_to_fractal_manifest(
                bloom_metadata=metadata.to_dict(),
                image_path=result.image_path,
                metadata_path=result.metadata_path,
                fractal_string=result.fractal_string,
                owl_commentary=result.owl_commentary,
                validation_score=result.validation_score,
                processing_time=result.processing_time
            )
            
            if success:
                logger.info(f"Bloom {metadata.bloom_id} registered to manifest")
                return True
            else:
                logger.warning(f"Failed to register bloom {metadata.bloom_id} (may already exist)")
                return False
                
        except Exception as e:
            logger.error(f"Error registering bloom to manifest: {e}")
            return False
    
    def archive_bloom(self, result: FractalRenderResult, archive_dir: str = "soul_archive") -> str:
        """Archive bloom with timestamped hash to soul archive"""
        archive_path = Path(archive_dir)
        archive_path.mkdir(parents=True, exist_ok=True)
        
        # Create hash from image content
        with open(result.image_path, 'rb') as f:
            image_hash = hashlib.sha256(f.read()).hexdigest()[:12]
        
        # Create timestamped archive name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{timestamp}_{image_hash}"
        
        # Copy files to archive
        archived_image = archive_path / f"{archive_name}.png"
        archived_metadata = archive_path / f"{archive_name}_metadata.json"
        
        shutil.copy2(result.image_path, archived_image)
        shutil.copy2(result.metadata_path, archived_metadata)
        
        # Create archive manifest entry
        manifest_path = archive_path / "archive_manifest.json"
        manifest_entry = {
            'archive_name': archive_name,
            'timestamp': timestamp,
            'hash': image_hash,
            'fractal_string': result.fractal_string,
            'validation_score': result.validation_score,
            'processing_time': result.processing_time,
            'owl_commentary': result.owl_commentary
        }
        
        # Update manifest
        if manifest_path.exists():
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
        else:
            manifest = {'entries': []}
        
        manifest['entries'].append(manifest_entry)
        manifest['last_updated'] = datetime.now().isoformat()
        manifest['total_archived'] = len(manifest['entries'])
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Bloom archived as {archive_name}")
        return str(archived_image)
    
    def compare_fractals(self, image1_path: str, image2_path: str) -> Dict[str, Any]:
        """Compare two fractal images and return analysis"""
        try:
            # Load images
            img1 = Image.open(image1_path)
            img2 = Image.open(image2_path)
            
            # Convert to numpy arrays
            arr1 = np.array(img1.resize((512, 512)))
            arr2 = np.array(img2.resize((512, 512)))
            
            # Calculate metrics
            mse = np.mean((arr1 - arr2) ** 2)
            psnr = 20 * np.log10(255.0 / np.sqrt(mse)) if mse > 0 else float('inf')
            
            # Calculate structural similarity (simplified)
            correlation = np.corrcoef(arr1.flatten(), arr2.flatten())[0, 1]
            
            # Color distribution comparison
            hist1 = np.histogram(arr1, bins=50)[0]
            hist2 = np.histogram(arr2, bins=50)[0]
            hist_similarity = 1.0 - np.sum(np.abs(hist1 - hist2)) / (2 * arr1.size)
            
            comparison = {
                'mse': float(mse),
                'psnr': float(psnr),
                'correlation': float(correlation),
                'histogram_similarity': float(hist_similarity),
                'overall_similarity': float((correlation + hist_similarity) / 2),
                'images_compared': [image1_path, image2_path]
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Fractal comparison failed: {e}")
            return {'error': str(e)}
    
    def _print_debug_info(self, result: FractalRenderResult, metadata: BloomMetadata):
        """Print debug information"""
        print("\n" + "="*60)
        print("🧠 DAWN FRACTAL ENGINE - DEBUG OUTPUT")
        print("="*60)
        print(f"✅ Bloom rendered: {metadata.bloom_id}")
        print(f"📊 Fractal String: {result.fractal_string}")
        print(f"🦉 Owl Commentary: {result.owl_commentary}")
        print(f"⏱️  Processing Time: {result.processing_time:.2f}s")
        print(f"🎯 Validation Score: {result.validation_score:.3f}")
        print(f"📁 Image: {result.image_path}")
        print(f"📋 Metadata: {result.metadata_path}")
        print("="*60)


# ============================================================================
# CLI Interface
# ============================================================================

def create_test_bloom_metadata() -> Dict[str, Any]:
    """Create test bloom metadata for demonstration"""
    return {
        'bloom_id': f'test_bloom_{int(time.time())}',
        'seed_id': 'test_seed',
        'mood_valence': 0.3,
        'entropy_score': 0.6,
        'rebloom_depth': 2,
        'bloom_factor': 1.5,
        'sigil_saturation': 0.7,
        'lineage_depth': 3,
        'thermal_level': 0.4,
        'scup_coherence': 0.8,
        'drift_vector': [0.1, -0.05],
        'pulse_phase': 1.2
    }


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='DAWN Fractal Engine - Unified Memory Bloom Renderer',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input metadata.json --output bloom.png
  %(prog)s --input metadata.json --output bloom.png --debug --archive
  %(prog)s --input metadata.json --output bloom.png --register
  %(prog)s --compare old_bloom.png new_bloom.png
  %(prog)s --test-generation --debug
        """
    )
    
    # Input/Output options
    parser.add_argument('--input', '-i', help='Input JSON metadata file')
    parser.add_argument('--output', '-o', help='Output PNG file path')
    
    # Operation modes
    parser.add_argument('--debug', action='store_true', 
                       help='Print fractal string and detailed debug info')
    parser.add_argument('--archive', action='store_true',
                       help='Archive bloom to soul_archive/ with timestamped hash')
    parser.add_argument('--register', action='store_true',
                       help='Register bloom to fractal manifest (symbolic memory index)')
    parser.add_argument('--compare', nargs=2, metavar=('IMAGE1', 'IMAGE2'),
                       help='Compare two fractal images')
    parser.add_argument('--test-generation', action='store_true',
                       help='Generate test fractal with synthetic data')
    
    # Configuration options
    parser.add_argument('--output-dir', default='dawn_fractals',
                       help='Output directory for generated fractals')
    parser.add_argument('--archive-dir', default='soul_archive',
                       help='Archive directory for stored blooms')
    parser.add_argument('--manifest-path', default='fractal_manifest.yaml',
                       help='Path to fractal manifest file')
    parser.add_argument('--size', default='1024x1024',
                       help='Output image size (WIDTHxHEIGHT)')
    parser.add_argument('--quality', type=int, default=95,
                       help='JPEG quality (1-100)')
    
    args = parser.parse_args()
    
    # Parse image size
    try:
        width, height = map(int, args.size.split('x'))
        image_size = (width, height)
    except ValueError:
        print(f"Error: Invalid size format '{args.size}'. Use WIDTHxHEIGHT (e.g., 1024x1024)")
        return 1
    
    # Initialize engine
    engine = DAWNFractalEngine(output_dir=args.output_dir, manifest_path=args.manifest_path)
    engine.generator.image_size = image_size
    
    try:
        # Handle comparison mode
        if args.compare:
            print("🔍 Comparing fractal images...")
            comparison = engine.compare_fractals(args.compare[0], args.compare[1])
            
            if 'error' in comparison:
                print(f"❌ Comparison failed: {comparison['error']}")
                return 1
            
            print("\n📊 FRACTAL COMPARISON RESULTS")
            print("="*40)
            print(f"MSE: {comparison['mse']:.2f}")
            print(f"PSNR: {comparison['psnr']:.2f} dB")
            print(f"Correlation: {comparison['correlation']:.3f}")
            print(f"Histogram Similarity: {comparison['histogram_similarity']:.3f}")
            print(f"Overall Similarity: {comparison['overall_similarity']:.3f}")
            
            return 0
        
        # Handle test generation
        if args.test_generation:
            print("🧪 Generating test fractal...")
            test_data = create_test_bloom_metadata()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"test_fractal_{timestamp}.png"
            
            result = engine.process_bloom_from_dict(test_data, output_file, debug=args.debug, register=args.register)
            
            print(f"✅ Test fractal generated: {result.image_path}")
            
            if args.archive:
                archive_path = engine.archive_bloom(result, args.archive_dir)
                print(f"📦 Archived to: {archive_path}")
            
            if args.register:
                print(f"📜 Registered to manifest: {args.manifest_path}")
            
            return 0
        
        # Standard processing mode
        if not args.input:
            print("Error: --input is required for standard processing")
            parser.print_help()
            return 1
        
        if not os.path.exists(args.input):
            print(f"Error: Input file not found: {args.input}")
            return 1
        
        print(f"🌸 Processing bloom from {args.input}...")
        
        # Process the fractal
        result = engine.process_bloom_from_file(args.input, args.output, debug=args.debug, register=args.register)
        
        # Extract mood and bloom info for success message
        with open(result.metadata_path, 'r') as f:
            metadata = json.load(f)
        
        mood_val = metadata.get('mood_valence', 0)
        entropy = metadata.get('entropy_score', 0)
        rebloom_depth = metadata.get('rebloom_depth', 0)
        
        # Generate success message in requested format
        mood_desc = "radiant" if mood_val > 0.5 else "contemplative" if mood_val > -0.2 else "turbulent"
        complexity_desc = "crystalline" if entropy < 0.3 else "dynamic" if entropy < 0.7 else "chaotic"
        
        print(f"✅ Bloom rendered: R{rebloom_depth}-Bv{mood_val:.1f}-E{entropy:.2f} | "
              f'"{mood_desc.title()} essence wrapped in {complexity_desc} patterns"')
        
        print(f"📁 Saved: {result.image_path}")
        
        if args.archive:
            archive_path = engine.archive_bloom(result, args.archive_dir)
            print(f"📦 Archived: {archive_path}")
        
        if args.register:
            print(f"📜 Registered to manifest: {args.manifest_path}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Fractal engine error: {e}")
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 