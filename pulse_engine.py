#!/usr/bin/env python3
"""
pulse_engine.py

Unified Pulse Engine interface for DAWN cognitive system
Combines zone tracking, state timing, and overheat detection

Integration:
    Primary: dawn.pulse.diagnostics.pulse_engine
    Dependencies: zone_tracker.py, state_timer.py, overheat_detector.py
    Interfaces with: Core tick engine, thermal monitoring
    Output streams: Unified diagnostics, event streams
    
Author: DAWN Development Team
Epoch: epoch_0601
"""

import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

# Pulse engine components
from pulse.zone_tracker import PulseZoneTracker, PulseZone, PulseEvent
from pulse.state_timer import PulseStateTimer
from pulse.overheat_detector import PulseOverheatDetector, ThermalEvent, ThermalAlert

# Core DAWN components (with fallbacks for testing)
try:
    from core.tick_engine import get_current_tick
    from health.thermal_monitoring import temperature_tracker
except ImportError:
    def get_current_tick():
        return int(time.time() * 1000)
    
    class MockThermalTracker:
        def __init__(self):
            self.base_temp = 30
            self.variation = 0
            
        def get_temperature(self):
            import random
            # Simulate temperature patterns
            self.variation += random.uniform(-2, 3)
            self.variation = max(-20, min(60, self.variation))
            return self.base_temp + self.variation
            
    temperature_tracker = MockThermalTracker()


@dataclass
class PulseEngineEvent:
    """Unified pulse engine event"""
    tick: int
    zone_event: Optional[PulseEvent]
    thermal_event: Optional[ThermalEvent]
    current_state: Dict[str, Any]
    
    @property
    def is_critical(self) -> bool:
        """Check if event represents critical condition"""
        if self.thermal_event:
            return self.thermal_event.alert_level in [ThermalAlert.CRITICAL, ThermalAlert.EMERGENCY]
        return False


