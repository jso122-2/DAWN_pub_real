#!/usr/bin/env python3
"""
Test script to verify all DAWN imports work correctly
"""

import sys
from pathlib import Path

# Add the parent directory to path so we can import from interface
sys.path.insert(0, str(Path(__file__).parent))

print("Testing DAWN imports...")

try:
    from cognitive.spontaneity import create_spontaneity_system, DAWNSpontaneity
    print("✓ Cognitive spontaneity imports OK")
except Exception as e:
    print(f"✗ Cognitive spontaneity import failed: {e}")

try:
    from core.consciousness import create_consciousness
    print("✓ Core consciousness import OK")
except Exception as e:
    print(f"✗ Core consciousness import failed: {e}")

try:
    from core.pattern_detector import create_pattern_detector
    print("✓ Core pattern_detector import OK")
except Exception as e:
    print(f"✗ Core pattern_detector import failed: {e}")

try:
    from core.state_machine import create_state_machine
    print("✓ Core state_machine import OK")
except Exception as e:
    print(f"✗ Core state_machine import failed: {e}")

try:
    from core.fractal_emotions import create_fractal_emotion_system
    print("✓ Core fractal_emotions import OK")
except Exception as e:
    print(f"✗ Core fractal_emotions import failed: {e}")

try:
    from core.memory_manager import get_memory_manager
    print("✓ Core memory_manager import OK")
except Exception as e:
    print(f"✗ Core memory_manager import failed: {e}")

try:
    from core.mood_gradient import create_mood_gradient_plotter
    print("✓ Core mood_gradient import OK")
except Exception as e:
    print(f"✗ Core mood_gradient import failed: {e}")

try:
    from core.consciousness_state import ConsciousnessStatePersistence
    print("✓ Core consciousness_state import OK")
except Exception as e:
    print(f"✗ Core consciousness_state import failed: {e}")

try:
    from bloom.rebloomer import Rebloomer
    print("✓ Bloom rebloomer import OK")
except Exception as e:
    print(f"✗ Bloom rebloomer import failed: {e}")

print("\n✅ All imports successful!" if all else "❌ Some imports failed") 