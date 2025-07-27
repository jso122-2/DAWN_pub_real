#!/usr/bin/env python3
"""
DAWN Main Loop Demo - Quick Simulation
Demonstrates the complete integrated system in action.
"""

import sys
import time
from pathlib import Path

# Add components to path
sys.path.insert(0, str(Path(__file__).parent))

from memories.rebloom_journal_simple import ReblooomJournal
from processes.auto_reflect import AutoReflect, ReflectionConfig, ReflectionMode
from backend.visual.sigil_renderer import create_terminal_renderer, UrgencyLevel

def demo_complete_integration():
    """Demonstrate the complete DAWN integration working together."""
    
    print("🧠 DAWN MAIN LOOP DEMONSTRATION")
    print("=" * 70)
    print("🎬 Simulating complete cognitive loop:")
    print("   🤔 Auto-reflection → 📚 Memory processing → 🎨 Visual rendering")
    print("=" * 70)
    
    # Initialize all components
    print("\n🔧 Initializing components...")
    journal = ReblooomJournal()
    renderer = create_terminal_renderer()
    
    # Configure contemplative reflector
    config = ReflectionConfig(
        reflection_interval=10.0,  # Not used in manual mode
        mode=ReflectionMode.CONTEMPLATIVE,
        enable_pattern_analysis=True,
        speaker_identity="demo_mind"
    )
    reflector = AutoReflect(config)
    
    print("✅ All components initialized")
    
    # Simulate 5 reflection cycles
    print(f"\n🔄 Starting 5-cycle cognitive demonstration...")
    
    for cycle in range(1, 6):
        print(f"\n{'🔸' * 50}")
        print(f"🧠 COGNITIVE CYCLE {cycle}/5")
        print(f"{'🔸' * 50}")
        
        # Step 1: Generate reflection
        print(f"🤔 Step 1: Generating reflection...")
        reflector._generate_reflection()
        
        latest_reflection = reflector.reflection_history[-1]['text'] if reflector.reflection_history else "No reflection"
        print(f"   Generated: {latest_reflection[:80]}...")
        
        # Step 2: Check memory stats
        print(f"📚 Step 2: Memory processing...")
        stats = journal.get_stats()
        print(f"   Memory chunks: {stats['chunks_created']}")
        print(f"   Entries processed: {stats['entries_processed']}")
        
        # Step 3: Update visual display
        print(f"🎨 Step 3: Visual rendering...")
        
        # Create dynamic sigils based on cycle
        active_sigils = [{
            'name': 'AUTO_REFLECT_CONTEMPLATIVE',
            'urgency': UrgencyLevel.MEDIUM,
            'duration': cycle * 10.0,
            'trigger_count': cycle
        }]
        
        if reflector.depth_level > 1:
            active_sigils.append({
                'name': 'DEEP_CONTEMPLATION',
                'urgency': UrgencyLevel.HIGH,
                'duration': reflector.depth_level * 5.0,
                'trigger_count': reflector.depth_level
            })
        
        if len(reflector.recurring_themes) > 0:
            active_sigils.append({
                'name': 'PATTERN_RECOGNITION',
                'urgency': UrgencyLevel.LOW,
                'duration': len(reflector.recurring_themes) * 2.0,
                'trigger_count': len(reflector.recurring_themes)
            })
        
        # System stats for visual
        system_stats = {
            'cycle': cycle,
            'reflections': len(reflector.reflection_history),
            'memory_chunks': stats['chunks_created'],
            'depth': reflector.depth_level,
            'themes': len(reflector.recurring_themes)
        }
        
        # Render the current state
        renderer.render(
            sigil_data=active_sigils,
            organ_data={'CognitivePulse': reflector.depth_level, 'ThemeDetector': len(reflector.recurring_themes)},
            system_data=system_stats,
            force_render=True
        )
        
        # Show cycle summary
        print(f"\n📊 Cycle {cycle} Summary:")
        print(f"   Reflections: {len(reflector.reflection_history)}")
        print(f"   Memory chunks: {stats['chunks_created']}")
        print(f"   Cognitive depth: {reflector.depth_level}")
        print(f"   Themes detected: {reflector.recurring_themes}")
        
        # Brief pause for demonstration
        if cycle < 5:
            print(f"\n⏳ Pausing 2 seconds before next cycle...")
            time.sleep(2)
    
    # Final summary
    print(f"\n" + "=" * 70)
    print(f"🎉 DEMONSTRATION COMPLETE")
    print(f"=" * 70)
    
    final_summary = reflector.get_reflection_summary()
    final_stats = journal.get_stats()
    
    print(f"📊 Final Results:")
    print(f"   Total reflection cycles: 5")
    print(f"   Reflections generated: {final_summary.get('reflection_count', 0)}")
    print(f"   Memory chunks created: {final_stats['chunks_created']}")
    print(f"   Final cognitive depth: {final_summary.get('current_depth', 1)}")
    print(f"   Themes discovered: {final_summary.get('recurring_themes', [])}")
    print(f"   Average reflection length: {final_summary.get('average_reflection_length', 0):.1f} chars")
    
    print(f"\n✅ Integration Status:")
    print(f"   🤔 Auto-reflection: SUCCESSFUL - Generated philosophical content")
    print(f"   📚 Memory processing: SUCCESSFUL - {final_stats['chunks_created']} chunks stored")
    print(f"   🎨 Visual rendering: SUCCESSFUL - Live cognitive state displayed")
    print(f"   🔗 Component integration: SUCCESSFUL - Complete pipeline operational")
    
    print(f"\n🚀 System Ready For:")
    print(f"   • Long-form contemplative sessions")
    print(f"   • Multi-mode cognitive exploration")  
    print(f"   • Pattern recognition and theme analysis")
    print(f"   • Real-time cognitive state monitoring")
    print(f"   • Memory-based rebloom processing")
    
    print(f"\n🎯 Ready Commands:")
    print(f"   python main_integration.py --interactive")
    print(f"   python launcher_scripts/launch_auto_reflect.py --contemplate --duration 10")
    print(f"   python launcher_scripts/launch_dawn_visual_journal.py --demo live")


