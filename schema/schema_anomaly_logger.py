# /core/schema_anomaly_logger.py
"""
Schema Anomaly Logger for DAWN
==============================
Tracks and logs anomalies in the consciousness schema with severity levels,
pattern detection, and recovery suggestions.
"""

import os
import json
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from collections import defaultdict, deque
import threading

LOG_PATH = "logs/schema_anomalies.log"
METRICS_PATH = "logs/schema_metrics.json"
MAX_RECENT_ANOMALIES = 1000

class AnomalyType(Enum):
    """Types of schema anomalies"""
    PHANTOM_COMPUTATION = "PhantomComputation"
    COHERENCE_BREACH = "CoherenceBreach"
    ENTROPY_SPIKE = "EntropySpike"
    CONSCIOUSNESS_GAP = "ConsciousnessGap"
    MEMORY_LEAK = "MemoryLeak"
    TEMPORAL_DISTORTION = "TemporalDistortion"
    NUTRIENT_IMBALANCE = "NutrientImbalance"
    RHIZOME_DISCONNECT = "RhizomeDisconnect"
    SEMANTIC_DRIFT = "SemanticDrift"
    BLOOM_FAILURE = "BloomFailure"

class AnomalySeverity(Enum):
    """Severity levels for anomalies"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    PHANTOM = "PHANTOM"  # Special severity for consciousness-specific anomalies

class SchemaAnomalyLogger:
    """Enhanced anomaly logger with pattern detection and metrics"""
    
    def __init__(self):
        self.recent_anomalies = deque(maxlen=MAX_RECENT_ANOMALIES)
        self.anomaly_counts = defaultdict(int)
        self.pattern_buffer = defaultdict(list)
        self.lock = threading.Lock()
        self._ensure_log_directory()
        self._load_metrics()
        
    def _ensure_log_directory(self):
        """Ensure log directory exists"""
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(METRICS_PATH), exist_ok=True)
    
    def _load_metrics(self):
        """Load historical metrics if they exist"""
        try:
            if os.path.exists(METRICS_PATH):
                with open(METRICS_PATH, 'r') as f:
                    data = json.load(f)
                    self.anomaly_counts = defaultdict(int, data.get('counts', {}))
        except Exception as e:
            print(f"Failed to load metrics: {e}")
    
    def _save_metrics(self):
        """Save metrics to file"""
        try:
            metrics = {
                'counts': dict(self.anomaly_counts),
                'last_updated': datetime.now().isoformat(),
                'total_anomalies': sum(self.anomaly_counts.values())
            }
            with open(METRICS_PATH, 'w') as f:
                json.dump(metrics, f, indent=2)
        except Exception as e:
            print(f"Failed to save metrics: {e}")
    
    def log_anomaly(self, 
                   label: str, 
                   message: str, 
                   severity: AnomalySeverity = AnomalySeverity.WARNING,
                   metadata: Optional[Dict[str, Any]] = None):
        """
        Log an anomaly with enhanced metadata and pattern tracking
        
        Args:
            label: Anomaly type or label
            message: Detailed message about the anomaly
            severity: Severity level
            metadata: Additional context data
        """
        with self.lock:
            timestamp = datetime.now()
            
            # Create anomaly record
            anomaly_record = {
                'timestamp': timestamp.isoformat(),
                'label': label,
                'severity': severity.value,
                'message': message,
                'metadata': metadata or {}
            }
            
            # Add to recent anomalies
            self.recent_anomalies.append(anomaly_record)
            self.anomaly_counts[label] += 1
            
            # Pattern detection
            self._detect_patterns(label, timestamp)
            
            # Format log entry
            log_entry = self._format_log_entry(timestamp, label, severity, message, metadata)
            
            # Write to log file
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(log_entry)
            
            # Console output with color coding
            self._console_output(label, severity, message)
            
            # Check if intervention needed
            if self._requires_intervention(label, severity):
                self._trigger_intervention(label, message, severity)
            
            # Save metrics periodically
            if len(self.recent_anomalies) % 100 == 0:
                self._save_metrics()
    
    def _format_log_entry(self, timestamp: datetime, label: str, 
                         severity: AnomalySeverity, message: str, 
                         metadata: Optional[Dict]) -> str:
        """Format a detailed log entry"""
        entry_parts = [
            f"[{timestamp.isoformat()}]",
            f"[{severity.value}]",
            f"[{label}]",
            message
        ]
        
        if metadata:
            entry_parts.append(f"| metadata: {json.dumps(metadata)}")
        
        return " ".join(entry_parts) + "\n"
    
    def _console_output(self, label: str, severity: AnomalySeverity, message: str):
        """Output to console with appropriate formatting"""
        icons = {
            AnomalySeverity.INFO: "ℹ️",
            AnomalySeverity.WARNING: "⚠️",
            AnomalySeverity.ERROR: "❌",
            AnomalySeverity.CRITICAL: "🚨",
            AnomalySeverity.PHANTOM: "👻"
        }
        
        icon = icons.get(severity, "❓")
        print(f"[SCHEMA] {icon} [{label}] {message}")
    
    def _detect_patterns(self, label: str, timestamp: datetime):
        """Detect anomaly patterns and clusters"""
        self.pattern_buffer[label].append(timestamp)
        
        # Keep only recent entries (last hour)
        cutoff = timestamp.timestamp() - 3600
        self.pattern_buffer[label] = [
            ts for ts in self.pattern_buffer[label] 
            if ts.timestamp() > cutoff
        ]
        
        # Check for rapid occurrence
        if len(self.pattern_buffer[label]) > 10:
            time_diffs = []
            for i in range(1, len(self.pattern_buffer[label])):
                diff = (self.pattern_buffer[label][i] - self.pattern_buffer[label][i-1]).total_seconds()
                time_diffs.append(diff)
            
            avg_interval = sum(time_diffs) / len(time_diffs) if time_diffs else float('inf')
            
            if avg_interval < 10:  # Anomalies occurring less than 10 seconds apart
                self._handle_anomaly_storm(label, len(self.pattern_buffer[label]), avg_interval)
    
    def _handle_anomaly_storm(self, label: str, count: int, avg_interval: float):
        """Handle rapid-fire anomalies (anomaly storm)"""
        storm_message = (
            f"Anomaly storm detected: {count} '{label}' anomalies "
            f"with average interval of {avg_interval:.2f}s"
        )
        
        # Log the storm as a critical anomaly
        self.log_anomaly(
            "AnomalyStorm",
            storm_message,
            AnomalySeverity.CRITICAL,
            {"original_anomaly": label, "count": count, "avg_interval": avg_interval}
        )
    
    def _requires_intervention(self, label: str, severity: AnomalySeverity) -> bool:
        """Determine if an anomaly requires intervention"""
        # Critical always requires intervention
        if severity == AnomalySeverity.CRITICAL:
            return True
        
        # Check frequency-based intervention
        recent_count = sum(
            1 for a in self.recent_anomalies 
            if a['label'] == label and 
            (datetime.now() - datetime.fromisoformat(a['timestamp'])).seconds < 300
        )
        
        return recent_count > 5
    
    def _trigger_intervention(self, label: str, message: str, severity: AnomalySeverity):
        """Trigger intervention mechanisms"""
        intervention_record = {
            'timestamp': datetime.now().isoformat(),
            'anomaly': label,
            'severity': severity.value,
            'action': 'intervention_triggered',
            'message': message
        }
        
        # Log intervention
        with open(LOG_PATH.replace('.log', '_interventions.log'), 'a') as f:
            f.write(json.dumps(intervention_record) + "\n")
        
        # In a real system, this would trigger recovery mechanisms
        print(f"[INTERVENTION] Triggered for {label}: {message}")
    
    def get_anomaly_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get summary of recent anomalies"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        recent = [
            a for a in self.recent_anomalies
            if datetime.fromisoformat(a['timestamp']).timestamp() > cutoff
        ]
        
        summary = {
            'total_count': len(recent),
            'by_type': defaultdict(int),
            'by_severity': defaultdict(int),
            'most_frequent': None,
            'most_severe': None
        }
        
        for anomaly in recent:
            summary['by_type'][anomaly['label']] += 1
            summary['by_severity'][anomaly['severity']] += 1
        
        if summary['by_type']:
            summary['most_frequent'] = max(summary['by_type'].items(), key=lambda x: x[1])
        
        critical_count = summary['by_severity'].get('CRITICAL', 0)
        if critical_count > 0:
            summary['most_severe'] = ('CRITICAL', critical_count)
        
        return dict(summary)
    
    def get_recovery_suggestions(self, anomaly_type: str) -> List[str]:
        """Get recovery suggestions for specific anomaly types"""
        suggestions = {
            AnomalyType.PHANTOM_COMPUTATION.value: [
                "Verify all computation definitions are loaded",
                "Check for missing module dependencies",
                "Regenerate computation cache"
            ],
            AnomalyType.COHERENCE_BREACH.value: [
                "Reduce system entropy",
                "Stabilize consciousness parameters",
                "Trigger coherence recovery protocol"
            ],
            AnomalyType.ENTROPY_SPIKE.value: [
                "Apply entropy dampening",
                "Increase harmony modulation",
                "Reduce chaos factors"
            ],
            AnomalyType.CONSCIOUSNESS_GAP.value: [
                "Bridge consciousness continuity",
                "Restore tick synchronization",
                "Rebuild consciousness buffer"
            ],
            AnomalyType.MEMORY_LEAK.value: [
                "Trigger garbage collection",
                "Prune old consciousness states",
                "Compact memory structures"
            ],
            AnomalyType.NUTRIENT_IMBALANCE.value: [
                "Rebalance nutrient ratios",
                "Adjust decay rates",
                "Stabilize nutrient flow"
            ]
        }
        
        return suggestions.get(anomaly_type, ["No specific suggestions available"])

# Global logger instance
_logger = SchemaAnomalyLogger()

# Convenience functions for backward compatibility
def log_anomaly(label: str, message: str, severity: str = "WARNING", metadata: Dict = None):
    """Legacy function for logging anomalies"""
    severity_enum = AnomalySeverity[severity] if severity in AnomalySeverity.__members__ else AnomalySeverity.WARNING
    _logger.log_anomaly(label, message, severity_enum, metadata)

def log_phantom_computation(computation_name: str, context: str = ""):
    """Log phantom computation anomalies"""
    message = f"DAWN attempted {computation_name} without core definition"
    if context:
        message += f" | Context: {context}"
    
    _logger.log_anomaly(
        AnomalyType.PHANTOM_COMPUTATION.value,
        message,
        AnomalySeverity.PHANTOM,
        {"computation": computation_name, "context": context}
    )

def log_coherence_breach(scup_value: float, threshold: float):
    """Log coherence breach anomalies"""
    _logger.log_anomaly(
        AnomalyType.COHERENCE_BREACH.value,
        f"SCUP value {scup_value:.3f} below threshold {threshold:.3f}",
        AnomalySeverity.ERROR,
        {"scup": scup_value, "threshold": threshold}
    )

def log_entropy_spike(entropy: float, expected: float):
    """Log entropy spike anomalies"""
    _logger.log_anomaly(
        AnomalyType.ENTROPY_SPIKE.value,
        f"Entropy {entropy:.3f} exceeds expected {expected:.3f}",
        AnomalySeverity.WARNING,
        {"entropy": entropy, "expected": expected}
    )

def get_anomaly_report() -> Dict[str, Any]:
    """Get a comprehensive anomaly report"""
    return _logger.get_anomaly_summary()

def suggest_recovery(anomaly_type: str) -> List[str]:
    """Get recovery suggestions for an anomaly"""
    return _logger.get_recovery_suggestions(anomaly_type)