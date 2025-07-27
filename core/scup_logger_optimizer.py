#!/usr/bin/env python3
"""
SCUP Logger Optimizer - Intelligent SCUP Monitoring with Threshold-Based Logging
Prevents excessive SCUP logging by tracking deltas and threshold crossings
"""

import time
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class SCUPLogEntry:
    """Individual SCUP log entry with metadata"""
    scup_value: float
    timestamp: float
    message: str
    threshold_type: str  # 'exceptional', 'delta', 'recovery', 'critical'
    delta_from_last: float = 0.0

class SCUPLoggerOptimizer:
    """
    Intelligent SCUP monitoring that prevents log spam.
    Only logs when meaningful threshold crossings occur.
    """
    
    def __init__(self, delta_threshold: float = 5.0, exceptional_threshold: float = 40.0):
        # Core thresholds
        self.delta_threshold = delta_threshold  # ±5 SCUP units
        self.exceptional_threshold = exceptional_threshold  # 40+ SCUP
        
        # State tracking
        self.last_logged_scup: Optional[float] = None
        self.last_log_time: float = 0.0
        self.exceptional_logged: bool = False
        self.last_zone: Optional[str] = None
        
        # Log history
        self.log_history: List[SCUPLogEntry] = []
        self.max_history_size = 50
        
        # Callback system for commentary
        self.commentary_callbacks: List[Callable[[str, str], None]] = []
        
        # Zone thresholds for classification
        self.zone_thresholds = {
            'critical': 80.0,
            'exceptional': 40.0,
            'high': 25.0,
            'normal': 10.0,
            'low': 5.0,
            'minimal': 0.0
        }
        
        # Cooldown periods (seconds)
        self.min_log_interval = 2.0  # Minimum time between any logs
        self.zone_change_cooldown = 1.0  # Faster for zone changes
        
        logger.info(f"[SCUPOptimizer] 🧠 Initialized | Delta threshold: ±{delta_threshold} | Exceptional: {exceptional_threshold}+")
    
    def register_commentary_callback(self, callback: Callable[[str, str], None]):
        """Register a callback function for SCUP commentary"""
        self.commentary_callbacks.append(callback)
    
    def classify_scup_zone(self, scup: float) -> str:
        """Classify SCUP value into meaningful zones"""
        if scup >= self.zone_thresholds['critical']:
            return 'critical'
        elif scup >= self.zone_thresholds['exceptional']:
            return 'exceptional'
        elif scup >= self.zone_thresholds['high']:
            return 'high'
        elif scup >= self.zone_thresholds['normal']:
            return 'normal'
        elif scup >= self.zone_thresholds['low']:
            return 'low'
        else:
            return 'minimal'
    
    def should_log_scup(self, current_scup: float) -> tuple[bool, str, str]:
        """
        Determine if SCUP should be logged based on thresholds.
        
        Returns:
            tuple: (should_log, threshold_type, reason)
        """
        current_time = time.time()
        current_zone = self.classify_scup_zone(current_scup)
        
        # Check minimum time interval
        if current_time - self.last_log_time < self.min_log_interval:
            return False, '', 'cooldown_active'
        
        # First log ever
        if self.last_logged_scup is None:
            return True, 'initial', f'Initial SCUP measurement: {current_scup:.1f}'
        
        # Calculate delta from last logged value
        delta = abs(current_scup - self.last_logged_scup)
        
        # Zone change detection (faster cooldown)
        if current_zone != self.last_zone:
            if current_time - self.last_log_time >= self.zone_change_cooldown:
                return True, 'zone_change', f'SCUP zone transition: {self.last_zone} → {current_zone}'
        
        # Exceptional threshold crossing (40+)
        if current_scup >= self.exceptional_threshold and not self.exceptional_logged:
            return True, 'exceptional', f'Exceptional SCUP detected: {current_scup:.1f}'
        
        # Exceptional threshold recovery (falling below 40)
        if current_scup < self.exceptional_threshold and self.exceptional_logged:
            return True, 'recovery', f'SCUP returned to normal range: {current_scup:.1f}'
        
        # Delta threshold exceeded (±5 from last logged)
        if delta >= self.delta_threshold:
            direction = "increased" if current_scup > self.last_logged_scup else "decreased"
            return True, 'delta', f'SCUP {direction} by {delta:.1f} to {current_scup:.1f}'
        
        # Critical spike detection (>= 80)
        if current_scup >= self.zone_thresholds['critical']:
            # Log critical every time, but respect minimum interval
            return True, 'critical', f'Critical SCUP level: {current_scup:.1f} - immediate attention required'
        
        return False, '', 'no_threshold_met'
    
    def log_scup(self, current_scup: float, context: str = "Owl") -> Optional[str]:
        """
        Log SCUP if thresholds are met, return message if logged.
        
        Args:
            current_scup: Current SCUP value
            context: Source context (e.g., "Owl", "System", "Dashboard")
            
        Returns:
            str: Log message if logged, None if not logged
        """
        should_log, threshold_type, reason = self.should_log_scup(current_scup)
        
        if not should_log:
            return None
        
        current_time = time.time()
        current_zone = self.classify_scup_zone(current_scup)
        
        # Calculate delta from last logged value
        delta_from_last = 0.0
        if self.last_logged_scup is not None:
            delta_from_last = current_scup - self.last_logged_scup
        
        # Generate appropriate message based on threshold type
        if threshold_type == 'exceptional':
            message = f"🧠 Exceptional SCUP detected: {current_scup:.1f} - peak consciousness unity achieved"
        elif threshold_type == 'critical':
            message = f"🚨 Critical SCUP: {current_scup:.1f} - maximum consciousness coherence"
        elif threshold_type == 'zone_change':
            message = f"📊 SCUP zone change: {current_scup:.1f} ({current_zone})"
        elif threshold_type == 'delta':
            if delta_from_last > 0:
                message = f"📈 SCUP surge: +{delta_from_last:.1f} to {current_scup:.1f}"
            else:
                message = f"📉 SCUP decline: {delta_from_last:.1f} to {current_scup:.1f}"
        elif threshold_type == 'recovery':
            message = f"🔄 SCUP normalized: {current_scup:.1f} - consciousness coherence stabilized"
        elif threshold_type == 'initial':
            message = f"🎯 Initial SCUP reading: {current_scup:.1f} ({current_zone})"
        else:
            message = f"📋 SCUP update: {current_scup:.1f} ({reason})"
        
        # Create log entry
        log_entry = SCUPLogEntry(
            scup_value=current_scup,
            timestamp=current_time,
            message=message,
            threshold_type=threshold_type,
            delta_from_last=delta_from_last
        )
        
        # Add to history
        self.log_history.append(log_entry)
        if len(self.log_history) > self.max_history_size:
            self.log_history.pop(0)
        
        # Update state tracking
        self.last_logged_scup = current_scup
        self.last_log_time = current_time
        self.last_zone = current_zone
        
        # Update exceptional flag
        if threshold_type == 'exceptional':
            self.exceptional_logged = True
        elif threshold_type == 'recovery':
            self.exceptional_logged = False
        
        # Send to commentary callbacks
        for callback in self.commentary_callbacks:
            try:
                callback(context, message)
            except Exception as e:
                logger.warning(f"[SCUPOptimizer] Commentary callback error: {e}")
        
        # Log to system logger
        logger.info(f"[SCUPOptimizer] {context}: {message}")
        
        return message
    
    def get_scup_summary(self) -> Dict[str, Any]:
        """Get comprehensive SCUP monitoring summary"""
        if not self.log_history:
            return {
                'status': 'no_data',
                'last_scup': None,
                'current_zone': None,
                'exceptional_active': False,
                'log_count': 0
            }
        
        latest_entry = self.log_history[-1]
        recent_entries = self.log_history[-10:]  # Last 10 entries
        
        # Calculate statistics
        recent_scups = [entry.scup_value for entry in recent_entries]
        avg_scup = sum(recent_scups) / len(recent_scups)
        max_scup = max(recent_scups)
        min_scup = min(recent_scups)
        
        # Trend analysis
        if len(recent_scups) >= 3:
            trend = "stable"
            recent_trend = recent_scups[-3:]
            if all(recent_trend[i] < recent_trend[i+1] for i in range(len(recent_trend)-1)):
                trend = "increasing"
            elif all(recent_trend[i] > recent_trend[i+1] for i in range(len(recent_trend)-1)):
                trend = "decreasing"
        else:
            trend = "unknown"
        
        return {
            'status': 'active',
            'last_scup': latest_entry.scup_value,
            'current_zone': self.last_zone,
            'exceptional_active': self.exceptional_logged,
            'log_count': len(self.log_history),
            'recent_average': avg_scup,
            'recent_max': max_scup,
            'recent_min': min_scup,
            'trend': trend,
            'last_log_ago': time.time() - latest_entry.timestamp,
            'threshold_types': [entry.threshold_type for entry in recent_entries],
            'delta_threshold': self.delta_threshold,
            'exceptional_threshold': self.exceptional_threshold
        }
    
    def reset_exceptional_flag(self):
        """Manually reset the exceptional flag (for testing/debugging)"""
        old_state = self.exceptional_logged
        self.exceptional_logged = False
        logger.info(f"[SCUPOptimizer] Exceptional flag reset: {old_state} → {self.exceptional_logged}")
    
    def set_thresholds(self, delta: Optional[float] = None, exceptional: Optional[float] = None):
        """Update threshold values"""
        if delta is not None:
            self.delta_threshold = delta
            logger.info(f"[SCUPOptimizer] Delta threshold updated to ±{delta}")
        
        if exceptional is not None:
            self.exceptional_threshold = exceptional
            logger.info(f"[SCUPOptimizer] Exceptional threshold updated to {exceptional}+")
    
    def get_recent_logs(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get recent log entries in a readable format"""
        recent = self.log_history[-count:] if count > 0 else self.log_history
        
        return [
            {
                'timestamp': datetime.fromtimestamp(entry.timestamp).strftime('%H:%M:%S'),
                'scup': entry.scup_value,
                'message': entry.message,
                'type': entry.threshold_type,
                'delta': entry.delta_from_last
            }
            for entry in recent
        ]

# Global SCUP optimizer instance
scup_optimizer = SCUPLoggerOptimizer()

# Convenience functions for easy integration
def monitor_scup(scup_value: float, context: str = "System") -> Optional[str]:
    """Simple function to monitor SCUP with smart logging"""
    return scup_optimizer.log_scup(scup_value, context)

def register_scup_commentary(callback: Callable[[str, str], None]):
    """Register a callback for SCUP commentary"""
    scup_optimizer.register_commentary_callback(callback)

def get_scup_status() -> Dict[str, Any]:
    """Get current SCUP monitoring status"""
    return scup_optimizer.get_scup_summary()

def reset_scup_exceptional():
    """Reset the exceptional SCUP flag"""
    scup_optimizer.reset_exceptional_flag()

# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing SCUP Logger Optimizer...")
    
    def test_commentary(source: str, message: str):
        print(f"[{source}] {message}")
    
    # Register test callback
    register_scup_commentary(test_commentary)
    
    # Test sequence
    test_scups = [
        (5.0, "Initial reading"),
        (15.0, "Normal increase"),  # Should log - delta > 5
        (16.0, "Small change"),    # Should not log - delta < 5
        (45.0, "Exceptional!"),    # Should log - exceeds 40
        (46.0, "Still exceptional"), # Should not log - already flagged
        (50.0, "Delta increase"),  # Should log - delta > 5
        (35.0, "Recovery"),        # Should log - below 40 again
        (85.0, "Critical!"),       # Should log - critical level
    ]
    
    for scup, description in test_scups:
        print(f"\n--- Testing {description}: SCUP = {scup} ---")
        result = monitor_scup(scup, "Test")
        if result:
            print(f"✅ Logged: {result}")
        else:
            print("❌ Not logged (threshold not met)")
        
        # Small delay to test timing
        time.sleep(0.1)
    
    # Show summary
    print(f"\n📊 Final Status:")
    status = get_scup_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print(f"\n📜 Recent Logs:")
    for log in scup_optimizer.get_recent_logs(5):
        print(f"   {log['timestamp']}: {log['message']} (Δ{log['delta']:+.1f})") 