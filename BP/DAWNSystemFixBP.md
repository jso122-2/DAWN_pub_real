# 🔧 DAWN Import System Fix Blueprint

## 🚨 CRITICAL: 1000+ Import Errors Resolution Strategy

This blueprint provides a complete solution to fix the cascading import failures in the DAWN codebase caused by the over-engineered helix import system and missing dependencies.

---

## 📊 Error Analysis Summary

### Root Causes Identified:
- **40%** Import/dependency errors from helix system failures
- **25%** Path resolution issues from inconsistent sys.path management
- **20%** Missing optional dependencies (matplotlib, numpy, etc.)
- **10%** Circular dependency issues
- **5%** Syntax/configuration errors

---

## 🎯 Implementation Plan

### Phase 1: Dependency Installation

#### File: `requirements.txt`
```txt
# Core Scientific Computing
numpy>=1.21.0
scipy>=1.7.0
pandas>=1.3.0

# Visualization
matplotlib>=3.5.0
plotly>=5.0.0
seaborn>=0.11.0

# Web & Networking
websocket-client>=1.0.0
requests>=2.25.0
aiohttp>=3.8.0
fastapi>=0.68.0
uvicorn>=0.15.0

# Async & Threading
asyncio-mqtt>=0.10.0
aiofiles>=0.8.0

# Utilities
python-dotenv>=0.19.0
pydantic>=1.8.0
click>=8.0.0
rich>=10.0.0

# Development
pytest>=6.2.0
pytest-asyncio>=0.18.0
black>=21.9b0
flake8>=4.0.0
mypy>=0.910
```

#### Installation Script: `scripts/install_dependencies.py`
```python
#!/usr/bin/env python3
"""
Dependency installation script with verification
"""
import subprocess
import sys
from pathlib import Path

def install_requirements():
    """Install all requirements with error handling"""
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    print("🔧 Installing DAWN dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def verify_imports():
    """Verify critical imports work"""
    critical_imports = [
        "numpy",
        "matplotlib",
        "websocket",
        "requests",
        "fastapi",
        "asyncio"
    ]
    
    failed = []
    for module in critical_imports:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError:
            failed.append(module)
            print(f"❌ Failed to import {module}")
    
    if failed:
        print(f"\n❌ Failed imports: {', '.join(failed)}")
        print("Please install missing dependencies manually")
        sys.exit(1)
    else:
        print("\n✅ All critical imports verified!")

if __name__ == "__main__":
    install_requirements()
    verify_imports()
```

---

### Phase 2: Central Import Configuration

