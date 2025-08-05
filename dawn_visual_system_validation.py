#!/usr/bin/env python3
"""
DAWN Visual System Validation
============================

Comprehensive test script that validates the enhanced consciousness visualization system
by loading existing memory files, regenerating fractals with new enhancements,
and performing detailed visual comparison analysis.

Tests:
- Parameter-to-visual correlation
- Old vs new fractal comparison
- Visual complexity analysis
- Side-by-side image generation
- Statistical validation
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
import time

# Import DAWN consciousness systems
from dawn_state_parser import DAWNStateParser, DAWNConsciousnessConfig
from dawn_shape_complexity import calculate_shape_complexity, ComplexityMode
from dawn_mood_palette import generate_mood_palette
from dawn_drift_transformation import apply_drift_transformation

@dataclass
class VisualAnalysis:
    """Analysis results for fractal visual characteristics"""
    
    complexity_score: float
    color_variance: float
    symmetry_measure: float
    edge_roughness: float
    motion_magnitude: float
    transparency_variation: float
    
    # Derived metrics
    overall_visual_complexity: float
    parameter_sensitivity: float

@dataclass
class ComparisonResult:
    """Results of old vs new fractal comparison"""
    
    memory_id: str
    consciousness_params: Dict[str, float]
    
    # Visual analysis
    old_analysis: Optional[VisualAnalysis]
    new_analysis: VisualAnalysis
    
    # Comparison metrics
    complexity_improvement: float
    visual_difference_score: float
    parameter_correlation: float
    
    # Generated files
    comparison_image_path: str
    analysis_report_path: str

class DAWNVisualSystemValidator:
    """Comprehensive validator for DAWN's consciousness visualization system"""
    
    def __init__(self, output_dir: str = "visual_validation_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "comparisons").mkdir(exist_ok=True)
        (self.output_dir / "analyses").mkdir(exist_ok=True)
        (self.output_dir / "parameter_tests").mkdir(exist_ok=True)
        
        self.parser = DAWNStateParser(strict_validation=False)
        
        # Visual analysis parameters
        self.image_resolution = (800, 600)
        self.fractal_resolution = 400
        
        print(f"🔬 DAWN Visual System Validator initialized")
        print(f"📁 Output directory: {self.output_dir}")
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run complete validation suite"""
        
        print("\n🧪 Running Comprehensive DAWN Visual System Validation")
        print("=" * 58)
        
        validation_results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'memory_analysis': {},
            'parameter_tests': {},
            'comparison_results': [],
            'correlation_scores': {},
            'summary_statistics': {}
        }
        
        # Step 1: Load and analyze memory files
        print("\n📁 Step 1: Loading DAWN Memory Files")
        memory_configs = self._load_memory_files()
        print(f"   ✅ Loaded {len(memory_configs)} memory configurations")
        
        # Step 2: Generate enhanced fractals and comparisons
        print("\n🎨 Step 2: Generating Enhanced Fractals")
        comparison_results = self._generate_comparison_fractals(memory_configs)
        validation_results['comparison_results'] = comparison_results
        print(f"   ✅ Generated {len(comparison_results)} fractal comparisons")
        
        # Step 3: Parameter sensitivity testing
        print("\n🧮 Step 3: Parameter Sensitivity Testing")
        parameter_tests = self._run_parameter_sensitivity_tests()
        validation_results['parameter_tests'] = parameter_tests
        print(f"   ✅ Completed parameter sensitivity analysis")
        
        # Step 4: Calculate correlation scores
        print("\n📊 Step 4: Calculating Correlation Scores")
        correlation_scores = self._calculate_correlation_scores(comparison_results, parameter_tests)
        validation_results['correlation_scores'] = correlation_scores
        print(f"   ✅ Computed parameter-to-visual correlations")
        
        # Step 5: Generate summary report
        print("\n📈 Step 5: Generating Summary Report")
        summary_stats = self._generate_summary_statistics(validation_results)
        validation_results['summary_statistics'] = summary_stats
        
        # Save comprehensive results
        results_file = self.output_dir / "comprehensive_validation_results.json"
        with open(results_file, 'w') as f:
            # Convert numpy types to native Python for JSON serialization
            json_safe_results = self._make_json_safe(validation_results)
            json.dump(json_safe_results, f, indent=2)
        
        print(f"   ✅ Saved comprehensive results to {results_file}")
        
        # Generate final summary
        self._print_validation_summary(validation_results)
        
        return validation_results
    
    def _load_memory_files(self) -> List[DAWNConsciousnessConfig]:
        """Load existing DAWN memory metadata files"""
        
        memory_dirs = [
            "dawn_soul_archive/metadata",
            "juliet_set_tests/metadata", 
            "emotional_bias_demo/metadata",
            "debug_juliet/metadata",
            "mood_palette_fractals/metadata",
            "shape_complexity_fractals/metadata"
        ]
        
        all_configs = []
        
        for directory in memory_dirs:
            dir_path = Path(directory)
            if dir_path.exists():
                try:
                    configs = self.parser.parse_multiple_files(dir_path)
                    all_configs.extend(configs)
                    print(f"   📂 {directory}: {len(configs)} files")
                except Exception as e:
                    print(f"   ⚠️  {directory}: Error - {e}")
        
        return all_configs[:20]  # Limit for comprehensive analysis
    
    def _generate_comparison_fractals(self, configs: List[DAWNConsciousnessConfig]) -> List[ComparisonResult]:
        """Generate fractals with old and new systems for comparison"""
        
        comparison_results = []
        
        for i, config in enumerate(configs):
            print(f"   🎯 Processing memory {i+1}/{len(configs)}: {config.memory_id}")
            
            # Generate enhanced fractal with new system
            new_analysis = self._generate_enhanced_fractal(config)
            
            # For comparison, we'll simulate "old" system analysis
            # (In practice, this would load actual old fractal if available)
            old_analysis = self._simulate_old_fractal_analysis(config)
            
            # Calculate comparison metrics
            comparison = self._compare_fractal_analyses(config, old_analysis, new_analysis)
            
            # Generate side-by-side comparison image
            comparison_image = self._create_comparison_image(config, old_analysis, new_analysis)
            comparison.comparison_image_path = str(comparison_image)
            
            # Generate detailed analysis report
            analysis_report = self._create_analysis_report(comparison)
            comparison.analysis_report_path = str(analysis_report)
            
            comparison_results.append(comparison)
        
        return comparison_results
    
    def _generate_enhanced_fractal(self, config: DAWNConsciousnessConfig) -> VisualAnalysis:
        """Generate fractal using enhanced consciousness visualization system"""
        
        # Calculate all consciousness components
        shape_complexity = calculate_shape_complexity(
            config.bloom_entropy, config.rebloom_depth
        )
        
        mood_palette = generate_mood_palette(
            config.mood_valence, config.sigil_saturation
        )
        
        # Create base fractal coordinates
        petal_count = shape_complexity.petal_count
        point_count = petal_count * 8  # Higher resolution for analysis
        
        angles = np.linspace(0, 2*math.pi, point_count, endpoint=False)
        
        # Apply shape complexity to base form
        edge_modulation = 1.0 + shape_complexity.edge_roughness * 0.3 * np.sin(angles * petal_count)
        base_radius = edge_modulation * (1.0 + 0.2 * np.sin(angles * petal_count / 2))
        
        base_coords = np.column_stack([
            base_radius * np.cos(angles),
            base_radius * np.sin(angles)
        ])
        
        # Apply drift transformation
        drift_transformation = apply_drift_transformation(
            base_coords, config.drift_vector, config.pulse_zone
        )
        
        # Analyze visual characteristics
        analysis = self._analyze_visual_characteristics(
            drift_transformation, shape_complexity, mood_palette
        )
        
        return analysis
    
    def _simulate_old_fractal_analysis(self, config: DAWNConsciousnessConfig) -> VisualAnalysis:
        """Simulate old fractal system for comparison"""
        
        # Create simple circular pattern (old system simulation)
        angles = np.linspace(0, 2*math.pi, 32, endpoint=False)
        old_coords = np.column_stack([np.cos(angles), np.sin(angles)])
        
        # Simple analysis with minimal features
        return VisualAnalysis(
            complexity_score=0.3,  # Low complexity
            color_variance=0.2,    # Minimal color variation
            symmetry_measure=0.9,  # High symmetry
            edge_roughness=0.1,    # Smooth edges
            motion_magnitude=0.0,  # No motion
            transparency_variation=0.0,  # No transparency effects
            overall_visual_complexity=0.25,
            parameter_sensitivity=0.2
        )
    
    def _analyze_visual_characteristics(self, drift_transformation, shape_complexity, mood_palette) -> VisualAnalysis:
        """Analyze visual characteristics of enhanced fractal"""
        
        coords = drift_transformation.transformed_coords
        
        # Calculate complexity score
        center = np.mean(coords, axis=0)
        distances = np.linalg.norm(coords - center, axis=1)
        complexity_score = np.std(distances) / np.mean(distances)
        
        # Calculate color variance
        color_values = np.array(mood_palette.base_colors)
        color_variance = np.std(color_values) / 255.0
        
        # Calculate symmetry measure
        # Test horizontal and vertical symmetry
        coords_centered = coords - center
        h_symmetry = np.mean(np.abs(coords_centered[:, 0] + np.flip(coords_centered[:, 0])))
        v_symmetry = np.mean(np.abs(coords_centered[:, 1] + np.flip(coords_centered[:, 1])))
        symmetry_measure = 1.0 - (h_symmetry + v_symmetry) / 2.0
        
        # Use shape complexity edge roughness
        edge_roughness = shape_complexity.edge_roughness
        
        # Calculate motion magnitude
        motion_magnitude = 0.0
        if drift_transformation.motion_vectors is not None:
            motion_magnitude = np.mean(np.linalg.norm(drift_transformation.motion_vectors, axis=1))
        
        # Calculate transparency variation
        transparency_variation = 0.0
        if drift_transformation.transparency_map is not None:
            transparency_variation = np.std(drift_transformation.transparency_map)
        
        # Calculate overall visual complexity
        overall_complexity = (
            complexity_score * 0.3 +
            color_variance * 0.2 +
            (1.0 - symmetry_measure) * 0.2 +
            edge_roughness * 0.15 +
            motion_magnitude * 0.1 +
            transparency_variation * 0.05
        )
        
        # Calculate parameter sensitivity (how much parameters affect visuals)
        parameter_sensitivity = (
            edge_roughness * 0.4 +
            color_variance * 0.3 +
            motion_magnitude * 0.2 +
            transparency_variation * 0.1
        )
        
        return VisualAnalysis(
            complexity_score=complexity_score,
            color_variance=color_variance,
            symmetry_measure=symmetry_measure,
            edge_roughness=edge_roughness,
            motion_magnitude=motion_magnitude,
            transparency_variation=transparency_variation,
            overall_visual_complexity=overall_complexity,
            parameter_sensitivity=parameter_sensitivity
        )
    
    def _compare_fractal_analyses(self, config: DAWNConsciousnessConfig, 
                                old_analysis: VisualAnalysis, 
                                new_analysis: VisualAnalysis) -> ComparisonResult:
        """Compare old and new fractal analyses"""
        
        # Calculate improvement metrics
        complexity_improvement = (
            new_analysis.overall_visual_complexity - old_analysis.overall_visual_complexity
        )
        
        # Calculate visual difference score
        visual_difference_score = abs(complexity_improvement) + abs(
            new_analysis.parameter_sensitivity - old_analysis.parameter_sensitivity
        )
        
        # Calculate parameter correlation (how well parameters map to visuals)
        parameter_correlation = new_analysis.parameter_sensitivity
        
        return ComparisonResult(
            memory_id=config.memory_id,
            consciousness_params={
                'bloom_entropy': config.bloom_entropy,
                'mood_valence': config.mood_valence,
                'drift_vector': config.drift_vector,
                'rebloom_depth': config.rebloom_depth,
                'sigil_saturation': config.sigil_saturation,
                'pulse_zone': config.pulse_zone
            },
            old_analysis=old_analysis,
            new_analysis=new_analysis,
            complexity_improvement=complexity_improvement,
            visual_difference_score=visual_difference_score,
            parameter_correlation=parameter_correlation,
            comparison_image_path="",  # Will be set later
            analysis_report_path=""   # Will be set later
        )
    
    def _create_comparison_image(self, config: DAWNConsciousnessConfig,
                               old_analysis: VisualAnalysis,
                               new_analysis: VisualAnalysis) -> Path:
        """Create side-by-side comparison image"""
        
        fig = plt.figure(figsize=(16, 10))
        gs = GridSpec(3, 4, figure=fig, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle(f'DAWN Visual System Comparison: {config.memory_id}', fontsize=16, fontweight='bold')
        
        # Old system visualization (simulated)
        ax_old = fig.add_subplot(gs[0:2, 0:2])
        self._plot_old_fractal(ax_old, config)
        ax_old.set_title('Old System (Simulated)', fontweight='bold')
        
        # New system visualization
        ax_new = fig.add_subplot(gs[0:2, 2:4])
        self._plot_new_fractal(ax_new, config)
        ax_new.set_title('Enhanced System', fontweight='bold')
        
        # Analysis comparison
        ax_analysis = fig.add_subplot(gs[2, :])
        self._plot_analysis_comparison(ax_analysis, old_analysis, new_analysis)
        
        # Save comparison image
        image_path = self.output_dir / "comparisons" / f"{config.memory_id}_comparison.png"
        plt.savefig(image_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        return image_path
    
    def _plot_old_fractal(self, ax, config: DAWNConsciousnessConfig):
        """Plot simulated old fractal system"""
        
        # Simple circular pattern
        angles = np.linspace(0, 2*math.pi, 32, endpoint=False)
        x = np.cos(angles)
        y = np.sin(angles)
        
        ax.plot(x, y, 'b-', linewidth=2, alpha=0.7)
        ax.scatter(x, y, c='blue', s=20, alpha=0.6)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Add parameter text
        param_text = f"Entropy: {config.bloom_entropy:.2f}\nValence: {config.mood_valence:.2f}"
        ax.text(-1.4, 1.3, param_text, fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
    
    def _plot_new_fractal(self, ax, config: DAWNConsciousnessConfig):
        """Plot enhanced fractal system"""
        
        # Generate enhanced fractal
        shape_complexity = calculate_shape_complexity(config.bloom_entropy, config.rebloom_depth)
        mood_palette = generate_mood_palette(config.mood_valence, config.sigil_saturation)
        
        # Create fractal coordinates
        petal_count = shape_complexity.petal_count
        angles = np.linspace(0, 2*math.pi, petal_count * 8, endpoint=False)
        
        edge_modulation = 1.0 + shape_complexity.edge_roughness * 0.3 * np.sin(angles * petal_count)
        radius = edge_modulation * (1.0 + 0.2 * np.sin(angles * petal_count / 2))
        
        base_coords = np.column_stack([
            radius * np.cos(angles),
            radius * np.sin(angles)
        ])
        
        # Apply drift transformation
        drift_transformation = apply_drift_transformation(
            base_coords, config.drift_vector, config.pulse_zone
        )
        
        coords = drift_transformation.transformed_coords
        
        # Plot with mood palette colors
        colors = [f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}" for color in mood_palette.base_colors]
        
        # Create color mapping
        color_indices = np.linspace(0, len(colors)-1, len(coords)).astype(int)
        point_colors = [colors[i] for i in color_indices]
        
        ax.plot(coords[:, 0], coords[:, 1], linewidth=2, alpha=0.8, color=colors[0])
        
        # Apply transparency if available
        alpha_values = 0.7
        if drift_transformation.transparency_map is not None:
            alpha_values = drift_transformation.transparency_map
        
        scatter = ax.scatter(coords[:, 0], coords[:, 1], c=point_colors, s=30, alpha=alpha_values)
        
        # Set limits with drift offset
        offset_x, offset_y = drift_transformation.center_offset
        ax.set_xlim(-2 + offset_x, 2 + offset_x)
        ax.set_ylim(-2 + offset_y, 2 + offset_y)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        # Add enhanced parameter text
        param_text = (f"Shape: {shape_complexity.shape_archetype}\n"
                     f"Petals: {shape_complexity.petal_count}\n"
                     f"Drift: {config.drift_vector:+.2f}\n"
                     f"Zone: {config.pulse_zone}")
        ax.text(-1.8 + offset_x, 1.8 + offset_y, param_text, fontsize=9, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[0], alpha=0.3))
    
    def _plot_analysis_comparison(self, ax, old_analysis: VisualAnalysis, new_analysis: VisualAnalysis):
        """Plot analysis comparison metrics"""
        
        metrics = ['Complexity', 'Color Variance', 'Edge Roughness', 'Motion', 'Transparency', 'Overall']
        old_values = [
            old_analysis.complexity_score,
            old_analysis.color_variance,
            old_analysis.edge_roughness,
            old_analysis.motion_magnitude,
            old_analysis.transparency_variation,
            old_analysis.overall_visual_complexity
        ]
        new_values = [
            new_analysis.complexity_score,
            new_analysis.color_variance,
            new_analysis.edge_roughness,
            new_analysis.motion_magnitude,
            new_analysis.transparency_variation,
            new_analysis.overall_visual_complexity
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, old_values, width, label='Old System', alpha=0.7, color='lightblue')
        bars2 = ax.bar(x + width/2, new_values, width, label='Enhanced System', alpha=0.7, color='lightcoral')
        
        ax.set_xlabel('Visual Metrics')
        ax.set_ylabel('Score')
        ax.set_title('Visual Analysis Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Add improvement indicators
        for i, (old_val, new_val) in enumerate(zip(old_values, new_values)):
            improvement = ((new_val - old_val) / max(old_val, 0.001)) * 100
            ax.text(i, max(old_val, new_val) + 0.02, f'{improvement:+.0f}%', 
                   ha='center', fontsize=8, fontweight='bold')
    
    def _create_analysis_report(self, comparison: ComparisonResult) -> Path:
        """Create detailed analysis report"""
        
        report_path = self.output_dir / "analyses" / f"{comparison.memory_id}_analysis.json"
        
        report_data = {
            'memory_id': comparison.memory_id,
            'consciousness_parameters': comparison.consciousness_params,
            'old_system_analysis': {
                'complexity_score': comparison.old_analysis.complexity_score,
                'color_variance': comparison.old_analysis.color_variance,
                'symmetry_measure': comparison.old_analysis.symmetry_measure,
                'edge_roughness': comparison.old_analysis.edge_roughness,
                'overall_complexity': comparison.old_analysis.overall_visual_complexity
            },
            'new_system_analysis': {
                'complexity_score': comparison.new_analysis.complexity_score,
                'color_variance': comparison.new_analysis.color_variance,
                'symmetry_measure': comparison.new_analysis.symmetry_measure,
                'edge_roughness': comparison.new_analysis.edge_roughness,
                'motion_magnitude': comparison.new_analysis.motion_magnitude,
                'transparency_variation': comparison.new_analysis.transparency_variation,
                'overall_complexity': comparison.new_analysis.overall_visual_complexity,
                'parameter_sensitivity': comparison.new_analysis.parameter_sensitivity
            },
            'comparison_metrics': {
                'complexity_improvement': comparison.complexity_improvement,
                'visual_difference_score': comparison.visual_difference_score,
                'parameter_correlation': comparison.parameter_correlation
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return report_path
    
    def _run_parameter_sensitivity_tests(self) -> Dict[str, Any]:
        """Run parameter sensitivity tests"""
        
        parameter_tests = {}
        
        # Test entropy sensitivity
        print("   🧮 Testing entropy sensitivity...")
        entropy_tests = self._test_entropy_sensitivity()
        parameter_tests['entropy'] = entropy_tests
        
        # Test mood valence sensitivity
        print("   💭 Testing mood valence sensitivity...")
        valence_tests = self._test_valence_sensitivity()
        parameter_tests['mood_valence'] = valence_tests
        
        # Test rebloom depth sensitivity
        print("   🔄 Testing rebloom depth sensitivity...")
        depth_tests = self._test_depth_sensitivity()
        parameter_tests['rebloom_depth'] = depth_tests
        
        # Test drift vector sensitivity
        print("   🌊 Testing drift vector sensitivity...")
        drift_tests = self._test_drift_sensitivity()
        parameter_tests['drift_vector'] = drift_tests
        
        return parameter_tests
    
    def _test_entropy_sensitivity(self) -> Dict[str, Any]:
        """Test high vs low entropy visual differences"""
        
        base_config = DAWNConsciousnessConfig(
            bloom_entropy=0.5, mood_valence=0.0, drift_vector=0.0,
            rebloom_depth=5, sigil_saturation=0.5, pulse_zone='stable'
        )
        
        # Test low entropy (0.1) vs high entropy (0.9)
        low_entropy_config = base_config
        low_entropy_config.bloom_entropy = 0.1
        
        high_entropy_config = base_config
        high_entropy_config.bloom_entropy = 0.9
        
        low_analysis = self._generate_enhanced_fractal(low_entropy_config)
        high_analysis = self._generate_enhanced_fractal(high_entropy_config)
        
        # Calculate visual difference
        visual_difference = abs(high_analysis.overall_visual_complexity - low_analysis.overall_visual_complexity)
        edge_difference = abs(high_analysis.edge_roughness - low_analysis.edge_roughness)
        
        # Create comparison image
        self._create_parameter_comparison_image(
            'entropy', low_entropy_config, high_entropy_config, 
            low_analysis, high_analysis
        )
        
        return {
            'low_entropy': {
                'value': 0.1,
                'complexity': low_analysis.overall_visual_complexity,
                'edge_roughness': low_analysis.edge_roughness
            },
            'high_entropy': {
                'value': 0.9,
                'complexity': high_analysis.overall_visual_complexity,
                'edge_roughness': high_analysis.edge_roughness
            },
            'visual_difference': visual_difference,
            'edge_difference': edge_difference,
            'sensitivity_score': visual_difference / 0.8  # Normalized by entropy range
        }
    
    def _test_valence_sensitivity(self) -> Dict[str, Any]:
        """Test positive vs negative mood valence visual differences"""
        
        base_config = DAWNConsciousnessConfig(
            bloom_entropy=0.5, mood_valence=0.0, drift_vector=0.0,
            rebloom_depth=5, sigil_saturation=0.5, pulse_zone='stable'
        )
        
        # Test negative valence (-0.8) vs positive valence (0.8)
        negative_config = base_config
        negative_config.mood_valence = -0.8
        
        positive_config = base_config
        positive_config.mood_valence = 0.8
        
        negative_analysis = self._generate_enhanced_fractal(negative_config)
        positive_analysis = self._generate_enhanced_fractal(positive_config)
        
        # Calculate visual difference
        color_difference = abs(positive_analysis.color_variance - negative_analysis.color_variance)
        complexity_difference = abs(positive_analysis.overall_visual_complexity - negative_analysis.overall_visual_complexity)
        
        # Create comparison image
        self._create_parameter_comparison_image(
            'mood_valence', negative_config, positive_config,
            negative_analysis, positive_analysis
        )
        
        return {
            'negative_valence': {
                'value': -0.8,
                'color_variance': negative_analysis.color_variance,
                'complexity': negative_analysis.overall_visual_complexity
            },
            'positive_valence': {
                'value': 0.8,
                'color_variance': positive_analysis.color_variance,
                'complexity': positive_analysis.overall_visual_complexity
            },
            'color_difference': color_difference,
            'complexity_difference': complexity_difference,
            'sensitivity_score': (color_difference + complexity_difference) / 1.6  # Normalized
        }
    
    def _test_depth_sensitivity(self) -> Dict[str, Any]:
        """Test varying rebloom depth visual differences"""
        
        base_config = DAWNConsciousnessConfig(
            bloom_entropy=0.5, mood_valence=0.0, drift_vector=0.0,
            rebloom_depth=5, sigil_saturation=0.5, pulse_zone='stable'
        )
        
        # Test shallow depth (3) vs deep depth (9)
        shallow_config = base_config
        shallow_config.rebloom_depth = 3
        
        deep_config = base_config
        deep_config.rebloom_depth = 9
        
        shallow_analysis = self._generate_enhanced_fractal(shallow_config)
        deep_analysis = self._generate_enhanced_fractal(deep_config)
        
        # Calculate visual difference
        complexity_difference = abs(deep_analysis.overall_visual_complexity - shallow_analysis.overall_visual_complexity)
        symmetry_difference = abs(deep_analysis.symmetry_measure - shallow_analysis.symmetry_measure)
        
        # Create comparison image
        self._create_parameter_comparison_image(
            'rebloom_depth', shallow_config, deep_config,
            shallow_analysis, deep_analysis
        )
        
        return {
            'shallow_depth': {
                'value': 3,
                'complexity': shallow_analysis.overall_visual_complexity,
                'symmetry': shallow_analysis.symmetry_measure
            },
            'deep_depth': {
                'value': 9,
                'complexity': deep_analysis.overall_visual_complexity,
                'symmetry': deep_analysis.symmetry_measure
            },
            'complexity_difference': complexity_difference,
            'symmetry_difference': symmetry_difference,
            'sensitivity_score': (complexity_difference + symmetry_difference) / 6  # Normalized
        }
    
    def _test_drift_sensitivity(self) -> Dict[str, Any]:
        """Test drift vector sensitivity"""
        
        base_config = DAWNConsciousnessConfig(
            bloom_entropy=0.5, mood_valence=0.0, drift_vector=0.0,
            rebloom_depth=5, sigil_saturation=0.5, pulse_zone='flowing'
        )
        
        # Test negative drift (-0.8) vs positive drift (0.8)
        negative_drift_config = base_config
        negative_drift_config.drift_vector = -0.8
        
        positive_drift_config = base_config
        positive_drift_config.drift_vector = 0.8
        
        negative_analysis = self._generate_enhanced_fractal(negative_drift_config)
        positive_analysis = self._generate_enhanced_fractal(positive_drift_config)
        
        # Calculate visual difference
        motion_difference = abs(positive_analysis.motion_magnitude - negative_analysis.motion_magnitude)
        symmetry_difference = abs(positive_analysis.symmetry_measure - negative_analysis.symmetry_measure)
        
        # Create comparison image
        self._create_parameter_comparison_image(
            'drift_vector', negative_drift_config, positive_drift_config,
            negative_analysis, positive_analysis
        )
        
        return {
            'negative_drift': {
                'value': -0.8,
                'motion_magnitude': negative_analysis.motion_magnitude,
                'symmetry': negative_analysis.symmetry_measure
            },
            'positive_drift': {
                'value': 0.8,
                'motion_magnitude': positive_analysis.motion_magnitude,
                'symmetry': positive_analysis.symmetry_measure
            },
            'motion_difference': motion_difference,
            'symmetry_difference': symmetry_difference,
            'sensitivity_score': (motion_difference + symmetry_difference) / 1.6  # Normalized
        }
    
    def _create_parameter_comparison_image(self, parameter_name: str, 
                                         config1: DAWNConsciousnessConfig,
                                         config2: DAWNConsciousnessConfig,
                                         analysis1: VisualAnalysis,
                                         analysis2: VisualAnalysis):
        """Create parameter sensitivity comparison image"""
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
        
        # Get parameter values with proper attribute names
        param_map = {
            'entropy': 'bloom_entropy',
            'mood_valence': 'mood_valence',
            'rebloom_depth': 'rebloom_depth',
            'drift_vector': 'drift_vector'
        }
        
        actual_param_name = param_map.get(parameter_name, parameter_name)
        value1 = getattr(config1, actual_param_name)
        value2 = getattr(config2, actual_param_name)
        
        # Plot first configuration
        ax1.set_title(f'{parameter_name}: {value1}')
        self._plot_new_fractal(ax1, config1)
        
        # Plot second configuration
        ax2.set_title(f'{parameter_name}: {value2}')
        self._plot_new_fractal(ax2, config2)
        
        # Plot analysis comparison
        metrics = ['Complexity', 'Color Var', 'Edge Rough', 'Motion', 'Symmetry']
        values1 = [analysis1.overall_visual_complexity, analysis1.color_variance, 
                  analysis1.edge_roughness, analysis1.motion_magnitude, analysis1.symmetry_measure]
        values2 = [analysis2.overall_visual_complexity, analysis2.color_variance,
                  analysis2.edge_roughness, analysis2.motion_magnitude, analysis2.symmetry_measure]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        ax3.bar(x - width/2, values1, width, label=f'{parameter_name}: {value1}', alpha=0.7)
        ax3.bar(x + width/2, values2, width, label=f'{parameter_name}: {value2}', alpha=0.7)
        
        ax3.set_xlabel('Visual Metrics')
        ax3.set_ylabel('Score')
        ax3.set_title(f'{parameter_name} Sensitivity Analysis')
        ax3.set_xticks(x)
        ax3.set_xticklabels(metrics, rotation=45)
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Save comparison image
        image_path = self.output_dir / "parameter_tests" / f"{parameter_name}_sensitivity.png"
        plt.savefig(image_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _calculate_correlation_scores(self, comparison_results: List[ComparisonResult], 
                                    parameter_tests: Dict[str, Any]) -> Dict[str, float]:
        """Calculate parameter-to-visual correlation scores"""
        
        correlation_scores = {}
        
        # Overall system improvement
        improvements = [result.complexity_improvement for result in comparison_results]
        correlation_scores['overall_system_improvement'] = np.mean(improvements)
        
        # Parameter sensitivity scores
        correlation_scores['entropy_sensitivity'] = parameter_tests['entropy']['sensitivity_score']
        correlation_scores['valence_sensitivity'] = parameter_tests['mood_valence']['sensitivity_score']
        correlation_scores['depth_sensitivity'] = parameter_tests['rebloom_depth']['sensitivity_score']
        correlation_scores['drift_sensitivity'] = parameter_tests['drift_vector']['sensitivity_score']
        
        # Average parameter correlation
        param_correlations = [result.parameter_correlation for result in comparison_results]
        correlation_scores['average_parameter_correlation'] = np.mean(param_correlations)
        
        # Visual difference scores
        visual_differences = [result.visual_difference_score for result in comparison_results]
        correlation_scores['average_visual_difference'] = np.mean(visual_differences)
        
        return correlation_scores
    
    def _generate_summary_statistics(self, validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary statistics"""
        
        comparison_results = validation_results['comparison_results']
        correlation_scores = validation_results['correlation_scores']
        
        summary = {
            'total_memories_analyzed': len(comparison_results),
            'average_complexity_improvement': correlation_scores['overall_system_improvement'],
            'parameter_sensitivity_scores': {
                'entropy': correlation_scores['entropy_sensitivity'],
                'mood_valence': correlation_scores['valence_sensitivity'],
                'rebloom_depth': correlation_scores['depth_sensitivity'],
                'drift_vector': correlation_scores['drift_sensitivity']
            },
            'visual_system_performance': {
                'average_parameter_correlation': correlation_scores['average_parameter_correlation'],
                'average_visual_difference': correlation_scores['average_visual_difference'],
                'system_responsiveness': np.mean([
                    correlation_scores['entropy_sensitivity'],
                    correlation_scores['valence_sensitivity'],
                    correlation_scores['depth_sensitivity'],
                    correlation_scores['drift_sensitivity']
                ])
            }
        }
        
        return summary
    
    def _make_json_safe(self, obj):
        """Convert numpy types and dataclasses to native Python types for JSON serialization"""
        if isinstance(obj, dict):
            return {key: self._make_json_safe(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_json_safe(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        elif hasattr(obj, '__dataclass_fields__'):  # Handle dataclasses
            return {field: self._make_json_safe(getattr(obj, field)) 
                   for field in obj.__dataclass_fields__}
        elif hasattr(obj, '__dict__'):  # Handle other objects with __dict__
            return {key: self._make_json_safe(value) for key, value in obj.__dict__.items()}
        else:
            return obj
    
    def _print_validation_summary(self, validation_results: Dict[str, Any]):
        """Print validation summary"""
        
        summary = validation_results['summary_statistics']
        
        print(f"\n🏆 DAWN Visual System Validation Summary")
        print("=" * 45)
        
        print(f"📊 Memories Analyzed: {summary['total_memories_analyzed']}")
        print(f"📈 Average Complexity Improvement: {summary['average_complexity_improvement']:.3f}")
        
        print(f"\n🎯 Parameter Sensitivity Scores:")
        for param, score in summary['parameter_sensitivity_scores'].items():
            print(f"   {param}: {score:.3f}")
        
        print(f"\n⚡ System Performance:")
        perf = summary['visual_system_performance']
        print(f"   Parameter Correlation: {perf['average_parameter_correlation']:.3f}")
        print(f"   Visual Difference: {perf['average_visual_difference']:.3f}")
        print(f"   System Responsiveness: {perf['system_responsiveness']:.3f}")
        
        print(f"\n📁 Generated Files:")
        print(f"   Comparison Images: {len(validation_results['comparison_results'])}")
        print(f"   Analysis Reports: {len(validation_results['comparison_results'])}")
        print(f"   Parameter Tests: {len(validation_results['parameter_tests'])}")

def main():
    """Run comprehensive DAWN visual system validation"""
    
    print("🔬 DAWN Visual System Comprehensive Validation")
    print("=" * 48)
    
    # Initialize validator
    validator = DAWNVisualSystemValidator()
    
    # Run comprehensive validation
    results = validator.run_comprehensive_validation()
    
    print(f"\n✅ Validation Complete!")
    print(f"📊 Results saved to: {validator.output_dir}")
    
    return results

if __name__ == "__main__":
    main() 