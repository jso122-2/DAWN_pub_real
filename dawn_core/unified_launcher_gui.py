#!/usr/bin/env python3
"""
DAWN Unified Launcher GUI - Single Interface for All DAWN Components
Lightweight GUI that consolidates all launcher scripts into one interface.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
import queue

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


class DAWNUnifiedLauncherGUI:
    """
    Unified GUI launcher for all DAWN components.
    Lightweight, fast, and consolidates all launcher functionality.
    """
    
    def __init__(self):
        """Initialize the unified launcher GUI."""
        self.root = tk.Tk()
        self.root.title("DAWN Unified Launcher")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a1a')
        
        # Color scheme - keep it lightweight
        self.colors = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'accent': '#00ff88',
            'button': '#2a2a2a',
            'button_active': '#3a3a3a',
            'warning': '#ffaa00',
            'success': '#00ff88',
            'error': '#ff4444'
        }
        
        # Running processes tracking
        self.running_processes = {}
        self.output_queue = queue.Queue()
        
        # Setup GUI
        self.setup_gui()
        
        # Start output monitoring
        self.monitor_output()
    
    def setup_gui(self):
        """Setup the main GUI layout."""
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🌅 DAWN Unified Launcher",
            font=('Consolas', 16, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['accent']
        )
        title_label.pack(pady=(0, 20))
        
        # Create sections
        self.setup_core_section(main_frame)
        self.setup_gui_section(main_frame)
        self.setup_specialized_section(main_frame)
        self.setup_output_section(main_frame)
        self.setup_control_section(main_frame)
    
    def setup_core_section(self, parent):
        """Setup core launcher section."""
        core_frame = tk.LabelFrame(
            parent,
            text="Core Systems",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2
        )
        core_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Core buttons grid
        core_grid = tk.Frame(core_frame, bg=self.colors['bg'])
        core_grid.pack(fill=tk.X, padx=10, pady=10)
        
        core_launchers = [
            ("🧠 DAWN Core Engine", "dawn_core/launch.py engine", "Main cognitive engine"),
            ("🔄 DAWN Unified", "launcher_scripts/launch_dawn_unified.py", "Complete consciousness system"),
            ("⚡ Enhanced DAWN", "launcher_scripts/launch_enhanced_dawn_gui.py", "Enhanced GUI with reflex"),
            ("🎯 Dawn Master Clean", "launcher_scripts/launch_dawn_master_clean.py", "Clean master interface")
        ]
        
        for i, (name, script, desc) in enumerate(core_launchers):
            btn = self.create_launcher_button(core_grid, name, script, desc)
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky='ew')
        
        # Configure grid weights
        core_grid.columnconfigure(0, weight=1)
        core_grid.columnconfigure(1, weight=1)
    
    def setup_gui_section(self, parent):
        """Setup GUI launcher section."""
        gui_frame = tk.LabelFrame(
            parent,
            text="GUI Interfaces",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2
        )
        gui_frame.pack(fill=tk.X, pady=(0, 10))
        
        gui_grid = tk.Frame(gui_frame, bg=self.colors['bg'])
        gui_grid.pack(fill=tk.X, padx=10, pady=10)
        
        gui_launchers = [
            ("🖥️ DAWN Dashboard", "dawn_core/launch.py gui", "Real-time cognitive dashboard"),
            ("🔮 Forecast GUI", "launcher_scripts/launch_forecast_gui.py", "Forecasting visualizer"),
            ("🎨 DAWN GUI Safe", "launcher_scripts/launch_dawn_gui_safe.py", "Safe GUI interface"),
            ("🌸 Sigil GUI", "launcher_scripts/launch_dawn_gui_with_sigils.py", "Sigil visualization"),
            ("🦉 Owl Commentary", "launcher_scripts/launch_dawn_with_owl_commentary.py", "Owl bridge interface"),
            ("🔗 Connect to Live", "launcher_scripts/connect_gui_to_live_dawn.py", "Connect to running DAWN")
        ]
        
        for i, (name, script, desc) in enumerate(gui_launchers):
            btn = self.create_launcher_button(gui_grid, name, script, desc)
            btn.grid(row=i//3, column=i%3, padx=3, pady=3, sticky='ew')
        
        # Configure grid weights
        for col in range(3):
            gui_grid.columnconfigure(col, weight=1)
    
    def setup_specialized_section(self, parent):
        """Setup specialized launcher section."""
        spec_frame = tk.LabelFrame(
            parent,
            text="Specialized Systems",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2
        )
        spec_frame.pack(fill=tk.X, pady=(0, 10))
        
        spec_grid = tk.Frame(spec_frame, bg=self.colors['bg'])
        spec_grid.pack(fill=tk.X, padx=10, pady=10)
        
        spec_launchers = [
            ("📦 Snapshot Export", "dawn_core/launch.py snapshot", "System snapshot creator"),
            ("🔬 Symbolic Anatomy", "launcher_scripts/launch_symbolic_anatomy_demo.py", "Symbolic anatomy demo"),
            ("🤖 Autonomous Reactor", "launcher_scripts/launch_dawn_autonomous_reactor.py", "Autonomous response system"),
            ("📊 Complete Consciousness", "launcher_scripts/launch_complete_dawn_consciousness.py", "Full consciousness"),
            ("🧮 Codex Integration", "launcher_scripts/launch_dawn_codex_integration.py", "Codex system"),
            ("🔥 Enhanced Entropy", "launcher_scripts/launch_dawn_with_enhanced_entropy.py", "Enhanced entropy system")
        ]
        
        for i, (name, script, desc) in enumerate(spec_launchers):
            btn = self.create_launcher_button(spec_grid, name, script, desc)
            btn.grid(row=i//3, column=i%3, padx=3, pady=3, sticky='ew')
        
        # Configure grid weights
        for col in range(3):
            spec_grid.columnconfigure(col, weight=1)
    
    def setup_output_section(self, parent):
        """Setup output monitoring section."""
        output_frame = tk.LabelFrame(
            parent,
            text="System Output",
            font=('Consolas', 12, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg'],
            bd=2
        )
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=8,
            font=('Consolas', 9),
            bg='#2a2a2a',
            fg=self.colors['fg'],
            insertbackground=self.colors['accent'],
            wrap=tk.WORD
        )
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add initial message
        self.add_output("🌅 DAWN Unified Launcher initialized")
        self.add_output("Click any button to launch DAWN components")
    
    def setup_control_section(self, parent):
        """Setup control buttons section."""
        control_frame = tk.Frame(parent, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X)
        
        # Control buttons
        self.stop_all_button = tk.Button(
            control_frame,
            text="🛑 Stop All",
            command=self.stop_all_processes,
            font=('Consolas', 11, 'bold'),
            bg=self.colors['error'],
            fg='#ffffff',
            activebackground='#cc3333',
            relief='flat',
            padx=20
        )
        self.stop_all_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_output_button = tk.Button(
            control_frame,
            text="🗑️ Clear Output",
            command=self.clear_output,
            font=('Consolas', 11),
            bg=self.colors['button'],
            fg=self.colors['fg'],
            activebackground=self.colors['button_active'],
            relief='flat',
            padx=20
        )
        self.clear_output_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            control_frame,
            text=f"Running processes: 0",
            font=('Consolas', 10),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.status_label.pack(side=tk.RIGHT)
    
    def create_launcher_button(self, parent, name, script, description):
        """Create a launcher button with tooltip."""
        
        def launch_command():
            self.launch_script(name, script)
        
        btn = tk.Button(
            parent,
            text=name,
            command=launch_command,
            font=('Consolas', 10),
            bg=self.colors['button'],
            fg=self.colors['fg'],
            activebackground=self.colors['button_active'],
            relief='flat',
            padx=10,
            pady=5,
            width=20
        )
        
        # Add tooltip (simple implementation)
        def on_enter(event):
            btn.config(bg=self.colors['button_active'])
            self.add_output(f"ℹ️ {description}")
        
        def on_leave(event):
            btn.config(bg=self.colors['button'])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def launch_script(self, name, script_path):
        """Launch a DAWN script in the background."""
        try:
            self.add_output(f"🚀 Launching {name}...")
            
            # Prepare command
            if script_path.startswith("dawn_core/launch.py"):
                # Special handling for our unified launcher
                cmd_parts = script_path.split()
                cmd = [sys.executable] + cmd_parts
            else:
                cmd = [sys.executable, script_path]
            
            # Start process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=str(project_root)
            )
            
            # Track process
            self.running_processes[name] = process
            self.update_status()
            
            # Start output monitoring thread
            output_thread = threading.Thread(
                target=self.monitor_process_output,
                args=(name, process),
                daemon=True
            )
            output_thread.start()
            
            self.add_output(f"✅ {name} launched successfully (PID: {process.pid})")
            
        except Exception as e:
            self.add_output(f"❌ Failed to launch {name}: {e}")
    
    def monitor_process_output(self, name, process):
        """Monitor output from a launched process."""
        try:
            for line in process.stdout:
                if line.strip():
                    self.output_queue.put(f"[{name}] {line.strip()}")
            
            # Process finished
            return_code = process.wait()
            if return_code == 0:
                self.output_queue.put(f"✅ {name} completed successfully")
            else:
                self.output_queue.put(f"⚠️ {name} exited with code {return_code}")
            
            # Remove from running processes
            if name in self.running_processes:
                del self.running_processes[name]
                self.output_queue.put("STATUS_UPDATE")
                
        except Exception as e:
            self.output_queue.put(f"❌ Error monitoring {name}: {e}")
    
    def monitor_output(self):
        """Monitor the output queue and update GUI."""
        try:
            while True:
                try:
                    message = self.output_queue.get_nowait()
                    if message == "STATUS_UPDATE":
                        self.update_status()
                    else:
                        self.add_output(message)
                except queue.Empty:
                    break
        except Exception as e:
            pass
        
        # Schedule next check
        self.root.after(500, self.monitor_output)
    
    def add_output(self, message):
        """Add a message to the output display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.output_text.insert(tk.END, formatted_message)
        self.output_text.see(tk.END)
        
        # Limit output length
        lines = self.output_text.get("1.0", tk.END).split('\n')
        if len(lines) > 200:
            # Keep only last 150 lines
            self.output_text.delete("1.0", f"{len(lines)-150}.0")
    
    def clear_output(self):
        """Clear the output display."""
        self.output_text.delete("1.0", tk.END)
        self.add_output("🗑️ Output cleared")
    
    def stop_all_processes(self):
        """Stop all running processes."""
        if not self.running_processes:
            self.add_output("ℹ️ No running processes to stop")
            return
        
        stopped_count = 0
        for name, process in list(self.running_processes.items()):
            try:
                process.terminate()
                self.add_output(f"🛑 Stopped {name}")
                stopped_count += 1
            except Exception as e:
                self.add_output(f"⚠️ Error stopping {name}: {e}")
        
        # Clear the dict
        self.running_processes.clear()
        self.update_status()
        
        self.add_output(f"🛑 Stopped {stopped_count} processes")
    
    def update_status(self):
        """Update the status display."""
        count = len(self.running_processes)
        self.status_label.config(text=f"Running processes: {count}")
        
        if count > 0:
            self.status_label.config(fg=self.colors['success'])
        else:
            self.status_label.config(fg=self.colors['fg'])
    
    def on_closing(self):
        """Handle window closing."""
        if self.running_processes:
            if messagebox.askokcancel("Quit", "Stop all running processes and quit?"):
                self.stop_all_processes()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the launcher GUI."""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.add_output("🎯 Ready to launch DAWN components")
        self.root.mainloop()


def main():
    """Main entry point for the unified launcher."""
    print("🌅 Starting DAWN Unified Launcher GUI...")
    
    # Check for GUI availability
    try:
        import tkinter
    except ImportError:
        print("❌ Tkinter not available - cannot run GUI")
        print("   Install tkinter: sudo apt-get install python3-tk (Linux)")
        return
    
    # Create and run launcher
    launcher = DAWNUnifiedLauncherGUI()
    launcher.run()


if __name__ == "__main__":
    main() 