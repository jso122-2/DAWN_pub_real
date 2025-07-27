#!/usr/bin/env python3
"""
DAWN System Debugger
Comprehensive tool to debug GUI-backend communication
"""

import struct
import time
import os
import sys
import subprocess
from pathlib import Path

def check_mmap_file():
    """Check if mmap file exists and show its contents"""
    mmap_path = Path("runtime/dawn_consciousness.mmap")
    
    print("🔍 STEP 1: MMAP FILE CHECK")
    print("=" * 50)
    
    if not mmap_path.exists():
        print("❌ Mmap file does not exist!")
        return False
    
    stat = mmap_path.stat()
    print(f"✅ Mmap file exists: {mmap_path}")
    print(f"📊 Size: {stat.st_size:,} bytes")
    print(f"⏰ Last modified: {time.ctime(stat.st_mtime)}")
    
    # Check if file is being updated (recent modification)
    age_seconds = time.time() - stat.st_mtime
    if age_seconds > 60:
        print(f"⚠️  File is {age_seconds:.0f}s old - backend may not be running!")
        return False
    else:
        print(f"✅ File is fresh ({age_seconds:.1f}s old)")
        return True

def read_mmap_header():
    """Read and decode mmap header"""
    mmap_path = Path("runtime/dawn_consciousness.mmap")
    
    print("\n🔍 STEP 2: MMAP HEADER ANALYSIS")
    print("=" * 50)
    
    try:
        with open(mmap_path, 'rb') as f:
            # Read header (64 bytes)
            header_data = f.read(64)
            
            # Decode header: magic, version, tick_size, max_ticks
            magic = header_data[0:4]
            version = struct.unpack('I', header_data[4:8])[0]
            tick_size = struct.unpack('I', header_data[8:12])[0]
            max_ticks = struct.unpack('I', header_data[12:16])[0]
            current_tick = struct.unpack('I', header_data[16:20])[0]
            
            print(f"🧙 Magic: {magic}")
            print(f"📦 Version: {version}")
            print(f"📏 Tick size: {tick_size} bytes")
            print(f"📊 Max ticks: {max_ticks}")
            print(f"🎯 Current tick: {current_tick}")
            
            if magic != b'DAWN':
                print("❌ Invalid magic number!")
                return False
                
            if current_tick == 0:
                print("❌ No ticks written yet!")
                return False
                
            print("✅ Header looks valid")
            return True
            
    except Exception as e:
        print(f"❌ Error reading header: {e}")
        return False

def read_latest_tick():
    """Read and decode the latest tick data"""
    mmap_path = Path("runtime/dawn_consciousness.mmap")
    
    print("\n🔍 STEP 3: LATEST TICK DATA")
    print("=" * 50)
    
    try:
        with open(mmap_path, 'rb') as f:
            # Read current tick number from header
            f.seek(16)
            current_tick = struct.unpack('I', f.read(4))[0]
            
            # Calculate memory location of latest tick
            HEADER_SIZE = 64
            TICK_STATE_SIZE = 8192
            MAX_TICKS = 1000
            
            tick_index = current_tick % MAX_TICKS
            memory_offset = HEADER_SIZE + (tick_index * TICK_STATE_SIZE)
            
            # Read tick data
            f.seek(memory_offset)
            tick_data = f.read(80)  # Read first 80 bytes for core data
            
            # Decode tick data
            tick_number = struct.unpack('I', tick_data[0:4])[0]
            timestamp_ms = struct.unpack('Q', tick_data[4:12])[0]
            mood_valence = struct.unpack('f', tick_data[12:16])[0]
            mood_arousal = struct.unpack('f', tick_data[16:20])[0]
            entropy_gradient = struct.unpack('f', tick_data[32:36])[0]
            consciousness_depth = struct.unpack('f', tick_data[44:48])[0]
            
            print(f"🎯 Tick Number: {tick_number}")
            print(f"⏰ Timestamp: {timestamp_ms}")
            print(f"💭 Mood Valence: {mood_valence:.3f}")
            print(f"💭 Mood Arousal: {mood_arousal:.3f}")
            print(f"🌀 Entropy: {entropy_gradient:.3f}")
            print(f"🧠 Consciousness Depth: {consciousness_depth:.3f}")
            
            # Check if data looks valid
            if tick_number == 0 and timestamp_ms == 0:
                print("❌ All zeros - no real data!")
                return False
                
            print("✅ Tick data looks valid")
            return True
            
    except Exception as e:
        print(f"❌ Error reading tick data: {e}")
        return False

