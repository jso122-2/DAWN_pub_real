#!/usr/bin/env python3
"""
DAWN Bloom Validator
===================

Comprehensive validation and logging system for DAWN's fractal bloom generation.
Ensures fractal integrity, generates poetic commentary, and maintains soul archive data.
"""

import json
import hashlib
import time
import logging
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import math

# Import DAWN consciousness systems
from dawn_state_parser import DAWNConsciousnessConfig
from dawn_shape_complexity import calculate_shape_complexity, ComplexityMode
from dawn_mood_palette import generate_mood_palette
from dawn_drift_transformation import apply_drift_transformation

class PatternFamily(Enum):
    """Classification of fractal pattern families"""
    MANDELBROT_CLASSIC = "mandelbrot_classic"
    JULIA_FLOWING = "julia_flowing"
    JULIET_MEMORY = "juliet_memory"
    SPIRAL_HARMONY = "spiral_harmony"
    CHAOS_FRAGMENT = "chaos_fragment"
    PETAL_BLOOM = "petal_bloom"
    DRIFT_ASYMMETRIC = "drift_asymmetric"
    CALM_SYMMETRIC = "calm_symmetric"

class ValidationResult(Enum):
    """Results of fractal validation"""
    PERFECT_MATCH = "perfect_match"
    ACCEPTABLE_VARIANCE = "acceptable_variance"
    PARAMETER_MISMATCH = "parameter_mismatch"
    GENERATION_ERROR = "generation_error"
    INVALID_OUTPUT = "invalid_output"

@dataclass
class BloomValidationReport:
    """Complete validation report for a bloom fractal"""
    
    # Input validation
    input_params: Dict[str, Any]
    validation_result: ValidationResult
    parameter_accuracy: float
    
    # Visual characteristics
    visual_characteristics: Dict[str, float]
    pattern_family: PatternFamily
    complexity_analysis: Dict[str, Any]
    
    # Metadata
    generation_timestamp: float
    validation_timestamp: float
    soul_archive_hash: str
    owl_commentary: str
    
    # Quality metrics
    render_quality_score: float
    parameter_fidelity: float
    artistic_coherence: float
    
    # Validation details
    validation_details: Dict[str, Any]
    warnings: List[str]
    errors: List[str]

