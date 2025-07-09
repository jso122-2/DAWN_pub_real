#!/usr/bin/env python3
"""
DAWN Log Manager - High-Fidelity Cognitive Logging System
========================================================

Provides structured terminal output and durable backlogs for DAWN's cognitive processes.
Maintains real-time terminal logging with file persistence for analysis and replay.

Features:
- Live terminal output with visual symbols
- Memory-buffered rolling logs
- Automatic file persistence every 100 ticks
- Timestamped log files in ./logs/
- Memory-safe operation (max 500 lines in memory)
- Clean, readable terminal formatting
"""

import os
import time
from datetime import datetime
from typing import List, Optional
from collections import deque
import threading


class LogManager:
    """
    Cognitive logging system for DAWN with terminal and file output.
    
    Handles tick logging, sigil tracking, bloom monitoring, and provides
    structured output for both real-time monitoring and historical analysis.
    """
    
    def __init__(self, logs_dir: str = "./logs", max_memory_lines: int = 500, auto_flush_interval: int = 100):
        """
        Initialize the log manager.
        
        Args:
            logs_dir: Directory for log files
            max_memory_lines: Maximum lines to keep in memory buffer
            auto_flush_interval: Number of ticks before auto-flushing to file
        """
        self.logs_dir = logs_dir
        self.max_memory_lines = max_memory_lines
        self.auto_flush_interval = auto_flush_interval
        
        # Memory buffer for logs (thread-safe deque)
        self.log_buffer = deque(maxlen=max_memory_lines)
        
        # Counters
        self.tick_count = 0
        self.total_logs = 0
        
        # Threading lock for buffer operations
        self.buffer_lock = threading.Lock()
        
        # Ensure logs directory exists
        self._ensure_logs_directory()
        
        # Initialize with startup message
        self._log_startup()
    
    def _ensure_logs_directory(self):
        """Ensure the logs directory exists."""
        try:
            os.makedirs(self.logs_dir, exist_ok=True)
        except OSError as e:
            print(f"⚠️  Warning: Could not create logs directory {self.logs_dir}: {e}")
            # Fallback to current directory
            self.logs_dir = "./logs_fallback"
            os.makedirs(self.logs_dir, exist_ok=True)
    
    def _log_startup(self):
        """Log system startup message."""
        startup_msg = f"🌅 DAWN Log Manager initialized | Directory: {self.logs_dir} | Buffer: {self.max_memory_lines} lines"
        self._add_to_buffer("SYSTEM", startup_msg)
        print(startup_msg)
    
    def _add_to_buffer(self, log_type: str, message: str):
        """
        Add a log entry to the memory buffer (thread-safe).
        
        Args:
            log_type: Type of log entry (TICK, SIGIL, BLOOM, SYSTEM)
            message: Formatted log message
        """
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Include milliseconds
        log_entry = f"[{timestamp}] {message}"
        
        with self.buffer_lock:
            self.log_buffer.append(log_entry)
            self.total_logs += 1
    
    def _format_zone_symbol(self, zone: str) -> str:
        """Get emoji symbol for zone type."""
        zone_symbols = {
            'dormant': '💤',
            'contemplative': '🟢', 
            'active': '🟡',
            'intense': '🟠',
            'critical': '🔴',
            'surge': '🔴',
            'calm': '🟢',
            'transcendent': '✨'
        }
        return zone_symbols.get(zone.lower(), '❓')
    
    def _format_scup_indicator(self, scup: float) -> str:
        """Get visual indicator for SCUP level."""
        if scup >= 0.8:
            return "🟢"  # Excellent
        elif scup >= 0.6:
            return "🟡"  # Good
        elif scup >= 0.4:
            return "🟠"  # Moderate
        else:
            return "🔴"  # Critical
    
    def _format_entropy_indicator(self, entropy: float) -> str:
        """Get visual indicator for entropy level."""
        if entropy <= 0.3:
            return "🌀"  # Low entropy
        elif entropy <= 0.6:
            return "🌪️"  # Medium entropy
        else:
            return "⚡"  # High entropy
    
    def log_tick(self, tick_id: int, pulse: str, scup: float, entropy: float, zone: str, owl_comment: str = ""):
        """
        Log a cognitive tick with full state information.
        
        Args:
            tick_id: Unique tick identifier
            pulse: Pulse state description
            scup: SCUP (Semantic Coherence Under Pressure) score 0.0-1.0
            entropy: Entropy level 0.0-1.0
            zone: Current cognitive zone
            owl_comment: Optional owl system comment
        """
        self.tick_count += 1
        
        # Format visual indicators
        zone_symbol = self._format_zone_symbol(zone)
        scup_indicator = self._format_scup_indicator(scup)
        entropy_indicator = self._format_entropy_indicator(entropy)
        
        # Format main tick message
        tick_msg = (f"[Tick {tick_id:04d} | {zone_symbol} {zone.upper()}] "
                   f"🌀 SCUP: {scup_indicator} {scup:.3f} | "
                   f"🌪️ Entropy: {entropy_indicator} {entropy:.3f}")
        
        # Add pulse information if provided
        if pulse and pulse.strip():
            tick_msg += f" | ⚡ Pulse: {pulse}"
        
        # Add owl comment if provided
        if owl_comment and owl_comment.strip():
            tick_msg += f" | 🦉 Owl: {owl_comment}"
        
        # Log to terminal and buffer
        print(tick_msg)
        self._add_to_buffer("TICK", tick_msg)
        
        # Auto-flush if interval reached
        if self.tick_count % self.auto_flush_interval == 0:
            self.flush_logs_to_file()
    
    def log_sigil(self, sigil_id: str, house: str, temp: int, convolution_level: int):
        """
        Log sigil activity with symbolic information.
        
        Args:
            sigil_id: Sigil symbol or identifier
            house: Sigil house/category
            temp: Temperature/intensity level 0-100
            convolution_level: Convolution complexity level
        """
        # Format temperature indicator
        if temp >= 80:
            temp_indicator = "🔥"
        elif temp >= 60:
            temp_indicator = "🌡️"
        elif temp >= 40:
            temp_indicator = "🔸"
        else:
            temp_indicator = "❄️"
        
        # Format convolution indicator
        if convolution_level >= 5:
            conv_indicator = "🌀"
        elif convolution_level >= 3:
            conv_indicator = "⚙️"
        else:
            conv_indicator = "🔹"
        
        sigil_msg = (f"[Sigil] {sigil_id} | House: {house} | "
                    f"{temp_indicator} Temp: {temp} | "
                    f"{conv_indicator} Convolution: {convolution_level}")
        
        print(sigil_msg)
        self._add_to_buffer("SIGIL", sigil_msg)
    
    def log_bloom(self, bloom_id: str, depth: int, entropy: float, rebloom_parent: Optional[str] = None):
        """
        Log bloom formation and evolution.
        
        Args:
            bloom_id: Unique bloom identifier
            depth: Bloom recursion depth
            entropy: Bloom entropy level 0.0-1.0
            rebloom_parent: Parent bloom ID if this is a rebloom
        """
        # Format depth indicator
        if depth >= 5:
            depth_indicator = "🌳"  # Deep tree
        elif depth >= 3:
            depth_indicator = "🌿"  # Medium growth
        else:
            depth_indicator = "🌱"  # Young sprout
        
        # Format entropy indicator for blooms
        entropy_indicator = self._format_entropy_indicator(entropy)
        
        bloom_msg = (f"[Bloom] ID: {bloom_id} | {depth_indicator} Depth: {depth} | "
                    f"{entropy_indicator} Entropy: {entropy:.3f}")
        
        # Add rebloom information if applicable
        if rebloom_parent:
            bloom_msg += f" | ⬅️ Rebloomed from: {rebloom_parent}"
        
        print(bloom_msg)
        self._add_to_buffer("BLOOM", bloom_msg)
    
    def log_schema_event(self, event_type: str, details: str, severity: str = "info"):
        """
        Log schema-related events (health, pressure, transitions).
        
        Args:
            event_type: Type of schema event
            details: Event details
            severity: Severity level (info, warning, critical)
        """
        # Format severity indicator
        severity_indicators = {
            'info': '💡',
            'warning': '⚠️',
            'critical': '🚨',
            'success': '✅'
        }
        severity_indicator = severity_indicators.get(severity.lower(), '📋')
        
        schema_msg = f"[Schema] {severity_indicator} {event_type}: {details}"
        
        print(schema_msg)
        self._add_to_buffer("SCHEMA", schema_msg)
    
    def log_owl_observation(self, observation: str, confidence: float = 1.0):
        """
        Log Owl system observations and insights.
        
        Args:
            observation: Owl observation text
            confidence: Confidence level 0.0-1.0
        """
        # Format confidence indicator
        if confidence >= 0.8:
            conf_indicator = "🎯"  # High confidence
        elif confidence >= 0.6:
            conf_indicator = "🔍"  # Medium confidence
        else:
            conf_indicator = "❓"  # Low confidence
        
        owl_msg = f"[Owl] 🦉 {conf_indicator} {observation} (confidence: {confidence:.2f})"
        
        print(owl_msg)
        self._add_to_buffer("OWL", owl_msg)
    
    def get_recent_log_lines(self, count: int = 50) -> List[str]:
        """
        Get recent log lines from memory buffer.
        
        Args:
            count: Number of recent lines to return
            
        Returns:
            List of recent log lines
        """
        with self.buffer_lock:
            # Convert deque to list and get last 'count' items
            recent_lines = list(self.log_buffer)
            return recent_lines[-count:] if len(recent_lines) > count else recent_lines
    
    def flush_logs_to_file(self):
        """
        Flush current memory buffer to a timestamped log file.
        """
        if not self.log_buffer:
            return
        
        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        filename = f"dawn_ticklog_{timestamp}.log"
        filepath = os.path.join(self.logs_dir, filename)
        
        try:
            with self.buffer_lock:
                # Copy current buffer
                logs_to_write = list(self.log_buffer)
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"# DAWN Cognitive Log - {datetime.now().isoformat()}\n")
                f.write(f"# Total logs in session: {self.total_logs}\n")
                f.write(f"# Tick count: {self.tick_count}\n")
                f.write(f"# Buffer size: {len(logs_to_write)} lines\n")
                f.write("# " + "="*60 + "\n\n")
                
                # Write log entries
                for log_line in logs_to_write:
                    f.write(log_line + "\n")
            
            # Confirmation message
            flush_msg = f"💾 Flushed {len(logs_to_write)} log entries to {filename}"
            print(flush_msg)
            self._add_to_buffer("SYSTEM", flush_msg)
            
        except Exception as e:
            error_msg = f"❌ Error writing log file {filepath}: {e}"
            print(error_msg)
            self._add_to_buffer("SYSTEM", error_msg)
    
    def get_log_stats(self) -> dict:
        """
        Get current logging statistics.
        
        Returns:
            Dictionary with logging statistics
        """
        with self.buffer_lock:
            buffer_size = len(self.log_buffer)
        
        return {
            'total_logs': self.total_logs,
            'tick_count': self.tick_count,
            'buffer_size': buffer_size,
            'max_buffer_size': self.max_memory_lines,
            'logs_directory': self.logs_dir,
            'auto_flush_interval': self.auto_flush_interval
        }
    
    def clear_buffer(self):
        """Clear the memory buffer (useful for testing or memory management)."""
        with self.buffer_lock:
            self.log_buffer.clear()
        
        clear_msg = "🧹 Log buffer cleared"
        print(clear_msg)
        self._add_to_buffer("SYSTEM", clear_msg)
    
    def shutdown(self):
        """
        Graceful shutdown - flush remaining logs and cleanup.
        """
        shutdown_msg = f"🌄 DAWN Log Manager shutting down | Total logs: {self.total_logs} | Ticks: {self.tick_count}"
        print(shutdown_msg)
        self._add_to_buffer("SYSTEM", shutdown_msg)
        
        # Final flush
        self.flush_logs_to_file()