def start_python_backend():
    """Start the Python consciousness backend"""
    print("\n🔍 STEP 4: START PYTHON BACKEND")
    print("=" * 50)
    
    backend_path = Path("consciousness/dawn_tick_state_writer.py")
    
    if not backend_path.exists():
        print(f"❌ Backend not found at: {backend_path.absolute()}")
        return None
    
    print(f"🚀 Starting backend: {backend_path}")
    
    # Command to start backend at 10Hz for testing
    cmd = [
        sys.executable,
        str(backend_path),
        "--interval", "0.1",  # 10 Hz
        "--mmap-path", "runtime/dawn_consciousness.mmap"
    ]
    
    print(f"💻 Command: {' '.join(cmd)}")
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print(f"✅ Backend started (PID: {process.pid})")
        return process
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return None

def monitor_mmap_updates(duration=10):
    """Monitor mmap file for updates"""
    print(f"\n🔍 STEP 5: MONITOR UPDATES ({duration}s)")
    print("=" * 50)
    
    mmap_path = Path("runtime/dawn_consciousness.mmap")
    last_tick = 0
    
    for i in range(duration):
        try:
            with open(mmap_path, 'rb') as f:
                f.seek(16)
                current_tick = struct.unpack('I', f.read(4))[0]
                
                if current_tick != last_tick:
                    print(f"🎯 Tick update: {current_tick} (was {last_tick})")
                    last_tick = current_tick
                else:
                    print(f"⏸️  No update - still tick {current_tick}")
                    
        except Exception as e:
            print(f"❌ Error monitoring: {e}")
            
        time.sleep(1)

def test_tauri_commands():
    """Show how to test Tauri commands"""
    print("\n🔍 STEP 6: TEST TAURI COMMANDS")
    print("=" * 50)
    
    print("To test Tauri commands:")
    print("1. Open browser console in the Tauri app")
    print("2. Run these commands:")
    print()
    print("// Test frontend data injection:")
    print("window.testDawnData()")
    print()
    print("// Check current state:")
    print("window.dawnDebug.get()")
    print()
    print("// Check subscribers:")
    print("window.dawnDebug.getSubscriberCount()")
    print()
    print("// Test Tauri commands:")
    print("await window.__TAURI__.invoke('reset_heat')")
    print("await window.__TAURI__.invoke('zero_entropy')")

def main():
    """Run complete system debug"""
    print("🌟 DAWN SYSTEM DEBUG TOOL")
    print("=" * 60)
    
    # Step 1: Check mmap file
    mmap_fresh = check_mmap_file()
    
    # Step 2: Check header
    header_valid = read_mmap_header()
    
    # Step 3: Read latest tick
    tick_valid = read_latest_tick()
    
    # Step 4: Start backend if needed
    backend_process = None
    if not mmap_fresh or not tick_valid:
        print("\n⚠️  Starting Python backend...")
        backend_process = start_python_backend()
        
        if backend_process:
            print("⏳ Waiting 3 seconds for backend to initialize...")
            time.sleep(3)
            
            # Re-check after starting backend
            print("\n🔄 RE-CHECKING AFTER BACKEND START:")
            check_mmap_file()
            read_mmap_header()
            read_latest_tick()
            
            # Monitor for updates
            monitor_mmap_updates(duration=5)
    
    # Step 5: Show Tauri testing instructions
    test_tauri_commands()
    
    print("\n🎯 SUMMARY:")
    print("=" * 30)
    if backend_process:
        print(f"✅ Python backend running (PID: {backend_process.pid})")
    print("✅ Now test the Tauri GUI to see if it receives updates!")
    print("✅ Check browser console for 'tick_update' events")
    
    return backend_process

if __name__ == "__main__":
    main() 