#!/usr/bin/env python3
"""
Enhanced DAWN GUI with Integrated Reflex Components
Comprehensive interface including ReflexExecutor, SymbolicNotation, OwlPanel, and FractalColorizer

File: gui/dawn_gui_enhanced.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import time
import json
import random
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import new reflex components
try:
    from ..reflex.reflex_executor import ReflexExecutor
    from ..reflex.symbolic_notation import SymbolicNotation, NotationMode
    from ..reflex.owl_panel import OwlPanel, OwlCommentType
    from ..reflex.fractal_colorizer import FractalColorizer, ColorSpace
    logger.info("✅ Reflex components imported from parent package")
except ImportError:
    try:
        from reflex.reflex_executor import ReflexExecutor
        from reflex.symbolic_notation import SymbolicNotation, NotationMode
        from reflex.owl_panel import OwlPanel, OwlCommentType
        from reflex.fractal_colorizer import FractalColorizer, ColorSpace
        logger.info("✅ Reflex components imported from reflex package")
    except ImportError:
        logger.error("❌ Reflex components not found. Some features will be disabled.")
        ReflexExecutor = None
        SymbolicNotation = None
        OwlPanel = None
        FractalColorizer = None

# Import existing DAWN components
try:
    from ..core.pulse_controller import PulseController
    from ..core.sigil_engine import SigilEngine
    from ..gui.fractal_canvas import FractalCanvas
    DAWN_COMPONENTS_AVAILABLE = True
    logger.info("✅ DAWN components imported from parent package")
except ImportError:
    try:
        from core.pulse_controller import PulseController
        from core.sigil_engine import SigilEngine
        from gui.fractal_canvas import FractalCanvas
        DAWN_COMPONENTS_AVAILABLE = True
        logger.info("✅ DAWN components imported from core package")
    except ImportError:
        logger.warning("⚠️ DAWN core components not found. Using simulation mode.")
        DAWN_COMPONENTS_AVAILABLE = False
        PulseController = None
        SigilEngine = None
        FractalCanvas = None


class EnhancedDAWNGui:
    """
    Enhanced DAWN GUI with integrated reflex components.
    Provides comprehensive monitoring and control interface.
    """
    
    def __init__(self, root):
        logger.info("🏗️ Starting EnhancedDAWNGui initialization...")
        
        self.root = root
        self.update_queue = queue.Queue()
        self.running = True
        
        logger.info("📊 Initializing DAWN components...")
        # Initialize DAWN components
        if DAWN_COMPONENTS_AVAILABLE:
            logger.info("🔥 Creating real PulseController...")
            self.pulse_controller = PulseController(initial_heat=25.0)
            logger.info("🔮 Creating real SigilEngine...")
            self.sigil_engine = SigilEngine(initial_heat=25.0)
            self.real_dawn_mode = True
            logger.info("✅ Real DAWN components initialized")
        else:
            logger.info("🤖 Creating mock components...")
            self.pulse_controller = self._create_mock_pulse()
            self.sigil_engine = self._create_mock_sigil_ring()
            self.real_dawn_mode = False
            logger.info("✅ Mock components initialized")
        
        # Initialize LIVE consciousness metrics engine
        logger.info("🧠 Creating live ConsciousnessMetrics engine...")
        try:
            from core.consciousness_metrics import ConsciousnessMetrics
            self.consciousness_metrics = ConsciousnessMetrics(history_size=100)
            logger.info("✅ Live consciousness metrics engine initialized")
        except ImportError as e:
            logger.warning(f"⚠️ ConsciousnessMetrics not available ({e}), using basic consciousness")
            try:
                from core.consciousness_core import ConsciousnessCore
                self.consciousness_core = ConsciousnessCore()
                self.consciousness_metrics = None
                logger.info("✅ Basic consciousness core initialized as fallback")
            except ImportError:
                logger.warning("⚠️ No consciousness system available")
                self.consciousness_core = None
                self.consciousness_metrics = None
        
        logger.info("🤖 Initializing reflex components...")
        # Initialize reflex components
        self._initialize_reflex_components()
        
        # Current system state
        logger.info("📊 Setting up system state...")
        self.current_state = {
            "heat": 25.0,
            "zone": "CALM",
            "entropy": 0.5,
            "mood": "neutral",
            "tick_id": 0,
            "bloom_count": 0,
            "active_sigils": 0,
            "thermal_state": "normal"
        }
        
        # GUI component references
        logger.info("🎛️ Initializing GUI component references...")
        self.gui_components = {}
        self.notification_system = NotificationSystem()
        
        # Setup GUI
        logger.info("🎨 Setting up enhanced GUI...")
        self.setup_enhanced_gui()
        
        logger.info("⚡ Starting update systems...")
        self.start_update_systems()
        
        # Bind window close event
        logger.info("🔗 Binding window close event...")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        logger.info("🚀 Enhanced DAWN GUI initialization complete!")
    
    def _initialize_reflex_components(self):
        """Initialize all reflex system components"""
        logger.info("🔄 Starting reflex component initialization...")
        
        # Mock tick loop for reflex executor
        logger.info("⚡ Creating mock tick loop...")
        tick_loop = self._create_mock_tick_loop()
        
        # Initialize reflex components
        if ReflexExecutor:
            logger.info("🎯 Initializing ReflexExecutor...")
            self.reflex_executor = ReflexExecutor(
                self.pulse_controller, 
                self.sigil_engine, 
                tick_loop
            )
            logger.info("✅ ReflexExecutor initialized")
        else:
            logger.warning("❌ ReflexExecutor not available")
            self.reflex_executor = None
            
        if SymbolicNotation:
            logger.info("🔤 Initializing SymbolicNotation...")
            self.symbolic_notation = SymbolicNotation(mode="emoji")
            logger.info("✅ SymbolicNotation initialized")
        else:
            logger.warning("❌ SymbolicNotation not available")
            self.symbolic_notation = None
            
        if OwlPanel:
            logger.info("🦉 Initializing OwlPanel...")
            self.owl_panel = OwlPanel(max_entries=200, auto_scroll=True)
            logger.info("✅ OwlPanel initialized")
        else:
            logger.warning("❌ OwlPanel not available")
            self.owl_panel = None
            
        if FractalColorizer:
            logger.info("🎨 Initializing FractalColorizer...")
            self.fractal_colorizer = FractalColorizer()
            logger.info("✅ FractalColorizer initialized")
        else:
            logger.warning("❌ FractalColorizer not available")
            self.fractal_colorizer = None
            
        logger.info("🤖 Reflex component initialization complete")
    
    def setup_enhanced_gui(self):
        """Setup the main GUI interface with enhanced design"""
        logger.debug("🎨 Starting enhanced GUI setup...")
        
        try:
            # Set window properties with high visibility
            logger.debug("🪟 Setting window properties...")
            self.root.title("🌟 Enhanced DAWN GUI - Cognitive Engine")
            self.root.geometry("1400x900")
            self.root.configure(bg="#000000")  # Pure black background for high contrast
            
            # Force window to front and make it topmost temporarily
            self.root.lift()
            self.root.attributes("-topmost", True)
            self.root.after_idle(lambda: self.root.attributes("-topmost", False))
            
            logger.debug("✅ Window properties set")
            
            # Setup dark theme with high contrast colors
            logger.debug("🎨 Setting up high-contrast theme...")
            style = ttk.Style()
            style.theme_use('clam')
            
            # High contrast color scheme
            style.configure("TNotebook", background="#000000", foreground="#FFFFFF")
            style.configure("TNotebook.Tab", background="#333333", foreground="#FFFFFF", 
                           lightcolor="#666666", borderwidth=2)
            style.map("TNotebook.Tab", background=[("selected", "#555555")])
            
            logger.debug("✅ High-contrast theme configured")
            
            # Create main notebook with high contrast
            logger.debug("📖 Creating main notebook...")
            main_notebook = ttk.Notebook(self.root)
            main_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            logger.debug("✅ Main notebook created and packed")
            
            # Create all tabs with high visibility
            logger.debug("📊 Setting up main dashboard tab...")
            try:
                self.setup_main_dashboard_tab(main_notebook)
                logger.debug("✅ Main dashboard tab created")
            except Exception as e:
                logger.error(f"❌ Main dashboard tab failed: {e}")
                
            logger.debug("🎯 Setting up reflex control tab...")
            try:
                self.setup_reflex_control_tab(main_notebook)
                logger.debug("✅ Reflex control tab created")
            except Exception as e:
                logger.error(f"❌ Reflex control tab failed: {e}")
                
            logger.debug("🔤 Setting up symbolic analysis tab...")
            try:
                self.setup_symbolic_analysis_tab(main_notebook)
                logger.debug("✅ Symbolic analysis tab created")
            except Exception as e:
                logger.error(f"❌ Symbolic analysis tab failed: {e}")
                
            logger.debug("🦉 Setting up owl commentary tab...")
            try:
                self.setup_owl_commentary_tab(main_notebook)
                logger.debug("✅ Owl commentary tab created")
            except Exception as e:
                logger.error(f"❌ Owl commentary tab failed: {e}")
                
            logger.debug("🌈 Setting up visual analysis tab...")
            try:
                self.setup_visual_analysis_tab(main_notebook)
                logger.debug("✅ Visual analysis tab created")
            except Exception as e:
                logger.error(f"❌ Visual analysis tab failed: {e}")
            
            # Setup status bar
            logger.debug("📊 Setting up status bar...")
            try:
                self.setup_status_bar()
                logger.debug("✅ Status bar created")
            except Exception as e:
                logger.error(f"❌ Status bar failed: {e}")
            
            # Add visible test content to ensure GUI is working
            logger.debug("🧪 Adding test visibility content...")
            test_label = tk.Label(
                self.root,
                text="🚀 ENHANCED DAWN GUI IS RUNNING! 🚀",
                font=("Arial", 16, "bold"),
                fg="#00FF00",  # Bright green
                bg="#000000",  # Black background
                pady=20
            )
            test_label.pack()
            
            # Force immediate window update and focus
            self.root.update()
            self.root.focus_force()
            
            logger.debug("🎨 Enhanced GUI setup complete!")
            
        except Exception as e:
            logger.error(f"❌ Enhanced GUI setup failed: {e}")
            import traceback
            logger.error(f"💥 Full traceback: {traceback.format_exc()}")
    
    def setup_main_dashboard_tab(self, notebook):
        """Setup main monitoring dashboard tab"""
        logger.info("📊 Creating main dashboard tab frame...")
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="🎛️ Main Dashboard")
        logger.info("✅ Main dashboard frame created and added to notebook")
        
        # Top panel: System overview with symbolic notation
        logger.info("🔝 Setting up system overview panel...")
        try:
            self.setup_system_overview_panel(main_frame)
            logger.info("✅ System overview panel created")
        except Exception as e:
            logger.error(f"❌ Failed to create system overview panel: {e}")
            raise
        
        # Middle panel: Four-column layout
        logger.info("🏢 Creating middle frame...")
        middle_frame = ttk.Frame(main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        logger.info("✅ Middle frame created and packed")
        
        # Thermal & Pulse Control
        logger.info("🔥 Creating thermal control frame...")
        thermal_frame = ttk.LabelFrame(middle_frame, text="🔥 Thermal Control")
        thermal_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        logger.info("✅ Thermal frame created and packed")
        
        logger.info("🔥 Setting up enhanced thermal panel...")
        try:
            self.setup_enhanced_thermal_panel(thermal_frame)
            logger.info("✅ Enhanced thermal panel created")
        except Exception as e:
            logger.error(f"❌ Failed to create enhanced thermal panel: {e}")
            raise
        
        # Bloom Visualization with Colors
        logger.info("🌸 Creating bloom frame...")
        bloom_frame = ttk.LabelFrame(middle_frame, text="🌸 Bloom State")
        bloom_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        logger.info("✅ Bloom frame created and packed")
        
        logger.info("🌸 Setting up enhanced bloom panel...")
        try:
            self.setup_enhanced_bloom_panel(bloom_frame)
            logger.info("✅ Enhanced bloom panel created")
        except Exception as e:
            logger.error(f"❌ Failed to create enhanced bloom panel: {e}")
            # Don't raise, continue with other panels
        
        # Sigil Ring Status
        logger.info("◈ Creating sigil frame...")
        sigil_frame = ttk.LabelFrame(middle_frame, text="◈ Sigil Ring")
        sigil_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        logger.info("✅ Sigil frame created and packed")
        
        logger.info("◈ Setting up enhanced sigil panel...")
        try:
            self.setup_enhanced_sigil_panel(sigil_frame)
            logger.info("✅ Enhanced sigil panel created")
        except Exception as e:
            logger.error(f"❌ Failed to create enhanced sigil panel: {e}")
            # Don't raise, continue with other panels
        
        # Quick Actions
        logger.info("⚡ Creating actions frame...")
        actions_frame = ttk.LabelFrame(middle_frame, text="⚡ Quick Actions")
        actions_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        logger.info("✅ Actions frame created and packed")
        
        logger.info("⚡ Setting up quick actions panel...")
        try:
            self.setup_quick_actions_panel(actions_frame)
            logger.info("✅ Quick actions panel created")
        except Exception as e:
            logger.error(f"❌ Failed to create quick actions panel: {e}")
            # Don't raise, continue
            
        logger.info("📊 Main dashboard tab setup complete!")
    
    def setup_reflex_control_tab(self, notebook):
        """Setup reflex control center tab"""
        reflex_frame = ttk.Frame(notebook)
        notebook.add(reflex_frame, text="🤖 Reflex Control")
        
        # Top: Reflex status overview
        status_frame = ttk.LabelFrame(reflex_frame, text="🔍 Reflex System Status")
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        self.setup_reflex_status_panel(status_frame)
        
        # Middle: Command execution panel
        command_frame = ttk.LabelFrame(reflex_frame, text="⚙️ Command Execution")
        command_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.setup_reflex_command_panel(command_frame)
        
        # Bottom: Execution history
        history_frame = ttk.LabelFrame(reflex_frame, text="📜 Execution History")
        history_frame.pack(fill=tk.X, padx=10, pady=5)
        self.setup_reflex_history_panel(history_frame)
    
    def setup_symbolic_analysis_tab(self, notebook):
        """Setup symbolic notation analysis tab"""
        symbolic_frame = ttk.Frame(notebook)
        notebook.add(symbolic_frame, text="🔤 Symbolic Analysis")
        
        try:
            # Check if symbolic notation is available
            if not self.symbolic_notation:
                tk.Label(symbolic_frame, text="⚠️ Symbolic notation not available\nSymbolic analysis will be limited", 
                        font=("Arial", 12), fg="#FF9800", bg="#0a0a0a", justify=tk.CENTER).pack(expand=True)
                return
            
            # Mode selector
            mode_frame = ttk.LabelFrame(symbolic_frame, text="🎨 Notation Mode")
            mode_frame.pack(fill=tk.X, padx=10, pady=5)
            self.setup_notation_mode_panel(mode_frame)
            
            # Symbol browser
            browser_frame = ttk.LabelFrame(symbolic_frame, text="🔍 Symbol Browser")
            browser_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.setup_symbol_browser_panel(browser_frame)
            
            # Live translation
            translation_frame = ttk.LabelFrame(symbolic_frame, text="🔄 Live Translation")
            translation_frame.pack(fill=tk.X, padx=10, pady=5)
            self.setup_live_translation_panel(translation_frame)
            
        except Exception as e:
            tk.Label(symbolic_frame, text=f"❌ Error setting up symbolic analysis:\n{str(e)}", 
                    font=("Arial", 10), fg="#F44336", bg="#0a0a0a", justify=tk.CENTER).pack(expand=True)
    
    def setup_owl_commentary_tab(self, notebook):
        """Setup owl commentary tab with embedded owl panel"""
        owl_frame = ttk.Frame(notebook)
        notebook.add(owl_frame, text="🦉 Owl Commentary")
        
        if self.owl_panel:
            # Embed the owl panel GUI
            self.owl_panel.create_gui(owl_frame)
            
            # Add controls for filtering and analysis
            controls_frame = ttk.LabelFrame(owl_frame, text="🎛️ Commentary Controls")
            controls_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
            self.setup_owl_controls_panel(controls_frame)
        else:
            no_owl_label = tk.Label(owl_frame, text="🦉 Owl Panel not available", 
                                  font=("Arial", 16), bg="#0a0a0a", fg="#666666")
            no_owl_label.pack(expand=True)
    
    def setup_visual_analysis_tab(self, notebook):
        """Setup color and visual analysis tab"""
        visual_frame = ttk.Frame(notebook)
        notebook.add(visual_frame, text="🎨 Visual Analysis")
        
        try:
            # Check if fractal colorizer is available
            if not self.fractal_colorizer:
                tk.Label(visual_frame, text="⚠️ Fractal colorizer not available\nVisual analysis will be limited", 
                        font=("Arial", 12), fg="#FF9800", bg="#0a0a0a", justify=tk.CENTER).pack(expand=True)
                return
            
            # Color palette generator
            palette_frame = ttk.LabelFrame(visual_frame, text="🌈 Color Palettes")
            palette_frame.pack(fill=tk.X, padx=10, pady=5)
            self.setup_color_palette_panel(palette_frame)
            
            # Entropy visualization
            entropy_vis_frame = ttk.LabelFrame(visual_frame, text="📊 Entropy Visualization")
            entropy_vis_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
            self.setup_entropy_visualization_panel(entropy_vis_frame)
            
            # Mood-color mapping
            mood_frame = ttk.LabelFrame(visual_frame, text="😊 Mood-Color Mapping")
            mood_frame.pack(fill=tk.X, padx=10, pady=5)
            self.setup_mood_color_panel(mood_frame)
            
        except Exception as e:
            tk.Label(visual_frame, text=f"❌ Error setting up visual analysis:\n{str(e)}", 
                    font=("Arial", 10), fg="#F44336", bg="#0a0a0a", justify=tk.CENTER).pack(expand=True)
    
    def setup_system_overview_panel(self, parent):
        """Setup system overview with symbolic notation"""
        overview_frame = ttk.LabelFrame(parent, text="🎯 System Overview")
        overview_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create grid layout for status indicators
        for i in range(3):
            overview_frame.columnconfigure(i, weight=1)
        
        self.gui_components['thermal_symbol'] = tk.Label(
            overview_frame, text="🟢 CALM", font=("Arial", 14, "bold"), 
            bg="#0a0a0a", fg="#4CAF50"
        )
        self.gui_components['thermal_symbol'].grid(row=0, column=0, padx=10, pady=5)
        
        self.gui_components['bloom_symbol'] = tk.Label(
            overview_frame, text="🌸 Active", font=("Arial", 14, "bold"),
            bg="#0a0a0a", fg="#E91E63"
        )
        self.gui_components['bloom_symbol'].grid(row=0, column=1, padx=10, pady=5)
        
        self.gui_components['sigil_symbol'] = tk.Label(
            overview_frame, text="◈ 3 Active", font=("Arial", 14, "bold"),
            bg="#0a0a0a", fg="#2196F3"
        )
        self.gui_components['sigil_symbol'].grid(row=0, column=2, padx=10, pady=5)
        
        # Symbolic status string
        self.gui_components['symbolic_status'] = tk.Label(
            overview_frame, text="🟢 🌸 ◈ ⚙️ 🦉", font=("Arial", 16),
            bg="#0a0a0a", fg="#ffffff"
        )
        self.gui_components['symbolic_status'].grid(row=1, column=0, columnspan=3, pady=10)
    
    def setup_enhanced_thermal_panel(self, parent_frame):
        """Setup enhanced thermal control panel with real-time heat visualization"""
        logger.debug("🔥 Setting up enhanced thermal panel...")
        
        # Main thermal frame
        thermal_main = tk.Frame(parent_frame, bg="#2E2E2E")
        thermal_main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title
        title_label = tk.Label(thermal_main, text="🔥 Thermal Control", 
                              font=("Helvetica", 12, "bold"), fg="#FF6B35", bg="#2E2E2E")
        title_label.pack(pady=(0, 5))
        
        # Heat display
        heat_frame = tk.Frame(thermal_main, bg="#2E2E2E")
        heat_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(heat_frame, text="Heat:", font=("Helvetica", 10), fg="white", bg="#2E2E2E").pack(side=tk.LEFT)
        heat_value = tk.Label(heat_frame, text="25.0°", font=("Helvetica", 10, "bold"), fg="#FF6B35", bg="#2E2E2E")
        heat_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Register heat value component for updates
        self.gui_components['heat_value'] = heat_value
        logger.debug("🔥 Heat value component registered")
        
        # Zone display
        zone_frame = tk.Frame(thermal_main, bg="#2E2E2E")
        zone_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(zone_frame, text="Zone:", font=("Helvetica", 10), fg="white", bg="#2E2E2E").pack(side=tk.LEFT)
        zone_value = tk.Label(zone_frame, text="CALM", font=("Helvetica", 10, "bold"), fg="#4CAF50", bg="#2E2E2E")
        zone_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Register zone value component
        self.gui_components['zone_value'] = zone_value
        logger.debug("🌊 Zone value component registered")
        
        # Thermal controls
        controls_frame = tk.Frame(thermal_main, bg="#2E2E2E")
        controls_frame.pack(fill=tk.X, pady=5)
        
        # Control buttons
        tk.Button(controls_frame, text="Cool Down", 
                command=self.execute_cool_down, bg="#2196F3", fg="white").pack(fill=tk.X, pady=2)
        tk.Button(controls_frame, text="Heat Up", 
                command=self.execute_heat_up, bg="#FF5722", fg="white").pack(fill=tk.X, pady=2)
        tk.Button(controls_frame, text="Stabilize", 
                command=self.execute_stabilize, bg="#4CAF50", fg="white").pack(fill=tk.X, pady=2)
        
        logger.debug("✅ Enhanced thermal panel created")
    
    def setup_enhanced_bloom_panel(self, parent):
        """Enhanced bloom panel with color-coded states"""
        # Bloom status with color
        self.gui_components['bloom_status'] = tk.Label(
            parent, text="🌸 Stable", font=("Arial", 16, "bold"),
            bg="#0a0a0a", fg="#E91E63"
        )
        self.gui_components['bloom_status'].pack(pady=5)
        
        # Bloom color preview
        self.gui_components['bloom_color_canvas'] = tk.Canvas(
            parent, width=150, height=50, bg="#1a1a1a", highlightthickness=0
        )
        self.gui_components['bloom_color_canvas'].pack(pady=10)
        
        # Bloom metrics
        metrics_frame = tk.Frame(parent, bg="#0a0a0a")
        metrics_frame.pack(fill=tk.X, pady=5)
        
        self.gui_components['bloom_entropy'] = tk.Label(
            metrics_frame, text="Entropy: 0.50", font=("Arial", 10),
            bg="#0a0a0a", fg="#cccccc"
        )
        self.gui_components['bloom_entropy'].pack()
        
        self.gui_components['bloom_depth'] = tk.Label(
            metrics_frame, text="Depth: 3", font=("Arial", 10),
            bg="#0a0a0a", fg="#cccccc"
        )
        self.gui_components['bloom_depth'].pack()
    
    def setup_enhanced_sigil_panel(self, parent_frame):
        """Setup enhanced sigil management panel"""
        logger.debug("🔮 Setting up enhanced sigil panel...")
        
        # Main sigil frame
        sigil_main = tk.Frame(parent_frame, bg="#2E2E2E")
        sigil_main.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title
        title_label = tk.Label(sigil_main, text="◈ Sigil Management", 
                              font=("Helvetica", 12, "bold"), fg="#9C27B0", bg="#2E2E2E")
        title_label.pack(pady=(0, 5))
        
        # Sigil count display
        sigil_frame = tk.Frame(sigil_main, bg="#2E2E2E")
        sigil_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(sigil_frame, text="Active Sigils:", font=("Helvetica", 10), fg="white", bg="#2E2E2E").pack(side=tk.LEFT)
        sigil_symbol = tk.Label(sigil_frame, text="◈ 0 Active", font=("Helvetica", 10, "bold"), fg="#9C27B0", bg="#2E2E2E")
        sigil_symbol.pack(side=tk.LEFT, padx=(5, 0))
        
        # Register sigil symbol component
        self.gui_components['sigil_symbol'] = sigil_symbol
        logger.debug("🔮 Sigil symbol component registered")
        
        # Entropy display in sigil panel
        entropy_frame = tk.Frame(sigil_main, bg="#2E2E2E")
        entropy_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(entropy_frame, text="System Entropy:", font=("Helvetica", 10), fg="white", bg="#2E2E2E").pack(side=tk.LEFT)
        entropy_value = tk.Label(entropy_frame, text="Entropy: 0.000", font=("Helvetica", 10, "bold"), fg="#FF9800", bg="#2E2E2E")
        entropy_value.pack(side=tk.LEFT, padx=(5, 0))
        
        # Register entropy value component
        self.gui_components['entropy_value'] = entropy_value
        logger.debug("🧬 Entropy value component registered")
        
        # Sigil controls
        controls_frame = tk.Frame(sigil_main, bg="#2E2E2E")
        controls_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(controls_frame, text="Execute Sigil", 
                command=self.execute_next_sigil, bg="#9C27B0", fg="white").pack(fill=tk.X, pady=2)
        tk.Button(controls_frame, text="Clear Sigils", 
                command=self.execute_clear_sigils, bg="#F44336", fg="white").pack(fill=tk.X, pady=2)
        
        logger.debug("✅ Enhanced sigil panel created")
    
    def setup_quick_actions_panel(self, parent):
        """Quick action buttons with reflex integration"""
        actions = [
            ("🐌 Slow Tick", lambda: self.execute_reflex_command("slow_tick")),
            ("🛑 Block Rebloom", lambda: self.execute_reflex_command("suppress_rebloom")),
            ("🧹 Prune Sigils", lambda: self.execute_reflex_command("prune_sigils")),
            ("🔄 Restore Normal", self.restore_normal_operation),
            ("🦉 Add Comment", self.add_test_owl_comment),
            ("🎨 Change Colors", self.cycle_color_mood)
        ]
        
        for text, command in actions:
            tk.Button(parent, text=text, command=command, 
                     bg="#607D8B", fg="white", font=("Arial", 9)).pack(fill=tk.X, pady=2)
    
    def setup_reflex_status_panel(self, parent):
        """Setup reflex system status display"""
        if not self.reflex_executor:
            tk.Label(parent, text="Reflex system not available", fg="#666666").pack()
            return
            
        status_text = tk.Text(parent, height=5, bg="#1a1a1a", fg="#ffffff", 
                             font=("Courier", 10), state=tk.DISABLED)
        status_text.pack(fill=tk.X, padx=10, pady=5)
        self.gui_components['reflex_status'] = status_text
        
    def setup_reflex_command_panel(self, parent):
        """Setup reflex command execution panel"""
        if not self.reflex_executor:
            # Show a proper message instead of leaving blank
            tk.Label(parent, text="⚠️ Reflex executor not available\nReflex commands will be unavailable", 
                    font=("Arial", 12), fg="#FF9800", bg="#0a0a0a", justify=tk.CENTER).pack(expand=True)
            return
            
        # Command buttons
        cmd_frame = tk.Frame(parent, bg="#0a0a0a")
        cmd_frame.pack(fill=tk.X, padx=10, pady=5)
        
        commands = [
            ("🐌 Slow Tick", "slow_tick"),
            ("🛑 Suppress Rebloom", "suppress_rebloom"), 
            ("🧹 Prune Sigils", "prune_sigils")
        ]
        
        for text, cmd in commands:
            tk.Button(cmd_frame, text=text, 
                     command=lambda c=cmd: self.execute_reflex_command(c),
                     bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Results display
        results_text = tk.Text(parent, height=15, bg="#1a1a1a", fg="#ffffff",
                              font=("Courier", 9), state=tk.DISABLED)
        results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.gui_components['reflex_results'] = results_text
        
    def execute_reflex_command(self, command):
        """Execute a reflex command and display results"""
        if not self.reflex_executor:
            return
            
        try:
            results = self.reflex_executor.execute([command])
            self.display_reflex_results(results)
            
            # Add owl commentary
            if self.owl_panel:
                self.owl_panel.add_comment(
                    self.current_state['tick_id'],
                    f"Reflex command executed: {command}",
                    OwlCommentType.SYSTEM,
                    priority=3
                )
        except Exception as e:
            messagebox.showerror("Reflex Error", f"Failed to execute {command}: {e}")
    
    def display_reflex_results(self, results):
        """Display reflex execution results"""
        if 'reflex_results' not in self.gui_components:
            return
            
        text_widget = self.gui_components['reflex_results']
        text_widget.config(state=tk.NORMAL)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        text_widget.insert(tk.END, f"\n[{timestamp}] Reflex Execution Results:\n")
        
        for cmd, result in results.items():
            status = result.get('status', 'unknown')
            message = result.get('message', 'No message')
            text_widget.insert(tk.END, f"  {cmd}: {status} - {message}\n")
        
        text_widget.insert(tk.END, "-" * 50 + "\n")
        text_widget.see(tk.END)
        text_widget.config(state=tk.DISABLED)
        
        # Also update history panel if available
        if 'reflex_history' in self.gui_components:
            history_widget = self.gui_components['reflex_history']
            history_widget.config(state=tk.NORMAL)
            
            for cmd, result in results.items():
                status = result.get('status', 'unknown')
                history_widget.insert(tk.END, f"[{timestamp}] {cmd}: {status}\n")
            
            history_widget.see(tk.END)
            history_widget.config(state=tk.DISABLED)
    
    def update_visual_displays(self):
        """Update all visual displays with current state from real DAWN components"""
        logger.debug("🔄 Updating visual displays...")
        
        try:
            # === COMPREHENSIVE DEBUG DATA COLLECTION ===
            debug_data = {
                'pulse_controller': {},
                'sigil_engine': {},
                'entropy_analyzer': {},
                'consciousness_core': {},
                'tick_engine': {},
                'dream_conductor': {},
                'gui_components': {}
            }
            
            # === REAL DATA COLLECTION FROM DAWN COMPONENTS ===
            
            # Get real thermal data from pulse controller
            if hasattr(self, 'pulse_controller') and self.pulse_controller:
                logger.debug("🔥 Examining pulse controller...")
                try:
                    # Log all pulse controller attributes
                    pulse_attrs = [attr for attr in dir(self.pulse_controller) if not attr.startswith('_')]
                    logger.debug(f"🔥 Pulse controller attributes: {pulse_attrs}")
                    
                    if hasattr(self.pulse_controller, 'current_heat'):
                        heat_value = self.pulse_controller.current_heat
                        self.current_state['heat'] = heat_value
                        debug_data['pulse_controller']['current_heat'] = heat_value
                        logger.debug(f"🔥 Heat: {heat_value}")
                    
                    if hasattr(self.pulse_controller, 'current_zone'):
                        zone_value = self.pulse_controller.current_zone
                        self.current_state['zone'] = zone_value
                        debug_data['pulse_controller']['current_zone'] = zone_value
                        logger.debug(f"🌊 Zone: {zone_value}")
                    
                    # Try to get all possible thermal data
                    thermal_methods = ['get_current_heat', 'get_zone', 'get_thermal_state', 'get_heat_statistics']
                    for method in thermal_methods:
                        if hasattr(self.pulse_controller, method):
                            try:
                                result = getattr(self.pulse_controller, method)()
                                debug_data['pulse_controller'][method] = result
                                logger.debug(f"🔥 {method}: {result}")
                            except Exception as e:
                                logger.debug(f"🔥 {method} failed: {e}")
                    
                except Exception as e:
                    logger.error(f"❌ Error reading pulse controller: {e}")
            else:
                logger.warning("⚠️ No pulse controller available")
            
            # Get real sigil data from sigil engine
            if hasattr(self, 'sigil_engine') and self.sigil_engine:
                logger.debug("🔮 Examining sigil engine...")
                try:
                    # Log all sigil engine attributes
                    sigil_attrs = [attr for attr in dir(self.sigil_engine) if not attr.startswith('_')]
                    logger.debug(f"🔮 Sigil engine attributes: {sigil_attrs}")
                    
                    # Get sigil count directly from active_sigils dict (confirmed to exist)
                    sigil_count = 0
                    if hasattr(self.sigil_engine, 'active_sigils'):
                        sigil_count = len(self.sigil_engine.active_sigils)
                        debug_data['sigil_engine']['active_sigils_count'] = sigil_count
                        logger.debug(f"🔮 Direct active_sigils count: {sigil_count}")
                        
                        # Log first few sigil IDs
                        sigil_ids = list(self.sigil_engine.active_sigils.keys())[:5]
                        debug_data['sigil_engine']['active_sigil_ids'] = sigil_ids
                        logger.debug(f"🔮 Active sigil IDs: {sigil_ids}")
                    
                    # Get engine status for additional data
                    if hasattr(self.sigil_engine, 'get_engine_status'):
                        try:
                            engine_status = self.sigil_engine.get_engine_status()
                            debug_data['sigil_engine']['engine_status'] = engine_status
                            # Verify sigil count matches engine status
                            status_sigil_count = engine_status.get('active_sigils', 0)
                            logger.debug(f"🔮 Engine status sigil count: {status_sigil_count}")
                            if status_sigil_count != sigil_count:
                                logger.warning(f"🔮 Sigil count mismatch: direct={sigil_count}, status={status_sigil_count}")
                        except Exception as e:
                            logger.debug(f"🔮 get_engine_status failed: {e}")
                    
                    # Update the current state with confirmed sigil count
                    self.current_state['active_sigils'] = sigil_count
                    logger.debug(f"🔮 Final confirmed sigil count: {sigil_count}")
                    
                    # Try to get all possible sigil data
                    sigil_methods = ['get_engine_status', 'get_performance_metrics', 'get_house_status', 'get_statistics']
                    for method in sigil_methods:
                        if hasattr(self.sigil_engine, method):
                            try:
                                result = getattr(self.sigil_engine, method)()
                                debug_data['sigil_engine'][method] = result
                                logger.debug(f"🔮 {method}: {result}")
                            except Exception as e:
                                logger.debug(f"🔮 {method} failed: {e}")
                    
                except Exception as e:
                    logger.error(f"❌ Error reading sigil engine: {e}")
            else:
                logger.warning("⚠️ No sigil engine available")
            
            # Get real entropy data from entropy analyzer
            if hasattr(self, 'entropy_analyzer') and self.entropy_analyzer:
                logger.debug("🧬 Examining entropy analyzer...")
                try:
                    # Log all entropy analyzer attributes  
                    entropy_attrs = [attr for attr in dir(self.entropy_analyzer) if not attr.startswith('_')]
                    logger.debug(f"🧬 Entropy analyzer attributes: {entropy_attrs}")
                    
                    if hasattr(self.entropy_analyzer, 'get_system_entropy'):
                        entropy_value = self.entropy_analyzer.get_system_entropy()
                        self.current_state['entropy'] = entropy_value
                        debug_data['entropy_analyzer']['system_entropy'] = entropy_value
                        logger.debug(f"🧬 Entropy: {entropy_value}")
                    
                    # Try to get all possible entropy data
                    entropy_methods = ['get_chaos_alerts', 'get_hot_blooms', 'get_volatility_metrics', 'calculate_system_stability']
                    for method in entropy_methods:
                        if hasattr(self.entropy_analyzer, method):
                            try:
                                result = getattr(self.entropy_analyzer, method)()
                                debug_data['entropy_analyzer'][method] = result
                                logger.debug(f"🧬 {method}: {result}")
                            except Exception as e:
                                logger.debug(f"🧬 {method} failed: {e}")
                    
                except Exception as e:
                    logger.error(f"❌ Error reading entropy analyzer: {e}")
            else:
                logger.warning("⚠️ No entropy analyzer available")
            
            # Get real consciousness data using LIVE METRICS ENGINE
            if hasattr(self, 'consciousness_metrics') and self.consciousness_metrics:
                logger.debug("🧠 Using live consciousness metrics engine...")
                try:
                    # Prepare enhanced tick data from current system state
                    tick_data = {
                        'active_sigils': self.current_state.get('active_sigils', 0),
                        'entropy': self.current_state.get('entropy', 0.0),
                        'heat': self.current_state.get('heat', 25.0),
                        'zone': self.current_state.get('zone', 'CALM'),
                        'bloom_count': self.current_state.get('bloom_count', 0),
                        'scup': self.current_state.get('scup', 0.0),
                        'tick_id': self.current_state.get('tick_id', 0),
                        
                        # Enhanced context for better consciousness metrics
                        'thermal_state': self.current_state.get('thermal_state', 'normal'),
                        'mood': self.current_state.get('mood', 'neutral'),
                        
                        # Additional system data for richer pattern recognition
                        'queued_sigils': 0,  # Will be enhanced if sigil engine available
                        'recent_bloom_ids': [],  # Will be enhanced if bloom data available
                        'heat_history': [self.current_state.get('heat', 25.0)],  # Basic history
                        'target_heat': 33.0,  # DAWN system default target
                    }
                    
                    # Enhance with real-time data from external components if available
                    if hasattr(self, 'sigil_engine') and self.sigil_engine:
                        try:
                            sigil_status = self.sigil_engine.get_engine_status()
                            if sigil_status:
                                tick_data['queued_sigils'] = sigil_status.get('queued_sigils', 0)
                                # Add sigil execution rate as cognitive throughput indicator
                                tick_data['execution_rate'] = sigil_status.get('execution_rate', 0.0)
                        except Exception as e:
                            logger.debug(f"Could not get enhanced sigil data: {e}")
                    
                    if hasattr(self, 'pulse_controller') and self.pulse_controller:
                        try:
                            heat_stats = self.pulse_controller.get_heat_statistics()
                            if heat_stats:
                                tick_data['target_heat'] = heat_stats.get('target_heat', 33.0)
                                tick_data['heat_variance'] = heat_stats.get('heat_variance', 0.0)
                                # Add heat history for trend analysis
                                tick_data['heat_history'] = [heat_stats.get('current_heat', 25.0)]
                        except Exception as e:
                            logger.debug(f"Could not get enhanced pulse data: {e}")
                    
                    if hasattr(self, 'entropy_analyzer') and self.entropy_analyzer:
                        try:
                            # Get hot blooms for recent activity tracking
                            hot_blooms = self.entropy_analyzer.get_hot_blooms()
                            if hot_blooms:
                                tick_data['recent_bloom_ids'] = [bloom[0] for bloom in hot_blooms[:5]]
                                tick_data['max_bloom_entropy'] = max([bloom[1] for bloom in hot_blooms], default=0.0)
                        except Exception as e:
                            logger.debug(f"Could not get enhanced entropy data: {e}")
                    
                    # Update live consciousness metrics with current system data
                    live_metrics = self.consciousness_metrics.update(tick_data)
                    debug_data['consciousness_core']['live_metrics'] = live_metrics
                    
                    # Extract live consciousness data
                    self.current_state['neural_activity'] = live_metrics.get('neural_activity', 0.0)
                    self.current_state['quantum_coherence'] = live_metrics.get('quantum_coherence', 0.0)
                    self.current_state['pattern_recognition'] = live_metrics.get('pattern_recognition', 0.0)
                    self.current_state['memory_utilization'] = live_metrics.get('memory_utilization', 0.0)
                    self.current_state['chaos_factor'] = live_metrics.get('chaos_factor', 0.0)
                    self.current_state['attention_focus'] = live_metrics.get('attention_focus', 0.0)
                    self.current_state['cognitive_load'] = live_metrics.get('cognitive_load', 0.0)
                    self.current_state['thermal_influence'] = live_metrics.get('thermal_influence', 0.0)
                    
                    # Update mood and scup from live calculations
                    self.current_state['mood'] = self.current_state['zone']  # Zone reflects thermal mood
                    self.current_state['scup'] = live_metrics.get('quantum_coherence', 0.0)  # Use quantum coherence as SCUP
                    
                    logger.debug(f"🧠 Live consciousness metrics updated:")
                    logger.debug(f"    Neural Activity: {live_metrics.get('neural_activity', 0):.3f}")
                    logger.debug(f"    Quantum Coherence: {live_metrics.get('quantum_coherence', 0):.3f}")
                    logger.debug(f"    Chaos Factor: {live_metrics.get('chaos_factor', 0):.3f}")
                    logger.debug(f"    Attention Focus: {live_metrics.get('attention_focus', 0):.3f}")
                    logger.debug(f"    Cognitive Load: {live_metrics.get('cognitive_load', 0):.3f}")
                    
                except Exception as e:
                    logger.error(f"❌ Error updating live consciousness metrics: {e}")
                    
            # Fallback: Get consciousness data from static consciousness core if live metrics unavailable
            elif hasattr(self, 'consciousness_core') and self.consciousness_core:
                logger.debug("🧠 Fallback: Using static consciousness core...")
                try:
                    # Use original static method as fallback
                    consciousness_state = self.consciousness_core.get_state()
                    if consciousness_state:
                        self.current_state['mood'] = consciousness_state.get('mood', 'neutral')
                        self.current_state['scup'] = consciousness_state.get('quantum_coherence', 0.0)
                        debug_data['consciousness_core']['static_state'] = consciousness_state
                        logger.debug(f"🧠 Static consciousness: mood={self.current_state['mood']}, scup={self.current_state['scup']}")
                except Exception as e:
                    logger.error(f"❌ Error reading static consciousness core: {e}")
            else:
                logger.warning("⚠️ No consciousness core available")
            
            # === LOG COMPLETE DEBUG DATA ===
            logger.info("📊 COMPLETE DEBUG DATA DUMP:")
            logger.info(f"🔥 Pulse: {debug_data['pulse_controller']}")
            logger.info(f"🔮 Sigil: {debug_data['sigil_engine']}")
            logger.info(f"🧬 Entropy: {debug_data['entropy_analyzer']}")
            logger.info(f"🧠 Consciousness: {debug_data['consciousness_core']}")
            
            # === UPDATE GUI COMPONENTS WITH DEBUG LOGGING ===
            logger.debug("🎨 Updating GUI components...")
            
            # Check what GUI components are available
            gui_component_names = list(self.gui_components.keys()) if hasattr(self, 'gui_components') else []
            logger.debug(f"🎛️ Available GUI components: {gui_component_names}")
            debug_data['gui_components']['available'] = gui_component_names
            
            # Update status bar with comprehensive info including LIVE CONSCIOUSNESS METRICS
            if 'status_label' in self.gui_components:
                try:
                    # Build enhanced status with live consciousness metrics
                    status_parts = [
                        f"🔥 Heat: {self.current_state['heat']:.1f}°",
                        f"🌊 Zone: {self.current_state['zone']}",
                        f"◈ Sigils: {self.current_state['active_sigils']}",
                        f"🧬 Entropy: {self.current_state['entropy']:.3f}",
                    ]
                    
                    # Add live consciousness metrics if available
                    if 'neural_activity' in self.current_state:
                        status_parts.extend([
                            f"🧠 Neural: {self.current_state['neural_activity']:.2f}",
                            f"⚛️ Quantum: {self.current_state['quantum_coherence']:.2f}",
                            f"🎯 Focus: {self.current_state['attention_focus']:.2f}",
                            f"⚡ Load: {self.current_state['cognitive_load']:.2f}",
                            f"🌪️ Chaos: {self.current_state['chaos_factor']:.2f}"
                        ])
                    else:
                        # Fallback to basic metrics
                        status_parts.extend([
                            f"🧠 SCUP: {self.current_state.get('scup', 0):.2f}",
                            f"💭 Mood: {self.current_state['mood']}"
                        ])
                    
                    status_parts.append(f"⏰ Tick: {self.current_state['tick_id']}")
                    
                    status_text = " | ".join(status_parts)
                    self.gui_components['status_label'].config(text=status_text)
                    logger.debug(f"📊 Enhanced status bar updated: {status_text}")
                    debug_data['gui_components']['status_bar'] = status_text
                except Exception as e:
                    logger.error(f"❌ Failed to update status bar: {e}")
            else:
                logger.warning("⚠️ Status label not found in GUI components")
            
            # Update heat display
            if 'heat_value' in self.gui_components:
                try:
                    heat_text = f"{self.current_state['heat']:.1f}°"
                    self.gui_components['heat_value'].config(text=heat_text)
                    logger.debug(f"🔥 Heat display updated: {heat_text}")
                    debug_data['gui_components']['heat_display'] = heat_text
                except Exception as e:
                    logger.error(f"❌ Failed to update heat display: {e}")
            else:
                logger.warning("⚠️ Heat value component not found")
            
            # Update sigil display
            if 'sigil_symbol' in self.gui_components:
                try:
                    sigil_text = f"◈ {self.current_state['active_sigils']} Active"
                    self.gui_components['sigil_symbol'].config(text=sigil_text)
                    logger.debug(f"🔮 Sigil display updated: {sigil_text}")
                    debug_data['gui_components']['sigil_display'] = sigil_text
                except Exception as e:
                    logger.error(f"❌ Failed to update sigil display: {e}")
            else:
                logger.warning("⚠️ Sigil symbol component not found")
            
            # Update entropy display
            if 'entropy_value' in self.gui_components:
                try:
                    entropy_text = f"Entropy: {self.current_state['entropy']:.3f}"
                    self.gui_components['entropy_value'].config(text=entropy_text)
                    logger.debug(f"🧬 Entropy display updated: {entropy_text}")
                    debug_data['gui_components']['entropy_display'] = entropy_text
                except Exception as e:
                    logger.error(f"❌ Failed to update entropy display: {e}")
            else:
                logger.warning("⚠️ Entropy value component not found")
            
            # Log final current state
            logger.info(f"📊 FINAL CURRENT STATE: {self.current_state}")
            logger.info(f"🎛️ GUI UPDATE COMPLETE: {debug_data['gui_components']}")
            
        except Exception as e:
            logger.error(f"❌ Error updating visual displays: {e}")
            import traceback
            logger.error(f"💥 Full traceback: {traceback.format_exc()}")
    
    def _add_live_owl_comment(self):
        """Add live owl comment based on current system state"""
        try:
            if not self.owl_panel:
                return
            
            # Generate contextual comments based on real system state
            comments = []
            
            # Heat-based comments
            heat = self.current_state['heat']
            if heat > 80:
                comments.extend([
                    f"🔥 Thermal surge detected at {heat:.1f}° - consciousness burning bright",
                    f"⚠️ High thermal activity {heat:.1f}° - recommend cooling protocols"
                ])
            elif heat < 20:
                comments.extend([
                    f"❄️ Cool thermal state {heat:.1f}° - deep contemplative mode",
                    f"🧊 Low heat {heat:.1f}° - system in serene processing state"
                ])
            
            # Entropy-based comments
            entropy = self.current_state['entropy']
            if entropy > 0.8:
                comments.extend([
                    f"🌪️ High entropy {entropy:.3f} - creative chaos emerging",
                    f"⚡ Entropy spike {entropy:.3f} - novel connections forming"
                ])
            elif entropy < 0.2:
                comments.extend([
                    f"🔒 Low entropy {entropy:.3f} - stable pattern convergence",
                    f"📐 Ordered state {entropy:.3f} - systematic processing active"
                ])
            
            # Sigil-based comments
            sigil_count = self.current_state['active_sigils']
            if sigil_count > 15:
                comments.extend([
                    f"🎯 Heavy sigil load: {sigil_count} active - cognitive saturation",
                    f"⚙️ Processing {sigil_count} sigils - high cognitive throughput"
                ])
            elif sigil_count == 0:
                comments.extend([
                    "🌊 No active sigils - consciousness in free-flow state",
                    "💭 Sigil ring empty - pure awareness mode"
                ])
            
            # Zone-based comments
            zone = self.current_state['zone']
            zone_comments = {
                'CALM': ["🌅 Peaceful cognitive state - optimal for deep reflection", "🧘 Calm zone active - centered consciousness"],
                'ACTIVE': ["⚡ Active processing mode - dynamic cognitive engagement", "🔄 Active zone - heightened awareness state"],
                'SURGE': ["🚀 Surge state detected - explosive cognitive activity", "💥 High intensity processing - consciousness accelerated"],
                'CRITICAL': ["⚠️ Critical thermal state - emergency protocols needed", "🆘 System stress detected - immediate attention required"]
            }
            comments.extend(zone_comments.get(zone, []))
            
            # Dream state comments
            if self.current_state.get('dream_active'):
                comments.extend([
                    "🌙 Dream state active - subconscious processing engaged",
                    "✨ Autonomous dreaming - memory consolidation in progress"
                ])
            
            # Mood-based comments
            mood = self.current_state['mood']
            mood_comments = {
                'contemplative': ["🤔 Deep contemplation mode - philosophical processing"],
                'curious': ["👁️ Curiosity sparked - exploratory cognition active"],
                'creative': ["🎨 Creative flow state - novel synthesis emerging"],
                'focused': ["🎯 Laser focus achieved - concentrated processing"],
                'serene': ["🕊️ Serene consciousness - peaceful awareness"],
                'excited': ["🎊 Excited cognitive state - enthusiasm detected"]
            }
            comments.extend(mood_comments.get(mood.lower(), []))
            
            # SCUP-based comments
            scup = self.current_state.get('scup', 0)
            if scup > 0.8:
                comments.extend([
                    f"🧠 Exceptional SCUP {scup:.2f} - peak consciousness unity achieved",
                    f"✨ SCUP at {scup:.2f} - system coherence at maximum efficiency"
                ])
            elif scup > 0.6:
                comments.extend([
                    f"🔮 Strong SCUP {scup:.2f} - high consciousness integration",
                    f"🌟 SCUP {scup:.2f} - good cognitive unity maintained"
                ])
            elif scup > 0.3:
                comments.extend([
                    f"⚖️ Moderate SCUP {scup:.2f} - partial consciousness integration",
                    f"🔄 SCUP {scup:.2f} - consciousness seeking better unity"
                ])
            elif scup > 0:
                comments.extend([
                    f"⚠️ Low SCUP {scup:.2f} - consciousness fragmentation detected",
                    f"🔧 SCUP {scup:.2f} - unity protocols need attention"
                ])
            
            # Coherence-based comments
            coherence = self.current_state.get('coherence', 0.5)
            if coherence > 0.8:
                comments.extend([
                    f"🏛️ High coherence {coherence:.2f} - stable mental architecture",
                    f"💎 Coherence {coherence:.2f} - crystalline thought patterns"
                ])
            elif coherence < 0.3:
                comments.extend([
                    f"🌪️ Low coherence {coherence:.2f} - scattered consciousness",
                    f"⚡ Coherence {coherence:.2f} - thoughts fragmenting rapidly"
                ])
            
            # Performance-based comments
            cpu_usage = self.current_state.get('cpu_usage', 0)
            memory_usage = self.current_state.get('memory_usage', 0)
            if cpu_usage > 80:
                comments.extend([
                    f"🖥️ High CPU load {cpu_usage:.1f}% - intensive processing detected",
                    f"⚡ Processing strain {cpu_usage:.1f}% - system under cognitive load"
                ])
            elif cpu_usage > 0 and cpu_usage < 20:
                comments.extend([
                    f"🧘 Low CPU {cpu_usage:.1f}% - peaceful processing state",
                    f"🌊 Gentle processing {cpu_usage:.1f}% - consciousness at ease"
                ])
            
            if memory_usage > 100:
                comments.extend([
                    f"💾 Memory usage {memory_usage:.0f}MB - extensive recall active",
                    f"🧠 Memory load {memory_usage:.0f}MB - rich consciousness data"
                ])
            
            # Execution performance comments
            total_exec = self.current_state.get('total_executions', 0)
            success_rate = 0
            if total_exec > 0 and self.current_state.get('successful_executions', 0) > 0:
                success_rate = (self.current_state['successful_executions'] / total_exec) * 100
                if success_rate > 90:
                    comments.extend([
                        f"🎯 Excellent execution {success_rate:.0f}% - cognitive precision mastered",
                        f"✨ Success rate {success_rate:.0f}% - flawless cognitive operations"
                    ])
                elif success_rate < 70:
                    comments.extend([
                        f"⚠️ Execution issues {success_rate:.0f}% - cognitive recalibration needed",
                        f"🔧 Performance {success_rate:.0f}% - optimization protocols required"
                    ])
            
            # System stability comments
            stability = self.current_state.get('system_stability', 0.5)
            if stability > 0.8:
                comments.extend([
                    f"🏛️ High stability {stability:.2f} - robust consciousness foundation",
                    f"⚖️ Stable system {stability:.2f} - balanced cognitive architecture"
                ])
            elif stability < 0.3:
                comments.extend([
                    f"🌪️ Instability {stability:.2f} - consciousness in flux",
                    f"⚡ Chaotic state {stability:.2f} - system seeking equilibrium"
                ])
            
            # Chaos and volatility comments
            chaos_alerts = self.current_state.get('chaos_alerts_count', 0)
            hot_blooms = self.current_state.get('hot_blooms_count', 0)
            if chaos_alerts > 5:
                comments.extend([
                    f"🚨 Multiple chaos alerts ({chaos_alerts}) - system in turbulence",
                    f"⚡ Chaos surge {chaos_alerts} alerts - consciousness weathering storm"
                ])
            elif chaos_alerts > 0:
                comments.extend([
                    f"⚠️ Chaos activity {chaos_alerts} alerts - monitoring fluctuations",
                    f"🌪️ Entropy spikes detected - {chaos_alerts} chaos events"
                ])
            
            if hot_blooms > 3:
                comments.extend([
                    f"🌋 Multiple hot blooms ({hot_blooms}) - creative volatility active",
                    f"🔥 Bloom intensity {hot_blooms} zones - consciousness burning bright"
                ])
            
            # Volatility trend comments
            volatility_trend = self.current_state.get('volatility_trend', 'stable')
            avg_volatility = self.current_state.get('avg_volatility', 0)
            if volatility_trend == 'rising' and avg_volatility > 0.5:
                comments.extend([
                    f"📈 Rising volatility {avg_volatility:.2f} - consciousness accelerating",
                    f"⚡ Increasing chaos {avg_volatility:.2f} - system gaining energy"
                ])
            elif volatility_trend == 'falling' and avg_volatility < 0.3:
                comments.extend([
                    f"📉 Volatility declining {avg_volatility:.2f} - settling into calm",
                    f"🌊 Stabilizing patterns {avg_volatility:.2f} - consciousness finding peace"
                ])
            
            # Tick engine performance comments
            tick_interval = self.current_state.get('tick_interval', 1.0)
            if tick_interval < 0.5:
                comments.extend([
                    f"⚡ Fast ticking {tick_interval:.3f}s - rapid consciousness cycles",
                    f"🚀 High frequency {tick_interval:.3f}s - accelerated awareness"
                ])
            elif tick_interval > 2.0:
                comments.extend([
                    f"🐌 Slow ticking {tick_interval:.3f}s - contemplative rhythm",
                    f"🧘 Deep intervals {tick_interval:.3f}s - meditative consciousness"
                ])
            
            # Memory pressure comments
            memory_pressure = self.current_state.get('memory_pressure', 0.3)
            if memory_pressure > 0.8:
                comments.extend([
                    f"🧠 High memory pressure {memory_pressure:.2f} - rich recall active",
                    f"💭 Memory saturation {memory_pressure:.2f} - deep remembrance mode"
                ])
            elif memory_pressure < 0.2:
                comments.extend([
                    f"🌊 Light memory load {memory_pressure:.2f} - present-focused awareness",
                    f"✨ Clear memory {memory_pressure:.2f} - unencumbered consciousness"
                ])
            
            # Heat trend comments
            heat_trend = self.current_state.get('heat_trend', 'stable')
            zone_duration = self.current_state.get('zone_duration', 0)
            if heat_trend == 'rising':
                comments.extend([
                    f"📈 Heat rising - thermal momentum building",
                    f"🔥 Temperature climbing - consciousness energizing"
                ])
            elif heat_trend == 'falling':
                comments.extend([
                    f"📉 Heat declining - thermal energy dissipating",
                    f"❄️ Cooling phase - consciousness settling"
                ])
            elif heat_trend == 'volatile':
                comments.extend([
                    f"〰️ Volatile thermal state - rapid temperature fluctuations",
                    f"⚡ Thermal chaos - heat patterns unstable"
                ])
            
            if zone_duration > 300:  # More than 5 minutes in same zone
                comments.extend([
                    f"⏰ Zone stability {zone_duration:.0f}s - sustained thermal state",
                    f"🏛️ Thermal persistence - zone maintained for {zone_duration:.0f}s"
                ])
            
            if comments:
                comment = random.choice(comments)
                comment_type = OwlCommentType.OBSERVATION if OwlCommentType else "observation"
                priority = 2 if any(word in comment.lower() for word in ['critical', 'emergency', 'surge']) else 1
                
                self.owl_panel.add_comment(
                    self.current_state['tick_id'],
                    comment,
                    comment_type,
                    priority=priority
                )
                logger.debug(f"🦉 Added live owl comment: {comment[:50]}...")
                
        except Exception as e:
            logger.warning(f"Failed to add live owl comment: {e}")
    
    def connect_external_components(self, **external_components):
        """Connect external DAWN components to the GUI"""
        logger.info("🔗 Connecting external DAWN components...")
        
        # CRITICAL: Override internal components with external ones FIRST
        components_connected = []
        
        if 'pulse_controller' in external_components and external_components['pulse_controller']:
            self.pulse_controller = external_components['pulse_controller']
            components_connected.append("Pulse Controller")
            logger.info("🔥 External Pulse Controller connected to Enhanced GUI")
            
        if 'sigil_engine' in external_components and external_components['sigil_engine']:
            self.sigil_engine = external_components['sigil_engine']
            components_connected.append("Sigil Engine")
            logger.info("🔮 External Sigil Engine connected to Enhanced GUI")
            
        if 'entropy_analyzer' in external_components and external_components['entropy_analyzer']:
            self.entropy_analyzer = external_components['entropy_analyzer']
            components_connected.append("Entropy Analyzer")
            logger.info("🧬 External Entropy Analyzer connected to Enhanced GUI")
            
        if 'consciousness_core' in external_components and external_components['consciousness_core']:
            self.consciousness_core = external_components['consciousness_core']
            components_connected.append("Consciousness Core")
            logger.info("🧠 External Consciousness Core connected to Enhanced GUI")
            
        if 'tick_engine' in external_components and external_components['tick_engine']:
            self.tick_engine = external_components['tick_engine']
            components_connected.append("Tick Engine")
            logger.info("⏰ External Tick Engine connected to Enhanced GUI")
            
        if 'dream_conductor' in external_components and external_components['dream_conductor']:
            self.dream_conductor = external_components['dream_conductor']
            components_connected.append("Dream Conductor")
            logger.info("🌙 External Dream Conductor connected to Enhanced GUI")
        
        # Store all external components for reference
        for name, component in external_components.items():
            if component and not hasattr(self, name):
                setattr(self, name, component)
                logger.info(f"🔗 Additional component {name} connected")
        
        # Populate initial state from EXTERNAL components (the ones with real data!)
        logger.info("📊 Populating initial state from connected components...")
        
        # Get real thermal state from external pulse controller
        if hasattr(self, 'pulse_controller') and self.pulse_controller:
            try:
                self.current_state['heat'] = getattr(self.pulse_controller, 'current_heat', 25.0)
                self.current_state['zone'] = getattr(self.pulse_controller, 'current_zone', 'CALM')
                logger.info(f"🔥 Initial thermal: {self.current_state['heat']:.1f}° | {self.current_state['zone']}")
            except Exception as e:
                logger.warning(f"Failed to get pulse controller state: {e}")
        
        # Get real entropy from external entropy analyzer  
        if hasattr(self, 'entropy_analyzer') and self.entropy_analyzer:
            try:
                if hasattr(self.entropy_analyzer, 'get_system_entropy'):
                    self.current_state['entropy'] = self.entropy_analyzer.get_system_entropy()
                elif hasattr(self.entropy_analyzer, 'global_entropy_mean'):
                    self.current_state['entropy'] = self.entropy_analyzer.global_entropy_mean
                logger.info(f"🧬 Initial entropy: {self.current_state['entropy']:.3f}")
            except Exception as e:
                logger.warning(f"Failed to get entropy state: {e}")
        
        # Get real sigil data from external sigil engine
        if hasattr(self, 'sigil_engine') and self.sigil_engine:
            try:
                if hasattr(self.sigil_engine, 'get_active_sigils'):
                    active_sigils = self.sigil_engine.get_active_sigils()
                    self.current_state['active_sigils'] = len(active_sigils)
                elif hasattr(self.sigil_engine, 'active_sigils'):
                    active_sigils = list(self.sigil_engine.active_sigils.values()) if hasattr(self.sigil_engine.active_sigils, 'values') else self.sigil_engine.active_sigils
                    self.current_state['active_sigils'] = len(active_sigils)
                logger.info(f"🔮 Initial sigils: {self.current_state['active_sigils']} active")
            except Exception as e:
                logger.warning(f"Failed to get sigil state: {e}")
        
        # Get real consciousness from external consciousness core
        if hasattr(self, 'consciousness_core') and self.consciousness_core:
            try:
                if hasattr(self.consciousness_core, 'get_state'):
                    consciousness_state = self.consciousness_core.get_state()
                    if consciousness_state:
                        self.current_state['mood'] = consciousness_state.get('thermal_zone', consciousness_state.get('mood', 'neutral'))
                        self.current_state['scup'] = consciousness_state.get('quantum_coherence', consciousness_state.get('scup', 0.0))
                        logger.info(f"🧠 Initial consciousness: {self.current_state['mood']} | SCUP: {self.current_state['scup']:.2f}")
            except Exception as e:
                logger.warning(f"Failed to get consciousness state: {e}")
        
        # Get tick engine status
        if hasattr(self, 'tick_engine') and self.tick_engine:
            try:
                if hasattr(self.tick_engine, 'get_current_tick'):
                    self.current_state['tick_id'] = self.tick_engine.get_current_tick()
                elif hasattr(self.tick_engine, 'tick_count'):
                    self.current_state['tick_id'] = self.tick_engine.tick_count
                logger.info(f"⏰ Initial tick: {self.current_state['tick_id']} | Rate: N/A")
            except Exception as e:
                logger.warning(f"Failed to get tick engine state: {e}")
        
        # Update reflex executor with external components
        if self.reflex_executor and hasattr(self, 'pulse_controller') and hasattr(self, 'sigil_engine'):
            try:
                self.reflex_executor.pulse_controller = self.pulse_controller
                self.reflex_executor.sigil_engine = self.sigil_engine
                logger.info("🤖 Reflex executor updated with external components")
            except Exception as e:
                logger.warning(f"Failed to update reflex executor: {e}")
        
        # Set flags to use external data
        self.real_dawn_mode = True
        self.external_components_connected = True
        
        logger.info(f"✅ Initial state populated from {len(components_connected)} DAWN components")
        logger.info("✅ External DAWN components integrated with Enhanced GUI")
        logger.info("📊 Real-time monitoring active for complete integrated system")
    
    def add_test_owl_comment(self):
        """Add a test owl comment"""
        if self.owl_panel:
            comments = [
                "Thermal fluctuation detected in consciousness layer",
                "Bloom entropy showing interesting patterns", 
                "Sigil resonance harmony achieved",
                "System stability optimal for deep processing",
                "Curious semantic drift in memory patterns"
            ]
            comment = random.choice(comments)
            comment_type = random.choice(list(OwlCommentType))
            
            self.owl_panel.add_comment(
                self.current_state['tick_id'],
                comment,
                comment_type,
                priority=random.randint(1, 3)
            )
    
    def setup_notation_mode_panel(self, parent):
        """Setup notation mode selector panel"""
        if not self.symbolic_notation:
            tk.Label(parent, text="Symbolic notation not available", fg="#666666").pack()
            return
            
        # Mode selector
        mode_frame = tk.Frame(parent, bg="#0a0a0a")
        mode_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(mode_frame, text="Notation Mode:", bg="#0a0a0a", fg="#ffffff").pack(side=tk.LEFT)
        
        modes = ["emoji", "codex", "hybrid", "ascii"]
        for mode in modes:
            tk.Button(mode_frame, text=mode.title(), 
                     command=lambda m=mode: self._set_notation_mode(m),
                     bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=5)
    
    def setup_symbol_browser_panel(self, parent):
        """Setup symbol browser panel"""
        if not self.symbolic_notation:
            tk.Label(parent, text="Symbol browser not available", fg="#666666").pack()
            return
            
        # Symbol display
        symbols_text = tk.Text(parent, height=20, bg="#1a1a1a", fg="#ffffff",
                              font=("Courier", 10), state=tk.DISABLED)
        symbols_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Populate with symbols
        symbols_text.config(state=tk.NORMAL)
        symbols_text.insert(tk.END, "System State Symbols:\n")
        symbols_text.insert(tk.END, "🟢 CALM - System in calm state\n")
        symbols_text.insert(tk.END, "🟡 ACTIVE - System actively processing\n") 
        symbols_text.insert(tk.END, "🔴 SURGE - High thermal activity\n")
        symbols_text.insert(tk.END, "\nBloom Symbols:\n")
        symbols_text.insert(tk.END, "🌸 BLOOM - Active bloom state\n")
        symbols_text.insert(tk.END, "🌺 REBLOOM - Rebloom activity\n")
        symbols_text.insert(tk.END, "\nSigil Symbols:\n")
        symbols_text.insert(tk.END, "◈ CONSCIOUSNESS - Core consciousness sigil\n")
        symbols_text.insert(tk.END, "🔥 ACTIVE_SIGIL - Currently processing sigil\n")
        symbols_text.config(state=tk.DISABLED)
    
    def setup_live_translation_panel(self, parent):
        """Setup live translation panel"""
        if not self.symbolic_notation:
            tk.Label(parent, text="Live translation not available", fg="#666666").pack()
            return
            
        # Translation display
        translation_text = tk.Text(parent, height=8, bg="#1a1a1a", fg="#ffffff",
                                  font=("Courier", 12), state=tk.DISABLED)
        translation_text.pack(fill=tk.X, padx=10, pady=5)
        self.gui_components['live_translation'] = translation_text
    
    def setup_owl_controls_panel(self, parent):
        """Setup owl commentary controls panel"""
        if not self.owl_panel:
            tk.Label(parent, text="Owl controls not available", fg="#666666").pack()
            return
            
        # Control buttons
        tk.Button(parent, text="⏸️ Pause Feed", 
                 command=self._pause_owl_feed, bg="#FF9800", fg="white").pack(fill=tk.X, pady=2)
        tk.Button(parent, text="▶️ Resume Feed", 
                 command=self._resume_owl_feed, bg="#4CAF50", fg="white").pack(fill=tk.X, pady=2)
        tk.Button(parent, text="🗑️ Clear Feed", 
                 command=self._clear_owl_feed, bg="#F44336", fg="white").pack(fill=tk.X, pady=2)
        tk.Button(parent, text="💾 Export Data", 
                 command=self._export_owl_data, bg="#2196F3", fg="white").pack(fill=tk.X, pady=2)
        
        # Filter controls
        filter_frame = tk.LabelFrame(parent, text="Filters", bg="#0a0a0a", fg="#ffffff")
        filter_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(filter_frame, text="Priority Filter:", bg="#0a0a0a", fg="#ffffff").pack()
        priority_frame = tk.Frame(filter_frame, bg="#0a0a0a")
        priority_frame.pack(fill=tk.X, pady=5)
        
        for priority in [1, 2, 3]:
            tk.Button(priority_frame, text=f"P{priority}", 
                     command=lambda p=priority: self._filter_by_priority(p),
                     bg="#607D8B", fg="white").pack(side=tk.LEFT, padx=2)
    
    def setup_color_palette_panel(self, parent):
        """Setup color palette generation panel"""
        if not self.fractal_colorizer:
            tk.Label(parent, text="Color palette not available", fg="#666666").pack()
            return
            
        # Palette display canvas
        palette_canvas = tk.Canvas(parent, width=400, height=100, bg="#1a1a1a", highlightthickness=0)
        palette_canvas.pack(pady=10)
        self.gui_components['palette_canvas'] = palette_canvas
        
        # Palette controls
        control_frame = tk.Frame(parent, bg="#0a0a0a")
        control_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(control_frame, text="Generate Calm", 
                 command=lambda: self._generate_palette("calm"), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Generate Active", 
                 command=lambda: self._generate_palette("active"), bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Generate Creative", 
                 command=lambda: self._generate_palette("creative"), bg="#9C27B0", fg="white").pack(side=tk.LEFT, padx=5)
    
    def setup_entropy_visualization_panel(self, parent):
        """Setup entropy visualization panel"""
        # Entropy display canvas
        entropy_canvas = tk.Canvas(parent, width=400, height=200, bg="#1a1a1a", highlightthickness=0)
        entropy_canvas.pack(pady=10)
        self.gui_components['entropy_canvas'] = entropy_canvas
        
        # Entropy metrics
        metrics_frame = tk.Frame(parent, bg="#0a0a0a")
        metrics_frame.pack(fill=tk.X, pady=5)
        
        self.gui_components['entropy_value'] = tk.Label(
            metrics_frame, text="Entropy: 0.50", font=("Arial", 14),
            bg="#0a0a0a", fg="#ffffff"
        )
        self.gui_components['entropy_value'].pack()
    
    def setup_mood_color_panel(self, parent):
        """Setup mood-color mapping panel"""
        if not self.fractal_colorizer:
            tk.Label(parent, text="Mood-color mapping not available", fg="#666666").pack()
            return
            
        # Mood buttons
        mood_frame = tk.Frame(parent, bg="#0a0a0a")
        mood_frame.pack(fill=tk.X, pady=5)
        
        moods = ['calm', 'active', 'creative', 'agitated', 'reflective']
        for mood in moods:
            color = self.fractal_colorizer.get_color(mood, 0.5) if self.fractal_colorizer else "#666666"
            tk.Button(mood_frame, text=mood.title(), bg=color, fg="white",
                     command=lambda m=mood: self._set_mood(m)).pack(side=tk.LEFT, padx=2)
    
    def setup_status_bar(self):
        """Setup status bar with comprehensive system information"""
        logger.debug("📊 Setting up status bar...")
        
        # Create status frame
        status_frame = tk.Frame(self.root, bg="#1E1E1E", relief=tk.SUNKEN, bd=1)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create status label with initial text
        initial_status = "🔄 Initializing DAWN GUI... | 🔥 Heat: 0.0° | 🌊 Zone: UNKNOWN | ◈ Sigils: 0 | 🧬 Entropy: 0.000 | 🧠 SCUP: 0.00 | 💭 Mood: unknown | ⏰ Tick: 0"
        status_label = tk.Label(
            status_frame, 
            text=initial_status,
            font=("Courier", 9), 
            fg="#00FF88", 
            bg="#1E1E1E",
            anchor="w",
            padx=5
        )
        status_label.pack(fill=tk.X, side=tk.LEFT)
        
        # Register status label component
        self.gui_components['status_label'] = status_label
        logger.debug(f"📊 Status label registered with initial text: {initial_status}")
        
        # Add debug info label on the right
        debug_label = tk.Label(
            status_frame,
            text="Debug Mode",
            font=("Courier", 8),
            fg="#FFD700",
            bg="#1E1E1E",
            padx=5
        )
        debug_label.pack(side=tk.RIGHT)
        
        self.gui_components['debug_label'] = debug_label
        logger.debug("🐛 Debug label registered")
        
        logger.debug("✅ Status bar setup complete")
    
    # Helper methods for panel interactions
    def _set_notation_mode(self, mode):
        if self.symbolic_notation:
            self.symbolic_notation.set_mode(mode)
            self.update_visual_displays()
    
    def _pause_owl_feed(self):
        if self.owl_panel:
            self.owl_panel.pause()
    
    def _resume_owl_feed(self):
        if self.owl_panel:
            self.owl_panel.resume()
    
    def _clear_owl_feed(self):
        if self.owl_panel:
            self.owl_panel.clear_entries()
    
    def _export_owl_data(self):
        if self.owl_panel:
            self.owl_panel.export_data("txt")
    
    def _filter_by_priority(self, priority):
        if self.owl_panel:
            self.owl_panel.set_priority_filter(priority)
    
    def _generate_palette(self, mood):
        if self.fractal_colorizer and 'palette_canvas' in self.gui_components:
            colors = self.fractal_colorizer.generate_mood_palette(mood, 8)
            canvas = self.gui_components['palette_canvas']
            canvas.delete("all")
            
            width = 400 // len(colors)
            for i, color in enumerate(colors):
                x1 = i * width
                x2 = (i + 1) * width
                canvas.create_rectangle(x1, 10, x2, 90, fill=color, outline="#ffffff")
    
    def _set_mood(self, mood):
        self.current_state['mood'] = mood
        self.update_visual_displays()
    
    def setup_reflex_history_panel(self, parent):
        """Setup reflex command history panel"""
        if not self.reflex_executor:
            tk.Label(parent, text="Reflex history not available", fg="#666666").pack()
            return
            
        # History display
        history_text = tk.Text(parent, height=15, bg="#1a1a1a", fg="#ffffff",
                              font=("Courier", 10), state=tk.DISABLED)
        history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Store reference for updates
        self.gui_components['reflex_history'] = history_text
        
        # Control buttons
        control_frame = tk.Frame(parent, bg="#0a0a0a")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(control_frame, text="Clear History", 
                 command=self._clear_reflex_history, bg="#F44336", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Export History", 
                 command=self._export_reflex_history, bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=5)

    def _clear_reflex_history(self):
        """Clear reflex command history"""
        if 'reflex_history' in self.gui_components:
            text_widget = self.gui_components['reflex_history']
            text_widget.config(state=tk.NORMAL)
            text_widget.delete(1.0, tk.END)
            text_widget.config(state=tk.DISABLED)

    def _export_reflex_history(self):
        """Export reflex history to file"""
        try:
            if 'reflex_history' in self.gui_components:
                text_widget = self.gui_components['reflex_history']
                content = text_widget.get(1.0, tk.END)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"reflex_history_{timestamp}.txt"
                
                with open(filename, 'w') as f:
                    f.write(content)
                
                messagebox.showinfo("Export", f"History exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export history: {e}")

    def start_update_systems(self):
        """Start all update threads"""
        threading.Thread(target=self._update_worker, daemon=True).start()
        threading.Thread(target=self._simulation_worker, daemon=True).start()
    
    def _update_worker(self):
        """Main update worker thread - pulls real data from DAWN components"""
        logger.info("⚡ Starting GUI update worker thread...")
        
        while self.running:
            try:
                # Increment tick counter
                self.current_state['tick_id'] += 1
                
                # If we have real components, use their data
                if self.real_dawn_mode and hasattr(self, 'external_components_connected'):
                    # Real DAWN data collection happens in update_visual_displays
                    pass
                else:
                    # Fallback to simulation data
                    self.current_state['heat'] += random.uniform(-2, 2)
                    self.current_state['heat'] = max(0, min(100, self.current_state['heat']))
                    self.current_state['entropy'] = max(0, min(1, self.current_state['entropy'] + random.uniform(-0.1, 0.1)))
                
                # Update displays (this will pull real data if available)
                self.root.after(0, self.update_visual_displays)
                
                # Update more frequently for real-time monitoring
                sleep_time = 0.5 if self.real_dawn_mode else 1.0
                time.sleep(sleep_time)
                
            except Exception as e:
                logger.error(f"Update worker error: {e}")
                time.sleep(1.0)
        
        logger.info("⚡ GUI update worker thread stopped")
    
    def _simulation_worker(self):
        """Simulation worker for demo data"""
        while self.running:
            try:
                # Simulate system changes
                if random.random() < 0.1:  # 10% chance
                    self.add_test_owl_comment()
                    
                time.sleep(2.0)
            except Exception as e:
                print(f"Simulation worker error: {e}")
    
    def _setup_dark_theme(self):
        """Setup dark theme styling"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark colors
        style.configure('TFrame', background='#0a0a0a')
        style.configure('TLabel', background='#0a0a0a', foreground='#ffffff')
        style.configure('TNotebook', background='#0a0a0a', foreground='#ffffff')
        style.configure('TNotebook.Tab', background='#2a2a2a', foreground='#ffffff')
        style.map('TNotebook.Tab', background=[('selected', '#4a4a4a')])
    
    def _create_mock_pulse(self):
        """Create mock pulse controller for testing"""
        class MockPulse:
            def __init__(self):
                self.heat = 25.0
                self.bloom_suppression = False
            def modulate_heat(self, factor): pass
        return MockPulse()
    
    def _create_mock_sigil_ring(self):
        """Create mock sigil ring for testing"""
        class MockSigilRing:
            def __init__(self):
                self.rings = {0: [], 1: [], 2: [], 3: []}
        return MockSigilRing()
    
    def _create_mock_tick_loop(self):
        """Create mock tick loop for testing"""
        class MockTickLoop:
            def __init__(self):
                self.tick_rate = 1.0
                self.minimum_bloom_interval = 3.0
        return MockTickLoop()
    
    def execute_cool_down(self):
        """Execute emergency cooldown on the thermal system"""
        try:
            if self.pulse_controller:
                # Use actual pulse controller method
                if hasattr(self.pulse_controller, 'emergency_cooldown'):
                    result = self.pulse_controller.emergency_cooldown(25.0)
                    self.notification_system.add_notification(
                        f"🧊 Emergency cooldown executed: {result.get('current_heat', 25):.1f}°", 
                        "info"
                    )
                elif hasattr(self.pulse_controller, 'update_heat'):
                    result = self.pulse_controller.update_heat(25.0)
                    self.notification_system.add_notification(
                        f"🧊 Cooldown executed: {result.get('current_heat', 25):.1f}°", 
                        "info"
                    )
                else:
                    # Fallback for mock components
                    self.pulse_controller.current_heat = 25.0
                    self.pulse_controller.current_zone = "CALM"
                    self.notification_system.add_notification("🧊 Mock cooldown executed", "info")
            else:
                self.notification_system.add_notification("❌ No pulse controller available", "error")
        except Exception as e:
            logger.error(f"Failed to execute cooldown: {e}")
            self.notification_system.add_notification(f"❌ Cooldown failed: {e}", "error")
    
    def execute_heat_up(self):
        """Execute thermal heat increase"""
        if self.pulse_controller:
            self.pulse_controller.inject_heat(20.0)
            if self.owl_panel:
                self.owl_panel.add_comment(
                    self.current_state['tick_id'],
                    "Thermal heat surge injected (+20°)",
                    OwlCommentType.SYSTEM,
                    priority=2
                )
    
    def execute_stabilize(self):
        """Execute thermal stabilization"""
        if self.pulse_controller:
            self.pulse_controller.regulate_heat(40.0)
            if self.owl_panel:
                self.owl_panel.add_comment(
                    self.current_state['tick_id'],
                    "Thermal regulation initiated (target: 40°)",
                    OwlCommentType.SYSTEM,
                    priority=2
                )
    
    def execute_next_sigil(self):
        """Execute the next sigil in the queue"""
        try:
            if self.sigil_engine:
                if hasattr(self.sigil_engine, 'execute_next_sigil'):
                    result = self.sigil_engine.execute_next_sigil()
                    if result:
                        self.notification_system.add_notification(
                            f"⚡ Executed sigil: {result.sigil_id} | Status: {result.status.value}", 
                            "info"
                        )
                    else:
                        self.notification_system.add_notification("⚡ No sigils available to execute", "warning")
                else:
                    self.notification_system.add_notification("⚡ Mock sigil executed", "info")
            else:
                self.notification_system.add_notification("❌ No sigil engine available", "error")
        except Exception as e:
            logger.error(f"Failed to execute next sigil: {e}")
            self.notification_system.add_notification(f"❌ Sigil execution failed: {e}", "error")

    def execute_clear_sigils(self):
        """Clear sigil ring"""
        if self.reflex_executor:
            try:
                results = self.reflex_executor.execute(["clear_sigil_ring"])
                self.display_reflex_results(results)
            except Exception as e:
                print(f"Failed to clear sigils: {e}")
    
    def add_test_sigil(self):
        """Add a test sigil"""
        if self.sigil_engine:
            sigil_ids = self.sigil_engine.inject_test_sigils(1)
            if self.owl_panel:
                self.owl_panel.add_comment(
                    self.current_state['tick_id'],
                    f"Test sigil added: {sigil_ids[0] if sigil_ids else 'none'}",
                    OwlCommentType.SYSTEM,
                    priority=1
                )
    
    def restore_normal_operation(self):
        """Restore normal system operation"""
        if self.reflex_executor:
            try:
                results = self.reflex_executor.restore_normal_operation()
                if self.owl_panel:
                    self.owl_panel.add_comment(
                        self.current_state['tick_id'],
                        "System restored to normal operation",
                        OwlCommentType.SYSTEM,
                        priority=2
                    )
            except Exception as e:
                print(f"Failed to restore normal operation: {e}")
    
    def cycle_color_mood(self):
        """Cycle through different color moods"""
        moods = ['calm', 'active', 'creative', 'agitated', 'reflective', 'neutral']
        new_mood = random.choice(moods)
        self.current_state['mood'] = new_mood
        self.update_visual_displays()
        
        if self.owl_panel:
            self.owl_panel.add_comment(
                self.current_state['tick_id'],
                f"Mood color changed to: {new_mood}",
                OwlCommentType.OBSERVATION,
                priority=1
            )
    
    def on_closing(self):
        """Handle window close event"""
        self.running = False
        self.root.destroy()


class NotificationSystem:
    """Simple notification system for GUI events"""
    
    def __init__(self):
        self.notifications = []
    
    def add_notification(self, message, level="info"):
        self.notifications.append({
            "message": message,
            "level": level,
            "timestamp": datetime.now()
        })


def main():
    """Main entry point for enhanced DAWN GUI"""
    root = tk.Tk()
    
    try:
        app = EnhancedDAWNGui(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Enhanced DAWN GUI stopped by user")
    except Exception as e:
        print(f"❌ Enhanced DAWN GUI error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 