#!/usr/bin/env python3
"""
DAWN with Consciousness GUI Launcher
===================================

Launches the DAWN unified system with the consciousness GUI integrated
Connects real DAWN consciousness data to the visualization interface
"""

import sys
import os
import time
import threading
import tkinter as tk
from pathlib import Path
import json
import struct
import mmap

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Add dawn-consciousness-gui to path
dawn_gui_path = project_root / "dawn-consciousness-gui"
if dawn_gui_path.exists():
    sys.path.insert(0, str(dawn_gui_path))

def start_dawn_unified_system():
    """Start the DAWN unified consciousness system"""
    print("🧠 Starting DAWN Unified Consciousness System...")
    
    try:
        from launcher_scripts.launch_dawn_unified import DAWNUnifiedLauncher
        
        # Create the unified launcher
        launcher = DAWNUnifiedLauncher()
        
        # Start the unified system in background thread
        def run_dawn_system():
            try:
                launcher._create_integrated_system()
                launcher._start_consciousness_monitoring()
                print("✅ DAWN consciousness system online")
            except Exception as e:
                print(f"⚠️ DAWN system error: {e}")
        
        # Start DAWN in background
        dawn_thread = threading.Thread(target=run_dawn_system, daemon=True)
        dawn_thread.start()
        
        return launcher
        
    except Exception as e:
        print(f"⚠️ Could not start DAWN unified system: {e}")
        return None

def create_consciousness_data_bridge(dawn_launcher=None):
    """Create a bridge that feeds DAWN data to the GUI"""
    
    class ConsciousnessDataBridge:
        def __init__(self):
            self.dawn_launcher = dawn_launcher
            self.mmap_path = project_root / "runtime" / "dawn_consciousness.mmap"
            self.running = True
            
            # Ensure runtime directory exists
            self.mmap_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Start data bridge thread
            self.bridge_thread = threading.Thread(target=self._bridge_loop, daemon=True)
            self.bridge_thread.start()
        
        def _bridge_loop(self):
            """Bridge DAWN consciousness data to memory map file"""
            while self.running:
                try:
                    # Get consciousness data from DAWN system
                    consciousness_data = self._get_dawn_consciousness_data()
                    
                    # Write to memory map file for GUI
                    self._write_consciousness_mmap(consciousness_data)
                    
                    time.sleep(0.0625)  # 16Hz update rate
                    
                except Exception as e:
                    print(f"Bridge error: {e}")
                    time.sleep(0.1)
        
        def _get_dawn_consciousness_data(self):
            """Extract consciousness data from running DAWN system"""
            try:
                if self.dawn_launcher and hasattr(self.dawn_launcher, 'systems'):
                    # Try to get data from DAWN systems
                    systems = self.dawn_launcher.systems
                    
                    data = {
                        'tick': int(time.time() * 16) % 10000,
                        'scup': 50.0,
                        'entropy': 0.5,
                        'mood_val': 0.0,
                        'mood_arousal': 0.3,
                        'timestamp': int(time.time() * 1000)
                    }
                    
                    # Try to get real entropy data
                    if 'autonomous_reactor' in systems and systems['autonomous_reactor']:
                        reactor = systems['autonomous_reactor']
                        if hasattr(reactor, 'current_entropy'):
                            data['entropy'] = float(reactor.current_entropy)
                    
                    # Try to get SCUP data
                    if hasattr(self.dawn_launcher, 'current_data'):
                        current_data = self.dawn_launcher.current_data
                        if 'scup' in current_data:
                            data['scup'] = float(current_data['scup'])
                        if 'mood' in current_data:
                            data['mood_val'] = float(current_data['mood'])
                    
                    return data
                    
            except Exception as e:
                print(f"Data extraction error: {e}")
            
            # Fallback simulation data
            return {
                'tick': int(time.time() * 16) % 10000,
                'scup': 50 + 20 * abs(hash(str(time.time())) % 100 - 50) / 50,
                'entropy': 0.3 + 0.4 * abs(hash(str(time.time() * 2)) % 100) / 100,
                'mood_val': 0.5,
                'mood_arousal': 0.3,
                'timestamp': int(time.time() * 1000)
            }
        
        def _write_consciousness_mmap(self, data):
            """Write consciousness data to memory map file"""
            try:
                # Create or update memory map file
                file_size = 1024  # 1KB should be enough
                
                # Create the file if it doesn't exist
                if not self.mmap_path.exists():
                    with open(self.mmap_path, 'wb') as f:
                        f.write(b'\x00' * file_size)
                
                # Write data to memory map
                with open(self.mmap_path, 'r+b') as f:
                    with mmap.mmap(f.fileno(), file_size) as mm:
                        # Write header
                        mm.seek(0)
                        mm.write(b'DAWN')  # Magic
                        mm.write(b'\x00' * 12)  # Reserved
                        mm.write(struct.pack('<I', data['tick']))  # Tick
                        mm.write(struct.pack('<Q', data['timestamp']))  # Timestamp
                        mm.write(b'\x00' * 4)  # Reserved
                        
                        # Write consciousness data
                        mm.seek(64)
                        mm.write(struct.pack('<f', data['scup']))
                        mm.write(struct.pack('<f', data['entropy']))
                        mm.write(struct.pack('<f', data['mood_val']))
                        mm.write(struct.pack('<f', data['mood_arousal']))
                        
            except Exception as e:
                print(f"Memory map write error: {e}")
        
        def stop(self):
            """Stop the data bridge"""
            self.running = False
    
    return ConsciousnessDataBridge()

def start_consciousness_gui(data_bridge=None):
    """Start the consciousness GUI"""
    print("🎨 Starting DAWN Consciousness GUI...")
    
    try:
        from simple_python_gui import DAWNConsciousnessGUI
        
        root = tk.Tk()
        
        # Handle window closing
        def on_closing():
            print("🛑 Shutting down DAWN Consciousness GUI...")
            if data_bridge:
                data_bridge.stop()
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Create GUI
        gui = DAWNConsciousnessGUI(root)
        root.title("DAWN Consciousness Monitor - Live Data")
        
        print("✅ DAWN Consciousness GUI ready")
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Failed to start GUI: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("🌅 DAWN with Consciousness GUI")
    print("=" * 50)
    print("🧠 Unified consciousness system + real-time GUI")
    print()
    
    # Start DAWN unified system
    dawn_launcher = start_dawn_unified_system()
    
    # Give DAWN time to initialize
    print("⏳ Waiting for DAWN consciousness to initialize...")
    time.sleep(3)
    
    # Create data bridge
    print("🔗 Creating consciousness data bridge...")
    data_bridge = create_consciousness_data_bridge(dawn_launcher)
    
    # Give bridge time to start
    time.sleep(1)
    
    # Start GUI
    try:
        success = start_consciousness_gui(data_bridge)
        return 0 if success else 1
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        if data_bridge:
            data_bridge.stop()
        return 0
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if data_bridge:
            data_bridge.stop()
        return 1

if __name__ == "__main__":
    exit(main()) 