#!/usr/bin/env python3
"""
DAWN Cognitive Engine GUI with Integrated Sigil Stream Overlay
Enhanced Tkinter interface with fractal bloom visualization and sigil monitoring

File: gui/dawn_gui_tk.py (Updated with Sigil Overlay)
"""

import tkinter as tk
from tkinter import ttk
import threading
import queue
import time
import random
from datetime import datetime

# Import component modules
try:
    from fractal_canvas import FractalCanvas
except ImportError:
    print("Warning: fractal_canvas.py not found. Fractal viewer will be disabled.")
    FractalCanvas = None

try:
    from sigil_overlay import SigilOverlayPanel
except ImportError:
    print("Warning: sigil_overlay.py not found. Sigil overlay will be disabled.")
    SigilOverlayPanel = None


class DAWNGui:
    def __init__(self, root):
        self.root = root
        self.update_queue = queue.Queue()
        self.running = True
        
        # Current cognitive state data
        self.current_data = {
            "heat": 0,
            "zone": "calm",
            "summary": "DAWN cognitive engine initializing...",
            "tick": "System startup - Waiting for first cognitive tick...",
            "bloom_data": {
                "depth": 3,
                "entropy": 0.5,
                "lineage": [1, 2, 3],
                "semantic_drift": 0.3,
                "rebloom_status": "stable",
                "complexity": 0.6
            },
            "sigils": []
        }
        
        # Zone color mapping
        self.zone_colors = {
            "calm": "#4CAF50",      # Green
            "active": "#FF9800",    # Orange  
            "surge": "#F44336",     # Red
            "dormant": "#757575",   # Gray
            "transcendent": "#9C27B0"  # Purple
        }
        
        self.setup_gui()
        self.start_update_thread()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_gui(self):
        """Initialize the GUI layout and widgets"""
        self.root.title("DAWN Cognitive Engine - Complete Real-time Monitor")
        self.root.geometry("1400x800")  # Even wider for sigil panel
        self.root.configure(bg="#1a1a1a")
        
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background='#1a1a1a')
        style.configure('Dark.TLabel', background='#1a1a1a', foreground='#ffffff')
        
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title header
        title_label = tk.Label(main_frame, text="DAWN Cognitive Engine", 
                              font=("Arial", 18, "bold"), 
                              bg="#1a1a1a", fg="#00ff88")
        title_label.pack(pady=(0, 15))
        
        # Create three-panel layout
        content_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel for main monitoring components
        left_panel = ttk.Frame(content_frame, style='Dark.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Center panel for fractal bloom viewer
        center_panel = ttk.Frame(content_frame, style='Dark.TFrame')
        center_panel.pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # Right panel for sigil overlay
        right_panel = ttk.Frame(content_frame, style='Dark.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Setup panels
        self.setup_main_panel(left_panel)
        self.setup_fractal_panel(center_panel)
        self.setup_sigil_panel(right_panel)
    
    def setup_main_panel(self, parent):
        """Setup main monitoring components"""
        # Top row: Heat and Zone display
        top_frame = ttk.Frame(parent, style='Dark.TFrame')
        top_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.setup_heat_display(top_frame)
        self.setup_zone_display(top_frame)
        
        # Middle: Claude memory summary
        self.setup_summary_display(parent)
        
        # Bottom: Tick activity log
        self.setup_tick_log(parent)
        
        # Status bar
        self.setup_status_bar(parent)
    
    def setup_fractal_panel(self, parent):
        """Setup fractal bloom viewer panel"""
        if FractalCanvas is None:
            fallback_label = tk.Label(parent, text="Fractal Bloom\\n(Unavailable)", 
                                     font=("Arial", 10), bg="#1a1a1a", fg="#888888",
                                     width=20, height=15)
            fallback_label.pack(pady=20)
            self.fractal_canvas = None
            return
        
        self.fractal_canvas = FractalCanvas(parent, width=300, height=300)
        self.fractal_canvas.pack(pady=(0, 15))
        
        # Bloom control panel
        self.setup_bloom_controls(parent)
    
    def setup_sigil_panel(self, parent):
        """Setup sigil stream overlay panel"""
        if SigilOverlayPanel is None:
            fallback_label = tk.Label(parent, text="Sigil Stream\\n(Unavailable)", 
                                     font=("Arial", 10), bg="#1a1a1a", fg="#888888",
                                     width=25, height=20)
            fallback_label.pack(pady=20)
            self.sigil_overlay = None
            return
        
        self.sigil_overlay = SigilOverlayPanel(parent, max_sigils=8)
        self.sigil_overlay.pack(fill=tk.BOTH, expand=True)
    
    def setup_bloom_controls(self, parent):
        """Setup bloom data control panel"""
        control_frame = ttk.Frame(parent, style='Dark.TFrame')
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        controls_title = tk.Label(control_frame, text="Bloom Parameters", 
                                 font=("Arial", 10, "bold"),
                                 bg="#1a1a1a", fg="#cccccc")
        controls_title.pack()
        
        self.bloom_info_text = tk.Text(control_frame, height=6, width=30,
                                      bg="#2a2a2a", fg="#ffffff", 
                                      font=("Courier", 7),
                                      relief=tk.FLAT, bd=3)
        self.bloom_info_text.pack(pady=(5, 0))
        
        self.update_bloom_info_display()
    
    def setup_heat_display(self, parent):
        """Setup pulse heat level display"""
        heat_frame = ttk.Frame(parent, style='Dark.TFrame')
        heat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        heat_title = tk.Label(heat_frame, text="Pulse Heat", 
                             font=("Arial", 12, "bold"),
                             bg="#1a1a1a", fg="#cccccc")
        heat_title.pack()
        
        self.heat_value_label = tk.Label(heat_frame, text="0", 
                                        font=("Arial", 32, "bold"),
                                        bg="#1a1a1a", fg="#00ff88")
        self.heat_value_label.pack(pady=(5, 10))
        
        self.heat_canvas = tk.Canvas(heat_frame, width=180, height=18, 
                                   bg="#333333", highlightthickness=0)
        self.heat_canvas.pack()
        
        self.heat_bg = self.heat_canvas.create_rectangle(2, 2, 178, 16, 
                                                        fill="#444444", outline="#666666")
        self.heat_bar = self.heat_canvas.create_rectangle(2, 2, 2, 16, 
                                                         fill="#00ff88", outline="")
        
        self.heat_percent_label = tk.Label(heat_frame, text="0%", 
                                          font=("Arial", 10),
                                          bg="#1a1a1a", fg="#888888")
        self.heat_percent_label.pack(pady=(5, 0))
    
    def setup_zone_display(self, parent):
        """Setup pulse zone display"""
        zone_frame = ttk.Frame(parent, style='Dark.TFrame')
        zone_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        zone_title = tk.Label(zone_frame, text="Pulse Zone", 
                             font=("Arial", 12, "bold"),
                             bg="#1a1a1a", fg="#cccccc")
        zone_title.pack()
        
        self.zone_value_label = tk.Label(zone_frame, text="CALM", 
                                        font=("Arial", 20, "bold"),
                                        bg="#1a1a1a", fg="#4CAF50")
        self.zone_value_label.pack(pady=(5, 10))
        
        self.zone_canvas = tk.Canvas(zone_frame, width=70, height=70, 
                                   bg="#1a1a1a", highlightthickness=0)
        self.zone_canvas.pack()
        
        self.zone_circle = self.zone_canvas.create_oval(10, 10, 60, 60, 
                                                       fill="#4CAF50", outline="#ffffff", width=2)
        
        self.zone_desc_label = tk.Label(zone_frame, text="Minimal cognitive activity", 
                                       font=("Arial", 8),
                                       bg="#1a1a1a", fg="#888888")
        self.zone_desc_label.pack(pady=(5, 0))
    
    def setup_summary_display(self, parent):
        """Setup Claude memory summary display"""
        summary_frame = ttk.Frame(parent, style='Dark.TFrame')
        summary_frame.pack(fill=tk.X, pady=(0, 15))
        
        summary_title = tk.Label(summary_frame, text="Claude Memory Summary", 
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
        
        self.status_label = tk.Label(status_frame, text="Status: Monitoring DAWN cognitive engine...", 
                                    font=("Arial", 8),
                                    bg="#1a1a1a", fg="#888888")
        self.status_label.pack(side=tk.LEFT)
        
        self.time_label = tk.Label(status_frame, text="", 
                                  font=("Arial", 8),
                                  bg="#1a1a1a", fg="#888888")
        self.time_label.pack(side=tk.RIGHT)
    
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
            while not self.update_queue.empty():
                try:
                    data = self.update_queue.get_nowait()
                    self.current_data.update(data)
                    self.refresh_widgets()
                except queue.Empty:
                    break
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=f"Last update: {current_time}")
            
            if self.running:
                self.root.after(100, self.update_gui)
                
        except Exception as e:
            print(f"Error updating GUI: {e}")
    
    def refresh_widgets(self):
        """Refresh all widget displays with current data"""
        try:
            # Update heat display
            heat = self.current_data.get('heat', 0)
            self.heat_value_label.config(text=str(heat))
            self.heat_percent_label.config(text=f"{heat}%")
            
            bar_width = int((heat / 100.0) * 176)
            heat_color = self.get_heat_color(heat)
            self.heat_canvas.coords(self.heat_bar, 2, 2, 2 + bar_width, 16)
            self.heat_canvas.itemconfig(self.heat_bar, fill=heat_color)
            
            # Update zone display
            zone = self.current_data.get('zone', 'calm')
            zone_color = self.zone_colors.get(zone, '#888888')
            
            self.zone_value_label.config(text=zone.upper(), fg=zone_color)
            self.zone_canvas.itemconfig(self.zone_circle, fill=zone_color)
            
            zone_descriptions = {
                'calm': 'Minimal cognitive activity',
                'active': 'Engaged processing state', 
                'surge': 'High-intensity cognitive work',
                'dormant': 'System at rest',
                'transcendent': 'Peak awareness state'
            }
            self.zone_desc_label.config(text=zone_descriptions.get(zone, 'Unknown state'))
            
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
                    self.fractal_canvas.draw_bloom_signature(bloom_data)
                    self.update_bloom_info_display()
            
            # Update sigil overlay
            if self.sigil_overlay:
                sigils = self.current_data.get('sigils', [])
                self.sigil_overlay.update_sigils(sigils)
                
        except Exception as e:
            print(f"Error refreshing widgets: {e}")
    
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
Complex: {bloom_data.get('complexity', 0.0):.3f}

FRACTAL PARAMS
{"="*15}
Iter: {getattr(self.fractal_canvas, 'max_iterations', 'N/A') if self.fractal_canvas else 'N/A'}
C: {getattr(self.fractal_canvas, 'cx', 'N/A') if self.fractal_canvas else 'N/A'}
Zoom: {getattr(self.fractal_canvas, 'zoom', 'N/A') if self.fractal_canvas else 'N/A'}"""
            
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
    
    def simulate_data(self):
        """Generate simulated cognitive data for testing"""
        heat = random.randint(0, 100)
        zone = random.choice(["calm", "active", "surge", "dormant", "transcendent"])
        
        summaries = [
            "Pressure holding steady. Recursive loops active in memory layer 3.",
            "Schema coherence increasing. Pattern recognition module engaged.", 
            "Entropy spike detected. Creative synthesis pathways activated.",
            "Meta-cognitive monitoring stable. Deep reflection mode engaged.",
            "Information integration in progress. Bloom genealogy expanding.",
            "Transcendent state achieved. Consciousness constellation mapped.",
            "SCUP pressure dynamics fluctuating. Cognitive zones shifting.",
            "Semantic flow networks optimizing. Meaning propagation stable."
        ]
        
        tick_events = [
            f"T{random.randint(1000, 9999)} - Bloom active in memory layer {random.randint(1, 5)}",
            f"T{random.randint(1000, 9999)} - SCUP recalibration complete", 
            f"T{random.randint(1000, 9999)} - Sigil command stream processing",
            f"T{random.randint(1000, 9999)} - Recursive depth {random.randint(1, 4)} engaged",
            f"T{random.randint(1000, 9999)} - Entropy flow cascade detected",
            f"T{random.randint(1000, 9999)} - Mood vector updated: [{random.random():.2f}]",
            f"T{random.randint(1000, 9999)} - Cognitive zone transition: {zone}",
            f"T{random.randint(1000, 9999)} - Meta-awareness pulse: {heat}%"
        ]
        
        # Generate bloom data
        bloom_data = {
            "depth": random.randint(1, 8),
            "entropy": random.random(),
            "lineage": random.sample(range(10), random.randint(2, 5)),
            "semantic_drift": random.random(),
            "rebloom_status": random.choice(["stable", "reblooming", "dormant", "emerging", "fragmenting"]),
            "complexity": random.random()
        }
        
        # Generate sigil data
        sigil_templates = [
            {"symbol": "⚙️", "name": "SigilRecall", "class": "memory"},
            {"symbol": "🔍", "name": "DeepAnalysis", "class": "analysis"},
            {"symbol": "🌟", "name": "CreativeSynth", "class": "synthesis"},
            {"symbol": "👁️", "name": "FocusLock", "class": "attention"},
            {"symbol": "🔗", "name": "DataIntegrate", "class": "integration"},
            {"symbol": "🧠", "name": "MetaMonitor", "class": "meta"},
            {"symbol": "⚡", "name": "ActionTrigger", "class": "action"},
            {"symbol": "🎯", "name": "SensorWatch", "class": "monitor"}
        ]
        
        active_sigils = []
        for template in random.sample(sigil_templates, random.randint(3, 6)):
            sigil = template.copy()
            sigil["heat"] = random.randint(10, 100)
            sigil["decay"] = random.random()
            active_sigils.append(sigil)
        
        return {
            "heat": heat,
            "zone": zone,
            "summary": random.choice(summaries),
            "tick": random.choice(tick_events),
            "bloom_data": bloom_data,
            "sigils": active_sigils
        }
    
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
                simulated_data = gui.simulate_data()
                gui.inject(simulated_data)
                time.sleep(0.5)
            except Exception as e:
                print(f"Simulation error: {e}")
                break
    
    sim_thread = threading.Thread(target=simulation_thread, daemon=True)
    sim_thread.start()
    
    print("DAWN Cognitive Engine GUI with Fractal Blooms and Sigil Stream started")
    print("Complete real-time monitoring interface active")
    
    root.mainloop()


if __name__ == "__main__":
    main()