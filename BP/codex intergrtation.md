#!/usr/bin/env python3
"""
GUI Codex Integration - Updates for dawn_gui_tk.py to use codex_engine functions
"""

# Import the codex engine functions at the top of your GUI file
from codex_engine import (
    get_pulse_zone, 
    describe_pulse_zone, 
    get_schema_health, 
    summarize_bloom
)

# Add this method to your main GUI class to update with codex functions
def update_with_codex(self, dawn_data):
    """Update GUI elements using codex engine functions"""
    
    # 1. Update Pulse Zone using codex functions
    heat = dawn_data.get('heat', 0.0)
    
    # Get the pulse zone from codex
    pulse_zone = get_pulse_zone(heat)
    
    # Update pulse zone label with the zone name
    if hasattr(self, 'pulse_zone_label'):
        self.pulse_zone_label.config(text=f"Zone: {pulse_zone}")
    
    # Get the pulse zone description
    zone_description = describe_pulse_zone(pulse_zone)
    
    # Update pulse zone descriptor label
    if hasattr(self, 'pulse_zone_descriptor_label'):
        self.pulse_zone_descriptor_label.config(text=zone_description)
    
    # Update pulse heat display with color based on zone
    if hasattr(self, 'pulse_heat_label'):
        # Color mapping for pulse zones
        zone_colors = {
            'dormant': '#0074D9',      # Blue
            'contemplative': '#2ECC40', # Green  
            'active': '#FFDC00',       # Yellow
            'intense': '#FF851B',      # Orange
            'critical': '#FF4136'      # Red
        }
        
        color = zone_colors.get(pulse_zone, '#AAAAAA')
        self.pulse_heat_label.config(
            text=f"Heat: {heat:.3f}",
            fg=color
        )
    
    # 2. Update Schema Health
    schema_health_data = get_schema_health(
        schema_pressure=dawn_data.get('scup', {}).get('schema', 0.5),
        coherence=dawn_data.get('scup', {}).get('coherence', 0.5),
        entropy=dawn_data.get('entropy', 0.5),
        heat=heat
    )
    
    # Update health status label
    if hasattr(self, 'schema_health_label'):
        self.schema_health_label.config(
            text=f"Schema Health: {schema_health_data['status']}"
        )
    
    # Update detailed health info if you have a text widget for it
    if hasattr(self, 'health_details_text'):
        self.health_details_text.config(state='normal')
        self.health_details_text.delete(1.0, 'end')
        
        # Format health details
        health_text = f"Status: {schema_health_data['status']}\n"
        health_text += f"Score: {schema_health_data['health_score']:.2f}\n"
        health_text += f"Stability: {schema_health_data['stability']:.2f}\n"
        
        # Add indicators
        if schema_health_data['indicators']:
            health_text += "\nIndicators:\n"
            for indicator in schema_health_data['indicators']:
                health_text += f"  • {indicator}\n"
        
        # Add recommendations
        if schema_health_data['recommendations']:
            health_text += "\nRecommendations:\n"
            for rec in schema_health_data['recommendations']:
                health_text += f"  → {rec}\n"
        
        self.health_details_text.insert(1.0, health_text)
        self.health_details_text.config(state='disabled')
    
    # 3. Update Bloom Summary
    # Extract bloom parameters from dawn_data
    bloom_params = {
        'depth': dawn_data.get('bloom', {}).get('depth', 0),
        'heat': heat,
        'coherence': dawn_data.get('scup', {}).get('coherence', 0.5),
        'frequency': dawn_data.get('bloom', {}).get('frequency', 1.0),
        'intensity': dawn_data.get('bloom', {}).get('intensity', 0.5)
    }
    
    # Get bloom summary from codex
    bloom_summary = summarize_bloom(**bloom_params)
    
    # Update bloom summary label
    if hasattr(self, 'bloom_summary_label'):
        self.bloom_summary_label.config(text=bloom_summary)
    
    # Update bloom details if you have a dedicated area
    if hasattr(self, 'bloom_info_frame'):
        # Update bloom depth indicator
        if hasattr(self, 'bloom_depth_label'):
            self.bloom_depth_label.config(
                text=f"Depth: {bloom_params['depth']}"
            )
        
        # Update bloom frequency
        if hasattr(self, 'bloom_frequency_label'):
            self.bloom_frequency_label.config(
                text=f"Frequency: {bloom_params['frequency']:.2f}"
            )
        
        # Update bloom intensity with color
        if hasattr(self, 'bloom_intensity_label'):
            intensity = bloom_params['intensity']
            intensity_color = self._get_intensity_color(intensity)
            self.bloom_intensity_label.config(
                text=f"Intensity: {intensity:.2f}",
                fg=intensity_color
            )

