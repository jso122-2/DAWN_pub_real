#!/usr/bin/env python3
"""
Test Entropy Visual Stream System
=================================

Test script to demonstrate the entropy visual stream system by simulating
different entropy and pressure states with varying mood pigments.
"""

import time
import random
from entropy_visual_stream import get_entropy_stream

def test_entropy_visual_stream():
    """Test the complete entropy visual stream system"""
    print("🌊 Testing DAWN Entropy Visual Stream System")
    print("=" * 60)
    
    stream = get_entropy_stream()
    
    # Start the stream if not already running
    if not stream.is_active:
        stream.start_stream()
        print("🚀 Started entropy visual stream")
    
    print("\n🎯 Testing entropy progression through all visual modes...")
    
    # Test progression through entropy levels
    entropy_tests = [
        {
            'entropy': 0.1,
            'pressure': 0.3,
            'mood': {'blue': 0.6, 'green': 0.3, 'violet': 0.1},
            'description': 'Deep calm - flowing mist (blue-green)',
            'expected_mode': 'flowing_mist'
        },
        {
            'entropy': 0.25,
            'pressure': 0.4,
            'mood': {'green': 0.5, 'blue': 0.3, 'yellow': 0.2},
            'description': 'Peaceful state - gentle mist flow',
            'expected_mode': 'flowing_mist'
        },
        {
            'entropy': 0.4,
            'pressure': 0.5,
            'mood': {'yellow': 0.4, 'orange': 0.3, 'green': 0.3},
            'description': 'Gentle activity - subtle waves begin',
            'expected_mode': 'subtle_waves'
        },
        {
            'entropy': 0.55,
            'pressure': 0.6,
            'mood': {'orange': 0.4, 'red': 0.3, 'yellow': 0.3},
            'description': 'Moderate tension - wave distortions',
            'expected_mode': 'subtle_waves'
        },
        {
            'entropy': 0.7,
            'pressure': 0.7,
            'mood': {'red': 0.5, 'orange': 0.4, 'yellow': 0.1},
            'description': 'High activity - sharp pulses start',
            'expected_mode': 'sharp_pulses'
        },
        {
            'entropy': 0.78,
            'pressure': 0.8,
            'mood': {'red': 0.6, 'orange': 0.3, 'violet': 0.1},
            'description': 'Stressed state - grid distortions',
            'expected_mode': 'sharp_pulses'
        },
        {
            'entropy': 0.88,
            'pressure': 0.9,
            'mood': {'yellow': 0.5, 'orange': 0.4, 'red': 0.1},
            'description': 'Critical state - fracture flicker begins',
            'expected_mode': 'fracture_flicker'
        },
        {
            'entropy': 0.95,
            'pressure': 0.95,
            'mood': {'yellow': 0.6, 'orange': 0.3, 'red': 0.1},
            'description': 'Maximum entropy - high-frequency flicker',
            'expected_mode': 'fracture_flicker'
        }
    ]
    
    for i, test in enumerate(entropy_tests, 1):
        print(f"\n🌊 {i}/{len(entropy_tests)}: {test['description']}")
        print(f"   Entropy: {test['entropy']:.2f}, Pressure: {test['pressure']:.2f}")
        print(f"   Mood pigment: {test['mood']}")
        print(f"   Expected mode: {test['expected_mode']}")
        
        # Update entropy visual
        stream.update_entropy_visual(
            test['entropy'],
            test['pressure'],
            test['mood']
        )
        
        # Show current state
        visual_state = stream.get_current_visual_state()
        if visual_state:
            actual_mode = visual_state['mode']
            intensity = visual_state['intensity']
            print(f"   ✓ Actual mode: {actual_mode}, Intensity: {intensity:.2f}")
            
            if actual_mode == test['expected_mode']:
                print(f"   ✅ Mode matches expected")
            else:
                print(f"   ⚠️ Mode mismatch - expected {test['expected_mode']}")
        
        # Wait between tests
        time.sleep(2)
    
    print(f"\n📊 System Status:")
    status = stream.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print(f"\n🎨 Testing mood pigment color modulation...")
    
    # Test different mood pigments at medium entropy
    test_entropy = 0.5
    test_pressure = 0.6
    
    pigment_tests = [
        {'red': 0.8, 'orange': 0.2, 'description': 'Fiery red-orange'},
        {'blue': 0.7, 'violet': 0.3, 'description': 'Cool blue-violet'},
        {'green': 0.6, 'yellow': 0.4, 'description': 'Natural green-yellow'},
        {'violet': 0.5, 'blue': 0.3, 'orange': 0.2, 'description': 'Mystical purple blend'},
        {'yellow': 0.4, 'red': 0.3, 'blue': 0.3, 'description': 'Balanced warm-cool'}
    ]
    
    for i, pigment in enumerate(pigment_tests, 1):
        description = pigment.pop('description')
        print(f"\n🎨 Pigment test {i}: {description}")
        print(f"   Pigment: {pigment}")
        
        stream.update_entropy_visual(test_entropy, test_pressure, pigment)
        
        visual_state = stream.get_current_visual_state()
        if visual_state and 'colors' in visual_state:
            colors = visual_state['colors']
            print(f"   Generated colors: {colors}")
        
        time.sleep(1.5)
    
    print(f"\n⚡ Testing rapid entropy changes...")
    
    # Test rapid entropy fluctuations
    for i in range(10):
        entropy = random.uniform(0.1, 0.95)
        pressure = random.uniform(0.3, 0.9)
        
        # Random mood pigment
        pigment_weights = [random.uniform(0, 1) for _ in range(6)]
        total = sum(pigment_weights)
        normalized = [w/total for w in pigment_weights]
        
        mood_pigment = {
            'red': normalized[0],
            'orange': normalized[1], 
            'yellow': normalized[2],
            'green': normalized[3],
            'blue': normalized[4],
            'violet': normalized[5]
        }
        
        stream.update_entropy_visual(entropy, pressure, mood_pigment)
        
        if i % 3 == 0:
            status = stream.get_current_visual_state()
            if status:
                print(f"   Rapid update {i+1}: entropy={entropy:.2f}, mode={status['mode']}, intensity={status['intensity']:.2f}")
        
        time.sleep(0.3)
    
    print(f"\n🌊 Testing continuous monitoring for 15 seconds...")
    
    start_time = time.time()
    update_count = 0
    
    while time.time() - start_time < 15:
        # Simulate gradual entropy changes
        elapsed = time.time() - start_time
        entropy_wave = 0.5 + 0.4 * math.sin(elapsed * 0.5)  # Sine wave 0.1-0.9
        pressure_wave = 0.6 + 0.3 * math.cos(elapsed * 0.3)  # Cosine wave 0.3-0.9
        
        # Slowly shifting mood
        mood_shift = elapsed / 15.0  # 0 to 1 over 15 seconds
        mood_pigment = {
            'blue': 0.5 - mood_shift * 0.3,
            'green': 0.3,
            'red': mood_shift * 0.4,
            'yellow': 0.2 + mood_shift * 0.2
        }
        
        stream.update_entropy_visual(entropy_wave, pressure_wave, mood_pigment)
        update_count += 1
        
        if update_count % 5 == 0:
            current_state = stream.get_current_visual_state()
            if current_state:
                print(f"   [{elapsed:5.1f}s] entropy={entropy_wave:.2f}, mode={current_state['mode']}, intensity={current_state['intensity']:.2f}")
        
        time.sleep(0.2)
    
    print(f"\n📈 Continuous monitoring complete!")
    print(f"   Total updates: {update_count}")
    print(f"   Average update rate: {update_count/15:.1f} Hz")
    
    final_status = stream.get_system_status()
    print(f"\n📊 Final System Status:")
    for key, value in final_status.items():
        print(f"   {key}: {value}")
    
    print(f"\n🎉 Entropy visual stream test complete!")
    print(f"🌐 Check your DAWN GUI at http://localhost:8080 to see the entropy background animations!")

