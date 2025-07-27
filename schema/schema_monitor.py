"""
DAWN Schema Monitoring System
=============================
Consolidates: schema_decay_handler.py, schema_suppressor.py, 
             schema_anomaly_logger.py, schema_coherence_tracker.py
Generated: 2025-06-04 21:31
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import deque
from datetime import datetime


class SchemaMonitor:
    """
    Unified schema monitoring system
    Handles decay, suppression, anomalies, and coherence tracking
    """
    
    def __init__(self, log_dir: str = "logs/schema"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Tracking structures
        self.cooldown_log = []
        self.anomaly_log = []
        self.coherence_history = deque(maxlen=100)
        self.decay_candidates = set()
        
        # Suppression state
        self.suppression_active = False
        self.suppression_level = 0.0
        self.suppression_reason = None
        
    def trigger_suppression(self, reason: str = "unknown", level: float = 0.0):
        """Trigger schema suppression event"""
        event = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "reason": reason,
            "level": round(level, 3),
            "action": "schema_cooldown"
        }
        
        self.cooldown_log.append(event)
        self.suppression_active = True
        self.suppression_level = level
        self.suppression_reason = reason
        
        print(f"[Monitor] ⛔ Triggered suppression due to {reason.upper()} | Level={level:.2f}")
        
        # Try to adjust tick interval
        try:
            from core.tick_engine import adjust_tick_interval
            adjust_tick_interval(multiplier=1.5)  # Slow by 50%
        except ImportError:
            print("[Monitor] ⚠️ Tick adjustment unavailable")
            
        # Log to file
        self._log_event("suppression", event)
        
        return event
    
    def decay_schema_memory(self):
        """Handle schema memory decay"""
        decay_count = 0
        
        # Check sigil memory ring
        try:
            from semantic.sigil_ring import sigil_memory_ring
            
            for sigil_id, sigil in sigil_memory_ring.items():
                if sigil.heat < 0.05 and sigil.entropy > 0.8:
                    sigil.connected = False
                    self.decay_candidates.add(sigil_id)
                    decay_count += 1
                    print(f"[Monitor] 🧊 Sigil {sigil_id} marked for decay")
                    
        except ImportError:
            print("[Monitor] ⚠️ Sigil ring unavailable for decay check")
        
        # Log decay pass
        self._log_event("decay", {
            "timestamp": datetime.now().isoformat(),
            "decay_count": decay_count,
            "candidates": list(self.decay_candidates)
        })
        
        print(f"[Monitor] 🧹 Schema decay pass complete ({decay_count} items)")
        
        return decay_count
    
    def log_anomaly(self, anomaly_type: str, details: str, severity: str = "INFO"):
        """Log schema anomaly"""
        anomaly = {
            "timestamp": datetime.now().isoformat(),
            "type": anomaly_type,
            "details": details,
            "severity": severity
        }
        
        self.anomaly_log.append(anomaly)
        
        # Print based on severity
        if severity == "CRITICAL":
            print(f"[Monitor] 🔴 CRITICAL ANOMALY: {anomaly_type} - {details}")
        elif severity == "WARNING":
            print(f"[Monitor] ⚠️ Warning: {anomaly_type} - {details}")
        else:
            print(f"[Monitor] 📝 {anomaly_type}: {details}")
        
        # Log to file
        self._log_event("anomaly", anomaly)
        
        # Check if suppression needed
        if severity == "CRITICAL":
            self.trigger_suppression(f"anomaly_{anomaly_type}", 0.8)
        
        return anomaly
    
    def track_coherence(self, coherence_score: float, components: Optional[Dict] = None):
        """Track schema coherence over time"""
        coherence_entry = {
            "timestamp": datetime.now().isoformat(),
            "score": round(coherence_score, 4),
            "components": components or {},
            "suppression_active": self.suppression_active
        }
        
        self.coherence_history.append(coherence_entry)
        
        # Check for coherence issues
        if coherence_score < 0.3:
            self.log_anomaly(
                "LOW_COHERENCE",
                f"Coherence dropped to {coherence_score:.3f}",
                "WARNING"
            )
        
        # Log significant changes
        if len(self.coherence_history) > 1:
            prev_score = self.coherence_history[-2]["score"]
            delta = abs(coherence_score - prev_score)
            
            if delta > 0.2:
                self.log_anomaly(
                    "COHERENCE_SPIKE",
                    f"Rapid change: {prev_score:.3f} → {coherence_score:.3f}",
                    "INFO"
                )
        
        return coherence_entry
    
    def get_cooldown_events(self) -> List[Dict]:
        """Get suppression/cooldown history"""
        return self.cooldown_log
    
    def get_recent_anomalies(self, limit: int = 10) -> List[Dict]:
        """Get recent anomalies"""
        return self.anomaly_log[-limit:]
    
    def get_coherence_trend(self) -> Dict[str, Any]:
        """Analyze coherence trend"""
        if not self.coherence_history:
            return {"trend": "no_data"}
        
        scores = [entry["score"] for entry in self.coherence_history]
        recent_avg = sum(scores[-10:]) / len(scores[-10:])
        overall_avg = sum(scores) / len(scores)
        
        if recent_avg > overall_avg + 0.05:
            trend = "improving"
        elif recent_avg < overall_avg - 0.05:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "current": scores[-1],
            "recent_average": recent_avg,
            "overall_average": overall_avg,
            "min": min(scores),
            "max": max(scores)
        }
    
    def check_schema_health(self) -> Dict[str, Any]:
        """Comprehensive schema health check"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "suppression_active": self.suppression_active,
            "suppression_level": self.suppression_level,
            "anomaly_count": len(self.anomaly_log),
            "critical_anomalies": sum(1 for a in self.anomaly_log if a["severity"] == "CRITICAL"),
            "decay_candidates": len(self.decay_candidates),
            "coherence_trend": self.get_coherence_trend()
        }
        
        # Calculate overall health score
        health_score = 1.0
        
        if self.suppression_active:
            health_score -= 0.3
        
        health_score -= (health_report["critical_anomalies"] * 0.1)
        health_score -= (len(self.decay_candidates) * 0.02)
        
        if health_report["coherence_trend"]["trend"] == "declining":
            health_score -= 0.2
        
        health_report["health_score"] = max(0.0, min(1.0, health_score))
        
        # Determine status
        if health_score > 0.8:
            health_report["status"] = "healthy"
        elif health_score > 0.5:
            health_report["status"] = "stressed"
        else:
            health_report["status"] = "critical"
        
        return health_report
    
    def _log_event(self, event_type: str, event_data: Dict):
        """Log event to file"""
        log_file = self.log_dir / f"{event_type}_log.jsonl"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            json.dump(event_data, f)
            f.write('\n')
    
    def reset_suppression(self):
        """Reset suppression state"""
        self.suppression_active = False
        self.suppression_level = 0.0
        self.suppression_reason = None
        
        print("[Monitor] ✅ Suppression reset")
        
        # Try to restore normal tick rate
        try:
            from core.tick_engine import adjust_tick_interval
            adjust_tick_interval(multiplier=1.0)
        except ImportError:
            pass
    
    def cleanup_decay_candidates(self) -> int:
        """Clean up decayed items"""
        cleaned = 0
        
        try:
            from semantic.sigil_ring import sigil_memory_ring
            
            for sigil_id in list(self.decay_candidates):
                if sigil_id in sigil_memory_ring:
                    del sigil_memory_ring[sigil_id]
                    cleaned += 1
                    
            self.decay_candidates.clear()
            
        except ImportError:
            print("[Monitor] ⚠️ Cannot clean decay candidates")
        
        if cleaned > 0:
            print(f"[Monitor] 🗑️ Cleaned {cleaned} decayed items")
            
        return cleaned


# Global monitor instance
schema_monitor = SchemaMonitor()


# =============== CONVENIENCE FUNCTIONS ===============

def trigger_suppression(reason: str = "unknown", level: float = 0.0):
    """Trigger schema suppression"""
    return schema_monitor.trigger_suppression(reason, level)

def decay_schema_memory():
    """Run decay pass on schema memory"""
    return schema_monitor.decay_schema_memory()

def log_anomaly(anomaly_type: str, details: str, severity: str = "INFO"):
    """Log schema anomaly"""
    return schema_monitor.log_anomaly(anomaly_type, details, severity)

def get_cooldown_events():
    """Get suppression history"""
    return schema_monitor.get_cooldown_events()

def check_schema_health():
    """Get schema health report"""
    return schema_monitor.check_schema_health()
