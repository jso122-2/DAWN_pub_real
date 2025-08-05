#!/usr/bin/env python3
"""
Test Sigil Overlay System
==========================

Test script to demonstrate the sigil overlay visual system by triggering
various sigil executions with different parameters and visual effects.
"""

import time
import random
from sigil_overlay_renderer import get_sigil_renderer

def test_sigil_overlay_system():
    """Test the complete sigil overlay system"""
    print("🔮 Testing DAWN Sigil Overlay System")
    print("=" * 50)
    
    renderer = get_sigil_renderer()
    
    # Start the renderer if not already running
    if not renderer.is_active:
        renderer.start_rendering()
        print("🚀 Started sigil renderer")
    
    print("\n🎯 Testing individual sigil types...")
    
    # Test sequence of different sigil types
    test_sigils = [
        {
            'sigil_id': 'DEEP_FOCUS',
            'entropy': 0.4,
            'saturation': 0.6,
            'execution_power': 1.2,
            'description': 'Deep focus meditation sigil'
        },
        {
            'sigil_id': 'STABILIZE_PROTOCOL', 
            'entropy': 0.8,
            'saturation': 0.4,
            'execution_power': 0.9,
            'description': 'System stabilization protocol'
        },
        {
            'sigil_id': 'EMERGENCY_STABILIZE',
            'entropy': 0.9,
            'saturation': 0.8,
            'execution_power': 1.8,
            'description': 'Emergency stabilization with high intensity'
        },
        {
            'sigil_id': 'THERMAL_STABILIZE',
            'entropy': 0.3,
            'saturation': 0.7,
            'execution_power': 1.1,
            'description': 'Thermal cooling wave pattern'
        },
        {
            'sigil_id': 'REBLOOM',
            'entropy': 0.6,
            'saturation': 0.9,
            'execution_power': 1.3,
            'description': 'Memory rebloom with halo effect'
        },
        {
            'sigil_id': 'CONSCIOUSNESS_PROBE',
            'entropy': 0.5,
            'saturation': 0.3,
            'execution_power': 1.0,
            'description': 'Consciousness probe in ethereal motion'
        },
        {
            'sigil_id': 'ENTROPY_INJECTION',
            'entropy': 0.7,
            'saturation': 0.6,
            'execution_power': 1.4,
            'description': 'Entropy injection with particle effects'
        }
    ]
    
    for i, sigil in enumerate(test_sigils, 1):
        print(f"\n🔮 {i}/{len(test_sigils)}: {sigil['description']}")
        print(f"   ID: {sigil['sigil_id']}")
        print(f"   Entropy: {sigil['entropy']:.1f}, Saturation: {sigil['saturation']:.1f}, Power: {sigil['execution_power']:.1f}")
        
        # Execute the sigil
        renderer.execute_sigil_overlay(
            sigil['sigil_id'],
            sigil['entropy'],
            sigil['saturation'],
            sigil['execution_power']
        )
        
        # Show current system status
        status = renderer.get_system_status()
        print(f"   Active overlays: {status['active_overlay_count']}")
        
        # Wait between sigils
        time.sleep(1.5)
    
    print(f"\n⏳ Letting sigils run for 8 seconds...")
    time.sleep(8)
    
    print("\n🎭 Testing concurrent sigil execution...")
    
    # Execute multiple sigils simultaneously
    concurrent_sigils = [
        ('DEEP_FOCUS', 0.5, 0.8, 1.0),
        ('STABILIZE_PROTOCOL', 0.7, 0.4, 1.2),
        ('REBLOOM', 0.4, 0.9, 1.1)
    ]
    
    for sigil_id, entropy, saturation, power in concurrent_sigils:
        renderer.execute_sigil_overlay(sigil_id, entropy, saturation, power)
        print(f"🔮 Executed concurrent sigil: {sigil_id}")
        time.sleep(0.2)
    
    print(f"\n📊 System Status:")
    status = renderer.get_system_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print(f"\n📋 Recent Visual Log:")
    visual_log = renderer.get_visual_log(5)
    for entry in visual_log[-5:]:
        timestamp = time.strftime('%H:%M:%S', time.localtime(entry['timestamp']))
        print(f"   [{timestamp}] {entry['sigil_id']} - {entry['glyph_symbol']} ({entry['motion_style']})")
    
    print(f"\n⏳ Running concurrent sigils for 10 seconds...")
    start_time = time.time()
    
    while time.time() - start_time < 10:
        # Show active overlays
        active = renderer.get_active_overlays()
        if active:
            print(f"\r   Active: {len(active)} overlays", end="", flush=True)
        time.sleep(1)
    
    print(f"\n\n🧪 Testing entropy persistence...")
    
    # Test high-entropy persistent sigil
    renderer.execute_sigil_overlay('DEEP_FOCUS', entropy=0.85, saturation=0.6, execution_power=1.5)
    print(f"🔮 Executed high-entropy DEEP_FOCUS (should persist longer)")
    
    print(f"\n⏳ Monitoring persistence for 15 seconds...")
    for i in range(15):
        active = renderer.get_active_overlays()
        active_count = len(active)
        persistent_overlays = [o for o in active if o['entropy'] > 0.7]
        print(f"   [{i+1:2d}s] Active: {active_count}, Persistent: {len(persistent_overlays)}")
        time.sleep(1)
    
    print(f"\n🧹 Testing overlay clearing...")
    renderer.clear_all_overlays()
    
    final_status = renderer.get_system_status()
    print(f"📊 Final active overlays: {final_status['active_overlay_count']}")
    
    print(f"\n🎉 Sigil overlay system test complete!")
    print(f"📈 Total sigil types available: {final_status['total_sigil_types']}")
    print(f"📋 Visual log entries: {final_status['visual_log_entries']}")
    print(f"🌐 Check your DAWN GUI at http://localhost:8080 to see the sigil overlays!")