# Global log manager instance
_log_manager = None

def get_log_manager(**kwargs) -> LogManager:
    """
    Get or create the global log manager instance.
    
    Args:
        **kwargs: Arguments passed to LogManager constructor on first call
        
    Returns:
        Global LogManager instance
    """
    global _log_manager
    if _log_manager is None:
        _log_manager = LogManager(**kwargs)
    return _log_manager


# Convenience functions for easy logging
def log_tick(tick_id: int, pulse: str = "", scup: float = 0.5, entropy: float = 0.5, 
             zone: str = "active", owl_comment: str = ""):
    """Convenience function for tick logging."""
    get_log_manager().log_tick(tick_id, pulse, scup, entropy, zone, owl_comment)

def log_sigil(sigil_id: str, house: str = "Unknown", temp: int = 50, convolution_level: int = 1):
    """Convenience function for sigil logging."""
    get_log_manager().log_sigil(sigil_id, house, temp, convolution_level)

def log_bloom(bloom_id: str, depth: int = 1, entropy: float = 0.5, rebloom_parent: Optional[str] = None):
    """Convenience function for bloom logging."""
    get_log_manager().log_bloom(bloom_id, depth, entropy, rebloom_parent)

def log_schema_event(event_type: str, details: str, severity: str = "info"):
    """Convenience function for schema event logging."""
    get_log_manager().log_schema_event(event_type, details, severity)

