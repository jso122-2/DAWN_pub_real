#!/usr/bin/env python3
"""
Fix All DAWN Visualizers Script
Adds headless mode, frame saving, and proper argument parsing to all visualizers
"""

import os
import sys
import re
import shutil
from pathlib import Path

# Visualizers that need fixing
VISUALIZERS_TO_FIX = [
    'scup_zone_animator.py',
    'consciousness_constellation.py', 
    'SCUP_pressure_grid.py',
    'semantic_flow_graph.py',
    'bloom_genealogy_network.py',
    'sigil_command_stream.py',
    'dawn_mood_state.py'
]

def add_headless_import(content):
    """Add matplotlib headless import at the top"""
    if 'matplotlib.use(\'Agg\')' in content:
        return content
    
    # Find matplotlib import line
    lines = content.split('\n')
    new_lines = []
    matplotlib_found = False
    
    for line in lines:
        if 'import matplotlib' in line and not matplotlib_found:
            new_lines.append("# Configure matplotlib for headless operation")
            new_lines.append("import matplotlib")
            new_lines.append("matplotlib.use('Agg')  # Use non-interactive backend")
            new_lines.append("")
            matplotlib_found = True
            if line.strip() != 'import matplotlib':
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def add_save_arguments(content):
    """Add --save and --output-dir arguments to argument parser"""
    if '--save' in content and '--output-dir' in content:
        return content
    
    # Find the argument parser section
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        # Add arguments before args = parser.parse_args()
        if 'args = parser.parse_args()' in line and i > 0:
            # Insert save arguments before this line
            new_lines.insert(-1, "    parser.add_argument('--save', action='store_true',")
            new_lines.insert(-1, "                       help='Save visualization frames as PNG files')")
            new_lines.insert(-1, "    parser.add_argument('--output-dir', default='./visual_output',")
            new_lines.insert(-1, "                       help='Directory to save output frames')")
            new_lines.insert(-1, "    ")
    
    return '\n'.join(new_lines)

def add_frame_saving_to_class(content, class_name):
    """Add frame saving functionality to the class"""
    if 'save_frames' in content and 'output_dir' in content:
        return content
    
    # Add to __init__ method
    init_pattern = rf'def __init__\(self[^)]*\):'
    
    def replace_init(match):
        init_line = match.group(0)
        # Add save parameters
        if 'save_frames=False' not in init_line:
            init_line = init_line.replace('):', ', save_frames=False, output_dir="./visual_output"):')
        return init_line
    
    content = re.sub(init_pattern, replace_init, content)
    
    # Add instance variables in __init__
    lines = content.split('\n')
    new_lines = []
    in_init = False
    added_save_vars = False
    
    for line in lines:
        new_lines.append(line)
        if 'def __init__(' in line:
            in_init = True
        elif in_init and not added_save_vars and ('self.' in line or line.strip() == ''):
            if 'self.save_frames' not in content:
                new_lines.insert(-1, "        self.save_frames = save_frames")
                new_lines.insert(-1, "        self.output_dir = output_dir")
                new_lines.insert(-1, "        self.frame_count = 0")
                new_lines.insert(-1, "        ")
                new_lines.insert(-1, "        # Create output directory if saving")
                new_lines.insert(-1, "        if self.save_frames:")
                new_lines.insert(-1, "            os.makedirs(self.output_dir, exist_ok=True)")
                new_lines.insert(-1, "        ")
                added_save_vars = True
        elif 'def ' in line and in_init:
            in_init = False
    
    return '\n'.join(new_lines)

def add_frame_saving_to_update(content):
    """Add frame saving to the update function"""
    if 'Save frame if requested' in content:
        return content
    
    # Find update functions
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        # Add frame saving at the end of update functions
        if ('return []' in line or 'return ' in line) and any('def update' in lines[j] for j in range(max(0, i-50), i)):
            # Add frame saving code before the return
            save_code = [
                "            ",
                "            # Save frame if requested",
                "            if self.save_frames and self.frame_count % 10 == 0:  # Save every 10th frame",
                "                filename = f\"{self.output_dir}/{self.__class__.__name__.lower()}_frame_{self.frame_count:06d}.png\"",
                "                self.fig.savefig(filename, dpi=100, bbox_inches='tight', ",
                "                               facecolor='#0a0a0a', edgecolor='none')",
                "            self.frame_count += 1",
                "            "
            ]
            for save_line in reversed(save_code):
                new_lines.insert(-1, save_line)
    
    return '\n'.join(new_lines)