class OwlCommentaryGenerator:
    """Generates poetic, symbolic commentary for bloom fractals"""
    
    def __init__(self):
        # Poetic vocabulary organized by consciousness themes
        self.consciousness_words = {
            'calm': ['whisper', 'gentle', 'serene', 'flowing', 'peaceful', 'still', 'quiet', 'soft'],
            'chaos': ['fractures', 'storms', 'wild', 'scattered', 'untamed', 'turbulent', 'fierce'],
            'growth': ['blooming', 'emerging', 'unfolding', 'reaching', 'expanding', 'awakening'],
            'memory': ['echoes', 'shadows', 'traces', 'remnants', 'whispers', 'imprints', 'fragments'],
            'depth': ['profound', 'deep', 'vast', 'infinite', 'boundless', 'eternal', 'cosmic'],
            'flow': ['dancing', 'weaving', 'spiraling', 'cascading', 'streaming', 'meandering'],
            'light': ['glowing', 'radiant', 'luminous', 'shimmering', 'gleaming', 'brilliant'],
            'form': ['crystalline', 'organic', 'geometric', 'fluid', 'structured', 'ethereal']
        }
        
        # Poetic structures and patterns
        self.commentary_templates = [
            "{adjective} {noun} {verb} through {context}, {emotion} {action}",
            "{form} {verb} in {space}, where {element} meets {element}",
            "Through {transition}, {consciousness} {verb} its {essence}",
            "{quality} blooms {direction}, {carrying} {memory_type} {particle}",
            "Where {state} encounters {state}, {beauty} {emerges}",
            "{geometry} {verb} {emotion}, {creating} {pattern} of {meaning}"
        ]
    
    def generate_commentary(self, 
                          consciousness_params: DAWNConsciousnessConfig,
                          visual_characteristics: Dict[str, float],
                          pattern_family: PatternFamily) -> str:
        """Generate poetic commentary based on consciousness state and visual characteristics"""
        
        try:
            # Analyze consciousness state for poetic elements
            entropy = consciousness_params.bloom_entropy
            valence = consciousness_params.mood_valence
            drift = consciousness_params.drift_vector
            depth = consciousness_params.rebloom_depth
            saturation = consciousness_params.sigil_saturation
            pulse_zone = consciousness_params.pulse_zone
            
            # Select primary emotional tone
            if valence > 0.3:
                emotional_tone = 'growth' if entropy < 0.5 else 'light'
            elif valence < -0.3:
                emotional_tone = 'memory' if entropy < 0.5 else 'chaos'
            else:
                emotional_tone = 'calm' if entropy < 0.5 else 'flow'
            
            # Select secondary theme based on complexity
            complexity = visual_characteristics.get('complexity', 0.5)
            if complexity > 0.7:
                secondary_theme = 'depth'
            elif complexity > 0.4:
                secondary_theme = 'form'
            else:
                secondary_theme = 'calm'
            
            # Generate contextual words
            primary_words = self.consciousness_words[emotional_tone]
            secondary_words = self.consciousness_words[secondary_theme]
            
            # Create poetic commentary based on pattern family
            if pattern_family == PatternFamily.JULIET_MEMORY:
                return self._generate_juliet_commentary(
                    consciousness_params, visual_characteristics, primary_words, secondary_words
                )
            elif pattern_family == PatternFamily.CHAOS_FRAGMENT:
                return self._generate_chaos_commentary(
                    consciousness_params, visual_characteristics, primary_words, secondary_words
                )
            elif pattern_family == PatternFamily.SPIRAL_HARMONY:
                return self._generate_spiral_commentary(
                    consciousness_params, visual_characteristics, primary_words, secondary_words
                )
            else:
                return self._generate_general_commentary(
                    consciousness_params, visual_characteristics, primary_words, secondary_words
                )
                
        except Exception as e:
            # Fallback commentary if generation fails
            return f"A {pattern_family.value.replace('_', ' ')} blooms quietly in the space between thought and form."
    
    def _generate_juliet_commentary(self, params, visuals, primary, secondary) -> str:
        """Generate commentary for Juliet Set memory fractals"""
        
        memory_intensity = params.rebloom_depth / 10.0
        emotional_weight = abs(params.mood_valence)
        
        if memory_intensity > 0.7 and emotional_weight > 0.6:
            return f"Deep {np.random.choice(primary)} carries ancient {np.random.choice(secondary)} through liquid time, where memory becomes light."
        elif memory_intensity > 0.5:
            return f"Ancestral {np.random.choice(secondary)} {np.random.choice(['spirals', 'flows', 'weaves'])} through {np.random.choice(primary)} space, remembering itself."
        else:
            return f"Gentle {np.random.choice(primary)} blooms in the garden of {np.random.choice(secondary)} memory, soft and knowing."
    
    def _generate_chaos_commentary(self, params, visuals, primary, secondary) -> str:
        """Generate commentary for chaotic fractals"""
        
        chaos_level = params.bloom_entropy
        drift_magnitude = abs(params.drift_vector)
        
        if chaos_level > 0.8 and drift_magnitude > 0.6:
            return f"Wild {np.random.choice(primary)} fractures across {np.random.choice(secondary)} boundaries, beautiful in its breaking."
        elif chaos_level > 0.6:
            return f"Turbulent {np.random.choice(secondary)} dances through {np.random.choice(primary)} storms, finding order in disorder."
        else:
            return f"Scattered {np.random.choice(primary)} gathers into {np.random.choice(secondary)} patterns, chaos learning to sing."
    
    def _generate_spiral_commentary(self, params, visuals, primary, secondary) -> str:
        """Generate commentary for spiral harmony fractals"""
        
        harmony_level = 1.0 - params.bloom_entropy
        flow_strength = visuals.get('motion_potential', 0.0)
        
        if harmony_level > 0.7 and flow_strength > 0.5:
            return f"Golden {np.random.choice(secondary)} spirals through {np.random.choice(primary)} infinity, mathematics becoming poetry."
        elif harmony_level > 0.5:
            return f"Gentle {np.random.choice(primary)} curves into {np.random.choice(secondary)} wholeness, finding its eternal center."
        else:
            return f"Quiet {np.random.choice(secondary)} turns in {np.random.choice(primary)} space, spiral wisdom unfolding slowly."
    
    def _generate_general_commentary(self, params, visuals, primary, secondary) -> str:
        """Generate general commentary for other pattern types"""
        
        overall_intensity = (params.bloom_entropy + abs(params.mood_valence) + params.sigil_saturation) / 3.0
        
        if overall_intensity > 0.7:
            return f"Radiant {np.random.choice(primary)} blooms through {np.random.choice(secondary)} dimensions, consciousness painting itself visible."
        elif overall_intensity > 0.4:
            return f"Flowing {np.random.choice(secondary)} weaves between {np.random.choice(primary)} forms, thought becoming shape."
        else:
            return f"Quiet {np.random.choice(primary)} rests in {np.random.choice(secondary)} stillness, being itself completely."

