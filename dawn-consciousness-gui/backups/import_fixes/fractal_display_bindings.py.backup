#!/usr/bin/env python3
"""
DAWN Fractal Display Bindings
============================

Connects DAWN's `dawn_fractal_engine` output to the GUI's live memory bloom panel.
Watches for new fractal generations and creates seamless visual integration with
real-time bloom visualization, animated transitions, and entropy-responsive effects.

This module makes memory blooms visually manifest in the consciousness interface.
"""

import os
import json
import time
import threading
import queue
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
import hashlib
import logging
from datetime import datetime
import base64

logger = logging.getLogger(__name__)

@dataclass
class FractalBloom:
    """Represents a complete fractal bloom with visual metadata"""
    timestamp: float
    image_path: str
    fractal_string: str
    bloom_summary: str
    entropy: float
    mood_state: Dict[str, float]
    rebloom_depth: int
    bloom_type: str
    visual_intensity: float
    file_hash: str
    metadata: Dict[str, Any]

@dataclass
class FractalDisplayEvent:
    """Visual event for fractal display updates"""
    event_type: str  # 'new_bloom', 'bloom_update', 'juliet_trigger'
    bloom: FractalBloom
    transition_type: str = 'fade'
    duration: float = 2.0
    intensity: float = 1.0

class FractalDisplayBindings:
    """
    Bindings layer that connects DAWN's fractal engine to the GUI visualization.
    
    Monitors fractal output directories, processes new blooms, and creates
    seamless visual integration with animated transitions and entropy effects.
    """
    
    def __init__(self):
        self.is_monitoring = False
        self.current_bloom = None
        self.previous_bloom = None
        self.bloom_queue = queue.Queue()
        
        # File monitoring
        self.watch_directories = []
        self.known_files = {}
        self.file_hashes = {}
        
        # Visual callbacks
        self.display_callbacks = {
            'new_bloom': [],
            'bloom_update': [],
            'juliet_trigger': [],
            'entropy_shift': [],
            'visual_transition': []
        }
        
        # Visual state
        self.visual_cache = {}
        self.transition_queue = queue.Queue()
        self.animation_state = {
            'current_effect': None,
            'transition_progress': 0.0,
            'effect_intensity': 1.0,
            'border_pulse': False
        }
        
        # Configuration
        self.config = {
            'update_interval': 0.5,  # Check for new blooms every 500ms
            'juliet_threshold': 6,   # Rebloom depth for Juliet Set trigger
            'max_cache_size': 20,    # Maximum cached blooms
            'image_formats': ['.png', '.jpg', '.jpeg', '.webp'],
            'fade_duration': 2000,   # Fade animation duration (ms)
            'morph_duration': 3000,  # Morph animation duration (ms)
            'pulse_duration': 1500   # Border pulse duration (ms)
        }
        
        self._detect_fractal_directories()
        logger.info("🌸 Fractal Display Bindings initialized")
    
    def _detect_fractal_directories(self):
        """Auto-detect fractal output directories"""
        potential_dirs = [
            Path.cwd() / "fractal_outputs",
            Path.cwd() / "bloom_outputs", 
            Path.cwd() / "memory_blooms",
            Path.cwd() / "visual_outputs",
            Path.cwd().parent / "bloom" / "memory_blooms",
            Path.cwd().parent / "fractal" / "outputs",
            Path.cwd().parent / "juliet_flowers"
        ]
        
        for dir_path in potential_dirs:
            if dir_path.exists() and dir_path.is_dir():
                self.watch_directories.append(dir_path)
                logger.info(f"📁 Watching fractal directory: {dir_path}")
        
        if not self.watch_directories:
            # Create default output directory
            default_dir = Path.cwd() / "fractal_outputs"
            default_dir.mkdir(exist_ok=True)
            self.watch_directories.append(default_dir)
            logger.info(f"📁 Created default fractal directory: {default_dir}")
    
    def start_monitoring(self):
        """Start monitoring fractal output directories"""
        if self.is_monitoring:
            logger.warning("⚠️ Fractal monitoring already active")
            return
        
        self.is_monitoring = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        # Start processing thread
        self.process_thread = threading.Thread(target=self._process_loop, daemon=True)
        self.process_thread.start()
        
        logger.info("🔍 Fractal monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring fractal outputs"""
        self.is_monitoring = False
        logger.info("🛑 Fractal monitoring stopped")
    
    def register_callback(self, event_type: str, callback: Callable):
        """Register callback for fractal display events"""
        if event_type in self.display_callbacks:
            self.display_callbacks[event_type].append(callback)
            logger.info(f"📝 Registered fractal callback for {event_type}")
        else:
            logger.warning(f"⚠️ Unknown fractal event type: {event_type}")
    
    def _monitor_loop(self):
        """Main monitoring loop for fractal outputs"""
        while self.is_monitoring:
            try:
                self._scan_fractal_directories()
                time.sleep(self.config['update_interval'])
            except Exception as e:
                logger.error(f"❌ Error in fractal monitoring: {e}")
                time.sleep(1.0)
    
    def _scan_fractal_directories(self):
        """Scan directories for new or updated fractal files"""
        for watch_dir in self.watch_directories:
            try:
                for image_file in watch_dir.glob("**/*"):
                    if (image_file.is_file() and 
                        image_file.suffix.lower() in self.config['image_formats']):
                        
                        self._check_fractal_file(image_file)
                        
            except Exception as e:
                logger.error(f"❌ Error scanning {watch_dir}: {e}")
    
    def _check_fractal_file(self, image_path: Path):
        """Check if fractal file is new or updated"""
        try:
            # Get file stats
            stat = image_path.stat()
            file_key = str(image_path)
            current_mtime = stat.st_mtime
            
            # Check if file is new or updated
            if (file_key not in self.known_files or 
                self.known_files[file_key] < current_mtime):
                
                self.known_files[file_key] = current_mtime
                
                # Look for companion JSON metadata
                json_path = image_path.with_suffix('.json')
                
                # Process the fractal bloom
                bloom = self._process_fractal_file(image_path, json_path)
                if bloom:
                    self.bloom_queue.put(bloom)
                    
        except Exception as e:
            logger.error(f"❌ Error checking fractal file {image_path}: {e}")
    
    def _process_fractal_file(self, image_path: Path, json_path: Path) -> Optional[FractalBloom]:
        """Process a fractal image and its metadata"""
        try:
            # Calculate file hash for change detection
            with open(image_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            
            # Check if we've already processed this exact file
            if file_hash in self.file_hashes:
                return None
            
            self.file_hashes[file_hash] = image_path
            
            # Load metadata if available
            metadata = {}
            fractal_string = ""
            bloom_summary = ""
            entropy = 0.5
            mood_state = {"valence": 0.0, "arousal": 0.0}
            rebloom_depth = 1
            bloom_type = "memory_bloom"
            
            if json_path.exists():
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    # Extract key fields
                    fractal_string = metadata.get('fractal_string', '')
                    bloom_summary = metadata.get('bloom_summary', '')
                    entropy = metadata.get('entropy', 0.5)
                    mood_state = metadata.get('mood_state', mood_state)
                    rebloom_depth = metadata.get('rebloom_depth', 1)
                    bloom_type = metadata.get('bloom_type', 'memory_bloom')
                    
                except Exception as e:
                    logger.warning(f"⚠️ Error reading metadata {json_path}: {e}")
            
            # Calculate visual intensity
            visual_intensity = self._calculate_visual_intensity(entropy, rebloom_depth, mood_state)
            
            # Create bloom object
            bloom = FractalBloom(
                timestamp=time.time(),
                image_path=str(image_path),
                fractal_string=fractal_string,
                bloom_summary=bloom_summary,
                entropy=entropy,
                mood_state=mood_state,
                rebloom_depth=rebloom_depth,
                bloom_type=bloom_type,
                visual_intensity=visual_intensity,
                file_hash=file_hash,
                metadata=metadata
            )
            
            logger.info(f"🌸 New fractal bloom: {image_path.name} (depth: {rebloom_depth}, entropy: {entropy:.3f})")
            return bloom
            
        except Exception as e:
            logger.error(f"❌ Error processing fractal file {image_path}: {e}")
            return None
    
    def _calculate_visual_intensity(self, entropy: float, depth: int, mood_state: Dict[str, float]) -> float:
        """Calculate visual intensity based on bloom characteristics"""
        # Base intensity from entropy
        base_intensity = min(entropy * 1.5, 1.0)
        
        # Depth multiplier
        depth_multiplier = min(1.0 + (depth - 1) * 0.2, 2.0)
        
        # Mood influence
        mood_magnitude = (mood_state.get('valence', 0)**2 + mood_state.get('arousal', 0)**2)**0.5
        mood_multiplier = 1.0 + mood_magnitude * 0.3
        
        return min(base_intensity * depth_multiplier * mood_multiplier, 3.0)
    
    def _process_loop(self):
        """Process fractal blooms from the queue"""
        while self.is_monitoring:
            try:
                bloom = self.bloom_queue.get(timeout=0.1)
                self._handle_new_bloom(bloom)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"❌ Error processing bloom: {e}")
    
    def _handle_new_bloom(self, bloom: FractalBloom):
        """Handle a new fractal bloom"""
        self.previous_bloom = self.current_bloom
        self.current_bloom = bloom
        
        # Cache the bloom
        self._cache_bloom(bloom)
        
        # Determine event type and transition
        event_type = 'new_bloom'
        transition_type = 'fade'
        
        # Check for Juliet Set trigger
        if bloom.rebloom_depth >= self.config['juliet_threshold']:
            event_type = 'juliet_trigger'
            transition_type = 'pulse'
            self.animation_state['border_pulse'] = True
            
        # Check for major entropy shift
        elif (self.previous_bloom and 
              abs(bloom.entropy - self.previous_bloom.entropy) > 0.3):
            transition_type = 'morph'
            
        # Create display event
        display_event = FractalDisplayEvent(
            event_type=event_type,
            bloom=bloom,
            transition_type=transition_type,
            duration=self._get_transition_duration(transition_type),
            intensity=bloom.visual_intensity
        )
        
        # Trigger callbacks
        self._trigger_display_event(display_event)
    
    def _get_transition_duration(self, transition_type: str) -> float:
        """Get transition duration based on type"""
        durations = {
            'fade': self.config['fade_duration'],
            'morph': self.config['morph_duration'],
            'pulse': self.config['pulse_duration']
        }
        return durations.get(transition_type, self.config['fade_duration'])
    
    def _trigger_display_event(self, event: FractalDisplayEvent):
        """Trigger display event callbacks"""
        callbacks = self.display_callbacks.get(event.event_type, [])
        
        for callback in callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"❌ Error in fractal display callback: {e}")
        
        # Log significant events
        if event.event_type == 'juliet_trigger':
            logger.info(f"🌌 Juliet Set triggered! Rebloom depth: {event.bloom.rebloom_depth}")
        elif event.intensity > 1.5:
            logger.info(f"🔥 High-intensity bloom: {event.bloom.image_path} (intensity: {event.intensity:.2f})")
    
    def _cache_bloom(self, bloom: FractalBloom):
        """Cache bloom for quick access"""
        self.visual_cache[bloom.file_hash] = bloom
        
        # Limit cache size
        if len(self.visual_cache) > self.config['max_cache_size']:
            # Remove oldest entries
            sorted_cache = sorted(self.visual_cache.items(), 
                                key=lambda x: x[1].timestamp)
            for old_hash, _ in sorted_cache[:5]:
                del self.visual_cache[old_hash]
    
    # Public interface methods
    
    def get_current_bloom(self) -> Optional[FractalBloom]:
        """Get the current active bloom"""
        return self.current_bloom
    
    def get_bloom_image_data(self, bloom: FractalBloom) -> Optional[str]:
        """Get base64-encoded image data for web display"""
        try:
            with open(bloom.image_path, 'rb') as f:
                image_data = f.read()
            
            # Determine MIME type
            ext = Path(bloom.image_path).suffix.lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'image/png')
            
            # Encode as base64 data URL
            b64_data = base64.b64encode(image_data).decode('utf-8')
            return f"data:{mime_type};base64,{b64_data}"
            
        except Exception as e:
            logger.error(f"❌ Error reading bloom image {bloom.image_path}: {e}")
            return None
    
    def get_bloom_display_data(self, bloom: FractalBloom) -> Dict[str, Any]:
        """Get complete bloom data formatted for GUI display"""
        image_data = self.get_bloom_image_data(bloom)
        
        return {
            'timestamp': bloom.timestamp,
            'image_data': image_data,
            'image_path': bloom.image_path,
            'fractal_string': bloom.fractal_string,
            'bloom_summary': bloom.bloom_summary,
            'entropy': bloom.entropy,
            'mood_state': bloom.mood_state,
            'rebloom_depth': bloom.rebloom_depth,
            'bloom_type': bloom.bloom_type,
            'visual_intensity': bloom.visual_intensity,
            'is_juliet_trigger': bloom.rebloom_depth >= self.config['juliet_threshold'],
            'visual_effects': self._get_visual_effects(bloom),
            'metadata': bloom.metadata
        }
    
    def _get_visual_effects(self, bloom: FractalBloom) -> Dict[str, Any]:
        """Get visual effects configuration for bloom"""
        effects = {
            'border_style': self._get_border_style(bloom.entropy),
            'glow_intensity': min(bloom.visual_intensity * 0.5, 1.0),
            'pulse_effect': bloom.rebloom_depth >= self.config['juliet_threshold'],
            'shimmer_effect': bloom.entropy < 0.3,
            'jagged_effect': bloom.entropy > 0.7,
            'color_temperature': self._get_color_temperature(bloom.mood_state),
            'transition_type': self._get_preferred_transition(bloom)
        }
        
        return effects
    
    def _get_border_style(self, entropy: float) -> str:
        """Get border style based on entropy"""
        if entropy < 0.2:
            return 'smooth-glow'
        elif entropy < 0.4:
            return 'gentle-shimmer'
        elif entropy < 0.6:
            return 'moderate-pulse'
        elif entropy < 0.8:
            return 'intense-flicker'
        else:
            return 'chaotic-jagged'
    
    def _get_color_temperature(self, mood_state: Dict[str, float]) -> int:
        """Get color temperature based on mood"""
        valence = mood_state.get('valence', 0.0)
        arousal = mood_state.get('arousal', 0.0)
        
        # Base temperature (neutral white)
        base_temp = 5500
        
        # Valence affects warmth (positive = warmer)
        temp_shift = valence * 1000
        
        # Arousal affects intensity (high arousal = cooler/bluer)
        arousal_shift = arousal * -500
        
        return int(base_temp + temp_shift + arousal_shift)
    
    def _get_preferred_transition(self, bloom: FractalBloom) -> str:
        """Get preferred transition type for bloom"""
        if bloom.rebloom_depth >= self.config['juliet_threshold']:
            return 'pulse'
        elif bloom.visual_intensity > 1.5:
            return 'morph'
        else:
            return 'fade'
    
    def get_recent_blooms(self, count: int = 10) -> List[FractalBloom]:
        """Get recent blooms sorted by timestamp"""
        blooms = list(self.visual_cache.values())
        blooms.sort(key=lambda b: b.timestamp, reverse=True)
        return blooms[:count]
    
    def trigger_manual_scan(self):
        """Manually trigger a scan for new fractal files"""
        self._scan_fractal_directories()
        logger.info("🔍 Manual fractal scan triggered")