# Helper method for intensity coloring
def _get_intensity_color(self, intensity):
    """Get color based on bloom intensity"""
    if intensity < 0.3:
        return '#2ECC40'  # Green - low
    elif intensity < 0.6:
        return '#FFDC00'  # Yellow - medium
    elif intensity < 0.8:
        return '#FF851B'  # Orange - high
    else:
        return '#FF4136'  # Red - critical

# Update your main tick/update loop to call this method
def update_display(self, dawn_data):
    """Main update method - add this to your existing update loop"""
    
    # ... existing update code ...
    
    # Add codex updates
    self.update_with_codex(dawn_data)
    
    # If you have an Owl Console, update it with schema health
    if hasattr(self, 'owl_console'):
        schema_health = get_schema_health(
            schema_pressure=dawn_data.get('scup', {}).get('schema', 0.5),
            coherence=dawn_data.get('scup', {}).get('coherence', 0.5),
            entropy=dawn_data.get('entropy', 0.5),
            heat=dawn_data.get('heat', 0.0)
        )
        
        # Log health status changes
        if schema_health['status'] == 'critical':
            self.owl_console.log_comment(
                f"Schema health critical! Score: {schema_health['health_score']:.2f}",
                msg_type='critical'
            )
        elif schema_health['status'] == 'unstable':
            self.owl_console.log_comment(
                f"Schema instability detected. {schema_health['indicators'][0] if schema_health['indicators'] else ''}",
                msg_type='highlight'
            )
        
        # Log bloom insights
        bloom_summary = summarize_bloom(
            depth=dawn_data.get('bloom', {}).get('depth', 0),
            heat=dawn_data.get('heat', 0.0),
            coherence=dawn_data.get('scup', {}).get('coherence', 0.5)
        )
        
        if 'Deep recursive' in bloom_summary:
            self.owl_console.log_comment(bloom_summary, msg_type='insight')
        elif 'High heat' in bloom_summary:
            self.owl_console.log_comment(bloom_summary, msg_type='highlight')

# If you need to create the specific labels, here's example widget creation
def create_codex_widgets(self, parent_frame):
    """Create widgets for codex display"""
    
    # Pulse Zone Frame
    pulse_frame = ttk.LabelFrame(parent_frame, text="Pulse State", padding=10)
    pulse_frame.pack(fill='x', padx=5, pady=5)
    
    # Pulse zone label
    self.pulse_zone_label = ttk.Label(pulse_frame, text="Zone: Unknown",
                                     font=('Arial', 12, 'bold'))
    self.pulse_zone_label.pack(anchor='w')
    
    # Pulse zone descriptor
    self.pulse_zone_descriptor_label = ttk.Label(pulse_frame, text="",
                                                font=('Arial', 10),
                                                wraplength=300)
    self.pulse_zone_descriptor_label.pack(anchor='w', pady=(5, 0))
    
    # Pulse heat label
    self.pulse_heat_label = ttk.Label(pulse_frame, text="Heat: 0.000",
                                     font=('Arial', 11))
    self.pulse_heat_label.pack(anchor='w', pady=(5, 0))
    
    # Schema Health Frame
    health_frame = ttk.LabelFrame(parent_frame, text="Schema Health", padding=10)
    health_frame.pack(fill='x', padx=5, pady=5)
    
    # Schema health status
    self.schema_health_label = ttk.Label(health_frame, text="Schema Health: Unknown",
                                        font=('Arial', 11, 'bold'))
    self.schema_health_label.pack(anchor='w')
    
    # Health details text
    self.health_details_text = tk.Text(health_frame, height=6, width=40,
                                      wrap='word', font=('Arial', 9))
    self.health_details_text.pack(fill='both', expand=True, pady=(5, 0))
    
    # Bloom Summary Frame
    bloom_frame = ttk.LabelFrame(parent_frame, text="Bloom State", padding=10)
    bloom_frame.pack(fill='x', padx=5, pady=5)
    
    # Bloom summary label
    self.bloom_summary_label = ttk.Label(bloom_frame, text="Awaiting bloom data...",
                                        font=('Arial', 10),
                                        wraplength=300)
    self.bloom_summary_label.pack(anchor='w')
    
    # Bloom metrics
    self.bloom_info_frame = ttk.Frame(bloom_frame)
    self.bloom_info_frame.pack(fill='x', pady=(5, 0))
    
    self.bloom_depth_label = ttk.Label(self.bloom_info_frame, text="Depth: 0")
    self.bloom_depth_label.pack(side='left', padx=(0, 15))
    
    self.bloom_frequency_label = ttk.Label(self.bloom_info_frame, text="Frequency: 0.00")
    self.bloom_frequency_label.pack(side='left', padx=(0, 15))
    
    self.bloom_intensity_label = ttk.Label(self.bloom_info_frame, text="Intensity: 0.00")
    self.bloom_intensity_label.pack(side='left')