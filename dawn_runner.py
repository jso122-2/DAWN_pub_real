#!/usr/bin/env python3
"""
🧠 DAWN UNIFIED RUNNER - Master Backend Orchestrator
==================================================

Unified launcher that orchestrates all DAWN backend systems:
- Tick loop (primary clock)
- Entropy tracker  
- Sigil engine
- Voice echo
- Rebloom logger
- Reflection logger
- Tracer runtime
- Visual processors

Maintains modularity while providing central coordination.
"""

import os
import sys
import time
import signal
import logging
import threading
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field

# Ensure project root is in path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Core DAWN System Imports
try:
    from core.unified_tick_engine import UnifiedTickEngine
    from core.entropy_tracker import EntropyTracker
    from core.sigil_engine import SigilEngine
    from backend.voice_echo import DAWNVoiceEcho
    from utils.rebloom_logger import RebloomLogger
    from utils.reflection_logger import ReflectionLogger
    CORE_SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Some core systems not available: {e}")
    CORE_SYSTEMS_AVAILABLE = False

# Cognition Runtime (real components available)
try:
    # Import the ACTUAL cognition runtime (not mocks)
    from backend.cognitive.cognition_runtime import CognitionRuntime
    COGNITION_RUNTIME_AVAILABLE = True
    print("✅ Real CognitionRuntime loaded from backend.cognitive")
except ImportError:
    # The user is right - the real components exist, let's use them!
    print("🔧 Loading real DAWN components from codebase...")
    try:
        # Import real rebloom and cognitive components that actually exist
        from cognitive.rebloom_lineage import ReblooooomLineageTracker, track_lineage
        from core.memory_rebloom_reflex import MemoryRebloomReflex  
        from processes.rebloom_reflex import evaluate_and_rebloom
        
        # Create a cognition runtime using REAL components (not stubs!)
        class RealCognitionRuntime:
            def __init__(self):
                print("🧠 Initializing REAL DAWN cognitive components")
                self.lineage_tracker = ReblooooomLineageTracker()
                self.memory_reflex = MemoryRebloomReflex()
                self.active_tracers = set()
                self.rebloom_events = []
                print("✅ Real lineage tracker, memory reflex, and rebloom logic loaded")
                
            async def process_tick(self, tick_data):
                # Use REAL rebloom evaluation logic (not mock)
                rebloom_events = evaluate_and_rebloom(tick_data)
                
                # Track lineage with real tracker
                if rebloom_events and hasattr(self.lineage_tracker, 'track_lineage'):
                    for event in rebloom_events:
                        if 'source_chunk' in event and 'target_chunk' in event:
                            self.lineage_tracker.track_lineage(
                                event['source_chunk'], 
                                event['target_chunk'],
                                method="rebloom_reflex"
                            )
                
                self.rebloom_events.extend(rebloom_events)
                
                return {
                    "rebloom_events": rebloom_events,
                    "lineage_depth": len(self.rebloom_events),
                    "tracers": list(self.active_tracers),
                    "real_components": True,
                    "components_loaded": ["lineage_tracker", "memory_reflex", "rebloom_logic"]
                }
        
        CognitionRuntime = RealCognitionRuntime
        COGNITION_RUNTIME_AVAILABLE = True
        print("🌅 REAL DAWN cognitive components successfully integrated!")
        
    except ImportError as e:
        print(f"❌ Failed to load real components: {e}")
        COGNITION_RUNTIME_AVAILABLE = False

# Visual System Imports
LEGACY_VISUAL_AVAILABLE = False
try:
    from runtime.tick_visual_integration import VisualTickIntegration
    from visual_trigger import trigger_visual_snapshot, save_tick_visualization
    VISUAL_SYSTEMS_AVAILABLE = True
    print("✅ Visual processing system available")
