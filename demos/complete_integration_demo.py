#!/usr/bin/env python3
"""
DAWN Complete Integration Demo - All Systems Unified
===================================================

Demonstrates the complete integration of:
1. 🧠 cognition_runtime.py with tick_loop.py
2. 🧬 GUI panels with live log files + runtime  
3. 🔊 Voice layer with symbolic tracer outputs
4. 📡 Web events via window.emit for full introspection feedback loop

This is the final demonstration of DAWN's recursive symbolic regulation system.
"""

import asyncio
import time
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

# Import all integration components
try:
    from cognition_runtime import process_cognition_tick, log_event, get_cognition_runtime
    from .tick_integration import integrate_with_tick_loop, setup_gui_integration
    from .voice_symbolic_integration import start_symbolic_voice_monitoring, stop_symbolic_voice_monitoring
    INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some integration components not available: {e}")
    INTEGRATION_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("complete_integration_demo")

class CompleteIntegrationDemo:
    """
    Complete demonstration of DAWN's integrated symbolic reflex system.
    
    Shows all four integration layers working together:
    - Cognition runtime processing
    - Tick loop integration
    - Voice narration
    - GUI event emission
    """
    
    def __init__(self):
        """Initialize the complete integration demo"""
        self.demo_running = False
        self.gui_events = []
        self.voice_narrator = None
        
        # Demo scenarios
        self.scenarios = {
            'awakening': self._scenario_cognitive_awakening,
            'thermal_spike': self._scenario_thermal_spike,
            'drift_cascade': self._scenario_drift_cascade,
            'symbolic_emergence': self._scenario_symbolic_emergence,
            'memory_storm': self._scenario_memory_storm
        }
        
        logger.info("🎯 Complete Integration Demo initialized")
    
    def mock_window_emit(self, event_type: str, data: Any):
        """Mock window.emit function for GUI event demonstration"""
        gui_event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'data': data
        }
        
        self.gui_events.append(gui_event)
        logger.info(f"📡 GUI Event: {event_type} - {data.get('type', 'unknown')}")
        
        # Show how GUI would receive this
        if event_type == 'symbolic_alert':
            alert_type = data.get('type', 'unknown')
            if alert_type == 'TRACER':
                tracer = data.get('tracer_type', 'unknown')
                severity = data.get('severity', 'info')
                message = data.get('message', '')
                print(f"  🎯 GUI Alert: [{tracer.upper()}] {severity} - {message}")
            elif alert_type == 'ROOT':
                root_type = data.get('root_type', 'unknown')
                symbolic_root = data.get('symbolic_root', 'unknown')
                print(f"  ✨ GUI Root: {root_type} - {symbolic_root}")
    
    async def run_complete_demo(self, scenario: str = 'awakening'):
        """Run the complete integration demo with specified scenario"""
        if not INTEGRATION_AVAILABLE:
            print("❌ Integration components not available - cannot run demo")
            return
        
        if scenario not in self.scenarios:
            print(f"❌ Unknown scenario: {scenario}")
            print(f"Available scenarios: {list(self.scenarios.keys())}")
            return
        
        print(f"\n🚀 Starting Complete Integration Demo: {scenario}")
        print("=" * 60)
        
        self.demo_running = True
        
        try:
            # 1. Setup GUI integration
            print("📡 Setting up GUI integration...")
            setup_gui_integration(self.mock_window_emit)
            
            # 2. Start voice monitoring  
            print("🔊 Starting voice monitoring...")
            self.voice_narrator = start_symbolic_voice_monitoring({
                'throttle_window': 5  # Faster for demo
            })
            
            # 3. Run the scenario
            print(f"🎭 Running scenario: {scenario}")
            await self.scenarios[scenario]()
            
            # 4. Show results
            await self._show_integration_results()
            
        except Exception as e:
            logger.error(f"Error in complete demo: {e}")
        finally:
            self.demo_running = False
            
            # Cleanup
            if self.voice_narrator:
                stop_symbolic_voice_monitoring()
    
    async def _scenario_cognitive_awakening(self):
        """Scenario: Cognitive awakening with progressive complexity"""
        scenario_states = [
            {
                'name': 'Initial Awareness',
                'state': {
                    'tick_id': 10001,
                    'entropy': 0.3,
                    'heat': 0.2,
                    'coherence': 0.9,
                    'complexity': 0.4,
                    'memory_activity': 0.3,
                    'forecast_reliability': 0.8
                }
            },
            {
                'name': 'Growing Complexity', 
                'state': {
                    'tick_id': 10002,
                    'entropy': 0.6,
                    'heat': 0.5,
                    'coherence': 0.8,
                    'complexity': 0.7,
                    'memory_activity': 0.6,
                    'forecast_reliability': 0.6
                }
            },
            {
                'name': 'Symbolic Emergence',
                'state': {
                    'tick_id': 10003,
                    'entropy': 0.7,
                    'heat': 0.4,
                    'coherence': 0.9,
                    'complexity': 0.8,
                    'memory_activity': 0.8,
                    'forecast_reliability': 0.7
                }
            }
        ]
        
        for step in scenario_states:
            print(f"\n  🧠 {step['name']}")
            await self._process_integrated_state(step['state'])
            await asyncio.sleep(2)
    
    async def _scenario_thermal_spike(self):
        """Scenario: Thermal regulation under pressure"""
        states = [
            {'tick_id': 20001, 'heat': 0.9, 'coherence': 0.4, 'entropy': 0.8},
            {'tick_id': 20002, 'heat': 0.95, 'coherence': 0.3, 'entropy': 0.9},
            {'tick_id': 20003, 'heat': 0.6, 'coherence': 0.7, 'entropy': 0.5}  # Recovery
        ]
        
        for state in states:
            await self._process_integrated_state(state)
            await asyncio.sleep(1.5)
    
    async def _scenario_drift_cascade(self):
        """Scenario: Progressive drift detection and correction"""
        states = [
            {'tick_id': 30001, 'entropy': 0.8, 'coherence': 0.5, 'forecast_reliability': 0.3},
            {'tick_id': 30002, 'entropy': 0.9, 'coherence': 0.3, 'forecast_reliability': 0.2},
            {'tick_id': 30003, 'entropy': 0.6, 'coherence': 0.8, 'forecast_reliability': 0.7}  # Recovery
        ]
        
        for state in states:
            await self._process_integrated_state(state)
            await asyncio.sleep(1.5)
    
    async def _scenario_symbolic_emergence(self):
        """Scenario: Major symbolic pattern formation"""
        states = [
            {
                'tick_id': 40001,
                'coherence': 0.9,
                'complexity': 0.8,
                'memory_activity': 0.9,
                'symbolic_significance': 0.9
            }
        ]
        
        for state in states:
            await self._process_integrated_state(state)
            await asyncio.sleep(2)
    
    async def _scenario_memory_storm(self):
        """Scenario: High memory network activity"""
        states = [
            {'tick_id': 50001, 'memory_activity': 0.9, 'complexity': 0.8, 'coherence': 0.7},
            {'tick_id': 50002, 'memory_activity': 0.95, 'complexity': 0.9, 'coherence': 0.8}
        ]
        
        for state in states:
            await self._process_integrated_state(state)
            await asyncio.sleep(1.5)
    
    async def _process_integrated_state(self, state: Dict[str, Any]):
        """Process a state through the complete integration stack"""
        # Add default values
        full_state = {
            'entropy': 0.5,
            'heat': 0.3,
            'coherence': 0.8,
            'mood': 0.5,
            'complexity': 0.5,
            'memory_activity': 0.0,
            'forecast_reliability': 0.7,
            **state
        }
        
        # Process through integrated tick loop
        result = integrate_with_tick_loop(full_state)
        
        # Show results
        cognition_result = result['cognition_result']
        if cognition_result['status'] == 'success':
            alerts = len(cognition_result['tracer_alerts'])
            roots = len(cognition_result['symbolic_roots'])
            
            print(f"    Tick {full_state['tick_id']}: {alerts} alerts, {roots} roots")
            
            # Show specific alerts
            for alert in cognition_result['tracer_alerts']:
                tracer = alert['tracer_type']
                severity = alert['severity']
                message = alert['message'][:50] + "..." if len(alert['message']) > 50 else alert['message']
                print(f"      🔍 {tracer}: {severity} - {message}")
            
            # Show symbolic roots
            for root in cognition_result['symbolic_roots']:
                root_type = root['type']
                symbolic_root = root['symbolic_root']
                print(f"      ✨ {root_type}: {symbolic_root}")
    
    async def _show_integration_results(self):
        """Show the results of the complete integration"""
        print(f"\n📊 Integration Results")
        print("=" * 40)
        
        # Show cognition runtime stats
        if INTEGRATION_AVAILABLE:
            runtime = get_cognition_runtime()
            stats = runtime.get_runtime_stats()
            
            print(f"🧠 Cognition Runtime:")
            print(f"  Total ticks: {stats['tick_count']}")
            print(f"  Alerts generated: {stats['alert_count']}")
            print(f"  Symbolic roots: {stats['symbolic_root_count']}")
            print(f"  Memory connections: {stats['memory_connection_count']}")
        
        # Show GUI events
        print(f"\n📡 GUI Events:")
        print(f"  Total events emitted: {len(self.gui_events)}")
        
        event_types = {}
        for event in self.gui_events:
            event_type = event['event_type']
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        for event_type, count in event_types.items():
            print(f"  {event_type}: {count}")
        
        # Show voice status
        if self.voice_narrator:
            status = self.voice_narrator.get_status()
            print(f"\n🔊 Voice System:")
            print(f"  Running: {status['running']}")
            print(f"  TTS Available: {status['tts_available']}")
            print(f"  Queue size: {status['queue_size']}")
        
        # Show log files created
        print(f"\n📄 Log Files Created:")
        runtime_logs = Path("runtime/logs")
        if runtime_logs.exists():
            for log_file in runtime_logs.glob("*.log"):
                size = log_file.stat().st_size
                print(f"  {log_file.name}: {size} bytes")
        
        runtime_memory = Path("runtime/memory")
        if runtime_memory.exists():
            for memory_file in runtime_memory.glob("*.json"):
                size = memory_file.stat().st_size
                print(f"  {memory_file.name}: {size} bytes")

