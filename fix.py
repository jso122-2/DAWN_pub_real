# debug_pulse_import.py - Save this in your Tick_engine folder and run it

import os
from pathlib import Path

print("=== Debugging pulse_heat import ===\n")

# Check current directory
current_dir = Path(__file__).parent
print(f"Current directory: {current_dir}")

# Check if pulse_heat.py exists
pulse_heat_file = current_dir / "pulse_heat.py"
print(f"\npulse_heat.py exists: {pulse_heat_file.exists()}")
if pulse_heat_file.exists():
    print(f"File size: {pulse_heat_file.stat().st_size} bytes")

# Try direct import
print("\n=== Trying direct import ===")
try:
    import pulse_heat
    print("✓ Direct import successful!")
    print(f"Module location: {pulse_heat.__file__}")
    
    # Check if pulse object exists
    if hasattr(pulse_heat, 'pulse'):
        print("✓ pulse object found in module")
        print(f"pulse type: {type(pulse_heat.pulse)}")
    else:
        print("✗ pulse object NOT found in module")
        print("Available attributes:", [attr for attr in dir(pulse_heat) if not attr.startswith('_')][:10])
        
except Exception as e:
    print(f"✗ Direct import failed: {e}")
    import traceback
    traceback.print_exc()

# Try helix import
print("\n=== Trying helix import ===")
try:
    from helix_import_architecture import helix_import
    pulse_module = helix_import("pulse_heat")
    if pulse_module:
        print("✓ Helix import successful!")
        if hasattr(pulse_module, 'pulse'):
            print("✓ pulse object found via helix import")
        else:
            print("✗ pulse object NOT found via helix import")
    else:
        print("✗ Helix import returned None")
except Exception as e:
    print(f"✗ Helix import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n=== End Debug ===")