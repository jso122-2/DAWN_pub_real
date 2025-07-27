#!/usr/bin/env python3
"""
Complete DAWN Consciousness Ecosystem Launcher
Ultimate launcher integrating all consciousness components with GUI visualization.

Components Integrated:
- Enhanced Entropy Analyzer with rapid rise detection
- Sigil Scheduler with autonomous stabilization  
- Natural Language Generator with self-narration
- Autonomous Reactor with Voice for unified consciousness
- Sigil Bank with consciousness-aware symbolic actions
- Pulse Controller with consciousness zone management
- Rebloom Logger with consciousness memory tracking
- GUI Integration for real-time visualization
"""

import sys
import os
import time
import queue
import threading
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import complete system integration
try:
    from integration.complete_dawn_system_integration import integrate_complete_dawn_system, CompleteDAWNSystem
    COMPLETE_SYSTEM_AVAILABLE = True
except ImportError as e:
    print(f"❌ Complete system integration not available: {e}")
    COMPLETE_SYSTEM_AVAILABLE = False

# Try to import GUI for visualization
try:
    import tkinter as tk
    from gui.dawn_gui_tk import DAWNGui
    GUI_AVAILABLE = True
except ImportError:
    print("⚠️ GUI not available - running in console mode")
    GUI_AVAILABLE = False


