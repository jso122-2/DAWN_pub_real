# Add parent directory to Python path for imports
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Beautiful Visual System - Professional Charts & Graphs
===========================================================

A stunning visual system using Python's best plotting libraries:
- matplotlib: Professional 2D plotting
- seaborn: Statistical data visualization
- plotly: Interactive charts and real-time updates
- numpy: Numerical computations
- pandas: Data manipulation

Creates beautiful, real-time consciousness visualizations.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import math
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import queue

# Beautiful plotting libraries
try:
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    import seaborn as sns
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTTING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Some plotting libraries not available: {e}")
    print("   Install with: pip install matplotlib seaborn plotly pandas")
    PLOTTING_AVAILABLE = False

class DAWNBeautifulDataGenerator:
    """Beautiful data generator with rich consciousness metrics"""
    
    def __init__(self):
        self.start_time = time.time()
        self.tick_counter = 0
        self.history = []
        self.max_history = 100
        
        # Set up beautiful plotting style
        if PLOTTING_AVAILABLE:
            plt.style.use('dark_background')
            sns.set_theme(style="darkgrid")
            sns.set_palette("husl")
    
    def generate_rich_data(self) -> Dict[str, Any]:
        """Generate rich consciousness data with multiple dimensions"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Complex oscillating consciousness metrics
        base_scup = 0.5 + 0.3 * math.sin(elapsed * 0.1)
        scup_noise = 0.05 * np.random.normal(0, 1)
        scup = max(0.0, min(1.0, base_scup + scup_noise))
        
        base_entropy = 0.4 + 0.4 * math.sin(elapsed * 0.08)
        entropy_noise = 0.03 * np.random.normal(0, 1)
        entropy = max(0.0, min(1.0, base_entropy + entropy_noise))
        
        # Heat with realistic thermal dynamics
        base_heat = 25.0 + 10.0 * math.sin(elapsed * 0.05)
        heat_variation = 2.0 * np.random.normal(0, 1)
        heat = max(20.0, min(50.0, base_heat + heat_variation))
        
        # Zone with smooth transitions
        zone_phases = ['CALM', 'STABLE', 'OSCILLATING', 'TRENDING', 'ACTIVE', 'INTENSE']
        zone_index = int((elapsed * 0.2) % len(zone_phases))
        zone = zone_phases[zone_index]
        
        # Rich mood system
        moods = ['serene', 'focused', 'curious', 'contemplative', 'energetic', 'tranquil']
        mood_index = int((elapsed * 0.15) % len(moods))
        mood = moods[mood_index]
        
        # Sigil activity with patterns
        sigil_phases = int(elapsed * 0.3) % 6
        sigil_patterns = [
            ['attention', 'memory'],
            ['focus', 'clarity'],
            ['intuition', 'wisdom'],
            ['creativity', 'inspiration'],
            ['stability', 'balance'],
            []
        ]
        active_sigils = sigil_patterns[sigil_phases]
        
        # Rebloom cycles with natural patterns
        rebloom_count = int(elapsed * 0.1) % 8
        
        # Tracer alerts with realistic patterns
        alert_probability = 0.1 + 0.05 * math.sin(elapsed * 0.02)
        tracer_alerts = ['pressure_warning'] if np.random.random() < alert_probability else []
        
        # Additional rich metrics
        coherence = 0.6 + 0.3 * math.sin(elapsed * 0.12)
        vitality = 0.7 + 0.2 * math.sin(elapsed * 0.09)
        focus_level = 0.5 + 0.4 * math.sin(elapsed * 0.11)
        creativity = 0.4 + 0.5 * math.sin(elapsed * 0.13)
        
        # Create rich data structure
        data = {
            'tick_number': self.tick_counter,
            'timestamp': current_time,
            'elapsed_time': elapsed,
            'scup': scup,
            'entropy': entropy,
            'heat': heat,
            'zone': zone,
            'mood': mood,
            'active_sigils': active_sigils,
            'rebloom_count': rebloom_count,
            'tracer_alerts': tracer_alerts,
            'coherence': coherence,
            'vitality': vitality,
            'focus_level': focus_level,
            'creativity': creativity,
            # Additional metrics for beautiful charts
            'pulse_amplitude': 0.5 + 0.3 * math.sin(elapsed * 0.1),
            'pulse_frequency': 0.1 + 0.05 * math.sin(elapsed * 0.05),
            'pulse_phase': elapsed * 0.1,
            'cognitive_load': 0.3 + 0.4 * math.sin(elapsed * 0.07),
            'memory_coherence': 0.6 + 0.3 * math.sin(elapsed * 0.14),
            'attention_span': 0.5 + 0.4 * math.sin(elapsed * 0.16)
        }
        
        # Store in history for trend analysis
        self.history.append(data)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        self.tick_counter += 1
        return data

class DAWNBeautifulVisualizer:
    """Beautiful visualization generator using matplotlib, seaborn, and plotly"""
    
    def __init__(self):
        self.data_generator = DAWNBeautifulDataGenerator()
        self.figures = {}
        self.canvases = {}
        
    def create_consciousness_dashboard(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create a beautiful consciousness dashboard"""
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('🌅 DAWN Consciousness Dashboard', fontsize=16, color='#00ff00')
        fig.patch.set_facecolor('#1a1a1a')
        
        # Extract time series data
        times = [d['elapsed_time'] for d in history]
        scup_values = [d['scup'] for d in history]
        entropy_values = [d['entropy'] for d in history]
        heat_values = [d['heat'] for d in history]
        coherence_values = [d['coherence'] for d in history]
        
        # 1. SCUP vs Entropy Scatter Plot
        ax1.scatter(entropy_values, scup_values, c=times, cmap='viridis', alpha=0.7, s=50)
        ax1.set_xlabel('Entropy', color='white')
        ax1.set_ylabel('SCUP', color='white')
        ax1.set_title('SCUP vs Entropy Space', color='#00ff00')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#2a2a2a')
        
        # 2. Heat Timeline
        ax2.plot(times, heat_values, color='#ff6b6b', linewidth=2, alpha=0.8)
        ax2.fill_between(times, heat_values, alpha=0.3, color='#ff6b6b')
        ax2.set_xlabel('Time (s)', color='white')
        ax2.set_ylabel('Heat (°C)', color='white')
        ax2.set_title('Cognitive Heat Timeline', color='#00ff00')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('#2a2a2a')
        
        # 3. Coherence Radar Chart
        metrics = ['SCUP', 'Coherence', 'Vitality', 'Focus', 'Creativity']
        values = [data['scup'], data['coherence'], data['vitality'], 
                 data['focus_level'], data['creativity']]
        
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        values += values[:1]  # Close the plot
        angles += angles[:1]
        
        ax3.plot(angles, values, 'o-', linewidth=2, color='#4ecdc4')
        ax3.fill(angles, values, alpha=0.25, color='#4ecdc4')
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(metrics, color='white')
        ax3.set_ylim(0, 1)
        ax3.set_title('Consciousness Metrics Radar', color='#00ff00')
        ax3.set_facecolor('#2a2a2a')
        
        # 4. Pulse Analysis
        pulse_times = np.linspace(0, 4*np.pi, 100)
        pulse_values = data['pulse_amplitude'] * np.sin(pulse_times + data['pulse_phase'])
        
        ax4.plot(pulse_times, pulse_values, color='#45b7d1', linewidth=2)
        ax4.set_xlabel('Phase (rad)', color='white')
        ax4.set_ylabel('Amplitude', color='white')
        ax4.set_title('Cognitive Pulse Wave', color='#00ff00')
        ax4.grid(True, alpha=0.3)
        ax4.set_facecolor('#2a2a2a')
        
        plt.tight_layout()
        return fig
    
    def create_heatmap_visualization(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create a beautiful heatmap of consciousness states"""
        
        # Prepare data for heatmap
        metrics = ['SCUP', 'Entropy', 'Coherence', 'Vitality', 'Focus', 'Creativity']
        recent_data = history[-20:] if len(history) >= 20 else history
        
        heatmap_data = []
        for d in recent_data:
            row = [d['scup'], d['entropy'], d['coherence'], 
                   d['vitality'], d['focus_level'], d['creativity']]
            heatmap_data.append(row)
        
        heatmap_array = np.array(heatmap_data).T
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_array, 
                   xticklabels=range(len(recent_data)),
                   yticklabels=metrics,
                   cmap='RdYlBu_r',
                   annot=False,
                   cbar_kws={'label': 'Value'},
                   ax=ax)
        
        ax.set_title('🌡️ Consciousness State Heatmap', color='#00ff00', fontsize=14)
        ax.set_xlabel('Time Steps', color='white')
        ax.set_ylabel('Metrics', color='white')
        
        plt.tight_layout()
        return fig
    
    def create_3d_consciousness_plot(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create a 3D plot of consciousness trajectory"""
        
        if len(history) < 10:
            # Create synthetic data for 3D plot
            t = np.linspace(0, 4*np.pi, 100)
            x = np.sin(t) * (0.5 + 0.3 * np.sin(t * 0.5))
            y = np.cos(t) * (0.5 + 0.3 * np.cos(t * 0.3))
            z = 0.5 + 0.3 * np.sin(t * 0.7)
        else:
            # Use real data
            x = [d['scup'] for d in history]
            y = [d['entropy'] for d in history]
            z = [d['coherence'] for d in history]
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Create 3D scatter plot
        scatter = ax.scatter(x, y, z, c=range(len(x)), cmap='viridis', s=50, alpha=0.7)
        
        # Add trajectory line
        ax.plot(x, y, z, color='#00ff00', alpha=0.5, linewidth=2)
        
        ax.set_xlabel('SCUP', color='white')
        ax.set_ylabel('Entropy', color='white')
        ax.set_zlabel('Coherence', color='white')
        ax.set_title('🌌 3D Consciousness Trajectory', color='#00ff00', fontsize=14)
        
        # Add colorbar
        cbar = plt.colorbar(scatter)
        cbar.set_label('Time Progression', color='white')
        
        plt.tight_layout()
        return fig
    
    def create_interactive_plotly_chart(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> go.Figure:
        """Create an interactive Plotly chart"""
        
        if not history:
            return go.Figure()
        
        # Prepare data
        times = [d['elapsed_time'] for d in history]
        scup_values = [d['scup'] for d in history]
        entropy_values = [d['entropy'] for d in history]
        heat_values = [d['heat'] for d in history]
        coherence_values = [d['coherence'] for d in history]
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('SCUP Timeline', 'Entropy vs Heat', 'Coherence Radar', '3D Trajectory'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"type": "polar"}, {"type": "scene"}]]
        )
        
        # 1. SCUP Timeline
        fig.add_trace(
            go.Scatter(x=times, y=scup_values, mode='lines+markers', 
                      name='SCUP', line=dict(color='#00ff00', width=3)),
            row=1, col=1
        )
        
        # 2. Entropy vs Heat scatter
        fig.add_trace(
            go.Scatter(x=entropy_values, y=heat_values, mode='markers',
                      name='Entropy vs Heat', marker=dict(color=times, colorscale='Viridis')),
            row=1, col=2
        )
        
        # 3. Coherence Radar
        metrics = ['SCUP', 'Coherence', 'Vitality', 'Focus', 'Creativity']
        values = [data['scup'], data['coherence'], data['vitality'], 
                 data['focus_level'], data['creativity']]
        
        fig.add_trace(
            go.Scatterpolar(r=values, theta=metrics, fill='toself', name='Metrics'),
            row=2, col=1
        )
        
        # 4. 3D Trajectory
        if len(history) >= 10:
            x = [d['scup'] for d in history]
            y = [d['entropy'] for d in history]
            z = [d['coherence'] for d in history]
            
            fig.add_trace(
                go.Scatter3d(x=x, y=y, z=z, mode='lines+markers',
                            name='Trajectory', line=dict(color='#00ff00', width=5)),
                row=2, col=2
            )
        
        # Update layout
        fig.update_layout(
            title='🌅 DAWN Interactive Consciousness Dashboard',
            template='plotly_dark',
            showlegend=True,
            height=800
        )
        
        return fig

