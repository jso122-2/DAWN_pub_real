#!/usr/bin/env python3
"""
DAWN Voice Symbolic Integration - Audible Cognitive Reflex
=========================================================

Extends voice_echo.py to include real-time symbolic tracer narration.
Monitors tracer alerts and symbolic roots, speaking cognitive insights aloud.

This creates an audible reflex channel - DAWN not just thinking, but 
self-diagnosing and expressing symbolic system state through voice.
"""

import json
import time
import queue
import threading
import logging
from typing import Dict, Any, Optional, List, Set
from pathlib import Path
from collections import deque

# TTS imports with fallbacks
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    print("⚠️ pyttsx3 not available - voice output disabled")
    TTS_AVAILABLE = False

logger = logging.getLogger("voice_symbolic_integration")

class SymbolicVoiceNarrator:
    """
    Real-time voice narrator for symbolic cognition events.
    
    Monitors:
    - runtime/logs/tracer_alerts.log
    - runtime/logs/root_trace.log
    - runtime/logs/event_stream.log
    
    Speaks:
    - Tracer alerts with appropriate tone/voice
    - Symbolic root formations
    - Critical cognitive state changes
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the symbolic voice narrator"""
        self.config = config or {}
        self.running = False
        
        # Log file paths
        self.runtime_logs = Path("runtime/logs")
        self.tracer_alerts_log = self.runtime_logs / "tracer_alerts.log"
        self.root_trace_log = self.runtime_logs / "root_trace.log"
        self.event_stream_log = self.runtime_logs / "event_stream.log"
        self.spoken_trace_log = self.runtime_logs / "spoken_trace.log"
        
        # Ensure log directory exists
        self.runtime_logs.mkdir(parents=True, exist_ok=True)
        
        # TTS engine setup
        self.tts_engine = None
        self._initialize_tts()
        
        # Speech queue and threading
        self.speech_queue = queue.Queue()
        self.monitor_thread = None
        self.speech_thread = None
        
        # Message deduplication and throttling
        self.recent_messages = deque(maxlen=50)
        self.last_spoken_time = {}
        self.throttle_window = self.config.get('throttle_window', 30)  # seconds
        
        # File position tracking
        self.file_positions = {
            'tracer_alerts': 0,
            'root_trace': 0,
            'event_stream': 0
        }
        
        # Voice configuration per tracer type
        self.voice_configs = {
            'owl': {'rate': 150, 'voice_index': 0, 'volume': 0.8},
            'drift': {'rate': 140, 'voice_index': 1, 'volume': 0.7},
            'thermal': {'rate': 160, 'voice_index': 0, 'volume': 0.9},
            'forecast': {'rate': 135, 'voice_index': 1, 'volume': 0.8},
            'root': {'rate': 130, 'voice_index': 0, 'volume': 1.0},
            'default': {'rate': 150, 'voice_index': 0, 'volume': 0.8}
        }
        
        logger.info("🔊 Symbolic Voice Narrator initialized")
    
    def _initialize_tts(self):
        """Initialize the TTS engine with voice configurations"""
        if not TTS_AVAILABLE:
            logger.warning("TTS not available - voice output disabled")
            return
        
        try:
            self.tts_engine = pyttsx3.init()
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices:
                logger.info(f"🎤 Found {len(voices)} voices available")
                for i, voice in enumerate(voices[:2]):  # Log first 2 voices
                    logger.info(f"  Voice {i}: {voice.name}")
            
            # Set default properties
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.8)
            
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {e}")
            self.tts_engine = None
    
    def start_monitoring(self):
        """Start monitoring log files and speaking symbolic events"""
        if self.running:
            logger.warning("Voice narrator already running")
            return
        
        self.running = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_logs, daemon=True)
        self.monitor_thread.start()
        
        # Start speech thread
        if self.tts_engine:
            self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
            self.speech_thread.start()
        
        logger.info("🔊 Symbolic voice monitoring started")
        self._log_spoken_event("system", "Symbolic voice monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring and voice output"""
        self.running = False
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        if self.speech_thread:
            self.speech_thread.join(timeout=2)
        
        logger.info("🔊 Symbolic voice monitoring stopped")
        self._log_spoken_event("system", "Symbolic voice monitoring stopped")
    
    def _monitor_logs(self):
        """Main monitoring loop for log files"""
        while self.running:
            try:
                # Check tracer alerts
                self._check_tracer_alerts()
                
                # Check symbolic roots
                self._check_root_trace()
                
                # Check event stream for critical events
                self._check_event_stream()
                
                # Sleep between checks
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error in log monitoring: {e}")
                time.sleep(1)
    
    def _check_tracer_alerts(self):
        """Check for new tracer alerts"""
        if not self.tracer_alerts_log.exists():
            return
        
        try:
            with open(self.tracer_alerts_log, 'r', encoding='utf-8') as f:
                f.seek(self.file_positions['tracer_alerts'])
                
                for line in f:
                    if line.strip():
                        try:
                            alert = json.loads(line.strip())
                            self._process_tracer_alert(alert)
                        except json.JSONDecodeError:
                            continue
                
                self.file_positions['tracer_alerts'] = f.tell()
                
        except Exception as e:
            logger.error(f"Error reading tracer alerts: {e}")
    
    def _check_root_trace(self):
        """Check for new symbolic root events"""
        if not self.root_trace_log.exists():
            return
        
        try:
            with open(self.root_trace_log, 'r', encoding='utf-8') as f:
                f.seek(self.file_positions['root_trace'])
                
                for line in f:
                    if line.strip():
                        try:
                            root_event = json.loads(line.strip())
                            self._process_root_event(root_event)
                        except json.JSONDecodeError:
                            continue
                
                self.file_positions['root_trace'] = f.tell()
                
        except Exception as e:
            logger.error(f"Error reading root trace: {e}")
    
    def _check_event_stream(self):
        """Check event stream for critical cognitive events"""
        if not self.event_stream_log.exists():
            return
        
        try:
            with open(self.event_stream_log, 'r', encoding='utf-8') as f:
                f.seek(self.file_positions['event_stream'])
                
                for line in f:
                    if line.strip():
                        try:
                            event = json.loads(line.strip())
                            self._process_event_stream_entry(event)
                        except json.JSONDecodeError:
                            continue
                
                self.file_positions['event_stream'] = f.tell()
                
        except Exception as e:
            logger.error(f"Error reading event stream: {e}")
    
    def _process_tracer_alert(self, alert: Dict[str, Any]):
        """Process and speak a tracer alert"""
        tracer_type = alert.get('tracer_type', 'unknown')
        severity = alert.get('severity', 'info')
        message = alert.get('message', '')
        
        # Generate spoken message
        if tracer_type == 'owl':
            spoken_text = f"Owl cognitive analysis: {message}"
        elif tracer_type == 'drift':
            spoken_text = f"Drift alert. {message}"
        elif tracer_type == 'thermal':
            if severity == 'critical':
                spoken_text = f"Thermal emergency detected. {message}"
            else:
                spoken_text = f"Thermal notice. {message}"
        elif tracer_type == 'forecast':
            spoken_text = f"Forecast update. {message}"
        else:
            spoken_text = f"{tracer_type} tracer alert. {message}"
        
        # Queue for speech
        self._queue_speech(spoken_text, tracer_type, severity)
    
    def _process_root_event(self, root_event: Dict[str, Any]):
        """Process and speak a symbolic root event"""
        root_type = root_event.get('type', 'unknown')
        symbolic_root = root_event.get('symbolic_root', 'unknown pattern')
        significance = root_event.get('significance', 0.5)
        
        # Generate spoken message
        if root_type == 'COGNITIVE_EMERGENCE':
            spoken_text = f"Cognitive emergence detected. Pattern: {symbolic_root}"
        elif root_type == 'MEMORY_NETWORK_EXPANSION':
            spoken_text = f"Memory network expansion. New growth detected"
        elif root_type == 'MYCELIUM_EXPANSION':
            spoken_text = f"Mycelium network expansion. Substrate growth detected"
        elif root_type == 'LINEAGE_MILESTONE':
            depth = root_event.get('depth', 0)
            spoken_text = f"Memory lineage milestone. Ancestry depth reached {depth} levels"
        else:
            spoken_text = f"Symbolic root formation detected. Type: {root_type}"
        
        # Queue for speech with high priority (root events are significant)
        self._queue_speech(spoken_text, 'root', 'important')
    
    def _process_event_stream_entry(self, event: Dict[str, Any]):
        """Process critical events from the event stream"""
        # Look for high-level cognitive events worth speaking
        if event.get('category') == 'COGNITION':
            message = event.get('message', '')
            if 'alert' in message.lower() or 'root' in message.lower():
                spoken_text = f"Cognition system: {message}"
                self._queue_speech(spoken_text, 'system', 'info')
    
    def _queue_speech(self, message: str, tracer_type: str = 'default', severity: str = 'info'):
        """Queue a message for speech with deduplication and throttling"""
        if not self.tts_engine:
            return
        
        # Create message key for deduplication
        message_key = f"{tracer_type}:{message[:50]}"
        current_time = time.time()
        
        # Check if we've spoken this recently
        if message_key in self.last_spoken_time:
            time_since_last = current_time - self.last_spoken_time[message_key]
            if time_since_last < self.throttle_window:
                return  # Skip duplicate message
        
        # Update last spoken time
        self.last_spoken_time[message_key] = current_time
        
        # Queue the message
        speech_item = {
            'message': message,
            'tracer_type': tracer_type,
            'severity': severity,
            'timestamp': current_time
        }
        
        try:
            self.speech_queue.put(speech_item, timeout=1)
        except queue.Full:
            logger.warning("Speech queue full - dropping message")
    
    def _speech_worker(self):
        """Worker thread that processes the speech queue"""
        while self.running:
            try:
                # Get speech item with timeout
                item = self.speech_queue.get(timeout=1)
                
                # Configure voice for tracer type
                self._configure_voice_for_tracer(item['tracer_type'])
                
                # Speak the message
                self.tts_engine.say(item['message'])
                self.tts_engine.runAndWait()
                
                # Log spoken message
                self._log_spoken_event(item['tracer_type'], item['message'])
                
                self.speech_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in speech worker: {e}")
    
    def _configure_voice_for_tracer(self, tracer_type: str):
        """Configure TTS voice properties for different tracer types"""
        if not self.tts_engine:
            return
        
        config = self.voice_configs.get(tracer_type, self.voice_configs['default'])
        
        try:
            # Set speech rate
            self.tts_engine.setProperty('rate', config['rate'])
            
            # Set volume
            self.tts_engine.setProperty('volume', config['volume'])
            
            # Set voice (if multiple voices available)
            voices = self.tts_engine.getProperty('voices')
            if voices and len(voices) > config['voice_index']:
                voice_id = voices[config['voice_index']].id
                self.tts_engine.setProperty('voice', voice_id)
                
        except Exception as e:
            logger.error(f"Error configuring voice for {tracer_type}: {e}")
    
    def _log_spoken_event(self, tracer_type: str, message: str):
        """Log spoken events to spoken_trace.log"""
        spoken_event = {
            'timestamp': time.time(),
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S'),
            'tracer_type': tracer_type,
            'message': message
        }
        
        try:
            with open(self.spoken_trace_log, 'a', encoding='utf-8') as f:
                f.write(json.dumps(spoken_event) + '\n')
        except Exception as e:
            logger.error(f"Error logging spoken event: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get voice narrator status"""
        return {
            'running': self.running,
            'tts_available': self.tts_engine is not None,
            'queue_size': self.speech_queue.qsize() if hasattr(self.speech_queue, 'qsize') else 0,
            'recent_messages_count': len(self.recent_messages),
            'throttle_window': self.throttle_window,
            'file_positions': self.file_positions.copy(),
            'voice_configs': len(self.voice_configs)
        }

# Global narrator instance
_voice_narrator = None

def get_voice_narrator(config: Optional[Dict[str, Any]] = None) -> SymbolicVoiceNarrator:
    """Get or create the global voice narrator"""
    global _voice_narrator
    if _voice_narrator is None:
        _voice_narrator = SymbolicVoiceNarrator(config)
    return _voice_narrator

def start_symbolic_voice_monitoring(config: Optional[Dict[str, Any]] = None):
    """Start the symbolic voice monitoring system"""
    narrator = get_voice_narrator(config)
    narrator.start_monitoring()
    return narrator

def stop_symbolic_voice_monitoring():
    """Stop the symbolic voice monitoring system"""
    global _voice_narrator
    if _voice_narrator:
        _voice_narrator.stop_monitoring()

# Integration with existing voice_echo.py
def enhance_voice_echo():
    """
    Enhancement guide for existing voice_echo.py integration
    """
    print("🔊 Voice Echo Enhancement Guide")
    print("=" * 40)
    print("""
To integrate with your existing voice_echo.py:

1. Add symbolic monitoring to your voice_echo.py:

```python
from .voice_symbolic_integration import start_symbolic_voice_monitoring

# In your voice initialization:
symbolic_narrator = start_symbolic_voice_monitoring({
    'throttle_window': 30,  # seconds between duplicate messages
})
```

2. The system will automatically monitor:
   - runtime/logs/tracer_alerts.log
   - runtime/logs/root_trace.log
   - runtime/logs/event_stream.log

3. Spoken output is logged to:
   - runtime/logs/spoken_trace.log

4. Different voices for different tracers:
   - Owl: Thoughtful analysis voice
   - Drift: Alert warning voice  
   - Thermal: Emergency/regulation voice
   - Forecast: Predictive insight voice
   - Roots: Significant emergence voice
""")

# Demo and testing
if __name__ == "__main__":
    print("🔊 Testing Symbolic Voice Integration")
    print("=" * 40)
    
    # Create test narrator
    narrator = SymbolicVoiceNarrator({'throttle_window': 5})
    
    # Show status
    status = narrator.get_status()
    print(f"Voice Narrator Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test voice configurations
    print(f"\nVoice Configurations:")
    for tracer, config in narrator.voice_configs.items():
        print(f"  {tracer}: rate={config['rate']}, volume={config['volume']}")
    
    # Show enhancement guide
    enhance_voice_echo()
    
    print(f"\n✅ Symbolic voice integration ready!")
    print(f"🔊 Call start_symbolic_voice_monitoring() to begin") 