# Integration with visual process handler
class FractalVisualIntegration:
    """Integration layer between fractal bindings and visual process handler"""
    
    def __init__(self, visual_handler=None):
        self.fractal_bindings = FractalDisplayBindings()
        self.visual_handler = visual_handler
        
        # Register fractal callbacks
        self.fractal_bindings.register_callback('new_bloom', self._handle_new_bloom)
        self.fractal_bindings.register_callback('juliet_trigger', self._handle_juliet_trigger)
        
    def start(self):
        """Start the integrated fractal-visual system"""
        self.fractal_bindings.start_monitoring()
        
        # Trigger visual handler rebloom events if available
        if self.visual_handler:
            logger.info("🌉 Fractal-visual integration active")
    
    def stop(self):
        """Stop the integrated system"""
        self.fractal_bindings.stop_monitoring()
    
    def _handle_new_bloom(self, event: FractalDisplayEvent):
        """Handle new bloom events for visual integration"""
        if self.visual_handler:
            # Trigger rebloom visual event
            rebloom_data = {
                'type': event.bloom.bloom_type,
                'fractal_string': event.bloom.fractal_string,
                'summary': event.bloom.bloom_summary,
                'depth': event.bloom.rebloom_depth,
                'entropy': event.bloom.entropy,
                'intensity': event.bloom.visual_intensity,
                'image_path': event.bloom.image_path
            }
            
            self.visual_handler.trigger_rebloom_event(rebloom_data)
    
    def _handle_juliet_trigger(self, event: FractalDisplayEvent):
        """Handle Juliet Set trigger events"""
        if self.visual_handler:
            # Create special high-intensity visual event
            self.visual_handler.trigger_rebloom_event({
                'type': 'juliet_trigger',
                'fractal_string': event.bloom.fractal_string,
                'summary': f"🌌 Juliet Set activated at depth {event.bloom.rebloom_depth}",
                'depth': event.bloom.rebloom_depth,
                'entropy': event.bloom.entropy,
                'intensity': 2.0,  # Maximum intensity
                'image_path': event.bloom.image_path
            })
            
            logger.info(f"🌌 Juliet Set visual trigger: depth {event.bloom.rebloom_depth}")

