#!/usr/bin/env python3
"""
DAWN Consciousness GUI - 100% Local Python Tkinter Interface
Real-time consciousness visualizations with embedded matplotlib
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Circle
import numpy as np
import websocket
import json
import threading
import time
import queue
from datetime import datetime
from collections import deque
import logging
import sys
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DAWNVisualizationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌊 DAWN Consciousness Monitor - Local GUI")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        # Data storage
        self.data_queue = queue.Queue()
        self.historical_data = deque(maxlen=100)
        self.current_data = None
        self.is_connected = False
        self.ws = None
        
        # Animation control
        self.animation_running = True
        self.animation_speed = 50  # milliseconds
        
        # Statistics
        self.stats = {
            'total_ticks': 0,
            'avg_scup': 0,
            'avg_entropy': 0,
            'peak_neural': 0,
            'connection_time': None
        }
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.setup_plots()
        
        # Start data processing
        self.start_data_thread()
        self.start_animation()
        
        # Connect to DAWN backend
        self.connect_to_dawn()
        
    def setup_styles(self):
        """Configure dark theme styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure dark theme
        style.configure('Title.TLabel', 
                       background='#0a0a0a', 
                       foreground='#00ff88', 
                       font=('Consolas', 14, 'bold'))
        style.configure('Status.TLabel', 
                       background='#0a0a0a', 
                       foreground='#ffffff', 
                       font=('Consolas', 10))
        style.configure('Dark.TFrame', background='#0a0a0a')
        style.configure('Green.TButton', 
                       background='#00ff88', 
                       foreground='#000000',
                       font=('Consolas', 10, 'bold'))
        style.configure('Red.TButton', 
                       background='#ff4444', 
                       foreground='#000000',
                       font=('Consolas', 10, 'bold'))
        
    def create_widgets(self):
        """Create the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title bar
        title_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, 
                               text="🌊 DAWN Consciousness Monitor", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Connection status
        self.status_label = ttk.Label(title_frame, 
                                     text="🔴 DISCONNECTED", 
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Control panel
        control_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.connect_btn = ttk.Button(control_frame, 
                                     text="🔌 CONNECT", 
                                     command=self.connect_to_dawn,
                                     style='Green.TButton')
        self.connect_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.pause_btn = ttk.Button(control_frame, 
                                   text="⏸ PAUSE", 
                                   command=self.toggle_animation,
                                   style='Red.TButton')
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Main content with notebook for different visualizations
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create stats panel at bottom
        self.create_stats_panel(main_frame)
        
    def create_stats_panel(self, parent):
        """Create bottom statistics panel"""
        stats_frame = ttk.Frame(parent, style='Dark.TFrame')
        stats_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Current data display
        self.data_label = ttk.Label(stats_frame, 
                                   text="🔄 Waiting for data...", 
                                   style='Status.TLabel')
        self.data_label.pack(side=tk.LEFT)
        
        # Connection info
        self.connection_label = ttk.Label(stats_frame,
                                         text="🔴 Not connected",
                                         style='Status.TLabel')
        self.connection_label.pack(side=tk.RIGHT)
        
    def setup_plots(self):
        """Create matplotlib plots for different visualizations"""
        # Main consciousness visualization
        self.create_consciousness_plot()
        
        # SCUP trend plot
        self.create_trend_plot()
        
        # Neural activity plot
        self.create_neural_plot()
        
    def create_consciousness_plot(self):
        """Create the main consciousness visualization"""
        # Create frame
        conscious_frame = ttk.Frame(self.notebook)
        self.notebook.add(conscious_frame, text="🧠 Consciousness")
        
        # Create matplotlib figure
        self.fig_conscious = Figure(figsize=(12, 8), facecolor='#0a0a0a')
        self.ax_conscious = self.fig_conscious.add_subplot(111, facecolor='#0a0a0a')
        
        # Configure plot
        self.ax_conscious.set_xlim(0, 10)
        self.ax_conscious.set_ylim(0, 10)
        self.ax_conscious.set_title('DAWN Consciousness State', color='#00ff88', fontsize=16, fontweight='bold')
        self.ax_conscious.tick_params(colors='#ffffff')
        
        # Remove axes for clean look
        self.ax_conscious.set_xticks([])
        self.ax_conscious.set_yticks([])
        
        # Create canvas
        self.canvas_conscious = FigureCanvasTkAgg(self.fig_conscious, conscious_frame)
        self.canvas_conscious.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_trend_plot(self):
        """Create SCUP and entropy trend visualization"""
        trend_frame = ttk.Frame(self.notebook)
        self.notebook.add(trend_frame, text="📈 Trends")
        
        self.fig_trend = Figure(figsize=(12, 8), facecolor='#0a0a0a')
        self.ax_trend = self.fig_trend.add_subplot(111, facecolor='#0a0a0a')
        
        self.ax_trend.set_title('Consciousness Metrics Trends', color='#00ff88', fontsize=16, fontweight='bold')
        self.ax_trend.set_xlabel('Time', color='#ffffff')
        self.ax_trend.set_ylabel('Value (%)', color='#ffffff')
        self.ax_trend.tick_params(colors='#ffffff')
        self.ax_trend.grid(True, alpha=0.3, color='#333333')
        
        # Initialize trend lines
        self.scup_line, = self.ax_trend.plot([], [], 'g-', linewidth=3, label='SCUP', alpha=0.9)
        self.entropy_line, = self.ax_trend.plot([], [], 'r-', linewidth=3, label='Entropy', alpha=0.9)
        self.neural_line, = self.ax_trend.plot([], [], 'b-', linewidth=3, label='Neural', alpha=0.9)
        
        legend = self.ax_trend.legend(loc='upper right', facecolor='#1a1a1a', edgecolor='#333333')
        plt.setp(legend.get_texts(), color='#ffffff')
        
        self.canvas_trend = FigureCanvasTkAgg(self.fig_trend, trend_frame)
        self.canvas_trend.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_neural_plot(self):
        """Create neural activity visualization"""
        neural_frame = ttk.Frame(self.notebook)
        self.notebook.add(neural_frame, text="🔥 Neural Activity")
        
        self.fig_neural = Figure(figsize=(12, 8), facecolor='#0a0a0a')
        self.ax_neural = self.fig_neural.add_subplot(111, facecolor='#0a0a0a', projection='polar')
        
        self.ax_neural.set_title('Neural Activity Radar', color='#00ff88', fontsize=16, fontweight='bold', pad=20)
        
        self.canvas_neural = FigureCanvasTkAgg(self.fig_neural, neural_frame)
        self.canvas_neural.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def connect_to_dawn(self):
        """Connect to the DAWN backend WebSocket"""
        if self.is_connected:
            self.disconnect()
            return
            
        try:
            self.log_message("🔌 Connecting to DAWN backend...")
            
            def on_open(ws):
                self.is_connected = True
                self.stats['connection_time'] = datetime.now()
                self.update_connection_status(True)
                self.log_message("✅ Connected to DAWN consciousness engine!")
                
            def on_message(ws, message):
                try:
                    data = json.loads(message)
                    self.data_queue.put(data)
                except json.JSONDecodeError as e:
                    self.log_message(f"❌ JSON decode error: {e}")
                    
            def on_error(ws, error):
                self.log_message(f"❌ WebSocket error: {error}")
                
            def on_close(ws, close_status_code, close_msg):
                self.is_connected = False
                self.update_connection_status(False)
                self.log_message("🔌 Disconnected from DAWN backend")
                
            # Create WebSocket connection
            self.ws = websocket.WebSocketApp("ws://localhost:8000/ws",
                                           on_open=on_open,
                                           on_message=on_message,
                                           on_error=on_error,
                                           on_close=on_close)
            
            # Start WebSocket in a separate thread
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            
        except Exception as e:
            self.log_message(f"❌ Connection failed: {e}")
            messagebox.showerror("Connection Error", f"Failed to connect to DAWN backend:\n{e}")
            
    def disconnect(self):
        """Disconnect from DAWN backend"""
        if self.ws:
            self.ws.close()
        self.is_connected = False
        self.update_connection_status(False)
        
    def update_connection_status(self, connected):
        """Update connection status display"""
        if connected:
            self.status_label.config(text="🟢 CONNECTED")
            self.connection_label.config(text="🟢 DAWN Backend Connected")
            self.connect_btn.config(text="🔌 DISCONNECT", style='Red.TButton')
        else:
            self.status_label.config(text="🔴 DISCONNECTED")
            self.connection_label.config(text="🔴 DAWN Backend Disconnected")
            self.connect_btn.config(text="🔌 CONNECT", style='Green.TButton')
            
    def start_data_thread(self):
        """Start the data processing thread"""
        def process_data():
            while True:
                try:
                    # Get data from queue
                    data = self.data_queue.get(timeout=1)
                    self.process_consciousness_data(data)
                except queue.Empty:
                    continue
                except Exception as e:
                    self.log_message(f"❌ Data processing error: {e}")
                    
        thread = threading.Thread(target=process_data)
        thread.daemon = True
        thread.start()
        
    def process_consciousness_data(self, data):
        """Process incoming consciousness data"""
        try:
            # Extract consciousness metrics
            if 'type' in data and data['type'] == 'tick' and 'data' in data:
                tick_data = data['data']
            elif 'scup' in data:
                tick_data = data
            else:
                return
                
            # Normalize data
            processed_data = {
                'scup': float(tick_data.get('scup', 0)),
                'entropy': float(tick_data.get('entropy', 0)),
                'neural_activity': float(tick_data.get('neural_activity', 0)),
                'heat': float(tick_data.get('heat', 0)),
                'mood': str(tick_data.get('mood', 'unknown')),
                'tick_number': int(tick_data.get('tick_number', 0)),
                'timestamp': time.time()
            }
            
            # Store data
            self.current_data = processed_data
            self.historical_data.append(processed_data)
            
            # Update statistics
            self.update_statistics()
            
            # Schedule GUI updates on main thread
            self.root.after(0, self.update_displays)
            
        except Exception as e:
            self.log_message(f"❌ Error processing data: {e}")
            
    def update_statistics(self):
        """Update internal statistics"""
        if not self.historical_data:
            return
            
        data_list = list(self.historical_data)
        
        self.stats['total_ticks'] = len(data_list)
        self.stats['avg_scup'] = np.mean([d['scup'] for d in data_list]) * 100
        self.stats['avg_entropy'] = np.mean([d['entropy'] for d in data_list]) * 100
        self.stats['peak_neural'] = max([d['neural_activity'] for d in data_list]) * 100
        
    def update_displays(self):
        """Update all visual displays"""
        if not self.current_data:
            return
            
        try:
            # Update consciousness visualization
            self.update_consciousness_plot()
            
            # Update trend plots
            self.update_trend_plot()
            
            # Update neural radar
            self.update_neural_plot()
            
            # Update status displays
            self.update_status_displays()
            
        except Exception as e:
            self.log_message(f"❌ Display update error: {e}")
            
    def update_consciousness_plot(self):
        """Update the main consciousness visualization"""
        if not self.current_data:
            return
            
        # Clear previous plots
        self.ax_conscious.clear()
        
        # Set up the plot
        self.ax_conscious.set_xlim(0, 10)
        self.ax_conscious.set_ylim(0, 10)
        self.ax_conscious.set_facecolor('#0a0a0a')
        self.ax_conscious.set_xticks([])
        self.ax_conscious.set_yticks([])
        
        # Draw SCUP as pulsing circle
        scup_val = self.current_data['scup']
        radius = 0.8 + (scup_val * 1.2)
        pulse = 1 + 0.3 * math.sin(time.time() * 3)
        
        scup_circle = Circle((2.5, 7), radius * pulse, 
                           color='#00ff88', alpha=0.5 + scup_val * 0.5)
        self.ax_conscious.add_patch(scup_circle)
        
        # SCUP label
        self.ax_conscious.text(2.5, 7, f'SCUP\n{scup_val*100:.1f}%', 
                              ha='center', va='center',
                              color='#ffffff', fontweight='bold', fontsize=14)
        
        # Draw entropy as heat map
        entropy_val = self.current_data['entropy']
        for i in range(8):
            for j in range(3):
                x = 7 + i * 0.3
                y = 6.5 + j * 0.5
                alpha = max(0.1, entropy_val - (i + j) * 0.05)
                self.ax_conscious.scatter(x, y, s=100, c='red', alpha=alpha)
                
        # Entropy label
        self.ax_conscious.text(8.5, 5.5, f'ENTROPY\n{entropy_val*100:.1f}%',
                              ha='center', va='center',
                              color='#ff6464', fontweight='bold', fontsize=12)
        
        # Neural activity as waves
        neural_val = self.current_data['neural_activity']
        x_wave = np.linspace(0.5, 9.5, 50)
        y_wave = 3 + neural_val * 0.8 * np.sin(x_wave * 1.5 + time.time() * 4)
        self.ax_conscious.plot(x_wave, y_wave, color='#4dabf7', linewidth=3, alpha=0.9)
        
        # Neural label
        self.ax_conscious.text(5, 1.5, f'NEURAL ACTIVITY: {neural_val*100:.1f}%',
                              ha='center', va='center',
                              color='#4dabf7', fontweight='bold', fontsize=12)
        
        # Mood indicator
        mood_colors = {
            'calm': '#64ffda',
            'energetic': '#ff9800',
            'chaotic': '#f44336',
            'contemplative': '#9c27b0',
            'analytical': '#2196f3'
        }
        
        mood = self.current_data['mood']
        mood_color = mood_colors.get(mood, '#ffffff')
        
        # Mood circle
        mood_circle = Circle((7.5, 2), 0.5, color=mood_color, alpha=0.7)
        self.ax_conscious.add_patch(mood_circle)
        
        self.ax_conscious.text(7.5, 2, mood.upper()[:4],
                              ha='center', va='center',
                              color='#ffffff', fontweight='bold', fontsize=10)
        
        # Connection status indicator
        status_color = '#00ff88' if self.is_connected else '#ff4444'
        status_text = 'CONNECTED' if self.is_connected else 'OFFLINE'
        
        status_circle = Circle((1, 1), 0.3, color=status_color, alpha=0.8)
        self.ax_conscious.add_patch(status_circle)
        
        self.ax_conscious.text(1, 0.3, status_text,
                              ha='center', va='center',
                              color=status_color, fontweight='bold', fontsize=8)
        
        # Title
        self.ax_conscious.text(5, 9.5, 'DAWN Consciousness State',
                              ha='center', va='center',
                              color='#00ff88', fontweight='bold', fontsize=16)
        
        # Refresh canvas
        self.canvas_conscious.draw()
        
    def update_trend_plot(self):
        """Update trend visualization"""
        if len(self.historical_data) < 2:
            return
            
        data_list = list(self.historical_data)
        times = range(len(data_list))
        
        scup_values = [d['scup'] * 100 for d in data_list]
        entropy_values = [d['entropy'] * 100 for d in data_list]
        neural_values = [d['neural_activity'] * 100 for d in data_list]
        
        # Update lines
        self.scup_line.set_data(times, scup_values)
        self.entropy_line.set_data(times, entropy_values)
        self.neural_line.set_data(times, neural_values)
        
        # Update axes
        self.ax_trend.set_xlim(0, max(50, len(data_list)))
        self.ax_trend.set_ylim(0, 100)
        
        # Refresh canvas
        self.canvas_trend.draw()
        
    def update_neural_plot(self):
        """Update neural radar visualization"""
        if not self.current_data:
            return
            
        # Clear and setup
        self.ax_neural.clear()
        
        # Create radar data
        categories = ['SCUP', 'Entropy', 'Neural', 'Heat', 'Coherence', 'Unity']
        values = [
            self.current_data['scup'] * 100,
            self.current_data['entropy'] * 100,
            self.current_data['neural_activity'] * 100,
            self.current_data['heat'] * 100,
            (1 - self.current_data['entropy']) * 100,  # Coherence
            self.current_data['scup'] * 100  # Unity
        ]
        
        # Plot radar
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
        values += values[:1]  # Close the plot
        angles = np.concatenate((angles, [angles[0]]))
        
        self.ax_neural.plot(angles, values, 'o-', color='#00ff88', linewidth=3, markersize=8)
        self.ax_neural.fill(angles, values, alpha=0.25, color='#00ff88')
        
        # Labels
        self.ax_neural.set_xticks(angles[:-1])
        self.ax_neural.set_xticklabels(categories, color='#ffffff', fontsize=12)
        self.ax_neural.set_ylim(0, 100)
        self.ax_neural.tick_params(colors='#ffffff')
        self.ax_neural.grid(True, alpha=0.3)
        
        # Refresh canvas
        self.canvas_neural.draw()
        
    def update_status_displays(self):
        """Update status displays"""
        if self.current_data:
            data_text = (f"🔄 LIVE: SCUP {self.current_data['scup']*100:.1f}% | "
                        f"Entropy {self.current_data['entropy']*100:.1f}% | "
                        f"Neural {self.current_data['neural_activity']*100:.1f}% | "
                        f"Mood: {self.current_data['mood'].upper()} | "
                        f"Tick #{self.current_data['tick_number']}")
            
            self.data_label.config(text=data_text)
        
    def start_animation(self):
        """Start the animation loop"""
        def animate():
            if self.animation_running and self.current_data:
                self.update_displays()
            
            # Schedule next animation frame
            self.root.after(self.animation_speed, animate)
            
        animate()
        
    def toggle_animation(self):
        """Toggle animation on/off"""
        self.animation_running = not self.animation_running
        
        if self.animation_running:
            self.pause_btn.config(text="⏸ PAUSE", style='Red.TButton')
            self.log_message("▶ Animation resumed")
        else:
            self.pause_btn.config(text="▶ RESUME", style='Green.TButton')
            self.log_message("⏸ Animation paused")
        
    def log_message(self, message):
        """Log message to console"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        logger.info(log_entry)
        print(log_entry)
        
    def on_closing(self):
        """Handle application closing"""
        self.log_message("🚪 Shutting down DAWN GUI...")
        
        if self.ws:
            self.ws.close()
            
        self.root.destroy()

def main():
    """Main application entry point"""
    print("🌊 Starting DAWN Consciousness GUI...")
    
    # Check dependencies
    try:
        import websocket
        print("✅ WebSocket library available")
    except ImportError:
        print("❌ websocket-client not installed. Run: pip install websocket-client")
        sys.exit(1)
        
    try:
        import matplotlib
        print("✅ Matplotlib available")
    except ImportError:
        print("❌ matplotlib not installed. Run: pip install matplotlib")
        sys.exit(1)
        
    # Create and run GUI
    root = tk.Tk()
    app = DAWNVisualizationGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    print("🚀 DAWN GUI initialized - connecting to backend...")
    root.mainloop()

if __name__ == "__main__":
    main() 