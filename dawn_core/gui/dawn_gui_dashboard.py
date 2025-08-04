#!/usr/bin/env python3
"""
DAWN Unified GUI Dashboard
A comprehensive, single-window dashboard for monitoring and controlling DAWN's cognitive state.
Consolidates all GUI panels into a clean, dark-mode interface.

File: dawn_core/gui/dawn_gui_dashboard.py
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os
import sys
import time
import json
import threading
import queue
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np

# Direct tick engine integration
try:
    from core.tick.tick_engine import TickEngine
    TICK_ENGINE_AVAILABLE = True
except ImportError:
    print("⚠️ Tick engine not available")
    TICK_ENGINE_AVAILABLE = False

# Matplotlib imports for embedded visualizations
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for Tkinter integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# DAWN system imports with fallbacks
try:
    from dawn_core.snapshot_exporter import DAWNSnapshotExporter
    from core.spontaneity import SubtleSpontaneity
    from reflection.owl.owl_tracer import OwlTracer
    DAWN_COMPONENTS_AVAILABLE = True
    print("✅ DAWN components imported successfully")
except ImportError as e:
    print(f"⚠️ DAWN components not available: {e}")
    print("🔧 Using simulation mode")
    DAWN_COMPONENTS_AVAILABLE = False
    DAWNSnapshotExporter = None
    SubtleSpontaneity = None
    OwlTracer = None

# DAWN visualization imports with fallbacks
try:
    from visual.entropy_flow import EntropyFlowVisualizer
    from visual.tick_pulse import TickPulseVisualizer
    from visual.sigil_command_stream import SigilCommandStream
    from visual.consciousness_constellation import ConsciousnessConstellation
    from visual.heat_monitor import HeatMonitorVisualizer
    from visual.SCUP_pressure_grid import SCUPPressureGrid
    from visual.dawn_mood_state import MoodStateVisualizer
    from visual.scup_zone_animator import SCUPZoneAnimator
    from backend.visual.base_visualizer import BaseVisualizer
    VISUAL_COMPONENTS_AVAILABLE = True
    print("✅ DAWN visualization components imported successfully")
except ImportError as e:
    print(f"⚠️ DAWN visualization components not available: {e}")
    print("🔧 Using mock visualizations")
    VISUAL_COMPONENTS_AVAILABLE = False
    EntropyFlowVisualizer = None
    TickPulseVisualizer = None
    SigilCommandStream = None
    ConsciousnessConstellation = None
    HeatMonitorVisualizer = None
    SCUPPressureGrid = None
    MoodStateVisualizer = None
    SCUPZoneAnimator = None
    BaseVisualizer = None


class DAWNUnifiedDashboard:
    """
    Unified GUI Dashboard for DAWN Cognitive Engine
    Provides comprehensive real-time monitoring and control interface.
    """
    
    def __init__(self, root):
        """Initialize the unified dashboard."""
        self.root = root
        self.running = True
        self.update_queue = queue.Queue()
        
        # Direct tick engine integration for live data
        self.tick_engine = None
        self.tick_engine_running = False
        self.tick_data_queue = queue.Queue()
        self.last_tick_data = None
        
        # Initialize live data structure
        self.live_data = {
            "tick": 0,
            "scup": 50.0,
            "entropy": 0.5,
            "heat": 25.0,
            "mood": "analytical",
            "zone": "CALM",
            "zone_color": "#90EE90",
            "thermal": {
                "heat": 0.5,
                "momentum": 0.0,
                "stability": 1.0,
            },
            "performance": {},
            "timestamp": time.time(),
            "connected": False
        }
        
        # Initialize DAWN components
        self.snapshot_exporter = None
        self.owl_tracer = None
        self.spontaneity = None
        
        if DAWN_COMPONENTS_AVAILABLE:
            try:
                self.snapshot_exporter = DAWNSnapshotExporter()
                self.owl_tracer = OwlTracer("DASHBOARD")
                self.spontaneity = SubtleSpontaneity()
                print("🔗 Real DAWN components connected")
            except Exception as e:
                print(f"⚠️ Error initializing DAWN components: {e}")
                self.snapshot_exporter = None
        
        # Initialize visualization components
        self.visualizers = {}
        self.figure_canvases = {}
        
        if VISUAL_COMPONENTS_AVAILABLE:
            try:
                # Note: These will be instantiated when needed to avoid issues
                self.visualizers = {
                    'entropy_flow': None,
                    'tick_pulse': None,
                    'sigil_stream': None,
                    'consciousness_constellation': None,
                    'heat_monitor': None,
                    'scup_pressure_grid': None,
                    'mood_state': None,
                    'scup_zone_animator': None
                }
                print("🎨 Advanced visualization components ready")
            except Exception as e:
                print(f"⚠️ Error preparing visualizations: {e}")
                self.visualizers = {}
        else:
            self.visualizers = {}
        
        # Current system state
        self.current_state = {
            "tick": 0,
            "timestamp": datetime.now().isoformat(),
            "entropy": 0.5,
            "heat": 25.0,
            "zone": "CALM",
            "scup": 0.5,
            "coherence": 0.7,
            "active_sigils": 0,
            "forecast": {
                "likely_action": "Processing",
                "confidence": 0.75,
                "limit_horizon": 10.0,
                "probability": 0.8,
                "reliability": 0.9
            },
            "symbolic_anatomy": {
                "fractal_heart_charge": 0.6,
                "soma_coil_glyph": "∞",
                "glyph_lung_breath": "◊",
                "resonance_level": 0.7
            },
            "commentary": []
        }
        
        # GUI components
        self.widgets = {}
        self.commentary_text = None
        
        # Setup the interface
        self.setup_gui()
        self.apply_dark_theme()
        self.start_refresh_loop()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        print("🌟 DAWN Unified Dashboard initialized")
        
        # Start direct tick engine integration
        self.start_tick_engine()
    
    async def tick_callback(self, tick_data):
        """Async callback function to receive tick data directly from tick engine."""
        try:
            # The TickEngine sends data in this format:
            # {
            #   "tick": tick_count,
            #   "delta": delta_time,
            #   "interval": current_interval, 
            #   "thermal": thermal_state_dict,
            #   "performance": performance_metrics_dict
            # }
            
# Debug: print(f"🔥 Received tick data: {tick_data}")
            
            # Put tick data in queue for main thread (thread-safe)
            self.tick_data_queue.put(tick_data)
            self.last_tick_data = tick_data
            
        except Exception as e:
            print(f"⚠️ Error processing tick data: {e}")
            
    def sync_tick_callback(self, tick_data):
        """Synchronous wrapper for tick callback."""
        try:
# Debug: print(f"🔥 Received tick data (sync): {tick_data}")
            
            # Put tick data in queue for main thread (thread-safe)
            self.tick_data_queue.put(tick_data)
            self.last_tick_data = tick_data
            
        except Exception as e:
            print(f"⚠️ Error processing tick data: {e}")
    
    def start_tick_engine(self):
        """Start tick engine directly integrated with GUI."""
        if not TICK_ENGINE_AVAILABLE:
            print("⚠️ Tick engine integration disabled - tick engine not available")
            return
            
        def tick_engine_thread():
            try:
                print("🔥 Starting integrated DAWN tick engine...")
                
                # Create and configure tick engine
                self.tick_engine = TickEngine()
                
                # Register our callback to receive tick data (try async first, then sync)
                try:
                    self.tick_engine.register_handler('tick', self.tick_callback)
                    print("✅ Registered async tick callback")
                except Exception as e:
                    print(f"⚠️ Async callback failed, trying sync: {e}")
                    self.tick_engine.register_handler('tick', self.sync_tick_callback)
                
                # Start the tick engine
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                async def run_engine():
                    self.tick_engine_running = True
                    print("✅ Tick engine connected to GUI!")
                    await self.tick_engine.start()
                
                loop.run_until_complete(run_engine())
                
            except Exception as e:
                print(f"❌ Tick engine error: {e}")
                self.tick_engine_running = False
            finally:
                loop.close()
        
        # Start tick engine in background thread
        engine_thread = threading.Thread(target=tick_engine_thread, daemon=True)
        engine_thread.start()
        print("🚀 Tick engine integration thread started")
    
    def process_live_tick_data(self):
        """Process live tick data from tick engine queue."""
        try:
            processed_count = 0
            while not self.tick_data_queue.empty():
                tick_data = self.tick_data_queue.get_nowait()
                processed_count += 1
                
# Debug: print(f"🎨 Processing tick data #{processed_count}: tick={tick_data.get('tick', 'N/A')}")
                
                # Update dashboard data with live tick data
                if tick_data:
                    # Map TickEngine data structure to dashboard format
                    # TickEngine sends: {"tick": count, "delta": time, "interval": float, "thermal": {...}, "performance": {...}}
                    
                    thermal = tick_data.get("thermal", {})
                    performance = tick_data.get("performance", {})
                    tick_num = tick_data.get("tick", 0)
                    
                    # Generate derived metrics from thermal data
                    import random  # Ensure random is available in this scope
                    heat_value = thermal.get("heat", 0.0)
                    entropy_value = min(1.0, max(0.0, 0.3 + heat_value * 0.4 + random.uniform(-0.1, 0.1)))
                    scup_value = max(0.0, min(100.0, (1.0 - entropy_value) * 100 + random.uniform(-5, 5)))
                    
                    # Determine zone based on heat
                    if heat_value > 0.8:
                        zone, zone_color = "HOT", "#FF4444"
                    elif heat_value > 0.6:
                        zone, zone_color = "WARM", "#FFA500"
                    elif heat_value > 0.4:
                        zone, zone_color = "MILD", "#FFFF00"
                    else:
                        zone, zone_color = "CALM", "#90EE90"
                    
                    self.live_data.update({
                        "tick": tick_num,
                        "scup": scup_value,
                        "entropy": entropy_value,
                        "heat": heat_value * 100,  # Convert to 0-100 range for display  
                        "zone": zone,
                        "zone_color": zone_color,
                        "mood": "analytical" if heat_value < 0.5 else "active",
                        "thermal": thermal,
                        "performance": performance,
                        "timestamp": time.time(),
                        "connected": self.tick_engine_running,
                        # Add forecast data
                        "forecast": {
                            "likely_action": "Processing" if heat_value < 0.7 else "Thermal Management",
                            "confidence": min(0.95, 0.5 + heat_value * 0.4),
                            "limit_horizon": 8.0 + heat_value * 4.0,
                            "probability": min(0.95, 0.6 + entropy_value * 0.3),
                            "reliability": max(0.3, 1.0 - heat_value * 0.5)
                        },
                        # Add sigil data
                        "active_sigils": min(8, int(tick_num / 5) + int(heat_value * 3)),
                        "last_sigil": f"THERMAL_{tick_num % 7}" if tick_num > 0 else "None"
                    })
                    
                    # Add some dynamic metrics for visual feedback
                    if tick_num > 0:
                        import math  # Ensure math is available in this scope
                        self.live_data.update({
                            "symbolic_anatomy": {
                                "fractal_heart_charge": 0.5 + 0.3 * math.sin(tick_num * 0.1),
                                "soma_coil_glyph": "∞",
                                "glyph_lung_breath": "◊",
                                "resonance_level": 0.6 + 0.2 * math.cos(tick_num * 0.15)
                            }
                        })
                    
                    # Put updated data in update queue for GUI refresh
                    self.update_queue.put(self.live_data.copy())
# Debug: print(f"📊 Updated GUI data: tick={tick_num}, heat={heat_value:.3f}, entropy={entropy_value:.3f}, scup={scup_value:.1f}")
                    
        except queue.Empty:
            pass
        except Exception as e:
            print(f"⚠️ Error processing live tick data: {e}")
    
    def setup_gui(self):
        """Setup the main GUI interface with tabbed visualization layout."""
        # Configure window
        self.root.title("🌟 DAWN Unified Cognitive Dashboard")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#121212")
        
        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Setup header
        self.setup_header(main_frame)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Setup all tabs
        self.setup_overview_tab()
        self.setup_symbolic_body_tab()
        self.setup_entropy_drift_tab()
        self.setup_forecast_map_tab()
        self.setup_sigils_tab()
        self.setup_consciousness_tab()
        self.setup_heat_monitor_tab()
        self.setup_mood_landscape_tab()
        self.setup_scup_dynamics_tab()
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
    
    def setup_header(self, parent):
        """Setup the header section."""
        header_frame = ttk.LabelFrame(parent, text="🧠 DAWN Cognitive Engine", padding=10)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Create horizontal layout for header info
        header_content = ttk.Frame(header_frame)
        header_content.pack(fill=tk.X)
        
        # Left side: Title and tick
        left_frame = ttk.Frame(header_content)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            left_frame,
            text="DAWN Unified Cognitive Dashboard",
            font=("Consolas", 16, "bold"),
            bg="#121212",
            fg="#E0E0E0"
        )
        title_label.pack(anchor="w")
        
        self.widgets['tick_time'] = tk.Label(
            left_frame,
            text="Tick 0 | 00:00:00",
            font=("Consolas", 12),
            bg="#121212",
            fg="#90EE90"
        )
        self.widgets['tick_time'].pack(anchor="w", pady=(5, 0))
        
        # Right side: Key metrics
        right_frame = ttk.Frame(header_content)
        right_frame.pack(side=tk.RIGHT)
        
        # Key metrics display
        metrics_frame = ttk.Frame(right_frame)
        metrics_frame.pack(pady=5)
        
        # Current entropy
        tk.Label(metrics_frame, text="Entropy:", font=("Consolas", 10), 
                bg="#121212", fg="#E0E0E0").grid(row=0, column=0, sticky="e")
        self.widgets['header_entropy'] = tk.Label(metrics_frame, text="0.500", 
                                                 font=("Consolas", 10, "bold"),
                                                 bg="#121212", fg="#FFD700")
        self.widgets['header_entropy'].grid(row=0, column=1, padx=(5, 10))
        
        # Current heat
        tk.Label(metrics_frame, text="Heat:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=2, sticky="e")
        self.widgets['header_heat'] = tk.Label(metrics_frame, text="25.0°C",
                                             font=("Consolas", 10, "bold"),
                                             bg="#121212", fg="#FF6B6B")
        self.widgets['header_heat'].grid(row=0, column=3, padx=(5, 10))
        
        # Current zone
        tk.Label(metrics_frame, text="Zone:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=4, sticky="e")
        self.widgets['header_zone'] = tk.Label(metrics_frame, text="CALM",
                                             font=("Consolas", 10, "bold"),
                                             bg="#121212", fg="#90EE90")
        self.widgets['header_zone'].grid(row=0, column=5, padx=(5, 0))
        
        # Connection status indicator
        tk.Label(metrics_frame, text="Status:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=6, sticky="e", padx=(10, 0))
        self.widgets['connection_status'] = tk.Label(metrics_frame, text="🔴 Disconnected",
                                                   font=("Consolas", 10, "bold"),
                                                   bg="#121212", fg="#FF6B6B")
        self.widgets['connection_status'].grid(row=0, column=7, padx=(5, 0))
    
    def setup_overview_tab(self):
        """Setup the overview tab with pulse, forecast, and commentary."""
        overview_frame = ttk.Frame(self.notebook)
        self.notebook.add(overview_frame, text="📊 Overview")
        
        # Create paned window for left/right layout
        paned = ttk.PanedWindow(overview_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for controls and metrics
        left_panel = ttk.Frame(paned)
        paned.add(left_panel, weight=1)
        
        # Right panel for commentary
        right_panel = ttk.Frame(paned)
        paned.add(right_panel, weight=1)
        
        # Setup left panel sections
        self.setup_pulse_metrics(left_panel)
        self.setup_forecast_display(left_panel)
        self.setup_control_buttons(left_panel)
        
        # Setup right panel
        self.setup_commentary_feed(right_panel)
    
    def setup_pulse_metrics(self, parent):
        """Setup the pulse monitoring metrics."""
        pulse_frame = ttk.LabelFrame(parent, text="🔥 Pulse Metrics", padding=10)
        pulse_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create grid for metrics
        grid_frame = ttk.Frame(pulse_frame)
        grid_frame.pack(fill=tk.X)
        
        # Row 0: Entropy and Heat
        tk.Label(grid_frame, text="Entropy:", font=("Consolas", 10), 
                bg="#121212", fg="#E0E0E0").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.widgets['entropy_value'] = tk.Label(grid_frame, text="0.500", 
                                                 font=("Consolas", 10, "bold"),
                                                 bg="#121212", fg="#FFD700")
        self.widgets['entropy_value'].grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(grid_frame, text="Heat:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.widgets['heat_value'] = tk.Label(grid_frame, text="25.0°C",
                                             font=("Consolas", 10, "bold"),
                                             bg="#121212", fg="#FF6B6B")
        self.widgets['heat_value'].grid(row=0, column=3, sticky="w")
        
        # Row 1: Zone and SCUP
        tk.Label(grid_frame, text="Zone:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.widgets['zone_label'] = tk.Label(grid_frame, text="CALM",
                                             font=("Consolas", 10, "bold"),
                                             bg="#121212", fg="#90EE90")
        self.widgets['zone_label'].grid(row=1, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(grid_frame, text="SCUP:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=1, column=2, sticky="w", padx=(0, 5))
        self.widgets['scup_value'] = tk.Label(grid_frame, text="0.500",
                                             font=("Consolas", 10, "bold"),
                                             bg="#121212", fg="#87CEEB")
        self.widgets['scup_value'].grid(row=1, column=3, sticky="w")
        
        # Progress bars
        progress_frame = ttk.Frame(pulse_frame)
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Entropy bar
        tk.Label(progress_frame, text="Entropy:", font=("Consolas", 9),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=0, sticky="w")
        self.widgets['entropy_bar'] = ttk.Progressbar(progress_frame, length=200, mode='determinate')
        self.widgets['entropy_bar'].grid(row=0, column=1, padx=(10, 0), pady=2)
        
        # Heat bar  
        tk.Label(progress_frame, text="Heat:", font=("Consolas", 9),
                bg="#121212", fg="#E0E0E0").grid(row=1, column=0, sticky="w")
        self.widgets['heat_bar'] = ttk.Progressbar(progress_frame, length=200, mode='determinate')
        self.widgets['heat_bar'].grid(row=1, column=1, padx=(10, 0), pady=2)
    
    def setup_forecast_display(self, parent):
        """Setup the forecast display panel."""
        forecast_frame = ttk.LabelFrame(parent, text="🔮 Cognitive Forecast", padding=10)
        forecast_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid layout for forecast info
        grid_frame = ttk.Frame(forecast_frame)
        grid_frame.pack(fill=tk.X)
        
        # Row 0: Action and Horizon
        tk.Label(grid_frame, text="Likely Action:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.widgets['forecast_action'] = tk.Label(grid_frame, text="Processing",
                                                  font=("Consolas", 10, "bold"),
                                                  bg="#121212", fg="#87CEEB")
        self.widgets['forecast_action'].grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(grid_frame, text="Horizon:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.widgets['forecast_horizon'] = tk.Label(grid_frame, text="10.0",
                                                   font=("Consolas", 10, "bold"),
                                                   bg="#121212", fg="#DDA0DD")
        self.widgets['forecast_horizon'].grid(row=0, column=3, sticky="w")
        
        # Row 1: Confidence and Probability
        tk.Label(grid_frame, text="Confidence:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.widgets['forecast_confidence'] = ttk.Progressbar(grid_frame, length=100, mode='determinate')
        self.widgets['forecast_confidence'].grid(row=1, column=1, sticky="w", pady=2, padx=(0, 20))
        
        tk.Label(grid_frame, text="Probability:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=1, column=2, sticky="w", padx=(0, 5))
        self.widgets['forecast_probability'] = tk.Label(grid_frame, text="80%",
                                                       font=("Consolas", 10, "bold"),
                                                       bg="#121212", fg="#98FB98")
        self.widgets['forecast_probability'].grid(row=1, column=3, sticky="w")
    
    def setup_control_buttons(self, parent):
        """Setup the control buttons panel."""
        control_frame = ttk.LabelFrame(parent, text="🎛️ System Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Button grid
        button_frame = ttk.Frame(control_frame)
        button_frame.pack()
        
        # Row 0
        snapshot_btn = tk.Button(
            button_frame, text="📸 Snapshot", font=("Consolas", 9),
            bg="#2D2D2D", fg="#E0E0E0", activebackground="#3D3D3D",
            command=self.take_snapshot, padx=10, pady=3
        )
        snapshot_btn.grid(row=0, column=0, padx=2, pady=2)
        
        export_btn = tk.Button(
            button_frame, text="📄 Export", font=("Consolas", 9),
            bg="#2D2D2D", fg="#E0E0E0", activebackground="#3D3D3D",
            command=self.export_trace, padx=10, pady=3
        )
        export_btn.grid(row=0, column=1, padx=2, pady=2)
        
        # Row 1
        rebloom_btn = tk.Button(
            button_frame, text="🌸 Rebloom", font=("Consolas", 9),
            bg="#2D4A2D", fg="#90EE90", activebackground="#3D5A3D",
            command=self.trigger_rebloom, padx=10, pady=3
        )
        rebloom_btn.grid(row=1, column=0, padx=2, pady=2)
        
        stabilize_btn = tk.Button(
            button_frame, text="🛡️ Stabilize", font=("Consolas", 9),
            bg="#4A2D2D", fg="#FF6B6B", activebackground="#5A3D3D",
            command=self.trigger_stabilize, padx=10, pady=3
        )
        stabilize_btn.grid(row=1, column=1, padx=2, pady=2)
    
    def setup_symbolic_body_tab(self):
        """Setup the symbolic body tab with anatomy display and visualization."""
        symbolic_frame = ttk.Frame(self.notebook)
        self.notebook.add(symbolic_frame, text="🌸 Symbolic Body")
        
        # Create vertical layout
        top_frame = ttk.Frame(symbolic_frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        bottom_frame = ttk.Frame(symbolic_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Symbolic anatomy metrics
        anatomy_frame = ttk.LabelFrame(top_frame, text="🌸 Symbolic Anatomy", padding=10)
        anatomy_frame.pack(fill=tk.X)
        
        # Grid layout for symbolic components
        grid_frame = ttk.Frame(anatomy_frame)
        grid_frame.pack()
        
        # FractalHeart and SomaCoil
        tk.Label(grid_frame, text="💖 FractalHeart:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.widgets['fractal_heart'] = tk.Label(grid_frame, text="60%",
                                                font=("Consolas", 10, "bold"),
                                                bg="#121212", fg="#FF69B4")
        self.widgets['fractal_heart'].grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(grid_frame, text="🌀 SomaCoil:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.widgets['soma_coil'] = tk.Label(grid_frame, text="∞",
                                           font=("Consolas", 14, "bold"),
                                           bg="#121212", fg="#00CED1")
        self.widgets['soma_coil'].grid(row=0, column=3, sticky="w")
        
        # GlyphLung and Resonance
        tk.Label(grid_frame, text="🫁 GlyphLung:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=1, column=0, sticky="w", padx=(0, 5))
        self.widgets['glyph_lung'] = tk.Label(grid_frame, text="◊",
                                            font=("Consolas", 14, "bold"),
                                            bg="#121212", fg="#F0E68C")
        self.widgets['glyph_lung'].grid(row=1, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(grid_frame, text="📻 Resonance:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=1, column=2, sticky="w", padx=(0, 5))
        self.widgets['resonance'] = tk.Label(grid_frame, text="70%",
                                           font=("Consolas", 10, "bold"),
                                           bg="#121212", fg="#9370DB")
        self.widgets['resonance'].grid(row=1, column=3, sticky="w")
        
        # Symbolic charge visualization
        viz_frame = ttk.LabelFrame(bottom_frame, text="📊 Symbolic Charge Graph", padding=5)
        viz_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure for symbolic visualization
        self.create_symbolic_visualization(viz_frame)
    
    def setup_entropy_drift_tab(self):
        """Setup the entropy drift tab with historical entropy visualization."""
        entropy_frame = ttk.Frame(self.notebook)
        self.notebook.add(entropy_frame, text="🌊 Entropy Drift")
        
        # Create matplotlib figure for entropy over time
        viz_frame = ttk.LabelFrame(entropy_frame, text="📈 Entropy Over Time", padding=5)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_entropy_visualization(viz_frame)
    
    def setup_forecast_map_tab(self):
        """Setup the forecast map tab with vector drift visualization."""
        forecast_frame = ttk.Frame(self.notebook)
        self.notebook.add(forecast_frame, text="🌐 Forecast Map")
        
        # Create matplotlib figure for forecast vectors
        viz_frame = ttk.LabelFrame(forecast_frame, text="🗺️ Forecast Vector Drift", padding=5)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_forecast_visualization(forecast_frame)
    
    def setup_sigils_tab(self):
        """Setup the sigils tab with execution timeline."""
        sigils_frame = ttk.Frame(self.notebook)
        self.notebook.add(sigils_frame, text="⚡ Sigils")
        
        # Top panel for sigil info
        info_frame = ttk.LabelFrame(sigils_frame, text="⚡ Sigil Status", padding=10)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Sigil metrics
        metrics_frame = ttk.Frame(info_frame)
        metrics_frame.pack()
        
        tk.Label(metrics_frame, text="Active Sigils:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=0, sticky="w", padx=(0, 5))
        self.widgets['active_sigils'] = tk.Label(metrics_frame, text="0",
                                               font=("Consolas", 10, "bold"),
                                               bg="#121212", fg="#FFD700")
        self.widgets['active_sigils'].grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(metrics_frame, text="Last Sigil:", font=("Consolas", 10),
                bg="#121212", fg="#E0E0E0").grid(row=0, column=2, sticky="w", padx=(0, 5))
        self.widgets['last_sigil'] = tk.Label(metrics_frame, text="None",
                                            font=("Consolas", 10, "bold"),
                                            bg="#121212", fg="#DDA0DD")
        self.widgets['last_sigil'].grid(row=0, column=3, sticky="w")
        
        # Bottom panel for visualization
        viz_frame = ttk.LabelFrame(sigils_frame, text="📊 Sigil Execution Timeline", padding=5)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_sigil_visualization(viz_frame)
    
    def setup_commentary_feed(self, parent):
        """Setup the commentary feed panel."""
        commentary_frame = ttk.LabelFrame(parent, text="💬 Live Commentary Feed", padding=10)
        commentary_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrolled text widget
        self.commentary_text = scrolledtext.ScrolledText(
            commentary_frame,
            font=("Consolas", 9),
            bg="#1E1E1E",
            fg="#E0E0E0",
            insertbackground="#E0E0E0",
            selectbackground="#444444",
            wrap=tk.WORD
        )
        self.commentary_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial commentary
        self.add_commentary("System", "DAWN Unified Dashboard initialized")
        self.add_commentary("Owl", "Cognitive monitoring active")
        self.add_commentary("Visuals", "Advanced visualization system online")
        self.add_commentary("Visuals", "9 integrated visualization modules: Entropy, Symbolic, Forecast, Sigils, Consciousness, Heat, Mood, SCUP")
        self.add_commentary("System", "Real-time 3D consciousness constellation active")
        self.add_commentary("System", "Emotional landscape heatmap ready")
    
    def create_symbolic_visualization(self, parent):
        """Create symbolic charge visualization using matplotlib."""
        # Create figure
        fig = Figure(figsize=(8, 4), facecolor='#121212')
        ax = fig.add_subplot(111, facecolor='#121212')
        
        # Sample symbolic data
        components = ['FractalHeart', 'SomaCoil', 'GlyphLung', 'Resonance']
        values = [0.6, 0.8, 0.7, 0.5]
        colors = ['#FF69B4', '#00CED1', '#F0E68C', '#9370DB']
        
        bars = ax.bar(components, values, color=colors, alpha=0.8)
        ax.set_ylim(0, 1)
        ax.set_ylabel('Charge Level', color='#E0E0E0')
        ax.set_title('Symbolic Charge Distribution', color='#E0E0E0', fontsize=12, pad=20)
        
        # Style the plot
        ax.tick_params(colors='#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['top'].set_color('#E0E0E0')
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['right'].set_color('#E0E0E0')
        ax.grid(True, alpha=0.3, color='#444444')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['symbolic'] = canvas
    
    def create_entropy_visualization(self, parent):
        """Create entropy over time visualization."""
        # Create figure
        fig = Figure(figsize=(10, 6), facecolor='#121212')
        ax = fig.add_subplot(111, facecolor='#121212')
        
        # Sample entropy data over time
        time_points = np.linspace(0, 100, 50)
        entropy_values = 0.5 + 0.3 * np.sin(time_points / 10) + 0.1 * np.random.random(50)
        
        line = ax.plot(time_points, entropy_values, color='#FFD700', linewidth=2, alpha=0.8)[0]
        ax.fill_between(time_points, entropy_values, alpha=0.3, color='#FFD700')
        
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 1)
        ax.set_xlabel('Time (ticks)', color='#E0E0E0')
        ax.set_ylabel('Entropy Level', color='#E0E0E0')
        ax.set_title('Entropy Drift Over Time', color='#E0E0E0', fontsize=12, pad=20)
        
        # Style the plot
        ax.tick_params(colors='#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['top'].set_color('#E0E0E0')
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['right'].set_color('#E0E0E0')
        ax.grid(True, alpha=0.3, color='#444444')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['entropy'] = canvas
    
    def create_forecast_visualization(self, parent):
        """Create forecast vector field visualization."""
        # Create figure
        fig = Figure(figsize=(8, 6), facecolor='#121212')
        ax = fig.add_subplot(111, facecolor='#121212')
        
        # Create vector field
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        X, Y = np.meshgrid(x, y)
        
        # Sample vector field data
        U = -Y + 0.1 * np.random.random((10, 10))
        V = X + 0.1 * np.random.random((10, 10))
        
        quiver = ax.quiver(X, Y, U, V, np.sqrt(U**2 + V**2), cmap='plasma', alpha=0.8)
        
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.set_xlabel('Forecast Dimension X', color='#E0E0E0')
        ax.set_ylabel('Forecast Dimension Y', color='#E0E0E0')
        ax.set_title('Forecast Vector Field', color='#E0E0E0', fontsize=12, pad=20)
        
        # Style the plot
        ax.tick_params(colors='#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['top'].set_color('#E0E0E0')
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['right'].set_color('#E0E0E0')
        ax.grid(True, alpha=0.3, color='#444444')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['forecast'] = canvas
    
    def create_sigil_visualization(self, parent):
        """Create sigil execution timeline visualization."""
        # Create figure
        fig = Figure(figsize=(10, 4), facecolor='#121212')
        ax = fig.add_subplot(111, facecolor='#121212')
        
        # Sample sigil execution data
        sigil_types = ['Attention', 'Memory', 'Reasoning', 'Creative', 'Action']
        execution_times = [10, 25, 40, 55, 70]
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
        
        for i, (sigil, time, color) in enumerate(zip(sigil_types, execution_times, colors)):
            ax.scatter(time, i, s=200, c=color, alpha=0.8, edgecolors='white', linewidth=2)
            ax.text(time + 2, i, sigil, color='#E0E0E0', fontsize=10, va='center')
        
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, len(sigil_types) - 0.5)
        ax.set_xlabel('Time (ticks)', color='#E0E0E0')
        ax.set_ylabel('Sigil Type', color='#E0E0E0')
        ax.set_title('Sigil Execution Timeline', color='#E0E0E0', fontsize=12, pad=20)
        ax.set_yticks(range(len(sigil_types)))
        ax.set_yticklabels([])
        
        # Style the plot
        ax.tick_params(colors='#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['top'].set_color('#E0E0E0')
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['right'].set_color('#E0E0E0')
        ax.grid(True, alpha=0.3, color='#444444')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['sigils'] = canvas
    
    def setup_consciousness_tab(self):
        """Setup the consciousness constellation tab."""
        consciousness_frame = ttk.Frame(self.notebook)
        self.notebook.add(consciousness_frame, text="🌌 Consciousness")
        
        # Create matplotlib figure for consciousness constellation
        viz_frame = ttk.LabelFrame(consciousness_frame, text="🌌 Consciousness Constellation", padding=5)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_consciousness_visualization(viz_frame)
    
    def setup_heat_monitor_tab(self):
        """Setup the heat monitor tab."""
        heat_frame = ttk.Frame(self.notebook)
        self.notebook.add(heat_frame, text="🌡️ Heat Monitor")
        
        # Create matplotlib figure for heat monitor
        viz_frame = ttk.LabelFrame(heat_frame, text="🌡️ Cognitive Heat Monitor", padding=5)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_heat_monitor_visualization(viz_frame)
    
    def setup_mood_landscape_tab(self):
        """Setup the mood landscape tab."""
        mood_frame = ttk.Frame(self.notebook)
        self.notebook.add(mood_frame, text="😊 Mood Landscape")
        
        # Create matplotlib figure for mood state heatmap
        viz_frame = ttk.LabelFrame(mood_frame, text="😊 Emotional Landscape", padding=5)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_mood_visualization(viz_frame)
    
    def setup_scup_dynamics_tab(self):
        """Setup the SCUP dynamics tab."""
        scup_frame = ttk.Frame(self.notebook)
        self.notebook.add(scup_frame, text="🔄 SCUP Dynamics")
        
        # Create split layout for SCUP visualizations
        top_frame = ttk.Frame(scup_frame)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        bottom_frame = ttk.Frame(scup_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # SCUP pressure grid
        pressure_frame = ttk.LabelFrame(top_frame, text="🔄 SCUP Pressure Grid", padding=5)
        pressure_frame.pack(fill=tk.BOTH, expand=True)
        self.create_scup_pressure_visualization(pressure_frame)
        
        # SCUP zone animator
        zone_frame = ttk.LabelFrame(bottom_frame, text="🎯 SCUP Zone Evolution", padding=5)
        zone_frame.pack(fill=tk.BOTH, expand=True)
        self.create_scup_zone_visualization(zone_frame)
    
    def create_consciousness_visualization(self, parent):
        """Create consciousness constellation visualization."""
        # Create 3D figure for consciousness constellation
        fig = Figure(figsize=(10, 8), facecolor='#121212')
        ax = fig.add_subplot(111, projection='3d', facecolor='#121212')
        
        # Sample consciousness trajectory data
        t = np.linspace(0, 4*np.pi, 100)
        x = np.sin(t) * (1 + 0.5 * np.cos(3*t))
        y = np.cos(t) * (1 + 0.5 * np.cos(3*t))
        z = 0.5 * np.sin(3*t)
        
        # Color by consciousness level
        colors = plt.cm.plasma(np.linspace(0, 1, len(t)))
        
        # Plot trajectory
        for i in range(len(t)-1):
            ax.plot([x[i], x[i+1]], [y[i], y[i+1]], [z[i], z[i+1]], 
                   color=colors[i], linewidth=2, alpha=0.8)
        
        # Add consciousness archetypes as reference points
        archetypes = [
            ('Dormant', [0, 0, -1], '#424242'),
            ('Focused', [1, 0, 0], '#1976d2'),
            ('Creative', [0, 1, 0], '#7b1fa2'),
            ('Transcendent', [0, 0, 1], '#c2185b')
        ]
        
        for name, pos, color in archetypes:
            ax.scatter(*pos, color=color, s=200, alpha=0.8)
            ax.text(pos[0], pos[1], pos[2]+0.2, name, color='#E0E0E0', fontsize=10)
        
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-1.5, 1.5)
        ax.set_xlabel('Schema', color='#E0E0E0')
        ax.set_ylabel('Coherence', color='#E0E0E0')
        ax.set_zlabel('Utility', color='#E0E0E0')
        ax.set_title('Consciousness Constellation Trajectory', color='#E0E0E0', fontsize=12, pad=20)
        
        # Style the 3D plot
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('#444444')
        ax.yaxis.pane.set_edgecolor('#444444')
        ax.zaxis.pane.set_edgecolor('#444444')
        ax.grid(True, alpha=0.3, color='#444444')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['consciousness'] = canvas
    
    def create_heat_monitor_visualization(self, parent):
        """Create heat monitor gauge visualization."""
        # Create figure for heat gauge
        fig = Figure(figsize=(10, 6), facecolor='#121212')
        ax = fig.add_subplot(111, facecolor='#121212')
        
        # Create radial gauge segments
        angles = np.linspace(0, np.pi, 6)  # Half circle
        colors = ['#0066cc', '#00aaff', '#00ff88', '#ffaa00', '#ff3300']
        labels = ['Dormant', 'Warming', 'Active', 'Intense', 'Critical']
        
        for i, (start, end, color, label) in enumerate(zip(angles[:-1], angles[1:], colors, labels)):
            theta = np.linspace(start, end, 20)
            r_outer = 1.0
            r_inner = 0.6
            
            x_outer = r_outer * np.cos(theta)
            y_outer = r_outer * np.sin(theta)
            x_inner = r_inner * np.cos(theta)
            y_inner = r_inner * np.sin(theta)
            
            # Create wedge
            verts_outer = list(zip(x_outer, y_outer))
            verts_inner = list(zip(x_inner[::-1], y_inner[::-1]))
            verts = verts_outer + verts_inner
            
            from matplotlib.patches import Polygon
            wedge = Polygon(verts, facecolor=color, alpha=0.7, edgecolor='white', linewidth=1)
            ax.add_patch(wedge)
            
            # Add label
            mid_angle = (start + end) / 2
            label_x = 1.15 * np.cos(mid_angle)
            label_y = 1.15 * np.sin(mid_angle)
            ax.text(label_x, label_y, label, ha='center', va='center', 
                   color='#E0E0E0', fontsize=10)
        
        # Current heat indicator (needle)
        current_heat = 0.65  # Sample value
        needle_angle = current_heat * np.pi  # Half circle
        needle_x = [0, 0.9 * np.cos(needle_angle)]
        needle_y = [0, 0.9 * np.sin(needle_angle)]
        ax.plot(needle_x, needle_y, color='white', linewidth=4)
        ax.scatter([0], [0], color='white', s=100, zorder=10)
        
        ax.set_xlim(-1.3, 1.3)
        ax.set_ylim(-0.2, 1.3)
        ax.set_aspect('equal')
        ax.set_title('Cognitive Heat Monitor', color='#E0E0E0', fontsize=12, pad=20)
        ax.axis('off')
        
        # Add heat value text
        ax.text(0, -0.1, f'{current_heat*100:.1f}°', ha='center', va='center',
               fontsize=16, color='#E0E0E0', weight='bold')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['heat_monitor'] = canvas
    
    def create_mood_visualization(self, parent):
        """Create mood landscape heatmap visualization."""
        # Create figure for mood heatmap
        fig = Figure(figsize=(10, 8), facecolor='#121212')
        ax = fig.add_subplot(111, facecolor='#121212')
        
        # Sample mood data (8x8 emotional landscape)
        mood_dimensions = [
            'Transcendent', 'Ecstatic', 'Serene', 'Curious',
            'Focused', 'Contemplative', 'Uncertain', 'Turbulent'
        ]
        
        # Generate sample mood intensities
        np.random.seed(42)  # For consistent demo data
        mood_matrix = np.random.beta(2, 5, (8, 8))  # Skewed toward lower intensities
        
        # Create custom colormap
        colors = ['#0a0a0a', '#1a1a2e', '#16213e', '#0f3460', '#533483', 
                 '#7209b7', '#a663cc', '#4cc9f0', '#7209b7', '#f72585']
        from matplotlib.colors import LinearSegmentedColormap
        mood_cmap = LinearSegmentedColormap.from_list('mood', colors, N=256)
        
        # Create heatmap
        im = ax.imshow(mood_matrix, cmap=mood_cmap, aspect='equal', vmin=0, vmax=1)
        
        # Add labels
        ax.set_xticks(range(8))
        ax.set_yticks(range(8))
        ax.set_xticklabels(mood_dimensions, rotation=45, ha='right', fontsize=9, color='#E0E0E0')
        ax.set_yticklabels([f"Level {i+1}" for i in range(8)], fontsize=9, color='#E0E0E0')
        
        ax.set_title('Emotional Landscape', color='#E0E0E0', fontsize=12, pad=20)
        
        # Add colorbar
        cbar = fig.colorbar(im, ax=ax, shrink=0.6)
        cbar.set_label('Emotional Intensity', color='#E0E0E0')
        cbar.ax.yaxis.set_tick_params(color='#E0E0E0')
        cbar.outline.set_edgecolor('#E0E0E0')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['mood'] = canvas
    
    def create_scup_pressure_visualization(self, parent):
        """Create SCUP pressure grid visualization."""
        # Create figure for SCUP pressure grid
        fig = Figure(figsize=(8, 6), facecolor='#121212')
        ax = fig.add_subplot(111, facecolor='#121212')
        
        # SCUP dimensions
        dimensions = ['Schema', 'Coherence', 'Utility', 'Pressure']
        
        # Sample SCUP interaction matrix
        scup_matrix = np.array([
            [0.7, 0.5, 0.3, 0.4],  # Schema interactions
            [0.5, 0.8, 0.6, 0.3],  # Coherence interactions
            [0.3, 0.6, 0.9, 0.7],  # Utility interactions
            [0.4, 0.3, 0.7, 0.6]   # Pressure interactions
        ])
        
        # Create heatmap
        im = ax.imshow(scup_matrix, cmap='plasma', aspect='equal', vmin=0, vmax=1)
        
        # Add labels
        ax.set_xticks(range(4))
        ax.set_yticks(range(4))
        ax.set_xticklabels(dimensions, fontsize=10, color='#E0E0E0')
        ax.set_yticklabels(dimensions, fontsize=10, color='#E0E0E0')
        
        # Add value annotations
        for i in range(4):
            for j in range(4):
                text = ax.text(j, i, f'{scup_matrix[i, j]:.2f}',
                             ha="center", va="center", color="white", fontsize=10)
        
        ax.set_title('SCUP Pressure Interaction Grid', color='#E0E0E0', fontsize=12, pad=20)
        
        # Add colorbar
        cbar = fig.colorbar(im, ax=ax, shrink=0.6)
        cbar.set_label('Interaction Strength', color='#E0E0E0')
        cbar.ax.yaxis.set_tick_params(color='#E0E0E0')
        cbar.outline.set_edgecolor('#E0E0E0')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['scup_pressure'] = canvas
    
    def create_scup_zone_visualization(self, parent):
        """Create SCUP zone evolution visualization."""
        # Create figure for SCUP zones
        fig = Figure(figsize=(10, 4), facecolor='#121212')
        ax = fig.add_subplot(111, facecolor='#121212')
        
        # Sample SCUP zone evolution over time
        time_points = np.linspace(0, 100, 50)
        
        # Different cognitive zones over time
        zones = ['Dormant', 'Contemplative', 'Active', 'Intense', 'Transcendent']
        zone_colors = ['#424242', '#2196f3', '#4caf50', '#ff9800', '#9c27b0']
        
        # Generate sample zone transitions
        zone_data = []
        current_zone = 1  # Start in contemplative
        for i in range(len(time_points)):
            # Random walk through zones with boundaries
            if np.random.random() < 0.1:  # 10% chance to change zone
                change = np.random.choice([-1, 1])
                current_zone = max(0, min(4, current_zone + change))
            zone_data.append(current_zone)
        
        # Plot zone evolution
        for i, (zone, color) in enumerate(zip(zones, zone_colors)):
            mask = np.array(zone_data) == i
            if np.any(mask):
                ax.fill_between(time_points[mask], i-0.4, i+0.4, 
                               color=color, alpha=0.7, label=zone)
        
        # Plot the actual trajectory
        ax.plot(time_points, zone_data, color='white', linewidth=2, alpha=0.8)
        ax.scatter(time_points, zone_data, c=[zone_colors[z] for z in zone_data], 
                  s=30, alpha=0.9, edgecolors='white', linewidth=1)
        
        ax.set_xlim(0, 100)
        ax.set_ylim(-0.5, 4.5)
        ax.set_xlabel('Time (ticks)', color='#E0E0E0')
        ax.set_ylabel('Cognitive Zone', color='#E0E0E0')
        ax.set_title('SCUP Zone Evolution', color='#E0E0E0', fontsize=12, pad=20)
        ax.set_yticks(range(5))
        ax.set_yticklabels(zones, color='#E0E0E0')
        ax.tick_params(colors='#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.spines['top'].set_color('#E0E0E0')
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['right'].set_color('#E0E0E0')
        ax.grid(True, alpha=0.3, color='#444444')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_canvases['scup_zone'] = canvas
    
    def on_tab_changed(self, event):
        """Handle tab change events."""
        selected_tab = event.widget.tab('current')['text']
        self.add_commentary("System", f"Switched to {selected_tab} view")
    

    
    def apply_dark_theme(self):
        """Apply dark theme styling to ttk widgets."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme
        style.configure("TFrame", background="#121212")
        style.configure("TLabelFrame", background="#121212", foreground="#E0E0E0")
        style.configure("TLabelFrame.Label", background="#121212", foreground="#E0E0E0")
        style.configure("TLabel", background="#121212", foreground="#E0E0E0")
        style.configure("TProgressbar", background="#444444", troughcolor="#2D2D2D")
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current system state from live tick data, DAWN, or simulation."""
        
        # PRIORITY 1: Use live tick data if available
        if hasattr(self, 'live_data') and self.live_data and self.live_data.get('tick', 0) > 0:
# Debug: print(f"🔥 Using live tick data: tick={self.live_data.get('tick')}")
            return self.live_data.copy()
        
        # PRIORITY 2: Use snapshot exporter if available
        if self.snapshot_exporter:
            try:
                return self.snapshot_exporter.get_state()
            except Exception as e:
                print(f"⚠️ Error getting real state: {e}")
        
        # PRIORITY 3: Simulation mode - generate realistic data
        import random
        import math
        
        # Simulate entropy with some oscillation
        time_factor = time.time() / 10
        base_entropy = 0.5 + 0.3 * math.sin(time_factor)
        entropy = max(0.0, min(1.0, base_entropy + random.uniform(-0.1, 0.1)))
        
        # Heat correlates with entropy
        heat = 20 + (entropy * 60) + random.uniform(-5, 5)
        
        # Zone based on heat
        if heat < 30:
            zone = "CALM"
            zone_color = "#90EE90"
        elif heat < 50:
            zone = "ACTIVE"
            zone_color = "#FFD700"
        elif heat < 70:
            zone = "STRESSED"
            zone_color = "#FFA500"
        else:
            zone = "SURGE"
            zone_color = "#FF6B6B"
        
        # Update current state
        self.current_state.update({
            "tick": self.current_state["tick"] + 1,
            "timestamp": datetime.now().isoformat(),
            "entropy": entropy,
            "heat": heat,
            "zone": zone,
            "zone_color": zone_color,
            "scup": 0.3 + (entropy * 0.4) + random.uniform(-0.1, 0.1),
            "coherence": 1.0 - entropy + random.uniform(-0.1, 0.1),
            "active_sigils": random.randint(0, 5)
        })
        
        return self.current_state
    
    def update_widgets(self, state: Dict[str, Any]):
        """Update all GUI widgets with current state."""
        try:
            # Update header with visual indicator
            tick = state.get("tick", 0)
            timestamp = datetime.now().strftime("%H:%M:%S")
            # Add blinking indicator to show live updates
            indicator = "●" if (tick % 2 == 0) else "○"
            self.widgets['tick_time'].config(text=f"Tick {tick} | {timestamp} {indicator}")
            
            # Update header metrics
            entropy = state.get("entropy", 0.5)
            heat = state.get("heat", 25.0)
            zone = state.get("zone", "CALM")
            zone_color = state.get("zone_color", "#90EE90")
            scup = state.get("scup", 0.5)
            
            self.widgets['header_entropy'].config(text=f"{entropy:.3f}")
            self.widgets['header_heat'].config(text=f"{heat:.1f}°C")
            self.widgets['header_zone'].config(text=zone, fg=zone_color)
            
            # Update connection status
            if self.tick_engine_running and self.last_tick_data:
                self.widgets['connection_status'].config(text="🟢 Live Data", fg="#90EE90")
            elif TICK_ENGINE_AVAILABLE:
                self.widgets['connection_status'].config(text="🟡 Starting...", fg="#FFD700")
            else:
                self.widgets['connection_status'].config(text="🔴 No Engine", fg="#FF6B6B")
            
            # Update overview tab metrics
            if 'entropy_value' in self.widgets:
                self.widgets['entropy_value'].config(text=f"{entropy:.3f}")
                self.widgets['entropy_bar']['value'] = entropy * 100
                
                self.widgets['heat_value'].config(text=f"{heat:.1f}°C")
                self.widgets['heat_bar']['value'] = min(heat, 100)
                
                self.widgets['zone_label'].config(text=zone, fg=zone_color)
                self.widgets['scup_value'].config(text=f"{scup:.3f}")
                
                # Update forecast
                forecast = state.get("forecast", {})
                self.widgets['forecast_action'].config(text=forecast.get("likely_action", "Processing"))
                self.widgets['forecast_confidence']['value'] = forecast.get("confidence", 0.75) * 100
                self.widgets['forecast_horizon'].config(text=f"{forecast.get('limit_horizon', 10.0):.1f}")
                self.widgets['forecast_probability'].config(text=f"{forecast.get('probability', 0.8)*100:.0f}%")
                print(f"📊 Updated forecast: action={forecast.get('likely_action', 'Processing')}, confidence={forecast.get('confidence', 0.75)*100:.0f}%")
            
            # Update symbolic anatomy
            if 'fractal_heart' in self.widgets:
                symbolic = state.get("symbolic_anatomy", {})
                self.widgets['fractal_heart'].config(text=f"{symbolic.get('fractal_heart_charge', 0.6)*100:.0f}%")
                self.widgets['soma_coil'].config(text=symbolic.get('soma_coil_glyph', '∞'))
                self.widgets['glyph_lung'].config(text=symbolic.get('glyph_lung_breath', '◊'))
                self.widgets['resonance'].config(text=f"{symbolic.get('resonance_level', 0.7)*100:.0f}%")
                print(f"🔮 Updated symbolic anatomy: heart={symbolic.get('fractal_heart_charge', 0.6)*100:.0f}%")
            else:
                print(f"⚠️ Symbolic anatomy widgets not found in widgets: {list(self.widgets.keys())[:10]}...")
            
            # Update sigil information
            if 'active_sigils' in self.widgets:
                self.widgets['active_sigils'].config(text=str(state.get("active_sigils", 0)))
                self.widgets['last_sigil'].config(text=state.get("last_sigil", "None"))
                print(f"🔯 Updated sigils: active={state.get('active_sigils', 0)}, last={state.get('last_sigil', 'None')}")
            else:
                print(f"⚠️ Sigil widgets not found")
            
            # Update visualizations
            self.refresh_visualizations(state)
            
        except Exception as e:
            print(f"⚠️ Error updating widgets: {e}")
            import traceback
            traceback.print_exc()
            
            # Try to update at least basic widgets
            try:
                tick = state.get("tick", 0)
                timestamp = datetime.now().strftime("%H:%M:%S")
                indicator = "●" if (tick % 2 == 0) else "○"
                self.widgets['tick_time'].config(text=f"Tick {tick} | {timestamp} {indicator}")
            except:
                pass
    
    def refresh_visualizations(self, state: Dict[str, Any]):
        """Refresh matplotlib visualizations with new data."""
        try:
            # Only update visualizations every few ticks to avoid performance issues
            tick = state.get("tick", 0)
            if tick % 5 != 0:  # Update every 5 ticks
                return
            
            # Update entropy visualization
            if 'entropy' in self.figure_canvases:
                canvas = self.figure_canvases['entropy']
                fig = canvas.figure
                ax = fig.axes[0]
                
                # Add new entropy data point
                entropy = state.get("entropy", 0.5)
                if hasattr(self, 'entropy_history'):
                    self.entropy_history.append(entropy)
                    if len(self.entropy_history) > 50:
                        self.entropy_history.pop(0)
                else:
                    self.entropy_history = [entropy]
                
                # Update plot
                ax.clear()
                time_points = list(range(len(self.entropy_history)))
                ax.plot(time_points, self.entropy_history, color='#FFD700', linewidth=2, alpha=0.8)
                ax.fill_between(time_points, self.entropy_history, alpha=0.3, color='#FFD700')
                
                ax.set_xlim(0, 50)
                ax.set_ylim(0, 1)
                ax.set_xlabel('Time (ticks)', color='#E0E0E0')
                ax.set_ylabel('Entropy Level', color='#E0E0E0')
                ax.set_title('Entropy Drift Over Time', color='#E0E0E0', fontsize=12, pad=20)
                ax.set_facecolor('#121212')
                ax.tick_params(colors='#E0E0E0')
                ax.spines['bottom'].set_color('#E0E0E0')
                ax.spines['top'].set_color('#E0E0E0')
                ax.spines['left'].set_color('#E0E0E0')
                ax.spines['right'].set_color('#E0E0E0')
                ax.grid(True, alpha=0.3, color='#444444')
                
                canvas.draw()
            
            # Update symbolic visualization
            if 'symbolic' in self.figure_canvases:
                canvas = self.figure_canvases['symbolic']
                fig = canvas.figure
                ax = fig.axes[0]
                
                # Update symbolic data
                symbolic = state.get("symbolic_anatomy", {})
                values = [
                    symbolic.get('fractal_heart_charge', 0.6),
                    symbolic.get('soma_coil_resonance', 0.8),
                    symbolic.get('glyph_lung_breath_rate', 0.7),
                    symbolic.get('resonance_level', 0.5)
                ]
                
                ax.clear()
                components = ['FractalHeart', 'SomaCoil', 'GlyphLung', 'Resonance']
                colors = ['#FF69B4', '#00CED1', '#F0E68C', '#9370DB']
                
                bars = ax.bar(components, values, color=colors, alpha=0.8)
                ax.set_ylim(0, 1)
                ax.set_ylabel('Charge Level', color='#E0E0E0')
                ax.set_title('Symbolic Charge Distribution', color='#E0E0E0', fontsize=12, pad=20)
                ax.set_facecolor('#121212')
                ax.tick_params(colors='#E0E0E0')
                ax.spines['bottom'].set_color('#E0E0E0')
                ax.spines['top'].set_color('#E0E0E0')
                ax.spines['left'].set_color('#E0E0E0')
                ax.spines['right'].set_color('#E0E0E0')
                ax.grid(True, alpha=0.3, color='#444444')
                
                canvas.draw()
                
        except Exception as e:
            print(f"⚠️ Error refreshing visualizations: {e}")
    
    def add_commentary(self, source: str, message: str):
        """Add a comment to the commentary feed."""
        if self.commentary_text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {source}: {message}\n"
            
            self.commentary_text.insert(tk.END, formatted_message)
            self.commentary_text.see(tk.END)
            
            # Keep only last 100 lines
            lines = self.commentary_text.get("1.0", tk.END).split('\n')
            if len(lines) > 100:
                self.commentary_text.delete("1.0", "2.0")
    
    def generate_commentary(self, state: Dict[str, Any]):
        """Generate contextual commentary based on system state."""
        entropy = state.get("entropy", 0.5)
        heat = state.get("heat", 25.0)
        zone = state.get("zone", "CALM")
        scup = state.get("scup", 0.5)
        
        # Generate commentary based on state
        if entropy > 0.8:
            self.add_commentary("Owl", f"High entropy detected: {entropy:.3f} - creative burst imminent")
        elif entropy < 0.2:
            self.add_commentary("Owl", f"Low entropy: {entropy:.3f} - system in stable configuration")
        
        if heat > 70:
            self.add_commentary("System", f"Thermal elevation: {heat:.1f}°C - {zone} zone active")
        elif heat < 25:
            self.add_commentary("System", f"Cool thermal state: {heat:.1f}°C - serene processing")
        
        # Use optimized SCUP logging to prevent spam
        try:
            from core.scup_logger_optimizer import monitor_scup
            scup_message = monitor_scup(scup, "Owl")
            if scup_message:
                self.add_commentary("Owl", scup_message)
        except ImportError:
            # Fallback to old behavior if optimizer not available
            if scup > 0.8:
                self.add_commentary("Owl", f"Exceptional SCUP: {scup:.3f} - peak consciousness unity")
            elif scup < 0.3:
                self.add_commentary("Owl", f"Low SCUP: {scup:.3f} - consciousness fragmentation detected")
        
        # Add spontaneous thoughts occasionally
        if self.spontaneity and hasattr(self.spontaneity, 'generate_spontaneous_thought'):
            try:
                thought = self.spontaneity.generate_spontaneous_thought(state, {})
                if thought:
                    self.add_commentary("DAWN", thought)
            except Exception as e:
                pass  # Ignore spontaneity errors
    
    def refresh(self):
        """Main refresh loop - updates every 2 seconds."""
        if not self.running:
            return
        
        try:
            # Process live tick data from tick engine
            self.process_live_tick_data()
            
            # Get current state
            state = self.get_current_state()
            
            # Debug: Show current state
            if hasattr(self, 'last_tick_data') and self.last_tick_data:
                # Debug: print(f"🖥️ Updating widgets with tick={state.get('tick', 0)}, heat={state.get('heat', 0):.1f}")
                pass
            
            # Update all widgets
            self.update_widgets(state)
            
            # Generate commentary occasionally (every ~10 seconds)
            if state.get("tick", 0) % 5 == 0:
                self.generate_commentary(state)
            
        except Exception as e:
            print(f"⚠️ Error in refresh loop: {e}")
            self.add_commentary("Error", f"Refresh error: {str(e)}")
        
        # Schedule next refresh - much faster for live data
        self.root.after(200, self.refresh)  # 200ms = 5Hz refresh rate
    
    def start_refresh_loop(self):
        """Start the non-blocking refresh loop."""
        self.root.after(1000, self.refresh)  # Start after 1 second
    
    # Control methods
    def trigger_stabilize(self):
        """Trigger the STABILIZE_PROTOCOL."""
        self.add_commentary("System", "🛡️ STABILIZE_PROTOCOL activated")
        messagebox.showinfo("Stabilize", "STABILIZE_PROTOCOL has been triggered")
    
    def take_snapshot(self):
        """Take a system state snapshot."""
        try:
            state = self.get_current_state()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(state, f, indent=2, default=str)
            
            self.add_commentary("System", f"📸 Snapshot saved: {filename}")
            messagebox.showinfo("Snapshot", f"System snapshot saved as {filename}")
        except Exception as e:
            self.add_commentary("Error", f"Snapshot failed: {str(e)}")
            messagebox.showerror("Error", f"Snapshot failed: {str(e)}")
    
    def export_trace(self):
        """Export symbolic trace."""
        try:
            # Generate trace data
            trace_data = {
                "timestamp": datetime.now().isoformat(),
                "state": self.get_current_state(),
                "commentary_history": self.commentary_text.get("1.0", tk.END).split('\n')
            }
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"symbolic_trace_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(trace_data, f, indent=2, default=str)
            
            self.add_commentary("System", f"📄 Symbolic trace exported: {filename}")
            messagebox.showinfo("Export", f"Symbolic trace exported as {filename}")
        except Exception as e:
            self.add_commentary("Error", f"Export failed: {str(e)}")
            messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def trigger_rebloom(self):
        """Trigger manual rebloom."""
        self.add_commentary("System", "🌸 Manual rebloom triggered")
        self.add_commentary("Bloom", "Rebloom sequence initiated - cognitive restructuring active")
        messagebox.showinfo("Rebloom", "Manual rebloom has been triggered")
    
    def on_closing(self):
        """Handle window closing."""
        self.running = False
        self.add_commentary("System", "🌅 DAWN Dashboard shutting down")
        
        # Stop tick engine if running
        if self.tick_engine_running and self.tick_engine:
            print("🛑 Stopping tick engine...")
            try:
                # Signal the tick engine to stop
                self.tick_engine_running = False
                self.add_commentary("System", "🛑 Tick engine stopped")
            except Exception as e:
                print(f"⚠️ Error stopping tick engine: {e}")
        
        self.root.after(500, self.root.destroy)  # Give time for final commentary


def main():
    """Main entry point for the DAWN Unified Dashboard."""
    print("🌟 Starting DAWN Unified Cognitive Dashboard...")
    
    # Create main window
    root = tk.Tk()
    
    # Create dashboard
    dashboard = DAWNUnifiedDashboard(root)
    
    # Start the GUI
    try:
        print("🚀 Dashboard ready - entering main loop")
        root.mainloop()
    except KeyboardInterrupt:
        print("\n⚠️ Dashboard shutdown requested")
        dashboard.on_closing()
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
    finally:
        print("🌅 DAWN Unified Dashboard closed")


if __name__ == "__main__":
    main() 