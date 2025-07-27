"""
Schema Anomaly Logger - Logging system for schema anomalies and deviations
"""

import logging
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('schema_anomaly')

class SchemaAnomalyLogger:
    """Logs and tracks schema anomalies in the system"""
    
    def __init__(self):
        """Initialize the schema anomaly logger"""
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        self.anomaly_file = os.path.join(self.log_dir, 'schema_anomalies.json')
        logger.info("Initialized SchemaAnomalyLogger")
    
    def log_anomaly(self, 
                   anomaly_type: str,
                   details: Dict[str, Any],
                   severity: str = 'warning',
                   context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a schema anomaly
        
        Args:
            anomaly_type: Type of anomaly detected
            details: Detailed information about the anomaly
            severity: Severity level ('info', 'warning', 'error', 'critical')
            context: Additional context information
        """
        # Create anomaly entry
        anomaly = {
            'timestamp': datetime.now().isoformat(),
            'type': anomaly_type,
            'severity': severity,
            'details': details,
            'context': context or {}
        }
        
        # Log to console
        log_method = getattr(logger, severity.lower(), logger.warning)
        log_method(f"Schema Anomaly: {anomaly_type} - {details}")
        
        # Log to file
        with open(self.anomaly_file, 'a') as f:
            f.write(json.dumps(anomaly) + '\n')
    
    def get_anomalies(self, 
                     anomaly_type: Optional[str] = None,
                     severity: Optional[str] = None,
                     limit: int = 100) -> list:
        """
        Retrieve logged anomalies with optional filtering
        
        Args:
            anomaly_type: Filter by anomaly type
            severity: Filter by severity level
            limit: Maximum number of anomalies to return
            
        Returns:
            List of matching anomalies
        """
        if not os.path.exists(self.anomaly_file):
            return []
            
        anomalies = []
        with open(self.anomaly_file, 'r') as f:
            for line in f:
                try:
                    anomaly = json.loads(line)
                    if (anomaly_type is None or anomaly['type'] == anomaly_type) and \
                       (severity is None or anomaly['severity'] == severity):
                        anomalies.append(anomaly)
                        if len(anomalies) >= limit:
                            break
                except json.JSONDecodeError:
                    continue
                    
        return anomalies

# Global instance
_anomaly_logger = None

def log_anomaly(anomaly_type: str,
                details: Dict[str, Any],
                severity: str = 'warning',
                context: Optional[Dict[str, Any]] = None) -> None:
    """Log a schema anomaly using the global logger instance"""
    global _anomaly_logger
    if _anomaly_logger is None:
        _anomaly_logger = SchemaAnomalyLogger()
    _anomaly_logger.log_anomaly(anomaly_type, details, severity, context)

__all__ = ['log_anomaly', 'SchemaAnomalyLogger'] 