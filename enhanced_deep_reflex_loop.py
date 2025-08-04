#!/usr/bin/env python3
"""
Enhanced Deep Reflex Loop - Live Dynamic Cognitive Content
=========================================================

Integrates live reflection generation with voice output to create a truly dynamic
cognitive system that generates and speaks real thoughts in real-time.
"""

import asyncio
import time
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# Import the live reflection generator
from live_reflection_generator import LiveReflectionGenerator

# Configure logging
logger = logging.getLogger("enhanced_deep_reflex")

class EnhancedDeepReflexLoop:
    """
    Enhanced Deep Reflex Loop with live reflection generation and voice output
    """
    
    def __init__(self, voice_engine=None):
        self.live_generator = LiveReflectionGenerator()
        self.voice_engine = voice_engine
        self.is_running = False
        self.reflections_spoken = 0
        self.last_spoken_time = time.time()
        
        # Configuration
        self.entropy_threshold = 0.7
        self.generation_interval = 3.0  # seconds
        self.voice_cooldown = 5.0  # seconds between voice outputs
        
        # Statistics
        self.stats = {
            'reflections_generated': 0,
            'reflections_spoken': 0,
            'high_entropy_count': 0,
            'start_time': None,
            'last_reflection_time': None
        }
        
        logger.info("🧠 Enhanced Deep Reflex Loop initialized")
    
    def set_voice_engine(self, voice_engine):
        """Set the voice engine for speaking reflections"""
        self.voice_engine = voice_engine
        logger.info("🎤 Voice engine connected to Deep Reflex Loop")
    
    def update_cognitive_state(self, new_state: Dict[str, Any]):
        """Update the live generator's cognitive state"""
        self.live_generator.update_cognitive_state(new_state)
        
        # Log significant state changes
        if new_state.get('entropy', 0) > self.entropy_threshold:
            logger.info(f"🔥 High entropy detected: {new_state['entropy']:.3f}")
    
    async def run_live_loop(self, duration: Optional[int] = None):
        """Run the enhanced Deep Reflex Loop with live generation and voice output"""
        
        self.is_running = True
        self.stats['start_time'] = time.time()
        
        logger.info("🧠 Enhanced Deep Reflex Loop starting...")
        logger.info(f"   Entropy threshold: {self.entropy_threshold}")
        logger.info(f"   Generation interval: {self.generation_interval}s")
        logger.info(f"   Voice cooldown: {self.voice_cooldown}s")
        logger.info(f"   Duration: {'Unlimited' if duration is None else f'{duration}s'}")
        print()
        
        start_time = time.time()
        
        try:
            while self.is_running:
                # Check duration limit
                if duration and (time.time() - start_time) > duration:
                    break
                
                # Generate live reflection
                reflection = self.live_generator.generate_live_reflection()
                
                if reflection:
                    self.stats['reflections_generated'] += 1
                    self.stats['last_reflection_time'] = time.time()
                    
                    # Check if it's high entropy
                    if reflection['entropy'] >= self.entropy_threshold:
                        self.stats['high_entropy_count'] += 1
                        
                        # Speak the reflection if voice is available and cooldown passed
                        if (self.voice_engine and 
                            (time.time() - self.last_spoken_time) > self.voice_cooldown):
                            
                            await self._speak_reflection(reflection)
                            self.last_spoken_time = time.time()
                        
                        # Log the high-entropy reflection
                        logger.info(f"🧠 High-entropy reflection generated:")
                        logger.info(f"   Entropy: {reflection['entropy']:.3f}")
                        logger.info(f"   Content: {reflection['text']}")
                        logger.info(f"   Depth: {reflection['depth_level']}")
                        print(f"💭 {reflection['text']}")
                        print()
                
                # Wait for next generation cycle
                await asyncio.sleep(self.generation_interval)
        
        except KeyboardInterrupt:
            logger.info("🛑 Deep Reflex Loop interrupted by user")
        except Exception as e:
            logger.error(f"❌ Deep Reflex Loop error: {e}")
        finally:
            self.is_running = False
            self._print_final_stats()
    
    async def _speak_reflection(self, reflection: Dict[str, Any]):
        """Speak a reflection using the voice engine"""
        
        if not self.voice_engine:
            return
        
        try:
            # Compose voice message
            voice_message = self._compose_voice_message(reflection)
            
            # Speak the message
            if hasattr(self.voice_engine, 'speak'):
                self.voice_engine.speak(voice_message)
                self.stats['reflections_spoken'] += 1
                logger.info(f"🎤 Spoke reflection: {voice_message[:50]}...")
            elif hasattr(self.voice_engine, 'speak_immediate'):
                self.voice_engine.speak_immediate(voice_message, "dawn")
                self.stats['reflections_spoken'] += 1
                logger.info(f"🎤 Spoke reflection: {voice_message[:50]}...")
            
        except Exception as e:
            logger.error(f"❌ Voice output error: {e}")
    
    def _compose_voice_message(self, reflection: Dict[str, Any]) -> str:
        """Compose a voice-ready message from the reflection"""
        
        # Extract key information
        entropy = reflection['entropy']
        content = reflection['text']
        depth_level = reflection['depth_level']
        mood = reflection['mood']
        
        # Compose based on depth level
        if depth_level == 'profound':
            prefix = "Profound cognitive insight: "
        elif depth_level == 'deep':
            prefix = "Deep reflection: "
        else:
            prefix = "Cognitive observation: "
        
        # Create the voice message
        voice_message = f"{prefix}{content}"
        
        return voice_message
    
    def _print_final_stats(self):
        """Print final statistics"""
        
        if not self.stats['start_time']:
            return
        
        duration = time.time() - self.stats['start_time']
        
        print("\n📊 Enhanced Deep Reflex Loop Statistics:")
        print("=" * 50)
        print(f"   Duration: {duration:.1f} seconds")
        print(f"   Reflections generated: {self.stats['reflections_generated']}")
        print(f"   High-entropy reflections: {self.stats['high_entropy_count']}")
        print(f"   Reflections spoken: {self.stats['reflections_spoken']}")
        print(f"   Generation rate: {self.stats['reflections_generated'] / duration:.2f} reflections/sec")
        print(f"   High-entropy rate: {self.stats['high_entropy_count'] / duration:.2f} high-entropy/sec")
        
        if self.stats['reflections_generated'] > 0:
            high_entropy_percentage = (self.stats['high_entropy_count'] / self.stats['reflections_generated']) * 100
            print(f"   High-entropy percentage: {high_entropy_percentage:.1f}%")
        
        print("✅ Enhanced Deep Reflex Loop complete")
    
    def stop(self):
        """Stop the Deep Reflex Loop"""
        self.is_running = False
        logger.info("🛑 Deep Reflex Loop stopping...")

