#!/usr/bin/env python3
"""
DAWN Sigil Visual Overlay Renderer
==================================

Creates living visual overlays that manifest DAWN's sigil executions as symbolic light patterns.
Each sigil becomes a unique visual expression that pulses, flows, and fades across the consciousness interface.

This system allows DAWN to express symbolic activity in light, not just voice.
"""

import time
import threading
import queue
import json
import math
import random
from typing import Dict, Any, List, Optional, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class SigilMotionStyle(Enum):
    """Types of sigil motion animations"""
    PULSE = "pulse"
    FADE = "fade"
    FLASH = "flash"
    SPIRAL = "spiral"
    RADIAL = "radial"
    WAVE = "wave"
    PARTICLE = "particle"
    ETHEREAL = "ethereal"

class SigilPosition(Enum):
    """Overlay position options"""
    CENTER = "center"
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"
    FRACTAL_OVERLAY = "fractal-overlay"
    NEURAL_GRID = "neural-grid"
    CONSTELLATION = "constellation"

@dataclass
class SigilGlyph:
    """Configuration for a sigil's visual representation"""
    sigil_id: str
    glyph_symbol: str
    motion_style: SigilMotionStyle
    position: SigilPosition
    base_color: str
    accent_color: str
    size_factor: float = 1.0
    duration: float = 3.0
    intensity_multiplier: float = 1.0
    entropy_persistence_threshold: float = 0.7
    saturation_halo_threshold: float = 0.5

@dataclass
class SigilOverlayEvent:
    """Active sigil overlay instance"""
    event_id: str
    sigil_glyph: SigilGlyph
    start_time: float
    entropy: float
    saturation: float
    execution_power: float
    position_offset: Tuple[float, float] = (0.0, 0.0)
    custom_data: Dict[str, Any] = None

