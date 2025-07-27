#!/usr/bin/env python3
"""
DAWN Auto-Reflect Launcher
Integrated launcher for automated reflection and journaling with visual feedback.
"""

import sys
import argparse
import threading
import time
from pathlib import Path

# Add DAWN components to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from processes.auto_reflect import AutoReflect, ReflectionConfig, ReflectionMode, start_auto_reflection
    from memories.rebloom_journal_simple import get_default_journal
    from backend.visual.dawn_renderer_integration import create_dawn_terminal_monitor, create_dawn_minimal_monitor
    print("✅ Auto-Reflect components loaded successfully")
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Could not import components: {e}")
    print("🔧 Please ensure all integration files are properly installed")
    COMPONENTS_AVAILABLE = False


class AutoReflectLauncher:
    """
    Integrated launcher for the DAWN Auto-Reflection system.
    Combines automated reflection, memory processing, and visual feedback.
    """
    
    def __init__(self):
        """Initialize the launcher with all integrated components."""
        if not COMPONENTS_AVAILABLE:
            print("❌ Required components not available")
            return
        
        self.reflector = None
        self.visual_monitor = None
        self.journal = get_default_journal()
        self.reflection_thread = None
        self.monitor_thread = None
        self.is_running = False
        
        print("🤔 Auto-Reflect Launcher initialized")
    
    def launch_contemplative_session(self, duration_minutes: float = 15.0, interval_seconds: float = 120.0):
        """Launch a contemplative reflection session with visual monitoring."""
        print(f"🧘 Starting contemplative reflection session")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Reflection interval: {interval_seconds} seconds")
        
        config = ReflectionConfig(
            reflection_interval=interval_seconds,
            mode=ReflectionMode.CONTEMPLATIVE,
            max_reflections_per_session=int((duration_minutes * 60) / interval_seconds),
            enable_visual_feedback=True,
            enable_pattern_analysis=True,
            speaker_identity="contemplative_mind"
        )
        
        self._start_integrated_session(config, duration_minutes)
    
    def launch_analytical_session(self, duration_minutes: float = 20.0, interval_seconds: float = 180.0):
        """Launch an analytical reflection session."""
        print(f"🔬 Starting analytical reflection session")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Reflection interval: {interval_seconds} seconds")
        
        config = ReflectionConfig(
            reflection_interval=interval_seconds,
            mode=ReflectionMode.ANALYTICAL,
            max_reflections_per_session=int((duration_minutes * 60) / interval_seconds),
            enable_visual_feedback=True,
            enable_pattern_analysis=True,
            speaker_identity="analytical_mind"
        )
        
        self._start_integrated_session(config, duration_minutes)
    
    def launch_creative_session(self, duration_minutes: float = 25.0, interval_seconds: float = 150.0):
        """Launch a creative exploration session."""
        print(f"🎨 Starting creative reflection session")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Reflection interval: {interval_seconds} seconds")
        
        config = ReflectionConfig(
            reflection_interval=interval_seconds,
            mode=ReflectionMode.CREATIVE,
            max_reflections_per_session=int((duration_minutes * 60) / interval_seconds),
            enable_visual_feedback=True,
            enable_pattern_analysis=True,
            speaker_identity="creative_mind"
        )
        
        self._start_integrated_session(config, duration_minutes)
    
    def launch_mixed_session(self, duration_minutes: float = 30.0):
        """Launch a mixed-mode session that cycles through different reflection types."""
        print(f"🌈 Starting mixed-mode reflection session")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Cycling through: contemplative → analytical → creative → introspective")
        
        modes = [
            (ReflectionMode.CONTEMPLATIVE, "contemplative_mind", 120.0),
            (ReflectionMode.ANALYTICAL, "analytical_mind", 180.0),
            (ReflectionMode.CREATIVE, "creative_mind", 150.0),
            (ReflectionMode.INTROSPECTIVE, "introspective_mind", 140.0)
        ]
        
        # Calculate time per mode
        time_per_mode = (duration_minutes * 60) / len(modes)
        
        self.is_running = True
        self.visual_monitor = create_dawn_terminal_monitor()
        
        # Start visual monitoring
        self.monitor_thread = threading.Thread(target=self._visual_monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        try:
            for i, (mode, speaker, interval) in enumerate(modes):
                if not self.is_running:
                    break
                
                print(f"\n{'='*60}")
                print(f"Phase {i+1}/4: {mode.value.upper()} MODE")
                print(f"{'='*60}")
                
                config = ReflectionConfig(
                    reflection_interval=interval,
                    mode=mode,
                    max_reflections_per_session=int(time_per_mode / interval),
                    enable_visual_feedback=True,
                    enable_pattern_analysis=True,
                    speaker_identity=speaker
                )
                
                # Run phase
                phase_reflector = AutoReflect(config)
                phase_thread = threading.Thread(target=phase_reflector.start_auto_reflection, daemon=True)
                phase_thread.start()
                
                # Wait for phase completion or time limit
                start_time = time.time()
                while time.time() - start_time < time_per_mode and self.is_running:
                    time.sleep(1.0)
                
                phase_reflector.stop_auto_reflection()
                
                # Show phase summary
                summary = phase_reflector.get_reflection_summary()
                print(f"\n📊 Phase {i+1} Summary:")
                print(f"   Reflections: {summary.get('reflection_count', 0)}")
                print(f"   Themes: {len(summary.get('recurring_themes', []))}")
                print(f"   Depth: {summary.get('current_depth', 1)}")
        
        except KeyboardInterrupt:
            print("\n⏹️ Mixed session interrupted")
        finally:
            self.stop_session()
    
    def _start_integrated_session(self, config: ReflectionConfig, duration_minutes: float):
        """Start an integrated reflection session with visual monitoring."""
        self.is_running = True
        self.reflector = AutoReflect(config)
        self.visual_monitor = create_dawn_terminal_monitor()
        
        print(f"\n🔄 Starting integrated session...")
        print(f"   Mode: {config.mode.value}")
        print(f"   Speaker: {config.speaker_identity}")
        print(f"   Visual feedback: {'Enabled' if config.enable_visual_feedback else 'Disabled'}")
        print(f"   Press Ctrl+C to stop early")
        
        # Start reflection in background thread
        self.reflection_thread = threading.Thread(target=self.reflector.start_auto_reflection, daemon=True)
        self.reflection_thread.start()
        
        # Start visual monitoring
        self.monitor_thread = threading.Thread(target=self._visual_monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        try:
            # Wait for duration or interruption
            time.sleep(duration_minutes * 60)
        except KeyboardInterrupt:
            print("\n⏹️ Session interrupted by user")
        finally:
            self.stop_session()
    
    def _visual_monitoring_loop(self):
        """Background visual monitoring loop."""
        while self.is_running:
            try:
                if self.visual_monitor:
                    # Show system state with reflection info
                    self.visual_monitor.render_current_state(force=True)
                
                time.sleep(3.0)  # Update every 3 seconds
            except Exception as e:
                print(f"⚠️ Visual monitoring error: {e}")
                time.sleep(5.0)
    
    def stop_session(self):
        """Stop the current reflection session."""
        self.is_running = False
        
        if self.reflector:
            self.reflector.stop_auto_reflection()
            
            # Show final summary
            summary = self.reflector.get_reflection_summary()
            print(f"\n📊 Final Session Summary:")
            for key, value in summary.items():
                if key != 'latest_reflection':  # Skip long text
                    print(f"   {key}: {value}")
        
        if self.journal:
            stats = self.journal.get_stats()
            print(f"\n📚 Journal Statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        
        print(f"\n✨ Session complete! All reflections stored in memory.")
    
    def quick_reflection(self, prompt: str = None, mode: str = "contemplative"):
        """Generate a single quick reflection."""
        if not COMPONENTS_AVAILABLE:
            print("❌ Components not available")
            return
        
        print(f"🤔 Generating {mode} reflection...")
        
        config = ReflectionConfig(
            mode=ReflectionMode(mode.lower()),
            speaker_identity=f"quick_{mode}_mind"
        )
        
        reflector = AutoReflect(config)
        reflection = reflector.manual_reflect(prompt)
        
        print(f"\n💭 Generated reflection:")
        print(f"   {reflection}")
        
        return reflection
    
    def interactive_mode(self):
        """Start interactive reflection mode."""
        if not COMPONENTS_AVAILABLE:
            print("❌ Components not available")
            return
        
        print("\n🤔 Interactive Auto-Reflection Mode")
        print("=" * 50)
        print("Commands:")
        print("  contemplate [duration] - Start contemplative session")
        print("  analyze [duration] - Start analytical session") 
        print("  create [duration] - Start creative session")
        print("  mixed [duration] - Start mixed-mode session")
        print("  quick [prompt] - Generate single reflection")
        print("  stats - Show journal statistics")
        print("  quit - Exit")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\nAuto-Reflect > ").strip()
                
                if not user_input:
                    continue
                
                parts = user_input.split()
                command = parts[0].lower()
                
                if command in ['quit', 'exit', 'q']:
                    break
                
                elif command == 'contemplate':
                    duration = float(parts[1]) if len(parts) > 1 else 15.0
                    self.launch_contemplative_session(duration)
                
                elif command == 'analyze':
                    duration = float(parts[1]) if len(parts) > 1 else 20.0
                    self.launch_analytical_session(duration)
                
                elif command == 'create':
                    duration = float(parts[1]) if len(parts) > 1 else 25.0
                    self.launch_creative_session(duration)
                
                elif command == 'mixed':
                    duration = float(parts[1]) if len(parts) > 1 else 30.0
                    self.launch_mixed_session(duration)
                
                elif command == 'quick':
                    prompt = ' '.join(parts[1:]) if len(parts) > 1 else None
                    self.quick_reflection(prompt)
                
                elif command == 'stats':
                    if self.journal:
                        stats = self.journal.get_stats()
                        print(f"📊 Journal Statistics:")
                        for key, value in stats.items():
                            print(f"   {key}: {value}")
                
                else:
                    print(f"❌ Unknown command: {command}")
            
            except KeyboardInterrupt:
                print("\n👋 Exiting interactive mode...")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("👋 Goodbye!")


def main():
    """Main launcher with command-line interface."""
    parser = argparse.ArgumentParser(
        description="DAWN Auto-Reflect Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick reflection
  python launch_auto_reflect.py --quick --prompt "consciousness and recursion"
  
  # Contemplative session
  python launch_auto_reflect.py --contemplate --duration 15 --interval 120
  
  # Analytical session  
  python launch_auto_reflect.py --analyze --duration 20 --interval 180
  
  # Creative session
  python launch_auto_reflect.py --create --duration 25 --interval 150
  
  # Mixed-mode session
  python launch_auto_reflect.py --mixed --duration 30
  
  # Interactive mode
  python launch_auto_reflect.py --interactive
        """
    )
    
    # Main action groups
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--quick', action='store_true',
                            help='Generate single quick reflection')
    action_group.add_argument('--contemplate', action='store_true',
                            help='Start contemplative session')
    action_group.add_argument('--analyze', action='store_true',
                            help='Start analytical session')
    action_group.add_argument('--create', action='store_true',
                            help='Start creative session')
    action_group.add_argument('--mixed', action='store_true',
                            help='Start mixed-mode session')
    action_group.add_argument('--interactive', action='store_true',
                            help='Start interactive mode')
    
    # Options
    parser.add_argument('--duration', type=float, default=15.0,
                       help='Session duration in minutes (default: 15)')
    parser.add_argument('--interval', type=float, default=120.0,
                       help='Reflection interval in seconds (default: 120)')
    parser.add_argument('--prompt', help='Prompt for quick reflection')
    parser.add_argument('--mode', choices=['contemplative', 'analytical', 'creative', 'introspective'],
                       default='contemplative', help='Mode for quick reflection')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Display header
    print("🤔 DAWN AUTO-REFLECT LAUNCHER")
    print("   Automated reflection with memory integration and visual feedback")
    print("=" * 70)
    
    # Create launcher
    launcher = AutoReflectLauncher()
    
    # Execute requested action
    try:
        if args.quick:
            launcher.quick_reflection(args.prompt, args.mode)
        
        elif args.contemplate:
            launcher.launch_contemplative_session(args.duration, args.interval)
        
        elif args.analyze:
            launcher.launch_analytical_session(args.duration, args.interval)
        
        elif args.create:
            launcher.launch_creative_session(args.duration, args.interval)
        
        elif args.mixed:
            launcher.launch_mixed_session(args.duration)
        
        elif args.interactive:
            launcher.interactive_mode()
    
    except KeyboardInterrupt:
        print("\n👋 Launcher interrupted. Goodbye!")
        launcher.stop_session()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 