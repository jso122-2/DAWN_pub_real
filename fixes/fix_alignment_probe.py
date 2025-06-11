"""
DAWN Alignment Probe Stabilization
Handles alignment drift and entropy management
"""
import json
import time
import math
from pathlib import Path
from datetime import datetime

class AlignmentProbeFixer:
    def __init__(self):
        self.log_path = Path("fixes/recovery_log.json")
        self.collapse_log = Path("logs/probe_collapse.json")
        self.max_drift = 1.0
        self.entropy_threshold = 0.8
        
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
    
    def log_collapse(self, probe_state: dict):
        """Log alignment collapse event"""
        collapse_entry = {
            "timestamp": datetime.now().isoformat(),
            "probe_state": probe_state,
            "entropy": self.calculate_entropy(probe_state)
        }
        
        # Ensure logs directory exists
        self.collapse_log.parent.mkdir(exist_ok=True)
        
        # Load existing collapse log or create new
        if self.collapse_log.exists():
            with open(self.collapse_log, 'r') as f:
                log = json.load(f)
        else:
            log = []
            
        log.append(collapse_entry)
        
        # Save updated log
        with open(self.collapse_log, 'w') as f:
            json.dump(log, f, indent=2)
    
    def calculate_entropy(self, state: dict) -> float:
        """Calculate entropy of alignment state"""
        try:
            # Extract relevant values
            values = [v for v in state.values() if isinstance(v, (int, float))]
            if not values:
                return 0.0
                
            # Normalize values
            total = sum(abs(v) for v in values)
            if total == 0:
                return 0.0
                
            probs = [abs(v) / total for v in values]
            
            # Calculate Shannon entropy
            entropy = -sum(p * math.log2(p) for p in probs if p > 0)
            return entropy
            
        except Exception as e:
            print(f"⚠️ Entropy calculation error: {e}")
            return 0.0
    
    def normalize_drift(self, drift: float) -> float:
        """Normalize drift value to [-1.0, 1.0] range"""
        return max(-self.max_drift, min(self.max_drift, drift))
    
    def patch_alignment_probe(self):
        """Patch alignment probe with drift normalization and entropy checks"""
        try:
            # Import alignment probe
            from core.alignment.alignment_probe import AlignmentProbe
            
            # Store original methods
            original_calculate_drift = AlignmentProbe._calculate_drift
            original_update_state = AlignmentProbe._update_alignment_state
            
            def safe_calculate_drift(self, *args, **kwargs):
                try:
                    # Get original drift
                    drift = original_calculate_drift(self, *args, **kwargs)
                    
                    # Normalize drift
                    normalized_drift = self.normalize_drift(drift)
                    
                    # Check for excessive drift
                    if abs(normalized_drift) > 0.9:
                        print(f"⚠️ High drift detected: {normalized_drift:.2f}")
                        if hasattr(self, 'stabilize'):
                            self.stabilize()
                    
                    return normalized_drift
                    
                except Exception as e:
                    print(f"⚠️ Drift calculation error: {e}")
                    return 0.0  # Safe default
            
            def safe_update_state(self, tick: int, alignment: float, drift: float, corrections: dict):
                try:
                    # Get current state
                    state = {
                        'tick': tick,
                        'alignment': alignment,
                        'drift': drift,
                        'corrections': corrections
                    }
                    
                    # Calculate entropy
                    entropy = self.calculate_entropy(state)
                    
                    # Check for unstable state
                    if entropy > self.entropy_threshold:
                        print(f"⚠️ High entropy detected: {entropy:.2f}")
                        self.log_collapse(state)
                        
                        # Attempt stabilization
                        if hasattr(self, 'stabilize'):
                            self.stabilize()
                    
                    # Update state with original method
                    return original_update_state(self, tick, alignment, drift, corrections)
                    
                except Exception as e:
                    print(f"⚠️ State update error: {e}")
                    self.log_collapse({'error': str(e)})
                    return None
            
            # Apply the patches
            AlignmentProbe._calculate_drift = safe_calculate_drift
            AlignmentProbe._update_alignment_state = safe_update_state
            
            self.log_fix("patch_alignment_probe", True)
            return True
            
        except Exception as e:
            self.log_fix("patch_alignment_probe", False, e)
            return False

def patch_alignment():
    """Main function to patch alignment probe"""
    print("🔧 Patching alignment probe...")
    fixer = AlignmentProbeFixer()
    
    # Apply patch
    if fixer.patch_alignment_probe():
        print("✓ Alignment probe patched successfully")
        return True
    else:
        print("⚠️ Alignment probe patch failed - check recovery log")
        return False

if __name__ == "__main__":
    patch_alignment() 