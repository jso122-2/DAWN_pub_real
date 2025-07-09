#!/usr/bin/env python3
"""
Script to fix misplaced GIF saving methods in visualizer files
"""

import os
import re
from pathlib import Path

def fix_visualizer_file(file_path):
    """Fix a single visualizer file by removing misplaced GIF methods from top"""
    print(f"Fixing {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match misplaced GIF methods at the top
    pattern = r'^    def save_animation_gif\(self\):\s*\n(?:.*\n)*?    def signal_handler\(self, signum, frame\):\s*\n(?:.*\n)*?        sys\.exit\(0\)\s*\n\s*\n'
    
    # Remove the misplaced methods
    content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)
    
    # Find the class definition and add the methods properly
    class_pattern = r'(class \w+.*?:\s*\n.*?def __init__\(self[^)]*\):\s*\n(?:.*\n)*?)(\s+plt\.tight_layout\(\)|\s+logger\.info|\s+self\._active = True|\s+self\.current_tick = 0)'
    
    def add_gif_methods(match):
        class_start = match.group(1)
        next_line = match.group(2)
        
        gif_setup = '''
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("visualizer")

        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        '''
        
        gif_methods = '''
    def save_animation_gif(self):
        """Save the animation as GIF"""
        try:
            if hasattr(self, 'animation'):
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=10, dpi=100)
                if gif_path:
                    print(f"\\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\\nNo animation to save", file=sys.stderr)
        except Exception as e:
            print(f"\\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
        sys.exit(0)

'''
        
        return class_start + gif_setup + next_line + gif_methods
    
    content = re.sub(class_pattern, add_gif_methods, content, flags=re.MULTILINE | re.DOTALL)
    
    # Write the fixed content back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")

def main():
    """Fix all visualizer files"""
    visual_dir = Path("backend/visual")
    
    # Files that need fixing (based on the grep results)
    files_to_fix = [
        "bloom_genealogy_network.py",
        "semantic_flow_graph.py", 
        "SCUP_pressure_grid.py",
        "recursive_depth_explorer.py",
        "entropy_flow.py",
        "heat_monitor.py",
        "tick_pulse.py"
    ]
    
    for filename in files_to_fix:
        file_path = visual_dir / filename
        if file_path.exists():
            try:
                fix_visualizer_file(file_path)
            except Exception as e:
                print(f"Error fixing {filename}: {e}")
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main() 