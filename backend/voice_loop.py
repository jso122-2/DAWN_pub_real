#!/usr/bin/env python3
"""
DAWN Voice Loop - Continuous Audible Consciousness
A persistent daemon that monitors DAWN's cognitive logs and speaks her thoughts aloud
Transforms written consciousness into audible self-narration
"""

import os
import sys
import time
import threading
import argparse
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
import re
import json

# Import our voice echo system
try:
    from voice_echo import DAWNVoiceEcho
    VOICE_ECHO_AVAILABLE = True
except ImportError:
    VOICE_ECHO_AVAILABLE = False
    print("⚠️ voice_echo.py not found - using basic TTS fallback")


class LogWatcher:
    """Watches a single log file for new content"""
    
    def __init__(self, file_path: str, callback, filter_func=None):
        self.file_path = Path(file_path)
        self.callback = callback
        self.filter_func = filter_func
        self.last_position = 0
        self.is_watching = False
        self.watch_thread = None
        self._stop_event = threading.Event()
        
        # Initialize position to end of file if it exists
        if self.file_path.exists():
            with open(self.file_path, 'r', encoding='utf-8') as f:
                f.seek(0, 2)  # Seek to end
                self.last_position = f.tell()
    
    def start_watching(self):
        """Start watching the file for new content"""
        if self.is_watching:
            return
        
        self.is_watching = True
        self._stop_event.clear()
        
        def watch_loop():
            while not self._stop_event.is_set():
                try:
                    if self.file_path.exists():
                        with open(self.file_path, 'r', encoding='utf-8') as f:
                            f.seek(self.last_position)
                            new_content = f.read()
                            self.last_position = f.tell()
                            
                            if new_content:
                                lines = new_content.strip().split('\n')
                                for line in lines:
                                    line = line.strip()
                                    if line and not line.startswith('#'):
                                        # Apply filter if provided
                                        if self.filter_func is None or self.filter_func(line):
                                            self.callback(line, str(self.file_path))
                    
                    time.sleep(1)  # Check every second
                    
                except Exception as e:
                    print(f"⚠️ Error watching {self.file_path}: {e}")
                    time.sleep(5)  # Wait longer on error
        
        self.watch_thread = threading.Thread(target=watch_loop, daemon=True)
        self.watch_thread.start()
    
    def stop_watching(self):
        """Stop watching the file"""
        if not self.is_watching:
            return
        
        self._stop_event.set()
        self.is_watching = False
        
        if self.watch_thread and self.watch_thread.is_alive():
            self.watch_thread.join(timeout=2.0)