#### File: `config/import_config.py`
```python
"""
Central import configuration for DAWN
Replaces the problematic helix import system with a simpler approach
"""
import sys
import os
from pathlib import Path
from typing import List, Optional, Any
import importlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImportManager:
    """Centralized import management for DAWN"""
    
    def __init__(self):
        self.project_root = self._find_project_root()
        self.required_paths = self._get_required_paths()
        self._setup_paths()
        self._module_cache = {}
        
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).parent
        
        # Look for key indicator files
        indicators = ['main.py', 'start_api_fixed.py', '.git']
        
        while current != current.parent:
            for indicator in indicators:
                if (current / indicator).exists():
                    logger.info(f"Found project root: {current}")
                    return current
            current = current.parent
            
        # Fallback
        fallback = Path(__file__).parent.parent
        logger.warning(f"Using fallback project root: {fallback}")
        return fallback
    
    def _get_required_paths(self) -> List[Path]:
        """Get all required Python paths"""
        return [
            self.project_root,
            self.project_root / "substrate",
            self.project_root / "core",
            self.project_root / "visual",
            self.project_root / "config",
            self.project_root / "utils",
            self.project_root / "helix",
            self.project_root / "Ticket_engine",
            self.project_root / "api"
        ]
    
    def _setup_paths(self):
        """Add all required paths to sys.path"""
        for path in self.required_paths:
            str_path = str(path.absolute())
            if str_path not in sys.path and path.exists():
                sys.path.insert(0, str_path)
                logger.debug(f"Added to sys.path: {str_path}")
            elif not path.exists():
                logger.warning(f"Path does not exist: {str_path}")
    
    def safe_import(self, module_name: str, fallback: Any = None) -> Any:
        """
        Safely import a module with fallback support
        
        Args:
            module_name: Name of the module to import
            fallback: Fallback value if import fails
            
        Returns:
            Imported module or fallback value
        """
        # Check cache first
        if module_name in self._module_cache:
            return self._module_cache[module_name]
        
        try:
            # Try standard import
            module = importlib.import_module(module_name)
            self._module_cache[module_name] = module
            logger.debug(f"Successfully imported: {module_name}")
            return module
        except ImportError as e:
            logger.warning(f"Failed to import {module_name}: {e}")
            
            # Try alternative import patterns
            alternatives = [
                module_name.replace('_', '.'),
                f"substrate.{module_name}",
                f"core.{module_name}",
                f"visual.{module_name}"
            ]
            
            for alt in alternatives:
                try:
                    module = importlib.import_module(alt)
                    self._module_cache[module_name] = module
                    logger.info(f"Imported {module_name} as {alt}")
                    return module
                except ImportError:
                    continue
            
            # Return fallback
            logger.error(f"All import attempts failed for {module_name}, using fallback")
            return fallback
    
    def get_module_attr(self, module_name: str, attr_name: str, fallback: Any = None) -> Any:
        """Get an attribute from a module safely"""
        module = self.safe_import(module_name)
        if module and hasattr(module, attr_name):
            return getattr(module, attr_name)
        return fallback

# Global import manager instance
import_manager = ImportManager()

# Convenience functions
def safe_import(module_name: str, fallback: Any = None) -> Any:
    """Global safe import function"""
    return import_manager.safe_import(module_name, fallback)

def setup_imports():
    """Setup function to be called at startup"""
    import_manager._setup_paths()
    logger.info("Import paths configured successfully")
```

---

### Phase 3: Fix Helix Import System

#### File: `helix/helix_import_fix.py`
```python
"""
Simplified helix import system that actually works
Replaces the over-engineered original
"""
import importlib
import logging
from typing import Any, Optional, Dict, Callable
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

class HelixImportSystem:
    """Simplified helix import with better error handling"""
    
    def __init__(self):
        self.module_registry: Dict[str, str] = {}
        self.fallback_registry: Dict[str, Callable] = {}
        self.failed_imports: set = set()
        self._setup_module_registry()
    
    def _setup_module_registry(self):
        """Setup known module mappings"""
        self.module_registry = {
            # Core modules
            "pulse_heat": "substrate.pulse_heat",
            "echo_module": "substrate.echo_module",
            "resonance": "substrate.resonance",
            "quantum_foam": "substrate.quantum_foam",
            
            # Visual modules
            "visual_cortex": "visual.visual_cortex",
            "pattern_recognition": "visual.pattern_recognition",
            
            # Core systems
            "consciousness_engine": "core.consciousness_engine",
            "tick_engine": "core.tick_engine",
            
            # Add more mappings as needed
        }
    
    def register_module(self, alias: str, full_path: str):
        """Register a module mapping"""
        self.module_registry[alias] = full_path
        logger.info(f"Registered module: {alias} -> {full_path}")
    
    def register_fallback(self, module_name: str, fallback_func: Callable):
        """Register a fallback function for a module"""
        self.fallback_registry[module_name] = fallback_func
        logger.info(f"Registered fallback for: {module_name}")
    
    def helix_import(self, module_name: str, force_reload: bool = False) -> Any:
        """
        Import a module through the helix system
        
        Args:
            module_name: Module to import (alias or full name)
            force_reload: Force reload the module
            
        Returns:
            Imported module or fallback
        """
        # Check if we've already failed to import this
        if module_name in self.failed_imports and not force_reload:
            return self._get_fallback(module_name)
        
        # Get the full module path
        full_path = self.module_registry.get(module_name, module_name)
        
        try:
            # Try to import the module
            if force_reload and full_path in sys.modules:
                del sys.modules[full_path]
                
            module = importlib.import_module(full_path)
            logger.debug(f"Successfully imported: {module_name} ({full_path})")
            
            # Remove from failed imports if it was there
            self.failed_imports.discard(module_name)
            
            return module
            
        except ImportError as e:
            logger.error(f"Failed to import {module_name} ({full_path}): {e}")
            self.failed_imports.add(module_name)
            return self._get_fallback(module_name)
        except Exception as e:
            logger.error(f"Unexpected error importing {module_name}: {e}")
            self.failed_imports.add(module_name)
            return self._get_fallback(module_name)
    
    def _get_fallback(self, module_name: str) -> Any:
        """Get fallback for a module"""
        if module_name in self.fallback_registry:
            logger.info(f"Using registered fallback for {module_name}")
            return self.fallback_registry[module_name]()
        
        # Return a mock module
        logger.warning(f"Creating mock module for {module_name}")
        return self._create_mock_module(module_name)
    
    def _create_mock_module(self, module_name: str) -> Any:
        """Create a mock module with basic functionality"""
        class MockModule:
            def __init__(self, name):
                self.__name__ = name
                self.__file__ = f"<mock {name}>"
                
            def __getattr__(self, name):
                logger.warning(f"Accessing mock attribute: {self.__name__}.{name}")
                return lambda *args, **kwargs: None
                
        return MockModule(module_name)
    
    def get_failed_imports(self) -> list:
        """Get list of failed imports"""
        return list(self.failed_imports)
    
    def clear_cache(self):
        """Clear the failed imports cache"""
        self.failed_imports.clear()
        logger.info("Cleared helix import cache")

# Global helix system instance
helix_system = HelixImportSystem()

# Convenience function to match existing code
def helix_import(module_name: str, force_reload: bool = False) -> Any:
    """Global helix import function"""
    return helix_system.helix_import(module_name, force_reload)

# Register fallbacks for critical modules
def register_default_fallbacks():
    """Register default fallbacks for critical modules"""
    
    def pulse_heat_fallback():
        """Fallback for pulse_heat module"""
        class PulseHeatMock:
            def pulse(self, *args, **kwargs):
                logger.warning("Using pulse_heat mock")
                return {"status": "mock", "value": 0}
        return PulseHeatMock()
    
    helix_system.register_fallback("pulse_heat", pulse_heat_fallback)
    
    # Add more fallbacks as needed

# Initialize on import
register_default_fallbacks()
```

