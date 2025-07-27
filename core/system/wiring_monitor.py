# core/system/wiring_monitor.py
"""
DAWN Wiring Monitor - System Connection Verification
===================================================
Ensures all neural pathways are properly connected
"""

from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import inspect
import traceback


class ConnectionStatus(Enum):
    """Connection health states"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    BROKEN = "broken"
    UNTESTED = "untested"
    MISSING = "missing"


@dataclass
class ConnectionTest:
    """Test result for a single connection"""
    source: str
    target: str
    direction: str  # 'forward', 'reverse', 'bidirectional'
    status: ConnectionStatus
    latency_ms: Optional[float] = None
    last_activity: Optional[datetime] = None
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class WiringDiagnostics:
    """Complete wiring diagnostics report"""
    timestamp: datetime
    overall_health: bool
    connection_tests: List[ConnectionTest]
    system_states: Dict[str, Dict]
    warnings: List[str]
    critical_failures: List[str]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for Owl/Butler consumption"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'overall_health': self.overall_health,
            'connections': [
                {
                    'link': f"{test.source}→{test.target}",
                    'status': test.status.value,
                    'latency_ms': test.latency_ms,
                    'last_activity': test.last_activity.isoformat() if test.last_activity else None,
                    'error': test.error
                }
                for test in self.connection_tests
            ],
            'warnings': self.warnings,
            'critical_failures': self.critical_failures,
            'health_score': self.calculate_health_score()
        }
    
    def calculate_health_score(self) -> float:
        """Calculate overall health score (0.0 - 1.0)"""
        if not self.connection_tests:
            return 0.0
            
        scores = {
            ConnectionStatus.HEALTHY: 1.0,
            ConnectionStatus.DEGRADED: 0.7,
            ConnectionStatus.UNTESTED: 0.5,
            ConnectionStatus.BROKEN: 0.0,
            ConnectionStatus.MISSING: 0.0
        }
        
        total_score = sum(scores.get(test.status, 0) for test in self.connection_tests)
        return total_score / len(self.connection_tests)


class WiringMonitor:
    """
    Active monitoring of DAWN's internal wiring
    
    Verifies:
    - Method injections are intact
    - Event subscriptions are active
    - Queue connections are flowing
    - Bidirectional links are responsive
    """
    
    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator
        self.test_history: List[WiringDiagnostics] = []
        self.connection_activity: Dict[str, datetime] = {}
        
        # Define expected connections
        self.expected_connections = [
            ('bloom', 'pulse', 'bidirectional'),
            ('pulse', 'owl', 'forward'),
            ('owl', 'sigil', 'forward'),
            ('sigil', 'bloom', 'forward')
        ]
        
        # Connection test methods
        self.connection_tests = {
            'bloom→pulse': self._test_bloom_to_pulse,
            'pulse→bloom': self._test_pulse_to_bloom,
            'pulse→owl': self._test_pulse_to_owl,
            'owl→sigil': self._test_owl_to_sigil,
            'sigil→bloom': self._test_sigil_to_bloom
        }
        
    def verify_all_connections(self) -> Dict[str, Any]:
        """
        Comprehensive verification of all system connections
        
        Returns:
            Dictionary with diagnostic information or False if critical failure
        """
        print("🔍 Beginning wiring verification...")
        
        diagnostics = WiringDiagnostics(
            timestamp=datetime.now(),
            overall_health=True,
            connection_tests=[],
            system_states={},
            warnings=[],
            critical_failures=[]
        )
        
        # 1. Verify systems exist
        if not self._verify_systems_exist(diagnostics):
            diagnostics.overall_health = False
            return diagnostics.to_dict()
        
        # 2. Test each connection
        for source, target, direction in self.expected_connections:
            if direction == 'bidirectional':
                # Test both directions
                self._test_connection(source, target, 'forward', diagnostics)
                self._test_connection(target, source, 'reverse', diagnostics)
            else:
                self._test_connection(source, target, direction, diagnostics)
        
        # 3. Verify event bus connections
        self._verify_event_bus(diagnostics)
        
        # 4. Check queue health
        self._verify_queues(diagnostics)
        
        # 5. Test data flow
        self._verify_data_flow(diagnostics)
        
        # 6. Calculate overall health
        failed_tests = [t for t in diagnostics.connection_tests 
                       if t.status in [ConnectionStatus.BROKEN, ConnectionStatus.MISSING]]
        
        if failed_tests:
            diagnostics.overall_health = False
            diagnostics.critical_failures.append(
                f"{len(failed_tests)} connection(s) failed"
            )
        
        # 7. Store history
        self.test_history.append(diagnostics)
        if len(self.test_history) > 100:
            self.test_history.pop(0)
        
        # 8. Return results
        return diagnostics.to_dict()
    
    def _verify_systems_exist(self, diagnostics: WiringDiagnostics) -> bool:
        """Verify all required systems are present"""
        if not self.orchestrator or not hasattr(self.orchestrator, 'systems'):
            diagnostics.critical_failures.append("Orchestrator not initialized")
            return False
            
        required_systems = ['bloom', 'pulse', 'owl', 'sigil']
        missing = []
        
        for system in required_systems:
            if system not in self.orchestrator.systems:
                missing.append(system)
            else:
                # Capture system state
                sys_obj = self.orchestrator.systems[system]
                diagnostics.system_states[system] = {
                    'type': type(sys_obj).__name__,
                    'has_tick': hasattr(sys_obj, 'tick'),
                    'initialized': getattr(sys_obj, '_initialized', True)
                }
        
        if missing:
            diagnostics.critical_failures.append(f"Missing systems: {missing}")
            return False
            
        return True
    
    def _test_connection(self, source: str, target: str, direction: str, 
                        diagnostics: WiringDiagnostics):
        """Test a specific connection"""
        connection_key = f"{source}→{target}"
        
        if connection_key not in self.connection_tests:
            diagnostics.warnings.append(f"No test defined for {connection_key}")
            return
            
        test_result = ConnectionTest(
            source=source,
            target=target,
            direction=direction,
            status=ConnectionStatus.UNTESTED
        )
        
        try:
            # Run specific test
            start_time = datetime.now()
            test_passed, details = self.connection_tests[connection_key]()
            end_time = datetime.now()
            
            test_result.latency_ms = (end_time - start_time).total_seconds() * 1000
            test_result.status = ConnectionStatus.HEALTHY if test_passed else ConnectionStatus.BROKEN
            test_result.metadata = details
            
            if test_passed:
                self.connection_activity[connection_key] = datetime.now()
                test_result.last_activity = self.connection_activity.get(connection_key)
                
        except Exception as e:
            test_result.status = ConnectionStatus.BROKEN
            test_result.error = str(e)
            diagnostics.warnings.append(f"Test failed for {connection_key}: {e}")
            
        diagnostics.connection_tests.append(test_result)
    
    def _test_bloom_to_pulse(self) -> Tuple[bool, Dict]:
        """Test bloom → pulse connection"""
        bloom = self.orchestrator.systems.get('bloom')
        pulse = self.orchestrator.systems.get('pulse')
        
        if not bloom or not pulse:
            return False, {'error': 'Systems not found'}
        
        # Check if bloom's spawn method is wrapped
        if hasattr(bloom.spawn_bloom, '__wrapped__'):
            # Method is properly wrapped
            return True, {'method': 'wrapped', 'type': 'direct'}
        
        # Check if pulse has modulation method
        if hasattr(pulse, 'modulate_from_bloom'):
            return True, {'method': 'modulate_from_bloom', 'type': 'interface'}
            
        return False, {'error': 'No connection method found'}
    
    def _test_pulse_to_bloom(self) -> Tuple[bool, Dict]:
        """Test pulse → bloom feedback"""
        pulse = self.orchestrator.systems.get('pulse')
        bloom = self.orchestrator.systems.get('bloom')
        
        if not pulse or not bloom:
            return False, {'error': 'Systems not found'}
            
        # Check for feedback mechanism
        if hasattr(bloom, 'receive_pulse_feedback'):
            return True, {'method': 'receive_pulse_feedback'}
            
        # Check event bus subscription
        if self.orchestrator.event_bus:
            subs = self.orchestrator.event_bus.get_subscribers('pulse.state_change')
            if any('bloom' in str(sub) for sub in subs):
                return True, {'method': 'event_bus', 'type': 'async'}
                
        return False, {'error': 'No feedback path found'}
    
    def _test_pulse_to_owl(self) -> Tuple[bool, Dict]:
        """Test pulse → owl connection"""
        pulse = self.orchestrator.systems.get('pulse')
        owl = self.orchestrator.systems.get('owl')
        
        if not pulse or not owl:
            return False, {'error': 'Systems not found'}
            
        # Check for tick callbacks
        if hasattr(pulse, 'on_tick_callbacks'):
            callbacks = pulse.on_tick_callbacks
            if any('owl' in str(cb) or 'reflect' in str(cb) for cb in callbacks):
                return True, {'method': 'tick_callbacks', 'count': len(callbacks)}
                
        # Check reflection queue
        if hasattr(self.orchestrator, 'reflection_queue'):
            return True, {'method': 'queue', 'type': 'async'}
            
        return False, {'error': 'No trigger mechanism found'}
    
    def _test_owl_to_sigil(self) -> Tuple[bool, Dict]:
        """Test owl → sigil connection"""
        owl = self.orchestrator.systems.get('owl')
        sigil = self.orchestrator.systems.get('sigil')
        
        if not owl or not sigil:
            return False, {'error': 'Systems not found'}
            
        # Check if log_reflection is wrapped
        if hasattr(owl.log_reflection, '__wrapped__'):
            return True, {'method': 'wrapped', 'type': 'direct'}
            
        # Check for direct sigil emission
        if hasattr(sigil, 'receive_observation'):
            return True, {'method': 'receive_observation'}
            
        return False, {'error': 'No observation path found'}
    
    def _test_sigil_to_bloom(self) -> Tuple[bool, Dict]:
        """Test sigil → bloom connection"""
        sigil = self.orchestrator.systems.get('sigil')
        bloom = self.orchestrator.systems.get('bloom')
        
        if not sigil or not bloom:
            return False, {'error': 'Systems not found'}
            
        # Check for emit callbacks
        if hasattr(sigil, 'on_emit_callbacks'):
            callbacks = sigil.on_emit_callbacks
            if any('bloom' in str(cb) or 'spawn' in str(cb) for cb in callbacks):
                return True, {'method': 'emit_callbacks', 'count': len(callbacks)}
                
        # Check event subscription
        if self.orchestrator.event_bus:
            subs = self.orchestrator.event_bus.get_subscribers('sigil.emitted')
            if any('bloom' in str(sub) for sub in subs):
                return True, {'method': 'event_bus'}
                
        return False, {'error': 'No seeding mechanism found'}
    
    def _verify_event_bus(self, diagnostics: WiringDiagnostics):
        """Verify event bus connections"""
        if not hasattr(self.orchestrator, 'event_bus'):
            diagnostics.warnings.append("No event bus found")
            return
            
        bus = self.orchestrator.event_bus
        
        # Check for expected event patterns
        expected_events = [
            'bloom.spawned',
            'pulse.state_change',
            'owl.reflection',
            'sigil.emitted'
        ]
        
        for event in expected_events:
            subs = bus.get_subscribers(event) if hasattr(bus, 'get_subscribers') else []
            if not subs:
                diagnostics.warnings.append(f"No subscribers for {event}")
    
    def _verify_queues(self, diagnostics: WiringDiagnostics):
        """Check queue health"""
        queues = ['pulse_queue', 'bloom_queue', 'reflection_queue']
        
        for queue_name in queues:
            if hasattr(self.orchestrator, queue_name):
                q = getattr(self.orchestrator, queue_name)
                if hasattr(q, 'qsize'):
                    size = q.qsize()
                    if size > 1000:
                        diagnostics.warnings.append(
                            f"{queue_name} may be backed up: {size} items"
                        )
    
    def _verify_data_flow(self, diagnostics: WiringDiagnostics):
        """Test actual data flow through connections"""
        # This would ideally send test signals through the system
        # For now, check last activity timestamps
        
        stale_threshold = 300  # 5 minutes
        now = datetime.now()
        
        for connection, last_active in self.connection_activity.items():
            age = (now - last_active).total_seconds()
            if age > stale_threshold:
                diagnostics.warnings.append(
                    f"{connection} inactive for {age:.0f} seconds"
                )
    
    def get_connection_graph(self) -> Dict[str, List[str]]:
        """Return connection graph for visualization"""
        graph = {}
        
        for test in self.test_history[-1].connection_tests if self.test_history else []:
            if test.source not in graph:
                graph[test.source] = []
            if test.status == ConnectionStatus.HEALTHY:
                graph[test.source].append(test.target)
                
        return graph
    
    def get_health_summary(self) -> str:
        """Get human-readable health summary"""
        if not self.test_history:
            return "No diagnostics available"
            
        latest = self.test_history[-1]
        health_score = latest.calculate_health_score()
        
        summary = f"""
🔌 DAWN Wiring Health Report
===========================
Time: {latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Overall Health: {'✅ HEALTHY' if latest.overall_health else '❌ UNHEALTHY'}
Health Score: {health_score:.1%}

Connections:
"""
        for test in latest.connection_tests:
            icon = {
                ConnectionStatus.HEALTHY: '✅',
                ConnectionStatus.DEGRADED: '⚠️',
                ConnectionStatus.BROKEN: '❌',
                ConnectionStatus.MISSING: '❓',
                ConnectionStatus.UNTESTED: '🔍'
            }.get(test.status, '?')
            
            summary += f"  {icon} {test.source} → {test.target}: {test.status.value}\n"
            
        if latest.warnings:
            summary += f"\nWarnings ({len(latest.warnings)}):\n"
            for warning in latest.warnings[:5]:  # First 5 warnings
                summary += f"  ⚠️ {warning}\n"
                
        if latest.critical_failures:
            summary += f"\nCritical Failures:\n"
            for failure in latest.critical_failures:
                summary += f"  ❌ {failure}\n"
                
        return summary