# Add parent directory to Python path for imports
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Visual Local - 100% Self-Contained Visual System
======================================================

A completely local, zero-dependency visual system that can run:
- Underwater
- In space  
- Offline
- Without any external servers
- Without any network connections

Pure Python with built-in GUI using tkinter.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import math
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
import queue

class DAWNLocalVisualData:
    """Local data generator - no external dependencies"""
    
    def __init__(self):
        self.start_time = time.time()
        self.tick_counter = 0
        self.last_update = 0
        
    def generate_local_data(self) -> Dict[str, Any]:
        """Generate synthetic consciousness data locally"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Oscillating consciousness metrics
        scup = 0.5 + 0.3 * math.sin(elapsed * 0.1)
        entropy = 0.4 + 0.4 * math.sin(elapsed * 0.08)
        heat = 25.0 + 10.0 * math.sin(elapsed * 0.05)
        
        # Zone cycling
        zones = ['CALM', 'STABLE', 'OSCILLATING', 'TRENDING', 'ACTIVE']
        zone = zones[int(elapsed) % len(zones)]
        
        # Mood cycling
        moods = ['serene', 'focused', 'curious', 'contemplative', 'energetic']
        mood = moods[int(elapsed * 0.5) % len(moods)]
        
        # Sigil activity
        sigil_phases = int(elapsed * 0.3) % 4
        active_sigils = ['attention', 'memory'] if sigil_phases == 0 else []
        
        # Rebloom cycles
        rebloom_count = int(elapsed * 0.2) % 5
        
        # Tracer alerts
        alert_phase = int(elapsed * 0.1) % 10
        tracer_alerts = ['pressure_warning'] if alert_phase == 0 else []
        
        self.tick_counter += 1
        
        return {
            'tick_number': self.tick_counter,
            'timestamp': current_time,
            'scup': max(0.0, min(1.0, scup)),
            'entropy': max(0.0, min(1.0, entropy)),
            'heat': max(20.0, min(50.0, heat)),
            'zone': zone,
            'mood': mood,
            'active_sigils': active_sigils,
            'rebloom_count': rebloom_count,
            'tracer_alerts': tracer_alerts,
            'elapsed_time': elapsed
        }

class DAWNLocalVisualGenerator:
    """Local visualization generator - no external dependencies"""
    
    def __init__(self):
        self.data_generator = DAWNLocalVisualData()
        
    def generate_tick_pulse_visualization(self, data: Dict[str, Any]) -> str:
        """Generate tick pulse visualization"""
        current_time = time.time()
        timestamp = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
        
        # Calculate pulse metrics
        amplitude = 0.5 + 0.3 * math.sin(current_time * 0.1)
        frequency = 0.1 + 0.05 * math.sin(current_time * 0.05)
        phase = current_time * 0.1
        
        # Visual representation
        visual_bars = int(10 + 5 * math.sin(current_time * 0.1))
        visual_empty = 20 - visual_bars
        
        return f"""
TICK PULSE VISUALIZATION
==========================
Time: {timestamp}
Module: Tick Pulse (Local)
Description: Real-time cognitive heartbeat visualization

Current State:
  Tick Number: {data['tick_number']}
  SCUP: {data['scup']:.3f}
  Entropy: {data['entropy']:.3f}
  Heat: {data['heat']:.1f}C
  Zone: {data['zone']}
  Mood: {data['mood']}

Pulse Analysis:
  Amplitude: {amplitude:.2f}
  Frequency: {frequency:.3f} Hz
  Phase: {phase:.1f} rad

Visual Representation:
{'#' * visual_bars}
{'.' * visual_empty}

Status: LOCAL MODE - No external dependencies
"""
    
    def generate_consciousness_constellation(self, data: Dict[str, Any]) -> str:
        """Generate consciousness constellation visualization"""
        current_time = time.time()
        timestamp = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
        
        # Calculate constellation position
        scup_pos = int(data['scup'] * 5)
        trajectory = ['NE', 'E', 'SE', 'SW', 'W', 'NW'][int(current_time) % 6]
        
        return f"""
CONSCIOUSNESS CONSTELLATION
==============================
Time: {timestamp}
Module: Consciousness Constellation (Local)
Description: 3D SCUP trajectory visualization

SCUP Space Coordinates:
  Schema: {data['scup']:.3f}
  Coherence: {data['entropy']:.3f}
  Utility: {1.0 - data['entropy']:.3f}

Current Position:
  Zone: {data['zone']}
  Mood: {data['mood']}
  Heat: {data['heat']:.1f}C

Constellation Map:
    * Dormant (0.0-0.2)
       |
    * Contemplative (0.2-0.4)
       |
    * Active (0.4-0.6) <- Current
       |
    * Intense (0.6-0.8)
       |
    * Transcendent (0.8-1.0)

Trajectory: {trajectory}

