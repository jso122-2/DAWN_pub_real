#!/usr/bin/env python3
"""
Script to add GIF saving functionality to all DAWN visualization scripts
"""

import os
import re
import glob
from pathlib import Path

def add_gif_imports(content):
    """Add GIF saver imports to the top of the file"""
    imports = [
        "import signal",
        "import atexit",
        "",
        "# Import GIF saver",
        "try:",
        "    from .gif_saver import setup_gif_saver",
        "except ImportError:",
        "    from gif_saver import setup_gif_saver"
    ]
    
    # Find the last import statement
    lines = content.split('\n')
    last_import = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith('import ') or line.strip().startswith('from '):
            last_import = i
    
    # Insert new imports after the last import
    lines.insert(last_import + 1, '\n'.join(imports))
    return '\n'.join(lines)

def add_gif_saver_to_class(content, class_name):
    """Add GIF saver initialization to the class __init__ method"""
    # Find the class definition
    class_pattern = rf'class {class_name}:'
    class_match = re.search(class_pattern, content)
    
    if not class_match:
        return content
    
    # Find the __init__ method
    init_pattern = r'def __init__\(self[^)]*\):'
    init_match = re.search(init_pattern, content)
    
    if not init_match:
        return content
    
    # Find the end of __init__ method (indentation level)
    init_start = init_match.start()
    lines = content.split('\n')
    
    # Find the end of __init__ method
    init_end = init_start
    init_indent = None
    
    for i, line in enumerate(lines[init_start:], init_start):
        if init_indent is None and line.strip():
            init_indent = len(line) - len(line.lstrip())
        elif init_indent is not None:
            if line.strip() and len(line) - len(line.lstrip()) <= init_indent:
                init_end = i
                break
    
    # Add GIF saver initialization
    gif_init = [
        "",
        "        # Setup GIF saver",
        f"        self.gif_saver = setup_gif_saver(\"{class_name.lower()}\")",
        "",
        "        # Register cleanup function",
        "        atexit.register(self.cleanup)",
        "        signal.signal(signal.SIGINT, self.signal_handler)",
        "        signal.signal(signal.SIGTERM, self.signal_handler)"
    ]
    
    # Insert before the end of __init__
    lines.insert(init_end, '\n'.join(gif_init))
    return '\n'.join(lines)

def add_gif_methods(content, class_name):
    """Add GIF saving methods to the class"""
    methods = [
        "",
        "    def save_animation_gif(self):",
        "        \"\"\"Save the animation as GIF\"\"\"",
        "        try:",
        "            if hasattr(self, 'animation'):",
        "                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=10, dpi=100)",
        "                if gif_path:",
        "                    print(f\"\\nAnimation GIF saved: {gif_path}\", file=sys.stderr)",
        "                else:",
        "                    print(\"\\nFailed to save animation GIF\", file=sys.stderr)",
        "            else:",
        "                print(\"\\nNo animation to save\", file=sys.stderr)",
        "        except Exception as e:",
        "            print(f\"\\nError saving animation GIF: {e}\", file=sys.stderr)",
        "",
        "    def cleanup(self):",
        "        \"\"\"Cleanup function to save GIF\"\"\"",
        "        self.save_animation_gif()",
        "",
        "    def signal_handler(self, signum, frame):",
        "        \"\"\"Signal handler to save GIF on termination\"\"\"",
        "        print(f\"\\nReceived signal {signum}, saving GIF...\", file=sys.stderr)",
        "        self.save_animation_gif()",
        "        sys.exit(0)"
    ]
    
    # Add methods at the end of the class
    lines = content.split('\n')
    class_end = len(lines)
    
    # Find the end of the class
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith(' ') and not line.startswith('\t'):
            if i > 0 and lines[i-1].strip() == '':
                class_end = i - 1
                break
    
    lines.insert(class_end, '\n'.join(methods))
    return '\n'.join(lines)

def modify_run_method(content):
    """Modify the run method to save animation and handle signals"""
    # Find the run method
    run_pattern = r'def run\(self[^)]*\):'
    run_match = re.search(run_pattern, content)
    
    if not run_match:
        return content
    
    # Replace the run method content
    old_run = r'def run\(self[^)]*\):.*?plt\.show\(\)'
    new_run = '''def run(self, interval=200):
        """Start the real-time visualization"""
        try:
            self.animation = animation.FuncAnimation(self.fig, self.update_visualization,
                                                   interval=interval, blit=False, cache_frame_data=False)
            plt.show()
        except KeyboardInterrupt:
            print("\\nVisualization terminated by user.")
            self.save_animation_gif()
        except Exception as e:
            print(f"Runtime error: {e}", file=sys.stderr)
            self.save_animation_gif()'''
    
    content = re.sub(old_run, new_run, content, flags=re.DOTALL)
    return content

def process_script(file_path):
    """Process a single visualization script"""
    print(f"Processing: {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Get the main class name
    class_match = re.search(r'class (\w+):', content)
    if not class_match:
        print(f"  No class found in {file_path}")
        return
    
    class_name = class_match.group(1)
    print(f"  Found class: {class_name}")
    
    # Add imports
    content = add_gif_imports(content)
    
    # Add GIF saver to class
    content = add_gif_saver_to_class(content, class_name)
    
    # Add GIF methods
    content = add_gif_methods(content, class_name)
    
    # Modify run method
    content = modify_run_method(content)
    
    # Write back to file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"  Updated: {file_path}")

def main():
    """Main function to process all visualization scripts"""
    visual_dir = Path(__file__).parent
    
    # Find all Python files in the visual directory
    script_files = list(visual_dir.glob('*.py'))
    
    # Filter out utility files
    exclude_files = ['gif_saver.py', 'add_gif_saving.py', 'test_stdin_reader.py']
    script_files = [f for f in script_files if f.name not in exclude_files]
    
    print(f"Found {len(script_files)} visualization scripts to process:")
    for script_file in script_files:
        print(f"  - {script_file.name}")
    
    print("\nProcessing scripts...")
    for script_file in script_files:
        try:
            process_script(script_file)
        except Exception as e:
            print(f"Error processing {script_file}: {e}")
    
    print("\nDone! All scripts have been updated with GIF saving functionality.")

if __name__ == "__main__":
    main() 