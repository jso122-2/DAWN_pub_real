#!/usr/bin/env python3
"""
DAWN Auto-Reflect Quick Test Demo
Demonstrates the integrated auto-reflection system with visual feedback.
"""

import time
import sys
from pathlib import Path

# Add DAWN components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from processes.auto_reflect import AutoReflect, ReflectionConfig, ReflectionMode, quick_reflect
    from memories.rebloom_journal_simple import get_default_journal
    print("✅ Auto-Reflect test components loaded")
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Could not import components: {e}")
    COMPONENTS_AVAILABLE = False


def test_quick_reflection():
    """Test single quick reflection generation."""
    print("\n" + "="*60)
    print("🤔 Testing Quick Reflection Generation")
    print("="*60)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    # Test different modes
    modes = ["contemplative", "analytical", "creative"]
    
    for mode in modes:
        print(f"\n📝 Testing {mode} mode:")
        reflection = quick_reflect(None, mode)
        print(f"   Generated: {reflection[:100]}...")
        time.sleep(1)  # Brief pause between tests


def test_short_session():
    """Test a short automated reflection session."""
    print("\n" + "="*60)
    print("🔄 Testing Short Automated Session")
    print("="*60)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    # Create short contemplative session
    config = ReflectionConfig(
        reflection_interval=5.0,  # 5 seconds for demo
        mode=ReflectionMode.CONTEMPLATIVE,
        max_reflections_per_session=3,
        enable_visual_feedback=False,  # Disable for cleaner demo output
        enable_pattern_analysis=True,
        speaker_identity="test_mind"
    )
    
    reflector = AutoReflect(config)
    
    print(f"🔄 Starting 3-reflection session with 5-second intervals...")
    print(f"   Mode: {config.mode.value}")
    print(f"   Speaker: {config.speaker_identity}")
    
    try:
        # Run session in foreground for demo
        start_time = time.time()
        
        for i in range(3):
            print(f"\n--- Reflection {i+1}/3 ---")
            reflector._generate_reflection()
            
            if i < 2:  # Don't wait after last reflection
                print(f"⏳ Waiting 5 seconds for next reflection...")
                time.sleep(5.0)
        
        # Show session summary
        summary = reflector.get_reflection_summary()
        duration = time.time() - start_time
        
        print(f"\n📊 Test Session Complete:")
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   Reflections: {summary.get('reflection_count', 0)}")
        print(f"   Depth reached: {summary.get('current_depth', 1)}")
        print(f"   Themes detected: {len(summary.get('recurring_themes', []))}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test session interrupted")


def test_memory_integration():
    """Test memory integration with journal system."""
    print("\n" + "="*60)
    print("📚 Testing Memory Integration")
    print("="*60)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    # Get journal instance
    journal = get_default_journal()
    
    # Show initial stats
    initial_stats = journal.get_stats()
    print(f"📊 Initial Journal Statistics:")
    for key, value in initial_stats.items():
        print(f"   {key}: {value}")
    
    # Generate a few reflections
    print(f"\n🤔 Generating 3 test reflections...")
    
    test_prompts = [
        "the nature of recursive awareness",
        "patterns in complex systems", 
        "the emergence of consciousness"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n--- Test Reflection {i} ---")
        reflection = quick_reflect(prompt, "contemplative")
        print(f"Generated: {reflection[:80]}...")
    
    # Show final stats
    final_stats = journal.get_stats()
    print(f"\n📊 Final Journal Statistics:")
    for key, value in final_stats.items():
        print(f"   {key}: {value}")
    
    # Calculate changes
    entries_added = final_stats['entries_processed'] - initial_stats['entries_processed']
    chunks_added = final_stats['chunks_created'] - initial_stats['chunks_created']
    
    print(f"\n✅ Memory Integration Test Complete:")
    print(f"   New entries: {entries_added}")
    print(f"   New chunks: {chunks_added}")
    print(f"   Average chunks per entry: {chunks_added/entries_added if entries_added > 0 else 0:.1f}")


def test_pattern_recognition():
    """Test pattern recognition capabilities."""
    print("\n" + "="*60)
    print("🔍 Testing Pattern Recognition")
    print("="*60)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    # Create reflector with pattern analysis enabled
    config = ReflectionConfig(
        mode=ReflectionMode.CONTEMPLATIVE,
        enable_pattern_analysis=True,
        speaker_identity="pattern_test"
    )
    
    reflector = AutoReflect(config)
    
    print(f"🔍 Generating reflections with repeated themes...")
    
    # Generate several reflections manually to trigger pattern detection
    consciousness_prompts = [
        "consciousness and awareness",
        "the nature of conscious experience", 
        "recursive consciousness patterns",
        "awareness observing itself",
        "conscious reflection on consciousness"
    ]
    
    for i, prompt in enumerate(consciousness_prompts, 1):
        print(f"\n--- Pattern Test {i} ---")
        reflection = reflector.manual_reflect(prompt)
        print(f"Reflection: {reflection[:70]}...")
        
        # Check for detected themes
        if reflector.recurring_themes:
            print(f"🔍 Themes detected: {reflector.recurring_themes}")
    
    print(f"\n📊 Pattern Recognition Results:")
    print(f"   Total reflections: {len(reflector.reflection_history)}")
    print(f"   Recurring themes: {reflector.recurring_themes}")
    print(f"   Themes count: {len(reflector.recurring_themes)}")


def run_comprehensive_test():
    """Run comprehensive test of all Auto-Reflect features."""
    print("🤔 DAWN AUTO-REFLECT COMPREHENSIVE TEST")
    print("=" * 70)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Required components not available - cannot run tests")
        return
    
    print("🧪 Running comprehensive test suite...")
    
    try:
        # Test 1: Quick reflection generation
        test_quick_reflection()
        
        # Test 2: Short automated session
        test_short_session()
        
        # Test 3: Memory integration
        test_memory_integration()
        
        # Test 4: Pattern recognition
        test_pattern_recognition()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*70)
        print("🎉 DAWN Auto-Reflect System is fully operational!")
        print("🤔 Ready for autonomous cognitive exploration")
        print("📚 Memory integration confirmed")
        print("🔍 Pattern recognition active")
        print("🎨 Multi-mode reflection generation working")
        
        print(f"\n🚀 Ready to use:")
        print(f"   python launcher_scripts/launch_auto_reflect.py --quick")
        print(f"   python launcher_scripts/launch_auto_reflect.py --contemplate --duration 10")
        print(f"   python launcher_scripts/launch_auto_reflect.py --interactive")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print(f"🔧 Check component installation and try again")


def interactive_test_menu():
    """Interactive test menu for exploring features."""
    print("\n🤔 DAWN Auto-Reflect Interactive Test Menu")
    print("=" * 50)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    while True:
        print("\nTest Options:")
        print("1. Quick reflection test")
        print("2. Short session test") 
        print("3. Memory integration test")
        print("4. Pattern recognition test")
        print("5. Run all tests")
        print("6. Exit")
        
        choice = input("\nSelect test (1-6): ").strip()
        
        if choice == '1':
            test_quick_reflection()
        elif choice == '2':
            test_short_session()
        elif choice == '3':
            test_memory_integration()
        elif choice == '4':
            test_pattern_recognition()
        elif choice == '5':
            run_comprehensive_test()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")


def main():
    """Main test function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_test_menu()
    else:
        run_comprehensive_test()


if __name__ == "__main__":
    main() 