def test_custom_sigil():
    """Test adding and using a custom sigil"""
    print("\n🛠️ Testing custom sigil creation...")
    
    renderer = get_sigil_renderer()
    
    # Add a custom sigil
    custom_config = {
        'glyph_symbol': '🌌',
        'motion_style': 'ethereal',
        'position': 'center',
        'base_color': '#ff6b9d',
        'accent_color': '#ffa8cc',
        'size_factor': 1.8,
        'duration': 5.0,
        'intensity_multiplier': 1.5,
        'entropy_persistence_threshold': 0.6,
        'saturation_halo_threshold': 0.4
    }
    
    renderer.add_custom_sigil('COSMIC_TRANSCENDENCE', custom_config)
    print("✅ Added custom sigil: COSMIC_TRANSCENDENCE")
    
    # Execute the custom sigil
    renderer.execute_sigil_overlay('COSMIC_TRANSCENDENCE', entropy=0.75, saturation=0.8, execution_power=2.0)
    print("🌌 Executed COSMIC_TRANSCENDENCE sigil")
    
    time.sleep(3)
    
    active = renderer.get_active_overlays()
    cosmic_sigils = [o for o in active if o['sigil_id'] == 'COSMIC_TRANSCENDENCE']
    print(f"🔍 Found {len(cosmic_sigils)} active cosmic transcendence sigils")

def test_stress_test():
    """Test system under high sigil load"""
    print("\n⚡ Running stress test...")
    
    renderer = get_sigil_renderer()
    
    # Execute many sigils rapidly
    sigil_types = ['DEEP_FOCUS', 'STABILIZE_PROTOCOL', 'REBLOOM', 'THERMAL_STABILIZE']
    
    for i in range(20):
        sigil_type = random.choice(sigil_types)
        entropy = random.uniform(0.2, 0.9)
        saturation = random.uniform(0.3, 0.9)
        power = random.uniform(0.8, 1.5)
        
        renderer.execute_sigil_overlay(sigil_type, entropy, saturation, power)
        
        if i % 5 == 0:
            status = renderer.get_system_status()
            print(f"   Executed {i+1}/20 sigils, active: {status['active_overlay_count']}")
        
        time.sleep(0.1)
    
    print("⚡ Stress test complete - system should handle concurrent overlays gracefully")

if __name__ == "__main__":
    try:
        test_sigil_overlay_system()
        test_custom_sigil()
        test_stress_test()
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc() 