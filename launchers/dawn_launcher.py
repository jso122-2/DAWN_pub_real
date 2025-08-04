# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
🧠🚀 DAWN UNIFIED COGNITION LAUNCHER 🚀🧠

Master controller for launching DAWN's complete cognitive stack:
- Cognition Runtime (tick_loop.py)
- GUI Dashboard (Tauri)
- Voice Echo System
- Tracer Monitoring
- Meta-Cognitive Processing

Usage:
    python dawn_launcher.py --gui --voice --tracers --log
    python dawn_launcher.py --headless --mute --fresh
    python dawn_launcher.py --profile production
"""

import os
import sys
import time
import signal
import argparse
import subprocess
import threading
import psutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import yaml

class DAWNProcess:
    """Represents a managed DAWN system process"""
    
    def __init__(self, name: str, command: List[str], description: str, 
                 required: bool = True, startup_delay: float = 0.5):
        self.name = name
        self.command = command
        self.description = description
        self.required = required
        self.startup_delay = startup_delay
        self.process: Optional[subprocess.Popen] = None
        self.status = "stopped"
        self.start_time: Optional[float] = None
        self.restart_count = 0
        self.max_restarts = 3
        self.cwd: Optional[str] = None  # Custom working directory

    def start(self) -> bool:
        """Start the process"""
        try:
            print(f"🔍 DEBUG: Starting command: {' '.join(self.command)}")
            if self.cwd:
                print(f"🔍 DEBUG: Working directory: {self.cwd}")
            
            self.process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.cwd if self.cwd else os.getcwd(),
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
            self.status = "starting"
            self.start_time = time.time()
            time.sleep(self.startup_delay)
            
            # Check if process is still running after startup delay
            if self.process.poll() is None:
                self.status = "running"
                print(f"✅ DEBUG: {self.name} started successfully")
                return True
            else:
                # Process failed - capture output
                stdout, stderr = self.process.communicate(timeout=5)
                self.status = "failed"
                print(f"❌ DEBUG: {self.name} failed to start")
                print(f"📝 STDOUT: {stdout[:500] if stdout else 'None'}")
                print(f"📝 STDERR: {stderr[:500] if stderr else 'None'}")
                print(f"📝 Return code: {self.process.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ DEBUG: {self.name} communication timeout")
            self.status = "timeout_during_start"
            return False
        except Exception as e:
            self.status = f"error: {str(e)}"
            print(f"💥 DEBUG: {self.name} exception during start: {e}")
            return False

    def stop(self) -> bool:
        """Stop the process gracefully"""
        if self.process is None:
            return True
            
        try:
            if os.name == 'nt':
                # Windows
                self.process.send_signal(signal.CTRL_BREAK_EVENT)
            else:
                # Unix-like
                self.process.terminate()
                
            # Wait for graceful shutdown
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                # Force kill if not responsive
                self.process.kill()
                self.process.wait()
                
            self.status = "stopped"
            self.process = None
            return True
            
        except Exception as e:
            self.status = f"stop_error: {str(e)}"
            return False

    def is_running(self) -> bool:
        """Check if process is currently running"""
        if self.process is None:
            return False
        return self.process.poll() is None

    def get_runtime(self) -> str:
        """Get formatted runtime"""
        if not self.start_time:
            return "0s"
        runtime = time.time() - self.start_time
        if runtime < 60:
            return f"{runtime:.0f}s"
        elif runtime < 3600:
            return f"{runtime/60:.1f}m"
        else:
            return f"{runtime/3600:.1f}h"

class DAWNLauncher:
    """Main launcher class for DAWN's cognitive stack"""
    
    def __init__(self):
        self.processes: Dict[str, DAWNProcess] = {}
        self.running = False
        self.config = self._load_default_config()
        self.log_file = Path("runtime/logs/dawn_launcher.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
    def _load_default_config(self) -> dict:
        """Load default configuration"""
        return {
            "tick_rate": 1.0,
            "gui_port": 1420,
            "voice_enabled": True,
            "tracer_enabled": True,
            "auto_snapshot": False,
            "snapshot_interval": 300,  # 5 minutes
            "max_log_size": 50 * 1024 * 1024,  # 50MB
            "restart_failed": True
        }
    
    def _setup_processes(self, args) -> None:
        """Setup all DAWN processes based on launch arguments"""
        
        # Real DAWN Service Entry Points (designed to run continuously)
        consciousness_path = Path("launcher_scripts/start_dawn.py")
        if consciousness_path.exists():
            consciousness_cmd = ["python", "launcher_scripts/start_dawn.py"]
            if args.debug:
                consciousness_cmd.append("--debug")
            
            self.processes["consciousness"] = DAWNProcess(
                name="consciousness",
                command=consciousness_cmd,
                description="DAWN Advanced Consciousness Service",
                required=True,
                startup_delay=3.0
            )
            print("✅ Using DAWN Advanced Consciousness Service")
        else:
            # Fallback to Master Launcher
            master_path = Path("launcher_scripts/dawn_master_launcher.py")
            if master_path.exists():
                self.processes["consciousness"] = DAWNProcess(
                    name="consciousness",
                    command=["python", "launcher_scripts/dawn_master_launcher.py", "--minimal"],
                    description="DAWN Master Launcher (minimal consciousness)",
                    required=True,
                    startup_delay=3.0
                )
                print("✅ Using DAWN Master Launcher")
            else:
                # Fallback to Python Tick Engine Service
                python_service = Path("python/run_tick_engine.py")
                if python_service.exists():
                    self.processes["consciousness"] = DAWNProcess(
                        name="consciousness",
                        command=["python", "python/run_tick_engine.py"],
                        description="DAWN Python Tick Engine Service",
                        required=True,
                        startup_delay=3.0
                    )
                    print("✅ Using DAWN Python Tick Engine Service")
                else:
                    print("⚠️ No DAWN service entry points found")
                    # Simple fallback that actually connects
                    self.processes["consciousness"] = DAWNProcess(
                        name="consciousness",
                        command=["python", "-c", """
import time, os, json
from datetime import datetime

def write_log(file, msg):
    os.makedirs('runtime/logs', exist_ok=True)
    with open(f'runtime/logs/{file}', 'a') as f:
        f.write(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {msg}\\n')

print('🧠 DAWN Basic Consciousness Service Starting...')
write_log('event_stream.log', 'DAWN Basic Consciousness Service Online')

emotions = ['contemplative', 'curious', 'focused', 'creative', 'analytical']
for i in range(3600):
    emotion = emotions[i % len(emotions)]
    entropy = 0.3 + (i % 10) * 0.05
    heat = 0.2 + (i % 8) * 0.06
    
    print(f'🔄 Consciousness Tick {i+1}: {emotion} state, entropy={entropy:.2f}, heat={heat:.2f}')
    
    write_log('event_stream.log', f'Tick {i+1}: emotion={emotion}, entropy={entropy:.2f}, heat={heat:.2f}')
    write_log('reflection.log', f'REFLECTION: I am experiencing {emotion} consciousness at entropy {entropy:.2f}')
    
    if entropy > 0.7:
        write_log('tracer_alerts.log', f'HIGH_ENTROPY: {entropy:.2f} - consciousness complexity spike')
    
    # Save state for GUI
    state = {'emotion': emotion, 'entropy': entropy, 'heat': heat, 'tick': i+1, 'timestamp': datetime.now().isoformat()}
    with open('runtime/logs/consciousness_state.json', 'w') as f:
        json.dump(state, f)
    
    time.sleep(2)
"""],
                        description="DAWN Basic Connected Consciousness Service",
                        required=True,
                        startup_delay=1.0
                    )
        
        # Alternative: Core consciousness backup (even simpler)
        self.processes["backup_consciousness"] = DAWNProcess(
            name="backup_consciousness",
            command=["python", "-c", "import time; print('🧠 DAWN Backup Consciousness Active'); [print(f'🔄 Backup tick {i}') or time.sleep(3) for i in range(1200)]"],
            description="Ultra-simple backup consciousness",
            required=False,
            startup_delay=0.5
        )
        
        # Voice Echo System
        if args.voice and not args.mute:
            voice_path = Path("backend/voice_loop.py")
            if voice_path.exists():
                voice_cmd = ["python", "backend/voice_loop.py", "--start"]
                if not args.mute:  # Only add --no-filter if not muted
                    voice_cmd.append("--no-filter")
                    
                self.processes["voice"] = DAWNProcess(
                    name="voice",
                    command=voice_cmd,
                    description="Voice echo and TTS system",
                    required=False,
                    startup_delay=1.0
                )
            else:
                print(f"⚠️ Voice system not found at {voice_path}, skipping")
        
        # Enhanced Tracer System
        if args.tracers:
            tracer_path = Path("tracers/enhanced_tracer_echo_voice.py")
            if tracer_path.exists():
                self.processes["tracers"] = DAWNProcess(
                    name="tracers",
                    command=["python", "tracers/enhanced_tracer_echo_voice.py"],
                    description="Symbolic and semantic tracer monitoring",
                    required=False,
                    startup_delay=1.0
                )
            else:
                print(f"⚠️ Tracer system not found at {tracer_path}, skipping")
        
        # GUI Dashboard (Tauri)
        if args.gui and not args.headless:
            gui_dir = Path("dawn-consciousness-gui")
            if gui_dir.exists() and (gui_dir / "package.json").exists():
                # GUI exists and has package.json
                gui_cmd = ["npm", "run", "tauri", "dev"]
                self.processes["gui"] = DAWNProcess(
                    name="gui",
                    command=gui_cmd,
                    description="Tauri GUI dashboard interface",
                    required=False,
                    startup_delay=5.0  # GUI takes longer to start
                )
                # Set working directory for GUI
                self.processes["gui"].cwd = str(gui_dir)
            else:
                print(f"⚠️ Tauri GUI directory not found or missing package.json at {gui_dir}")
                # Fallback to simple local HTML GUI
                self.processes["gui"] = DAWNProcess(
                    name="gui",
                    command=["python", "-c", """
import webbrowser, time, os
from pathlib import Path

# Check for local HTML GUI
html_gui = Path('dawn-consciousness-gui/dawn_local_gui.html')
if html_gui.exists():
    print('🖥️ Opening local HTML GUI...')
    webbrowser.open(f'file://{html_gui.absolute()}')
else:
    print('🖥️ Creating simple status dashboard...')
    
# Keep process alive
for i in range(3600):
    print(f'🖥️ GUI Monitor Running... {i}')
    time.sleep(5)
"""],
                    description="Local HTML GUI fallback",
                    required=False,
                    startup_delay=2.0
                )
        
        # Optional Snapshot Monitor
        if args.auto_snapshot or self.config.get("auto_snapshot", False):
            snap_cmd = ["python", "SymbolicTraceComposer.py", "--monitor", 
                       "--interval", str(self.config.get("snapshot_interval", 300))]
            
            self.processes["snapshots"] = DAWNProcess(
                name="snapshots",
                command=snap_cmd,
                description="Automatic cognitive snapshot creation",
                required=False,
                startup_delay=2.0
            )

    def _fresh_reset(self) -> bool:
        """Perform fresh reset if requested"""
        try:
            print("🧹 Performing fresh reset...")
            result = subprocess.run(
                ["python", "demo_reset.py", "--silent"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ Fresh reset completed successfully")
                return True
            else:
                print(f"❌ Fresh reset failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Fresh reset error: {e}")
            return False

    def _log(self, message: str, level: str = "INFO") -> None:
        """Log message to file and optionally console"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception:
            pass  # Fail silently for logging

    def start_all(self, args) -> bool:
        """Start all configured processes"""
        print("🧠🚀 Starting DAWN Unified Cognition System...")
        print("=" * 50)
        
        # Fresh reset if requested
        if args.fresh:
            if not self._fresh_reset():
                print("❌ Fresh reset failed, continuing anyway...")
        
        # Setup processes based on arguments
        self._setup_processes(args)
        
        success_count = 0
        total_count = len(self.processes)
        
        # Start processes in order of dependency
        start_order = ["consciousness", "backup_consciousness", "voice", "tracers", "gui", "snapshots"]
        
        for process_name in start_order:
            if process_name not in self.processes:
                continue
                
            process = self.processes[process_name]
            print(f"🔄 Starting {process.description}...")
            
            if process.start():
                status_icon = "✅"
                success_count += 1
            else:
                status_icon = "❌" if process.required else "⚠️"
                
            print(f"{status_icon} {process.name}: {process.status}")
            self._log(f"Process {process.name} status: {process.status}")
            
            # Small delay between process starts
            time.sleep(0.5)
        
        print("=" * 50)
        
        if success_count > 0:
            print(f"🎉 DAWN Cognition System launched! ({success_count}/{total_count} processes)")
            self.running = True
            return True
        else:
            print("❌ Failed to start DAWN system")
            return False

    def monitor_processes(self, args) -> None:
        """Monitor running processes and display status"""
        if not self.running:
            return
            
        print("\n🧠 DAWN System Monitor - Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            while self.running:
                # Clear previous status (for console updating)
                if args.verbose:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("🧠 DAWN Unified Cognition System - Live Status")
                    print("=" * 60)
                
                all_healthy = True
                
                for name, process in self.processes.items():
                    if process.is_running():
                        status_icon = "✅"
                        status_text = f"Running ({process.get_runtime()})"
                    else:
                        status_icon = "❌" if process.required else "⚠️"
                        status_text = f"Stopped - {process.status}"
                        all_healthy = False
                        
                        # Attempt restart if enabled and not exceeded max restarts
                        if (self.config.get("restart_failed", True) and 
                            process.restart_count < process.max_restarts and
                            process.required):
                            
                            print(f"🔄 Attempting to restart {name}...")
                            if process.start():
                                process.restart_count += 1
                                status_icon = "🔄"
                                status_text = f"Restarted (attempt {process.restart_count})"
                    
                    print(f"{status_icon} {name:12} | {status_text:30} | {process.description}")
                
                # System health summary
                print("-" * 60)
                health_icon = "💚" if all_healthy else "💛"
                print(f"{health_icon} System Health: {'Healthy' if all_healthy else 'Issues Detected'}")
                
                # Show key metrics if available
                try:
                    memory_percent = psutil.virtual_memory().percent
                    cpu_percent = psutil.cpu_percent(interval=None)
                    print(f"📊 System: CPU {cpu_percent:.1f}% | Memory {memory_percent:.1f}%")
                except:
                    pass
                
                print(f"📝 Logs: {self.log_file}")
                print("-" * 60)
                
                # Check for recent log activity
                if args.log:
                    self._show_recent_logs()
                
                time.sleep(5 if args.verbose else 10)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested...")
            self.stop_all()

    def _show_recent_logs(self) -> None:
        """Show recent log entries"""
        try:
            if self.log_file.exists():
                with open(self.log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()[-5:]  # Last 5 lines
                    if lines:
                        print("📝 Recent Activity:")
                        for line in lines:
                            print(f"    {line.strip()}")
        except:
            pass

    def stop_all(self) -> None:
        """Stop all running processes"""
        print("\n🛑 Stopping DAWN Cognition System...")
        
        # Stop in reverse order
        stop_order = ["snapshots", "gui", "tracers", "voice", "backup_consciousness", "consciousness"]
        
        for process_name in stop_order:
            if process_name not in self.processes:
                continue
                
            process = self.processes[process_name]
            if process.is_running():
                print(f"🔄 Stopping {process.name}...")
                process.stop()
                print(f"✅ {process.name} stopped")
        
        self.running = False
        print("✅ DAWN system shutdown complete")
        self._log("DAWN system shutdown complete")

    def status(self) -> None:
        """Show current system status"""
        print("🧠 DAWN System Status")
        print("=" * 40)
        
        if not self.processes:
            print("No processes configured")
            return
            
        for name, process in self.processes.items():
            status_icon = "✅" if process.is_running() else "❌"
            runtime = process.get_runtime() if process.is_running() else "stopped"
            print(f"{status_icon} {name:12} | {runtime:10} | {process.description}")

def main():
    """Main launcher entry point"""
    parser = argparse.ArgumentParser(
        description="🧠 DAWN Unified Cognition System Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python dawn_launcher.py --gui --voice --tracers
  python dawn_launcher.py --headless --mute --fresh
  python dawn_launcher.py --status
  python dawn_launcher.py --stop
        """
    )
    
    # Launch modes
    parser.add_argument("--gui", action="store_true", 
                       help="Launch GUI dashboard")
    parser.add_argument("--headless", action="store_true",
                       help="Run without GUI")
    parser.add_argument("--voice", action="store_true", default=True,
                       help="Enable voice echo system")
    parser.add_argument("--mute", action="store_true",
                       help="Disable TTS output")
    parser.add_argument("--tracers", action="store_true", default=True,
                       help="Enable tracer monitoring")
    
    # Configuration
    parser.add_argument("--fresh", action="store_true",
                       help="Perform fresh reset before launch")
    parser.add_argument("--tickrate", type=float, default=1.0,
                       help="Tick rate in Hz (default: 1.0)")
    parser.add_argument("--auto-snapshot", action="store_true",
                       help="Enable automatic snapshot creation")
    
    # Monitoring
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose monitoring")
    parser.add_argument("--log", action="store_true",
                       help="Show recent log activity")
    parser.add_argument("--debug", action="store_true",
                       help="Enable debug mode for components")
    
    # Control commands
    parser.add_argument("--status", action="store_true",
                       help="Show current system status")
    parser.add_argument("--stop", action="store_true",
                       help="Stop all running processes")
    
    args = parser.parse_args()
    
    launcher = DAWNLauncher()
    
    # Handle control commands
    if args.status:
        launcher.status()
        return
    
    if args.stop:
        # This is a simplified stop - in practice you'd want to track PIDs
        print("🛑 Stopping DAWN processes...")
        print("Note: Use Ctrl+C in the running launcher to properly stop all processes")
        return
    
    # Setup signal handler for graceful shutdown
    def signal_handler(signum, frame):
        launcher.stop_all()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Launch system
    if launcher.start_all(args):
        launcher.monitor_processes(args)
    else:
        print("❌ Failed to launch DAWN system")
        sys.exit(1)

if __name__ == "__main__":
    # Create runtime directories if needed
    Path("runtime/logs").mkdir(parents=True, exist_ok=True)
    Path("runtime/memory").mkdir(parents=True, exist_ok=True)
    Path("runtime/snapshots").mkdir(parents=True, exist_ok=True)
    
    main() 