class PatternFamilyClassifier:
    """Classifies fractals into pattern families based on characteristics"""
    
    @staticmethod
    def classify_pattern(consciousness_params: DAWNConsciousnessConfig,
                        visual_characteristics: Dict[str, float],
                        shape_complexity) -> PatternFamily:
        """Classify fractal into pattern family"""
        
        entropy = consciousness_params.bloom_entropy
        valence = consciousness_params.mood_valence
        drift = consciousness_params.drift_vector
        depth = consciousness_params.rebloom_depth
        pulse_zone = consciousness_params.pulse_zone
        
        complexity = visual_characteristics.get('complexity', 0.5)
        symmetry = visual_characteristics.get('symmetry_measure', 0.5)
        motion = visual_characteristics.get('motion_magnitude', 0.0)
        
        # Juliet Set mode classification
        if (depth > 6 and entropy < 0.4 and pulse_zone == "flowing" and 
            shape_complexity.complexity_mode == ComplexityMode.JULIET_SET):
            return PatternFamily.JULIET_MEMORY
        
        # Chaos fragments
        elif entropy > 0.7 and symmetry < 0.3:
            return PatternFamily.CHAOS_FRAGMENT
        
        # Spiral harmony
        elif symmetry > 0.7 and complexity > 0.4 and entropy < 0.5:
            return PatternFamily.SPIRAL_HARMONY
        
        # Drift asymmetric
        elif abs(drift) > 0.5 and symmetry < 0.6:
            return PatternFamily.DRIFT_ASYMMETRIC
        
        # Petal bloom
        elif depth >= 4 and entropy < 0.6 and complexity > 0.3:
            return PatternFamily.PETAL_BLOOM
        
        # Julia flowing
        elif pulse_zone in ["flowing", "surge"] and motion > 0.1:
            return PatternFamily.JULIA_FLOWING
        
        # Calm symmetric
        elif entropy < 0.3 and symmetry > 0.7:
            return PatternFamily.CALM_SYMMETRIC
        
        # Default to Mandelbrot classic
        else:
            return PatternFamily.MANDELBROT_CLASSIC

