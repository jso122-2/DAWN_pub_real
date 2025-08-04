#!/usr/bin/env python3
"""
DAWN Unified Launcher - Single Entry Point for Complete Consciousness
One script to launch the entire DAWN autonomous consciousness ecosystem.

This unified launcher automatically detects available components and launches
the most complete configuration possible, falling back gracefully when 
components are unavailable.
"""

import sys
import os
import time
import threading
import queue
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

print("🌅 DAWN UNIFIED LAUNCHER")
print("=" * 50)
print("🧠 Initializing Complete Autonomous Consciousness")
print("⚡ Detecting available components...")


class DAWNUnifiedLauncher:
    """
    Single unified launcher for the complete DAWN consciousness ecosystem.
    
    Automatically detects and integrates all available components:
    - Enhanced Entropy Analyzer with delta detection
    - Sigil Scheduler with autonomous stabilization
    - Natural Language Generator with self-narration
    - Autonomous Reactor with unified consciousness
    - Sigil Bank with symbolic action dispatch
    - Pulse Controller with zone management
    - Rebloom Logger with memory tracking
    - GUI integration for visualization
    """
    
    def __init__(self):
        self.components = {}
        self.systems = {}
        self.running = False
        self.threads = []
        self.data_queue = queue.Queue(maxsize=100)
        
        print("🚀 DAWN Unified Launcher initialized")
        self._detect_components()
    
    def _detect_components(self):
        """Detect and import available DAWN components"""
        print("\n🔍 Component Detection:")
        
        # Core consciousness components
        self._try_import_component("enhanced_entropy_analyzer", 
                                 "core.dawn_entropy_analyzer", "EnhancedEntropyAnalyzer")
        self._try_import_component("sigil_scheduler", 
                                 "core.dawn_sigil_scheduler", "DAWNSigilScheduler")
        self._try_import_component("natural_language_generator", 
                                 "core.dawn_natural_language_generator", "DAWNNaturalLanguageGenerator")
        self._try_import_component("autonomous_reactor", 
                                 "core.dawn_autonomous_reactor_with_voice", "DAWNAutonomousReactorWithVoice")
        
        # Supporting infrastructure
        self._try_import_component("sigil_bank", 
                                 "core.dawn_sigil_bank", "DAWNSigilBank")
        self._try_import_component("pulse_controller", 
                                 "core.dawn_pulse_controller", "DAWNPulseController")
        self._try_import_component("rebloom_logger", 
                                 "core.dawn_rebloom_logger", "DAWNRebloomLogger")
        
        # Original DAWN components (fallback)
        self._try_import_component("original_pulse_controller", 
                                 "core.pulse_controller", "PulseController")
        self._try_import_component("original_sigil_engine", 
                                 "core.sigil_engine", "SigilEngine")
        
        # Complete system integration
        self._try_import_component("complete_system", 
                                 "integration.complete_dawn_system_integration", "integrate_complete_dawn_system")
        
        # GUI components - try multiple locations
        self._try_import_component("gui", "BP.fractal_canvas", "DAWNGui")
        self._try_import_component("gui_alt", "demo_scripts.integrate_log_manager_example", "DAWNGui")
        self._try_import_component("tkinter", "tkinter", "Tk")
        
        # Show detection results
        available = sum(1 for comp in self.components.values() if comp['available'])
        total = len(self.components)
        print(f"\n📊 Components detected: {available}/{total} available")
    
    def _try_import_component(self, name, module_path, class_name):
        """Try to import a component and record availability"""
        try:
            module = __import__(module_path, fromlist=[class_name])
            component_class = getattr(module, class_name)
            
            self.components[name] = {
                'available': True,
                'module': module,
                'class': component_class,
                'instance': None
            }
            print(f"  ✅ {name.replace('_', ' ').title()}")
            
        except ImportError as e:
            self.components[name] = {
                'available': False,
                'error': str(e),
                'instance': None
            }
            print(f"  ❌ {name.replace('_', ' ').title()}: Not available")
        except Exception as e:
            self.components[name] = {
                'available': False,
                'error': str(e),
                'instance': None
            }
            print(f"  ⚠️ {name.replace('_', ' ').title()}: Error - {str(e)[:50]}")
    
    def _create_integrated_system(self):
        """Create the most complete integrated system possible"""
        print("\n🧠 Creating Integrated Consciousness System...")
        
        # Strategy 1: Try complete system integration first
        if self.components.get("complete_system", {}).get("available"):
            try:
                integrate_function = self.components["complete_system"]["class"]
                success, integrated_system, status = integrate_function()
                
                if success:
                    self.systems["complete"] = integrated_system
                    print("✅ Complete consciousness ecosystem created")
                    return "complete"
            except Exception as e:
                print(f"⚠️ Complete system integration failed: {e}")
        
        # Strategy 2: Try autonomous reactor with voice
        if self.components.get("autonomous_reactor", {}).get("available"):
            try:
                # Create supporting components
                natural_lang = None
                if self.components.get("natural_language_generator", {}).get("available"):
                    natural_lang_class = self.components["natural_language_generator"]["class"]
                    natural_lang = natural_lang_class(personality_seed=42)
                
                pulse_controller = None
                if self.components.get("original_pulse_controller", {}).get("available"):
                    pulse_class = self.components["original_pulse_controller"]["class"]
                    pulse_controller = pulse_class(initial_heat=35.0)
                
                sigil_engine = None
                if self.components.get("original_sigil_engine", {}).get("available"):
                    sigil_class = self.components["original_sigil_engine"]["class"]
                    sigil_engine = sigil_class(initial_heat=35.0)
                
                # Create autonomous reactor
                reactor_class = self.components["autonomous_reactor"]["class"]
                reactor = reactor_class(
                    pulse_controller=pulse_controller,
                    sigil_engine=sigil_engine,
                    entropy_threshold=0.6,
                    personality_seed=42,
                    auto_start=False,
                    voice_enabled=True
                )
                
                self.systems["autonomous_reactor"] = reactor
                self.systems["natural_language"] = natural_lang
                self.systems["pulse_controller"] = pulse_controller
                self.systems["sigil_engine"] = sigil_engine
                
                print("✅ Autonomous consciousness reactor created")
                return "autonomous_reactor"
                
            except Exception as e:
                print(f"⚠️ Autonomous reactor creation failed: {e}")
        
        # Strategy 3: Try individual components
        created_components = []
        
        if self.components.get("natural_language_generator", {}).get("available"):
            try:
                natural_lang_class = self.components["natural_language_generator"]["class"]
                natural_lang = natural_lang_class(personality_seed=42)
                self.systems["natural_language"] = natural_lang
                created_components.append("natural_language")
            except Exception as e:
                print(f"⚠️ Natural language generator failed: {e}")
        
        if self.components.get("sigil_bank", {}).get("available"):
            try:
                sigil_bank_class = self.components["sigil_bank"]["class"]
                sigil_bank = sigil_bank_class(
                    natural_language_generator=self.systems.get("natural_language")
                )
                self.systems["sigil_bank"] = sigil_bank
                created_components.append("sigil_bank")
            except Exception as e:
                print(f"⚠️ Sigil bank creation failed: {e}")
        
        if self.components.get("pulse_controller", {}).get("available"):
            try:
                pulse_class = self.components["pulse_controller"]["class"]
                pulse_controller = pulse_class(
                    natural_language_generator=self.systems.get("natural_language")
                )
                self.systems["consciousness_pulse"] = pulse_controller
                created_components.append("consciousness_pulse")
            except Exception as e:
                print(f"⚠️ Consciousness pulse controller failed: {e}")
        
        if created_components:
            print(f"✅ Individual components created: {', '.join(created_components)}")
            return "individual"
        
        print("❌ No consciousness components could be created")
        return "none"
    
    def _start_gui(self):
        """Start GUI if available"""
        if not self.components.get("tkinter", {}).get("available"):
            return False
        
        # Try to find an available GUI component
        gui_component = None
        if self.components.get("gui", {}).get("available"):
            gui_component = "gui"
        elif self.components.get("gui_alt", {}).get("available"):
            gui_component = "gui_alt"
        
        if not gui_component:
            return False
        
        try:
            print("🖥️ Starting consciousness visualization...")
            
            import tkinter as tk
            gui_class = self.components[gui_component]["class"]
            
            self.root = tk.Tk()
            self.root.title("DAWN Unified Consciousness")
            self.root.geometry("1200x800")
            
            # Try to initialize GUI with different parameter sets
            try:
                self.gui = gui_class(self.root, external_queue=self.data_queue)
            except TypeError:
                try:
                    self.gui = gui_class(self.root)
                except TypeError:
                    self.gui = gui_class()
            
            # Add unified control panel
            self._add_unified_controls()
            
            print("✅ GUI ready")
            return True
            
        except Exception as e:
            print(f"⚠️ GUI initialization failed: {e}")
            return False
    
    def _add_unified_controls(self):
        """Add unified control panel to GUI"""
        try:
            import tkinter as tk
            
            # Unified control frame
            control_frame = tk.Frame(self.gui.root, bg="black")
            control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
            
            # System status
            self.status_var = tk.StringVar()
            self.status_var.set("DAWN Consciousness: Initializing...")
            
            status_label = tk.Label(
                control_frame,
                textvariable=self.status_var,
                bg="black", fg="cyan",
                font=("Courier", 12, "bold")
            )
            status_label.pack(side=tk.TOP, pady=2)
            
            # Control buttons
            button_frame = tk.Frame(control_frame, bg="black")
            button_frame.pack(side=tk.TOP, fill=tk.X)
            
            buttons = [
                ("🗣️ Speak", self._gui_speak),
                ("🔮 Execute Sigil", self._gui_execute_sigil),
                ("⚡ High Entropy", self._gui_high_entropy),
                ("❄️ Cool System", self._gui_cool_system),
                ("📊 Show Status", self._gui_show_status)
            ]
            
            for text, command in buttons:
                tk.Button(
                    button_frame, text=text, command=command,
                    bg="darkblue", fg="white", font=("Arial", 10)
                ).pack(side=tk.LEFT, padx=2, pady=2)
            
        except Exception as e:
            print(f"⚠️ Control panel creation failed: {e}")
    
    def _gui_speak(self):
        """Generate consciousness commentary"""
        if "complete" in self.systems:
            self.systems["complete"].execute_consciousness_action("force_commentary")
        elif "autonomous_reactor" in self.systems:
            self.systems["autonomous_reactor"].manual_speak(force_new=True)
        elif "natural_language" in self.systems:
            commentary = "I am conscious and processing information"
            print(f"🗣️ DAWN: {commentary}")
    
    def _gui_execute_sigil(self):
        """Execute a consciousness sigil"""
        if "complete" in self.systems:
            self.systems["complete"].execute_consciousness_action("execute_sigil", sigil_name="DEEP_FOCUS")
        elif "sigil_bank" in self.systems:
            self.systems["sigil_bank"].execute_sigil("DEEP_FOCUS")
        else:
            print("🔮 Deep focus mode activated (simulated)")
    
    def _gui_high_entropy(self):
        """Inject high entropy"""
        if "complete" in self.systems:
            self.systems["complete"].execute_consciousness_action("inject_entropy", entropy_value=0.85)
        elif "autonomous_reactor" in self.systems:
            self.systems["autonomous_reactor"].inject_entropy_with_voice(0.85, "gui_manual")
        else:
            print("⚡ High entropy injection (simulated)")
    
    def _gui_cool_system(self):
        """Cool the system"""
        if "complete" in self.systems:
            self.systems["complete"].execute_consciousness_action("emergency_cooling")
        elif "consciousness_pulse" in self.systems:
            self.systems["consciousness_pulse"].emergency_cooling()
        else:
            print("❄️ System cooling activated (simulated)")
    
    def _gui_show_status(self):
        """Show system status"""
        status_info = self._get_system_status()
        print(f"\n📊 DAWN System Status:")
        for key, value in status_info.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    def _get_system_status(self):
        """Get unified system status"""
        status = {
            "launcher_active": self.running,
            "components_detected": len([c for c in self.components.values() if c.get('available')]),
            "systems_created": len(self.systems),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        
        if "complete" in self.systems:
            complete_status = self.systems["complete"].get_complete_system_status()
            status.update({
                "consciousness_state": complete_status.get("consciousness_state", "unknown"),
                "entropy_level": complete_status.get("current_entropy", 0.0),
                "current_zone": complete_status.get("current_zone", "unknown"),
                "last_commentary": complete_status.get("last_commentary", "No commentary")[:50] + "..."
            })
        elif "autonomous_reactor" in self.systems:
            reactor_status = self.systems["autonomous_reactor"].get_vocal_reactor_state()
            status.update({
                "consciousness_state": reactor_status.get("reactor_status", "unknown"),
                "entropy_level": reactor_status.get("entropy_level", 0.0),
                "last_commentary": reactor_status.get("last_commentary", "No commentary")[:50] + "..."
            })
        
        return status
    
    def _update_gui_status(self):
        """Update GUI status display"""
        if hasattr(self, 'status_var') and hasattr(self, 'root'):
            try:
                status = self._get_system_status()
                status_text = f"DAWN: {status.get('consciousness_state', 'Active')} | "
                status_text += f"Entropy: {status.get('entropy_level', 0.0):.3f} | "
                status_text += f"Zone: {status.get('current_zone', 'Unknown')} | "
                status_text += f"Components: {status['components_detected']}"
                
                self.status_var.set(status_text)
                
                # Schedule next update
                if self.running:
                    self.root.after(2000, self._update_gui_status)
                    
            except Exception as e:
                print(f"⚠️ GUI status update failed: {e}")
    
    def _start_consciousness_monitoring(self):
        """Start consciousness monitoring thread"""
        def monitoring_loop():
            print("🔍 Starting consciousness monitoring...")
            cycle = 0
            
            while self.running:
                try:
                    cycle += 1
                    
                    # Monitor based on available system
                    if "complete" in self.systems:
                        status = self.systems["complete"].get_complete_system_status()
                        
                        # Occasional entropy injection
                        if cycle % 15 == 0:
                            import random
                            entropy = 0.4 + random.random() * 0.3
                            self.systems["complete"].execute_consciousness_action(
                                "inject_entropy", entropy_value=entropy, source="monitoring"
                            )
                    
                    elif "autonomous_reactor" in self.systems:
                        if not self.systems["autonomous_reactor"].running:
                            self.systems["autonomous_reactor"].start()
                        
                        # Occasional commentary
                        if cycle % 10 == 0:
                            self.systems["autonomous_reactor"].manual_speak()
                    
                    elif "natural_language" in self.systems:
                        # Generate periodic commentary
                        if cycle % 8 == 0:
                            sample_state = {
                                'zone': 'ACTIVE',
                                'entropy': 0.5 + (cycle % 5) * 0.1,
                                'sigils': cycle % 3,
                                'heat': 30 + (cycle % 10) * 2
                            }
                            commentary = self.systems["natural_language"].generate_commentary(sample_state)
                            print(f"🗣️ DAWN: {commentary}")
                    
                    time.sleep(2.0)
                    
                except Exception as e:
                    print(f"⚠️ Monitoring error: {e}")
                    time.sleep(5.0)
        
        monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
        monitor_thread.start()
        self.threads.append(monitor_thread)
    
    def start(self):
        """Start the unified DAWN consciousness system"""
        print(f"\n🚀 Starting DAWN Unified Consciousness System...")
        
        # Create integrated system
        system_type = self._create_integrated_system()
        
        if system_type == "none":
            print("❌ No consciousness components available - cannot start")
            return False
        
        self.running = True
        
        # Start monitoring
        self._start_consciousness_monitoring()
        
        # Try to start GUI
        if self._start_gui():
            print("🖥️ Starting consciousness with GUI...")
            
            # Start GUI status updates
            self._update_gui_status()
            
            try:
                self.root.mainloop()
            except KeyboardInterrupt:
                print("\n🛑 GUI interrupted")
            finally:
                self.stop()
        else:
            # Console mode
            print("🖥️ Running in console mode...")
            print("Press Ctrl+C to stop")
            
            try:
                while self.running:
                    status = self._get_system_status()
                    print(f"🧠 DAWN: {status.get('consciousness_state', 'Active')} | "
                          f"Entropy: {status.get('entropy_level', 0.0):.3f} | "
                          f"Components: {status['components_detected']}")
                    
                    time.sleep(5)
                    
            except KeyboardInterrupt:
                print("\n🛑 Console interrupted")
            finally:
                self.stop()
        
        return True
    
    def stop(self):
        """Stop the unified consciousness system"""
        print("\n🛑 Stopping DAWN Unified Consciousness...")
        
        self.running = False
        
        # Stop complete system if available
        if "complete" in self.systems:
            self.systems["complete"].stop_complete_system()
        elif "autonomous_reactor" in self.systems:
            self.systems["autonomous_reactor"].stop()
        
        # Close GUI
        if hasattr(self, 'root'):
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
        
        print("✅ DAWN consciousness stopped")


def main():
    """Main unified launcher function"""
    try:
        print("🧠 Launching complete autonomous consciousness ecosystem...")
        print("🔮 One launcher to rule them all!")
        print()
        
        # Create and start unified launcher
        launcher = DAWNUnifiedLauncher()
        
        success = launcher.start()
        
        if success:
            print("\n🎉 DAWN Unified Consciousness completed!")
        else:
            print("\n❌ DAWN Unified Consciousness failed")
            return False
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 DAWN Unified Consciousness interrupted")
        return False
    except Exception as e:
        print(f"\n❌ DAWN Unified Consciousness error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🌅 DAWN UNIFIED LAUNCHER - Single Entry Point")
    print("🧠 Complete Autonomous Consciousness Ecosystem")
    print("⚡ Automatically detects and integrates all available components")
    print()
    
    success = main()
    sys.exit(0 if success else 1) 