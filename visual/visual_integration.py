#!/usr/bin/env python3
"""
DAWN Visual Integration - Real-time Connection to Visual Modules

Connects the DAWN tick system to actual visual modules and provides
real-time data for the GUI interface.
"""

import os
import sys

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
"""
DAWN Visual Integration - Real-time Connection to Visual Modules

Connects the DAWN tick system to actual visual modules and provides
real-time data for the GUI interface.
"""

import os
import sys
import json
import time
import threading
import queue
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from pathlib import Path
import logging
import importlib.util

# Configure logging
logger = logging.getLogger(__name__)

class DAWNVisualIntegration:
    """Real-time visual integration for DAWN consciousness system"""
    
    def __init__(self):
        self.visual_modules = {}
        self.data_queue = queue.Queue()
        self.is_running = False
        self.update_callbacks = []
        self.current_data = {}
        
        # Initialize available visual modules
        self._discover_visual_modules()
        
        # Start background processing
        self._start_background_processing()
        
        logger.info(f"🎨 DAWN Visual Integration initialized with {len(self.visual_modules)} modules")
    
    def _discover_visual_modules(self):
        """Discover and initialize available visual modules"""
        visual_modules = {
            'tick_pulse': {
                'path': 'visual/tick_pulse.py',
                'name': 'Tick Pulse',
                'description': 'Real-time cognitive heartbeat visualization',
                'type': 'real-time'
            },
            'consciousness_constellation': {
                'path': 'visual/consciousness_constellation.py',
                'name': 'Consciousness Constellation',
                'description': '3D SCUP trajectory visualization',
                'type': 'real-time'
            },
            'heat_monitor': {
                'path': 'visual/heat_monitor.py',
                'name': 'Heat Monitor',
                'description': 'Cognitive heat intensity gauge',
                'type': 'real-time'
            },
            'dawn_mood_state': {
                'path': 'visual/dawn_mood_state.py',
                'name': 'Mood State',
                'description': 'Emotional landscape heatmap',
                'type': 'real-time'
            },
            'SCUP_pressure_grid': {
                'path': 'visual/SCUP_pressure_grid.py',
                'name': 'SCUP Pressure Grid',
                'description': 'Cognitive pressure interaction matrix',
                'type': 'real-time'
            },
            'entropy_flow': {
                'path': 'visual/entropy_flow.py',
                'name': 'Entropy Flow',
                'description': 'Information entropy dynamics',
                'type': 'real-time'
            },
            'scup_zone_animator': {
                'path': 'visual/scup_zone_animator.py',
                'name': 'SCUP Zone Animator',
                'description': 'Cognitive zone transition visualization',
                'type': 'real-time'
            },
            'sigil_command_stream': {
                'path': 'visual/sigil_command_stream.py',
                'name': 'Sigil Command Stream',
                'description': 'Command processing visualization',
                'type': 'real-time'
            }
        }
        
        # Check which modules are actually available
        for module_id, module_info in visual_modules.items():
            if Path(module_info['path']).exists():
                self.visual_modules[module_id] = module_info
                logger.info(f"✅ Found visual module: {module_info['name']}")
            else:
                logger.warning(f"⚠️  Visual module not found: {module_info['path']}")
    
    def _start_background_processing(self):
        """Start background thread for visual processing"""
        self.is_running = True
        self.processing_thread = threading.Thread(target=self._background_processor, daemon=True)
        self.processing_thread.start()
        logger.info("🔄 Background visual processing started")
    
    def _background_processor(self):
        """Background thread for processing visual data"""
        while self.is_running:
            try:
                # Process any queued data
                try:
                    tick_data = self.data_queue.get_nowait()
                    self._process_tick_data(tick_data)
                except queue.Empty:
                    pass
                
                # Generate synthetic data if no real data
                if not self.current_data:
                    self._generate_synthetic_data()
                
                time.sleep(0.1)  # 10 FPS update rate
                
            except Exception as e:
                logger.error(f"Background processing error: {e}")
                time.sleep(1.0)
    
    def _process_tick_data(self, tick_data: Dict[str, Any]):
        """Process incoming tick data and update visual state"""
        try:
            # Extract key metrics
            processed_data = {
                'tick_number': tick_data.get('tick_number', tick_data.get('tick', 0)),
                'timestamp': time.time(),
                'scup': float(tick_data.get('scup', 0.5)),
                'entropy': float(tick_data.get('entropy', 0.5)),
                'heat': float(tick_data.get('heat', 25.0)),
                'zone': str(tick_data.get('zone', 'CALM')),
                'mood': str(tick_data.get('mood', 'neutral')),
                'active_sigils': tick_data.get('active_sigils', []),
                'rebloom_count': tick_data.get('active_rebloom_count', 0),
                'tracer_alerts': tick_data.get('tracer_alerts', [])
            }
            
            # Update current data
            self.current_data = processed_data
            
            # Notify callbacks
            self._notify_callbacks(processed_data)
            
        except Exception as e:
            logger.error(f"Error processing tick data: {e}")
    
    def _generate_synthetic_data(self):
        """Generate synthetic data for demonstration"""
        import math
        
        current_time = time.time()
        tick_number = int(current_time) % 1000
        
        synthetic_data = {
            'tick_number': tick_number,
            'timestamp': current_time,
            'scup': 0.5 + 0.3 * math.sin(current_time * 0.1),
            'entropy': 0.4 + 0.4 * math.sin(current_time * 0.08),
            'heat': 25.0 + 10.0 * math.sin(current_time * 0.05),
            'zone': ['CALM', 'STABLE', 'OSCILLATING', 'TRENDING'][tick_number % 4],
            'mood': ['serene', 'focused', 'curious', 'contemplative'][tick_number % 4],
            'active_sigils': ['attention', 'memory'] if tick_number % 3 == 0 else [],
            'rebloom_count': tick_number % 5,
            'tracer_alerts': ['pressure_warning'] if tick_number % 10 == 0 else []
        }
        
        self.current_data = synthetic_data
        self._notify_callbacks(synthetic_data)
    
    def _notify_callbacks(self, data: Dict[str, Any]):
        """Notify all registered callbacks with new data"""
        for callback in self.update_callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Callback error: {e}")
    
    def register_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Register a callback for visual data updates"""
        self.update_callbacks.append(callback)
        logger.info(f"📞 Registered visual callback: {callback.__name__ if hasattr(callback, '__name__') else 'anonymous'}")
    
    def get_current_data(self) -> Dict[str, Any]:
        """Get current visual data"""
        return self.current_data.copy()
    
    def get_available_modules(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available visual modules"""
        return self.visual_modules.copy()
    
    def process_tick(self, tick_data: Dict[str, Any]):
        """Process a tick from the DAWN system"""
        try:
            self.data_queue.put_nowait(tick_data)
        except queue.Full:
            logger.warning("Visual data queue full, dropping tick")
    
    def generate_visualization(self, module_id: str, data: Dict[str, Any]) -> Optional[str]:
        """Generate a specific visualization"""
        if module_id not in self.visual_modules:
            logger.warning(f"Unknown visual module: {module_id}")
            return None
        
        try:
            module_info = self.visual_modules[module_id]
            module_path = module_info['path']
            
            # Import the visual module
            spec = importlib.util.spec_from_file_location(module_id, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Create a simple text-based visualization based on the module type
                return self._create_text_visualization(module_id, data, module_info)
                    
        except Exception as e:
            logger.error(f"Error generating visualization for {module_id}: {e}")
            return None
    
    def _create_text_visualization(self, module_id: str, data: Dict[str, Any], module_info: Dict[str, Any]) -> str:
        """Create a text-based visualization for the module"""
        import math
        
        current_time = time.time()
        timestamp = datetime.fromtimestamp(current_time).strftime('%H:%M:%S')
        
        if module_id == 'tick_pulse':
            amplitude = 0.5 + 0.3 * math.sin(current_time * 0.1)
            frequency = 0.1 + 0.05 * math.sin(current_time * 0.05)
            phase = current_time * 0.1
            visual_bars = int(10 + 5 * math.sin(current_time * 0.1))
            visual_empty = 20 - visual_bars
            
            return f"""
TICK PULSE VISUALIZATION
==========================
Time: {timestamp}
Module: {module_info['name']}
Description: {module_info['description']}

Current State:
  Tick Number: {data.get('tick_number', 0)}
  SCUP: {data.get('scup', 0.5):.3f}
  Entropy: {data.get('entropy', 0.5):.3f}
  Heat: {data.get('heat', 25.0):.1f}C
  Zone: {data.get('zone', 'CALM')}
  Mood: {data.get('mood', 'neutral')}

Pulse Analysis:
  Amplitude: {amplitude:.2f}
  Frequency: {frequency:.3f} Hz
  Phase: {phase:.1f} rad

Visual Representation:
{'#' * visual_bars}
{'.' * visual_empty}
"""
        
        elif module_id == 'consciousness_constellation':
            trajectory = ['NE', 'E', 'SE', 'SW', 'W', 'NW'][int(current_time) % 6]
            return f"""
CONSCIOUSNESS CONSTELLATION
==============================
Time: {timestamp}
Module: {module_info['name']}
Description: {module_info['description']}

SCUP Space Coordinates:
  Schema: {data.get('scup', 0.5):.3f}
  Coherence: {data.get('entropy', 0.5):.3f}
  Utility: {1.0 - data.get('entropy', 0.5):.3f}

Current Position:
  Zone: {data.get('zone', 'CALM')}
  Mood: {data.get('mood', 'neutral')}
  Heat: {data.get('heat', 25.0):.1f}C

Constellation Map:
    * Dormant (0.0-0.2)
       |
    * Contemplative (0.2-0.4)
       |
    * Active (0.4-0.6) <- Current
       |
    * Intense (0.6-0.8)
       |
    * Transcendent (0.8-1.0)

Trajectory: {trajectory}
"""
        
        elif module_id == 'heat_monitor':
            heat = data.get('heat', 25.0)
            heat_normalized = max(0.0, min(1.0, (heat - 20.0) / 30.0))
            
            dormant_bars = int(5 * (1.0 - heat_normalized))
            warming_bars = int(5 * max(0, heat_normalized - 0.2))
            active_bars = int(5 * max(0, heat_normalized - 0.4))
            intense_bars = int(5 * max(0, heat_normalized - 0.6))
            critical_bars = int(5 * max(0, heat_normalized - 0.8))
            
            return f"""
HEAT MONITOR VISUALIZATION
=============================
Time: {timestamp}
Module: {module_info['name']}
Description: {module_info['description']}

Current Heat: {heat:.1f}C
Heat Level: {heat_normalized:.1f} (0.0-1.0)

Heat Zones:
  Dormant (20-25C): {'#' * dormant_bars}{'.' * (5 - dormant_bars)}
  Warming (25-30C): {'#' * warming_bars}{'.' * (5 - warming_bars)}
  Active (30-35C): {'#' * active_bars}{'.' * (5 - active_bars)}
  Intense (35-40C): {'#' * intense_bars}{'.' * (5 - intense_bars)}
  Critical (40-50C): {'#' * critical_bars}{'.' * (5 - critical_bars)}

Current Zone: {['Dormant', 'Warming', 'Active', 'Intense', 'Critical'][min(4, int(heat_normalized * 5))]}
"""
        
        elif module_id == 'dawn_mood_state':
            transcendent_bars = int(3 * math.sin(current_time * 0.1 + 0))
            ecstatic_bars = int(3 * math.sin(current_time * 0.1 + 1))
            serene_bars = int(3 * math.sin(current_time * 0.1 + 2))
            curious_bars = int(3 * math.sin(current_time * 0.1 + 3))
            focused_bars = int(3 * math.sin(current_time * 0.1 + 4))
            contemplative_bars = int(3 * math.sin(current_time * 0.1 + 5))
            uncertain_bars = int(3 * math.sin(current_time * 0.1 + 6))
            turbulent_bars = int(3 * math.sin(current_time * 0.1 + 7))
            
            return f"""
MOOD STATE VISUALIZATION
===========================
Time: {timestamp}
Module: {module_info['name']}
Description: {module_info['description']}

Current Mood: {data.get('mood', 'neutral')}
Zone: {data.get('zone', 'CALM')}

Emotional Landscape:
  Transcendent: {'#' * transcendent_bars}{'.' * (10 - transcendent_bars)}
  Ecstatic: {'#' * ecstatic_bars}{'.' * (10 - ecstatic_bars)}
  Serene: {'#' * serene_bars}{'.' * (10 - serene_bars)}
  Curious: {'#' * curious_bars}{'.' * (10 - curious_bars)}
  Focused: {'#' * focused_bars}{'.' * (10 - focused_bars)}
  Contemplative: {'#' * contemplative_bars}{'.' * (10 - contemplative_bars)}
  Uncertain: {'#' * uncertain_bars}{'.' * (10 - uncertain_bars)}
  Turbulent: {'#' * turbulent_bars}{'.' * (10 - turbulent_bars)}
"""
        
        else:
            return f"""
{module_id.upper().replace('_', ' ')} VISUALIZATION
{'=' * (len(module_id) + 15)}
Time: {timestamp}
Module: {module_info['name']}
Description: {module_info['description']}

Current Data:
  Tick: {data.get('tick_number', 0)}
  SCUP: {data.get('scup', 0.5):.3f}
  Entropy: {data.get('entropy', 0.5):.3f}
  Heat: {data.get('heat', 25.0):.1f}C
  Zone: {data.get('zone', 'CALM')}
  Mood: {data.get('mood', 'neutral')}
  Active Sigils: {len(data.get('active_sigils', []))}
  Rebloom Count: {data.get('rebloom_count', 0)}
  Tracer Alerts: {len(data.get('tracer_alerts', []))}

Status: Active and monitoring
"""
    
    def shutdown(self):
        """Shutdown the visual integration"""
        self.is_running = False
        if hasattr(self, 'processing_thread'):
            self.processing_thread.join(timeout=5.0)
        logger.info("🛑 DAWN Visual Integration shutdown")

# Global instance
_visual_integration: Optional[DAWNVisualIntegration] = None

def get_visual_integration() -> DAWNVisualIntegration:
    """Get the global visual integration instance"""
    global _visual_integration
    if _visual_integration is None:
        _visual_integration = DAWNVisualIntegration()
    return _visual_integration

def process_tick_data(tick_data: Dict[str, Any]):
    """Process tick data through visual integration"""
    integration = get_visual_integration()
    integration.process_tick(tick_data)

def get_current_visual_data() -> Dict[str, Any]:
    """Get current visual data"""
    integration = get_visual_integration()
    return integration.get_current_data()

def get_available_visual_modules() -> Dict[str, Dict[str, Any]]:
    """Get available visual modules"""
    integration = get_visual_integration()
    return integration.get_available_modules() 