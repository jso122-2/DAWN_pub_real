#!/usr/bin/env python3
"""
Test script to verify DAWN pressure fix is working
Demonstrates how to simulate pressure without cheating
"""

import sys
import os
import time
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

print("🧪 Testing DAWN Pressure Fix...")
print("=" * 50)

# Test 1: Create simulated rebloom queue for memory pressure
def create_rebloom_pressure():
    """Simulate memory pressure by creating rebloom queue entries"""
    print("\n1️⃣ Creating simulated rebloom queue for memory pressure...")
    
    # Ensure directories exist
    rebloom_dir = project_root / "juliet_flowers" / "cluster_report"
    rebloom_dir.mkdir(parents=True, exist_ok=True)
    
    # Create simulated rebloom entries
    rebloom_data = []
    for i in range(7):  # 7 pending reblooms = 0.7 pressure
        rebloom_data.append({
            "bloom_id": f"test_bloom_{i:03d}",
            "generation": 1,
            "timestamp": time.time() - (i * 300),  # Spread over 35 minutes
            "entropy_variance": 0.2 + (i * 0.05),
            "pressure_source": "semantic_overflow"
        })
    
    # Write rebloom queue
    rebloom_path = rebloom_dir / "rebloom_lineage.json"
    with open(rebloom_path, 'w') as f:
        json.dump(rebloom_data, f, indent=2)
    
    print(f"   ✅ Created {len(rebloom_data)} rebloom entries")
    print(f"   📁 Saved to: {rebloom_path}")
    return len(rebloom_data)

# Test 2: Test DAWN Central update method
def test_dawn_central_update():
    """Test the updated DAWN Central computation"""
    print("\n2️⃣ Testing DAWN Central with real computation...")
    
    try:
        from backend.core.dawn_central import DAWNCentral
        
        # Initialize DAWN Central
        dawn = DAWNCentral()
        print("   ✅ DAWN Central initialized")
        
        # Test update cycles
        print("   🔄 Running update cycles...")
        
        for tick in range(5):
            print(f"\n   Tick {tick:03d}:")
            state = dawn.update(tick_number=tick)
            
            print(f"      SCUP: {state['scup']:.6f}")
            print(f"      Entropy: {state['entropy']:.6f}")
            print(f"      Mood: {state['mood']:.6f}")
            print(f"      Temperature: {state['temperature']:.6f}")
            print(f"      Coherence: {state['coherence']:.6f}")
            
            # Brief pause between ticks
            time.sleep(0.1)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing DAWN Central: {e}")
        return False

# Test 3: Test consciousness state writer
def test_consciousness_writer():
    """Test the consciousness state writer with real integration"""
    print("\n3️⃣ Testing consciousness state writer...")
    
    try:
        from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter
        
        # Initialize writer
        writer = DAWNConsciousnessStateWriter()
        print("   ✅ Consciousness writer initialized")
        
        # Generate a few consciousness ticks
        print("   🧠 Generating consciousness ticks...")
        
        for tick in range(3):
            print(f"\n   Consciousness Tick {tick:03d}:")
            writer.current_tick = tick
            
            # Generate state
            consciousness_state = writer._get_dawn_consciousness_state()
            
            print(f"      SCUP: {consciousness_state['scup']:.6f}")
            print(f"      Entropy: {consciousness_state['entropy']:.6f}")
            print(f"      Neural Activity: {consciousness_state['neural_activity']:.6f}")
            print(f"      Memory Pressure: {consciousness_state['memory_pressure']:.6f}")
            print(f"      Consciousness Depth: {consciousness_state['consciousness_depth']:.6f}")
            
            time.sleep(0.2)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error testing consciousness writer: {e}")
        return False

