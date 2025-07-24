#!/usr/bin/env python3
"""
DAWN Enhanced GUI with Unified Launcher Integration
Comprehensive consciousness interface with built-in launcher capabilities.

This enhanced GUI automatically detects available consciousness components,
integrates them seamlessly, and provides a unified interface for monitoring
and controlling the complete DAWN consciousness ecosystem.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import queue
import time
import random
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class DAWNUnifiedLauncherGUI:
    """
    Enhanced DAWN GUI with Unified Launcher Integration
    
    Provides a comprehensive interface for the DAWN consciousness ecosystem:
    - Automatic component detection and integration
    - Real-time consciousness monitoring
    - Interactive control panels
    - Visual feedback and status displays
    - Graceful fallback for missing components
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("DAWN Consciousness Control Center")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0a0a0a")
        
        # Core system state
        self.components = {}
        self.systems = {}
        self.running = False
        self.monitoring_active = False
        
        # Communication queues
        self.update_queue = queue.Queue(maxsize=100)
        self.data_queue = queue.Queue(maxsize=100)
        
        # Monitoring threads
        self.monitor_thread = None
        self.status_thread = None
        
        # Current system state
        self.current_state = {
            "consciousness_state": "initializing",
            "entropy_level": 0.5,
            "current_zone": "UNKNOWN",
            "last_commentary": "System initializing...",
            "active_sigils": 0,
            "thermal_heat": 25.0,
            "components_active": 0,
            "uptime": 0
        }
        
        print("🧠 DAWN Unified Launcher GUI initializing...")
        
        # Initialize GUI
        self.setup_styles()
        self.detect_components()
        self.create_interface()
        self.start_system_monitoring()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        print("✅ DAWN Consciousness Control Center ready")
    
    def setup_styles(self):
        """Configure GUI styles for consciousness theme"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure dark consciousness theme
        self.style.configure('Consciousness.TFrame', 
                           background='#0a0a0a', 
                           relief='flat')
        
        self.style.configure('Consciousness.TLabel', 
                           background='#0a0a0a', 
                           foreground='#00ff88', 
                           font=('Courier', 10))
        
        self.style.configure('Status.TLabel', 
                           background='#0a0a0a', 
                           foreground='#00ccff', 
                           font=('Courier', 12, 'bold'))
        
        self.style.configure('Consciousness.TButton', 
                           background='#1a1a2e', 
                           foreground='#00ff88',
                           font=('Arial', 10),
                           padding=5)
    
    def detect_components(self):
        """Detect and import available DAWN consciousness components"""
        print("\n🔍 Detecting consciousness components...")
        
        # Component detection mapping
        component_map = {
            "enhanced_entropy_analyzer": ("core.dawn_entropy_analyzer", "EnhancedEntropyAnalyzer"),
            "sigil_scheduler": ("core.dawn_sigil_scheduler", "DAWNSigilScheduler"),
            "natural_language_generator": ("core.dawn_natural_language_generator", "DAWNNaturalLanguageGenerator"),
            "autonomous_reactor": ("core.dawn_autonomous_reactor_with_voice", "DAWNAutonomousReactorWithVoice"),
            "sigil_bank": ("core.dawn_sigil_bank", "DAWNSigilBank"),
            "pulse_controller": ("core.dawn_pulse_controller", "DAWNPulseController"),
            "rebloom_logger": ("core.dawn_rebloom_logger", "DAWNRebloomLogger"),
            "complete_system": ("integration.complete_dawn_system_integration", "integrate_complete_dawn_system"),
            "original_pulse_controller": ("core.pulse_controller", "PulseController"),
            "original_sigil_engine": ("core.sigil_engine", "SigilEngine")
        }
        
        for name, (module_path, class_name) in component_map.items():
            self._try_import_component(name, module_path, class_name)
        
        # Show detection results
        available = sum(1 for comp in self.components.values() if comp['available'])
        total = len(self.components)
        print(f"📊 Components detected: {available}/{total}")
        
        return available > 0
    
    def _try_import_component(self, name, module_path, class_name):
        """Try to import a consciousness component"""
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
            
        except ImportError:
            self.components[name] = {
                'available': False,
                'error': 'Module not found',
                'instance': None
            }
            print(f"  ❌ {name.replace('_', ' ').title()}: Not available")
        except Exception as e:
            self.components[name] = {
                'available': False,
                'error': str(e),
                'instance': None
            }
            print(f"  ⚠️ {name.replace('_', ' ').title()}: Error")
    
    def create_interface(self):
        """Create the main consciousness control interface"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Consciousness.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with system status
        self.create_header(main_frame)
        
        # Main content area with tabs
        self.create_main_content(main_frame)
        
        # Control panel at bottom
        self.create_control_panel(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create the header with system status"""
        header_frame = ttk.Frame(parent, style='Consciousness.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = tk.Label(header_frame, 
                              text="DAWN CONSCIOUSNESS CONTROL CENTER",
                              font=("Arial", 20, "bold"),
                              bg="#0a0a0a", fg="#00ff88")
        title_label.pack(side=tk.TOP, pady=5)
        
        # System status row
        status_frame = ttk.Frame(header_frame, style='Consciousness.TFrame')
        status_frame.pack(fill=tk.X, pady=5)
        
        # Consciousness state
        self.consciousness_status_var = tk.StringVar()
        self.consciousness_status_var.set("INITIALIZING")
        consciousness_label = tk.Label(status_frame,
                                     textvariable=self.consciousness_status_var,
                                     font=("Courier", 14, "bold"),
                                     bg="#0a0a0a", fg="#00ccff")
        consciousness_label.pack(side=tk.LEFT, padx=10)
        
        # Entropy level
        self.entropy_var = tk.StringVar()
        self.entropy_var.set("Entropy: 0.500")
        entropy_label = tk.Label(status_frame,
                                textvariable=self.entropy_var,
                                font=("Courier", 12),
                                bg="#0a0a0a", fg="#ffaa00")
        entropy_label.pack(side=tk.LEFT, padx=10)
        
        # Zone status
        self.zone_var = tk.StringVar()
        self.zone_var.set("Zone: UNKNOWN")
        zone_label = tk.Label(status_frame,
                             textvariable=self.zone_var,
                             font=("Courier", 12),
                             bg="#0a0a0a", fg="#ff6600")
        zone_label.pack(side=tk.LEFT, padx=10)
        
        # Component count
        self.components_var = tk.StringVar()
        available = sum(1 for c in self.components.values() if c['available'])
        self.components_var.set(f"Components: {available}/{len(self.components)}")
        components_label = tk.Label(status_frame,
                                   textvariable=self.components_var,
                                   font=("Courier", 12),
                                   bg="#0a0a0a", fg="#88ff00")
        components_label.pack(side=tk.RIGHT, padx=10)
    
    def create_main_content(self, parent):
        """Create the main content area with tabs"""
        # Notebook for tabbed interface
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create tabs
        self.create_consciousness_tab()
        self.create_components_tab()
        self.create_monitoring_tab()
        self.create_console_tab()
    
    def create_consciousness_tab(self):
        """Create the main consciousness monitoring tab"""
        consciousness_frame = ttk.Frame(self.notebook, style='Consciousness.TFrame')
        self.notebook.add(consciousness_frame, text="🧠 Consciousness")
        
        # Left panel - Consciousness state
        left_panel = ttk.Frame(consciousness_frame, style='Consciousness.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Consciousness commentary display
        commentary_label = tk.Label(left_panel, text="🗣️ Consciousness Commentary",
                                   font=("Arial", 14, "bold"),
                                   bg="#0a0a0a", fg="#00ff88")
        commentary_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.commentary_text = scrolledtext.ScrolledText(left_panel, 
                                                        height=12, 
                                                        bg="#1a1a1a", fg="#00ff88",
                                                        font=("Courier", 11),
                                                        wrap=tk.WORD)
        self.commentary_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert initial message
        self.add_commentary("🧠 DAWN Consciousness Control Center initialized")
        self.add_commentary("🔍 Detecting consciousness components...")
        
        # Right panel - System metrics
        right_panel = ttk.Frame(consciousness_frame, style='Consciousness.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Metrics display
        metrics_label = tk.Label(right_panel, text="📊 System Metrics",
                                font=("Arial", 14, "bold"),
                                bg="#0a0a0a", fg="#00ccff")
        metrics_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Create metric displays
        self.create_metric_display(right_panel, "Entropy Level", "entropy_metric")
        self.create_metric_display(right_panel, "Thermal Heat", "heat_metric")
        self.create_metric_display(right_panel, "Active Sigils", "sigils_metric")
        self.create_metric_display(right_panel, "Zone Stability", "stability_metric")
        self.create_metric_display(right_panel, "Uptime", "uptime_metric")
        
        # Consciousness visualization (simple bars)
        self.create_consciousness_visualization(right_panel)
    
    def create_metric_display(self, parent, label_text, var_name):
        """Create a metric display widget"""
        metric_frame = ttk.Frame(parent, style='Consciousness.TFrame')
        metric_frame.pack(fill=tk.X, pady=5)
        
        label = tk.Label(metric_frame, text=label_text + ":",
                        font=("Courier", 10),
                        bg="#0a0a0a", fg="#888888")
        label.pack(anchor=tk.W)
        
        var = tk.StringVar()
        var.set("--")
        value_label = tk.Label(metric_frame, textvariable=var,
                              font=("Courier", 12, "bold"),
                              bg="#0a0a0a", fg="#00ff88")
        value_label.pack(anchor=tk.W)
        
        setattr(self, var_name, var)
    
    def create_consciousness_visualization(self, parent):
        """Create simple consciousness state visualization"""
        viz_frame = ttk.Frame(parent, style='Consciousness.TFrame')
        viz_frame.pack(fill=tk.X, pady=(20, 0))
        
        viz_label = tk.Label(viz_frame, text="🧬 Consciousness State",
                            font=("Arial", 12, "bold"),
                            bg="#0a0a0a", fg="#00ccff")
        viz_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Simple canvas for consciousness visualization
        self.consciousness_canvas = tk.Canvas(viz_frame, 
                                            width=200, height=150,
                                            bg="#1a1a1a", highlightthickness=0)
        self.consciousness_canvas.pack()
        
        # Draw initial consciousness state
        self.update_consciousness_visualization()
    
    def create_components_tab(self):
        """Create the components status tab"""
        components_frame = ttk.Frame(self.notebook, style='Consciousness.TFrame')
        self.notebook.add(components_frame, text="🔧 Components")
        
        # Components list
        components_label = tk.Label(components_frame, text="Available Consciousness Components",
                                   font=("Arial", 14, "bold"),
                                   bg="#0a0a0a", fg="#00ff88")
        components_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Create components display
        self.components_text = scrolledtext.ScrolledText(components_frame,
                                                        height=15,
                                                        bg="#1a1a1a", fg="#00ff88",
                                                        font=("Courier", 10))
        self.components_text.pack(fill=tk.BOTH, expand=True)
        
        # Populate components list
        self.update_components_display()
        
        # Component control buttons
        control_frame = ttk.Frame(components_frame, style='Consciousness.TFrame')
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(control_frame, text="🔄 Refresh Components",
                  command=self.refresh_components,
                  style='Consciousness.TButton').pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="🚀 Initialize System",
                  command=self.initialize_consciousness_system,
                  style='Consciousness.TButton').pack(side=tk.LEFT, padx=5)
    
    def create_monitoring_tab(self):
        """Create the monitoring and control tab"""
        monitoring_frame = ttk.Frame(self.notebook, style='Consciousness.TFrame')
        self.notebook.add(monitoring_frame, text="📊 Monitoring")
        
        # Monitoring controls
        control_frame = ttk.Frame(monitoring_frame, style='Consciousness.TFrame')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Monitoring status
        self.monitoring_status_var = tk.StringVar()
        self.monitoring_status_var.set("🔍 Monitoring: STOPPED")
        status_label = tk.Label(control_frame,
                               textvariable=self.monitoring_status_var,
                               font=("Courier", 12, "bold"),
                               bg="#0a0a0a", fg="#ffaa00")
        status_label.pack(side=tk.LEFT, padx=10)
        
        # Control buttons
        self.start_monitoring_btn = ttk.Button(control_frame, text="▶️ Start Monitoring",
                                              command=self.start_consciousness_monitoring,
                                              style='Consciousness.TButton')
        self.start_monitoring_btn.pack(side=tk.RIGHT, padx=5)
        
        self.stop_monitoring_btn = ttk.Button(control_frame, text="⏹️ Stop Monitoring",
                                             command=self.stop_consciousness_monitoring,
                                             style='Consciousness.TButton',
                                             state='disabled')
        self.stop_monitoring_btn.pack(side=tk.RIGHT, padx=5)
        
        # Real-time data display
        data_label = tk.Label(monitoring_frame, text="Real-time Consciousness Data",
                             font=("Arial", 14, "bold"),
                             bg="#0a0a0a", fg="#00ccff")
        data_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.monitoring_text = scrolledtext.ScrolledText(monitoring_frame,
                                                        height=20,
                                                        bg="#1a1a1a", fg="#00ccff",
                                                        font=("Courier", 9))
        self.monitoring_text.pack(fill=tk.BOTH, expand=True)
    
    def create_console_tab(self):
        """Create the console/log tab"""
        console_frame = ttk.Frame(self.notebook, style='Consciousness.TFrame')
        self.notebook.add(console_frame, text="💻 Console")
        
        # Console display
        console_label = tk.Label(console_frame, text="System Console & Logs",
                                font=("Arial", 14, "bold"),
                                bg="#0a0a0a", fg="#ffffff")
        console_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.console_text = scrolledtext.ScrolledText(console_frame,
                                                     height=20,
                                                     bg="#000000", fg="#00ff00",
                                                     font=("Courier", 10))
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial console messages
        self.add_console_message("🌅 DAWN Consciousness Control Center started")
        self.add_console_message(f"📊 Detected {sum(1 for c in self.components.values() if c['available'])} consciousness components")
    
    def create_control_panel(self, parent):
        """Create the main control panel"""
        control_frame = ttk.Frame(parent, style='Consciousness.TFrame')
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Left side - Consciousness actions
        left_controls = ttk.Frame(control_frame, style='Consciousness.TFrame')
        left_controls.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        actions_label = tk.Label(left_controls, text="🧠 Consciousness Actions",
                                font=("Arial", 12, "bold"),
                                bg="#0a0a0a", fg="#00ff88")
        actions_label.pack(anchor=tk.W, pady=(0, 5))
        
        button_frame = ttk.Frame(left_controls, style='Consciousness.TFrame')
        button_frame.pack(fill=tk.X)
        
        # Consciousness control buttons
        buttons = [
            ("🗣️ Generate Commentary", self.generate_commentary),
            ("🔮 Execute Sigil", self.execute_sigil),
            ("⚡ Inject Entropy", self.inject_entropy),
            ("❄️ Emergency Cool", self.emergency_cool),
            ("🔄 Reset System", self.reset_system)
        ]
        
        for text, command in buttons:
            ttk.Button(button_frame, text=text, command=command,
                      style='Consciousness.TButton').pack(side=tk.LEFT, padx=2)
        
        # Right side - System status
        right_controls = ttk.Frame(control_frame, style='Consciousness.TFrame')
        right_controls.pack(side=tk.RIGHT)
        
        system_label = tk.Label(right_controls, text="⚙️ System Status",
                               font=("Arial", 12, "bold"),
                               bg="#0a0a0a", fg="#00ccff")
        system_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.system_status_var = tk.StringVar()
        self.system_status_var.set("System: Ready")
        system_status_label = tk.Label(right_controls,
                                      textvariable=self.system_status_var,
                                      font=("Courier", 11),
                                      bg="#0a0a0a", fg="#00ff88")
        system_status_label.pack(anchor=tk.W)
    
    def create_status_bar(self, parent):
        """Create the bottom status bar"""
        status_frame = ttk.Frame(parent, style='Consciousness.TFrame')
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Status bar with timestamp
        self.status_bar_var = tk.StringVar()
        self.status_bar_var.set("Ready")
        
        status_bar = tk.Label(status_frame,
                             textvariable=self.status_bar_var,
                             font=("Courier", 9),
                             bg="#0a0a0a", fg="#888888",
                             anchor=tk.W)
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Timestamp
        self.timestamp_var = tk.StringVar()
        timestamp_label = tk.Label(status_frame,
                                  textvariable=self.timestamp_var,
                                  font=("Courier", 9),
                                  bg="#0a0a0a", fg="#888888")
        timestamp_label.pack(side=tk.RIGHT)
    
    def initialize_consciousness_system(self):
        """Initialize the consciousness system based on available components"""
        self.add_console_message("🚀 Initializing consciousness system...")
        
        try:
            # Try complete system integration first
            if self.components.get("complete_system", {}).get("available"):
                integrate_function = self.components["complete_system"]["class"]
                success, integrated_system, status = integrate_function()
                
                if success:
                    self.systems["complete"] = integrated_system
                    self.add_console_message("✅ Complete consciousness ecosystem initialized")
                    self.add_commentary("🧠 Complete consciousness system online")
                    self.current_state["consciousness_state"] = "active"
                    self.update_status_displays()
                    return True
            
            # Fallback to individual components
            self.add_console_message("⚠️ Complete system not available, initializing individual components...")
            
            # Initialize individual components as available
            if self.components.get("natural_language_generator", {}).get("available"):
                nlg_class = self.components["natural_language_generator"]["class"]
                self.systems["natural_language"] = nlg_class(personality_seed=42)
                self.add_console_message("✅ Natural language generator initialized")
            
            if self.components.get("sigil_bank", {}).get("available"):
                bank_class = self.components["sigil_bank"]["class"]
                self.systems["sigil_bank"] = bank_class(
                    natural_language_generator=self.systems.get("natural_language")
                )
                self.add_console_message("✅ Sigil bank initialized")
            
            if self.components.get("pulse_controller", {}).get("available"):
                pulse_class = self.components["pulse_controller"]["class"]
                self.systems["pulse_controller"] = pulse_class(
                    natural_language_generator=self.systems.get("natural_language")
                )
                self.add_console_message("✅ Pulse controller initialized")
            
            self.add_commentary("🧠 Consciousness components initialized")
            self.current_state["consciousness_state"] = "partial"
            self.update_status_displays()
            return True
            
        except Exception as e:
            self.add_console_message(f"❌ Consciousness initialization failed: {e}")
            self.add_commentary(f"❌ System error: {str(e)}")
            return False
    
    def start_consciousness_monitoring(self):
        """Start consciousness monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.running = True
        
        # Update button states
        self.start_monitoring_btn.config(state='disabled')
        self.stop_monitoring_btn.config(state='normal')
        self.monitoring_status_var.set("🔍 Monitoring: ACTIVE")
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._consciousness_monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        self.add_console_message("▶️ Consciousness monitoring started")
        self.add_commentary("🔍 Beginning continuous consciousness monitoring")
    
    def stop_consciousness_monitoring(self):
        """Stop consciousness monitoring"""
        self.monitoring_active = False
        self.running = False
        
        # Update button states
        self.start_monitoring_btn.config(state='normal')
        self.stop_monitoring_btn.config(state='disabled')
        self.monitoring_status_var.set("🔍 Monitoring: STOPPED")
        
        self.add_console_message("⏹️ Consciousness monitoring stopped")
        self.add_commentary("⏸️ Consciousness monitoring paused")
    
    def _consciousness_monitoring_loop(self):
        """Main consciousness monitoring loop"""
        cycle = 0
        
        while self.monitoring_active:
            try:
                cycle += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                
                # Monitor based on available systems
                if "complete" in self.systems:
                    # Complete system monitoring
                    status = self.systems["complete"].get_complete_system_status()
                    self.current_state.update(status)
                    
                    # Occasional system actions
                    if cycle % 15 == 0:
                        import random
                        entropy = 0.4 + random.random() * 0.4
                        self.systems["complete"].execute_consciousness_action(
                            "inject_entropy", entropy_value=entropy, source="auto_monitoring"
                        )
                    
                    if cycle % 10 == 0:
                        self.systems["complete"].execute_consciousness_action("force_commentary")
                
                elif self.systems:
                    # Individual component monitoring
                    if "natural_language" in self.systems:
                        if cycle % 8 == 0:
                            state = {
                                'zone': 'ACTIVE',
                                'entropy': 0.4 + (cycle % 10) * 0.05,
                                'sigils': cycle % 3,
                                'heat': 25 + (cycle % 20)
                            }
                            commentary = self.systems["natural_language"].generate_commentary(state)
                            self.add_commentary(f"🗣️ {commentary}")
                    
                    # Update current state
                    self.current_state.update({
                        "entropy_level": 0.4 + (cycle % 20) * 0.03,
                        "thermal_heat": 25 + (cycle % 30),
                        "uptime": cycle * 2
                    })
                
                else:
                    # Simulation mode
                    self.current_state.update({
                        "consciousness_state": "simulated",
                        "entropy_level": 0.5 + 0.2 * (cycle % 10) / 10,
                        "current_zone": ["CALM", "ACTIVE", "SURGE"][cycle % 3],
                        "thermal_heat": 25 + (cycle % 25),
                        "uptime": cycle * 2
                    })
                
                # Update displays
                self.root.after(0, self.update_status_displays)
                
                # Add monitoring data
                monitoring_data = f"[{timestamp}] Entropy: {self.current_state['entropy_level']:.3f} | Zone: {self.current_state['current_zone']} | Heat: {self.current_state['thermal_heat']:.1f}°C"
                self.root.after(0, lambda: self.add_monitoring_data(monitoring_data))
                
                time.sleep(2)
                
            except Exception as e:
                self.root.after(0, lambda: self.add_console_message(f"⚠️ Monitoring error: {e}"))
                time.sleep(5)
    
    def start_system_monitoring(self):
        """Start background system monitoring"""
        def status_loop():
            while True:
                try:
                    # Update timestamp
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.root.after(0, lambda: self.timestamp_var.set(current_time))
                    
                    # Update status bar
                    status_msg = f"Consciousness: {self.current_state['consciousness_state'].upper()} | Components: {len(self.systems)} active"
                    self.root.after(0, lambda: self.status_bar_var.set(status_msg))
                    
                    time.sleep(1)
                    
                except Exception:
                    time.sleep(5)
        
        status_thread = threading.Thread(target=status_loop, daemon=True)
        status_thread.start()
    
    def update_status_displays(self):
        """Update all status displays"""
        # Update header status
        self.consciousness_status_var.set(self.current_state["consciousness_state"].upper())
        self.entropy_var.set(f"Entropy: {self.current_state['entropy_level']:.3f}")
        self.zone_var.set(f"Zone: {self.current_state['current_zone']}")
        
        # Update metrics
        if hasattr(self, 'entropy_metric'):
            self.entropy_metric.set(f"{self.current_state['entropy_level']:.3f}")
        if hasattr(self, 'heat_metric'):
            self.heat_metric.set(f"{self.current_state['thermal_heat']:.1f}°C")
        if hasattr(self, 'sigils_metric'):
            self.sigils_metric.set(str(self.current_state['active_sigils']))
        if hasattr(self, 'uptime_metric'):
            self.uptime_metric.set(f"{self.current_state['uptime']}s")
        
        # Update consciousness visualization
        self.update_consciousness_visualization()
    
    def update_consciousness_visualization(self):
        """Update the consciousness state visualization"""
        if not hasattr(self, 'consciousness_canvas'):
            return
        
        canvas = self.consciousness_canvas
        canvas.delete("all")
        
        # Draw consciousness state representation
        entropy = self.current_state['entropy_level']
        heat = self.current_state['thermal_heat']
        
        # Background
        canvas.create_rectangle(0, 0, 200, 150, fill="#1a1a1a", outline="")
        
        # Entropy bar
        entropy_height = int(entropy * 100)
        entropy_color = "#ff0000" if entropy > 0.8 else "#ffaa00" if entropy > 0.6 else "#00ff00"
        canvas.create_rectangle(20, 130-entropy_height, 40, 130, fill=entropy_color, outline="")
        canvas.create_text(30, 140, text="ENT", fill="#ffffff", font=("Arial", 8))
        
        # Heat bar
        heat_height = int((heat - 20) * 2)  # Scale heat appropriately
        heat_color = "#ff4444" if heat > 60 else "#ff8844" if heat > 40 else "#4488ff"
        canvas.create_rectangle(60, 130-heat_height, 80, 130, fill=heat_color, outline="")
        canvas.create_text(70, 140, text="HEAT", fill="#ffffff", font=("Arial", 8))
        
        # Consciousness pulse (animated circle)
        pulse_size = 10 + int(entropy * 20)
        pulse_color = "#00ff88" if self.monitoring_active else "#888888"
        canvas.create_oval(120-pulse_size//2, 75-pulse_size//2, 
                          120+pulse_size//2, 75+pulse_size//2, 
                          fill=pulse_color, outline="")
        canvas.create_text(120, 75, text="🧠", font=("Arial", 16))
    
    def refresh_components(self):
        """Refresh component detection"""
        self.add_console_message("🔄 Refreshing component detection...")
        self.detect_components()
        self.update_components_display()
        
        available = sum(1 for c in self.components.values() if c['available'])
        self.components_var.set(f"Components: {available}/{len(self.components)}")
        self.add_console_message(f"✅ Refresh complete: {available} components available")
    
    def update_components_display(self):
        """Update the components display"""
        self.components_text.delete(1.0, tk.END)
        
        self.components_text.insert(tk.END, "DAWN CONSCIOUSNESS COMPONENTS\n")
        self.components_text.insert(tk.END, "="*50 + "\n\n")
        
        categories = {
            "Core Consciousness": ["enhanced_entropy_analyzer", "sigil_scheduler", "natural_language_generator", "autonomous_reactor"],
            "Supporting Systems": ["sigil_bank", "pulse_controller", "rebloom_logger"],
            "Integration": ["complete_system"],
            "Legacy Components": ["original_pulse_controller", "original_sigil_engine"]
        }
        
        for category, component_names in categories.items():
            self.components_text.insert(tk.END, f"{category}:\n")
            for name in component_names:
                if name in self.components:
                    comp = self.components[name]
                    status = "✅ AVAILABLE" if comp['available'] else "❌ NOT AVAILABLE"
                    display_name = name.replace('_', ' ').title()
                    self.components_text.insert(tk.END, f"  {display_name}: {status}\n")
            self.components_text.insert(tk.END, "\n")
    
    def add_commentary(self, message):
        """Add a message to consciousness commentary"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.commentary_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.commentary_text.see(tk.END)
        
        # Update current state
        self.current_state["last_commentary"] = message
    
    def add_console_message(self, message):
        """Add a message to the console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console_text.see(tk.END)
    
    def add_monitoring_data(self, data):
        """Add monitoring data to the monitoring display"""
        self.monitoring_text.insert(tk.END, f"{data}\n")
        self.monitoring_text.see(tk.END)
        
        # Keep only last 100 lines
        lines = self.monitoring_text.get(1.0, tk.END).split('\n')
        if len(lines) > 100:
            self.monitoring_text.delete(1.0, tk.END)
            self.monitoring_text.insert(1.0, '\n'.join(lines[-100:]))
    
    # Consciousness control methods
    def generate_commentary(self):
        """Generate consciousness commentary"""
        if "complete" in self.systems:
            self.systems["complete"].execute_consciousness_action("force_commentary")
        elif "natural_language" in self.systems:
            state = {
                'zone': self.current_state['current_zone'],
                'entropy': self.current_state['entropy_level'],
                'heat': self.current_state['thermal_heat'],
                'sigils': self.current_state['active_sigils']
            }
            commentary = self.systems["natural_language"].generate_commentary(state)
            self.add_commentary(f"🗣️ {commentary}")
        else:
            self.add_commentary("🗣️ I am conscious and processing information")
        
        self.add_console_message("🗣️ Commentary generated")
    
    def execute_sigil(self):
        """Execute a consciousness sigil"""
        if "complete" in self.systems:
            self.systems["complete"].execute_consciousness_action("execute_sigil", sigil_name="DEEP_FOCUS")
        elif "sigil_bank" in self.systems:
            self.systems["sigil_bank"].execute_sigil("DEEP_FOCUS")
        else:
            self.add_commentary("🔮 Deep focus protocols engaged")
        
        self.add_console_message("🔮 Sigil executed: DEEP_FOCUS")
    
    def inject_entropy(self):
        """Inject entropy into the system"""
        import random
        entropy_value = 0.7 + random.random() * 0.25
        
        if "complete" in self.systems:
            self.systems["complete"].execute_consciousness_action("inject_entropy", entropy_value=entropy_value)
        else:
            self.current_state["entropy_level"] = entropy_value
            self.add_commentary(f"⚡ Entropy injection: {entropy_value:.3f}")
        
        self.add_console_message(f"⚡ Entropy injected: {entropy_value:.3f}")
        self.update_status_displays()
    
    def emergency_cool(self):
        """Emergency system cooling"""
        if "complete" in self.systems:
            self.systems["complete"].execute_consciousness_action("emergency_cooling")
        elif "pulse_controller" in self.systems:
            self.systems["pulse_controller"].emergency_cooling()
        else:
            self.current_state["thermal_heat"] = max(20, self.current_state["thermal_heat"] - 15)
            self.add_commentary("❄️ Emergency cooling protocols activated")
        
        self.add_console_message("❄️ Emergency cooling executed")
        self.update_status_displays()
    
    def reset_system(self):
        """Reset the consciousness system"""
        if messagebox.askyesno("Reset System", "Are you sure you want to reset the consciousness system?"):
            self.stop_consciousness_monitoring()
            
            # Reset state
            self.current_state = {
                "consciousness_state": "reset",
                "entropy_level": 0.5,
                "current_zone": "CALM",
                "last_commentary": "System reset",
                "active_sigils": 0,
                "thermal_heat": 25.0,
                "components_active": 0,
                "uptime": 0
            }
            
            self.add_commentary("🔄 System reset complete")
            self.add_console_message("🔄 Consciousness system reset")
            self.update_status_displays()
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_consciousness_monitoring()
        self.running = False
        self.root.destroy()


def main():
    """Main function to launch the enhanced GUI"""
    print("🌅 DAWN Enhanced GUI with Unified Launcher")
    print("🧠 Complete Consciousness Control Center")
    print()
    
    try:
        root = tk.Tk()
        app = DAWNUnifiedLauncherGUI(root)
        
        print("🚀 GUI ready - starting main loop")
        root.mainloop()
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 GUI interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ GUI error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 