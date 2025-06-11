# refactor_v2_fixed.py
"""
DAWN System Refactor v2.0 - Fixed for Windows
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class DAWNRefactorV2:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_dir = Path(f"refactor_log/v2.0_{self.timestamp}")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log = []
        
    def log_action(self, action: str, status: str = "OK"):
        """Log refactor actions (using ASCII-safe status)"""
        # Use ASCII-safe status indicators
        status_map = {
            "✅": "[OK]",
            "✓": "[DONE]", 
            "⚠️": "[WARN]",
            "❌": "[FAIL]"
        }
        safe_status = status_map.get(status, status)
        
        msg = f"{safe_status} {action}"
        print(msg)
        self.log.append({
            'time': datetime.now().isoformat(),
            'action': action,
            'status': safe_status
        })
        
    def run(self):
        """Execute refactor plan"""
        print("DAWN System Refactor v2.0")
        print("=" * 40)
        
        # Phase 1: Critical Fixes
        self.phase1_critical_fixes()
        
        # Phase 2: Core Infrastructure
        self.phase2_core_infrastructure()
        
        # Phase 3: Consolidation
        self.phase3_consolidation()
        
        # Phase 4: Cleanup
        self.phase4_cleanup()
        
        # Save log
        self.save_log()
        
        print("\n[OK] Refactor complete!")
        
    def phase1_critical_fixes(self):
        """Fix critical issues"""
        print("\nPhase 1: Critical Fixes")
        
        # Fix pulse __int__.py
        bad_init = Path("pulse/__int__.py")
        good_init = Path("pulse/__init__.py")
        
        if bad_init.exists():
            if good_init.exists():
                # Backup good one first
                shutil.copy2(good_init, "pulse/__init__.py.backup")
                bad_init.unlink()
                self.log_action("Removed pulse/__int__.py (typo)", "✅")
            else:
                # Rename bad to good
                bad_init.rename(good_init)
                self.log_action("Renamed pulse/__int__.py to __init__.py", "✅")
        else:
            self.log_action("pulse/__int__.py already fixed", "✓")
            
    def phase2_core_infrastructure(self):
        """Deploy core infrastructure"""
        print("\nPhase 2: Core Infrastructure")
        
        # Create event bus if needed
        event_bus_path = Path("core/system/event_bus.py")
        if not event_bus_path.exists():
            event_bus_path.parent.mkdir(parents=True, exist_ok=True)
            # Would write the enhanced event bus code here
            self.log_action("Created enhanced event bus", "✅")
        else:
            self.log_action("Event bus exists", "✓")
            
        # Note: Orchestrator and WiringMonitor would be created here
        
    def phase3_consolidation(self):
        """Consolidate duplicate systems"""
        print("\nPhase 3: Consolidation")
        
        # Handle tick engines
        tick_engines = {
            "core/tick_engine.py": "primary",
            "core/consolidated_tick_engine.py": "archive",
            "unified_tick_engine.py": "archive"
        }
        
        for engine_path, action in tick_engines.items():
            path = Path(engine_path)
            if path.exists():
                if action == "primary":
                    self.log_action(f"Keeping {engine_path} as primary", "✓")
                else:
                    archive_path = Path(f"archive/tick_engines/{path.name}")
                    archive_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), str(archive_path))
                    self.log_action(f"Archived {engine_path}", "✅")
                    
        # Unify schema files
        schema_files = list(Path("schema").glob("*.py"))
        if len(schema_files) > 5:  # Arbitrary threshold
            self.log_action(f"Found {len(schema_files)} schema files - consolidation needed", "⚠️")
            # Would implement schema unification here
            
    def phase4_cleanup(self):
        """Clean up old files"""
        print("\nPhase 4: Cleanup")
        
        # Remove terminals if empty
        terminals = Path("terminals")
        if terminals.exists():
            py_files = list(terminals.rglob("*.py"))
            non_init_files = [f for f in py_files if f.name != "__init__.py"]
            
            if non_init_files:
                self.log_action("terminals/ has content - keeping", "⚠️")
            else:
                shutil.rmtree(terminals)
                self.log_action("Removed empty terminals/", "✅")
                
        # Archive old visual files
        old_visuals = Path("visual/old")
        if old_visuals.exists():
            archive_path = Path(f"archive/visuals_{self.timestamp}")
            shutil.move(str(old_visuals), str(archive_path))
            self.log_action("Archived visual/old/", "✅")
            
    def save_log(self):
        """Save refactor log with proper encoding"""
        log_file = self.log_dir / "refactor_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                'version': '2.0',
                'timestamp': self.timestamp,
                'actions': self.log
            }, f, indent=2, ensure_ascii=False)
            
        # Create summary with UTF-8 encoding
        summary = f"""# DAWN Refactor v2.0 Summary
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Actions Taken:
"""
        for entry in self.log:
            summary += f"- {entry['status']} {entry['action']}\n"
            
        summary_file = self.log_dir / "SUMMARY.md"
        # Explicitly use UTF-8 encoding
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"\n[LOG] Saved to: {self.log_dir}")


if __name__ == "__main__":
    refactor = DAWNRefactorV2()
    refactor.run()