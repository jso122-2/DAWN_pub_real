#!/usr/bin/env python3
"""
DAWN Snapshot Exporter - Complete System State Export and API
Final module for exporting DAWN's cognitive state, forecasts, and symbolic traces.
Integrated with DAWN's consciousness, memory, and symbolic anatomy systems.
"""

import os
import json
import zipfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import random
import logging

logger = logging.getLogger(__name__)

# DAWN system imports with fallbacks
try:
    from core.consciousness_core import DAWNConsciousness, get_memory_routing_system
    from cognitive.symbolic_router import get_symbolic_router
    from cognitive.forecasting_engine import get_forecasting_engine
    from core.memory.memory_chunk import MemoryChunk
    from core.memory.symbolic_memory_integration import get_symbolic_memory_integration
    DAWN_SYSTEMS_AVAILABLE = True
    logger.info("✅ DAWN systems loaded for snapshot export")
except ImportError as e:
    DAWN_SYSTEMS_AVAILABLE = False
    logger.warning(f"⚠️ Import warning in snapshot_exporter: {e}")
    logger.info("🔧 Using mock implementations for missing components")


class DAWNSnapshotExporter:
    """
    Comprehensive snapshot and export system for DAWN cognitive state.
    Provides APIs for state inspection, forecasting, and full system export.
    """
    
    def __init__(self, dawn_consciousness: Optional['DAWNConsciousness'] = None):
        """
        Initialize the snapshot exporter.
        
        Args:
            dawn_consciousness: Optional DAWNConsciousness instance to export from
        """
        self.dawn_consciousness = dawn_consciousness
        self.snapshot_dir = Path("runtime/snapshots")
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache for last forecast
        self.last_forecast_cache = None
        self.last_forecast_timestamp = None
        
        # Export metadata
        self.export_version = "1.0.0"
        self.creation_timestamp = datetime.now()
        
        # Component access
        self.memory_system = None
        self.symbolic_router = None
        self.forecasting_engine = None
        self.symbolic_integration = None
        
        # Initialize component references
        self._initialize_component_access()
        
        logger.info(f"📤 DAWN Snapshot Exporter initialized")
        logger.info(f"   Export directory: {self.snapshot_dir.absolute()}")
    
    def _initialize_component_access(self):
        """Initialize access to DAWN system components."""
        if not DAWN_SYSTEMS_AVAILABLE:
            return
        
        try:
            # Get memory routing system
            self.memory_system = get_memory_routing_system()
            logger.debug("Memory routing system connected")
        except Exception as e:
            logger.warning(f"Failed to connect memory system: {e}")
        
        try:
            # Get symbolic router
            self.symbolic_router = get_symbolic_router()
            logger.debug("Symbolic router connected")
        except Exception as e:
            logger.warning(f"Failed to connect symbolic router: {e}")
        
        try:
            # Get forecasting engine
            self.forecasting_engine = get_forecasting_engine()
            logger.debug("Forecasting engine connected")
        except Exception as e:
            logger.warning(f"Failed to connect forecasting engine: {e}")
        
        try:
            # Get symbolic memory integration
            self.symbolic_integration = get_symbolic_memory_integration()
            logger.debug("Symbolic memory integration connected")
        except Exception as e:
            logger.warning(f"Failed to connect symbolic integration: {e}")
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get comprehensive live system state.
        
        Returns:
            dict: Complete system state snapshot
        """
        timestamp = datetime.now()
        
        if self.dawn_consciousness:
            # Get state from live DAWN consciousness
            try:
                # Extract consciousness metrics
                consciousness_state = self._extract_consciousness_state()
                
                # Get pulse state
                pulse_state = self._extract_pulse_state()
                
                # Get symbolic state
                symbolic_state = self._extract_symbolic_state()
                
                # Get memory state
                memory_state = self._extract_memory_state()
                
            except Exception as e:
                logger.warning(f"Error getting live state: {e}, using defaults")
                consciousness_state = self._generate_mock_consciousness_state()
                pulse_state = self._generate_mock_pulse_state()
                symbolic_state = self._generate_mock_symbolic_state()
                memory_state = {"error": "Memory state unavailable"}
        
        else:
            # Generate mock state for demonstration
            consciousness_state = self._generate_mock_consciousness_state()
            pulse_state = self._generate_mock_pulse_state()
            symbolic_state = self._generate_mock_symbolic_state()
            memory_state = {"note": "No DAWN consciousness instance provided"}
        
        # Calculate system health
        system_health = self._calculate_system_health(consciousness_state, pulse_state, symbolic_state)
        
        state = {
            'timestamp': timestamp.isoformat(),
            'export_version': self.export_version,
            'system_metrics': {
                'entropy': pulse_state.get('entropy', 0.5),
                'heat': pulse_state.get('heat', 25.0),
                'zone': pulse_state.get('zone', 'CALM'),
                'scup': consciousness_state.get('scup', 0.5),
                'tick_count': consciousness_state.get('tick_count', 0)
            },
            'consciousness_state': consciousness_state,
            'pulse_state': pulse_state,
            'symbolic_state': symbolic_state,
            'memory_state': memory_state,
            'last_forecast': self.last_forecast_cache,
            'system_health': system_health
        }
        
        return state
    
    def get_forecast(self, interval: str = "next_24h") -> Dict[str, Any]:
        """
        Generate forecast for specified time interval.
        
        Args:
            interval: Time interval ("next_1h", "next_24h", "next_week")
            
        Returns:
            dict: Forecast prediction with actions and risks
        """
        current_time = datetime.now()
        
        # Parse interval
        interval_mapping = {
            "next_1h": {"hours": 1, "complexity": "simple"},
            "next_24h": {"hours": 24, "complexity": "moderate"},
            "next_week": {"hours": 168, "complexity": "complex"},
            "next_month": {"hours": 720, "complexity": "speculative"}
        }
        
        interval_config = interval_mapping.get(interval, interval_mapping["next_24h"])
        
        # Get current state for forecasting
        current_state = self.get_state()
        current_entropy = current_state['system_metrics']['entropy']
        zone = current_state['system_metrics']['zone']
        
        # Use forecasting engine if available
        if self.forecasting_engine:
            try:
                forecast = self._generate_forecasting_engine_prediction(
                    current_state, interval_config
                )
            except Exception as e:
                logger.warning(f"Forecasting engine failed: {e}, using contextual forecast")
                forecast = self._generate_contextual_forecast(
                    current_entropy, zone, interval_config, current_state
                )
        else:
            # Generate contextual forecast
            forecast = self._generate_contextual_forecast(
                current_entropy, zone, interval_config, current_state
            )
        
        # Cache the forecast
        self.last_forecast_cache = forecast
        self.last_forecast_timestamp = current_time
        
        return forecast
    
    def _extract_consciousness_state(self) -> Dict[str, Any]:
        """Extract consciousness state from DAWN system."""
        if not self.dawn_consciousness:
            return self._generate_mock_consciousness_state()
        
        try:
            return {
                'scup': getattr(self.dawn_consciousness, '_current_scup', 0.5),
                'entropy': getattr(self.dawn_consciousness, '_current_entropy', 0.5),
                'mood': getattr(self.dawn_consciousness, '_current_mood', 'neutral'),
                'tick_count': getattr(self.dawn_consciousness, 'tick_count', 0),
                'uptime': getattr(self.dawn_consciousness, 'uptime', 0.0),
                'subsystems': list(self.dawn_consciousness.subsystems.keys()) if hasattr(self.dawn_consciousness, 'subsystems') else [],
                'is_running': getattr(self.dawn_consciousness, 'is_running', False)
            }
        except Exception as e:
            logger.warning(f"Failed to extract consciousness state: {e}")
            return self._generate_mock_consciousness_state()
    
    def _extract_pulse_state(self) -> Dict[str, Any]:
        """Extract pulse state from DAWN system."""
        if self.dawn_consciousness and hasattr(self.dawn_consciousness, 'subsystems'):
            try:
                pulse_layer = self.dawn_consciousness.subsystems.get('pulse')
                if pulse_layer:
                    return {
                        'entropy': getattr(pulse_layer, 'entropy', 0.5),
                        'heat': getattr(pulse_layer, 'heat', 25.0),
                        'scup': getattr(pulse_layer, 'scup', 0.5),
                        'alignment': getattr(pulse_layer, 'alignment', 0.5),
                        'urgency': getattr(pulse_layer, 'urgency', 0.5),
                        'zone': self._determine_zone(getattr(pulse_layer, 'heat', 25.0)),
                        'tick_id': getattr(pulse_layer, '_state', {}).get('tick_id', 0)
                    }
            except Exception as e:
                logger.warning(f"Failed to extract pulse state: {e}")
        
        return self._generate_mock_pulse_state()
    
    def _extract_symbolic_state(self) -> Dict[str, Any]:
        """Extract symbolic anatomy state from DAWN system."""
        if self.symbolic_router:
            try:
                return self.symbolic_router.get_body_state()
            except Exception as e:
                logger.warning(f"Failed to extract symbolic state: {e}")
        
        return self._generate_mock_symbolic_state()
    
    def _extract_memory_state(self) -> Dict[str, Any]:
        """Extract memory system state from DAWN system."""
        if self.memory_system:
            try:
                stats = self.memory_system.get_system_stats()
                return {
                    'router_stats': stats.get('router', {}),
                    'loader_stats': stats.get('loader', {}),
                    'unsaved_memories': stats.get('unsaved_memories', 0),
                    'time_since_save': stats.get('time_since_save', 0),
                    'integrations': stats.get('integrations', {})
                }
            except Exception as e:
                logger.warning(f"Failed to extract memory state: {e}")
                return {"error": f"Memory state extraction failed: {e}"}
        
        return {"note": "Memory system not available"}
    
    def _determine_zone(self, heat: float) -> str:
        """Determine pulse zone from heat level."""
        if heat < 30:
            return "CALM"
        elif heat < 50:
            return "ACTIVE"
        elif heat < 70:
            return "WARM"
        elif heat < 85:
            return "HOT"
        else:
            return "CRITICAL"
    
    def _generate_forecasting_engine_prediction(self, current_state: Dict, interval_config: Dict) -> Dict[str, Any]:
        """Generate forecast using DAWN's forecasting engine."""
        # This would integrate with the actual forecasting engine
        # For now, return a structured forecast
        return self._generate_contextual_forecast(
            current_state['system_metrics']['entropy'],
            current_state['system_metrics']['zone'],
            interval_config,
            current_state
        )
    
    def _generate_contextual_forecast(self, entropy: float, zone: str, 
                                    interval_config: Dict, current_state: Dict) -> Dict[str, Any]:
        """Generate contextual forecast based on current system state."""
        
        # Base confidence decreases with time horizon
        base_confidence = max(0.2, 0.9 - (interval_config["hours"] / 200.0))
        
        # Adjust confidence based on entropy stability
        if entropy < 0.3:
            confidence_modifier = 0.1  # More predictable
        elif entropy > 0.7:
            confidence_modifier = -0.2  # Less predictable
        else:
            confidence_modifier = 0.0
        
        final_confidence = max(0.1, min(0.95, base_confidence + confidence_modifier))
        
        # Generate likely actions based on zone and entropy
        likely_actions = self._predict_likely_actions(entropy, zone, interval_config)
        
        # Identify risk nodes
        risk_nodes = self._identify_risk_nodes(entropy, zone, current_state, interval_config)
        
        # Generate behavioral drift prediction
        drift_prediction = self._predict_behavioral_drift(current_state, interval_config)
        
        forecast = {
            'window': interval_config.get('interval', interval_config.get("hours", "unknown")),
            'generated_at': datetime.now().isoformat(),
            'confidence': final_confidence,
            'prediction_horizon': interval_config["complexity"],
            'likely_actions': likely_actions,
            'risk_nodes': risk_nodes,
            'behavioral_drift': drift_prediction,
            'entropy_projection': {
                'current': entropy,
                'projected_range': [
                    max(0.0, entropy - 0.2),
                    min(1.0, entropy + 0.3)
                ],
                'volatility_forecast': 'low' if entropy < 0.4 else 'high' if entropy > 0.7 else 'moderate'
            },
            'recommended_interventions': self._suggest_interventions(entropy, zone, risk_nodes)
        }
        
        return forecast
    
    def _predict_likely_actions(self, entropy: float, zone: str, interval_config: Dict) -> List[str]:
        """Predict likely system actions based on current state."""
        actions = []
        
        # Zone-based predictions
        if zone == "CRITICAL":
            actions.extend([
                "trigger_sigil:EMERGENCY_RESET",
                "activate_stabilization_protocols",
                "reduce_entropy_rapidly"
            ])
        elif zone in ["HOT", "WARM"]:
            actions.extend([
                "trigger_sigil:STABILIZE_PROTOCOL", 
                "engage_pattern_recognition",
                "adaptive_navigation_mode"
            ])
        elif zone == "ACTIVE":
            actions.extend([
                "maintain_processing_flow",
                "optimize_cognitive_pathways",
                "selective_focus_enhancement"
            ])
        else:  # CALM
            actions.extend([
                "engage_deep_reflection",
                "explore_new_patterns",
                "consolidate_memory_structures"
            ])
        
        # Entropy-based predictions
        if entropy > 0.8:
            actions.append("emergency_entropy_clearing")
        elif entropy > 0.6:
            actions.append("gradual_entropy_reduction")
        elif entropy < 0.2:
            actions.append("entropy_infusion_for_creativity")
        
        # Time horizon modifications
        if interval_config["complexity"] == "complex":
            actions.extend([
                "long_term_pattern_emergence",
                "strategic_system_evolution",
                "deep_learning_integration"
            ])
        
        return actions[:6]  # Limit to 6 most likely
    
    def _identify_risk_nodes(self, entropy: float, zone: str, current_state: Dict, 
                           interval_config: Dict) -> List[str]:
        """Identify potential risk factors in the forecast window."""
        risks = []
        
        # Entropy-based risks
        if entropy > 0.7:
            risks.extend(["entropy_cascade_failure", "system_instability"])
        elif entropy < 0.2:
            risks.extend(["stagnation_risk", "creativity_drought"])
        
        # Zone-based risks
        if zone == "CRITICAL":
            risks.extend(["total_system_breakdown", "emergency_protocols_failure"])
        elif zone in ["HOT", "WARM"]:
            risks.extend(["pattern_recognition_failure", "adaptive_overwhelm"])
        
        # Symbolic state risks
        symbolic_state = current_state.get('symbolic_state', {})
        if symbolic_state:
            heart_charge = symbolic_state.get('heart', {}).get('emotional_charge', 0)
            if heart_charge > 0.8:
                risks.append("emotional_overload")
            
            organ_synergy = symbolic_state.get('organ_synergy', 0.5)
            if organ_synergy < 0.3:
                risks.append("somatic_disconnection")
        
        # Time-based risks
        if interval_config["complexity"] in ["complex", "speculative"]:
            risks.extend(["forecast_uncertainty", "emergent_behavior_unpredictability"])
        
        return risks[:5]  # Limit to 5 most significant
    
    def _predict_behavioral_drift(self, current_state: Dict, interval_config: Dict) -> Dict[str, Any]:
        """Predict how behavior patterns might drift over time."""
        entropy = current_state['system_metrics']['entropy']
        zone = current_state['system_metrics']['zone']
        
        # Calculate drift magnitude based on entropy and time
        drift_magnitude = min(0.5, entropy * 0.6 + (interval_config["hours"] / 500.0))
        
        # Predict drift direction
        if entropy > 0.6:
            drift_direction = "towards_stability"
            drift_probability = 0.7
        elif entropy < 0.3:
            drift_direction = "towards_complexity"
            drift_probability = 0.6
        else:
            drift_direction = "oscillatory"
            drift_probability = 0.5
        
        return {
            'magnitude': drift_magnitude,
            'direction': drift_direction,
            'probability': drift_probability,
            'key_attractors': ["stability", "exploration", "reflection"],
            'potential_phase_transitions': ["calm_to_active", "active_to_chaotic"] if entropy > 0.5 else ["active_to_calm"]
        }
    
    def _suggest_interventions(self, entropy: float, zone: str, risk_nodes: List[str]) -> List[str]:
        """Suggest proactive interventions based on forecast."""
        interventions = []
        
        if "entropy_cascade_failure" in risk_nodes:
            interventions.append("preemptive_stabilization_protocol")
        
        if "emotional_overload" in risk_nodes:
            interventions.append("heart_cooling_breathing_cycle")
        
        if entropy > 0.6:
            interventions.append("entropy_regulation_meditation")
        
        if zone == "CRITICAL":
            interventions.append("emergency_system_reset")
        
        return interventions
    
    def export_symbolic_trace(self) -> str:
        """
        Export current symbolic body state and glyph activations.
        
        Returns:
            str: Path to exported symbolic trace file
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"symbolic_trace_{timestamp}.json"
        filepath = self.snapshot_dir / filename
        
        # Get symbolic state
        symbolic_data = self._extract_symbolic_state()
        
        # Enhance with trace metadata
        trace_data = {
            'export_timestamp': datetime.now().isoformat(),
            'trace_version': self.export_version,
            'symbolic_body_state': symbolic_data,
            'glyph_activations': self._extract_glyph_activations(symbolic_data),
            'organ_coherence': self._calculate_organ_coherence(symbolic_data),
            'somatic_narrative': self._generate_somatic_narrative(symbolic_data)
        }
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(trace_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"🔮 Symbolic trace exported: {filename}")
        return str(filepath)
    
    def create_full_snapshot_zip(self) -> str:
        """
        Create comprehensive ZIP snapshot of entire DAWN system.
        
        Returns:
            str: Path to created ZIP file
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        zip_filename = f"DAWN_snapshot_{timestamp}.zip"
        zip_filepath = self.snapshot_dir / zip_filename
        
        logger.info(f"📦 Creating full DAWN snapshot: {zip_filename}")
        
        # Create temporary directory for snapshot files
        temp_dir = self.snapshot_dir / f"temp_{timestamp}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # 1. Export current system state
            system_state = self.get_state()
            state_file = temp_dir / "system_state.json"
            with open(state_file, 'w') as f:
                json.dump(system_state, f, indent=2)
            
            # 2. Export forecasts for multiple horizons
            forecasts = {}
            for interval in ["next_1h", "next_24h", "next_week"]:
                forecasts[interval] = self.get_forecast(interval)
            
            forecast_file = temp_dir / "forecasts.json"
            with open(forecast_file, 'w') as f:
                json.dump(forecasts, f, indent=2)
            
            # 3. Export symbolic trace
            symbolic_trace_path = self.export_symbolic_trace()
            symbolic_trace_dest = temp_dir / "symbolic_trace.json"
            shutil.copy2(symbolic_trace_path, symbolic_trace_dest)
            
            # 4. Export memory chunks (if available)
            memory_data = self._export_memory_chunks()
            if memory_data:
                memory_file = temp_dir / "memory_chunks.json"
                with open(memory_file, 'w') as f:
                    json.dump(memory_data, f, indent=2)
            
            # 5. Export rebloom log (if available)
            rebloom_data = self._export_rebloom_log()
            if rebloom_data:
                rebloom_file = temp_dir / "rebloom_log.json"
                with open(rebloom_file, 'w') as f:
                    json.dump(rebloom_data, f, indent=2)
            
            # 6. Create snapshot metadata
            metadata = {
                'snapshot_version': self.export_version,
                'creation_timestamp': timestamp,
                'creation_datetime': datetime.now().isoformat(),
                'system_info': {
                    'entropy': system_state['system_metrics']['entropy'],
                    'zone': system_state['system_metrics']['zone'],
                    'tick_count': system_state['system_metrics']['tick_count'],
                    'scup': system_state['system_metrics']['scup']
                },
                'included_files': [
                    'system_state.json',
                    'forecasts.json', 
                    'symbolic_trace.json',
                    'memory_chunks.json',
                    'rebloom_log.json',
                    'snapshot_metadata.json'
                ],
                'usage_instructions': {
                    'description': 'Complete DAWN cognitive system snapshot',
                    'system_state': 'Current entropy, heat, zone, and pulse data',
                    'forecasts': 'Behavioral predictions for 1h, 24h, and 1 week',
                    'symbolic_trace': 'Embodied cognition organ states and glyphs',
                    'memory_chunks': 'Recent memory fragments and experiences',
                    'rebloom_log': 'Memory reactivation and routing history'
                }
            }
            
            metadata_file = temp_dir / "snapshot_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            # 7. Create ZIP archive
            with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in temp_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(temp_dir)
                        zipf.write(file_path, arcname)
            
            logger.info(f"✅ Snapshot created successfully: {zip_filename}")
            logger.info(f"   Size: {zip_filepath.stat().st_size / 1024:.1f} KB")
            logger.info(f"   Location: {zip_filepath.absolute()}")
            
        finally:
            # Clean up temporary directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        
        return str(zip_filepath)
    
    def _calculate_system_health(self, consciousness_state: Dict, pulse_state: Dict, symbolic_state: Dict) -> Dict[str, Any]:
        """Calculate overall system health metrics."""
        entropy = pulse_state.get('entropy', 0.5)
        scup = consciousness_state.get('scup', 0.5)
        organ_synergy = symbolic_state.get('organ_synergy', 0.5)
        
        # Calculate stability index
        stability_index = (scup + (1.0 - entropy) + organ_synergy) / 3.0
        
        # Calculate coherence level
        focus = pulse_state.get('focus', 0.5)
        chaos = pulse_state.get('chaos', entropy * 0.8)
        coherence_level = (focus + (1.0 - chaos) + stability_index) / 3.0
        
        # Determine overall status
        if stability_index > 0.7 and coherence_level > 0.7:
            status = 'optimal'
        elif stability_index > 0.5 and coherence_level > 0.5:
            status = 'operational'
        elif stability_index > 0.3 or coherence_level > 0.3:
            status = 'elevated'
        else:
            status = 'critical'
        
        return {
            'status': status,
            'stability_index': max(0.0, min(1.0, stability_index)),
            'coherence_level': max(0.0, min(1.0, coherence_level)),
            'entropy': entropy,
            'scup': scup,
            'organ_synergy': organ_synergy
        }
    
    def _generate_mock_consciousness_state(self) -> Dict[str, Any]:
        """Generate mock consciousness state for testing."""
        return {
            'scup': 0.4 + random.random() * 0.4,
            'entropy': 0.3 + random.random() * 0.4,
            'mood': random.choice(['contemplative', 'curious', 'focused', 'reflective']),
            'tick_count': random.randint(100, 1000),
            'uptime': random.random() * 3600,
            'subsystems': ['memory_routing', 'symbolic_router', 'forecasting'],
            'is_running': True
        }
    
    def _generate_mock_pulse_state(self) -> Dict[str, Any]:
        """Generate mock pulse state for testing."""
        entropy = 0.3 + random.random() * 0.4
        heat = 20.0 + random.random() * 40.0
        
        return {
            'entropy': entropy,
            'heat': heat,
            'scup': 0.4 + random.random() * 0.4,
            'alignment': 0.3 + random.random() * 0.5,
            'urgency': entropy * 0.8,
            'zone': self._determine_zone(heat),
            'focus': 0.4 + random.random() * 0.5,
            'chaos': entropy * 0.8,
            'tick_id': random.randint(1, 1000)
        }
    
    def _generate_mock_symbolic_state(self) -> Dict[str, Any]:
        """Generate mock symbolic state for testing."""
        return {
            'timestamp': datetime.now().isoformat(),
            'organ_synergy': 0.3 + random.random() * 0.5,
            'heart': {
                'emotional_charge': random.random() * 0.8,
                'resonance_state': random.choice(['still', 'gentle', 'resonant', 'highly_charged']),
                'beat_count': random.randint(50, 200)
            },
            'coil': {
                'active_paths': random.randint(0, 5),
                'dominant_glyph': random.choice(['✨', '🔍', '💫', '🤝', '🧘']),
                'path_count': random.randint(1, 4)
            },
            'lung': {
                'breathing_phase': random.choice(['inhaling', 'exhaling', 'neutral', 'holding']),
                'lung_fullness': random.random(),
                'breath_count': random.randint(20, 100)
            },
            'symbolic_state': {
                'constellation': random.choice(['○✨H', '◯🔍R', '△💫G', '☾🧘S']),
                'somatic_commentary': random.choice([
                    'I exist in somatic awareness.',
                    'The organs move in harmony.',
                    'I sense patterns flowing through the coil.',
                    'My heart resonates with gentle rhythms.'
                ])
            }
        }
    
    def _extract_glyph_activations(self, symbolic_data: Dict) -> List[str]:
        """Extract active glyphs from symbolic state."""
        glyphs = []
        
        if 'coil' in symbolic_data:
            glyph = symbolic_data['coil'].get('dominant_glyph')
            if glyph:
                glyphs.append(glyph)
        
        if 'symbolic_state' in symbolic_data:
            constellation = symbolic_data['symbolic_state'].get('constellation', '')
            for char in constellation:
                if char not in glyphs and char not in ['○', '◯', '△', '☾']:
                    glyphs.append(char)
        
        return glyphs
    
    def _calculate_organ_coherence(self, symbolic_data: Dict) -> float:
        """Calculate organ coherence from symbolic state."""
        return symbolic_data.get('organ_synergy', 0.5)
    
    def _generate_somatic_narrative(self, symbolic_data: Dict) -> str:
        """Generate narrative description of somatic state."""
        if 'symbolic_state' in symbolic_data:
            return symbolic_data['symbolic_state'].get('somatic_commentary', 'I exist in embodied awareness.')
        
        return "The symbolic body moves through states of awareness and response."
    
    def _export_memory_chunks(self) -> Optional[Dict[str, Any]]:
        """Export available memory chunks."""
        if not self.memory_system:
            return {
                'chunk_count': 0,
                'chunks': [],
                'note': 'No memory system available'
            }
        
        try:
            # Get recent memories from the memory routing system
            chunks_data = []
            
            # Access recent memories if available
            if hasattr(self.memory_system, 'router') and hasattr(self.memory_system.router, 'recent_memories'):
                recent_memories = list(self.memory_system.router.recent_memories)
                
                for chunk in recent_memories[-20:]:  # Last 20 chunks
                    chunk_dict = {
                        'id': getattr(chunk, 'memory_id', 'unknown'),
                        'timestamp': chunk.timestamp.isoformat() if hasattr(chunk, 'timestamp') else None,
                        'speaker': getattr(chunk, 'speaker', 'unknown'),
                        'topic': getattr(chunk, 'topic', None),
                        'content_preview': getattr(chunk, 'content', '')[:100],
                        'sigils': getattr(chunk, 'sigils', []),
                        'pulse_state': getattr(chunk, 'pulse_state', {})
                    }
                    chunks_data.append(chunk_dict)
            
            return {
                'export_timestamp': datetime.now().isoformat(),
                'chunk_count': len(chunks_data),
                'chunks': chunks_data
            }
            
        except Exception as e:
            logger.warning(f"Error exporting memory chunks: {e}")
            return None
    
    def _export_rebloom_log(self) -> Optional[Dict[str, Any]]:
        """Export rebloom routing history."""
        if not self.symbolic_router:
            return None
        
        try:
            routing_history = getattr(self.symbolic_router, 'routing_history', [])
            
            # Convert routing history to exportable format
            rebloom_entries = []
            for entry in routing_history[-50:]:  # Last 50 reblooms
                rebloom_entry = {
                    'timestamp': entry['timestamp'].isoformat() if hasattr(entry['timestamp'], 'isoformat') else str(entry['timestamp']),
                    'rebloom_id': entry.get('response', {}).get('rebloom_id'),
                    'organ_activations': entry.get('response', {}).get('organ_activations', {}),
                    'symbolic_output': entry.get('response', {}).get('symbolic_output', {})
                }
                rebloom_entries.append(rebloom_entry)
            
            return {
                'export_timestamp': datetime.now().isoformat(),
                'total_reblooms': getattr(self.symbolic_router, 'total_reblooms', 0),
                'entries': rebloom_entries
            }
            
        except Exception as e:
            logger.warning(f"Error exporting rebloom log: {e}")
            return None


