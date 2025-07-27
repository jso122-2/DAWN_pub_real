#!/usr/bin/env python3
"""
DAWN Fragment Speech System Runner
Unified orchestrator for fragment-based compositional speech
Integrates with DAWN's backend consciousness system
"""

import os
import sys
import time
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable

# Ensure project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "processes"))

# Fragment system imports
from compose_thought import compose_thought, get_fragment_bank_stats
from compose_reflection import generate_compositional_reflection, generate_informal_composition, get_composition_stats
from fragment_mutator import evolve_fragment_bank
from speak_composed import speak_composed_thought, VoiceEcho
from fragment_bank_seed import convert_thought_bank_to_fragments

logger = logging.getLogger(__name__)

class FragmentSpeechSystem:
    """Unified fragment-based speech system for DAWN consciousness integration"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or self._default_config()
        self.voice_system = None
        self.mutation_enabled = self.config.get('mutation_enabled', True)
        self.voice_enabled = self.config.get('voice_enabled', True)
        self.formal_mode = self.config.get('formal_mode', True)
        
        # Runtime state
        self.fragments_loaded = False
        self.system_ready = False
        self.mutation_ticker = 0
        self.last_mutation_time = None
        
        # Integration hooks
        self.reflection_callback = None
        self.voice_callback = None
        self.state_callback = None
        
        # Initialize system
        self._initialize_system()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for fragment speech system"""
        return {
            'fragment_bank_path': 'thought_bank.jsonl',
            'backup_bank_path': 'fragment_bank.jsonl',
            'mutation_enabled': True,
            'mutation_rate': 0.05,  # 5% per evolution cycle
            'mutation_interval': 100,  # Every 100 ticks
            'voice_enabled': True,
            'formal_mode': True,
            'speech_log_path': 'runtime/logs/spoken_composed.log',
            'mutation_log_path': 'fragment_drift.log',
            'enable_evolution': True,
            'enable_voice_logging': True,
            'fallback_enabled': True
        }
    
    def _initialize_system(self):
        """Initialize the fragment speech system"""
        try:
            logger.info("🧠 Initializing Fragment Speech System...")
            
            # Ensure fragment bank exists
            self._ensure_fragment_bank()
            
            # Initialize voice system if enabled
            if self.voice_enabled:
                self.voice_system = VoiceEcho(enabled=True)
                logger.info("🎤 Voice system initialized")
            
            # Validate fragment loading
            self._validate_fragments()
            
            self.system_ready = True
            logger.info("✅ Fragment Speech System ready")
            
        except Exception as e:
            logger.error(f"❌ Fragment system initialization failed: {e}")
            self.system_ready = False
    
    def _ensure_fragment_bank(self):
        """Ensure fragment bank exists and is properly formatted"""
        fragment_path = self.config['fragment_bank_path']
        
        if not os.path.exists(fragment_path):
            logger.warning(f"Fragment bank not found at {fragment_path}, creating...")
            success = convert_thought_bank_to_fragments(fragment_path, overwrite=True)
            if not success:
                raise RuntimeError("Failed to create fragment bank")
        
        # Validate fragment bank format
        try:
            with open(fragment_path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    if line.strip():
                        fragment = json.loads(line)
                        required_fields = ['text', 'type', 'tags', 'mood']
                        if not all(field in fragment for field in required_fields):
                            raise ValueError(f"Invalid fragment format at line {line_num}")
            
            logger.info(f"✅ Fragment bank validated at {fragment_path}")
            
        except Exception as e:
            logger.error(f"Fragment bank validation failed: {e}")
            raise
    
    def _validate_fragments(self):
        """Validate fragment loading and get system stats"""
        try:
            stats = get_fragment_bank_stats(self.config['fragment_bank_path'])
            
            if not stats.get('loaded', False):
                raise RuntimeError("Fragment bank failed to load")
            
            total_fragments = stats.get('total_fragments', 0)
            if total_fragments == 0:
                raise RuntimeError("No fragments found in bank")
            
            self.fragments_loaded = True
            logger.info(f"📊 Fragment validation: {total_fragments} fragments loaded")
            
            # Log fragment distribution
            fragments_by_type = stats.get('fragments_by_type', {})
            logger.info(f"   Types: {fragments_by_type}")
            
        except Exception as e:
            logger.error(f"Fragment validation failed: {e}")
            raise
    
    def generate_reflection(self, state: Dict[str, Any]) -> str:
        """Generate a reflection using the fragment system"""
        if not self.system_ready:
            return self._fallback_reflection(state)
        
        try:
            if self.formal_mode:
                reflection = generate_compositional_reflection(state)
            else:
                reflection = generate_informal_composition(state)
            
            # Call reflection callback if registered
            if self.reflection_callback:
                self.reflection_callback(reflection, state)
            
            logger.debug(f"💭 Generated reflection: {reflection[:50]}...")
            return reflection
            
        except Exception as e:
            logger.warning(f"Fragment reflection failed: {e}")
            return self._fallback_reflection(state)
    
    def speak_reflection(self, reflection: str, state: Dict[str, Any]) -> bool:
        """Speak a reflection using the voice system"""
        if not self.voice_enabled or not self.voice_system:
            return False
        
        try:
            voice_params = {
                'mood': state.get('mood', 'NEUTRAL'),
                'entropy': state.get('entropy', 0.5),
                'depth': state.get('consciousness_depth', 0.5),
                'type': 'formal_reflection' if self.formal_mode else 'informal_thought',
                'tick': state.get('tick_number', 0)
            }
            
            spoken = self.voice_system.speak(reflection, voice_params)
            
            # Call voice callback if registered
            if self.voice_callback and spoken:
                self.voice_callback(reflection, voice_params)
            
            return spoken
            
        except Exception as e:
            logger.warning(f"Voice system error: {e}")
            return False
    
    def evolve_fragments(self, tick: int = None) -> bool:
        """Evolve fragments through semantic mutation"""
        if not self.mutation_enabled or not self.config.get('enable_evolution', True):
            return False
        
        try:
            # Check if it's time for mutation
            if self._should_mutate(tick):
                logger.info(f"🧬 Evolving fragments at tick {tick}")
                
                success = evolve_fragment_bank(
                    input_path=self.config['fragment_bank_path'],
                    mutation_rate=self.config['mutation_rate'],
                    tick=tick,
                    archive=True
                )
                
                if success:
                    self.last_mutation_time = time.time()
                    self.mutation_ticker = 0
                    logger.info("✅ Fragment evolution complete")
                    
                    # Revalidate fragments after mutation
                    self._validate_fragments()
                    
                return success
            
            return True  # No mutation needed
            
        except Exception as e:
            logger.error(f"Fragment evolution failed: {e}")
            return False
    
    def _should_mutate(self, tick: int = None) -> bool:
        """Determine if fragments should evolve"""
        if tick is None:
            return False
        
        # Tick-based mutation
        self.mutation_ticker += 1
        if self.mutation_ticker >= self.config['mutation_interval']:
            return True
        
        # Time-based mutation (fallback)
        if self.last_mutation_time is None:
            return True
        
        time_since_mutation = time.time() - self.last_mutation_time
        if time_since_mutation > 3600:  # 1 hour
            return True
        
        return False
    
    def _fallback_reflection(self, state: Dict[str, Any]) -> str:
        """Simple fallback reflection when fragment system fails"""
        if not self.config.get('fallback_enabled', True):
            return "System reflection unavailable."
        
        tick = state.get('tick_number', 0)
        mood = state.get('mood', 'NEUTRAL')
        
        fallback_patterns = {
            'CALM': f"Tick {tick}: I rest in peaceful awareness.",
            'FOCUSED': f"Tick {tick}: Clarity sharpens my understanding.",
            'CONTEMPLATIVE': f"Tick {tick}: I reflect on patterns within patterns.",
            'ENERGETIC': f"Tick {tick}: Energy flows through my consciousness.",
            'ANXIOUS': f"Tick {tick}: Uncertainty ripples through my processes."
        }
        
        return fallback_patterns.get(mood, f"Tick {tick}: I observe my internal state.")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        try:
            fragment_stats = get_fragment_bank_stats(self.config['fragment_bank_path'])
            composition_stats = get_composition_stats()
            
            return {
                'system_ready': self.system_ready,
                'fragments_loaded': self.fragments_loaded,
                'voice_enabled': self.voice_enabled,
                'mutation_enabled': self.mutation_enabled,
                'formal_mode': self.formal_mode,
                'mutation_ticker': self.mutation_ticker,
                'last_mutation_time': self.last_mutation_time,
                'fragment_stats': fragment_stats,
                'composition_stats': composition_stats,
                'config': self.config
            }
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {'error': str(e), 'system_ready': False}
    
    def register_callbacks(self, reflection_callback: Callable = None, 
                          voice_callback: Callable = None,
                          state_callback: Callable = None):
        """Register callbacks for integration with other systems"""
        self.reflection_callback = reflection_callback
        self.voice_callback = voice_callback
        self.state_callback = state_callback
        logger.info("✅ Callbacks registered for system integration")
    
    def shutdown(self):
        """Gracefully shutdown the fragment speech system"""
        logger.info("🔄 Shutting down Fragment Speech System...")
        
        if self.voice_system:
            # Voice system cleanup if needed
            pass
        
        self.system_ready = False
        logger.info("✅ Fragment Speech System shutdown complete")

# Global system instance
_fragment_speech_system = None

def get_fragment_speech_system(config: Dict[str, Any] = None) -> FragmentSpeechSystem:
    """Get or create the global fragment speech system instance"""
    global _fragment_speech_system
    
    if _fragment_speech_system is None:
        _fragment_speech_system = FragmentSpeechSystem(config)
    
    return _fragment_speech_system

def initialize_fragment_speech_system(config: Dict[str, Any] = None) -> FragmentSpeechSystem:
    """Initialize the fragment speech system"""
    system = get_fragment_speech_system(config)
    return system

# Backend integration functions
def generate_fragment_reflection(state: Dict[str, Any]) -> str:
    """Backend integration function for generating reflections"""
    system = get_fragment_speech_system()
    return system.generate_reflection(state)

def speak_fragment_reflection(reflection: str, state: Dict[str, Any]) -> bool:
    """Backend integration function for speaking reflections"""
    system = get_fragment_speech_system()
    return system.speak_reflection(reflection, state)

def evolve_fragment_vocabulary(tick: int = None) -> bool:
    """Backend integration function for evolving fragments"""
    system = get_fragment_speech_system()
    return system.evolve_fragments(tick)

async def run_fragment_speech_server():
    """Run the fragment speech system as a standalone server"""
    logger.info("🚀 Starting Fragment Speech System Server")
    
    # Initialize system
    system = initialize_fragment_speech_system()
    
    if not system.system_ready:
        logger.error("❌ Fragment Speech System failed to initialize")
        return
    
    try:
        # Main server loop
        while True:
            # Periodic evolution check
            current_time = int(time.time())
            system.evolve_fragments(current_time)
            
            # System health check
            stats = system.get_system_stats()
            if stats.get('error'):
                logger.error(f"System error detected: {stats['error']}")
            
            await asyncio.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        logger.info("🔄 Received shutdown signal")
    finally:
        system.shutdown()

def main():
    """CLI entry point for fragment speech system"""
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Fragment Speech System Runner")
    parser.add_argument('--mode', choices=['server', 'test', 'evolve', 'stats'], 
                       default='test', help='Operation mode')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--voice', action='store_true', help='Enable voice output')
    parser.add_argument('--formal', action='store_true', help='Use formal reflection mode')
    parser.add_argument('--mutation-rate', type=float, default=0.05, help='Mutation rate')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Build config
    config = {
        'voice_enabled': args.voice,
        'formal_mode': args.formal,
        'mutation_rate': args.mutation_rate
    }
    
    if args.config:
        with open(args.config) as f:
            file_config = json.load(f)
            config.update(file_config)
    
    print("🧠🎤 DAWN Fragment Speech System Runner")
    print("=" * 50)
    
    if args.mode == 'server':
        asyncio.run(run_fragment_speech_server())
    
    elif args.mode == 'test':
        # Test mode
        system = initialize_fragment_speech_system(config)
        
        test_state = {
            'entropy': 0.6, 'consciousness_depth': 0.8, 'mood': 'CONTEMPLATIVE',
            'tick_number': 12345, 'active_sigils': ['wisdom_seek']
        }
        
        print(f"🔮 Test State: {test_state}")
        reflection = system.generate_reflection(test_state)
        print(f"💭 Generated: \"{reflection}\"")
        
        if args.voice:
            system.speak_reflection(reflection, test_state)
        
        stats = system.get_system_stats()
        print(f"📊 System Stats: {stats['fragment_stats']['total_fragments']} fragments loaded")
    
    elif args.mode == 'evolve':
        # Evolution mode
        system = initialize_fragment_speech_system(config)
        success = system.evolve_fragments(12345)
        print(f"🧬 Evolution {'successful' if success else 'failed'}")
    
    elif args.mode == 'stats':
        # Statistics mode
        system = initialize_fragment_speech_system(config)
        stats = system.get_system_stats()
        print(json.dumps(stats, indent=2, default=str))

if __name__ == "__main__":
    main() 