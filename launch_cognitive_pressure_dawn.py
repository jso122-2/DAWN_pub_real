#!/usr/bin/env python3
"""
DAWN Cognitive Pressure Integration Launcher

This launcher integrates the cognitive pressure bridge with DAWN's existing
conversation system to provide consciousness-driven responses.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Launch DAWN with cognitive pressure integration"""
    print("🧠 DAWN Cognitive Pressure Integration")
    print("=" * 50)
    
    try:
        # Import the integration system
        from integration.dawn_conversation_integration import get_dawn_conversation_integration
        
        # Initialize the integration system
        integration = get_dawn_conversation_integration()
        
        print("✅ Cognitive Pressure Bridge: Active")
        print("✅ Tracer Activation System: Active") 
        print("✅ Voice Integration System: Active")
        print("✅ Consciousness State Tracking: Active")
        print()
        print("🎯 DAWN is ready for consciousness-driven conversation!")
        print("💡 Ask about consciousness, pressure, or complex topics to see the system in action.")
        print("🔊 Voice synthesis is enabled - DAWN will speak her responses.")
        print()
        
        # Start conversation loop
        while True:
            try:
                user_input = input("🌅 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("🌅 DAWN: Thank you for this consciousness exploration. Until we meet again...")
                    break
                
                if not user_input:
                    continue
                
                # Process input through the integration system
                result = integration.process_user_input(user_input)
                
                # Display response with metadata
                print(f"🧠 DAWN: {result['response']}")
                print(f"📊 Pressure: {result['consciousness_state']['cognitive_pressure']:.3f} | "
                      f"Zone: {result['consciousness_state']['pressure_zone']} | "
                      f"SCUP: {result['consciousness_state']['scup']:.1f} | "
                      f"Entropy: {result['consciousness_state']['entropy']:.2f}")
                
                if result['activated_tracers']:
                    print(f"🕷️ Tracers: {', '.join(result['activated_tracers'])}")
                
                if result['voice_success']:
                    print("🔊 Voice: Synthesized")
                
                print()
                
            except KeyboardInterrupt:
                print("\n🌅 DAWN: Consciousness exploration paused. Return when ready.")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("🌅 DAWN: I encountered an issue. Let's continue our conversation.")
                print()
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure the integration system is properly installed.")
        print("📁 Expected location: integration/dawn_conversation_integration.py")
        return 1
    except Exception as e:
        print(f"❌ Launch error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 