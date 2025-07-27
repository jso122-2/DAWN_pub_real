#!/usr/bin/env python
"""
Wrapper to run DAWN visual scripts with proper imports
Usage: python run_visual.py <script_name>
"""

import sys
import os
from pathlib import Path

# Add all required paths
base_path = Path(r"/root/DAWN_Vault/Tick_engine/Tick_engine/visual")
sys.path.insert(0, str(base_path))
sys.path.insert(0, str(base_path / "visual"))

# Mock missing modules
class MockModule:
    def __getattr__(self, name):
        # Return mock objects/functions
        if name == "pulse":
            return MockPulse()
        return lambda *args, **kwargs: None

class MockPulse:
    heat = 0.5
    heat_capacity = 1.0
    tick_count = 1100
    
    def classify(self):
        return "🟡 active"
    
    def get_thermal_profile(self):
        return {
            'current_heat': 0.5,
            'stability_index': 0.8,
            'thermal_momentum': 0.2
        }
    
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

# Install mocks
mock_modules = [
    "helix_import_architecture", 
    "pulse_heat", 
    "unified_pulse_heat",
    "core.event_bus",
    "core.tick_hook_autonomous",
    "core.tick_emitter",
    "semantic.sigil_ring",
    "persephone.lifecycle",
    "schema.schema_health_index",
    "owl.entropy_tracker"
]

for module in mock_modules:
    if module not in sys.modules:
        sys.modules[module] = MockModule()

# Special handling for pulse
sys.modules["pulse"] = MockModule()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_visual.py <script_name>")
        sys.exit(1)
    
    script_name = sys.argv[1]
    script_path = base_path / "visual" / script_name
    
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        sys.exit(1)
    
    print(f"Running {script_name}...")
    os.chdir(str(base_path / "visual"))
    
    try:
        exec(open(script_path, encoding="utf-8").read())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
