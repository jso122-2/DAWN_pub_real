import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread
from pathlib import Path

def run_frontend():
    os.chdir('frontend')
    if sys.platform == 'win32':
        subprocess.run(['npm', 'install'], shell=True)
        subprocess.run(['npm', 'run', 'dev'], shell=True)
    else:
        subprocess.run(['npm', 'install'])
        subprocess.run(['npm', 'run', 'dev'])

def run_backend():
    os.chdir('backend')
    if sys.platform == 'win32':
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'], shell=True)
        subprocess.run(['python', 'visual_processes.py'], shell=True)
    else:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
        subprocess.run(['python', 'visual_processes.py'])

def setup_visual_components():
    """Setup visual components directory structure"""
    visual_dir = Path('visual')
    if not visual_dir.exists():
        visual_dir.mkdir()
        
    # Create __init__.py if it doesn't exist
    init_file = visual_dir / '__init__.py'
    if not init_file.exists():
        init_file.touch()
        
    # Create README.md if it doesn't exist
    readme_file = visual_dir / 'README.md'
    if not readme_file.exists():
        with open(readme_file, 'w') as f:
            f.write("""# DAWN Visual Components

This directory contains the visual components for the DAWN system:

- drift_vector_field.py: Semantic drift and vector field analysis
- mood_heatmap.py: Real-time emotional state heatmap
- sigil_trace_visualizer.py: Emotional sigil patterns and traces
- scup_zone_animator.py: SCUP zone visualization
- pulse_waveform_renderer.py: Core consciousness pulse visualization
- synthesis_entropy_chart.py: Entropy synthesis and distribution
- visual_consciousness_manager.py: Manages visual consciousness processes
- dawn_visualizer.py: Main visualizer for DAWN system state
- metrics_dashboard.py: System metrics visualization
- visual_utilities.py: Utility functions for visualizations
""")

if __name__ == '__main__':
    # Setup visual components
    setup_visual_components()
    
    # Start backend in a separate thread
    backend_thread = Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Wait for backend to start
    time.sleep(2)

    # Start frontend in a separate thread
    frontend_thread = Thread(target=run_frontend)
    frontend_thread.daemon = True
    frontend_thread.start()

    # Wait for frontend to start
    time.sleep(5)

    # Open browser
    webbrowser.open('http://localhost:5173/visuals')

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        sys.exit(0) 