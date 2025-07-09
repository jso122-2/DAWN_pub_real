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
        heat = dawn_data.get('heat', 0.5)
        mood = dawn_data.get('mood', {})
        scup = dawn_data.get('scup', {})
        
        # Generate contextual comments based on state
        comments = []
        
        # Entropy analysis
        if entropy > 0.8:
            comments.append(("High entropy detected. Cognitive exploration active.", 'highlight'))
        elif entropy < 0.2:
            comments.append(("Low entropy state. Pattern crystallization likely.", 'normal'))
            
        # Heat analysis
        if heat > 0.7:
            comments.append(("Thermal elevation suggests focused processing.", 'normal'))
        elif heat < 0.3:
            comments.append(("Cooling phase. Integration processes dominant.", 'insight'))
            
        # SCUP analysis
        schema = scup.get('schema', 0.5)
        coherence = scup.get('coherence', 0.5)
        utility = scup.get('utility', 0.5)
        pressure = scup.get('pressure', 0.5)
        
        if pressure > 0.8:
            comments.append(("Pressure surge detected. Monitor stability.", 'critical'))
            
        if coherence > 0.7 and schema > 0.7:
            comments.append(("High coherence-schema correlation. Deep understanding forming.", 'insight'))
            
        if utility < 0.3 and pressure > 0.6:
            comments.append(("Utility-pressure imbalance. Recommend recalibration.", 'highlight'))
            
        # Mood dynamics
        base_mood = mood.get('base_level', 0.5)
        if base_mood > 0.7:
            comments.append(("Positive mood elevation enhancing creativity.", 'normal'))
            
        # Log selected comments
        for comment, msg_type in comments[:3]:  # Limit to 3 comments per update
            self.log_comment(comment, msg_type=msg_type)

# Example usage and testing
if __name__ == "__main__":
    # Create test window
    root = tk.Tk()
    root.title("Owl Console Panel Test")
    root.geometry("600x400")
    root.configure(bg='#1a1a1a')
    
    # Create and pack the console panel
    console = OwlConsolePanel(root, height=200)
    console.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Control frame
    control_frame = ttk.Frame(root)
    control_frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Test buttons
    def test_normal():
        console.log_comment("Normal observation: Processing stable.")
        
    def test_highlight():
        console.log_comment("Attention spike detected in semantic layer.", 
                          msg_type='highlight')
        
    def test_critical():
        console.log_comment("WARNING: Coherence breakdown imminent.", 
                          msg_type='critical')
        
    def test_insight():
        console.log_comment("Meta-pattern emergence observed in recursion depth 3.", 
                          msg_type='insight')
        
    def toggle_test_mode():
        if console.test_mode:
            console.stop_test_mode()
            test_btn.config(text="Start Test Mode")
        else:
            console.inject_test_comments(interval=1500)
            test_btn.config(text="Stop Test Mode")
    
    # Create buttons
    ttk.Button(control_frame, text="Normal", command=test_normal).pack(side=tk.LEFT, padx=2)
    ttk.Button(control_frame, text="Highlight", command=test_highlight).pack(side=tk.LEFT, padx=2)
    ttk.Button(control_frame, text="Critical", command=test_critical).pack(side=tk.LEFT, padx=2)
    ttk.Button(control_frame, text="Insight", command=test_insight).pack(side=tk.LEFT, padx=2)
    
    test_btn = ttk.Button(control_frame, text="Start Test Mode", command=toggle_test_mode)
    test_btn.pack(side=tk.LEFT, padx=20)
    
    # Example of analyzing DAWN state
    def test_dawn_analysis():
        test_data = {
            'entropy': random.uniform(0, 1),
            'heat': random.uniform(0, 1),
            'scup': {
                'schema': random.uniform(0, 1),
                'coherence': random.uniform(0, 1),
                'utility': random.uniform(0, 1),
                'pressure': random.uniform(0, 1)
            },
            'mood': {
                'base_level': random.uniform(0, 1)
            }
        }
        console.analyze_dawn_state(test_data)
    
    ttk.Button(control_frame, text="Analyze DAWN", 
              command=test_dawn_analysis).pack(side=tk.LEFT, padx=2)
    
    root.mainloop()