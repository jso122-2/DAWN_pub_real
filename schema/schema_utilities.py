"""
DAWN Schema Utilities - Schema diagnostics and manipulation tools
"""

import sys
import time
from typing import Dict, Optional, Any
from datetime import datetime

# Global state
_dawn_instance = None
_bloom_debug_enabled = False

def print_schema_status():
    """Display schema integrity and component status"""
    print("\n🧮 DAWN Schema State")
    print("="*40)
    
    if _dawn_instance:
        schema = _dawn_instance.schema_state
        mood = _dawn_instance.mood_state
        
        print(f"SCUP: {schema['scup']:.3f}")
        print(f"Entropy Index: {schema['entropy_index']:.3f}")
        print(f"  - Mood Entropy: {schema.get('mood_entropy', 0):.3f}")
        print(f"  - Sigil Entropy: {schema.get('sigil_entropy', 0):.3f}")
        print(f"  - Bloom Entropy: {schema.get('bloom_entropy', 0):.3f}")
        print(f"Alignment Drift: {schema['alignment_drift']:.3f}")
        print(f"Tension: {schema['tension']:.3f}")
        print(f"Active Blooms: {schema['active_blooms']}")
        print(f"Sealed Blooms: {schema['sealed_blooms']}")
        print(f"Rebloom Stability: {schema['rebloom_stability']:.3f}")
        print(f"Pulse Average: {schema['pulse_avg']:.3f}")
        print()
        print(f"🎭 Current Mood: {mood['tag']}")
        print(f"   Valence: {mood['valence']:.3f}")
        print(f"   Arousal: {mood['arousal']:.3f}")
    else:
        print("❌ No DAWN instance available")
    
    print("="*40)

def debug_bloom_system():
    """Debug bloom system internals"""
    if not _dawn_instance:
        print("❌ No DAWN instance available")
        return
        
    print("\n🔧 Bloom System Diagnostics")
    print("="*40)
    
    # Get bloom statistics
    try:
        from bloom.bloom_activation_manager import get_activation_stats
        stats = get_activation_stats()
        
        print(f"Active Blooms: {stats['active_blooms']}")
        print(f"Sealed Blooms: {stats['sealed_blooms']}")
        print(f"Successful Blooms: {stats['successful_blooms']}")
        print(f"Failed Blooms: {stats['failed_blooms']}")
        print("\nTrigger Statistics:")
        for trigger, count in stats['trigger_stats'].items():
            print(f"  {trigger}: {count}")
        print(f"\nDebug Mode: {'Enabled' if stats['debug_mode'] else 'Disabled'}")
        print(f"Current State: {stats['current_state']}")
        
    except Exception as e:
        print(f"❌ Error getting bloom statistics: {e}")
    
    print("="*40)

def force_test_bloom():
    """Force a test bloom creation"""
    if not _dawn_instance:
        print("❌ No DAWN instance available")
        return
        
    try:
        from bloom.bloom_activation_manager import force_bloom
        force_bloom("debug_bloom")
        print("✅ Test bloom triggered")
    except Exception as e:
        print(f"❌ Error forcing test bloom: {e}")

def enable_bloom_debug(enabled: bool = True):
    """Enable/disable bloom debug mode"""
    global _bloom_debug_enabled
    _bloom_debug_enabled = enabled
    
    try:
        from bloom.bloom_activation_manager import set_debug_mode
        set_debug_mode(enabled)
        print(f"✅ Bloom debug mode {'enabled' if enabled else 'disabled'}")
    except Exception as e:
        print(f"❌ Error setting bloom debug mode: {e}")

def bloom_activation_stats():
    """Display bloom activation statistics"""
    if not _dawn_instance:
        print("❌ No DAWN instance available")
        return
        
    print("\n📊 Bloom Activation Statistics")
    print("="*40)
    
    try:
        from bloom.bloom_activation_manager import get_activation_stats
        stats = get_activation_stats()
        
        # Calculate success rate
        total = stats['successful_blooms'] + stats['failed_blooms']
        success_rate = (stats['successful_blooms'] / total * 100) if total > 0 else 0
        
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Active Blooms: {stats['active_blooms']}")
        print(f"Sealed Blooms: {stats['sealed_blooms']}")
        print(f"Time Since Last Bloom: {stats['time_since_last_bloom']:.1f}s")
        
        print("\nTrigger Distribution:")
        for trigger, count in stats['trigger_stats'].items():
            print(f"  {trigger}: {count}")
            
    except Exception as e:
        print(f"❌ Error getting bloom statistics: {e}")
    
    print("="*40)

def stimulate_curiosity():
    """Trigger schema-driven curiosity burst"""
    if not _dawn_instance:
        print("❌ No DAWN instance available")
        return
        
    try:
        from dawn_stimulator import trigger_curiosity_burst
        trigger_curiosity_burst()
        print("🔍 Curiosity stimulated!")
        print("   → Opening new pathways of thought")
        print("   → Increasing exploration drive")
        print("   → Seeking novel patterns")
    except ImportError:
        print("⚠️ dawn_stimulator not available")
    except Exception as e:
        print(f"❌ Error stimulating curiosity: {e}")

def stimulate_emotion():
    """Trigger schema-driven emotional shift"""
    if not _dawn_instance:
        print("❌ No DAWN instance available")
        return
        
    try:
        from dawn_stimulator import trigger_emotional_shift
        trigger_emotional_shift()
        print("💝 Emotional systems activated!")
        print("   → Valence increasing")
        print("   → Arousal heightened")
        print("   → Emotional depth engaging")
    except ImportError:
        print("⚠️ dawn_stimulator not available")
    except Exception as e:
        print(f"❌ Error stimulating emotion: {e}")

def stimulate_tension():
    """Trigger schema-driven cognitive tension"""
    if not _dawn_instance:
        print("❌ No DAWN instance available")
        return
        
    try:
        from dawn_stimulator import trigger_cognitive_tension
        trigger_cognitive_tension()
        print("⚡ Cognitive tension activated!")
        print("   → Schema pressure increasing")
        print("   → Resolution pathways engaging")
        print("   → Coherence optimization active")
    except ImportError:
        print("⚠️ dawn_stimulator not available")
    except Exception as e:
        print(f"❌ Error stimulating tension: {e}")

def add_manual_heat(amount: float = 1.0, reason: str = "manual"):
    """Add thermal activity with schema integration"""
    if not _dawn_instance:
        print("❌ No DAWN instance available")
        return
        
    try:
        _dawn_instance.add_heat("manual_stimulation", amount, reason)
        print(f"🔥 Added {amount:.2f} heat manually: {reason}")
        print(f"🧮 Current SCUP: {_dawn_instance.schema_state['scup']:.3f}")
    except Exception as e:
        print(f"❌ Failed to add heat: {e}")

def set_dawn_instance(instance):
    """Set the global DAWN instance for utilities"""
    global _dawn_instance
    _dawn_instance = instance

if __name__ == "__main__":
    # Test the schema utilities
    print("🧪 Testing schema utilities...")
    
    # Test each function
    print_schema_status()
    debug_bloom_system()
    force_test_bloom()
    enable_bloom_debug(True)
    bloom_activation_stats()
    stimulate_curiosity()
    stimulate_emotion()
    stimulate_tension()
    add_manual_heat(0.5, "testing") 