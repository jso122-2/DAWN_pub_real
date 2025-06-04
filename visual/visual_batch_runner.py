"""
Quick fix to make DAWN visualization scripts work
Run this from the Tick_engine directory
"""

import os
import sys
from pathlib import Path

# Get paths
tick_engine_path = Path.cwd()
visual_path = tick_engine_path / "visual"

print("🔧 DAWN Visual Scripts Quick Fix")
print(f"📁 Working directory: {tick_engine_path}")

# 1. Create required directories
print("\n📁 Creating required directories...")
required_dirs = [
    "visual_output",
    "visual_output/bloom_lineage",
    "visual_output/pulse_maps", 
    "visual_output/entropy_charts",
    "visual_output/sigil_trace",
    "juliet_flowers",
    "juliet_flowers/bloom_metadata",
    "juliet_flowers/cluster_report",
    "juliet_flowers/sealed",
    "logs",
    "codex",
    "semantic",
    "owl",
    "bloom",
    "schema"
]

for dir_name in required_dirs:
    dir_path = tick_engine_path / dir_name
    dir_path.mkdir(parents=True, exist_ok=True)
    print(f"  ✅ {dir_name}")

# 2. Create dummy data files
print("\n📄 Creating dummy data files...")

# Tick log
tick_log = tick_engine_path / "logs" / "tick_log.csv"
if not tick_log.exists():
    with open(tick_log, 'w') as f:
        f.write("tick,zone,pulse,entropy,scup,timestamp\n")
        for i in range(1000, 1200):
            zone = ["🟢 calm", "🟡 active", "🔴 surge"][i % 3]
            f.write(f"{i},{zone},{0.3 + (i%10)*0.05},{0.2 + (i%20)*0.02},{0.8 - (i%30)*0.01},2024-01-{i%30+1}\n")
    print("  ✅ logs/tick_log.csv")

# Field snapshot
field_snapshot = tick_engine_path / "logs" / "field_snapshot.json"
if not field_snapshot.exists():
    import json
    data = {
        "current_tick": 1100,
        "snapshots": [
            {
                "tick": 1000 + i,
                "zone": ["calm", "active", "surge"][i % 3],
                "pulse_heat": 0.5 + (i % 10) * 0.05,
                "entropy": 0.3 + (i % 20) * 0.02,
                "scup": 0.7 - (i % 30) * 0.01,
                "bloom_count": i % 5
            }
            for i in range(100)
        ]
    }
    with open(field_snapshot, 'w') as f:
        json.dump(data, f, indent=2)
    print("  ✅ logs/field_snapshot.json")

# Interval log
interval_log = tick_engine_path / "juliet_flowers" / "cluster_report" / "interval_log.csv"
with open(interval_log, 'w') as f:
    for i in range(100):
        f.write(f"{1.0 + i * 0.01 + (i%10) * 0.001}\n")
print("  ✅ juliet_flowers/cluster_report/interval_log.csv")

# Zone overlay log
zone_log = tick_engine_path / "juliet_flowers" / "cluster_report" / "zone_overlay_log.csv"
with open(zone_log, 'w') as f:
    for i in range(100):
        tick = 1000 + i
        zone = ["🟢 calm", "🟡 active", "🔴 surge"][i % 3]
        heat = 0.3 + (i % 10) * 0.05
        f.write(f"{tick},{zone},{heat:.3f}\n")
print("  ✅ juliet_flowers/cluster_report/zone_overlay_log.csv")

# Sigil memory
sigil_memory = tick_engine_path / "codex" / "sigil_memory_ring.json"
if not sigil_memory.exists():
    import json
    data = {
        "sigils": {
            f"sigil_{i}": {
                "name": f"sigil_{i}",
                "type": ["entropy_bloom", "memory_cascade", "semantic_drift"][i % 3],
                "entropy": 0.1 + i * 0.15,
                "created_tick": 1000 + i * 10,
                "last_active": 1050 + i * 5
            }
            for i in range(8)
        },
        "current_tick": 1100
    }
    with open(sigil_memory, 'w') as f:
        json.dump(data, f, indent=2)
    print("  ✅ codex/sigil_memory_ring.json")

# Bloom metadata
for i in range(5):
    bloom_file = tick_engine_path / "juliet_flowers" / "bloom_metadata" / f"bloom_{i}.json"
    if not bloom_file.exists():
        import json
        bloom_data = {
            "seed_id": f"A{i}",
            "bloom_type": ["memory", "semantic", "temporal"][i % 3],
            "created_tick": 1000 + i * 20,
            "entropy": 0.2 + i * 0.1,
            "depth": i + 1,
            "lineage": f"root-{i}"
        }
        with open(bloom_file, 'w') as f:
            json.dump(bloom_data, f, indent=2)
print("  ✅ Created 5 bloom metadata files")

# 3. Create a wrapper script for running visuals with proper imports
print("\n🔄 Creating run_visual.py wrapper...")

wrapper_content = f'''#!/usr/bin/env python
"""
Wrapper to run DAWN visual scripts with proper imports
Usage: python run_visual.py <script_name>
"""

import sys
import os
from pathlib import Path

# Add all required paths
base_path = Path(r"{tick_engine_path}")
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
        return {{
            'current_heat': 0.5,
            'stability_index': 0.8,
            'thermal_momentum': 0.2
        }}
    
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
        print(f"Script not found: {{script_path}}")
        sys.exit(1)
    
    print(f"Running {{script_name}}...")
    os.chdir(str(base_path / "visual"))
    
    try:
        exec(open(script_path, encoding="utf-8").read())
    except Exception as e:
        print(f"Error: {{e}}")
        import traceback
        traceback.print_exc()
'''

wrapper_path = tick_engine_path / "run_visual.py"
with open(wrapper_path, 'w') as f:
    f.write(wrapper_content)
print(f"  ✅ Created run_visual.py")

print("\n✅ Quick fix complete!")
print("\n📖 How to use:")
print("1. To run a specific visual:")
print("   python run_visual.py bloom_lineage_radar.py")
print("\n2. To diagnose issues:")
print("   python visual_diagnostic.py --script bloom_lineage_radar.py")
print("\n3. To create fixed versions of all scripts:")
print("   python visual_diagnostic.py --fix-imports")