#!/usr/bin/env python3
"""
DAWN Fragment Speech Standalone Backend
Standalone backend runner focused on fragment speech integration
Bypasses problematic visualization imports to ensure clean operation
"""

import sys
import os
import asyncio
import logging
import time
import json
from pathlib import Path
from typing import Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Core DAWN imports (minimal set to avoid import errors)
try:
    from core.consciousness_core import DAWNConsciousness
    DAWN_CONSCIOUSNESS_AVAILABLE = True
except ImportError:
    DAWN_CONSCIOUSNESS_AVAILABLE = False

try:
    from backend.voice_echo import DAWNVoiceEcho
    VOICE_ECHO_AVAILABLE = True
except ImportError:
    VOICE_ECHO_AVAILABLE = False

# Fragment speech integration
try:
    from backend.fragment_speech_integration import (
        initialize_fragment_speech_integration,
        hook_reflection_system,
        get_fragment_speech_integration
    )
    FRAGMENT_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Fragment speech integration not available: {e}")
    FRAGMENT_INTEGRATION_AVAILABLE = False

logger = logging.getLogger(__name__)

class StandaloneDAWNBackend:
    """Standalone DAWN backend focused on fragment speech integration"""
    
    def __init__(self):
        self.consciousness = None
        self.voice_system = None
        self.fragment_integration = None
        self.backend_running = False
        self.tick_count = 0
        
        # System status
        self.systems_status = {
            'consciousness': False,
            'voice': False,
            'fragments': False,
            'integration': False
        }
    
    async def initialize(self):
        """Initialize all available systems"""
        
        print("🚀 Initializing Standalone DAWN Backend with Fragment Speech...")
        print("=" * 60)
        
        # Initialize consciousness (use mock if real not available)
        if DAWN_CONSCIOUSNESS_AVAILABLE:
            try:
                self.consciousness = DAWNConsciousness()
                self.systems_status['consciousness'] = True
                print("✅ DAWN Consciousness initialized")
            except Exception as e:
                print(f"⚠️ DAWN Consciousness failed: {e}")
                self.consciousness = self._create_mock_consciousness()
                print("🔄 Using mock consciousness")
        else:
            self.consciousness = self._create_mock_consciousness()
            print("🔄 Using mock consciousness (DAWN not available)")
        
        # Initialize voice system
        if VOICE_ECHO_AVAILABLE:
            try:
                self.voice_system = DAWNVoiceEcho()
                self.systems_status['voice'] = True
                print("✅ Voice system initialized")
            except Exception as e:
                print(f"⚠️ Voice system failed: {e}")
                self.voice_system = self._create_mock_voice()
                print("🔄 Using mock voice system")
        else:
            self.voice_system = self._create_mock_voice()
            print("🔄 Using mock voice system (Voice Echo not available)")
        
        # Initialize fragment speech integration
        if FRAGMENT_INTEGRATION_AVAILABLE:
            try:
                self.fragment_integration = initialize_fragment_speech_integration(
                    self.consciousness, 
                    self.voice_system
                )
                
                if self.fragment_integration.integration_active:
                    # Hook fragment system into consciousness
                    hook_success = hook_reflection_system(
                        self.consciousness, 
                        self.voice_system
                    )
                    
                    if hook_success:
                        self.systems_status['fragments'] = True
                        self.systems_status['integration'] = True
                        print("✅ Fragment speech integration active")
                        
                        # Log integration stats
                        stats = self.fragment_integration.get_integration_stats()
                        fragment_stats = stats.get('fragment_system_stats', {}).get('fragment_stats', {})
                        total_fragments = fragment_stats.get('total_fragments', 0)
                        print(f"📊 Fragment bank: {total_fragments} fragments available")
                    else:
                        print("❌ Fragment speech hook failed")
                else:
                    print("❌ Fragment speech integration inactive")
                    
            except Exception as e:
                print(f"❌ Fragment speech integration failed: {e}")
                self.fragment_integration = None
        else:
            print("❌ Fragment speech integration not available")
        
        # Final system status
        self.backend_running = True
        print(f"\n📊 System Status Summary:")
        for system, status in self.systems_status.items():
            print(f"   {system.title()}: {'✅' if status else '❌'}")
        
        if not any(self.systems_status.values()):
            print("⚠️ Warning: No systems successfully initialized")
        
        print(f"\n✅ Standalone backend initialization complete")
        return True
    
    def _create_mock_consciousness(self):
        """Create mock consciousness for demonstration"""
        
        class MockConsciousness:
            def __init__(self):
                self.state = {
                    'entropy': 0.5,
                    'consciousness_depth': 0.7,
                    'mood': 'CONTEMPLATIVE',
                    'tick_number': 0,
                    'heat': 0.4,
                    'scup': 0.6,
                    'active_sigils': ['wisdom_seek'],
                    'symbolic_roots': ['depth_probe']
                }
            
            def get_current_state(self):
                return self.state.copy()
            
            def generate_reflection(self, state=None):
                if state is None:
                    state = self.get_current_state()
                return f"Tick {state['tick_number']}: Mock consciousness reflection."
            
            def update_state(self, **kwargs):
                self.state.update(kwargs)
                self.state['tick_number'] += 1
        
        return MockConsciousness()
    
    def _create_mock_voice(self):
        """Create mock voice system"""
        
        class MockVoiceSystem:
            def __init__(self):
                self.enabled = True
            
            def speak_reflection(self, reflection, state=None):
                print(f"🎤 Mock Voice: {reflection[:50]}...")
                return True
        
        return MockVoiceSystem()
    
    async def run_consciousness_loop(self, cycles: int = 10):
        """Run the consciousness loop with fragment speech"""
        
        if not self.backend_running:
            print("❌ Backend not initialized")
            return
        
        print(f"\n🧠 Starting Consciousness Loop ({cycles} cycles)...")
        print("=" * 50)
        
        try:
            for cycle in range(cycles):
                cycle_num = cycle + 1
                print(f"\n🔄 Cycle {cycle_num}/{cycles}")
                
                # Update consciousness state
                self._update_consciousness_state(cycle_num)
                
                # Get current state (using correct DAWN API)
                if hasattr(self.consciousness, 'get_state'):
                    current_state = self.consciousness.get_state()
                else:
                    # Fallback state for systems without get_state
                    current_state = {
                        'entropy': 0.5,
                        'consciousness_depth': 0.7,
                        'mood': 'CONTEMPLATIVE',
                        'tick_number': cycle_num,
                        'heat': 0.4,
                        'scup': 0.6
                    }
                
                # Generate reflection using fragment integration system
                if self.fragment_integration and self.systems_status['integration']:
                    reflection = self.fragment_integration.generate_consciousness_reflection(current_state)
                else:
                    # Fallback reflection
                    reflection = f"Cycle {cycle_num}: I observe my internal state through DAWN consciousness."
                print(f"💭 Reflection: \"{reflection}\"")
                
                # Speak reflection
                if self.voice_system:
                    # Try different voice methods depending on the system
                    if hasattr(self.voice_system, 'speak_reflection'):
                        spoken = self.voice_system.speak_reflection(reflection, current_state)
                    elif hasattr(self.voice_system, 'speak_last_reflection'):
                        spoken = self.voice_system.speak_last_reflection()
                    else:
                        spoken = False
                    if spoken:
                        print(f"🎤 Spoken successfully")
                
                # Evolve fragment vocabulary periodically
                if (self.fragment_integration and 
                    self.systems_status['integration'] and 
                    cycle_num % 5 == 0):
                    
                    evolved = self.fragment_integration.evolve_consciousness_vocabulary(
                        current_state['tick_number']
                    )
                    if evolved:
                        print(f"🧬 Fragment vocabulary evolved at cycle {cycle_num}")
                
                # Show state evolution
                print(f"📊 State: entropy={current_state['entropy']:.3f}, "
                      f"depth={current_state['consciousness_depth']:.3f}, "
                      f"mood={current_state['mood']}, "
                      f"tick={current_state['tick_number']}")
                
                # Pause between cycles
                await asyncio.sleep(1.5)
            
            print(f"\n✅ Consciousness loop complete!")
            
            # Final stats
            if self.fragment_integration and self.systems_status['integration']:
                stats = self.fragment_integration.get_integration_stats()
                print(f"📊 Final integration status: Active")
                print(f"   Fragment system ready: {stats.get('integration_active', False)}")
            else:
                print(f"📊 Final integration status: Mock/Fallback mode")
            
        except KeyboardInterrupt:
            print(f"\n🔄 Consciousness loop interrupted by user")
        except Exception as e:
            print(f"\n❌ Consciousness loop error: {e}")
            logger.exception("Consciousness loop error")
    
    def _update_consciousness_state(self, cycle: int):
        """Update consciousness state to simulate evolution"""
        
        import random
        import math
        
        # Simulate dynamic evolution
        entropy = 0.5 + 0.3 * math.sin(cycle * 0.1)
        depth = 0.7 + 0.2 * math.cos(cycle * 0.15)
        
        # Mood evolution
        moods = ['CALM', 'CONTEMPLATIVE', 'FOCUSED', 'ENERGETIC', 'ANXIOUS']
        if cycle % 4 == 0:
            mood = random.choice(moods)
        else:
            if hasattr(self.consciousness, 'get_state'):
                current_state = self.consciousness.get_state()
            else:
                current_state = {'mood': 'CONTEMPLATIVE'}  # Fallback if no state method
            mood = current_state.get('mood', 'CONTEMPLATIVE')
        
        # Update consciousness (check if real DAWN or mock)
        if hasattr(self.consciousness, 'update_state'):
            # DAWN consciousness only accepts: scup, entropy, mood
            # Note: DAWN's update_state is async, so we'll store values for next integration
            # For now, we'll skip direct state updates and let DAWN manage its own state
            pass
        else:
            # For real DAWN consciousness, update through proper interface
            # This would need actual DAWN consciousness state update methods
            pass
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        status = {
            'backend_running': self.backend_running,
            'systems_status': self.systems_status.copy(),
            'cycles_completed': self.tick_count
        }
        
        if self.consciousness:
            if hasattr(self.consciousness, 'get_state'):
                status['current_state'] = self.consciousness.get_state()
            else:
                status['current_state'] = {'error': 'No state method available'}
        
        if self.fragment_integration and self.systems_status['integration']:
            try:
                integration_stats = self.fragment_integration.get_integration_stats()
                status['fragment_integration'] = integration_stats
            except Exception as e:
                status['fragment_integration_error'] = str(e)
        
        return status
    
    async def shutdown(self):
        """Shutdown the backend"""
        
        print("\n🔄 Shutting down Standalone DAWN Backend...")
        
        if self.fragment_integration:
            self.fragment_integration.shutdown()
        
        self.backend_running = False
        print("✅ Standalone backend shutdown complete")

async def run_standalone_backend():
    """Run the standalone backend with fragment speech"""
    
    backend = StandaloneDAWNBackend()
    
    try:
        # Initialize all systems
        success = await backend.initialize()
        
        if not success:
            print("❌ Backend initialization failed")
            return
        
        # Run consciousness loop
        await backend.run_consciousness_loop(cycles=10)
        
    finally:
        # Ensure clean shutdown
        await backend.shutdown()

def main():
    """Main entry point"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Standalone Backend with Fragment Speech")
    parser.add_argument('--cycles', type=int, default=10, help='Number of consciousness cycles')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🧠🎤 DAWN STANDALONE BACKEND WITH FRAGMENT SPEECH 🎤🧠")
    print("=" * 70)
    print("Bypassing problematic visualization imports for clean operation")
    print()
    
    # Override cycles if specified
    async def run_with_cycles():
        backend = StandaloneDAWNBackend()
        try:
            await backend.initialize()
            await backend.run_consciousness_loop(cycles=args.cycles)
        finally:
            await backend.shutdown()
    
    asyncio.run(run_with_cycles())

if __name__ == "__main__":
    main() 