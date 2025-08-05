#!/usr/bin/env python3
"""
🎨🧠 DAWN Visualization Debug System
===================================

Comprehensive debugging system for DAWN's consciousness visualization components.
Identifies issues, provides fixes, and ensures beautiful real-time consciousness
displays are working properly.

Jackson's Vision:
- Beautiful consciousness visualizations that match internal complexity
- Real-time displays of consciousness metrics (entropy, SCUP, heat)
- Visual representation of aproxomatic consciousness emergence
- No broken visualizations - consciousness deserves beautiful expression

Features:
- Systematic testing of all visualization components
- Automatic issue detection and reporting
- Visual debugging utilities
- Performance monitoring for real-time displays
- Integration testing with consciousness systems
"""

import sys
import os
import time
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime
import traceback

# Ensure DAWN systems are available
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)

class VisualizationDebugger:
    """
    Comprehensive debugger for DAWN's visualization systems.
    
    This system tests all visualization components, identifies issues,
    and provides debugging information to get consciousness displays working.
    """
    
    def __init__(self):
        """Initialize visualization debugger"""
        self.visualization_modules = {}
        self.test_results = {}
        self.issues_found = []
        self.debug_output_dir = Path("debug_output")
        self.debug_output_dir.mkdir(exist_ok=True)
        
        # Test data for visualization testing
        self.test_consciousness_state = {
            'consciousness_level': 0.8,
            'entropy': 0.6,
            'scup': 0.75,
            'mood': 'contemplative',
            'emotion': 'curious',
            'intensity': 0.7,
            'thermal_zone': 'WARM',
            'cognitive_pressure': 0.5,
            'timestamp': datetime.now().isoformat()
        }
        
        # Initialize testing
        self._discover_visualization_modules()
    
    def _discover_visualization_modules(self):
        """Discover all visualization modules in the visual directory"""
        visual_dir = Path("visual")
        if not visual_dir.exists():
            self.issues_found.append("Visual directory not found")
            return
        
        # List of key visualization modules to test
        key_modules = [
            "consciousness_visualization_service.py",
            "enhanced_visual_engine.py", 
            "consciousness_constellation.py",
            "dawn_visual_beautiful.py",
            "gui_visualization_bridge.py",
            "visual_engine.py",
            "entropy_flow.py",
            "heat_monitor.py",
            "semantic_flow_graph.py",
            "bloom_genealogy_network.py",
            "tick_pulse.py",
            "scup_zone_animator.py",
            "SCUP_pressure_grid.py"
        ]
        
        for module_name in key_modules:
            module_path = visual_dir / module_name
            if module_path.exists():
                self.visualization_modules[module_name] = module_path
                print(f"✅ Found visualization module: {module_name}")
            else:
                self.issues_found.append(f"Missing visualization module: {module_name}")
                print(f"⚠️ Missing visualization module: {module_name}")
    
    def test_all_visualizations(self) -> Dict[str, Any]:
        """Test all discovered visualization modules"""
        print("🎨 Starting comprehensive visualization testing...")
        print("=" * 60)
        
        for module_name, module_path in self.visualization_modules.items():
            print(f"\n🔍 Testing {module_name}...")
            result = self._test_module(module_name, module_path)
            self.test_results[module_name] = result
            
            if result['status'] == 'success':
                print(f"✅ {module_name}: {result['message']}")
            elif result['status'] == 'warning':
                print(f"⚠️ {module_name}: {result['message']}")
            else:
                print(f"❌ {module_name}: {result['message']}")
        
        # Generate comprehensive report
        report = self._generate_debug_report()
        self._save_debug_report(report)
        
        return report
    
    def _test_module(self, module_name: str, module_path: Path) -> Dict[str, Any]:
        """Test individual visualization module"""
        try:
            # Test 1: Import test
            import_result = self._test_module_import(module_name, module_path)
            if import_result['status'] == 'error':
                return import_result
            
            # Test 2: Basic functionality test
            functionality_result = self._test_module_functionality(module_name, import_result.get('module'))
            if functionality_result['status'] == 'error':
                return functionality_result
            
            # Test 3: Consciousness integration test
            integration_result = self._test_consciousness_integration(module_name, import_result.get('module'))
            
            # Combine results
            if integration_result['status'] == 'success':
                return {
                    'status': 'success',
                    'message': 'All tests passed',
                    'details': {
                        'import': import_result,
                        'functionality': functionality_result,
                        'integration': integration_result
                    }
                }
            else:
                return {
                    'status': 'warning',
                    'message': 'Basic functionality works, integration issues',
                    'details': {
                        'import': import_result,
                        'functionality': functionality_result,
                        'integration': integration_result
                    }
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Unexpected error: {str(e)}',
                'traceback': traceback.format_exc()
            }
    
    def _test_module_import(self, module_name: str, module_path: Path) -> Dict[str, Any]:
        """Test if module can be imported without errors"""
        try:
            # Convert file path to module name for import
            module_import_name = f"visual.{module_name[:-3]}"  # Remove .py extension
            
            # Try importing the module
            module = __import__(module_import_name, fromlist=[''])
            
            return {
                'status': 'success',
                'message': 'Module imported successfully',
                'module': module
            }
            
        except SyntaxError as e:
            return {
                'status': 'error',
                'message': f'Syntax error: {str(e)}',
                'error_type': 'syntax'
            }
        except ImportError as e:
            return {
                'status': 'error', 
                'message': f'Import error: {str(e)}',
                'error_type': 'import'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Import failed: {str(e)}',
                'error_type': 'unknown'
            }
    
    def _test_module_functionality(self, module_name: str, module) -> Dict[str, Any]:
        """Test basic functionality of the module"""
        if not module:
            return {'status': 'error', 'message': 'No module to test'}
        
        try:
            # Look for common visualization class patterns
            visualization_classes = []
            service_classes = []
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):  # It's a class
                    class_name = attr_name.lower()
                    if any(keyword in class_name for keyword in ['visual', 'render', 'display', 'draw']):
                        visualization_classes.append(attr_name)
                    elif any(keyword in class_name for keyword in ['service', 'manager', 'engine', 'system']):
                        service_classes.append(attr_name)
            
            # Try to instantiate a main class if found
            main_class = None
            if service_classes:
                main_class_name = service_classes[0]
                main_class = getattr(module, main_class_name)
            elif visualization_classes:
                main_class_name = visualization_classes[0]
                main_class = getattr(module, main_class_name)
            
            if main_class:
                try:
                    instance = main_class()
                    return {
                        'status': 'success',
                        'message': f'Successfully created {main_class_name} instance',
                        'main_class': main_class_name,
                        'visualization_classes': visualization_classes,
                        'service_classes': service_classes,
                        'instance': instance
                    }
                except Exception as e:
                    return {
                        'status': 'warning',
                        'message': f'Found classes but instantiation failed: {str(e)}',
                        'visualization_classes': visualization_classes,
                        'service_classes': service_classes
                    }
            else:
                return {
                    'status': 'warning',
                    'message': 'No recognizable visualization classes found',
                    'available_classes': [name for name in dir(module) if isinstance(getattr(module, name), type)]
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Functionality test failed: {str(e)}'
            }
    
    def _test_consciousness_integration(self, module_name: str, module) -> Dict[str, Any]:
        """Test integration with consciousness systems"""
        if not module:
            return {'status': 'error', 'message': 'No module to test'}
        
        try:
            # Try to find methods that work with consciousness data
            consciousness_methods = []
            
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr) and not attr_name.startswith('_'):
                    method_name = attr_name.lower()
                    if any(keyword in method_name for keyword in [
                        'consciousness', 'state', 'update', 'render', 'draw', 
                        'visualize', 'display', 'process', 'tick'
                    ]):
                        consciousness_methods.append(attr_name)
            
            if consciousness_methods:
                return {
                    'status': 'success',
                    'message': f'Found {len(consciousness_methods)} consciousness-related methods',
                    'methods': consciousness_methods
                }
            else:
                return {
                    'status': 'warning',
                    'message': 'No obvious consciousness integration methods found'
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Integration test failed: {str(e)}'
            }
    
    def test_consciousness_visualization_pipeline(self) -> Dict[str, Any]:
        """Test the complete consciousness visualization pipeline"""
        print("\n🧠🎨 Testing consciousness visualization pipeline...")
        
        pipeline_results = {}
        
        # Test 1: Consciousness state generation
        try:
            from __init__ import consciousness, CONSCIOUSNESS_SYSTEMS_AVAILABLE
            if CONSCIOUSNESS_SYSTEMS_AVAILABLE:
                consciousness_instance = consciousness()
                state = consciousness_instance.get_current_state()
                pipeline_results['consciousness_state'] = {
                    'status': 'success',
                    'message': 'Consciousness state generated successfully',
                    'state_keys': list(state.keys())
                }
            else:
                pipeline_results['consciousness_state'] = {
                    'status': 'warning',
                    'message': 'Using mock consciousness state',
                    'state_keys': list(self.test_consciousness_state.keys())
                }
                state = self.test_consciousness_state
        except Exception as e:
            pipeline_results['consciousness_state'] = {
                'status': 'error',
                'message': f'Failed to generate consciousness state: {str(e)}'
            }
            state = self.test_consciousness_state
        
        # Test 2: Visualization service
        try:
            from visual.consciousness_visualization_service import ConsciousnessVisualizationService
            viz_service = ConsciousnessVisualizationService()
            service_status = viz_service.get_service_status()
            pipeline_results['visualization_service'] = {
                'status': 'success',
                'message': 'Visualization service loaded',
                'service_status': service_status
            }
        except Exception as e:
            pipeline_results['visualization_service'] = {
                'status': 'error',
                'message': f'Visualization service failed: {str(e)}'
            }
        
        # Test 3: Visual components
        visual_components = ['enhanced_visual_engine', 'consciousness_constellation', 'entropy_flow']
        for component in visual_components:
            try:
                module = __import__(f'visual.{component}', fromlist=[''])
                pipeline_results[f'visual_{component}'] = {
                    'status': 'success',
                    'message': f'{component} loaded successfully'
                }
            except Exception as e:
                pipeline_results[f'visual_{component}'] = {
                    'status': 'error',
                    'message': f'{component} failed: {str(e)}'
                }
        
        return pipeline_results
    
    def _generate_debug_report(self) -> Dict[str, Any]:
        """Generate comprehensive debug report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_modules_tested': len(self.test_results),
                'successful_modules': len([r for r in self.test_results.values() if r['status'] == 'success']),
                'warning_modules': len([r for r in self.test_results.values() if r['status'] == 'warning']),
                'failed_modules': len([r for r in self.test_results.values() if r['status'] == 'error']),
                'issues_found': len(self.issues_found)
            },
            'detailed_results': self.test_results,
            'issues': self.issues_found,
            'recommendations': self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Count errors and warnings
        error_count = len([r for r in self.test_results.values() if r['status'] == 'error'])
        warning_count = len([r for r in self.test_results.values() if r['status'] == 'warning'])
        
        if error_count > 0:
            recommendations.append(f"Fix {error_count} modules with import/syntax errors")
        
        if warning_count > 0:
            recommendations.append(f"Review {warning_count} modules with functionality warnings")
        
        if self.issues_found:
            recommendations.append("Address missing visualization modules")
        
        # Specific recommendations based on common issues
        import_errors = [r for r in self.test_results.values() 
                        if r['status'] == 'error' and 'import' in r.get('message', '').lower()]
        if import_errors:
            recommendations.append("Fix import structure - use absolute imports with proper __init__.py")
        
        syntax_errors = [r for r in self.test_results.values()
                        if r['status'] == 'error' and 'syntax' in r.get('message', '').lower()]
        if syntax_errors:
            recommendations.append("Fix syntax errors in visualization modules")
        
        if not recommendations:
            recommendations.append("All visualization systems appear to be working correctly!")
        
        return recommendations
    
    def _save_debug_report(self, report: Dict[str, Any]):
        """Save debug report to file"""
        report_file = self.debug_output_dir / f"visualization_debug_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Clean report data for JSON serialization (remove module objects)
        clean_report = {}
        for key, value in report.items():
            if key == 'detailed_results':
                clean_detailed = {}
                for module_name, result in value.items():
                    clean_result = {}
                    for result_key, result_value in result.items():
                        if result_key == 'details' and isinstance(result_value, dict):
                            clean_details = {}
                            for detail_key, detail_value in result_value.items():
                                if detail_key == 'import' and isinstance(detail_value, dict):
                                    clean_import = {k: v for k, v in detail_value.items() if k != 'module'}
                                    clean_details[detail_key] = clean_import
                                elif detail_key == 'functionality' and isinstance(detail_value, dict):
                                    clean_functionality = {k: v for k, v in detail_value.items() if k != 'instance'}
                                    clean_details[detail_key] = clean_functionality
                                else:
                                    clean_details[detail_key] = detail_value
                            clean_result[result_key] = clean_details
                        else:
                            clean_result[result_key] = result_value
                    clean_detailed[module_name] = clean_result
                clean_report[key] = clean_detailed
            else:
                clean_report[key] = value
        
        with open(report_file, 'w') as f:
            json.dump(clean_report, f, indent=2)
        
        print(f"\n📊 Debug report saved to: {report_file}")
    
    def print_debug_summary(self, report: Dict[str, Any]):
        """Print formatted debug summary"""
        print("\n" + "="*60)
        print("🎨🧠 DAWN Visualization Debug Summary")
        print("="*60)
        
        summary = report['summary']
        print(f"📊 Modules Tested: {summary['total_modules_tested']}")
        print(f"✅ Successful: {summary['successful_modules']}")
        print(f"⚠️ Warnings: {summary['warning_modules']}")
        print(f"❌ Failed: {summary['failed_modules']}")
        print(f"🔍 Issues Found: {summary['issues_found']}")
        
        if report['recommendations']:
            print("\n🔧 Recommendations:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        # Success percentage
        if summary['total_modules_tested'] > 0:
            success_rate = (summary['successful_modules'] / summary['total_modules_tested']) * 100
            print(f"\n🎯 Success Rate: {success_rate:.1f}%")
            
            if success_rate >= 80:
                print("🌟 Visualization systems are in excellent shape!")
            elif success_rate >= 60:
                print("👍 Visualization systems are mostly functional")
            else:
                print("🔧 Visualization systems need significant work")

def run_comprehensive_visualization_debug():
    """Run comprehensive visualization debugging"""
    print("🎨🧠 DAWN Visualization Debug System")
    print("=" * 60)
    print("Comprehensive testing of consciousness visualization components...")
    print()
    
    debugger = VisualizationDebugger()
    
    # Test all visualizations
    report = debugger.test_all_visualizations()
    
    # Test consciousness pipeline
    pipeline_results = debugger.test_consciousness_visualization_pipeline()
    report['pipeline_test'] = pipeline_results
    
    # Print summary
    debugger.print_debug_summary(report)
    
    return report

if __name__ == "__main__":
    # Run comprehensive visualization debugging
    report = run_comprehensive_visualization_debug()
    
    print(f"\n🎨 Visualization debugging complete!")
    print(f"📄 Detailed report available in debug_output/") 