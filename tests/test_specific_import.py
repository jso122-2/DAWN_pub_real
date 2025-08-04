#!/usr/bin/env python3
"""
Test Specific Import
===================

Test specific imports to isolate the relative import error.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

def test_specific_imports():
    """Test specific imports that might be causing the relative import error"""
    
    print("🔍 Testing Specific Imports")
    print("=" * 40)
    
    # Test 1: Import cognitive.rebloom_lineage
    print("1. Testing cognitive.rebloom_lineage import...")
    try:
        from cognitive.rebloom_lineage import ReblooooomLineageTracker, track_rebloom_lineage
        print("   ✅ cognitive.rebloom_lineage import successful")
    except Exception as e:
        print(f"   ❌ cognitive.rebloom_lineage import failed: {e}")
    
    # Test 2: Import core.memory_rebloom_reflex
    print("\n2. Testing core.memory_rebloom_reflex import...")
    try:
        from core.memory_rebloom_reflex import MemoryRebloomReflex
        print("   ✅ core.memory_rebloom_reflex import successful")
    except Exception as e:
        print(f"   ❌ core.memory_rebloom_reflex import failed: {e}")
    
    # Test 3: Import processes.rebloom_reflex
    print("\n3. Testing processes.rebloom_reflex import...")
    try:
        from processes.rebloom_reflex import evaluate_and_rebloom
        print("   ✅ processes.rebloom_reflex import successful")
    except Exception as e:
        print(f"   ❌ processes.rebloom_reflex import failed: {e}")
    
    # Test 4: Import backend.cognitive.cognition_runtime
    print("\n4. Testing backend.cognitive.cognition_runtime import...")
    try:
        from backend.cognitive.cognition_runtime import CognitionRuntime
        print("   ✅ backend.cognitive.cognition_runtime import successful")
    except Exception as e:
        print(f"   ❌ backend.cognitive.cognition_runtime import failed: {e}")
    
    print("\n✅ Specific import test complete")

if __name__ == "__main__":
    test_specific_imports() 