Status: LOCAL MODE - Self-contained operation
"""
    
    def generate_heat_monitor(self, data: Dict[str, Any]) -> str:
        """Generate heat monitor visualization"""
        current_time = time.time()
        timestamp = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
        
        heat = data['heat']
        heat_normalized = max(0.0, min(1.0, (heat - 20.0) / 30.0))
        
        # Calculate heat zone bars
        dormant_bars = int(5 * (1.0 - heat_normalized))
        warming_bars = int(5 * max(0, heat_normalized - 0.2))
        active_bars = int(5 * max(0, heat_normalized - 0.4))
        intense_bars = int(5 * max(0, heat_normalized - 0.6))
        critical_bars = int(5 * max(0, heat_normalized - 0.8))
        
        current_zone = ['Dormant', 'Warming', 'Active', 'Intense', 'Critical'][min(4, int(heat_normalized * 5))]
        
        return f"""
HEAT MONITOR VISUALIZATION
=============================
Time: {timestamp}
Module: Heat Monitor (Local)
Description: Cognitive heat intensity gauge

Current Heat: {heat:.1f}C
Heat Level: {heat_normalized:.1f} (0.0-1.0)

Heat Zones:
  Dormant (20-25C): {'#' * dormant_bars}{'.' * (5 - dormant_bars)}
  Warming (25-30C): {'#' * warming_bars}{'.' * (5 - warming_bars)}
  Active (30-35C): {'#' * active_bars}{'.' * (5 - active_bars)}
  Intense (35-40C): {'#' * intense_bars}{'.' * (5 - intense_bars)}
  Critical (40-50C): {'#' * critical_bars}{'.' * (5 - critical_bars)}

Current Zone: {current_zone}

Status: LOCAL MODE - Independent operation
"""
    
    def generate_mood_state(self, data: Dict[str, Any]) -> str:
        """Generate mood state visualization"""
        current_time = time.time()
        timestamp = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
        
        # Calculate mood landscape
        transcendent_bars = int(3 * math.sin(current_time * 0.1 + 0))
        ecstatic_bars = int(3 * math.sin(current_time * 0.1 + 1))
        serene_bars = int(3 * math.sin(current_time * 0.1 + 2))
        curious_bars = int(3 * math.sin(current_time * 0.1 + 3))
        focused_bars = int(3 * math.sin(current_time * 0.1 + 4))
        contemplative_bars = int(3 * math.sin(current_time * 0.1 + 5))
        uncertain_bars = int(3 * math.sin(current_time * 0.1 + 6))
        turbulent_bars = int(3 * math.sin(current_time * 0.1 + 7))
        
        return f"""
MOOD STATE VISUALIZATION
===========================
Time: {timestamp}
Module: Mood State (Local)
Description: Emotional landscape heatmap

Current Mood: {data['mood']}
Zone: {data['zone']}

Emotional Landscape:
  Transcendent: {'#' * transcendent_bars}{'.' * (10 - transcendent_bars)}
  Ecstatic: {'#' * ecstatic_bars}{'.' * (10 - ecstatic_bars)}
  Serene: {'#' * serene_bars}{'.' * (10 - serene_bars)}
  Curious: {'#' * curious_bars}{'.' * (10 - curious_bars)}
  Focused: {'#' * focused_bars}{'.' * (10 - focused_bars)}
  Contemplative: {'#' * contemplative_bars}{'.' * (10 - contemplative_bars)}
  Uncertain: {'#' * uncertain_bars}{'.' * (10 - uncertain_bars)}
  Turbulent: {'#' * turbulent_bars}{'.' * (10 - turbulent_bars)}

Status: LOCAL MODE - Self-sustaining
"""
    
    def generate_visualization(self, module_id: str, data: Dict[str, Any]) -> str:
        """Generate visualization for any module"""
        if module_id == 'tick_pulse':
            return self.generate_tick_pulse_visualization(data)
        elif module_id == 'consciousness_constellation':
            return self.generate_consciousness_constellation(data)
        elif module_id == 'heat_monitor':
            return self.generate_heat_monitor(data)
        elif module_id == 'dawn_mood_state':
            return self.generate_mood_state(data)
        else:
            return self.generate_generic_visualization(module_id, data)
    
    def generate_generic_visualization(self, module_id: str, data: Dict[str, Any]) -> str:
        """Generate generic visualization for unknown modules"""
        current_time = time.time()
        timestamp = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
        
        return f"""
{module_id.upper().replace('_', ' ')} VISUALIZATION
{'=' * (len(module_id) + 15)}
Time: {timestamp}
Module: {module_id.title()} (Local)
Description: Local consciousness visualization

Current Data:
  Tick: {data['tick_number']}
  SCUP: {data['scup']:.3f}
  Entropy: {data['entropy']:.3f}
  Heat: {data['heat']:.1f}C
  Zone: {data['zone']}
  Mood: {data['mood']}
  Active Sigils: {len(data['active_sigils'])}
  Rebloom Count: {data['rebloom_count']}
  Tracer Alerts: {len(data['tracer_alerts'])}

