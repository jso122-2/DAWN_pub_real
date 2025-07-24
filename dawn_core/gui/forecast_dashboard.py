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
    DAWN_AVAILABLE = True
except ImportError:
    DAWN_AVAILABLE = False


class DAWNForecastDashboard:
    """
    Real-time GUI dashboard for DAWN cognitive state monitoring.
    """
    
    def __init__(self):
        """Initialize the dashboard."""
        self.root = tk.Tk()
        self.root.title("DAWN Cognitive Dashboard")
        self.root.geometry("1000x700")
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
            'chaotic': '#ff8844'
        }
        
        # State tracking
        self.running = False
        self.engine = None
        self.exporter = None
        self.last_update = None
        
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
        
        # Zone status
        self.zone_label = tk.Label(
            metrics_grid,
            text="Zone: CALM",
            font=('Consolas', 14, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['calm']
        )
        self.zone_label.grid(row=1, column=0, columnspan=2, sticky='w', pady=(10, 0))
        
        # Tick count
        self.tick_label = tk.Label(
            metrics_grid,
            text="Ticks: 0",
            font=('Consolas', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.tick_label.grid(row=1, column=2, columnspan=2, sticky='w', pady=(10, 0))
    
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
        self.heat_label.config(text=f"Heat: {heat:.1f}°")
        self.heat_bar['value'] = min(100, heat / 80.0 * 100)  # Scale to 0-80
        
        # Zone
        zone = metrics.get('zone', 'CALM')
        zone_color = self.colors.get(zone.lower(), self.colors['fg'])
        self.zone_label.config(text=f"Zone: {zone}", fg=zone_color)
        
        # Tick count
        tick_count = state.get('tick_count', 0)
        self.tick_label.config(text=f"Ticks: {tick_count}")
    
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
        heat = 20 + random.random() * 40
        zone = "CALM" if entropy < 0.4 else "ACTIVE" if entropy < 0.7 else "CHAOTIC"
        
        self.entropy_label.config(text=f"Entropy: {entropy:.2f}")
        self.entropy_bar['value'] = entropy * 100
        
        self.heat_label.config(text=f"Heat: {heat:.1f}°")
        self.heat_bar['value'] = heat / 80.0 * 100
        
        zone_color = self.colors.get(zone.lower(), self.colors['fg'])
        self.zone_label.config(text=f"Zone: {zone}", fg=zone_color)
        
        # Add periodic commentary
        if random.random() < 0.3:  # 30% chance each update
            comments = [
                "🧠 Cognitive patterns stabilizing",
                "✨ New neural pathways forming", 
                "🔍 Deep introspection mode active",
                "💫 Consciousness exploring new territories",
                "🌸 Symbolic organs in harmony"
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
        self.root.mainloop()


def main():
    """Main entry point for the dashboard."""
    print("🖥️ DAWN Cognitive Dashboard starting...")
    
    dashboard = DAWNForecastDashboard()
    dashboard.run()


if __name__ == "__main__":
    main() 