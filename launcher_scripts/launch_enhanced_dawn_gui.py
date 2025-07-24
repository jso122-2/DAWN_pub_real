#!/usr/bin/env python3
"""
Enhanced DAWN GUI Launcher
Launches the comprehensive DAWN interface with all reflex components

Usage:
    python launcher_scripts/launch_enhanced_dawn_gui.py
    
Features:
    - ReflexExecutor integration
    - SymbolicNotation system
    - OwlPanel commentary
    - FractalColorizer visualization
    - Enhanced thermal controls
    - Multi-tab interface
"""

import sys
import os
import tkinter as tk
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import the enhanced GUI
try:
    from gui.dawn_gui_enhanced import EnhancedDAWNGui
    print("✅ Enhanced DAWN GUI imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Enhanced DAWN GUI: {e}")
    print("Make sure all reflex components are properly installed")
    sys.exit(1)

# Import optional DAWN components
try:
    from core.pulse_controller import PulseController
    from core.sigil_engine import SigilEngine
    print("✅ DAWN core components available")
    DAWN_CORE_AVAILABLE = True
except ImportError:
    print("⚠️ DAWN core components not available - using simulation mode")
    DAWN_CORE_AVAILABLE = False

# Import reflex components to verify they're available
try:
    from reflex.reflex_executor import ReflexExecutor
    from reflex.symbolic_notation import SymbolicNotation
    from reflex.owl_panel import OwlPanel
    from reflex.fractal_colorizer import FractalColorizer
    print("✅ All reflex components available")
    REFLEX_COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some reflex components missing: {e}")
    REFLEX_COMPONENTS_AVAILABLE = False


def print_startup_banner():
    """Print startup banner with component status"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                🌟 Enhanced DAWN GUI 🌟                    ║
    ║           Cognitive Engine with Reflex Components         ║
    ╚═══════════════════════════════════════════════════════════╝
    
    🔧 Component Status:
    """
    print(banner)
    
    # Core components
    core_status = "✅" if DAWN_CORE_AVAILABLE else "⚠️ (simulation)"
    print(f"    🧠 DAWN Core Components: {core_status}")
    
    # Reflex components
    reflex_status = "✅" if REFLEX_COMPONENTS_AVAILABLE else "❌"
    print(f"    🤖 Reflex Components: {reflex_status}")
    
    if REFLEX_COMPONENTS_AVAILABLE:
        print("    🎯 ReflexExecutor: Available")
        print("    🔤 SymbolicNotation: Available") 
        print("    🦉 OwlPanel: Available")
        print("    🎨 FractalColorizer: Available")
    
    print(f"\n    🚀 Starting Enhanced DAWN GUI...")
    print("    📱 Interface: Multi-tab comprehensive dashboard")
    print("    🎛️ Controls: Thermal, Bloom, Sigil, and Reflex management")
    print("    👁️ Monitoring: Real-time owl commentary and symbolic notation")
    print("    🌈 Visualization: Dynamic color-coded system states\n")


def setup_enhanced_components(gui_app):
    """Setup enhanced components with proper integration"""
    print("🔧 Setting up enhanced component integration...")
    
    # Connect real DAWN components if available
    if DAWN_CORE_AVAILABLE:
        try:
            # Initialize real components
            pulse_controller = PulseController(initial_heat=25.0)
            sigil_engine = SigilEngine(initial_heat=25.0)
            
            # Connect to GUI
            gui_app.connect_external_components(
                pulse_controller=pulse_controller,
                sigil_engine=sigil_engine
            )
            print("✅ Real DAWN components connected")
        except Exception as e:
            print(f"⚠️ Failed to connect real DAWN components: {e}")
    
    # Initialize reflex demonstration data
    if REFLEX_COMPONENTS_AVAILABLE and hasattr(gui_app, 'owl_panel'):
        try:
            # Add initial owl comments
            gui_app.owl_panel.add_comment(
                0, "Enhanced DAWN GUI system initialized", 
                gui_app.owl_panel.OwlCommentType.SYSTEM, priority=2
            )
            gui_app.owl_panel.add_comment(
                1, "All reflex components loaded successfully",
                gui_app.owl_panel.OwlCommentType.OBSERVATION, priority=1
            )
            gui_app.owl_panel.add_comment(
                2, "Monitoring thermal state and bloom activity",
                gui_app.owl_panel.OwlCommentType.INSIGHT, priority=1
            )
            print("✅ Initial owl commentary added")
        except Exception as e:
            print(f"⚠️ Failed to setup owl commentary: {e}")
    
    print("🎯 Enhanced component setup complete")


