#!/usr/bin/env python3
"""
🚀 DAWN UNIFIED LAUNCHER
Simple launcher for the DAWN Unified Runner with various options
"""

import sys
import os
import argparse
import asyncio
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def print_banner():
    """Print the DAWN banner"""
    print("\n" + "="*70)
    print("🧠 DAWN UNIFIED RUNNER - Master Backend Orchestrator")
    print("="*70)
    print("🔄 Tick Engine | ⚡ Entropy Tracker | 🔮 Sigil Engine")
    print("🔊 Voice Echo | 🌸 Rebloom Logger | 💭 Reflection Logger")
    print("🔍 Tracer Runtime | 🎨 Visual Processors")
    print("="*70)

async def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="Launch DAWN Unified Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_dawn.py                              # Run normally
  python launch_dawn.py --test                       # Run 30 second test
  python launch_dawn.py --verbose                    # Verbose logging
  python launch_dawn.py --no-voice                   # Disable voice systems
  python launch_dawn.py --visual-snapshots           # Enable visual snapshots
  python launch_dawn.py --enhanced-visuals           # Enable rich multi-panel visuals  
  python launch_dawn.py --force-visual-snapshot      # Take startup snapshot
  python launch_dawn.py --snapshot-interval 5        # Snapshot every 5 ticks
        """
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Run for 30 seconds then exit (for testing)'
    )
    
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--no-voice', 
        action='store_true',
        help='Disable voice systems'
    )
    
    parser.add_argument(
        '--tick-interval',
        type=float,
        default=2.0,
        help='Tick interval in seconds (default: 2.0)'
    )
    
    parser.add_argument(
        '--visual-snapshots',
        action='store_true',
        help='Enable automatic visual snapshots (every 10 ticks)'
    )
    
    parser.add_argument(
        '--snapshot-interval',
        type=int,
        default=10,
        help='Visual snapshot interval in ticks (default: 10)'
    )
    
    parser.add_argument(
        '--force-visual-snapshot',
        action='store_true',
        help='Take immediate visual snapshot on startup'
    )
    
    parser.add_argument(
        '--enhanced-visuals',
        action='store_true',
        help='Use enhanced visual engine for rich multi-panel snapshots'
    )
    
    args = parser.parse_args()
    
    print_banner()
    
    # Import after banner to show any import issues
    try:
        from core.dawn_runner import DAWNUnifiedRunner
    except ImportError as e:
        print(f"❌ Failed to import DAWN Runner: {e}")
        print("Please ensure all dependencies are installed.")
        sys.exit(1)
    
    # Configure logging level
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
        print("🔍 Verbose logging enabled")
    
    # Create runner
    runner = DAWNUnifiedRunner()
    
    # Configure visual processing
    if args.visual_snapshots:
        if args.enhanced_visuals:
            print(f"🎨 Enhanced visual snapshots enabled (every {args.snapshot_interval} ticks)")
            print("   - Multi-panel consciousness dashboard")
            print("   - Entropy evolution analysis") 
            print("   - Performance radar charts")
            print("   - Cognitive network visualization")
            print("   - Mood & zone analysis")
        else:
            print(f"📸 Visual snapshots enabled (every {args.snapshot_interval} ticks)")
        
        # Update snapshot interval if visual integration is available
        if 'visual_integration' in runner.systems:
            visual_integration = runner.systems['visual_integration']
            if hasattr(visual_integration, 'snapshot_interval'):
                visual_integration.snapshot_interval = args.snapshot_interval
                print(f"   ✅ Updated visual integration interval to {args.snapshot_interval} ticks")
            
            # Configure enhanced visuals
            if args.enhanced_visuals and hasattr(visual_integration, 'use_enhanced_engine'):
                visual_integration.use_enhanced_engine = True
                print("   ✅ Enhanced visual engine enabled")
    
    # Always configure the interval even if --visual-snapshots isn't used
    # (in case visual processing is enabled by default)
    if args.snapshot_interval != 10:  # Only if different from default
        if 'visual_integration' in runner.systems:
            visual_integration = runner.systems['visual_integration']
            if hasattr(visual_integration, 'snapshot_interval'):
                visual_integration.snapshot_interval = args.snapshot_interval
                print(f"   🔧 Set visual integration interval to {args.snapshot_interval} ticks")
    
    # Take immediate snapshot if requested
    if args.force_visual_snapshot:
        print("📸 Taking immediate visual snapshot...")
        try:
            from visual.visual_trigger import trigger_visual_snapshot
            # Generate simulated tick data for immediate snapshot
            import time
            test_tick_data = {
                'tick': 0,
                'timestamp': time.time(),
                'scup': 0.5,
                'entropy': 0.3,
                'heat': 25.0,
                'mood': 'startup',
                'zone': 'CALM',
                'startup_snapshot': True
            }
            rendered_files = trigger_visual_snapshot(test_tick_data, force=True)
            if rendered_files:
                print(f"   ✅ Generated {len(rendered_files)} startup visualizations")
                for file_path in rendered_files:
                    print(f"   📁 {file_path}")
            else:
                print("   ⚠️  No visualizations generated")
        except Exception as e:
            print(f"   ❌ Failed to generate startup snapshot: {e}")
    
    # Disable voice if requested
    if args.no_voice:
        print("🔇 Voice systems disabled")
        # Remove voice systems from runner
        if 'voice_echo' in runner.systems:
            del runner.systems['voice_echo']
        if 'tracer_voice' in runner.systems:
            del runner.systems['tracer_voice']
    
    # Test mode
    if args.test:
        print("🧪 Running in test mode (30 seconds)")
        
        async def test_timeout():
            await asyncio.sleep(30)
            print("\n⏰ Test completed - shutting down...")
            runner.running = False
        
        try:
            await asyncio.gather(
                runner.run(),
                test_timeout()
            )
        except KeyboardInterrupt:
            print("\n🛑 Test interrupted")
        finally:
            await runner.shutdown()
            print("🎯 Test completed successfully!")
            return
    
    # Normal mode
    print("🚀 Starting DAWN Unified Runner...")
    print("🛑 Press Ctrl+C to shutdown gracefully")
    
    try:
        await runner.run()
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await runner.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Launcher error: {e}")
        sys.exit(1) 