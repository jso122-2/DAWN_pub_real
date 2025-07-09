#!/usr/bin/env python3
"""
Test FractalCanvas Debug System
Demonstrates the enhanced live visual debugger for bloom signature failures
"""

import sys
import os
import tkinter as tk
import time
import math

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from gui.fractal_canvas import FractalCanvas

def test_fractal_debug_system():
    """Test the enhanced debug system with various bloom data scenarios"""
    
    print("🧪 FRACTAL CANVAS DEBUG SYSTEM TEST")
    print("="*60)
    print("This test demonstrates the live visual debugger that turns")
    print("bloom failures into readable diagnostic output.")
    print("="*60)
    
    # Create test window
    root = tk.Tk()
    root.title("FractalCanvas Debug Test")
    root.geometry("400x500")
    root.configure(bg="#0a0a0a")
    
    # Create fractal canvas
    fractal_canvas = FractalCanvas(root, width=300, height=300)
    fractal_canvas.pack(pady=20)
    
    # Test data scenarios
    test_scenarios = [
        {
            "name": "🌟 Perfect Bloom Data",
            "data": {
                "depth": 5,
                "entropy": 0.7,
                "lineage": [2, 3, 1],
                "semantic_drift": 0.4,
                "rebloom_status": "emerging",
                "complexity": 0.8
            }
        },
        {
            "name": "⚠️ Problematic String Data",
            "data": {
                "depth": "not_a_number",
                "entropy": "high",
                "lineage": "broken",
                "semantic_drift": None,
                "rebloom_status": 123,
                "complexity": {"nested": "data"}
            }
        },
        {
            "name": "🔥 NaN and Infinity Chaos",
            "data": {
                "depth": float('nan'),
                "entropy": float('inf'),
                "lineage": [],
                "semantic_drift": -float('inf'),
                "rebloom_status": "",
                "complexity": 0.0
            }
        },
        {
            "name": "💥 Non-Dictionary Input",
            "data": "this_is_not_a_dict"
        },
        {
            "name": "🌀 Extreme Values",
            "data": {
                "depth": 999,
                "entropy": -5.0,
                "lineage": [x for x in range(100)],  # Huge lineage
                "semantic_drift": 10.0,
                "rebloom_status": "超級不穩定",  # Unicode
                "complexity": math.pi
            }
        }
    ]
    
    current_test = [0]  # Use list for closure access
    
    def cycle_tests():
        """Cycle through test scenarios"""
        if current_test[0] < len(test_scenarios):
            scenario = test_scenarios[current_test[0]]
            
            print(f"\n🧪 TESTING SCENARIO {current_test[0] + 1}: {scenario['name']}")
            print("-" * 40)
            
            # Apply the test data to fractal canvas
            fractal_canvas.draw_bloom_signature(scenario['data'])
            
            current_test[0] += 1
            
            # Schedule next test
            if current_test[0] < len(test_scenarios):
                root.after(5000, cycle_tests)  # 5 second delay
            else:
                print("\\n🎉 ALL DEBUG TESTS COMPLETE!")
                print("The FractalCanvas now provides comprehensive debug output")
                print("for any bloom data issues. Every failure tells a story!")
        
    # Control buttons
    button_frame = tk.Frame(root, bg="#0a0a0a")
    button_frame.pack(pady=10)
    
    def next_test():
        if current_test[0] < len(test_scenarios):
            cycle_tests()
    
    def reset_tests():
        current_test[0] = 0
        print("\\n🔄 Tests reset - ready to start over")
    
    next_btn = tk.Button(button_frame, text="Next Test", command=next_test,
                        bg="#333333", fg="#ffffff", font=("Arial", 10))
    next_btn.pack(side=tk.LEFT, padx=5)
    
    reset_btn = tk.Button(button_frame, text="Reset", command=reset_tests,
                         bg="#333333", fg="#ffffff", font=("Arial", 10))
    reset_btn.pack(side=tk.LEFT, padx=5)
    
    # Info label
    info_label = tk.Label(root, 
                         text="Click 'Next Test' to cycle through debug scenarios\\n"
                              "Watch the console for detailed debug output!",
                         bg="#0a0a0a", fg="#cccccc", font=("Arial", 9),
                         justify=tk.CENTER)
    info_label.pack(pady=10)
    
    # Start with first test
    print("\\n🚀 Starting debug test sequence...")
    print("Watch the console output for detailed bloom analysis!")
    root.after(1000, cycle_tests)
    
    # Run the test
    root.mainloop()

if __name__ == "__main__":
    test_fractal_debug_system() 