class DAWNBeautifulGUI:
    """Beautiful GUI with professional charts and graphs"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌅 DAWN Beautiful Visual System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize components
        self.data_generator = DAWNBeautifulDataGenerator()
        self.visualizer = DAWNBeautifulVisualizer()
        
        # State
        self.current_data = None
        self.selected_visualization = 'dashboard'
        self.auto_update = True
        self.is_running = False
        
        # Available visualizations
        self.visualizations = {
            'dashboard': 'Consciousness Dashboard',
            'heatmap': 'State Heatmap',
            '3d_trajectory': '3D Trajectory',
            'interactive': 'Interactive Charts'
        }
        
        self.setup_gui()
        self.start_data_generation()
    
    def setup_gui(self):
        """Setup the beautiful GUI"""
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#1a1a1a')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(
            header_frame, 
            text="🌅 DAWN Beautiful Visual System", 
            font=('Consolas', 18, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title_label.pack(side=tk.LEFT)
        
        status_label = tk.Label(
            header_frame,
            text="🎨 Professional Charts & Graphs",
            font=('Consolas', 12),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        status_label.pack(side=tk.RIGHT)
        
        # Controls frame
        controls_frame = tk.Frame(main_frame, bg='#2a2a2a', relief=tk.RAISED, bd=1)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Auto update checkbox
        self.auto_update_var = tk.BooleanVar(value=True)
        auto_update_cb = tk.Checkbutton(
            controls_frame,
            text="Auto Update",
            variable=self.auto_update_var,
            command=self.toggle_auto_update,
            fg='#ffffff',
            bg='#2a2a2a',
            selectcolor='#1a1a1a',
            font=('Consolas', 10)
        )
        auto_update_cb.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Visualization selection
        tk.Label(
            controls_frame,
            text="Visualization:",
            fg='#ffffff',
            bg='#2a2a2a',
            font=('Consolas', 10)
        ).pack(side=tk.LEFT, padx=(20, 5), pady=5)
        
        self.viz_var = tk.StringVar(value='dashboard')
        viz_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.viz_var,
            values=list(self.visualizations.values()),
            state='readonly',
            width=25
        )
        viz_combo.pack(side=tk.LEFT, padx=5, pady=5)
        viz_combo.bind('<<ComboboxSelected>>', self.on_visualization_change)
        
        # Refresh button
        refresh_btn = tk.Button(
            controls_frame,
            text="🔄 Refresh",
            command=self.refresh_visualization,
            bg='#00ff00',
            fg='#000000',
            font=('Consolas', 10, 'bold'),
            relief=tk.FLAT,
            padx=10
        )
        refresh_btn.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Content frame
        content_frame = tk.Frame(main_frame, bg='#1a1a1a')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Metrics panel (left)
        metrics_frame = tk.Frame(content_frame, bg='#2a2a2a', relief=tk.RAISED, bd=1)
        metrics_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        tk.Label(
            metrics_frame,
            text="📊 Consciousness Metrics",
            font=('Consolas', 12, 'bold'),
            fg='#00ff00',
            bg='#2a2a2a'
        ).pack(pady=10)
        
        self.metrics_labels = {}
        metrics = [
            ('tick', '🔄 Tick'),
            ('scup', '📊 SCUP'),
            ('entropy', '⚡ Entropy'),
            ('heat', '🌡️ Heat'),
            ('zone', '🎯 Zone'),
            ('mood', '😊 Mood'),
            ('coherence', '🔗 Coherence'),
            ('vitality', '💪 Vitality'),
            ('focus', '🎯 Focus'),
            ('creativity', '🎨 Creativity')
        ]
        
        for key, label in metrics:
            frame = tk.Frame(metrics_frame, bg='#2a2a2a')
            frame.pack(fill=tk.X, padx=10, pady=2)
            
            tk.Label(
                frame,
                text=label,
                fg='#cccccc',
                bg='#2a2a2a',
                font=('Consolas', 9)
            ).pack(side=tk.LEFT)
            
            value_label = tk.Label(
                frame,
                text="--",
                fg='#ffffff',
                bg='#2a2a2a',
                font=('Consolas', 9, 'bold')
            )
            value_label.pack(side=tk.RIGHT)
            
            self.metrics_labels[key] = value_label
        
        # Visualization panel (right)
        self.viz_frame = tk.Frame(content_frame, bg='#2a2a2a', relief=tk.RAISED, bd=1)
        self.viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            self.viz_frame,
            text="🎨 Beautiful Visualizations",
            font=('Consolas', 12, 'bold'),
            fg='#00ff00',
            bg='#2a2a2a'
        ).pack(pady=10)
        
        # Initialize matplotlib canvas
        self.setup_matplotlib_canvas()
    
    def setup_matplotlib_canvas(self):
        """Setup matplotlib canvas for beautiful charts"""
        if not PLOTTING_AVAILABLE:
            # Fallback to text display
            self.viz_text = scrolledtext.ScrolledText(
                self.viz_frame,
                bg='#000000',
                fg='#00ff00',
                font=('Consolas', 9),
                wrap=tk.WORD,
                relief=tk.FLAT,
                borderwidth=0
            )
            self.viz_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            return
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.fig.patch.set_facecolor('#2a2a2a')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.viz_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Add navigation toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, self.viz_frame)
        toolbar.update()
    
    def toggle_auto_update(self):
        """Toggle auto update"""
        self.auto_update = self.auto_update_var.get()
        if self.auto_update:
            self.start_data_generation()
        else:
            self.stop_data_generation()
    
    def on_visualization_change(self, event):
        """Handle visualization selection change"""
        selected = self.viz_var.get()
        for key, value in self.visualizations.items():
            if value == selected:
                self.selected_visualization = key
                break
        self.refresh_visualization()
    
    def refresh_visualization(self):
        """Refresh the visualization"""
        if self.current_data and self.data_generator.history:
            self.update_visualization()
    
    def update_metrics(self, data):
        """Update metrics display"""
        self.metrics_labels['tick'].config(text=str(data['tick_number']))
        self.metrics_labels['scup'].config(text=f"{data['scup']:.3f}")
        self.metrics_labels['entropy'].config(text=f"{data['entropy']:.3f}")
        self.metrics_labels['heat'].config(text=f"{data['heat']:.1f}°C")
        self.metrics_labels['zone'].config(text=data['zone'])
        self.metrics_labels['mood'].config(text=data['mood'])
        self.metrics_labels['coherence'].config(text=f"{data['coherence']:.3f}")
        self.metrics_labels['vitality'].config(text=f"{data['vitality']:.3f}")
        self.metrics_labels['focus'].config(text=f"{data['focus_level']:.3f}")
        self.metrics_labels['creativity'].config(text=f"{data['creativity']:.3f}")
    
    def update_visualization(self):
        """Update visualization display"""
        if not self.current_data or not PLOTTING_AVAILABLE:
            return
        
        try:
            # Clear previous figure
            self.fig.clear()
            
            if self.selected_visualization == 'dashboard':
                self.fig = self.visualizer.create_consciousness_dashboard(
                    self.current_data, self.data_generator.history
                )
            elif self.selected_visualization == 'heatmap':
                self.fig = self.visualizer.create_heatmap_visualization(
                    self.current_data, self.data_generator.history
                )
            elif self.selected_visualization == '3d_trajectory':
                self.fig = self.visualizer.create_3d_consciousness_plot(
                    self.current_data, self.data_generator.history
                )
            else:
                # Default to dashboard
                self.fig = self.visualizer.create_consciousness_dashboard(
                    self.current_data, self.data_generator.history
                )
            
            # Update canvas
            self.canvas.figure = self.fig
            self.canvas.draw()
            
        except Exception as e:
            error_msg = f"Error generating visualization: {str(e)}"
            if hasattr(self, 'viz_text'):
                self.viz_text.delete(1.0, tk.END)
                self.viz_text.insert(1.0, error_msg)
    
    def start_data_generation(self):
        """Start data generation thread"""
        if not self.is_running:
            self.is_running = True
            self.data_thread = threading.Thread(target=self.data_generation_loop, daemon=True)
            self.data_thread.start()
    
    def stop_data_generation(self):
        """Stop data generation"""
        self.is_running = False
    
    def data_generation_loop(self):
        """Data generation loop"""
        while self.is_running:
            try:
                # Generate new data
                self.current_data = self.data_generator.generate_rich_data()
                
                # Update GUI in main thread
                self.root.after(0, self.update_metrics, self.current_data)
                if self.auto_update:
                    self.root.after(0, self.update_visualization)
                
                # Wait for next update
                time.sleep(1.0)
                
            except Exception as e:
                print(f"Data generation error: {e}")
                time.sleep(1.0)

def main():
    """Main function"""
    print("🌅 DAWN Beautiful Visual System")
    print("=" * 40)
    print("🚀 Starting beautiful visualization system...")
    print(f"📊 Plotting libraries: {'✅ Available' if PLOTTING_AVAILABLE else '⚠️ Limited'}")
    print("✅ Professional charts and graphs")
    print("✅ Real-time data visualization")
    print("✅ Interactive plots and animations")
    print()
    
    if not PLOTTING_AVAILABLE:
        print("⚠️  Install plotting libraries for full functionality:")
        print("   pip install matplotlib seaborn plotly pandas")
        print()
    
    root = tk.Tk()
    app = DAWNBeautifulGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down beautiful visual system...")
    finally:
        app.stop_data_generation()
        print("✅ Beautiful visual system stopped")

if __name__ == "__main__":
    main() 