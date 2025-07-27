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
        try:
            from config.import_config import import_manager
            self.import_manager = import_manager
        except ImportError:
            logger.warning("Import manager not available, using basic verification")
            self.import_manager = None
        
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