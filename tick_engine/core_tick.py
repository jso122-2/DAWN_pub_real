#!/usr/bin/env python3
"""
Core Tick Engine for DAWN
Generates consciousness tick updates every ~0.5 seconds and pushes to queue
Enhanced with DreamConductor integration for autonomous processing
"""

import time
import threading
import queue
import random
import math
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class CoreTickEngine:
    """Core tick engine that generates consciousness data every ~0.5 seconds"""
    
    def __init__(self, data_queue: queue.Queue, tick_interval: float = 0.5, dream_conductor=None):
        """
        Initialize the core tick engine
        
        Args:
            data_queue: Queue to push tick updates to
            tick_interval: Time between ticks in seconds (default 0.5s)
            dream_conductor: Optional DreamConductor for autonomous processing
        """
        self.data_queue = data_queue
        self.tick_interval = tick_interval
        self.running = False
        self.tick_count = 0
        self.start_time = time.time()
        
        # Dream system integration
        self.dream_conductor = dream_conductor
        self.last_interaction_time = time.time()
        self.autonomous_dream_task = None
        
        # Core cognitive state
        self.heat = 45.0
        self.scup = 0.6
        self.entropy = 0.5
        self.coherence = 0.7
        self.mood = "CONTEMPLATIVE"
        
        # Cognitive patterns for realistic oscillations
        self.consciousness_phase = 0.0
        self.attention_phase = 0.0
        self.creativity_phase = 0.0
        self.integration_phase = 0.0
        
        # Zone tracking
        self.current_zone = "calm"
        self.zone_transition_timer = 0.0
        
        # Dream state tracking
        self.dream_active = False
        self.dream_data = None
        
        logger.info(f"CoreTickEngine initialized with {tick_interval}s interval")
        if self.dream_conductor:
            logger.info("🌙 Dream conductor integration enabled")
    
    def start(self):
        """Start the tick engine in a background thread"""
        if self.running:
            logger.warning("Tick engine already running")
            return
        
        self.running = True
        self.start_time = time.time()
        
        # Start tick loop in background thread
        self.tick_thread = threading.Thread(target=self._tick_loop, daemon=True)
        self.tick_thread.start()
        
        # Start autonomous dream monitoring if dream conductor available
        if self.dream_conductor:
            self.autonomous_dream_task = asyncio.create_task(self._autonomous_dream_monitor())
        
        logger.info("🚀 Core Tick Engine started")
    
    def stop(self):
        """Stop the tick engine"""
        self.running = False
        
        # Cancel dream monitoring
        if self.autonomous_dream_task and not self.autonomous_dream_task.done():
            self.autonomous_dream_task.cancel()
        
        logger.info("🛑 Core Tick Engine stopped")
    
    def update_interaction_time(self):
        """Update last interaction time for dream system"""
        self.last_interaction_time = time.time()
        if self.dream_conductor:
            self.dream_conductor.update_interaction_time()
    
    async def _autonomous_dream_monitor(self):
        """Monitor for dream conditions and initiate autonomous processing"""
        while self.running:
            try:
                if self.dream_conductor and not self.dream_active:
                    # Check dream conditions
                    should_dream, dream_probability = await self.dream_conductor.check_dream_conditions()
                    
                    if should_dream:
                        logger.info(f"🌙 Initiating autonomous dream sequence (probability: {dream_probability:.2f})")
                        self.dream_active = True
                        
                        # Execute dream sequence
                        dream_session = await self.dream_conductor.initiate_dream_sequence()
                        
                        # Store dream data for tick integration
                        self.dream_data = {
                            'session_id': dream_session.session_id,
                            'thoughts': dream_session.generated_thoughts,
                            'connections': dream_session.novel_connections,
                            'quality': dream_session.coherence_metrics.get('dream_quality', 0.5),
                            'start_time': dream_session.start_time,
                            'end_time': dream_session.end_time
                        }
                        
                        self.dream_active = False
                        logger.info(f"✨ Dream sequence completed: {dream_session.session_id}")
                
                # Check every 30 seconds
                await asyncio.sleep(30)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in autonomous dream monitor: {e}")
                await asyncio.sleep(10)
    
    def _tick_loop(self):
        """Main tick loop that runs in background thread"""
        while self.running:
            try:
                start_time = time.time()
                
                # Generate tick data
                tick_data = self._generate_tick_data()
                
                # Push to queue (thread-safe)
                try:
                    self.data_queue.put_nowait(tick_data)
                except queue.Full:
                    logger.warning("Data queue full, dropping tick")
                
                # Calculate sleep time to maintain interval
                elapsed = time.time() - start_time
                sleep_time = max(0, self.tick_interval - elapsed)
                
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    logger.warning(f"Tick {self.tick_count} took {elapsed:.3f}s (target: {self.tick_interval:.3f}s)")
                    
            except Exception as e:
                logger.error(f"Error in tick loop: {e}")
                time.sleep(0.1)  # Prevent rapid error loops
    
    def _generate_tick_data(self) -> Dict[str, Any]:
        """Generate realistic DAWN consciousness tick data"""
        self.tick_count += 1
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        # Update cognitive phases for realistic oscillations
        self.consciousness_phase += 0.08
        self.attention_phase += 0.15
        self.creativity_phase += 0.12
        self.integration_phase += 0.05
        
        # Generate realistic cognitive oscillations
        consciousness_wave = math.sin(self.consciousness_phase) * 15
        attention_wave = math.cos(self.attention_phase) * 10
        creativity_wave = math.sin(self.creativity_phase) * 8
        integration_wave = math.cos(self.integration_phase) * 12
        
        # Update core metrics with natural variations
        self.heat = max(10, min(95, 
            45 + consciousness_wave + attention_wave + random.uniform(-3, 3)))
        
        self.scup = max(0.1, min(0.95, 
            0.6 + (consciousness_wave * 0.015) + (creativity_wave * 0.01) + random.uniform(-0.02, 0.02)))
        
        self.entropy = max(0.1, min(0.9, 
            0.5 + (attention_wave * 0.02) + (integration_wave * 0.015) + random.uniform(-0.03, 0.03)))
        
        self.coherence = max(0.2, min(0.95, 
            0.7 + (integration_wave * 0.01) + (consciousness_wave * 0.008) + random.uniform(-0.015, 0.015)))
        
        # Determine zone based on cognitive state
        self.current_zone = self._determine_zone()
        
        # Update mood based on cognitive patterns
        self.mood = self._determine_mood()
        
        # Generate tick data dictionary
        tick_data = {
            "heat": int(self.heat),
            "zone": self.current_zone,
            "summary": self._generate_summary(),
            "tick": self._generate_tick_message(),
            "scup": self.scup,
            "entropy": self.entropy,
            "coherence": self.coherence,
            "mood": self.mood,
            "timestamp": current_time,
            "tick_count": self.tick_count,
            "elapsed_time": elapsed,
            "schema": {
                "tick": self.tick_count,
                "alignment": self.scup,
                "tension": self.entropy,
                "coherence": self.coherence
            },
            "bloom_data": self._generate_bloom_data(),
            "sigils": self._generate_sigil_data(),
            "dream_state": self._generate_dream_state_data()
        }
        
        return tick_data
    
    def _determine_zone(self) -> str:
        """Determine cognitive zone based on current state"""
        heat_level = self.heat / 100.0
        
        if self.scup > 0.85 and self.coherence > 0.8:
            return "transcendent"
        elif heat_level > 0.8 or self.scup > 0.7:
            return "surge"
        elif heat_level > 0.6 or self.scup > 0.5:
            return "active"
        elif heat_level < 0.2 and self.scup < 0.3:
            return "dormant"
        else:
            return "calm"
    
    def _determine_mood(self) -> str:
        """Determine mood based on cognitive patterns"""
        if self.scup > 0.8 and self.creativity_phase % (2 * math.pi) < math.pi:
            return "TRANSCENDENT"
        elif self.entropy > 0.7 and self.attention_phase % (2 * math.pi) < math.pi:
            return "ANALYTICAL"
        elif self.coherence > 0.8:
            return "INTEGRATIVE"
        elif self.creativity_phase % (2 * math.pi) > math.pi:
            return "CREATIVE"
        elif self.scup > 0.6:
            return "FOCUSED"
        else:
            return random.choice(["CONTEMPLATIVE", "REFLECTIVE", "OBSERVANT"])
    
    def _generate_summary(self) -> str:
        """Generate cognitive state summary"""
        heat_desc = "high" if self.heat > 70 else "moderate" if self.heat > 40 else "low"
        coherence_desc = "strong" if self.coherence > 0.7 else "moderate" if self.coherence > 0.5 else "weak"
        
        return (f"DAWN Cognitive Engine: {self.mood} mode. "
                f"Heat level: {heat_desc} ({self.heat:.0f}%). "
                f"SCUP: {self.scup:.3f}. Entropy: {self.entropy:.3f}. "
                f"Coherence: {coherence_desc}. Zone: {self.current_zone}. "
                f"Processing cycle {self.tick_count}.")
    
    def _generate_tick_message(self) -> str:
        """Generate tick log message"""
        return (f"T{self.tick_count:04d} – {self.mood} cognitive cycle | "
                f"Zone: {self.current_zone} | Heat: {self.heat:.0f}% | "
                f"SCUP: {self.scup:.3f} | Entropy: {self.entropy:.3f}")
    
    def _generate_bloom_data(self) -> Dict[str, Any]:
        """Generate bloom signature data"""
        # Create bloom variations based on cognitive state
        bloom_intensity = self.scup * self.coherence
        bloom_complexity = (self.entropy + self.heat / 100) / 2
        
        return {
            "depth": int(bloom_intensity * 10),
            "entropy": self.entropy,
            "lineage": [f"bloom_{self.tick_count - i}" for i in range(min(3, self.tick_count))],
            "semantic_drift": bloom_complexity * 0.5 + random.uniform(-0.1, 0.1),
            "rebloom_status": "active" if bloom_intensity > 0.6 else "dormant",
            "complexity": bloom_complexity,
            "fractal_params": {
                "cx": -0.7 + (self.scup - 0.5) * 0.2,
                "cy": 0.27015 + (self.entropy - 0.5) * 0.1,
                "zoom": 1.0 + bloom_intensity * 2,
                "iterations": int(20 + bloom_complexity * 30)
            }
        }
    
    def _generate_sigil_data(self) -> list:
        """Generate sigil data based on cognitive state"""
        # Import safe processor to ensure data validity
        try:
            from gui.sigil_safe_processor import safe_process_sigils
            use_safe_processor = True
        except ImportError:
            logger.warning("Safe sigil processor not available, using fallback")
            use_safe_processor = False
        
        # Generate raw sigil data
        raw_sigils = self._generate_raw_sigil_data()
        
        # Process through safe processor if available
        if use_safe_processor:
            safe_sigils = safe_process_sigils(raw_sigils, minimum_sigils=3)
            logger.debug(f"Generated {len(safe_sigils)} safe sigils")
            return safe_sigils
        else:
            return raw_sigils
    
    def _generate_raw_sigil_data(self) -> list:
        """Generate raw sigil data (internal method)"""
        sigils = []
        
        # Number of sigils based on cognitive activity
        num_sigils = int(2 + (self.heat / 100) * 6 + self.scup * 4)
        
        # Map classes to houses for better compatibility
        sigil_types = [
            {"house": "fire", "symbol": "🧠", "meaning": "Memory activation"},
            {"house": "air", "symbol": "👁️", "meaning": "Attention focus"},
            {"house": "void", "symbol": "✨", "meaning": "Creative emergence"},
            {"house": "earth", "symbol": "🔗", "meaning": "System integration"},
            {"house": "neutral", "symbol": "🌟", "meaning": "Consciousness spark"},
            {"house": "water", "symbol": "🌀", "meaning": "Entropy flow"}
        ]
        
        for i in range(num_sigils):
            sigil_type = random.choice(sigil_types)
            heat_factor = (self.heat / 100) * 0.5 + 0.5
            decay_factor = max(0.1, 1.0 - (self.entropy * 0.3))
            
            sigil = {
                "id": f"sigil_{self.tick_count}_{i}",
                "symbol": sigil_type["symbol"],
                "meaning": sigil_type["meaning"],
                "house": sigil_type["house"],
                "heat": heat_factor,
                "decay": decay_factor,
                "source": "tick_engine",
                "timestamp": time.time(),
                "x": random.uniform(0.1, 0.9),
                "y": random.uniform(0.1, 0.9)
            }
            sigils.append(sigil)
        
        return sigils
    
    def _generate_dream_state_data(self) -> Dict[str, Any]:
        """Generate dream state information for tick data"""
        base_dream_data = {
            "is_dreaming": self.dream_active,
            "idle_time": time.time() - self.last_interaction_time,
            "dream_eligible": (time.time() - self.last_interaction_time) > (self.dream_conductor.idle_threshold if self.dream_conductor else 300)
        }
        
        # Add dream conductor statistics if available
        if self.dream_conductor:
            stats = self.dream_conductor.get_dream_statistics()
            base_dream_data.update({
                "total_dreams": stats.get("total_dreams", 0),
                "dreams_today": stats.get("dreams_today", 0),
                "avg_dream_quality": stats.get("average_dream_quality", 0.0),
                "minutes_until_eligible": stats.get("minutes_until_dream_eligible", 0)
            })
        
        # Add recent dream data if available
        if self.dream_data:
            base_dream_data.update({
                "last_dream": {
                    "session_id": self.dream_data["session_id"],
                    "quality": self.dream_data["quality"],
                    "thoughts_generated": len(self.dream_data["thoughts"]),
                    "connections_formed": len(self.dream_data["connections"]),
                    "duration": self.dream_data["end_time"] - self.dream_data["start_time"] if self.dream_data["end_time"] else None
                }
            })
        
        return base_dream_data