def test_entropy_visualization_modes():
    """Test specific visualization mode behaviors"""
    print("\n🎭 Testing specific visualization mode behaviors...")
    
    stream = get_entropy_stream()
    
    mode_tests = [
        {
            'name': 'Flowing Mist - Horizontal Drift',
            'entropy': 0.15,
            'pressure': 0.3,
            'mood': {'blue': 0.6, 'green': 0.4},
            'duration': 5
        },
        {
            'name': 'Subtle Waves - Vibration',
            'entropy': 0.45,
            'pressure': 0.6,
            'mood': {'orange': 0.5, 'yellow': 0.3, 'green': 0.2},
            'duration': 4
        },
        {
            'name': 'Sharp Pulses - Grid Distortion',
            'entropy': 0.75,
            'pressure': 0.8,
            'mood': {'red': 0.6, 'orange': 0.4},
            'duration': 3
        },
        {
            'name': 'Fracture Flicker - High Frequency',
            'entropy': 0.92,
            'pressure': 0.95,
            'mood': {'yellow': 0.7, 'orange': 0.3},
            'duration': 2
        }
    ]
    
    for test in mode_tests:
        print(f"\n🎭 {test['name']}")
        
        stream.update_entropy_visual(
            test['entropy'],
            test['pressure'], 
            test['mood']
        )
        
        state = stream.get_current_visual_state()
        if state:
            print(f"   Mode: {state['mode']}")
            print(f"   Intensity: {state['intensity']:.2f}")
            print(f"   Colors: {state.get('colors', 'N/A')}")
            print(f"   Animation duration: {state.get('animation_duration', 'N/A')}s")
        
        print(f"   Running for {test['duration']} seconds...")
        time.sleep(test['duration'])

if __name__ == "__main__":
    try:
        # Import math for the continuous monitoring test
        import math
        
        test_entropy_visual_stream()
        test_entropy_visualization_modes()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc() 