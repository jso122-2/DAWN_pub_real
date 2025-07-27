#!/usr/bin/env python3
"""
Script to add GIF saving functionality to all DAWN visualization scripts
"""

import os
import re
import glob
from pathlib import Path

def ensure_import(content, import_line):
    """Ensure a specific import is present in the file."""
    if import_line not in content:
        # Insert after last import
        lines = content.split('\n')
        last_import = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                last_import = i
        lines.insert(last_import + 1, import_line)
        return '\n'.join(lines)
    return content

def add_gif_imports(content):
    """Add GIF saver imports to the top of the file, and ensure sys is imported."""
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
    lines.insert(last_import + 1, '\n'.join(imports))
    content = '\n'.join(lines)
    # Ensure sys is imported
    content = ensure_import(content, 'import sys')
    return content

def add_gif_saver_to_class(content, class_name):
    """Add GIF saver initialization to the class __init__ method, if not present."""
    class_pattern = rf'class {class_name}:'
    class_match = re.search(class_pattern, content)
    if not class_match:
        print(f"  [WARN] No class '{class_name}' found.")
        return content
    # Find the __init__ method
    init_pattern = r'def __init__\(self[^)]*\):'
    init_match = re.search(init_pattern, content)
    if not init_match:
        print(f"  [WARN] No __init__ found in class '{class_name}'.")
        return content
    # Check if gif_saver is already present
    if 'self.gif_saver' in content:
        return content
    # Find the end of __init__ method (indentation level)
    init_start = init_match.start()
    lines = content.split('\n')
    # Find the line number of __init__
    init_line = None
    for i, line in enumerate(lines):
        if 'def __init__(' in line:
            init_line = i
            break
    if init_line is None:
        return content
    # Find the end of __init__ by indentation
    init_indent = len(lines[init_line]) - len(lines[init_line].lstrip())
    insert_line = init_line + 1
    for i in range(init_line + 1, len(lines)):
        if lines[i].strip() and (len(lines[i]) - len(lines[i].lstrip())) <= init_indent:
            insert_line = i
            break
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
    lines.insert(insert_line, '\n'.join(gif_init))
    return '\n'.join(lines)

def add_gif_methods(content, class_name):
    """Add GIF saving methods to the class if not present."""
    if 'def save_animation_gif' in content:
        return content
    methods = [
        "",
        "    def save_animation_gif(self):",
        "        \"\"\"Save the animation as GIF\"\"\"",
        "        try:",
        "            if hasattr(self, 'animation'):",
        "                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)",
        "                if gif_path:",
        "                    print(f'\\nAnimation GIF saved: {gif_path}', file=sys.stderr)",
        "                else:",
        "                    print('\\nFailed to save animation GIF', file=sys.stderr)",
        "            else:",
        "                print('\\nNo animation to save', file=sys.stderr)",
        "        except Exception as e:",
        "            print(f'\\nError saving animation GIF: {e}', file=sys.stderr)",
        "",
        "    def cleanup(self):",
        "        \"\"\"Cleanup function to save GIF\"\"\"",
        "        self.save_animation_gif()",
        "",
        "    def signal_handler(self, signum, frame):",
        "        \"\"\"Signal handler to save GIF on termination\"\"\"",
        "        print(f'\\nReceived signal {signum}, saving GIF...', file=sys.stderr)",
        "        self.save_animation_gif()",
        "        sys.exit(0)"
    ]
    # Add methods at the end of the class
    lines = content.split('\n')
    # Find the last line of the class by indentation
    class_start = None
    for i, line in enumerate(lines):
        if f'class {class_name}:' in line:
            class_start = i
            break
    if class_start is None:
        return content
    # Find where the next class or function starts at the same or less indentation
    class_indent = len(lines[class_start]) - len(lines[class_start].lstrip())
    insert_line = len(lines)
    for i in range(class_start + 1, len(lines)):
        if lines[i].strip() and not lines[i].startswith(' ') and not lines[i].startswith('\t'):
            insert_line = i
            break
    lines.insert(insert_line, '\n'.join(methods))
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

            self.animation = animation.FuncAnimation(frames=1000, self.fig, self.update_visualization,
                                                   interval=interval, blit=False, cache_frame_data=False)
            plt.show()
            print("\\nVisualization terminated by user.")
            self.save_animation_gif()
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
        print(f"  [WARN] No class found in {file_path}")
        return
    class_name = class_match.group(1)
    print(f"  Found class: {class_name}")
    # Add imports
    content = add_gif_imports(content)
    # Add GIF saver to class
    content = add_gif_saver_to_class(content, class_name)
    # Add GIF methods
    content = add_gif_methods(content, class_name)
    # Modify run method (optional, not robust for all cases)
    # content = modify_run_method(content)
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

            process_script(script_file)
            print(f"Error processing {script_file}: {e}")
    
    print("\nDone! All scripts have been updated with GIF saving functionality.")

if __name__ == "__main__":
    main() 