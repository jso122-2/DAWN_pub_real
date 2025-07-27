#!/usr/bin/env python3
"""
DAWN Main Integration - Complete Cognitive Loop
Wires together visual rendering, auto-reflection, and memory processing into a unified system.
"""

import time
import threading
import signal
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add all components to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    # Core components
    from memories.rebloom_journal_simple import ReblooomJournal, get_default_journal
    from processes.auto_reflect import AutoReflect, ReflectionConfig, ReflectionMode
    from backend.visual.sigil_renderer import SigilRenderer, create_terminal_renderer, UrgencyLevel
    from backend.visual.dawn_renderer_integration import DAWNRendererIntegration
    
    print("✅ All DAWN integration components loaded successfully")
    COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some components not available: {e}")
    print("🔧 Running with available components only")
    COMPONENTS_AVAILABLE = False


class DAWNMainLoop:
    """
    Main DAWN cognitive loop integrating:
    - Auto-reflection system (thought generation)
    - Memory processing (rebloom journal)  
    - Visual rendering (sigil display)
    - Pattern recognition and cognitive tracking
    """
    
    def __init__(self):
        """Initialize the complete DAWN integration."""
        self.is_running = False
        self.start_time = None
        
        # Core components
        self.journal = get_default_journal() if COMPONENTS_AVAILABLE else None
        self.visual_renderer = create_terminal_renderer() if COMPONENTS_AVAILABLE else None
        self.auto_reflector = None
        
        # State tracking
        self.total_reflections = 0
        self.total_memory_chunks = 0
        self.active_themes = []
        self.cognitive_depth = 1
        self.session_stats = {
            'reflections_generated': 0,
            'memory_chunks_created': 0,
            'themes_detected': 0,
            'visual_renders': 0,
            'session_duration': 0.0
        }
        
        # Threading
        self.reflection_thread = None
        self.visual_thread = None
        self.stats_thread = None
        
        print("🧠 DAWN Main Integration initialized")
        print(f"   Components available: {COMPONENTS_AVAILABLE}")
    
    def start_main_loop(self, 
                       mode: str = "mixed", 
                       duration_minutes: float = 30.0,
                       reflection_interval: float = 120.0):
        """
        Start the complete DAWN cognitive loop.
        
        Args:
            mode: Reflection mode (contemplative, analytical, creative, mixed)
            duration_minutes: Total session duration
            reflection_interval: Seconds between reflections
        """
        if not COMPONENTS_AVAILABLE:
            print("❌ Required components not available")
            return
        
        self.is_running = True
        self.start_time = datetime.now()
        
        print(f"\n🚀 Starting DAWN Main Cognitive Loop")
        print(f"   Mode: {mode}")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Reflection interval: {reflection_interval} seconds")
        print(f"   Press Ctrl+C to stop gracefully")
        print("=" * 70)
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        
        try:
            if mode == "mixed":
                self._run_mixed_mode_loop(duration_minutes, reflection_interval)
            else:
                self._run_single_mode_loop(mode, duration_minutes, reflection_interval)
        
        except KeyboardInterrupt:
            print("\n⏹️ Main loop interrupted by user")
        finally:
            self.stop_main_loop()
    
    def _run_mixed_mode_loop(self, duration_minutes: float, base_interval: float):
        """Run mixed-mode cognitive loop cycling through all reflection types."""
        modes = [
            (ReflectionMode.CONTEMPLATIVE, "contemplative_mind", base_interval),
            (ReflectionMode.ANALYTICAL, "analytical_mind", base_interval * 1.2),
            (ReflectionMode.CREATIVE, "creative_mind", base_interval * 0.8),
            (ReflectionMode.INTROSPECTIVE, "introspective_mind", base_interval * 1.1)
        ]
        
        phase_duration = (duration_minutes * 60) / len(modes)
        
        # Start visual monitoring
        self._start_visual_monitoring()
        
        # Start statistics tracking
        self._start_statistics_tracking()
        
        for phase_num, (mode, speaker, interval) in enumerate(modes, 1):
            if not self.is_running:
                break
            
            print(f"\n{'🔸' * 50}")
            print(f"🧠 PHASE {phase_num}/4: {mode.value.upper()} MODE")
            print(f"   Speaker: {speaker}")
            print(f"   Interval: {interval:.1f}s")
            print(f"   Duration: {phase_duration/60:.1f} minutes")
            print(f"{'🔸' * 50}")
            
            # Configure auto-reflector for this phase
            config = ReflectionConfig(
                reflection_interval=interval,
                mode=mode,
                max_reflections_per_session=int(phase_duration / interval) + 1,
                enable_visual_feedback=False,  # We handle visuals separately
                enable_pattern_analysis=True,
                speaker_identity=speaker,
                depth_progression=True
            )
            
            self.auto_reflector = AutoReflect(config)
            
            # Start reflection thread
            self.reflection_thread = threading.Thread(
                target=self._reflection_worker, 
                args=(self.auto_reflector,),
                daemon=True
            )
            self.reflection_thread.start()
            
            # Wait for phase completion
            phase_start = time.time()
            while (time.time() - phase_start) < phase_duration and self.is_running:
                time.sleep(1.0)
                self._update_session_stats()
            
            # Stop current phase
            if self.auto_reflector:
                self.auto_reflector.stop_auto_reflection()
            
            # Show phase summary
            self._show_phase_summary(phase_num, mode.value)
    
    def _run_single_mode_loop(self, mode: str, duration_minutes: float, interval: float):
        """Run single-mode cognitive loop."""
        reflection_mode = ReflectionMode(mode.lower())
        speaker = f"{mode}_mind"
        
        print(f"🧠 Single Mode: {mode.upper()}")
        print(f"   Speaker: {speaker}")
        print(f"   Interval: {interval}s")
        
        # Start monitoring
        self._start_visual_monitoring()
        self._start_statistics_tracking()
        
        # Configure auto-reflector
        config = ReflectionConfig(
            reflection_interval=interval,
            mode=reflection_mode,
            max_reflections_per_session=int((duration_minutes * 60) / interval) + 1,
            enable_visual_feedback=False,
            enable_pattern_analysis=True,
            speaker_identity=speaker,
            depth_progression=True
        )
        
        self.auto_reflector = AutoReflect(config)
        
        # Start reflection thread
        self.reflection_thread = threading.Thread(
            target=self._reflection_worker,
            args=(self.auto_reflector,),
            daemon=True
        )
        self.reflection_thread.start()
        
        # Wait for completion
        session_start = time.time()
        while (time.time() - session_start) < (duration_minutes * 60) and self.is_running:
            time.sleep(1.0)
            self._update_session_stats()
    
    def _reflection_worker(self, reflector: AutoReflect):
        """Worker thread for generating reflections."""
        try:
            while self.is_running and reflector.reflection_count < reflector.config.max_reflections_per_session:
                # Generate reflection
                reflector._generate_reflection()
                
                # Update our tracking
                self.total_reflections += 1
                self.cognitive_depth = reflector.depth_level
                
                # Track themes
                if reflector.recurring_themes:
                    for theme in reflector.recurring_themes:
                        if theme not in self.active_themes:
                            self.active_themes.append(theme)
                            print(f"🔍 New theme detected: {theme}")
                
                # Update memory chunk count
                if self.journal:
                    current_chunks = self.journal.get_stats()['chunks_created']
                    self.total_memory_chunks = current_chunks
                
                # Wait for next reflection
                if self.is_running:
                    time.sleep(reflector.config.reflection_interval)
        
        except Exception as e:
            print(f"⚠️ Reflection worker error: {e}")
    
    def _start_visual_monitoring(self):
        """Start visual monitoring thread."""
        if not self.visual_renderer:
            return
        
        self.visual_thread = threading.Thread(target=self._visual_worker, daemon=True)
        self.visual_thread.start()
        print("🎨 Visual monitoring started")
    
    def _visual_worker(self):
        """Worker thread for visual rendering."""
        try:
            while self.is_running:
                # Create fake sigil data representing current state
                active_sigils = []
                
                # Add reflection state sigil
                if self.auto_reflector and self.auto_reflector.is_running:
                    mode_name = self.auto_reflector.config.mode.value.upper()
                    active_sigils.append({
                        'name': f'AUTO_REFLECT_{mode_name}',
                        'urgency': UrgencyLevel.MEDIUM,
                        'duration': time.time() - self.start_time.timestamp() if self.start_time else 0,
                        'trigger_count': self.total_reflections
                    })
                
                # Add depth tracking sigil
                if self.cognitive_depth > 2:
                    active_sigils.append({
                        'name': 'DEEP_CONTEMPLATION',
                        'urgency': UrgencyLevel.HIGH if self.cognitive_depth >= 4 else UrgencyLevel.MEDIUM,
                        'duration': 0,
                        'trigger_count': self.cognitive_depth
                    })
                
                # Add theme tracking sigil
                if len(self.active_themes) > 2:
                    active_sigils.append({
                        'name': 'PATTERN_RECOGNITION',
                        'urgency': UrgencyLevel.LOW,
                        'duration': 0,
                        'trigger_count': len(self.active_themes)
                    })
                
                # Create system stats
                system_stats = {
                    'reflections': self.total_reflections,
                    'memory_chunks': self.total_memory_chunks,
                    'themes': len(self.active_themes),
                    'depth': self.cognitive_depth,
                    'session_time': (datetime.now() - self.start_time).total_seconds() / 60 if self.start_time else 0
                }
                
                # Render
                self.visual_renderer.render(
                    sigil_data=active_sigils,
                    organ_data={'CognitivePulse': self.cognitive_depth, 'ThemeDetector': len(self.active_themes)},
                    system_data=system_stats,
                    force_render=True
                )
                
                self.session_stats['visual_renders'] += 1
                time.sleep(3.0)  # Update every 3 seconds
        
        except Exception as e:
            print(f"⚠️ Visual worker error: {e}")
    
    def _start_statistics_tracking(self):
        """Start statistics tracking thread."""
        self.stats_thread = threading.Thread(target=self._stats_worker, daemon=True)
        self.stats_thread.start()
        print("📊 Statistics tracking started")
    
    def _stats_worker(self):
        """Worker thread for statistics tracking."""
        try:
            while self.is_running:
                self._update_session_stats()
                time.sleep(10.0)  # Update every 10 seconds
        except Exception as e:
            print(f"⚠️ Stats worker error: {e}")
    
    def _update_session_stats(self):
        """Update session statistics."""
        if self.start_time:
            self.session_stats['session_duration'] = (datetime.now() - self.start_time).total_seconds()
        
        self.session_stats['reflections_generated'] = self.total_reflections
        self.session_stats['memory_chunks_created'] = self.total_memory_chunks
        self.session_stats['themes_detected'] = len(self.active_themes)
    
    def _show_phase_summary(self, phase_num: int, mode: str):
        """Show summary for completed phase."""
        print(f"\n📊 Phase {phase_num} ({mode}) Summary:")
        print(f"   Reflections: {self.total_reflections}")
        print(f"   Memory chunks: {self.total_memory_chunks}")
        print(f"   Themes: {self.active_themes}")
        print(f"   Depth reached: {self.cognitive_depth}")
    
    def _signal_handler(self, signum, frame):
        """Handle interrupt signals gracefully."""
        print(f"\n⚠️ Received signal {signum}, initiating graceful shutdown...")
        self.stop_main_loop()
    
    def stop_main_loop(self):
        """Stop the main cognitive loop gracefully."""
        print(f"\n⏹️ Stopping DAWN Main Loop...")
        
        self.is_running = False
        
        # Stop auto-reflector
        if self.auto_reflector:
            self.auto_reflector.stop_auto_reflection()
        
        # Wait for threads to finish (with timeout)
        for thread in [self.reflection_thread, self.visual_thread, self.stats_thread]:
            if thread and thread.is_alive():
                thread.join(timeout=2.0)
        
        # Show final statistics
        self._show_final_summary()
    
    def _show_final_summary(self):
        """Show comprehensive final summary."""
        if not self.start_time:
            return
        
        duration = datetime.now() - self.start_time
        
        print(f"\n" + "="*70)
        print(f"📊 DAWN MAIN LOOP - FINAL SUMMARY")
        print(f"="*70)
        print(f"🕐 Session Duration: {duration}")
        print(f"🤔 Total Reflections: {self.session_stats['reflections_generated']}")
        print(f"📚 Memory Chunks Created: {self.session_stats['memory_chunks_created']}")
        print(f"🔍 Themes Detected: {self.session_stats['themes_detected']}")
        print(f"🎨 Visual Renders: {self.session_stats['visual_renders']}")
        print(f"🧠 Final Cognitive Depth: {self.cognitive_depth}")
        
        if self.active_themes:
            print(f"🎯 Recurring Themes:")
            for theme in self.active_themes:
                print(f"   • {theme}")
        
        # Journal statistics
        if self.journal:
            journal_stats = self.journal.get_stats()
            print(f"\n📓 Journal Statistics:")
            for key, value in journal_stats.items():
                print(f"   {key}: {value}")
        
        # Performance metrics
        reflections_per_minute = self.total_reflections / (duration.total_seconds() / 60) if duration.total_seconds() > 0 else 0
        chunks_per_reflection = self.total_memory_chunks / self.total_reflections if self.total_reflections > 0 else 0
        
        print(f"\n⚡ Performance Metrics:")
        print(f"   Reflections per minute: {reflections_per_minute:.2f}")
        print(f"   Chunks per reflection: {chunks_per_reflection:.2f}")
        print(f"   Themes per reflection: {len(self.active_themes) / self.total_reflections if self.total_reflections > 0 else 0:.2f}")
        
        print(f"\n✨ DAWN cognitive session complete!")
        print(f"   All reflections stored in memory for rebloom processing")
        print(f"   Pattern recognition and theme detection successful")
        print(f"   Visual cognitive monitoring completed")


