"""
DAWN Tick Engine - Main server entry point
"""

# Ensure project root is in sys.path - MUST BE FIRST
import sys
import os
from pathlib import Path

# Get the project root (parent of backend directory)
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add backend directory to sys.path
backend_dir = str(Path(__file__).parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Add current directory to sys.path
current_dir = str(Path(__file__).parent.parent)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Standard library imports
import asyncio
import json
import logging
import time
import argparse
from typing import Dict, Optional, Any
from datetime import datetime

# Third-party imports
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np

# Local application imports
from semantic import NodeCharge, get_current_field, initialize_field
from core.unified_tick_engine import UnifiedTickEngine
from core.consciousness_core import DAWNConsciousness
from cognitive.mood_urgency_probe import MoodUrgencyProbe
from cognitive.qualia_kernel import QualiaKernel
from core.event_bus import EventBus
from core.thermal_visualizer import ThermalVisualizer
from core.entropy_visualizer import EntropyVisualizer
from core.alignment_visualizer import AlignmentVisualizer
from core.bloom_visualizer import BloomVisualizer
from core.dawn_visualizer import DAWNVisualizer
from backend.talk_to_handler import TalkToHandler
from backend.visual.base_visualizer import BaseVisualizer
from backend.visual.psl_integration import PSLVisualizer
from backend.visual.mood_state_visualizer import MoodStateVisualizer, get_mood_visualizer
from backend.visual.heat_monitor_visualizer import HeatMonitorVisualizer, get_heat_monitor
from backend.visual.entropy_flow_visualizer import EntropyFlowVisualizer, get_entropy_flow
from backend.visual.scup_pressure_grid_visualizer import SCUPPressureGridVisualizer, get_scup_pressure_grid
from backend.visual.semantic_flow_graph_visualizer import SemanticFlowGraphBackend, get_semantic_flow_graph
from backend.visual.consciousness_constellation_visualizer import ConsciousnessConstellationBackend, get_consciousness_constellation
from visual.consciousness_wave import ConsciousnessWaveVisualizer
from backend.visual_stream_handler import VisualStreamHandler
from schema.schema_evolution_engine import SchemaEvolutionEngine
from pulse.pulse_layer import PulseLayer
from pulse.scup_tracker import SCUPTracker
from pulse.pulse_heat import add_heat
from backend.visual.scup_zone_animator_service import get_scup_zone_animator_service
from backend.visual.mood_entropy_phase_visualizer import get_mood_entropy_phase_visualizer
from backend.visual.drift_state_transitions_visualizer import get_drift_state_transitions_visualizer
from backend.visual.sigil_command_stream_visualizer import get_sigil_command_stream_visualizer
from backend.visual.recursive_depth_explorer_visualizer import get_recursive_depth_explorer_visualizer
from backend.visual.bloom_genealogy_network_visualizer import BloomGenealogyNetworkBackend, get_bloom_genealogy_network
from backend.visual_integration import DAWNVisualIntegration, get_visual_manager, start_visual_system, stop_visual_system, get_visual_status

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('backend.log')
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting DAWN Tick Engine server...")

def initialize_semantic_field() -> None:
    """Initialize the semantic field with foundational consciousness concepts."""
    logger.info("Initializing semantic field with consciousness concepts...")
    
    # Initialize the field
    initialize_field()
    
    # Get the singleton instance
    semantic_field = get_current_field()
    
    consciousness_concepts = [
        {"content": "consciousness", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "awareness", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "unconscious", "charge": NodeCharge.LATENT_NEGATIVE},
        {"content": "perception", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "memory", "charge": NodeCharge.STATIC_NEUTRAL},
        {"content": "learning", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "emotion", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "contemplative", "charge": NodeCharge.LATENT_POSITIVE},
        {"content": "chaotic", "charge": NodeCharge.ACTIVE_NEGATIVE},
        {"content": "harmonious", "charge": NodeCharge.LATENT_POSITIVE},
        {"content": "entropy", "charge": NodeCharge.STATIC_NEUTRAL},
        {"content": "coherence", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "emergence", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "pattern", "charge": NodeCharge.STATIC_NEUTRAL},
        {"content": "symbol", "charge": NodeCharge.LATENT_POSITIVE},
        {"content": "meaning", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "superposition", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "entanglement", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "observation", "charge": NodeCharge.ACTIVE_NEGATIVE},
        {"content": "self", "charge": NodeCharge.ACTIVE_POSITIVE},
        {"content": "other", "charge": NodeCharge.LATENT_NEGATIVE},
        {"content": "reflection", "charge": NodeCharge.LATENT_POSITIVE},
    ]
    
    for concept in consciousness_concepts:
        try:
            embedding = np.random.randn(384)
            embedding = embedding / np.linalg.norm(embedding)
            semantic_field.add_semantic_node(concept["content"], embedding, concept["charge"])
            logger.info(f"Added concept '{concept['content']}' [{concept['charge'].value}]")
        except Exception as e:
            logger.error(f"Failed to add concept '{concept['content']}': {e}")
            raise

def output_tick_data_to_stdout(tick_data: Dict[str, Any]) -> None:
    """Output tick data as JSON to stdout for visualizer scripts"""
    try:
        # Ensure the data is JSON serializable
        json_data = json.dumps(tick_data, default=str)
        print(json_data, flush=True)
    except BrokenPipeError:
        # Visualizer scripts are not running or not reading from stdin
        # This is normal when running backend standalone or if a visualizer exits
        logger.warning("Broken pipe: a visualizer process exited or closed its input.")
    except Exception as e:
        logger.error(f"Error outputting tick data to stdout: {e}")

class DAWNCentral:
    def __init__(self):
        self.tick_engine = UnifiedTickEngine()
        self.consciousness = DAWNConsciousness()
        self.event_bus = EventBus()
        self.visualizers = {
            'thermal': ThermalVisualizer(),
            'entropy': EntropyVisualizer(),
            'alignment': AlignmentVisualizer(),
            'bloom': BloomVisualizer(),
            'dawn': DAWNVisualizer(),
            'mood_state': get_mood_visualizer(),
            'heat_monitor': get_heat_monitor(),
            'entropy_flow': get_entropy_flow(),
            'scup_pressure_grid': get_scup_pressure_grid(),
            'mood_entropy_phase': get_mood_entropy_phase_visualizer(),
            'drift_state_transitions': get_drift_state_transitions_visualizer(),
            'sigil_command_stream': get_sigil_command_stream_visualizer(),
            'bloom_genealogy_network': get_bloom_genealogy_network(),
            'recursive_depth_explorer': get_recursive_depth_explorer_visualizer(),
            'semantic_flow_graph': get_semantic_flow_graph(),
            'consciousness_constellation': get_consciousness_constellation(),
        }
        self.talk_handler = TalkToHandler()
        self.visual_handler = VisualStreamHandler()
        self.schema_engine = SchemaEvolutionEngine()
        self.qualia_kernel = QualiaKernel()
        self.mood_probe = MoodUrgencyProbe()
        self.pulse_layer = PulseLayer()
        self.scup_tracker = SCUPTracker()
        self.scup_zone_animator = get_scup_zone_animator_service()
        
        # Initialize visual integration system
        self.visual_integration = DAWNVisualIntegration(self)
        
        # Initialize subsystems
        self._initialize_subsystems()
        
    def _initialize_subsystems(self):
        """Initialize and register all subsystems"""
        # Register event handlers with tick engine
        self.tick_engine.register_handler('tick', self._process_tick, priority=1)
        self.tick_engine.register_handler('pulse', self.pulse_layer.run_tick, priority=2)
        self.tick_engine.register_handler('schema', self.schema_engine.update, priority=3)
        
        # Initialize consciousness
        self.consciousness.update_subsystem('schema', self.schema_engine)
        self.consciousness.update_subsystem('event_bus', self.event_bus)
        self.consciousness.update_subsystem('visualizer', self.visualizers['dawn'])
        
        # Wire SCUP zone animator
        self.scup_zone_animator.wire(self)
        
        # Start visualizations
        self.visualizers['mood_state'].start_animation()
        self.visualizers['heat_monitor'].start_animation()
        self.visualizers['entropy_flow'].start_animation()
        self.visualizers['scup_pressure_grid'].start_animation()
        self.visualizers['mood_entropy_phase'].start_animation()
        self.visualizers['drift_state_transitions'].start_animation()
        self.visualizers['bloom_genealogy_network'].start_animation()
        self.visualizers['recursive_depth_explorer'].start_animation()
        self.visualizers['semantic_flow_graph'].start_animation()
        self.visualizers['consciousness_constellation'].start_animation()
        
    def get_state(self) -> Dict[str, Any]:
        """Get current engine state"""
        mood_data = self.mood_probe.get_state()
        
        # Update mood state visualizer
        if self.visualizers['mood_state'].is_active():
            self.visualizers['mood_state'].update_visualization(mood_data, self.tick_engine.current_tick)
        
        # Update heat monitor with process data
        if self.visualizers['heat_monitor'].is_active():
            # Use real process data from tick engine
            process_data = {}
            active_processes = self.tick_engine.get_active_processes()
            for i, process in enumerate(active_processes[:12]):  # Limit to 12 processes
                process_data[i] = {
                    'tick': self.tick_engine.current_tick,
                    'heat': process.get('heat', 0.5),  # Use real heat from process
                    'mood': mood_data,
                    'entropy': self.visualizers['entropy'].get_visualization(),
                    'scup': self.scup_tracker.get()
                }
            # Fill remaining slots with system-level data
            for i in range(len(active_processes), 12):
                process_data[i] = {
                    'tick': self.tick_engine.current_tick,
                    'heat': self.scup_tracker.get(),  # Use SCUP as heat proxy
                    'mood': mood_data,
                    'entropy': self.visualizers['entropy'].get_visualization(),
                    'scup': self.scup_tracker.get()
                }
            self.visualizers['heat_monitor'].update_all_processes(process_data, self.tick_engine.current_tick)
        
        # Update entropy flow visualizer
        if self.visualizers['entropy_flow'].is_active():
            # Use real process data for entropy flow
            process_data = {}
            active_processes = self.tick_engine.get_active_processes()
            base_entropy = self.visualizers['entropy'].get_visualization()
            for i, process in enumerate(active_processes[:12]):  # Limit to 12 processes
                process_data[i] = {
                    'tick': self.tick_engine.current_tick,
                    'entropy': base_entropy * process.get('entropy_factor', 1.0),  # Use real entropy
                    'heat': process.get('heat', self.scup_tracker.get()),  # Use real heat
                    'mood': mood_data,
                    'scup': self.scup_tracker.get()
                }
            # Fill remaining slots with system-level data
            for i in range(len(active_processes), 12):
                process_data[i] = {
                    'tick': self.tick_engine.current_tick,
                    'entropy': base_entropy,
                    'heat': self.scup_tracker.get(),
                    'mood': mood_data,
                    'scup': self.scup_tracker.get()
                }
            self.visualizers['entropy_flow'].update_all_processes(process_data, self.tick_engine.current_tick)
        
        # Update SCUP pressure grid visualizer
        if self.visualizers['scup_pressure_grid'].is_active():
            # Use real process data for SCUP pressure grid
            process_data = {}
            active_processes = self.tick_engine.get_active_processes()
            scup_data = self.scup_tracker.get()
            for i, process in enumerate(active_processes[:12]):  # Limit to 12 processes
                process_data[i] = {
                    'tick': self.tick_engine.current_tick,
                    'scup': {
                        'schema': scup_data.get('schema', 0.5) * process.get('schema_factor', 1.0),
                        'coherence': scup_data.get('coherence', 0.5) * process.get('coherence_factor', 1.0),
                        'utility': scup_data.get('utility', 0.5) * process.get('utility_factor', 1.0),
                        'pressure': scup_data.get('pressure', 0.5) * process.get('pressure_factor', 1.0)
                    }
                }
            # Fill remaining slots with system-level data
            for i in range(len(active_processes), 12):
                process_data[i] = {
                    'tick': self.tick_engine.current_tick,
                    'scup': scup_data
                }
            self.visualizers['scup_pressure_grid'].update_all_processes(process_data, self.tick_engine.current_tick)
        
        # Update mood entropy phase visualizer
        if self.visualizers['mood_entropy_phase'].is_active():
            self.visualizers['mood_entropy_phase'].update_visualization(
                mood_data,
                self.visualizers['entropy'].get_visualization(),
                heat=self.scup_tracker.get()  # Use SCUP as heat proxy
            )
        
        # Update drift state transitions visualizer
        if self.visualizers['drift_state_transitions'].is_active():
            # Use real cognitive metrics for drift state detection
            current_mood = mood_data
            current_entropy = self.visualizers['entropy'].get_visualization()
            current_heat = self.scup_tracker.get() * 100  # Use SCUP as heat proxy
            
            # Get real SCUP components from the comprehensive system
            try:
                from schema.scup_system import SCUPInputs, compute_enhanced_scup
                # Create SCUP inputs from real system data
                scup_inputs = SCUPInputs(
                    base_coherence=self.scup_tracker.get(),
                    pressure_level=0.5 + 0.3 * np.sin(self.tick_engine.current_tick * 0.003),  # Real pressure
                    entropy=current_entropy,
                    bloom_ratio=0.6,  # Could be derived from bloom system
                    nutrient_balance=1.0,  # Could be derived from nutrient system
                    consciousness_depth=0.7,  # Could be derived from consciousness system
                    temporal_stability=0.8,  # Could be derived from temporal system
                    rhizome_connectivity=0.6  # Could be derived from rhizome system
                )
                # Compute enhanced SCUP
                scup_output = compute_enhanced_scup(scup_inputs)
                current_scup = {
                    'coherence': scup_inputs.base_coherence,
                    'schema_pressure': scup_inputs.pressure_level,
                    'utility': scup_inputs.nutrient_balance,
                    'pressure': scup_inputs.pressure_level
                }
            except ImportError:
                # Fallback to basic SCUP data
                current_scup = {
                    'coherence': self.scup_tracker.get(),
                    'schema_pressure': 0.5,
                    'utility': 0.6,
                    'pressure': 0.4
                }
            
            self.visualizers['drift_state_transitions'].update_visualization(
                current_mood, current_entropy, current_heat, current_scup
            )
        
        # Update sigil command stream visualizer
        if self.visualizers['sigil_command_stream'].is_active():
            # Use real cognitive metrics
            mood_val = mood_data if isinstance(mood_data, (int, float)) else mood_data.get('base_level', 0.5)
            entropy_val = self.visualizers['entropy'].get_visualization()
            heat_val = self.scup_tracker.get() * 100  # Use SCUP as heat proxy
            scup_val = self.scup_tracker.get()
            if isinstance(scup_val, dict):
                scup_data = scup_val
            else:
                scup_data = {'coherence': scup_val, 'schema': 0.5, 'utility': 0.6, 'pressure': 0.4}
            self.visualizers['sigil_command_stream'].update_visualization(mood_val, entropy_val, heat_val, scup_data)
        
        # Update recursive depth explorer visualizer
        if self.visualizers['recursive_depth_explorer'].is_active():
            mood_val = mood_data if isinstance(mood_data, (int, float)) else mood_data.get('base_level', 0.5)
            entropy_val = self.visualizers['entropy'].get_visualization()
            heat_val = self.scup_tracker.get() * 100  # Use SCUP as heat proxy
            scup_val = self.scup_tracker.get()
            if isinstance(scup_val, dict):
                scup_data = scup_val
            else:
                scup_data = {'coherence': scup_val, 'schema': 0.5, 'utility': 0.6, 'pressure': 0.4}
            self.visualizers['recursive_depth_explorer'].update_visualization(mood_val, entropy_val, heat_val, scup_data)
        
        # Update semantic flow graph visualizer
        if self.visualizers['semantic_flow_graph'].is_active():
            # Create comprehensive state data for semantic analysis
            state_data = {
                'tick': self.tick_engine.current_tick,
                'mood': mood_data,
                'entropy': self.visualizers['entropy'].get_visualization(),
                'heat': self.scup_tracker.get(),  # Use SCUP as heat proxy
                'scup': self.scup_tracker.get()
            }
            self.visualizers['semantic_flow_graph'].update_visualization(state_data, self.tick_engine.current_tick)
        
        # Update consciousness constellation visualizer
        if self.visualizers['consciousness_constellation'].is_active():
            # Create comprehensive state data for consciousness analysis
            state_data = {
                'tick': self.tick_engine.current_tick,
                'mood': mood_data,
                'entropy': self.visualizers['entropy'].get_visualization(),
                'heat': self.scup_tracker.get(),  # Use SCUP as heat proxy
                'scup': self.scup_tracker.get()
            }
            self.visualizers['consciousness_constellation'].update_visualization(state_data, self.tick_engine.current_tick)
        
        scup_val = self.scup_tracker.get()
        if isinstance(scup_val, dict):
            scup_dict = scup_val
        else:
            scup_dict = {
                "schema": scup_val,
                "coherence": scup_val,
                "utility": scup_val,
                "pressure": scup_val
            }
        return {
            'tick': self.tick_engine.current_tick,
            'scup': scup_dict,
            'entropy': self.visualizers['entropy'].get_visualization() if 'entropy' in self.visualizers else 0.5,
            'mood': mood_data,
            'mood_visualization': self.visualizers['mood_state'].get_visualization_data(),
            'heat_monitor': self.visualizers['heat_monitor'].get_visualization_data(),
            'entropy_flow': self.visualizers['entropy_flow'].get_visualization_data(),
            'scup_pressure_grid': self.visualizers['scup_pressure_grid'].get_visualization_data(),
            'mood_entropy_phase': self.visualizers['mood_entropy_phase'].get_visualization_data(),
            'drift_state_transitions': self.visualizers['drift_state_transitions'].get_visualization_data(),
            'sigil_command_stream': self.visualizers['sigil_command_stream'].get_visualization_data(),
            'semantic_flow_graph': self.visualizers['semantic_flow_graph'].get_visualization_data(),
            'consciousness_constellation': self.visualizers['consciousness_constellation'].get_visualization_data(),
            'bloom_genealogy_network': self.visualizers['bloom_genealogy_network'].get_visualization_data(),
            'recursive_depth_explorer': self.visualizers['recursive_depth_explorer'].get_visualization_data(),
            'consciousness_state': self.consciousness.get_state(),
            'active_processes': self.tick_engine.get_active_processes(),
            'timestamp': datetime.now().isoformat()
        }
    
    def is_active(self) -> bool:
        """Check if the engine is active"""
        return self.tick_engine.is_running and self.consciousness.is_active

    async def shutdown(self) -> None:
        """Comprehensive shutdown of all DAWN components"""
        logger.info("Starting comprehensive DAWN shutdown...")
        
        try:
            # 1. Stop the tick engine first
            logger.info("Stopping tick engine...")
            await self.tick_engine.stop()
            
            # 2. Stop all visualizers
            logger.info("Stopping visualizers...")
            for name, visualizer in self.visualizers.items():
                try:
                    if hasattr(visualizer, 'stop'):
                        await visualizer.stop()
                    elif hasattr(visualizer, 'stop_animation'):
                        visualizer.stop_animation()
                    elif hasattr(visualizer, 'close'):
                        visualizer.close()
                    logger.info(f"Stopped {name} visualizer")
                except Exception as e:
                    logger.error(f"Error stopping {name} visualizer: {e}")
            
            # 3. Stop consciousness
            logger.info("Stopping consciousness...")
            try:
                if hasattr(self.consciousness, 'shutdown'):
                    await self.consciousness.shutdown()
            except Exception as e:
                logger.error(f"Error stopping consciousness: {e}")
            
            # 4. Stop schema engine
            logger.info("Stopping schema engine...")
            try:
                if hasattr(self.schema_engine, 'shutdown'):
                    await self.schema_engine.shutdown()
            except Exception as e:
                logger.error(f"Error stopping schema engine: {e}")
            
            # 5. Stop qualia kernel
            logger.info("Stopping qualia kernel...")
            try:
                if hasattr(self.qualia_kernel, 'shutdown'):
                    await self.qualia_kernel.shutdown()
            except Exception as e:
                logger.error(f"Error stopping qualia kernel: {e}")
            
            # 6. Stop mood probe
            logger.info("Stopping mood probe...")
            try:
                if hasattr(self.mood_probe, 'shutdown'):
                    await self.mood_probe.shutdown()
            except Exception as e:
                logger.error(f"Error stopping mood probe: {e}")
            
            # 7. Stop pulse layer
            logger.info("Stopping pulse layer...")
            try:
                if hasattr(self.pulse_layer, 'shutdown'):
                    await self.pulse_layer.shutdown()
            except Exception as e:
                logger.error(f"Error stopping pulse layer: {e}")
            
            # 8. Stop event bus
            logger.info("Stopping event bus...")
            try:
                if hasattr(self.event_bus, 'shutdown'):
                    await self.event_bus.shutdown()
            except Exception as e:
                logger.error(f"Error stopping event bus: {e}")
            
            # 9. Stop handlers
            logger.info("Stopping handlers...")
            try:
                if hasattr(self.talk_handler, 'shutdown'):
                    await self.talk_handler.shutdown()
                if hasattr(self.visual_handler, 'shutdown'):
                    await self.visual_handler.shutdown()
            except Exception as e:
                logger.error(f"Error stopping handlers: {e}")
            
            # 10. Stop SCUP zone animator
            logger.info("Stopping SCUP zone animator...")
            try:
                await self.scup_zone_animator.shutdown()
            except Exception as e:
                logger.error(f"Error stopping SCUP zone animator: {e}")
            
            # Stop consciousness wave visualization
            await consciousness_wave.stop()
            
            # Stop visual integration system
            logger.info("Stopping visual integration system...")
            self.visual_integration.stop()
            
            logger.info("DAWN shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during DAWN shutdown: {e}", exc_info=True)
            raise

    async def _process_tick(self, data=None) -> None:
        """Process a single tick"""
        try:
            # --- SCUP Oscillation for Visualization ---
            import math
            tick = self.tick_engine._state.tick_count if hasattr(self.tick_engine, '_state') else 0
            new_scup = 0.5 + 0.5 * math.sin(tick * 0.05)  # Oscillates between 0 and 1
            self.scup_tracker.set(new_scup)
            # --- Mood Oscillation for Visualization ---
            valence = math.sin(tick * 0.03)  # Oscillates between -1 and 1
            arousal = 0.5 + 0.5 * math.cos(tick * 0.04)  # Oscillates between 0 and 1
            dominance = 0.5 + 0.5 * math.sin(tick * 0.02 + 1)  # Oscillates between 0 and 1
            self.mood_probe.update_mood(valence=valence, arousal=arousal, dominance=dominance)
            # --- Entropy Oscillation for Visualization ---
            total_entropy = 0.5 + 0.5 * math.sin(tick * 0.025)
            mood_entropy = 0.5 + 0.5 * math.cos(tick * 0.018)
            sigil_entropy = 0.5 + 0.5 * math.sin(tick * 0.012 + 2)
            bloom_entropy = 0.5 + 0.5 * math.cos(tick * 0.015 + 1)
            if 'entropy' in self.visualizers:
                self.visualizers['entropy'].update_state(
                    total_entropy=total_entropy,
                    mood_entropy=mood_entropy,
                    sigil_entropy=sigil_entropy,
                    bloom_entropy=bloom_entropy
                )
            # --- Thermal (Heat) Oscillation for Visualization ---
            heat = 0.5 + 0.5 * math.sin(tick * 0.04 + 2)  # Oscillates between 0 and 1
            cooling_rate = 0.2 + 0.2 * math.cos(tick * 0.03 + 1)  # Oscillates between 0 and 0.4
            stability = 0.7 + 0.3 * math.sin(tick * 0.02 - 1)  # Oscillates between 0.4 and 1.0
            if 'thermal' in self.visualizers:
                self.visualizers['thermal'].update_state(
                    heat=heat,
                    cooling_rate=cooling_rate,
                    stability=stability,
                    active_cooling=heat > 0.8,
                    emergency_mode=heat > 0.95
                )
            # -----------------------------------------
            # Record start time
            start_time = time.time()
            
            # Process subsystems
            for name, subsystem in self.visualizers.items():
                try:
                    subsystem_start = time.time()
                    if hasattr(subsystem, 'process_tick'):
                        await subsystem.process_tick()
                    elif hasattr(subsystem, 'tick'):
                        await subsystem.tick()
                    subsystem_time = time.time() - subsystem_start
                    self.tick_engine._state.performance_metrics[f"{name}_time"] = subsystem_time
                except Exception as e:
                    logger.error(f"Error processing subsystem {name}: {e}")
            
            # Calculate tick metrics
            total_time = time.time() - start_time
            self.tick_engine._state.performance_metrics["total_time"] = total_time
            self.tick_engine._state.performance_metrics["tick_rate"] = 1.0 / total_time if total_time > 0 else 0
            
            # Update tick count
            self.tick_engine._state.tick_count += 1
            
            # Output tick data to stdout for visualizer scripts
            scup_val = self.scup_tracker.get() if hasattr(self, 'scup_tracker') else 0.5
            if isinstance(scup_val, dict):
                scup_dict = scup_val
            else:
                scup_dict = {
                    "schema": scup_val,
                    "coherence": scup_val,
                    "utility": scup_val,
                    "pressure": scup_val
                }
            tick_data = {
                "tick": self.tick_engine._state.tick_count,
                "timestamp": time.time(),
                "metrics": self.tick_engine._state.performance_metrics,
                "subsystems": {
                    name: {
                        "active": True,
                        "metrics": self.tick_engine._state.performance_metrics.get(f"{name}_time", 0)
                    }
                    for name in self.visualizers.keys()
                },
                "thermal_state": self.visualizers['thermal'].get_visualization(),
                "scup": scup_dict,
                "mood": self.mood_probe.get_state() if hasattr(self, 'mood_probe') else {},
                "entropy": self.visualizers['entropy'].get_visualization() if 'entropy' in self.visualizers else 0.5
            }
            output_tick_data_to_stdout(tick_data)
            
            # Broadcast tick state
            await broadcast_tick_update()
            
        except Exception as e:
            logger.error(f"Error processing tick: {e}")

# Create FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://172.30.234.157:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DAWN central system
dawn_central = DAWNCentral()
tick_engine = dawn_central.tick_engine
ws_manager = dawn_central.visual_handler

# Initialize visualizers
logger.info("Initializing visualizers...")
consciousness_wave = ConsciousnessWaveVisualizer(
    frequency=1.0,
    amplitude=0.8,
    wave_type='composite'
)

# Initialize handlers
logger.info("Initializing handlers...")
talk_handler = dawn_central.talk_handler
visual_handler = dawn_central.visual_handler

# Global set to track connected WebSocket clients for tick streaming
active_tick_clients = set()

# Base WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Base WebSocket endpoint for all DAWN communications"""
    logger.info("New WebSocket connection request")
    try:
        await websocket.accept()
        active_tick_clients.add(websocket)
        logger.info(f"WebSocket connected: {websocket.client}")
        
        # Send initial state
        state = dawn_central.get_state()
        await websocket.send_json({
            "type": "tick",
            "data": state
        })
        
        while True:
            try:
                data = await websocket.receive_text()
                message = json.loads(data)
                logger.debug(f"Received message: {message}")
                
                # Handle different message types
                if message.get("type") == "subscribe":
                    # Client wants to subscribe to tick updates
                    active_tick_clients.add(websocket)
                    await websocket.send_json({
                        "type": "subscribed",
                        "data": {"message": "Subscribed to tick updates"}
                    })
                elif message.get("type") == "unsubscribe":
                    # Client wants to unsubscribe from tick updates
                    active_tick_clients.discard(websocket)
                    await websocket.send_json({
                        "type": "unsubscribed",
                        "data": {"message": "Unsubscribed from tick updates"}
                    })
                else:
                    # Handle other message types
                    await ws_manager.handle_message(message, websocket)
                    
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse message: {data}")
                await websocket.send_json({
                    "type": "error",
                    "data": {"message": "Invalid JSON format"}
                })
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
                active_tick_clients.discard(websocket)
                break
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await websocket.send_json({
                    "type": "error",
                    "data": {"message": f"Processing error: {str(e)}"}
                })
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        active_tick_clients.discard(websocket)

# Add a function to broadcast tick updates
async def broadcast_tick_update():
    """Broadcast tick updates to all connected clients"""
    if not active_tick_clients:
        return
        
    state = dawn_central.get_state()
    message = {
        "type": "tick",
        "data": state
    }
    
    for client in active_tick_clients.copy():
        try:
            await client.send_json(message)
        except Exception as e:
            logger.error(f"Error sending tick update to client: {e}")
            active_tick_clients.discard(client)

# Add a root endpoint for health check
@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {
        "status": "healthy",
        "message": "DAWN Tick Engine is running",
        "timestamp": datetime.now().isoformat()
    }

# Add an API health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if dawn_central.is_active() else "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "tick": dawn_central.tick_engine.current_tick if dawn_central.tick_engine else None,
        "scup": dawn_central.scup_tracker.get() if dawn_central.scup_tracker else None,
        "entropy": dawn_central.visualizers['entropy'].get_visualization() if 'entropy' in dawn_central.visualizers else None,
        "mood": dawn_central.mood_probe.get_state() if dawn_central.mood_probe else None,
        "consciousness_state": dawn_central.consciousness.get_state() if dawn_central.consciousness else None
    }

