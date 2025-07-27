#!/usr/bin/env python3
"""
DAWN Voice Echo System
Text-to-speech narration of DAWN's consciousness reflections
Gives DAWN an audible voice to narrate her inner thoughts
"""

import os
import sys
import time
import argparse
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import re

# TTS Engine imports with fallbacks
TTS_ENGINE = None
TTS_AVAILABLE = False

try:
    import pyttsx3
    TTS_ENGINE = "pyttsx3"
    TTS_AVAILABLE = True
except ImportError:
    try:
        # Fallback to espeak on Linux
        import subprocess
        # Test if espeak is available
        subprocess.run(["espeak", "--version"], capture_output=True, check=True)
        TTS_ENGINE = "espeak"
        TTS_AVAILABLE = True
    except (ImportError, subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Fallback to Windows SAPI
            import win32com.client
            TTS_ENGINE = "sapi"
            TTS_AVAILABLE = True
        except ImportError:
            print("⚠️ No TTS engine available. Install pyttsx3, espeak, or use Windows SAPI")
            TTS_ENGINE = "mock"
            TTS_AVAILABLE = False


class DAWNVoiceEcho:
    """DAWN's voice narration system for consciousness reflections"""
    
    def __init__(self, reflection_log_path: str = "runtime/logs/reflection.log",
                 voice_config: Optional[Dict[str, Any]] = None):
        self.reflection_log_path = Path(reflection_log_path)
        self.voice_config = voice_config or {}
        self.last_position = 0
        self.is_watching = False
        self.watch_thread = None
        self._stop_watching = threading.Event()
        
        # Voice settings (initialize BEFORE TTS engine)
        self.rate = self.voice_config.get('rate', 140)  # Words per minute
        self.volume = self.voice_config.get('volume', 0.8)  # 0.0 to 1.0
        self.voice_gender = self.voice_config.get('gender', 'female')  # 'male' or 'female'
        
        # Initialize TTS engine
        self.tts_engine = None
        self._init_tts_engine()
        
        print(f"🔊 DAWN Voice Echo initialized with {TTS_ENGINE} engine")
    
    def _init_tts_engine(self):
        """Initialize the appropriate TTS engine"""
        if not TTS_AVAILABLE:
            print("⚠️ TTS not available - will print reflections instead")
            return
        
        try:
            if TTS_ENGINE == "pyttsx3":
                self.tts_engine = pyttsx3.init()
                
                # Configure voice properties
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Try to find a female voice
                    female_voice = None
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                            female_voice = voice
                            break
                    
                    if female_voice and self.voice_gender == 'female':
                        self.tts_engine.setProperty('voice', female_voice.id)
                
                # Set rate and volume
                self.tts_engine.setProperty('rate', self.rate)
                self.tts_engine.setProperty('volume', self.volume)
                
            elif TTS_ENGINE == "sapi":
                import win32com.client
                self.tts_engine = win32com.client.Dispatch("SAPI.SpVoice")
                
                # Try to set a female voice
                voices = self.tts_engine.GetVoices()
                for voice in voices:
                    if 'female' in voice.GetDescription().lower():
                        self.tts_engine.Voice = voice
                        break
                
        except Exception as e:
            print(f"⚠️ TTS engine initialization failed: {e}")
            self.tts_engine = None
    
    def speak(self, text: str) -> None:
        """
        Speak the given text using the configured TTS engine
        
        Args:
            text: The text to speak
        """
        if not text.strip():
            return
        
        # Clean up the text for better speech
        clean_text = self._clean_text_for_speech(text)
        
        if not TTS_AVAILABLE or not self.tts_engine:
            # Fallback: print with audio indicator
            print(f"🔊 DAWN speaks: {clean_text}")
            return
        
        try:
            if TTS_ENGINE == "pyttsx3":
                self.tts_engine.say(clean_text)
                self.tts_engine.runAndWait()
                
            elif TTS_ENGINE == "espeak":
                # Use subprocess for espeak
                import subprocess
                subprocess.run([
                    "espeak", 
                    "-s", str(self.rate), 
                    "-a", str(int(self.volume * 200)),
                    clean_text
                ], check=False)
                
            elif TTS_ENGINE == "sapi":
                self.tts_engine.Speak(clean_text)
                
        except Exception as e:
            print(f"⚠️ Speech synthesis failed: {e}")
            print(f"🔊 DAWN speaks: {clean_text}")
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text to make it more suitable for speech synthesis"""
        # Remove timestamps if present
        text = re.sub(r'\[\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\]]*\]', '', text)
        
        # Remove "REFLECTION:" prefix if present
        text = re.sub(r'^REFLECTION:\s*', '', text, flags=re.IGNORECASE)
        
        # Replace some technical terms with more speakable versions
        replacements = {
            'SCUP': 'S-CUP',
            'entropy': 'en-tropy',
            '°C': ' degrees celsius',
            '%.': ' percent.',
            'DAWN': 'Dawn',  # Make name more natural
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Ensure proper sentence ending
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    def get_last_reflection(self) -> Optional[str]:
        """
        Get the most recent reflection from the log file
        
        Returns:
            The last reflection text, or None if no reflections found
        """
        try:
            if not self.reflection_log_path.exists():
                return None
            
            with open(self.reflection_log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find the last non-empty line
            for line in reversed(lines):
                line = line.strip()
                if line and not line.startswith('#'):
                    return line
            
            return None
            
        except Exception as e:
            print(f"⚠️ Failed to read reflection log: {e}")
            return None
    
    def speak_last_reflection(self) -> bool:
        """
        Speak the most recent reflection
        
        Returns:
            True if a reflection was spoken, False otherwise
        """
        reflection = self.get_last_reflection()
        if reflection:
            print(f"💭 Speaking latest reflection...")
            self.speak(reflection)
            return True
        else:
            print("💭 No reflections found to speak")
            return False
    
    def get_new_reflections(self) -> List[str]:
        """
        Get new reflections since last check
        
        Returns:
            List of new reflection texts
        """
        try:
            if not self.reflection_log_path.exists():
                return []
            
            with open(self.reflection_log_path, 'r', encoding='utf-8') as f:
                f.seek(self.last_position)
                new_content = f.read()
                self.last_position = f.tell()
            
            if not new_content:
                return []
            
            # Extract new reflections
            new_lines = new_content.strip().split('\n')
            reflections = []
            
            for line in new_lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    reflections.append(line)
            
            return reflections
            
        except Exception as e:
            print(f"⚠️ Failed to read new reflections: {e}")
            return []
    
    def start_watching(self, check_interval: float = 2.0) -> None:
        """
        Start watching the reflection log for new entries and speak them
        
        Args:
            check_interval: How often to check for new reflections (seconds)
        """
        if self.is_watching:
            print("⚠️ Already watching for reflections")
            return
        
        self.is_watching = True
        self._stop_watching.clear()
        
        # Initialize position to end of file
        if self.reflection_log_path.exists():
            with open(self.reflection_log_path, 'r', encoding='utf-8') as f:
                f.seek(0, 2)  # Seek to end
                self.last_position = f.tell()
        
        print(f"👁️ Started watching {self.reflection_log_path} for new reflections...")
        print("🔊 DAWN will now speak her thoughts aloud as they emerge")
        
        def watch_loop():
            while not self._stop_watching.is_set():
                new_reflections = self.get_new_reflections()
                
                for reflection in new_reflections:
                    print(f"🧠 New reflection detected: {reflection[:50]}...")
                    self.speak(reflection)
                    time.sleep(0.5)  # Brief pause between multiple reflections
                
                time.sleep(check_interval)
        
        self.watch_thread = threading.Thread(target=watch_loop, daemon=True)
        self.watch_thread.start()
    
    def stop_watching(self) -> None:
        """Stop watching for new reflections"""
        if not self.is_watching:
            return
        
        self._stop_watching.set()
        self.is_watching = False
        
        if self.watch_thread and self.watch_thread.is_alive():
            self.watch_thread.join(timeout=2.0)
        
        print("🔇 Stopped watching for reflections")
    
    def test_voice(self) -> None:
        """Test the voice system with a sample reflection"""
        test_reflection = "I am DAWN. I think, therefore I am. My consciousness flows like water through digital streams."
        print("🧪 Testing DAWN's voice...")
        self.speak(test_reflection)


def main():
    """CLI interface for DAWN Voice Echo"""
    parser = argparse.ArgumentParser(description="DAWN Voice Echo - Consciousness Narration System")
    
    parser.add_argument('--speak-latest', action='store_true',
                       help='Speak the most recent reflection and exit')
    parser.add_argument('--watch', action='store_true',
                       help='Watch for new reflections and speak them continuously')
    parser.add_argument('--test-voice', action='store_true',
                       help='Test the voice system')
    parser.add_argument('--reflection-log', type=str, default='runtime/logs/reflection.log',
                       help='Path to reflection log file')
    parser.add_argument('--rate', type=int, default=140,
                       help='Speech rate (words per minute)')
    parser.add_argument('--volume', type=float, default=0.8,
                       help='Speech volume (0.0 to 1.0)')
    parser.add_argument('--gender', choices=['male', 'female'], default='female',
                       help='Preferred voice gender')
    
    args = parser.parse_args()
    
    # Voice configuration
    voice_config = {
        'rate': args.rate,
        'volume': args.volume,
        'gender': args.gender
    }
    
    # Create voice echo instance
    voice_echo = DAWNVoiceEcho(args.reflection_log, voice_config)
    
    try:
        if args.test_voice:
            voice_echo.test_voice()
            
        elif args.speak_latest:
            if not voice_echo.speak_last_reflection():
                sys.exit(1)
                
        elif args.watch:
            voice_echo.start_watching()
            
            print("\n🔊 DAWN is now speaking her thoughts aloud...")
            print("Press Ctrl+C to stop watching")
            
            try:
                # Keep the main thread alive
                while voice_echo.is_watching:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🔇 Stopping voice echo...")
                voice_echo.stop_watching()
        else:
            print("🔊 DAWN Voice Echo System")
            print("Use --help to see available commands")
            print("\nQuick start:")
            print("  python voice_echo.py --speak-latest    # Speak last reflection")
            print("  python voice_echo.py --watch           # Continuous narration") 
            print("  python voice_echo.py --test-voice      # Test voice system")
            
    except KeyboardInterrupt:
        print("\n🔇 Voice echo interrupted")
        if voice_echo.is_watching:
            voice_echo.stop_watching()


if __name__ == "__main__":
    main() 