# ============================================
# DAWN BLOOM SYSTEM - QUICK PATCH
# Apply this patch to get blooms spawning immediately
# ============================================

"""
INSTRUCTIONS:
1. Save this file as bloom_patch.py in your DAWN root directory
2. Run: python bloom_patch.py
3. This will create patched versions of your files
4. Test with: python test_patched_bloom.py
"""

import os
import shutil
from datetime import datetime

def apply_bloom_patch():
    """Apply emergency patches to get blooms spawning"""
    
    print("🔧 DAWN Bloom System Quick Patch")
    print("=" * 50)
    
    # Patch 1: Create a forced spawn_bloom function
    forced_spawn_bloom = '''# Patched version of spawn_bloom.py with force spawn enabled
import os
import json
from datetime import datetime

# Force bloom spawning for debugging
FORCE_BLOOM_SPAWN = True

def enhanced_spawn_bloom(bloom_data, pulse, bypass_scup=False):
    """Patched version - forces bloom spawning"""
    
    global FORCE_BLOOM_SPAWN
    
    if FORCE_BLOOM_SPAWN:
        print("[PATCH] Force spawning enabled - bypassing all checks")
        bypass_scup = True
    
    # Extract parameters
    seed_id = bloom_data.get("seed_id", f"patched_bloom_{datetime.now().strftime('%H%M%S')}")
    
    print(f"[PATCH] Spawning bloom: {seed_id}")
    
    # Create directories
    os.makedirs("juliet_flowers/bloom_metadata", exist_ok=True)
    os.makedirs("juliet_flowers/fractal_signatures", exist_ok=True)
    
    # Generate fractal memory string (simple version)
    fractal_memory = {
        "raw": f"α{bloom_data.get('mood', 'debug')[0]}~₅|Ψ@|Σ^",
        "metadata": {
            "encoding": "juliet-fractal-v1",
            "bloom_id": seed_id
        }
    }
    bloom_data["fractal_memory"] = fractal_memory
    
    # Save bloom
    timestamp_str = datetime.now().isoformat(timespec='seconds').replace(':', '-')
    filename = f"{seed_id}_{timestamp_str}.json"
    filepath = os.path.join("juliet_flowers/bloom_metadata", filename)
    
    bloom_data["generated_at"] = datetime.now().isoformat()
    bloom_data["patched"] = True
    
    with open(filepath, "w") as f:
        json.dump(bloom_data, f, indent=2)
    
    print(f"[PATCH] ✅ Bloom saved: {filepath}")
    print(f"[PATCH] ✅ Fractal memory: {fractal_memory['raw']}")
    
    return filepath

# Fallback imports
def calculate_SCUP(**kwargs):
    return 0.5  # Default SCUP value

def generate_julia_image(**kwargs):
    return "patched_fractal.png"

# Export the patched function
spawn_bloom = enhanced_spawn_bloom
'''
    
    # Save patched spawn_bloom
    with open("spawn_bloom_patched.py", "w") as f:
        f.write(forced_spawn_bloom)
    print("✅ Created spawn_bloom_patched.py")
    
    # Patch 2: Create test script
    test_script = '''# Test script for patched bloom system
import sys
sys.path.insert(0, '.')  # Use current directory first

from spawn_bloom_patched import enhanced_spawn_bloom
from datetime import datetime

print("\\n🧪 Testing Patched Bloom System")
print("=" * 50)

# Test 1: Basic bloom
test_bloom = {
    "seed_id": "patch_test_001",
    "lineage_depth": 1,
    "bloom_factor": 1.0,
    "entropy_score": 0.5,
    "mood": "curious",
    "trigger_type": "patch_test"
}

pulse = {"heat": 0.0, "mood_pressure": {}}

print("\\n[TEST 1] Spawning basic bloom...")
result = enhanced_spawn_bloom(test_bloom, pulse)
print(f"Result: {result}")

# Test 2: Multiple moods
moods = ["joyful", "anxious", "reflective", "focused", "curious"]
for i, mood in enumerate(moods):
    bloom = {
        "seed_id": f"mood_test_{mood}",
        "lineage_depth": i + 1,
        "bloom_factor": 1.0 + i * 0.1,
        "entropy_score": 0.3 + i * 0.1,
        "mood": mood,
        "trigger_type": "mood_test"
    }
    print(f"\\n[TEST {i+2}] Spawning {mood} bloom...")
    result = enhanced_spawn_bloom(bloom, pulse)
    print(f"Result: {result}")

print("\\n✅ Testing complete!")
print("Check juliet_flowers/bloom_metadata/ for generated blooms")
'''
    
    with open("test_patched_bloom.py", "w") as f:
        f.write(test_script)
    print("✅ Created test_patched_bloom.py")
    
    # Patch 3: Create fractal string visualizer
    fractal_viz = '''# Simple fractal string visualizer
import json
import os

def visualize_bloom_fractals():
    """Display fractal strings from blooms"""
    
    bloom_dir = "juliet_flowers/bloom_metadata"
    if not os.path.exists(bloom_dir):
        print("No bloom directory found")
        return
    
    print("\\n🌸 Bloom Fractal Memory Strings")
    print("=" * 50)
    
    files = sorted([f for f in os.listdir(bloom_dir) if f.endswith('.json')])[-10:]
    
    for file in files:
        with open(os.path.join(bloom_dir, file), 'r') as f:
            bloom = json.load(f)
        
        print(f"\\nBloom: {bloom.get('seed_id', 'unknown')}")
        print(f"Mood: {bloom.get('mood', 'unknown')}")
        
        if 'fractal_memory' in bloom:
            fractal = bloom['fractal_memory']
            if isinstance(fractal, dict):
                print(f"Fractal: {fractal.get('raw', 'no string')}")
            else:
                print(f"Fractal: {fractal}")
        else:
            print("Fractal: not found")
        
        print(f"Factor: {bloom.get('bloom_factor', 0):.2f}")
        print(f"Entropy: {bloom.get('entropy_score', 0):.2f}")

if __name__ == "__main__":
    visualize_bloom_fractals()
'''
    
    with open("visualize_fractals.py", "w") as f:
        f.write(fractal_viz)
    print("✅ Created visualize_fractals.py")
    
    # Create backup of original files if they exist
    if os.path.exists("bloom/spawn_bloom.py"):
        backup_name = f"bloom/spawn_bloom_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        shutil.copy("bloom/spawn_bloom.py", backup_name)
        print(f"✅ Backed up original to {backup_name}")
    
    print("\n" + "=" * 50)
    print("🎉 Patch applied successfully!")
    print("\nNext steps:")
    print("1. Run: python test_patched_bloom.py")
    print("2. Check juliet_flowers/bloom_metadata/ for new blooms")
    print("3. Run: python visualize_fractals.py to see fractal strings")
    print("\nTo use patched version in your code:")
    print("  from spawn_bloom_patched import enhanced_spawn_bloom")
    print("\n⚠️  This is a temporary patch for debugging.")
    print("Once working, integrate the fixes into your main code.")

if __name__ == "__main__":
    apply_bloom_patch()