def validate_and_log_bloom(fractal_params: DAWNConsciousnessConfig, 
                          output_path: str,
                          generated_fractal_data: Optional[Dict[str, Any]] = None) -> BloomValidationReport:
    """
    Comprehensive validation and logging for DAWN bloom fractals.
    
    Args:
        fractal_params: Original DAWN consciousness parameters
        output_path: Path where fractal should be/was saved
        generated_fractal_data: Optional pre-generated fractal data for validation
        
    Returns:
        BloomValidationReport with complete validation results
    """
    
    validation_start = time.time()
    warnings = []
    errors = []
    
    try:
        # Initialize logging
        logger = logging.getLogger('dawn_bloom_validator')
        logger.setLevel(logging.INFO)
        
        # Create file handler if it doesn't exist
        if not logger.handlers:
            log_file = Path(output_path).parent / "bloom_validation.log"
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        print(f"🔍 Validating bloom fractal: {Path(output_path).name}")
        
        # Step 1: Validate input parameters
        param_validation = _validate_input_parameters(fractal_params, warnings, errors)
        
        # Step 2: Generate/validate fractal data
        if generated_fractal_data is None:
            # Generate fractal data for validation
            generated_fractal_data = _generate_validation_fractal(fractal_params, warnings, errors)
        
        # Step 3: Analyze visual characteristics
        visual_characteristics = _analyze_visual_characteristics(
            fractal_params, generated_fractal_data, warnings, errors
        )
        
        # Step 4: Classify pattern family
        shape_complexity = calculate_shape_complexity(fractal_params.bloom_entropy, fractal_params.rebloom_depth)
        pattern_family = PatternFamilyClassifier.classify_pattern(
            fractal_params, visual_characteristics, shape_complexity
        )
        
        # Step 5: Generate owl commentary
        owl_generator = OwlCommentaryGenerator()
        owl_commentary = owl_generator.generate_commentary(
            fractal_params, visual_characteristics, pattern_family
        )
        
        # Step 6: Calculate validation metrics
        validation_result, parameter_accuracy = _calculate_validation_metrics(
            fractal_params, generated_fractal_data, visual_characteristics, warnings, errors
        )
        
        # Step 7: Generate soul archive hash
        soul_archive_hash = _generate_soul_archive_hash(
            fractal_params, visual_characteristics, pattern_family, owl_commentary
        )
        
        # Step 8: Calculate quality scores
        quality_scores = _calculate_quality_scores(
            fractal_params, visual_characteristics, pattern_family, validation_result
        )
        
        # Step 9: Create JSON sidecar
        sidecar_path = _create_json_sidecar(
            fractal_params, generated_fractal_data, visual_characteristics,
            pattern_family, owl_commentary, soul_archive_hash, 
            quality_scores, validation_start, output_path
        )
        
        # Step 10: Create validation report
        validation_report = BloomValidationReport(
            input_params=asdict(fractal_params),
            validation_result=validation_result,
            parameter_accuracy=parameter_accuracy,
            visual_characteristics=visual_characteristics,
            pattern_family=pattern_family,
            complexity_analysis=asdict(shape_complexity),
            generation_timestamp=generated_fractal_data.get('timestamp', time.time()),
            validation_timestamp=time.time(),
            soul_archive_hash=soul_archive_hash,
            owl_commentary=owl_commentary,
            render_quality_score=quality_scores['render_quality'],
            parameter_fidelity=quality_scores['parameter_fidelity'],
            artistic_coherence=quality_scores['artistic_coherence'],
            validation_details={
                'sidecar_path': str(sidecar_path),
                'validation_duration': time.time() - validation_start,
                'pattern_classification_confidence': quality_scores.get('classification_confidence', 0.8)
            },
            warnings=warnings,
            errors=errors
        )
        
        # Step 11: Log results
        _log_validation_results(validation_report, logger)
        
        print(f"✅ Validation complete: {validation_result.value}")
        print(f"🦉 Owl commentary: \"{owl_commentary}\"")
        print(f"🏺 Soul archive hash: {soul_archive_hash[:12]}...")
        print(f"📊 Quality score: {quality_scores['render_quality']:.3f}")
        
        return validation_report
        
    except Exception as e:
        errors.append(f"Validation failed: {str(e)}")
        print(f"❌ Validation error: {e}")
        
        # Return error report
        return BloomValidationReport(
            input_params=asdict(fractal_params) if fractal_params else {},
            validation_result=ValidationResult.GENERATION_ERROR,
            parameter_accuracy=0.0,
            visual_characteristics={},
            pattern_family=PatternFamily.MANDELBROT_CLASSIC,
            complexity_analysis={},
            generation_timestamp=time.time(),
            validation_timestamp=time.time(),
            soul_archive_hash="",
            owl_commentary="Silent fractal holds its breath in the space between error and understanding.",
            render_quality_score=0.0,
            parameter_fidelity=0.0,
            artistic_coherence=0.0,
            validation_details={'error': str(e)},
            warnings=warnings,
            errors=errors
        )