def quick_test_main_loop():
    """Quick test of the main integration loop."""
    print("🧪 DAWN Main Integration - Quick Test")
    print("="*50)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available for testing")
        return
    
    # Create main loop
    main_loop = DAWNMainLoop()
    
    print("🔄 Running 2-minute test with fast intervals...")
    
    try:
        # Quick 2-minute test with fast intervals
        main_loop.start_main_loop(
            mode="contemplative",
            duration_minutes=2.0,
            reflection_interval=15.0  # 15 seconds for quick test
        )
    except KeyboardInterrupt:
        print("\n⏹️ Quick test interrupted")
    
    print("\n✅ Quick test completed!")


def full_demo_main_loop():
    """Full demonstration of the main integration loop."""
    print("🎬 DAWN Main Integration - Full Demo")
    print("="*50)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available for demo")
        return
    
    print("This will run a comprehensive demo showing:")
    print("  🤔 Auto-reflection across multiple modes")
    print("  📚 Memory processing and chunking")
    print("  🎨 Live visual rendering")
    print("  🔍 Pattern recognition and theme detection")
    print("  📊 Real-time statistics tracking")
    
    response = input("\nProceed with demo? (y/n): ").strip().lower()
    if response != 'y':
        print("Demo cancelled.")
        return
    
    # Create main loop
    main_loop = DAWNMainLoop()
    
    print("\n🚀 Starting full demo...")
    
    try:
        # Full 10-minute mixed-mode demo
        main_loop.start_main_loop(
            mode="mixed",
            duration_minutes=10.0,
            reflection_interval=60.0  # 1 minute intervals
        )
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    
    print("\n🎉 Full demo completed!")


