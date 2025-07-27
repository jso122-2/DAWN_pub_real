#!/usr/bin/env python3
"""
Demo script showcasing OWL Sigil GUI integration
Quick demonstration of the OWL tracer with sigil processing GUI
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def demo_owl_sigil_gui():
    """Demonstrate OWL sigil GUI integration"""
    print("🦉 OWL Sigil GUI Integration Demo")
    print("=" * 40)
    
    try:
        # Test GUI components
        print("🔧 Testing GUI availability...")
        import tkinter as tk
        print("✅ tkinter available")
        
        # Test OWL components (if available)
        try:
            from reflection.owl.owl_tracer import OwlTracer
            print("✅ OwlTracer available")
        except ImportError as e:
            print(f"⚠️  OwlTracer not available: {e}")
        
        # Test reflex components
        try:
            from reflex.owl_panel import OwlPanel
            print("✅ OwlPanel available")
        except ImportError as e:
            print(f"⚠️  OwlPanel not available: {e}")
        
        # Create basic GUI demo
        print("\n🎨 Creating demo GUI...")
        root = tk.Tk()
        root.title("OWL Sigil Demo")
        root.geometry("600x400")
        root.configure(bg='black')
        
        # Create main frame
        main_frame = tk.Frame(root, bg='black', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="🦉 OWL Sigil Processor", 
                              font=("Arial", 16, "bold"), 
                              fg='white', bg='black')
        title_label.pack(pady=(0, 20))
        
        # Status display
        status_frame = tk.Frame(main_frame, bg='black')
        status_frame.pack(fill='x', pady=10)
        
        tk.Label(status_frame, text="Status:", font=("Arial", 12), 
                fg='cyan', bg='black').pack(anchor='w')
        
        status_text = tk.Text(status_frame, height=8, width=60, 
                             bg='gray10', fg='white', font=("Courier", 9))
        status_text.pack(fill='both', expand=True)
        
        # Add some demo content
        demo_content = """🦉 OWL Tracer Initialized
🔮 Sigil processing engine ready
📊 Pattern analysis: Active
🧠 Cognitive depth: Level 7
⚡ Analysis threads: 3 active
🎯 Tracking 5 bloom targets
"""
        status_text.insert('1.0', demo_content)
        status_text.config(state='disabled')
        
        # Control buttons
        button_frame = tk.Frame(main_frame, bg='black')
        button_frame.pack(fill='x', pady=20)
        
        def simulate_analysis():
            """Simulate an analysis cycle"""
            status_text.config(state='normal')
            status_text.insert('end', "\n🔍 Analysis cycle started...")
            status_text.insert('end', "\n📈 Pattern detected: Cognitive resonance")
            status_text.insert('end', "\n✨ Sigil evolution triggered")
            status_text.see('end')
            status_text.config(state='disabled')
        
        def clear_log():
            """Clear the status log"""
            status_text.config(state='normal')
            status_text.delete('1.0', 'end')
            status_text.insert('1.0', demo_content)
            status_text.config(state='disabled')
        
        analyze_btn = tk.Button(button_frame, text="🔍 Run Analysis", 
                               command=simulate_analysis,
                               bg='blue', fg='white', font=("Arial", 10))
        analyze_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = tk.Button(button_frame, text="🧹 Clear Log", 
                             command=clear_log,
                             bg='gray30', fg='white', font=("Arial", 10))
        clear_btn.pack(side='left')
        
        close_btn = tk.Button(button_frame, text="❌ Close", 
                             command=root.destroy,
                             bg='red', fg='white', font=("Arial", 10))
        close_btn.pack(side='right')
        
        print("✅ Demo GUI created successfully")
        print("💡 Close the window to continue...")
        
        # Run the GUI (will block until closed)
        root.mainloop()
        
        print("✅ GUI demo completed")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demo_owl_sigil_gui() 