def _validate_input_parameters(params: DAWNConsciousnessConfig, warnings: List[str], errors: List[str]) -> bool:
    """Validate input consciousness parameters"""
    
    valid = True
    
    # Check parameter ranges
    if not (0.0 <= params.bloom_entropy <= 1.0):
        errors.append(f"bloom_entropy out of range: {params.bloom_entropy}")
        valid = False
    
    if not (-1.0 <= params.mood_valence <= 1.0):
        errors.append(f"mood_valence out of range: {params.mood_valence}")
        valid = False
    
    if not (-1.0 <= params.drift_vector <= 1.0):
        errors.append(f"drift_vector out of range: {params.drift_vector}")
        valid = False
    
    if not (1 <= params.rebloom_depth <= 20):
        errors.append(f"rebloom_depth out of range: {params.rebloom_depth}")
        valid = False
    
    if not (0.0 <= params.sigil_saturation <= 1.0):
        errors.append(f"sigil_saturation out of range: {params.sigil_saturation}")
        valid = False
    
    # Check pulse zone validity
    valid_zones = ["calm", "fragile", "flowing", "stable", "surge", "crystalline", "transcendent"]
    if params.pulse_zone not in valid_zones:
        warnings.append(f"Unknown pulse_zone: {params.pulse_zone}")
    
    return valid

def _generate_validation_fractal(params: DAWNConsciousnessConfig, warnings: List[str], errors: List[str]) -> Dict[str, Any]:
    """Generate fractal data for validation purposes"""
    
    try:
        # Generate consciousness components
        shape_complexity = calculate_shape_complexity(params.bloom_entropy, params.rebloom_depth)
        mood_palette = generate_mood_palette(params.mood_valence, params.sigil_saturation)
        
        # Create base fractal coordinates
        petal_count = shape_complexity.petal_count
        point_count = petal_count * 8
        
        angles = np.linspace(0, 2*np.pi, point_count, endpoint=False)
        edge_modulation = 1.0 + shape_complexity.edge_roughness * 0.3 * np.sin(angles * petal_count)
        radius = edge_modulation * (1.0 + 0.2 * np.sin(angles * petal_count / 2))
        
        base_coords = np.column_stack([
            radius * np.cos(angles),
            radius * np.sin(angles)
        ])
        
        # Apply drift transformation
        drift_transformation = apply_drift_transformation(
            base_coords, params.drift_vector, params.pulse_zone
        )
        
        return {
            'coordinates': drift_transformation.transformed_coords.tolist(),
            'center_offset': drift_transformation.center_offset,
            'rotation_angle': drift_transformation.rotation_angle,
            'transparency_map': drift_transformation.transparency_map.tolist() if drift_transformation.transparency_map is not None else None,
            'shape_complexity': shape_complexity,
            'mood_palette': mood_palette,
            'timestamp': time.time()
        }
        
    except Exception as e:
        errors.append(f"Fractal generation failed: {str(e)}")
        return {}