def log_owl_observation(observation: str, confidence: float = 1.0):
    """Convenience function for owl observation logging."""
    get_log_manager().log_owl_observation(observation, confidence)

def flush_logs():
    """Convenience function to flush logs to file."""
    get_log_manager().flush_logs_to_file()

def get_recent_logs(count: int = 50) -> List[str]:
    """Convenience function to get recent logs."""
    return get_log_manager().get_recent_log_lines(count)


# Demo function for testing
def demo_logging():
    """Demonstration of the logging system."""
    print("🚀 DAWN Log Manager Demo")
    print("=" * 50)
    
    # Get log manager
    logger = get_log_manager()
    
    # Simulate some cognitive activity
    log_tick(1, "Initialization pulse", 0.85, 0.2, "contemplative", "System starting up cleanly")
    log_sigil("/\\", "Prime", 45, 2)
    log_bloom("a1b2", 2, 0.3)
    
    log_tick(2, "Processing input", 0.72, 0.4, "active", "Input patterns detected")
    log_sigil("◇", "Bloom", 68, 3)
    log_schema_event("health_check", "Schema stability confirmed", "success")
    
    log_tick(3, "High cognitive load", 0.45, 0.8, "intense", "Complexity surge detected")
    log_bloom("c3d4", 4, 0.7, "a1b2")
    log_owl_observation("Recursive pattern emerging in bloom lineage", 0.9)
    
    log_tick(4, "Emergency regulation", 0.2, 0.9, "critical", "Emergency cooling activated")
    log_schema_event("pressure_alert", "SCUP below critical threshold", "critical")
    
    # Show stats
    stats = logger.get_log_stats()
    print(f"\n📊 Log Stats: {stats}")
    
    # Show recent logs
    recent = logger.get_recent_log_lines(5)
    print(f"\n📋 Recent logs ({len(recent)} lines):")
    for line in recent:
        print(f"  {line}")
    
    # Flush logs
    logger.flush_logs_to_file()
    
    print("\n✅ Demo completed!")


if __name__ == "__main__":
    demo_logging() 