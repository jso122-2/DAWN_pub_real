#!/usr/bin/env python3
"""
DAWN Cognitive Engine GUI with Integrated Pulse Controller
Enhanced Tkinter interface with pulse controller thermal regulation

File: gui/dawn_gui_tk.py (Updated with Pulse Controller Integration)
"""

import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
import random
from datetime import datetime

# Import DAWN components
try:
    from ..core.pulse_controller import PulseController
    from ..core.sigil_engine import SigilEngine
    DAWN_COMPONENTS_AVAILABLE = True
except ImportError:
    try:
        from core.pulse_controller import PulseController
        from core.sigil_engine import SigilEngine
        DAWN_COMPONENTS_AVAILABLE = True
    except ImportError:
        print("Warning: DAWN core components not found. Using simulation mode.")
        DAWN_COMPONENTS_AVAILABLE = False
        PulseController = None
        SigilEngine = None

# Import visualization components
try:
    from .fractal_canvas import FractalCanvas
except ImportError:
    try:
        from fractal_canvas import FractalCanvas
    except ImportError:
        print("Warning: fractal_canvas.py not found. Fractal viewer will be disabled.")
        FractalCanvas = None

try:
    from .sigil_overlay import SigilOverlayPanel
except ImportError:
    try:
        from sigil_overlay import SigilOverlayPanel
    except ImportError:
        print("Warning: sigil_overlay.py not found. Sigil overlay will be disabled.")
        SigilOverlayPanel = None

try:
    from .owl_console_panel import OwlConsolePanel
except ImportError:
    try:
        from owl_console_panel import OwlConsolePanel
    except ImportError:
        print("Warning: owl_console_panel.py not found. Owl commentary will be disabled.")
        OwlConsolePanel = None

# Import owl-sigil bridge
try:
    from ..core.owl_sigil_bridge import get_owl_sigil_bridge, initialize_owl_sigil_bridge
    OWL_SIGIL_BRIDGE_AVAILABLE = True
except ImportError:
    try:
        from core.owl_sigil_bridge import get_owl_sigil_bridge, initialize_owl_sigil_bridge
        OWL_SIGIL_BRIDGE_AVAILABLE = True
    except ImportError:
        print("Warning: Owl-Sigil bridge not found. Bridge functionality will be disabled.")
        OWL_SIGIL_BRIDGE_AVAILABLE = False


