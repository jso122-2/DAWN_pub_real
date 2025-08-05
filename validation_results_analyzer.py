#!/usr/bin/env python3
"""
DAWN Visual System Validation Results Analyzer
==============================================

Analyzes the comprehensive validation results and provides detailed insights
about the DAWN consciousness visualization system performance.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Dict, List, Any

class ValidationResultsAnalyzer:
    """Analyzes DAWN visual system validation results"""
    
    def __init__(self, results_dir: str = "visual_validation_results"):
        self.results_dir = Path(results_dir)
        self.results_file = self.results_dir / "comprehensive_validation_results.json"
        
        if not self.results_file.exists():
            raise FileNotFoundError(f"Results file not found: {self.results_file}")
        
        # Load results
        with open(self.results_file, 'r') as f:
            self.results = json.load(f)
    
    def generate_comprehensive_report(self):
        """Generate comprehensive analysis report"""
        
        print("📊 DAWN Visual System Validation - Detailed Analysis")
        print("=" * 55)
        
        # Basic statistics
        self._analyze_basic_statistics()
        
        # Parameter analysis
        self._analyze_parameter_effects()
        
        # Visual complexity analysis
        self._analyze_visual_complexity()
        
        # System performance metrics
        self._analyze_system_performance()
        
        # Correlation analysis
        self._analyze_correlations()
        
        # Generate visualizations
        self._create_analysis_visualizations()
        
        # Final recommendations
        self._provide_recommendations()
    
    def _analyze_basic_statistics(self):
        """Analyze basic validation statistics"""
        
        print(f"\n📈 Basic Validation Statistics")
        print("=" * 32)
        
        summary = self.results['summary_statistics']
        
        print(f"Total Memories Analyzed: {summary['total_memories_analyzed']}")
        print(f"Average Complexity Improvement: {summary['average_complexity_improvement']:.3f}")
        
        # Analyze comparison results
        comparisons = self.results['comparison_results']
        
        improvements = [comp['complexity_improvement'] for comp in comparisons]
        visual_diffs = [comp['visual_difference_score'] for comp in comparisons]
        param_correlations = [comp['parameter_correlation'] for comp in comparisons]
        
        print(f"\nComplexity Improvements:")
        print(f"  Range: {min(improvements):.3f} to {max(improvements):.3f}")
        print(f"  Standard Deviation: {np.std(improvements):.3f}")
        print(f"  Positive Improvements: {sum(1 for i in improvements if i > 0)}/{len(improvements)}")
        
        print(f"\nVisual Differences:")
        print(f"  Range: {min(visual_diffs):.3f} to {max(visual_diffs):.3f}")
        print(f"  Average: {np.mean(visual_diffs):.3f}")
        
        print(f"\nParameter Correlations:")
        print(f"  Range: {min(param_correlations):.3f} to {max(param_correlations):.3f}")
        print(f"  Average: {np.mean(param_correlations):.3f}")
    
    def _analyze_parameter_effects(self):
        """Analyze individual parameter effects"""
        
        print(f"\n🎯 Parameter Effect Analysis")
        print("=" * 29)
        
        param_tests = self.results['parameter_tests']
        
        for param_name, test_data in param_tests.items():
            print(f"\n{param_name.upper()}:")
            
            if param_name == 'entropy':
                low_data = test_data['low_entropy']
                high_data = test_data['high_entropy']
                print(f"  Low Entropy ({low_data['value']}):")
                print(f"    Complexity: {low_data['complexity']:.3f}")
                print(f"    Edge Roughness: {low_data['edge_roughness']:.3f}")
                print(f"  High Entropy ({high_data['value']}):")
                print(f"    Complexity: {high_data['complexity']:.3f}")
                print(f"    Edge Roughness: {high_data['edge_roughness']:.3f}")
                print(f"  Visual Difference: {test_data['visual_difference']:.3f}")
                print(f"  Edge Difference: {test_data['edge_difference']:.3f}")
                
            elif param_name == 'mood_valence':
                neg_data = test_data['negative_valence']
                pos_data = test_data['positive_valence']
                print(f"  Negative Valence ({neg_data['value']}):")
                print(f"    Color Variance: {neg_data['color_variance']:.3f}")
                print(f"  Positive Valence ({pos_data['value']}):")
                print(f"    Color Variance: {pos_data['color_variance']:.3f}")
                print(f"  Color Difference: {test_data['color_difference']:.3f}")
                
            elif param_name == 'rebloom_depth':
                shallow_data = test_data['shallow_depth']
                deep_data = test_data['deep_depth']
                print(f"  Shallow Depth ({shallow_data['value']}):")
                print(f"    Complexity: {shallow_data['complexity']:.3f}")
                print(f"  Deep Depth ({deep_data['value']}):")
                print(f"    Complexity: {deep_data['complexity']:.3f}")
                print(f"  Complexity Difference: {test_data['complexity_difference']:.3f}")
                
            elif param_name == 'drift_vector':
                neg_data = test_data['negative_drift']
                pos_data = test_data['positive_drift']
                print(f"  Negative Drift ({neg_data['value']}):")
                print(f"    Motion: {neg_data['motion_magnitude']:.4f}")
                print(f"  Positive Drift ({pos_data['value']}):")
                print(f"    Motion: {pos_data['motion_magnitude']:.4f}")
                print(f"  Motion Difference: {test_data['motion_difference']:.4f}")
            
            print(f"  Sensitivity Score: {test_data['sensitivity_score']:.3f}")
    
    def _analyze_visual_complexity(self):
        """Analyze visual complexity patterns"""
        
        print(f"\n🎨 Visual Complexity Analysis")
        print("=" * 31)
        
        comparisons = self.results['comparison_results']
        
        # Group by consciousness parameters
        entropy_groups = {'low': [], 'medium': [], 'high': []}
        valence_groups = {'negative': [], 'neutral': [], 'positive': []}
        depth_groups = {'shallow': [], 'medium': [], 'deep': []}
        
        for comp in comparisons:
            params = comp['consciousness_params']
            new_analysis = comp['new_analysis']
            
            # Group by entropy
            if params['bloom_entropy'] < 0.4:
                entropy_groups['low'].append(new_analysis['overall_complexity'])
            elif params['bloom_entropy'] < 0.7:
                entropy_groups['medium'].append(new_analysis['overall_complexity'])
            else:
                entropy_groups['high'].append(new_analysis['overall_complexity'])
            
            # Group by valence
            if params['mood_valence'] < -0.2:
                valence_groups['negative'].append(new_analysis['overall_complexity'])
            elif params['mood_valence'] < 0.2:
                valence_groups['neutral'].append(new_analysis['overall_complexity'])
            else:
                valence_groups['positive'].append(new_analysis['overall_complexity'])
            
            # Group by depth
            if params['rebloom_depth'] < 5:
                depth_groups['shallow'].append(new_analysis['overall_complexity'])
            elif params['rebloom_depth'] < 8:
                depth_groups['medium'].append(new_analysis['overall_complexity'])
            else:
                depth_groups['deep'].append(new_analysis['overall_complexity'])
        
        # Report complexity by groups
        print(f"Complexity by Entropy Level:")
        for level, complexities in entropy_groups.items():
            if complexities:
                avg_complexity = np.mean(complexities)
                print(f"  {level.capitalize()}: {avg_complexity:.3f} (n={len(complexities)})")
        
        print(f"\nComplexity by Mood Valence:")
        for mood, complexities in valence_groups.items():
            if complexities:
                avg_complexity = np.mean(complexities)
                print(f"  {mood.capitalize()}: {avg_complexity:.3f} (n={len(complexities)})")
        
        print(f"\nComplexity by Rebloom Depth:")
        for depth, complexities in depth_groups.items():
            if complexities:
                avg_complexity = np.mean(complexities)
                print(f"  {depth.capitalize()}: {avg_complexity:.3f} (n={len(complexities)})")
    
    def _analyze_system_performance(self):
        """Analyze overall system performance"""
        
        print(f"\n⚡ System Performance Analysis")
        print("=" * 32)
        
        performance = self.results['summary_statistics']['visual_system_performance']
        correlations = self.results['correlation_scores']
        
        print(f"Parameter Correlation: {performance['average_parameter_correlation']:.3f}")
        print(f"Visual Difference Score: {performance['average_visual_difference']:.3f}")
        print(f"System Responsiveness: {performance['system_responsiveness']:.3f}")
        
        print(f"\nSystem Improvement Metrics:")
        print(f"  Overall System Improvement: {correlations['overall_system_improvement']:.3f}")
        
        # Calculate success rate
        comparisons = self.results['comparison_results']
        successful_improvements = sum(1 for comp in comparisons if comp['complexity_improvement'] > 0)
        success_rate = successful_improvements / len(comparisons)
        
        print(f"  Improvement Success Rate: {success_rate:.1%}")
        
        # Calculate visual enhancement score
        visual_enhancements = [comp['visual_difference_score'] for comp in comparisons]
        avg_enhancement = np.mean(visual_enhancements)
        
        print(f"  Average Visual Enhancement: {avg_enhancement:.3f}")
    
    def _analyze_correlations(self):
        """Analyze parameter-to-visual correlations"""
        
        print(f"\n🔗 Parameter-Visual Correlations")
        print("=" * 34)
        
        correlations = self.results['correlation_scores']
        
        sensitivity_scores = {
            'Entropy': correlations['entropy_sensitivity'],
            'Mood Valence': correlations['valence_sensitivity'],
            'Rebloom Depth': correlations['depth_sensitivity'],
            'Drift Vector': correlations['drift_sensitivity']
        }
        
        print(f"Parameter Sensitivity Rankings:")
        sorted_sensitivities = sorted(sensitivity_scores.items(), key=lambda x: x[1], reverse=True)
        
        for i, (param, score) in enumerate(sorted_sensitivities, 1):
            print(f"  {i}. {param}: {score:.3f}")
        
        # Calculate correlation strength
        avg_sensitivity = np.mean(list(sensitivity_scores.values()))
        
        if avg_sensitivity > 0.3:
            correlation_strength = "Strong"
        elif avg_sensitivity > 0.1:
            correlation_strength = "Moderate"
        else:
            correlation_strength = "Weak"
        
        print(f"\nOverall Correlation Strength: {correlation_strength} ({avg_sensitivity:.3f})")
    
    def _create_analysis_visualizations(self):
        """Create analysis visualization charts"""
        
        print(f"\n📈 Generating Analysis Visualizations")
        print("=" * 37)
        
        # Create multi-panel analysis chart
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('DAWN Visual System Validation Analysis', fontsize=16, fontweight='bold')
        
        # 1. Complexity improvement distribution
        comparisons = self.results['comparison_results']
        improvements = [comp['complexity_improvement'] for comp in comparisons]
        
        ax1.hist(improvements, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.axvline(np.mean(improvements), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(improvements):.3f}')
        ax1.set_xlabel('Complexity Improvement')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Complexity Improvement Distribution')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Parameter sensitivity comparison
        sensitivity_data = [
            self.results['correlation_scores']['entropy_sensitivity'],
            self.results['correlation_scores']['valence_sensitivity'],
            self.results['correlation_scores']['depth_sensitivity'],
            self.results['correlation_scores']['drift_sensitivity']
        ]
        
        param_names = ['Entropy', 'Valence', 'Depth', 'Drift']
        bars = ax2.bar(param_names, sensitivity_data, alpha=0.7, 
                      color=['red', 'blue', 'green', 'purple'])
        ax2.set_ylabel('Sensitivity Score')
        ax2.set_title('Parameter Sensitivity Comparison')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, sensitivity_data):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')
        
        # 3. Visual complexity vs parameters scatter
        entropies = [comp['consciousness_params']['bloom_entropy'] for comp in comparisons]
        complexities = [comp['new_analysis']['overall_complexity'] for comp in comparisons]
        
        ax3.scatter(entropies, complexities, alpha=0.6, s=50)
        ax3.set_xlabel('Bloom Entropy')
        ax3.set_ylabel('Visual Complexity')
        ax3.set_title('Entropy vs Visual Complexity')
        ax3.grid(True, alpha=0.3)
        
        # Add trend line
        z = np.polyfit(entropies, complexities, 1)
        p = np.poly1d(z)
        ax3.plot(entropies, p(entropies), "r--", alpha=0.8)
        
        # 4. System performance metrics
        performance_metrics = [
            self.results['summary_statistics']['visual_system_performance']['average_parameter_correlation'],
            self.results['summary_statistics']['visual_system_performance']['average_visual_difference'],
            self.results['summary_statistics']['visual_system_performance']['system_responsiveness']
        ]
        
        metric_names = ['Param\nCorrelation', 'Visual\nDifference', 'System\nResponsiveness']
        colors = ['lightcoral', 'lightblue', 'lightgreen']
        
        bars = ax4.bar(metric_names, performance_metrics, alpha=0.7, color=colors)
        ax4.set_ylabel('Score')
        ax4.set_title('System Performance Metrics')
        ax4.set_ylim(0, max(performance_metrics) * 1.2)
        ax4.grid(True, alpha=0.3)
        
        # Add value labels
        for bar, value in zip(bars, performance_metrics):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        # Save analysis chart
        analysis_chart_path = self.results_dir / "validation_analysis_summary.png"
        plt.savefig(analysis_chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ Analysis chart saved: {analysis_chart_path}")
    
    def _provide_recommendations(self):
        """Provide recommendations based on analysis"""
        
        print(f"\n💡 System Recommendations")
        print("=" * 27)
        
        correlations = self.results['correlation_scores']
        performance = self.results['summary_statistics']['visual_system_performance']
        
        recommendations = []
        
        # Check parameter sensitivity
        avg_sensitivity = (
            correlations['entropy_sensitivity'] +
            correlations['valence_sensitivity'] +
            correlations['depth_sensitivity'] +
            correlations['drift_sensitivity']
        ) / 4
        
        if avg_sensitivity < 0.1:
            recommendations.append(
                "🔧 LOW PARAMETER SENSITIVITY: Consider increasing parameter influence on visual output"
            )
        
        # Check system improvement
        if correlations['overall_system_improvement'] < 0.1:
            recommendations.append(
                "📈 LOW IMPROVEMENT: Enhanced system shows minimal improvement over baseline"
            )
        else:
            recommendations.append(
                "✅ POSITIVE IMPROVEMENT: Enhanced system successfully improves visual complexity"
            )
        
        # Check parameter correlation
        if performance['average_parameter_correlation'] < 0.3:
            recommendations.append(
                "🎯 WEAK CORRELATION: Strengthen mapping between consciousness parameters and visuals"
            )
        
        # Check individual parameters
        if correlations['entropy_sensitivity'] > 0.2:
            recommendations.append(
                "🧮 ENTROPY EFFECTIVE: Entropy parameter successfully affects visual complexity"
            )
        
        if correlations['valence_sensitivity'] > 0.2:
            recommendations.append(
                "💭 VALENCE EFFECTIVE: Mood valence successfully affects color variation"
            )
        
        if correlations['drift_sensitivity'] > 0.2:
            recommendations.append(
                "🌊 DRIFT EFFECTIVE: Drift vector successfully creates visual movement"
            )
        
        # Print recommendations
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
        
        if not recommendations:
            print("   ℹ️  No specific recommendations - system performing within expected ranges")
    
    def create_executive_summary(self):
        """Create executive summary report"""
        
        summary_path = self.results_dir / "executive_summary.txt"
        
        with open(summary_path, 'w') as f:
            f.write("DAWN Visual System Validation - Executive Summary\n")
            f.write("=" * 50 + "\n\n")
            
            # Key metrics
            summary_stats = self.results['summary_statistics']
            f.write(f"VALIDATION OVERVIEW:\n")
            f.write(f"• Memories Analyzed: {summary_stats['total_memories_analyzed']}\n")
            f.write(f"• System Improvement: {summary_stats['average_complexity_improvement']:.3f}\n")
            f.write(f"• Parameter Correlation: {summary_stats['visual_system_performance']['average_parameter_correlation']:.3f}\n")
            f.write(f"• Visual Enhancement: {summary_stats['visual_system_performance']['average_visual_difference']:.3f}\n\n")
            
            # Success metrics
            comparisons = self.results['comparison_results']
            successful_improvements = sum(1 for comp in comparisons if comp['complexity_improvement'] > 0)
            success_rate = successful_improvements / len(comparisons)
            
            f.write(f"SUCCESS METRICS:\n")
            f.write(f"• Improvement Success Rate: {success_rate:.1%}\n")
            f.write(f"• System Responsiveness: {summary_stats['visual_system_performance']['system_responsiveness']:.3f}\n\n")
            
            # Parameter effectiveness
            correlations = self.results['correlation_scores']
            f.write(f"PARAMETER EFFECTIVENESS:\n")
            f.write(f"• Entropy Sensitivity: {correlations['entropy_sensitivity']:.3f}\n")
            f.write(f"• Valence Sensitivity: {correlations['valence_sensitivity']:.3f}\n")
            f.write(f"• Depth Sensitivity: {correlations['depth_sensitivity']:.3f}\n")
            f.write(f"• Drift Sensitivity: {correlations['drift_sensitivity']:.3f}\n\n")
            
            # Conclusion
            if summary_stats['average_complexity_improvement'] > 0:
                conclusion = "POSITIVE: Enhanced system successfully improves visual representation"
            else:
                conclusion = "MIXED: Enhanced system shows limited improvement over baseline"
                
            f.write(f"CONCLUSION: {conclusion}\n")
        
        print(f"   ✅ Executive summary saved: {summary_path}")

def main():
    """Run comprehensive results analysis"""
    
    try:
        analyzer = ValidationResultsAnalyzer()
        analyzer.generate_comprehensive_report()
        analyzer.create_executive_summary()
        
        print(f"\n✅ Comprehensive Analysis Complete!")
        print(f"📊 Detailed insights generated for DAWN visual system validation")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("   Please run dawn_visual_system_validation.py first")

if __name__ == "__main__":
    main() 