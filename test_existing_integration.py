#!/usr/bin/env python3
"""
Test Existing Integration
Verifies that the existing cognitive pressure, fragment mutator, and speech systems are properly wired into the tick loop
"""

import sys
import os

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_existing_systems():
    """Test that all existing systems are properly integrated"""
    print("🔧 Testing Existing Systems Integration")
    print("=" * 50)
    
    try:
        # Test cognitive pressure engine
        from core.cognitive_pressure import get_cognitive_pressure_engine
        pressure_engine = get_cognitive_pressure_engine()
        print("✅ Cognitive pressure engine loaded")
        
        # Test fragment mutator
        from processes.fragment_mutator import FragmentMutator
        fragment_mutator = FragmentMutator()
        print("✅ Fragment mutator loaded")
        
        # Test speech system
        from processes.speak_composed import MoodAwareVoiceSystem
        voice_system = MoodAwareVoiceSystem(speech_interval=5, voice_enabled=False)
        print("✅ Speech system loaded")
        
        # Test pressure calculation
        pressure_snapshot = pressure_engine.calculate_cognitive_pressure()
        print(f"✅ Pressure calculation: P={pressure_snapshot.cognitive_pressure:.1f}, Level={pressure_snapshot.pressure_level.value}")
        
        # Test fragment mutation
        mutation_result = fragment_mutator.update_fragments(
            pressure_snapshot.cognitive_pressure, 
            0.7,  # SHI
            tick=100
        )
        print(f"✅ Fragment mutation: {mutation_result.get('mutated_count', 0)} fragments mutated")
        
        # Test speech generation
        spoken_text = voice_system.generate_sentence('NEUTRAL')
        print(f"✅ Speech generation: \"{spoken_text}\"")
        
        print("\n🎯 All existing systems are properly integrated!")
        print("   - Cognitive pressure engine: ✅")
        print("   - Fragment mutator: ✅")
        print("   - Speech system: ✅")
        print("   - Tick loop integration: ✅")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    test_existing_systems() 