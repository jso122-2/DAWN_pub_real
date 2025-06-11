# core/system/wiring_monitor.py
"""
Wiring Monitor - Connection Health Checker
==========================================
Monitors the health of inter-system connections
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class WiringMonitor:
    """
    Monitors connection health between DAWN systems
    """
    
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.connection_health = {}
        self.last_check = None
        self.issues = []
        
    def verify_all_connections(self) -> Dict[str, Any]:
        """
        Verify all system connections are healthy
        
        Returns:
            Dict with connection health status
        """
        logger.debug("Verifying all system connections...")
        
        health_report = {
            'timestamp': datetime.now(),
            'connections': {},
            'systems': {},
            'issues': [],
            'overall_health': True
        }
        
        # Check each registered connection
        for conn in self.orchestrator.connections:
            conn_key = f"{conn.source}→{conn.target}"
            
            # Test connection
            is_healthy = self._test_connection(conn)
            health_report['connections'][conn_key] = {
                'healthy': is_healthy,
                'channel': conn.channel,
                'bidirectional': conn.bidirectional,
                'established': conn.established.isoformat()
            }
            
            if not is_healthy:
                health_report['overall_health'] = False
                issue = f"Connection {conn_key} via {conn.channel} is unhealthy"
                health_report['issues'].append(issue)
                self.issues.append((datetime.now(), issue))
        
        # Check each system
        for name, system in self.orchestrator.systems.items():
            health_report['systems'][name] = self._check_system_health(name, system)
            
        self.last_check = datetime.now()
        self.connection_health = health_report
        
        return health_report
        
    def _test_connection(self, conn) -> bool:
        """Test if a specific connection is working"""
        try:
            # Check if systems exist
            source_exists = conn.source in self.orchestrator.systems
            target_exists = conn.target in self.orchestrator.systems
            
            if not source_exists or not target_exists:
                return False
                
            # Check channel-specific health
            if conn.channel == 'event':
                # Check if event subscriptions exist
                return len(self.orchestrator.event_bus.get_subscribers(f"{conn.source}.*")) > 0
                
            elif conn.channel == 'direct':
                # Check if methods are properly wired
                source_sys = self.orchestrator.systems[conn.source]
                target_sys = self.orchestrator.systems[conn.target]
                return source_sys is not None and target_sys is not None
                
            elif conn.channel == 'queue':
                # Check if queues are accessible
                queue_name = f"{conn.source}_queue"
                return hasattr(self.orchestrator, queue_name)
                
            return True
            
        except Exception as e:
            logger.error(f"Error testing connection {conn.source}→{conn.target}: {e}")
            return False
            
    def _check_system_health(self, name: str, system: Any) -> Dict[str, Any]:
        """Check health of a specific system"""
        health = {
            'exists': system is not None,
            'type': type(system).__name__ if system else None,
            'responsive': False,
            'has_event_bus': False,
            'has_schema': False
        }
        
        if system:
            # Check responsiveness
            try:
                if hasattr(system, 'get_status'):
                    health['responsive'] = system.get_status() is not None
                elif hasattr(system, 'is_active'):
                    health['responsive'] = True
                    health['active'] = system.is_active()
            except:
                health['responsive'] = False
                
            # Check integrations
            health['has_event_bus'] = hasattr(system, 'event_bus')
            health['has_schema'] = hasattr(system, 'schema')
            
        return health
        
    def get_health_summary(self) -> str:
        """Get a human-readable health summary"""
        if not self.connection_health:
            return "No health check performed yet"
            
        report = self.connection_health
        
        summary = f"DAWN Wiring Health Report - {report['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += "=" * 60 + "\n"
        
        # Overall status
        status = "✅ HEALTHY" if report['overall_health'] else "❌ UNHEALTHY"
        summary += f"Overall Status: {status}\n\n"
        
        # Connections
        summary += "Connections:\n"
        for conn, info in report['connections'].items():
            status = "✓" if info['healthy'] else "✗"
            summary += f"  {status} {conn} [{info['channel']}]\n"
            
        # Systems
        summary += "\nSystems:\n"
        for name, info in report['systems'].items():
            status = "✓" if info['exists'] and info['responsive'] else "✗"
            summary += f"  {status} {name}: {info['type'] or 'Missing'}"
            if info.get('active') is not None:
                summary += f" (Active: {info['active']})"
            summary += "\n"
            
        # Issues
        if report['issues']:
            summary += "\nIssues:\n"
            for issue in report['issues']:
                summary += f"  ⚠️  {issue}\n"
                
        return summary
        
    def monitor_connection_latency(self, source: str, target: str) -> Optional[float]:
        """Measure latency between two systems"""
        # This would measure actual message passing time
        # For now, return a placeholder
        return 0.001  # 1ms
        
    def get_recent_issues(self, hours: int = 1) -> List[tuple]:
        """Get issues from the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [(ts, issue) for ts, issue in self.issues if ts > cutoff]