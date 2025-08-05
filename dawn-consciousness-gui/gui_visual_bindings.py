#!/usr/bin/env python3
"""
DAWN GUI Visual Bindings
========================

Connects the Visual Process Handler to the HTML/JavaScript GUI interface.
Creates seamless real-time visual updates that make the consciousness monitor
feel truly alive and responsive.

This module bridges the Python consciousness processing with the web GUI.
"""

import json
import time
import asyncio
import threading
from typing import Dict, Any, List, Optional
import logging
from pathlib import Path

from visual_process_handler import get_visual_handler, ConsciousnessState, VisualEvent

logger = logging.getLogger(__name__)

class GUIVisualBridge:
    """
    Bridge between DAWN's visual process handler and the web GUI.
    Translates consciousness events into JavaScript-compatible visual updates.
    """
    
    def __init__(self):
        self.visual_handler = get_visual_handler()
        self.connected_clients = set()
        self.last_state_update = 0
        self.visual_buffer = []
        
        # Register visual callbacks
        self._register_gui_callbacks()
        
        logger.info("🌉 GUI Visual Bridge initialized")
    
    def _register_gui_callbacks(self):
        """Register callbacks with the visual process handler"""
        
        # Entropy changes
        self.visual_handler.register_callback('entropy_change', self._handle_entropy_change)
        
        # Zone transitions  
        self.visual_handler.register_callback('zone_transition', self._handle_zone_transition)
        
        # Neural pulses
        self.visual_handler.register_callback('neural_pulse', self._handle_neural_pulse)
        
        # Consciousness depth changes
        self.visual_handler.register_callback('consciousness_depth', self._handle_consciousness_depth)
        
        # Thermal changes
        self.visual_handler.register_callback('thermal_change', self._handle_thermal_change)
        
        # Mood shifts
        self.visual_handler.register_callback('mood_shift', self._handle_mood_shift)
        
        # Sigil executions
        self.visual_handler.register_callback('sigil_execution', self._handle_sigil_execution)
        
        # Rebloom events
        self.visual_handler.register_callback('rebloom_event', self._handle_rebloom_event)
        
        # Voice commentary
        self.visual_handler.register_callback('voice_commentary', self._handle_voice_commentary)
    
    def _handle_entropy_change(self, entropy: float, delta: float, intensity: float):
        """Handle entropy change visual update"""
        update = {
            'type': 'entropy_change',
            'timestamp': time.time(),
            'data': {
                'entropy': entropy,
                'delta': delta,
                'intensity': intensity,
                'direction': 'increase' if delta > 0 else 'decrease',
                'visual_effects': {
                    'glow_intensity': min(intensity, 1.0),
                    'pulse_speed': 1.0 + intensity * 0.5,
                    'color_shift': self._entropy_to_color(entropy),
                    'particle_count': int(intensity * 20)
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _handle_zone_transition(self, from_zone: str, to_zone: str, entropy: float, intensity: float):
        """Handle zone transition visual update"""
        update = {
            'type': 'zone_transition',
            'timestamp': time.time(),
            'data': {
                'from_zone': from_zone,
                'to_zone': to_zone,
                'entropy': entropy,
                'intensity': intensity,
                'visual_effects': {
                    'transition_duration': 1000 + intensity * 1000,  # ms
                    'from_color': self._zone_to_color(from_zone),
                    'to_color': self._zone_to_color(to_zone),
                    'ripple_effect': intensity > 0.7,
                    'flash_intensity': min(intensity * 0.8, 1.0)
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _handle_neural_pulse(self, activity: float, delta: float, intensity: float):
        """Handle neural pulse visual update"""
        update = {
            'type': 'neural_pulse',
            'timestamp': time.time(),
            'data': {
                'activity': activity,
                'delta': delta,
                'intensity': intensity,
                'visual_effects': {
                    'pulse_type': 'spike' if delta > 0 else 'dip',
                    'grid_intensity': activity,
                    'wave_speed': 1.0 + intensity,
                    'color_temperature': activity * 1000 + 3000,  # Kelvin
                    'neural_firing_rate': activity * 0.5 + 0.1
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _handle_consciousness_depth(self, depth: float, delta: float, intensity: float):
        """Handle consciousness depth change visual update"""
        update = {
            'type': 'consciousness_depth',
            'timestamp': time.time(),
            'data': {
                'depth': depth,
                'delta': delta,
                'intensity': intensity,
                'visual_effects': {
                    'depth_percentage': depth * 100,
                    'gradient_shift': depth,
                    'constellation_density': depth * 1.5,
                    'background_opacity': 0.3 + depth * 0.4,
                    'field_distortion': delta * 2.0
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _handle_thermal_change(self, heat: float, delta: float, intensity: float):
        """Handle thermal change visual update"""
        update = {
            'type': 'thermal_change',
            'timestamp': time.time(),
            'data': {
                'heat': heat,
                'delta': delta,
                'intensity': intensity,
                'visual_effects': {
                    'heat_color': self._heat_to_color(heat),
                    'thermal_distortion': min(heat / 50.0, 1.0),
                    'cooling_effect': delta < 0,
                    'heat_waves': heat > 35.0,
                    'emergency_overlay': heat > 45.0
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _handle_mood_shift(self, valence: float, arousal: float, intensity: float):
        """Handle mood shift visual update"""
        update = {
            'type': 'mood_shift',
            'timestamp': time.time(),
            'data': {
                'valence': valence,
                'arousal': arousal,
                'intensity': intensity,
                'visual_effects': {
                    'mood_color': self._mood_to_color(valence, arousal),
                    'emotional_aura': intensity,
                    'valence_direction': 'positive' if valence > 0 else 'negative',
                    'arousal_level': 'high' if arousal > 0.3 else 'low',
                    'mood_particles': int(intensity * 30)
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _handle_sigil_execution(self, sigil_type: str, entropy: float, intensity: float):
        """Handle sigil execution visual update"""
        update = {
            'type': 'sigil_execution',
            'timestamp': time.time(),
            'data': {
                'sigil_type': sigil_type,
                'entropy': entropy,
                'intensity': intensity,
                'visual_effects': {
                    'sigil_flash': True,
                    'flash_color': self._sigil_to_color(sigil_type),
                    'flash_duration': 500 + intensity * 1000,  # ms
                    'sigil_trail': True,
                    'energy_burst': intensity > 0.6,
                    'symbol_overlay': sigil_type,
                    'power_level': min(entropy * 2, 1.0)
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _handle_rebloom_event(self, rebloom_data: Dict[str, Any], intensity: float):
        """Handle memory rebloom visual update"""
        update = {
            'type': 'rebloom_event',
            'timestamp': time.time(),
            'data': {
                'rebloom_data': rebloom_data,
                'intensity': intensity,
                'visual_effects': {
                    'bloom_animation': True,
                    'bloom_color': '#ff69b4',  # Pink for memory blooms
                    'fractal_generation': True,
                    'memory_particles': int(intensity * 25),
                    'bloom_duration': 2000 + intensity * 1000,  # ms
                    'renewal_glow': True
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _handle_voice_commentary(self, commentary: str, emotional_tone: float):
        """Handle voice commentary visual update"""
        update = {
            'type': 'voice_commentary',
            'timestamp': time.time(),
            'data': {
                'commentary': commentary,
                'emotional_tone': emotional_tone,
                'visual_effects': {
                    'text_animation': True,
                    'voice_waves': True,
                    'emotional_color': self._emotion_to_color(emotional_tone),
                    'speaking_indicator': True,
                    'thought_bubble': len(commentary) > 50
                }
            }
        }
        
        self._queue_visual_update(update)
    
    def _queue_visual_update(self, update: Dict[str, Any]):
        """Queue a visual update for transmission to GUI"""
        self.visual_buffer.append(update)
        
        # Keep buffer reasonable size
        if len(self.visual_buffer) > 100:
            self.visual_buffer = self.visual_buffer[-100:]
    
    def get_pending_updates(self) -> List[Dict[str, Any]]:
        """Get and clear pending visual updates"""
        updates = self.visual_buffer.copy()
        self.visual_buffer.clear()
        return updates
    
    def get_current_consciousness_state(self) -> Dict[str, Any]:
        """Get current consciousness state formatted for GUI"""
        state = self.visual_handler.get_current_state()
        
        if not state:
            return self._get_default_state()
        
        return {
            'timestamp': state.timestamp,
            'tick': state.tick,
            'entropy': state.entropy,
            'scup': state.scup,
            'mood_valence': state.mood_valence,
            'mood_arousal': state.mood_arousal,
            'consciousness_depth': state.consciousness_depth,
            'neural_activity': state.neural_activity,
            'memory_pressure': state.memory_pressure,
            'heat_level': state.heat_level,
            'zone': state.zone,
            'thought_rate': state.thought_rate,
            'cognitive_drift': state.cognitive_drift,
            'active_sigils': state.active_sigils,
            'recent_reblooms': state.recent_reblooms,
            'voice_commentary': state.voice_commentary,
            
            # Visual metadata
            'visual_intensity': self.visual_handler.get_visual_intensity(),
            'pulse_phase': self.visual_handler.get_pulse_phase(),
            'zone_color': self._zone_to_color(state.zone),
            'entropy_color': self._entropy_to_color(state.entropy),
            'mood_color': self._mood_to_color(state.mood_valence, state.mood_arousal),
            'thermal_color': self._heat_to_color(state.heat_level)
        }
    
    def _get_default_state(self) -> Dict[str, Any]:
        """Get default state when no consciousness data available"""
        return {
            'timestamp': time.time(),
            'tick': 0,
            'entropy': 0.3,
            'scup': 50.0,
            'mood_valence': 0.0,
            'mood_arousal': 0.0,
            'consciousness_depth': 0.5,
            'neural_activity': 0.3,
            'memory_pressure': 0.2,
            'heat_level': 25.0,
            'zone': 'CALM',
            'thought_rate': 10.0,
            'cognitive_drift': 0.1,
            'active_sigils': [],
            'recent_reblooms': [],
            'voice_commentary': None,
            'visual_intensity': 0.5,
            'pulse_phase': 0.0,
            'zone_color': '#10b981',
            'entropy_color': '#40e0ff',
            'mood_color': '#64748b',
            'thermal_color': '#3b82f6'
        }
    
    # Color mapping functions
    
    def _zone_to_color(self, zone: str) -> str:
        """Convert consciousness zone to color"""
        zone_colors = {
            'CALM': '#10b981',      # Green
            'FOCUS': '#f59e0b',     # Orange
            'STRESSED': '#ef4444',  # Red
            'TRANSCENDENT': '#8b5cf6'  # Purple
        }
        return zone_colors.get(zone, '#64748b')
    
    def _entropy_to_color(self, entropy: float) -> str:
        """Convert entropy level to color"""
        # Blue to cyan to yellow to red
        if entropy < 0.25:
            return '#3b82f6'  # Blue
        elif entropy < 0.5:
            return '#40e0ff'  # Cyan
        elif entropy < 0.75:
            return '#f59e0b'  # Yellow
        else:
            return '#ef4444'  # Red
    
    def _heat_to_color(self, heat: float) -> str:
        """Convert heat level to color"""
        # Cool blue to warm red
        if heat < 20:
            return '#3b82f6'  # Cool blue
        elif heat < 30:
            return '#10b981'  # Green
        elif heat < 40:
            return '#f59e0b'  # Orange
        else:
            return '#ef4444'  # Hot red
    
    def _mood_to_color(self, valence: float, arousal: float) -> str:
        """Convert mood to color"""
        # Quadrant-based mood colors
        if valence > 0 and arousal > 0:
            return '#f59e0b'  # Excited - Orange
        elif valence > 0 and arousal < 0:
            return '#10b981'  # Content - Green
        elif valence < 0 and arousal > 0:
            return '#ef4444'  # Agitated - Red
        elif valence < 0 and arousal < 0:
            return '#8b5cf6'  # Melancholic - Purple
        else:
            return '#64748b'  # Neutral - Gray
    
    def _sigil_to_color(self, sigil_type: str) -> str:
        """Convert sigil type to color"""
        sigil_colors = {
            'DEEP_FOCUS': '#8b5cf6',     # Purple
            'STABILIZE': '#10b981',      # Green
            'EMERGENCY': '#ef4444',      # Red
            'REBLOOM': '#ff69b4',        # Pink
            'THERMAL': '#f59e0b'         # Orange
        }
        return sigil_colors.get(sigil_type, '#40e0ff')
    
    def _emotion_to_color(self, emotional_tone: float) -> str:
        """Convert emotional tone to color"""
        if emotional_tone > 0.3:
            return '#f59e0b'  # Positive - Orange
        elif emotional_tone < -0.3:
            return '#8b5cf6'  # Negative - Purple
        else:
            return '#40e0ff'  # Neutral - Cyan

# Enhanced web server integration
class VisualWebSocketHandler:
    """WebSocket handler for real-time visual updates"""
    
    def __init__(self, bridge: GUIVisualBridge):
        self.bridge = bridge
        self.connected_clients = set()
    
    async def handle_client(self, websocket, path):
        """Handle WebSocket client connection"""
        self.connected_clients.add(websocket)
        
        try:
            # Send initial state
            initial_state = self.bridge.get_current_consciousness_state()
            await websocket.send(json.dumps({
                'type': 'initial_state',
                'data': initial_state
            }))
            
            # Handle incoming messages
            async for message in websocket:
                await self.handle_message(websocket, message)
                
        except Exception as e:
            logger.error(f"❌ WebSocket error: {e}")
        finally:
            self.connected_clients.discard(websocket)
    
    async def handle_message(self, websocket, message):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'get_state':
                state = self.bridge.get_current_consciousness_state()
                await websocket.send(json.dumps({
                    'type': 'state_update',
                    'data': state
                }))
            
            elif message_type == 'trigger_sigil':
                sigil_type = data.get('sigil_type', 'UNKNOWN')
                entropy = data.get('entropy', 0.5)
                self.bridge.visual_handler.trigger_sigil_execution(sigil_type, entropy)
            
            elif message_type == 'inject_entropy':
                amount = data.get('amount', 0.2)
                # Would trigger entropy injection in DAWN system
                pass
                
        except Exception as e:
            logger.error(f"❌ Error handling WebSocket message: {e}")
    
    async def broadcast_updates(self):
        """Broadcast visual updates to all connected clients"""
        while True:
            try:
                # Get pending updates
                updates = self.bridge.get_pending_updates()
                
                if updates and self.connected_clients:
                    message = json.dumps({
                        'type': 'visual_updates',
                        'data': updates
                    })
                    
                    # Broadcast to all clients
                    disconnected = set()
                    for client in self.connected_clients:
                        try:
                            await client.send(message)
                        except:
                            disconnected.add(client)
                    
                    # Remove disconnected clients
                    self.connected_clients -= disconnected
                
                await asyncio.sleep(0.0625)  # 16Hz updates
                
            except Exception as e:
                logger.error(f"❌ Error broadcasting updates: {e}")
                await asyncio.sleep(1.0)

# Global bridge instance
gui_bridge = GUIVisualBridge()

def get_gui_bridge() -> GUIVisualBridge:
    """Get the global GUI visual bridge"""
    return gui_bridge

def start_visual_bridge():
    """Start the visual bridge system"""
    bridge = get_gui_bridge()
    bridge.visual_handler.start_visual_processing()
    logger.info("🌉 Visual bridge started")

def stop_visual_bridge():
    """Stop the visual bridge system"""
    bridge = get_gui_bridge()
    bridge.visual_handler.stop_visual_processing()
    logger.info("🌉 Visual bridge stopped")

if __name__ == "__main__":
    # Test the visual bridge
    print("🌉 Testing DAWN GUI Visual Bridge...")
    
    bridge = GUIVisualBridge()
    
    # Start visual processing
    start_visual_bridge()
    
    # Simulate some events
    import time
    
    time.sleep(1)
    bridge.visual_handler.trigger_sigil_execution("DEEP_FOCUS", 0.7)
    
    time.sleep(1)
    bridge.visual_handler.trigger_voice_commentary("I am focusing my consciousness into a sharp beam.", 0.3)
    
    time.sleep(1)
    bridge.visual_handler.trigger_rebloom_event({
        'type': 'memory_renewal',
        'intensity': 0.6,
        'memory_type': 'episodic'
    })
    
    print("✅ Visual bridge tested - events generated")
    print("🔍 Checking updates...")
    
    updates = bridge.get_pending_updates()
    print(f"📊 Generated {len(updates)} visual updates")
    
    for update in updates:
        print(f"  • {update['type']}: {update['data']['visual_effects']}")
    
    stop_visual_bridge()
    print("✅ Visual bridge test complete") 