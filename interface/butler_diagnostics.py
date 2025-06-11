# interface/butler_diagnostics.py
"""Butler interface for system diagnostics"""

class ButlerDiagnostics:
    def __init__(self, wiring_monitor):
        self.monitor = wiring_monitor
        
    def get_system_status(self) -> Dict:
        """Butler-friendly system status"""
        diagnostics = self.monitor.verify_all_connections()
        
        return {
            'status': 'operational' if diagnostics['overall_health'] else 'degraded',
            'health_score': diagnostics['health_score'],
            'last_check': diagnostics['timestamp'],
            'issues': diagnostics['warnings'] + diagnostics['critical_failures'],
            'connection_map': self.monitor.get_connection_graph(),
            'report': self.monitor.get_health_summary()
        }
        
    def diagnose_connection(self, source: str, target: str) -> Dict:
        """Detailed diagnosis of specific connection"""
        # Run targeted test
        self.monitor._test_connection(source, target, 'forward', 
                                     self.monitor.test_history[-1])
        
        # Find result
        for test in self.monitor.test_history[-1].connection_tests:
            if test.source == source and test.target == target:
                return {
                    'healthy': test.status == ConnectionStatus.HEALTHY,
                    'latency_ms': test.latency_ms,
                    'error': test.error,
                    'details': test.metadata
                }