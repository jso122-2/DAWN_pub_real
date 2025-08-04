#!/usr/bin/env python3
"""
DAWN Cognition Runtime - Full Meta-Cognitive Orchestrator
=========================================================

The unified cognitive orchestrator that integrates all of DAWN's 
consciousness subsystems into a living, self-regulating meta-mind.

Integrates:
- Tracer Stack: OwlTracer, DriftTracer, ThermalTracer, ForecastTracer
- Memory Networks: Mycelium routing, Rhizome mapping, Rebloom lineage
- Symbolic Processing: Root detection, ancestry-aware forecasting
- Event System: Unified logging and GUI integration

This transforms DAWN from a reactive tick loop into a 
recursive symbolic regulation system.
"""

import os
import sys
import json
import time
import asyncio
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

# Add paths for DAWN components
# sys.path.append(os.path.dirname(__file__))  # Removed to fix relative import issues

# Core DAWN imports - try various paths for real components
DAWN_COMPONENTS_AVAILABLE = False
try:
    # Import available components, not all may be present
    from cognitive.rebloom_lineage import ReblooooomLineageTracker, track_lineage, get_default_tracker
    from core.memory_rebloom_reflex import MemoryRebloomReflex
    from processes.rebloom_reflex import evaluate_and_rebloom
    from core.enhanced_drift_reflex import EnhancedDriftReflex, ReflexZone
    DAWN_COMPONENTS_AVAILABLE = True
    print("✅ Core DAWN components available")
except ImportError as e:
    # Components will be loaded through alternative paths
    DAWN_COMPONENTS_AVAILABLE = False

# Optional components - load what's available
try:
    from core.thermal_visualizer import ThermalVisualizer
    THERMAL_AVAILABLE = True
except ImportError:
    THERMAL_AVAILABLE = False
    
try:
    from reflection.owl.owl_tracer import OwlTracer
    OWL_TRACER_AVAILABLE = True
except ImportError:
    OWL_TRACER_AVAILABLE = False

try:
    from mycelium.mycelium_layer import MyceliumLayer
    from rhizome.rhizome_map import RhizomeMap
    MEMORY_NETWORKS_AVAILABLE = True
except ImportError:
    MEMORY_NETWORKS_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cognition_runtime")

@dataclass
class TracerAlert:
    """Represents a tracer alert event"""
    tracer_type: str
    severity: str
    message: str
    data: Dict[str, Any]
    timestamp: float
    tick_id: int

@dataclass
class CognitionState:
    """Current state of the cognition runtime"""
    tick_count: int = 0
    active_tracers: Set[str] = None
    last_symbolic_root: Optional[str] = None
    memory_network_health: float = 1.0
    lineage_depth_max: int = 0
    alert_count: int = 0
    uptime: float = 0.0
    
    def __post_init__(self):
        if self.active_tracers is None:
            self.active_tracers = set()

