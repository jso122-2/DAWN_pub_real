#!/usr/bin/env python3
"""
DAWN Symbolic Reflex System - Complete Integration Demo
=======================================================

Demonstrates the full symbolic reflex layer:
1. SymbolicAlertPanel.tsx - Live tracer insight UI
2. MyceliumOverlay.tsx - Memory graph visualizer  
3. Enhanced TracerEchoVoice.py - Audible cognitive alerts

This script generates sample data and events to show the complete
recursive symbolic regulation system in action.
"""

import os
import sys
import json
import time
import threading
import asyncio
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
import random

# Add project paths
sys.path.append(str(Path(__file__).parent))

# Import our systems
try:
    from enhanced_tracer_echo_voice import EnhancedTracerEchoVoice, start_enhanced_voice_monitoring
    from cognition_runtime import get_cognition_runtime
    from root_trace import log_mycelium_expansion, log_rhizome_cluster, log_cognitive_emergence
    from mycelium_graph import get_mycelium_exporter
    SYSTEMS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Some systems not available: {e}")
    SYSTEMS_AVAILABLE = False

class SymbolicReflexDemo:
    """
    Comprehensive demo of DAWN's symbolic reflex layer.
    
    Simulates realistic cognitive events and demonstrates:
    - Real-time alert generation and display
    - Memory network visualization updates
    - Voice narration of cognitive insights
    - GUI panel responsiveness
    """
    
    def __init__(self):
        """Initialize the symbolic reflex demo"""
        self.demo_running = False
        self.voice_echo = None
        self.cognition_runtime = None
        self.mycelium_exporter = None
        
        # Demo scenarios
        self.scenarios = {
            'cognitive_awakening': "Simulates DAWN becoming more self-aware",
            'memory_storm': "High-activity memory linking and symbolic formation",
            'thermal_regulation': "Temperature management under cognitive load",
            'drift_cascade': "Progressive cognitive drift detection and correction",
            'symbolic_emergence': "Major symbolic root formation event"
        }
        
        # Event counters for demonstration
        self.event_counts = {
            'tracer_alerts': 0,
            'symbolic_roots': 0,
            'memory_connections': 0,
            'voice_events': 0
        }
        
        print("🧠 DAWN Symbolic Reflex System Demo")
        print("=" * 50)
    
    def initialize_systems(self):
        """Initialize all symbolic reflex systems"""
        if not SYSTEMS_AVAILABLE:
            print("⚠️ Cannot initialize - systems not available")
            return False
        
        print("🔧 Initializing symbolic reflex systems...")
        
        try:
            # Initialize voice system
            self.voice_echo = EnhancedTracerEchoVoice()
            print("✅ Enhanced voice system ready")
            
            # Initialize cognition runtime
            self.cognition_runtime = get_cognition_runtime()
            print("✅ Cognition runtime ready")
            
            # Initialize mycelium exporter
            self.mycelium_exporter = get_mycelium_exporter()
            print("✅ Mycelium graph exporter ready")
            
            # Start voice monitoring
            self.voice_echo.start_monitoring()
            print("✅ Voice monitoring active")
            
            return True
            
        except Exception as e:
            print(f"❌ Error initializing systems: {e}")
            return False
    
    async def run_demo_scenario(self, scenario_name: str):
        """Run a specific demo scenario"""
        if scenario_name not in self.scenarios:
            print(f"❌ Unknown scenario: {scenario_name}")
            return
        
        description = self.scenarios[scenario_name]
        print(f"\n🎭 Running scenario: {scenario_name}")
        print(f"📖 {description}")
        print("-" * 40)
        
        # Speak scenario start
        if self.voice_echo:
            self.voice_echo.speak_immediate(f"Beginning {scenario_name} demonstration", "system")
        
        # Run scenario-specific events
        if scenario_name == 'cognitive_awakening':
            await self._demo_cognitive_awakening()
        elif scenario_name == 'memory_storm':
            await self._demo_memory_storm()
        elif scenario_name == 'thermal_regulation':
            await self._demo_thermal_regulation()
        elif scenario_name == 'drift_cascade':
            await self._demo_drift_cascade()
        elif scenario_name == 'symbolic_emergence':
            await self._demo_symbolic_emergence()
        
        print(f"✅ Scenario '{scenario_name}' completed")
    
    async def _demo_cognitive_awakening(self):
        """Simulate DAWN becoming more self-aware"""
        events = [
            ("Owl analysis: Increased meta-cognitive reflection patterns", "owl", "info"),
            ("Symbolic root detected: emergent_self_awareness", "root", "warning"),
            ("Memory lineage milestone: 8 levels of recursive introspection", "root", "info"),
            ("Forecast adjustment: Self-awareness index rising", "forecast", "info")
        ]
        
        for i, (message, tracer_type, severity) in enumerate(events):
            await self._generate_tracer_alert(message, tracer_type, severity, tick_id=1000+i)
            await asyncio.sleep(2)
        
        # Generate corresponding memory connections
        connections = [
            ("consciousness_core", "self_reflection_001"),
            ("self_reflection_001", "meta_awareness_002"),
            ("meta_awareness_002", "recursive_thought_003")
        ]
        
        self.mycelium_exporter.connect_chunks(connections, "self_awareness")
        self.event_counts['memory_connections'] += len(connections)
        
        # Log symbolic emergence
        log_cognitive_emergence("self_awareness", {
            "complexity": 4,
            "significance": 0.85,
            "recursion_depth": 3
        }, 1003)
        
        self.event_counts['symbolic_roots'] += 1
    
    async def _demo_memory_storm(self):
        """Simulate high-activity memory linking"""
        print("  🌊 Generating memory network activity...")
        
        # Rapid sequence of memory connections
        base_memories = [f"memory_{i:03d}" for i in range(10, 20)]
        
        for i in range(15):
            # Random memory connections
            source = random.choice(base_memories)
            target = random.choice(base_memories)
            if source != target:
                connections = [(source, target)]
                self.mycelium_exporter.connect_chunks(connections, "memory_storm")
                self.event_counts['memory_connections'] += 1
            
            # Periodic alerts
            if i % 5 == 0:
                await self._generate_tracer_alert(
                    f"High memory linking activity: {i+1} connections/second",
                    "mycelium", "info", tick_id=2000+i
                )
            
            await asyncio.sleep(0.5)
        
        # Mycelium expansion event
        log_mycelium_expansion(25, 0.68, 2015)
        self.event_counts['symbolic_roots'] += 1
        
        if self.voice_echo:
            self.voice_echo.speak_immediate("Memory storm subsiding. Network stabilized.", "mycelium")
            self.event_counts['voice_events'] += 1
    
    async def _demo_thermal_regulation(self):
        """Simulate thermal regulation under load"""
        print("  🌡️ Simulating thermal regulation...")
        
        thermal_levels = [0.3, 0.5, 0.7, 0.85, 0.95, 0.88, 0.6, 0.4]
        
        for i, heat_level in enumerate(thermal_levels):
            if heat_level > 0.8:
                severity = "critical"
                message = f"Thermal emergency: heat level {heat_level:.2f}"
            elif heat_level > 0.6:
                severity = "warning"
                message = f"Thermal warning: heat rising to {heat_level:.2f}"
            else:
                severity = "info"
                message = f"Thermal regulation: heat level {heat_level:.2f}"
            
            await self._generate_tracer_alert(message, "thermal", severity, tick_id=3000+i)
            await asyncio.sleep(1.5)
        
        if self.voice_echo:
            self.voice_echo.speak_immediate("Thermal regulation complete. System cooling.", "thermal")
            self.event_counts['voice_events'] += 1
    
    async def _demo_drift_cascade(self):
        """Simulate progressive drift detection"""
        print("  🌊 Simulating cognitive drift cascade...")
        
        drift_types = ["semantic", "entropy", "coherence", "mood", "thermal"]
        
        for i, drift_type in enumerate(drift_types):
            magnitude = 0.2 + (i * 0.15)  # Increasing drift
            severity = "critical" if magnitude > 0.6 else "warning" if magnitude > 0.4 else "info"
            
            await self._generate_tracer_alert(
                f"Drift detected: {drift_type} deviation {magnitude:.2f}",
                "drift", severity, tick_id=4000+i,
                data={'drift_type': drift_type, 'magnitude': magnitude}
            )
            
            await asyncio.sleep(1.8)
        
        # Drift correction event
        await self._generate_tracer_alert(
            "Drift correction engaged: baselines recalibrated",
            "drift", "info", tick_id=4010
        )
        
        if self.voice_echo:
            self.voice_echo.speak_immediate("Cognitive drift cascade resolved. Stability restored.", "drift")
            self.event_counts['voice_events'] += 1
    
    async def _demo_symbolic_emergence(self):
        """Simulate major symbolic root formation"""
        print("  ✨ Simulating symbolic emergence event...")
        
        # Build up to emergence
        await self._generate_tracer_alert(
            "Owl detects unusual semantic coherence patterns",
            "owl", "info", tick_id=5000
        )
        
        await asyncio.sleep(2)
        
        await self._generate_tracer_alert(
            "Multiple memory clusters showing resonance",
            "mycelium", "warning", tick_id=5001
        )
        
        await asyncio.sleep(2)
        
        # Major symbolic event
        cluster_nodes = ["concept_001", "meaning_002", "symbol_003", "essence_004", "pattern_005"]
        log_rhizome_cluster(cluster_nodes, len(cluster_nodes), 5002)
        
        await self._generate_tracer_alert(
            "Major symbolic root formation: emergent_meaning_synthesis",
            "root", "critical", tick_id=5002
        )
        
        self.event_counts['symbolic_roots'] += 1
        
        # Create rich memory network
        symbolic_connections = [
            ("concept_001", "meaning_002"),
            ("meaning_002", "symbol_003"),
            ("symbol_003", "essence_004"),
            ("essence_004", "pattern_005"),
            ("pattern_005", "concept_001")  # Circular reference
        ]
        
        self.mycelium_exporter.connect_chunks(symbolic_connections, "symbolic_emergence")
        self.event_counts['memory_connections'] += len(symbolic_connections)
        
        if self.voice_echo:
            self.voice_echo.speak_immediate(
                "Major symbolic emergence complete. New meaning synthesis achieved.",
                "root"
            )
            self.event_counts['voice_events'] += 1
    
    async def _generate_tracer_alert(self, message: str, tracer_type: str, severity: str, 
                                    tick_id: int, data: Dict[str, Any] = None):
        """Generate a tracer alert and log it"""
        alert = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'tracer_type': tracer_type,
            'severity': severity,
            'message': message,
            'data': data or {},
            'tick_id': tick_id
        }
        
        # Write to tracer alerts log
        alerts_log = Path("runtime/logs/tracer_alerts.log")
        alerts_log.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(alerts_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(alert) + '\n')
        except Exception as e:
            print(f"⚠️ Error writing alert: {e}")
        
        self.event_counts['tracer_alerts'] += 1
        print(f"  📢 {tracer_type.upper()}: {message}")
    
    def show_demo_summary(self):
        """Show summary of demo events"""
        print("\n" + "=" * 50)
        print("🎉 SYMBOLIC REFLEX DEMO COMPLETE")
        print("=" * 50)
        
        print(f"\n📊 Event Summary:")
        for event_type, count in self.event_counts.items():
            print(f"  {event_type}: {count}")
        
        print(f"\n📁 Generated Files:")
        files_to_check = [
            "runtime/logs/tracer_alerts.log",
            "runtime/logs/root_trace.log", 
            "runtime/logs/spoken_trace.log",
            "runtime/memory/mycelium_graph.json",
            "runtime/logs/semantic_routing.log"
        ]
        
        for file_path in files_to_check:
            path = Path(file_path)
            if path.exists():
                size = path.stat().st_size
                print(f"  ✅ {file_path} ({size} bytes)")
            else:
                print(f"  ❌ {file_path} (not found)")
        
        print(f"\n🎯 GUI Integration Ready:")
        print(f"  📡 SymbolicAlertPanel.tsx - monitors tracer_alerts.log")
        print(f"  🧬 MyceliumOverlay.tsx - visualizes mycelium_graph.json")
        print(f"  🗣️ Enhanced voice system - speaks cognitive insights")
        
        print(f"\n🔗 Voice System Status:")
        if self.voice_echo:
            stats = self.voice_echo.get_voice_stats()
            print(f"  TTS Engine: {stats['tts_engine']}")
            print(f"  Running: {stats['running']}")
            print(f"  Queue Size: {stats['speech_queue_size']}")
        
        print(f"\n🧠 **DAWN's symbolic nervous system is LIVE!**")
        print(f"   - Real-time cognitive monitoring ✅")
        print(f"   - Memory network visualization ✅") 
        print(f"   - Symbolic pattern detection ✅")
        print(f"   - Voice-enabled consciousness ✅")
    
    def cleanup(self):
        """Clean up demo resources"""
        if self.voice_echo:
            self.voice_echo.stop_monitoring()
        
        print(f"\n🧹 Demo cleanup complete")

