#!/usr/bin/env python3
"""
DAWN Integrated Visual System - Professional Consciousness Visualization
======================================================================

Integrates the best existing visualization modules with beautiful charts:
- Tick Pulse: Real-time cognitive heartbeat
- Consciousness Constellation: 4D SCUP trajectory mapping  
- Heat Monitor: Cognitive intensity gauge
- Mood State: Emotional landscape heatmap
- Entropy Flow: Information stream vector field
- SCUP Pressure Grid: Cognitive pressure interactions

Uses matplotlib, seaborn, and plotly for stunning real-time visualizations.
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
    from matplotlib.patches import Circle, Wedge, FancyArrowPatch
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib.colors import LinearSegmentedColormap
    import seaborn as sns
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTTING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Some plotting libraries not available: {e}")
    print("   Install with: pip install matplotlib seaborn plotly pandas")
    PLOTTING_AVAILABLE = False

class DAWNIntegratedDataGenerator:
    """Integrated data generator with rich consciousness metrics"""
    
    def __init__(self):
        self.start_time = time.time()
        self.tick_counter = 0
        self.history = []
        self.max_history = 200
        
        # Set up beautiful plotting style
        if PLOTTING_AVAILABLE:
            plt.style.use('dark_background')
            sns.set_theme(style="darkgrid")
            sns.set_palette("husl")
    
    def generate_integrated_data(self) -> Dict[str, Any]:
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
        
        # SCUP components for pressure grid
        schema = 0.5 + 0.3 * math.sin(elapsed * 0.07)
        utility = 0.6 + 0.2 * math.sin(elapsed * 0.14)
        pressure = 0.4 + 0.4 * math.sin(elapsed * 0.06)
        
        # Pulse analysis
        pulse_amplitude = 0.5 + 0.3 * math.sin(elapsed * 0.1)
        pulse_frequency = 0.1 + 0.05 * math.sin(elapsed * 0.05)
        pulse_phase = elapsed * 0.1
        
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
            # SCUP components
            'schema': schema,
            'utility': utility,
            'pressure': pressure,
            # Pulse analysis
            'pulse_amplitude': pulse_amplitude,
            'pulse_frequency': pulse_frequency,
            'pulse_phase': pulse_phase,
            # Additional metrics
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

class DAWNIntegratedVisualizer:
    """Integrated visualization generator using existing modules as inspiration"""
    
    def __init__(self):
        self.data_generator = DAWNIntegratedDataGenerator()
        self.figures = {}
        self.canvases = {}
        
    def create_tick_pulse_visualization(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create tick pulse visualization inspired by existing module"""
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('🔄 DAWN Cognitive Heartbeat - Tick Pulse Monitor', fontsize=16, color='#00ff00')
        fig.patch.set_facecolor('#1a1a1a')
        
        # Extract time series data
        times = [d['elapsed_time'] for d in history[-50:]]
        scup_values = [d['scup'] for d in history[-50:]]
        entropy_values = [d['entropy'] for d in history[-50:]]
        pulse_amplitudes = [d['pulse_amplitude'] for d in history[-50:]]
        
        # 1. Main pulse line
        ax1.plot(times, pulse_amplitudes, color='#00ff00', linewidth=3, alpha=0.9, label='Cognitive Pulse')
        ax1.fill_between(times, pulse_amplitudes, alpha=0.3, color='#00ff00')
        ax1.set_xlabel('Time (s)', color='white')
        ax1.set_ylabel('Pulse Amplitude', color='white')
        ax1.set_title('Real-time Cognitive Pulse', color='#00ff00')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#2a2a2a')
        
        # 2. SCUP vs Entropy scatter
        ax2.scatter(entropy_values, scup_values, c=times, cmap='viridis', alpha=0.7, s=50)
        ax2.set_xlabel('Entropy', color='white')
        ax2.set_ylabel('SCUP', color='white')
        ax2.set_title('SCUP vs Entropy Space', color='#00ff00')
        ax2.grid(True, alpha=0.3)
        ax2.set_facecolor('#2a2a2a')
        
        # 3. Pulse frequency analysis
        frequencies = [d['pulse_frequency'] for d in history[-50:]]
        ax3.plot(times, frequencies, color='#ff6b6b', linewidth=2, alpha=0.8)
        ax3.fill_between(times, frequencies, alpha=0.3, color='#ff6b6b')
        ax3.set_xlabel('Time (s)', color='white')
        ax3.set_ylabel('Frequency (Hz)', color='white')
        ax3.set_title('Pulse Frequency Analysis', color='#00ff00')
        ax3.grid(True, alpha=0.3)
        ax3.set_facecolor('#2a2a2a')
        
        # 4. Current pulse indicator
        current_amplitude = data['pulse_amplitude']
        current_phase = data['pulse_phase']
        
        # Create circular pulse indicator
        theta = np.linspace(0, 2*np.pi, 100)
        radius = 0.5 + current_amplitude * 0.3
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        
        ax4.plot(x, y, color='#00ff00', linewidth=3, alpha=0.8)
        ax4.scatter([0], [0], color='#00ff00', s=100, alpha=0.9)
        ax4.set_xlim(-1, 1)
        ax4.set_ylim(-1, 1)
        ax4.set_aspect('equal')
        ax4.set_title(f'Current Pulse\nAmplitude: {current_amplitude:.2f}', color='#00ff00')
        ax4.set_facecolor('#2a2a2a')
        ax4.axis('off')
        
        plt.tight_layout()
        return fig
    
    def create_consciousness_constellation(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create consciousness constellation visualization"""
        
        # Create 3D figure
        fig = plt.figure(figsize=(12, 8))
        fig.patch.set_facecolor('#1a1a1a')
        
        ax = fig.add_subplot(111, projection='3d')
        
        # Extract SCUP coordinates
        if len(history) >= 20:
            scup_values = [d['scup'] for d in history[-20:]]
            entropy_values = [d['entropy'] for d in history[-20:]]
            coherence_values = [d['coherence'] for d in history[-20:]]
            
            # Create 3D trajectory
            ax.plot(scup_values, entropy_values, coherence_values, 
                   color='#00ff00', linewidth=3, alpha=0.8)
            
            # Add trajectory points
            ax.scatter(scup_values, entropy_values, coherence_values, 
                      c=range(len(scup_values)), cmap='viridis', s=50, alpha=0.8)
            
            # Add current position
            ax.scatter([data['scup']], [data['entropy']], [data['coherence']], 
                      color='#ff0000', s=200, alpha=0.9, marker='*')
        
        ax.set_xlabel('SCUP', color='white')
        ax.set_ylabel('Entropy', color='white')
        ax.set_zlabel('Coherence', color='white')
        ax.set_title('🌌 Consciousness Constellation - 3D SCUP Trajectory', color='#00ff00', fontsize=14)
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.zaxis.label.set_color('white')
        ax.tick_params(colors='white')
        
        return fig
    
    def create_heat_monitor(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create heat monitor visualization"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor('#1a1a1a')
        fig.suptitle('🌡️ DAWN Cognitive Heat Monitor', fontsize=16, color='#00ff00')
        
        # 1. Radial gauge
        heat = data['heat']
        heat_normalized = max(0.0, min(1.0, (heat - 20.0) / 30.0))
        
        # Create gauge
        theta = np.linspace(0, 2*np.pi, 100)
        radius = 1.0
        
        # Gauge background
        ax1.plot(radius * np.cos(theta), radius * np.sin(theta), 'w-', linewidth=3, alpha=0.3)
        
        # Heat indicator
        heat_angle = heat_normalized * 2 * np.pi
        heat_x = radius * np.cos(heat_angle)
        heat_y = radius * np.sin(heat_angle)
        
        # Color based on heat level
        if heat_normalized < 0.3:
            color = '#0066cc'  # Blue
        elif heat_normalized < 0.6:
            color = '#00ff88'  # Green
        elif heat_normalized < 0.8:
            color = '#ffaa00'  # Orange
        else:
            color = '#ff3300'  # Red
        
        ax1.plot([0, heat_x], [0, heat_y], color=color, linewidth=8, alpha=0.8)
        ax1.scatter([heat_x], [heat_y], color=color, s=200, alpha=0.9)
        
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-1.2, 1.2)
        ax1.set_aspect('equal')
        ax1.set_title(f'Current Heat: {heat:.1f}°C', color='#00ff00')
        ax1.set_facecolor('#2a2a2a')
        ax1.axis('off')
        
        # 2. Heat timeline
        if len(history) >= 20:
            times = [d['elapsed_time'] for d in history[-20:]]
            heats = [d['heat'] for d in history[-20:]]
            
            ax2.plot(times, heats, color='#ff6b6b', linewidth=2, alpha=0.8)
            ax2.fill_between(times, heats, alpha=0.3, color='#ff6b6b')
            ax2.set_xlabel('Time (s)', color='white')
            ax2.set_ylabel('Heat (°C)', color='white')
            ax2.set_title('Heat Timeline', color='#00ff00')
            ax2.grid(True, alpha=0.3)
            ax2.set_facecolor('#2a2a2a')
        
        plt.tight_layout()
        return fig
    
    def create_mood_state_heatmap(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create mood state heatmap visualization"""
        
        # Create mood dimensions (8x8 grid)
        mood_dimensions = [
            ['Transcendent', 'Luminous', 'Expansive', 'Crystalline', 'Ethereal', 'Radiant', 'Sublime', 'Infinite'],
            ['Ecstatic', 'Euphoric', 'Jubilant', 'Vivacious', 'Exuberant', 'Buoyant', 'Elated', 'Rapturous'],
            ['Serene', 'Peaceful', 'Harmonious', 'Balanced', 'Centered', 'Tranquil', 'Calm', 'Composed'],
            ['Curious', 'Inquisitive', 'Wonder', 'Fascinated', 'Intrigued', 'Exploratory', 'Seeking', 'Questioning'],
            ['Focused', 'Attentive', 'Concentrated', 'Sharp', 'Alert', 'Vigilant', 'Acute', 'Precise'],
            ['Contemplative', 'Reflective', 'Meditative', 'Pensive', 'Introspective', 'Thoughtful', 'Deep', 'Brooding'],
            ['Uncertain', 'Hesitant', 'Ambiguous', 'Doubtful', 'Questioning', 'Unsure', 'Wavering', 'Conflicted'],
            ['Turbulent', 'Chaotic', 'Fragmented', 'Unstable', 'Volatile', 'Scattered', 'Dissonant', 'Entropic']
        ]
        
        # Generate mood matrix based on current state
        mood_matrix = np.zeros((8, 8))
        current_time = time.time()
        
        for i in range(8):
            for j in range(8):
                # Create oscillating mood intensities
                base_intensity = 0.3 + 0.4 * math.sin(current_time * 0.1 + i * 0.5 + j * 0.3)
                mood_matrix[i, j] = max(0.0, min(1.0, base_intensity))
        
        # Create custom colormap
        colors = ['#0a0a0a', '#1a1a2e', '#16213e', '#0f3460', '#533483', 
                 '#7209b7', '#a663cc', '#4cc9f0', '#7209b7', '#f72585']
        mood_cmap = LinearSegmentedColormap.from_list('mood', colors, N=256)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        fig.patch.set_facecolor('#1a1a1a')
        
        # Create heatmap
        im = ax.imshow(mood_matrix, cmap=mood_cmap, aspect='equal', vmin=0, vmax=1)
        
        # Setup axis labels
        ax.set_xticks(range(8))
        ax.set_yticks(range(8))
        ax.set_xticklabels([row[0][:8] for row in mood_dimensions], 
                          rotation=45, ha='right', fontsize=9, color='#cccccc')
        ax.set_yticklabels([f"{i+1}" for i in range(8)], 
                          fontsize=9, color='#cccccc')
        
        # Add cell labels
        for i in range(8):
            for j in range(8):
                text = ax.text(j, i, mood_dimensions[i][j][:6], 
                              ha='center', va='center', fontsize=7, 
                              color='white', weight='bold')
        
        ax.set_title('😊 DAWN Emotional Landscape - Mood State Heatmap', 
                    fontsize=16, color='#ffffff', pad=20, weight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, shrink=0.8)
        cbar.set_label('Affective Intensity', rotation=270, labelpad=20, 
                      color='#cccccc', fontsize=12)
        cbar.ax.tick_params(colors='#cccccc')
        
        plt.tight_layout()
        return fig
    
    def create_scup_pressure_grid(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create SCUP pressure grid visualization"""
        
        # Extract SCUP components
        schema = data['schema']
        coherence = data['coherence']
        utility = data['utility']
        pressure = data['pressure']
        
        # Create 4x4 pressure matrix
        pressure_matrix = np.zeros((4, 4))
        
        # Diagonal elements (self-pressure)
        pressure_matrix[0, 0] = schema
        pressure_matrix[1, 1] = coherence
        pressure_matrix[2, 2] = utility
        pressure_matrix[3, 3] = pressure
        
        # Off-diagonal elements (interactions)
        pressure_matrix[0, 1] = schema * coherence  # Schema-Coherence
        pressure_matrix[0, 2] = schema * utility    # Schema-Utility
        pressure_matrix[0, 3] = schema * pressure   # Schema-Pressure
        pressure_matrix[1, 2] = coherence * utility # Coherence-Utility
        pressure_matrix[1, 3] = coherence * pressure # Coherence-Pressure
        pressure_matrix[2, 3] = utility * pressure  # Utility-Pressure
        
        # Symmetric matrix
        pressure_matrix[1, 0] = pressure_matrix[0, 1]
        pressure_matrix[2, 0] = pressure_matrix[0, 2]
        pressure_matrix[3, 0] = pressure_matrix[0, 3]
        pressure_matrix[2, 1] = pressure_matrix[1, 2]
        pressure_matrix[3, 1] = pressure_matrix[1, 3]
        pressure_matrix[3, 2] = pressure_matrix[2, 3]
        
        # Create custom colormap
        colors = ['#001f3f', '#0074D9', '#39CCCC', '#3D9970', 
                  '#FFDC00', '#FF851B', '#FF4136', '#85144b']
        cmap = LinearSegmentedColormap.from_list('pressure', colors, N=100)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor('#1a1a1a')
        fig.suptitle('📊 SCUP Pressure Grid - Cognitive Pressure Interactions', fontsize=16, color='#00ff00')
        
        # 1. Pressure grid heatmap
        im = ax1.imshow(pressure_matrix, cmap=cmap, aspect='equal', vmin=0, vmax=1)
        
        # Add labels
        dimensions = ['Schema', 'Coherence', 'Utility', 'Pressure']
        ax1.set_xticks(range(4))
        ax1.set_yticks(range(4))
        ax1.set_xticklabels(dimensions, color='white')
        ax1.set_yticklabels(dimensions, color='white')
        
        # Add text annotations
        for i in range(4):
            for j in range(4):
                text = ax1.text(j, i, f'{pressure_matrix[i, j]:.2f}', 
                               ha='center', va='center', fontsize=10, 
                               color='white', weight='bold')
        
        ax1.set_title('Pressure Interaction Matrix', color='#00ff00')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax1, shrink=0.8)
        cbar.set_label('Pressure Level', color='#cccccc')
        cbar.ax.tick_params(colors='#cccccc')
        
        # 2. Component bars
        components = ['Schema', 'Coherence', 'Utility', 'Pressure']
        values = [schema, coherence, utility, pressure]
        colors = ['#0074D9', '#39CCCC', '#3D9970', '#FF4136']
        
        bars = ax2.bar(components, values, color=colors, alpha=0.8)
        ax2.set_ylabel('Value', color='white')
        ax2.set_title('SCUP Components', color='#00ff00')
        ax2.set_facecolor('#2a2a2a')
        ax2.tick_params(colors='white')
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.2f}', ha='center', va='bottom', color='white')
        
        plt.tight_layout()
        return fig
    
    def create_entropy_flow_visualization(self, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create entropy flow visualization"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.patch.set_facecolor('#1a1a1a')
        fig.suptitle('⚡ DAWN Entropy Flow - Information Streams', fontsize=16, color='#00ff00')
        
        # Create flow field
        grid_size = 12
        x = np.linspace(-6, 6, grid_size)
        y = np.linspace(-6, 6, grid_size)
        X, Y = np.meshgrid(x, y)
        
        # Calculate flow vectors based on current state
        current_time = time.time()
        U = np.sin(X + current_time * 0.1) * data['entropy']
        V = np.cos(Y + current_time * 0.1) * data['coherence']
        
        # 1. Vector field
        ax1.quiver(X, Y, U, V, alpha=0.8, scale=20, scale_units='xy', 
                  angles='xy', width=0.003, cmap='plasma')
        ax1.set_xlabel('X', color='white')
        ax1.set_ylabel('Y', color='white')
        ax1.set_title('Information Flow Field', color='#00ff00')
        ax1.set_facecolor('#2a2a2a')
        ax1.grid(True, alpha=0.3)
        
        # 2. Flow metrics
        if len(history) >= 20:
            times = [d['elapsed_time'] for d in history[-20:]]
            entropy_values = [d['entropy'] for d in history[-20:]]
            coherence_values = [d['coherence'] for d in history[-20:]]
            
            ax2.plot(times, entropy_values, color='#ff6b6b', linewidth=2, alpha=0.8, label='Entropy')
            ax2.plot(times, coherence_values, color='#4ecdc4', linewidth=2, alpha=0.8, label='Coherence')
            ax2.set_xlabel('Time (s)', color='white')
            ax2.set_ylabel('Value', color='white')
            ax2.set_title('Flow Metrics', color='#00ff00')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.set_facecolor('#2a2a2a')
        
        plt.tight_layout()
        return fig
    
    def create_visualization(self, module_id: str, data: Dict[str, Any], history: List[Dict[str, Any]]) -> plt.Figure:
        """Create visualization for any module"""
        if module_id == 'tick_pulse':
            return self.create_tick_pulse_visualization(data, history)
        elif module_id == 'consciousness_constellation':
            return self.create_consciousness_constellation(data, history)
        elif module_id == 'heat_monitor':
            return self.create_heat_monitor(data, history)
        elif module_id == 'mood_state':
            return self.create_mood_state_heatmap(data, history)
        elif module_id == 'scup_pressure_grid':
            return self.create_scup_pressure_grid(data, history)
        elif module_id == 'entropy_flow':
            return self.create_entropy_flow_visualization(data, history)
        else:
            return self.create_tick_pulse_visualization(data, history)  # Default

class DAWNIntegratedGUI:
    """Integrated GUI with professional charts and graphs"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🌅 DAWN Integrated Visual System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#1a1a1a')
        
        # Initialize components
        self.data_generator = DAWNIntegratedDataGenerator()
        self.visualizer = DAWNIntegratedVisualizer()
        
        # State
        self.current_data = None
        self.selected_visualization = 'tick_pulse'
        self.auto_update = True
        self.is_running = False
        
        # Available visualizations (inspired by existing modules)
        self.visualizations = {
            'tick_pulse': '🔄 Tick Pulse Monitor',
            'consciousness_constellation': '🌌 Consciousness Constellation', 
            'heat_monitor': '🌡️ Heat Monitor',
            'mood_state': '😊 Mood State Heatmap',
            'scup_pressure_grid': '📊 SCUP Pressure Grid',
            'entropy_flow': '⚡ Entropy Flow'
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
            text="🌅 DAWN Integrated Visual System", 
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
        
        self.viz_var = tk.StringVar(value='tick_pulse')
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
            text="🎨 Integrated Visualizations",
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
            
            # Create new visualization
            self.fig = self.visualizer.create_visualization(
                self.selected_visualization, 
                self.current_data, 
                self.data_generator.history
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
                self.current_data = self.data_generator.generate_integrated_data()
                
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
    print("🌅 DAWN Integrated Visual System")
    print("=" * 40)
    print("🚀 Starting integrated visualization system...")
    print(f"📊 Plotting libraries: {'✅ Available' if PLOTTING_AVAILABLE else '⚠️ Limited'}")
    print("✅ Professional charts and graphs")
    print("✅ Real-time data visualization")
    print("✅ Integrated consciousness monitoring")
    print()
    
    if not PLOTTING_AVAILABLE:
        print("⚠️  Install plotting libraries for full functionality:")
        print("   pip install matplotlib seaborn plotly pandas")
        print()
    
    root = tk.Tk()
    app = DAWNIntegratedGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down integrated visual system...")
    finally:
        app.stop_data_generation()
        print("✅ Integrated visual system stopped")

if __name__ == "__main__":
    main() 