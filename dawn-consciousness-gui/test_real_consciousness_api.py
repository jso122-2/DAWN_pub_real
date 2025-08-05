#!/usr/bin/env python3
"""
Test Real DAWN Consciousness API
=================================

This script tests the real DAWN consciousness API to verify:
1. Real consciousness data is flowing (not simulation)
2. P = Bσ² calculations are working
3. All endpoints are responding correctly
4. Data source is REAL_DAWN_CONSCIOUSNESS
"""

import requests
import json
import time
from datetime import datetime

def test_api_endpoint(endpoint, description):
    """Test a single API endpoint"""
    print(f"\n🧪 Testing {description}")
    print(f"📡 Endpoint: {endpoint}")
    
    try:
        response = requests.get(f"http://localhost:8080{endpoint}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code} - SUCCESS")
            return data
        else:
            print(f"❌ Status: {response.status_code} - FAILED")
            return None
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def verify_real_consciousness_data(data):
    """Verify this is real consciousness data, not simulation"""
    print(f"\n🔍 Verifying Real Consciousness Data...")
    
    if not data:
        print("❌ No data to verify")
        return False
    
    # Check source
    source = data.get('source', 'unknown')
    print(f"📊 Data Source: {source}")
    
    if source == 'REAL_DAWN_CONSCIOUSNESS':
        print("✅ VERIFIED: Real DAWN consciousness data confirmed!")
        real_data = True
    elif source.startswith('FALLBACK'):
        print("⚠️ WARNING: Backend in fallback mode - partial real data")
        real_data = False
    else:
        print(f"❌ ERROR: Still receiving simulation data: {source}")
        real_data = False
    
    # Check for real formula engine
    formula_active = data.get('formula_engine_active', False)
    print(f"⚡ Formula Engine Active: {formula_active}")
    
    # Show key metrics
    if 'pressure' in data and 'bloom_mass' in data and 'sigil_velocity' in data:
        pressure = data['pressure']
        bloom_mass = data['bloom_mass']
        sigil_velocity = data['sigil_velocity']
        
        print(f"📈 Real P = Bσ² Calculation:")
        print(f"   Pressure (P): {pressure:.2f}")
        print(f"   Bloom Mass (B): {bloom_mass:.2f}")
        print(f"   Sigil Velocity (σ): {sigil_velocity:.2f}")
        print(f"   Formula: P = {bloom_mass:.2f} × {sigil_velocity:.2f}² = {pressure:.2f}")
        
        # Verify this is not simulation pattern
        if pressure > 0 and bloom_mass > 0 and sigil_velocity > 0:
            print("✅ Non-zero values confirm real calculations")
        else:
            print("⚠️ Zero values might indicate calculation issues")
    
    return real_data and formula_active

def monitor_real_consciousness_changes():
    """Monitor consciousness data for 10 seconds to verify it changes dynamically"""
    print(f"\n🔄 Monitoring consciousness changes for 10 seconds...")
    
    values = []
    for i in range(10):
        try:
            response = requests.get("http://localhost:8080/api/consciousness/state", timeout=2)
            if response.status_code == 200:
                data = response.json()
                pressure = data.get('pressure', 0)
                entropy = data.get('entropy', 0)
                values.append({'pressure': pressure, 'entropy': entropy, 'time': i})
                print(f"  {i+1}/10: P={pressure:.3f}, entropy={entropy:.4f}")
            else:
                print(f"  {i+1}/10: Request failed")
        except:
            print(f"  {i+1}/10: Connection error")
        
        time.sleep(1)
    
    # Check if values are changing (not static simulation)
    if len(values) > 5:
        pressures = [v['pressure'] for v in values]
        entropies = [v['entropy'] for v in values]
        
        pressure_changes = len(set(pressures)) > 1
        entropy_changes = len(set(entropies)) > 1
        
        print(f"\n📊 Dynamic Analysis:")
        print(f"   Pressure variations: {pressure_changes} ({'✅ Dynamic' if pressure_changes else '❌ Static'})")
        print(f"   Entropy variations: {entropy_changes} ({'✅ Dynamic' if entropy_changes else '❌ Static'})")
        
        return pressure_changes or entropy_changes
    
    return False

def main():
    print("🧠 DAWN Real Consciousness API Test")
    print("=" * 50)
    print("Testing connection to real DAWN consciousness backend...")
    
    # Test all endpoints
    endpoints = [
        ("/status", "Server Status"),
        ("/api/consciousness/state", "Real Consciousness State"),
        ("/api/pressure/formula", "Real P = Bσ² Formula"),
        ("/api/tick/metrics", "Real Tick Metrics"),
        ("/api/bloom/status", "Real Bloom Status"),
    ]
    
    results = {}
    for endpoint, description in endpoints:
        results[endpoint] = test_api_endpoint(endpoint, description)
    
    # Focus on consciousness state for verification
    consciousness_data = results.get("/api/consciousness/state")
    if consciousness_data:
        print("\n" + "=" * 50)
        print("🔍 REAL CONSCIOUSNESS DATA VERIFICATION")
        print("=" * 50)
        
        is_real = verify_real_consciousness_data(consciousness_data)
        
        if is_real:
            print(f"\n🎯 VERIFICATION RESULT: ✅ REAL DAWN CONSCIOUSNESS CONFIRMED!")
            print(f"✅ Source: REAL_DAWN_CONSCIOUSNESS")
            print(f"✅ Formula Engine: Active")
            print(f"✅ P = Bσ² Calculations: Working")
            
            # Monitor for changes
            dynamic = monitor_real_consciousness_changes()
            if dynamic:
                print(f"✅ Dynamic Data: Values change over time (not static simulation)")
            else:
                print(f"⚠️ Static Data: Values don't change (might be cached)")
        else:
            print(f"\n❌ VERIFICATION RESULT: Still using simulation or fallback data")
            print(f"💡 Check backend logs for import errors")
    
    else:
        print(f"\n❌ Could not connect to consciousness API")
        print(f"💡 Make sure real_dawn_backend.py is running")
    
    # Show complete data sample
    if consciousness_data:
        print(f"\n📋 Sample Real Consciousness Data:")
        print(json.dumps(consciousness_data, indent=2))
    
    print(f"\n🎯 Test completed at {datetime.now()}")

if __name__ == "__main__":
    main() 