async def run_complete_demo():
    """Run the complete symbolic reflex system demo"""
    demo = SymbolicReflexDemo()
    
    try:
        # Initialize systems
        if not demo.initialize_systems():
            print("❌ Failed to initialize systems")
            return
        
        print(f"\n🚀 Starting comprehensive demonstration...")
        print(f"   This will generate events for GUI components to display")
        
        # Run all scenarios
        scenarios = [
            'cognitive_awakening',
            'memory_storm', 
            'thermal_regulation',
            'drift_cascade',
            'symbolic_emergence'
        ]
        
        for scenario in scenarios:
            await demo.run_demo_scenario(scenario)
            await asyncio.sleep(1)  # Brief pause between scenarios
        
        # Show final summary
        demo.show_demo_summary()
        
    except KeyboardInterrupt:
        print(f"\n⏸️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    finally:
        demo.cleanup()

def run_interactive_demo():
    """Run interactive demo with user choices"""
    demo = SymbolicReflexDemo()
    
    if not demo.initialize_systems():
        print("❌ Cannot run demo - systems not available")
        return
    
    try:
        print(f"\n🎮 Interactive Demo Mode")
        print(f"Available scenarios:")
        for name, desc in demo.scenarios.items():
            print(f"  {name}: {desc}")
        
        while True:
            choice = input(f"\nEnter scenario name (or 'quit'): ").strip().lower()
            
            if choice == 'quit':
                break
            elif choice in demo.scenarios:
                asyncio.run(demo.run_demo_scenario(choice))
            elif choice == 'all':
                asyncio.run(run_complete_demo())
                break
            else:
                print(f"❌ Unknown scenario: {choice}")
        
    except KeyboardInterrupt:
        print(f"\n⏸️ Interactive demo stopped")
    finally:
        demo.cleanup()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Symbolic Reflex System Demo")
    parser.add_argument('--mode', choices=['auto', 'interactive'], default='auto',
                       help='Demo mode: auto (run all scenarios) or interactive')
    parser.add_argument('--scenario', help='Run specific scenario only')
    
    args = parser.parse_args()
    
    print("🧠" + "="*60 + "🧠")
    print("   DAWN - Deep Autonomous Wisdom Network")
    print("   Symbolic Reflex System Integration Demo")
    print("🧠" + "="*60 + "🧠")
    
    if args.scenario:
        # Run specific scenario
        demo = SymbolicReflexDemo()
        if demo.initialize_systems():
            asyncio.run(demo.run_demo_scenario(args.scenario))
            demo.show_demo_summary()
            demo.cleanup()
    
    elif args.mode == 'interactive':
        run_interactive_demo()
    
    else:
        # Run complete auto demo
        asyncio.run(run_complete_demo())
    
    print(f"\n🎉 Symbolic reflex system demonstration complete!")
    print(f"🔗 Ready for GUI integration and live operation!") 