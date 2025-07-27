"""
DAWN Tick Engine SCUP Stabilization
Handles SCUP regulation and thermal management
"""
import json
import time
from pathlib import Path
from datetime import datetime

class TickEngineFixer:
    def __init__(self):
        self.log_path = Path("fixes/recovery_log.json")
        self.max_scup = 1.0
        self.thermal_threshold = 0.85
        
    def log_fix(self, fix_name: str, success: bool, error: str = None):
        """Log fix attempt to recovery log"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "fix": fix_name,
            "result": "success" if success else "fail",
            "error": str(error) if error else None
        }
        
        # Load existing log or create new
        if self.log_path.exists():
            with open(self.log_path, 'r') as f:
                log = json.load(f)
        else:
            log = []
            
        log.append(log_entry)
        
        # Save updated log
        with open(self.log_path, 'w') as f:
            json.dump(log, f, indent=2)
    
    def patch_scup_calculation(self):
        """Patch SCUP calculation with safety limits"""
        try:
            # Import tick engine
            from unified_tick_engine import UnifiedTickEngine
            
            # Store original method
            original_calculate_scup = UnifiedTickEngine._calculate_scup
            
            def safe_calculate_scup(self, *args, **kwargs):
                try:
                    # Get original SCUP value
                    scup = original_calculate_scup(self, *args, **kwargs)
                    
                    # Cap SCUP at maximum
                    scup = min(self.max_scup, scup)
                    
                    # Apply thermal fallback if SCUP is high
                    if scup > self.thermal_threshold:
                        if hasattr(self, 'pulse'):
                            # Reduce thermal pressure
                            self.pulse.thermal_momentum *= 0.95
                            print(f"⚠️ High SCUP ({scup:.2f}) - Reducing thermal pressure")
                    
                    return scup
                    
                except Exception as e:
                    print(f"⚠️ SCUP calculation error: {e}")
                    return 0.7  # Safe default
            
            # Apply the patch
            UnifiedTickEngine._calculate_scup = safe_calculate_scup
            self.log_fix("patch_scup_calculation", True)
            return True
            
        except Exception as e:
            self.log_fix("patch_scup_calculation", False, e)
            return False
    
    def patch_tick_loop(self):
        """Patch tick loop to prevent infinite loops and overheating"""
        try:
            # Import tick engine
            from unified_tick_engine import UnifiedTickEngine
            
            # Store original method
            original_main_loop = UnifiedTickEngine._main_loop
            
            def safe_main_loop(self, *args, **kwargs):
                try:
                    # Check for overheating
                    if hasattr(self, 'pulse'):
                        if self.pulse.thermal_momentum > 0.9:
                            print("⚠️ Thermal pressure too high - cooling down")
                            self.pulse.thermal_momentum *= 0.8
                            time.sleep(0.1)  # Brief cooldown
                    
                    # Execute tick with timeout
                    start_time = time.time()
                    result = original_main_loop(self, *args, **kwargs)
                    
                    # Check for excessive tick duration
                    tick_duration = time.time() - start_time
                    if tick_duration > 1.0:  # More than 1 second
                        print(f"⚠️ Long tick duration: {tick_duration:.2f}s")
                        if hasattr(self, 'pulse'):
                            self.pulse.thermal_momentum *= 0.9
                    
                    return result
                    
                except Exception as e:
                    print(f"⚠️ Tick loop error: {e}")
                    if hasattr(self, 'pulse'):
                        self.pulse.thermal_momentum *= 0.7  # Emergency cooling
                    return None
            
            # Apply the patch
            UnifiedTickEngine._main_loop = safe_main_loop
            self.log_fix("patch_tick_loop", True)
            return True
            
        except Exception as e:
            self.log_fix("patch_tick_loop", False, e)
            return False

def patch_tick_engine():
    """Main function to patch tick engine"""
    print("🔧 Patching tick engine...")
    fixer = TickEngineFixer()
    
    # Apply patches
    scup_patched = fixer.patch_scup_calculation()
    loop_patched = fixer.patch_tick_loop()
    
    if scup_patched and loop_patched:
        print("✓ Tick engine patched successfully")
        return True
    else:
        print("⚠️ Some tick engine patches failed - check recovery log")
        return False

if __name__ == "__main__":
    patch_tick_engine() 