class DAWNGui:
    def __init__(self, root):
        self.root = root
        self.update_queue = queue.Queue()
        self.running = True
        
        # Initialize DAWN components (will be overridden if external components are connected)
        if DAWN_COMPONENTS_AVAILABLE:
            self.pulse_controller = PulseController(initial_heat=25.0)
            self.sigil_engine = SigilEngine(initial_heat=25.0)
            
            # Initialize entropy analyzer
            try:
                from ..core.entropy_analyzer import EntropyAnalyzer
            except ImportError:
                from core.entropy_analyzer import EntropyAnalyzer
            
            try:
                self.entropy_analyzer = EntropyAnalyzer(
                    max_samples_per_bloom=500,
                    volatility_window=30,
                    chaos_threshold=0.7,
                    pulse_controller=self.pulse_controller,
                    sigil_engine=self.sigil_engine
                )
                
                # Connect components
                self.pulse_controller.set_entropy_analyzer(self.entropy_analyzer)
                self.sigil_engine.set_entropy_analyzer(self.entropy_analyzer)
                
                print("🧬 Entropy Analyzer integrated with Pulse Controller and Sigil Engine")
            except ImportError:
                print("⚠️ Entropy Analyzer not available")
                self.entropy_analyzer = None
            
            self.real_dawn_mode = True
            print("✅ Real DAWN mode: Complete integration active")
        else:
            self.pulse_controller = None
            self.sigil_engine = None
            self.entropy_analyzer = None
            self.real_dawn_mode = False
            print("⚠️ Simulation mode: Using mock data")
        
        # Initialize Owl-Sigil Bridge
        self.owl_sigil_bridge = None
        if OWL_SIGIL_BRIDGE_AVAILABLE:
            try:
                self.owl_sigil_bridge = get_owl_sigil_bridge()
                if self.owl_sigil_bridge is None:
                    self.owl_sigil_bridge = initialize_owl_sigil_bridge()
                print("🦉🔮 Owl-Sigil Bridge initialized")
            except Exception as e:
                print(f"⚠️ Failed to initialize Owl-Sigil Bridge: {e}")
                self.owl_sigil_bridge = None
        
        # Flag to track if external components are connected
        self.external_components_connected = False
        
        # Flag to control simulation thread
        self.simulation_enabled = not self.real_dawn_mode
        
        # Current cognitive state data
        self.current_data = {
            "heat": 25.0,
            "zone": "CALM",
            "summary": "DAWN cognitive engine with pulse controller initializing...",
            "tick": "System startup - Pulse controller online, waiting for first cognitive tick...",
            "bloom_data": {
                "depth": 3,
                "entropy": 0.5,
                "lineage": [1, 2, 3],
                "semantic_drift": 0.3,
                "rebloom_status": "stable",
                "complexity": 0.6
            },
            "sigils": [],
            "pulse_stats": {
                "tick_interval": 1.0,
                "grace_period": 0.0,
                "surge_count": 0,
                "zone_transitions": 0
            },
            "owl_observations": [],
            "owl_sigil_connections": {},
            "bridge_activity": {
                "observations_processed": 0,
                "sigils_triggered": 0,
                "reflections_generated": 0,
                "last_activity": None
            }
        }
        
        # Zone color mapping
        self.zone_colors = {
            "CALM": "#4CAF50",      # Green
            "ACTIVE": "#FF9800",    # Orange  
            "SURGE": "#F44336",     # Red
            "DORMANT": "#757575",   # Gray
            "TRANSCENDENT": "#9C27B0"  # Purple
        }
        
        self.setup_gui()
        self.start_update_thread()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def connect_external_components(self, pulse_controller=None, sigil_engine=None, entropy_analyzer=None):
        """Connect external DAWN components to override internal ones"""
        if pulse_controller:
            self.pulse_controller = pulse_controller
            print("🔥 External Pulse Controller connected")
        
        if sigil_engine:
            self.sigil_engine = sigil_engine
            print("🔮 External Sigil Engine connected")
        
        if entropy_analyzer:
            self.entropy_analyzer = entropy_analyzer
            print("🧬 External Entropy Analyzer connected")
        
        if any([pulse_controller, sigil_engine, entropy_analyzer]):
            self.external_components_connected = True
            self.real_dawn_mode = True
            print("✅ External DAWN components integrated")
            
            # Update the title to reflect external connection
            current_title = self.root.title()
            if "External" not in current_title:
                self.root.title(current_title + " - External Components")
                
            # Update mode indicator
            self.update_mode_indicator()
            
            # Disable simulation mode
            self.simulation_enabled = False
            print("🔗 Simulation disabled - using real DAWN data")
            
            # Start activity thread to generate real data changes
            self.start_activity_thread()
    
    def get_mode_text(self):
        """Get current mode text"""
        if self.external_components_connected:
            return "🔗 UNIFIED DAWN MODE"
        elif self.real_dawn_mode:
            return "🔥 REAL DAWN MODE"
        else:
            return "🧪 SIMULATION MODE"
    
    def get_mode_color(self):
        """Get current mode color"""
        if self.external_components_connected:
            return "#00ccff"  # Blue for unified mode
        elif self.real_dawn_mode:
            return "#00ff88"  # Green for real mode
        else:
            return "#ff8800"  # Orange for simulation
    
    def update_mode_indicator(self):
        """Update the mode indicator in the title"""
        if hasattr(self, 'title_label'):
            mode_text = self.get_mode_text()
            self.title_label.config(
                text=f"DAWN Cognitive Engine - {mode_text}",
                fg=self.get_mode_color()
            )
    
    def setup_gui(self):
        """Initialize the GUI layout and widgets"""
        self.root.title("DAWN Cognitive Engine - Owl-Sigil Bridge Integration")
        self.root.geometry("1600x900")  # Larger for pulse controller data
        self.root.configure(bg="#1a1a1a")
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background='#1a1a1a')
        style.configure('Dark.TLabel', background='#1a1a1a', foreground='#ffffff')
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title header with mode indicator
        mode_text = self.get_mode_text()
        self.title_label = tk.Label(main_frame, text=f"DAWN Cognitive Engine - {mode_text}", 
                              font=("Arial", 18, "bold"), 
                              bg="#1a1a1a", fg=self.get_mode_color())
        self.title_label.pack(pady=(0, 15))
        
        # Create four-panel layout
        content_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top row: Left panel for main monitoring, right panel for pulse controller
        top_frame = ttk.Frame(content_frame, style='Dark.TFrame')
        top_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for main monitoring components
        left_panel = ttk.Frame(top_frame, style='Dark.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Right panel for pulse controller
        pulse_panel = ttk.Frame(top_frame, style='Dark.TFrame')
        pulse_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Bottom row: Four panels for fractal bloom, entropy analyzer, owl console, and sigil overlay
        bottom_frame = ttk.Frame(content_frame, style='Dark.TFrame')
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Left bottom panel for fractal bloom viewer
        center_panel = ttk.Frame(bottom_frame, style='Dark.TFrame')
        center_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 3))
        
        # Center-left bottom panel for entropy analyzer
        entropy_panel = ttk.Frame(bottom_frame, style='Dark.TFrame')
        entropy_panel.pack(side=tk.LEFT, fill=tk.Y, padx=3)
        
        # Center-right bottom panel for owl console
        owl_panel = ttk.Frame(bottom_frame, style='Dark.TFrame')
        owl_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
        
        # Right bottom panel for sigil overlay
        right_panel = ttk.Frame(bottom_frame, style='Dark.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(3, 0))
        
        # Setup panels
        self.setup_main_panel(left_panel)
        self.setup_pulse_controller_panel(pulse_panel)
        self.setup_fractal_panel(center_panel)
        self.setup_entropy_panel(entropy_panel)
        self.setup_owl_console_panel(owl_panel)
        self.setup_sigil_panel(right_panel)
    
    def setup_pulse_controller_panel(self, parent):
        """Setup pulse controller monitoring panel"""
        # Title
        pulse_title = tk.Label(parent, text="🔥 Pulse Controller", 
                              font=("Arial", 14, "bold"),
                              bg="#1a1a1a", fg="#ff6b35")
        pulse_title.pack(pady=(0, 10))
        
        # Heat display
        heat_frame = ttk.Frame(parent, style='Dark.TFrame')
        heat_frame.pack(fill=tk.X, pady=(0, 10))
        
        heat_label = tk.Label(heat_frame, text="Thermal Heat", 
                             font=("Arial", 10, "bold"),
                             bg="#1a1a1a", fg="#cccccc")
        heat_label.pack()
        
        self.pulse_heat_value = tk.Label(heat_frame, text="25.0°", 
                                        font=("Arial", 24, "bold"),
                                        bg="#1a1a1a", fg="#00ff88")
        self.pulse_heat_value.pack(pady=5)
        
        # Heat bar
        self.pulse_heat_canvas = tk.Canvas(heat_frame, width=200, height=20, 
                                          bg="#333333", highlightthickness=0)
        self.pulse_heat_canvas.pack()
        
        self.pulse_heat_bg = self.pulse_heat_canvas.create_rectangle(2, 2, 198, 18, 
                                                                    fill="#444444", outline="#666666")
        self.pulse_heat_bar = self.pulse_heat_canvas.create_rectangle(2, 2, 50, 18, 
                                                                     fill="#00ff88", outline="")
        
        # Zone display
        zone_frame = ttk.Frame(parent, style='Dark.TFrame')
        zone_frame.pack(fill=tk.X, pady=(10, 10))
        
        zone_label = tk.Label(zone_frame, text="Pulse Zone", 
                             font=("Arial", 10, "bold"),
                             bg="#1a1a1a", fg="#cccccc")
        zone_label.pack()
        
        self.pulse_zone_value = tk.Label(zone_frame, text="CALM", 
                                        font=("Arial", 16, "bold"),
                                        bg="#1a1a1a", fg="#4CAF50")
        self.pulse_zone_value.pack(pady=5)
        
        # Zone indicator circle
        self.pulse_zone_canvas = tk.Canvas(zone_frame, width=60, height=60, 
                                          bg="#1a1a1a", highlightthickness=0)
        self.pulse_zone_canvas.pack()
        
        self.pulse_zone_circle = self.pulse_zone_canvas.create_oval(10, 10, 50, 50, 
                                                                   fill="#4CAF50", outline="#ffffff", width=2)
        
        # Pulse statistics
        stats_frame = ttk.Frame(parent, style='Dark.TFrame')
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        stats_label = tk.Label(stats_frame, text="Pulse Statistics", 
                              font=("Arial", 10, "bold"),
                              bg="#1a1a1a", fg="#cccccc")
        stats_label.pack()
        
        self.pulse_stats_text = tk.Text(stats_frame, height=12, width=30,
                                       bg="#2a2a2a", fg="#ffffff", 
                                       font=("Courier", 8),
                                       relief=tk.FLAT, bd=3)
        self.pulse_stats_text.pack(pady=(5, 0))
        
        # Control buttons
        controls_frame = ttk.Frame(parent, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.emergency_cooldown_btn = tk.Button(controls_frame, text="🚨 Emergency Cooldown",
                                               command=self.emergency_cooldown,
                                               bg="#ff4444", fg="white", font=("Arial", 8, "bold"))
        self.emergency_cooldown_btn.pack(fill=tk.X, pady=2)
        
        self.regulate_heat_btn = tk.Button(controls_frame, text="🎯 Regulate to 40°",
                                          command=lambda: self.regulate_heat(40.0),
                                          bg="#4488ff", fg="white", font=("Arial", 8, "bold"))
        self.regulate_heat_btn.pack(fill=tk.X, pady=2)
        
        self.inject_heat_btn = tk.Button(controls_frame, text="🔥 Heat Surge +20",
                                        command=lambda: self.inject_heat(20.0),
                                        bg="#ff8800", fg="white", font=("Arial", 8, "bold"))
        self.inject_heat_btn.pack(fill=tk.X, pady=2)
    
    def setup_main_panel(self, parent):
        """Setup main monitoring components"""
        # Top row: Heat and Zone display (now simplified since pulse controller has detail)
        top_frame = ttk.Frame(parent, style='Dark.TFrame')
        top_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.setup_simplified_heat_display(top_frame)
        self.setup_simplified_zone_display(top_frame)
        
        # Middle: Claude memory summary
        self.setup_summary_display(parent)
        
        # Bottom: Tick activity log
        self.setup_tick_log(parent)
        
        # Status bar
        self.setup_status_bar(parent)
    
    def setup_simplified_heat_display(self, parent):
        """Setup simplified heat display for main panel"""
        heat_frame = ttk.Frame(parent, style='Dark.TFrame')
        heat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        heat_title = tk.Label(heat_frame, text="System Heat", 
                             font=("Arial", 12, "bold"),
                             bg="#1a1a1a", fg="#cccccc")
        heat_title.pack()
        
        self.heat_value_label = tk.Label(heat_frame, text="25", 
                                        font=("Arial", 28, "bold"),
                                        bg="#1a1a1a", fg="#00ff88")
        self.heat_value_label.pack(pady=(5, 10))
        
        self.tick_interval_label = tk.Label(heat_frame, text="Tick: 1.000s", 
                                           font=("Arial", 9),
                                           bg="#1a1a1a", fg="#888888")
        self.tick_interval_label.pack()
    
    def setup_simplified_zone_display(self, parent):
        """Setup simplified zone display for main panel"""
        zone_frame = ttk.Frame(parent, style='Dark.TFrame')
        zone_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        zone_title = tk.Label(zone_frame, text="Cognitive Zone", 
                             font=("Arial", 12, "bold"),
                             bg="#1a1a1a", fg="#cccccc")
        zone_title.pack()
        
        self.zone_value_label = tk.Label(zone_frame, text="CALM", 
                                        font=("Arial", 18, "bold"),
                                        bg="#1a1a1a", fg="#4CAF50")
        self.zone_value_label.pack(pady=(5, 10))
        
        self.grace_period_label = tk.Label(zone_frame, text="Grace: 0.0s", 
                                          font=("Arial", 9),
                                          bg="#1a1a1a", fg="#888888")
        self.grace_period_label.pack()
    
    def setup_summary_display(self, parent):
        """Setup Claude memory summary display"""
        summary_frame = ttk.Frame(parent, style='Dark.TFrame')
        summary_frame.pack(fill=tk.X, pady=(0, 15))
        
        summary_title = tk.Label(summary_frame, text="System Summary", 
                                font=("Arial", 11, "bold"),
                                bg="#1a1a1a", fg="#cccccc")
        summary_title.pack(anchor=tk.W)
        
        summary_text_frame = tk.Frame(summary_frame, bg="#1a1a1a")
        summary_text_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.summary_text = tk.Text(summary_text_frame, height=3, 
                                   bg="#2a2a2a", fg="#ffffff", 
                                   font=("Arial", 9),
                                   relief=tk.FLAT, bd=5,
                                   wrap=tk.WORD)
        
        summary_scrollbar = tk.Scrollbar(summary_text_frame, command=self.summary_text.yview)
        self.summary_text.configure(yscrollcommand=summary_scrollbar.set)
        
        self.summary_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_tick_log(self, parent):
        """Setup tick activity log display"""
        log_frame = ttk.Frame(parent, style='Dark.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_title = tk.Label(log_frame, text="Tick Activity Log", 
                            font=("Arial", 11, "bold"),
                            bg="#1a1a1a", fg="#cccccc")
        log_title.pack(anchor=tk.W)
        
        log_text_frame = tk.Frame(log_frame, bg="#1a1a1a")
        log_text_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        self.tick_log_text = tk.Text(log_text_frame, 
                                    bg="#0a0a0a", fg="#00ff88", 
                                    font=("Courier", 8),
                                    relief=tk.FLAT, bd=5,
                                    wrap=tk.WORD)
        
        log_scrollbar = tk.Scrollbar(log_text_frame, command=self.tick_log_text.yview)
        self.tick_log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.tick_log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tick_log_text.see(tk.END)
    
    def setup_status_bar(self, parent):
        """Setup status bar at bottom"""
        status_frame = ttk.Frame(parent, style='Dark.TFrame')
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(status_frame, text="Status: DAWN cognitive engine with pulse controller monitoring...", 
                                    font=("Arial", 8),
                                    bg="#1a1a1a", fg="#888888")
        self.status_label.pack(side=tk.LEFT)
        
        self.time_label = tk.Label(status_frame, text="", 
                                  font=("Arial", 8),
                                  bg="#1a1a1a", fg="#888888")
        self.time_label.pack(side=tk.RIGHT)
    
    def setup_fractal_panel(self, parent):
        """Setup fractal bloom viewer panel"""
        if FractalCanvas is None:
            fallback_label = tk.Label(parent, text="Fractal Bloom\\n(Unavailable)", 
                                     font=("Arial", 10), bg="#1a1a1a", fg="#888888",
                                     width=20, height=15)
            fallback_label.pack(pady=20)
            self.fractal_canvas = None
            return
        
        self.fractal_canvas = FractalCanvas(parent, width=300, height=250)
        self.fractal_canvas.pack(pady=(0, 15))
        
        # Bloom control panel
        self.setup_bloom_controls(parent)
    
    def setup_bloom_controls(self, parent):
        """Setup bloom data control panel"""
        control_frame = ttk.Frame(parent, style='Dark.TFrame')
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        controls_title = tk.Label(control_frame, text="Bloom Parameters", 
                                 font=("Arial", 10, "bold"),
                                 bg="#1a1a1a", fg="#cccccc")
        controls_title.pack()
        
        self.bloom_info_text = tk.Text(control_frame, height=5, width=30,
                                      bg="#2a2a2a", fg="#ffffff", 
                                      font=("Courier", 7),
                                      relief=tk.FLAT, bd=3)
        self.bloom_info_text.pack(pady=(5, 0))
        
        self.update_bloom_info_display()
    
    def setup_entropy_panel(self, parent):
        """Setup entropy analyzer monitoring panel"""
        # Title
        entropy_title = tk.Label(parent, text="🧬 Entropy Analyzer", 
                                font=("Arial", 12, "bold"),
                                bg="#1a1a1a", fg="#9c27b0")
        entropy_title.pack(pady=(0, 10))
        
        # Hot blooms display
        hot_blooms_frame = ttk.Frame(parent, style='Dark.TFrame')
        hot_blooms_frame.pack(fill=tk.X, pady=(0, 5))
        
        hot_blooms_label = tk.Label(hot_blooms_frame, text="🔥 Hot Blooms", 
                                   font=("Arial", 9, "bold"),
                                   bg="#1a1a1a", fg="#cccccc")
        hot_blooms_label.pack()
        
        self.hot_blooms_text = tk.Text(hot_blooms_frame, height=4, width=25,
                                      bg="#2a2a2a", fg="#ff6b35", 
                                      font=("Courier", 7),
                                      relief=tk.FLAT, bd=3)
        self.hot_blooms_text.pack(pady=2)
        
        # Chaos alerts display
        chaos_frame = ttk.Frame(parent, style='Dark.TFrame')
        chaos_frame.pack(fill=tk.X, pady=(5, 5))
        
        chaos_label = tk.Label(chaos_frame, text="🌪️ Chaos Alerts", 
                              font=("Arial", 9, "bold"),
                              bg="#1a1a1a", fg="#cccccc")
        chaos_label.pack()
        
        self.chaos_alerts_text = tk.Text(chaos_frame, height=4, width=25,
                                        bg="#2a2a2a", fg="#f44336", 
                                        font=("Courier", 7),
                                        relief=tk.FLAT, bd=3)
        self.chaos_alerts_text.pack(pady=2)
        
        # Entropy statistics
        stats_frame = ttk.Frame(parent, style='Dark.TFrame')
        stats_frame.pack(fill=tk.X, pady=(5, 5))
        
        stats_label = tk.Label(stats_frame, text="📊 Entropy Stats", 
                              font=("Arial", 9, "bold"),
                              bg="#1a1a1a", fg="#cccccc")
        stats_label.pack()
        
        self.entropy_stats_text = tk.Text(stats_frame, height=6, width=25,
                                         bg="#2a2a2a", fg="#ffffff", 
                                         font=("Courier", 7),
                                         relief=tk.FLAT, bd=3)
        self.entropy_stats_text.pack(pady=2)
        
        # Controls
        controls_frame = ttk.Frame(parent, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Stabilization button
        self.stabilize_button = tk.Button(controls_frame, text="🧬 Stabilize",
                                         command=self.trigger_stabilization,
                                         bg="#4CAF50", fg="white",
                                         font=("Arial", 8, "bold"))
        self.stabilize_button.pack(fill=tk.X, pady=2)
        
        # Entropy injection button
        self.entropy_inject_button = tk.Button(controls_frame, text="🌪️ Inject Chaos",
                                              command=self.inject_entropy_chaos,
                                              bg="#F44336", fg="white",
                                              font=("Arial", 8, "bold"))
        self.entropy_inject_button.pack(fill=tk.X, pady=2)
    
    def setup_owl_console_panel(self, parent):
        """Setup owl console panel for cognitive reflections"""
        # Panel title
        owl_title = tk.Label(parent, text="🦉 Owl Cognitive Observer", 
                            font=("Arial", 12, "bold"),
                            bg="#1a1a1a", fg="#00ccff")
        owl_title.pack(pady=(0, 5))
        
        if OwlConsolePanel is None:
            fallback_label = tk.Label(parent, text="Owl Console\\n(Unavailable)", 
                                     font=("Arial", 10), bg="#1a1a1a", fg="#888888",
                                     width=35, height=10)
            fallback_label.pack(pady=20)
            self.owl_console = None
            return
        
        # Create owl console
        self.owl_console = OwlConsolePanel(parent, height=150)
        self.owl_console.pack(fill=tk.BOTH, expand=True)
        
        # Bridge status indicator
        bridge_status_frame = tk.Frame(parent, bg="#1a1a1a")
        bridge_status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.bridge_status_label = tk.Label(bridge_status_frame, 
                                          text="🔗 Bridge: Initializing...", 
                                          font=("Arial", 8),
                                          bg="#1a1a1a", fg="#888888")
        self.bridge_status_label.pack(side=tk.LEFT)
        
        self.bridge_activity_label = tk.Label(bridge_status_frame, 
                                            text="Activity: 0/0/0", 
                                            font=("Arial", 8),
                                            bg="#1a1a1a", fg="#666666")
        self.bridge_activity_label.pack(side=tk.RIGHT)

    def setup_sigil_panel(self, parent):
        """Setup sigil stream overlay panel"""
        if SigilOverlayPanel is None:
            fallback_label = tk.Label(parent, text="Sigil Stream\\n(Unavailable)", 
                                     font=("Arial", 10), bg="#1a1a1a", fg="#888888",
                                     width=25, height=15)
            fallback_label.pack(pady=20)
            self.sigil_overlay = None
            return
        
        self.sigil_overlay = SigilOverlayPanel(parent, max_sigils=8)
        self.sigil_overlay.pack(fill=tk.BOTH, expand=True)
    
    def inject(self, data):
        """Inject data from external DAWN engine (thread-safe)"""
        try:
            data['timestamp'] = datetime.now().strftime("%H:%M:%S")
            self.update_queue.put(data)
        except Exception as e:
            print(f"Error injecting data: {e}")
    
    def update_gui(self):
        """Process queued updates and refresh GUI"""
        try:
            data_updated = False
            
            # Get real DAWN data if available
            if self.real_dawn_mode and (self.pulse_controller or self.sigil_engine or self.entropy_analyzer):
                self.update_from_real_dawn()
                data_updated = True
            
            while not self.update_queue.empty():
                try:
                    data = self.update_queue.get_nowait()
                    self.current_data.update(data)
                    data_updated = True
                except queue.Empty:
                    break
            
            # Always refresh widgets if we have real data or data was updated
            if data_updated:
                self.refresh_widgets()
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=f"Last update: {current_time}")
            
            if self.running:
                self.root.after(100, self.update_gui)
                
        except Exception as e:
            print(f"Error updating GUI: {e}")
    
    def update_from_real_dawn(self):
        """Update data from real DAWN components"""
        try:
            component_status = []
            tick_events = []
            
            if self.pulse_controller:
                # Get pulse controller stats
                stats = self.pulse_controller.get_heat_statistics()
                
                # Store previous heat and zone for change detection
                prev_heat = self.current_data.get('heat', 0)
                prev_zone = self.current_data.get('zone', 'CALM')
                
                current_heat = stats['current_heat']
                current_zone = stats['current_zone']
                
                self.current_data.update({
                    "heat": current_heat,
                    "zone": current_zone,
                    "pulse_stats": {
                        "tick_interval": stats['current_tick_interval'],
                        "grace_period": stats['current_grace_period'],
                        "surge_count": stats['total_surges'],
                        "zone_transitions": stats['zone_transitions'],
                        "average_heat": stats['average_heat'],
                        "heat_variance": stats['heat_variance'],
                        "uptime": stats['uptime'],
                        "time_in_zone": stats['time_in_current_zone']
                    }
                })
                
                component_status.append(f"Heat: {current_heat:.1f}°")
                component_status.append(f"Zone: {current_zone}")
                
                # Generate tick events for significant changes
                if abs(current_heat - prev_heat) > 1.0:
                    heat_change = "+" if current_heat > prev_heat else ""
                    tick_events.append(f"🌡️ Heat change: {prev_heat:.1f}° → {current_heat:.1f}° ({heat_change}{current_heat - prev_heat:.1f})")
                
                if current_zone != prev_zone:
                    tick_events.append(f"🔄 Zone transition: {prev_zone} → {current_zone}")
            
            if self.sigil_engine:
                # Get sigil engine status
                engine_status = self.sigil_engine.get_engine_status()
                
                # Store previous execution count for change detection
                prev_executions = getattr(self, '_prev_executions', 0)
                current_executions = engine_status.get('total_executions', 0)
                
                component_status.append(f"Active sigils: {engine_status.get('active_sigils', 0)}")
                component_status.append(f"Executions: {current_executions}")
                
                # Get active sigils from the engine
                active_sigils_data = []
                if hasattr(self.sigil_engine, 'active_sigils'):
                    active_sigils_raw = self.sigil_engine.active_sigils
                    for sigil_id, sigil_info in active_sigils_raw.items():
                        # Convert sigil object to display format
                        thermal_sig = getattr(sigil_info, 'thermal_signature', 50.0)
                        decay_rate = getattr(sigil_info, 'decay_rate', 0.0)
                        cognitive_house = getattr(sigil_info, 'cognitive_house', 'unknown')
                        
                        active_sigils_data.append({
                            "symbol": getattr(sigil_info, 'symbol', '◉'),
                            "name": getattr(sigil_info, 'command', sigil_id),
                            "class": cognitive_house,
                            "heat": int(thermal_sig),
                            "decay": decay_rate,
                            "id": sigil_id,
                            "level": getattr(sigil_info, 'level', 1)
                        })
                
                # Update current data with active sigils
                self.current_data["sigils"] = active_sigils_data
                
                # Generate tick events for new executions
                if current_executions > prev_executions:
                    new_executions = current_executions - prev_executions
                    tick_events.append(f"⚡ Sigil executions: +{new_executions} (Total: {current_executions})")
                
                self._prev_executions = current_executions
                
                # Get entropy metrics if available
                if hasattr(self.sigil_engine, 'get_entropy_metrics'):
                    entropy_metrics = self.sigil_engine.get_entropy_metrics()
                    if entropy_metrics.get('chaos_alerts_count', 0) > 0:
                        component_status.append(f"Chaos alerts: {entropy_metrics['chaos_alerts_count']}")
            
            if self.entropy_analyzer:
                # Get entropy analyzer status
                prev_samples = getattr(self, '_prev_entropy_samples', 0)
                current_samples = self.entropy_analyzer.total_samples
                
                component_status.append(f"Entropy samples: {current_samples}")
                component_status.append(f"Hot blooms: {len(self.entropy_analyzer.hot_blooms)}")
                
                # Generate tick events for new entropy samples
                if current_samples > prev_samples:
                    new_samples = current_samples - prev_samples
                    tick_events.append(f"🧬 Entropy analysis: +{new_samples} samples (Total: {current_samples})")
                
                self._prev_entropy_samples = current_samples
                
                if len(self.entropy_analyzer.critical_blooms) > 0:
                    component_status.append(f"Critical blooms: {len(self.entropy_analyzer.critical_blooms)}")
                    tick_events.append(f"🚨 Critical blooms detected: {len(self.entropy_analyzer.critical_blooms)}")
            
            # Generate comprehensive summary
            mode_indicator = "🔗 UNIFIED" if self.external_components_connected else "🔥 INTEGRATED"
            summary = f"{mode_indicator} DAWN System Active | " + " | ".join(component_status)
            self.current_data["summary"] = summary
            
            # Generate owl observations from real system state
            owl_observations = []
            current_heat = self.current_data.get('heat', 0)
            current_zone = self.current_data.get('zone', 'CALM')
            active_sigil_count = len(self.current_data.get('sigils', []))
            
            # Generate observations based on real system state
            if hasattr(self, '_last_heat') and abs(current_heat - self._last_heat) > 5:
                if current_heat > self._last_heat:
                    owl_observations.append({
                        "comment": f"Thermal acceleration detected: {self._last_heat:.1f}° → {current_heat:.1f}°",
                        "type": "highlight"
                    })
                else:
                    owl_observations.append({
                        "comment": f"Thermal stabilization observed: {self._last_heat:.1f}° → {current_heat:.1f}°", 
                        "type": "normal"
                    })
            
            if hasattr(self, '_last_zone') and current_zone != self._last_zone:
                owl_observations.append({
                    "comment": f"Cognitive zone transition: {self._last_zone} → {current_zone}",
                    "type": "insight"
                })
            
            if active_sigil_count > 0:
                active_sigils = self.current_data.get('sigils', [])
                high_heat_sigils = [s for s in active_sigils if s.get('heat', 0) > 70]
                if high_heat_sigils:
                    sigil_names = [s.get('name', 'Unknown') for s in high_heat_sigils[:2]]
                    owl_observations.append({
                        "comment": f"High-intensity sigil activity detected: {', '.join(sigil_names)}",
                        "type": "critical" if len(high_heat_sigils) > 2 else "highlight"
                    })
            
            # Store current values for next comparison
            self._last_heat = current_heat
            self._last_zone = current_zone
            
            # Update owl observations
            if owl_observations:
                existing_observations = self.current_data.get('owl_observations', [])
                self.current_data['owl_observations'] = existing_observations + owl_observations
            
            # Update bridge activity based on real system activity
            bridge_activity = self.current_data.get('bridge_activity', {})
            bridge_activity.update({
                "observations_processed": bridge_activity.get('observations_processed', 0) + len(owl_observations),
                "sigils_triggered": len(self.current_data.get('sigils', [])),
                "reflections_generated": bridge_activity.get('reflections_generated', 0) + (1 if tick_events else 0),
                "last_activity": datetime.now().strftime("%H:%M:%S") if (owl_observations or tick_events) else bridge_activity.get('last_activity')
            })
            self.current_data['bridge_activity'] = bridge_activity
            
            # Add tick events to show real activity
            if tick_events:
                # Pick the most recent/important event
                tick_event = tick_events[-1]
                self.current_data["tick"] = tick_event
                self.current_data["timestamp"] = datetime.now().strftime("%H:%M:%S")
                
        except Exception as e:
            print(f"Error updating from real DAWN: {e}")
    
    def refresh_widgets(self):
        """Refresh all widget displays with current data"""
        try:
            # Update main heat display
            heat = self.current_data.get('heat', 0)
            self.heat_value_label.config(text=str(int(heat)))
            
            # Update main zone display
            zone = self.current_data.get('zone', 'CALM')
            zone_color = self.zone_colors.get(zone, '#888888')
            self.zone_value_label.config(text=zone, fg=zone_color)
            
            # Update pulse controller panel
            self.update_pulse_controller_display()
            
            # Update tick interval and grace period
            pulse_stats = self.current_data.get('pulse_stats', {})
            tick_interval = pulse_stats.get('tick_interval', 1.0)
            grace_period = pulse_stats.get('grace_period', 0.0)
            
            self.tick_interval_label.config(text=f"Tick: {tick_interval:.3f}s")
            self.grace_period_label.config(text=f"Grace: {grace_period:.1f}s")
            
            # Update summary
            summary = self.current_data.get('summary', '')
            if summary:
                self.summary_text.delete(1.0, tk.END)
                self.summary_text.insert(tk.END, summary)
            
            # Update tick log
            tick = self.current_data.get('tick', '')
            if tick:
                timestamp = self.current_data.get('timestamp', datetime.now().strftime("%H:%M:%S"))
                log_entry = f"[{timestamp}] {tick}\\n"
                
                self.tick_log_text.insert(tk.END, log_entry)
                
                lines = self.tick_log_text.get("1.0", tk.END).split('\\n')
                if len(lines) > 100:
                    self.tick_log_text.delete("1.0", f"{len(lines)-100}.0")
                
                self.tick_log_text.see(tk.END)
            
            # Update fractal bloom viewer
            if self.fractal_canvas:
                bloom_data = self.current_data.get('bloom_data', {})
                if bloom_data:
                    # Add real system data for fractal variation
                    bloom_data['system_heat'] = self.current_data.get('heat', 50.0)
                    bloom_data['active_sigils'] = len(self.current_data.get('sigils', []))
                    self.fractal_canvas.draw_bloom_signature(bloom_data)
                    self.update_bloom_info_display()
            
            # Update sigil overlay
            if self.sigil_overlay:
                sigils = self.current_data.get('sigils', [])
                self.sigil_overlay.update_sigils(sigils)
            
            # Update owl console with observations
            if self.owl_console:
                owl_observations = self.current_data.get('owl_observations', [])
                for observation in owl_observations:
                    if not hasattr(observation, '_logged'):  # Prevent duplicate logging
                        self.owl_console.log_comment(
                            observation.get('comment', 'Unknown observation'),
                            msg_type=observation.get('type', 'normal')
                        )
                        observation['_logged'] = True
                
                # Update bridge status
                bridge_activity = self.current_data.get('bridge_activity', {})
                if bridge_activity:
                    observations = bridge_activity.get('observations_processed', 0)
                    sigils = bridge_activity.get('sigils_triggered', 0) 
                    reflections = bridge_activity.get('reflections_generated', 0)
                    activity_text = f"Activity: {observations}/{sigils}/{reflections}"
                    self.bridge_activity_label.config(text=activity_text)
                    
                    last_activity = bridge_activity.get('last_activity')
                    if last_activity and self.external_components_connected:
                        self.bridge_status_label.config(text="🔗 Bridge: Active", fg="#00ff88")
                    else:
                        self.bridge_status_label.config(text="🔗 Bridge: Monitoring", fg="#888888")
            
            # Update entropy panel
            self.update_entropy_panel()
                
        except Exception as e:
            print(f"Error refreshing widgets: {e}")
    
    def update_pulse_controller_display(self):
        """Update pulse controller specific displays"""
        try:
            heat = self.current_data.get('heat', 25.0)
            zone = self.current_data.get('zone', 'CALM')
            pulse_stats = self.current_data.get('pulse_stats', {})
            
            # Update heat display
            self.pulse_heat_value.config(text=f"{heat:.1f}°")
            
            # Update heat bar
            bar_width = int((heat / 100.0) * 196)
            heat_color = self.get_heat_color(heat)
            self.pulse_heat_canvas.coords(self.pulse_heat_bar, 2, 2, 2 + bar_width, 18)
            self.pulse_heat_canvas.itemconfig(self.pulse_heat_bar, fill=heat_color)
            
            # Update zone display
            zone_color = self.zone_colors.get(zone, '#888888')
            self.pulse_zone_value.config(text=zone, fg=zone_color)
            self.pulse_zone_canvas.itemconfig(self.pulse_zone_circle, fill=zone_color)
            
            # Update statistics text
            stats_text = f"""PULSE STATISTICS
{"="*20}
Heat: {heat:.1f}°
Zone: {zone}
Tick Interval: {pulse_stats.get('tick_interval', 0):.3f}s
Grace Period: {pulse_stats.get('grace_period', 0):.1f}s

THERMAL HISTORY
{"="*20}
Average Heat: {pulse_stats.get('average_heat', heat):.1f}°
Heat Variance: {pulse_stats.get('heat_variance', 0):.1f}
Time in Zone: {pulse_stats.get('time_in_zone', 0):.1f}s

SURGE TRACKING  
{"="*20}
Total Surges: {pulse_stats.get('surge_count', 0)}
Zone Transitions: {pulse_stats.get('zone_transitions', 0)}
System Uptime: {pulse_stats.get('uptime', 0):.1f}s"""
            
            self.pulse_stats_text.delete(1.0, tk.END)
            self.pulse_stats_text.insert(tk.END, stats_text)
            
        except Exception as e:
            print(f"Error updating pulse controller display: {e}")
    
    def emergency_cooldown(self):
        """Trigger emergency cooldown"""
        if self.pulse_controller:
            result = self.pulse_controller.emergency_cooldown(25.0)
            self.inject({
                "tick": f"🚨 Emergency cooldown triggered | Heat: {result.get('current_heat', 25):.1f}°"
            })
        else:
            self.inject({
                "heat": 25.0,
                "tick": "🚨 Emergency cooldown triggered (simulation)"
            })
    
    def regulate_heat(self, target_heat: float):
        """Regulate heat to target"""
        if self.pulse_controller:
            result = self.pulse_controller.regulate_heat(target_heat, 0.3)
            self.inject({
                "tick": f"🎯 Heat regulation to {target_heat}° | Current: {result.get('current_heat', target_heat):.1f}°"
            })
        else:
            self.inject({
                "heat": target_heat,
                "tick": f"🎯 Heat regulation to {target_heat}° (simulation)"
            })
    
    def inject_heat(self, heat_increase: float):
        """Inject additional heat"""
        if self.pulse_controller:
            new_heat = self.pulse_controller.current_heat + heat_increase
            result = self.pulse_controller.update_heat(new_heat)
            self.inject({
                "tick": f"🔥 Heat surge +{heat_increase}° | New heat: {result.get('current_heat', new_heat):.1f}°"
            })
        else:
            current_heat = self.current_data.get('heat', 25.0)
            new_heat = min(100.0, current_heat + heat_increase)
            self.inject({
                "heat": new_heat,
                "tick": f"🔥 Heat surge +{heat_increase}° (simulation)"
            })
    
    def update_bloom_info_display(self):
        """Update bloom information display"""
        if hasattr(self, 'bloom_info_text'):
            bloom_data = self.current_data.get('bloom_data', {})
            
            info_text = f"""BLOOM DATA
{"="*15}
Depth: {bloom_data.get('depth', 0)}
Entropy: {bloom_data.get('entropy', 0.0):.3f}
Lineage: {bloom_data.get('lineage', [])}
Drift: {bloom_data.get('semantic_drift', 0.0):.3f}
Status: {bloom_data.get('rebloom_status', 'unknown')}

HEAT INTEGRATION
{"="*15}
Heat: {self.current_data.get('heat', 0):.1f}°
Zone: {self.current_data.get('zone', 'UNKNOWN')}"""
            
            self.bloom_info_text.delete(1.0, tk.END)
            self.bloom_info_text.insert(tk.END, info_text)
    
    def get_heat_color(self, heat):
        """Get color for heat level"""
        if heat < 20:
            return "#4CAF50"
        elif heat < 40:
            return "#8BC34A"
        elif heat < 60:
            return "#FFC107"
        elif heat < 80:
            return "#FF9800"
        else:
            return "#F44336"
    
    def start_update_thread(self):
        """Start the GUI update thread"""
        self.update_gui()
    
    def start_activity_thread(self):
        """Start activity thread to generate real data changes in connected components"""
        def activity_thread():
            import time
            import random
            
            while self.running and self.external_components_connected:
                try:
                    # Trigger some real activity every few seconds
                    time.sleep(2.0)
                    
                    if self.pulse_controller and random.random() < 0.7:
                        # Occasionally adjust heat
                        heat_change = random.uniform(-2.0, 3.0)
                        new_heat = max(20.0, min(95.0, self.pulse_controller.current_heat + heat_change))
                        self.pulse_controller.update_heat(new_heat)
                    
                    if self.sigil_engine and random.random() < 0.5:
                        # Execute a sigil occasionally
                        result = self.sigil_engine.execute_next_sigil()
                        if not result:  # If no sigils available, inject some
                            self.sigil_engine.inject_test_sigils(2)
                    
                    if self.entropy_analyzer and random.random() < 0.4:
                        # Add some entropy samples
                        test_blooms = ["activity_bloom_1", "activity_bloom_2", "dynamic_analysis"]
                        bloom_id = random.choice(test_blooms)
                        entropy = random.uniform(0.2, 0.8)
                        self.entropy_analyzer.add_entropy_sample(bloom_id, entropy, source="gui_activity")
                        
                except Exception as e:
                    print(f"Activity thread error: {e}")
                    break
        
        if self.external_components_connected:
            activity_thread_obj = threading.Thread(target=activity_thread, daemon=True)
            activity_thread_obj.start()
            print("🎬 Activity thread started - generating real DAWN system activity")
    
    def simulate_data(self):
        """Generate simulated cognitive data for testing (fallback mode)"""
        if self.real_dawn_mode:
            return {}  # Real data is handled in update_from_real_dawn
        
        heat = random.randint(20, 90)
        
        if heat < 40:
            zone = "CALM"
        elif heat < 60:
            zone = "ACTIVE"
        else:
            zone = "SURGE"
        
        summaries = [
            f"Pulse controller simulation active. Heat regulation at {heat}° in {zone} zone.",
            f"Thermal dynamics stabilizing. Zone: {zone}, Heat variance tracking normal.",
            f"Cognitive load balancing in progress. Pulse controller maintaining {zone} state.",
            f"Heat signature analysis complete. System operating in {zone} thermal zone.",
        ]
        
        tick_events = [
            f"T{random.randint(1000, 9999)} - Pulse controller tick | Zone: {zone} | Heat: {heat}°",
            f"T{random.randint(1000, 9999)} - Thermal regulation cycle complete",
            f"T{random.randint(1000, 9999)} - Zone transition detected: {zone}",
            f"T{random.randint(1000, 9999)} - Heat variance: ±{random.randint(1, 5)}°",
        ]
        
        # Generate owl observations
        owl_observation_templates = [
            {"comment": "Cognitive entropy stabilizing after thermal event.", "type": "normal"},
            {"comment": "Pattern recognition spike detected in heat transition.", "type": "highlight"},
            {"comment": "Thermal coherence approaching critical threshold.", "type": "critical"},
            {"comment": "Meta-cognitive awareness rising with zone change.", "type": "insight"},
            {"comment": "Pulse regulation optimization in progress.", "type": "normal"},
            {"comment": "Heat-entropy correlation patterns emerging.", "type": "highlight"},
            {"comment": "Zone fragmentation detected in thermal mapping.", "type": "critical"},
            {"comment": "Transcendent thermal state proximity increasing.", "type": "insight"},
        ]
        
        # Generate 0-2 new observations per update (less frequent)
        new_observations = []
        for _ in range(random.randint(0, 2)):
            if random.random() < 0.2:  # 20% chance of new observation
                obs = random.choice(owl_observation_templates).copy()
                new_observations.append(obs)
        
        # Generate bridge activity data (simulation)
        bridge_activity = {
            "observations_processed": random.randint(10, 50),
            "sigils_triggered": random.randint(2, 15),
            "reflections_generated": random.randint(1, 8),
            "last_activity": datetime.now().strftime("%H:%M:%S")
        }
        
        return {
            "heat": heat,
            "zone": zone,
            "summary": random.choice(summaries),
            "tick": random.choice(tick_events),
            "pulse_stats": {
                "tick_interval": max(0.1, 5.0 - (heat / 25.0)),
                "grace_period": max(0, 30 - heat/2) if heat > 60 else 0,
                "surge_count": random.randint(0, 5),
                "zone_transitions": random.randint(0, 10)
            },
            "owl_observations": new_observations,
            "bridge_activity": bridge_activity
        }
    
    def update_entropy_panel(self):
        """Update entropy analyzer panel displays"""
        try:
            if not self.entropy_analyzer:
                # Show simulation data
                self.hot_blooms_text.delete(1.0, tk.END)
                self.hot_blooms_text.insert(tk.END, "bloom_001: 0.85\nbloom_002: 0.73\nbloom_sim: 0.91")
                
                self.chaos_alerts_text.delete(1.0, tk.END)
                self.chaos_alerts_text.insert(tk.END, "bloom_sim: HIGH\nChaos: 0.87\nPredicted: 5min")
                
                self.entropy_stats_text.delete(1.0, tk.END)
                self.entropy_stats_text.insert(tk.END, 
                    "ENTROPY STATS\n=============\nSamples: 342\nHot Blooms: 3\nCooling: 1\nCritical: 0\nGlobal Entropy: 0.45")
                return
            
            # Update hot blooms
            hot_blooms = self.entropy_analyzer.get_hot_blooms(threshold=0.6)
            hot_blooms_text = ""
            for bloom_id, entropy in hot_blooms[:5]:  # Show top 5
                hot_blooms_text += f"{bloom_id}: {entropy:.3f}\n"
            
            self.hot_blooms_text.delete(1.0, tk.END)
            self.hot_blooms_text.insert(tk.END, hot_blooms_text or "No hot blooms")
            
            # Update chaos alerts
            alerts = self.entropy_analyzer.get_chaos_alerts()
            chaos_text = ""
            for alert in alerts[:3]:  # Show top 3
                time_str = ""
                if alert.predicted_cascade_time:
                    delta = alert.predicted_cascade_time - datetime.now()
                    minutes = int(delta.total_seconds() / 60)
                    time_str = f" ({minutes}min)"
                
                chaos_text += f"{alert.bloom_id}: {alert.risk_level.upper()}\n"
                chaos_text += f"Score: {alert.chaos_score:.3f}{time_str}\n\n"
            
            self.chaos_alerts_text.delete(1.0, tk.END)
            self.chaos_alerts_text.insert(tk.END, chaos_text or "No alerts")
            
            # Update entropy statistics
            stats_text = f"""ENTROPY STATS
=================
Samples: {self.entropy_analyzer.total_samples}
Hot Blooms: {len(self.entropy_analyzer.hot_blooms)}
Cooling: {len(self.entropy_analyzer.cooling_blooms)}
Critical: {len(self.entropy_analyzer.critical_blooms)}

GLOBAL METRICS
=================
Mean: {self.entropy_analyzer.global_entropy_mean:.3f}
Std Dev: {self.entropy_analyzer.global_entropy_std:.3f}

CORRELATIONS
=================
Thermal: {'Yes' if self.pulse_controller else 'No'}
Sigil: {'Yes' if self.sigil_engine else 'No'}"""
            
            self.entropy_stats_text.delete(1.0, tk.END)
            self.entropy_stats_text.insert(tk.END, stats_text)
            
        except Exception as e:
            print(f"Error updating entropy panel: {e}")
    
    def trigger_stabilization(self):
        """Trigger entropy stabilization"""
        try:
            if self.entropy_analyzer:
                # Get at-risk blooms
                at_risk = self.entropy_analyzer.recommend_stabilization()
                
                if at_risk:
                    # Apply stabilization to first bloom
                    bloom_id = at_risk[0]
                    self.entropy_analyzer.add_entropy_sample(bloom_id, 0.3, source="stabilization")
                    
                    self.inject({
                        "tick": f"🧬 Entropy stabilization applied to {bloom_id}"
                    })
                else:
                    self.inject({
                        "tick": "🧬 No blooms require stabilization"
                    })
            else:
                self.inject({
                    "tick": "🧬 Stabilization triggered (simulation mode)"
                })
        except Exception as e:
            print(f"Error triggering stabilization: {e}")
    
    def inject_entropy_chaos(self):
        """Inject entropy chaos for testing"""
        try:
            if self.entropy_analyzer:
                # Create chaotic bloom
                chaos_bloom_id = f"chaos_test_{int(time.time())}"
                
                # Inject high entropy samples
                for _ in range(5):
                    high_entropy = 0.8 + random.random() * 0.2
                    self.entropy_analyzer.add_entropy_sample(chaos_bloom_id, high_entropy, source="chaos_test")
                
                self.inject({
                    "tick": f"🌪️ Chaos injection: created volatile bloom {chaos_bloom_id}"
                })
            else:
                self.inject({
                    "tick": "🌪️ Chaos injection triggered (simulation mode)"
                })
        except Exception as e:
            print(f"Error injecting chaos: {e}")
    
    def on_closing(self):
        """Handle window closing"""
        self.running = False
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    gui = DAWNGui(root)
    
    def simulation_thread():
        while gui.running:
            try:
                # Only run simulation if enabled and not using external components
                if gui.simulation_enabled and not gui.external_components_connected:
                    simulated_data = gui.simulate_data()
                    if simulated_data:  # Only inject if in simulation mode
                        gui.inject(simulated_data)
                time.sleep(0.5)
            except Exception as e:
                print(f"Simulation error: {e}")
                break
    
    # Start simulation thread (it will automatically disable when external components connect)
    sim_thread = threading.Thread(target=simulation_thread, daemon=True)
    sim_thread.start()
    
    mode_text = "with Real DAWN Components" if gui.real_dawn_mode else "in Simulation Mode"
    print(f"DAWN Cognitive Engine GUI {mode_text} started")
    print("Pulse Controller Integration active")
    
    root.mainloop()


if __name__ == "__main__":
    main() 