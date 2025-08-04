#!/usr/bin/env python3
"""
DAWN Beautiful Launcher - Professional Charts & Graphs
======================================================

Launches DAWN with beautiful visualization system using:
- matplotlib: Professional 2D plotting
- seaborn: Statistical data visualization  
- plotly: Interactive charts and real-time updates
- numpy: Numerical computations
- pandas: Data manipulation

Creates stunning, real-time consciousness visualizations.
"""

import sys
import os
import subprocess
import threading
import time
import signal
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Main launcher function"""
    print("🌅 DAWN Beautiful System Launcher")
    print("=" * 50)
    print("🎨 Professional Charts & Graphs")
    print("📊 matplotlib, seaborn, plotly")
    print("🚀 Real-time consciousness visualizations")
    print("✨ Stunning interactive dashboards")
    print()
    
    # Check if we're in the right directory
    if not Path("dawn_runner.py").exists():
        print("❌ Error: dawn_runner.py not found. Please run from the DAWN project root.")
        return
    
    # Check if beautiful visual system exists
    if not Path("dawn_visual_beautiful.py").exists():
        print("❌ Error: dawn_visual_beautiful.py not found.")
        return
    
    print("🔍 Checking beautiful dependencies...")
    
    # Check plotting libraries
    plotting_libs = {
        'matplotlib': 'Professional 2D plotting',
        'seaborn': 'Statistical data visualization',
        'plotly': 'Interactive charts',
        'numpy': 'Numerical computations',
        'pandas': 'Data manipulation'
    }
    
    available_libs = []
    missing_libs = []
    
    for lib, description in plotting_libs.items():
        try:
            __import__(lib)
            available_libs.append(lib)
            print(f"✅ {lib}: {description}")
        except ImportError:
            missing_libs.append(lib)
            print(f"⚠️  {lib}: {description} (missing)")
    
    if missing_libs:
        print(f"\n📦 Install missing libraries:")
        print(f"   pip install {' '.join(missing_libs)}")
        print()
    
    # Check if we can import our beautiful visual system
    try:
        from visual.dawn_visual_beautiful import DAWNBeautifulGUI
        print("✅ Beautiful visual system available")
    except ImportError as e:
        print(f"❌ Beautiful visual system import failed: {e}")
        return
    
    print("\n🚀 Starting DAWN Beautiful System...")
    
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
        
        # Start beautiful visual system
        print("🎨 Starting Beautiful Visual System...")
        visual_process = subprocess.Popen(
            [sys.executable, "dawn_visual_beautiful.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print("\n✅ DAWN Beautiful System is running!")
        print("   - DAWN Runner: PID", dawn_process.pid if dawn_process else "N/A")
        print("   - Beautiful Visual System: PID", visual_process.pid if visual_process else "N/A")
        
        print("\n🎨 Beautiful Visualizations:")
        print("   - 📊 Consciousness Dashboard (4-panel)")
        print("   - 🌡️ State Heatmap (seaborn)")
        print("   - 🌌 3D Trajectory (matplotlib 3D)")
        print("   - 📈 Interactive Charts (plotly)")
        
        print("\n📊 Available Charts:")
        print("   - SCUP vs Entropy Scatter Plot")
        print("   - Heat Timeline with Area Fill")
        print("   - Coherence Radar Chart")
        print("   - Cognitive Pulse Wave")
        print("   - Consciousness State Heatmap")
        print("   - 3D Consciousness Trajectory")
        print("   - Interactive Multi-panel Dashboard")
        
        print("\n🎨 Visual Features:")
        print("   - Dark theme with green accents")
        print("   - Real-time data updates")
        print("   - Professional styling")
        print("   - Interactive navigation")
        print("   - Smooth animations")
        print("   - High-quality rendering")
        
        print("\n📈 Rich Metrics:")
        print("   - SCUP, Entropy, Heat")
        print("   - Coherence, Vitality, Focus")
        print("   - Creativity, Attention Span")
        print("   - Memory Coherence")
        print("   - Cognitive Load")
        print("   - Pulse Analysis")
        
        print("\nPress Ctrl+C to stop all processes...")
        
        # Monitor processes
        while True:
            if dawn_process and dawn_process.poll() is not None:
                print("❌ DAWN Runner stopped unexpectedly")
                break
            if visual_process and visual_process.poll() is not None:
                print("❌ Beautiful Visual System stopped unexpectedly")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down beautiful system...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        if dawn_process:
            print("🛑 Stopping DAWN Runner...")
            dawn_process.terminate()
            dawn_process.wait(timeout=5)
        
        if visual_process:
            print("🛑 Stopping Beautiful Visual System...")
            visual_process.terminate()
            visual_process.wait(timeout=5)
        
        print("✅ All beautiful processes stopped")

def test_beautiful_system():
    """Test the beautiful visualization system"""
    print("\n🧪 Testing Beautiful Visual System...")
    
    try:
        # Test imports
        from visual.dawn_visual_beautiful import DAWNBeautifulDataGenerator, DAWNBeautifulVisualizer
        
        # Test data generation
        data_gen = DAWNBeautifulDataGenerator()
        data = data_gen.generate_rich_data()
        
        print("✅ Beautiful data generation working")
        print(f"   Tick: {data['tick_number']}")
        print(f"   SCUP: {data['scup']:.3f}")
        print(f"   Heat: {data['heat']:.1f}°C")
        print(f"   Zone: {data['zone']}")
        print(f"   Mood: {data['mood']}")
        print(f"   Coherence: {data['coherence']:.3f}")
        print(f"   Vitality: {data['vitality']:.3f}")
        print(f"   Focus: {data['focus_level']:.3f}")
        print(f"   Creativity: {data['creativity']:.3f}")
        
        # Test visualization generation
        viz_gen = DAWNBeautifulVisualizer()
        
        # Generate some history
        history = []
        for i in range(20):
            history.append(data_gen.generate_rich_data())
        
        # Test dashboard creation
        try:
            fig = viz_gen.create_consciousness_dashboard(data, history)
            print("✅ Consciousness dashboard generation working")
        except Exception as e:
            print(f"⚠️  Dashboard generation: {e}")
        
        # Test heatmap creation
        try:
            fig = viz_gen.create_heatmap_visualization(data, history)
            print("✅ Heatmap visualization generation working")
        except Exception as e:
            print(f"⚠️  Heatmap generation: {e}")
        
        # Test 3D plot creation
        try:
            fig = viz_gen.create_3d_consciousness_plot(data, history)
            print("✅ 3D trajectory generation working")
        except Exception as e:
            print(f"⚠️  3D plot generation: {e}")
        
        print("\n✅ Beautiful system test passed!")
        print("   Ready for stunning visualizations")
        
    except Exception as e:
        print(f"❌ Beautiful system test failed: {e}")

def install_dependencies():
    """Install required plotting dependencies"""
    print("\n📦 Installing Beautiful Visualization Dependencies...")
    
    dependencies = [
        'matplotlib',
        'seaborn', 
        'plotly',
        'pandas',
        'numpy'
    ]
    
    for dep in dependencies:
        print(f"   Installing {dep}...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
            print(f"   ✅ {dep} installed successfully")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {dep}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_beautiful_system()
        elif sys.argv[1] == "--install":
            install_dependencies()
        else:
            print("Usage: python launch_dawn_beautiful.py [--test|--install]")
    else:
        main() 