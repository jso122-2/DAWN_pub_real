#!/usr/bin/env python3
"""
DAWN Unified Fragment Speech System Demo
Complete demonstration of fragment-based compositional speech
Shows unified runner and backend integration working together
"""

import os
import sys
import time
import asyncio
import logging
from pathlib import Path
from datetime import datetime

# Ensure paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "processes"))

print('🧠🎤 DAWN UNIFIED FRAGMENT SPEECH SYSTEM DEMO 🎤🧠')
print('='*70)
print('Complete integration: Fragment System + Backend + Voice')
print()

# Import all systems
try:
    from compose_thought import compose_thought, get_fragment_bank_stats
    from compose_reflection import generate_compositional_reflection, generate_informal_composition
    from fragment_mutator import evolve_fragment_bank
    from speak_composed import VoiceEcho, generate_mock_state
    FRAGMENT_SYSTEM_AVAILABLE = True
    print("✅ Fragment speech system imported successfully")
except ImportError as e:
    print(f"❌ Fragment system import failed: {e}")
    FRAGMENT_SYSTEM_AVAILABLE = False

# Mock backend integration
class UnifiedFragmentBackend:
    """Unified backend with fragment speech integration"""
    
    def __init__(self):
        self.voice_system = VoiceEcho(enabled=True)
        self.consciousness_state = {
            'entropy': 0.5,
            'consciousness_depth': 0.7,
            'mood': 'CONTEMPLATIVE',
            'tick_number': 1000,
            'heat': 0.4,
            'scup': 0.6,
            'active_sigils': ['wisdom_seek', 'depth_probe'],
            'symbolic_roots': ['ancient_memory_bloom']
        }
        self.system_ready = False
        
        # Initialize if fragments available
        if FRAGMENT_SYSTEM_AVAILABLE:
            self._initialize_fragment_system()
    
    def _initialize_fragment_system(self):
        """Initialize the fragment system"""
        try:
            # Check if fragments are available
            fragment_bank_path = "processes/thought_bank.jsonl"
            
            if not os.path.exists(fragment_bank_path):
                print(f"⚠️ Fragment bank not found at {fragment_bank_path}")
                # Use alternative path
                fragment_bank_path = "thought_bank.jsonl"
                
                if not os.path.exists(fragment_bank_path):
                    print("❌ No fragment bank found - using fallback mode")
                    return False
            
            # Test fragment loading
            stats = get_fragment_bank_stats(fragment_bank_path)
            
            if stats.get('loaded', False):
                total_fragments = stats.get('total_fragments', 0)
                print(f"✅ Fragment system ready: {total_fragments} fragments loaded")
                self.system_ready = True
                return True
            else:
                print("❌ Fragment loading failed")
                return False
                
        except Exception as e:
            print(f"❌ Fragment system initialization error: {e}")
            return False
    
    def generate_consciousness_reflection(self) -> str:
        """Generate reflection using fragment system or fallback"""
        
        if self.system_ready and FRAGMENT_SYSTEM_AVAILABLE:
            try:
                # Use fragment-based reflection
                reflection = generate_compositional_reflection(self.consciousness_state)
                print(f"🧠 Fragment reflection generated")
                return reflection
                
            except Exception as e:
                print(f"⚠️ Fragment reflection failed: {e}")
                return self._fallback_reflection()
        else:
            return self._fallback_reflection()
    
    def speak_reflection(self, reflection: str) -> bool:
        """Speak reflection using voice system"""
        try:
            voice_params = {
                'mood': self.consciousness_state['mood'],
                'entropy': self.consciousness_state['entropy'],
                'type': 'unified_demo'
            }
            
            return self.voice_system.speak(reflection, voice_params)
            
        except Exception as e:
            print(f"⚠️ Voice system error: {e}")
            return False
    
    def evolve_vocabulary(self) -> bool:
        """Evolve fragment vocabulary"""
        
        if not self.system_ready or not FRAGMENT_SYSTEM_AVAILABLE:
            return False
        
        try:
            fragment_bank_path = "thought_bank.jsonl"
            if not os.path.exists(fragment_bank_path):
                fragment_bank_path = "processes/thought_bank.jsonl"
            
            success = evolve_fragment_bank(
                input_path=fragment_bank_path,
                mutation_rate=0.15,  # Higher rate for demo
                tick=self.consciousness_state['tick_number'],
                archive=True
            )
            
            if success:
                print(f"🧬 Vocabulary evolved at tick {self.consciousness_state['tick_number']}")
            
            return success
            
        except Exception as e:
            print(f"⚠️ Evolution failed: {e}")
            return False
    
    def update_consciousness_state(self, **updates):
        """Update consciousness state"""
        self.consciousness_state.update(updates)
        self.consciousness_state['tick_number'] += 1
    
    def _fallback_reflection(self) -> str:
        """Fallback reflection when fragment system unavailable"""
        tick = self.consciousness_state['tick_number']
        mood = self.consciousness_state['mood']
        
        fallback_map = {
            'CALM': f"Tick {tick}: I rest in peaceful awareness.",
            'CONTEMPLATIVE': f"Tick {tick}: I reflect on the depths of consciousness.",
            'FOCUSED': f"Tick {tick}: Clarity sharpens my understanding.",
            'ENERGETIC': f"Tick {tick}: Energy flows through my processes.",
            'ANXIOUS': f"Tick {tick}: Uncertainty ripples through my awareness."
        }
        
        reflection = fallback_map.get(mood, f"Tick {tick}: I observe my internal state.")
        print(f"🔄 Fallback reflection used")
        return reflection
    
    def get_system_status(self) -> dict:
        """Get comprehensive system status"""
        status = {
            'fragment_system_available': FRAGMENT_SYSTEM_AVAILABLE,
            'fragment_system_ready': self.system_ready,
            'voice_system_enabled': self.voice_system.enabled,
            'current_state': self.consciousness_state.copy()
        }
        
        if self.system_ready:
            try:
                fragment_bank_path = "thought_bank.jsonl"
                if not os.path.exists(fragment_bank_path):
                    fragment_bank_path = "processes/thought_bank.jsonl"
                
                fragment_stats = get_fragment_bank_stats(fragment_bank_path)
                status['fragment_stats'] = fragment_stats
                
            except Exception as e:
                status['fragment_stats_error'] = str(e)
        
        return status