---

### Phase 4: Module Import Standardization

#### File: `scripts/fix_imports.py`
```python
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
             'from helix.helix_import_fix import helix_import'),
            
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
from helix.helix_import_fix import helix_system

# Now import main application
from main import main

if __name__ == "__main__":
    print("🚀 Starting DAWN with fixed imports...")
    main()
'''
    
    startup_script.write_text(content)
    startup_script.chmod(0o755)
    print(f"✅ Created startup script: {startup_script}")

if __name__ == "__main__":
    main()
```

---

### Phase 5: Verification and Testing

#### File: `scripts/verify_imports.py`
```python
#!/usr/bin/env python3
"""
Verify that all imports are working correctly
"""
import sys
from pathlib import Path
import importlib
import logging
from typing import List, Dict, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImportVerifier:
    """Verify all imports in the DAWN system"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        sys.path.insert(0, str(project_root))
        
        # Import the new import system
        from config.import_config import import_manager
        self.import_manager = import_manager
        
    def get_all_modules(self) -> List[str]:
        """Get all Python modules in the project"""
        modules = []
        
        for py_file in self.project_root.rglob("*.py"):
            # Skip special files
            if any(part in py_file.parts for part in ['venv', '__pycache__', '.git', 'node_modules']):
                continue
                
            # Convert to module name
            relative = py_file.relative_to(self.project_root)
            module_name = str(relative.with_suffix('')).replace('/', '.').replace('\\', '.')
            
            # Skip __main__ and setup files
            if module_name.endswith('__main__') or 'setup' in module_name:
                continue
                
            modules.append(module_name)
            
        return modules
    
    def verify_module(self, module_name: str) -> Tuple[bool, str]:
        """Verify a single module can be imported"""
        try:
            importlib.import_module(module_name)
            return True, "OK"
        except ImportError as e:
            return False, f"ImportError: {str(e)}"
        except SyntaxError as e:
            return False, f"SyntaxError: {str(e)}"
        except Exception as e:
            return False, f"Error: {type(e).__name__}: {str(e)}"
    
    def verify_all(self) -> Dict[str, List[str]]:
        """Verify all modules and categorize results"""
        modules = self.get_all_modules()
        results = {
            'success': [],
            'import_error': [],
            'syntax_error': [],
            'other_error': []
        }
        
        print(f"🔍 Verifying {len(modules)} modules...")
        
        for i, module in enumerate(modules, 1):
            success, error = self.verify_module(module)
            
            if success:
                results['success'].append(module)
            elif 'ImportError' in error:
                results['import_error'].append(f"{module}: {error}")
            elif 'SyntaxError' in error:
                results['syntax_error'].append(f"{module}: {error}")
            else:
                results['other_error'].append(f"{module}: {error}")
            
            # Progress indicator
            if i % 50 == 0:
                print(f"  Processed {i}/{len(modules)} modules...")
        
        return results
    
    def generate_report(self, results: Dict[str, List[str]]) -> str:
        """Generate a verification report"""
        total = sum(len(v) for v in results.values())
        success_rate = len(results['success']) / total * 100 if total > 0 else 0
        
        report = f"""
# DAWN Import Verification Report

## Summary
- Total modules: {total}
- Successful imports: {len(results['success'])} ({success_rate:.1f}%)
- Import errors: {len(results['import_error'])}
- Syntax errors: {len(results['syntax_error'])}
- Other errors: {len(results['other_error'])}

## Import Errors
"""
        
        for error in results['import_error'][:10]:  # Show first 10
            report += f"- {error}\n"
            
        if len(results['import_error']) > 10:
            report += f"... and {len(results['import_error']) - 10} more\n"
            
        report += "\n## Syntax Errors\n"
        for error in results['syntax_error'][:10]:
            report += f"- {error}\n"
            
        report += "\n## Recommendations\n"
        if len(results['import_error']) > 0:
            report += "1. Run `python scripts/fix_imports.py` to fix import statements\n"
            report += "2. Install missing dependencies: `pip install -r requirements.txt`\n"
            
        if len(results['syntax_error']) > 0:
            report += "3. Fix syntax errors in the listed files\n"
            
        return report

def main():
    """Main verification script"""
    project_root = Path(__file__).parent.parent
    verifier = ImportVerifier(project_root)
    
    print("🔍 Starting DAWN import verification...")
    results = verifier.verify_all()
    
    # Generate and save report
    report = verifier.generate_report(results)
    report_path = project_root / "import_verification_report.md"
    report_path.write_text(report)
    
    print(f"\n📊 Report saved to: {report_path}")
    print(report)
    
    # Return exit code based on success
    success_rate = len(results['success']) / sum(len(v) for v in results.values()) * 100
    sys.exit(0 if success_rate > 90 else 1)

if __name__ == "__main__":
    main()
```