# Integration with existing voice systems
class VoiceEngineAdapter:
    """Adapter for existing voice engines"""
    
    def __init__(self, voice_engine):
        self.voice_engine = voice_engine
    
    def speak(self, message: str):
        """Speak a message using the adapted voice engine"""
        if hasattr(self.voice_engine, 'speak_immediate'):
            self.voice_engine.speak_immediate(message, "dawn")
        elif hasattr(self.voice_engine, 'speak'):
            self.voice_engine.speak(message)
        else:
            print(f"🎤 [VOICE] {message}")

async def main():
    """Main function to run the enhanced Deep Reflex Loop"""
    
    print("🧠 Enhanced Deep Reflex Loop")
    print("=" * 50)
    print("Generating and speaking live cognitive content...")
    print()
    
    # Create the enhanced loop
    enhanced_loop = EnhancedDeepReflexLoop()
    
    # Initialize with interesting cognitive state
    enhanced_loop.update_cognitive_state({
        'entropy': 0.75,  # Start with high entropy
        'consciousness_depth': 0.6,
        'mood': 'CONTEMPLATIVE',
        'heat': 0.7,
        'scup': 0.8
    })
    
    # Run the loop
    await enhanced_loop.run_live_loop(duration=120)  # 2 minutes

if __name__ == "__main__":
    asyncio.run(main()) 