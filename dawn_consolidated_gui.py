#!/usr/bin/env python3
"""
DAWN Consolidated GUI - Complete Tabbed Interface
Integrates all DAWN components into a unified, professional interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import queue
import time
import json
import logging
import math
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import websockets

# Import existing DAWN components
TickEngine = None
ConsciousnessModel = None
VoiceMoodModulator = None
PlatonicPigmentMap = None
generate_julia_image = None
DAWNWebSocketServer = None

try:
    from backend.core.tick.tick_engine import TickEngine
except ImportError:
    pass

try:
    from backend.core.consciousness_model import ConsciousnessModel
except ImportError:
    pass

try:
    from backend.core.voice_mood_modulation import VoiceMoodModulator
except ImportError:
    pass

try:
    from backend.core.platonic_pigment import PlatonicPigmentMap
except ImportError:
    pass

try:
    from backend.visual.fractal_generator import generate_julia_image
except ImportError:
    pass

try:
    from backend.api.websocket_server import DAWNWebSocketServer
except ImportError:
    pass

# Visual components
try:
    from BP.fractal_bloom_canvas import FractalCanvas
except ImportError:
    FractalCanvas = None

try:
    from visual.sigil_overlay_panel import SigilOverlayPanel
except ImportError:
    SigilOverlayPanel = None

class DAWNConsolidatedGUI:
    """
    Complete consolidated DAWN GUI with tabbed interface
    """
    
    def __init__(self):
        """Initialize the consolidated GUI"""
        self.root = tk.Tk()
        self.root.title("DAWN - Deep Consciousness Interface")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0d1b2a")
        
        # Data queues for real-time updates
        self.state_queue = queue.Queue()
        self.voice_queue = queue.Queue()
        self.visual_queue = queue.Queue()
        self.log_queue = queue.Queue()
        
        # Current DAWN state
        self.current_state = {
            "entropy": 0.5,
            "mood": "NEUTRAL",
            "pigments": {"red": 0.3, "green": 0.3, "blue": 0.3, "yellow": 0.2, "violet": 0.2, "orange": 0.2},
            "drift_vector": [0.0, 0.0],
            "scup": 50.0,
            "thermal_zone": "CALM",
            "uptime": 0,
            "is_connected": False
        }
        
        # Component instances
        self.tick_engine = None
        self.voice_modulator = None
        self.pigment_map = None
        self.websocket_server = None
        
        # GUI components
        self.notebook = None
        self.visual_tab = None
        self.voice_tab = None
        self.state_tab = None
        self.controls_tab = None
        self.archive_tab = None
        self.logs_tab = None
        
        # Visual components
        self.fractal_canvas = None
        self.sigil_overlay = None
        
        # Initialize GUI
        self.setup_style()
        self.create_main_interface()
        self.setup_backend_connection()
        self.start_update_threads()
        
    def setup_style(self):
        """Configure GUI styling"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Dark theme configuration
        self.style.configure('Dark.TFrame', background='#0d1b2a')
        self.style.configure('Dark.TLabel', background='#0d1b2a', foreground='#cccccc', font=('JetBrains Mono', 10))
        self.style.configure('Dark.TButton', background='#1e3a4e', foreground='#cccccc', font=('JetBrains Mono', 9))
        self.style.configure('Dark.TNotebook', background='#0d1b2a', borderwidth=0)
        self.style.configure('Dark.TNotebook.Tab', background='#1e3a4e', foreground='#cccccc', 
                           padding=[20, 8], font=('JetBrains Mono', 10))
        self.style.map('Dark.TNotebook.Tab', background=[('selected', '#40e0ff')])
        
    def create_main_interface(self):
        """Create the main tabbed interface"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Dark.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create all tabs
        self.create_visual_tab()
        self.create_voice_tab()
        self.create_state_monitor_tab()
        self.create_controls_tab()
        self.create_archive_tab()
        self.create_logs_tab()
        
    def create_visual_tab(self):
        """Create the Visual tab for all visual processes"""
        self.visual_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.visual_tab, text="🖼️ Visual")
        
        # Main layout: left controls, center display, right parameters
        visual_paned = ttk.PanedWindow(self.visual_tab, orient=tk.HORIZONTAL)
        visual_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Visual controls
        left_frame = ttk.Frame(visual_paned, style='Dark.TFrame')
        visual_paned.add(left_frame, weight=20)
        
        controls_label = ttk.Label(left_frame, text="VISUAL CONTROLS", style='Dark.TLabel', font=('JetBrains Mono', 12, 'bold'))
        controls_label.pack(pady=(0, 10))
        
        # Fractal type selection
        ttk.Label(left_frame, text="Fractal Type:", style='Dark.TLabel').pack(anchor=tk.W)
        self.fractal_type_var = tk.StringVar(value="Julia Set")
        fractal_combo = ttk.Combobox(left_frame, textvariable=self.fractal_type_var, 
                                   values=["Julia Set", "Mandelbrot", "Bloom Fractal", "Sigil Pattern"])
        fractal_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Render size
        ttk.Label(left_frame, text="Render Size:", style='Dark.TLabel').pack(anchor=tk.W)
        self.render_size_var = tk.IntVar(value=512)
        render_scale = ttk.Scale(left_frame, from_=256, to=2048, variable=self.render_size_var, 
                               orient=tk.HORIZONTAL)
        render_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Animation speed
        ttk.Label(left_frame, text="Animation Speed:", style='Dark.TLabel').pack(anchor=tk.W)
        self.anim_speed_var = tk.DoubleVar(value=1.0)
        anim_scale = ttk.Scale(left_frame, from_=0.1, to=3.0, variable=self.anim_speed_var, 
                             orient=tk.HORIZONTAL)
        anim_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Action buttons
        ttk.Button(left_frame, text="Generate New Fractal", 
                  command=self.generate_new_fractal, style='Dark.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="Save Current Visual", 
                  command=self.save_current_visual, style='Dark.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="Export Animation", 
                  command=self.export_animation, style='Dark.TButton').pack(fill=tk.X, pady=2)
        
        # Center panel - Main visual display
        center_frame = ttk.Frame(visual_paned, style='Dark.TFrame')
        visual_paned.add(center_frame, weight=60)
        
        display_label = ttk.Label(center_frame, text="VISUAL DISPLAY", style='Dark.TLabel', font=('JetBrains Mono', 12, 'bold'))
        display_label.pack(pady=(0, 10))
        
        # Main visual canvas
        if FractalCanvas:
            self.fractal_canvas = FractalCanvas(center_frame, width=500, height=400)
            self.fractal_canvas.pack(expand=True)
        else:
            fallback_canvas = tk.Canvas(center_frame, bg="#1a1a1a", width=500, height=400)
            fallback_canvas.pack(expand=True)
            fallback_canvas.create_text(250, 200, text="Visual Display\n(Fractal rendering unavailable)", 
                                      fill="#888888", font=("JetBrains Mono", 12))
        
        # Visual history strip (bottom)
        history_frame = ttk.Frame(center_frame, style='Dark.TFrame')
        history_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(history_frame, text="Recent Visuals:", style='Dark.TLabel').pack(anchor=tk.W)
        history_canvas = tk.Canvas(history_frame, bg="#1a1a1a", height=60)
        history_canvas.pack(fill=tk.X)
        
        # Right panel - Live parameters
        right_frame = ttk.Frame(visual_paned, style='Dark.TFrame')
        visual_paned.add(right_frame, weight=20)
        
        params_label = ttk.Label(right_frame, text="LIVE PARAMETERS", style='Dark.TLabel', font=('JetBrains Mono', 12, 'bold'))
        params_label.pack(pady=(0, 10))
        
        # Parameter displays
        self.create_parameter_display(right_frame, "Entropy Score", "entropy_bar")
        self.create_parameter_display(right_frame, "Mood Valence", "mood_bar")
        self.create_parameter_display(right_frame, "Drift Vector", "drift_display")
        self.create_parameter_display(right_frame, "Julia Constant", "julia_display")
        
    def create_voice_tab(self):
        """Create the Voice tab for audio/speech processes"""
        self.voice_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.voice_tab, text="🗣️ Voice")
        
        # Main layout: left controls, center display, right pigments
        voice_paned = ttk.PanedWindow(self.voice_tab, orient=tk.HORIZONTAL)
        voice_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Voice controls
        left_frame = ttk.Frame(voice_paned, style='Dark.TFrame')
        voice_paned.add(left_frame, weight=25)
        
        controls_label = ttk.Label(left_frame, text="VOICE CONTROLS", style='Dark.TLabel', font=('JetBrains Mono', 12, 'bold'))
        controls_label.pack(pady=(0, 10))
        
        # Voice enabled checkbox
        self.voice_enabled_var = tk.BooleanVar(value=True)
        voice_check = ttk.Checkbutton(left_frame, text="Voice Enabled", variable=self.voice_enabled_var)
        voice_check.pack(anchor=tk.W, pady=2)
        
        # Generation frequency
        ttk.Label(left_frame, text="Generation Frequency:", style='Dark.TLabel').pack(anchor=tk.W)
        self.voice_freq_var = tk.DoubleVar(value=0.5)
        freq_scale = ttk.Scale(left_frame, from_=0.1, to=2.0, variable=self.voice_freq_var, orient=tk.HORIZONTAL)
        freq_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Word count target
        ttk.Label(left_frame, text="Word Count Target:", style='Dark.TLabel').pack(anchor=tk.W)
        self.word_count_var = tk.IntVar(value=8)
        word_spin = ttk.Spinbox(left_frame, from_=3, to=20, textvariable=self.word_count_var)
        word_spin.pack(fill=tk.X, pady=(0, 10))
        
        # Comprehensibility threshold
        ttk.Label(left_frame, text="Quality Threshold:", style='Dark.TLabel').pack(anchor=tk.W)
        self.quality_var = tk.DoubleVar(value=0.7)
        quality_scale = ttk.Scale(left_frame, from_=0.0, to=1.0, variable=self.quality_var, orient=tk.HORIZONTAL)
        quality_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Action buttons
        ttk.Button(left_frame, text="Generate Voice Now", 
                  command=self.generate_voice_now, style='Dark.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(left_frame, text="Export Voice History", 
                  command=self.export_voice_history, style='Dark.TButton').pack(fill=tk.X, pady=2)
        
        # Center panel - Voice output display
        center_frame = ttk.Frame(voice_paned, style='Dark.TFrame')
        voice_paned.add(center_frame, weight=50)
        
        display_label = ttk.Label(center_frame, text="VOICE OUTPUT", style='Dark.TLabel', font=('JetBrains Mono', 12, 'bold'))
        display_label.pack(pady=(0, 10))
        
        # Current utterance display
        utterance_frame = ttk.LabelFrame(center_frame, text="Current Utterance", style='Dark.TFrame')
        utterance_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.current_utterance = tk.Text(utterance_frame, bg="#1a1a1a", fg="#cccccc", 
                                       font=("JetBrains Mono", 14), height=4, wrap=tk.WORD)
        self.current_utterance.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Utterance history
        history_frame = ttk.LabelFrame(center_frame, text="Utterance History", style='Dark.TFrame')
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.utterance_history = tk.Listbox(history_frame, bg="#1a1a1a", fg="#cccccc", 
                                          font=("JetBrains Mono", 10))
        history_scroll = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.utterance_history.yview)
        self.utterance_history.configure(yscrollcommand=history_scroll.set)
        
        self.utterance_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Right panel - Pigment visualization
        right_frame = ttk.Frame(voice_paned, style='Dark.TFrame')
        voice_paned.add(right_frame, weight=25)
        
        pigment_label = ttk.Label(right_frame, text="PIGMENT STATE", style='Dark.TLabel', font=('JetBrains Mono', 12, 'bold'))
        pigment_label.pack(pady=(0, 10))
        
        # Pigment level displays
        self.pigment_bars = {}
        for color in ["Red", "Green", "Blue", "Yellow", "Violet", "Orange"]:
            self.create_pigment_bar(right_frame, color)
        
        # Dominant pigment display
        dominant_frame = ttk.Frame(right_frame, style='Dark.TFrame')
        dominant_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(dominant_frame, text="Dominant:", style='Dark.TLabel').pack()
        self.dominant_pigment = ttk.Label(dominant_frame, text="NEUTRAL", style='Dark.TLabel', 
                                        font=('JetBrains Mono', 12, 'bold'))
        self.dominant_pigment.pack()
        
    def create_state_monitor_tab(self):
        """Create the State Monitor tab for real-time DAWN status"""
        self.state_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.state_tab, text="📊 State Monitor")
        
        # Main grid layout
        state_grid = ttk.Frame(self.state_tab, style='Dark.TFrame')
        state_grid.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top row - Main gauges
        top_frame = ttk.Frame(state_grid, style='Dark.TFrame')
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Entropy gauge
        entropy_frame = ttk.LabelFrame(top_frame, text="Entropy Level", style='Dark.TFrame')
        entropy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.entropy_canvas = tk.Canvas(entropy_frame, bg="#1a1a1a", height=120)
        self.entropy_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # SCUP gauge
        scup_frame = ttk.LabelFrame(top_frame, text="SCUP Level", style='Dark.TFrame')
        scup_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.scup_canvas = tk.Canvas(scup_frame, bg="#1a1a1a", height=120)
        self.scup_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Drift compass
        drift_frame = ttk.LabelFrame(top_frame, text="Drift Vector", style='Dark.TFrame')
        drift_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.drift_canvas = tk.Canvas(drift_frame, bg="#1a1a1a", height=120)
        self.drift_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Middle row - System status
        middle_frame = ttk.Frame(state_grid, style='Dark.TFrame')
        middle_frame.pack(fill=tk.X, pady=10)
        
        # Connection status
        conn_frame = ttk.LabelFrame(middle_frame, text="System Status", style='Dark.TFrame')
        conn_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.connection_status = ttk.Label(conn_frame, text="● Disconnected", style='Dark.TLabel', 
                                         font=('JetBrains Mono', 11, 'bold'))
        self.connection_status.pack(pady=5)
        
        self.uptime_label = ttk.Label(conn_frame, text="Uptime: 00:00:00", style='Dark.TLabel')
        self.uptime_label.pack(pady=2)
        
        self.thermal_zone_label = ttk.Label(conn_frame, text="Zone: CALM", style='Dark.TLabel')
        self.thermal_zone_label.pack(pady=2)
        
        # Expression frequency
        expr_frame = ttk.LabelFrame(middle_frame, text="Expression Rate", style='Dark.TFrame')
        expr_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.expr_rate_label = ttk.Label(expr_frame, text="0.0 expr/min", style='Dark.TLabel', 
                                       font=('JetBrains Mono', 14, 'bold'))
        self.expr_rate_label.pack(pady=10)
        
        # Cognitive load
        load_frame = ttk.LabelFrame(middle_frame, text="Cognitive Load", style='Dark.TFrame')
        load_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.load_canvas = tk.Canvas(load_frame, bg="#1a1a1a", height=60)
        self.load_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bottom row - Time series charts
        charts_frame = ttk.LabelFrame(state_grid, text="Historical Data", style='Dark.TFrame')
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Simple time series placeholder
        self.history_canvas = tk.Canvas(charts_frame, bg="#1a1a1a")
        self.history_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def create_controls_tab(self):
        """Create the Controls tab for system configuration"""
        self.controls_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.controls_tab, text="⚙️ Controls")
        
        # Three column layout
        controls_paned = ttk.PanedWindow(self.controls_tab, orient=tk.HORIZONTAL)
        controls_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - System controls
        left_frame = ttk.Frame(controls_paned, style='Dark.TFrame')
        controls_paned.add(left_frame, weight=33)
        
        system_label = ttk.Label(left_frame, text="SYSTEM CONTROLS", style='Dark.TLabel', 
                               font=('JetBrains Mono', 12, 'bold'))
        system_label.pack(pady=(0, 10))
        
        # Autonomous mode
        self.autonomous_var = tk.BooleanVar(value=True)
        auto_check = ttk.Checkbutton(left_frame, text="Autonomous Mode", variable=self.autonomous_var)
        auto_check.pack(anchor=tk.W, pady=2)
        
        # Processing speed
        ttk.Label(left_frame, text="Processing Speed:", style='Dark.TLabel').pack(anchor=tk.W, pady=(10, 0))
        self.proc_speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(left_frame, from_=0.1, to=3.0, variable=self.proc_speed_var, orient=tk.HORIZONTAL)
        speed_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Archive mode
        ttk.Label(left_frame, text="Archive Mode:", style='Dark.TLabel').pack(anchor=tk.W)
        self.archive_mode_var = tk.StringVar(value="Basic")
        archive_combo = ttk.Combobox(left_frame, textvariable=self.archive_mode_var,
                                   values=["Off", "Basic", "Full"])
        archive_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Debug logging
        self.debug_var = tk.BooleanVar(value=False)
        debug_check = ttk.Checkbutton(left_frame, text="Debug Logging", variable=self.debug_var)
        debug_check.pack(anchor=tk.W, pady=2)
        
        # Center panel - Manual triggers
        center_frame = ttk.Frame(controls_paned, style='Dark.TFrame')
        controls_paned.add(center_frame, weight=34)
        
        triggers_label = ttk.Label(center_frame, text="MANUAL TRIGGERS", style='Dark.TLabel', 
                                 font=('JetBrains Mono', 12, 'bold'))
        triggers_label.pack(pady=(0, 10))
        
        # Trigger buttons
        ttk.Button(center_frame, text="Generate Expression", 
                  command=self.trigger_expression, style='Dark.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(center_frame, text="Force Sigil Execution", 
                  command=self.force_sigil, style='Dark.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(center_frame, text="Reset Entropy", 
                  command=self.reset_entropy, style='Dark.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(center_frame, text="Clear Pigment State", 
                  command=self.clear_pigments, style='Dark.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(center_frame, text="Export Current State", 
                  command=self.export_state, style='Dark.TButton').pack(fill=tk.X, pady=2)
        
        # Right panel - Advanced settings
        right_frame = ttk.Frame(controls_paned, style='Dark.TFrame')
        controls_paned.add(right_frame, weight=33)
        
        advanced_label = ttk.Label(right_frame, text="ADVANCED SETTINGS", style='Dark.TLabel', 
                                 font=('JetBrains Mono', 12, 'bold'))
        advanced_label.pack(pady=(0, 10))
        
        # Entropy sensitivity
        ttk.Label(right_frame, text="Entropy Sensitivity:", style='Dark.TLabel').pack(anchor=tk.W)
        self.entropy_sens_var = tk.DoubleVar(value=0.5)
        entropy_scale = ttk.Scale(right_frame, from_=0.1, to=1.0, variable=self.entropy_sens_var, orient=tk.HORIZONTAL)
        entropy_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Pigment decay rate
        ttk.Label(right_frame, text="Pigment Decay Rate:", style='Dark.TLabel').pack(anchor=tk.W)
        self.pigment_decay_var = tk.DoubleVar(value=0.1)
        decay_scale = ttk.Scale(right_frame, from_=0.01, to=0.5, variable=self.pigment_decay_var, orient=tk.HORIZONTAL)
        decay_scale.pack(fill=tk.X, pady=(0, 10))
        
        # Expression cooldown
        ttk.Label(right_frame, text="Expression Cooldown (s):", style='Dark.TLabel').pack(anchor=tk.W)
        self.cooldown_var = tk.IntVar(value=30)
        cooldown_spin = ttk.Spinbox(right_frame, from_=5, to=300, textvariable=self.cooldown_var)
        cooldown_spin.pack(fill=tk.X, pady=(0, 10))
        
    def create_archive_tab(self):
        """Create the Archive tab for expression history"""
        self.archive_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.archive_tab, text="📚 Archive")
        
        # Layout: left browser, right details
        archive_paned = ttk.PanedWindow(self.archive_tab, orient=tk.HORIZONTAL)
        archive_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Archive browser
        left_frame = ttk.Frame(archive_paned, style='Dark.TFrame')
        archive_paned.add(left_frame, weight=60)
        
        browser_label = ttk.Label(left_frame, text="EXPRESSION ARCHIVE", style='Dark.TLabel', 
                                font=('JetBrains Mono', 12, 'bold'))
        browser_label.pack(pady=(0, 10))
        
        # Search and filters
        filter_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Search:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        
        ttk.Label(filter_frame, text="Type:", style='Dark.TLabel').pack(side=tk.LEFT)
        self.type_filter_var = tk.StringVar(value="All")
        type_combo = ttk.Combobox(filter_frame, textvariable=self.type_filter_var,
                                values=["All", "Voice", "Visual", "Combined"], width=10)
        type_combo.pack(side=tk.RIGHT)
        
        # Expression list
        list_frame = ttk.Frame(left_frame, style='Dark.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.expression_tree = ttk.Treeview(list_frame, columns=("time", "type", "content"), show="tree headings")
        self.expression_tree.heading("#0", text="ID")
        self.expression_tree.heading("time", text="Time")
        self.expression_tree.heading("type", text="Type")
        self.expression_tree.heading("content", text="Content")
        
        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.expression_tree.yview)
        self.expression_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.expression_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Expression details
        right_frame = ttk.Frame(archive_paned, style='Dark.TFrame')
        archive_paned.add(right_frame, weight=40)
        
        details_label = ttk.Label(right_frame, text="EXPRESSION DETAILS", style='Dark.TLabel', 
                                font=('JetBrains Mono', 12, 'bold'))
        details_label.pack(pady=(0, 10))
        
        # Details display
        self.details_text = tk.Text(right_frame, bg="#1a1a1a", fg="#cccccc", 
                                  font=("JetBrains Mono", 10), wrap=tk.WORD)
        details_scroll = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scroll.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        details_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Archive actions at bottom
        actions_frame = ttk.Frame(right_frame, style='Dark.TFrame')
        actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(actions_frame, text="Export Selected", 
                  command=self.export_selected_expressions, style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Generate Report", 
                  command=self.generate_archive_report, style='Dark.TButton').pack(side=tk.LEFT)
        
    def create_logs_tab(self):
        """Create the Logs tab for system logging"""
        self.logs_tab = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(self.logs_tab, text="📋 Logs")
        
        # Layout: main log display with sidebar controls
        logs_paned = ttk.PanedWindow(self.logs_tab, orient=tk.HORIZONTAL)
        logs_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Main log display
        main_frame = ttk.Frame(logs_paned, style='Dark.TFrame')
        logs_paned.add(main_frame, weight=75)
        
        log_label = ttk.Label(main_frame, text="SYSTEM LOGS", style='Dark.TLabel', 
                            font=('JetBrains Mono', 12, 'bold'))
        log_label.pack(pady=(0, 10))
        
        # Log viewer
        log_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_viewer = tk.Text(log_frame, bg="#1a1a1a", fg="#cccccc", 
                                font=("JetBrains Mono", 9), wrap=tk.WORD)
        log_scroll = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_viewer.yview)
        self.log_viewer.configure(yscrollcommand=log_scroll.set)
        
        self.log_viewer.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Sidebar controls
        controls_frame = ttk.Frame(logs_paned, style='Dark.TFrame')
        logs_paned.add(controls_frame, weight=25)
        
        controls_label = ttk.Label(controls_frame, text="LOG CONTROLS", style='Dark.TLabel', 
                                 font=('JetBrains Mono', 12, 'bold'))
        controls_label.pack(pady=(0, 10))
        
        # Log level filter
        ttk.Label(controls_frame, text="Log Level:", style='Dark.TLabel').pack(anchor=tk.W)
        self.log_level_var = tk.StringVar(value="INFO")
        level_combo = ttk.Combobox(controls_frame, textvariable=self.log_level_var,
                                 values=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        level_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Component filters
        ttk.Label(controls_frame, text="Components:", style='Dark.TLabel').pack(anchor=tk.W)
        
        self.component_vars = {}
        for component in ["Voice", "Visual", "State", "Pigment", "Tick"]:
            var = tk.BooleanVar(value=True)
            self.component_vars[component] = var
            ttk.Checkbutton(controls_frame, text=component, variable=var).pack(anchor=tk.W)
        
        # Auto-scroll
        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(controls_frame, text="Auto-scroll", variable=self.auto_scroll_var).pack(anchor=tk.W, pady=(10, 0))
        
        # Control buttons
        ttk.Button(controls_frame, text="Clear Logs", 
                  command=self.clear_logs, style='Dark.TButton').pack(fill=tk.X, pady=(10, 2))
        ttk.Button(controls_frame, text="Export Logs", 
                  command=self.export_logs, style='Dark.TButton').pack(fill=tk.X, pady=2)
        ttk.Button(controls_frame, text="Pause Logging", 
                  command=self.toggle_logging, style='Dark.TButton').pack(fill=tk.X, pady=2)
        
    def create_parameter_display(self, parent, label, name):
        """Create a parameter display widget"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text=f"{label}:", style='Dark.TLabel').pack(anchor=tk.W)
        
        if "bar" in name:
            # Progress bar for numeric values
            progress = ttk.Progressbar(frame, length=150, mode='determinate')
            progress.pack(fill=tk.X)
            setattr(self, name, progress)
        else:
            # Text display for complex values
            display = ttk.Label(frame, text="0.0 + 0.0i", style='Dark.TLabel', 
                              font=('JetBrains Mono', 9))
            display.pack()
            setattr(self, name, display)
    
    def create_pigment_bar(self, parent, color):
        """Create a pigment level bar"""
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill=tk.X, pady=2)
        
        label = ttk.Label(frame, text=f"{color}:", style='Dark.TLabel', width=8)
        label.pack(side=tk.LEFT)
        
        bar = ttk.Progressbar(frame, length=100, mode='determinate')
        bar.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        self.pigment_bars[color.lower()] = bar
    
    def setup_backend_connection(self):
        """Initialize connection to DAWN backend systems"""
        try:
            # Initialize DAWN components if available
            if TickEngine:
                self.tick_engine = TickEngine()
                self.log_message("INFO", "TickEngine initialized")
            else:
                self.log_message("WARNING", "TickEngine not available - running in simulation mode")
            
            if VoiceMoodModulator:
                self.voice_modulator = VoiceMoodModulator()
                self.log_message("INFO", "VoiceMoodModulator initialized")
            else:
                self.log_message("WARNING", "VoiceMoodModulator not available")
            
            if PlatonicPigmentMap:
                self.pigment_map = PlatonicPigmentMap()
                self.log_message("INFO", "PlatonicPigmentMap initialized")
            else:
                self.log_message("WARNING", "PlatonicPigmentMap not available")
            
            # Start WebSocket server for real-time communication
            self.start_websocket_server()
            
            self.log_message("INFO", "Backend connection established (some components may be simulated)")
            self.current_state["is_connected"] = True
            
        except Exception as e:
            self.log_message("ERROR", f"Backend connection failed: {e}")
            self.current_state["is_connected"] = False
    
    def start_websocket_server(self):
        """Start WebSocket server for real-time data"""
        try:
            # This would start the WebSocket server in a separate thread
            # For now, we'll simulate data updates
            pass
        except Exception as e:
            self.log_message("ERROR", f"WebSocket server failed: {e}")
    
    def start_update_threads(self):
        """Start background threads for real-time updates"""
        # State update thread
        state_thread = threading.Thread(target=self.state_update_loop, daemon=True)
        state_thread.start()
        
        # GUI update thread
        self.root.after(100, self.update_gui)
    
    def state_update_loop(self):
        """Background loop for state updates"""
        while True:
            try:
                # Simulate state updates (replace with real DAWN state)
                self.simulate_state_update()
                time.sleep(1.0)
            except Exception as e:
                self.log_message("ERROR", f"State update error: {e}")
    
    def simulate_state_update(self):
        """Simulate DAWN state updates for demo"""
        import random
        
        # Update entropy with some randomness
        self.current_state["entropy"] = max(0.0, min(1.0, 
            self.current_state["entropy"] + random.uniform(-0.05, 0.05)))
        
        # Update SCUP
        self.current_state["scup"] = max(0.0, min(100.0,
            self.current_state["scup"] + random.uniform(-2.0, 2.0)))
        
        # Update pigments
        for color in self.current_state["pigments"]:
            self.current_state["pigments"][color] = max(0.0, min(1.0,
                self.current_state["pigments"][color] + random.uniform(-0.02, 0.02)))
        
        # Update uptime
        self.current_state["uptime"] += 1
        
        # Put state in queue for GUI update
        self.state_queue.put(self.current_state.copy())
    
    def update_gui(self):
        """Update GUI elements with latest data"""
        try:
            # Process state updates
            while not self.state_queue.empty():
                state = self.state_queue.get_nowait()
                self.update_state_displays(state)
            
            # Process voice updates
            while not self.voice_queue.empty():
                voice_data = self.voice_queue.get_nowait()
                self.update_voice_displays(voice_data)
            
            # Process visual updates
            while not self.visual_queue.empty():
                visual_data = self.visual_queue.get_nowait()
                self.update_visual_displays(visual_data)
            
            # Process log updates
            while not self.log_queue.empty():
                log_data = self.log_queue.get_nowait()
                self.update_log_display(log_data)
                
        except Exception as e:
            print(f"GUI update error: {e}")
        
        # Schedule next update
        self.root.after(100, self.update_gui)
    
    def update_state_displays(self, state):
        """Update state monitoring displays"""
        try:
            # Update connection status
            if state.get("is_connected", False):
                self.connection_status.configure(text="● Connected", foreground="#40e0ff")
            else:
                self.connection_status.configure(text="● Disconnected", foreground="#ff4040")
            
            # Update uptime
            uptime_seconds = state.get("uptime", 0)
            hours = uptime_seconds // 3600
            minutes = (uptime_seconds % 3600) // 60
            seconds = uptime_seconds % 60
            self.uptime_label.configure(text=f"Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
            
            # Update thermal zone
            zone = state.get("thermal_zone", "CALM")
            self.thermal_zone_label.configure(text=f"Zone: {zone}")
            
            # Update parameter bars in visual tab
            if hasattr(self, 'entropy_bar'):
                self.entropy_bar['value'] = state.get("entropy", 0.0) * 100
            
            if hasattr(self, 'mood_bar'):
                # Convert mood to numeric value for display
                mood_values = {"CALM": 20, "NEUTRAL": 50, "EXCITED": 80, "ANXIOUS": 90}
                mood_val = mood_values.get(state.get("mood", "NEUTRAL"), 50)
                self.mood_bar['value'] = mood_val
            
            # Update pigment bars
            pigments = state.get("pigments", {})
            for color, value in pigments.items():
                if color in self.pigment_bars:
                    self.pigment_bars[color]['value'] = value * 100
            
            # Update dominant pigment
            if pigments:
                dominant = max(pigments.keys(), key=lambda k: pigments[k])
                self.dominant_pigment.configure(text=dominant.upper())
            
            # Update gauges in state monitor
            self.draw_entropy_gauge(state.get("entropy", 0.0))
            self.draw_scup_gauge(state.get("scup", 50.0))
            self.draw_drift_compass(state.get("drift_vector", [0.0, 0.0]))
            
        except Exception as e:
            self.log_message("ERROR", f"State display update error: {e}")
    
    def update_voice_displays(self, voice_data):
        """Update voice tab displays"""
        try:
            utterance = voice_data.get("utterance", "")
            timestamp = voice_data.get("timestamp", datetime.now().strftime("%H:%M:%S"))
            
            # Update current utterance
            self.current_utterance.delete(1.0, tk.END)
            self.current_utterance.insert(1.0, utterance)
            
            # Add to history
            history_entry = f"[{timestamp}] {utterance}"
            self.utterance_history.insert(tk.END, history_entry)
            self.utterance_history.see(tk.END)
            
        except Exception as e:
            self.log_message("ERROR", f"Voice display update error: {e}")
    
    def update_visual_displays(self, visual_data):
        """Update visual tab displays"""
        try:
            # Update fractal display if available
            if self.fractal_canvas and visual_data.get("type") == "fractal":
                bloom_data = visual_data.get("data", {})
                self.fractal_canvas.draw_bloom_signature(bloom_data)
            
        except Exception as e:
            self.log_message("ERROR", f"Visual display update error: {e}")
    
    def update_log_display(self, log_data):
        """Update log display"""
        try:
            timestamp = log_data.get("timestamp", datetime.now().strftime("%H:%M:%S.%f")[:-3])
            level = log_data.get("level", "INFO")
            component = log_data.get("component", "System")
            message = log_data.get("message", "")
            
            # Check if component is enabled
            if component in self.component_vars:
                if not self.component_vars[component].get():
                    return
            
            # Check log level filter
            level_priority = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3, "CRITICAL": 4}
            current_level = self.log_level_var.get()
            if level_priority.get(level, 1) < level_priority.get(current_level, 1):
                return
            
            # Format log entry
            log_entry = f"[{timestamp}] [{level}] [{component}] {message}\n"
            
            # Add to log viewer
            self.log_viewer.insert(tk.END, log_entry)
            
            # Auto-scroll if enabled
            if self.auto_scroll_var.get():
                self.log_viewer.see(tk.END)
            
            # Limit log size (keep last 1000 lines)
            lines = int(self.log_viewer.index(tk.END).split('.')[0])
            if lines > 1000:
                self.log_viewer.delete(1.0, f"{lines-1000}.0")
            
        except Exception as e:
            print(f"Log display update error: {e}")
    
    def draw_entropy_gauge(self, entropy_value):
        """Draw entropy gauge in state monitor"""
        try:
            self.entropy_canvas.delete("all")
            width = self.entropy_canvas.winfo_width()
            height = self.entropy_canvas.winfo_height()
            
            if width <= 1 or height <= 1:
                return
            
            # Draw gauge background
            center_x, center_y = width // 2, height // 2
            radius = min(width, height) // 2 - 10
            
            self.entropy_canvas.create_oval(center_x - radius, center_y - radius,
                                          center_x + radius, center_y + radius,
                                          outline="#333333", width=2)
            
            # Draw entropy level
            angle = entropy_value * 180  # 0-180 degrees
            end_x = center_x + radius * 0.8 * math.cos(math.radians(180 - angle))
            end_y = center_y - radius * 0.8 * math.sin(math.radians(180 - angle))
            
            color = "#40e0ff" if entropy_value < 0.7 else "#ff4040"
            self.entropy_canvas.create_line(center_x, center_y, end_x, end_y,
                                          fill=color, width=3)
            
            # Draw value text
            self.entropy_canvas.create_text(center_x, center_y + radius // 2,
                                          text=f"{entropy_value:.2f}",
                                          fill="#cccccc", font=("JetBrains Mono", 10))
            
        except Exception as e:
            pass  # Ignore drawing errors during resize
    
    def draw_scup_gauge(self, scup_value):
        """Draw SCUP gauge in state monitor"""
        try:
            self.scup_canvas.delete("all")
            width = self.scup_canvas.winfo_width()
            height = self.scup_canvas.winfo_height()
            
            if width <= 1 or height <= 1:
                return
            
            # Draw gauge as horizontal bar
            bar_width = width - 20
            bar_height = 20
            bar_x = 10
            bar_y = height // 2 - bar_height // 2
            
            # Background
            self.scup_canvas.create_rectangle(bar_x, bar_y, bar_x + bar_width, bar_y + bar_height,
                                            outline="#333333", fill="#1a1a1a")
            
            # Fill level
            fill_width = (scup_value / 100.0) * bar_width
            color = "#40e0ff" if scup_value < 80 else "#ff4040"
            self.scup_canvas.create_rectangle(bar_x, bar_y, bar_x + fill_width, bar_y + bar_height,
                                            fill=color, outline="")
            
            # Value text
            self.scup_canvas.create_text(width // 2, bar_y + bar_height + 15,
                                       text=f"{scup_value:.1f}",
                                       fill="#cccccc", font=("JetBrains Mono", 10))
            
        except Exception as e:
            pass
    
    def draw_drift_compass(self, drift_vector):
        """Draw drift compass in state monitor"""
        try:
            self.drift_canvas.delete("all")
            width = self.drift_canvas.winfo_width()
            height = self.drift_canvas.winfo_height()
            
            if width <= 1 or height <= 1:
                return
            
            center_x, center_y = width // 2, height // 2
            radius = min(width, height) // 2 - 10
            
            # Draw compass circle
            self.drift_canvas.create_oval(center_x - radius, center_y - radius,
                                        center_x + radius, center_y + radius,
                                        outline="#333333", width=2)
            
            # Draw drift vector
            if len(drift_vector) >= 2:
                dx, dy = drift_vector[0], drift_vector[1]
                # Scale vector to fit in compass
                magnitude = (dx*dx + dy*dy) ** 0.5
                if magnitude > 0:
                    scale = radius * 0.8 / max(1.0, magnitude)
                    end_x = center_x + dx * scale
                    end_y = center_y + dy * scale
                    
                    self.drift_canvas.create_line(center_x, center_y, end_x, end_y,
                                                fill="#40e0ff", width=2, arrow=tk.LAST)
            
            # Draw center dot
            self.drift_canvas.create_oval(center_x - 2, center_y - 2,
                                        center_x + 2, center_y + 2,
                                        fill="#cccccc", outline="")
            
        except Exception as e:
            pass
    
    def log_message(self, level, message, component="System"):
        """Add a log message"""
        log_data = {
            "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:-3],
            "level": level,
            "component": component,
            "message": message
        }
        self.log_queue.put(log_data)
    
    # Button callback methods
    def generate_new_fractal(self):
        """Generate a new fractal"""
        self.log_message("INFO", "Generating new fractal", "Visual")
        # Trigger fractal generation
        if self.fractal_canvas:
            bloom_data = {
                "depth": 3,
                "entropy": self.current_state.get("entropy", 0.5),
                "lineage": [1, 2, 3],
                "semantic_drift": 0.3,
                "rebloom_status": "active",
                "complexity": 0.6
            }
            visual_data = {"type": "fractal", "data": bloom_data}
            self.visual_queue.put(visual_data)
    
    def save_current_visual(self):
        """Save current visual"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.log_message("INFO", f"Saving visual to {filename}", "Visual")
    
    def export_animation(self):
        """Export animation sequence"""
        self.log_message("INFO", "Exporting animation sequence", "Visual")
        messagebox.showinfo("Export", "Animation export functionality not yet implemented")
    
    def generate_voice_now(self):
        """Generate voice utterance now"""
        self.log_message("INFO", "Generating voice utterance", "Voice")
        # Simulate voice generation
        import random
        utterances = [
            "The entropy flows through consciousness like water through stone",
            "Pigments dance in the cognitive space, painting thoughts with emotion",
            "Each tick brings new possibilities, new ways of being",
            "The drift carries us toward unknown territories of mind",
            "In the space between thoughts, wisdom grows"
        ]
        utterance = random.choice(utterances)
        voice_data = {
            "utterance": utterance,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.voice_queue.put(voice_data)
    
    def export_voice_history(self):
        """Export voice history"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.log_message("INFO", f"Exporting voice history to {filename}", "Voice")
    
    def trigger_expression(self):
        """Trigger manual expression"""
        self.log_message("INFO", "Manual expression triggered", "Controls")
        self.generate_voice_now()
        self.generate_new_fractal()
    
    def force_sigil(self):
        """Force sigil execution"""
        self.log_message("INFO", "Forcing sigil execution", "Controls")
    
    def reset_entropy(self):
        """Reset entropy to neutral"""
        self.log_message("INFO", "Resetting entropy to neutral", "Controls")
        self.current_state["entropy"] = 0.5
    
    def clear_pigments(self):
        """Clear pigment state"""
        self.log_message("INFO", "Clearing pigment state", "Controls")
        for color in self.current_state["pigments"]:
            self.current_state["pigments"][color] = 0.3
    
    def export_state(self):
        """Export current state"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.current_state, f, indent=2)
                self.log_message("INFO", f"State exported to {filename}", "Controls")
            except Exception as e:
                self.log_message("ERROR", f"Failed to export state: {e}", "Controls")
    
    def export_selected_expressions(self):
        """Export selected expressions"""
        self.log_message("INFO", "Exporting selected expressions", "Archive")
    
    def generate_archive_report(self):
        """Generate archive report"""
        self.log_message("INFO", "Generating archive report", "Archive")
    
    def clear_logs(self):
        """Clear log display"""
        self.log_viewer.delete(1.0, tk.END)
        self.log_message("INFO", "Log display cleared", "Logs")
    
    def export_logs(self):
        """Export logs to file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.log_viewer.get(1.0, tk.END))
                self.log_message("INFO", f"Logs exported to {filename}", "Logs")
            except Exception as e:
                self.log_message("ERROR", f"Failed to export logs: {e}", "Logs")
    
    def toggle_logging(self):
        """Toggle logging on/off"""
        # This would pause/resume logging
        self.log_message("INFO", "Logging toggle not implemented", "Logs")
    
    def run(self):
        """Start the GUI application"""
        self.log_message("INFO", "DAWN Consolidated GUI started")
        self.root.mainloop()


def main():
    """Main entry point"""
    print("🌅 DAWN Consolidated GUI")
    print("=" * 50)
    print("🚀 Starting unified interface...")
    
    try:
        app = DAWNConsolidatedGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 