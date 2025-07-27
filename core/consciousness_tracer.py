#!/usr/bin/env python3
"""
ConsciousnessTracer - Comprehensive tracing system for DAWN consciousness states
Tracks, logs, and analyzes consciousness state transitions and patterns
"""

import json
import time
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set, Callable
from dataclasses import dataclass, field, asdict
from collections import deque, defaultdict
from enum import Enum
import threading
import traceback
import hashlib
import numpy as np
from bloom.bloom_core.rebloom_router import route_rebloom, seal_bloom, is_rebloom_unstable
from core.event_bus import event_bus

# Trace event types
class TraceEventType(Enum):
    STATE_CHANGE = "state_change"
    DIMENSION_UPDATE = "dimension_update"
    PATTERN_DETECTED = "pattern_detected"
    ANOMALY_DETECTED = "anomaly_detected"
    CHECKPOINT = "checkpoint"
    ERROR = "error"
    METRIC = "metric"
    TRANSITION = "transition"
    RESONANCE = "resonance"
    COHERENCE_SHIFT = "coherence_shift"
    EMERGENCE = "emergence"

# Trace levels
class TraceLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

@dataclass
class TraceEvent:
    """Represents a single trace event"""
    timestamp: float
    event_type: TraceEventType
    level: TraceLevel
    component: str
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)
    correlation_id: Optional[str] = None
    duration_ms: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type.value,
            "level": self.level.value,
            "component": self.component,
            "message": self.message,
            "data": self.data,
            "tags": list(self.tags),
            "correlation_id": self.correlation_id,
            "duration_ms": self.duration_ms
        }

@dataclass
class StateSnapshot:
    """Snapshot of consciousness state at a point in time"""
    timestamp: float
    state_name: str
    dimensions: Dict[str, float]
    active_patterns: List[str]
    resonance_level: float
    coherence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def calculate_hash(self) -> str:
        """Calculate hash of state for comparison"""
        state_str = f"{self.state_name}:{sorted(self.dimensions.items())}"
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]

@dataclass
class TransitionTrace:
    """Detailed trace of a state transition"""
    from_state: str
    to_state: str
    start_time: float
    end_time: float
    trigger: str
    success: bool
    intermediate_states: List[str] = field(default_factory=list)
    metrics: Dict[str, float] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