Status: LOCAL MODE - Independent operation
Elapsed Time: {data['elapsed_time']:.1f}s
"""

class DAWNLocalVisualGUI:
    """100% Local DAWN Visual GUI - No external dependencies"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌅 DAWN Visual Processes - LOCAL MODE")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Local components
        self.data_generator = DAWNLocalVisualData()
        self.visual_generator = DAWNLocalVisualGenerator()
        
        # State
        self.current_data = None
        self.selected_module = 'tick_pulse'
        self.auto_update = True
        self.is_running = False
        
        # Available modules
        self.available_modules = {
            'tick_pulse': 'Tick Pulse',
            'consciousness_constellation': 'Consciousness Constellation', 
            'heat_monitor': 'Heat Monitor',
            'dawn_mood_state': 'Mood State'
        }
        
        self.setup_gui()
        self.start_data_generation()
    
    def setup_gui(self):
        """Setup the GUI components"""
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
            text="🌅 DAWN Visual Processes - LOCAL MODE", 
            font=('Consolas', 16, 'bold'),
            fg='#00ff00',
            bg='#1a1a1a'
        )
        title_label.pack(side=tk.LEFT)
        
        status_label = tk.Label(
            header_frame,
            text="🟢 LOCAL OPERATION - NO EXTERNAL DEPENDENCIES",
            font=('Consolas', 10),
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
        
        # Module selection
        tk.Label(
            controls_frame,
            text="Module:",
            fg='#ffffff',
            bg='#2a2a2a',
            font=('Consolas', 10)
        ).pack(side=tk.LEFT, padx=(20, 5), pady=5)
        
        self.module_var = tk.StringVar(value='tick_pulse')
        module_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.module_var,
            values=list(self.available_modules.values()),
            state='readonly',
            width=25
        )
        module_combo.pack(side=tk.LEFT, padx=5, pady=5)
        module_combo.bind('<<ComboboxSelected>>', self.on_module_change)
        
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
            ('sigils', '🔮 Sigils'),
            ('rebloom', '🌸 Rebloom'),
            ('alerts', '⚡ Alerts')
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
        viz_frame = tk.Frame(content_frame, bg='#2a2a2a', relief=tk.RAISED, bd=1)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(
            viz_frame,
            text="🎨 Visualization Output",
            font=('Consolas', 12, 'bold'),
            fg='#00ff00',
            bg='#2a2a2a'
        ).pack(pady=10)
        
        # Visualization text area
        self.viz_text = scrolledtext.ScrolledText(
            viz_frame,
            bg='#000000',
            fg='#00ff00',
            font=('Consolas', 9),
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0
        )
        self.viz_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
    
    def toggle_auto_update(self):
        """Toggle auto update"""
        self.auto_update = self.auto_update_var.get()
        if self.auto_update:
            self.start_data_generation()
        else:
            self.stop_data_generation()
    
    def on_module_change(self, event):
        """Handle module selection change"""
        selected = self.module_var.get()
        for key, value in self.available_modules.items():
            if value == selected:
                self.selected_module = key
                break
        self.refresh_visualization()
    
    def refresh_visualization(self):
        """Refresh the visualization"""
        if self.current_data:
            self.update_visualization()
    
    def update_metrics(self, data):
        """Update metrics display"""
        self.metrics_labels['tick'].config(text=str(data['tick_number']))
        self.metrics_labels['scup'].config(text=f"{data['scup']:.3f}")
        self.metrics_labels['entropy'].config(text=f"{data['entropy']:.3f}")
        self.metrics_labels['heat'].config(text=f"{data['heat']:.1f}°C")
        self.metrics_labels['zone'].config(text=data['zone'])
        self.metrics_labels['mood'].config(text=data['mood'])
        self.metrics_labels['sigils'].config(text=f"{len(data['active_sigils'])} active")
        self.metrics_labels['rebloom'].config(text=str(data['rebloom_count']))
        self.metrics_labels['alerts'].config(text=f"{len(data['tracer_alerts'])} alerts")
    
    def update_visualization(self):
        """Update visualization display"""
        if not self.current_data:
            return
        
        try:
            visualization = self.visual_generator.generate_visualization(
                self.selected_module, 
                self.current_data
            )
            
            self.viz_text.delete(1.0, tk.END)
            self.viz_text.insert(1.0, visualization)
            
        except Exception as e:
            error_msg = f"Error generating visualization: {str(e)}"
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
                self.current_data = self.data_generator.generate_local_data()
                
                # Update GUI in main thread
                self.root.after(0, self.update_metrics, self.current_data)
                if self.auto_update:
                    self.root.after(0, self.update_visualization)
                
                # Wait for next update
                time.sleep(2.0)
                
            except Exception as e:
                print(f"Data generation error: {e}")
                time.sleep(1.0)

def main():
    """Main function"""
    print("🌅 DAWN Local Visual System")
    print("=" * 40)
    print("🚀 Starting 100% local visual system...")
    print("✅ No external dependencies required")
    print("✅ Can run underwater, in space, or offline")
    print("✅ Pure Python with built-in tkinter GUI")
    print()
    
    root = tk.Tk()
    app = DAWNLocalVisualGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down local visual system...")
    finally:
        app.stop_data_generation()
        print("✅ Local visual system stopped")

if __name__ == "__main__":
    main() 