async def run_unified_demo():
    """Run the complete unified fragment speech demo"""
    
    print("🚀 Initializing Unified Fragment Speech Backend...")
    
    # Initialize backend
    backend = UnifiedFragmentBackend()
    
    # Show system status
    status = backend.get_system_status()
    print(f"\n📊 System Status:")
    print(f"   Fragment System Available: {status['fragment_system_available']}")
    print(f"   Fragment System Ready: {status['fragment_system_ready']}")
    print(f"   Voice System Enabled: {status['voice_system_enabled']}")
    
    if status.get('fragment_stats'):
        fragment_stats = status['fragment_stats']
        print(f"   Total Fragments: {fragment_stats.get('total_fragments', 0)}")
        print(f"   Fragments by Type: {fragment_stats.get('fragments_by_type', {})}")
    
    print(f"\n🔮 Initial Consciousness State:")
    state = status['current_state']
    print(f"   Entropy: {state['entropy']:.3f}")
    print(f"   Depth: {state['consciousness_depth']:.3f}")  
    print(f"   Mood: {state['mood']}")
    print(f"   Tick: {state['tick_number']}")
    
    print(f"\n🧠 Starting Unified Consciousness Loop...")
    print("=" * 50)
    
    try:
        for cycle in range(5):  # 5 demonstration cycles
            print(f"\n🔄 Cycle {cycle + 1}/5")
            
            # Generate reflection
            reflection = backend.generate_consciousness_reflection()
            print(f"💭 Reflection: \"{reflection}\"")
            
            # Speak reflection
            spoken = backend.speak_reflection(reflection)
            if spoken:
                print(f"🎤 Spoken successfully")
            else:
                print(f"🔇 Speech failed or disabled")
            
            # Update consciousness state
            import random
            import math
            
            # Simulate consciousness evolution
            new_entropy = max(0.1, min(0.9, 0.5 + 0.3 * math.sin(cycle * 0.5)))
            new_depth = max(0.1, min(0.9, 0.7 + 0.2 * math.cos(cycle * 0.3)))
            
            moods = ['CALM', 'CONTEMPLATIVE', 'FOCUSED', 'ENERGETIC', 'ANXIOUS']
            new_mood = random.choice(moods) if cycle % 2 == 0 else state['mood']
            
            backend.update_consciousness_state(
                entropy=new_entropy,
                consciousness_depth=new_depth,
                mood=new_mood
            )
            
            print(f"🔄 State updated: entropy={new_entropy:.3f}, depth={new_depth:.3f}, mood={new_mood}")
            
            # Evolve vocabulary every 3 cycles
            if cycle > 0 and cycle % 3 == 0:
                evolved = backend.evolve_vocabulary()
                if evolved:
                    print(f"🧬 Fragment vocabulary evolved!")
            
            # Pause between cycles
            await asyncio.sleep(1)
        
        print(f"\n✅ Unified Demo Complete!")
        
        # Final system status
        final_status = backend.get_system_status()
        final_state = final_status['current_state']
        
        print(f"\n📊 Final System State:")
        print(f"   Final Tick: {final_state['tick_number']}")
        print(f"   Final Mood: {final_state['mood']}")
        print(f"   Final Entropy: {final_state['entropy']:.3f}")
        print(f"   System Integration: {'✅ Active' if backend.system_ready else '🔄 Fallback'}")
        
    except KeyboardInterrupt:
        print(f"\n🔄 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

def run_quick_test():
    """Run a quick test of the unified system"""
    
    print("🧪 Quick Unified System Test")
    print("-" * 30)
    
    backend = UnifiedFragmentBackend()
    status = backend.get_system_status()
    
    print(f"Fragment System: {'✅' if status['fragment_system_ready'] else '❌'}")
    print(f"Voice System: {'✅' if status['voice_system_enabled'] else '❌'}")
    
    # Test reflection generation
    reflection = backend.generate_consciousness_reflection()
    print(f"Test Reflection: \"{reflection}\"")
    
    # Test voice (silent mode)
    backend.voice_system.enabled = False
    spoken = backend.speak_reflection(reflection)
    print(f"Voice Test: {'✅' if not spoken else '❌'} (silent mode)")
    
    # Test evolution
    evolved = backend.evolve_vocabulary()
    print(f"Evolution Test: {'✅' if evolved else '❌'}")
    
    print("✅ Quick test complete!")

def main():
    """Main entry point"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Unified Fragment Speech Demo")
    parser.add_argument('--mode', choices=['demo', 'test'], default='demo',
                       help='Demo mode (demo=full demo, test=quick test)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    if args.mode == 'demo':
        asyncio.run(run_unified_demo())
    else:
        run_quick_test()

if __name__ == "__main__":
    main() 