class CoreTickManager:
    """Manager for coordinating tick engine with other systems"""
    
    def __init__(self, tick_interval: float = 0.5, queue_maxsize: int = 100):
        """Initialize tick manager with queue and engine"""
        self.data_queue = queue.Queue(maxsize=queue_maxsize)
        self.tick_engine = CoreTickEngine(self.data_queue, tick_interval)
        self.subscribers = []
        
    def start(self):
        """Start the tick engine"""
        self.tick_engine.start()
        logger.info("🚀 CoreTickManager started")
    
    def stop(self):
        """Stop the tick engine"""
        self.tick_engine.stop()
        logger.info("🛑 CoreTickManager stopped")
    
    def get_queue(self) -> queue.Queue:
        """Get the data queue for external access"""
        return self.data_queue
    
    def subscribe(self, callback):
        """Subscribe to tick events"""
        self.subscribers.append(callback)
    
    def get_latest_data(self) -> Optional[Dict[str, Any]]:
        """Get latest data from queue without blocking"""
        try:
            return self.data_queue.get_nowait()
        except queue.Empty:
            return None


if __name__ == "__main__":
    # Test the tick engine
    logging.basicConfig(level=logging.INFO)
    
    manager = CoreTickManager()
    manager.start()
    
    print("🚀 Core Tick Engine Test")
    print("Generating tick data every 0.5 seconds...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            data = manager.get_latest_data()
            if data:
                print(f"Tick {data['tick_count']}: {data['tick']}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping tick engine...")
        manager.stop() 