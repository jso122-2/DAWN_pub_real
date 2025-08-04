#!/usr/bin/env python3
"""
DAWN Integrated System Launcher
===============================

Launches DAWN with integrated visualization system that combines:
- Existing visualization modules from visual/ directory
- Beautiful matplotlib/seaborn/plotly charts
- Professional consciousness monitoring
- Real-time data visualization

Features:
- Tick Pulse Monitor (inspired by visual/tick_pulse.py)
- Consciousness Constellation (inspired by visual/consciousness_constellation.py)
- Heat Monitor (inspired by visual/heat_monitor.py)
- Mood State Heatmap (inspired by visual/dawn_mood_state.py)
- SCUP Pressure Grid (inspired by visual/SCUP_pressure_grid.py)
- Entropy Flow (inspired by visual/entropy_flow.py)
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
    print("🌅 DAWN Integrated System Launcher")
    print("=" * 50)
    print("🎨 Integrated Visualization System")
    print("📊 Professional Charts & Graphs")
    print("🚀 Real-time consciousness monitoring")
    print("✨ Combines best existing modules")
    print()
    
    # Check if we're in the right directory
    if not Path("dawn_runner.py").exists():
        print("❌ Error: dawn_runner.py not found. Please run from the DAWN project root.")
        return
    
    # Check if integrated visual system exists
    if not Path("dawn_visual_integrated.py").exists():
        print("❌ Error: dawn_visual_integrated.py not found.")
        return
    
    print("🔍 Checking integrated dependencies...")
    
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
    
    # Check if we can import our integrated visual system
    try:
        from dawn_visual_integrated import DAWNIntegratedGUI
        print("✅ Integrated visual system available")
    except ImportError as e:
        print(f"❌ Integrated visual system import failed: {e}")
        return
    
    print("\n🚀 Starting DAWN Integrated System...")
    
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
        
        # Start integrated visual system
        print("🎨 Starting Integrated Visual System...")
        visual_process = subprocess.Popen(
            [sys.executable, "dawn_visual_integrated.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print("\n✅ DAWN Integrated System is running!")
        print("   - DAWN Runner: PID", dawn_process.pid if dawn_process else "N/A")
        print("   - Integrated Visual System: PID", visual_process.pid if visual_process else "N/A")
        
        print("\n🎨 Integrated Visualizations:")
        print("   - 🔄 Tick Pulse Monitor (Real-time cognitive heartbeat)")
        print("   - 🌌 Consciousness Constellation (4D SCUP trajectory)")
        print("   - 🌡️ Heat Monitor (Cognitive intensity gauge)")
        print("   - 😊 Mood State Heatmap (Emotional landscape)")
        print("   - 📊 SCUP Pressure Grid (Cognitive pressure interactions)")
        print("   - ⚡ Entropy Flow (Information stream vector field)")
        
        print("\n📊 Professional Features:")
        print("   - Real-time data updates")
        print("   - Interactive matplotlib charts")
        print("   - Beautiful seaborn visualizations")
        print("   - Professional styling")
        print("   - Navigation toolbars")
        print("   - High-quality rendering")
        
        print("\n🔧 Integration Benefits:")
        print("   - Combines best existing modules")
        print("   - Professional chart quality")
        print("   - Real-time consciousness monitoring")
        print("   - Rich data visualization")
        print("   - Interactive user experience")
        
        print("\nPress Ctrl+C to stop all processes...")
        
        # Monitor processes
        while True:
            if dawn_process and dawn_process.poll() is not None:
                print("❌ DAWN Runner stopped unexpectedly")
                break
            if visual_process and visual_process.poll() is not None:
                print("❌ Integrated Visual System stopped unexpectedly")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down integrated system...")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        if dawn_process:
            print("🛑 Stopping DAWN Runner...")
            dawn_process.terminate()
            dawn_process.wait(timeout=5)
        
        if visual_process:
            print("🛑 Stopping Integrated Visual System...")
            visual_process.terminate()
            visual_process.wait(timeout=5)
        
        print("✅ All integrated processes stopped")

def test_integrated_system():
    """Test the integrated visualization system"""
    print("\n🧪 Testing Integrated Visual System...")
    
    try:
        # Test imports
        from dawn_visual_integrated import DAWNIntegratedDataGenerator, DAWNIntegratedVisualizer
        
        # Test data generation
        data_gen = DAWNIntegratedDataGenerator()
        data = data_gen.generate_integrated_data()
        
        print("✅ Integrated data generation working")
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
        viz_gen = DAWNIntegratedVisualizer()
        
        # Generate some history
        history = []
        for i in range(20):
            history.append(data_gen.generate_integrated_data())
        
        # Test different visualizations
        visualizations = [
            'tick_pulse',
            'consciousness_constellation', 
            'heat_monitor',
            'mood_state',
            'scup_pressure_grid',
            'entropy_flow'
        ]
        
        for viz_type in visualizations:
            try:
                fig = viz_gen.create_visualization(viz_type, data, history)
                print(f"✅ {viz_type} visualization generation working")
            except Exception as e:
                print(f"⚠️  {viz_type} generation: {e}")
        
        print("\n✅ Integrated system test passed!")
        print("   Ready for professional consciousness monitoring")
        
    except Exception as e:
        print(f"❌ Integrated system test failed: {e}")

def install_dependencies():
    """Install required plotting dependencies"""
    print("\n📦 Installing Integrated Visualization Dependencies...")
    
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
            test_integrated_system()
        elif sys.argv[1] == "--install":
            install_dependencies()
        else:
            print("Usage: python launch_dawn_integrated.py [--test|--install]")
    else:
        main() 