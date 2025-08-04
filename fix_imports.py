#!/usr/bin/env python3
"""
DAWN Import Fixer

This script scans the entire codebase and fixes import statements to use
correct relative imports based on the new file organization.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class ImportFixer:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.fixed_files = []
        self.import_patterns = []
        
    def scan_codebase(self):
        """Scan the entire codebase for import statements"""
        print("🔍 Scanning codebase for import statements...")
        
        # Find all Python files
        python_files = list(self.root_dir.rglob("*.py"))
        print(f"📁 Found {len(python_files)} Python files")
        
        # Collect import patterns
        for py_file in python_files:
            self.analyze_file_imports(py_file)
        
        print(f"📊 Found {len(self.import_patterns)} import patterns to fix")
    
    def analyze_file_imports(self, file_path: Path):
        """Analyze imports in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all import statements
            import_lines = re.findall(r'^(from\s+[\w\.]+\s+import\s+.*|import\s+[\w\.]+.*)$', 
                                    content, re.MULTILINE)
            
            for line in import_lines:
                self.import_patterns.append({
                    'file': str(file_path),
                    'line': line.strip(),
                    'type': 'from' if line.startswith('from') else 'import'
                })
                
        except Exception as e:
            print(f"❌ Error analyzing {file_path}: {e}")
    
    def fix_imports(self):
        """Fix import statements throughout the codebase"""
        print("\n🔧 Fixing import statements...")
        
        # Define import fix rules
        import_fixes = {
            # Fix relative imports for moved modules
            r'from conversation\.': 'from .',
            r'import conversation\.': 'from .',
            r'from tests\.': 'from .',
            r'import tests\.': 'from .',
            r'from demos\.': 'from .',
            r'import demos\.': 'from .',
            r'from launcher_scripts\.': 'from .',
            r'import launcher_scripts\.': 'from .',
            
            # Fix common import patterns
            r'from \.\.core\.': 'from core.',
            r'from \.\.visual\.': 'from visual.',
            r'from \.\.backend\.': 'from backend.',
            r'from \.\.integration\.': 'from integration.',
            r'from \.\.processes\.': 'from processes.',
            r'from \.\.mood\.': 'from mood.',
            r'from \.\.cognitive\.': 'from cognitive.',
            r'from \.\.memories\.': 'from memories.',
            r'from \.\.bloom\.': 'from bloom.',
            r'from \.\.pulse\.': 'from pulse.',
            r'from \.\.schema\.': 'from schema.',
            r'from \.\.semantic\.': 'from semantic.',
            r'from \.\.reflection\.': 'from reflection.',
            r'from \.\.reflex\.': 'from reflex.',
            r'from \.\.fractal\.': 'from fractal.',
            r'from \.\.mycelium\.': 'from mycelium.',
            r'from \.\.codex\.': 'from codex.',
            r'from \.\.utils\.': 'from utils.',
            r'from \.\.config\.': 'from config.',
            r'from \.\.state\.': 'from state.',
            r'from \.\.runtime\.': 'from runtime.',
            r'from \.\.logs\.': 'from logs.',
            r'from \.\.docs\.': 'from docs.',
        }
        
        # Process each Python file
        python_files = list(self.root_dir.rglob("*.py"))
        
        for py_file in python_files:
            self.fix_file_imports(py_file, import_fixes)
        
        print(f"\n✅ Import fixing complete! Updated {len(self.fixed_files)} files")
    
    def fix_file_imports(self, file_path: Path, import_fixes: Dict[str, str]):
        """Fix imports in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply import fixes
            for pattern, replacement in import_fixes.items():
                content = re.sub(pattern, replacement, content)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_files.append(str(file_path))
                print(f"📝 Fixed imports in {file_path.name}")
                
        except Exception as e:
            print(f"❌ Error fixing imports in {file_path}: {e}")
    
    def create_init_files(self):
        """Create __init__.py files for all packages"""
        print("\n📦 Creating package __init__.py files...")
        
        # Find all directories that should be packages
        package_dirs = set()
        
        for py_file in self.root_dir.rglob("*.py"):
            if py_file.name != "__init__.py":
                package_dirs.add(py_file.parent)
        
        # Create __init__.py files
        for package_dir in package_dirs:
            init_file = package_dir / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                print(f"📦 Created {init_file}")
    
    def update_relative_imports(self):
        """Update relative imports to use proper relative paths"""
        print("\n🔄 Updating relative imports...")
        
        # Define relative import updates based on file structure
        relative_import_updates = {
            # Core module imports
            'core/': {
                r'from \.\.': 'from ..',
                r'from \.': 'from .',
            },
            'visual/': {
                r'from \.\.core\.': 'from core.',
                r'from \.\.backend\.': 'from backend.',
            },
            'conversation/': {
                r'from \.\.core\.': 'from core.',
                r'from \.\.backend\.': 'from backend.',
            },
            'tests/': {
                r'from \.\.core\.': 'from core.',
                r'from \.\.conversation\.': 'from ..conversation.',
            },
            'demos/': {
                r'from \.\.core\.': 'from core.',
                r'from \.\.conversation\.': 'from ..conversation.',
            },
        }
        
        # Apply relative import updates
        for directory, updates in relative_import_updates.items():
            dir_path = self.root_dir / directory
            if dir_path.exists():
                for py_file in dir_path.rglob("*.py"):
                    self.apply_relative_import_updates(py_file, updates)
    
    def apply_relative_import_updates(self, file_path: Path, updates: Dict[str, str]):
        """Apply relative import updates to a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Apply updates
            for pattern, replacement in updates.items():
                content = re.sub(pattern, replacement, content)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"📝 Updated relative imports in {file_path.name}")
                
        except Exception as e:
            print(f"❌ Error updating relative imports in {file_path}: {e}")
    
    def validate_imports(self):
        """Validate that all imports are working correctly"""
        print("\n🔍 Validating imports...")
        
        # Test import of main modules
        test_modules = [
            'core',
            'conversation', 
            'visual',
            'tests',
            'demos',
            'launcher_scripts'
        ]
        
        for module in test_modules:
            try:
                module_path = self.root_dir / module
                if module_path.exists():
                    # Try to import the module
                    import sys
                    sys.path.insert(0, str(self.root_dir))
                    
                    try:
                        __import__(module)
                        print(f"✅ {module} imports successfully")
                    except ImportError as e:
                        print(f"❌ {module} import failed: {e}")
                    except Exception as e:
                        print(f"⚠️ {module} import warning: {e}")
                        
            except Exception as e:
                print(f"❌ Error testing {module}: {e}")

def main():
    """Main import fixing function"""
    fixer = ImportFixer()
    
    print("🌅 DAWN Import Fixer")
    print("=" * 50)
    
    # Perform import fixing operations
    fixer.scan_codebase()
    fixer.fix_imports()
    fixer.create_init_files()
    fixer.update_relative_imports()
    fixer.validate_imports()
    
    print("\n🎉 Import fixing completed successfully!")
    print(f"\n📋 Summary:")
    print(f"   📝 Files updated: {len(fixer.fixed_files)}")
    print(f"   🔍 Import patterns analyzed: {len(fixer.import_patterns)}")
    print("\n💡 Next steps:")
    print("   1. Test the system with: python main.py")
    print("   2. Run tests with: python main.py --mode test")
    print("   3. Check for any remaining import errors")

if __name__ == "__main__":
    main() 