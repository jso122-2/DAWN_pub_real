#!/usr/bin/env python3
"""
Test script for the Owl Console Panel
Demonstrates the functionality with sample DAWN data
"""

import tkinter as tk
from tkinter import ttk
import random
import time
from owl_console_panel import OwlConsolePanel

def main():
    """Main test function"""
    # Create test window
    root = tk.Tk()
    root.title("Owl Console Panel Test")
    root.geometry("700x500")
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
            test_btn.config(text="Start Auto-Commentary")
        else:
            console.inject_test_comments(interval=1500)
            test_btn.config(text="Stop Auto-Commentary")
    
    # Example of analyzing DAWN state
    def test_dawn_analysis():
        # Generate random DAWN data for testing
        test_data = {
            'entropy': random.uniform(0, 1),
            'heat': random.randint(0, 100),
            'scup': random.uniform(0, 1),
            'coherence': random.uniform(0, 1),
            'zone': random.choice(['calm', 'active', 'surge', 'dormant', 'transcendent']),
            'schema': {
                'tick': random.randint(1000, 9999),
                'alignment': random.uniform(0, 1)
            }
        }
        
        # Log current state
        console.log_comment(
            f"Analyzing DAWN state: Heat={test_data['heat']}%, "
            f"Zone={test_data['zone']}, Entropy={test_data['entropy']:.3f}",
            msg_type='normal'
        )
        
        # Analyze the state
        console.analyze_dawn_state(test_data)
    
    # Create buttons
    ttk.Button(control_frame, text="Normal", command=test_normal).pack(side=tk.LEFT, padx=2)
    ttk.Button(control_frame, text="Highlight", command=test_highlight).pack(side=tk.LEFT, padx=2)
    ttk.Button(control_frame, text="Critical", command=test_critical).pack(side=tk.LEFT, padx=2)
    ttk.Button(control_frame, text="Insight", command=test_insight).pack(side=tk.LEFT, padx=2)
    
    test_btn = ttk.Button(control_frame, text="Start Auto-Commentary", command=toggle_test_mode)
    test_btn.pack(side=tk.LEFT, padx=20)
    
    ttk.Button(control_frame, text="Analyze DAWN", 
              command=test_dawn_analysis).pack(side=tk.LEFT, padx=2)
    
    # Instructions
    instructions = tk.Label(root, 
                           text="🦉 Owl Console Panel Test\n"
                                "Click buttons to test different message types.\n"
                                "'Analyze DAWN' generates contextual commentary based on simulated cognitive state.",
                           font=('Arial', 10),
                           bg='#1a1a1a', fg='#cccccc',
                           justify=tk.LEFT)
    instructions.pack(pady=(5, 0))
    
    print("🦉 Owl Console Panel Test Started")
    print("Use the buttons to test different message types and features.")
    print("The Owl Console provides high-trust cognitive commentary for DAWN.")
    
    # Start the GUI
    root.mainloop()

if __name__ == "__main__":
    main() 