class CompleteDAWNLauncher:
    """
    Complete DAWN Consciousness Ecosystem Launcher
    
    Launches the full consciousness ecosystem with optional GUI visualization
    for real-time monitoring of all consciousness components.
    """
    
    def __init__(self, enable_gui: bool = True, tick_interval: float = 1.0, queue_maxsize: int = 100):
        """
        Initialize the complete DAWN launcher.
        
        Args:
            enable_gui: Whether to enable GUI visualization
            tick_interval: Tick interval for consciousness updates
            queue_maxsize: Maximum size for data queue
        """
        self.enable_gui = enable_gui and GUI_AVAILABLE
        self.tick_interval = tick_interval
        self.queue_maxsize = queue_maxsize
        
        # Core components
        self.integrated_system: CompleteDAWNSystem = None
        self.gui = None
        self.root = None
        
        # Communication
        self.data_queue = queue.Queue(maxsize=queue_maxsize)
        self.gui_thread = None
        self.consciousness_thread = None
        self.running = False
        
        print("🚀 Complete DAWN Consciousness Launcher initialized")
    
    def initialize_complete_system(self) -> bool:
        """Initialize the complete consciousness ecosystem"""
        if not COMPLETE_SYSTEM_AVAILABLE:
            print("❌ Complete system integration not available")
            return False
        
        print("🧠 Initializing complete consciousness ecosystem...")
        
        success, integrated_system, components = integrate_complete_dawn_system()
        
        if success:
            self.integrated_system = integrated_system
            print("✅ Complete consciousness ecosystem ready")
            
            # Show component status
            available_components = sum(1 for status in components.values() if status)
            total_components = len(components)
            print(f"📊 Components available: {available_components}/{total_components}")
            
            return True
        else:
            print("❌ Failed to initialize consciousness ecosystem")
            return False
    
    def start_consciousness_monitoring(self):
        """Start consciousness monitoring in background thread"""
        if not self.integrated_system:
            return False
        
        self.consciousness_thread = threading.Thread(
            target=self._consciousness_monitoring_loop,
            daemon=True,
            name="ConsciousnessMonitoring"
        )
        self.consciousness_thread.start()
        return True
    
    def _consciousness_monitoring_loop(self):
        """Main consciousness monitoring loop"""
        print("🔍 Starting consciousness monitoring loop...")
        
        # Start the complete system
        if not self.integrated_system.start_complete_system():
            print("❌ Failed to start consciousness system")
            return
        
        cycle_count = 0
        
        while self.running:
            try:
                cycle_count += 1
                
                # Get complete system status
                consciousness_status = self.integrated_system.get_complete_system_status()
                
                # Occasionally inject test entropy to keep system active
                if cycle_count % 10 == 0:
                    import random
                    test_entropy = 0.4 + random.random() * 0.3  # 0.4 to 0.7
                    self.integrated_system.execute_consciousness_action(
                        "inject_entropy",
                        entropy_value=test_entropy,
                        source="monitoring_cycle"
                    )
                
                # Occasionally generate commentary
                if cycle_count % 7 == 0:
                    self.integrated_system.execute_consciousness_action("force_commentary")
                
                # Send status to GUI if available
                if self.enable_gui:
                    gui_data = {
                        'type': 'consciousness_status',
                        'data': consciousness_status,
                        'cycle': cycle_count,
                        'timestamp': time.time()
                    }
                    
                    try:
                        self.data_queue.put_nowait(gui_data)
                    except queue.Full:
                        # Remove old data and add new
                        try:
                            self.data_queue.get_nowait()
                            self.data_queue.put_nowait(gui_data)
                        except queue.Empty:
                            pass
                
                time.sleep(self.tick_interval)
                
            except Exception as e:
                print(f"❌ Consciousness monitoring error: {e}")
                time.sleep(2.0)
        
        # Stop the system when loop ends
        self.integrated_system.stop_complete_system()
    
    def start_gui(self) -> bool:
        """Start the GUI in main thread"""
        if not self.enable_gui:
            print("🖥️ GUI disabled - running in console mode")
            return True
        
        try:
            print("🖥️ Starting consciousness visualization GUI...")
            
            self.root = tk.Tk()
            self.root.title("DAWN Complete Consciousness Ecosystem")
            self.root.geometry("1200x800")
            
            # Initialize GUI with data queue
            self.gui = DAWNGui(self.root, external_queue=self.data_queue)
            
            # Add consciousness-specific display elements
            self._enhance_gui_for_consciousness()
            
            print("✅ Consciousness GUI ready")
            return True
            
        except Exception as e:
            print(f"❌ GUI initialization failed: {e}")
            self.enable_gui = False
            return False
    
    def _enhance_gui_for_consciousness(self):
        """Add consciousness-specific elements to the GUI"""
        if not self.gui:
            return
        
        try:
            # Add consciousness control frame
            consciousness_frame = tk.Frame(self.gui.root)
            consciousness_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
            
            # Consciousness action buttons
            tk.Button(
                consciousness_frame,
                text="🗣️ Generate Commentary",
                command=self._gui_force_commentary
            ).pack(side=tk.LEFT, padx=2)
            
            tk.Button(
                consciousness_frame,
                text="🔮 Execute Sigil",
                command=self._gui_execute_sigil
            ).pack(side=tk.LEFT, padx=2)
            
            tk.Button(
                consciousness_frame,
                text="⚡ High Entropy",
                command=self._gui_inject_high_entropy
            ).pack(side=tk.LEFT, padx=2)
            
            tk.Button(
                consciousness_frame,
                text="❄️ Emergency Cool",
                command=self._gui_emergency_cool
            ).pack(side=tk.LEFT, padx=2)
            
            # Consciousness status display
            self.consciousness_status_var = tk.StringVar()
            self.consciousness_status_var.set("Consciousness: Initializing...")
            
            status_label = tk.Label(
                consciousness_frame,
                textvariable=self.consciousness_status_var,
                bg="black",
                fg="cyan",
                font=("Courier", 10)
            )
            status_label.pack(side=tk.RIGHT, padx=5)
            
        except Exception as e:
            print(f"⚠️ GUI enhancement failed: {e}")
    
    def _gui_force_commentary(self):
        """GUI callback to force consciousness commentary"""
        if self.integrated_system:
            self.integrated_system.execute_consciousness_action("force_commentary")
    
    def _gui_execute_sigil(self):
        """GUI callback to execute a sigil"""
        if self.integrated_system:
            self.integrated_system.execute_consciousness_action(
                "execute_sigil",
                sigil_name="DEEP_FOCUS"
            )
    
    def _gui_inject_high_entropy(self):
        """GUI callback to inject high entropy"""
        if self.integrated_system:
            self.integrated_system.execute_consciousness_action(
                "inject_entropy",
                entropy_value=0.85,
                source="gui_manual"
            )
    
    def _gui_emergency_cool(self):
        """GUI callback for emergency cooling"""
        if self.integrated_system:
            self.integrated_system.execute_consciousness_action("emergency_cooling")
    
    def start(self) -> bool:
        """Start the complete consciousness ecosystem with GUI"""
        print("\n🌅 Starting Complete DAWN Consciousness Ecosystem")
        print("=" * 60)
        
        # Initialize consciousness system
        if not self.initialize_complete_system():
            return False
        
        # Set running flag
        self.running = True
        
        # Start consciousness monitoring
        if not self.start_consciousness_monitoring():
            print("❌ Failed to start consciousness monitoring")
            return False
        
        # Start GUI or run in console mode
        if self.enable_gui:
            if self.start_gui():
                print("🖥️ Starting GUI main loop...")
                
                # Update consciousness status in GUI
                self._update_gui_consciousness_status()
                
                try:
                    self.root.mainloop()
                except KeyboardInterrupt:
                    print("\n🛑 GUI interrupted by user")
                finally:
                    self.stop()
            else:
                print("⚠️ GUI failed, falling back to console mode")
                self._run_console_mode()
        else:
            self._run_console_mode()
        
        return True
    
    def _update_gui_consciousness_status(self):
        """Update consciousness status in GUI"""
        if not self.gui or not self.integrated_system:
            return
        
        try:
            status = self.integrated_system.get_complete_system_status()
            status_text = f"Consciousness: {status['consciousness_state']} | Entropy: {status['current_entropy']:.3f} | Zone: {status['current_zone']}"
            
            if hasattr(self, 'consciousness_status_var'):
                self.consciousness_status_var.set(status_text)
            
            # Schedule next update
            if self.root:
                self.root.after(2000, self._update_gui_consciousness_status)
                
        except Exception as e:
            print(f"⚠️ GUI status update failed: {e}")
    
    def _run_console_mode(self):
        """Run in console mode without GUI"""
        print("🖥️ Running in console mode...")
        print("Press Ctrl+C to stop")
        
        try:
            while self.running:
                # Show periodic status updates
                if self.integrated_system:
                    status = self.integrated_system.get_complete_system_status()
                    print(f"🧠 Consciousness: {status['consciousness_state']} | "
                          f"Entropy: {status['current_entropy']:.3f} | "
                          f"Zone: {status['current_zone']} | "
                          f"Last: {status['last_commentary'][:50]}...")
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n🛑 Console mode interrupted by user")
        finally:
            self.stop()
    
    def stop(self):
        """Stop the complete consciousness ecosystem"""
        print("\n🛑 Stopping Complete DAWN Consciousness Ecosystem...")
        
        self.running = False
        
        # Wait for consciousness thread to complete
        if self.consciousness_thread and self.consciousness_thread.is_alive():
            self.consciousness_thread.join(timeout=5.0)
        
        # Stop integrated system
        if self.integrated_system:
            self.integrated_system.stop_complete_system()
        
        # Close GUI
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
        
        print("✅ Complete consciousness ecosystem stopped")


