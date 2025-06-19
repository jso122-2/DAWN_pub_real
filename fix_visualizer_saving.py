#!/usr/bin/env python3
"""
Fix all visualizers to work properly in headless mode and save images correctly.
"""

import os
import re
import glob

def fix_visualizer_file(filepath):
    """Fix a single visualizer file"""
    print(f"Fixing {filepath}...")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if it already has the fixed run method
    if 'matplotlib.get_backend() == \'Agg\'' in content:
        print(f"  Already fixed, skipping...")
        return
    
    # Find the run method
    run_pattern = r'def run\(self, interval=200\):\s*\n\s*"""Start the real-time visualization"""\s*\n\s*try:\s*\n\s*self\.animation = animation\.FuncAnimation\(self\.fig, self\.update_visualization,\s*\n\s*interval=interval, blit=False, cache_frame_data=False\)\s*\n\s*plt\.show\(\)\s*\n\s*except KeyboardInterrupt:\s*\n\s*print\("\nVisualization terminated by user\."\)\s*\n\s*self\.save_animation_gif\(\)\s*\n\s*except Exception as e:\s*\n\s*print\(f"Runtime error: \{e\}", file=sys\.stderr\)\s*\n\s*self\.save_animation_gif\(\)'
    
    new_run_method = '''def run(self, interval=200):
        """Start the real-time visualization"""
        try:
            # In headless mode, we need to create the animation differently
            if matplotlib.get_backend() == 'Agg':
                # Headless mode: create animation without showing
                self.animation = animation.FuncAnimation(
                    self.fig, 
                    self.update_visualization,
                    interval=interval, 
                    blit=False, 
                    cache_frame_data=False,
                    repeat=False  # Don't repeat in headless mode
                )
                
                # Start the stdin reader thread if it exists
                if hasattr(self, 'stdin_reader'):
                    self.stdin_thread = threading.Thread(target=self.stdin_reader, daemon=True)
                    self.stdin_thread.start()
                elif hasattr(self, 'read_stdin_data'):
                    self.stdin_thread = threading.Thread(target=self.read_stdin_data, daemon=True)
                    self.stdin_thread.start()
                
                # Run the animation for a fixed number of frames or until interrupted
                try:
                    # Keep running until interrupted
                    while True:
                        time.sleep(interval / 1000.0)  # Convert to seconds
                        # Force a redraw
                        self.fig.canvas.draw()
                        
                except KeyboardInterrupt:
                    print("\\nVisualization terminated by user.")
                    self.save_animation_gif()
                    
            else:
                # Interactive mode: use plt.show()
                self.animation = animation.FuncAnimation(
                    self.fig, 
                    self.update_visualization,
                    interval=interval, 
                    blit=False, 
                    cache_frame_data=False
                )
                plt.show()
                
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)
            self.save_animation_gif()'''
    
    # Replace the run method
    if re.search(run_pattern, content, re.MULTILINE | re.DOTALL):
        content = re.sub(run_pattern, new_run_method, content, flags=re.MULTILINE | re.DOTALL)
        
        # Add save_static_image method if it doesn't exist
        if 'def save_static_image(self):' not in content:
            save_static_method = '''
    def save_static_image(self):
        """Save current state as a static PNG image"""
        try:
            # Update the visualization one more time to ensure current state
            self.update_visualization(0)
            
            # Save the current figure as PNG
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            script_name = os.path.basename(__file__).replace(".py", "")
            filename = f"{script_name}_{timestamp}.png"
            output_path = os.path.join(self.gif_saver.output_dir, filename)
            
            self.fig.savefig(output_path, dpi=100, bbox_inches='tight')
            print(f"\\nStatic image saved: {output_path}", file=sys.stderr)
            
        except Exception as e:
            print(f"\\nError saving static image: {e}", file=sys.stderr)'''
            
            # Find a good place to insert the method (before the cleanup method)
            if 'def cleanup(self):' in content:
                content = content.replace('def cleanup(self):', save_static_method + '\n\n    def cleanup(self):')
            else:
                # Add at the end of the class
                content = content.replace('    def signal_handler(self, signum, frame):', 
                                        save_static_method + '\n\n    def signal_handler(self, signum, frame):')
        
        # Fix the save_animation_gif method if it exists
        save_gif_pattern = r'if hasattr\(self, \'animation\'\):'
        if save_gif_pattern in content:
            content = content.replace(save_gif_pattern, 'if hasattr(self, \'animation\') and self.animation is not None:')
            
            # Add fallback to static image
            no_animation_pattern = r'print\("\nNo animation to save", file=sys\.stderr\)'
            if no_animation_pattern in content:
                content = content.replace(no_animation_pattern, 
                                        '# Save a static image instead\n                self.save_static_image()')
        
        # Add missing imports if needed
        if 'import os' not in content and 'import time' not in content:
            # Find the import section and add missing imports
            import_pattern = r'(import [^\n]+\n)'
            imports = re.findall(import_pattern, content)
            if imports:
                # Add after the last import
                last_import = imports[-1]
                if 'import os' not in content:
                    content = content.replace(last_import, last_import + 'import os\n')
                if 'import time' not in content:
                    content = content.replace(last_import, last_import + 'import time\n')
        
        # Write the fixed content back
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"  Fixed {filepath}")
    else:
        print(f"  Could not find run method pattern in {filepath}")

def main():
    """Fix all visualizer files"""
    visualizer_files = glob.glob('backend/visual/*.py')
    
    # Filter out non-visualizer files
    visualizer_files = [f for f in visualizer_files if not f.endswith('__init__.py')]
    visualizer_files = [f for f in visualizer_files if not f.endswith('gif_saver.py')]
    visualizer_files = [f for f in visualizer_files if not f.endswith('add_gif_saving.py')]
    visualizer_files = [f for f in visualizer_files if not f.endswith('fix_visualizer_saving.py')]
    
    print(f"Found {len(visualizer_files)} visualizer files to fix:")
    for f in visualizer_files:
        print(f"  {f}")
    
    print("\nFixing visualizers...")
    for filepath in visualizer_files:
        try:
            fix_visualizer_file(filepath)
        except Exception as e:
            print(f"Error fixing {filepath}: {e}")
    
    print("\nDone!")

if __name__ == "__main__":
    main() 