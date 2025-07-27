#!/usr/bin/env python3
"""
DAWN Backend Runner with Fragment Speech Integration
Enhanced backend that integrates fragment-based compositional speech with consciousness
"""

import sys
import os
import asyncio
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Backend imports
from backend.main import dawn_central
from backend.voice_echo import DAWNVoiceEcho

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

class DAWNBackendWithFragments:
    """Enhanced DAWN backend with fragment speech integration"""
    
    def __init__(self):
        self.dawn_consciousness = None
        self.voice_echo = None
        self.fragment_integration = None
        self.backend_running = False
        
    async def initialize_systems(self):
        """Initialize all backend systems including fragment speech"""
        
        logger.info("🚀 Initializing DAWN Backend with Fragment Speech...")
        
        # Initialize core consciousness (simplified for demo)
        # In real integration, this would use the actual DAWN consciousness
        self.dawn_consciousness = self._create_mock_consciousness()
        
        # Initialize voice system
        self.voice_echo = DAWNVoiceEcho()
        
        # Initialize fragment speech integration if available
        if FRAGMENT_INTEGRATION_AVAILABLE:
            try:
                self.fragment_integration = initialize_fragment_speech_integration(
                    self.dawn_consciousness, 
                    self.voice_echo
                )
                
                if self.fragment_integration.integration_active:
                    # Hook fragment system into consciousness
                    hook_success = hook_reflection_system(
                        self.dawn_consciousness, 
                        self.voice_echo
                    )
                    
                    if hook_success:
                        logger.info("✅ Fragment speech integration active")
                        
                        # Log integration stats
                        stats = self.fragment_integration.get_integration_stats()
                        fragment_stats = stats.get('fragment_system_stats', {}).get('fragment_stats', {})
                        total_fragments = fragment_stats.get('total_fragments', 0)
                        logger.info(f"📊 Integration: {total_fragments} fragments available")
                    else:
                        logger.error("❌ Fragment speech hook failed")
                else:
                    logger.error("❌ Fragment speech integration inactive")
                    
            except Exception as e:
                logger.error(f"❌ Fragment speech integration failed: {e}")
                self.fragment_integration = None
        
        else:
            logger.warning("⚠️ Fragment speech system not available - using standard reflection")
        
        self.backend_running = True
        logger.info("✅ DAWN Backend initialization complete")
    
    def _create_mock_consciousness(self):
        """Create mock consciousness for demonstration"""
        
        class MockDAWNConsciousness:
            def __init__(self):
                self.current_state = {
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
                return self.current_state.copy()
            
            def generate_reflection(self, state=None):
                if state is None:
                    state = self.get_current_state()
                return f"Tick {state['tick_number']}: Default reflection from consciousness."
            
            def update_state(self, **kwargs):
                self.current_state.update(kwargs)
                self.current_state['tick_number'] += 1
        
        return MockDAWNConsciousness()
    
    async def run_consciousness_loop(self):
        """Run the main consciousness loop with fragment speech"""
        
        if not self.backend_running:
            logger.error("❌ Backend not initialized")
            return
        
        logger.info("🧠 Starting consciousness loop with fragment speech...")
        
        try:
            tick_count = 0
            
            while True:
                tick_count += 1
                
                # Update consciousness state (simulate cognitive evolution)
                self._update_consciousness_state(tick_count)
                
                # Generate and speak reflection using fragment system
                current_state = self.dawn_consciousness.get_current_state()
                
                # Generate reflection (now using fragment system if hooked)
                reflection = self.dawn_consciousness.generate_reflection(current_state)
                
                print(f"💭 Tick {tick_count}: {reflection}")
                
                # Speak reflection if voice available
                if self.voice_echo:
                    spoken = self.voice_echo.speak_reflection(reflection, current_state)
                    if spoken:
                        print(f"🎤 Spoken: {reflection[:50]}...")
                
                # Evolve fragment vocabulary periodically
                if self.fragment_integration and tick_count % 10 == 0:
                    evolved = self.fragment_integration.evolve_consciousness_vocabulary(tick_count)
                    if evolved:
                        print(f"🧬 Fragment vocabulary evolved at tick {tick_count}")
                
                # Log system stats periodically
                if tick_count % 25 == 0:
                    self._log_system_stats()
                
                # Simulate consciousness tick rate
                await asyncio.sleep(2)  # 2 second ticks for demo
                
        except KeyboardInterrupt:
            logger.info("🔄 Consciousness loop interrupted")
        except Exception as e:
            logger.error(f"❌ Consciousness loop error: {e}")
    
    def _update_consciousness_state(self, tick_count: int):
        """Update consciousness state to simulate cognitive evolution"""
        
        # Simulate dynamic state changes
        import random
        import math
        
        # Oscillating entropy
        entropy = 0.5 + 0.3 * math.sin(tick_count * 0.1)
        
        # Slowly changing depth
        depth = 0.7 + 0.2 * math.sin(tick_count * 0.05)
        
        # Mood transitions
        moods = ['CALM', 'CONTEMPLATIVE', 'FOCUSED', 'ENERGETIC', 'ANXIOUS']
        if tick_count % 15 == 0:  # Change mood every 15 ticks
            mood = random.choice(moods)
        else:
            mood = self.dawn_consciousness.current_state['mood']
        
        # Update consciousness
        self.dawn_consciousness.update_state(
            entropy=max(0.1, min(0.9, entropy)),
            consciousness_depth=max(0.1, min(0.9, depth)),
            mood=mood,
            heat=random.uniform(0.2, 0.8),
            scup=random.uniform(0.3, 0.9)
        )
    
    def _log_system_stats(self):
        """Log system statistics"""
        
        if self.fragment_integration:
            stats = self.fragment_integration.get_integration_stats()
            
            if stats.get('integration_active'):
                fragment_stats = stats.get('fragment_system_stats', {})
                system_stats = fragment_stats.get('fragment_stats', {})
                
                print(f"📊 System Stats:")
                print(f"   Fragments loaded: {system_stats.get('total_fragments', 0)}")
                print(f"   Integration active: {stats['integration_active']}")
                print(f"   Voice enabled: {fragment_stats.get('voice_enabled', False)}")
                print(f"   Mutation enabled: {fragment_stats.get('mutation_enabled', False)}")
            else:
                print("📊 Fragment integration inactive - using fallback reflection")
        else:
            print("📊 No fragment integration - using standard reflection")
    
    async def shutdown(self):
        """Shutdown all systems"""
        
        logger.info("🔄 Shutting down DAWN Backend...")
        
        if self.fragment_integration:
            self.fragment_integration.shutdown()
        
        self.backend_running = False
        logger.info("✅ DAWN Backend shutdown complete")

async def run_integrated_backend():
    """Run the integrated DAWN backend with fragment speech"""
    
    backend = DAWNBackendWithFragments()
    
    try:
        # Initialize all systems
        await backend.initialize_systems()
        
        # Run consciousness loop
        await backend.run_consciousness_loop()
        
    finally:
        # Ensure clean shutdown
        await backend.shutdown()

def main():
    """Main entry point for integrated backend"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Backend with Fragment Speech Integration")
    parser.add_argument('--mode', choices=['integrated', 'standard'], default='integrated',
                       help='Backend mode (integrated=with fragments, standard=original)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🧠🎤 DAWN Backend with Fragment Speech Integration")
    print("=" * 60)
    
    if args.mode == 'integrated':
        print("🔗 Running with fragment speech integration...")
        asyncio.run(run_integrated_backend())
    else:
        print("📝 Running standard backend...")
        # Fall back to original backend
        dawn_central()

if __name__ == "__main__":
    main() 