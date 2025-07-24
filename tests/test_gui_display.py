#!/usr/bin/env python3
"""
Test script for GUI display functionality
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_gui_display():
    """Test GUI display components"""
    print("🖥️ Testing GUI Display Components")
    print("=" * 50)
    
    try:
        # Test tkinter availability
        print("🔧 Testing tkinter availability...")
        import tkinter as tk
        print("✅ tkinter imported successfully")
        
        # Test GUI components
        try:
            from gui.dawn_gui_tk import DawnGUITk
            print("✅ DawnGUITk imported successfully")
        except Exception as e:
            print(f"❌ DawnGUITk import failed: {e}")
        
        try:
            from gui.dawn_gui_enhanced import EnhancedDawnGUI
            print("✅ EnhancedDawnGUI imported successfully")
        except Exception as e:
            print(f"❌ EnhancedDawnGUI import failed: {e}")
        
        # Test display creation
        print("\n🎨 Testing basic display creation...")
        root = tk.Tk()
        root.title("DAWN Display Test")
        root.geometry("400x300")
        
        # Create a test label
        test_label = tk.Label(root, text="DAWN GUI Test", font=("Arial", 16))
        test_label.pack(pady=20)
        
        print("✅ Basic tkinter window created successfully")
        
        # Don't actually show the window in test mode
        root.withdraw()
        root.destroy()
        
        print("✅ GUI display test completed successfully")
        
    except Exception as e:
        print(f"❌ GUI display test failed: {e}")
        import traceback
        traceback.print_exc()


def test_canvas_functionality():
    """Test canvas-specific functionality"""
    print("\n🎯 Testing Canvas Functionality")
    print("=" * 40)
    
    try:
        import tkinter as tk
        from tkinter import Canvas
        
        root = tk.Tk()
        root.withdraw()  # Hide window during test
        
        # Create test canvas
        canvas = Canvas(root, width=300, height=200, bg='black')
        canvas.pack()
        
        # Test drawing operations
        canvas.create_oval(50, 50, 150, 150, fill='blue', outline='white')
        canvas.create_line(0, 0, 300, 200, fill='red', width=2)
        canvas.create_text(150, 100, text="DAWN", fill='white', font=("Arial", 14))
        
        print("✅ Canvas drawing operations successful")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Canvas test failed: {e}")


if __name__ == "__main__":
    test_gui_display()
    test_canvas_functionality()
    print("\n🏆 All GUI display tests completed!") 