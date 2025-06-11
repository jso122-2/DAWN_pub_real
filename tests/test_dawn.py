#!/usr/bin/env python3
"""DAWN Simple Test"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.dawn_registry import consciousness

print("🌅 DAWN Simple Test")
print("=" * 40)

# Try each component
for name in ['pulse_heat', 'bloom_engine', 'owl_system']:
    try:
        comp = consciousness.summon(name)
        print(f"✓ {name}: {type(comp).__name__}")
    except Exception as e:
        print(f"✗ {name}: {e}")

print("\nDone!")