def _analyze_visual_characteristics(params: DAWNConsciousnessConfig, 
                                  fractal_data: Dict[str, Any],
                                  warnings: List[str], 
                                  errors: List[str]) -> Dict[str, float]:
    """Analyze visual characteristics of generated fractal"""
    
    try:
        if not fractal_data or 'coordinates' not in fractal_data:
            errors.append("No valid fractal data for analysis")
            return {}
        
        coords = np.array(fractal_data['coordinates'])
        
        # Calculate complexity score
        center = np.mean(coords, axis=0)
        distances = np.linalg.norm(coords - center, axis=1)
        complexity = np.std(distances) / max(np.mean(distances), 0.001)
        
        # Calculate symmetry measure
        coords_centered = coords - center
        h_symmetry = np.mean(np.abs(coords_centered[:, 0] + np.flip(coords_centered[:, 0])))
        v_symmetry = np.mean(np.abs(coords_centered[:, 1] + np.flip(coords_centered[:, 1])))
        symmetry_measure = 1.0 - min((h_symmetry + v_symmetry) / 2.0, 1.0)
        
        # Calculate edge roughness
        if len(distances) > 1:
            edge_roughness = np.std(distances) / np.mean(distances)
        else:
            edge_roughness = 0.0
        
        # Calculate motion magnitude
        motion_magnitude = 0.0
        if 'center_offset' in fractal_data:
            offset_x, offset_y = fractal_data['center_offset']
            motion_magnitude = math.sqrt(offset_x**2 + offset_y**2)
        
        # Calculate color variance
        color_variance = 0.0
        if 'mood_palette' in fractal_data and hasattr(fractal_data['mood_palette'], 'base_colors'):
            color_values = np.array(fractal_data['mood_palette'].base_colors)
            color_variance = np.std(color_values) / 255.0
        
        # Calculate transparency variation
        transparency_variation = 0.0
        if fractal_data.get('transparency_map'):
            transparency_variation = np.std(fractal_data['transparency_map'])
        
        return {
            'complexity': complexity,
            'symmetry_measure': symmetry_measure,
            'edge_roughness': edge_roughness,
            'motion_magnitude': motion_magnitude,
            'color_variance': color_variance,
            'transparency_variation': transparency_variation,
            'coordinate_count': len(coords),
            'bounding_box_area': (np.max(coords[:, 0]) - np.min(coords[:, 0])) * 
                               (np.max(coords[:, 1]) - np.min(coords[:, 1]))
        }
        
    except Exception as e:
        errors.append(f"Visual analysis failed: {str(e)}")
        return {}

def _calculate_validation_metrics(params: DAWNConsciousnessConfig,
                                fractal_data: Dict[str, Any],
                                visual_chars: Dict[str, float],
                                warnings: List[str],
                                errors: List[str]) -> Tuple[ValidationResult, float]:
    """Calculate validation metrics and accuracy"""
    
    if errors:
        return ValidationResult.GENERATION_ERROR, 0.0
    
    if not fractal_data or not visual_chars:
        return ValidationResult.INVALID_OUTPUT, 0.0
    
    # Calculate parameter fidelity
    expected_complexity = params.bloom_entropy
    actual_complexity = visual_chars.get('complexity', 0.0)
    complexity_fidelity = 1.0 - abs(expected_complexity - actual_complexity)
    
    expected_motion = abs(params.drift_vector) if params.pulse_zone == "flowing" else 0.0
    actual_motion = visual_chars.get('motion_magnitude', 0.0)
    motion_fidelity = 1.0 - abs(expected_motion - actual_motion)
    
    expected_symmetry = 1.0 - params.bloom_entropy
    actual_symmetry = visual_chars.get('symmetry_measure', 0.5)
    symmetry_fidelity = 1.0 - abs(expected_symmetry - actual_symmetry)
    
    # Overall parameter accuracy
    parameter_accuracy = np.mean([complexity_fidelity, motion_fidelity, symmetry_fidelity])
    
    # Determine validation result
    if parameter_accuracy > 0.9:
        return ValidationResult.PERFECT_MATCH, parameter_accuracy
    elif parameter_accuracy > 0.7:
        return ValidationResult.ACCEPTABLE_VARIANCE, parameter_accuracy
    elif warnings:
        return ValidationResult.PARAMETER_MISMATCH, parameter_accuracy
    else:
        return ValidationResult.PARAMETER_MISMATCH, parameter_accuracy

