#!/usr/bin/env python3
"""
DAWN Visual Process Launcher
Universal launcher for DAWN visual consciousness processes
"""

import sys
import os
import argparse
import time
import signal
import threading
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "visual"))

# Import DAWN modules
try:
    from visual.visual_consciousness_manager import VisualConsciousnessManager
    VISUAL_MANAGER_AVAILABLE = True
except ImportError:
    VISUAL_MANAGER_AVAILABLE = False

# Available visual processes
VISUAL_PROCESSES = {
    'pulse_map_renderer': {
        'script': 'pulse_waveform_renderer.py',
        'description': 'Core consciousness pulse visualization',
        'category': 'consciousness',
        'priority': 'CRITICAL'
    },
    'mood_heatmap': {
        'script': 'mood_heatmap.py',
        'description': 'Real-time emotional state heatmap',
        'category': 'consciousness',
        'priority': 'HIGH'
    },
    'drift_vector_field': {
        'script': 'drift_vector_field.py',
        'description': 'Semantic drift and vector field analysis',
        'category': 'analysis',
        'priority': 'HIGH'
    },
    'sigil_trace_visualizer': {
        'script': 'sigil_trace_visualizer.py',
        'description': 'Emotional sigil patterns and traces',
        'category': 'consciousness',
        'priority': 'HIGH'
    },
    'tracer_drift_vectors': {
        'script': 'tracer_drift_vectors.py',
        'description': 'Semantic tracer movement analysis',
        'category': 'analysis',
        'priority': 'MEDIUM'
    },
    'synthesis_entropy_chart': {
        'script': 'synthesis_entropy_chart.py',
        'description': 'Entropy synthesis and distribution',
        'category': 'analysis',
        'priority': 'MEDIUM'
    },
    'rebloom_trail_animation': {
        'script': 'rebloom_trail_animation.py',
        'description': 'Rebloom event trails and cascades',
        'category': 'dynamics',
        'priority': 'MEDIUM'
    },
    'recursive_bloom_tree': {
        'script': 'recursive_bloom_tree.py',
        'description': 'Hierarchical bloom structures',
        'category': 'structure',
        'priority': 'LOW'
    },
    'hybrid_field_visualizer': {
        'script': 'hybrid_field_visualizer.py',
        'description': 'Multi-dimensional consciousness fields',
        'category': 'structure',
        'priority': 'LOW'
    },
    'semantic_timeline_animator': {
        'script': 'semantic_timeline_animator.py',
        'description': 'Semantic evolution timeline',
        'category': 'timeline',
        'priority': 'LOW'
    },
    'stall_density_animator': {
        'script': 'stall_density_animator.py',
        'description': 'Cognitive stall pattern visualization',
        'category': 'analysis',
        'priority': 'MEDIUM'
    },
    'scup_zone_animator': {
        'script': 'scup_zone_animator.py',
        'description': 'SCUP zone visualization',
        'category': 'consciousness',
        'priority': 'HIGH'
    }
}

class VisualProcessLauncher:
    def __init__(self):
        self.running = False
        self.stop_event = threading.Event()
        self.process_name = None
        
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\n🛑 Visual process '{self.process_name}' received signal {signum}, shutting down...")
        self.stop_event.set()
        self.running = False
        
    def run_visual_process(self, process_id: str, duration: int = 300, fps: float = 10.0):
        """Run a specific visual process"""
        if process_id not in VISUAL_PROCESSES:
            print(f"❌ Unknown visual process: {process_id}")
            print(f"Available processes: {', '.join(VISUAL_PROCESSES.keys())}")
            return False
            
        process_info = VISUAL_PROCESSES[process_id]
        self.process_name = process_id
        self.running = True
        
        print(f"🎬 Starting DAWN Visual Process: {process_id}")
        print(f"   Description: {process_info['description']}")
        print(f"   Category: {process_info['category']}")
        print(f"   Priority: {process_info['priority']}")
        print(f"   Target FPS: {fps}")
        print(f"   Duration: {duration}s")
        print(f"   PID: {os.getpid()}")
        
        # Setup shutdown handlers
        self.setup_signal_handlers()
        
        start_time = time.time()
        frame_count = 0
        frame_interval = 1.0 / fps
        
        try:
            # Try to import and run the specific module
            script_path = Path(__file__).parent / process_info['script']
            
            if script_path.exists():
                # Try to run the script's main function if it exists
                module_name = process_info['script'].replace('.py', '')
                try:
                    module = __import__(module_name)
                    if hasattr(module, 'main'):
                        print(f"🚀 Running {module_name}.main()")
                        module.main()
                    else:
                        print(f"🔄 Running generic visual loop for {process_id}")
                        self._run_generic_visual_loop(process_id, duration, fps)
                except ImportError as e:
                    print(f"⚠️ Could not import {module_name}: {e}")
                    self._run_generic_visual_loop(process_id, duration, fps)
            else:
                print(f"⚠️ Script not found: {script_path}")
                self._run_generic_visual_loop(process_id, duration, fps)
                
        except Exception as e:
            print(f"❌ Error in visual process {process_id}: {e}")
            return False
        finally:
            elapsed = time.time() - start_time
            print(f"🏁 Visual process '{process_id}' finished")
            print(f"   Runtime: {elapsed:.1f}s")
            print(f"   Frames: {frame_count}")
            print(f"   Avg FPS: {frame_count/elapsed:.1f}" if elapsed > 0 else "   Avg FPS: 0")
            
        return True
    
    def _run_generic_visual_loop(self, process_id: str, duration: int, fps: float):
        """Generic visual process loop"""
        start_time = time.time()
        frame_count = 0
        frame_interval = 1.0 / fps
        
        while self.running and not self.stop_event.is_set():
            current_time = time.time()
            elapsed = current_time - start_time
            
            if elapsed >= duration:
                print(f"✅ Process completed after {elapsed:.1f}s ({frame_count} frames)")
                break
                
            frame_count += 1
            
            # Simulate visual processing work
            cpu_load = 10 + (frame_count % 20)
            memory_usage = 50 + (frame_count % 30)
            
            print(f"🎬 {process_id} Frame {frame_count}: {elapsed:.1f}s elapsed, "
                  f"CPU: {cpu_load}%, MEM: {memory_usage}MB")
            
            # Wait for next frame
            time.sleep(frame_interval)
            
    def list_processes(self):
        """List all available visual processes"""
        print("🎬 DAWN Visual Processes:")
        print("=" * 50)
        
        for process_id, info in VISUAL_PROCESSES.items():
            print(f"  {process_id}")
            print(f"    Description: {info['description']}")
            print(f"    Category: {info['category']}")
            print(f"    Priority: {info['priority']}")
            print(f"    Script: {info['script']}")
            print()

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(description='DAWN Visual Process Launcher')
    parser.add_argument('process', nargs='?', help='Visual process to run')
    parser.add_argument('--duration', type=int, default=300, help='Run duration in seconds')
    parser.add_argument('--fps', type=float, default=10.0, help='Target frames per second')
    parser.add_argument('--list', action='store_true', help='List available processes')
    
    args = parser.parse_args()
    
    launcher = VisualProcessLauncher()
    
    if args.list:
        launcher.list_processes()
        return
    
    if not args.process:
        print("❌ No process specified")
        launcher.list_processes()
        return
    
    # Run the visual process
    success = launcher.run_visual_process(args.process, args.duration, args.fps)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 