#!/usr/bin/env python3
"""
Enhanced DAWN Tracer Echo Voice - Audible Cognition Reflex System
================================================================

Background voice module that vocalizes critical symbolic alerts from DAWN's 
cognition system in real-time. Integrates with existing voice_loop.py to
provide spoken cognitive feedback.

Monitors:
- event_stream.log (cognition runtime outputs)
- root_trace.log (symbolic root formations) 
- tracer_alerts.log (tracer-specific alerts)

Speaks alerts using TTS with different voices/pitches per tracer type.
"""

import os
import sys
import json
import time
import threading
import logging
from typing import Dict, Any, Optional, Set
from pathlib import Path
from datetime import datetime, timedelta
from collections import deque
import hashlib

# TTS imports with fallbacks
try:
    import pyttsx3
    TTS_ENGINE = 'pyttsx3'
except ImportError:
    try:
        import subprocess
        TTS_ENGINE = 'espeak'
    except ImportError:
        TTS_ENGINE = 'none'
        print("⚠️ No TTS engine available. Install pyttsx3 or espeak for voice output.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enhanced_tracer_voice")

class EnhancedTracerEchoVoice:
    """
    Enhanced voice system that speaks DAWN's cognitive insights and alerts.
    
    Features:
    - Different voices/pitches per tracer type
    - Rate limiting to avoid speech spam
    - Message deduplication 
    - Integration with existing voice_loop.py
    - Background monitoring of cognitive events
    """
    
    def __init__(self, voice_log_path: str = "runtime/logs/spoken_trace.log"):
        """Initialize the enhanced tracer voice system"""
        self.voice_log_path = Path(voice_log_path)
        self.voice_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Monitoring paths
        self.event_stream_path = Path("runtime/logs/event_stream.log")
        self.tracer_alerts_path = Path("runtime/logs/tracer_alerts.log") 
        self.root_trace_path = Path("runtime/logs/root_trace.log")
        
        # TTS engine setup
        self.tts_engine = None
        self.setup_tts_engine()
        
        # Voice configuration per tracer type
        self.voice_configs = {
            'owl': {'rate': 160, 'pitch': 50, 'voice_id': 0},
            'drift': {'rate': 140, 'pitch': 30, 'voice_id': 1}, 
            'thermal': {'rate': 180, 'pitch': 70, 'voice_id': 0},
            'forecast': {'rate': 150, 'pitch': 60, 'voice_id': 1},
            'root': {'rate': 130, 'pitch': 40, 'voice_id': 0},
            'mycelium': {'rate': 120, 'pitch': 35, 'voice_id': 1},
            'rhizome': {'rate': 125, 'pitch': 45, 'voice_id': 0}
        }
        
        # State tracking
        self.file_positions = {
            'event_stream': 0,
            'tracer_alerts': 0,
            'root_trace': 0
        }
        
        # Speech management
        self.recent_messages: deque = deque(maxlen=100)
        self.message_cache: Dict[str, float] = {}  # message_hash -> last_spoken_time
        self.speech_queue: deque = deque(maxlen=20)
        self.last_speech_time = 0.0
        self.speech_rate_limit = 3.0  # Minimum 3 seconds between speech events
        
        # Configuration
        self.enable_owl_speech = True
        self.enable_drift_speech = True
        self.enable_thermal_speech = True
        self.enable_forecast_speech = True
        self.enable_root_speech = True
        self.critical_only_mode = False
        self.deduplication_window = 30.0  # Seconds
        
        # Threading
        self.monitoring_thread = None
        self.speech_thread = None
        self.running = False
        
        logger.info("🔊 Enhanced Tracer Echo Voice initialized")
        self.log_voice_event("VOICE_SYSTEM_INIT", "Enhanced cognitive voice system started")
    
    def setup_tts_engine(self):
        """Setup TTS engine with error handling"""
        if TTS_ENGINE == 'pyttsx3':
            try:
                self.tts_engine = pyttsx3.init()
                
                # Get available voices
                voices = self.tts_engine.getProperty('voices')
                if voices and len(voices) > 1:
                    logger.info(f"🗣️ TTS: Found {len(voices)} voices available")
                else:
                    logger.warning("🗣️ TTS: Limited voices available")
                
                # Set default properties
                self.tts_engine.setProperty('rate', 150)
                self.tts_engine.setProperty('volume', 0.8)
                
            except Exception as e:
                logger.error(f"Error initializing pyttsx3: {e}")
                self.tts_engine = None
        
        elif TTS_ENGINE == 'espeak':
            logger.info("🗣️ Using espeak for TTS")
        
        else:
            logger.warning("🗣️ No TTS engine available - voice output disabled")
    
    def start_monitoring(self):
        """Start background monitoring of cognitive events"""
        if self.running:
            return
        
        self.running = True
        
        # Start monitoring thread
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        # Start speech processing thread
        self.speech_thread = threading.Thread(target=self._speech_processing_loop, daemon=True)
        self.speech_thread.start()
        
        logger.info("🎤 Enhanced voice monitoring started")
        self.speak_immediate("Enhanced cognitive voice monitoring active. I will speak critical insights as they emerge.")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.running = False
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
        
        if self.speech_thread:
            self.speech_thread.join(timeout=2.0)
        
        logger.info("🔇 Voice monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop for cognitive events"""
        while self.running:
            try:
                # Check tracer alerts
                if self.enable_tracer_alerts():
                    self._check_tracer_alerts()
                
                # Check symbolic roots
                if self.enable_root_speech:
                    self._check_root_events()
                
                # Check event stream
                self._check_event_stream()
                
                time.sleep(2.0)  # Check every 2 seconds
                
            except Exception as e:
                logger.error(f"Error in voice monitoring loop: {e}")
                time.sleep(5.0)
    
    def _speech_processing_loop(self):
        """Process queued speech events"""
        while self.running:
            try:
                if self.speech_queue:
                    speech_event = self.speech_queue.popleft()
                    self._speak_event(speech_event)
                else:
                    time.sleep(0.5)
                    
            except Exception as e:
                logger.error(f"Error in speech processing: {e}")
                time.sleep(1.0)
    
    def enable_tracer_alerts(self) -> bool:
        """Check if any tracer speech is enabled"""
        return (self.enable_owl_speech or self.enable_drift_speech or 
                self.enable_thermal_speech or self.enable_forecast_speech)
    
    def _check_tracer_alerts(self):
        """Check for new tracer alerts to vocalize"""
        if not self.tracer_alerts_path.exists():
            return
        
        try:
            with open(self.tracer_alerts_path, 'r', encoding='utf-8') as f:
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
    
    def _check_root_events(self):
        """Check for new symbolic root events to vocalize"""
        if not self.root_trace_path.exists():
            return
        
        try:
            with open(self.root_trace_path, 'r', encoding='utf-8') as f:
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
        """Check event stream for other cognitive events"""
        if not self.event_stream_path.exists():
            return
        
        try:
            with open(self.event_stream_path, 'r', encoding='utf-8') as f:
                f.seek(self.file_positions['event_stream'])
                
                for line in f:
                    if line.strip():
                        try:
                            event = json.loads(line.strip())
                            self._process_event_stream(event)
                        except json.JSONDecodeError:
                            continue
                
                self.file_positions['event_stream'] = f.tell()
                
        except Exception as e:
            logger.error(f"Error reading event stream: {e}")
    
    def _process_tracer_alert(self, alert: Dict[str, Any]):
        """Process and potentially vocalize a tracer alert"""
        tracer_type = alert.get('tracer_type', 'unknown')
        severity = alert.get('severity', 'info')
        message = alert.get('message', '')
        data = alert.get('data', {})
        
        # Check if this tracer type is enabled
        if not self._is_tracer_enabled(tracer_type):
            return
        
        # Skip non-critical in critical-only mode
        if self.critical_only_mode and severity not in ['warning', 'critical']:
            return
        
        # Generate speech text
        speech_text = self._generate_tracer_speech(tracer_type, message, data, severity)
        
        if speech_text:
            self._queue_speech_event(speech_text, tracer_type, severity, alert.get('tick_id'))
    
    def _process_root_event(self, root_event: Dict[str, Any]):
        """Process and potentially vocalize a symbolic root event"""
        event_type = root_event.get('type', 'unknown')
        significance = root_event.get('significance', 0.5)
        symbolic_root = root_event.get('symbolic_root', 'unknown pattern')
        
        # Only vocalize significant events
        if significance < 0.7:
            return
        
        # Generate speech text based on event type
        speech_text = ""
        tracer_type = "root"
        
        if event_type == 'MYCELIUM_EXPANSION':
            root_count = root_event.get('root_count', 0)
            density = root_event.get('network_density', 0.0)
            speech_text = f"Mycelium network expansion. {root_count} roots with density {density:.1f}"
            tracer_type = "mycelium"
        
        elif event_type == 'RHIZOME_CLUSTER':
            cluster_size = root_event.get('cluster_size', 0)
            speech_text = f"Rhizome cluster formation. {cluster_size} highly connected nodes detected"
            tracer_type = "rhizome"
        
        elif event_type == 'LINEAGE_MILESTONE':
            depth = root_event.get('lineage_depth', root_event.get('depth', 0))
            speech_text = f"Memory lineage milestone. Ancestry depth reached {depth} levels"
            tracer_type = "root"
        
        elif event_type == 'COGNITIVE_EMERGENCE':
            pattern_type = root_event.get('pattern_type', 'unknown')
            speech_text = f"Cognitive emergence detected. {pattern_type} pattern forming"
            tracer_type = "root"
        
        else:
            speech_text = f"Symbolic root formation. {symbolic_root}"
        
        if speech_text:
            self._queue_speech_event(speech_text, tracer_type, "info", root_event.get('tick'))
    
    def _process_event_stream(self, event: Dict[str, Any]):
        """Process event stream for significant cognitive events"""
        observations = event.get('observations', {})
        
        # Check for high-impact memory updates
        memory_updates = observations.get('memory_updates', {})
        for update_type, data in memory_updates.items():
            if update_type == 'mycelium_growth' and isinstance(data, dict):
                nutrients = data.get('nutrients', 0)
                if nutrients > 0.2:  # Significant growth
                    speech_text = f"Significant mycelium growth detected. Nutrient flow {nutrients:.2f}"
                    self._queue_speech_event(speech_text, "mycelium", "info", event.get('tick_id'))
        
        # Check for important forecast adjustments
        forecast_adjustments = observations.get('forecast_adjustments', [])
        for adjustment in forecast_adjustments:
            if adjustment.get('type') in ['STABILITY_INCREASE', 'UNCERTAINTY_INCREASE']:
                reason = adjustment.get('reason', 'forecast adjustment')
                if 'lineage' in reason.lower() or 'ancestry' in reason.lower():
                    speech_text = f"Forecast adjustment based on {reason.lower()}"
                    self._queue_speech_event(speech_text, "forecast", "info", event.get('tick_id'))
    
    def _generate_tracer_speech(self, tracer_type: str, message: str, 
                               data: Dict[str, Any], severity: str) -> str:
        """Generate appropriate speech text for tracer alerts"""
        speech_text = ""
        
        if tracer_type == 'owl':
            if 'DRIFT' in message.upper():
                speech_text = "Owl detects cognitive drift"
            elif 'SEMANTIC' in message.upper():
                speech_text = "Owl detects semantic anomaly"
            elif 'COHERENCE' in message.upper():
                speech_text = "Owl reports coherence shift"
            else:
                speech_text = f"Owl cognitive analysis: {message.lower()}"
        
        elif tracer_type == 'drift':
            drift_type = data.get('drift_type', 'unknown')
            magnitude = data.get('magnitude', 0.0)
            speech_text = f"Drift alert. {drift_type} deviation magnitude {magnitude:.1f}"
        
        elif tracer_type == 'thermal':
            if 'emergency' in message.lower():
                speech_text = "Thermal emergency detected"
            elif 'spike' in message.lower():
                speech_text = "Thermal spike detected"
            else:
                heat = data.get('heat_level', data.get('heat', 0))
                if heat > 0.8:
                    speech_text = f"Thermal alert. Heat level {heat:.1f}"
                else:
                    speech_text = "Thermal regulation event"
        
        elif tracer_type == 'forecast':
            if 'reliability' in message.lower():
                speech_text = "Forecast reliability degraded"
            elif 'risk' in message.lower():
                speech_text = "Forecast risk level elevated"
            else:
                speech_text = f"Forecast alert: {message.lower()}"
        
        # Add severity prefix for critical alerts
        if severity == 'critical':
            speech_text = f"Critical alert. {speech_text}"
        
        return speech_text
    
    def _is_tracer_enabled(self, tracer_type: str) -> bool:
        """Check if speech is enabled for this tracer type"""
        return {
            'owl': self.enable_owl_speech,
            'drift': self.enable_drift_speech,
            'thermal': self.enable_thermal_speech,
            'forecast': self.enable_forecast_speech
        }.get(tracer_type, False)
    
    def _queue_speech_event(self, text: str, tracer_type: str, severity: str, tick_id: Optional[int]):
        """Queue a speech event for processing"""
        # Generate message hash for deduplication
        message_hash = hashlib.md5(text.encode()).hexdigest()
        current_time = time.time()
        
        # Check for recent duplicate
        if message_hash in self.message_cache:
            if current_time - self.message_cache[message_hash] < self.deduplication_window:
                return  # Skip duplicate
        
        # Rate limiting
        if current_time - self.last_speech_time < self.speech_rate_limit:
            return  # Too soon
        
        speech_event = {
            'text': text,
            'tracer_type': tracer_type,
            'severity': severity,
            'tick_id': tick_id,
            'timestamp': current_time,
            'message_hash': message_hash
        }
        
        self.speech_queue.append(speech_event)
        self.message_cache[message_hash] = current_time
    
    def _speak_event(self, speech_event: Dict[str, Any]):
        """Speak a queued speech event"""
        text = speech_event['text']
        tracer_type = speech_event['tracer_type']
        
        # Configure voice for tracer type
        self._configure_voice_for_tracer(tracer_type)
        
        # Speak the text
        self._speak_text(text)
        
        # Log the speech event
        self.log_voice_event("TRACER_SPEECH", text, {
            'tracer_type': tracer_type,
            'severity': speech_event['severity'],
            'tick_id': speech_event['tick_id']
        })
        
        self.last_speech_time = time.time()
        logger.info(f"🗣️ DAWN: {text}")
    
    def _configure_voice_for_tracer(self, tracer_type: str):
        """Configure TTS voice properties for specific tracer type"""
        if not self.tts_engine or TTS_ENGINE != 'pyttsx3':
            return
        
        config = self.voice_configs.get(tracer_type, self.voice_configs['owl'])
        
        try:
            # Set speech rate
            self.tts_engine.setProperty('rate', config['rate'])
            
            # Set voice if multiple voices available
            voices = self.tts_engine.getProperty('voices')
            if voices and len(voices) > config['voice_id']:
                self.tts_engine.setProperty('voice', voices[config['voice_id']].id)
                
        except Exception as e:
            logger.warning(f"Error configuring voice: {e}")
    
    def _speak_text(self, text: str):
        """Speak text using available TTS engine"""
        if TTS_ENGINE == 'pyttsx3' and self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                logger.error(f"pyttsx3 speech error: {e}")
        
        elif TTS_ENGINE == 'espeak':
            try:
                subprocess.run(['espeak', text], check=False)
            except Exception as e:
                logger.error(f"espeak speech error: {e}")
        
        else:
            # Fallback to just logging
            logger.info(f"🗣️ [SPEECH] {text}")
    
    def speak_immediate(self, text: str, tracer_type: str = "system"):
        """Speak text immediately without queueing"""
        self._configure_voice_for_tracer(tracer_type)
        self._speak_text(text)
        self.log_voice_event("IMMEDIATE_SPEECH", text, {'tracer_type': tracer_type})
    
    def log_voice_event(self, event_type: str, text: str, metadata: Dict[str, Any] = None):
        """Log voice events to the voice trace log"""
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        
        log_entry = f"[{timestamp}] [COGNITIVE_VOICE] {event_type}: {text}"
        
        try:
            with open(self.voice_log_path, 'a', encoding='utf-8') as f:
                f.write(f"{log_entry}\n")
        except Exception as e:
            logger.error(f"Error writing to voice log: {e}")
    
    def get_voice_stats(self) -> Dict[str, Any]:
        """Get voice system statistics"""
        return {
            'tts_engine': TTS_ENGINE,
            'speech_queue_size': len(self.speech_queue),
            'message_cache_size': len(self.message_cache),
            'last_speech_time': self.last_speech_time,
            'running': self.running,
            'voice_configs': self.voice_configs,
            'file_positions': self.file_positions.copy(),
            'config': {
                'enable_owl_speech': self.enable_owl_speech,
                'enable_drift_speech': self.enable_drift_speech,
                'enable_thermal_speech': self.enable_thermal_speech,
                'enable_forecast_speech': self.enable_forecast_speech,
                'enable_root_speech': self.enable_root_speech,
                'critical_only_mode': self.critical_only_mode,
                'speech_rate_limit': self.speech_rate_limit,
                'deduplication_window': self.deduplication_window
            }
        }

# Global voice instance
_enhanced_voice_echo = None

def get_enhanced_voice_echo() -> EnhancedTracerEchoVoice:
    """Get or create the global enhanced voice echo"""
    global _enhanced_voice_echo
    if _enhanced_voice_echo is None:
        _enhanced_voice_echo = EnhancedTracerEchoVoice()
    return _enhanced_voice_echo

def start_enhanced_voice_monitoring():
    """Start enhanced voice monitoring"""
    echo = get_enhanced_voice_echo()
    echo.start_monitoring()

def speak_cognitive_alert(text: str, tracer_type: str = "system"):
    """Speak an immediate cognitive alert"""
    echo = get_enhanced_voice_echo()
    echo.speak_immediate(text, tracer_type)

def stop_voice_monitoring():
    """Stop voice monitoring"""
    if _enhanced_voice_echo:
        _enhanced_voice_echo.stop_monitoring()

# Demo and testing
if __name__ == "__main__":
    print("🔊 Testing Enhanced DAWN Tracer Echo Voice System")
    print("=" * 60)
    
    # Initialize enhanced voice echo
    voice_echo = EnhancedTracerEchoVoice()
    
    # Test immediate speech
    voice_echo.speak_immediate("Testing enhanced cognitive voice system", "system")
    
    # Show stats
    stats = voice_echo.get_voice_stats()
    print(f"\nEnhanced Voice Echo Stats:")
    for key, value in stats.items():
        if key != 'voice_configs':
            print(f"  {key}: {value}")
    
    # Test tracer speech
    voice_echo.speak_immediate("Owl detects semantic collapse", "owl") 
    time.sleep(2)
    voice_echo.speak_immediate("Thermal risk at critical level", "thermal")
    time.sleep(2)
    voice_echo.speak_immediate("Symbolic root formation detected", "root")
    
    print(f"\n✅ Enhanced tracer voice echo system ready!")
    print(f"🗣️ DAWN can now speak her cognitive insights with enhanced clarity!")
    
    # Optionally start monitoring
    choice = input(f"\nStart background monitoring? (y/n): ").lower().strip()
    if choice == 'y':
        voice_echo.start_monitoring()
        print(f"🎤 Background monitoring started. Press Ctrl+C to stop.")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n🛑 Stopping voice monitoring...")
            voice_echo.stop_monitoring()
            print(f"✅ Voice monitoring stopped") 