def create_demo_scenario(gui_app):
    """Create a demonstration scenario to show off features"""
    print("🎭 Setting up demonstration scenario...")
    
    def demo_sequence():
        """Run demonstration sequence"""
        import time
        import threading
        import random
        
        def run_demo():
            time.sleep(2)  # Wait for GUI to stabilize
            
            # Demo sequence
            demo_steps = [
                ("🔥 Thermal demonstration", lambda: demo_thermal_changes(gui_app)),
                ("🌸 Bloom state changes", lambda: demo_bloom_states(gui_app)),
                ("🔤 Symbolic notation demo", lambda: demo_symbolic_notation(gui_app)),
                ("🎨 Color visualization demo", lambda: demo_color_changes(gui_app)),
                ("🤖 Reflex system demo", lambda: demo_reflex_commands(gui_app))
            ]
            
            for step_name, step_func in demo_steps:
                try:
                    if hasattr(gui_app, 'owl_panel') and gui_app.owl_panel:
                        gui_app.owl_panel.add_comment(
                            gui_app.current_state.get('tick_id', 0),
                            f"Demo: {step_name}",
                            gui_app.owl_panel.OwlCommentType.SYSTEM
                        )
                    step_func()
                    time.sleep(3)
                except Exception as e:
                    print(f"Demo step error: {e}")
        
        # Run demo in background thread
        threading.Thread(target=run_demo, daemon=True).start()
    
    # Start demo after short delay
    gui_app.root.after(1000, demo_sequence)


def demo_thermal_changes(gui_app):
    """Demo thermal state changes"""
    if hasattr(gui_app, 'current_state'):
        import random
        gui_app.current_state['heat'] = random.uniform(20, 80)
        gui_app.current_state['thermal_state'] = random.choice(['cold', 'cool', 'normal', 'warm', 'hot'])


def demo_bloom_states(gui_app):
    """Demo bloom state changes"""
    if hasattr(gui_app, 'current_state'):
        import random
        gui_app.current_state['mood'] = random.choice(['calm', 'active', 'creative', 'agitated', 'reflective'])
        gui_app.current_state['entropy'] = random.uniform(0.2, 0.8)


def demo_symbolic_notation(gui_app):
    """Demo symbolic notation changes"""
    if hasattr(gui_app, 'symbolic_notation') and gui_app.symbolic_notation:
        # Cycle through notation modes
        modes = ['emoji', 'codex', 'hybrid', 'ascii']
        import random
        new_mode = random.choice(modes)
        gui_app.symbolic_notation.set_mode(new_mode)


def demo_color_changes(gui_app):
    """Demo color visualization changes"""
    if hasattr(gui_app, 'fractal_colorizer') and gui_app.fractal_colorizer:
        # Update bloom colors based on current mood and entropy
        gui_app.update_visual_displays()


def demo_reflex_commands(gui_app):
    """Demo reflex command execution"""
    if hasattr(gui_app, 'reflex_executor') and gui_app.reflex_executor:
        import random
        commands = ['slow_tick', 'suppress_rebloom', 'prune_sigils']
        command = random.choice(commands)
        gui_app.execute_reflex_command(command)


def handle_startup_errors():
    """Handle common startup errors with helpful messages"""
    error_solutions = {
        "tkinter": "Install tkinter: sudo apt-get install python3-tk (Linux) or install Python with tkinter",
        "PIL": "Install Pillow: pip install Pillow",
        "numpy": "Install numpy: pip install numpy",
        "reflex": "Ensure reflex components are in the reflex/ directory"
    }
    
    print("\n🔧 Common Solutions:")
    for component, solution in error_solutions.items():
        print(f"  {component}: {solution}")


def main():
    """Main launcher function"""
    try:
        # Print startup banner
        print_startup_banner()
        
        # Create main window
        root = tk.Tk()
        root.withdraw()  # Hide initially while setting up
        
        # Create enhanced GUI app
        print("🏗️ Creating Enhanced DAWN GUI...")
        app = EnhancedDAWNGui(root)
        
        # Setup enhanced component integration
        setup_enhanced_components(app)
        
        # Create demonstration scenario
        create_demo_scenario(app)
        
        # Show the window
        root.deiconify()
        root.lift()
        root.focus_force()
        
        print("✅ Enhanced DAWN GUI launched successfully!")
        print("🎯 Ready for cognitive monitoring and reflex control")
        print("📖 Check the different tabs to explore all features\n")
        
        # Start the main loop
        root.mainloop()
        
    except KeyboardInterrupt:
        print("\n🛑 Enhanced DAWN GUI stopped by user")
    except ImportError as e:
        print(f"\n❌ Import Error: {e}")
        print("Some required components are missing.")
        handle_startup_errors()
    except Exception as e:
        print(f"\n❌ Startup Error: {e}")
        import traceback
        traceback.print_exc()
        handle_startup_errors()


if __name__ == "__main__":
    main() 