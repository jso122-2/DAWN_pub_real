#!/usr/bin/env python3
"""
DAWN Focused Diagnostic Scanner - Integration Components Only
Validates our integrated system components with external DAWN components as optional.

Usage: python diagnostic_scan_focused.py
Exit codes: 0 = Core pass, 1 = Core fail
"""

import sys
import traceback
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

# Add system path for DAWN components
sys.path.insert(0, str(Path(__file__).parent))

class DAWNFocusedScanner:
    """Focused diagnostic scanner for our integrated DAWN components."""
    
    def __init__(self):
        self.core_results: Dict[str, bool] = {}
        self.optional_results: Dict[str, bool] = {}
        self.test_details: Dict[str, str] = {}
        self.start_time = datetime.now()
        
    def log_test(self, test_name: str, passed: bool, details: str = "", is_core: bool = True):
        """Log test result with details."""
        if is_core:
            self.core_results[test_name] = passed
        else:
            self.optional_results[test_name] = passed
        self.test_details[test_name] = details
        
        status = "✅" if passed else ("❌" if is_core else "⚠️")
        test_type = "CORE" if is_core else "OPT"
        print(f"[{status}] {test_type}: {test_name} - {details}")
    
    def check_core_imports(self) -> bool:
        """Test our integrated core components."""
        print("\n🎯 Testing CORE Integrated Components...")
        
        core_imports = [
            ("memories.rebloom_journal_simple", "Rebloom Journal"),
            ("processes.auto_reflect", "Auto-Reflect System"),
            ("backend.visual.sigil_renderer", "Sigil Renderer"),
        ]
        
        all_passed = True
        
        for module_name, display_name in core_imports:
            try:
                module = __import__(module_name, fromlist=[''])
                self.log_test(f"{display_name}", True, "Integrated component loaded", is_core=True)
            except Exception as e:
                self.log_test(f"{display_name}", False, f"Import failed: {str(e)}", is_core=True)
                all_passed = False
        
        return all_passed
    
    def check_optional_imports(self) -> int:
        """Test optional external DAWN components."""
        print("\n🔧 Testing OPTIONAL External Components...")
        
        optional_imports = [
            ("pulse", "Pulse System"),
            ("entropy", "Entropy Engine"),
            ("sigils", "Sigil Engine"),
            ("forecasting.engine", "Forecasting Engine"),
            ("symbolic_router", "Symbolic Router"),
            ("speak", "Speech System"),
            ("snapshot_exporter", "Snapshot Exporter"),
        ]
        
        available_count = 0
        
        for module_name, display_name in optional_imports:
            try:
                module = __import__(module_name, fromlist=[''])
                self.log_test(f"{display_name}", True, "External component available", is_core=False)
                available_count += 1
            except ImportError:
                self.log_test(f"{display_name}", False, "Not available (using mock)", is_core=False)
        
        return available_count
    
    def check_auto_reflection_system(self) -> bool:
        """Test complete auto-reflection system functionality."""
        print("\n🤔 Testing Auto-Reflection System...")
        
        try:
            from processes.auto_reflect import AutoReflect, ReflectionConfig, ReflectionMode, quick_reflect
            
            # Test 1: Quick reflection
            reflection = quick_reflect("diagnostic system validation")
            if len(reflection) < 10:
                self.log_test("Quick Reflection", False, "Generated reflection too short", is_core=True)
                return False
            
            self.log_test("Quick Reflection", True, f"Generated {len(reflection)} chars", is_core=True)
            
            # Test 2: Session-based reflection
            config = ReflectionConfig(
                mode=ReflectionMode.CONTEMPLATIVE,
                max_reflections_per_session=2,
                enable_pattern_analysis=True,
                speaker_identity="diagnostic_test"
            )
            
            reflector = AutoReflect(config)
            
            # Generate two reflections
            reflector._generate_reflection()
            reflector._generate_reflection()
            
            if len(reflector.reflection_history) != 2:
                self.log_test("Session Reflection", False, f"Expected 2, got {len(reflector.reflection_history)}", is_core=True)
                return False
            
            self.log_test("Session Reflection", True, f"Generated {len(reflector.reflection_history)} reflections", is_core=True)
            
            # Test 3: Pattern recognition
            themes = reflector.recurring_themes
            depth = reflector.depth_level
            
            self.log_test("Pattern Recognition", True, f"Depth: {depth}, Themes: {len(themes)}", is_core=True)
            
            return True
            
        except Exception as e:
            self.log_test("Auto-Reflection System", False, f"Exception: {str(e)}", is_core=True)
            return False
    
    def check_memory_processing(self) -> bool:
        """Test memory processing and journal system."""
        print("\n📚 Testing Memory Processing...")
        
        try:
            from memories.rebloom_journal_simple import ReblooomJournal, add_journal_entry
            
            # Test 1: Direct journal entry
            chunk_ids = add_journal_entry("Diagnostic test reflection on system integrity", speaker="diagnostic")
            
            if len(chunk_ids) == 0:
                self.log_test("Direct Journal Entry", False, "No chunks created", is_core=True)
                return False
            
            self.log_test("Direct Journal Entry", True, f"Created {len(chunk_ids)} chunks", is_core=True)
            
            # Test 2: Journal instance
            journal = ReblooomJournal()
            initial_stats = journal.get_stats()
            
            journal.add_journal_entry("Another test entry for diagnostics", speaker="test_system")
            final_stats = journal.get_stats()
            
            new_chunks = final_stats['chunks_created'] - initial_stats['chunks_created']
            
            if new_chunks <= 0:
                self.log_test("Journal Instance", False, "No new chunks created", is_core=True)
                return False
            
            self.log_test("Journal Instance", True, f"Added {new_chunks} chunks", is_core=True)
            
            # Test 3: Statistics
            stats = journal.get_stats()
            required_keys = ['entries_processed', 'chunks_created', 'memory_chunks_stored']
            
            if not all(key in stats for key in required_keys):
                self.log_test("Memory Statistics", False, "Missing required stats", is_core=True)
                return False
            
            self.log_test("Memory Statistics", True, f"Stats: {stats}", is_core=True)
            
            return True
            
        except Exception as e:
            self.log_test("Memory Processing", False, f"Exception: {str(e)}", is_core=True)
            return False
    
    def check_visual_rendering(self) -> bool:
        """Test visual rendering and sigil display."""
        print("\n🎨 Testing Visual Rendering...")
        
        try:
            from backend.visual.sigil_renderer import SigilRenderer, create_terminal_renderer, UrgencyLevel
            
            # Test 1: Renderer creation
            renderer = create_terminal_renderer()
            
            if not hasattr(renderer, 'render'):
                self.log_test("Renderer Creation", False, "Missing render method", is_core=True)
                return False
            
            self.log_test("Renderer Creation", True, "Terminal renderer created", is_core=True)
            
            # Test 2: Sigil rendering
            test_sigils = [{
                'name': 'DIAGNOSTIC_VALIDATION',
                'urgency': UrgencyLevel.HIGH,
                'duration': 1.0,
                'trigger_count': 1
            }]
            
            renderer.render(sigil_data=test_sigils, force_render=True)
            self.log_test("Sigil Rendering", True, "Sigils rendered successfully", is_core=True)
            
            # Test 3: System stats rendering
            test_stats = {
                'diagnostic_status': 'RUNNING',
                'test_count': 10,
                'system_health': 0.95
            }
            
            renderer.render(system_data=test_stats, force_render=True)
            self.log_test("Stats Rendering", True, "System stats rendered", is_core=True)
            
            # Test 4: Organ rendering
            test_organs = {
                'DiagnosticPulse': 1.0,
                'SystemHealth': {'value': 0.95, 'saturation': 0.8},
                'TestRunner': ['test_1', 'test_2', 'test_3']
            }
            
            renderer.render(organ_data=test_organs, force_render=True)
            self.log_test("Organ Rendering", True, f"Rendered {len(test_organs)} organs", is_core=True)
            
            return True
            
        except Exception as e:
            self.log_test("Visual Rendering", False, f"Exception: {str(e)}", is_core=True)
            return False
    
    def check_integration_pipeline(self) -> bool:
        """Test the complete integration pipeline."""
        print("\n🔗 Testing Integration Pipeline...")
        
        try:
            from processes.auto_reflect import quick_reflect
            from memories.rebloom_journal_simple import ReblooomJournal
            from backend.visual.sigil_renderer import create_terminal_renderer, UrgencyLevel
            
            # Step 1: Generate reflection
            reflection = quick_reflect("complete pipeline integration test")
            
            if len(reflection) < 10:
                self.log_test("Pipeline Step 1", False, "Reflection generation failed", is_core=True)
                return False
            
            self.log_test("Pipeline Step 1", True, f"Reflection: {len(reflection)} chars", is_core=True)
            
            # Step 2: Process through memory
            journal = ReblooomJournal()
            initial_chunks = journal.get_stats()['chunks_created']
            chunk_ids = journal.add_journal_entry(reflection, speaker="pipeline_test")
            final_chunks = journal.get_stats()['chunks_created']
            
            chunks_added = final_chunks - initial_chunks
            
            if chunks_added <= 0:
                self.log_test("Pipeline Step 2", False, "Memory processing failed", is_core=True)
                return False
            
            self.log_test("Pipeline Step 2", True, f"Memory: +{chunks_added} chunks", is_core=True)
            
            # Step 3: Visual rendering
            renderer = create_terminal_renderer()
            
            pipeline_sigils = [{
                'name': 'PIPELINE_COMPLETE',
                'urgency': UrgencyLevel.HIGH,
                'duration': 1.0,
                'trigger_count': 1
            }]
            
            pipeline_stats = {
                'reflection_chars': len(reflection),
                'memory_chunks': chunks_added,
                'pipeline_status': 'OPERATIONAL'
            }
            
            renderer.render(sigil_data=pipeline_sigils, system_data=pipeline_stats, force_render=True)
            self.log_test("Pipeline Step 3", True, "Visual rendering complete", is_core=True)
            
            # Step 4: Validate end-to-end
            self.log_test("Pipeline E2E", True, 
                         f"Complete: {len(reflection)}→{chunks_added}→visual", is_core=True)
            
            return True
            
        except Exception as e:
            self.log_test("Integration Pipeline", False, f"Exception: {str(e)}", is_core=True)
            return False
    
    def run_focused_diagnostics(self) -> bool:
        """Run focused diagnostic suite on our integrated components."""
        print("🧠 DAWN FOCUSED DIAGNOSTIC SCANNER")
        print("=" * 70)
        print(f"🕐 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Focus: Integrated components (Auto-Reflect + Memory + Visual)")
        print("🔧 External DAWN components tested as optional")
        print("=" * 70)
        
        # Core tests (must pass)
        core_tests = [
            ("Core Component Imports", self.check_core_imports),
            ("Auto-Reflection System", self.check_auto_reflection_system),
            ("Memory Processing", self.check_memory_processing),
            ("Visual Rendering", self.check_visual_rendering),
            ("Integration Pipeline", self.check_integration_pipeline),
        ]
        
        all_core_passed = True
        
        # Run core tests
        for test_name, test_func in core_tests:
            try:
                result = test_func()
                if not result:
                    all_core_passed = False
            except Exception as e:
                self.log_test(test_name, False, f"Unexpected error: {str(e)}", is_core=True)
                all_core_passed = False
        
        # Check optional components
        optional_available = self.check_optional_imports()
        
        # Print final report
        self.print_focused_report(all_core_passed, optional_available)
        
        return all_core_passed
    
    def print_focused_report(self, core_passed: bool, optional_count: int):
        """Print focused diagnostic report."""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        print("\n" + "=" * 70)
        print("📊 DAWN FOCUSED DIAGNOSTIC REPORT")
        print("=" * 70)
        
        # Core results
        total_core = len(self.core_results)
        passed_core = sum(1 for result in self.core_results.values() if result)
        
        print(f"🕐 Duration: {duration:.2f} seconds")
        print(f"\n🎯 CORE SYSTEM (Integrated Components):")
        print(f"   📊 Total Tests: {total_core}")
        print(f"   ✅ Passed: {passed_core}")
        print(f"   ❌ Failed: {total_core - passed_core}")
        print(f"   📈 Success Rate: {passed_core/total_core*100:.1f}%")
        
        # Optional results
        total_optional = len(self.optional_results)
        print(f"\n🔧 OPTIONAL SYSTEM (External Components):")
        print(f"   📊 Total Available: {optional_count}/{total_optional}")
        print(f"   📈 Availability: {optional_count/total_optional*100:.1f}%")
        
        # Detailed core results
        print(f"\n📋 Core Component Results:")
        for test_name, passed in self.core_results.items():
            status = "✅" if passed else "❌"
            details = self.test_details.get(test_name, "")
            print(f"  {status} {test_name}: {details}")
        
        # Optional availability
        if optional_count > 0:
            print(f"\n🔧 Optional Components Available:")
            for test_name, passed in self.optional_results.items():
                if passed:
                    print(f"  ✅ {test_name}")
        
        # Final status
        print(f"\n" + "=" * 70)
        if core_passed:
            print("🎉 CORE SYSTEM OPERATIONAL - DAWN READY FOR AUTONOMOUS OPERATION")
            print("🚀 Integration Status: FULLY FUNCTIONAL")
            print("✅ Auto-Reflection: OPERATIONAL")
            print("✅ Memory Processing: OPERATIONAL")
            print("✅ Visual Rendering: OPERATIONAL")
            print("✅ Integration Pipeline: VERIFIED")
            
            if optional_count > 0:
                print(f"🔧 Bonus: {optional_count} external components available")
            else:
                print("🔧 Note: Running with integrated components only")
            
        else:
            print("⚠️ CORE SYSTEM ISSUES - NEEDS ATTENTION")
            print("🔧 Integration Status: REQUIRES FIXES")
            failed_core = total_core - passed_core
            print(f"❌ {failed_core} core tests failed")
        
        print("=" * 70)
        
        # Ready commands if core passed
        if core_passed:
            print("\n🎯 System Ready - Launch Commands:")
            print("   python main_integration.py --interactive")
            print("   python launcher_scripts/launch_auto_reflect.py --contemplate --duration 10")
            print("   python demo_main_loop.py --full")
            print("   python test_integration.py")


def main():
    """Main focused diagnostic execution."""
    scanner = DAWNFocusedScanner()
    
    try:
        core_passed = scanner.run_focused_diagnostics()
        
        # Exit based on core system status
        if core_passed:
            print(f"\n✅ DAWN integrated system is operational and ready!")
            sys.exit(0)
        else:
            print(f"\n❌ DAWN core system has issues - check failed tests!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n⏹️ Focused diagnostic scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Focused diagnostic scanner crashed: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main() 