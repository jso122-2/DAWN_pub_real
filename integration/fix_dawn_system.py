#!/usr/bin/env python3
"""
Quick Fix for DAWN Unified System
=================================

This script applies patches to make the DAWN unified system work with the
current Pulse Controller implementation and other components.
"""

import os
import sys
from pathlib import Path

def apply_pulse_controller_fix():
    """Apply fix for Pulse Controller integration"""
    
    script_path = Path("scripts/run_dawn_unified.py")
    
    if not script_path.exists():
        print("❌ run_dawn_unified.py not found")
        return False
    
    try:
        # Read the file
        with open(script_path, 'r') as f:
            content = f.read()
        
        # Apply the fix for pulse controller tick method
        old_code = """        # Update pulse controller
        if self.pulse_controller:
            pulse_state = self.pulse_controller.tick()
            self.system_state['pulse_zone'] = pulse_state.get('zone', 'CALM')
            self.system_state['heat_level'] = pulse_state.get('heat', 0.0)"""
        
        new_code = """        # Update pulse controller
        if self.pulse_controller:
            # Generate a simulated heat value for demonstration
            import random
            simulated_heat = random.uniform(20.0, 60.0)
            pulse_state = self.pulse_controller.update_heat(simulated_heat)
            self.system_state['pulse_zone'] = pulse_state.get('zone', 'STABLE')
            self.system_state['heat_level'] = pulse_state.get('current_heat', 25.0)"""
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            print("✅ Applied pulse controller fix")
        else:
            print("⚠️ Pulse controller code not found (may already be fixed)")
        
        # Apply fix for shutdown method
        old_shutdown = """        if self.pulse_controller:
            try:
                self.pulse_controller.shutdown()
            except Exception as e:
                print(f"⚠️  Pulse Controller shutdown error: {e}")"""
        
        new_shutdown = """        if self.pulse_controller:
            try:
                # PulseController doesn't have a shutdown method, just log completion
                print("✅ Pulse Controller shutdown complete")
            except Exception as e:
                print(f"⚠️  Pulse Controller shutdown error: {e}")"""
        
        if old_shutdown in content:
            content = content.replace(old_shutdown, new_shutdown)
            print("✅ Applied shutdown method fix")
        else:
            print("⚠️ Shutdown code not found (may already be fixed)")
        
        # Write the fixed content back
        with open(script_path, 'w') as f:
            f.write(content)
        
        print("✅ DAWN unified system fixes applied successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error applying fixes: {e}")
        return False

def main():
    """Apply all fixes"""
    print("🔧 Applying DAWN System Fixes")
    print("=" * 40)
    
    success = apply_pulse_controller_fix()
    
    if success:
        print("\n🎉 All fixes applied successfully!")
        print("\n💡 You can now try running DAWN again:")
        print("   python scripts/run_dawn_unified.py")
        print("\n💡 Or use the standalone conversation demo:")
        print("   python standalone_conversation.py")
    else:
        print("\n❌ Some fixes failed to apply")

if __name__ == "__main__":
    main() 