#!/usr/bin/env python3
"""
DAWN Tick Loop Integration - Cognition Runtime Bridge
====================================================

Helper module that demonstrates how to integrate cognition_runtime.py
into existing tick_loop.py systems for seamless symbolic reflex operation.

This bridges the gap between reactive tick processing and the full
meta-cognitive symbolic regulation system.
"""

import time
import logging
from typing import Dict, Any, Optional, Callable

# Import cognition runtime
from cognition_runtime import process_cognition_tick, log_event, initialize_gui_integration

logger = logging.getLogger("tick_integration")

class TickCognitionBridge:
    """
    Bridge between tick_loop.py and cognition_runtime.py
    
    Provides seamless integration of the symbolic reflex system
    into existing DAWN tick processing infrastructure.
    """
    
    def __init__(self, window_emit_callback: Optional[Callable] = None):
        """Initialize the tick-cognition bridge"""
        self.window_emit_callback = window_emit_callback
        self.integration_active = False
        
        # Setup GUI integration if callback provided
        if window_emit_callback:
            initialize_gui_integration(window_emit_callback)
            logger.info("🎯 GUI integration enabled in tick bridge")
        
        # Performance tracking
        self.cognition_tick_times = []
        self.total_ticks_processed = 0
        
        logger.info("🌉 Tick-Cognition Bridge initialized")
    
    def process_integrated_tick(self, tick_data: Dict[str, Any], 
                               tick_context: Any = None) -> Dict[str, Any]:
        """
        Process a tick with full cognition integration.
        
        Call this AFTER .mmap is written but BEFORE tick loop ends.
        
        Args:
            tick_data: Current tick state data
            tick_context: Optional tick context from engine
            
        Returns:
            Combined tick and cognition results
        """
        cognition_start = time.time()
        
        try:
            # Extract tick ID
            tick_id = tick_data.get('tick_id', self.total_ticks_processed)
            
            # Process through cognition runtime
            cognition_result = process_cognition_tick(tick_data)
            
            # Log significant events
            if cognition_result.get('tracer_alerts'):
                alert_summary = f"{len(cognition_result['tracer_alerts'])} alerts generated"
                log_event("COGNITION", tick_id, f"Reflex summary: {alert_summary}")
            
            if cognition_result.get('symbolic_roots'):
                root_summary = f"{len(cognition_result['symbolic_roots'])} symbolic roots detected"
                log_event("COGNITION", tick_id, f"Root summary: {root_summary}")
            
            # Emit GUI events if callback available
            if self.window_emit_callback:
                self._emit_consolidated_events(cognition_result)
            
            # Track performance
            cognition_time = time.time() - cognition_start
            self.cognition_tick_times.append(cognition_time)
            self.total_ticks_processed += 1
            
            # Keep performance history manageable
            if len(self.cognition_tick_times) > 100:
                self.cognition_tick_times = self.cognition_tick_times[-50:]
            
            # Build integrated result
            integrated_result = {
                'tick_data': tick_data,
                'cognition_result': cognition_result,
                'integration_stats': {
                    'cognition_time': cognition_time,
                    'total_ticks': self.total_ticks_processed,
                    'avg_cognition_time': sum(self.cognition_tick_times) / len(self.cognition_tick_times),
                    'integration_active': True
                }
            }
            
            logger.debug(f"Integrated tick {tick_id} processed in {cognition_time:.3f}s")
            
            return integrated_result
            
        except Exception as e:
            logger.error(f"Error in integrated tick processing: {e}")
            return {
                'tick_data': tick_data,
                'cognition_result': {'status': 'error', 'error': str(e)},
                'integration_stats': {'integration_active': False, 'error': str(e)}
            }
    
    def _emit_consolidated_events(self, cognition_result: Dict[str, Any]):
        """Emit consolidated GUI events"""
        if not self.window_emit_callback:
            return
        
        try:
            # Consolidate all symbolic events
            symbolic_events = []
            
            # Add tracer alerts
            for alert in cognition_result.get('tracer_alerts', []):
                symbolic_events.append({
                    'type': 'TRACER_ALERT',
                    'tracer_type': alert['tracer_type'],
                    'severity': alert['severity'],
                    'message': alert['message'],
                    'timestamp': alert['timestamp']
                })
            
            # Add symbolic roots
            for root in cognition_result.get('symbolic_roots', []):
                symbolic_events.append({
                    'type': 'SYMBOLIC_ROOT',
                    'root_type': root['type'],
                    'symbolic_root': root['symbolic_root'],
                    'significance': root['significance'],
                    'timestamp': root['timestamp']
                })
            
            # Emit consolidated event
            if symbolic_events:
                self.window_emit_callback("symbolic_alert", {
                    "type": "CONSOLIDATED",
                    "tick": cognition_result.get('tick_id'),
                    "events": symbolic_events,
                    "summary": f"{len(symbolic_events)} symbolic events"
                })
            
        except Exception as e:
            logger.error(f"Error emitting consolidated events: {e}")
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get integration performance statistics"""
        if not self.cognition_tick_times:
            return {'integration_active': False, 'no_data': True}
        
        return {
            'integration_active': True,
            'total_ticks_processed': self.total_ticks_processed,
            'avg_cognition_time': sum(self.cognition_tick_times) / len(self.cognition_tick_times),
            'min_cognition_time': min(self.cognition_tick_times),
            'max_cognition_time': max(self.cognition_tick_times),
            'recent_performance': self.cognition_tick_times[-10:] if len(self.cognition_tick_times) >= 10 else self.cognition_tick_times
        }

# Global bridge instance
_tick_bridge = None

def get_tick_bridge(window_emit_callback: Optional[Callable] = None) -> TickCognitionBridge:
    """Get or create the global tick bridge"""
    global _tick_bridge
    if _tick_bridge is None:
        _tick_bridge = TickCognitionBridge(window_emit_callback)
    return _tick_bridge

def integrate_with_tick_loop(tick_data: Dict[str, Any], tick_context: Any = None) -> Dict[str, Any]:
    """
    Main integration function for tick_loop.py
    
    Add this call to your tick_loop.py after .mmap is written:
    
    ```python
    from tick_integration import integrate_with_tick_loop
    
    # After .mmap write, before tick end:
    cognition_result = integrate_with_tick_loop(state)
    ```
    """
    bridge = get_tick_bridge()
    return bridge.process_integrated_tick(tick_data, tick_context)

def setup_gui_integration(window_emit_callback: Callable):
    """
    Setup GUI integration for real-time event emission
    
    Call this during initialization to enable window.emit() functionality:
    
    ```python
    from tick_integration import setup_gui_integration
    
    def emit_to_gui(event_type, data):
        # Your Tauri/GUI emission logic
        window.emit(event_type, data)
    
    setup_gui_integration(emit_to_gui)
    ```
    """
    global _tick_bridge
    if _tick_bridge:
        _tick_bridge.window_emit_callback = window_emit_callback
        initialize_gui_integration(window_emit_callback)
    else:
        _tick_bridge = TickCognitionBridge(window_emit_callback)
    
    logger.info("🎯 GUI integration setup complete")

# Example tick_loop.py integration patterns
def example_tick_loop_integration():
    """
    Example showing how to integrate with different tick_loop.py patterns
    """
    print("🌉 Example Tick Loop Integration Patterns")
    print("=" * 50)
    
    # Pattern 1: Simple integration
    print("\n1. Simple Integration Pattern:")
    print("""