class ConsciousnessTracer:
    """Comprehensive consciousness state tracing system"""
    
    def __init__(self, 
                 buffer_size: int = 10000,
                 persist_interval: int = 60,
                 trace_dir: Optional[Path] = None,
                 level: TraceLevel = TraceLevel.INFO,
                 timeline_events_enabled: bool = False):
        """
        Initialize the consciousness tracer
        
        Args:
            buffer_size: Maximum number of events to keep in memory
            persist_interval: Seconds between automatic persistence
            trace_dir: Directory for trace files
            level: Minimum trace level to record
            timeline_events_enabled: Whether to enable timeline event emission
        """
        self.buffer_size = buffer_size
        self.persist_interval = persist_interval
        self.trace_dir = trace_dir or Path("logs/consciousness_traces")
        self.level = level
        self.timeline_events_enabled = timeline_events_enabled
        
        # Event buffer
        self.events = deque(maxlen=buffer_size)
        self.event_lock = threading.Lock()
        
        # State tracking
        self.current_state: Optional[StateSnapshot] = None
        self.state_history = deque(maxlen=1000)
        self.transitions: List[TransitionTrace] = []
        self.active_transition: Optional[TransitionTrace] = None
        
        # Metrics and analytics
        self.metrics = defaultdict(lambda: defaultdict(float))
        self.event_counts = defaultdict(int)
        self.pattern_frequencies = defaultdict(int)
        
        # Correlation tracking
        self.correlation_map: Dict[str, List[TraceEvent]] = {}
        
        # Callbacks
        self.event_callbacks: List[Callable[[TraceEvent], None]] = []
        self.anomaly_callbacks: List[Callable[[TraceEvent], None]] = []
        
        # Analysis caches
        self._pattern_cache = {}
        self._anomaly_thresholds = {}
        
        # Persistence
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        self._persist_thread = None
        self._stop_persist = threading.Event()
        
        # Session tracking
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_start = time.time()
        
        # Start persistence thread
        self._start_persistence_thread()
    
    def trace(self,
              event_type: TraceEventType,
              component: str,
              message: str,
              data: Optional[Dict[str, Any]] = None,
              level: TraceLevel = TraceLevel.INFO,
              tags: Optional[Set[str]] = None,
              correlation_id: Optional[str] = None) -> TraceEvent:
        """
        Record a trace event
        
        Args:
            event_type: Type of event
            component: Component generating the event
            message: Human-readable message
            data: Additional event data
            level: Trace level
            tags: Event tags for filtering
            correlation_id: ID for correlating related events
            
        Returns:
            The created trace event
        """
        if level.value < self.level.value:
            return None
            
        event = TraceEvent(
            timestamp=time.time(),
            event_type=event_type,
            level=level,
            component=component,
            message=message,
            data=data or {},
            tags=tags or set(),
            correlation_id=correlation_id
        )
        
        with self.event_lock:
            self.events.append(event)
            self.event_counts[event_type] += 1
            
            # Track correlation
            if correlation_id:
                if correlation_id not in self.correlation_map:
                    self.correlation_map[correlation_id] = []
                self.correlation_map[correlation_id].append(event)
        
        # Trigger callbacks
        for callback in self.event_callbacks:
            try:
                callback(event)
            except Exception as e:
                self._log_error(f"Event callback error: {e}")
        
        # Check for anomalies
        if event_type == TraceEventType.ANOMALY_DETECTED:
            for callback in self.anomaly_callbacks:
                try:
                    callback(event)
                except Exception as e:
                    self._log_error(f"Anomaly callback error: {e}")
        
        return event
    
    def trace_state_change(self,
                          from_state: str,
                          to_state: str,
                          dimensions: Dict[str, float],
                          trigger: str = "unknown",
                          metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Trace a consciousness state change
        
        Returns:
            Correlation ID for the state change
        """
        correlation_id = f"state_change_{int(time.time() * 1000)}"
        
        # End active transition if exists
        if self.active_transition:
            self.active_transition.success = False
            self.active_transition.errors.append("Interrupted by new transition")
            self.transitions.append(self.active_transition)
        
        # Start new transition
        self.active_transition = TransitionTrace(
            from_state=from_state,
            to_state=to_state,
            start_time=time.time(),
            end_time=0,
            trigger=trigger,
            success=False
        )
        
        # Record events
        self.trace(
            TraceEventType.STATE_CHANGE,
            "consciousness",
            f"State change: {from_state} -> {to_state}",
            data={
                "from_state": from_state,
                "to_state": to_state,
                "dimensions": dimensions,
                "trigger": trigger,
                "metadata": metadata or {}
            },
            level=TraceLevel.INFO,
            tags={"state_change", from_state, to_state},
            correlation_id=correlation_id
        )
        
        # Create state snapshot
        self.current_state = StateSnapshot(
            timestamp=time.time(),
            state_name=to_state,
            dimensions=dimensions,
            active_patterns=[],
            resonance_level=dimensions.get("resonance", 0.0),
            coherence=dimensions.get("coherence", 0.0),
            metadata=metadata or {}
        )
        
        self.state_history.append(self.current_state)
        
        # Timeline event emission
        if self.timeline_events_enabled:
            event = {
                'id': correlation_id,
                'type': 'mode_shift',
                'timestamp': int(time.time() * 1000),
                'label': to_state.upper(),
                'duration': 100,
                'data': {
                    'from': from_state,
                    'to': to_state,
                    'trigger': trigger,
                    'coherence': dimensions.get('coherence', 0.0)
                }
            }
            event_bus.emit('timeline_event', event)
        
        return correlation_id
    
    def trace_dimension_update(self,
                             dimension: str,
                             old_value: float,
                             new_value: float,
                             component: str = "unknown") -> None:
        """Trace a dimension value update"""
        delta = new_value - old_value
        percent_change = (delta / old_value * 100) if old_value != 0 else 0
        
        self.trace(
            TraceEventType.DIMENSION_UPDATE,
            component,
            f"Dimension '{dimension}' updated: {old_value:.3f} -> {new_value:.3f}",
            data={
                "dimension": dimension,
                "old_value": old_value,
                "new_value": new_value,
                "delta": delta,
                "percent_change": percent_change
            },
            level=TraceLevel.DEBUG,
            tags={"dimension", dimension}
        )
        
        # Update metrics
        self.metrics["dimensions"][dimension] = new_value
        
        # Timeline event emission for flux
        if self.timeline_events_enabled and dimension == 'neural_load':
            event = {
                'id': f'flux_{int(time.time() * 1000)}',
                'type': 'flux',
                'timestamp': int(time.time() * 1000),
                'label': f'{int(new_value)}%',
                'duration': 100,
                'data': {
                    'channel': dimension,
                    'intensity': int(new_value),
                    'coherence': self.current_state.coherence if self.current_state else 0.0
                }
            }
            event_bus.emit('timeline_event', event)
        
        # Check for anomalies
        if dimension in self._anomaly_thresholds:
            threshold = self._anomaly_thresholds[dimension]
            if abs(percent_change) > threshold:
                self.trace(
                    TraceEventType.ANOMALY_DETECTED,
                    component,
                    f"Anomaly in dimension '{dimension}': {percent_change:.1f}% change exceeds threshold",
                    data={
                        "dimension": dimension,
                        "threshold": threshold,
                        "actual_change": percent_change
                    },
                    level=TraceLevel.WARNING,
                    tags={"anomaly", dimension}
                )
        
        # Fault event emission on anomaly
        if self.timeline_events_enabled and dimension in self._anomaly_thresholds:
            threshold = self._anomaly_thresholds[dimension]
            if abs(percent_change) > threshold:
                event = {
                    'id': f'fault_{int(time.time() * 1000)}',
                    'type': 'fault',
                    'timestamp': int(time.time() * 1000),
                    'label': 'OVERFLOW' if percent_change > 0 else 'FRAGMENT',
                    'duration': 100,
                    'data': {
                        'severity': 'high',
                        'recovery': 1000,
                        'coherence': self.current_state.coherence if self.current_state else 0.0
                    }
                }
                event_bus.emit('timeline_event', event)
    
    def trace_pattern(self,
                     pattern_name: str,
                     confidence: float,
                     data: Optional[Dict[str, Any]] = None) -> None:
        """Trace detection of a consciousness pattern"""
        self.pattern_frequencies[pattern_name] += 1
        
        self.trace(
            TraceEventType.PATTERN_DETECTED,
            "pattern_detector",
            f"Pattern detected: {pattern_name} (confidence: {confidence:.2f})",
            data={
                "pattern": pattern_name,
                "confidence": confidence,
                "frequency": self.pattern_frequencies[pattern_name],
                **(data or {})
            },
            level=TraceLevel.INFO,
            tags={"pattern", pattern_name}
        )
        
        if self.current_state:
            self.current_state.active_patterns.append(pattern_name)
        
        # Timeline event emission for pulse
        if self.timeline_events_enabled:
            event = {
                'id': f'pulse_{int(time.time() * 1000)}',
                'type': 'pulse',
                'timestamp': int(time.time() * 1000),
                'label': pattern_name,
                'duration': 100,
                'data': {
                    'pattern': pattern_name,
                    'frequency': data.get('frequency', 0.0) if data else 0.0,
                    'intensity': data.get('intensity', 0.0) if data else 0.0,
                    'coherence': self.current_state.coherence if self.current_state else 0.0
                }
            }
            event_bus.emit('timeline_event', event)
    
    def complete_transition(self, success: bool = True, error: Optional[str] = None) -> None:
        """Complete the active state transition"""
        if not self.active_transition:
            return
            
        self.active_transition.end_time = time.time()
        self.active_transition.success = success
        if error:
            self.active_transition.errors.append(error)
            
        duration = (self.active_transition.end_time - self.active_transition.start_time) * 1000
        
        self.trace(
            TraceEventType.TRANSITION,
            "consciousness",
            f"Transition completed: {self.active_transition.from_state} -> {self.active_transition.to_state}",
            data={
                "duration_ms": duration,
                "success": success,
                "errors": self.active_transition.errors
            },
            level=TraceLevel.INFO if success else TraceLevel.WARNING,
            duration_ms=duration
        )
        
        self.transitions.append(self.active_transition)
        self.active_transition = None
    
    def add_metric(self, category: str, name: str, value: float) -> None:
        """Add a metric value"""
        self.metrics[category][name] = value
        
        self.trace(
            TraceEventType.METRIC,
            "metrics",
            f"Metric {category}.{name}: {value}",
            data={
                "category": category,
                "name": name,
                "value": value
            },
            level=TraceLevel.DEBUG
        )
    
    def set_anomaly_threshold(self, dimension: str, threshold: float) -> None:
        """Set anomaly detection threshold for a dimension"""
        self._anomaly_thresholds[dimension] = threshold
    
    def add_event_callback(self, callback: Callable[[TraceEvent], None]) -> None:
        """Add a callback for all events"""
        self.event_callbacks.append(callback)
    
    def add_anomaly_callback(self, callback: Callable[[TraceEvent], None]) -> None:
        """Add a callback for anomaly events"""
        self.anomaly_callbacks.append(callback)
    
    def get_recent_events(self,
                         count: int = 100,
                         event_type: Optional[TraceEventType] = None,
                         component: Optional[str] = None,
                         min_level: Optional[TraceLevel] = None) -> List[TraceEvent]:
        """Get recent events with optional filtering"""
        with self.event_lock:
            events = list(self.events)
        
        # Apply filters
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if component:
            events = [e for e in events if e.component == component]
        if min_level:
            events = [e for e in events if e.level.value >= min_level.value]
            
        return events[-count:]
    
    def get_correlated_events(self, correlation_id: str) -> List[TraceEvent]:
        """Get all events with a correlation ID"""
        return self.correlation_map.get(correlation_id, [])
    
    def analyze_patterns(self, window_minutes: int = 60) -> Dict[str, Any]:
        """Analyze patterns in recent events"""
        cutoff_time = time.time() - (window_minutes * 60)
        recent_events = [e for e in self.events if e.timestamp > cutoff_time]
        
        analysis = {
            "window_minutes": window_minutes,
            "total_events": len(recent_events),
            "events_by_type": defaultdict(int),
            "events_by_component": defaultdict(int),
            "error_rate": 0,
            "patterns": {},
            "anomalies": []
        }
        
        error_count = 0
        for event in recent_events:
            analysis["events_by_type"][event.event_type.value] += 1
            analysis["events_by_component"][event.component] += 1
            if event.level.value >= TraceLevel.ERROR.value:
                error_count += 1
                
        analysis["error_rate"] = error_count / len(recent_events) if recent_events else 0
        
        # Pattern analysis
        pattern_events = [e for e in recent_events if e.event_type == TraceEventType.PATTERN_DETECTED]
        for event in pattern_events:
            pattern_name = event.data.get("pattern", "unknown")
            if pattern_name not in analysis["patterns"]:
                analysis["patterns"][pattern_name] = {
                    "count": 0,
                    "avg_confidence": 0,
                    "occurrences": []
                }
            analysis["patterns"][pattern_name]["count"] += 1
            analysis["patterns"][pattern_name]["occurrences"].append(event.timestamp)
            
        # Calculate pattern metrics
        for pattern_data in analysis["patterns"].values():
            if len(pattern_data["occurrences"]) > 1:
                intervals = np.diff(pattern_data["occurrences"])
                pattern_data["avg_interval"] = np.mean(intervals)
                pattern_data["interval_std"] = np.std(intervals)
        
        # Anomaly summary
        anomaly_events = [e for e in recent_events if e.event_type == TraceEventType.ANOMALY_DETECTED]
        analysis["anomalies"] = [
            {
                "timestamp": e.timestamp,
                "component": e.component,
                "message": e.message,
                "data": e.data
            }
            for e in anomaly_events
        ]
        
        return analysis
    
    def get_state_history(self, count: int = 100) -> List[StateSnapshot]:
        """Get recent state history"""
        return list(self.state_history)[-count:]
    
    def get_transition_stats(self) -> Dict[str, Any]:
        """Get statistics about state transitions"""
        if not self.transitions:
            return {"total_transitions": 0}
            
        stats = {
            "total_transitions": len(self.transitions),
            "success_rate": sum(1 for t in self.transitions if t.success) / len(self.transitions),
            "avg_duration_ms": np.mean([(t.end_time - t.start_time) * 1000 for t in self.transitions]),
            "transitions_by_trigger": defaultdict(int),
            "transition_pairs": defaultdict(int)
        }
        
        for transition in self.transitions:
            stats["transitions_by_trigger"][transition.trigger] += 1
            pair = f"{transition.from_state}->{transition.to_state}"
            stats["transition_pairs"][pair] += 1
            
        return stats
    
    def export_session(self, format: str = "json") -> Path:
        """Export the current session data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"consciousness_trace_{self.session_id}_{timestamp}.{format}"
        export_path = self.trace_dir / filename
        
        if format == "json":
            data = {
                "session_id": self.session_id,
                "session_start": self.session_start,
                "export_time": time.time(),
                "events": [e.to_dict() for e in self.events],
                "state_history": [asdict(s) for s in self.state_history],
                "transitions": [asdict(t) for t in self.transitions],
                "metrics": dict(self.metrics),
                "event_counts": dict(self.event_counts),
                "pattern_frequencies": dict(self.pattern_frequencies),
                "analysis": self.analyze_patterns()
            }
            
            with open(export_path, 'w') as f:
                json.dump(data, f, indent=2)
                
        return export_path
    
    def _start_persistence_thread(self) -> None:
        """Start the background persistence thread"""
        def persist_loop():
            while not self._stop_persist.is_set():
                try:
                    self._persist_events()
                    self._stop_persist.wait(self.persist_interval)
                except Exception as e:
                    self._log_error(f"Persistence error: {e}")
                    
        self._persist_thread = threading.Thread(target=persist_loop, daemon=True)
        self._persist_thread.start()
    
    def _persist_events(self) -> None:
        """Persist events to disk"""
        if not self.events:
            return
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        persist_file = self.trace_dir / f"trace_{self.session_id}_{timestamp}.jsonl"
        
        with self.event_lock:
            events_to_persist = list(self.events)
            self.events.clear()
            
        with open(persist_file, 'a') as f:
            for event in events_to_persist:
                f.write(json.dumps(event.to_dict()) + '\n')
    
    def _log_error(self, message: str) -> None:
        """Internal error logging"""
        self.trace(
            TraceEventType.ERROR,
            "tracer",
            message,
            data={"traceback": traceback.format_exc()},
            level=TraceLevel.ERROR
        )
    
    def shutdown(self) -> None:
        """Shutdown the tracer and persist remaining data"""
        self._stop_persist.set()
        if self._persist_thread:
            self._persist_thread.join(timeout=5)
            
        # Final persistence
        self._persist_events()
        
        # Export session summary
        self.export_session()
    
    def __enter__(self):
        """Context manager entry"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.shutdown()
        
    async def async_trace(self, *args, **kwargs) -> TraceEvent:
        """Async version of trace"""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.trace, *args, **kwargs
        )