def add_headless_run_mode(content):
    """Add headless run mode to run() method"""
    if 'save_frames' in content and 'range(1000)' in content:
        return content
    
    # Find run method and add headless mode
    lines = content.split('\n')
    new_lines = []
    in_run_method = False
    
    for i, line in enumerate(lines):
        if 'def run(' in line:
            in_run_method = True
            new_lines.append(line)
        elif in_run_method and 'plt.show()' in line:
            # Replace plt.show() with headless mode check
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + 'if self.save_frames:')
            new_lines.append(' ' * indent + '    # Headless mode: run limited frames')
            new_lines.append(' ' * indent + '    for frame in range(1000):')
            new_lines.append(' ' * indent + '        self.update_visualization(frame)')
            new_lines.append(' ' * indent + '        if frame % 50 == 0:')
            new_lines.append(' ' * indent + '            print(f"Processed frame {frame}", file=sys.stderr)')
            new_lines.append(' ' * indent + '    print(f"Frames saved to: {self.output_dir}")')
            new_lines.append(' ' * indent + 'else:')
            new_lines.append(' ' * indent + '    # Interactive mode')
            new_lines.append(line)
        elif in_run_method and 'def ' in line and not line.strip().startswith('def run'):
            in_run_method = False
            new_lines.append(line)
        else:
            new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_main_function(content):
    """Fix main function to pass save arguments"""
    if 'save_frames=args.save' in content:
        return content
    
    # Find where the class is instantiated and add save arguments
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if '= ' in line and '(' in line and ')' in line:
            # Look for class instantiation
            for class_name in ['SCUPZoneAnimator', 'ConsciousnessConstellation', 'SCUPPressureGrid', 
                              'SemanticFlowGraph', 'BloomGenealogyNetwork', 'SigilCommandStream', 'DawnMoodState']:
                if class_name in line and '(' in line:
                    # Add save arguments
                    if 'save_frames=' not in line:
                        line = line.replace(')', ', save_frames=args.save, output_dir=args.output_dir)')
                    break
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def fix_visualizer(file_path):
    """Fix a single visualizer file"""
    print(f"Fixing {file_path}...")
    
    try:
        with open(str(file_path), 'r') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all fixes
        content = add_headless_import(content)
        content = add_save_arguments(content)
        
        # Get class name from file
        class_match = re.search(r'class (\w+):', content)
        class_name = class_match.group(1) if class_match else 'Unknown'
        
        content = add_frame_saving_to_class(content, class_name)
        content = add_frame_saving_to_update(content)
        content = add_headless_run_mode(content)
        content = fix_main_function(content)
        
        # Only write if content changed
        if content != original_content:
            # Backup original
            backup_path = str(file_path) + '.backup'
            shutil.copy2(str(file_path), backup_path)
            
            # Write fixed content
            with open(str(file_path), 'w') as f:
                f.write(content)
            
            print(f"  ✅ Fixed {file_path}")
            print(f"  📦 Backup saved as {backup_path}")
        else:
            print(f"  ⏭️  No changes needed for {file_path}")
            
    except Exception as e:
        print(f"  ❌ Error fixing {file_path}: {e}")

def main():
    """Main function"""
    print("🔧 DAWN Visualizer Fix Script")
    print("=" * 50)
    
    backend_visual_dir = Path('backend/visual')
    if not backend_visual_dir.exists():
        print("❌ backend/visual directory not found!")
        return
    
    for visualizer in VISUALIZERS_TO_FIX:
        file_path = backend_visual_dir / visualizer
        if file_path.exists():
            fix_visualizer(file_path)
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n✅ All visualizers processed!")
    print("🔄 Ready to test with the batch script")

if __name__ == '__main__':
    main() 