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
    structured output for both real-time viewing and historical analysis.
    """
    
    def __init__(self, log_directory: str = "logs", buffer_size: int = 500):
        """
        Initialize the log manager.
        
        Args:
            log_directory: Directory to store log files
            buffer_size: Maximum number of log entries to keep in memory
        """
        self.log_directory = log_directory
        self.buffer_size = buffer_size
        
        # Memory buffer for fast access to recent logs
        self.memory_buffer = deque(maxlen=buffer_size)
        
        # Counters and state
        self.tick_count = 0
        self.session_start_time = datetime.now()
        self.last_file_write = 0
        self.file_write_interval = 100  # Write to file every N ticks
        
        # Threading lock for safe concurrent access
        self.lock = threading.Lock()
        
        # Ensure log directory exists
        os.makedirs(self.log_directory, exist_ok=True)
        
        # Generate session log filename
        timestamp = self.session_start_time.strftime("%Y%m%d_%H%M%S")
        self.session_log_file = os.path.join(self.log_directory, f"dawn_session_{timestamp}.log")
        
        # Initialize session
        self._log_session_start()
    
    def _log_session_start(self):
        """Log the start of a new DAWN session."""
        start_message = f"🌅 DAWN Session Started: {self.session_start_time.isoformat()}"
        self._write_log_entry("SESSION", start_message, level="INFO")
        print(f"\n{start_message}")
        print(f"📁 Session log: {self.session_log_file}")
        print("=" * 60)
    
    def _write_log_entry(self, category: str, message: str, level: str = "INFO", 
                        metadata: Optional[dict] = None):
        """
        Write a log entry to memory buffer and conditionally to file.
        
        Args:
            category: Log category (e.g., 'TICK', 'SIGIL', 'BLOOM')
            message: Log message content
            level: Log level (DEBUG, INFO, WARN, ERROR)
            metadata: Optional metadata dictionary
        """
        timestamp = datetime.now()
        
        log_entry = {
            'timestamp': timestamp.isoformat(),
            'tick': self.tick_count,
            'category': category,
            'level': level,
            'message': message,
            'metadata': metadata or {}
        }
        
        with self.lock:
            # Add to memory buffer
            self.memory_buffer.append(log_entry)
            
            # Check if we should write to file
            if self.tick_count - self.last_file_write >= self.file_write_interval:
                self._flush_to_file()
                self.last_file_write = self.tick_count
    
    def _flush_to_file(self):
        """Flush recent log entries to the session log file."""
        try:
            with open(self.session_log_file, 'a', encoding='utf-8') as f:
                # Write any unbuffered entries
                entries_to_write = list(self.memory_buffer)[-self.file_write_interval:]
                
                for entry in entries_to_write:
                    log_line = f"{entry['timestamp']} | {entry['level']:5} | {entry['category']:8} | {entry['message']}"
                    
                    if entry['metadata']:
                        log_line += f" | META: {entry['metadata']}"
                    
                    f.write(log_line + "\n")
                
                f.flush()
        except Exception as e:
            print(f"⚠️  Log file write error: {e}")
    
    def log_tick(self, tick_number: int, zone: str, heat: float, entropy: float, 
                 active_sigils: int = 0):
        """
        Log a system tick with core metrics.
        
        Args:
            tick_number: Current tick number
            zone: Pulse zone (CALM, ACTIVE, SURGE)
            heat: Heat level (0.0-1.0)
            entropy: Entropy level (0.0-1.0)
            active_sigils: Number of active sigils
        """
        self.tick_count = tick_number
        
        # Create visual representation
        heat_bar = self._create_bar(heat, 10)
        entropy_bar = self._create_bar(entropy, 10)
        zone_symbol = self._get_zone_symbol(zone)
        
        # Terminal output
        tick_message = (f"⚡ Tick {tick_number:04d} | {zone_symbol} {zone:6} | "
                       f"🔥 {heat_bar} {heat:.3f} | 🌀 {entropy_bar} {entropy:.3f}")
        
        if active_sigils > 0:
            tick_message += f" | 🔮 Sigils: {active_sigils}"
        
        print(tick_message)
        
        # Log to file
        metadata = {
            'zone': zone,
            'heat': heat,
            'entropy': entropy,
            'active_sigils': active_sigils
        }
        self._write_log_entry("TICK", f"Tick {tick_number}", metadata=metadata)
    
    def log_sigil_event(self, sigil_id: str, event_type: str, details: str = "",
                       temperature: float = 0.0, house: str = ""):
        """
        Log a sigil-related event.
        
        Args:
            sigil_id: Unique sigil identifier
            event_type: Type of event (CREATED, ACTIVATED, EXPIRED, etc.)
            details: Additional event details
            temperature: Sigil temperature
            house: Cognitive house
        """
        sigil_symbol = self._get_sigil_symbol(event_type)
        
        # Terminal output
        sigil_message = f"🔮 {sigil_symbol} Sigil {sigil_id} | {event_type}"
        if house:
            sigil_message += f" | House: {house}"
        if temperature > 0:
            sigil_message += f" | Temp: {temperature:.3f}"
        if details:
            sigil_message += f" | {details}"
        
        print(f"   {sigil_message}")
        
        # Log to file
        metadata = {
            'sigil_id': sigil_id,
            'event_type': event_type,
            'temperature': temperature,
            'house': house,
            'details': details
        }
        self._write_log_entry("SIGIL", sigil_message, metadata=metadata)
    
    def log_bloom_event(self, bloom_id: str, event_type: str, entropy_change: float = 0.0,
                       bloom_type: str = "", details: str = ""):
        """
        Log a bloom-related event.
        
        Args:
            bloom_id: Unique bloom identifier
            event_type: Type of event (SPAWNED, EVOLVED, MERGED, etc.)
            entropy_change: Change in entropy
            bloom_type: Type of bloom
            details: Additional event details
        """
        bloom_symbol = self._get_bloom_symbol(event_type)
        
        # Terminal output
        bloom_message = f"🌸 {bloom_symbol} Bloom {bloom_id} | {event_type}"
        if bloom_type:
            bloom_message += f" | Type: {bloom_type}"
        if entropy_change != 0:
            change_symbol = "📈" if entropy_change > 0 else "📉"
            bloom_message += f" | {change_symbol} Δ{entropy_change:+.3f}"
        if details:
            bloom_message += f" | {details}"
        
        print(f"   {bloom_message}")
        
        # Log to file
        metadata = {
            'bloom_id': bloom_id,
            'event_type': event_type,
            'entropy_change': entropy_change,
            'bloom_type': bloom_type,
            'details': details
        }
        self._write_log_entry("BLOOM", bloom_message, metadata=metadata)
    
    def log_system_event(self, event_type: str, message: str, level: str = "INFO",
                        metadata: Optional[dict] = None):
        """
        Log a general system event.
        
        Args:
            event_type: Type of system event
            message: Event message
            level: Log level
            metadata: Optional metadata
        """
        level_symbol = self._get_level_symbol(level)
        
        # Terminal output
        system_message = f"🧠 {level_symbol} {event_type}: {message}"
        print(f"   {system_message}")
        
        # Log to file
        self._write_log_entry("SYSTEM", f"{event_type}: {message}", level=level, metadata=metadata)
    
    def log_error(self, error_message: str, exception: Optional[Exception] = None,
                 context: str = ""):
        """
        Log an error with optional exception details.
        
        Args:
            error_message: Error description
            exception: Optional exception object
            context: Additional context
        """
        error_text = f"❌ ERROR: {error_message}"
        if context:
            error_text += f" | Context: {context}"
        if exception:
            error_text += f" | Exception: {str(exception)}"
        
        print(f"   {error_text}")
        
        # Log to file with full details
        metadata = {
            'context': context,
            'exception_type': type(exception).__name__ if exception else None,
            'exception_message': str(exception) if exception else None
        }
        self._write_log_entry("ERROR", error_message, level="ERROR", metadata=metadata)
    
    def get_recent_logs(self, count: int = 50, category: Optional[str] = None) -> List[dict]:
        """
        Get recent log entries from memory buffer.
        
        Args:
            count: Number of recent entries to return
            category: Optional category filter
            
        Returns:
            List of log entry dictionaries
        """
        with self.lock:
            entries = list(self.memory_buffer)
        
        if category:
            entries = [entry for entry in entries if entry['category'] == category]
        
        return entries[-count:] if entries else []
    
    def search_logs(self, search_term: str, category: Optional[str] = None,
                   last_n_entries: int = 1000) -> List[dict]:
        """
        Search recent log entries for a specific term.
        
        Args:
            search_term: Term to search for
            category: Optional category filter
            last_n_entries: Number of recent entries to search
            
        Returns:
            List of matching log entries
        """
        recent_entries = self.get_recent_logs(last_n_entries, category)
        
        matching_entries = []
        for entry in recent_entries:
            if (search_term.lower() in entry['message'].lower() or
                search_term.lower() in str(entry['metadata']).lower()):
                matching_entries.append(entry)
        
        return matching_entries
    
    def get_session_summary(self) -> dict:
        """
        Get a summary of the current session.
        
        Returns:
            Dictionary with session statistics
        """
        runtime = datetime.now() - self.session_start_time
        
        with self.lock:
            entries_by_category = {}
            entries_by_level = {}
            
            for entry in self.memory_buffer:
                category = entry['category']
                level = entry['level']
                
                entries_by_category[category] = entries_by_category.get(category, 0) + 1
                entries_by_level[level] = entries_by_level.get(level, 0) + 1
        
        return {
            'session_start': self.session_start_time.isoformat(),
            'runtime_seconds': runtime.total_seconds(),
            'current_tick': self.tick_count,
            'total_log_entries': len(self.memory_buffer),
            'entries_by_category': entries_by_category,
            'entries_by_level': entries_by_level,
            'log_file': self.session_log_file
        }
    
    def close_session(self):
        """Close the current logging session and flush all data."""
        # Final flush to file
        self._flush_to_file()
        
        # Log session end
        end_time = datetime.now()
        runtime = end_time - self.session_start_time
        
        end_message = f"🌇 DAWN Session Ended: {end_time.isoformat()} | Runtime: {runtime}"
        self._write_log_entry("SESSION", end_message, level="INFO")
        
        print(f"\n{end_message}")
        print(f"📊 Session Summary:")
        
        summary = self.get_session_summary()
        print(f"   Total ticks: {summary['current_tick']}")
        print(f"   Log entries: {summary['total_log_entries']}")
        print(f"   Log file: {summary['log_file']}")
        print("=" * 60)
    
    # Utility methods for visual formatting
    def _create_bar(self, value: float, length: int = 10) -> str:
        """Create a visual bar representation of a value (0.0-1.0)."""
        filled_length = int(value * length)
        bar = "█" * filled_length + "░" * (length - filled_length)
        return bar
    
    def _get_zone_symbol(self, zone: str) -> str:
        """Get emoji symbol for pulse zone."""
        zone_symbols = {
            'CALM': '🟢',
            'ACTIVE': '🟡',
            'SURGE': '🔴'
        }
        return zone_symbols.get(zone, '⚪')
    
    def _get_sigil_symbol(self, event_type: str) -> str:
        """Get emoji symbol for sigil event type."""
        sigil_symbols = {
            'CREATED': '✨',
            'ACTIVATED': '⚡',
            'EVOLVED': '🔄',
            'EXPIRED': '💨',
            'MERGED': '🔗'
        }
        return sigil_symbols.get(event_type, '🔮')
    
    def _get_bloom_symbol(self, event_type: str) -> str:
        """Get emoji symbol for bloom event type."""
        bloom_symbols = {
            'SPAWNED': '🌱',
            'EVOLVED': '🌿',
            'BLOOMED': '🌸',
            'MERGED': '🌺',
            'DECAYED': '🍂'
        }
        return bloom_symbols.get(event_type, '🌸')
    
    def _get_level_symbol(self, level: str) -> str:
        """Get emoji symbol for log level."""
        level_symbols = {
            'DEBUG': '🔍',
            'INFO': 'ℹ️',
            'WARN': '⚠️',
            'ERROR': '❌'
        }
        return level_symbols.get(level, 'ℹ️')


# Example usage and testing
if __name__ == "__main__":
    print("📝 DAWN Log Manager Test Suite")
    print("=" * 40)
    
    # Create log manager
    log_manager = LogManager()
    
    # Simulate some DAWN system activity
    print("\n🧪 Simulating DAWN system activity...")
    
    # Log some ticks
    for tick in range(1, 6):
        zone = ["CALM", "ACTIVE", "SURGE"][tick % 3]
        heat = min(1.0, tick * 0.2)
        entropy = min(1.0, tick * 0.15)
        active_sigils = tick
        
        log_manager.log_tick(tick, zone, heat, entropy, active_sigils)
        time.sleep(0.1)  # Brief pause for realism
    
    # Log some sigil events
    print("\n🔮 Simulating sigil events...")
    sigil_events = [
        ("sigil_001", "CREATED", "Cognitive processing sigil", 0.3, "analytical"),
        ("sigil_002", "ACTIVATED", "Memory retrieval sigil", 0.7, "memory"),
        ("sigil_001", "EVOLVED", "Enhanced pattern recognition", 0.5, "analytical")
    ]
    
    for sigil_id, event_type, details, temp, house in sigil_events:
        log_manager.log_sigil_event(sigil_id, event_type, details, temp, house)
    
    # Log some bloom events
    print("\n🌸 Simulating bloom events...")
    bloom_events = [
        ("bloom_alpha", "SPAWNED", 0.2, "cognitive", "New cognitive bloom"),
        ("bloom_beta", "EVOLVED", 0.15, "memory", "Memory consolidation"),
        ("bloom_alpha", "MERGED", -0.1, "cognitive", "Merged with bloom_gamma")
    ]
    
    for bloom_id, event_type, entropy_change, bloom_type, details in bloom_events:
        log_manager.log_bloom_event(bloom_id, event_type, entropy_change, bloom_type, details)
    
    # Log system events
    print("\n🧠 Simulating system events...")
    log_manager.log_system_event("INITIALIZATION", "DAWN consciousness system started")
    log_manager.log_system_event("OPTIMIZATION", "Pulse controller calibrated", level="INFO")
    log_manager.log_error("Component timeout", context="Sigil processing")
    
    # Show session summary
    print("\n📊 Session Summary:")
    summary = log_manager.get_session_summary()
    print(f"   Runtime: {summary['runtime_seconds']:.1f} seconds")
    print(f"   Current tick: {summary['current_tick']}")
    print(f"   Total entries: {summary['total_log_entries']}")
    print(f"   Categories: {summary['entries_by_category']}")
    
    # Search logs
    print("\n🔍 Testing log search...")
    search_results = log_manager.search_logs("sigil")
    print(f"   Found {len(search_results)} entries containing 'sigil'")
    
    # Close session
    log_manager.close_session()
    
    print("\n🎉 Log manager test completed!") 