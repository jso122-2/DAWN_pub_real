# Add parent directory to Python path for imports
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Conversation Input - Speech-to-Text Module
===============================================

Real-time speech recognition for interactive conversation with DAWN.
Handles continuous listening, ambient noise calibration, and speech processing.
"""

import speech_recognition as sr
import threading
import time
import logging
from typing import Optional, Callable
from queue import Queue

logger = logging.getLogger("conversation_input")

class ConversationInput:
    """
    Speech-to-text input system for DAWN's conversational interface.
    
    Features:
    - Continuous speech recognition
    - Ambient noise calibration
    - Background listening thread
    - Speech input queue management
    - Error handling and recovery
    """
    
    def __init__(self):
        """Initialize the conversation input system"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.conversation_active = False
        self.last_input = ""
        self.input_queue = Queue()
        self.callback_function: Optional[Callable[[str], None]] = None
        
        # Speech recognition settings
        self.recognizer.energy_threshold = 4000  # Adjust for sensitivity
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Seconds of silence to end phrase
        
        # Calibrate microphone for ambient noise
        try:
            with self.microphone as source:
                logger.info("🎤 Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                logger.info("✅ Microphone calibration complete")
        except Exception as e:
            logger.warning(f"⚠️ Microphone calibration failed: {e}")
    
    def start_listening(self, callback: Optional[Callable[[str], None]] = None):
        """
        Start continuous speech recognition
        
        Args:
            callback: Optional callback function to handle recognized speech
        """
        if self.listening:
            logger.warning("🎤 Already listening")
            return
        
        self.listening = True
        self.conversation_active = True
        self.callback_function = callback
        
        logger.info("🎤 Starting speech recognition...")
        
        # Start listening in background thread
        threading.Thread(target=self._listen_loop, daemon=True, name="SpeechRecognition").start()
    
    def stop_listening(self):
        """Stop speech recognition"""
        if not self.listening:
            return
            
        self.listening = False
        self.conversation_active = False
        logger.info("🔇 Speech recognition stopped")
    
    def _listen_loop(self):
        """Main speech recognition loop"""
        logger.info("🎤 Speech recognition loop started")
        
        while self.listening:
            try:
                with self.microphone as source:
                    # Listen for speech with timeout
                    audio = self.recognizer.listen(
                        source, 
                        timeout=1, 
                        phrase_time_limit=10,
                        snowboy_configuration=None
                    )
                
                # Recognize speech using Google's service
                text = self.recognizer.recognize_google(audio)
                
                if text and text.strip():
                    text = text.strip()
                    self.last_input = text
                    self.input_queue.put(text)
                    
                    logger.info(f"🎤 Jackson: {text}")
                    
                    # Call callback if provided
                    if self.callback_function:
                        try:
                            self.callback_function(text)
                        except Exception as e:
                            logger.error(f"🎤 Callback error: {e}")
                    
            except sr.WaitTimeoutError:
                # No speech detected within timeout - continue listening
                pass
            except sr.UnknownValueError:
                # Speech was unintelligible - continue listening
                pass
            except sr.RequestError as e:
                logger.error(f"🎤 Speech recognition service error: {e}")
                time.sleep(1)  # Wait before retrying
            except Exception as e:
                logger.error(f"🎤 Speech recognition error: {e}")
                time.sleep(0.5)
            
            # Small delay to prevent CPU spinning
            time.sleep(0.1)
    
    def get_last_input(self) -> Optional[str]:
        """
        Get the last recognized speech input
        
        Returns:
            Last recognized text or None if no new input
        """
        if not self.input_queue.empty():
            return self.input_queue.get()
        return None
    
    def get_all_inputs(self) -> list:
        """
        Get all pending speech inputs
        
        Returns:
            List of all pending recognized texts
        """
        inputs = []
        while not self.input_queue.empty():
            inputs.append(self.input_queue.get())
        return inputs
    
    def is_listening(self) -> bool:
        """Check if speech recognition is active"""
        return self.listening
    
    def is_conversation_active(self) -> bool:
        """Check if conversation mode is active"""
        return self.conversation_active
    
    def adjust_sensitivity(self, energy_threshold: int = None):
        """
        Adjust speech recognition sensitivity
        
        Args:
            energy_threshold: New energy threshold (lower = more sensitive)
        """
        if energy_threshold is not None:
            self.recognizer.energy_threshold = energy_threshold
            logger.info(f"🎤 Adjusted energy threshold to {energy_threshold}")
    
    def recalibrate_microphone(self):
        """Recalibrate microphone for current ambient conditions"""
        try:
            with self.microphone as source:
                logger.info("🎤 Recalibrating microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                logger.info("✅ Microphone recalibration complete")
        except Exception as e:
            logger.error(f"🎤 Recalibration failed: {e}")
    
    def get_status(self) -> dict:
        """Get current status of the speech recognition system"""
        return {
            "listening": self.listening,
            "conversation_active": self.conversation_active,
            "energy_threshold": self.recognizer.energy_threshold,
            "dynamic_energy_threshold": self.recognizer.dynamic_energy_threshold,
            "pause_threshold": self.recognizer.pause_threshold,
            "queue_size": self.input_queue.qsize()
        } 