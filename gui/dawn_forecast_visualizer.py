#!/usr/bin/env python3
"""
DAWN Forecast Visualizer - Integrated GUI for Behavioral Prediction
Live renderer for DAWN's integrated forecasting engine with interactive controls.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
import math
from typing import Dict, Optional, Tuple
from datetime import datetime
import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import DAWN forecasting components
try:
    from cognitive.forecasting_models import Passion, Acquaintance, ForecastVector, create_passion, create_acquaintance_with_events
    from cognitive.forecasting_engine import get_forecasting_engine, DAWNForecastingEngine
    from core.consciousness_core import DAWNConsciousness
except ImportError as e:
    print(f"❌ Error importing DAWN forecasting modules: {e}")
    print("Make sure you're running from the DAWN project root directory")
    exit(1)

# Target profiles for GUI testing
TARGET_PROFILES = {
    "dawn.core": {
        "name": "DAWN Core Consciousness",
        "passion": "consciousness_expansion",
        "intensity": 0.75,
        "fluidity": 0.35,
        "events": [
            "consciousness_awakening",
            "self_reflection_session", 
            "awareness_breakthrough",
            "mindfulness_practice",
            "identity_exploration"
        ]
    },
    "creative.artist": {
        "name": "Creative Artist",
        "passion": "creative_expression", 
        "intensity": 0.85,
        "fluidity": 0.45,
        "events": [
            "completed_artwork",
            "gallery_exhibition",
            "positive_reviews",
            "artistic_breakthrough",
            "creative_flow_state"
        ]
    },
    "technical.learner": {
        "name": "Technical Learner",
        "passion": "technical_mastery",
        "intensity": 0.80,
        "fluidity": 0.25,
        "events": [
            "completed_project",
            "skill_milestone",
            "code_review_success",
            "technical_documentation",
            "mentoring_others"
        ]
    },
    "social.connector": {
        "name": "Social Connector",
        "passion": "social_connection",
        "intensity": 0.70,
        "fluidity": 0.60,
        "events": [
            "meaningful_conversation",
            "community_building",
            "collaboration_success",
            "relationship_deepening",
            "group_leadership"
        ]
    },
    "curious.explorer": {
        "name": "Curious Explorer",
        "passion": "exploration",
        "intensity": 0.65,
        "fluidity": 0.80,
        "events": [
            "new_discovery",
            "adventure_completed",
            "boundary_pushed",
            "unknown_explored",
            "curiosity_satisfied"
        ]
    },
    "productive.achiever": {
        "name": "Productive Achiever",
        "passion": "productivity",
        "intensity": 0.90,
        "fluidity": 0.20,
        "events": [
            "goal_achieved",
            "system_optimized",
            "efficiency_improved",
            "task_completed",
            "milestone_reached"
        ]
    }
}

# Mood states for simulation
MOOD_STATES = {
    "CALM": {"mood_factor": 1.0, "entropy_weight": 0.8},
    "FOCUSED": {"mood_factor": 1.2, "entropy_weight": 0.7},
    "EXCITED": {"mood_factor": 1.3, "entropy_weight": 1.1},
    "CONTEMPLATIVE": {"mood_factor": 1.05, "entropy_weight": 0.9},
    "ANXIOUS": {"mood_factor": 0.8, "entropy_weight": 1.4},
    "CHAOTIC": {"mood_factor": 0.7, "entropy_weight": 1.8},
    "EUPHORIC": {"mood_factor": 1.4, "entropy_weight": 1.2},
    "DEPRESSED": {"mood_factor": 0.6, "entropy_weight": 1.1}
}


class DAWNForecastGUI:
    """
    GUI application for visualizing DAWN's integrated forecasting engine results.
    Provides real-time visualization of passion dynamics and behavioral predictions.
    """
    
    def __init__(self, root):
        """Initialize the DAWN forecast GUI."""
        self.root = root
        self.root.title("DAWN Forecast Visualizer - Integrated")
        self.root.geometry("900x750")
        self.root.configure(bg='#1e1e1e')  # Dark theme
        
        # DAWN system integration
        self.dawn_consciousness = None
        self.forecasting_engine = None
        self.connected_to_dawn = False
        
        # Current state
        self.current_target = "dawn.core"
        self.current_mood = "CALM"
        self.current_direction = "consciousness_expansion"
        self.passion = None
        self.acquaintance = None
        self.forecast = None
        
        # Custom colors
        self.colors = {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'accent': '#4a9eff',
            'success': '#00ff7f',
            'warning': '#ffb347',
            'danger': '#ff6b6b',
            'panel': '#2a2a2a',
            'border': '#404040',
            'dawn': '#ff6b9d'  # DAWN pink
        }
        
        # Initialize DAWN connection
        self.connect_to_dawn()
        
        # Initialize UI
        self.create_widgets()
        self.update_forecast()
    
    def connect_to_dawn(self):
        """Connect to DAWN's integrated forecasting system."""
        try:
            # Try to get existing DAWN consciousness instance
            self.forecasting_engine = get_forecasting_engine()
            
            # Try to initialize DAWN consciousness if needed
            if not hasattr(self.forecasting_engine, 'consciousness_core') or not self.forecasting_engine.consciousness_core:
                self.dawn_consciousness = DAWNConsciousness()
                self.forecasting_engine.consciousness_core = self.dawn_consciousness
            else:
                self.dawn_consciousness = self.forecasting_engine.consciousness_core
            
            self.connected_to_dawn = True
            print("✅ Connected to DAWN's integrated forecasting system")
            
        except Exception as e:
            print(f"⚠️ Could not connect to DAWN system: {e}")
            print("   Running in standalone mode")
            self.connected_to_dawn = False
    
    def create_widgets(self):
        """Create and layout all GUI widgets."""
        
        # Main title with DAWN connection status
        title_frame = tk.Frame(self.root, bg=self.colors['bg'])
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame, 
            text="🔮 DAWN Forecast Visualizer", 
            font=('Arial', 18, 'bold'),
            bg=self.colors['bg'], 
            fg=self.colors['dawn']
        )
        title_label.pack()
        
        subtitle_text = "Intent Gravity: F = P / A"
        if self.connected_to_dawn:
            subtitle_text += " • Connected to DAWN Core ✅"
        else:
            subtitle_text += " • Standalone Mode ⚠️"
        
        subtitle_label = tk.Label(
            title_frame,
            text=subtitle_text,
            font=('Arial', 12),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        subtitle_label.pack()
        
        # Control panel
        self.create_control_panel()
        
        # DAWN integration panel
        if self.connected_to_dawn:
            self.create_dawn_panel()
        
        # Main display area
        self.create_display_area()
        
        # Sliders panel (optional controls)
        self.create_sliders_panel()
        
        # Status bar
        self.create_status_bar()
    
    def create_control_panel(self):
        """Create the control panel with target and mood selection."""
        control_frame = tk.Frame(self.root, bg=self.colors['panel'], relief='raised', bd=1)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            control_frame, 
            text="🎯 Simulation Controls", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel'], 
            fg=self.colors['fg']
        ).pack(pady=5)
        
        # Target and mood selection row
        selection_frame = tk.Frame(control_frame, bg=self.colors['panel'])
        selection_frame.pack(pady=5)
        
        # Target selection
        tk.Label(selection_frame, text="Target:", bg=self.colors['panel'], fg=self.colors['fg']).grid(row=0, column=0, padx=5)
        
        self.target_var = tk.StringVar(value=self.current_target)
        target_combo = ttk.Combobox(
            selection_frame, 
            textvariable=self.target_var,
            values=list(TARGET_PROFILES.keys()),
            state='readonly',
            width=15
        )
        target_combo.grid(row=0, column=1, padx=5)
        target_combo.bind('<<ComboboxSelected>>', self.on_target_change)
        
        # Mood selection
        tk.Label(selection_frame, text="Mood:", bg=self.colors['panel'], fg=self.colors['fg']).grid(row=0, column=2, padx=5)
        
        self.mood_var = tk.StringVar(value=self.current_mood)
        mood_combo = ttk.Combobox(
            selection_frame,
            textvariable=self.mood_var,
            values=list(MOOD_STATES.keys()),
            state='readonly',
            width=12
        )
        mood_combo.grid(row=0, column=3, padx=5)
        mood_combo.bind('<<ComboboxSelected>>', self.on_mood_change)
        
        # Update button
        update_btn = tk.Button(
            selection_frame,
            text="🔄 Update Forecast",
            command=self.update_forecast,
            bg=self.colors['accent'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=10
        )
        update_btn.grid(row=0, column=4, padx=10)
    
    def create_dawn_panel(self):
        """Create DAWN integration panel for live system data."""
        dawn_frame = tk.Frame(self.root, bg=self.colors['panel'], relief='raised', bd=1)
        dawn_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            dawn_frame, 
            text="🌅 DAWN System Integration", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel'], 
            fg=self.colors['dawn']
        ).pack(pady=5)
        
        dawn_row = tk.Frame(dawn_frame, bg=self.colors['panel'])
        dawn_row.pack(pady=5)
        
        # Passion direction selection for DAWN forecasts
        tk.Label(dawn_row, text="Direction:", bg=self.colors['panel'], fg=self.colors['fg']).pack(side='left', padx=5)
        
        self.direction_var = tk.StringVar(value=self.current_direction)
        direction_combo = ttk.Combobox(
            dawn_row,
            textvariable=self.direction_var,
            values=[
                'creative_expression', 'learning', 'consciousness_expansion',
                'technical_mastery', 'social_connection', 'introspection',
                'exploration', 'productivity'
            ],
            state='readonly',
            width=20
        )
        direction_combo.pack(side='left', padx=5)
        direction_combo.bind('<<ComboboxSelected>>', self.on_direction_change)
        
        # DAWN live forecast button
        dawn_forecast_btn = tk.Button(
            dawn_row,
            text="🌅 Live DAWN Forecast",
            command=self.get_live_dawn_forecast,
            bg=self.colors['dawn'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=10
        )
        dawn_forecast_btn.pack(side='left', padx=10)
        
        # Current DAWN state display
        self.dawn_state_label = tk.Label(
            dawn_frame,
            text="DAWN State: Initializing...",
            font=('Arial', 9),
            bg=self.colors['panel'],
            fg=self.colors['fg']
        )
        self.dawn_state_label.pack(pady=2)
    
    def create_display_area(self):
        """Create the main display area for forecast visualization."""
        display_frame = tk.Frame(self.root, bg=self.colors['bg'])
        display_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Passion info
        left_panel = tk.Frame(display_frame, bg=self.colors['panel'], relief='raised', bd=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        tk.Label(
            left_panel, 
            text="🧠 Passion State", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel'], 
            fg=self.colors['fg']
        ).pack(pady=5)
        
        # Passion direction
        self.passion_direction_label = tk.Label(
            left_panel,
            text="Direction: Loading...",
            font=('Arial', 11),
            bg=self.colors['panel'],
            fg=self.colors['success'],
            anchor='w'
        )
        self.passion_direction_label.pack(fill='x', padx=10, pady=2)
        
        # Rigidity vs Fluidity bars
        self.create_passion_bars(left_panel)
        
        # Right panel - Forecast results
        right_panel = tk.Frame(display_frame, bg=self.colors['panel'], relief='raised', bd=1)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        tk.Label(
            right_panel, 
            text="🔮 Forecast Results", 
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel'], 
            fg=self.colors['fg']
        ).pack(pady=5)
        
        # Confidence display
        self.create_confidence_display(right_panel)
        
        # Predicted behavior
        self.behavior_label = tk.Label(
            right_panel,
            text="Predicted Behavior:\nLoading...",
            font=('Arial', 10),
            bg=self.colors['panel'],
            fg=self.colors['warning'],
            justify='left',
            wraplength=300
        )
        self.behavior_label.pack(fill='x', padx=10, pady=10)
        
        # Intent gravity breakdown
        self.gravity_label = tk.Label(
            right_panel,
            text="Intent Gravity:\nP / A = F",
            font=('Arial', 9),
            bg=self.colors['panel'],
            fg=self.colors['fg'],
            justify='left'
        )
        self.gravity_label.pack(fill='x', padx=10, pady=5)
    
    def create_passion_bars(self, parent):
        """Create visual bars for passion metrics."""
        bars_frame = tk.Frame(parent, bg=self.colors['panel'])
        bars_frame.pack(fill='x', padx=10, pady=10)
        
        # Intensity bar
        tk.Label(bars_frame, text="Intensity:", bg=self.colors['panel'], fg=self.colors['fg']).pack(anchor='w')
        self.intensity_canvas = tk.Canvas(bars_frame, height=20, bg=self.colors['border'], highlightthickness=0)
        self.intensity_canvas.pack(fill='x', pady=2)
        
        # Fluidity bar
        tk.Label(bars_frame, text="Fluidity:", bg=self.colors['panel'], fg=self.colors['fg']).pack(anchor='w', pady=(5,0))
        self.fluidity_canvas = tk.Canvas(bars_frame, height=20, bg=self.colors['border'], highlightthickness=0)
        self.fluidity_canvas.pack(fill='x', pady=2)
        
        # Rigidity bar (computed)
        tk.Label(bars_frame, text="Rigidity:", bg=self.colors['panel'], fg=self.colors['fg']).pack(anchor='w', pady=(5,0))
        self.rigidity_canvas = tk.Canvas(bars_frame, height=20, bg=self.colors['border'], highlightthickness=0)
        self.rigidity_canvas.pack(fill='x', pady=2)
    
    def create_confidence_display(self, parent):
        """Create confidence visualization with slope indicator."""
        confidence_frame = tk.Frame(parent, bg=self.colors['panel'])
        confidence_frame.pack(fill='x', padx=10, pady=10)
        
        # Confidence label
        self.confidence_label = tk.Label(
            confidence_frame,
            text="Confidence: 0.00",
            font=('Arial', 12, 'bold'),
            bg=self.colors['panel'],
            fg=self.colors['accent']
        )
        self.confidence_label.pack(anchor='w')
        
        # Confidence slope canvas
        tk.Label(confidence_frame, text="Confidence Slope:", bg=self.colors['panel'], fg=self.colors['fg']).pack(anchor='w', pady=(10,0))
        self.confidence_canvas = tk.Canvas(confidence_frame, height=60, bg=self.colors['border'], highlightthickness=0)
        self.confidence_canvas.pack(fill='x', pady=2)
        
        # Additional metrics
        self.metrics_label = tk.Label(
            confidence_frame,
            text="Risk: Low\nHorizon: Short\nCertainty: High",
            font=('Arial', 9),
            bg=self.colors['panel'],
            fg=self.colors['fg'],
            justify='left'
        )
        self.metrics_label.pack(anchor='w', pady=(5,0))
    
    def create_sliders_panel(self):
        """Create optional sliders for real-time adjustment."""
        sliders_frame = tk.Frame(self.root, bg=self.colors['panel'], relief='raised', bd=1)
        sliders_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            sliders_frame, 
            text="🎛️ Live Adjustment (Override Mode)", 
            font=('Arial', 11, 'bold'),
            bg=self.colors['panel'], 
            fg=self.colors['fg']
        ).pack(pady=5)
        
        sliders_row = tk.Frame(sliders_frame, bg=self.colors['panel'])
        sliders_row.pack(pady=5)
        
        # Override checkbox
        self.override_var = tk.BooleanVar()
        override_check = tk.Checkbutton(
            sliders_row,
            text="Override",
            variable=self.override_var,
            command=self.on_override_toggle,
            bg=self.colors['panel'],
            fg=self.colors['fg'],
            selectcolor=self.colors['accent']
        )
        override_check.pack(side='left', padx=5)
        
        # Intensity slider
        tk.Label(sliders_row, text="Intensity:", bg=self.colors['panel'], fg=self.colors['fg']).pack(side='left', padx=5)
        self.intensity_slider = tk.Scale(
            sliders_row,
            from_=0.0, to=1.0, resolution=0.01,
            orient='horizontal',
            command=self.on_slider_change,
            bg=self.colors['panel'],
            fg=self.colors['fg'],
            highlightbackground=self.colors['panel'],
            state='disabled'
        )
        self.intensity_slider.pack(side='left', padx=5)
        
        # Fluidity slider
        tk.Label(sliders_row, text="Fluidity:", bg=self.colors['panel'], fg=self.colors['fg']).pack(side='left', padx=5)
        self.fluidity_slider = tk.Scale(
            sliders_row,
            from_=0.0, to=1.0, resolution=0.01,
            orient='horizontal',
            command=self.on_slider_change,
            bg=self.colors['panel'],
            fg=self.colors['fg'],
            highlightbackground=self.colors['panel'],
            state='disabled'
        )
        self.fluidity_slider.pack(side='left', padx=5)
    
    def create_status_bar(self):
        """Create status bar for system information."""
        status_frame = tk.Frame(self.root, bg=self.colors['border'], relief='sunken', bd=1)
        status_frame.pack(fill='x', side='bottom')
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready - Select target and mood, then click Update Forecast",
            bg=self.colors['border'],
            fg=self.colors['fg'],
            font=('Arial', 9),
            anchor='w'
        )
        self.status_label.pack(fill='x', padx=5, pady=2)
    
    def on_target_change(self, event=None):
        """Handle target selection change."""
        self.current_target = self.target_var.get()
        self.update_status(f"Target changed to {self.current_target}")
    
    def on_mood_change(self, event=None):
        """Handle mood selection change."""
        self.current_mood = self.mood_var.get()
        self.update_status(f"Mood changed to {self.current_mood}")
    
    def on_direction_change(self, event=None):
        """Handle direction selection change."""
        self.current_direction = self.direction_var.get()
        self.update_status(f"Direction changed to {self.current_direction}")
    
    def on_override_toggle(self):
        """Handle override mode toggle."""
        if self.override_var.get():
            self.intensity_slider.config(state='normal')
            self.fluidity_slider.config(state='normal')
            if self.passion:
                self.intensity_slider.set(self.passion.intensity)
                self.fluidity_slider.set(self.passion.fluidity)
            self.update_status("Override mode enabled - use sliders to adjust passion")
        else:
            self.intensity_slider.config(state='disabled')
            self.fluidity_slider.config(state='disabled')
            self.update_status("Override mode disabled - using target profile")
            self.update_forecast()
    
    def on_slider_change(self, value=None):
        """Handle slider value changes in override mode."""
        if self.override_var.get() and self.passion:
            # Update passion with slider values
            new_intensity = self.intensity_slider.get()
            new_fluidity = self.fluidity_slider.get()
            
            self.passion.intensity = new_intensity
            self.passion.fluidity = new_fluidity
            
            # Regenerate forecast with modified passion
            mood_params = self.get_mood_params()
            self.forecast = self.forecasting_engine.generate_forecast(self.passion, self.acquaintance, **mood_params)
            
            # Update display
            self.update_display()
            self.update_status(f"Live adjustment: I={new_intensity:.2f}, F={new_fluidity:.2f}")
    
    def get_mood_params(self):
        """Get mood modulation parameters."""
        return MOOD_STATES.get(self.current_mood, {"mood_factor": 1.0, "entropy_weight": 1.0})
    
    def create_target_objects(self, target_key):
        """Create passion and acquaintance objects from target profile."""
        profile = TARGET_PROFILES[target_key]
        
        # Create passion
        passion = create_passion(
            profile["passion"],
            profile["intensity"],
            profile["fluidity"]
        )
        
        # Create acquaintance with events
        acquaintance = create_acquaintance_with_events(profile["events"])
        
        return passion, acquaintance
    
    def update_forecast(self):
        """Update the forecast based on current selections."""
        try:
            self.update_status("Generating forecast...")
            
            # Create passion and acquaintance objects
            self.passion, self.acquaintance = self.create_target_objects(self.current_target)
            
            # Apply mood modulation
            mood_params = self.get_mood_params()
            
            # Generate forecast using integrated engine
            self.forecast = self.forecasting_engine.generate_forecast(self.passion, self.acquaintance, **mood_params)
            
            # Update display
            self.update_display()
            
            # Update sliders if in override mode
            if not self.override_var.get():
                self.intensity_slider.set(self.passion.intensity)
                self.fluidity_slider.set(self.passion.fluidity)
            
            profile_name = TARGET_PROFILES[self.current_target]['name']
            self.update_status(f"Forecast updated for {profile_name} in {self.current_mood} mood")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate forecast: {e}")
            self.update_status(f"Error: {e}")
    
    def get_live_dawn_forecast(self):
        """Get a live forecast from DAWN's consciousness system."""
        if not self.connected_to_dawn:
            messagebox.showwarning("DAWN Not Connected", "DAWN system not available for live forecasting")
            return
        
        try:
            self.update_status("Generating live DAWN forecast...")
            
            # Use DAWN's current consciousness state
            if hasattr(self.dawn_consciousness, 'get_current_forecasts'):
                forecasts_data = self.dawn_consciousness.get_current_forecasts()
                recent_forecasts = forecasts_data.get('recent_forecasts', [])
                
                # Find forecast for current direction
                direction_forecast = None
                for forecast_dict in recent_forecasts:
                    if forecast_dict.get('passion_direction') == self.current_direction:
                        direction_forecast = forecast_dict
                        break
                
                if direction_forecast:
                    # Convert back to ForecastVector for display
                    self.forecast = ForecastVector(
                        predicted_behavior=direction_forecast['predicted_behavior'],
                        confidence=direction_forecast['confidence'],
                        risk=direction_forecast.get('risk', 0.0),
                        passion_direction=direction_forecast['passion_direction'],
                        forecast_horizon=direction_forecast.get('forecast_horizon', 'short')
                    )
                    
                    # Create synthetic passion for display
                    self.passion = create_passion(
                        self.current_direction,
                        intensity=0.5,  # Default values since we don't have the original
                        fluidity=0.5
                    )
                    
                    # Create empty acquaintance
                    self.acquaintance = Acquaintance()
                    
                    self.update_display()
                    self.update_dawn_state()
                    self.update_status(f"Live DAWN forecast retrieved for {self.current_direction}")
                else:
                    self.update_status(f"No live forecast available for {self.current_direction}")
            else:
                # Generate instant forecast
                forecast_dict = asyncio.run(
                    self.dawn_consciousness.generate_instant_forecast(self.current_direction)
                )
                
                if forecast_dict:
                    self.forecast = ForecastVector(
                        predicted_behavior=forecast_dict['predicted_behavior'],
                        confidence=forecast_dict['confidence'],
                        risk=forecast_dict.get('risk', 0.0),
                        passion_direction=forecast_dict['passion_direction'],
                        forecast_horizon=forecast_dict.get('forecast_horizon', 'short')
                    )
                    
                    # Create synthetic passion for display
                    self.passion = create_passion(self.current_direction, 0.5, 0.5)
                    self.acquaintance = Acquaintance()
                    
                    self.update_display()
                    self.update_dawn_state()
                    self.update_status(f"Generated instant DAWN forecast for {self.current_direction}")
                else:
                    self.update_status("Failed to generate live DAWN forecast")
            
        except Exception as e:
            messagebox.showerror("DAWN Forecast Error", f"Failed to get live DAWN forecast: {e}")
            self.update_status(f"DAWN forecast error: {e}")
    
    def update_dawn_state(self):
        """Update DAWN state display."""
        if not self.connected_to_dawn:
            return
        
        try:
            # Get current DAWN state
            if hasattr(self.dawn_consciousness, '_current_scup'):
                scup = getattr(self.dawn_consciousness, '_current_scup', 0.5)
                entropy = getattr(self.dawn_consciousness, '_current_entropy', 0.5)
                mood = getattr(self.dawn_consciousness, '_current_mood', 'neutral')
                
                state_text = f"DAWN State: SCUP={scup:.2f}, Entropy={entropy:.2f}, Mood={mood}"
                self.dawn_state_label.config(text=state_text)
            else:
                self.dawn_state_label.config(text="DAWN State: Connected, retrieving...")
                
        except Exception as e:
            self.dawn_state_label.config(text=f"DAWN State: Error - {e}")
    
    def update_display(self):
        """Update all visual displays with current forecast data."""
        if not self.passion or not self.forecast:
            return
        
        # Update passion direction
        direction_text = f"Direction: {self.passion.direction}"
        self.passion_direction_label.config(text=direction_text)
        
        # Update passion bars
        self.draw_bar(self.intensity_canvas, self.passion.intensity, self.colors['success'])
        self.draw_bar(self.fluidity_canvas, self.passion.fluidity, self.colors['warning'])
        self.draw_bar(self.rigidity_canvas, self.passion.rigidity_score(), self.colors['accent'])
        
        # Update confidence display
        confidence_text = f"Confidence: {self.forecast.confidence:.3f}"
        self.confidence_label.config(text=confidence_text)
        
        # Draw confidence slope
        self.draw_confidence_slope()
        
        # Update behavior prediction
        behavior_text = f"Predicted Behavior:\n{self.forecast.predicted_behavior.replace('_', ' ').title()}"
        self.behavior_label.config(text=behavior_text)
        
        # Update metrics
        metrics_text = f"Risk: {self.forecast.risk_level().title()}\nHorizon: {self.forecast.forecast_horizon.title()}\nCertainty: {self.forecast.certainty_band()}"
        self.metrics_label.config(text=metrics_text)
        
        # Update intent gravity breakdown
        if hasattr(self.forecasting_engine, 'analyze_forecast_components'):
            components = self.forecasting_engine.analyze_forecast_components(self.passion, self.acquaintance)
            gravity_text = f"Intent Gravity:\nP={components['passion_rigidity']:.3f} / A={components['resistance_factor']:.3f} = {components['intent_gravity']:.3f}"
            self.gravity_label.config(text=gravity_text)
    
    def draw_bar(self, canvas, value, color):
        """Draw a horizontal bar representing a value from 0-1."""
        canvas.delete("all")
        
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1:  # Canvas not yet sized
            canvas.after(100, lambda: self.draw_bar(canvas, value, color))
            return
        
        # Background
        canvas.create_rectangle(0, 0, width, height, fill=self.colors['border'], outline='')
        
        # Value bar
        bar_width = int(width * value)
        if bar_width > 0:
            canvas.create_rectangle(0, 0, bar_width, height, fill=color, outline='')
        
        # Value text
        text_color = 'white' if value > 0.5 else self.colors['fg']
        canvas.create_text(width//2, height//2, text=f"{value:.2f}", fill=text_color, font=('Arial', 9, 'bold'))
    
    def draw_confidence_slope(self):
        """Draw a slope visualization for confidence level."""
        canvas = self.confidence_canvas
        canvas.delete("all")
        
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1:  # Canvas not yet sized
            canvas.after(100, self.draw_confidence_slope)
            return
        
        # Background
        canvas.create_rectangle(0, 0, width, height, fill=self.colors['border'], outline='')
        
        if not self.forecast:
            return
        
        confidence = self.forecast.confidence
        
        # Draw slope based on confidence
        # Higher confidence = steeper upward slope
        start_y = height - 5
        end_y = height - 5 - (confidence * (height - 10))
        
        # Slope line
        slope_color = self.colors['success'] if confidence > 0.7 else self.colors['warning'] if confidence > 0.4 else self.colors['danger']
        canvas.create_line(5, start_y, width-5, end_y, fill=slope_color, width=3)
        
        # Confidence markers
        for i in range(0, 11, 2):
            x = (i / 10) * (width - 10) + 5
            marker_y = height - 2
            canvas.create_line(x, marker_y, x, marker_y + 4, fill=self.colors['fg'], width=1)
        
        # Current confidence indicator
        conf_x = confidence * (width - 10) + 5
        conf_y = start_y - (confidence * (height - 10))
        canvas.create_oval(conf_x-3, conf_y-3, conf_x+3, conf_y+3, fill='white', outline=slope_color, width=2)
    
    def update_status(self, message):
        """Update the status bar message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_label.config(text=f"[{timestamp}] {message}")


def main():
    """Launch the DAWN Forecast Visualizer."""
    try:
        root = tk.Tk()
        app = DAWNForecastGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 DAWN Forecast Visualizer terminated by user")
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🔮 Launching DAWN Forecast Visualizer...")
    main() 