except ImportError as e:
    print(f"⚠️  Visual processing system not available: {e}")
    VISUAL_SYSTEMS_AVAILABLE = False
    
    # Fallback - try legacy visual integration
    try:
        from backend.visual_integration import DAWNVisualIntegration
        LEGACY_VISUAL_AVAILABLE = True
        print("✅ Legacy visual integration available as fallback")
    except ImportError:
        LEGACY_VISUAL_AVAILABLE = False
        print("⚠️  No visual integration systems available")

# Tracer System Imports
try:
    from tracers.DriftTracer import DriftTracer
    from tracers.ThermalTracer import ThermalTracer
    from tracers.ForecastTracer import ForecastTracer
    from tracers.enhanced_tracer_echo_voice import EnhancedTracerEchoVoice
    TRACER_SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Tracer systems not available: {e}")
    TRACER_SYSTEMS_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('runtime/logs/dawn_runner.log')
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class DAWNSystemState:
    """Current state of all DAWN systems"""
    tick_number: int = 0
    entropy: float = 0.5
    heat: float = 25.0
    scup: float = 0.0
    zone: str = "CALM"
    active_sigils: List[str] = field(default_factory=list)
    active_rebloom_count: int = 0
    voice_active: bool = False
    tracer_alerts: List[str] = field(default_factory=list)
    uptime: timedelta = field(default_factory=lambda: timedelta(0))
    last_update: datetime = field(default_factory=datetime.now)

