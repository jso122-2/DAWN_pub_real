#!/usr/bin/env python3
"""
DAWN Core Runtime - Unified Cognitive System Loop
Integrates all DAWN subsystems into a coherent, self-aware runtime.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import asyncio
import random

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Ensure runtime directories exist
runtime_dir = Path("runtime")
logs_dir = runtime_dir / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / 'dawn_core.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DAWN_Core')

# Import DAWN subsystems with fallbacks
try:
    from cognitive.forecasting_engine import DAWNForecastingEngine, get_forecasting_engine
    from cognitive.forecasting_models import Passion, Acquaintance
    from core.memory.memory_routing_system import MemoryRouter
    from core.memory.cognitive_router import CognitiveRouter
    from cognitive.symbolic_router import SymbolicRouter
    COGNITIVE_AVAILABLE = True
    logger.info("✅ DAWN cognitive systems loaded")
except ImportError as e:
    logger.warning(f"⚠️ Import warning: {e}")
    logger.info("🔧 Using fallback implementations")
    COGNITIVE_AVAILABLE = False
    
    # Fallback implementations
    class Passion:
        def __init__(self, intensity=0.5, topic="general", emotional_valence=0.5, time_decay=0.1):
            self.intensity = intensity
            self.topic = topic
            self.emotional_valence = emotional_valence
            self.time_decay = time_decay
    
    class Acquaintance:
        def __init__(self, familiarity=0.5, emotional_charge=0.5, trust_level=0.5, interaction_history=None):
            self.familiarity = familiarity
            self.emotional_charge = emotional_charge
            self.trust_level = trust_level
            self.interaction_history = interaction_history or []
    
    def compute_forecast_fallback(passion, acquaintance, current_entropy, context=""):
        """Fallback forecast function."""
        import random
        import time
        
        # Add realistic processing time
        time.sleep(0.001 + random.random() * 0.005)  # 1-6ms of processing
        
        confidence = max(0.1, min(0.9, 0.7 - current_entropy * 0.5))
        risk_level = min(0.8, current_entropy + random.random() * 0.3)
        
        return {
            'confidence': confidence,
            'limit_horizon': 0.3 + random.random() * 0.5,
            'risk_level': risk_level,
            'emotional_intensity': passion.emotional_valence if hasattr(passion, 'emotional_valence') else 0.5,
            'commentary': f"Synthetic forecast generated for {context}",
            'forecast_factors': {
                'passion_intensity': passion.intensity if hasattr(passion, 'intensity') else 0.5,
                'acquaintance_familiarity': acquaintance.familiarity if hasattr(acquaintance, 'familiarity') else 0.5
            }
        }
    
    def generate_commentary_fallback(state):
        """Fallback commentary function."""
        zone = state.get('zone', 'CALM')
        entropy = state.get('entropy', 0.5)
        tick = state.get('tick_count', 0)
        
        if zone == "CRITICAL":
            return f"🚨 Critical state detected at tick {tick} - system stabilization required"
        elif zone == "CHAOTIC":
            return f"🌪️ Chaotic dynamics emerging - entropy at {entropy:.2f}"
        elif zone == "ACTIVE":
            return f"⚡ Active processing mode - cognitive patterns flowing"
        else:
            return f"🧘 Calm reflection state - deep introspection at tick {tick}"
    
# Import snapshot exporter for state management
try:
    # Try to import from the attached file location first
    import sys
    import importlib.util
    snapshot_file = Path(__file__).parent / "snapshot_exporter.py"
    if snapshot_file.exists():
        spec = importlib.util.spec_from_file_location("snapshot_exporter", snapshot_file)
        snapshot_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(snapshot_module)
        DAWNSnapshotExporter = snapshot_module.DAWNSnapshotExporter
        logger.info("✅ Snapshot exporter loaded from file")
    else:
        from dawn_core.snapshot_exporter import DAWNSnapshotExporter
        logger.info("✅ Snapshot exporter loaded from module")
except ImportError:
    logger.warning("⚠️ Snapshot exporter not found, using mock")
    DAWNSnapshotExporter = None

# Import existing DAWN systems if available
try:
    from core.consciousness_core import DAWNConsciousness
    from pulse.pulse_loader import load_pulse_system
    from core.tick.tick import start_engine, stop_engine
    EXISTING_DAWN_AVAILABLE = True
    logger.info("✅ Existing DAWN systems available")
except ImportError:
    EXISTING_DAWN_AVAILABLE = False
    logger.info("🔧 Using standalone cognitive engine")


class DAWNCognitiveEngine:
    """
    Unified DAWN cognitive engine that orchestrates all subsystems.
    """
    
    def __init__(self):
        """Initialize the cognitive engine with all subsystems."""
        self.tick_count = 0
        self.start_time = datetime.now()
        self.running = False
        
        # Initialize runtime directories
        self.runtime_dir = Path("runtime")
        self.logs_dir = self.runtime_dir / "logs"
        self.state_dir = self.runtime_dir / "state"
        self.memory_dir = self.runtime_dir / "memories"
        
        for dir_path in [self.runtime_dir, self.logs_dir, self.state_dir, self.memory_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize subsystems
        self._initialize_subsystems()
        
        # State tracking
        self.current_entropy = 0.3
        self.current_heat = 25.0
        self.current_zone = "CALM"
        self.forecast_cache = None
        self.last_forecast_time = None
        self.active_sigils = []  # Track active sigils
        self.pulse_state = {}    # Track pulse state
        
        logger.info("🧠 DAWN Cognitive Engine initialized")
    
    def _initialize_subsystems(self):
        """Initialize all cognitive subsystems."""
        
        # 1. Memory Systems
        try:
            if COGNITIVE_AVAILABLE:
                self.memory_router = MemoryRouter()
                self.cognitive_router = CognitiveRouter()
                self._symbolic_router = SymbolicRouter(consciousness_core=self)
                # Initialize real forecasting engine
                self.forecasting_engine = get_forecasting_engine(consciousness_core=self)
            else:
                self.memory_router = None
                self.cognitive_router = None
                self._symbolic_router = None
                self.forecasting_engine = None
            logger.info("✅ Memory systems initialized")
        except Exception as e:
            logger.error(f"❌ Memory system error: {e}")
            self.memory_router = None
            self.cognitive_router = None
            self._symbolic_router = None
            self.forecasting_engine = None
        
        # 2. Snapshot Exporter
        try:
            if DAWNSnapshotExporter:
                self.snapshot_exporter = DAWNSnapshotExporter(dawn_engine=self)
                logger.info("✅ Snapshot exporter initialized")
            else:
                self.snapshot_exporter = None
                logger.info("⚠️ Snapshot exporter not available")
        except Exception as e:
            logger.error(f"❌ Snapshot exporter error: {e}")
            self.snapshot_exporter = None
        
        # 3. Existing DAWN Integration
        self.dawn_consciousness = None
        if EXISTING_DAWN_AVAILABLE:
            try:
                self._initialize_existing_dawn()
            except Exception as e:
                logger.warning(f"⚠️ Existing DAWN integration failed: {e}")
        
        # 4. Load mock memory data
        self._load_initial_memories()
    
    async def _initialize_existing_dawn(self):
        """Initialize integration with existing DAWN systems."""
        try:
            # Load pulse system
            pulse_result = await load_pulse_system()
            if pulse_result and len(pulse_result) >= 4:
                pulse, tick_thermal_update, add_heat, scup_tracker = pulse_result
                
                # Initialize consciousness
                self.dawn_consciousness = DAWNConsciousness(
                    pulse=pulse,
                    tick_thermal_update=tick_thermal_update,
                    add_heat=add_heat,
                    scup_tracker=scup_tracker
                )
                
                logger.info("✅ Existing DAWN consciousness integrated")
            
        except Exception as e:
            logger.error(f"❌ DAWN integration error: {e}")
    
    def _load_initial_memories(self):
        """Load or create initial memory chunks."""
        memory_file = self.memory_dir / "memory_chunks.jsonl"
        
        if not memory_file.exists():
            # Create mock memories
            mock_memories = [
                {
                    "timestamp": datetime.now().isoformat(),
                    "speaker": "system",
                    "content": "DAWN cognitive engine initialized",
                    "topic": "initialization",
                    "sigils": ["🧠", "✨"],
                    "pulse_state": {"entropy": 0.3, "heat": 25.0, "zone": "CALM"}
                },
                {
                    "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                    "speaker": "user", 
                    "content": "Beginning consciousness exploration",
                    "topic": "consciousness",
                    "sigils": ["🔍", "💫"],
                    "pulse_state": {"entropy": 0.4, "heat": 30.0, "zone": "ACTIVE"}
                }
            ]
            
            with open(memory_file, 'w') as f:
                for memory in mock_memories:
                    f.write(json.dumps(memory) + '\n')
            
            logger.info("📝 Created initial memory chunks")
    
    def get_latest_memory_chunk(self) -> Dict[str, Any]:
        """Get the latest memory chunk or create a mock one."""
        memory_file = self.memory_dir / "memory_chunks.jsonl"
        
        if memory_file.exists():
            try:
                with open(memory_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        return json.loads(lines[-1].strip())
            except Exception as e:
                logger.warning(f"⚠️ Error reading memory: {e}")
        
        # Create mock memory chunk
        return {
            "timestamp": datetime.now().isoformat(),
            "speaker": "system",
            "content": f"Cognitive tick {self.tick_count} processing",
            "topic": "cognition",
            "sigils": ["🧠", "⚡"],
            "pulse_state": {
                "entropy": self.current_entropy,
                "heat": self.current_heat,
                "zone": self.current_zone
            }
        }
    
    def extract_passion_acquaintance(self, memory_chunk: Dict[str, Any]) -> tuple:
        """Extract or simulate Passion and Acquaintance from memory."""
        try:
            # Extract from content
            content = memory_chunk.get("content", "")
            topic = memory_chunk.get("topic", "general")
            
            # Create Passion based on content analysis
            passion_intensity = len(content) / 200.0  # Simple heuristic
            passion_intensity = min(1.0, max(0.1, passion_intensity))
            
            passion = Passion(
                direction=topic,
                intensity=passion_intensity,
                fluidity=0.3 + random.random() * 0.4  # Moderate fluidity
            )
            
            # Create Acquaintance based on speaker
            speaker = memory_chunk.get("speaker", "unknown")
            
            # Create event log for acquaintance
            event_log = [f"interaction_with_{speaker}", f"topic_{topic}"]
            acquaintance = Acquaintance(event_log=event_log)
            
            return passion, acquaintance
            
        except Exception as e:
            logger.warning(f"⚠️ Error extracting passion/acquaintance: {e}")
            
            # Fallback to random values
            passion = Passion(
                direction="general",
                intensity=0.3 + random.random() * 0.4,
                fluidity=0.5
            )
            
            acquaintance = Acquaintance(
                event_log=["general_interaction", "fallback_event"]
            )
            
            return passion, acquaintance
    
    def _convert_risk_level_to_numeric(self, risk_level):
        """Convert string risk level to numeric value."""
        if isinstance(risk_level, (int, float)):
            return float(risk_level)
        
        if isinstance(risk_level, str):
            risk_mapping = {
                "low": 0.2,
                "medium": 0.5, 
                "high": 0.7,
                "critical": 0.9
            }
            return risk_mapping.get(risk_level.lower(), 0.3)
        
        return 0.3  # Default fallback

    def generate_commentary(self, state):
        """Generate commentary using available systems or fallback."""
        if COGNITIVE_AVAILABLE:
            try:
                from cognitive.symbolic_anatomy import FractalHeart, SomaCoil, GlyphLung
                # Create temporary organs for commentary
                heart = FractalHeart()
                heart.pulse(state.get('entropy', 0.5), "cognitive")
                
                zone = state.get('zone', 'CALM')
                tick = state.get('tick_count', 0)
                
                if zone == "CRITICAL":
                    return f"💗 Heart resonates with urgency - stabilization protocols engaging at tick {tick}"
                elif zone == "CHAOTIC":
                    return f"🌀 Coil paths fragmenting - entropy patterns reorganizing"
                elif zone == "ACTIVE":
                    return f"🫁 Lung breathing deeply - cognitive flow patterns active"
                else:
                    return f"💫 Organs in harmony - peaceful contemplation at tick {tick}"
            except Exception:
                return generate_commentary_fallback(state)
        else:
            return generate_commentary_fallback(state)

    def update_pulse_state(self, forecast: Dict[str, Any]):
        """Update internal pulse state based on forecast."""
        confidence = forecast.get('confidence', 0.5)
        limit_horizon = forecast.get('limit_horizon', 0.5)
        risk_level_raw = forecast.get('risk_level', 0.3)
        
        # Convert risk level to numeric value
        risk_level = self._convert_risk_level_to_numeric(risk_level_raw)
        
        # Update entropy based on risk and confidence
        entropy_change = (risk_level - confidence) * 0.1
        self.current_entropy = max(0.0, min(1.0, self.current_entropy + entropy_change))
        
        # Update heat based on activity
        heat_change = (1.0 - limit_horizon) * 5.0 - 2.0  # More activity = more heat
        self.current_heat = max(10.0, min(80.0, self.current_heat + heat_change))
        
        # Update zone based on entropy
        if self.current_entropy > 0.8:
            self.current_zone = "CRITICAL"
        elif self.current_entropy > 0.6:
            self.current_zone = "CHAOTIC" 
        elif self.current_entropy > 0.3:
            self.current_zone = "ACTIVE"
        else:
            self.current_zone = "CALM"
        
        # Update pulse state for external access
        self.pulse_state = {
            'entropy': self.current_entropy,
            'heat': self.current_heat,
            'zone': self.current_zone,
            'focus': min(1.0, 1.0 - self.current_entropy),
            'chaos': self.current_entropy
        }
    
    def tick(self):
        """Execute one cognitive tick cycle."""
        tick_start = datetime.now()
        self.tick_count += 1
        
        try:
            # 1. Get latest memory chunk
            memory_chunk = self.get_latest_memory_chunk()
            
            # 2. Extract passion and acquaintance
            passion, acquaintance = self.extract_passion_acquaintance(memory_chunk)
            
            # 3. Compute forecast
            if self.forecasting_engine:
                # Use real DAWN forecasting engine
                forecast_vector = self.forecasting_engine.generate_forecast(
                    passion=passion,
                    acquaintance=acquaintance,
                    context=f"Tick {self.tick_count}",
                    entropy_level=self.current_entropy
                )
                # Convert ForecastVector to dict format
                forecast = {
                    'confidence': forecast_vector.confidence,
                    'limit_horizon': 0.7 if forecast_vector.forecast_horizon == "short" else 0.5 if forecast_vector.forecast_horizon == "medium" else 0.3,
                    'risk_level': self._convert_risk_level_to_numeric(forecast_vector.risk_level() if hasattr(forecast_vector, 'risk_level') else 0.3),
                    'emotional_intensity': 0.5,  # Default since this attribute doesn't exist
                    'commentary': forecast_vector.predicted_behavior,
                    'forecast_factors': {
                        'passion_direction': forecast_vector.passion_direction or "general",
                        'forecast_horizon': forecast_vector.forecast_horizon or "medium"
                    }
                }
            else:
                # Use fallback
                forecast = compute_forecast_fallback(
                    passion=passion,
                    acquaintance=acquaintance,
                    current_entropy=self.current_entropy,
                    context=f"Tick {self.tick_count}"
                )
            
            # 4. Cache forecast
            self.forecast_cache = forecast
            self.last_forecast_time = tick_start
            
            # 5. Update pulse state
            self.update_pulse_state(forecast)
            
            # 6. Generate commentary
            state = {
                'entropy': self.current_entropy,
                'heat': self.current_heat,
                'zone': self.current_zone,
                'tick_count': self.tick_count,
                'forecast': forecast
            }
            
            commentary = self.generate_commentary(state)
            
            # 7. Handle high-risk situations
            risk_level = forecast.get('risk_level', 0.3)
            if risk_level > 0.7:
                self._handle_high_risk(forecast, state)
            
            # 8. Handle low horizon situations (rebloom trigger)
            limit_horizon = forecast.get('limit_horizon', 0.5)
            if limit_horizon < 0.3 and self._symbolic_router:
                self._trigger_rebloom(forecast, state)
            
            # 9. Log results
            self._log_tick_results(tick_start, forecast, commentary, state)
            
            # 10. Update existing DAWN if available
            if self.dawn_consciousness:
                self._update_existing_dawn(state)
            
            tick_duration = (datetime.now() - tick_start).total_seconds()
            logger.info(f"🔄 Tick {self.tick_count} completed in {tick_duration:.3f}s - Zone: {self.current_zone}")
            
        except Exception as e:
            logger.error(f"❌ Tick {self.tick_count} error: {e}")
    
    def _handle_high_risk(self, forecast: Dict[str, Any], state: Dict[str, Any]):
        """Handle high-risk forecast situations."""
        try:
            logger.warning(f"⚠️ High risk detected: {forecast.get('risk_level', 0):.2f}")
            
            # Create emergency sigil registration (mock)
            sigil_data = {
                'type': 'EMERGENCY_STABILIZE',
                'timestamp': datetime.now().isoformat(),
                'trigger_state': state,
                'forecast': forecast
            }
            
            # Log emergency sigil
            emergency_file = self.logs_dir / "emergency_sigils.jsonl"
            with open(emergency_file, 'a') as f:
                f.write(json.dumps(sigil_data) + '\n')
            
            logger.info("🚨 Emergency sigil registered")
            
        except Exception as e:
            logger.error(f"❌ Emergency handling error: {e}")
    
    def _trigger_rebloom(self, forecast: Dict[str, Any], state: Dict[str, Any]):
        """Trigger symbolic rebloom for low horizon situations."""
        try:
            if self._symbolic_router:
                rebloom_result = self._symbolic_router.rebloom_trigger(
                    emotional_input=forecast.get('emotional_intensity', 0.5),
                    context=f"Low horizon rebloom - Tick {self.tick_count}"
                )
                
                logger.info(f"🌸 Rebloom triggered: {rebloom_result.get('rebloom_id', 'unknown')}")
                
                # Log rebloom
                rebloom_file = self.logs_dir / "reblooms.jsonl"
                rebloom_data = {
                    'timestamp': datetime.now().isoformat(),
                    'tick': self.tick_count,
                    'trigger_state': state,
                    'result': rebloom_result
                }
                
                with open(rebloom_file, 'a') as f:
                    f.write(json.dumps(rebloom_data) + '\n')
            
        except Exception as e:
            logger.error(f"❌ Rebloom error: {e}")
    
    def _log_tick_results(self, tick_start: datetime, forecast: Dict[str, Any], 
                         commentary: str, state: Dict[str, Any]):
        """Log comprehensive tick results."""
        tick_data = {
            'timestamp': tick_start.isoformat(),
            'tick': self.tick_count,
            'duration_ms': (datetime.now() - tick_start).total_seconds() * 1000,
            'state': state,
            'forecast': forecast,
            'commentary': commentary
        }
        
        # Write to cognitive tick log
        cog_log_file = self.logs_dir / "cog_tick.log"
        with open(cog_log_file, 'a') as f:
            f.write(json.dumps(tick_data) + '\n')
    
    def _update_existing_dawn(self, state: Dict[str, Any]):
        """Update existing DAWN consciousness with new state."""
        try:
            if hasattr(self.dawn_consciousness, 'update_cognitive_state'):
                self.dawn_consciousness.update_cognitive_state(state)
        except Exception as e:
            logger.warning(f"⚠️ DAWN update error: {e}")
    
    def get_current_entropy(self) -> float:
        """Get current entropy level."""
        return self.current_entropy
    
    def get_pulse_heat(self) -> float:
        """Get current pulse heat."""
        return self.current_heat
    
    def get_pulse_zone(self) -> str:
        """Get current pulse zone."""
        return self.current_zone
    
    @property 
    def symbolic_router(self):
        """Get symbolic router for compatibility."""
        return self._symbolic_router
    
    def get_state(self) -> Dict[str, Any]:
        """Get comprehensive current state for external access."""
        return {
            'timestamp': datetime.now().isoformat(),
            'tick_count': self.tick_count,
            'uptime': (datetime.now() - self.start_time).total_seconds(),
            'system_metrics': {
                'entropy': self.current_entropy,
                'heat': self.current_heat,
                'zone': self.current_zone,
                'running': self.running
            },
            'forecast_cache': self.forecast_cache,
            'last_forecast_time': self.last_forecast_time.isoformat() if self.last_forecast_time else None
        }
    
    async def run_async(self):
        """Run the cognitive engine asynchronously."""
        self.running = True
        logger.info("🚀 DAWN Cognitive Engine starting...")
        
        try:
            while self.running:
                self.tick()
                await asyncio.sleep(2.0)  # 2-second tick interval
                
        except KeyboardInterrupt:
            logger.info("⚠️ Shutdown signal received")
        except Exception as e:
            logger.error(f"❌ Runtime error: {e}")
        finally:
            self.shutdown()
    
    def run(self):
        """Run the cognitive engine in blocking mode."""
        self.running = True
        logger.info("🚀 DAWN Cognitive Engine starting...")
        
        try:
            while self.running:
                self.tick()
                time.sleep(2.0)  # 2-second tick interval
                
        except KeyboardInterrupt:
            logger.info("⚠️ Shutdown signal received")
        except Exception as e:
            logger.error(f"❌ Runtime error: {e}")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown the cognitive engine."""
        self.running = False
        
        # Create final snapshot
        if self.snapshot_exporter:
            try:
                final_snapshot = self.snapshot_exporter.create_full_snapshot_zip()
                logger.info(f"📦 Final snapshot created: {final_snapshot}")
            except Exception as e:
                logger.error(f"❌ Final snapshot error: {e}")
        
        logger.info(f"🛑 DAWN Cognitive Engine shutdown after {self.tick_count} ticks")


# Factory function
def create_dawn_engine() -> DAWNCognitiveEngine:
    """Create and return a DAWN cognitive engine instance."""
    return DAWNCognitiveEngine()


# Main execution
if __name__ == "__main__":
    print("🧠 DAWN Core Runtime - Unified Cognitive System")
    print("=" * 50)
    
    # Create and run the engine
    engine = create_dawn_engine()
    
    try:
        # Run with async support if available
        if EXISTING_DAWN_AVAILABLE:
            asyncio.run(engine.run_async())
        else:
            engine.run()
    except KeyboardInterrupt:
        print("\n⚠️ Shutdown requested")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
    finally:
        print("🎯 DAWN Core Runtime complete") 