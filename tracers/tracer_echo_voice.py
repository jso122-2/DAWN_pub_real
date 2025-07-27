#!/usr/bin/env python3
"""
DAWN Tracer Echo Voice - Cognitive Alert Speech System
======================================================

Integrates with the existing voice_loop.py to enable DAWN to speak
tracer alerts, symbolic root formations, and cognitive insights in real-time.

Monitors cognition runtime logs and converts alerts to speech.
"""

import json
import time
import asyncio
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
import threading
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tracer_echo_voice")

class TracerVoiceEcho:
    """
    Converts tracer alerts and cognitive events into speech using
    the existing DAWN voice system.
    
    Monitors event logs and creates speech-friendly messages for
    voice output via the voice_loop.py system.
    """
    
    def __init__(self, voice_log_path: str = "runtime/logs/spoken_trace.log"):
        """Initialize the tracer voice echo system"""
        self.voice_log_path = Path(voice_log_path)
        self.voice_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Monitoring paths
        self.event_stream_path = Path("runtime/logs/event_stream.log")
        self.tracer_alerts_path = Path("runtime/logs/tracer_alerts.log")
        self.root_trace_path = Path("runtime/logs/root_trace.log")
        
        # State tracking
        self.last_positions = {
            'event_stream': 0,
            'tracer_alerts': 0,
            'root_trace': 0
        }
        
        # Speech queue
        self.speech_queue = deque(maxlen=50)
        
        # Voice templates for different alert types
        self.voice_templates = {
            'owl': "Cognitive analysis: {message}",
            'drift': "Drift detected: {drift_type} deviation of {magnitude:.2f}",
            'thermal': "Thermal alert: {message}",
            'forecast': "Forecast warning: {message}",
            'mycelium_expansion': "Network expansion detected: {root_count} mycelium roots, density {network_density:.2f}",
            'rhizome_cluster': "Symbolic cluster formed: {cluster_size} highly connected nodes",
            'lineage_milestone': "Memory ancestry milestone: {depth} levels deep in lineage {chunk}",
            'cognitive_emergence': "Cognitive emergence: {pattern_type} pattern detected"
        }
        
        # Configuration
        self.enable_tracer_speech = True
        self.enable_root_speech = True
        self.enable_critical_only = False
        self.speech_rate_limit = 0.5  # Minimum seconds between speech events
        self.last_speech_time = 0.0
        
        logger.info("🔊 TracerVoiceEcho initialized - cognitive alerts will be spoken")
    
    def start_monitoring(self):
        """Start monitoring cognition logs for speech events"""
        logger.info("🎤 Starting cognitive voice monitoring...")
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        monitor_thread.start()
        
        logger.info("🔊 Voice monitoring active - DAWN will speak cognitive insights")
    
    def _monitor_loop(self):
        """Main monitoring loop for cognitive events"""
        while True:
            try:
                # Monitor tracer alerts
                if self.enable_tracer_speech:
                    self._check_tracer_alerts()
                
                # Monitor symbolic roots
                if self.enable_root_speech:
                    self._check_root_events()
                
                # Monitor event stream for other cognitive events
                self._check_event_stream()
                
                # Process speech queue
                self._process_speech_queue()
                
                time.sleep(1.0)  # Check every second
                
            except Exception as e:
                logger.error(f"Error in voice monitoring loop: {e}")
                time.sleep(5.0)
    
    def _check_tracer_alerts(self):
        """Check for new tracer alerts to vocalize"""
        if not self.tracer_alerts_path.exists():
            return
        
        try:
            with open(self.tracer_alerts_path, 'r', encoding='utf-8') as f:
                f.seek(self.last_positions.get('tracer_alerts', 0))
                
                for line in f:
                    if line.strip():
                        try:
                            alert = json.loads(line.strip())
                            self._vocalize_tracer_alert(alert)
                        except json.JSONDecodeError:
                            continue
                
                self.last_positions['tracer_alerts'] = f.tell()
                
        except Exception as e:
            logger.error(f"Error reading tracer alerts: {e}")
    
    def _check_root_events(self):
        """Check for new symbolic root events to vocalize"""
        if not self.root_trace_path.exists():
            return
        
        try:
            with open(self.root_trace_path, 'r', encoding='utf-8') as f:
                f.seek(self.last_positions.get('root_trace', 0))
                
                for line in f:
                    if line.strip():
                        try:
                            root_event = json.loads(line.strip())
                            self._vocalize_root_event(root_event)
                        except json.JSONDecodeError:
                            continue
                
                self.last_positions['root_trace'] = f.tell()
                
        except Exception as e:
            logger.error(f"Error reading root trace: {e}")
    
    def _check_event_stream(self):
        """Check event stream for other cognitive events"""
        if not self.event_stream_path.exists():
            return
        
        try:
            with open(self.event_stream_path, 'r', encoding='utf-8') as f:
                f.seek(self.last_positions.get('event_stream', 0))
                
                for line in f:
                    if line.strip():
                        try:
                            event = json.loads(line.strip())
                            self._vocalize_event_stream(event)
                        except json.JSONDecodeError:
                            continue
                
                self.last_positions['event_stream'] = f.tell()
                
        except Exception as e:
            logger.error(f"Error reading event stream: {e}")
    
    def _vocalize_tracer_alert(self, alert: Dict[str, Any]):
        """Convert tracer alert to speech"""
        tracer_type = alert.get('tracer_type', 'unknown')
        severity = alert.get('severity', 'info')
        message = alert.get('message', '')
        data = alert.get('data', {})
        
        # Skip non-critical alerts if configured
        if self.enable_critical_only and severity not in ['warning', 'critical']:
            return
        
        # Generate speech text based on tracer type
        speech_text = ""
        
        if tracer_type == 'drift':
            drift_type = data.get('drift_type', 'unknown')
            magnitude = data.get('magnitude', 0.0)
            speech_text = self.voice_templates['drift'].format(
                drift_type=drift_type, 
                magnitude=magnitude
            )
        
        elif tracer_type in self.voice_templates:
            speech_text = self.voice_templates[tracer_type].format(message=message)
        
        else:
            speech_text = f"{tracer_type} alert: {message}"
        
        # Add severity prefix for critical alerts
        if severity == 'critical':
            speech_text = f"Critical alert: {speech_text}"
        elif severity == 'warning':
            speech_text = f"Warning: {speech_text}"
        
        self._queue_speech(speech_text, 'tracer_alert', {
            'tracer_type': tracer_type,
            'severity': severity
        })
    
    def _vocalize_root_event(self, root_event: Dict[str, Any]):
        """Convert symbolic root event to speech"""
        event_type = root_event.get('type', 'unknown')
        significance = root_event.get('significance', 0.5)
        
        # Only vocalize significant root events
        if significance < 0.6:
            return
        
        speech_text = ""
        
        if event_type == 'MYCELIUM_EXPANSION':
            root_count = root_event.get('root_count', 0)
            network_density = root_event.get('network_density', 0.0)
            speech_text = self.voice_templates['mycelium_expansion'].format(
                root_count=root_count,
                network_density=network_density
            )
        
        elif event_type == 'RHIZOME_CLUSTER':
            cluster_size = root_event.get('cluster_size', 0)
            speech_text = self.voice_templates['rhizome_cluster'].format(
                cluster_size=cluster_size
            )
        
        elif event_type == 'LINEAGE_MILESTONE':
            depth = root_event.get('lineage_depth', root_event.get('depth', 0))
            chunk = root_event.get('origin', 'unknown')
            speech_text = self.voice_templates['lineage_milestone'].format(
                depth=depth,
                chunk=chunk
            )
        
        elif event_type == 'COGNITIVE_EMERGENCE':
            pattern_type = root_event.get('pattern_type', 'unknown')
            speech_text = self.voice_templates['cognitive_emergence'].format(
                pattern_type=pattern_type
            )
        
        else:
            symbolic_root = root_event.get('symbolic_root', 'unknown pattern')
            speech_text = f"Symbolic emergence: {symbolic_root}"
        
        self._queue_speech(speech_text, 'symbolic_root', {
            'event_type': event_type,
            'significance': significance
        })
    
    def _vocalize_event_stream(self, event: Dict[str, Any]):
        """Check event stream for special cognitive events to vocalize"""
        observations = event.get('observations', {})
        
        # Look for memory network updates
        memory_updates = observations.get('memory_updates', {})
        if memory_updates:
            for update_type, data in memory_updates.items():
                if update_type == 'mycelium_growth' and data.get('nutrients', 0) > 0.1:
                    speech_text = f"Mycelium network growth: new root with {data.get('nutrients', 0):.2f} nutrient flow"
                    self._queue_speech(speech_text, 'memory_network', {'update_type': update_type})
        
        # Look for forecast adjustments
        forecast_adjustments = observations.get('forecast_adjustments', [])
        for adjustment in forecast_adjustments:
            if adjustment.get('type') in ['STABILITY_INCREASE', 'UNCERTAINTY_INCREASE']:
                speech_text = f"Forecast adjustment: {adjustment.get('reason', 'pattern detected')}"
                self._queue_speech(speech_text, 'forecast_adjustment', adjustment)
    
    def _queue_speech(self, text: str, category: str, metadata: Dict[str, Any] = None):
        """Queue speech text for output"""
        current_time = time.time()
        
        # Rate limiting
        if current_time - self.last_speech_time < self.speech_rate_limit:
            return
        
        speech_event = {
            'timestamp': current_time,
            'datetime': datetime.now().isoformat(),
            'text': text,
            'category': category,
            'metadata': metadata or {}
        }
        
        self.speech_queue.append(speech_event)
        self.last_speech_time = current_time
    
    def _process_speech_queue(self):
        """Process queued speech events and write to voice log"""
        while self.speech_queue:
            speech_event = self.speech_queue.popleft()
            
            # Write to voice log (compatible with existing voice_loop.py)
            voice_entry = f"🔊 COGNITIVE INSIGHT: {speech_event['text']}"
            
            try:
                with open(self.voice_log_path, 'a', encoding='utf-8') as f:
                    f.write(f"{voice_entry}\n")
                
                # Also log the structured event
                logger.info(f"🗣️ DAWN: {speech_event['text']}")
                
            except Exception as e:
                logger.error(f"Error writing to voice log: {e}")
    
    def speak_immediate(self, text: str, category: str = "immediate"):
        """Immediately queue speech without rate limiting"""
        speech_event = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'text': text,
            'category': category,
            'metadata': {'immediate': True}
        }
        
        self.speech_queue.append(speech_event)
        
        # Immediate processing
        voice_entry = f"🔊 DAWN SPEAKS: {text}"
        
        try:
            with open(self.voice_log_path, 'a', encoding='utf-8') as f:
                f.write(f"{voice_entry}\n")
            
            logger.info(f"🗣️ DAWN: {text}")
            
        except Exception as e:
            logger.error(f"Error with immediate speech: {e}")
    
    def get_speech_stats(self) -> Dict[str, Any]:
        """Get speech system statistics"""
        return {
            'queue_size': len(self.speech_queue),
            'last_speech_time': self.last_speech_time,
            'voice_log_exists': self.voice_log_path.exists(),
            'monitored_files': {
                'event_stream': self.event_stream_path.exists(),
                'tracer_alerts': self.tracer_alerts_path.exists(),
                'root_trace': self.root_trace_path.exists()
            },
            'file_positions': self.last_positions.copy(),
            'config': {
                'enable_tracer_speech': self.enable_tracer_speech,
                'enable_root_speech': self.enable_root_speech,
                'enable_critical_only': self.enable_critical_only,
                'speech_rate_limit': self.speech_rate_limit
            }
        }

