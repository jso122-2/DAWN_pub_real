#!/usr/bin/env python3
"""
DAWN Forecast Dashboard - Real-time Cognitive State Visualizer
Live GUI showing DAWN's entropy, forecasts, pulse zones, and symbolic states.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import json
import math
from datetime import datetime
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Import DAWN systems
try:
    from dawn_core.main import create_dawn_engine
    from dawn_core.snapshot_exporter import DAWNSnapshotExporter
    # Import SCUP optimizer for intelligent monitoring
    from core.scup_logger_optimizer import get_scup_status
    DAWN_AVAILABLE = True
except ImportError:
    DAWN_AVAILABLE = False
    # Fallback function if SCUP optimizer not available
    def get_scup_status():
        return {'last_scup': 0.0, 'current_zone': 'minimal'}


class DAWNForecastDashboard:
    """
    Real-time GUI dashboard for DAWN cognitive state monitoring.
    """
    
    def __init__(self):
        """Initialize the dashboard."""
        self.root = tk.Tk()
        self.root.title("DAWN Cognitive Dashboard")
        self.root.geometry("1200x800")  # Increased size for new components
        self.root.configure(bg='#1a1a1a')
        
        # Color scheme
        self.colors = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'accent': '#00ff88',
            'warning': '#ffaa00', 
            'critical': '#ff4444',
            'calm': '#4488ff',
            'active': '#88ff44',
            'chaotic': '#ff8844',
            'scup_low': '#4488ff',      # Blue for low SCUP
            'scup_high': '#8844ff',     # Violet for high SCUP
            'heat_cool': '#44ccff',     # Cool blue
            'heat_warm': '#ffaa44',     # Warm orange
            'heat_hot': '#ff4444'       # Hot red
        }
        
        # State tracking
        self.running = False
        self.engine = None
        self.exporter = None
        self.last_update = None
        
        # Visual component references
        self.scup_canvas = None
        self.heat_canvas = None
        self.current_scup = 0.0
        self.current_heat = 25.0
        
        # Ensure runtime directories exist
        runtime_dir = Path("runtime")
        runtime_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize DAWN engine if available
        if DAWN_AVAILABLE:
            try:
                self.engine = create_dawn_engine()
                self.exporter = DAWNSnapshotExporter(dawn_engine=self.engine)
            except Exception as e:
                print(f"⚠️ DAWN engine initialization failed: {e}")
        
        # Setup GUI
        self.setup_gui()
        
        # Start update loop
        self.start_updates()
    
    def setup_gui(self):
        """Setup the GUI layout and widgets."""
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🧠 DAWN Cognitive Dashboard",
            font=('Consolas', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        title_label.pack(pady=(0, 20))
        
        # Create main sections
        self.setup_metrics_section(main_frame)
        self.setup_visual_meters_section(main_frame)  # New visual components
        self.setup_forecast_section(main_frame)
        self.setup_symbolic_section(main_frame)
        self.setup_commentary_section(main_frame)
        self.setup_controls_section(main_frame)
    
    def setup_metrics_section(self, parent):
        """Setup the system metrics section."""
        metrics_frame = tk.LabelFrame(
            parent,
            text="System Metrics",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2,
            relief='groove'
        )
        metrics_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Metrics grid
        metrics_grid = tk.Frame(metrics_frame, bg=self.colors['bg'])
        metrics_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Entropy
        self.entropy_label = tk.Label(
            metrics_grid,
            text="Entropy: 0.00",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.entropy_label.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        self.entropy_bar = ttk.Progressbar(
            metrics_grid,
            length=200,
            mode='determinate'
        )
        self.entropy_bar.grid(row=0, column=1, padx=(0, 20))
        
        # Heat
        self.heat_label = tk.Label(
            metrics_grid,
            text="Heat: 25.0°",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.heat_label.grid(row=0, column=2, sticky='w', padx=(0, 20))
        
        self.heat_bar = ttk.Progressbar(
            metrics_grid,
            length=200,
            mode='determinate'
        )
        self.heat_bar.grid(row=0, column=3)
        
        # SCUP (new)
        self.scup_label = tk.Label(
            metrics_grid,
            text="SCUP: 0.0",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.scup_label.grid(row=1, column=0, sticky='w', padx=(0, 20), pady=(10, 0))
        
        self.scup_bar = ttk.Progressbar(
            metrics_grid,
            length=200,
            mode='determinate'
        )
        self.scup_bar.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        
        # Zone status
        self.zone_label = tk.Label(
            metrics_grid,
            text="Zone: CALM",
            font=('Consolas', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['calm']
        )
        self.zone_label.grid(row=1, column=2, sticky='w', pady=(10, 0))
        
        # Tick count
        self.tick_label = tk.Label(
            metrics_grid,
            text="Ticks: 0",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.tick_label.grid(row=1, column=3, sticky='w', pady=(10, 0))

    def setup_visual_meters_section(self, parent):
        """Setup the new visual meters section with SCUP bar and Heat arc."""
        visual_frame = tk.LabelFrame(
            parent,
            text="Live Visual Meters",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2,
            relief='groove'
        )
        visual_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Visual components container
        visual_container = tk.Frame(visual_frame, bg=self.colors['bg'])
        visual_container.pack(fill=tk.X, padx=20, pady=15)
        
        # SCUP Bar (left side)
        scup_frame = tk.Frame(visual_container, bg=self.colors['bg'])
        scup_frame.pack(side=tk.LEFT, padx=(0, 40))
        
        scup_title = tk.Label(
            scup_frame,
            text="SCUP (Semantic Coherence Under Pressure)",
            font=('Consolas', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        scup_title.pack(pady=(0, 5))
        
        # SCUP Canvas - Vertical bar
        self.scup_canvas = tk.Canvas(
            scup_frame,
            width=60,
            height=200,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.scup_canvas.pack()
        
        # SCUP value label
        self.scup_value_label = tk.Label(
            scup_frame,
            text="0.0",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.scup_value_label.pack(pady=(5, 0))
        
        # Heat Arc (right side)
        heat_frame = tk.Frame(visual_container, bg=self.colors['bg'])
        heat_frame.pack(side=tk.LEFT, padx=(40, 0))
        
        heat_title = tk.Label(
            heat_frame,
            text="Thermal Pressure",
            font=('Consolas', 10, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        heat_title.pack(pady=(0, 5))
        
        # Heat Canvas - Circular arc
        self.heat_canvas = tk.Canvas(
            heat_frame,
            width=200,
            height=200,
            bg=self.colors['bg'],
            highlightthickness=0
        )
        self.heat_canvas.pack()
        
        # Heat value label
        self.heat_value_label = tk.Label(
            heat_frame,
            text="25.0°C",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.heat_value_label.pack(pady=(5, 0))
        
        # Initialize the visual components
        self.draw_scup_bar(0.0)
        self.draw_heat_arc(25.0)

    def draw_scup_bar(self, scup_value):
        """Draw the SCUP vertical bar with blue-to-violet gradient."""
        if not self.scup_canvas:
            return
        
        self.scup_canvas.delete("all")
        
        # Canvas dimensions
        width = 60
        height = 200
        margin = 5
        bar_width = width - (2 * margin)
        bar_height = height - (2 * margin)
        
        # Background outline
        self.scup_canvas.create_rectangle(
            margin, margin, 
            width - margin, height - margin,
            outline=self.colors['fg'], 
            width=2,
            fill=''
        )
        
        # Normalize SCUP (assuming 0-100 range, but cap at 100)
        normalized_scup = min(max(scup_value, 0), 100) / 100.0
        fill_height = int(normalized_scup * bar_height)
        
        if fill_height > 0:
            # Create gradient effect by drawing multiple rectangles
            steps = max(1, fill_height // 2)
            for i in range(steps):
                # Calculate position from bottom
                y_bottom = height - margin - (i * 2)
                y_top = max(margin, y_bottom - 2)
                
                # Calculate color gradient from blue to violet
                ratio = i / max(1, steps - 1) if steps > 1 else 0
                
                # Interpolate between blue and violet
                r = int(0x44 + (0x88 - 0x44) * ratio)  # 44 to 88
                g = int(0x88 - (0x88 - 0x44) * ratio)  # 88 to 44  
                b = 0xff  # Keep blue component high
                
                color = f"#{r:02x}{g:02x}{b:02x}"
                
                if y_top < y_bottom:
                    self.scup_canvas.create_rectangle(
                        margin + 1, y_top,
                        width - margin - 1, y_bottom,
                        fill=color,
                        outline=""
                    )
        
        # Add scale markers
        for i in range(5):  # 0, 25, 50, 75, 100
            y = height - margin - (i * bar_height // 4)
            self.scup_canvas.create_line(
                width - margin, y,
                width - margin + 5, y,
                fill=self.colors['fg'],
                width=1
            )
            
            # Add scale labels
            if i % 2 == 0:  # Only label 0, 50, 100
                value = i * 25
                self.scup_canvas.create_text(
                    width + 15, y,
                    text=str(value),
                    fill=self.colors['fg'],
                    font=('Consolas', 8),
                    anchor='w'
                )

    def draw_heat_arc(self, heat_value):
        """Draw the Heat circular arc (0-100°C) that turns red above 80°C."""
        if not self.heat_canvas:
            return
        
        self.heat_canvas.delete("all")
        
        # Canvas dimensions
        size = 200
        center = size // 2
        radius = 80
        
        # Background circle
        self.heat_canvas.create_oval(
            center - radius, center - radius,
            center + radius, center + radius,
            outline=self.colors['fg'],
            width=2,
            fill=''
        )
        
        # Normalize heat (0-100°C)
        normalized_heat = min(max(heat_value, 0), 100) / 100.0
        
        # Calculate arc extent (270° total, starting from -45°)
        start_angle = -45  # Start from top-right
        arc_extent = normalized_heat * 270  # Up to 270° clockwise
        
        # Determine color based on temperature
        if heat_value >= 80:
            color = self.colors['heat_hot']  # Red
        elif heat_value >= 50:
            # Gradient from orange to red
            ratio = (heat_value - 50) / 30
            r = 0xff
            g = int(0xaa - (0xaa - 0x44) * ratio)  # aa to 44
            b = int(0x44 * (1 - ratio))  # 44 to 00
            color = f"#{r:02x}{g:02x}{b:02x}"
        else:
            # Gradient from blue to orange
            ratio = heat_value / 50
            r = int(0x44 + (0xff - 0x44) * ratio)  # 44 to ff
            g = int(0xcc - (0xcc - 0xaa) * ratio)  # cc to aa
            b = int(0xff - (0xff - 0x44) * ratio)  # ff to 44
            color = f"#{r:02x}{g:02x}{b:02x}"
        
        # Draw the arc
        if arc_extent > 0:
            # Create arc by drawing a pie slice
            arc_radius = radius - 10
            self.heat_canvas.create_arc(
                center - arc_radius, center - arc_radius,
                center + arc_radius, center + arc_radius,
                start=start_angle,
                extent=arc_extent,
                fill=color,
                outline=color,
                width=15,
                style='arc'
            )
        
        # Add temperature markers
        for temp in [0, 25, 50, 75, 100]:
            angle_deg = -45 + (temp / 100) * 270
            angle_rad = math.radians(angle_deg)
            
            # Outer point
            x_outer = center + (radius + 5) * math.cos(angle_rad)
            y_outer = center + (radius + 5) * math.sin(angle_rad)
            
            # Inner point
            x_inner = center + (radius - 5) * math.cos(angle_rad)
            y_inner = center + (radius - 5) * math.sin(angle_rad)
            
            self.heat_canvas.create_line(
                x_inner, y_inner, x_outer, y_outer,
                fill=self.colors['fg'],
                width=2
            )
            
            # Add temperature labels
            if temp % 25 == 0:  # Label every 25°
                x_label = center + (radius + 20) * math.cos(angle_rad)
                y_label = center + (radius + 20) * math.sin(angle_rad)
                
                self.heat_canvas.create_text(
                    x_label, y_label,
                    text=f"{temp}°",
                    fill=self.colors['fg'],
                    font=('Consolas', 9),
                    anchor='center'
                )
        
        # Center label
        self.heat_canvas.create_text(
            center, center,
            text="THERMAL",
            fill=self.colors['fg'],
            font=('Consolas', 10, 'bold'),
            anchor='center'
        )
    
    def setup_forecast_section(self, parent):
        """Setup the forecast section."""
        forecast_frame = tk.LabelFrame(
            parent,
            text="Cognitive Forecast",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2,
            relief='groove'
        )
        forecast_frame.pack(fill=tk.X, pady=(0, 10))
        
        forecast_grid = tk.Frame(forecast_frame, bg=self.colors['bg'])
        forecast_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Confidence
        self.confidence_label = tk.Label(
            forecast_grid,
            text="Confidence: 0.50",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.confidence_label.grid(row=0, column=0, sticky='w', padx=(0, 20))
        
        self.confidence_bar = ttk.Progressbar(
            forecast_grid,
            length=200,
            mode='determinate'
        )
        self.confidence_bar.grid(row=0, column=1, padx=(0, 20))
        
        # Limit Horizon
        self.horizon_label = tk.Label(
            forecast_grid,
            text="Horizon: 0.50",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.horizon_label.grid(row=0, column=2, sticky='w', padx=(0, 20))
        
        self.horizon_bar = ttk.Progressbar(
            forecast_grid,
            length=200,
            mode='determinate'
        )
        self.horizon_bar.grid(row=0, column=3)
        
        # Risk Level
        self.risk_label = tk.Label(
            forecast_grid,
            text="Risk: 0.30",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.risk_label.grid(row=1, column=0, sticky='w', pady=(10, 0))
        
        self.risk_bar = ttk.Progressbar(
            forecast_grid,
            length=200,
            mode='determinate'
        )
        self.risk_bar.grid(row=1, column=1, pady=(10, 0))
        
        # Emotional Intensity
        self.emotion_label = tk.Label(
            forecast_grid,
            text="Emotion: 0.50",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.emotion_label.grid(row=1, column=2, sticky='w', pady=(10, 0))
        
        self.emotion_bar = ttk.Progressbar(
            forecast_grid,
            length=200,
            mode='determinate'
        )
        self.emotion_bar.grid(row=1, column=3, pady=(10, 0))
    
    def setup_symbolic_section(self, parent):
        """Setup the symbolic state section."""
        symbolic_frame = tk.LabelFrame(
            parent,
            text="Symbolic Anatomy",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2,
            relief='groove'
        )
        symbolic_frame.pack(fill=tk.X, pady=(0, 10))
        
        symbolic_grid = tk.Frame(symbolic_frame, bg=self.colors['bg'])
        symbolic_grid.pack(fill=tk.X, padx=10, pady=10)
        
        # Heart state
        self.heart_label = tk.Label(
            symbolic_grid,
            text="💗 Heart: gentle (0.50)",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.heart_label.grid(row=0, column=0, sticky='w', padx=(0, 30))
        
        # Coil state  
        self.coil_label = tk.Label(
            symbolic_grid,
            text="🌀 Coil: 2 paths (✨)",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.coil_label.grid(row=0, column=1, sticky='w', padx=(0, 30))
        
        # Lung state
        self.lung_label = tk.Label(
            symbolic_grid,
            text="🫁 Lung: inhaling (0.60)",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.lung_label.grid(row=0, column=2, sticky='w')
        
        # Organ synergy
        self.synergy_label = tk.Label(
            symbolic_grid,
            text="Organ Synergy: 0.50",
            font=('Consolas', 11, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        self.synergy_label.grid(row=1, column=0, columnspan=2, sticky='w', pady=(10, 0))
        
        # Active constellation
        self.constellation_label = tk.Label(
            symbolic_grid,
            text="Constellation: ○✨H",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.constellation_label.grid(row=1, column=2, sticky='w', pady=(10, 0))
    
    def setup_commentary_section(self, parent):
        """Setup the commentary section."""
        commentary_frame = tk.LabelFrame(
            parent,
            text="Cognitive Commentary",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2,
            relief='groove'
        )
        commentary_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Commentary text area
        self.commentary_text = scrolledtext.ScrolledText(
            commentary_frame,
            height=8,
            font=('Consolas', 10),
            bg='#2a2a2a',
            fg=self.colors['fg'],
            insertbackground=self.colors['accent'],
            wrap=tk.WORD
        )
        self.commentary_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add initial message
        self.add_commentary("🧠 DAWN Cognitive Dashboard initialized")
        self.add_commentary("Monitoring cognitive state and forecasts...")
    
    def setup_controls_section(self, parent):
        """Setup the controls section."""
        controls_frame = tk.Frame(parent, bg=self.colors['bg'])
        controls_frame.pack(fill=tk.X)
        
        # Start/Stop button
        self.start_button = tk.Button(
            controls_frame,
            text="Start Engine" if not self.running else "Stop Engine",
            command=self.toggle_engine,
            font=('Consolas', 11, 'bold'),
            bg=self.colors['accent'],
            fg='#000000',
            activebackground=self.colors['fg'],
            activeforeground=self.colors['bg'],
            relief='flat',
            padx=20
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Rebloom button
        self.rebloom_button = tk.Button(
            controls_frame,
            text="Trigger Rebloom",
            command=self.trigger_rebloom,
            font=('Consolas', 11),
            bg=self.colors['warning'],
            fg='#000000',
            activebackground=self.colors['fg'],
            activeforeground=self.colors['bg'],
            relief='flat',
            padx=20
        )
        self.rebloom_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Snapshot button
        self.snapshot_button = tk.Button(
            controls_frame,
            text="Create Snapshot",
            command=self.create_snapshot,
            font=('Consolas', 11),
            bg=self.colors['calm'],
            fg='#ffffff',
            activebackground=self.colors['fg'],
            activeforeground=self.colors['bg'],
            relief='flat',
            padx=20
        )
        self.snapshot_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            controls_frame,
            text="Status: Ready",
            font=('Consolas', 10),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.status_label.pack(side=tk.RIGHT)
    
    def start_updates(self):
        """Start the periodic update loop."""
        self.update_display()
        self.root.after(2000, self.start_updates)  # Update every 2 seconds
    
    def update_display(self):
        """Update all display elements with current state."""
        try:
            if self.exporter:
                # Get current state from snapshot exporter
                state = self.exporter.get_state()
                self.update_metrics(state)
                self.update_forecast(state)
                self.update_symbolic(state)
                
                # Update status
                self.last_update = datetime.now()
                self.status_label.config(text=f"Updated: {self.last_update.strftime('%H:%M:%S')}")
                
            elif self.engine:
                # Get state directly from engine
                state = self.engine.get_state()
                self.update_metrics(state)
                
            else:
                # Mock data for demonstration
                self.update_mock_data()
            
        except Exception as e:
            self.add_commentary(f"⚠️ Update error: {e}")
    
    def update_metrics(self, state):
        """Update the metrics section."""
        metrics = state.get('system_metrics', {})
        
        # Entropy
        entropy = metrics.get('entropy', 0.0)
        self.entropy_label.config(text=f"Entropy: {entropy:.2f}")
        self.entropy_bar['value'] = entropy * 100
        
        # Heat
        heat = metrics.get('heat', 25.0)
        self.current_heat = heat
        self.heat_label.config(text=f"Heat: {heat:.1f}°")
        self.heat_bar['value'] = min(100, heat / 80.0 * 100)  # Scale to 0-80
        
        # SCUP (get from optimizer or state)
        scup = 0.0
        try:
            # Try to get SCUP from optimizer first
            scup_status = get_scup_status()
            if scup_status and 'last_scup' in scup_status:
                scup = scup_status['last_scup'] or 0.0
        except:
            # Fallback to state
            scup = metrics.get('scup', 0.0)
        
        self.current_scup = scup
        self.scup_label.config(text=f"SCUP: {scup:.1f}")
        self.scup_bar['value'] = min(100, scup)
        
        # Zone
        zone = metrics.get('zone', 'CALM')
        zone_color = self.colors.get(zone.lower(), self.colors['fg'])
        self.zone_label.config(text=f"Zone: {zone}", fg=zone_color)
        
        # Tick count
        tick_count = state.get('tick_count', 0)
        self.tick_label.config(text=f"Ticks: {tick_count}")
        
        # Update visual meters
        self.update_visual_meters()
    
    def update_visual_meters(self):
        """Update the visual SCUP bar and Heat arc."""
        try:
            # Update SCUP bar
            self.draw_scup_bar(self.current_scup)
            self.scup_value_label.config(text=f"{self.current_scup:.1f}")
            
            # Update Heat arc  
            self.draw_heat_arc(self.current_heat)
            self.heat_value_label.config(text=f"{self.current_heat:.1f}°C")
            
            # Update colors based on values
            if self.current_scup >= 80:
                scup_color = self.colors['scup_high']
            elif self.current_scup >= 40:
                scup_color = self.colors['accent']
            else:
                scup_color = self.colors['scup_low']
            self.scup_value_label.config(fg=scup_color)
            
            if self.current_heat >= 80:
                heat_color = self.colors['heat_hot']
            elif self.current_heat >= 50:
                heat_color = self.colors['heat_warm']
            else:
                heat_color = self.colors['heat_cool']
            self.heat_value_label.config(fg=heat_color)
            
        except Exception as e:
            self.add_commentary(f"⚠️ Visual meter update error: {e}")
    
    def update_forecast(self, state):
        """Update the forecast section."""
        forecast = state.get('last_forecast', {})
        
        if forecast:
            # Confidence
            confidence = forecast.get('confidence', 0.5)
            self.confidence_label.config(text=f"Confidence: {confidence:.2f}")
            self.confidence_bar['value'] = confidence * 100
            
            # Limit Horizon
            horizon = forecast.get('limit_horizon', 0.5)
            self.horizon_label.config(text=f"Horizon: {horizon:.2f}")
            self.horizon_bar['value'] = horizon * 100
            
            # Risk Level
            risk = forecast.get('risk_level', 0.3)
            self.risk_label.config(text=f"Risk: {risk:.2f}")
            self.risk_bar['value'] = risk * 100
            
            # Emotional Intensity
            emotion = forecast.get('emotional_intensity', 0.5)
            self.emotion_label.config(text=f"Emotion: {emotion:.2f}")
            self.emotion_bar['value'] = emotion * 100
            
            # Add forecast commentary
            if 'commentary' in forecast:
                self.add_commentary(f"🔮 {forecast['commentary']}")
    
    def update_symbolic(self, state):
        """Update the symbolic section."""
        symbolic = state.get('symbolic_state', {})
        
        if symbolic:
            # Heart
            heart = symbolic.get('heart', {})
            charge = heart.get('emotional_charge', 0.5)
            resonance = heart.get('resonance_state', 'gentle')
            self.heart_label.config(text=f"💗 Heart: {resonance} ({charge:.2f})")
            
            # Coil
            coil = symbolic.get('coil', {})
            paths = coil.get('active_paths', 2)
            glyph = coil.get('dominant_glyph', '✨')
            self.coil_label.config(text=f"🌀 Coil: {paths} paths ({glyph})")
            
            # Lung
            lung = symbolic.get('lung', {})
            phase = lung.get('breathing_phase', 'inhaling')
            fullness = lung.get('lung_fullness', 0.6)
            self.lung_label.config(text=f"🫁 Lung: {phase} ({fullness:.2f})")
            
            # Synergy
            synergy = symbolic.get('organ_synergy', 0.5)
            self.synergy_label.config(text=f"Organ Synergy: {synergy:.2f}")
            
            # Constellation
            constellation = symbolic.get('symbolic_state', {}).get('constellation', '○✨H')
            self.constellation_label.config(text=f"Constellation: {constellation}")
    
    def update_mock_data(self):
        """Update with mock data for demonstration."""
        import random
        
        # Mock metrics
        entropy = 0.3 + random.random() * 0.4
        heat = 20 + random.random() * 60  # Extended range for testing heat arc
        scup = random.random() * 80  # SCUP range 0-80
        zone = "CALM" if entropy < 0.4 else "ACTIVE" if entropy < 0.7 else "CHAOTIC"
        
        # Update current values
        self.current_heat = heat
        self.current_scup = scup
        
        self.entropy_label.config(text=f"Entropy: {entropy:.2f}")
        self.entropy_bar['value'] = entropy * 100
        
        self.heat_label.config(text=f"Heat: {heat:.1f}°")
        self.heat_bar['value'] = heat / 80.0 * 100
        
        self.scup_label.config(text=f"SCUP: {scup:.1f}")
        self.scup_bar['value'] = scup
        
        zone_color = self.colors.get(zone.lower(), self.colors['fg'])
        self.zone_label.config(text=f"Zone: {zone}", fg=zone_color)
        
        # Update visual meters
        self.update_visual_meters()
        
        # Add periodic commentary
        if random.random() < 0.3:  # 30% chance each update
            comments = [
                "🧠 Cognitive patterns stabilizing",
                "✨ New neural pathways forming", 
                "🔍 Deep introspection mode active",
                "💫 Consciousness exploring new territories",
                "🌸 Symbolic organs in harmony",
                f"📊 SCUP reading: {scup:.1f} (monitoring coherence)",
                f"🌡️ Thermal pressure: {heat:.1f}°C"
            ]
            self.add_commentary(random.choice(comments))
    
    def add_commentary(self, text):
        """Add commentary to the text area."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_text = f"[{timestamp}] {text}\n"
        
        self.commentary_text.insert(tk.END, formatted_text)
        self.commentary_text.see(tk.END)
        
        # Limit text length
        lines = self.commentary_text.get("1.0", tk.END).split('\n')
        if len(lines) > 100:
            # Keep only last 80 lines
            self.commentary_text.delete("1.0", f"{len(lines)-80}.0")
    
    def toggle_engine(self):
        """Toggle the DAWN engine on/off."""
        if not self.engine:
            self.add_commentary("⚠️ No DAWN engine available")
            return
        
        if not self.running:
            # Start engine in background thread
            self.running = True
            self.engine_thread = threading.Thread(target=self.run_engine, daemon=True)
            self.engine_thread.start()
            
            self.start_button.config(text="Stop Engine", bg=self.colors['critical'])
            self.add_commentary("🚀 DAWN engine started")
        else:
            # Stop engine
            self.running = False
            self.engine.shutdown()
            
            self.start_button.config(text="Start Engine", bg=self.colors['accent'])
            self.add_commentary("🛑 DAWN engine stopped")
    
    def run_engine(self):
        """Run the DAWN engine in background."""
        try:
            self.engine.running = True
            while self.running and self.engine.running:
                self.engine.tick()
                time.sleep(2.0)
        except Exception as e:
            self.add_commentary(f"❌ Engine error: {e}")
    
    def trigger_rebloom(self):
        """Trigger a manual rebloom."""
        if self.engine and hasattr(self.engine, 'symbolic_router') and self.engine.symbolic_router:
            try:
                rebloom_result = self.engine.symbolic_router.rebloom_trigger(
                    emotional_input=0.8,
                    context="Manual GUI trigger"
                )
                rebloom_id = rebloom_result.get('rebloom_id', 'unknown')
                self.add_commentary(f"🌸 Manual rebloom triggered: {rebloom_id}")
            except Exception as e:
                self.add_commentary(f"⚠️ Rebloom error: {e}")
        else:
            self.add_commentary("⚠️ Symbolic router not available")
    
    def create_snapshot(self):
        """Create a snapshot of current state."""
        if self.exporter:
            try:
                snapshot_path = self.exporter.create_full_snapshot_zip()
                filename = Path(snapshot_path).name
                self.add_commentary(f"📦 Snapshot created: {filename}")
            except Exception as e:
                self.add_commentary(f"⚠️ Snapshot error: {e}")
        else:
            self.add_commentary("⚠️ Snapshot exporter not available")
    
    def run(self):
        """Run the dashboard."""
        self.add_commentary("🖥️ Dashboard started - monitoring DAWN cognition")
        self.add_commentary("📊 Live visual meters: SCUP bar and Thermal arc active")
        self.root.mainloop()


def main():
    """Main entry point for the dashboard."""
    print("🖥️ DAWN Cognitive Dashboard starting...")
    
    dashboard = DAWNForecastDashboard()
    dashboard.run()


if __name__ == "__main__":
    main() 