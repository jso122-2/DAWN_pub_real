# Add parent directory to Python path for imports
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Visual GUI - Clean, Simple Interface

A clean, simple GUI that connects to the DAWN visual integration
and displays real-time consciousness data.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import json
import math
from datetime import datetime
from typing import Dict, Any, Optional

# Import our visual integration
try:
    from visual.visual_integration import get_visual_integration, get_current_visual_data, get_available_visual_modules
    VISUAL_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Visual integration not available: {e}")
    VISUAL_INTEGRATION_AVAILABLE = False

class DAWNVisualGUI:
    """Clean, simple DAWN visual interface"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌅 DAWN Visual Processes")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Data
        self.current_data = {}
        self.available_modules = {}
        self.update_thread = None
        self.is_running = False
        
        # Initialize visual integration
        if VISUAL_INTEGRATION_AVAILABLE:
            self.visual_integration = get_visual_integration()
            self.available_modules = get_available_visual_modules()
            self.visual_integration.register_callback(self._on_data_update)
        else:
            self.visual_integration = None
            print("⚠️  Running in demo mode without visual integration")
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        
        # Start updates
        self.start_updates()
        
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Dark.TFrame', background='#1a1a1a')
        style.configure('Dark.TLabel', background='#1a1a1a', foreground='#ffffff')
        style.configure('Header.TLabel', background='#1a1a1a', foreground='#00ff00', font=('Arial', 14, 'bold'))
        style.configure('Metric.TLabel', background='#2a2a2a', foreground='#ffffff', font=('Arial', 10))
        style.configure('Status.TLabel', background='#2a2a2a', foreground='#00ff00', font=('Arial', 9))
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="🌅 DAWN Visual Processes", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Status indicator
        self.status_label = ttk.Label(header_frame, text="🟢 Connected", style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Main content area
        content_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Metrics
        self.create_metrics_panel(content_frame)
        
        # Right panel - Visualizations
        self.create_visualization_panel(content_frame)
        
    def create_metrics_panel(self, parent):
        """Create the metrics display panel"""
        metrics_frame = ttk.Frame(parent, style='Dark.TFrame')
        metrics_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Metrics title
        ttk.Label(metrics_frame, text="📊 Consciousness Metrics", style='Header.TLabel').pack(pady=(0, 10))
        
        # Metrics container
        self.metrics_container = ttk.Frame(metrics_frame, style='Dark.TFrame')
        self.metrics_container.pack(fill=tk.BOTH, expand=True)
        
        # Create metric labels
        self.metric_labels = {}
        metrics = [
            ('tick_number', '🔄 Tick Number'),
            ('scup', '📊 SCUP'),
            ('entropy', '⚡ Entropy'),
            ('heat', '🌡️ Heat'),
            ('zone', '🎯 Zone'),
            ('mood', '😊 Mood'),
            ('active_sigils', '🔮 Active Sigils'),
            ('rebloom_count', '🌸 Rebloom Count'),
            ('tracer_alerts', '⚡ Tracer Alerts')
        ]
        
        for metric_id, metric_name in metrics:
            frame = ttk.Frame(self.metrics_container, style='Dark.TFrame')
            frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(frame, text=f"{metric_name}:", style='Metric.TLabel').pack(side=tk.LEFT)
            value_label = ttk.Label(frame, text="--", style='Metric.TLabel')
            value_label.pack(side=tk.RIGHT)
            
            self.metric_labels[metric_id] = value_label
    
    def create_visualization_panel(self, parent):
        """Create the visualization panel"""
        viz_frame = ttk.Frame(parent, style='Dark.TFrame')
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Visualization title
        ttk.Label(viz_frame, text="🎨 Visual Processes", style='Header.TLabel').pack(pady=(0, 10))
        
        # Available modules
        if self.available_modules:
            ttk.Label(viz_frame, text="Available Modules:", style='Dark.TLabel').pack(anchor=tk.W)
            
            # Create module list
            self.module_listbox = tk.Listbox(
                viz_frame,
                bg='#2a2a2a',
                fg='#ffffff',
                selectbackground='#404040',
                height=8,
                font=('Arial', 9)
            )
            self.module_listbox.pack(fill=tk.X, pady=(5, 10))
            
            # Populate module list
            for module_id, module_info in self.available_modules.items():
                self.module_listbox.insert(tk.END, f"📊 {module_info['name']}")
            
            # Generate button
            self.generate_button = tk.Button(
                viz_frame,
                text="Generate Visualization",
                bg='#404040',
                fg='#ffffff',
                command=self.generate_visualization,
                font=('Arial', 10)
            )
            self.generate_button.pack(pady=(0, 10))
        
        # Visualization display area
        self.viz_display = tk.Text(
            viz_frame,
            bg='#2a2a2a',
            fg='#ffffff',
            wrap=tk.WORD,
            font=('Consolas', 9),
            height=15
        )
        self.viz_display.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(viz_frame, orient=tk.VERTICAL, command=self.viz_display.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.viz_display.configure(yscrollcommand=scrollbar.set)
        
        # Initial message
        self.viz_display.insert(tk.END, "🎨 DAWN Visual Processes\n")
        self.viz_display.insert(tk.END, "=" * 40 + "\n\n")
        self.viz_display.insert(tk.END, "Select a module and click 'Generate Visualization'\n")
        self.viz_display.insert(tk.END, "to see real-time consciousness data.\n\n")
        
        if not self.available_modules:
            self.viz_display.insert(tk.END, "⚠️  No visual modules available\n")
            self.viz_display.insert(tk.END, "Running in demo mode with synthetic data.\n")
    
    def _on_data_update(self, data: Dict[str, Any]):
        """Callback for visual data updates"""
        self.current_data = data
        self.root.after(0, self.update_display)
    
    def update_display(self):
        """Update the display with current data"""
        if not self.current_data:
            return
        
        # Update metrics
        for metric_id, label in self.metric_labels.items():
            value = self.current_data.get(metric_id, '--')
            
            # Format the value
            if metric_id == 'scup':
                formatted_value = f"{value:.1f}%"
            elif metric_id == 'entropy':
                formatted_value = f"{value:.3f}"
            elif metric_id == 'heat':
                formatted_value = f"{value:.1f}°C"
            elif metric_id == 'active_sigils':
                formatted_value = f"{len(value)} active"
            elif metric_id == 'tracer_alerts':
                formatted_value = f"{len(value)} alerts"
            else:
                formatted_value = str(value)
            
            label.config(text=formatted_value)
        
        # Update status
        if self.visual_integration:
            self.status_label.config(text="🟢 Connected")
        else:
            self.status_label.config(text="🟡 Demo Mode")
    
    def generate_visualization(self):
        """Generate visualization for selected module"""
        if not self.available_modules:
            messagebox.showinfo("Info", "No visual modules available")
            return
        
        # Get selected module
        selection = self.module_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a module first")
            return
        
        selected_index = selection[0]
        module_id = list(self.available_modules.keys())[selected_index]
        module_info = self.available_modules[module_id]
        
        # Clear display
        self.viz_display.delete(1.0, tk.END)
        
        # Show generating message
        self.viz_display.insert(tk.END, f"🎨 Generating {module_info['name']}...\n")
        self.viz_display.insert(tk.END, "=" * 40 + "\n\n")
        
        # Generate visualization in background
        threading.Thread(target=self._generate_viz_background, args=(module_id,), daemon=True).start()
    
    def _generate_viz_background(self, module_id: str):
        """Generate visualization in background thread"""
        try:
            if self.visual_integration:
                result = self.visual_integration.generate_visualization(module_id, self.current_data)
            else:
                result = self._generate_demo_visualization(module_id)
            
            # Update display on main thread
            self.root.after(0, lambda: self._show_visualization_result(module_id, result))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_error(f"Error generating visualization: {e}"))
    
    def _generate_demo_visualization(self, module_id: str) -> str:
        """Generate demo visualization data"""
        import math
        
        current_time = time.time()
        
        if module_id == 'tick_pulse':
            return f"""