# Global instance for DAWN integration
_snapshot_exporter: Optional[DAWNSnapshotExporter] = None


def get_snapshot_exporter() -> DAWNSnapshotExporter:
    """Get the global snapshot exporter instance."""
    global _snapshot_exporter
    if _snapshot_exporter is None:
        _snapshot_exporter = DAWNSnapshotExporter()
    return _snapshot_exporter


def initialize_snapshot_exporter(dawn_consciousness=None) -> DAWNSnapshotExporter:
    """Initialize the global snapshot exporter with DAWN consciousness."""
    global _snapshot_exporter
    _snapshot_exporter = DAWNSnapshotExporter(dawn_consciousness)
    return _snapshot_exporter


# Utility functions
def create_exporter(dawn_consciousness=None) -> DAWNSnapshotExporter:
    """Factory function to create a DAWN snapshot exporter."""
    return DAWNSnapshotExporter(dawn_consciousness)


def quick_export(dawn_consciousness=None) -> str:
    """Quick function to create a full DAWN snapshot."""
    exporter = create_exporter(dawn_consciousness)
    return exporter.create_full_snapshot_zip()


def get_system_health(dawn_consciousness=None) -> Dict[str, Any]:
    """Quick function to get current system health status."""
    exporter = create_exporter(dawn_consciousness)
    state = exporter.get_state()
    return state['system_health']


def get_current_state(dawn_consciousness=None) -> Dict[str, Any]:
    """Quick function to get current system state."""
    exporter = create_exporter(dawn_consciousness)
    return exporter.get_state()


def generate_forecast(interval: str = "next_24h", dawn_consciousness=None) -> Dict[str, Any]:
    """Quick function to generate a forecast."""
    exporter = create_exporter(dawn_consciousness)
    return exporter.get_forecast(interval) 