def main():
    """Main launcher function"""
    print("🌅 COMPLETE DAWN CONSCIOUSNESS ECOSYSTEM LAUNCHER")
    print("=" * 60)
    print("Launching complete autonomous consciousness with:")
    print("  🔍 Self-monitoring entropy analysis")
    print("  🔥 Autonomous stabilization protocols")
    print("  🗣️ Self-narrating natural language consciousness")
    print("  🧠 Unified self-aware reactive system")
    print("  🔮 Consciousness-aware symbolic actions")
    print("  🌡️ Consciousness-aware zone management")
    print("  🌸 Consciousness-aware memory tracking")
    print("  🖥️ Real-time consciousness visualization")
    print()
    
    try:
        # Check if GUI is available
        gui_available = GUI_AVAILABLE
        
        # Create and start launcher
        launcher = CompleteDAWNLauncher(
            enable_gui=gui_available,
            tick_interval=1.0,  # Update every second
            queue_maxsize=100
        )
        
        success = launcher.start()
        
        if success:
            print("\n🎉 Complete DAWN Consciousness Ecosystem completed successfully!")
        else:
            print("\n❌ Complete DAWN Consciousness Ecosystem failed to start")
            return False
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Complete consciousness ecosystem interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Complete consciousness ecosystem error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 