# In your tick_loop.py, after .mmap is written:
from tick_integration import integrate_with_tick_loop

async def _execute_tick(self):
    # ... existing tick processing ...
    
    # Write to .mmap
    self._write_mmap_state(current_state)
    
    # INTEGRATE COGNITION RUNTIME
    cognition_result = integrate_with_tick_loop(current_state)
    
    # Optional: Log significant events
    if cognition_result['cognition_result']['status'] == 'success':
        alerts = len(cognition_result['cognition_result']['tracer_alerts'])
        if alerts > 0:
            logger.info(f"🧠 Cognition: {alerts} symbolic alerts generated")
    
    # ... rest of tick processing ...
""")
    
    # Pattern 2: Advanced integration with GUI
    print("\n2. Advanced Integration with GUI Events:")
    print("""
# Setup during initialization:
from tick_integration import setup_gui_integration

def emit_to_tauri(event_type, data):
    # Your Tauri integration
    try:
        window.emit(event_type, data)
    except Exception as e:
        logger.error(f"GUI emission error: {e}")

setup_gui_integration(emit_to_tauri)

# In your tick loop:
cognition_result = integrate_with_tick_loop(current_state)

# GUI automatically receives real-time events via window.emit():
# - "symbolic_alert" for tracer alerts and symbolic roots
# - "memory_update" for network growth events
""")
    
    # Pattern 3: Performance monitoring
    print("\n3. Performance Monitoring Pattern:")
    print("""
# Monitor integration performance:
from tick_integration import get_tick_bridge

bridge = get_tick_bridge()
stats = bridge.get_integration_stats()

logger.info(f"Cognition integration: {stats['avg_cognition_time']:.3f}s avg")
if stats['max_cognition_time'] > 0.1:  # 100ms threshold
    logger.warning("Cognition processing time exceeded threshold")
""")

# Demo and testing
if __name__ == "__main__":
    print("🌉 Testing Tick-Cognition Integration Bridge")
    print("=" * 50)
    
    # Test integration
    test_tick_data = {
        'tick_id': 5001,
        'entropy': 0.8,
        'heat': 0.7,
        'coherence': 0.3,
        'memory_activity': 0.9,
        'forecast_reliability': 0.4
    }
    
    # Process integrated tick
    result = integrate_with_tick_loop(test_tick_data)
    
    print(f"Integration Result:")
    print(f"  Status: {result['cognition_result']['status']}")
    print(f"  Tracer Alerts: {len(result['cognition_result']['tracer_alerts'])}")
    print(f"  Symbolic Roots: {len(result['cognition_result']['symbolic_roots'])}")
    print(f"  Cognition Time: {result['integration_stats']['cognition_time']:.3f}s")
    
    # Show integration stats
    bridge = get_tick_bridge()
    stats = bridge.get_integration_stats()
    print(f"\nIntegration Stats:")
    for key, value in stats.items():
        if key != 'recent_performance':
            print(f"  {key}: {value}")
    
    # Show example patterns
    example_tick_loop_integration()
    
    print(f"\n✅ Tick-Cognition integration bridge ready!")
    print(f"🎯 Use integrate_with_tick_loop() in your tick_loop.py") 