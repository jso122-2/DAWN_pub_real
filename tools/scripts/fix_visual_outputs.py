"""
Fix DAWN visual scripts to save output instead of just showing
"""

import os
from pathlib import Path
import re

def add_savefig_to_scripts():
    """Add savefig commands to scripts that only show plots"""
    
    visual_dir = Path("visual")
    fixed_count = 0
    
    print("🔧 Fixing visual scripts to save output...")
    print("=" * 60)
    
    for script_path in visual_dir.glob("*.py"):
        if script_path.name.startswith("__"):
            continue
            
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if already saves
            if 'savefig' in content:
                continue
            
            # Check if it uses matplotlib
            if 'plt.show()' not in content and 'pyplot.show()' not in content:
                continue
            
            print(f"\n📝 Fixing: {script_path.name}")
            
            # Create backup
            backup = script_path.with_suffix('.py.bak')
            with open(backup, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Add output directory creation
            if 'visual_output' not in content:
                import_section = []
                other_lines = []
                
                lines = content.split('\n')
                in_imports = True
                
                for line in lines:
                    if in_imports and (line.strip() == '' or not line.startswith(('import', 'from', '#'))):
                        in_imports = False
                        import_section.append('')
                        import_section.append('# Ensure output directory exists')
                        import_section.append('from pathlib import Path')
                        import_section.append('output_dir = Path("visual_output")')
                        import_section.append('output_dir.mkdir(exist_ok=True)')
                        import_section.append('')
                    
                    if in_imports:
                        import_section.append(line)
                    else:
                        other_lines.append(line)
                
                content = '\n'.join(import_section + other_lines)
            
            # Replace plt.show() with savefig + show
            script_base = script_path.stem
            
            # Pattern to find plt.show() or pyplot.show()
            show_pattern = r'(\s*)(plt\.show\(\)|pyplot\.show\(\))'
            
            def replace_show(match):
                indent = match.group(1)
                return f'{indent}# Save the figure\n{indent}output_path = output_dir / "{script_base}.png"\n{indent}plt.savefig(output_path, dpi=150, bbox_inches="tight")\n{indent}print(f"Saved to: {{output_path}}")\n{indent}plt.show()'
            
            content = re.sub(show_pattern, replace_show, content)
            
            # Handle cases where figure is created explicitly
            if 'fig' in content and 'plt.show()' in content:
                # Add figure saving before show
                lines = content.split('\n')
                new_lines = []
                
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    
                    # If this line has plt.show() and we haven't added savefig yet
                    if 'plt.show()' in line and i > 0:
                        # Check if previous lines have savefig
                        recent_lines = '\n'.join(lines[max(0, i-5):i])
                        if 'savefig' not in recent_lines:
                            indent = len(line) - len(line.lstrip())
                            new_lines.insert(-1, ' ' * indent + f'# Auto-added save')
                            new_lines.insert(-1, ' ' * indent + f'if "fig" in locals():')
                            new_lines.insert(-1, ' ' * indent + f'    fig.savefig(output_dir / "{script_base}_fig.png", dpi=150, bbox_inches="tight")')
                            new_lines.insert(-1, ' ' * indent + f'    print(f"Saved figure to: {{output_dir}}/{script_base}_fig.png")')
                
                content = '\n'.join(new_lines)
            
            # Write the fixed content
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Added save functionality")
            fixed_count += 1
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Fixed {fixed_count} scripts")
    print("\n💡 Original files backed up as .py.bak")
    
    return fixed_count

def test_fixed_scripts():
    """Test a few of the fixed scripts"""
    test_scripts = [
        "entropy_cluster_plot.py",
        "bloom_lineage_radar.py",
        "drift_compass.py",
        "pulse_zone_timeline.py",
        "memory_clusters.py"
    ]
    
    print("\n🧪 Testing fixed scripts...")
    
    for script in test_scripts:
        if Path(f"visual/{script}").exists():
            print(f"\n▶️ Testing {script}...")
            result = os.system(f"python run_visual.py {script}")
            if result == 0:
                print(f"  ✅ Success")
            else:
                print(f"  ❌ Failed")

def restore_backups():
    """Restore original scripts from backups"""
    visual_dir = Path("visual")
    restored = 0
    
    for backup in visual_dir.glob("*.py.bak"):
        original = backup.with_suffix('')
        try:
            with open(backup, 'r') as f:
                content = f.read()
            with open(original, 'w') as f:
                f.write(content)
            restored += 1
        except Exception as e:
            print(f"Error restoring {original}: {e}")
    
    print(f"Restored {restored} files from backups")

if __name__ == "__main__":
    print("🎨 DAWN Visual Output Fixer")
    print("=" * 60)
    print("This will modify scripts to save output instead of just displaying")
    print("\nOptions:")
    print("1. Fix scripts (add save functionality)")
    print("2. Test fixed scripts")
    print("3. Restore from backups")
    
    choice = input("\nChoice (1-3): ").strip()
    
    if choice == "1":
        fixed = add_savefig_to_scripts()
        if fixed > 0:
            print("\n🎯 Next step: Run option 2 to test the fixed scripts")
    elif choice == "2":
        test_fixed_scripts()
    elif choice == "3":
        restore_backups()
    else:
        print("Invalid choice")