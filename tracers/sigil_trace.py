#!/usr/bin/env python3
"""
DAWN Sigil Trace System
Logs symbolic trigger events for consciousness monitoring
Tracks sigil registrations, executions, and symbolic state changes
"""

import os
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


class SigilTracer:
    """Thread-safe sigil event tracer for DAWN's symbolic consciousness"""
    
    def __init__(self, log_path: Optional[str] = None):
        self.log_path = Path(log_path) if log_path else Path("runtime/logs/sigil_trace.log")
        self._lock = threading.Lock()
        
        # Ensure directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize log file if it doesn't exist
        if not self.log_path.exists():
            with open(self.log_path, 'w', encoding='utf-8') as f:
                f.write(f"# DAWN Sigil Trace Log - Started {datetime.now().isoformat()}\n")
                f.write("# Format: [EVENT_TYPE] [Tick NUMBER] SIGIL_NAME | metadata\n")
    
    def log_sigil_event(self, event_type: str, tick: int, sigil_name: str, 
                       metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log a sigil event to the trace
        
        Args:
            event_type: Type of event (REGISTERED, EXECUTED, ACTIVATED, DEACTIVATED, etc.)
            tick: Current tick number
            sigil_name: Name/identifier of the sigil
            metadata: Optional metadata dictionary
        """
        timestamp = datetime.now().isoformat(timespec='milliseconds')
        
        # Format sigil trace entry
        trace_line = f"[{event_type}] [Tick {tick}] {sigil_name}"
        
        # Add metadata if provided
        if metadata:
            metadata_str = " | ".join([f"{k}={v}" for k, v in metadata.items()])
            trace_line += f" | {metadata_str}"
        
        trace_line += "\n"
        
        # Thread-safe write
        with self._lock:
            try:
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write(trace_line)
                    f.flush()  # Ensure immediate write for monitoring
            except Exception as e:
                # Fallback to console if file write fails
                print(f"⚠️ Sigil trace write failed: {e}")
                print(f"Sigil Event: {trace_line.strip()}")
    
    def log_registration(self, tick: int, sigil_name: str, threshold: float = None, 
                        category: str = None) -> None:
        """Log a sigil registration event"""
        metadata = {}
        if threshold is not None:
            metadata["threshold"] = threshold
        if category:
            metadata["category"] = category
        
        self.log_sigil_event("REGISTERED", tick, sigil_name, metadata)
    
    def log_execution(self, tick: int, sigil_name: str, strength: float = None, 
                     duration_ms: int = None) -> None:
        """Log a sigil execution event"""
        metadata = {}
        if strength is not None:
            metadata["strength"] = strength
        if duration_ms is not None:
            metadata["duration_ms"] = duration_ms
        
        self.log_sigil_event("EXECUTED", tick, sigil_name, metadata)
    
    def log_activation(self, tick: int, sigil_name: str, trigger_source: str = None,
                      activation_strength: float = None) -> None:
        """Log a sigil activation event"""
        metadata = {}
        if trigger_source:
            metadata["trigger_source"] = trigger_source
        if activation_strength is not None:
            metadata["activation_strength"] = activation_strength
        
        self.log_sigil_event("ACTIVATED", tick, sigil_name, metadata)
    
    def log_deactivation(self, tick: int, sigil_name: str, reason: str = None) -> None:
        """Log a sigil deactivation event"""
        metadata = {}
        if reason:
            metadata["reason"] = reason
        
        self.log_sigil_event("DEACTIVATED", tick, sigil_name, metadata)
    
    def log_chain_trigger(self, tick: int, chain_sigils: List[str], 
                         chain_type: str = "cascade") -> None:
        """Log a sigil chain reaction"""
        chain_str = " -> ".join(chain_sigils)
        metadata = {"chain_type": chain_type, "chain_length": len(chain_sigils)}
        
        self.log_sigil_event("CHAIN", tick, chain_str, metadata)
    
    def log_symbolic_state(self, tick: int, active_sigils: List[str], 
                          total_energy: float = None) -> None:
        """Log the current symbolic state snapshot"""
        state_summary = f"Active[{len(active_sigils)}]: {', '.join(active_sigils[:3])}"
        if len(active_sigils) > 3:
            state_summary += f" +{len(active_sigils) - 3} more"
        
        metadata = {"active_count": len(active_sigils)}
        if total_energy is not None:
            metadata["total_energy"] = total_energy
        
        self.log_sigil_event("STATE", tick, state_summary, metadata)
    
    def get_recent_activity(self, lines: int = 10) -> List[str]:
        """Get recent sigil activity from the log"""
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                
            # Filter out comment lines and return last N entries
            trace_lines = [line.strip() for line in all_lines if not line.startswith('#')]
            return trace_lines[-lines:] if trace_lines else []
            
        except Exception as e:
            print(f"⚠️ Failed to read sigil trace: {e}")
            return []
    
    def get_sigil_statistics(self) -> Dict[str, Any]:
        """Get statistics about sigil activity"""
        try:
            recent_activity = self.get_recent_activity(100)  # Last 100 events
            
            stats = {
                "total_events": len(recent_activity),
                "event_types": {},
                "active_sigils": set(),
                "most_frequent_sigils": {}
            }
            
            sigil_counts = {}
            
            for line in recent_activity:
                if '[' in line and ']' in line:
                    # Parse event type
                    event_type = line.split(']')[0].replace('[', '')
                    stats["event_types"][event_type] = stats["event_types"].get(event_type, 0) + 1
                    
                    # Parse sigil name (between second ] and first |)
                    parts = line.split(']')
                    if len(parts) >= 3:
                        sigil_part = parts[2].split('|')[0].strip()
                        sigil_counts[sigil_part] = sigil_counts.get(sigil_part, 0) + 1
                        
                        if event_type == "ACTIVATED":
                            stats["active_sigils"].add(sigil_part)
                        elif event_type == "DEACTIVATED":
                            stats["active_sigils"].discard(sigil_part)
            
            # Convert active sigils set to list
            stats["active_sigils"] = list(stats["active_sigils"])
            
            # Get most frequent sigils
            sorted_sigils = sorted(sigil_counts.items(), key=lambda x: x[1], reverse=True)
            stats["most_frequent_sigils"] = dict(sorted_sigils[:5])
            
            return stats
            
        except Exception as e:
            print(f"⚠️ Failed to generate sigil statistics: {e}")
            return {"error": str(e)}


# Global sigil tracer instance
_global_tracer = None
_tracer_lock = threading.Lock()


def get_sigil_tracer() -> SigilTracer:
    """Get the global sigil tracer instance (thread-safe singleton)"""
    global _global_tracer
    
    if _global_tracer is None:
        with _tracer_lock:
            if _global_tracer is None:
                _global_tracer = SigilTracer()
    
    return _global_tracer


# Convenience functions for easy integration
def log_sigil_event(event_type: str, tick: int, sigil_name: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a sigil event using the global tracer"""
    tracer = get_sigil_tracer()
    tracer.log_sigil_event(event_type, tick, sigil_name, metadata)


def log_sigil_registration(tick: int, sigil_name: str, threshold: float = None) -> None:
    """Log a sigil registration using the global tracer"""
    tracer = get_sigil_tracer()
    tracer.log_registration(tick, sigil_name, threshold)


def log_sigil_execution(tick: int, sigil_name: str, strength: float = None) -> None:
    """Log a sigil execution using the global tracer"""
    tracer = get_sigil_tracer()
    tracer.log_execution(tick, sigil_name, strength)


def log_sigil_activation(tick: int, sigil_name: str, trigger_source: str = None) -> None:
    """Log a sigil activation using the global tracer"""
    tracer = get_sigil_tracer()
    tracer.log_activation(tick, sigil_name, trigger_source)


def log_sigil_state(tick: int, active_sigils: List[str]) -> None:
    """Log the current sigil state using the global tracer"""
    tracer = get_sigil_tracer()
    tracer.log_symbolic_state(tick, active_sigils)


if __name__ == "__main__":
    # Test the sigil tracing system
    print("🌀 Testing DAWN Sigil Trace System")
    print("=" * 50)
    
    # Create test tracer
    test_tracer = SigilTracer("test_sigil_trace.log")
    
    # Test various sigil events
    test_tracer.log_registration(1001, "REBLOOM_MEMORY", threshold=0.7)
    test_tracer.log_registration(1002, "STABILIZE_PROTOCOL", threshold=0.8)
    test_tracer.log_activation(1003, "REBLOOM_MEMORY", trigger_source="entropy_spike")
    test_tracer.log_execution(1004, "REBLOOM_MEMORY", strength=0.9, duration_ms=150)
    test_tracer.log_chain_trigger(1005, ["REBLOOM_MEMORY", "STABILIZE_PROTOCOL", "WISDOM_SIGIL"])
    test_tracer.log_symbolic_state(1006, ["REBLOOM_MEMORY", "WISDOM_SIGIL"], total_energy=1.7)
    test_tracer.log_deactivation(1007, "REBLOOM_MEMORY", reason="threshold_decay")
    
    print("✅ Test sigil events logged to test_sigil_trace.log")
    
    # Test statistics
    stats = test_tracer.get_sigil_statistics()
    print("\n📊 Sigil Activity Statistics:")
    print(f"   Total events: {stats['total_events']}")
    print(f"   Event types: {stats['event_types']}")
    print(f"   Active sigils: {stats['active_sigils']}")
    print(f"   Most frequent: {stats['most_frequent_sigils']}")
    
    print("\n📄 Check test_sigil_trace.log to see the symbolic trace format") 