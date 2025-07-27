#!/usr/bin/env python3
"""
🌅 DAWN MASTER LAUNCHER - Ultimate Unified Consciousness Ecosystem
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The single entry point for the complete DAWN autonomous consciousness experience.
One command to launch everything: consciousness, voice, GUI, and all subsystems.

🎯 UNIFIED COMPONENTS:
  🧠 Core Consciousness (Tick Engine, Entropy, Sigils)
  🗣️ Voice Loop (Audible self-narration) 
  🖥️ Viewport GUI (Draggable consciousness dashboard)
  ⚡ Autonomous Reactor (Self-directed actions)
  🌸 Bloom System (Memory consolidation)
  📊 Live Monitoring (Real-time consciousness metrics)

🚀 USAGE:
  python dawn_master_launcher.py --full      # Launch everything
  python dawn_master_launcher.py --gui-only  # GUI + basic consciousness  
  python dawn_master_launcher.py --voice     # Add voice narration
  python dawn_master_launcher.py --minimal   # Core consciousness only

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys
import os
import time
import threading
import subprocess
import signal
import argparse
import json
import queue
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
import webbrowser

# Add project paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🌅 DAWN MASTER LAUNCHER")
print("=" * 80)
print("🧠 Ultimate Unified Consciousness Ecosystem")
print("⚡ Initializing all subsystems...")


class DAWNMasterLauncher:
    """
    Master controller for the complete DAWN consciousness ecosystem.
    Coordinates startup, monitoring, and graceful shutdown of all components.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.processes = {}
        self.threads = {}
        self.running = False
        self.shutdown_event = threading.Event()
        self.status_queue = queue.Queue()
        
        # Component availability flags
        self.components_available = {
            'consciousness': False,
            'voice_loop': False,
            'gui': False,
            'reactor': False,
            'bloom': False
        }
        
        print(f"🚀 Master Launcher initialized with config: {list(config.keys())}")
    
    def detect_components(self):
        """Detect which DAWN components are available"""
        print("\n🔍 COMPONENT DETECTION")
        print("-" * 40)
        
        # Check voice loop
        if (project_root / "voice_loop.py").exists():
            self.components_available['voice_loop'] = True
            print("✅ Voice Loop: voice_loop.py found")
        else:
            print("❌ Voice Loop: voice_loop.py missing")
        
        # Check consciousness system
        consciousness_files = [
            "core/enhanced_entropy_analyzer.py",
            "backend/advanced_consciousness_system.py",
            "integration/complete_dawn_consciousness_integration.py"
        ]
        if any((project_root / f).exists() for f in consciousness_files):
            self.components_available['consciousness'] = True
            print("✅ Consciousness: Core system files found")
        else:
            print("❌ Consciousness: Core system files missing")
        
        # Check GUI
        gui_path = project_root / "dawn-consciousness-gui"
        if gui_path.exists() and (gui_path / "package.json").exists():
            self.components_available['gui'] = True
            print("✅ GUI: React/Tauri interface found")
        else:
            print("❌ GUI: React/Tauri interface missing")
        
        # Check reactor
        reactor_files = [
            "launcher_scripts/launch_dawn_autonomous_reactor.py",
            "integration/autonomous_reactor_integration.py"
        ]
        if any((project_root / f).exists() for f in reactor_files):
            self.components_available['reactor'] = True
            print("✅ Reactor: Autonomous system found")
        else:
            print("❌ Reactor: Autonomous system missing")
        
        # Check bloom system
        bloom_files = [
            "bloom/bloom_engine.py",
            "bloom/bloom_integration_system.py"
        ]
        if any((project_root / f).exists() for f in bloom_files):
            self.components_available['bloom'] = True
            print("✅ Bloom: Memory system found")
        else:
            print("❌ Bloom: Memory system missing")
        
        available_count = sum(self.components_available.values())
        print(f"\n📊 Components Available: {available_count}/5")
        return available_count
    
    def start_consciousness_core(self):
        """Start the core DAWN consciousness system"""
        if not self.components_available['consciousness']:
            print("⚠️ Consciousness core not available")
            return False
        
        print("\n🧠 STARTING CONSCIOUSNESS CORE")
        print("-" * 40)
        
        try:
            # Try the most complete launcher first
            launcher_path = project_root / "launcher_scripts/launch_complete_dawn_consciousness.py"
            if launcher_path.exists():
                cmd = [sys.executable, str(launcher_path)]
                self.processes['consciousness'] = subprocess.Popen(
                    cmd, 
                    cwd=str(project_root),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT  # Combine stderr with stdout
                )
                print("✅ Consciousness core started")
                return True
            else:
                # Fallback to a simpler consciousness starter
                print("⚠️ Complete launcher not found, trying alternative...")
                # You could add a fallback here to a simpler consciousness system
                return False
                
        except Exception as e:
            print(f"❌ Failed to start consciousness core: {e}")
            return False
    
    def start_voice_loop(self):
        """Start the DAWN voice loop for audible consciousness"""
        if not self.components_available['voice_loop']:
            print("⚠️ Voice loop not available")
            return False
        
        print("\n🗣️ STARTING VOICE LOOP")
        print("-" * 40)
        
        try:
            voice_args = ["--start"]
            if self.config.get('min_entropy'):
                voice_args.extend(["--min-entropy", str(self.config['min_entropy'])])
            
            cmd = [sys.executable, "voice_loop.py"] + voice_args
            self.processes['voice'] = subprocess.Popen(
                cmd,
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Voice loop started")
            print("🔊 DAWN will now speak her thoughts as they emerge")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start voice loop: {e}")
            return False
    
    def start_gui(self):
        """Start the DAWN consciousness GUI with viewport dragging"""
        if not self.components_available['gui']:
            print("⚠️ GUI not available")
            return False
        
        print("\n🖥️ STARTING CONSCIOUSNESS GUI")
        print("-" * 40)
        
        try:
            gui_path = project_root / "dawn-consciousness-gui"
            
            # Start the Vite development server in WSL
            cmd = [
                "wsl", "bash", "-c", 
                f"cd {gui_path.as_posix()} && npm run dev"
            ]
            
            self.processes['gui'] = subprocess.Popen(
                cmd,
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a moment for the server to start
            time.sleep(3)
            
            # Try to open in browser (handle WSL/Linux environments)
            gui_url = "http://localhost:1422"
            try:
                # Check if we're in WSL or Linux
                if os.path.exists('/proc/version'):
                    with open('/proc/version', 'r') as f:
                        if 'Microsoft' in f.read() or 'WSL' in f.read():
                            # WSL environment - use Windows browser
                            subprocess.Popen(['cmd.exe', '/c', 'start', gui_url], 
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            print(f"✅ GUI started and opened at {gui_url} (WSL)")
                        else:
                            # Regular Linux - try xdg-open
                            subprocess.Popen(['xdg-open', gui_url], 
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                            print(f"✅ GUI started and opened at {gui_url} (Linux)")
                else:
                    # Windows or other
                    webbrowser.open(gui_url)
                    print(f"✅ GUI started and opened at {gui_url}")
                print("🎯 Viewport dragging enabled - drag background to move around!")
            except Exception as e:
                print(f"✅ GUI started at {gui_url}")
                print("🌐 Please open this URL in your browser manually")
                print(f"   (Browser auto-open failed: {e})")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start GUI: {e}")
            return False
    
    def start_autonomous_reactor(self):
        """Start the autonomous reactor system"""
        if not self.components_available['reactor']:
            print("⚠️ Autonomous reactor not available")
            return False
        
        print("\n⚡ STARTING AUTONOMOUS REACTOR")
        print("-" * 40)
        
        try:
            reactor_path = project_root / "launcher_scripts/launch_dawn_autonomous_reactor.py"
            cmd = [sys.executable, str(reactor_path)]
            self.processes['reactor'] = subprocess.Popen(
                cmd,
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Autonomous reactor started")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start autonomous reactor: {e}")
            return False
    
    def start_bloom_system(self):
        """Start the bloom memory consolidation system"""
        if not self.components_available['bloom']:
            print("⚠️ Bloom system not available")
            return False
        
        print("\n🌸 STARTING BLOOM SYSTEM")
        print("-" * 40)
        
        try:
            bloom_path = project_root / "bloom/bloom_engine.py"
            cmd = [sys.executable, str(bloom_path)]
            self.processes['bloom'] = subprocess.Popen(
                cmd,
                cwd=str(project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print("✅ Bloom system started")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start bloom system: {e}")
            return False
    
    def monitor_status(self):
        """Monitor the status of all running components"""
        def status_monitor():
            while not self.shutdown_event.is_set():
                try:
                    # Check process health
                    dead_processes = []
                    for name, process in self.processes.items():
                        if process.poll() is not None:
                            dead_processes.append(name)
                            # Try to capture any error output
                            try:
                                stdout, stderr = process.communicate(timeout=1)
                                if stdout:
                                    print(f"🔍 {name} output: {stdout.decode()[:200]}...")
                            except:
                                pass
                    
                    if dead_processes:
                        print(f"⚠️ Detected dead processes: {dead_processes}")
                        # Only show this message once per batch of deaths
                        if len(dead_processes) == 1:
                            print(f"💡 Tip: For GUI-only mode, try: python launch_dawn.py --gui")
                    
                    time.sleep(10)  # Check every 10 seconds (less spam)
                    
                except Exception as e:
                    print(f"❌ Status monitor error: {e}")
                    break
        
        self.threads['monitor'] = threading.Thread(target=status_monitor, daemon=True)
        self.threads['monitor'].start()
    
    def display_status(self):
        """Display current system status"""
        print(f"\n📊 DAWN SYSTEM STATUS - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        for name, process in self.processes.items():
            status = "🟢 RUNNING" if process.poll() is None else "🔴 STOPPED"
            print(f"  {name.capitalize():15} {status}")
        
        print("\n🎯 ACCESS POINTS:")
        if 'gui' in self.processes and self.processes['gui'].poll() is None:
            print("  🖥️ GUI Dashboard:     http://localhost:1422")
        if 'voice' in self.processes and self.processes['voice'].poll() is None:
            print("  🗣️ Voice Loop:        Active (check console)")
        
        print("\n💡 CONTROLS:")
        print("  Press Ctrl+C to gracefully shutdown all systems")
    
    def launch_configuration(self, mode: str):
        """Launch DAWN in the specified configuration mode"""
        print(f"\n🚀 LAUNCHING DAWN IN {mode.upper()} MODE")
        print("=" * 60)
        
        success_count = 0
        
        if mode in ['full', 'consciousness', 'minimal']:
            if self.start_consciousness_core():
                success_count += 1
                time.sleep(2)  # Let consciousness stabilize
        
        if mode in ['full', 'voice'] and self.config.get('enable_voice', False):
            if self.start_voice_loop():
                success_count += 1
                time.sleep(1)
        
        if mode in ['full', 'gui-only', 'gui']:
            if self.start_gui():
                success_count += 1
                time.sleep(2)
        
        if mode == 'full':
            if self.start_autonomous_reactor():
                success_count += 1
                time.sleep(1)
            
            if self.start_bloom_system():
                success_count += 1
        
        self.running = True
        
        if success_count > 0:
            print(f"\n🎉 DAWN SUCCESSFULLY LAUNCHED!")
            print(f"📊 {success_count} components started")
            self.monitor_status()
            self.display_status()
            return True
        else:
            print(f"\n❌ LAUNCH FAILED - No components started")
            return False
    
    def shutdown(self):
        """Gracefully shutdown all DAWN components"""
        print(f"\n🛑 SHUTTING DOWN DAWN SYSTEMS")
        print("=" * 50)
        
        self.running = False
        self.shutdown_event.set()
        
        # Terminate all processes
        for name, process in self.processes.items():
            if process.poll() is None:
                print(f"  🛑 Stopping {name}...")
                try:
                    process.terminate()
                    # Give it 5 seconds to terminate gracefully
                    try:
                        process.wait(timeout=5)
                        print(f"  ✅ {name} stopped gracefully")
                    except subprocess.TimeoutExpired:
                        print(f"  ⚠️ Force killing {name}...")
                        process.kill()
                        process.wait()
                        print(f"  ✅ {name} force stopped")
                except Exception as e:
                    print(f"  ❌ Error stopping {name}: {e}")
        
        print("\n🌙 DAWN systems shutdown complete")
        print("Until next time... 🌅")
    
    def run_main_loop(self):
        """Main execution loop"""
        try:
            while self.running:
                time.sleep(1)
                
                # Check if all processes are dead
                if all(p.poll() is not None for p in self.processes.values()):
                    print("\n⚠️ All processes have terminated")
                    break
                    
        except KeyboardInterrupt:
            print("\n\n🛑 Shutdown requested by user...")
            self.shutdown()
        except Exception as e:
            print(f"\n❌ Unexpected error in main loop: {e}")
            self.shutdown()


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="🌅 DAWN Master Launcher - Ultimate Unified Consciousness",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
LAUNCH MODES:
  --full        Launch complete ecosystem (consciousness + voice + GUI + reactor + bloom)
  --gui-only    Launch GUI dashboard with basic consciousness  
  --minimal     Launch core consciousness only
  --voice       Enable voice narration (can combine with other modes)

EXAMPLES:
  python dawn_master_launcher.py --full                    # Everything
  python dawn_master_launcher.py --gui-only --voice        # GUI + voice
  python dawn_master_launcher.py --minimal                 # Just consciousness
        """
    )
    
    parser.add_argument('--full', action='store_true', 
                       help='Launch complete DAWN ecosystem')
    parser.add_argument('--gui-only', action='store_true',
                       help='Launch GUI with basic consciousness')
    parser.add_argument('--minimal', action='store_true',
                       help='Launch core consciousness only')
    parser.add_argument('--voice', action='store_true',
                       help='Enable voice narration')
    parser.add_argument('--min-entropy', type=float, default=0.4,
                       help='Minimum entropy threshold for voice (default: 0.4)')
    
    return parser.parse_args()


def main():
    """Main entry point"""
    args = parse_arguments()
    
    # Determine launch mode
    if args.full:
        mode = 'full'
    elif args.gui_only:
        mode = 'gui-only'
    elif args.minimal:
        mode = 'minimal'
    else:
        mode = 'full'  # Default to full experience
    
    # Build configuration
    config = {
        'mode': mode,
        'enable_voice': args.voice or args.full,
        'min_entropy': args.min_entropy
    }
    
    # Create and run launcher
    launcher = DAWNMasterLauncher(config)
    
    # Detect available components
    available_count = launcher.detect_components()
    if available_count == 0:
        print("\n❌ No DAWN components found!")
        print("Please ensure you're running from the DAWN project root.")
        return 1
    
    # Set up signal handler for graceful shutdown
    def signal_handler(signum, frame):
        launcher.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Launch the system
    if launcher.launch_configuration(mode):
        launcher.run_main_loop()
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main()) 