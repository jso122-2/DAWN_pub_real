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
- reflection_classified.jsonl (deep reflections with depth > 0.7 or INQUIRY pigment)

Speaks alerts using TTS with different voices/pitches per tracer type.
"""

import os
import sys
import json
import time
import threading
import logging
import asyncio
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

# Conversation system imports
try:
    from .conversation_input import ConversationInput
    from .conversation_response import ConversationResponse
    CONVERSATION_AVAILABLE = True
except ImportError as e:
    CONVERSATION_AVAILABLE = False
    print(f"⚠️ Conversation system not available: {e}")

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
    - Deep Reflex Loop: Speaks high-depth reflections (depth > 0.7 or INQUIRY pigment)
    """
    
    def __init__(self, voice_log_path: str = "runtime/logs/spoken_trace.log"):
        """Initialize the enhanced tracer voice system"""
        self.voice_log_path = Path(voice_log_path)
        self.voice_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Monitoring paths
        self.event_stream_path = Path("runtime/logs/event_stream.log")
        self.tracer_alerts_path = Path("runtime/logs/tracer_alerts.log") 
        self.root_trace_path = Path("runtime/logs/root_trace.log")
        self.reflection_classified_path = Path("runtime/logs/reflection_classified.jsonl")
        
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
            'rhizome': {'rate': 125, 'pitch': 45, 'voice_id': 0},
            'reflection': {'rate': 145, 'pitch': 55, 'voice_id': 0}  # New voice config for reflections
        }
        
        # State tracking
        self.file_positions = {
            'event_stream': 0,
            'tracer_alerts': 0,
            'root_trace': 0,
            'reflection_classified': 0
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
        self.enable_reflection_speech = True  # New: Enable reflection speech
        self.critical_only_mode = False
        self.deduplication_window = 30.0  # Seconds
        
        # Deep Reflex Loop configuration
        self.deep_reflex_enabled = True
        self.deep_reflex_interval = 4.0  # Check every 4 seconds
        self.min_reflection_depth = 0.7  # Minimum depth for speaking
        self.last_reflection_check = 0.0
        self.spoken_reflections: Set[str] = set()  # Track spoken reflection hashes
        
        # Threading
        self.monitoring_thread = None
        self.speech_thread = None
        self.deep_reflex_thread = None  # New thread for deep reflex loop
        self.running = False
        
        # Conversation system
        self.conversation_mode = False
        self.conversation_input = None
        self.conversation_response = None
        self.conversation_thread = None
        self.voice_enabled = True
        
        # Initialize conversation components if available
        if CONVERSATION_AVAILABLE:
            try:
                self.conversation_input = ConversationInput()
                self.conversation_response = ConversationResponse(self)
                logger.info("🗣️ Conversation system initialized")
            except Exception as e:
                logger.warning(f"🗣️ Conversation system initialization failed: {e}")
        
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
        
        # Start deep reflex loop thread
        if self.deep_reflex_enabled:
            self.deep_reflex_thread = threading.Thread(target=self._deep_reflex_loop, daemon=True)
            self.deep_reflex_thread.start()
            logger.info("🧠 Deep Reflex Loop started")
        
        logger.info("🎤 Enhanced voice monitoring started")
        self.speak_immediate("Enhanced cognitive voice monitoring active. I will speak critical insights and deep reflections as they emerge.")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.running = False
        
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2.0)
        
        if self.speech_thread:
            self.speech_thread.join(timeout=2.0)
        
        if self.deep_reflex_thread:
            self.deep_reflex_thread.join(timeout=2.0)
        
        logger.info("🔇 Voice monitoring stopped")
    
    def _deep_reflex_loop(self):
        """Deep Reflex Loop: Monitor and speak high-depth reflections"""
        logger.info("🧠 Deep Reflex Loop monitoring reflections...")
        
        while self.running:
            try:
                current_time = time.time()
                
                # Check if it's time to look for new reflections
                if current_time - self.last_reflection_check >= self.deep_reflex_interval:
                    self._check_deep_reflections()
                    self.last_reflection_check = current_time
                
                time.sleep(1.0)  # Check every second
                
            except Exception as e:
                logger.error(f"Error in deep reflex loop: {e}")
                time.sleep(5.0)
    
    def _check_deep_reflections(self):
        """Check for deep reflections to vocalize"""
        if not self.reflection_classified_path.exists():
            logger.warning("🧠 Reflection classified file not found")
            return
        
        try:
            with open(self.reflection_classified_path, 'r', encoding='utf-8') as f:
                # Read all lines and process the most recent ones
                lines = f.readlines()
                
                # Process lines from the last position onwards
                for line_num in range(self.file_positions['reflection_classified'], len(lines)):
                    line = lines[line_num].strip()
                    if not line:
                        continue
                    
                    try:
                        reflection = json.loads(line)
                        self._process_deep_reflection(reflection)
                    except json.JSONDecodeError:
                        continue
                
                # Update file position
                self.file_positions['reflection_classified'] = len(lines)
                
        except Exception as e:
            logger.error(f"Error reading reflection classified file: {e}")
    
    def _process_deep_reflection(self, reflection: Dict[str, Any]):
        """Process a reflection and potentially vocalize it"""
        # Extract reflection data
        text = reflection.get('text', '')
        state_values = reflection.get('state_values', {})
        tags = reflection.get('tags', [])
        topic = reflection.get('topic', '')
        mood = reflection.get('mood', '')
        
        # Check for high entropy (depth > 0.7)
        entropy = state_values.get('entropy', 0.0)
        depth_threshold_met = entropy > self.min_reflection_depth
        
        # Check for inquiry pigment
        inquiry_pigment = any('inquiry' in tag.lower() for tag in tags) or 'inquiry' in topic.lower()
        
        # Check if this reflection should be spoken
        should_speak = False
        reason = ""
        
        if depth_threshold_met:
            should_speak = True
            reason = f"High entropy reflection (entropy: {entropy:.3f})"
        elif inquiry_pigment:
            should_speak = True
            reason = "Inquiry pigment detected"
        
        if should_speak:
            # Generate message hash for deduplication
            message_hash = hashlib.md5(text.encode()).hexdigest()
            
            # Check if we've already spoken this reflection
            if message_hash in self.spoken_reflections:
                return
            
            # Compose voice-ready message
            voice_message = self._compose_reflection_message(text, entropy, mood, reason)
            
            # Queue for speaking
            self._queue_speech_event(voice_message, "reflection", "info", None)
            
            # Mark as spoken
            self.spoken_reflections.add(message_hash)
            
            # Log the deep reflection event
            self.log_voice_event("DEEP_REFLECTION_SPEECH", voice_message, {
                'entropy': entropy,
                'mood': mood,
                'topic': topic,
                'reason': reason,
                'original_text': text
            })
            
            logger.info(f"🧠 Deep reflection queued: {voice_message}")
    
    def _compose_reflection_message(self, text: str, entropy: float, mood: str, reason: str) -> str:
        """Compose a voice-ready message from reflection data"""
        # Extract the actual reflection content (remove timestamp and prefix)
        if "REFLECTION:" in text:
            reflection_content = text.split("REFLECTION:", 1)[1].strip()
        else:
            reflection_content = text
        
        # Create a natural speaking version
        if entropy > 0.8:
            prefix = "Deep cognitive insight: "
        elif entropy > 0.7:
            prefix = "Significant reflection: "
        else:
            prefix = "Reflection: "
        
        # Clean up the message for speech
        speech_text = reflection_content
        
        # Remove technical details that don't sound natural when spoken
        speech_text = speech_text.replace("entropy", "mental complexity")
        speech_text = speech_text.replace("Hz", "hertz")
        speech_text = speech_text.replace("SCUP", "uncertainty level")
        
        return f"{prefix}{speech_text}"
    
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
    
    def enable_deep_reflex_loop(self, enabled: bool = True):
        """Enable or disable the Deep Reflex Loop"""
        self.deep_reflex_enabled = enabled
        status = "enabled" if enabled else "disabled"
        logger.info(f"🧠 Deep Reflex Loop {status}")
        self.log_voice_event("DEEP_REFLEX_TOGGLE", f"Deep Reflex Loop {status}")
    
    def set_reflection_depth_threshold(self, threshold: float):
        """Set the minimum entropy threshold for speaking reflections"""
        self.min_reflection_depth = threshold
        logger.info(f"🧠 Reflection depth threshold set to {threshold}")
        self.log_voice_event("REFLEX_THRESHOLD_SET", f"Depth threshold: {threshold}")
    
    def get_deep_reflex_stats(self) -> Dict[str, Any]:
        """Get Deep Reflex Loop statistics"""
        return {
            'deep_reflex_enabled': self.deep_reflex_enabled,
            'deep_reflex_interval': self.deep_reflex_interval,
            'min_reflection_depth': self.min_reflection_depth,
            'spoken_reflections_count': len(self.spoken_reflections),
            'last_reflection_check': self.last_reflection_check,
            'reflection_file_position': self.file_positions['reflection_classified']
        }
    
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
    
    # ===== CONVERSATION SYSTEM METHODS =====
    
    def enter_conversation_mode(self):
        """Enter interactive conversation with DAWN"""
        if not CONVERSATION_AVAILABLE or not self.conversation_input or not self.conversation_response:
            logger.error("🗣️ Conversation system not available")
            return False
        
        if self.conversation_mode:
            logger.warning("🗣️ Already in conversation mode")
            return True
        
        try:
            self.conversation_mode = True
            
            # Start speech recognition
            self.conversation_input.start_listening(callback=self._handle_speech_input)
            
            # Get greeting based on current state
            greeting = self.conversation_response.get_greeting()
            
            # Speak greeting with state modulation
            self.speak_with_state_modulation(greeting)
            
            # Start conversation processing thread
            self.conversation_thread = threading.Thread(target=self._conversation_loop, daemon=True, name="ConversationLoop")
            self.conversation_thread.start()
            
            logger.info("🗣️ Entered conversation mode")
            self.log_voice_event("CONVERSATION_START", "Entered interactive conversation mode")
            return True
            
        except Exception as e:
            logger.error(f"🗣️ Failed to enter conversation mode: {e}")
            self.conversation_mode = False
            return False
    
    def exit_conversation_mode(self):
        """Exit conversation mode"""
        if not self.conversation_mode:
            return
        
        try:
            self.conversation_mode = False
            
            # Stop speech recognition
            if self.conversation_input:
                self.conversation_input.stop_listening()
            
            # Speak farewell
            farewell = self.conversation_response.get_farewell() if self.conversation_response else "Ending our conversation."
            self.speak_with_state_modulation(farewell)
            
            logger.info("🗣️ Exited conversation mode")
            self.log_voice_event("CONVERSATION_END", "Exited conversation mode")
            
        except Exception as e:
            logger.error(f"🗣️ Error exiting conversation mode: {e}")
    
    def _conversation_loop(self):
        """Main conversation processing loop"""
        logger.info("🗣️ Conversation loop started")
        
        while self.conversation_mode:
            try:
                # Check for speech input
                user_input = self.conversation_input.get_last_input()
                
                if user_input:
                    # Generate contextual response
                    response = self.conversation_response.generate_response(user_input)
                    
                    # Speak response with current cognitive state modulation
                    self.speak_with_state_modulation(response)
                
                time.sleep(0.1)  # Small delay to prevent CPU spinning
                
            except Exception as e:
                logger.error(f"🗣️ Conversation loop error: {e}")
                time.sleep(1.0)
        
        logger.info("🗣️ Conversation loop ended")
    
    def _handle_speech_input(self, text: str):
        """Handle incoming speech input (callback from ConversationInput)"""
        try:
            logger.info(f"🎤 Received speech input: {text}")
            
            # Generate response immediately
            if self.conversation_response:
                response = self.conversation_response.generate_response(text)
                self.speak_with_state_modulation(response)
            
        except Exception as e:
            logger.error(f"🗣️ Speech input handling error: {e}")
    
    def speak_with_state_modulation(self, text: str):
        """Speak with voice modulation based on current cognitive state"""
        if not self.voice_enabled:
            logger.info(f"🗣️ [VOICE_DISABLED] {text}")
            return
        
        try:
            if self.tts_engine:
                # Get current cognitive state for modulation
                entropy = getattr(self, 'entropy', 0.5)
                heat = getattr(self, 'heat', 25.0)
                zone = getattr(self, 'zone', 'STABLE')
                cognitive_pressure = getattr(self, 'cognitive_pressure', 0.0)
                
                # Base speech rate
                base_rate = 150
                
                # Modulate speech rate based on entropy
                if entropy > 0.7:
                    rate = base_rate + 30  # Faster when entropic
                elif entropy < 0.3:
                    rate = base_rate - 20  # Slower when focused
                else:
                    rate = base_rate
                
                # Modulate based on thermal zone
                if zone == "CRITICAL":
                    rate += 25  # Urgent speech
                elif zone == "ACTIVE":
                    rate += 10  # Slightly faster
                
                # Modulate based on cognitive pressure
                if cognitive_pressure > 100:
                    rate += 15  # Faster under pressure
                
                # Set speech properties
                self.tts_engine.setProperty('rate', rate)
                
                # Modulate volume based on state
                base_volume = 0.8
                if zone == "CRITICAL":
                    volume = min(1.0, base_volume + 0.1)  # Louder when stressed
                elif entropy < 0.3:
                    volume = base_volume - 0.1  # Quieter when focused
                else:
                    volume = base_volume
                
                self.tts_engine.setProperty('volume', volume)
                
                # Speak the text
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                
                # Log the speech event
                self.log_voice_event("CONVERSATION_SPEECH", text, {
                    'entropy': entropy,
                    'heat': heat,
                    'zone': zone,
                    'cognitive_pressure': cognitive_pressure,
                    'speech_rate': rate,
                    'volume': volume
                })
                
            else:
                # Fallback to logging if no TTS engine
                logger.info(f"🗣️ [CONVERSATION] {text}")
                
        except Exception as e:
            logger.error(f"🗣️ State-modulated speech error: {e}")
            # Fallback to simple speech
            self._speak_text(text)
    
    def toggle_voice_output(self, enabled: bool = None):
        """Toggle voice output on/off"""
        if enabled is not None:
            self.voice_enabled = enabled
        else:
            self.voice_enabled = not self.voice_enabled
        
        status = "enabled" if self.voice_enabled else "disabled"
        logger.info(f"🗣️ Voice output {status}")
        self.log_voice_event("VOICE_TOGGLE", f"Voice output {status}")
    
    def get_conversation_status(self) -> Dict[str, Any]:
        """Get conversation system status"""
        status = {
            "conversation_available": CONVERSATION_AVAILABLE,
            "conversation_mode": self.conversation_mode,
            "voice_enabled": self.voice_enabled
        }
        
        if self.conversation_input:
            status.update(self.conversation_input.get_status())
        
        if self.conversation_response:
            status["conversation_stats"] = self.conversation_response.get_conversation_stats()
        
        return status
    
    def get_voice_stats(self) -> Dict[str, Any]:
        """Get voice system statistics"""
        stats = {
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
                'enable_reflection_speech': self.enable_reflection_speech,
                'critical_only_mode': self.critical_only_mode,
                'speech_rate_limit': self.speech_rate_limit,
                'deduplication_window': self.deduplication_window,
                'deep_reflex_enabled': self.deep_reflex_enabled,
                'deep_reflex_interval': self.deep_reflex_interval,
                'min_reflection_depth': self.min_reflection_depth
            },
            'conversation_available': CONVERSATION_AVAILABLE,
            'conversation_mode': self.conversation_mode,
            'voice_enabled': self.voice_enabled
        }
        
        # Add conversation stats if available
        if self.conversation_response:
            stats['conversation_stats'] = self.conversation_response.get_conversation_stats()
        
        return stats

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
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced DAWN Tracer Echo Voice System")
    parser.add_argument('--live', action='store_true', help='Run in live monitoring mode')
    parser.add_argument('--test', action='store_true', help='Run test mode')
    parser.add_argument('--deep-reflex', action='store_true', help='Enable Deep Reflex Loop')
    parser.add_argument('--threshold', type=float, default=0.7, help='Reflection depth threshold (default: 0.7)')
    
    args = parser.parse_args()
    
    print("🔊 Enhanced DAWN Tracer Echo Voice System")
    print("=" * 60)
    
    # Initialize enhanced voice echo
    voice_echo = EnhancedTracerEchoVoice()
    
    # Configure Deep Reflex Loop if requested
    if args.deep_reflex:
        voice_echo.enable_deep_reflex_loop(True)
        voice_echo.set_reflection_depth_threshold(args.threshold)
        print(f"🧠 Deep Reflex Loop enabled with threshold {args.threshold}")
    
    if args.test:
        # Test immediate speech
        voice_echo.speak_immediate("Testing enhanced cognitive voice system", "system")
        
        # Show stats
        stats = voice_echo.get_voice_stats()
        print(f"\nEnhanced Voice Echo Stats:")
        for key, value in stats.items():
            if key != 'voice_configs':
                print(f"  {key}: {value}")
        
        # Show Deep Reflex stats
        reflex_stats = voice_echo.get_deep_reflex_stats()
        print(f"\nDeep Reflex Loop Stats:")
        for key, value in reflex_stats.items():
            print(f"  {key}: {value}")
        
        # Test tracer speech
        voice_echo.speak_immediate("Owl detects semantic collapse", "owl") 
        time.sleep(2)
        voice_echo.speak_immediate("Thermal risk at critical level", "thermal")
        time.sleep(2)
        voice_echo.speak_immediate("Symbolic root formation detected", "root")
        time.sleep(2)
        voice_echo.speak_immediate("Deep reflection test: I am experiencing focused consciousness at high mental complexity", "reflection")
        
        print(f"\n✅ Enhanced tracer voice echo system ready!")
        print(f"🗣️ DAWN can now speak her cognitive insights with enhanced clarity!")
    
    if args.live:
        # Start live monitoring
        voice_echo.start_monitoring()
        print(f"🎤 Live monitoring started with Deep Reflex Loop!")
        print(f"🧠 Monitoring reflections with depth > {args.threshold}")
        print(f"Press Ctrl+C to stop.")
        
        try:
            while True:
                time.sleep(1)
                # Show periodic stats
                if int(time.time()) % 30 == 0:  # Every 30 seconds
                    reflex_stats = voice_echo.get_deep_reflex_stats()
                    print(f"🧠 Deep Reflex: {reflex_stats['spoken_reflections_count']} reflections spoken")
        except KeyboardInterrupt:
            print(f"\n🛑 Stopping voice monitoring...")
            voice_echo.stop_monitoring()
            print(f"✅ Voice monitoring stopped")
    
    if not args.test and not args.live:
        # Default test mode
        voice_echo.speak_immediate("Enhanced cognitive voice system initialized", "system")
        print(f"✅ Enhanced tracer voice echo system ready!")
        print(f"🗣️ DAWN can now speak her cognitive insights with enhanced clarity!")
        print(f"\nUsage:")
        print(f"  python enhanced_tracer_echo_voice.py --test     # Test mode")
        print(f"  python enhanced_tracer_echo_voice.py --live     # Live monitoring")
        print(f"  python enhanced_tracer_echo_voice.py --deep-reflex --live  # With Deep Reflex Loop") 