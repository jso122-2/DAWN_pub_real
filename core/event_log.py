#!/usr/bin/env python3
"""
DAWN Event Log System
Unified event streaming for GUI panels and system monitoring
Logs reflections, reblooms, state changes, and system activity
"""

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import threading


class EventLogger:
    """Thread-safe event logger for DAWN's unified event stream"""
    
    def __init__(self, log_path: Optional[str] = None):
        self.log_path = Path(log_path) if log_path else Path("runtime/logs/event_stream.log")
        self._lock = threading.Lock()
        
        # Ensure directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize log file if it doesn't exist
        if not self.log_path.exists():
            with open(self.log_path, 'w', encoding='utf-8') as f:
                f.write(f"# DAWN Event Stream Log - Started {datetime.now().isoformat()}\n")
    
    def log_event(self, kind: str, tick: int, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an event to the unified stream
        
        Args:
            kind: Event type (REFLECTION, STATE, REBLOOM, SIGIL, etc.)
            tick: Current tick number
            message: Event message/description
            metadata: Optional metadata dictionary
        """
        timestamp = datetime.now().isoformat(timespec='milliseconds')
        
        # Format event entry
        event_line = f"[{timestamp}] [{kind}] [Tick {tick}] {message}"
        
        # Add metadata if provided
        if metadata:
            metadata_str = " | ".join([f"{k}={v}" for k, v in metadata.items()])
            event_line += f" | {metadata_str}"
        
        event_line += "\n"
        
        # Thread-safe write
        with self._lock:
            try:
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write(event_line)
                    f.flush()  # Ensure immediate write for GUI polling
            except Exception as e:
                # Fallback to console if file write fails
                print(f"⚠️ Event log write failed: {e}")
                print(f"Event: {event_line.strip()}")
    
    def log_reflection(self, tick: int, reflection: str) -> None:
        """Log a reflection event"""
        # Truncate very long reflections for readability
        display_reflection = reflection[:100] + "..." if len(reflection) > 100 else reflection
        self.log_event("REFLECTION", tick, display_reflection)
    
    def log_state_update(self, tick: int, entropy: float, scup: float, 
                        mood: str = None, zone: str = None) -> None:
        """Log a state update event"""
        metadata = {}
        if mood:
            metadata["mood"] = mood
        if zone:
            metadata["zone"] = zone
        
        message = f"Entropy={entropy:.3f}, SCUP={scup:.3f}"
        self.log_event("STATE", tick, message, metadata)
    
    def log_rebloom(self, tick: int, source: str, rebloom_id: str = None, 
                   intensity: float = None) -> None:
        """Log a rebloom event"""
        metadata = {}
        if rebloom_id:
            metadata["rebloom_id"] = rebloom_id
        if intensity is not None:
            metadata["intensity"] = intensity
        
        message = f"Rebloom triggered from {source}"
        self.log_event("REBLOOM", tick, message, metadata)
    
    def log_sigil_activation(self, tick: int, sigil_type: str, activation_strength: float = None) -> None:
        """Log a sigil activation event"""
        metadata = {}
        if activation_strength is not None:
            metadata["strength"] = activation_strength
        
        message = f"Sigil activated: {sigil_type}"
        self.log_event("SIGIL", tick, message, metadata)
    
    def log_system_event(self, tick: int, event_type: str, description: str, 
                        metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log a general system event"""
        self.log_event("SYSTEM", tick, f"{event_type}: {description}", metadata)
    
    def log_memory_event(self, tick: int, operation: str, chunk_id: str = None) -> None:
        """Log a memory operation event"""
        metadata = {}
        if chunk_id:
            metadata["chunk_id"] = chunk_id
        
        message = f"Memory {operation}"
        self.log_event("MEMORY", tick, message, metadata)


# Global event logger instance
_global_logger = None
_logger_lock = threading.Lock()


def get_event_logger() -> EventLogger:
    """Get the global event logger instance (thread-safe singleton)"""
    global _global_logger
    
    if _global_logger is None:
        with _logger_lock:
            if _global_logger is None:
                _global_logger = EventLogger()
    
    return _global_logger


# Convenience functions for backward compatibility and ease of use
def log_event(kind: str, tick: int, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log an event using the global logger"""
    logger = get_event_logger()
    logger.log_event(kind, tick, message, metadata)


def log_reflection_event(tick: int, reflection: str) -> None:
    """Log a reflection event using the global logger"""
    logger = get_event_logger()
    logger.log_reflection(tick, reflection)


def log_state_event(tick: int, entropy: float, scup: float, mood: str = None, zone: str = None) -> None:
    """Log a state update event using the global logger"""
    logger = get_event_logger()
    logger.log_state_update(tick, entropy, scup, mood, zone)


def log_rebloom_event(tick: int, source: str, rebloom_id: str = None, intensity: float = None) -> None:
    """Log a rebloom event using the global logger"""
    logger = get_event_logger()
    logger.log_rebloom(tick, source, rebloom_id, intensity)


def log_system_activity(tick: int, event_type: str, description: str, 
                       metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a system activity event using the global logger"""
    logger = get_event_logger()
    logger.log_system_event(tick, event_type, description, metadata)


if __name__ == "__main__":
    # Test the event logging system
    print("🧪 Testing DAWN Event Log System")
    print("=" * 50)
    
    # Create test logger
    test_logger = EventLogger("test_event_stream.log")
    
    # Test various event types
    test_logger.log_reflection(1001, "I observe my internal state shifting with awareness.")
    test_logger.log_state_update(1001, 0.75, 67.5, mood="CONTEMPLATIVE", zone="DEEP")
    test_logger.log_rebloom(1002, "memory_trigger", rebloom_id="RB_001", intensity=0.8)
    test_logger.log_sigil_activation(1003, "wisdom_sigil", activation_strength=0.9)
    test_logger.log_system_event(1004, "STARTUP", "Cognitive subsystem initialized")
    test_logger.log_memory_event(1005, "consolidation", chunk_id="MC_12345")
    
    print("✅ Test events logged to test_event_stream.log")
    print("📄 Check the file to see the unified event stream format") 