"""
Fix DAWN visual scripts to save output, then test them
Run from Tick_engine directory
"""

import os
import re
from pathlib import Path
import subprocess
import sys
import time
import json
from datetime import datetime

class DawnVisualFixer:
    def __init__(self):
        self.visual_dir = Path("visual")
        self.fixed_scripts = []
        self.test_results = {}
        
    def fix_script_to_save(self, script_path):
        """Fix a single script to save output instead of just showing"""
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip if already saves
            if 'savefig' in content:
                return False
            
            # Check if it uses matplotlib
            if 'plt.show()' not in content and 'pyplot.show()' not in content:
                return False
            
            # Create backup
            backup = script_path.with_suffix('.py.bak')
            if not backup.exists():
                with open(backup, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Prepare the modified content
            lines = content.split('\n')
            modified_lines = []
            added_imports = False
            script_name = script_path.stem
            
            # First pass - add imports
            for i, line in enumerate(lines):
                modified_lines.append(line)
                
                # Add output setup after imports
                if not added_imports and line.strip() and not line.startswith(('import', 'from', '#')):
                    if 'visual_output' not in content:
                        modified_lines.insert(-1, '\n# Setup output directory')
                        modified_lines.insert(-1, 'from pathlib import Path')
                        modified_lines.insert(-1, 'output_dir = Path("visual_output")')
                        modified_lines.insert(-1, 'output_dir.mkdir(exist_ok=True)')
                        modified_lines.insert(-1, '')
                    added_imports = True
            
            content = '\n'.join(modified_lines)
            
            # Replace plt.show() with save + show
            # Count occurrences to create unique filenames
            show_count = content.count('plt.show()')
            
            if show_count == 1:
                # Single plot - simple replacement
                replacement = f'''output_path = output_dir / "{script_name}.png"
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"✅ Saved to: {{output_path}}")
plt.show()'''
                content = content.replace('plt.show()', replacement)
            else:
                # Multiple plots - number them
                counter = 0
                def replace_show(match):
                    nonlocal counter
                    counter += 1
                    return f'''output_path = output_dir / "{script_name}_plot{counter}.png"
plt.savefig(output_path, dpi=150, bbox_inches="tight")
print(f"✅ Saved plot {counter} to: {{output_path}}")
plt.show()'''
                
                content = re.sub(r'plt\.show\(\)', replace_show, content)
            
            # Save the fixed content
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.fixed_scripts.append(script_path.name)
            return True
            
        except Exception as e:
            print(f"❌ Error fixing {script_path.name}: {e}")
            return False
    
    def fix_all_scripts(self):
        """Fix all visual scripts to save output"""
        print("🔧 Fixing visual scripts to save output...")
        print("=" * 60)
        
        scripts = list(self.visual_dir.glob("*.py"))
        scripts = [s for s in scripts if not s.name.startswith("__")]
        
        fixed_count = 0
        for script in scripts:
            if self.fix_script_to_save(script):
                print(f"✅ Fixed: {script.name}")
                fixed_count += 1
        
        print(f"\n✅ Fixed {fixed_count} scripts to save output")
        print(f"💾 Backups saved as .py.bak files")
        
        return fixed_count
    
    def test_script(self, script_name, timeout=5):
        """Test a single script"""
        try:
            result = subprocess.run(
                [sys.executable, "run_visual.py", script_name],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=Path.cwd()
            )
            
            success = result.returncode == 0
            output_created = any(keyword in result.stdout.lower() 
                               for keyword in ['saved to:', 'created', 'output'])
            
            return {
                'success': success,
                'output_created': output_created,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'status': 'success' if success and output_created else 'failed'
            }
            
        except subprocess.TimeoutExpired:
            return {'status': 'timeout'}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def test_fixed_scripts(self):
        """Test only the scripts we fixed"""
        if not self.fixed_scripts:
            print("No scripts were fixed to test")
            return
        
        print(f"\n🧪 Testing {len(self.fixed_scripts)} fixed scripts...")
        print("=" * 60)
        
        working = []
        failed = []
        
        for i, script in enumerate(self.fixed_scripts, 1):
            print(f"[{i}/{len(self.fixed_scripts)}] Testing {script}... ", end='', flush=True)
            
            result = self.test_script(script)
            self.test_results[script] = result
            
            if result['status'] == 'success':
                working.append(script)
                print("✅ SUCCESS")
            elif result['status'] == 'timeout':
                print("⏱️ TIMEOUT")
            else:
                failed.append(script)
                print("❌ FAILED")
                if result.get('stderr'):
                    print(f"    Error: {result['stderr'].strip().split(chr(10))[-1][:60]}")
        
        print(f"\n📊 Results:")
        print(f"✅ Working: {len(working)}")
        print(f"❌ Failed: {len(failed)}")
        
        return working, failed
    
    def restore_backups(self):
        """Restore original scripts from backups"""
        restored = 0
        for backup in self.visual_dir.glob("*.py.bak"):
            original = backup.with_suffix('')
            try:
                with open(backup, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(original, 'w', encoding='utf-8') as f:
                    f.write(content)
                restored += 1
            except Exception as e:
                print(f"Error restoring {original}: {e}")
        
        print(f"✅ Restored {restored} files from backups")
    
    def create_test_report(self):
        """Create a simple test report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {
            'timestamp': timestamp,
            'fixed_scripts': self.fixed_scripts,
            'test_results': self.test_results
        }
        
        report_file = f"visual_fix_report_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Report saved to: {report_file}")


def main():
    fixer = DawnVisualFixer()
    
    print("🎨 DAWN Visual Script Fixer & Tester")
    print("=" * 60)
    print("This tool will:")
    print("1. Fix scripts to save output (plt.savefig)")
    print("2. Test the fixed scripts")
    print("3. Show you which ones work")
    print("\nOptions:")
    print("1. Fix and test all scripts")
    print("2. Test specific script")
    print("3. Restore from backups")
    print("4. Quick fix & test (first 10 scripts)")
    
    choice = input("\nChoice (1-4): ").strip()
    
    if choice == "1":
        # Fix all scripts
        fixed_count = fixer.fix_all_scripts()
        
        if fixed_count > 0:
            # Test the fixed scripts
            working, failed = fixer.test_fixed_scripts()
            
            # Create report
            fixer.create_test_report()
            
            # Show working scripts
            if working:
                print(f"\n✅ Working scripts you can run:")
                for script in working[:5]:
                    print(f"   python run_visual.py {script}")
                if len(working) > 5:
                    print(f"   ... and {len(working) - 5} more")
    
    elif choice == "2":
        script_name = input("Script name (e.g. entropy_cluster_plot.py): ").strip()
        script_path = Path("visual") / script_name
        
        if script_path.exists():
            # Fix if needed
            if fixer.fix_script_to_save(script_path):
                print(f"✅ Fixed {script_name}")
            
            # Test it
            print(f"\n🧪 Testing {script_name}...")
            result = fixer.test_script(script_name, timeout=10)
            
            if result['status'] == 'success':
                print("✅ Script works and creates output!")
            else:
                print(f"❌ Script failed: {result}")
        else:
            print(f"❌ Script not found: {script_name}")
    
    elif choice == "3":
        fixer.restore_backups()
    
    elif choice == "4":
        # Quick test - just fix first 10 scripts
        print("\n🚀 Quick fix & test mode...")
        
        scripts = list(Path("visual").glob("*.py"))[:10]
        for script in scripts:
            if fixer.fix_script_to_save(script):
                print(f"\n▶️ Testing {script.name}...")
                result = fixer.test_script(script.name)
                if result['status'] == 'success':
                    print("  ✅ Works!")
                    # Show the command
                    print(f"  Run: python run_visual.py {script.name}")
                    break  # Stop at first working script

if __name__ == "__main__":
    main()