def run_demo_scenario(scenario: str = 'awakening'):
    """Run a specific demo scenario"""
    demo = CompleteIntegrationDemo()
    asyncio.run(demo.run_complete_demo(scenario))

def show_integration_guide():
    """Show the complete integration guide"""
    print("🎯 DAWN Complete Integration Guide")
    print("=" * 50)
    
    print("\n1. 🧠 Tick Loop Integration:")
    print("""
# In your tick_loop.py:
from .tick_integration import integrate_with_tick_loop

async def _execute_tick(self):
    # ... existing tick processing ...
    
    # Write to .mmap
    self._write_mmap_state(current_state)
    
    # INTEGRATE COGNITION RUNTIME
    cognition_result = integrate_with_tick_loop(current_state)
    
    # Process results
    if cognition_result['cognition_result']['status'] == 'success':
        alerts = len(cognition_result['cognition_result']['tracer_alerts'])
        logger.info(f"🧠 Cognition: {alerts} symbolic alerts generated")
""")
    
    print("\n2. 📡 GUI Event Integration:")
    print("""
# Setup GUI integration:
from .tick_integration import setup_gui_integration

def emit_to_tauri(event_type, data):
    # Your Tauri integration
    window.emit(event_type, data)

setup_gui_integration(emit_to_tauri)

# GUI automatically receives:
# - "symbolic_alert" for tracer alerts and symbolic roots
# - "memory_update" for network growth events
""")
    
    print("\n3. 🔊 Voice System Integration:")
    print("""
# Start voice monitoring:
from .voice_symbolic_integration import start_symbolic_voice_monitoring

narrator = start_symbolic_voice_monitoring({
    'throttle_window': 30,  # seconds between duplicate messages
})

# Voice system automatically monitors:
# - runtime/logs/tracer_alerts.log
# - runtime/logs/root_trace.log  
# - runtime/logs/event_stream.log
""")
    
    print("\n4. 🧬 GUI Component Setup:")
    print("""
# Add to your React app:

import EnhancedSymbolicAlertPanel from './components/EnhancedSymbolicAlertPanel';
import EnhancedMyceliumOverlay from './components/EnhancedMyceliumOverlay';

// Components automatically connect to:
// - /api/logs/tracer_alerts (polling)
// - /api/logs/root_trace (polling)
// - /api/memory/mycelium_graph (polling)
// - window events (real-time)
""")
    
    print("\n5. 📊 API Endpoints:")
    print("""
# Add to your backend:

app.get('/api/logs/tracer_alerts', (req, res) => {
  res.sendFile(path.join(__dirname, 'runtime/logs/tracer_alerts.log'));
});

app.get('/api/logs/root_trace', (req, res) => {
  res.sendFile(path.join(__dirname, 'runtime/logs/root_trace.log'));
});

app.get('/api/memory/mycelium_graph', (req, res) => {
  res.sendFile(path.join(__dirname, 'runtime/memory/mycelium_graph.json'));
});
""")

def main():
    """Main demo function"""
    print("🧠 DAWN Complete Integration Demo")
    print("=" * 50)
    
    if not INTEGRATION_AVAILABLE:
        print("❌ Integration components not available")
        print("Please ensure all integration files are present:")
        print("  - cognition_runtime.py")
        print("  - tick_integration.py")
        print("  - voice_symbolic_integration.py")
        return
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == '--guide':
            show_integration_guide()
        elif command == '--scenario':
            scenario = sys.argv[2] if len(sys.argv) > 2 else 'awakening'
            run_demo_scenario(scenario)
        else:
            print(f"Unknown command: {command}")
    else:
        print("\nAvailable commands:")
        print("  python complete_integration_demo.py --guide")
        print("  python complete_integration_demo.py --scenario <scenario>")
        print("\nAvailable scenarios:")
        demo = CompleteIntegrationDemo()
        for scenario in demo.scenarios.keys():
            print(f"  - {scenario}")
        
        print("\nRunning default awakening scenario...")
        run_demo_scenario('awakening')

if __name__ == "__main__":
    main() 