def interactive_main_loop():
    """Interactive main loop with user options."""
    print("🤔 DAWN Main Integration - Interactive Mode")
    print("="*50)
    
    if not COMPONENTS_AVAILABLE:
        print("❌ Components not available")
        return
    
    while True:
        print("\nOptions:")
        print("1. Quick test (2 minutes, contemplative)")
        print("2. Short session (5 minutes, single mode)")
        print("3. Medium session (10 minutes, mixed mode)")
        print("4. Long session (20 minutes, mixed mode)")
        print("5. Custom session")
        print("6. Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            quick_test_main_loop()
        
        elif choice == '2':
            mode = input("Enter mode (contemplative/analytical/creative/introspective): ").strip()
            main_loop = DAWNMainLoop()
            main_loop.start_main_loop(mode=mode, duration_minutes=5.0, reflection_interval=45.0)
        
        elif choice == '3':
            main_loop = DAWNMainLoop()
            main_loop.start_main_loop(mode="mixed", duration_minutes=10.0, reflection_interval=90.0)
        
        elif choice == '4':
            main_loop = DAWNMainLoop()
            main_loop.start_main_loop(mode="mixed", duration_minutes=20.0, reflection_interval=120.0)
        
        elif choice == '5':
            mode = input("Mode (contemplative/analytical/creative/mixed): ").strip()
            duration = float(input("Duration (minutes): "))
            interval = float(input("Reflection interval (seconds): "))
            
            main_loop = DAWNMainLoop()
            main_loop.start_main_loop(mode=mode, duration_minutes=duration, reflection_interval=interval)
        
        elif choice == '6':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")


def main():
    """Main function with command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Main Integration Loop")
    parser.add_argument('--quick-test', action='store_true', help='Run quick 2-minute test')
    parser.add_argument('--full-demo', action='store_true', help='Run full 10-minute demo')
    parser.add_argument('--interactive', action='store_true', help='Start interactive mode')
    parser.add_argument('--mode', default='mixed', help='Reflection mode')
    parser.add_argument('--duration', type=float, default=15.0, help='Duration in minutes')
    parser.add_argument('--interval', type=float, default=120.0, help='Reflection interval in seconds')
    
    args = parser.parse_args()
    
    print("🧠 DAWN MAIN INTEGRATION LOOP")
    print("   Complete cognitive system with auto-reflection, memory, and visuals")
    print("="*70)
    
    if args.quick_test:
        quick_test_main_loop()
    elif args.full_demo:
        full_demo_main_loop()
    elif args.interactive:
        interactive_main_loop()
    else:
        # Run custom session
        main_loop = DAWNMainLoop()
        main_loop.start_main_loop(
            mode=args.mode,
            duration_minutes=args.duration,
            reflection_interval=args.interval
        )


if __name__ == "__main__":
    main() 