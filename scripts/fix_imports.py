#!/usr/bin/env python3
"""
Script to fix import statements across the codebase
"""
import re
from pathlib import Path
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImportFixer:
    """Fix import statements across the codebase"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.import_patterns = [
            # Pattern: (regex, replacement)
            (r'from helix\.helix_import_architecture import helix_import',
             'from substrate.helix.helix_import_fix import helix_import'),
            
            # Standardize substrate imports
            (r'pulse_heat = helix_import\("pulse_heat"\)',
             'from substrate import pulse_heat'),
            
            # Fix try/except import patterns
            (r'try:\s*import matplotlib\.pyplot as plt\s*\n\s*MATPLOTLIB_AVAILABLE = True\s*\nexcept.*?False',
             'from config.import_config import safe_import\nplt = safe_import("matplotlib.pyplot", None)\nMATPLOTLIB_AVAILABLE = plt is not None'),
        ]
        
    def fix_file(self, file_path: Path) -> bool:
        """Fix imports in a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Apply all import fixes
            for pattern, replacement in self.import_patterns:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
            
            # Only write if changes were made
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                logger.info(f"Fixed imports in: {file_path}")
                return True
                
            return False
            
        except Exception as e:
            logger.error(f"Error fixing {file_path}: {e}")
            return False
    
    def fix_directory(self, directory: Path) -> Tuple[int, int]:
        """Fix all Python files in a directory"""
        fixed = 0
        total = 0
        
        for py_file in directory.rglob("*.py"):
            # Skip virtual environments and cache
            if any(part in py_file.parts for part in ['venv', '__pycache__', '.git']):
                continue
                
            total += 1
            if self.fix_file(py_file):
                fixed += 1
        
        return fixed, total
    
    def add_init_files(self) -> int:
        """Add missing __init__.py files"""
        added = 0
        
        for directory in self.project_root.rglob("*/"):
            # Skip special directories
            if any(part in directory.parts for part in ['venv', '__pycache__', '.git', 'node_modules']):
                continue
            
            # Check if it contains Python files
            py_files = list(directory.glob("*.py"))
            if py_files and not (directory / "__init__.py").exists():
                (directory / "__init__.py").touch()
                logger.info(f"Added __init__.py to: {directory}")
                added += 1
        
        return added

def main():
    """Main fix script"""
    project_root = Path(__file__).parent.parent
    fixer = ImportFixer(project_root)
    
    print("🔧 Starting DAWN import fixes...")
    
    # Fix imports
    fixed, total = fixer.fix_directory(project_root)
    print(f"📝 Fixed imports in {fixed}/{total} files")
    
    # Add missing __init__.py files
    added = fixer.add_init_files()
    print(f"📄 Added {added} missing __init__.py files")
    
    # Create startup script
    create_startup_script(project_root)
    
    print("✅ Import fixes complete!")

def create_startup_script(project_root: Path):
    """Create a startup script that properly initializes the system"""
    startup_script = project_root / "startup.py"
    
    content = '''#!/usr/bin/env python3
"""
DAWN Startup Script
Properly initializes all import paths and systems
"""
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Initialize import system
from config.import_config import setup_imports
setup_imports()

# Initialize helix system with new implementation
from substrate.helix.helix_import_fix import helix_system

# Now import main application
try:
    from main import main
except ImportError:
    # Fallback if main.py doesn't exist
    def main():
        print("🚀 DAWN import system initialized successfully!")
        print("Import the modules you need and start your application.")

if __name__ == "__main__":
    print("🚀 Starting DAWN with fixed imports...")
    main()
'''
    
    startup_script.write_text(content)
    print(f"✅ Created startup script: {startup_script}")

if __name__ == "__main__":
    main() 