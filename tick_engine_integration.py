"""
Integration code to connect UnifiedTickEngine with DAWN main.py
Save this as: tick_engine_integration.py in your Tick_engine directory
"""

import asyncio
import threading
from typing import Optional
from unified_tick_engine import create_unified_tick_engine, UnifiedTickEngine

class DAWNTickEngineIntegration:
    """Bridge between DAWN consciousness and UnifiedTickEngine"""
    
    def __init__(self, dawn_consciousness):
        self.dawn = dawn_consciousness
        self.tick_engine: Optional[UnifiedTickEngine] = None
        self.engine_thread = None
        self.engine_loop = None
        
    async def activity_sensor(self) -> float:
        """Convert DAWN activity to tick engine metric"""
        try:
            # Use schema coherence as activity measure
            scup = self.dawn.schema_state.get('scup', 0.5)
            arousal = self.dawn.mood_state.get('arousal', 0.5)
            return (scup + arousal) / 2.0
        except:
            return 0.5
    
    async def pressure_sensor(self) -> float:
        """Convert DAWN pressure to tick engine metric"""
        try:
            # Use thermal heat as pressure
            # Access pulse from builtins since it's made global in main.py
            import builtins
            pulse = getattr(builtins, 'pulse', None)
            if pulse:
                current_heat = pulse.get_heat()
                heat_capacity = getattr(pulse, 'heat_capacity', 10.0)
                return min(1.0, current_heat / heat_capacity)
            return 0.0
        except:
            return 0.0
    
    async def mood_sensor(self) -> float:
        """Convert DAWN mood to tick engine metric"""
        try:
            valence = self.dawn.mood_state.get('valence', 0.5)
            return valence
        except:
            return 0.5
    
    async def tick_event_handler(self, event):
        """Handle tick events from the engine"""
        try:
            # Increment DAWN's tick counter
            self.dawn.tick_count += 1
            
            # Update DAWN's schema state from tick engine
            if hasattr(self.tick_engine, 'state'):
                engine_state = self.tick_engine.state
                
                # Sync some values
                self.dawn.schema_state['entropy_index'] = engine_state.entropy
                self.dawn.schema_state['tension'] = engine_state.cascade_risk
                
                # Update mood from engine
                self.dawn.mood_state['valence'] = engine_state.valence
                self.dawn.mood_state['arousal'] = engine_state.arousal
                
        except Exception as e:
            print(f"[Integration] Error handling tick event: {e}")
    
    def start_tick_engine(self):
        """Start the unified tick engine in a separate thread"""
        print("[Integration] Starting UnifiedTickEngine...")
        
        # Create tick engine with DAWN sensors
        self.tick_engine = create_unified_tick_engine(
            base_interval=0.5,  # Faster than DAWN's default
            activity_sensor=self.activity_sensor,
            pressure_sensor=self.pressure_sensor,
            mood_sensor=self.mood_sensor,
            enable_narrative=True
        )
        
        # Set tick event handler
        self.tick_engine.emit_tick_event = self.tick_event_handler
        
        # Run in separate thread with its own event loop
        def run_engine():
            self.engine_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.engine_loop)
            
            try:
                self.engine_loop.run_until_complete(self.tick_engine.start())
            except Exception as e:
                print(f"[Integration] Engine error: {e}")
            finally:
                self.engine_loop.close()
        
        self.engine_thread = threading.Thread(
            target=run_engine,
            name="UnifiedTickEngine",
            daemon=True
        )
        self.engine_thread.start()
        
        print("[Integration] ✅ UnifiedTickEngine started successfully")
    
    def stop_tick_engine(self):
        """Stop the tick engine"""
        if self.tick_engine:
            print("[Integration] Stopping UnifiedTickEngine...")
            self.tick_engine.stop()
            
            if self.engine_loop:
                self.engine_loop.call_soon_threadsafe(self.engine_loop.stop)
            
            if self.engine_thread:
                self.engine_thread.join(timeout=5.0)
            
            print("[Integration] ✅ UnifiedTickEngine stopped")
    
    def get_engine_status(self):
        """Get tick engine status"""
        if self.tick_engine:
            return self.tick_engine.get_engine_stats()
        return None