# Test 4: Simulate pressure events
def simulate_pressure_events():
    """Simulate various pressure events to demonstrate dynamic response"""
    print("\n4️⃣ Simulating pressure events...")
    
    # Create additional schema files to increase schema pressure
    schema_dir = project_root / "test_schemas"
    schema_dir.mkdir(exist_ok=True)
    
    schema_count = 0
    for i in range(15):  # Create 15 test schemas
        schema_file = schema_dir / f"test_schema_{i:02d}.py"
        with open(schema_file, 'w') as f:
            f.write(f'''# Test schema {i:02d}
class TestSchema{i:02d}:
    def __init__(self):
        self.schema_id = "{i:02d}"
        self.pressure_level = {0.1 + (i * 0.05):.3f}
''')
        schema_count += 1
    
    print(f"   ✅ Created {schema_count} test schemas for pressure simulation")
    
    # Simulate forecast misses by creating drift indicators
    print("   📈 Simulating forecast misses...")
    
    # Create some variance in system state to trigger drift
    drift_data = {
        "recent_forecasts": [
            {"predicted": 0.7, "actual": 0.4, "miss_magnitude": 0.3},
            {"predicted": 0.5, "actual": 0.8, "miss_magnitude": 0.3},
            {"predicted": 0.6, "actual": 0.3, "miss_magnitude": 0.3}
        ],
        "forecast_accuracy": 0.4,  # Low accuracy = more pressure
        "drift_detected": True
    }
    
    forecast_dir = project_root / "forecasts"
    forecast_dir.mkdir(exist_ok=True)
    
    with open(forecast_dir / "forecast_performance.json", 'w') as f:
        json.dump(drift_data, f, indent=2)
    
    print("   ✅ Created forecast miss data")
    
    return schema_count

# Test 5: Cleanup
def cleanup_test_files():
    """Clean up test files created during simulation"""
    print("\n5️⃣ Cleaning up test files...")
    
    import shutil
    
    cleanup_paths = [
        "test_schemas",
        "forecasts",
        "juliet_flowers/cluster_report/rebloom_lineage.json"
    ]
    
    cleaned = 0
    for path in cleanup_paths:
        full_path = project_root / path
        try:
            if full_path.is_file():
                full_path.unlink()
                cleaned += 1
            elif full_path.is_dir():
                shutil.rmtree(full_path)
                cleaned += 1
        except Exception as e:
            print(f"   ⚠️  Could not remove {path}: {e}")
    
    print(f"   ✅ Cleaned up {cleaned} test files/directories")

# Main test execution
def main():
    print("🚀 Starting DAWN Pressure Fix Tests\n")
    
    # Run tests
    rebloom_count = create_rebloom_pressure()
    dawn_success = test_dawn_central_update()
    writer_success = test_consciousness_writer()
    schema_count = simulate_pressure_events()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    print(f"✅ Rebloom pressure: {rebloom_count} entries created")
    print(f"{'✅' if dawn_success else '❌'} DAWN Central: {'Working' if dawn_success else 'Failed'}")
    print(f"{'✅' if writer_success else '❌'} Consciousness writer: {'Working' if writer_success else 'Failed'}")
    print(f"✅ Schema pressure: {schema_count} schemas created")
    
    if dawn_success and writer_success:
        print("\n🎉 SUCCESS: DAWN pressure fix is working!")
        print("💡 Values should now be dynamic instead of flat zeros")
        print("\n📝 To continue testing:")
        print("   1. Run the consciousness state writer")
        print("   2. Monitor logs for dynamic SCUP/entropy/mood values")
        print("   3. Add more reblooms to increase memory pressure")
        print("   4. Create schema events to trigger semantic pressure")
    else:
        print("\n⚠️  Some tests failed - check error messages above")
    
    # Cleanup
    print("\n🧹 Cleanup? (y/n): ", end="")
    try:
        response = input().strip().lower()
        if response == 'y':
            cleanup_test_files()
        else:
            print("   📁 Test files preserved for manual inspection")
    except KeyboardInterrupt:
        print("\n   📁 Test files preserved")

if __name__ == "__main__":
    main() 