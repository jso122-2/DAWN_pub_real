#!/usr/bin/env python3
"""
Test import to debug the issue
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Python path:")
for path in sys.path:
    print(f"  {path}")

print("\nTrying to import core.dawn_runner...")
try:
    from core.dawn_runner import DAWNUnifiedRunner
    print("✅ Successfully imported DAWNUnifiedRunner")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print(f"   Error type: {type(e)}")
    
    # Try to import the module directly
    try:
        import core.dawn_runner
        print("✅ Successfully imported core.dawn_runner module")
    except ImportError as e2:
        print(f"❌ Module import also failed: {e2}")

print("\nChecking if core directory exists...")
core_path = Path("core")
if core_path.exists():
    print(f"✅ Core directory exists: {core_path}")
    print(f"   Contents: {list(core_path.glob('*.py'))[:5]}")
else:
    print("❌ Core directory not found")

print("\nChecking if dawn_runner.py exists...")
dawn_runner_path = Path("core/dawn_runner.py")
if dawn_runner_path.exists():
    print(f"✅ dawn_runner.py exists: {dawn_runner_path}")
else:
    print("❌ dawn_runner.py not found") 