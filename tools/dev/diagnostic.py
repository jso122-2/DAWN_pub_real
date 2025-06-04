# diagnostic.py - Save this in your Tick_engine folder and run it

import os
import sys
from pathlib import Path

print("=== DAWN HelixBridge Diagnostic ===\n")

# Check current directory
current_dir = Path(__file__).parent
print(f"Current directory: {current_dir}")

# Check if helix folder exists
helix_dir = current_dir / "helix"
print(f"\nChecking for helix directory: {helix_dir}")
print(f"Exists: {helix_dir.exists()}")

if helix_dir.exists():
    # List contents
    print("\nContents of helix directory:")
    for item in helix_dir.iterdir():
        print(f"  - {item.name}")
    
    # Check for helix_bridge.py
    helix_bridge_file = helix_dir / "helix_bridge.py"
    print(f"\nhelix_bridge.py exists: {helix_bridge_file.exists()}")
    
    if helix_bridge_file.exists():
        print(f"File size: {helix_bridge_file.stat().st_size} bytes")

# Try to import HelixBridge
print("\n=== Import Test ===")
try:
    from helix.helix_bridge import HelixBridge
    print("✓ Successfully imported HelixBridge from helix.helix_bridge")
    
    # Check what methods it has
    print("\nHelixBridge methods:")
    for attr in dir(HelixBridge):
        if not attr.startswith('__'):
            print(f"  - {attr}")
    
    # Check specifically for _safe_import
    if hasattr(HelixBridge, '_safe_import'):
        print("\n✓ HelixBridge has _safe_import method")
    else:
        print("\n✗ HelixBridge MISSING _safe_import method!")
        
    # Try to instantiate it
    try:
        bridge = HelixBridge()
        print("\n✓ Successfully instantiated HelixBridge")
        
        # Check instance methods
        print("\nInstance methods:")
        for attr in dir(bridge):
            if not attr.startswith('__') and callable(getattr(bridge, attr)):
                print(f"  - {attr}")
                
    except Exception as e:
        print(f"\n✗ Error instantiating HelixBridge: {e}")
        
except ImportError as e:
    print(f"✗ Failed to import HelixBridge: {e}")
    print("\nUsing fallback implementation check...")
    
    # Check if the fallback is being used
    try:
        # Add current dir to path
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))
            
        # Try importing helix_import_architecture
        import helix_import_architecture
        
        if hasattr(helix_import_architecture, 'HelixBridge'):
            print("✓ Found HelixBridge in helix_import_architecture")
            HB = helix_import_architecture.HelixBridge
            
            # Check methods
            print("\nFallback HelixBridge methods:")
            for attr in dir(HB):
                if not attr.startswith('__'):
                    print(f"  - {attr}")
                    
            if hasattr(HB, '_safe_import'):
                print("\n✓ Fallback HelixBridge has _safe_import method")
            else:
                print("\n✗ Fallback HelixBridge MISSING _safe_import method!")
                
    except Exception as e:
        print(f"Error checking fallback: {e}")

print("\n=== End Diagnostic ===")