🔄 TICK PULSE VISUALIZATION
==========================
Current Time: {datetime.now().strftime('%H:%M:%S')}
Tick Number: {self.current_data.get('tick_number', 0)}
Pulse Rate: {60 + 20 * math.sin(current_time * 0.1):.1f} BPM
Amplitude: {0.5 + 0.3 * math.sin(current_time * 0.05):.2f}
Phase: {current_time * 0.1:.1f} rad

Pulse Pattern:
{'█' * int(10 + 5 * math.sin(current_time * 0.1))}
{'░' * (20 - int(10 + 5 * math.sin(current_time * 0.1)))}
"""
        
        elif module_id == 'consciousness_constellation':
            return f"""
🌌 CONSCIOUSNESS CONSTELLATION
=============================
SCUP Coordinates: ({self.current_data.get('scup', 0.5):.2f}, {self.current_data.get('entropy', 0.5):.2f})
Zone: {self.current_data.get('zone', 'CALM')}
Mood: {self.current_data.get('mood', 'neutral')}

Constellation Map:
    🌟 Dormant
       |
    🌟 Contemplative
       |
    🌟 Active ← Current Position
       |
    🌟 Intense
       |
    🌟 Transcendent
"""
        
        else:
            return f"""
📊 {module_id.upper().replace('_', ' ')} VISUALIZATION
{'=' * (len(module_id) + 15)}
Module: {module_id}
Status: Demo Mode
Data: {json.dumps(self.current_data, indent=2)}
"""
    
    def _show_visualization_result(self, module_id: str, result: Optional[str]):
        """Show visualization result in display"""
        self.viz_display.delete(1.0, tk.END)
        
        if result:
            self.viz_display.insert(tk.END, result)
        else:
            self.viz_display.insert(tk.END, f"❌ Failed to generate visualization for {module_id}")
    
    def _show_error(self, error_message: str):
        """Show error message in display"""
        self.viz_display.delete(1.0, tk.END)
        self.viz_display.insert(tk.END, f"❌ {error_message}")
    
    def start_updates(self):
        """Start the update loop"""
        self.is_running = True
        
        def update_loop():
            while self.is_running:
                try:
                    # Get current data
                    if VISUAL_INTEGRATION_AVAILABLE:
                        data = get_current_visual_data()
                        if data:
                            self.current_data = data
                            self.root.after(0, self.update_display)
                    
                    time.sleep(0.5)  # Update every 500ms
                    
                except Exception as e:
                    print(f"Update loop error: {e}")
                    time.sleep(1.0)
        
        self.update_thread = threading.Thread(target=update_loop, daemon=True)
        self.update_thread.start()
    
    def stop_updates(self):
        """Stop the update loop"""
        self.is_running = False
        if self.update_thread:
            self.update_thread.join(timeout=1.0)

def main():
    """Main function"""
    root = tk.Tk()
    app = DAWNVisualGUI(root)
    
    # Handle window close
    def on_closing():
        app.stop_updates()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main() 