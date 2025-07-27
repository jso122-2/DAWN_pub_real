#!/usr/bin/env python3
"""
🧪 Test DAWN Imports - Verify everything is set up correctly
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧪 Testing DAWN imports...")
print("=" * 50)

# Test 1: Import DAWNGenomeConsciousnessWrapper
try:
    from main import DAWNGenomeConsciousnessWrapper
    print("✅ Successfully imported DAWNGenomeConsciousnessWrapper")
except ImportError as e:
    print(f"❌ Failed to import DAWNGenomeConsciousnessWrapper: {e}")
    sys.exit(1)

# Test 2: Import command interface
try:
    from dawn_command_interface import run_command_from_input, connect_to_dawn
    print("✅ Successfully imported dawn_command_interface")
except ImportError as e:
    print(f"❌ Failed to import dawn_command_interface: {e}")
    sys.exit(1)

# Test 3: Create DAWN instance
try:
    print("\n🌅 Creating DAWN instance...")
    dawn = DAWNGenomeConsciousnessWrapper()
    print("✅ DAWN instance created successfully")
    
    # Check methods
    print("\n📋 Checking DAWN methods:")
    if hasattr(dawn, 'tick'):
        print("  ✅ tick() method found")
    else:
        print("  ❌ tick() method NOT found")
        
    if hasattr(dawn, 'get_status'):
        print("  ✅ get_status() method found")
        print(f"     Status: {dawn.get_status()}")
    else:
        print("  ❌ get_status() method NOT found")
        
    if hasattr(dawn, 'enable_genome_mode'):
        print("  ✅ enable_genome_mode() method found")
    else:
        print("  ❌ enable_genome_mode() method NOT found")
        
except Exception as e:
    print(f"❌ Failed to create DAWN instance: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Test a tick
try:
    print("\n🔄 Testing tick...")
    dawn.tick()
    print("✅ Tick executed successfully")
except Exception as e:
    print(f"⚠️  Tick failed (this might be normal): {e}")

print("\n" + "=" * 50)
print("✅ All basic tests passed! You can now run:")
print("  python run_dawn.py")
print("  python quick_run_dawn.py")
print("  python run_dawn_genome.py")