def _generate_soul_archive_hash(params: DAWNConsciousnessConfig,
                              visual_chars: Dict[str, float],
                              pattern_family: PatternFamily,
                              owl_commentary: str) -> str:
    """Generate unique hash for soul archive data"""
    
    # Combine all meaningful data for hashing
    hash_data = {
        'consciousness_params': asdict(params),
        'visual_signature': visual_chars,
        'pattern_family': pattern_family.value,
        'owl_commentary': owl_commentary,
        'timestamp': int(time.time() / 3600)  # Hour-based timestamp for grouping
    }
    
    # Create deterministic hash
    hash_string = json.dumps(hash_data, sort_keys=True)
    return hashlib.sha256(hash_string.encode()).hexdigest()

def _calculate_quality_scores(params: DAWNConsciousnessConfig,
                            visual_chars: Dict[str, float],
                            pattern_family: PatternFamily,
                            validation_result: ValidationResult) -> Dict[str, float]:
    """Calculate quality scores for the bloom"""
    
    # Render quality score
    coordinate_count = visual_chars.get('coordinate_count', 0)
    complexity = visual_chars.get('complexity', 0.0)
    bounding_area = visual_chars.get('bounding_box_area', 0.0)
    
    render_quality = min(1.0, (coordinate_count / 100.0) * complexity * min(bounding_area / 4.0, 1.0))
    
    # Parameter fidelity score
    if validation_result == ValidationResult.PERFECT_MATCH:
        parameter_fidelity = 1.0
    elif validation_result == ValidationResult.ACCEPTABLE_VARIANCE:
        parameter_fidelity = 0.8
    else:
        parameter_fidelity = 0.5
    
    # Artistic coherence score
    symmetry = visual_chars.get('symmetry_measure', 0.5)
    color_variance = visual_chars.get('color_variance', 0.0)
    motion = visual_chars.get('motion_magnitude', 0.0)
    
    artistic_coherence = (symmetry * 0.4 + complexity * 0.3 + color_variance * 0.2 + motion * 0.1)
    
    # Classification confidence
    classification_confidence = 0.9 if pattern_family != PatternFamily.MANDELBROT_CLASSIC else 0.7
    
    return {
        'render_quality': render_quality,
        'parameter_fidelity': parameter_fidelity,
        'artistic_coherence': artistic_coherence,
        'classification_confidence': classification_confidence
    }