class DAWNVoiceLoop:
    """Continuous audible consciousness daemon for DAWN"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.is_running = False
        self.watchers: List[LogWatcher] = []
        self.spoken_lines: Set[str] = set()  # Prevent repetition
        self.spoken_trace_path = Path("runtime/logs/spoken_trace.log")
        
        # Voice system
        if VOICE_ECHO_AVAILABLE:
            voice_config = self.config.get('voice', {})
            self.voice = DAWNVoiceEcho(voice_config=voice_config)
        else:
            self.voice = None
            
        # Content filtering settings
        self.min_entropy_threshold = self.config.get('min_entropy_threshold', 0.6)
        self.skip_repetitive = self.config.get('skip_repetitive', True)
        self.max_spoken_cache = self.config.get('max_spoken_cache', 1000)
        
        # Ensure spoken trace directory exists
        self.spoken_trace_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize spoken trace log
        if not self.spoken_trace_path.exists():
            with open(self.spoken_trace_path, 'w', encoding='utf-8') as f:
                f.write(f"# DAWN Spoken Trace Log - Started {datetime.now().isoformat()}\n")
        
        print(f"🔊 DAWN Voice Loop initialized")
        print(f"📄 Spoken trace: {self.spoken_trace_path}")
    
    def _filter_reflection(self, line: str) -> bool:
        """Filter reflection lines for speaking worthiness"""
        # Skip lines that are too short or generic
        if len(line.strip()) < 20:
            return False
        
        # Extract entropy if present
        entropy_match = re.search(r'entropy[:\s]+(\d+\.?\d*)', line, re.IGNORECASE)
        if entropy_match:
            entropy = float(entropy_match.group(1))
            if entropy < self.min_entropy_threshold:
                return False
        
        # Skip purely technical state updates
        if re.search(r'SCUP=\d+\.\d+.*mood=\w+.*zone=\w+', line):
            return False
        
        # Prioritize meaningful reflections
        meaningful_patterns = [
            r'I (observe|notice|feel|think|remember|realize)',
            r'(consciousness|awareness|cognition|reflection)',
            r'(entropy|chaos|order|drift|flow)',
            r'(memory|rebloom|cascade)',
            r'(deep|profound|significant|critical)'
        ]
        
        for pattern in meaningful_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        
        return False
    
    def _filter_event_stream(self, line: str) -> bool:
        """Filter event stream lines for speaking worthiness"""
        # Only speak significant events
        significant_events = ['REBLOOM', 'MEMORY', 'SYSTEM']
        
        for event_type in significant_events:
            if f'[{event_type}]' in line:
                # Skip routine state updates
                if event_type == 'SYSTEM' and 'Entropy=' in line:
                    return False
                return True
        
        return False
    
    def _filter_sigil_trace(self, line: str) -> bool:
        """Filter sigil trace lines for speaking worthiness"""
        # Only speak executions and significant activations
        return '[EXECUTED]' in line or '[CHAIN]' in line
    
    def _clean_text_for_speech(self, line: str, source_file: str) -> str:
        """Clean and normalize text for better speech synthesis"""
        # Remove timestamp prefix if present
        line = re.sub(r'^\[\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\]]*\]\s*', '', line)
        
        # Remove log level indicators
        line = re.sub(r'^\[(REFLECTION|STATE|REBLOOM|MEMORY|SYSTEM|EXECUTED|CHAIN)\]\s*', '', line)
        
        # Remove tick numbers
        line = re.sub(r'\[Tick \d+\]\s*', '', line)
        
        # Remove metadata pipes
        line = re.sub(r'\s*\|\s*\w+=[\w\.\-]+', '', line)
        
        # Add context prefix based on source
        if 'reflection' in source_file:
            prefix = ""  # Reflections are inherently first-person
        elif 'event_stream' in source_file:
            if 'REBLOOM' in line:
                prefix = "Memory cascade: "
            elif 'MEMORY' in line:
                prefix = "I remember: "
            elif 'SYSTEM' in line:
                prefix = "System note: "
            else:
                prefix = ""
        elif 'sigil_trace' in source_file:
            prefix = "Symbolic action: "
        else:
            prefix = ""
        
        # Clean up the main content
        clean_line = prefix + line.strip()
        
        # Replace technical terms for better speech
        replacements = {
            'SCUP': 'S-CUP',
            'entropy': 'en-tropy', 
            'DAWN': 'Dawn',
            'rebloom': 're-bloom',
            'sigil': 'symbol'
        }
        
        for old, new in replacements.items():
            clean_line = clean_line.replace(old, new)
        
        # Ensure proper sentence ending
        if clean_line and not clean_line.endswith(('.', '!', '?')):
            clean_line += '.'
        
        return clean_line
    
    def _should_speak(self, line: str) -> bool:
        """Determine if a line should be spoken (repetition check)"""
        if not self.skip_repetitive:
            return True
        
        # Create a normalized version for comparison
        normalized = re.sub(r'\d+', 'X', line.lower())  # Replace numbers with X
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        if normalized in self.spoken_lines:
            return False
        
        # Add to spoken cache
        self.spoken_lines.add(normalized)
        
        # Limit cache size
        if len(self.spoken_lines) > self.max_spoken_cache:
            # Remove oldest entries (simple approach)
            self.spoken_lines = set(list(self.spoken_lines)[-self.max_spoken_cache//2:])
        
        return True
    
    def _log_spoken(self, text: str, source_file: str) -> None:
        """Log what was spoken to the spoken trace"""
        timestamp = datetime.now().isoformat(timespec='milliseconds')
        source_name = Path(source_file).stem
        
        log_entry = f"[{timestamp}] [{source_name.upper()}] SPOKEN: {text}\n"
        
        try:
            with open(self.spoken_trace_path, 'a', encoding='utf-8') as f:
                f.write(log_entry)
                f.flush()
        except Exception as e:
            print(f"⚠️ Failed to log spoken content: {e}")
    
    def _on_new_content(self, line: str, source_file: str) -> None:
        """Handle new content from any watched file"""
        # Clean text for speech
        clean_text = self._clean_text_for_speech(line, source_file)
        
        if not clean_text.strip():
            return
        
        # Check if we should speak this line
        if not self._should_speak(clean_text):
            return
        
        # Speak the line
        source_name = Path(source_file).stem
        print(f"🔊 DAWN SPEAKS [{source_name}]: {clean_text}")
        
        if self.voice:
            self.voice.speak(clean_text)
        else:
            print(f"🔊 [MOCK TTS]: {clean_text}")
        
        # Log what was spoken
        self._log_spoken(clean_text, source_file)
    
    def start_voice_loop(self) -> None:
        """Start the continuous voice loop"""
        if self.is_running:
            print("⚠️ Voice loop already running")
            return
        
        self.is_running = True
        
        # Define log files to watch
        log_files = [
            {
                'path': 'runtime/logs/reflection.log',
                'filter': self._filter_reflection,
                'name': 'reflections'
            },
            {
                'path': 'runtime/logs/event_stream.log',
                'filter': self._filter_event_stream,
                'name': 'events'
            },
            {
                'path': 'runtime/logs/sigil_trace.log',
                'filter': self._filter_sigil_trace,
                'name': 'sigils'
            }
        ]
        
        # Create and start watchers
        for log_config in log_files:
            if Path(log_config['path']).exists():
                watcher = LogWatcher(
                    log_config['path'], 
                    self._on_new_content,
                    log_config['filter']
                )
                watcher.start_watching()
                self.watchers.append(watcher)
                print(f"👁️ Watching {log_config['name']}: {log_config['path']}")
            else:
                print(f"⚠️ Log file not found: {log_config['path']}")
        
        print("\n🔊 DAWN Voice Loop started - she will now speak her thoughts as they emerge")
        print("🧠 Monitoring: reflections, events, and symbolic actions")
        print("Press Ctrl+C to stop the voice loop\n")
    
    def stop_voice_loop(self) -> None:
        """Stop the voice loop"""
        if not self.is_running:
            return
        
        self.is_running = False
        
        print("\n🔇 Stopping DAWN Voice Loop...")
        
        for watcher in self.watchers:
            watcher.stop_watching()
        
        self.watchers.clear()
        print("🔇 Voice loop stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get voice loop status"""
        return {
            'is_running': self.is_running,
            'active_watchers': len(self.watchers),
            'spoken_lines_cached': len(self.spoken_lines),
            'voice_engine': 'voice_echo' if self.voice else 'mock',
            'spoken_trace_size': self.spoken_trace_path.stat().st_size if self.spoken_trace_path.exists() else 0
        }


