#!/usr/bin/env python3
"""
Owl Console Panel - Terminal-style commentary display for DAWN's cognitive reflections
Displays high-trust observations about DAWN's cognitive state in a console-like interface.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import time
from datetime import datetime
import random
import threading

class OwlConsolePanel(ttk.Frame):
    """Terminal-style panel for displaying Owl commentary about DAWN's state"""
    
    def __init__(self, parent, height=150, **kwargs):
        """
        Initialize the Owl Console Panel
        
        Args:
            parent: Parent widget
            height: Fixed height of the console in pixels (default: 150)
            **kwargs: Additional arguments passed to ttk.Frame
        """
        super().__init__(parent, **kwargs)
        
        # Configuration
        self.height = height
        self.max_messages = 100  # Maximum messages to keep in history
        self.message_history = []
        
        # Terminal color scheme
        self.bg_color = '#0a0a0a'
        self.fg_color = '#00ff00'
        self.timestamp_color = '#888888'
        self.highlight_color = '#ffff00'
        self.critical_color = '#ff4444'
        self.insight_color = '#00ffff'
        
        # Create the interface
        self.setup_ui()
        
        # Test mode flag
        self.test_mode = False
        
    def setup_ui(self):
        """Create the console interface"""
        # Configure frame
        self.configure(relief=tk.SUNKEN, borderwidth=2)
        
        # Title bar
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=2, pady=(2, 0))
        
        title_label = ttk.Label(title_frame, text="🦉 Owl Commentary", 
                               font=('Consolas', 10, 'bold'))
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(title_frame, text="Clear", 
                              command=self.clear, width=6)
        clear_btn.pack(side=tk.RIGHT, padx=2)
        
        # Console text area
        self.console_frame = tk.Frame(self, bg=self.bg_color, height=self.height)
        self.console_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.console_frame.pack_propagate(False)  # Maintain fixed height
        
        # Create scrolled text widget with terminal styling
        self.console_text = scrolledtext.ScrolledText(
            self.console_frame,
            wrap=tk.WORD,
            bg=self.bg_color,
            fg=self.fg_color,
            font=('Consolas', 9),
            insertbackground=self.fg_color,
            selectbackground='#333333',
            selectforeground=self.fg_color,
            relief=tk.FLAT,
            borderwidth=0,
            padx=5,
            pady=5,
            state=tk.DISABLED  # Read-only
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for different message types
        self.console_text.tag_configure('timestamp', foreground=self.timestamp_color)
        self.console_text.tag_configure('normal', foreground=self.fg_color)
        self.console_text.tag_configure('highlight', foreground=self.highlight_color, 
                                       font=('Consolas', 9, 'bold'))
        self.console_text.tag_configure('critical', foreground=self.critical_color,
                                       font=('Consolas', 9, 'bold'))
        self.console_text.tag_configure('insight', foreground=self.insight_color,
                                       font=('Consolas', 9, 'italic'))
        
        # Initial welcome message
        self.log_comment("Owl Console initialized. Monitoring cognitive patterns...", 
                        msg_type='insight')
        
    def log_comment(self, comment, msg_type='normal', timestamp=True):
        """
        Log a comment to the console
        
        Args:
            comment: The comment text to display
            msg_type: Type of message ('normal', 'highlight', 'critical', 'insight')
            timestamp: Whether to include timestamp (default: True)
        """
        # Enable text widget for editing
        self.console_text.config(state=tk.NORMAL)
        
        # Add to history
        self.message_history.append({
            'comment': comment,
            'type': msg_type,
            'time': datetime.now()
        })
        
        # Trim history if needed
        if len(self.message_history) > self.max_messages:
            self.message_history.pop(0)
            # Clear and redraw all messages
            self.redraw_console()
        else:
            # Just append the new message
            self.append_message(comment, msg_type, timestamp)
        
        # Auto-scroll to bottom
        self.console_text.see(tk.END)
        
        # Disable text widget again
        self.console_text.config(state=tk.DISABLED)
        
    def append_message(self, comment, msg_type='normal', timestamp=True):
        """Append a single message to the console"""
        # Add timestamp if requested
        if timestamp:
            time_str = datetime.now().strftime("%H:%M:%S")
            self.console_text.insert(tk.END, f"[{time_str}] ", 'timestamp')
        
        # Add the comment with appropriate styling
        self.console_text.insert(tk.END, f"{comment}\n", msg_type)
        
    def redraw_console(self):
        """Redraw all messages in the console"""
        self.console_text.delete(1.0, tk.END)
        
        for msg in self.message_history:
            time_str = msg['time'].strftime("%H:%M:%S")
            self.console_text.insert(tk.END, f"[{time_str}] ", 'timestamp')
            self.console_text.insert(tk.END, f"{msg['comment']}\n", msg['type'])
            
    def clear(self):
        """Clear all messages from the console"""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.delete(1.0, tk.END)
        self.message_history.clear()
        self.console_text.config(state=tk.DISABLED)
        
        # Log clear action
        self.log_comment("Console cleared.", msg_type='insight')
        
    def inject_test_comments(self, interval=2000):
        """
        Inject test comments for simulation/debug purposes
        
        Args:
            interval: Milliseconds between test comments (default: 2000)
        """
        if self.test_mode:
            return  # Already running
            
        self.test_mode = True
        
        # Test comment templates
        test_comments = [
            # Normal observations
            ("Entropy stabilizing.", 'normal'),
            ("Coherence patterns nominal.", 'normal'),
            ("Schema pressure within bounds.", 'normal'),
            ("Utility optimization proceeding.", 'normal'),
            ("Cognitive load balanced.", 'normal'),
            
            # Highlight observations
            ("Bloom depth exceeds average.", 'highlight'),
            ("Recursive depth approaching limit.", 'highlight'),
            ("Pattern recognition spike detected.", 'highlight'),
            ("Creative synthesis emerging.", 'highlight'),
            
            # Critical observations
            ("Semantic coherence critical.", 'critical'),
            ("Pressure cascade imminent.", 'critical'),
            ("Stability threshold breached.", 'critical'),
            ("Attention fragmentation detected.", 'critical'),
            
            # Insight observations
            ("Meta-cognitive awareness rising.", 'insight'),
            ("Transcendent state proximity: 0.7", 'insight'),
            ("Consciousness constellation shifting.", 'insight'),
            ("Novel pattern synthesis observed.", 'insight'),
            ("Self-referential loop stabilized.", 'insight')
        ]
        
        def inject_comment():
            if self.test_mode:
                # Select random comment
                comment, msg_type = random.choice(test_comments)
                
                # Add some dynamic elements
                if "Entropy" in comment:
                    value = random.uniform(0.3, 0.8)
                    comment = f"Entropy stabilizing at {value:.3f}."
                elif "depth" in comment:
                    depth = random.randint(3, 12)
                    comment = f"Bloom depth exceeds average: {depth} layers."
                elif "proximity" in comment:
                    proximity = random.uniform(0.5, 0.95)
                    comment = f"Transcendent state proximity: {proximity:.2f}"
                
                self.log_comment(comment, msg_type=msg_type)
                
                # Schedule next comment
                self.after(interval + random.randint(-500, 500), inject_comment)
        
        # Start injection
        inject_comment()
        
    def stop_test_mode(self):
        """Stop test comment injection"""
        self.test_mode = False
        
    def analyze_dawn_state(self, dawn_data):
        """
        Analyze DAWN state and generate appropriate commentary
        
        Args:
            dawn_data: Dictionary containing DAWN's current state
        """
        # Extract key metrics
        entropy = dawn_data.get('entropy', 0.5)
        heat = dawn_data.get('heat', 50) / 100.0  # Convert to 0-1 range
        scup = dawn_data.get('scup', 0.5)
        coherence = dawn_data.get('coherence', 0.5)
        zone = dawn_data.get('zone', 'calm')
        
        # Generate contextual comments based on state
        comments = []
        
        # Entropy analysis
        if entropy > 0.8:
            comments.append(("High entropy detected. Cognitive exploration active.", 'highlight'))
        elif entropy < 0.2:
            comments.append(("Low entropy state. Pattern crystallization likely.", 'normal'))
        elif 0.3 < entropy < 0.7:
            comments.append((f"Entropy stabilizing at {entropy:.3f}.", 'normal'))
            
        # Heat analysis
        if heat > 0.7:
            comments.append(("Thermal elevation suggests focused processing.", 'normal'))
        elif heat < 0.3:
            comments.append(("Cooling phase. Integration processes dominant.", 'insight'))
        elif heat > 0.9:
            comments.append(("Critical heat levels. Monitor thermal regulation.", 'critical'))
            
        # SCUP analysis
        if scup > 0.8:
            comments.append(("High SCUP detected. Deep understanding forming.", 'insight'))
        elif scup < 0.2:
            comments.append(("SCUP degradation. Recalibration recommended.", 'highlight'))
            
        # Coherence analysis
        if coherence > 0.7:
            comments.append(("Coherence optimal. Stable processing achieved.", 'normal'))
        elif coherence < 0.3:
            comments.append(("Coherence fragmentation detected.", 'critical'))
            
        # Zone-specific observations
        zone_comments = {
            'surge': ("Cognitive surge detected. Peak performance mode.", 'highlight'),
            'active': ("Active processing engaged. Nominal operation.", 'normal'),
            'calm': ("Calm reflection mode. Consolidation active.", 'normal'),
            'transcendent': ("Transcendent state achieved. Monitor carefully.", 'insight'),
            'dormant': ("Dormant phase. Minimal cognitive activity.", 'normal')
        }
        
        if zone in zone_comments:
            comments.append(zone_comments[zone])
            
        # Complex pattern detection
        if heat > 0.6 and entropy > 0.7:
            comments.append(("Heat-entropy correlation. Creative burst imminent.", 'insight'))
            
        if scup > 0.6 and coherence > 0.6 and entropy < 0.4:
            comments.append(("Stable high-coherence state. Optimal for reasoning.", 'insight'))
            
        if heat < 0.3 and entropy < 0.3 and scup < 0.4:
            comments.append(("System approaching dormancy. Consider stimulation.", 'highlight'))
            
        # Randomly select and log some comments (max 2 per update to avoid spam)
        selected_comments = random.sample(comments, min(2, len(comments))) if comments else []
        
        for comment, msg_type in selected_comments:
            self.log_comment(comment, msg_type=msg_type) 