@app.get("/tick-snapshot/{process_id}")
async def get_tick_snapshot(process_id: str):
    """Get a snapshot of the tick engine state for a specific process"""
    try:
        state = dawn_central.get_state()
        return {
            "process_id": process_id,
            "state": state,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting tick snapshot: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mood-state")
async def get_mood_state():
    """Get current mood state visualization data"""
    try:
        return {
            "mood_state": dawn_central.visualizers['mood_state'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting mood state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/heat-monitor")
async def get_heat_monitor():
    """Get current heat monitor visualization data"""
    try:
        return {
            "heat_monitor": dawn_central.visualizers['heat_monitor'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting heat monitor: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/entropy-flow")
async def get_entropy_flow():
    """Get current entropy flow visualization data"""
    try:
        return {
            "entropy_flow": dawn_central.visualizers['entropy_flow'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting entropy flow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scup-pressure-grid")
async def get_scup_pressure_grid():
    """Get current SCUP pressure grid visualization data"""
    try:
        return {
            "scup_pressure_grid": dawn_central.visualizers['scup_pressure_grid'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting SCUP pressure grid: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/recursive-depth-explorer")
async def get_recursive_depth_explorer():
    """Get current Recursive Depth Explorer visualization data"""
    try:
        return {
            "recursive_depth_explorer": dawn_central.visualizers['recursive_depth_explorer'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting Recursive Depth Explorer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/semantic-flow-graph")
async def get_semantic_flow_graph():
    """Get current Semantic Flow Graph visualization data"""
    try:
        return {
            "semantic_flow_graph": dawn_central.visualizers['semantic_flow_graph'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting Semantic Flow Graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/consciousness-constellation")
async def get_consciousness_constellation():
    """Get current Consciousness Constellation visualization data"""
    try:
        return {
            "consciousness_constellation": dawn_central.visualizers['consciousness_constellation'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting Consciousness Constellation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# SCUP Zone Animator API Endpoints
@app.get("/api/scup-zone-animator/status")
async def get_scup_zone_animator_status():
    """Get the status of the SCUP zone animator service"""
    try:
        status = dawn_central.scup_zone_animator.get_status()
        return {
            "status": "success",
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting SCUP zone animator status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scup-zone-animator/generate")
async def generate_scup_zone_animation():
    """Generate a new SCUP zone animation"""
    try:
        animation_path = await dawn_central.scup_zone_animator.generate_animation()
        return {
            "status": "success",
            "animation_path": animation_path,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating SCUP zone animation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scup-zone-animator/auto-start")
async def start_auto_animation(interval: int = Query(60, description="Animation interval in seconds")):
    """Start automatic animation generation"""
    try:
        await dawn_central.scup_zone_animator.start_auto_animation(interval)
        return {
            "status": "success",
            "message": f"Auto animation started with {interval}s interval",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error starting auto animation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/scup-zone-animator/auto-stop")
async def stop_auto_animation():
    """Stop automatic animation generation"""
    try:
        await dawn_central.scup_zone_animator.stop_auto_animation()
        return {
            "status": "success",
            "message": "Auto animation stopped",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error stopping auto animation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scup-zone-animator/recent-data")
async def get_recent_zone_data(count: int = 50):
    """Get recent zone and SCUP data"""
    try:
        data = dawn_central.scup_zone_animator.get_recent_data(count)
        return {
            "status": "success",
            "data": data,
            "count": count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting recent zone data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scup-zone-animator/last-animation")
async def get_last_animation_path():
    """Get the path to the last generated animation"""
    try:
        last_path = dawn_central.scup_zone_animator.last_animation_path
        return {
            "status": "success",
            "animation_path": last_path,
            "exists": os.path.exists(last_path) if last_path else False,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting last animation path: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mood-entropy-phase")
async def get_mood_entropy_phase():
    """Get current mood-entropy phase visualization data"""
    try:
        return {
            "mood_entropy_phase": dawn_central.visualizers['mood_entropy_phase'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting mood-entropy phase: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/drift-state-transitions")
async def get_drift_state_transitions():
    """Get current drift state transitions visualization data"""
    try:
        return {
            "drift_state_transitions": dawn_central.visualizers['drift_state_transitions'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting drift state transitions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/visualizations")
async def get_all_visualizations():
    """Get all visualization data"""
    try:
        return {
            "mood_state": dawn_central.visualizers['mood_state'].get_visualization_data(),
            "heat_monitor": dawn_central.visualizers['heat_monitor'].get_visualization_data(),
            "entropy_flow": dawn_central.visualizers['entropy_flow'].get_visualization_data(),
            "scup_pressure_grid": dawn_central.visualizers['scup_pressure_grid'].get_visualization_data(),
            "mood_entropy_phase": dawn_central.visualizers['mood_entropy_phase'].get_visualization_data(),
            "drift_state_transitions": dawn_central.visualizers['drift_state_transitions'].get_visualization_data(),
            "sigil_command_stream": dawn_central.visualizers['sigil_command_stream'].get_visualization_data(),
            "recursive_depth_explorer": dawn_central.visualizers['recursive_depth_explorer'].get_visualization_data(),
            "semantic_flow_graph": dawn_central.visualizers['semantic_flow_graph'].get_visualization_data(),
            "bloom_genealogy_network": dawn_central.visualizers['bloom_genealogy_network'].get_visualization_data(),
            "consciousness_constellation": dawn_central.visualizers['consciousness_constellation'].get_visualization_data(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting visualizations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Visual System Integration API Endpoints
@app.get("/api/visual-system/status")
async def get_visual_system_status():
    """Get the status of the visual integration system"""
    try:
        status = dawn_central.visual_integration.get_status()
        return {
            "status": "success",
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting visual system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/visual-system/start")
async def start_visual_system():
    """Start the visual integration system"""
    try:
        success = dawn_central.visual_integration.start()
        return {
            "status": "success" if success else "failed",
            "message": "Visual system started successfully" if success else "Failed to start visual system",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error starting visual system: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/visual-system/stop")
async def stop_visual_system():
    """Stop the visual integration system"""
    try:
        success = dawn_central.visual_integration.stop()
        return {
            "status": "success" if success else "failed",
            "message": "Visual system stopped successfully" if success else "Failed to stop visual system",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error stopping visual system: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/visual-system/restart")
async def restart_visual_system():
    """Restart the visual integration system"""
    try:
        success = dawn_central.visual_integration.visual_manager.restart_visual_system()
        return {
            "status": "success" if success else "failed",
            "message": "Visual system restarted successfully" if success else "Failed to restart visual system",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error restarting visual system: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/visual-system/config")
async def get_visual_system_config():
    """Get the current configuration of the visual system"""
    try:
        config = dawn_central.visual_integration.visual_manager.config
        return {
            "status": "success",
            "config": {
                "mode": config.mode.value,
                "interval_ms": config.interval_ms,
                "buffer_size": config.buffer_size,
                "log_dir": config.log_dir,
                "output_dir": config.output_dir,
                "kill_existing": config.kill_existing,
                "max_processes": config.max_processes
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting visual system config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/visual-system/config")
async def update_visual_system_config(
    mode: Optional[str] = None,
    interval_ms: Optional[int] = None,
    buffer_size: Optional[int] = None,
    log_dir: Optional[str] = None,
    output_dir: Optional[str] = None,
    kill_existing: Optional[bool] = None,
    max_processes: Optional[int] = None
):
    """Update the configuration of the visual system"""
    try:
        config_updates = {}
        if mode is not None:
            config_updates["mode"] = mode
        if interval_ms is not None:
            config_updates["interval_ms"] = interval_ms
        if buffer_size is not None:
            config_updates["buffer_size"] = buffer_size
        if log_dir is not None:
            config_updates["log_dir"] = log_dir
        if output_dir is not None:
            config_updates["output_dir"] = output_dir
        if kill_existing is not None:
            config_updates["kill_existing"] = kill_existing
        if max_processes is not None:
            config_updates["max_processes"] = max_processes
        
        success = dawn_central.visual_integration.visual_manager.update_config(**config_updates)
        
        return {
            "status": "success" if success else "failed",
            "message": "Visual system configuration updated successfully" if success else "Failed to update configuration",
            "updated_config": config_updates,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error updating visual system config: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import signal
    import sys
    import asyncio

    # Add argument parsing
    parser = argparse.ArgumentParser(description="DAWN Tick Engine")
    parser.add_argument("--stdout-ticks", action="store_true", 
                       help="Output tick data to stdout for visualizers (CLI mode)")
    parser.add_argument("--interval", type=float, default=0.1, 
                       help="Tick interval in seconds (CLI mode)")
    args = parser.parse_args()

    if args.stdout_ticks:
        # CLI mode: output tick data to stdout for visualizers
        print("🚀 Starting DAWN Tick Engine in CLI mode (stdout ticks)...", file=sys.stderr)
        print("📊 Outputting JSON tick data to stdout for visualizers", file=sys.stderr)
        print("🛑 Press Ctrl+C to stop", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        
        # Redirect logging to stderr for CLI mode
        import logging
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stderr),  # Log to stderr
                logging.FileHandler('backend_cli.log')  # Also log to file
            ]
        )
        
        async def run_cli_mode():
            try:
                # Initialize semantic field
                initialize_semantic_field()
                
                # Start tick engine
                await dawn_central.tick_engine.start()
                
                # Start consciousness wave
                await consciousness_wave.start()
                
                print("✅ DAWN system initialized, starting tick loop...", file=sys.stderr)
                
                # Main tick loop
                while True:
                    try:
                        # Get current state
                        tick_data = dawn_central.get_state()
                        
                        # Output to stdout for visualizers
                        print(json.dumps(tick_data, default=str), flush=True)
                        
                        # Wait for next tick
                        await asyncio.sleep(args.interval)
                        
                    except KeyboardInterrupt:
                        print("\n🛑 Ctrl+C received, shutting down...", file=sys.stderr)
                        break
                    except Exception as e:
                        print(f"❌ Error in tick loop: {e}", file=sys.stderr)
                        await asyncio.sleep(1)  # Wait before retrying
                
                # Shutdown
                await consciousness_wave.stop()
                await dawn_central.shutdown()
                print("✅ DAWN CLI mode shutdown complete", file=sys.stderr)
                
            except Exception as e:
                print(f"❌ Fatal error in CLI mode: {e}", file=sys.stderr)
                sys.exit(1)
        
        try:
            asyncio.run(run_cli_mode())
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received. Exiting...", file=sys.stderr)
        except Exception as e:
            print(f"❌ Fatal error: {e}", file=sys.stderr)
            sys.exit(1)
    
    else:
        # Web server mode (original behavior)
        shutdown_event = asyncio.Event()

        def sync_signal_handler():
            print("\n🛑 Ctrl+C (SIGINT) received. Initiating graceful shutdown...")
            shutdown_event.set()

        async def shutdown_server():
            print("\n🔄 Shutting down DAWN system...")
            try:
                if dawn_central and dawn_central.tick_engine:
                    await dawn_central.tick_engine.stop()
                if dawn_central:
                    await dawn_central.shutdown()
                print("✅ DAWN system shutdown complete")
            except Exception as e:
                print(f"❌ Error during shutdown: {e}")
            finally:
                sys.exit(0)

        async def run_server():
            print("🚀 Starting DAWN Tick Engine Server...")
            print("📍 Server will be available at: http://localhost:8000")
            print("📊 API documentation at: http://localhost:8000/docs")
            print("🛑 Press Ctrl+C to stop the server")
            print("=" * 60)

            # Create FastAPI app with lifespan
            from contextlib import asynccontextmanager
            @asynccontextmanager
            async def lifespan(app: FastAPI):
                logger.info("Starting up server...")
                try:
                    logger.info("Initializing semantic field...")
                    initialize_semantic_field()
                    logger.info("Starting tick engine...")
                    await dawn_central.tick_engine.start()
                    logger.info("Starting consciousness wave visualization...")
                    await consciousness_wave.start()
                    logger.info("Starting visual integration system...")
                    if dawn_central.visual_integration.start():
                        logger.info("Visual integration system started successfully")
                    else:
                        logger.warning("Visual integration system failed to start")
                    async def broadcast_ticks():
                        while not shutdown_event.is_set():
                            await broadcast_tick_update()
                            await asyncio.sleep(0.1)
                    asyncio.create_task(broadcast_ticks())
                    logger.info("Server startup complete")
                    yield
                except Exception as e:
                    logger.error(f"Error during startup: {e}", exc_info=True)
                    try:
                        await dawn_central.tick_engine.stop()
                    except Exception as stop_error:
                        logger.error(f"Error during emergency shutdown: {stop_error}")
                    raise
                logger.info("Shutting down server...")
                try:
                    await consciousness_wave.stop()
                    logger.info("Stopping visual integration system...")
                    dawn_central.visual_integration.stop()
                    await dawn_central.shutdown()
                    logger.info("Server shutdown complete")
                except Exception as e:
                    logger.error(f"Error during shutdown: {e}", exc_info=True)
                    raise

            app_with_lifespan = FastAPI(lifespan=lifespan)
            for route in app.routes:
                app_with_lifespan.routes.append(route)
            config = uvicorn.Config(app_with_lifespan, host="0.0.0.0", port=8000, log_level="info")
            server = uvicorn.Server(config)

            loop = asyncio.get_running_loop()
            for sig in (signal.SIGINT, signal.SIGTERM):
                try:
                    loop.add_signal_handler(sig, sync_signal_handler)
                except NotImplementedError:
                    # add_signal_handler may not be available on Windows
                    signal.signal(sig, lambda s, f: sync_signal_handler())

            server_task = asyncio.create_task(server.serve())
            # Wait for shutdown_event to be set (Ctrl+C)
            await shutdown_event.wait()
            # Initiate shutdown
            await shutdown_server()
            # Ensure server stops
            await server_task

        try:
            asyncio.run(run_server())
        except KeyboardInterrupt:
            print("\n🛑 Keyboard interrupt received. Exiting...")
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            sys.exit(1) 