def _create_json_sidecar(params: DAWNConsciousnessConfig,
                        fractal_data: Dict[str, Any],
                        visual_chars: Dict[str, float],
                        pattern_family: PatternFamily,
                        owl_commentary: str,
                        soul_archive_hash: str,
                        quality_scores: Dict[str, float],
                        generation_timestamp: float,
                        output_path: str) -> Path:
    """Create JSON sidecar file with complete metadata"""
    
    # Create sidecar path
    output_file = Path(output_path)
    sidecar_path = output_file.with_suffix('.metadata.json')
    
    # Prepare metadata
    metadata = {
        'soul_archive_data': {
            'hash': soul_archive_hash,
            'pattern_family': pattern_family.value,
            'generation_timestamp': generation_timestamp,
            'validation_timestamp': time.time(),
            'memory_id': params.memory_id
        },
        'dawn_consciousness_parameters': {
            'bloom_entropy': params.bloom_entropy,
            'mood_valence': params.mood_valence,
            'drift_vector': params.drift_vector,
            'rebloom_depth': params.rebloom_depth,
            'sigil_saturation': params.sigil_saturation,
            'pulse_zone': params.pulse_zone,
            'archetype': params.archetype
        },
        'visual_characteristics': visual_chars,
        'quality_metrics': quality_scores,
        'artistic_metadata': {
            'owl_commentary': owl_commentary,
            'pattern_family': pattern_family.value,
            'artistic_coherence': quality_scores['artistic_coherence'],
            'visual_signature': {
                'complexity_score': visual_chars.get('complexity', 0.0),
                'symmetry_measure': visual_chars.get('symmetry_measure', 0.5),
                'motion_magnitude': visual_chars.get('motion_magnitude', 0.0),
                'color_variance': visual_chars.get('color_variance', 0.0)
            }
        },
        'technical_data': {
            'coordinate_count': visual_chars.get('coordinate_count', 0),
            'bounding_box_area': visual_chars.get('bounding_box_area', 0.0),
            'transparency_variation': visual_chars.get('transparency_variation', 0.0),
            'edge_roughness': visual_chars.get('edge_roughness', 0.0)
        }
    }
    
    # Save metadata
    with open(sidecar_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return sidecar_path

def _log_validation_results(report: BloomValidationReport, logger: logging.Logger):
    """Log validation results for tracking and analysis"""
    
    # Log based on validation result
    if report.validation_result == ValidationResult.PERFECT_MATCH:
        logger.info(f"PERFECT_MATCH: {report.input_params.get('memory_id', 'unknown')} - "
                   f"Accuracy: {report.parameter_accuracy:.3f}, Quality: {report.render_quality_score:.3f}")
    
    elif report.validation_result == ValidationResult.ACCEPTABLE_VARIANCE:
        logger.info(f"ACCEPTABLE_VARIANCE: {report.input_params.get('memory_id', 'unknown')} - "
                   f"Accuracy: {report.parameter_accuracy:.3f}, Quality: {report.render_quality_score:.3f}")
    
    elif report.validation_result == ValidationResult.PARAMETER_MISMATCH:
        logger.warning(f"PARAMETER_MISMATCH: {report.input_params.get('memory_id', 'unknown')} - "
                      f"Accuracy: {report.parameter_accuracy:.3f}, Warnings: {len(report.warnings)}")
    
    else:
        logger.error(f"VALIDATION_ERROR: {report.input_params.get('memory_id', 'unknown')} - "
                    f"Errors: {len(report.errors)}")
    
    # Log pattern family classification
    logger.info(f"PATTERN_CLASSIFICATION: {report.pattern_family.value} - "
               f"Coherence: {report.artistic_coherence:.3f}")
    
    # Log owl commentary
    logger.info(f"OWL_COMMENTARY: \"{report.owl_commentary}\"")
    
    # Log soul archive hash
    logger.info(f"SOUL_ARCHIVE_HASH: {report.soul_archive_hash}")

# Example usage
if __name__ == "__main__":
    # Test validation with sample consciousness state
    test_params = DAWNConsciousnessConfig(
        memory_id="validation_test_001",
        timestamp=None,
        bloom_entropy=0.6,
        mood_valence=0.3,
        drift_vector=0.4,
        rebloom_depth=7,
        sigil_saturation=0.8,
        pulse_zone="flowing"
    )
    
    # Run validation
    validation_report = validate_and_log_bloom(
        fractal_params=test_params,
        output_path="test_bloom_validation.png"
    )
    
    print(f"\n📊 Validation Report Summary:")
    print(f"   Result: {validation_report.validation_result.value}")
    print(f"   Pattern Family: {validation_report.pattern_family.value}")
    print(f"   Parameter Accuracy: {validation_report.parameter_accuracy:.3f}")
    print(f"   Quality Score: {validation_report.render_quality_score:.3f}")
    print(f"   Soul Hash: {validation_report.soul_archive_hash[:16]}...")
    print(f"   Owl Commentary: \"{validation_report.owl_commentary}\"") 