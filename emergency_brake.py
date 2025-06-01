from helix_import_architecture import helix_import
pulse_heat = helix_import("pulse_heat")
# /Tick_engine/emergency_brake.py
# Emergency brake to stop the heat saturation loop

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def apply_emergency_brake():
    """Stop the emergency recovery loop immediately"""
    try:
        
        print("[EMERGENCY] 🚨 Applying emergency brake...")
        print(f"[EMERGENCY] Current heat: {pulse.get_heat():.3f}")
        
        # Force cool the system
        if hasattr(pulse, 'remove_heat'):
            cooled = pulse.remove_heat(6.0, "emergency_brake")
            print(f"[EMERGENCY] ❄️ Emergency cooling applied: -{cooled:.3f}")
        else:
            pulse.heat = 3.0
            pulse.current_heat = 3.0
            print("[EMERGENCY] ❄️ Direct heat reset to 3.0")
        
        # Reset thermal momentum
        if hasattr(pulse, 'thermal_momentum'):
            pulse.thermal_momentum = 0.0
            print("[EMERGENCY] 🔄 Thermal momentum reset")
        
        # Clear emergency recovery source
        if hasattr(pulse, 'heat_sources') and 'emergency_recovery' in pulse.heat_sources:
            pulse.heat_sources['emergency_recovery'].cumulative = 0.0
            pulse.heat_sources['emergency_recovery'].last_contribution = 0.0
            print("[EMERGENCY] 🧹 Emergency recovery source cleared")
        
        print(f"[EMERGENCY] ✅ New heat: {pulse.get_heat():.3f}")
        return True
        
    except Exception as e:
        print(f"[EMERGENCY] ❌ Brake failed: {e}")
        return False

if __name__ == "__main__":
    success = apply_emergency_brake()
    if success:
        print("[EMERGENCY] 🎉 Emergency brake successful! DAWN should stabilize now.")
    else:
        print("[EMERGENCY] 💥 Emergency brake failed - system may need restart.")
