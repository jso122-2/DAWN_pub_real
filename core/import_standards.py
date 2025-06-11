# core/import_standards.py
"""
DAWN Import Standards
====================
Enforces consistent import patterns across the system
"""

import ast
from pathlib import Path
from typing import List, Tuple


class ImportStandards:
    """
    Import rules:
    1. Use absolute imports from DAWN root
    2. Group imports: stdlib → third-party → dawn
    3. Import order: modules → classes → functions
    4. One import per line for DAWN modules
    """
    
    IMPORT_ORDER = [
        'stdlib',      # Python standard library
        'third_party', # External packages
        'dawn_core',   # DAWN core systems
        'dawn_local'   # Local module imports
    ]
    
    @staticmethod
    def validate_imports(file_path: Path) -> List[str]:
        """Validate imports in a Python file"""
        violations = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
            
        imports = [node for node in ast.walk(tree) 
                  if isinstance(node, (ast.Import, ast.ImportFrom))]
        
        # Check for relative imports in non-init files
        if file_path.name != '__init__.py':
            for imp in imports:
                if isinstance(imp, ast.ImportFrom) and imp.level > 0:
                    violations.append(
                        f"Relative import found: {ast.unparse(imp)}"
                    )
        
        return violations
    
    @staticmethod
    def generate_import_header(component_name: str) -> str:
        """Generate standard import header for a component"""
        return f'''"""
{component_name} - DAWN Component
{'=' * (len(component_name) + 16)}

Standard imports follow DAWN conventions:
- Absolute imports from project root
- Grouped by type (stdlib/third-party/dawn)
- Alphabetical within groups
"""

# Standard library imports
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any

# Third-party imports
import numpy as np

# DAWN core imports
from core.dawn_registry import registry
from substrate.registry import SubstrateRegistry

# Local component imports
'''


# Import rules enforcer
class ImportEnforcer:
    """Enforce import consistency across DAWN"""
    
    def __init__(self):
        self.violations = []
        
    def check_file(self, filepath: Path) -> bool:
        """Check a single file for import violations"""
        if filepath.suffix != '.py':
            return True
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for PascalCase module names
        if filepath.stem != '__init__' and any(c.isupper() for c in filepath.stem):
            self.violations.append(
                f"{filepath}: Module name should be snake_case, not {filepath.stem}"
            )
            
        # Check for old registry imports
        old_registries = [
            'from core.dawn_registry import registry #',
            'from core.dawn_registry import registry #',
            'from core.dawn_registry import registry #'
        ]
        
        for old_import in old_registries:
            if old_import in content:
                self.violations.append(
                    f"{filepath}: Use 'from core.dawn_registry import registry' instead"
                )
                
        return len(self.violations) == 0
    
    def fix_imports(self, filepath: Path) -> None:
        """Auto-fix common import issues"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Replace old registry imports
        replacements = {
            'from core.dawn_registry import registry #': 'from core.dawn_registry import registry #',
            'from core.dawn_registry import registry #': 'from core.dawn_registry import registry #',
            'from core.dawn_registry import registry #': 'from core.dawn_registry import registry #',
            'semantic_context_engine': 'semantic_context_engine'  # fix module name
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)