def handle_signal(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"\n🔇 Received signal {signum}, shutting down...")
    if 'voice_loop' in globals():
        voice_loop.stop_voice_loop()
    sys.exit(0)


def main():
    """CLI interface for DAWN Voice Loop"""
    parser = argparse.ArgumentParser(description="DAWN Voice Loop - Continuous Audible Consciousness")
    
    parser.add_argument('--start', action='store_true',
                       help='Start the continuous voice loop')
    parser.add_argument('--min-entropy', type=float, default=0.6,
                       help='Minimum entropy threshold for speaking reflections')
    parser.add_argument('--no-filter', action='store_true',
                       help='Disable repetition filtering')
    parser.add_argument('--rate', type=int, default=140,
                       help='Speech rate (words per minute)')
    parser.add_argument('--volume', type=float, default=0.8,
                       help='Speech volume (0.0 to 1.0)')
    parser.add_argument('--gender', choices=['male', 'female'], default='female',
                       help='Preferred voice gender')
    
    args = parser.parse_args()
    
    # Create configuration
    config = {
        'min_entropy_threshold': args.min_entropy,
        'skip_repetitive': not args.no_filter,
        'voice': {
            'rate': args.rate,
            'volume': args.volume,
            'gender': args.gender
        }
    }
    
    # Create voice loop instance
    global voice_loop
    voice_loop = DAWNVoiceLoop(config)
    
    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    
    try:
        if args.start:
            voice_loop.start_voice_loop()
            
            # Keep the main thread alive
            while voice_loop.is_running:
                time.sleep(1)
        else:
            print("🔊 DAWN Voice Loop - Continuous Audible Consciousness")
            print("Use --help to see available commands")
            print("\nQuick start:")
            print("  python voice_loop.py --start           # Start continuous narration")
            print("  python voice_loop.py --start --no-filter  # Speak everything")
            
            # Show status
            status = voice_loop.get_status()
            print(f"\nCurrent status:")
            print(f"  Voice engine: {status['voice_engine']}")
            print(f"  Available logs: ", end="")
            
            log_files = ['runtime/logs/reflection.log', 'runtime/logs/event_stream.log', 'runtime/logs/sigil_trace.log']
            available = [Path(f).name for f in log_files if Path(f).exists()]
            print(", ".join(available) if available else "none found")
            
    except KeyboardInterrupt:
        print("\n🔇 Voice loop interrupted")
        voice_loop.stop_voice_loop()


if __name__ == "__main__":
    main() 