#!/usr/bin/env python3
"""
🔧🎨 DAWN Visualization Import Fixer
====================================

Systematically fixes import issues in all DAWN visualization modules.
Based on the comprehensive debug analysis, this fixes the widespread
'sys' import issues affecting 12 out of 13 visualization modules.

Jackson's Clean Code Philosophy:
- No broken imports - consciousness deserves clean, working code
- Systematic fixes over individual patches
- Beautiful visualizations require beautiful code structure
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any

class VisualizationImportFixer:
    """
    Fixes import issues in DAWN visualization modules systematically.
    """
    
    def __init__(self):
        """Initialize the import fixer"""
        self.visual_dir = Path("visual")
        self.fixes_applied = []
        self.errors_encountered = []
        
        # List of files that need fixing (from debug analysis)
        self.files_to_fix = [
            "consciousness_visualization_service.py",
            "enhanced_visual_engine.py", 
            "consciousness_constellation.py",
            "gui_visualization_bridge.py",
            "visual_engine.py",
            "entropy_flow.py",
            "heat_monitor.py",
            "semantic_flow_graph.py",
            "bloom_genealogy_network.py",
            "tick_pulse.py",
            "scup_zone_animator.py",
            "SCUP_pressure_grid.py"
            # dawn_visual_beautiful.py is working, so excluded
        ]
    
    def fix_all_imports(self) -> Dict[str, Any]:
        """Fix import issues in all visualization files"""
        print("🔧🎨 DAWN Visualization Import Fixer")
        print("=" * 50)
        print(f"Fixing {len(self.files_to_fix)} visualization modules...")
        print()
        
        results = {
            'total_files': len(self.files_to_fix),
            'fixed_files': 0,
            'skipped_files': 0,
            'error_files': 0,
            'fixes_applied': [],
            'errors': []
        }
        
        for file_name in self.files_to_fix:
            file_path = self.visual_dir / file_name
            
            if not file_path.exists():
                print(f"⚠️ File not found: {file_name}")
                results['skipped_files'] += 1
                continue
            
            print(f"🔧 Fixing {file_name}...")
            
            try:
                fix_result = self._fix_file_imports(file_path)
                
                if fix_result['fixed']:
                    print(f"✅ Fixed {file_name}: {fix_result['description']}")
                    results['fixed_files'] += 1
                    results['fixes_applied'].append({
                        'file': file_name,
                        'fixes': fix_result['fixes']
                    })
                else:
                    print(f"ℹ️ No fixes needed for {file_name}")
                    results['skipped_files'] += 1
                    
            except Exception as e:
                print(f"❌ Error fixing {file_name}: {str(e)}")
                results['error_files'] += 1
                results['errors'].append({
                    'file': file_name,
                    'error': str(e)
                })
        
        # Print summary
        self._print_summary(results)
        
        return results
    
    def _fix_file_imports(self, file_path: Path) -> Dict[str, Any]:
        """Fix import issues in a specific file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_applied = []
        
        # Fix 1: sys.path.insert before sys import
        if 'sys.path.insert' in content and 'import sys' in content:
            # Check if sys.path.insert appears before import sys
            sys_path_pos = content.find('sys.path.insert')
            import_sys_pos = content.find('import sys')
            
            if sys_path_pos != -1 and import_sys_pos != -1 and sys_path_pos < import_sys_pos:
                # Move the sys.path.insert line after the imports
                lines = content.split('\n')
                new_lines = []
                sys_path_lines = []
                found_imports = False
                
                for line in lines:
                    if 'sys.path.insert' in line:
                        sys_path_lines.append(line)
                    elif line.strip().startswith('import ') or line.strip().startswith('from '):
                        new_lines.append(line)
                        found_imports = True
                    else:
                        new_lines.append(line)
                        # Add sys.path.insert lines after the first group of imports
                        if found_imports and sys_path_lines and not line.strip().startswith(('import ', 'from ', '#')):
                            new_lines.extend(sys_path_lines)
                            sys_path_lines = []
                            found_imports = False
                
                content = '\n'.join(new_lines)
                fixes_applied.append("Moved sys.path.insert after sys import")
        
        # Fix 2: Missing sys import before sys usage
        if 'sys.' in content and 'import sys' not in content:
            # Add import sys at the top after the shebang and docstring
            lines = content.split('\n')
            new_lines = []
            added_import = False
            
            for i, line in enumerate(lines):
                new_lines.append(line)
                
                # Add import sys after shebang/docstring but before first sys usage
                if not added_import and ('import ' in line or 'from ' in line) and 'sys' not in line:
                    new_lines.append('import sys')
                    added_import = True
                    break
            
            if not added_import:
                # If no other imports found, add after docstring
                for i, line in enumerate(lines):
                    if line.strip() and not line.startswith('#') and '"""' not in line:
                        lines.insert(i, 'import sys')
                        break
                content = '\n'.join(lines)
            else:
                content = '\n'.join(new_lines + lines[len(new_lines):])
            
            fixes_applied.append("Added missing sys import")
        
        # Fix 3: Duplicate imports
        import_lines = []
        other_lines = []
        for line in content.split('\n'):
            if line.strip().startswith(('import ', 'from ')) and 'import' in line:
                if line not in import_lines:
                    import_lines.append(line)
            else:
                other_lines.append(line)
        
        if len(import_lines) != len([l for l in content.split('\n') if l.strip().startswith(('import ', 'from '))]):
            # Reconstruct with deduplicated imports
            docstring_ended = False
            new_lines = []
            
            for line in content.split('\n'):
                if line.strip().startswith(('import ', 'from ')) and not docstring_ended:
                    if not any(imp in new_lines for imp in import_lines):
                        new_lines.extend(import_lines)
                        new_lines.append('')  # Empty line after imports
                    docstring_ended = True
                elif not line.strip().startswith(('import ', 'from ')):
                    new_lines.append(line)
            
            content = '\n'.join(new_lines)
            fixes_applied.append("Deduplicated imports")
        
        # Fix 4: Improve import organization
        if fixes_applied:
            content = self._organize_imports(content)
            fixes_applied.append("Organized import structure")
        
        # Write the fixed content back to file if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                'fixed': True,
                'description': f"Applied {len(fixes_applied)} fixes",
                'fixes': fixes_applied
            }
        else:
            return {
                'fixed': False,
                'description': "No fixes needed",
                'fixes': []
            }
    
    def _organize_imports(self, content: str) -> str:
        """Organize imports in a clean, standardized way"""
        lines = content.split('\n')
        
        # Separate different parts of the file
        shebang_and_docstring = []
        import_lines = []
        other_lines = []
        
        in_docstring = False
        docstring_ended = False
        
        for line in lines:
            if line.startswith('#!') or (line.strip().startswith('"""') and not docstring_ended):
                in_docstring = '"""' in line
                shebang_and_docstring.append(line)
                if line.strip().endswith('"""') and len(line.strip()) > 3:
                    in_docstring = False
                    docstring_ended = True
            elif in_docstring:
                shebang_and_docstring.append(line)
                if '"""' in line:
                    in_docstring = False
                    docstring_ended = True
            elif line.strip().startswith(('import ', 'from ')) and not docstring_ended:
                import_lines.append(line)
                docstring_ended = True
            else:
                other_lines.append(line)
                if not docstring_ended and line.strip():
                    docstring_ended = True
        
        # Organize imports: standard library, third party, local
        std_imports = []
        third_party_imports = []
        local_imports = []
        
        for imp in import_lines:
            if any(std_lib in imp for std_lib in ['sys', 'os', 'time', 'json', 'logging', 're', 'pathlib', 'datetime']):
                std_imports.append(imp)
            elif imp.strip().startswith('from visual.') or imp.strip().startswith('from core.') or imp.strip().startswith('from cognitive.'):
                local_imports.append(imp)
            else:
                third_party_imports.append(imp)
        
        # Reconstruct file with organized imports
        organized_lines = []
        organized_lines.extend(shebang_and_docstring)
        
        if std_imports or third_party_imports or local_imports:
            organized_lines.append('')  # Empty line before imports
            
        if std_imports:
            organized_lines.extend(sorted(std_imports))
            if third_party_imports or local_imports:
                organized_lines.append('')  # Separate import groups
                
        if third_party_imports:
            organized_lines.extend(sorted(third_party_imports))
            if local_imports:
                organized_lines.append('')
                
        if local_imports:
            organized_lines.extend(sorted(local_imports))
            
        if import_lines:
            organized_lines.append('')  # Empty line after imports
            
        organized_lines.extend(other_lines)
        
        return '\n'.join(organized_lines)
    
    def _print_summary(self, results: Dict[str, Any]):
        """Print a summary of the fixes applied"""
        print("\n" + "=" * 50)
        print("🎨 Visualization Import Fix Summary")
        print("=" * 50)
        
        print(f"📊 Files processed: {results['total_files']}")
        print(f"✅ Files fixed: {results['fixed_files']}")
        print(f"ℹ️ Files skipped: {results['skipped_files']}")
        print(f"❌ Files with errors: {results['error_files']}")
        
        if results['fixes_applied']:
            print("\n🔧 Fixes applied:")
            for fix in results['fixes_applied']:
                print(f"  📄 {fix['file']}:")
                for fix_desc in fix['fixes']:
                    print(f"    • {fix_desc}")
        
        if results['errors']:
            print("\n❌ Errors encountered:")
            for error in results['errors']:
                print(f"  📄 {error['file']}: {error['error']}")
        
        # Calculate success rate
        if results['total_files'] > 0:
            success_rate = (results['fixed_files'] / results['total_files']) * 100
            print(f"\n🎯 Success Rate: {success_rate:.1f}%")
            
            if success_rate >= 90:
                print("🌟 Excellent! Visualization imports are now clean!")
            elif success_rate >= 70:
                print("👍 Good! Most visualization imports are fixed")
            else:
                print("🔧 More work needed on visualization imports")

def main():
    """Run the visualization import fixer"""
    fixer = VisualizationImportFixer()
    results = fixer.fix_all_imports()
    
    print(f"\n🔧 Import fixing complete!")
    print(f"🎨 Visualization modules should now load properly")
    
    return results

if __name__ == "__main__":
    main() 