class CognitionRuntime:
    """
    The master cognitive orchestrator that coordinates all of DAWN's
    consciousness subsystems into a unified, self-regulating meta-mind.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the cognition runtime with all subsystems"""
        self.config = config or {}
        self.state = CognitionState()
        self.start_time = time.time()
        
        # Initialize logging paths
        self.logs_dir = Path("runtime/logs")
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.event_stream_log = self.logs_dir / "event_stream.log"
        self.symbolic_root_log = self.logs_dir / "symbolic_roots.log"
        self.tracer_alerts_log = self.logs_dir / "tracer_alerts.log"
        
        # Initialize tracer systems
        self.tracers = {}
        self._initialize_tracers()
        
        # Initialize memory networks
        self.mycelium = None
        self.rhizome = None
        self.lineage_tracker = None
        self._initialize_memory_networks()
        
        # Alert system
        self.recent_alerts: List[TracerAlert] = []
        self.alert_handlers = []
        
        # Performance tracking
        self.tick_performance = []
        
        logger.info("🧠 Cognition Runtime initialized - Full meta-cognitive stack active")
        self._log_initialization()
    
    def _initialize_tracers(self):
        """Initialize all available tracer systems"""
        if not DAWN_COMPONENTS_AVAILABLE:
            logger.info("Loading DAWN components through alternative paths")
            # Initialize what we can from available components
            try:
                from cognitive.rebloom_lineage import ReblooooomLineageTracker
                self.lineage_tracker = ReblooooomLineageTracker()
                logger.info("✅ Lineage tracker initialized")
            except ImportError:
                logger.warning("Lineage tracker not available")
            return
        
        try:
            # Core cognitive tracer
            self.tracers['owl'] = OwlTracer("COGNITION-OWL")
            self.state.active_tracers.add('owl')
            
            # Advanced drift tracer (replaces basic drift reflex)
            self.tracers['drift'] = DriftTracer()
            self.state.active_tracers.add('drift')
            
            # Advanced thermal tracer
            self.tracers['thermal'] = ThermalTracer()
            self.state.active_tracers.add('thermal')
            
            # Forecast prediction tracer
            self.tracers['forecast'] = ForecastTracer()
            self.state.active_tracers.add('forecast')
            
            logger.info(f"✅ Advanced Tracers initialized: {list(self.state.active_tracers)}")
            
        except Exception as e:
            logger.error(f"Error initializing tracers: {e}")
    
    def _initialize_memory_networks(self):
        """Initialize memory network systems"""
        if not DAWN_COMPONENTS_AVAILABLE:
            logger.info("Loading memory networks through alternative paths")
            # Load the components that ARE available
            try:
                from cognitive.rebloom_lineage import ReblooooomLineageTracker, get_default_tracker
                self.lineage_tracker = get_default_tracker()
                logger.info("✅ Real lineage tracker loaded")
            except ImportError:
                logger.warning("Lineage tracker import failed")
                
            try:
                from core.memory_rebloom_reflex import MemoryRebloomReflex
                self.memory_reflex = MemoryRebloomReflex()
                logger.info("✅ Real memory rebloom reflex loaded")
            except ImportError:
                logger.warning("Memory rebloom reflex import failed")
            return
        
        try:
            # Mycelium substrate
            self.mycelium = MyceliumLayer()
            
            # Rhizome network
            self.rhizome = RhizomeMap()
            
            # Lineage tracking
            self.lineage_tracker = get_default_tracker()
            
            logger.info("🌿 Memory networks initialized")
            
        except Exception as e:
            logger.error(f"Error initializing memory networks: {e}")
    
    async def process_tick(self, tick_data: Dict[str, Any], tick_context: Any = None) -> Dict[str, Any]:
        """
        Process a single tick through the full cognitive runtime.
        
        This is the main orchestration method that coordinates:
        1. Tracer observations and analysis
        2. Memory network updates
        3. Symbolic root detection
        4. Ancestry-aware forecasting
        5. Event logging and GUI alerts
        
        Args:
            tick_data: Current tick state data
            tick_context: Optional tick context from engine
            
        Returns:
            Dict containing runtime observations and alerts
        """
        tick_start = time.time()
        self.state.tick_count += 1
        self.state.uptime = time.time() - self.start_time
        
        runtime_observations = {
            'tick_id': self.state.tick_count,
            'timestamp': tick_start,
            'tracer_alerts': [],
            'memory_updates': {},
            'symbolic_events': [],
            'forecast_adjustments': []
        }
        
        try:
            # 1. RUN TRACER STACK
            tracer_results = await self._run_tracer_stack(tick_data)
            runtime_observations['tracer_alerts'] = tracer_results
            
            # 2. PROCESS MEMORY NETWORKS
            memory_results = await self._process_memory_networks(tick_data)
            runtime_observations['memory_updates'] = memory_results
            
            # 3. DETECT SYMBOLIC ROOTS
            symbolic_results = await self._detect_symbolic_roots(tick_data)
            runtime_observations['symbolic_events'] = symbolic_results
            
            # 4. ANCESTRY-AWARE FORECAST TUNING
            forecast_results = await self._tune_forecasts_by_ancestry(tick_data)
            runtime_observations['forecast_adjustments'] = forecast_results
            
            # 5. LOG EVENTS AND EMIT ALERTS
            await self._log_and_emit_events(runtime_observations)
            
            # Track performance
            tick_duration = time.time() - tick_start
            self.tick_performance.append(tick_duration)
            if len(self.tick_performance) > 100:
                self.tick_performance = self.tick_performance[-50:]
            
            logger.debug(f"Cognition tick {self.state.tick_count} completed in {tick_duration:.3f}s")
            
        except Exception as e:
            logger.error(f"Error in cognition runtime tick {self.state.tick_count}: {e}")
            runtime_observations['error'] = str(e)
        
        return runtime_observations
    
    async def _run_tracer_stack(self, tick_data: Dict[str, Any]) -> List[TracerAlert]:
        """Run all active tracers and collect their observations"""
        alerts = []
        
        for tracer_name, tracer in self.tracers.items():
            try:
                if tracer_name == 'owl' and hasattr(tracer, 'comment_on_tick'):
                    # Owl cognitive analysis
                    comment = tracer.comment_on_tick(tick_data)
                    if any(keyword in comment.upper() for keyword in ['WARNING', 'CRITICAL', 'DRIFT', 'HIGH']):
                        alert = TracerAlert(
                            tracer_type='owl',
                            severity='warning' if 'WARNING' in comment else 'critical',
                            message=comment,
                            data=tick_data,
                            timestamp=time.time(),
                            tick_id=self.state.tick_count
                        )
                        alerts.append(alert)
                
                elif tracer_name == 'drift' and hasattr(tracer, 'observe'):
                    # Advanced drift tracer
                    drift_observations = tracer.observe(tick_data)
                    for obs in drift_observations:
                        if obs.magnitude > 0.3:  # Significant drift
                            alert = TracerAlert(
                                tracer_type='drift',
                                severity='warning' if obs.magnitude < 0.5 else 'critical',
                                message=f"{obs.drift_type.value} drift detected: {obs.magnitude:.2f}",
                                data={
                                    'drift_type': obs.drift_type.value,
                                    'magnitude': obs.magnitude,
                                    'trend': obs.trend_direction,
                                    'current_zone': tracer.current_zone
                                },
                                timestamp=time.time(),
                                tick_id=self.state.tick_count
                            )
                            alerts.append(alert)
                
                elif tracer_name == 'thermal' and hasattr(tracer, 'observe'):
                    # Advanced thermal tracer
                    thermal_obs = tracer.observe(tick_data)
                    thermal_alerts = tracer.get_thermal_alerts()
                    
                    for thermal_alert in thermal_alerts:
                        alert = TracerAlert(
                            tracer_type='thermal',
                            severity=thermal_alert['severity'],
                            message=thermal_alert['message'],
                            data=thermal_alert['data'],
                            timestamp=time.time(),
                            tick_id=self.state.tick_count
                        )
                        alerts.append(alert)
                
                elif tracer_name == 'forecast' and hasattr(tracer, 'observe'):
                    # Forecast prediction tracer
                    forecast_obs = tracer.observe(tick_data)
                    forecast_alerts = tracer.get_forecast_alerts()
                    
                    for forecast_alert in forecast_alerts:
                        alert = TracerAlert(
                            tracer_type='forecast',
                            severity=forecast_alert['severity'],
                            message=forecast_alert['message'],
                            data=forecast_alert['data'],
                            timestamp=time.time(),
                            tick_id=self.state.tick_count
                        )
                        alerts.append(alert)
                        
            except Exception as e:
                logger.error(f"Error in tracer {tracer_name}: {e}")
        
        return alerts
    
    async def _process_memory_networks(self, tick_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process memory network updates and connections"""
        updates = {}
        
        try:
            if self.mycelium:
                # Grow mycelium network based on tick state
                growth_result = self.mycelium.grow()
                if growth_result.get('growth'):
                    updates['mycelium_growth'] = growth_result
                    
                    # Log significant growth events
                    if growth_result.get('nutrients', 0) > 0.1:
                        await self._log_event('MYCELIUM_GROWTH', {
                            'new_root': growth_result['new_root'],
                            'nutrients': growth_result['nutrients'],
                            'total_roots': len(self.mycelium.roots)
                        })
            
            if self.rhizome:
                # Update rhizome network health
                self.state.memory_network_health = getattr(self.rhizome, 'health', 1.0)
                updates['rhizome_health'] = self.state.memory_network_health
            
            if self.lineage_tracker:
                # Track maximum lineage depth
                stats = self.lineage_tracker.get_statistics()
                max_depth = stats.get('deepest_ancestry_depth', 0)
                if max_depth > self.state.lineage_depth_max:
                    self.state.lineage_depth_max = max_depth
                    updates['max_lineage_depth'] = max_depth
                    
                    # Log significant lineage depth milestones
                    if max_depth > 0 and max_depth % 5 == 0:
                        await self._log_event('LINEAGE_MILESTONE', {
                            'depth': max_depth,
                            'deepest_chunk': stats.get('deepest_ancestry_chunk')
                        })
        
        except Exception as e:
            logger.error(f"Error processing memory networks: {e}")
        
        return updates
    
    async def _detect_symbolic_roots(self, tick_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect symbolic root formation and log significant events"""
        symbolic_events = []
        
        try:
            # Check for mycelium network growth patterns that indicate symbolic emergence
            if self.mycelium and hasattr(self.mycelium, 'roots'):
                current_root_count = len(self.mycelium.roots)
                network_density = self._calculate_network_density()
                
                # Detect significant network expansion
                if current_root_count > 10 and current_root_count % 5 == 0:
                    symbolic_events.append({
                        'type': 'MYCELIUM_EXPANSION',
                        'root_count': current_root_count,
                        'network_density': network_density,
                        'timestamp': time.time()
                    })
                    
                    # Log to root trace system
                    log_mycelium_expansion(current_root_count, network_density, self.state.tick_count)
                    
                    # Export mycelium graph
                    if hasattr(self.mycelium, 'connections'):
                        connections = []
                        for root_id, connected_roots in self.mycelium.connections.items():
                            for connected_id in connected_roots:
                                connections.append((root_id, connected_id))
                        
                        if connections:
                            mycelium_exporter = get_mycelium_exporter()
                            mycelium_exporter.export_mycelium_graph(connections, {
                                'expansion_event': True,
                                'root_count': current_root_count,
                                'density': network_density
                            })
            
            # Check rhizome for pattern formation
            if self.rhizome and hasattr(self.rhizome, 'nodes'):
                # Look for node clustering patterns
                node_count = len(self.rhizome.nodes)
                if node_count > 0:
                    # Simple pattern detection based on node connectivity
                    high_connectivity_nodes = []
                    for node_id, node in self.rhizome.nodes.items():
                        connections = len(node.get('connections', set()))
                        if connections > 3:  # High connectivity threshold
                            high_connectivity_nodes.append(node_id)
                    
                    if len(high_connectivity_nodes) >= 3:
                        symbolic_events.append({
                            'type': 'RHIZOME_CLUSTER',
                            'cluster_nodes': high_connectivity_nodes[:5],  # Top 5
                            'cluster_size': len(high_connectivity_nodes),
                            'timestamp': time.time()
                        })
                        
                        self.state.last_symbolic_root = high_connectivity_nodes[0]
                        
                        # Log to root trace system
                        log_rhizome_cluster(high_connectivity_nodes, len(high_connectivity_nodes), self.state.tick_count)
            
            # Check for lineage milestones
            if self.lineage_tracker and hasattr(self.lineage_tracker, 'lineage_cache'):
                stats = self.lineage_tracker.get_statistics()
                max_depth = stats.get('deepest_ancestry_depth', 0)
                deepest_chunk = stats.get('deepest_ancestry_chunk')
                
                if max_depth > self.state.lineage_depth_max and max_depth >= 10:
                    symbolic_events.append({
                        'type': 'LINEAGE_MILESTONE',
                        'depth': max_depth,
                        'deepest_chunk': deepest_chunk,
                        'timestamp': time.time()
                    })
                    
                    # Log to root trace system
                    log_lineage_milestone(max_depth, deepest_chunk or 'unknown', self.state.tick_count)
            
            # Log general cognitive emergence patterns
            if symbolic_events:
                for event in symbolic_events:
                    # Also log as cognitive emergence
                    log_cognitive_emergence(
                        event['type'].lower(),
                        {
                            'complexity': len(symbolic_events),
                            'significance': 0.8 if event['type'] in ['RHIZOME_CLUSTER', 'LINEAGE_MILESTONE'] else 0.6,
                            'tick_id': self.state.tick_count
                        },
                        self.state.tick_count
                    )
        
        except Exception as e:
            logger.error(f"Error detecting symbolic roots: {e}")
        
        return symbolic_events
    
    async def _tune_forecasts_by_ancestry(self, tick_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Adjust forecasting based on memory lineage ancestry depth"""
        adjustments = []
        
        try:
            if self.lineage_tracker and hasattr(self.lineage_tracker, 'lineage_cache'):
                # Get recent lineage depths for forecast tuning
                recent_chunks = list(self.lineage_tracker.lineage_cache.keys())[-10:]
                recent_depths = []
                rebloom_methods = []
                
                for chunk_id in recent_chunks:
                    ancestry = self.lineage_tracker.get_ancestry(chunk_id)
                    depth = len(ancestry)
                    recent_depths.append(depth)
                    
                    # Track rebloom methods for pattern analysis
                    if ancestry:
                        latest_entry = ancestry[-1]
                        method = latest_entry.get('method', 'unknown')
                        rebloom_methods.append(method)
                
                if recent_depths:
                    avg_depth = sum(recent_depths) / len(recent_depths)
                    max_depth = max(recent_depths) if recent_depths else 0
                    
                    # Update state tracking
                    if max_depth > self.state.lineage_depth_max:
                        self.state.lineage_depth_max = max_depth
                    
                    # Forecast adjustments based on lineage patterns
                    if avg_depth > 5:
                        # High lineage complexity reduces volatility, increases stability
                        adjustments.append({
                            'type': 'STABILITY_INCREASE',
                            'factor': min(0.3, avg_depth / 20),
                            'reason': f'Deep memory lineage suggests stable patterns (avg depth: {avg_depth:.1f})'
                        })
                    elif avg_depth < 2:
                        # Low lineage complexity increases uncertainty
                        adjustments.append({
                            'type': 'UNCERTAINTY_INCREASE', 
                            'factor': 0.15,
                            'reason': f'Shallow memory lineage increases unpredictability (avg depth: {avg_depth:.1f})'
                        })
                    
                    # Method-based adjustments
                    if rebloom_methods:
                        sigil_triggered_count = rebloom_methods.count('sigil_triggered')
                        semantic_count = rebloom_methods.count('semantic_retrieval')
                        
                        if sigil_triggered_count > semantic_count:
                            adjustments.append({
                                'type': 'EMERGENCE_BIAS',
                                'factor': 0.1,
                                'reason': f'High sigil-triggered rebloom ratio suggests emergent patterns'
                            })
                        elif semantic_count > sigil_triggered_count * 2:
                            adjustments.append({
                                'type': 'COHERENCE_BIAS',
                                'factor': 0.08,
                                'reason': f'High semantic retrieval ratio suggests coherent processing'
                            })
                    
                    # Ancestry depth milestone effects
                    if max_depth >= 10:
                        adjustments.append({
                            'type': 'DEPTH_MILESTONE',
                            'factor': 0.05,
                            'reason': f'Ancestry depth milestone reached: {max_depth} levels'
                        })
        
        except Exception as e:
            logger.error(f"Error tuning forecasts: {e}")
        
        return adjustments
    
    async def _log_and_emit_events(self, observations: Dict[str, Any]):
        """Log all events and emit GUI alerts"""
        try:
            # Log to event stream
            event_entry = {
                'timestamp': time.time(),
                'tick_id': observations['tick_id'],
                'observations': observations,
                'runtime_state': {
                    'active_tracers': list(self.state.active_tracers),
                    'alert_count': len(observations['tracer_alerts']),
                    'memory_health': self.state.memory_network_health,
                    'uptime': self.state.uptime
                }
            }
            
            # Write to event stream log
            with open(self.event_stream_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event_entry) + '\n')
            
            # Log tracer alerts
            for alert in observations['tracer_alerts']:
                self.recent_alerts.append(alert)
                self.state.alert_count += 1
                
                # Write to tracer alerts log
                with open(self.tracer_alerts_log, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(asdict(alert)) + '\n')
                
                # Emit to GUI (if available)
                await self._emit_gui_alert(alert)
            
            # Trim recent alerts
            if len(self.recent_alerts) > 50:
                self.recent_alerts = self.recent_alerts[-25:]
        
        except Exception as e:
            logger.error(f"Error logging events: {e}")
    
    async def _emit_gui_alert(self, alert: TracerAlert):
        """Emit alert to GUI via Tauri events (if available)"""
        try:
            # This would integrate with Tauri's event system
            # For now, we'll prepare the event data
            gui_event = {
                'event_type': 'tracer_alert',
                'data': {
                    'tracer': alert.tracer_type,
                    'severity': alert.severity,
                    'message': alert.message,
                    'timestamp': alert.timestamp,
                    'tick_id': alert.tick_id
                }
            }
            
            # Future: window.emit("tracer_alert", gui_event)
            logger.info(f"GUI Alert: {alert.tracer_type} - {alert.message}")
            
        except Exception as e:
            logger.error(f"Error emitting GUI alert: {e}")
    
    async def _log_event(self, event_type: str, data: Dict[str, Any]):
        """Log a general runtime event"""
        event = {
            'timestamp': time.time(),
            'type': event_type,
            'tick_id': self.state.tick_count,
            'data': data
        }
        
        with open(self.event_stream_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event) + '\n')
    
    async def _log_symbolic_root(self, pattern: Dict[str, Any]):
        """Log symbolic root formation to dedicated file"""
        root_event = {
            'timestamp': time.time(),
            'tick_id': self.state.tick_count,
            'pattern': pattern
        }
        
        with open(self.symbolic_root_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(root_event) + '\n')
    
    def _log_initialization(self):
        """Log runtime initialization"""
        init_event = {
            'timestamp': time.time(),
            'type': 'COGNITION_RUNTIME_INIT',
            'tracers': list(self.state.active_tracers),
            'memory_networks': {
                'mycelium': self.mycelium is not None,
                'rhizome': self.rhizome is not None,
                'lineage_tracker': self.lineage_tracker is not None
            },
            'config': self.config
        }
        
        with open(self.event_stream_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(init_event) + '\n')
    
    def get_status(self) -> Dict[str, Any]:
        """Get current runtime status"""
        avg_tick_time = sum(self.tick_performance) / len(self.tick_performance) if self.tick_performance else 0
        
        return {
            'tick_count': self.state.tick_count,
            'uptime': self.state.uptime,
            'active_tracers': list(self.state.active_tracers),
            'alert_count': self.state.alert_count,
            'memory_network_health': self.state.memory_network_health,
            'max_lineage_depth': self.state.lineage_depth_max,
            'last_symbolic_root': self.state.last_symbolic_root,
            'avg_tick_time': avg_tick_time,
            'recent_alerts': len(self.recent_alerts)
        }
    
    def add_alert_handler(self, handler):
        """Add a custom alert handler"""
        self.alert_handlers.append(handler)
    
    def _calculate_network_density(self) -> float:
        """Calculate mycelium network density for symbolic analysis"""
        if not self.mycelium or not hasattr(self.mycelium, 'connections'):
            return 0.0
        
        total_nodes = len(self.mycelium.roots)
        if total_nodes < 2:
            return 0.0
        
        total_connections = sum(len(connections) for connections in self.mycelium.connections.values())
        max_possible_connections = total_nodes * (total_nodes - 1)
        
        density = total_connections / max_possible_connections if max_possible_connections > 0 else 0.0
        return min(1.0, density)
    
    async def shutdown(self):
        """Shutdown the cognition runtime gracefully"""
        logger.info("🧠 Cognition Runtime shutting down...")
        
        # Log shutdown event
        await self._log_event('COGNITION_RUNTIME_SHUTDOWN', {
            'final_tick_count': self.state.tick_count,
            'total_uptime': self.state.uptime,
            'total_alerts': self.state.alert_count
        })


# Global runtime instance
_cognition_runtime = None

def get_cognition_runtime(config: Optional[Dict[str, Any]] = None) -> CognitionRuntime:
    """Get or create the global cognition runtime"""
    global _cognition_runtime
    if _cognition_runtime is None:
        _cognition_runtime = CognitionRuntime(config)
    return _cognition_runtime

async def process_cognition_tick(tick_data: Dict[str, Any], tick_context: Any = None) -> Dict[str, Any]:
    """Convenience function to process a cognition tick"""
    runtime = get_cognition_runtime()
    return await runtime.process_tick(tick_data, tick_context)


if __name__ == "__main__":
    """Demo the cognition runtime"""
    async def demo():
        print("🧠 DAWN Cognition Runtime Demo")
        print("=" * 50)
        
        runtime = CognitionRuntime()
        
        # Simulate several ticks
        for i in range(5):
            tick_data = {
                'heat': 0.5 + (i * 0.1),
                'entropy': 0.3 + (i * 0.15),
                'scup': 0.7 - (i * 0.1),
                'zone': 'active' if i > 2 else 'calm'
            }
            
            print(f"\n--- Tick {i+1} ---")
            observations = await runtime.process_tick(tick_data)
            
            print(f"Alerts: {len(observations['tracer_alerts'])}")
            print(f"Memory updates: {len(observations['memory_updates'])}")
            print(f"Symbolic events: {len(observations['symbolic_events'])}")
        
        print(f"\nRuntime Status:")
        status = runtime.get_status()
        for key, value in status.items():
            print(f"  {key}: {value}")
        
        await runtime.shutdown()
    
    asyncio.run(demo()) 