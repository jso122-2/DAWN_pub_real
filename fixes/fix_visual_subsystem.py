"""
DAWN Visual Subsystem Recovery
Handles visual rendering failures and provides fallback mechanisms
"""
import json
import time
from pathlib import Path
from datetime import datetime

class VisualSubsystemFixer:
    def __init__(self):
        self.log_path = Path("fixes/recovery_log.json")
        self.fallback_rgb = (0.5, 0.5, 0.5)  # Neutral gray fallback
        
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
    
    def create_fallback_visual(self, width: int = 800, height: int = 600):
        """Create a simple fallback visual layer"""
        try:
            # Create a basic grid pattern
            grid = []
            for y in range(height):
                row = []
                for x in range(width):
                    # Create a subtle grid pattern
                    intensity = 0.5 + 0.1 * ((x + y) % 2)
                    row.append((intensity, intensity, intensity))
                grid.append(row)
            return grid
        except Exception as e:
            self.log_fix("fallback_visual", False, e)
            return None
    
    def patch_visualizer(self):
        """Patch the unified visualizer with error handling"""
        try:
            # Import the visualizer
            from experiments.dawn_unified_visualizer_2 import DawnUnifiedVisualizer
            
            # Create patched methods
            def safe_create_visualization(self, viz_func, *args, **kwargs):
                try:
                    return viz_func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ Visualization error in {viz_func.__name__}: {e}")
                    # Create fallback visualization
                    fallback = self.create_fallback_visual()
                    if fallback:
                        print("✓ Using fallback visualization")
                        return fallback
                    return None
            
            # Patch each visualization method
            for method_name in [
                'create_mood_pressure_timeseries',
                'create_cognition_pressure_map',
                'create_pulse_field_evolution',
                'create_mood_transition_histogram'
            ]:
                if hasattr(DawnUnifiedVisualizer, method_name):
                    original = getattr(DawnUnifiedVisualizer, method_name)
                    patched = lambda self, *a, **k: safe_create_visualization(
                        self, original, *a, **k
                    )
                    setattr(DawnUnifiedVisualizer, method_name, patched)
            
            self.log_fix("patch_visualizer", True)
            return True
            
        except Exception as e:
            self.log_fix("patch_visualizer", False, e)
            return False
    
    def patch_rendering_exceptions(self):
        """Patch known rendering exceptions with diagnostic logging"""
        try:
            # Import necessary modules
            import sys
            from pathlib import Path
            
            # Add diagnostic logging to visual modules
            visual_dir = Path("visual")
            if visual_dir.exists():
                for py_file in visual_dir.glob("*.py"):
                    if py_file.name.startswith("__"):
                        continue
                        
                    # Read file content
                    content = py_file.read_text()
                    
                    # Add diagnostic logging if not present
                    if "def render" in content and "try:" not in content:
                        # Add try-except block around render functions
                        content = content.replace(
                            "def render",
                            "def render\n    try:\n        "
                        ).replace(
                            "return result",
                            "        return result\n    except Exception as e:\n        print(f'[RENDER] Error in {__name__}: {e}')\n        return None"
                        )
                        
                        # Write modified content
                        py_file.write_text(content)
            
            self.log_fix("patch_rendering_exceptions", True)
            return True
            
        except Exception as e:
            self.log_fix("patch_rendering_exceptions", False, e)
            return False

def patch_visuals():
    """Main function to patch visual subsystem"""
    print("🔧 Patching visual subsystem...")
    fixer = VisualSubsystemFixer()
    
    # Apply patches
    visualizer_patched = fixer.patch_visualizer()
    rendering_patched = fixer.patch_rendering_exceptions()
    
    if visualizer_patched and rendering_patched:
        print("✓ Visual subsystem patched successfully")
        return True
    else:
        print("⚠️ Some visual patches failed - check recovery log")
        return False

if __name__ == "__main__":
    patch_visuals() 