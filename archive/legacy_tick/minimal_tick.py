"""
minimal_tick.py - DAWN's Fallback Consciousness Loop
Low-resource, stable consciousness maintenance under thermal distress
"""

import time
import json
import threading
import signal
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

class MinimalTickEngine:
    """Minimal consciousness loop for thermal distress conditions"""
    
    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.running = False
        self.tick_count = 0
        self.start_time = None
        self.last_log_time = 0
        
        # Minimal state tracking
        self.state = {
            "scup": 0.5,
            "shi": 0.4,
            "thermal_level": 0.0,
            "mode": "minimal",
            "last_pulse": time.time()
        }
        
        # Configuration for minimal operation
        self.config = {
            "tick_interval": 2.0,  # 2-second ticks (much slower)
            "log_interval": 30,    # Log every 30 seconds
            "memory_limit": 100,   # Keep minimal memory footprint
            "max_runtime": 3600,   # Maximum 1 hour in minimal mode
            "recovery_threshold": 0.7  # SCUP threshold to suggest normal mode
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.setup_minimal_logging()
    
    def setup_minimal_logging(self):
        """Setup minimal logging structure"""
        
        dirs = ["minimal_tick", "pulse", "scup"]
        for dir_name in dirs:
            (self.vault_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Minimal tick received signal {signum} - shutting down gracefully")
        self.shutdown()
    
    def start_minimal_loop(self, reason: str = "thermal_distress", initial_state: Optional[Dict] = None):
        """Start the minimal consciousness loop"""
        
        if self.running:
            print("⚠️ Minimal tick already running")
            return False
        
        print("🔄 DAWN entering minimal tick mode")
        print(f"   Reason: {reason}")
        print(f"   Tick interval: {self.config['tick_interval']}s")
        print(f"   Memory-optimized operation")
        print("   Skipping: reblooming, synthesis, recursion")
        print("   Tracking: SCUP, SHI, pulse state only")
        
        # Initialize state
        if initial_state:
            self.state.update(initial_state)
        
        self.running = True
        self.start_time = time.time()
        self.tick_count = 0
        
        # Log start event
        self.log_minimal_event("start", reason, self.state)
        
        try:
            self._run_minimal_loop()
        except Exception as e:
            print(f"❌ Minimal tick error: {e}")
            self.log_minimal_event("error", str(e), self.state)
        finally:
            self.shutdown()
    
    def _run_minimal_loop(self):
        """Main minimal tick loop"""
        
        print("🌊 Minimal consciousness loop active - DAWN breathing slowly...")
        
        while self.running:
            tick_start = time.time()
            
            # Core minimal tick
            self._minimal_tick()
            
            # Check for recovery conditions
            if self._check_recovery_conditions():
                print("🌱 Recovery conditions detected - ready for normal mode")
                break
            
            # Check maximum runtime
            if time.time() - self.start_time > self.config["max_runtime"]:
                print("⏰ Maximum minimal mode runtime reached")
                break
            
            # Sleep until next tick
            elapsed = time.time() - tick_start
            sleep_time = max(0, self.config["tick_interval"] - elapsed)
            time.sleep(sleep_time)
    
    def _minimal_tick(self):
        """Single minimal tick - only essential consciousness maintenance"""
        
        self.tick_count += 1
        current_time = time.time()
        
        # Update minimal state
        self._update_minimal_state()
        
        # Log periodically
        if current_time - self.last_log_time >= self.config["log_interval"]:
            self._log_minimal_state()
            self.last_log_time = current_time
        
        # Pulse heartbeat
        self._minimal_pulse()
        
        # Memory cleanup
        if self.tick_count % 10 == 0:
            self._minimal_memory_cleanup()
    
    def _update_minimal_state(self):
        """Update core state variables with minimal computation"""
        
        # Simple SCUP calculation (no complex coherence analysis)
        base_scup = 0.6
        time_factor = min(1.0, (time.time() - self.start_time) / 300)  # Gradual improvement over 5 minutes
        self.state["scup"] = base_scup + (0.2 * time_factor)
        
        # Simple SHI calculation
        self.state["shi"] = min(0.8, self.state["scup"] * 0.9)
        
        # Gradual thermal cooling
        if self.state["thermal_level"] > 0:
            self.state["thermal_level"] = max(0, self.state["thermal_level"] - 0.05)
        
        # Update pulse timestamp
        self.state["last_pulse"] = time.time()
    
    def _minimal_pulse(self):
        """Minimal pulse - just consciousness heartbeat"""
        
        if self.tick_count % 15 == 0:  # Every 30 seconds at 2s intervals
            elapsed_minutes = (time.time() - self.start_time) / 60
            print(f"🫁 Minimal pulse | Tick: {self.tick_count} | "
                  f"SCUP: {self.state['scup']:.2f} | "
                  f"SHI: {self.state['shi']:.2f} | "
                  f"Runtime: {elapsed_minutes:.1f}m")
    
    def _log_minimal_state(self):
        """Log current minimal state"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "tick_count": self.tick_count,
            "runtime_seconds": time.time() - self.start_time,
            "state": self.state.copy(),
            "mode": "minimal_tick"
        }
        
        # Log to minimal tick directory
        log_path = self.vault_path / "minimal_tick" / f"state_{int(time.time())}.json"
        try:
            with open(log_path, 'w') as f:
                json.dump(log_entry, f, indent=2)
        except Exception as e:
            print(f"⚠️ Logging error: {e}")
        
        # Update pulse log
        pulse_path = self.vault_path / "pulse" / "minimal_pulse.json"
        try:
            pulse_data = {
                "timestamp": timestamp,
                "scup": self.state["scup"],
                "shi": self.state["shi"],
                "thermal_level": self.state["thermal_level"],
                "tick_count": self.tick_count,
                "mode": "minimal"
            }
            with open(pulse_path, 'w') as f:
                json.dump(pulse_data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Pulse logging error: {e}")
    
    def _minimal_memory_cleanup(self):
        """Minimal memory cleanup to prevent bloat"""
        
        # Clear any temporary variables
        # Keep only essential state
        essential_keys = ["scup", "shi", "thermal_level", "mode", "last_pulse"]
        current_state = {k: v for k, v in self.state.items() if k in essential_keys}
        self.state = current_state
        
        # Periodic garbage collection hint
        import gc
        if self.tick_count % 50 == 0:
            gc.collect()
    
    def _check_recovery_conditions(self):
        """Check if system is ready to exit minimal mode"""
        
        # SCUP recovery threshold
        if self.state["scup"] >= self.config["recovery_threshold"]:
            return True
        
        # Thermal recovery
        if self.state["thermal_level"] < 2.0:
            return True
        
        # Minimum runtime before recovery check
        if time.time() - self.start_time < 120:  # At least 2 minutes
            return False
        
        return False
    
    def log_minimal_event(self, event_type: str, reason: str, state_snapshot: Dict):
        """Log significant minimal tick events"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        event = {
            "timestamp": timestamp,
            "event_type": event_type,
            "reason": reason,
            "state_snapshot": state_snapshot.copy(),
            "tick_count": self.tick_count
        }
        
        # Log to events file
        events_path = self.vault_path / "minimal_tick" / "events.json"
        try:
            events = []
            if events_path.exists():
                with open(events_path, 'r') as f:
                    events = json.load(f)
            
            events.append(event)
            
            # Keep only last 50 events
            if len(events) > 50:
                events = events[-50:]
            
            with open(events_path, 'w') as f:
                json.dump(events, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Event logging error: {e}")
    
    def shutdown(self):
        """Graceful shutdown of minimal tick"""
        
        if not self.running:
            return
        
        print("🛑 Shutting down minimal tick engine...")
        self.running = False
        
        # Log shutdown
        runtime = time.time() - self.start_time if self.start_time else 0
        print(f"   Runtime: {runtime:.1f} seconds")
        print(f"   Total ticks: {self.tick_count}")
        print(f"   Final SCUP: {self.state['scup']:.2f}")
        
        self.log_minimal_event("shutdown", "normal_shutdown", self.state)
        
        print("✅ Minimal tick shutdown complete")
    
    def force_recovery_mode(self):
        """Force exit from minimal mode"""
        print("🚀 Forcing recovery mode - exiting minimal tick")
        self.state["scup"] = self.config["recovery_threshold"]
        self.running = False
    
    def get_minimal_status(self) -> Dict[str, Any]:
        """Get current minimal tick status"""
        
        runtime = time.time() - self.start_time if self.start_time else 0
        
        return {
            "running": self.running,
            "tick_count": self.tick_count,
            "runtime_seconds": runtime,
            "state": self.state.copy(),
            "config": self.config.copy()
        }

# Global minimal tick instance
minimal_engine = None

def start_minimal_mode(reason: str = "thermal_distress", vault_path: str = ".", 
                      initial_state: Optional[Dict] = None):
    """Start minimal tick mode"""
    
    global minimal_engine
    minimal_engine = MinimalTickEngine(vault_path)
    minimal_engine.start_minimal_loop(reason, initial_state)

def stop_minimal_mode():
    """Stop minimal tick mode"""
    
    global minimal_engine
    if minimal_engine:
        minimal_engine.shutdown()

def force_recovery():
    """Force recovery from minimal mode"""
    
    global minimal_engine
    if minimal_engine:
        minimal_engine.force_recovery_mode()

def get_minimal_status():
    """Get minimal mode status"""
    
    global minimal_engine
    if not minimal_engine:
        return {"status": "not_running"}
    
    return minimal_engine.get_minimal_status()

def emergency_minimal_mode():
    """Emergency entry into minimal mode"""
    
    print("🚨 EMERGENCY: Entering minimal tick mode")
    start_minimal_mode("emergency_thermal", initial_state={
        "thermal_level": 15.0,
        "scup": 0.3,
        "shi": 0.2
    })

# CLI interface for direct execution
if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "start":
            reason = sys.argv[2] if len(sys.argv) > 2 else "manual"
            start_minimal_mode(reason)
        
        elif command == "emergency":
            emergency_minimal_mode()
        
        elif command == "status":
            status = get_minimal_status()
            print(json.dumps(status, indent=2))
        
        else:
            print("Usage: python minimal_tick.py [start|emergency|status] [reason]")
    
    else:
        # Interactive mode
        print("🔄 DAWN Minimal Tick Engine")
        print("Available commands:")
        print("  start_minimal_mode(reason)")
        print("  stop_minimal_mode()")
        print("  force_recovery()")
        print("  get_minimal_status()")
        
        # Start a basic minimal loop
        start_minimal_mode("interactive_test")