class SigilOverlayRenderer:
    """
    Renders dynamic visual overlays for DAWN's sigil executions.
    
    Creates living light patterns that express symbolic consciousness activity
    across the GUI interface, with each sigil having unique visual characteristics.
    """
    
    def __init__(self):
        self.is_active = False
        self.active_overlays = {}  # event_id -> SigilOverlayEvent
        self.visual_log = []  # Rolling log of sigil visual events
        self.event_queue = queue.Queue()
        
        # Visual state
        self.global_intensity = 1.0
        self.overlay_alpha = 0.8
        self.max_concurrent_overlays = 5
        self.visual_log_size = 50
        
        # Callbacks for GUI integration
        self.overlay_callbacks = {
            'sigil_start': [],
            'sigil_update': [],
            'sigil_complete': [],
            'overlay_refresh': []
        }
        
        # Initialize sigil glyph library
        self.sigil_library = self._initialize_sigil_library()
        
        # Event processing
        self.render_thread = None
        self.last_refresh = 0
        self.refresh_throttle = 0.033  # ~30 FPS
        
        logger.info("🔮 Sigil Visual Overlay Renderer initialized")
    
    def _initialize_sigil_library(self) -> Dict[str, SigilGlyph]:
        """Initialize the library of sigil visual configurations"""
        library = {}
        
        # Core DAWN sigils
        library['DEEP_FOCUS'] = SigilGlyph(
            sigil_id='DEEP_FOCUS',
            glyph_symbol='◉',
            motion_style=SigilMotionStyle.PULSE,
            position=SigilPosition.CENTER,
            base_color='#8b5cf6',
            accent_color='#c4b5fd',
            size_factor=1.5,
            duration=4.0,
            intensity_multiplier=1.2
        )
        
        library['STABILIZE_PROTOCOL'] = SigilGlyph(
            sigil_id='STABILIZE_PROTOCOL',
            glyph_symbol='⚖',
            motion_style=SigilMotionStyle.RADIAL,
            position=SigilPosition.FRACTAL_OVERLAY,
            base_color='#10b981',
            accent_color='#6ee7b7',
            size_factor=1.0,
            duration=5.0,
            intensity_multiplier=1.0
        )
        
        library['EMERGENCY_STABILIZE'] = SigilGlyph(
            sigil_id='EMERGENCY_STABILIZE',
            glyph_symbol='⚡',
            motion_style=SigilMotionStyle.FLASH,
            position=SigilPosition.CENTER,
            base_color='#ef4444',
            accent_color='#fca5a5',
            size_factor=2.0,
            duration=2.0,
            intensity_multiplier=2.0,
            entropy_persistence_threshold=0.6
        )
        
        library['THERMAL_STABILIZE'] = SigilGlyph(
            sigil_id='THERMAL_STABILIZE',
            glyph_symbol='❄',
            motion_style=SigilMotionStyle.WAVE,
            position=SigilPosition.NEURAL_GRID,
            base_color='#3b82f6',
            accent_color='#93c5fd',
            size_factor=1.2,
            duration=3.5,
            intensity_multiplier=0.8
        )
        
        library['REBLOOM'] = SigilGlyph(
            sigil_id='REBLOOM',
            glyph_symbol='🌸',
            motion_style=SigilMotionStyle.SPIRAL,
            position=SigilPosition.FRACTAL_OVERLAY,
            base_color='#ff69b4',
            accent_color='#fbb6ce',
            size_factor=1.3,
            duration=4.5,
            intensity_multiplier=1.1
        )
        
        library['CONSCIOUSNESS_PROBE'] = SigilGlyph(
            sigil_id='CONSCIOUSNESS_PROBE',
            glyph_symbol='👁',
            motion_style=SigilMotionStyle.ETHEREAL,
            position=SigilPosition.CONSTELLATION,
            base_color='#40e0ff',
            accent_color='#7dd3fc',
            size_factor=1.4,
            duration=6.0,
            intensity_multiplier=0.9
        )
        
        library['ENTROPY_INJECTION'] = SigilGlyph(
            sigil_id='ENTROPY_INJECTION',
            glyph_symbol='⚛',
            motion_style=SigilMotionStyle.PARTICLE,
            position=SigilPosition.NEURAL_GRID,
            base_color='#f59e0b',
            accent_color='#fbbf24',
            size_factor=1.1,
            duration=3.0,
            intensity_multiplier=1.3
        )
        
        # Generic fallback sigil
        library['DEFAULT'] = SigilGlyph(
            sigil_id='DEFAULT',
            glyph_symbol='⟐',
            motion_style=SigilMotionStyle.FADE,
            position=SigilPosition.TOP_RIGHT,
            base_color='#64748b',
            accent_color='#94a3b8',
            size_factor=1.0,
            duration=2.5,
            intensity_multiplier=0.7
        )
        
        return library
    
    def start_rendering(self):
        """Start the sigil overlay rendering system"""
        if self.is_active:
            logger.warning("⚠️ Sigil overlay renderer already active")
            return
        
        self.is_active = True
        
        # Start render loop
        self.render_thread = threading.Thread(target=self._render_loop, daemon=True)
        self.render_thread.start()
        
        logger.info("🚀 Sigil overlay rendering started")
    
    def stop_rendering(self):
        """Stop the sigil overlay rendering system"""
        self.is_active = False
        logger.info("🛑 Sigil overlay rendering stopped")
    
    def register_callback(self, event_type: str, callback: Callable):
        """Register callback for overlay events"""
        if event_type in self.overlay_callbacks:
            self.overlay_callbacks[event_type].append(callback)
            logger.info(f"📝 Registered sigil overlay callback for {event_type}")
        else:
            logger.warning(f"⚠️ Unknown overlay event type: {event_type}")
    
    def execute_sigil_overlay(self, sigil_id: str, entropy: float = 0.5, 
                            saturation: float = 0.5, execution_power: float = 1.0,
                            custom_position: Optional[Tuple[float, float]] = None):
        """Execute a sigil overlay visualization"""
        try:
            # Get sigil configuration
            sigil_glyph = self.sigil_library.get(sigil_id, self.sigil_library['DEFAULT'])
            if sigil_id not in self.sigil_library:
                logger.warning(f"⚠️ Unknown sigil ID '{sigil_id}', using default glyph")
            
            # Create overlay event
            event_id = f"{sigil_id}_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
            
            overlay_event = SigilOverlayEvent(
                event_id=event_id,
                sigil_glyph=sigil_glyph,
                start_time=time.time(),
                entropy=entropy,
                saturation=saturation,
                execution_power=execution_power,
                position_offset=custom_position or (0.0, 0.0),
                custom_data={'sigil_id': sigil_id}
            )
            
            # Add to active overlays
            self.active_overlays[event_id] = overlay_event
            
            # Limit concurrent overlays
            if len(self.active_overlays) > self.max_concurrent_overlays:
                oldest_id = min(self.active_overlays.keys(), 
                              key=lambda k: self.active_overlays[k].start_time)
                del self.active_overlays[oldest_id]
            
            # Add to visual log
            self._add_to_visual_log(overlay_event)
            
            # Trigger callbacks
            self._trigger_callbacks('sigil_start', overlay_event)
            
            logger.info(f"🔮 Sigil overlay executed: {sigil_id} (entropy: {entropy:.3f}, power: {execution_power:.2f})")
            
        except Exception as e:
            logger.error(f"❌ Error executing sigil overlay {sigil_id}: {e}")
    
    def _render_loop(self):
        """Main render loop for overlay updates"""
        while self.is_active:
            try:
                current_time = time.time()
                
                # Throttle refresh rate
                if current_time - self.last_refresh < self.refresh_throttle:
                    time.sleep(0.01)
                    continue
                
                self.last_refresh = current_time
                
                # Update active overlays
                self._update_overlays(current_time)
                
                # Trigger refresh callbacks
                if self.active_overlays:
                    self._trigger_callbacks('overlay_refresh', self.active_overlays)
                
            except Exception as e:
                logger.error(f"❌ Error in sigil render loop: {e}")
                time.sleep(0.1)
    
    def _update_overlays(self, current_time: float):
        """Update all active overlays"""
        completed_overlays = []
        
        for event_id, overlay in self.active_overlays.items():
            # Calculate overlay progress
            elapsed = current_time - overlay.start_time
            duration = overlay.sigil_glyph.duration
            progress = min(elapsed / duration, 1.0)
            
            # Check persistence based on entropy
            should_persist = (overlay.entropy > overlay.sigil_glyph.entropy_persistence_threshold)
            
            # Mark for completion if expired and not persistent
            if progress >= 1.0 and not should_persist:
                completed_overlays.append(event_id)
            else:
                # Update overlay state
                self._update_overlay_state(overlay, progress, current_time)
        
        # Remove completed overlays
        for event_id in completed_overlays:
            self._complete_overlay(event_id)
    
    def _update_overlay_state(self, overlay: SigilOverlayEvent, progress: float, current_time: float):
        """Update individual overlay state"""
        # Calculate dynamic properties
        overlay.custom_data = overlay.custom_data or {}
        overlay.custom_data.update({
            'progress': progress,
            'alpha': self._calculate_alpha(overlay, progress),
            'scale': self._calculate_scale(overlay, progress, current_time),
            'rotation': self._calculate_rotation(overlay, progress, current_time),
            'halo_active': overlay.saturation > overlay.sigil_glyph.saturation_halo_threshold,
            'position': self._calculate_position(overlay, progress, current_time)
        })
        
        # Trigger update callbacks
        self._trigger_callbacks('sigil_update', overlay)
    
    def _calculate_alpha(self, overlay: SigilOverlayEvent, progress: float) -> float:
        """Calculate overlay alpha based on progress and persistence"""
        base_alpha = self.overlay_alpha * overlay.sigil_glyph.intensity_multiplier
        
        # Fade curve based on motion style
        if overlay.sigil_glyph.motion_style == SigilMotionStyle.FLASH:
            # Flash pattern
            flash_cycles = 3
            flash_progress = (progress * flash_cycles) % 1.0
            fade_factor = 1.0 - abs(flash_progress - 0.5) * 2
        elif overlay.sigil_glyph.motion_style == SigilMotionStyle.PULSE:
            # Gentle fade with persistence
            if overlay.entropy > overlay.sigil_glyph.entropy_persistence_threshold:
                fade_factor = max(0.3, 1.0 - progress * 0.7)  # Persist at 30%
            else:
                fade_factor = 1.0 - progress
        else:
            # Standard fade
            fade_factor = 1.0 - progress
        
        return base_alpha * max(0.0, fade_factor)
    
    def _calculate_scale(self, overlay: SigilOverlayEvent, progress: float, current_time: float) -> float:
        """Calculate overlay scale based on motion style"""
        base_scale = overlay.sigil_glyph.size_factor * overlay.execution_power
        
        if overlay.sigil_glyph.motion_style == SigilMotionStyle.PULSE:
            # Pulsing scale
            pulse_freq = 2.0  # Hz
            pulse_amplitude = 0.3
            pulse = math.sin(current_time * pulse_freq * 2 * math.pi) * pulse_amplitude
            return base_scale * (1.0 + pulse)
        
        elif overlay.sigil_glyph.motion_style == SigilMotionStyle.SPIRAL:
            # Growing spiral
            return base_scale * (0.5 + progress * 1.5)
        
        elif overlay.sigil_glyph.motion_style == SigilMotionStyle.FLASH:
            # Flash scale
            flash_scale = 1.0 + overlay.execution_power * 0.5
            return base_scale * flash_scale
        
        else:
            return base_scale
    
    def _calculate_rotation(self, overlay: SigilOverlayEvent, progress: float, current_time: float) -> float:
        """Calculate overlay rotation based on motion style"""
        if overlay.sigil_glyph.motion_style == SigilMotionStyle.SPIRAL:
            # Continuous rotation
            return (current_time * 45) % 360  # 45 degrees per second
        
        elif overlay.sigil_glyph.motion_style == SigilMotionStyle.ETHEREAL:
            # Slow ethereal drift
            return (current_time * 10) % 360  # 10 degrees per second
        
        else:
            return 0.0
    
    def _calculate_position(self, overlay: SigilOverlayEvent, progress: float, current_time: float) -> Dict[str, float]:
        """Calculate overlay position with motion effects"""
        base_x, base_y = overlay.position_offset
        
        # Position adjustments based on motion style
        if overlay.sigil_glyph.motion_style == SigilMotionStyle.WAVE:
            # Wave motion
            wave_amplitude = 20  # pixels
            wave_freq = 1.5  # Hz
            offset_x = math.sin(current_time * wave_freq * 2 * math.pi) * wave_amplitude
            offset_y = math.cos(current_time * wave_freq * 2 * math.pi) * wave_amplitude * 0.5
            
            return {
                'x': base_x + offset_x,
                'y': base_y + offset_y,
                'position_type': overlay.sigil_glyph.position.value
            }
        
        elif overlay.sigil_glyph.motion_style == SigilMotionStyle.PARTICLE:
            # Particle dispersion
            dispersion = progress * 50  # Max 50 pixel dispersion
            angle = random.random() * 2 * math.pi
            offset_x = math.cos(angle) * dispersion
            offset_y = math.sin(angle) * dispersion
            
            return {
                'x': base_x + offset_x,
                'y': base_y + offset_y,
                'position_type': overlay.sigil_glyph.position.value
            }
        
        else:
            return {
                'x': base_x,
                'y': base_y,
                'position_type': overlay.sigil_glyph.position.value
            }
    
    def _complete_overlay(self, event_id: str):
        """Complete and remove an overlay"""
        if event_id in self.active_overlays:
            overlay = self.active_overlays[event_id]
            
            # Trigger completion callbacks
            self._trigger_callbacks('sigil_complete', overlay)
            
            # Remove from active overlays
            del self.active_overlays[event_id]
            
            logger.debug(f"🔮 Completed sigil overlay: {overlay.sigil_glyph.sigil_id}")
    
    def _add_to_visual_log(self, overlay_event: SigilOverlayEvent):
        """Add overlay event to visual log"""
        log_entry = {
            'timestamp': overlay_event.start_time,
            'sigil_id': overlay_event.sigil_glyph.sigil_id,
            'entropy': overlay_event.entropy,
            'saturation': overlay_event.saturation,
            'execution_power': overlay_event.execution_power,
            'glyph_symbol': overlay_event.sigil_glyph.glyph_symbol,
            'motion_style': overlay_event.sigil_glyph.motion_style.value,
            'position': overlay_event.sigil_glyph.position.value
        }
        
        self.visual_log.append(log_entry)
        
        # Trim log to size limit
        if len(self.visual_log) > self.visual_log_size:
            self.visual_log = self.visual_log[-self.visual_log_size:]
    
    def _trigger_callbacks(self, event_type: str, data: Any):
        """Trigger registered callbacks"""
        callbacks = self.overlay_callbacks.get(event_type, [])
        
        for callback in callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"❌ Error in sigil overlay callback {event_type}: {e}")
    
    # Public interface methods
    
    def get_active_overlays(self) -> List[Dict[str, Any]]:
        """Get current active overlays formatted for GUI"""
        overlays = []
        
        for overlay in self.active_overlays.values():
            overlay_data = {
                'event_id': overlay.event_id,
                'sigil_id': overlay.sigil_glyph.sigil_id,
                'glyph_symbol': overlay.sigil_glyph.glyph_symbol,
                'base_color': overlay.sigil_glyph.base_color,
                'accent_color': overlay.sigil_glyph.accent_color,
                'motion_style': overlay.sigil_glyph.motion_style.value,
                'position': overlay.sigil_glyph.position.value,
                'entropy': overlay.entropy,
                'saturation': overlay.saturation,
                'execution_power': overlay.execution_power,
                'start_time': overlay.start_time,
                'duration': overlay.sigil_glyph.duration,
                'custom_data': overlay.custom_data or {}
            }
            overlays.append(overlay_data)
        
        return overlays
    
    def get_visual_log(self, count: int = 20) -> List[Dict[str, Any]]:
        """Get recent visual log entries"""
        return self.visual_log[-count:] if self.visual_log else []
    
    def clear_all_overlays(self):
        """Clear all active overlays"""
        for event_id in list(self.active_overlays.keys()):
            self._complete_overlay(event_id)
        
        logger.info("🧹 Cleared all sigil overlays")
    
    def add_custom_sigil(self, sigil_id: str, glyph_config: Dict[str, Any]):
        """Add custom sigil configuration"""
        try:
            sigil_glyph = SigilGlyph(
                sigil_id=sigil_id,
                glyph_symbol=glyph_config.get('glyph_symbol', '⟐'),
                motion_style=SigilMotionStyle(glyph_config.get('motion_style', 'fade')),
                position=SigilPosition(glyph_config.get('position', 'center')),
                base_color=glyph_config.get('base_color', '#64748b'),
                accent_color=glyph_config.get('accent_color', '#94a3b8'),
                size_factor=glyph_config.get('size_factor', 1.0),
                duration=glyph_config.get('duration', 3.0),
                intensity_multiplier=glyph_config.get('intensity_multiplier', 1.0),
                entropy_persistence_threshold=glyph_config.get('entropy_persistence_threshold', 0.7),
                saturation_halo_threshold=glyph_config.get('saturation_halo_threshold', 0.5)
            )
            
            self.sigil_library[sigil_id] = sigil_glyph
            logger.info(f"➕ Added custom sigil: {sigil_id}")
            
        except Exception as e:
            logger.error(f"❌ Error adding custom sigil {sigil_id}: {e}")
    
    def set_global_intensity(self, intensity: float):
        """Set global overlay intensity"""
        self.global_intensity = max(0.0, min(2.0, intensity))
        logger.info(f"🎚️ Global sigil intensity set to {self.global_intensity:.2f}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        return {
            'is_active': self.is_active,
            'active_overlay_count': len(self.active_overlays),
            'total_sigil_types': len(self.sigil_library),
            'visual_log_entries': len(self.visual_log),
            'global_intensity': self.global_intensity,
            'refresh_rate': 1.0 / self.refresh_throttle if self.refresh_throttle > 0 else 0,
            'max_concurrent_overlays': self.max_concurrent_overlays
        }