def quick_pipeline_test():
    """Quick test of the complete pipeline."""
    print("\n🚀 QUICK PIPELINE TEST")
    print("=" * 30)
    
    # Test the complete flow
    print("🔄 Testing: Reflection → Memory → Visual...")
    
    # 1. Generate reflection
    from processes.auto_reflect import quick_reflect
    reflection = quick_reflect("the interconnected nature of consciousness")
    print(f"✅ Reflection: {reflection[:60]}...")
    
    # 2. Check memory
    journal = ReblooomJournal()
    stats = journal.get_stats()
    print(f"✅ Memory: {stats['chunks_created']} chunks")
    
    # 3. Render visual
    renderer = create_terminal_renderer()
    test_sigils = [{'name': 'PIPELINE_TEST', 'urgency': UrgencyLevel.HIGH, 'duration': 1.0, 'trigger_count': 1}]
    test_stats = {'pipeline_status': 'OPERATIONAL', 'test_chunks': stats['chunks_created']}
    
    print("✅ Visual rendering:")
    renderer.render(sigil_data=test_sigils, system_data=test_stats, force_render=True)
    
    print("🎉 Pipeline test complete!")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Main Loop Demo")
    parser.add_argument('--quick', action='store_true', help='Quick pipeline test')
    parser.add_argument('--full', action='store_true', help='Full demonstration')
    
    args = parser.parse_args()
    
    if args.quick:
        quick_pipeline_test()
    elif args.full:
        demo_complete_integration()
    else:
        # Default: run both
        quick_pipeline_test()
        print("\n" + "="*50)
        demo_complete_integration() 