class PulseEngine:
    """Unified pulse engine diagnostics interface"""
    
    def __init__(self, log_dir: str = "pulse/logs"):
        """Initialize pulse engine with all components"""
        self.log_dir = log_dir
        
        # Initialize components
        self.tracker = PulseZoneTracker(log_dir=log_dir)
        self.timer = PulseStateTimer()
        self.detector = PulseOverheatDetector(zone_tracker=self.tracker, log_dir=log_dir)
        
        # Engine state
        self.running = True
        self.update_count = 0
        self.last_update_tick = get_current_tick()
        
        # Event history
        self.event_history: List[PulseEngineEvent] = []
        self.critical_event_count = 0
        
        print(f"[PULSE ENGINE] Initialized at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[PULSE ENGINE] Logging to: {log_dir}")
    
    def update(self, temperature: Optional[float] = None, 
               sigil_burn_rate: float = 0.0) -> PulseEngineEvent:
        """Update all pulse components and return unified event"""
        current_tick = get_current_tick()
        
        # Get temperature if not provided
        if temperature is None:
            temperature = temperature_tracker.get_temperature()
        
        # Update zone tracker
        zone_event = self.tracker.update(temperature, sigil_burn_rate)
        
        # Record transition if occurred
        if zone_event:
            self.timer.record_transition(zone_event)
        
        # Update overheat detector
        thermal_event = self.detector.update(temperature, sigil_burn_rate)
        
        # Create unified event
        event = PulseEngineEvent(
            tick=current_tick,
            zone_event=zone_event,
            thermal_event=thermal_event,
            current_state=self._get_current_state()
        )
        
        # Track critical events
        if event.is_critical:
            self.critical_event_count += 1
        
        # Update engine state
        self.update_count += 1
        self.last_update_tick = current_tick
        self.event_history.append(event)
        
        # Limit history size
        if len(self.event_history) > 1000:
            self.event_history.pop(0)
        
        return event
    
    def _get_current_state(self) -> Dict[str, Any]:
        """Get current state snapshot"""
        return {
            'zone': self.tracker.current_zone.name,
            'temperature': self.tracker.current_temperature,
            'sigil_burn_rate': self.tracker.sigil_burn_rate,
            'alert_level': self.detector.current_alert.name,
            'transition_velocity': self.timer.get_transition_velocity(),
            'update_count': self.update_count
        }
    
    def get_diagnostics(self) -> Dict[str, Any]:
        """Get comprehensive diagnostics from all components"""
        # Get component reports
        zone_status = self.tracker.get_status_display()
        state_analysis = self.timer.get_zone_residence_report()
        thermal_report = self.detector.get_overheat_report()
        
        # Get predictions
        next_zone, confidence = self.timer.predict_next_state()
        
        # Compile recommendations
        recommendations = []
        recommendations.extend(self.tracker.get_thermal_recommendations())
        
        # Add engine-specific recommendations
        if self.critical_event_count > 5:
            recommendations.append("🚨 Multiple critical events detected - review system load")
        
        return {
            'zone_status': zone_status,
            'state_analysis': state_analysis,
            'thermal_report': thermal_report,
            'recommendations': recommendations,
            'prediction': {
                'next_zone': next_zone.name,
                'confidence': confidence
            },
            'metrics': {
                'updates': self.update_count,
                'critical_events': self.critical_event_count,
                'current_zone': self.tracker.current_zone.name,
                'temperature': self.tracker.current_temperature
            }
        }
    
    def get_unified_display(self) -> str:
        """Generate unified status display"""
        current_zone = self.tracker.current_zone
        zone_color = current_zone.get_color_code()
        alert_color = self.detector.current_alert.get_color()
        reset = "\033[0m"
        
        lines = [
            "╔═══════════════════════════════════════════════╗",
            "║          DAWN PULSE ENGINE STATUS             ║",
            "╚═══════════════════════════════════════════════╝",
            "",
            f"Pulse Zone: {zone_color}{current_zone.name:8}{reset} │ "
            f"Alert: {alert_color}{self.detector.current_alert.name:9}{reset}",
            f"Temperature: {self.tracker.current_temperature:5.1f}°C │ "
            f"Burn Rate: {self.tracker.sigil_burn_rate:.3f}/tick",
            ""
        ]
        
        # Add timeline visualization
        timeline = self.timer.get_state_timeline_visualization(width=40)
        lines.append(timeline)
        lines.append("")
        
        # Add key metrics
        lines.extend([
            "Key Metrics:",
            "─────────────────────────────────────",
            f"Updates: {self.update_count:,} │ Critical Events: {self.critical_event_count}",
            f"Transition Rate: {self.timer.get_transition_velocity():.2f}/sec",
            f"System Uptime: {(get_current_tick() - self.last_update_tick) / 1000:.1f}s"
        ])
        
        # Add top recommendations
        recommendations = self.tracker.get_thermal_recommendations()
        if recommendations:
            lines.extend(["", "Active Recommendations:", "─────────────────────────────────────"])
            for rec in recommendations[:3]:  # Top 3
                lines.append(f"  {rec}")
        
        return "\n".join(lines)
    
    def run_diagnostic_loop(self, duration: int = 60, update_rate: float = 1.0):
        """Run diagnostic loop for testing"""
        print(f"\n[PULSE ENGINE] Starting diagnostic loop for {duration} seconds...")
        print(f"[PULSE ENGINE] Update rate: {update_rate} Hz\n")
        
        start_time = time.time()
        
        try:
            while (time.time() - start_time) < duration and self.running:
                # Update engine
                event = self.update()
                
                # Print significant events
                if event.zone_event:
                    print(f"[ZONE] Transition: {event.zone_event.from_zone.name if event.zone_event.from_zone else 'INIT'} "
                          f"→ {event.zone_event.to_zone.name}")
                
                if event.thermal_event:
                    print(f"[THERMAL] {event.thermal_event.event_type}: "
                          f"{event.thermal_event.temperature:.1f}°C "
                          f"({event.thermal_event.alert_level.name})")
                
                # Sleep for update interval
                time.sleep(1.0 / update_rate)
                
                # Periodic status display
                if self.update_count % 10 == 0:
                    print("\n" + self.get_unified_display() + "\n")
                    
        except KeyboardInterrupt:
            print("\n[PULSE ENGINE] Diagnostic loop interrupted")
        
        # Final report
        print("\n" + "="*50)
        print("FINAL DIAGNOSTIC REPORT")
        print("="*50)
        
        diagnostics = self.get_diagnostics()
        print(diagnostics['thermal_report'])
        print("\n" + diagnostics['state_analysis'])
    
    def shutdown(self):
        """Graceful shutdown of pulse engine"""
        self.running = False
        print(f"\n[PULSE ENGINE] Shutting down...")
        print(f"[PULSE ENGINE] Total updates: {self.update_count}")
        print(f"[PULSE ENGINE] Critical events: {self.critical_event_count}")
        print(f"[PULSE ENGINE] Logs saved to: {self.log_dir}")


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    print("=== DAWN PULSE ENGINE TEST ===")
    print("Unified diagnostics interface")
    print("="*50 + "\n")
    
    # Create pulse engine
    engine = PulseEngine()
    
    # Run test scenarios
    if len(sys.argv) > 1 and sys.argv[1] == "--loop":
        # Run diagnostic loop
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        engine.run_diagnostic_loop(duration=duration)
    else:
        # Run quick test
        print("Running quick test sequence...\n")
        
        # Simulate temperature patterns
        test_temps = [
            30, 35, 40, 45, 50,  # Gradual rise
            55, 60, 65, 70, 75,  # Into surge
            80, 85, 80, 75, 70,  # Critical and recovery
            65, 60, 55, 50, 45,  # Cool down
            40, 35, 30, 25, 20   # Return to calm
        ]
        
        for i, temp in enumerate(test_temps):
            # Calculate burn rate based on temperature
            burn_rate = min(1.0, temp / 100 * 1.2)
            
            # Update engine
            event = engine.update(temp, burn_rate)
            
            # Small delay
            time.sleep(0.5)
            
            # Show status periodically
            if i % 5 == 4:
                print("\n" + engine.get_unified_display() + "\n")
        
        # Final diagnostics
        print("\n" + "="*50)
        print("TEST COMPLETE - FINAL DIAGNOSTICS")
        print("="*50)
        
        diagnostics = engine.get_diagnostics()
        for key, value in diagnostics['metrics'].items():
            print(f"{key}: {value}")
    
    # Shutdown
    engine.shutdown()