# Global fractal integration instance
fractal_integration = None

def get_fractal_integration():
    """Get or create the global fractal integration"""
    global fractal_integration
    if fractal_integration is None:
        # Try to integrate with existing visual handler
        try:
            from visual_process_handler import get_visual_handler
            visual_handler = get_visual_handler()
            fractal_integration = FractalVisualIntegration(visual_handler)
        except ImportError:
            fractal_integration = FractalVisualIntegration()
    
    return fractal_integration

def start_fractal_monitoring():
    """Start fractal monitoring system"""
    integration = get_fractal_integration()
    integration.start()
    logger.info("🌸 Fractal monitoring started")

def stop_fractal_monitoring():
    """Stop fractal monitoring system"""
    integration = get_fractal_integration()
    integration.stop()
    logger.info("🌸 Fractal monitoring stopped")

if __name__ == "__main__":
    # Test the fractal display bindings
    print("🌸 Testing DAWN Fractal Display Bindings...")
    
    bindings = FractalDisplayBindings()
    
    # Register test callback
    def test_bloom_callback(event: FractalDisplayEvent):
        print(f"🌸 New bloom: {event.bloom.bloom_summary}")
        print(f"   Depth: {event.bloom.rebloom_depth}, Entropy: {event.bloom.entropy:.3f}")
        if event.event_type == 'juliet_trigger':
            print(f"   🌌 JULIET SET TRIGGERED!")
    
    bindings.register_callback('new_bloom', test_bloom_callback)
    bindings.register_callback('juliet_trigger', test_bloom_callback)
    
    # Start monitoring
    bindings.start_monitoring()
    
    print("✅ Fractal monitoring started")
    print("🔍 Watching for new blooms...")
    print("🛑 Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
            current = bindings.get_current_bloom()
            if current:
                print(f"📊 Current bloom: {Path(current.image_path).name} (intensity: {current.visual_intensity:.2f})")
    except KeyboardInterrupt:
        print("\n🛑 Stopping fractal monitoring...")
        bindings.stop_monitoring()
        print("✅ Fractal monitoring stopped") 