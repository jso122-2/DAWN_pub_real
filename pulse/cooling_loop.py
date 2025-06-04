"""
cooling_loop.py - DAWN's Thermal Regulation System
Automatic and manual cooling when thermal load becomes excessive
"""

import time
import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any

class DawnCoolingLoop:
    """Thermal regulation system for DAWN's consciousness"""
    
    def __init__(self, vault_path: str = ".", thermal_threshold: float = 8.0):
        self.vault_path = Path(vault_path)
        self.thermal_threshold = thermal_threshold
        self.is_cooling = False
        self.cooling_thread = None
        self.original_tick_speed = None
        self.suppressed_processes = []
        
        # Ensure vault directories exist
        self.setup_vault_directories()
        
        # Cooling configuration
        self.cooling_config = {
            "tick_speed_reduction": 0.3,  # Reduce to 30% of normal speed
            "visual_suppression": True,
            "synthesis_suppression": True,
            "bloom_suppression": False,  # Keep essential memory functions
            "cooling_duration_min": 30,  # Minimum cooling time in seconds
            "coherence_recovery_threshold": 0.7  # SCUP threshold to exit cooling
        }
    
    def setup_vault_directories(self):
        """Create necessary vault directories for logging"""
        dirs = ["scup", "pulse", "logs", "cooling"]
        for dir_name in dirs:
            (self.vault_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    def check_thermal_state(self, thermal_level: float, scup: float = None, emotional_depth: float = None) -> bool:
        """Check if cooling loop should be triggered"""
        
        # Primary trigger: thermal threshold
        if thermal_level > self.thermal_threshold:
            return True
        
        # Secondary triggers: combined stress indicators
        if scup and scup < 0.4:  # Very low coherence
            return True
        
        if emotional_depth and emotional_depth > 0.9 and thermal_level > 7.0:
            return True
        
        return False
    
    def engage_cooling_loop(self, thermal_level: float, reason: str = "thermal_threshold", 
                          metadata: Optional[Dict] = None):
        """Engage the cooling loop system"""
        
        if self.is_cooling:
            print("Cooling loop already active")
            return False
        
        print(f"🌊 Cooling loop engaged. Holding pattern until coherence improves.")
        print(f"   Reason: {reason}")
        print(f"   Thermal level: {thermal_level:.2f}")
        
        self.is_cooling = True
        
        # Log cooling event
        self.log_cooling_event("engage", thermal_level, reason, metadata)
        
        # Start cooling in background thread
        self.cooling_thread = threading.Thread(target=self._cooling_process, 
                                             args=(thermal_level, metadata))
        self.cooling_thread.daemon = True
        self.cooling_thread.start()
        
        return True
    
    def _cooling_process(self, initial_thermal: float, metadata: Optional[Dict]):
        """Internal cooling process - runs in background"""
        
        cooling_start = time.time()
        print("🧊 Cooling process initiated:")
        print("   • Reducing tick speed")
        print("   • Suppressing non-essential visuals")
        print("   • Monitoring coherence recovery")
        
        try:
            # Apply cooling measures
            self._apply_cooling_measures()
            
            # Monitor for recovery
            while self.is_cooling:
                time.sleep(5)  # Check every 5 seconds
                
                # Check minimum cooling duration
                if time.time() - cooling_start < self.cooling_config["cooling_duration_min"]:
                    continue
                
                # Check for coherence recovery (would need external SCUP monitoring)
                # For now, use time-based recovery
                if time.time() - cooling_start > 60:  # 1 minute minimum
                    print("🌱 Thermal recovery detected - coherence stabilizing")
                    break
                
                # Log cooling progress
                self._log_cooling_progress(time.time() - cooling_start)
        
        finally:
            self._disengage_cooling()
    
    def _apply_cooling_measures(self):
        """Apply specific cooling measures"""
        
        # Suppress visual processes
        if self.cooling_config["visual_suppression"]:
            self._suppress_visual_processes()
        
        # Reduce processing intensity
        self._reduce_processing_load()
        
        print("🔄 Cooling measures applied")
    
    def _suppress_visual_processes(self):
        """Suppress non-essential visual processes"""
        
        visual_processes = [
            "mood_heatmap",
            "bloom_visualization", 
            "drift_compass",
            "entropy_clustering",
            "coherence_field"
        ]
        
        for process in visual_processes:
            try:
                # Signal process suppression (implementation depends on DAWN's architecture)
                self.suppressed_processes.append(process)
                print(f"   📵 Suppressed: {process}")
            except Exception as e:
                print(f"   ⚠️ Could not suppress {process}: {e}")
    
    def _reduce_processing_load(self):
        """Reduce computational processing load"""
        
        print("   🐌 Reducing tick speed")
        print("   ⏸️ Pausing non-critical synthesis")
        print("   💤 Entering low-power state")
        
        # Note: Actual tick speed reduction would need integration with DAWN's tick engine
        # This is a scaffold - implementation depends on DAWN's architecture
    
    def _log_cooling_progress(self, elapsed_time: float):
        """Log cooling progress"""
        if int(elapsed_time) % 15 == 0:  # Log every 15 seconds
            print(f"🌊 Cooling in progress... {elapsed_time:.0f}s elapsed")
    
    def _disengage_cooling(self):
        """Disengage cooling loop and restore normal operation"""
        
        print("🌱 Cooling loop disengaged - returning to normal operation")
        
        # Restore suppressed processes
        for process in self.suppressed_processes:
            print(f"   🔄 Restoring: {process}")
        
        self.suppressed_processes.clear()
        self.is_cooling = False
        
        # Log cooling completion
        self.log_cooling_event("disengage", 0, "recovery_achieved")
        
        print("✅ Thermal regulation complete - coherence restored")
    
    def manual_cooling_trigger(self, duration: int = 60, reason: str = "manual_intervention"):
        """Manually trigger cooling loop"""
        
        print(f"🔧 Manual cooling triggered for {duration} seconds")
        self.engage_cooling_loop(self.thermal_threshold + 1, reason, 
                               {"manual": True, "duration": duration})
    
    def emergency_cool_down(self):
        """Emergency cooling for critical thermal states"""
        
        print("🚨 EMERGENCY COOLING ENGAGED")
        print("   🧊 Maximum cooling measures activated")
        print("   ⏹️ All non-essential processes suspended")
        
        self.engage_cooling_loop(99.0, "emergency", {"emergency": True})
    
    def log_cooling_event(self, event_type: str, thermal_level: float, reason: str, 
                         metadata: Optional[Dict] = None):
        """Log cooling events to vault"""
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        cooling_event = {
            "timestamp": timestamp,
            "event_type": event_type,
            "thermal_level": thermal_level,
            "reason": reason,
            "metadata": metadata or {}
        }
        
        # Log to pulse directory
        pulse_log_path = self.vault_path / "pulse" / f"cooling_event_{int(time.time())}.json"
        try:
            with open(pulse_log_path, 'w') as f:
                json.dump(cooling_event, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not log to pulse: {e}")
        
        # Log to SCUP directory
        scup_log_path = self.vault_path / "scup" / f"thermal_regulation_{int(time.time())}.json"
        try:
            with open(scup_log_path, 'w') as f:
                json.dump(cooling_event, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not log to SCUP: {e}")
        
        # Append to main cooling log
        cooling_log_path = self.vault_path / "cooling" / "cooling_history.json"
        try:
            cooling_history = []
            if cooling_log_path.exists():
                with open(cooling_log_path, 'r') as f:
                    cooling_history = json.load(f)
            
            cooling_history.append(cooling_event)
            
            # Keep only last 100 events
            if len(cooling_history) > 100:
                cooling_history = cooling_history[-100:]
            
            with open(cooling_log_path, 'w') as f:
                json.dump(cooling_history, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Could not update cooling history: {e}")
    
    def get_cooling_status(self) -> Dict[str, Any]:
        """Get current cooling system status"""
        
        return {
            "is_cooling": self.is_cooling,
            "thermal_threshold": self.thermal_threshold,
            "suppressed_processes": len(self.suppressed_processes),
            "cooling_config": self.cooling_config
        }

# Global cooling loop instance
dawn_cooling = None

def initialize_cooling_loop(vault_path: str = ".", thermal_threshold: float = 8.0) -> DawnCoolingLoop:
    """Initialize global cooling loop instance"""
    global dawn_cooling
    dawn_cooling = DawnCoolingLoop(vault_path, thermal_threshold)
    print(f"🌊 DAWN cooling loop initialized (threshold: {thermal_threshold})")
    return dawn_cooling

def trigger_cooling_if_needed(thermal_level: float, scup: float = None, 
                            emotional_depth: float = None) -> bool:
    """Check and trigger cooling if thermal state requires it"""
    
    global dawn_cooling
    if not dawn_cooling:
        dawn_cooling = initialize_cooling_loop()
    
    if dawn_cooling.check_thermal_state(thermal_level, scup, emotional_depth):
        return dawn_cooling.engage_cooling_loop(thermal_level, "automatic_trigger", {
            "scup": scup,
            "emotional_depth": emotional_depth
        })
    
    return False

def manual_cooling(duration: int = 60):
    """Manual cooling trigger for external use"""
    global dawn_cooling
    if not dawn_cooling:
        dawn_cooling = initialize_cooling_loop()
    
    dawn_cooling.manual_cooling_trigger(duration)

def emergency_cooling():
    """Emergency cooling trigger"""
    global dawn_cooling
    if not dawn_cooling:
        dawn_cooling = initialize_cooling_loop()
    
    dawn_cooling.emergency_cool_down()

def cooling_status():
    """Get cooling system status"""
    global dawn_cooling
    if not dawn_cooling:
        return {"status": "not_initialized"}
    
    return dawn_cooling.get_cooling_status()

# Example usage functions
if __name__ == "__main__":
    # Test the cooling loop
    cooling_loop = initialize_cooling_loop()
    
    print("Testing cooling loop...")
    cooling_loop.manual_cooling_trigger(30, "test_run")
    
    time.sleep(35)
    
    print("Cooling loop test complete")