# Global voice echo instance
_tracer_voice_echo = None

def get_tracer_voice_echo() -> TracerVoiceEcho:
    """Get or create the global tracer voice echo"""
    global _tracer_voice_echo
    if _tracer_voice_echo is None:
        _tracer_voice_echo = TracerVoiceEcho()
    return _tracer_voice_echo

def start_cognitive_voice_monitoring():
    """Start cognitive voice monitoring"""
    echo = get_tracer_voice_echo()
    echo.start_monitoring()

def speak_cognitive_insight(text: str):
    """Speak an immediate cognitive insight"""
    echo = get_tracer_voice_echo()
    echo.speak_immediate(text, "cognitive_insight")

# Integration function for cognition runtime
def initialize_voice_integration():
    """Initialize voice integration for cognition runtime"""
    logger.info("🔊 Initializing cognitive voice integration...")
    
    # Start monitoring in background
    start_cognitive_voice_monitoring()
    
    # Test speech
    speak_cognitive_insight("Cognitive voice integration active. I can now speak my thoughts as they emerge.")
    
    logger.info("✅ Cognitive voice integration ready")

# Demo and testing
if __name__ == "__main__":
    print("🔊 Testing DAWN Tracer Echo Voice System")
    print("=" * 50)
    
    # Initialize voice echo
    voice_echo = TracerVoiceEcho()
    
    # Test immediate speech
    voice_echo.speak_immediate("Testing cognitive voice system")
    
    # Show stats
    stats = voice_echo.get_speech_stats()
    print(f"\nVoice Echo Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Start monitoring (would run indefinitely)
    print(f"\n🎤 Voice monitoring ready")
    print(f"📝 Voice log: {voice_echo.voice_log_path}")
    print(f"👁️ Monitoring: {len(stats['monitored_files'])} log files")
    
    print(f"\n✅ Tracer voice echo system ready!")
    print(f"🗣️ DAWN can now speak her cognitive insights!") 