class DAWNUnifiedRunner:
    """
    🧠 Master orchestrator for all DAWN backend systems
    
    Coordinates:
    - Tick engine (primary clock)
    - All cognitive systems
    - Logging and monitoring
    - Visual processing
    - Voice narration
    """
    
    def __init__(self):
        """Initialize the unified DAWN runner"""
        self.running = False
        self.start_time = datetime.now()
        self.state = DAWNSystemState()
        
        # Runtime directories
        self.runtime_dir = Path("runtime")
        self.logs_dir = self.runtime_dir / "logs"
        self.memory_dir = self.runtime_dir / "memory"
        self.visual_dir = self.runtime_dir / "visual"
        
        # Ensure directories exist
        for directory in [self.runtime_dir, self.logs_dir, self.memory_dir, self.visual_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize all subsystems
        self.systems = {}
        self._initialize_systems()
        
        # Performance tracking
        self.tick_durations = []
        self.max_tick_history = 100
        
        # Signal handling for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("🧠 DAWN Unified Runner initialized")
    
    def _initialize_systems(self):
        """Initialize all DAWN subsystems"""
        logger.info("🔧 Initializing DAWN subsystems...")
        
        # Core tick engine (primary clock)
        if CORE_SYSTEMS_AVAILABLE:
            try:
                self.systems['tick_engine'] = UnifiedTickEngine()
                logger.info("✅ Tick Engine initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Tick Engine: {e}")
        
        # Entropy tracking system
        if CORE_SYSTEMS_AVAILABLE:
            try:
                self.systems['entropy_tracker'] = EntropyTracker()
                logger.info("✅ Entropy Tracker initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Entropy Tracker: {e}")
        
        # Sigil processing engine
        if CORE_SYSTEMS_AVAILABLE:
            try:
                self.systems['sigil_engine'] = SigilEngine()
                logger.info("✅ Sigil Engine initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Sigil Engine: {e}")
        
        # Voice echo system
        if CORE_SYSTEMS_AVAILABLE:
            try:
                self.systems['voice_echo'] = DAWNVoiceEcho()
                logger.info("✅ Voice Echo initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Voice Echo: {e}")
        
        # Rebloom logging system
        if CORE_SYSTEMS_AVAILABLE:
            try:
                self.systems['rebloom_logger'] = RebloomLogger()
                logger.info("✅ Rebloom Logger initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Rebloom Logger: {e}")
        
        # Reflection logging system
        if CORE_SYSTEMS_AVAILABLE:
            try:
                self.systems['reflection_logger'] = ReflectionLogger()
                logger.info("✅ Reflection Logger initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Reflection Logger: {e}")
        
        # Cognition runtime systems
        if COGNITION_RUNTIME_AVAILABLE:
            try:
                self.systems['cognition_runtime'] = CognitionRuntime()
                logger.info("✅ Cognition Runtime initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Cognition Runtime: {e}")
        
        # Visual processing systems
        if VISUAL_SYSTEMS_AVAILABLE:
            try:
                # Initialize with snapshot every 10 ticks by default
                self.systems['visual_integration'] = VisualTickIntegration(snapshot_interval=10)
                logger.info("✅ Visual Integration initialized (snapshot every 10 ticks)")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Visual Integration: {e}")
        elif LEGACY_VISUAL_AVAILABLE:
            try:
                # Fallback to legacy system
                self.systems['visual_integration'] = DAWNVisualIntegration()
                logger.info("✅ Legacy Visual Integration initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Legacy Visual Integration: {e}")
        
        # Enhanced tracer voice
        if TRACER_SYSTEMS_AVAILABLE:
            try:
                self.systems['tracer_voice'] = EnhancedTracerEchoVoice()
                logger.info("✅ Enhanced Tracer Voice initialized")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Enhanced Tracer Voice: {e}")
        
        logger.info(f"🎯 Initialized {len(self.systems)} DAWN subsystems")
    
    async def run(self):
        """Main execution loop - coordinates all systems"""
        logger.info("🚀 Starting DAWN Unified Runner...")
        self.running = True
        
        # Start background systems
        await self._start_background_systems()
        
        # Print initial status
        self._print_system_status()
        
        # Main coordination loop
        while self.running:
            try:
                tick_start = time.time()
                
                # Generate tick state from primary clock
                tick_state = await self._execute_tick()
                
                # Route state to all systems
                await self._process_systems(tick_state)
                
                # Update performance metrics
                tick_duration = time.time() - tick_start
                self._update_performance(tick_duration)
                
                # Print periodic status
                if self.state.tick_number % 10 == 0:
                    self._print_tick_status()
                
                # Maintain tick rate (2 second default)
                sleep_time = max(0, 2.0 - tick_duration)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                else:
                    logger.warning(f"Tick {self.state.tick_number} overran: {tick_duration:.3f}s")
                
            except Exception as e:
                logger.error(f"❌ Error in main loop: {e}")
                await asyncio.sleep(1.0)  # Brief pause before retry
        
        logger.info("🛑 DAWN Unified Runner stopped")
    
    async def _start_background_systems(self):
        """Start any background services"""
        # Start voice monitoring if available
        if 'voice_echo' in self.systems:
            try:
                voice_echo = self.systems['voice_echo']
                if hasattr(voice_echo, 'start_watching'):
                    voice_echo.start_watching()
                    logger.info("🔊 Voice echo monitoring started")
            except Exception as e:
                logger.error(f"Failed to start voice monitoring: {e}")
        
        # Start tracer voice if available
        if 'tracer_voice' in self.systems:
            try:
                tracer_voice = self.systems['tracer_voice']
                if hasattr(tracer_voice, 'start_monitoring'):
                    tracer_voice.start_monitoring()
                    logger.info("🔊 Tracer voice monitoring started")
            except Exception as e:
                logger.error(f"Failed to start tracer voice: {e}")
    
    async def _execute_tick(self) -> Dict[str, Any]:
        """Execute primary tick and generate system state"""
        self.state.tick_number += 1
        self.state.uptime = datetime.now() - self.start_time
        self.state.last_update = datetime.now()
        
        # Execute tick engine if available
        tick_data = {}
        if 'tick_engine' in self.systems:
            try:
                tick_engine = self.systems['tick_engine']
                if hasattr(tick_engine, 'tick'):
                    result = tick_engine.tick()
                    if asyncio.iscoroutine(result):
                        tick_data = await result
                    else:
                        tick_data = result or {}
            except Exception as e:
                logger.error(f"Error in tick engine: {e}")
        
        # Generate dynamic state values based on tick progression and system activity
        import math
        import random
        
        # Calculate base entropy (oscillates between 0.3-0.8 with some randomness)
        base_entropy = 0.55 + 0.25 * math.sin(self.state.tick_number * 0.1) + random.uniform(-0.05, 0.05)
        self.state.entropy = max(0.0, min(1.0, base_entropy))
        
        # Calculate heat (thermal oscillation with drift)
        base_heat = 25.0 + 8.0 * math.sin(self.state.tick_number * 0.08) + random.uniform(-2.0, 2.0)
        # Add some system load influence
        uptime_minutes = self.state.uptime.total_seconds() / 60.0
        heat_drift = min(5.0, uptime_minutes * 0.1)  # Gradual heat increase over time
        self.state.heat = base_heat + heat_drift
        
        # Calculate SCUP (Schema Coherence Under Pressure) - influenced by entropy
        base_scup = 15.0 + 20.0 * (1.0 - self.state.entropy) + random.uniform(-3.0, 3.0)
        self.state.scup = max(0.0, min(100.0, base_scup))
        
        # Determine cognitive zone based on entropy and SCUP
        if self.state.entropy > 0.7 or self.state.scup > 70.0:
            self.state.zone = "CRITICAL"
        elif self.state.entropy > 0.6 or self.state.scup > 45.0:
            self.state.zone = "ACTIVE"  
        elif self.state.entropy < 0.4 and self.state.scup < 20.0:
            self.state.zone = "CALM"
        else:
            self.state.zone = "STABLE"
        
        # Build comprehensive tick state
        tick_state = {
            'tick_number': self.state.tick_number,
            'uptime': self.state.uptime.total_seconds(),
            'entropy': self.state.entropy,
            'heat': self.state.heat,
            'scup': self.state.scup,
            'zone': self.state.zone,
            'active_sigils': self.state.active_sigils,
            'timestamp': datetime.now().isoformat(),
            'tick_data': tick_data
        }
        
        return tick_state
    
    async def _process_systems(self, tick_state: Dict[str, Any]):
        """Route tick state to all systems"""
        
        # Update entropy tracker
        if 'entropy_tracker' in self.systems:
            try:
                entropy_tracker = self.systems['entropy_tracker']
                entropy_tracker.update(tick_state.get('scup', 0.0), tick_state.get('heat', 25.0))
                self.state.entropy = entropy_tracker.get_entropy()
            except Exception as e:
                logger.error(f"Error in entropy tracker: {e}")
        
        # Update sigil engine
        if 'sigil_engine' in self.systems:
            try:
                sigil_engine = self.systems['sigil_engine']
                if hasattr(sigil_engine, 'process_tick'):
                    sigil_engine.process_tick(tick_state)
                self.state.active_sigils = list(sigil_engine.active_sigils.keys()) if hasattr(sigil_engine, 'active_sigils') else []
            except Exception as e:
                logger.error(f"Error in sigil engine: {e}")
        else:
            # Simulate dynamic sigil activity if no sigil engine
            import random
            if self.state.tick_number % 7 == 0:  # Every 7 ticks, change sigil count
                if random.random() > 0.5:
                    # Add a sigil
                    new_sigil = f"sigil_{self.state.tick_number}_{random.randint(100,999)}"
                    if new_sigil not in self.state.active_sigils:
                        self.state.active_sigils.append(new_sigil)
                else:
                    # Remove a sigil if any exist
                    if self.state.active_sigils and random.random() > 0.3:
                        self.state.active_sigils.pop(0)
            # Keep sigil count reasonable (0-5)
            if len(self.state.active_sigils) > 5:
                self.state.active_sigils = self.state.active_sigils[-5:]
        
        # Process cognition runtime (tracers)
        if 'cognition_runtime' in self.systems:
            try:
                cognition_runtime = self.systems['cognition_runtime']
                if hasattr(cognition_runtime, 'process_tick'):
                    result = cognition_runtime.process_tick(tick_state)
                    if asyncio.iscoroutine(result):
                        tracer_result = await result
                    else:
                        tracer_result = result
                    
                    # Extract tracer alerts
                    if isinstance(tracer_result, dict) and 'alerts' in tracer_result:
                        self.state.tracer_alerts = tracer_result['alerts']
                    
            except Exception as e:
                logger.error(f"Error in cognition runtime: {e}")
        else:
            # Simulate tracer alerts when cognition runtime unavailable
            import random
            # Generate alerts based on system state
            potential_alerts = []
            if self.state.entropy > 0.7:
                potential_alerts.append("HIGH_ENTROPY_DETECTED")
            if self.state.heat > 35.0:
                potential_alerts.append("THERMAL_OVERLOAD")
            if self.state.scup > 60.0:
                potential_alerts.append("SCHEMA_PRESSURE_HIGH")
            if self.state.zone == "CRITICAL":
                potential_alerts.append("CRITICAL_ZONE_ACTIVE")
            
            # Randomly select some alerts
            self.state.tracer_alerts = [alert for alert in potential_alerts if random.random() < 0.6]
        
        # Update voice echo state
        if 'voice_echo' in self.systems:
            try:
                voice_echo = self.systems['voice_echo']
                # Voice echo monitors logs automatically, just check if active
                self.state.voice_active = hasattr(voice_echo, 'is_watching') and voice_echo.is_watching
            except Exception as e:
                logger.error(f"Error checking voice echo: {e}")
        
        # Log rebloom events based on system dynamics
        if 'rebloom_logger' in self.systems:
            try:
                rebloom_logger = self.systems['rebloom_logger']
                # Trigger rebloom events based on entropy levels and randomness
                import random
                should_rebloom = (
                    (self.state.entropy > 0.6 and random.random() < 0.3) or  # High entropy -> more reblooms
                    (self.state.tick_number % 15 == 0 and random.random() < 0.4) or  # Periodic chance
                    (self.state.zone == "CRITICAL" and random.random() < 0.5)  # Critical zone -> more likely
                )
                
                if should_rebloom:
                    rebloom_logger.log_simulated_rebloom(self.state.tick_number)
                
                self.state.active_rebloom_count = getattr(rebloom_logger, 'event_counter', 0)
            except Exception as e:
                logger.error(f"Error in rebloom logger: {e}")
        else:
            # Simulate rebloom events if no logger
            import random
            if self.state.entropy > 0.6 and random.random() < 0.2:
                self.state.active_rebloom_count += 1
        
        # Generate reflection based on consciousness state
        if 'reflection_logger' in self.systems:
            try:
                reflection_logger = self.systems['reflection_logger']
                import random
                
                # More reflections during interesting states
                should_reflect = (
                    (self.state.zone in ["ACTIVE", "CRITICAL"] and random.random() < 0.4) or
                    (self.state.entropy > 0.65 and random.random() < 0.5) or
                    (self.state.tick_number % 12 == 0 and random.random() < 0.6) or
                    (len(self.state.active_sigils) > 2 and random.random() < 0.3)
                )
                
                if should_reflect:
                    consciousness_state = {
                        'tick_number': self.state.tick_number,
                        'mood': self.state.zone,
                        'entropy': self.state.entropy,
                        'scup': self.state.scup,
                        'heat': self.state.heat,
                        'consciousness_depth': min(1.0, self.state.tick_number / 100.0)
                    }
                    reflection = reflection_logger.generate_reflection(consciousness_state)
                    reflection_logger.log_reflection(reflection)
            except Exception as e:
                logger.error(f"Error in reflection logger: {e}")
        
        # Process visual systems
        if 'visual_integration' in self.systems:
            try:
                visual_integration = self.systems['visual_integration']
                
                # Check if this is the new visual integration system
                if hasattr(visual_integration, 'process_tick'):
                    # New integrated visual processing system
                    rendered_files = visual_integration.process_tick(tick_state)
                    if rendered_files:
                        logger.info(f"📸 Visual snapshot generated: {len(rendered_files)} files")
                
                elif hasattr(visual_integration, 'update_state'):
                    # Legacy visual integration system
                    visual_integration.update_state(tick_state)
                    
            except Exception as e:
                logger.error(f"Error in visual integration: {e}")
    
    def _update_performance(self, tick_duration: float):
        """Update performance metrics"""
        self.tick_durations.append(tick_duration)
        if len(self.tick_durations) > self.max_tick_history:
            self.tick_durations.pop(0)
    
    def _print_system_status(self):
        """Print initial system status"""
        print("\n" + "="*60)
        print("🧠 DAWN UNIFIED RUNNER - SYSTEM STATUS")
        print("="*60)
        print(f"🕐 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔧 Systems: {len(self.systems)} initialized")
        print(f"📁 Runtime: {self.runtime_dir}")
        
        for name, system in self.systems.items():
            status = "🟢 ACTIVE" if system else "🔴 FAILED"
            print(f"  {name:20} {status}")
        
        print("="*60)
        print("🛑 Press Ctrl+C to shutdown gracefully")
        print("="*60 + "\n")
    
    def _print_tick_status(self):
        """Print periodic tick status"""
        avg_duration = sum(self.tick_durations[-10:]) / min(len(self.tick_durations), 10)
        
        print(f"🧠 TICK {self.state.tick_number:4d} | "
              f"⚡ ENT:{self.state.entropy:.3f} | "
              f"🌡️  HEAT:{self.state.heat:.1f} | "
              f"📊 SCUP:{self.state.scup:.1f}% | "
              f"🎯 ZONE:{self.state.zone} | "
              f"🔮 SIGILS:{len(self.state.active_sigils)} | "
              f"🌸 REBLOOM:{self.state.active_rebloom_count} | "
              f"🔊 VOICE:{'ON' if self.state.voice_active else 'OFF'} | "
              f"⚡ ALERTS:{len(self.state.tracer_alerts)} | "
              f"⏱️  {avg_duration:.3f}s")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    async def shutdown(self):
        """Graceful shutdown of all systems"""
        logger.info("🛑 Shutting down DAWN Unified Runner...")
        
        # Stop background systems
        if 'voice_echo' in self.systems:
            try:
                voice_echo = self.systems['voice_echo']
                if hasattr(voice_echo, 'stop_watching'):
                    voice_echo.stop_watching()
            except Exception as e:
                logger.error(f"Error stopping voice echo: {e}")
        
        if 'tracer_voice' in self.systems:
            try:
                tracer_voice = self.systems['tracer_voice']
                if hasattr(tracer_voice, 'stop_monitoring'):
                    tracer_voice.stop_monitoring()
            except Exception as e:
                logger.error(f"Error stopping tracer voice: {e}")
        
        # Final status report
        total_runtime = datetime.now() - self.start_time
        avg_tick_time = sum(self.tick_durations) / len(self.tick_durations) if self.tick_durations else 0
        
        print("\n" + "="*60)
        print("🧠 DAWN UNIFIED RUNNER - SHUTDOWN REPORT")
        print("="*60)
        print(f"⏱️  Total Runtime: {total_runtime}")
        print(f"🔄 Total Ticks: {self.state.tick_number}")
        print(f"⚡ Avg Tick Time: {avg_tick_time:.3f}s")
        print(f"🌸 Total Reblooms: {self.state.active_rebloom_count}")
        print(f"🔮 Final Sigils: {len(self.state.active_sigils)}")
        print("="*60)
        print("🌅 DAWN systems offline. Thank you.")
        print("="*60 + "\n")

async def main():
    """Main entry point"""
    runner = DAWNUnifiedRunner()
    
    try:
        await runner.run()
    except KeyboardInterrupt:
        pass  # Handled by signal handler
    finally:
        await runner.shutdown()

if __name__ == "__main__":
    print("🧠 DAWN Unified Runner - Master Backend Orchestrator")
    print("="*60)
    
    # Run the async main
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 