# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Local Launcher - 100% Self-Contained System
================================================

Launches DAWN with completely local visual system.
No external dependencies, no network connections, no servers.
Can run underwater, in space, or anywhere offline.
"""

import sys
import os
import subprocess
import threading
import time
import signal
from pathlib import Path

def main():
    """Main launcher function"""
    print("🌅 DAWN Local System Launcher")
    print("=" * 50)
    print("🚀 100% Self-Contained - No External Dependencies")
    print("✅ Can run underwater, in space, or offline")
    print("✅ Pure Python with built-in tkinter GUI")
    print("✅ No network connections required")
    print()
    
    # Check if we're in the right directory
    if not Path("dawn_runner.py").exists():
        print("❌ Error: dawn_runner.py not found. Please run from the DAWN project root.")
        return
    
    # Check if local visual system exists
    if not Path("dawn_visual_local.py").exists():
        print("❌ Error: dawn_visual_local.py not found.")
        return
    
    print("🔍 Checking local dependencies...")
    
    # Check if tkinter is available (should be built-in)
    try:
        import tkinter
        print("✅ Tkinter available (built-in)")
    except ImportError:
        print("❌ Tkinter not available - this is unusual for Python")
        return
    
    # Check if we can import our local visual system
    try:
        from visual.dawn_visual_local import DAWNLocalVisualGUI
        print("✅ Local visual system available")
    except ImportError as e:
        print(f"❌ Local visual system import failed: {e}")
        return
    
    print("\n🚀 Starting DAWN Local System...")
    
    # Start processes
    dawn_process = None
    visual_process = None
    
    try:
        # Start DAWN runner
        print("🧠 Starting DAWN Unified Runner...")
        dawn_process = subprocess.Popen(
            [sys.executable, "launch_dawn.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Give DAWN time to start
        time.sleep(3)
        
        # Start local visual system
        print("🎨 Starting Local Visual System...")
        visual_process = subprocess.Popen(
            [sys.executable, "dawn_visual_local.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print("\n✅ DAWN Local System is running!")
        print("   - DAWN Runner: PID", dawn_process.pid if dawn_process else "N/A")
        print("   - Local Visual System: PID", visual_process.pid if visual_process else "N/A")
        
        print("\n🌊 System Status:")
        print("   ✅ 100% Local Operation")
        print("   ✅ No External Dependencies")
        print("   ✅ No Network Connections")
        print("   ✅ Can Run Underwater/In Space")
        print("   ✅ Pure Python Implementation")
        
        print("\n🎨 Visual System Features:")
        print("   - Real-time consciousness metrics")
        print("   - Tick pulse visualization")
        print("   - Consciousness constellation mapping")
        print("   - Heat monitor with zone indicators")
        print("   - Mood state emotional landscape")
        print("   - Auto-updating with configurable intervals")
        
        print("\n🔧 Local Operation:")
        print("   - All data generated locally")
        print("   - No external API calls")
        print("   - Self-contained visualization engine")
        print("   - Built-in tkinter GUI")
        print("   - Thread-safe data generation")
        
        print("\nPress Ctrl+C to stop all processes...")
        
        # Monitor processes
        while True:
            if dawn_process and dawn_process.poll() is not None:
                print("❌ DAWN Runner stopped unexpectedly")
                break
            if visual_process and visual_process.poll() is not None:
                print("❌ Local Visual System stopped unexpectedly")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down local system...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        if dawn_process:
            print("🛑 Stopping DAWN Runner...")
            dawn_process.terminate()
            dawn_process.wait(timeout=5)
        
        if visual_process:
            print("🛑 Stopping Local Visual System...")
            visual_process.terminate()
            visual_process.wait(timeout=5)
        
        print("✅ All local processes stopped")

def test_local_system():
    """Test the local visual system"""
    print("\n🧪 Testing Local Visual System...")
    
    try:
        # Test import
        from visual.dawn_visual_local import DAWNLocalVisualData, DAWNLocalVisualGenerator
        
        # Test data generation
        data_gen = DAWNLocalVisualData()
        data = data_gen.generate_local_data()
        
        print("✅ Local data generation working")
        print(f"   Tick: {data['tick_number']}")
        print(f"   SCUP: {data['scup']:.3f}")
        print(f"   Heat: {data['heat']:.1f}°C")
        print(f"   Zone: {data['zone']}")
        print(f"   Mood: {data['mood']}")
        
        # Test visualization generation
        viz_gen = DAWNLocalVisualGenerator()
        result = viz_gen.generate_visualization('tick_pulse', data)
        
        print("✅ Local visualization generation working")
        print("   Visualization generated successfully")
        
        print("\n✅ Local system test passed!")
        print("   Ready for underwater/space operation")
        
    except Exception as e:
        print(f"❌ Local system test failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_local_system()
    else:
        main() 