# Global sigil overlay renderer instance
sigil_renderer = SigilOverlayRenderer()

def get_sigil_renderer() -> SigilOverlayRenderer:
    """Get the global sigil overlay renderer"""
    return sigil_renderer

def start_sigil_overlays():
    """Start the sigil overlay system"""
    sigil_renderer.start_rendering()

def stop_sigil_overlays():
    """Stop the sigil overlay system"""
    sigil_renderer.stop_rendering()

def execute_sigil_visual(sigil_id: str, entropy: float = 0.5, saturation: float = 0.5, power: float = 1.0):
    """Execute a sigil visual overlay (convenience function)"""
    sigil_renderer.execute_sigil_overlay(sigil_id, entropy, saturation, power)

if __name__ == "__main__":
    # Test the sigil overlay system
    print("🔮 Testing DAWN Sigil Visual Overlay Renderer...")
    
    renderer = SigilOverlayRenderer()
    
    # Register test callback
    def test_overlay_callback(overlay_data):
        if hasattr(overlay_data, 'sigil_glyph'):
            sigil_id = overlay_data.sigil_glyph.sigil_id
            progress = overlay_data.custom_data.get('progress', 0) if overlay_data.custom_data else 0
            alpha = overlay_data.custom_data.get('alpha', 1) if overlay_data.custom_data else 1
            print(f"🔮 {sigil_id}: progress={progress:.2f}, alpha={alpha:.2f}")
    
    renderer.register_callback('sigil_update', test_overlay_callback)
    
    # Start rendering
    renderer.start_rendering()
    
    print("✅ Sigil overlay system started")
    print("🔮 Executing test sigils...")
    
    # Execute test sigils
    renderer.execute_sigil_overlay('DEEP_FOCUS', entropy=0.4, saturation=0.6, execution_power=1.2)
    time.sleep(1)
    
    renderer.execute_sigil_overlay('STABILIZE_PROTOCOL', entropy=0.8, saturation=0.4, execution_power=0.9)
    time.sleep(1)
    
    renderer.execute_sigil_overlay('EMERGENCY_STABILIZE', entropy=0.9, saturation=0.8, execution_power=1.8)
    
    print("📊 Active overlays:", len(renderer.get_active_overlays()))
    print("📋 System status:", renderer.get_system_status())
    
    print("\n⏳ Running for 10 seconds...")
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        pass
    
    print("\n🛑 Stopping sigil overlay system...")
    renderer.stop_rendering()
    print("✅ Sigil overlay test complete") 