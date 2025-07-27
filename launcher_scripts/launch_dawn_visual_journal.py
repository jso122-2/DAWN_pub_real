#!/usr/bin/env python3
"""
DAWN Visual Journal Launcher
Easy-to-use launcher for the integrated visual rendering and journal memory systems.
"""

import sys
import os
import argparse
from pathlib import Path

# Add DAWN components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from backend.visual.dawn_renderer_integration import (
        create_dawn_terminal_monitor, 
        create_dawn_minimal_monitor,
        quick_dawn_render
    )
    from memories.journal_memory_adapter import (
        create_enhanced_journal_adapter,
        quick_enhanced_entry
    )
    from examples.dawn_visual_journal_demo import DAWNVisualJournalDemo
    print("✅ DAWN Visual Journal components loaded successfully")
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Could not import DAWN components: {e}")
    print("🔧 Please ensure all integration files are properly installed")
    COMPONENTS_AVAILABLE = False


def launch_visual_monitor(mode='full', live=False):
    """Launch the visual monitor for DAWN symbolic state."""
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    print(f"🎨 Launching DAWN Visual Monitor ({mode} mode)")
    
    if mode == 'minimal':
        monitor = create_dawn_minimal_monitor()
    else:
        monitor = create_dawn_terminal_monitor()
    
    if live:
        print("🔴 Starting live monitoring (Press Ctrl+C to stop)")
        try:
            monitor.start_live_monitor(interval=2.0)
        except KeyboardInterrupt:
            print("⏹️ Monitor stopped")
    else:
        print("📸 Single render:")
        monitor.render_current_state(force=True)


def launch_journal_processor(entry_text=None, file_path=None, speaker="user"):
    """Launch the journal processor for memory integration."""
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    print("📚 Launching DAWN Journal Processor")
    
    adapter = create_enhanced_journal_adapter()
    
    if file_path:
        # Process journal file
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"❌ Journal file not found: {file_path}")
            return
        
        print(f"📖 Processing journal file: {file_path.name}")
        summary = adapter.load_journal_file_enhanced(str(file_path), speaker)
        
        print(f"\n📊 Processing Summary:")
        for key, value in summary.items():
            if isinstance(value, dict):
                print(f"   {key}:")
                for subkey, subvalue in value.items():
                    print(f"     {subkey}: {subvalue}")
            else:
                print(f"   {key}: {value}")
    
    elif entry_text:
        # Process single entry
        print(f"📝 Processing journal entry from {speaker}")
        results = adapter.add_enhanced_journal_entry(entry_text, speaker)
        
        print(f"\n📊 Processing Results:")
        for key, value in results.items():
            if isinstance(value, list):
                print(f"   {key}: {len(value)} items")
            elif isinstance(value, dict):
                print(f"   {key}: {value}")
            else:
                print(f"   {key}: {value}")
    
    else:
        # Interactive mode
        print("💬 Interactive journal mode")
        print("   Enter journal entries (type 'quit' to exit)")
        
        while True:
            try:
                entry = input("\n📝 Journal entry: ").strip()
                if entry.lower() in ['quit', 'exit', 'q']:
                    break
                
                if entry:
                    results = adapter.add_enhanced_journal_entry(entry, speaker)
                    print(f"✅ Processed: {len(results['chunk_ids'])} chunks created")
                
            except KeyboardInterrupt:
                break
        
        print("👋 Journal session ended")


def launch_integrated_demo(mode='sequential'):
    """Launch the integrated demo showing both systems working together."""
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    print(f"🎬 Launching DAWN Integrated Demo ({mode} mode)")
    
    demo = DAWNVisualJournalDemo()
    
    if mode == 'sequential':
        demo.run_sequential_demo()
    elif mode == 'live':
        demo.run_live_demo()
    elif mode == 'async':
        import asyncio
        asyncio.run(demo.run_async_demo())
    elif mode == 'minimal':
        demo.test_minimal_integration()
    else:
        print(f"❌ Unknown demo mode: {mode}")


def quick_test():
    """Run a quick test of all integrated components."""
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    print("🧪 Running DAWN Integration Quick Test")
    
    # Test visual render
    print("\n1. Testing visual renderer...")
    quick_dawn_render()
    
    # Test journal processing
    print("\n2. Testing journal processor...")
    test_entry = "A moment of reflection on the integration of consciousness and technology."
    results = quick_enhanced_entry(test_entry, "test_user")
    print(f"   ✅ Created {len(results['chunk_ids'])} memory chunks")
    
    # Test minimal integration
    print("\n3. Testing minimal integration...")
    demo = DAWNVisualJournalDemo()
    demo.test_minimal_integration()
    
    print("\n✅ Quick test complete! All components operational.")


def main():
    """Main launcher with command-line interface."""
    parser = argparse.ArgumentParser(
        description="DAWN Visual Journal Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick test of all components
  python launch_dawn_visual_journal.py --quick-test
  
  # Launch visual monitor
  python launch_dawn_visual_journal.py --visual --live
  python launch_dawn_visual_journal.py --visual --mode minimal
  
  # Process journal entries
  python launch_dawn_visual_journal.py --journal --text "My thoughts today..."
  python launch_dawn_visual_journal.py --journal --file my_journal.txt --speaker "philosopher"
  python launch_dawn_visual_journal.py --journal --interactive
  
  # Run integrated demos
  python launch_dawn_visual_journal.py --demo sequential
  python launch_dawn_visual_journal.py --demo live
  python launch_dawn_visual_journal.py --demo async
        """
    )
    
    # Main action groups
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--quick-test', action='store_true',
                            help='Run quick test of all components')
    action_group.add_argument('--visual', action='store_true',
                            help='Launch visual monitor')
    action_group.add_argument('--journal', action='store_true',
                            help='Launch journal processor')
    action_group.add_argument('--demo', choices=['sequential', 'live', 'async', 'minimal'],
                            help='Launch integrated demo')
    
    # Visual monitor options
    visual_group = parser.add_argument_group('visual monitor options')
    visual_group.add_argument('--mode', choices=['full', 'minimal'], default='full',
                            help='Visual monitor mode (default: full)')
    visual_group.add_argument('--live', action='store_true',
                            help='Start live monitoring')
    
    # Journal processor options
    journal_group = parser.add_argument_group('journal processor options')
    journal_group.add_argument('--text', help='Journal entry text to process')
    journal_group.add_argument('--file', help='Journal file to process')
    journal_group.add_argument('--speaker', default='user',
                             help='Journal speaker identity (default: user)')
    journal_group.add_argument('--interactive', action='store_true',
                             help='Start interactive journal mode')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Display header
    print("🧠 DAWN VISUAL JOURNAL LAUNCHER")
    print("   Integrated cognitive visualization and memory processing")
    print("=" * 60)
    
    # Execute requested action
    try:
        if args.quick_test:
            quick_test()
        
        elif args.visual:
            launch_visual_monitor(mode=args.mode, live=args.live)
        
        elif args.journal:
            if args.interactive:
                launch_journal_processor(speaker=args.speaker)
            else:
                launch_journal_processor(
                    entry_text=args.text,
                    file_path=args.file,
                    speaker=args.speaker
                )
        
        elif args.demo:
            launch_integrated_demo(mode=args.demo)
    
    except KeyboardInterrupt:
        print("\n👋 Launcher interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 