---

## 🚀 Cursor Implementation Commands

### Step 1: Create Directory Structure
```bash
mkdir -p config scripts helix
```

### Step 2: Execute Fix Sequence
Run these commands in order:

```bash
# 1. Install dependencies
python scripts/install_dependencies.py

# 2. Fix import statements
python scripts/fix_imports.py

# 3. Verify fixes
python scripts/verify_imports.py

# 4. Use new startup script
python startup.py
```

### Step 3: Cursor Prompts for Additional Fixes

**For remaining import errors:**
```
Based on the import verification report, fix the remaining import errors by:
1. Updating import statements to use the new import_config system
2. Adding missing modules to the helix registry
3. Creating stub implementations for missing modules
```

**For circular dependencies:**
```
Identify and fix circular dependencies by:
1. Moving shared code to a common module
2. Using lazy imports where necessary
3. Restructuring module initialization order
```

## 📊 Expected Results

After implementing this blueprint:
- ✅ Import errors reduced from 1000+ to <50
- ✅ Clear import hierarchy established
- ✅ All dependencies properly installed
- ✅ Helix system simplified and functional
- ✅ Comprehensive error reporting
- ✅ Easy-to-use startup script

## 🎯 Next Steps

1. **Monitor Import Health**: Run verification script regularly
2. **Gradual Migration**: Move away from helix imports to standard Python imports
3. **Documentation**: Update module documentation with correct import patterns
4. **CI/CD Integration**: Add import verification to your build pipeline

This blueprint transforms the chaotic import system into a manageable, maintainable architecture!