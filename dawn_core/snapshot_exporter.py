#!/usr/bin/env python3
"""
DAWN Snapshot Exporter - Complete System State Export and API
Final module for exporting DAWN's cognitive state, forecasts, and symbolic traces.
"""

import os
import json
import zipfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import random

# DAWN system imports with fallbacks
try:
    from core.tick.tick_loop import TickLoop as DAWNPulseEngine
    from core.entropy_analyzer import EntropyAnalyzer
    from cognitive.forecasting_models import Passion, Acquaintance
    from cognitive.forecasting_engine import DAWNForecastingEngine
    
    # Try to import MemoryChunk from correct path
    try:
        from core.memory.memory_chunk import MemoryChunk
    except ImportError:
        try:
            from memory_router.memory_chunk import MemoryChunk
        except ImportError:
            # Fallback MemoryChunk definition
            from datetime import datetime
            class MemoryChunk:
                def __init__(self, content="", speaker="system", topic="general"):
                    self.content = content
                    self.speaker = speaker
                    self.topic = topic
                    self.timestamp = datetime.now()
                    self.sigils = []
                    self.pulse_state = {}
                
                def get(self, key, default=None):
                    return getattr(self, key, default)
    
    from core.memory.memory_routing_system import get_memory_routing_system as MemoryRouter
    from cognitive.symbolic_router import SymbolicRouter
    from core.owl_bridge import OwlBridge
    print("✅ DAWN systems loaded for snapshot export")
except ImportError as e:
    print(f"⚠️ Import warning in snapshot_exporter: {e}")
    print("🔧 Using mock implementations for missing components")


class DAWNSnapshotExporter:
    """
    Comprehensive snapshot and export system for DAWN cognitive state.
    Provides APIs for state inspection, forecasting, and full system export.
    """
    
    def __init__(self, dawn_engine: Optional[Any] = None):
        """
        Initialize the snapshot exporter.
        
        Args:
            dawn_engine: Optional DAWNPulseEngine instance to export from
        """
        self.dawn_engine = dawn_engine
        self.snapshot_dir = Path("runtime/snapshots")
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Cache for last forecast
        self.last_forecast_cache = None
        self.last_forecast_timestamp = None
        
        # Export metadata
        self.export_version = "1.0.0"
        self.creation_timestamp = datetime.now()
        
        print(f"📤 DAWN Snapshot Exporter initialized")
        print(f"   Export directory: {self.snapshot_dir.absolute()}")
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get comprehensive live system state.
        
        Returns:
            dict: Complete system state snapshot
        """
        timestamp = datetime.now()
        
        if self.dawn_engine:
            # Get state from live DAWN engine
            try:
                current_entropy = self.dawn_engine.get_current_entropy()
                heat = self.dawn_engine.get_pulse_heat()
                zone = self.dawn_engine.get_pulse_zone()
                active_sigils = len(self.dawn_engine.active_sigils)
                pulse_state = self.dawn_engine.pulse_state.copy()
                
                # Get symbolic router state
                symbolic_state = None
                if hasattr(self.dawn_engine, 'symbolic_router') and self.dawn_engine.symbolic_router:
                    try:
                        symbolic_state = self.dawn_engine.symbolic_router.get_body_state()
                    except AttributeError:
                        symbolic_state = None
                
            except Exception as e:
                print(f"⚠️ Error getting live state: {e}, using defaults")
                current_entropy = 0.5
                heat = 25.0
                zone = "CALM"
                active_sigils = 0
                pulse_state = {}
                symbolic_state = None
        
        else:
            # Generate mock state for demonstration
            current_entropy = 0.3 + random.random() * 0.4  # 0.3-0.7 range
            heat = 20.0 + random.random() * 40.0  # 20-60 range
            
            if current_entropy > 0.6:
                zone = "CHAOTIC"
            elif current_entropy > 0.4:
                zone = "ACTIVE"
            else:
                zone = "CALM"
            
            active_sigils = random.randint(0, 3)
            pulse_state = {
                'entropy': current_entropy,
                'heat': heat,
                'zone': zone,
                'focus': 0.4 + random.random() * 0.5,
                'chaos': current_entropy * 0.8
            }
            
            symbolic_state = self._generate_mock_symbolic_state()
        
        state = {
            'timestamp': timestamp.isoformat(),
            'export_version': self.export_version,
            'system_metrics': {
                'entropy': current_entropy,
                'heat': heat,
                'zone': zone,
                'active_sigils': active_sigils,
                'tick_count': getattr(self.dawn_engine, 'tick_count', 0) if self.dawn_engine else 0
            },
            'pulse_state': pulse_state,
            'last_forecast': self.last_forecast_cache,
            'symbolic_state': symbolic_state,
            'system_health': {
                'status': 'operational' if current_entropy < 0.8 else 'elevated',
                'stability_index': 1.0 - current_entropy,
                'coherence_level': self._calculate_system_coherence(pulse_state)
            }
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
        
        # Generate contextual forecast
        forecast = self._generate_contextual_forecast(
            current_entropy, 
            zone, 
            interval_config,
            current_state
        )
        
        # Cache the forecast
        self.last_forecast_cache = forecast
        self.last_forecast_timestamp = current_time
        
        return forecast
    
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
            'window': interval_config.get('interval', 'next_24h'),
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
        elif zone == "CHAOTIC":
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
        elif zone == "CHAOTIC":
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
        if self.dawn_engine and hasattr(self.dawn_engine, 'symbolic_router') and self.dawn_engine.symbolic_router:
            try:
                symbolic_data = self.dawn_engine.symbolic_router.get_body_state()
            except (AttributeError, TypeError):
                symbolic_data = self._generate_mock_symbolic_state()
        else:
            symbolic_data = self._generate_mock_symbolic_state()
        
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
        
        print(f"🔮 Symbolic trace exported: {filename}")
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
        
        print(f"📦 Creating full DAWN snapshot: {zip_filename}")
        
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
                    'tick_count': system_state['system_metrics']['tick_count']
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
            
            print(f"✅ Snapshot created successfully: {zip_filename}")
            print(f"   Size: {zip_filepath.stat().st_size / 1024:.1f} KB")
            print(f"   Location: {zip_filepath.absolute()}")
            
        finally:
            # Clean up temporary directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
        
        return str(zip_filepath)
    
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
                'constellation': '○✨H',
                'somatic_commentary': 'I exist in somatic awareness.'
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
                if char not in glyphs and char not in ['○', '◯']:
                    glyphs.append(char)
        
        return glyphs
    
    def _calculate_system_coherence(self, pulse_state: Dict) -> float:
        """Calculate overall system coherence."""
        entropy = pulse_state.get('entropy', 0.5)
        focus = pulse_state.get('focus', 0.5)
        chaos = pulse_state.get('chaos', 0.5)
        
        coherence = (focus + (1.0 - entropy) + (1.0 - chaos)) / 3.0
        return max(0.0, min(1.0, coherence))
    
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
        if not self.dawn_engine or not hasattr(self.dawn_engine, 'memory_router'):
            return {
                'chunk_count': 0,
                'chunks': [],
                'note': 'No memory router available - using mock data'
            }
        
        try:
            # Get memory chunks from router
            chunks_data = []
            memory_router = self.dawn_engine.memory_router
            
            for chunk_id, chunk in getattr(memory_router, 'chunks', {}).items():
                chunk_dict = {
                    'id': chunk_id,
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
                'chunks': chunks_data[-20:]  # Last 20 chunks
            }
            
        except Exception as e:
            print(f"⚠️ Error exporting memory chunks: {e}")
            return None
    
    def _export_rebloom_log(self) -> Optional[Dict[str, Any]]:
        """Export rebloom routing history."""
        if not self.dawn_engine or not hasattr(self.dawn_engine, 'symbolic_router') or not self.dawn_engine.symbolic_router:
            return None
        
        try:
            symbolic_router = self.dawn_engine.symbolic_router
            routing_history = getattr(symbolic_router, 'routing_history', [])
            
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
                'total_reblooms': getattr(symbolic_router, 'total_reblooms', 0),
                'entries': rebloom_entries
            }
            
        except Exception as e:
            print(f"⚠️ Error exporting rebloom log: {e}")
            return None


# Utility functions
def create_exporter(dawn_engine=None) -> DAWNSnapshotExporter:
    """Factory function to create a DAWN snapshot exporter."""
    return DAWNSnapshotExporter(dawn_engine)


def quick_export(dawn_engine=None) -> str:
    """Quick function to create a full DAWN snapshot."""
    exporter = create_exporter(dawn_engine)
    return exporter.create_full_snapshot_zip()


def get_system_health(dawn_engine=None) -> Dict[str, Any]:
    """Quick function to get current system health status."""
    exporter = create_exporter(dawn_engine)
    state = exporter.get_state()
    return state['system_health']


# Command-line interface
def main():
    """Command-line interface for DAWN snapshot export."""
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Snapshot Exporter")
    parser.add_argument('--action', choices=['state', 'forecast', 'symbolic', 'full-zip'], 
                       default='state', help='Export action to perform')
    parser.add_argument('--interval', default='next_24h', 
                       help='Forecast interval (next_1h, next_24h, next_week)')
    parser.add_argument('--output', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    print("📤 DAWN Snapshot Exporter")
    print("=" * 40)
    
    exporter = create_exporter()
    
    if args.action == 'state':
        state = exporter.get_state()
        output_path = args.output or f"runtime/snapshots/state_{datetime.now().strftime('%H%M%S')}.json"
        
        with open(output_path, 'w') as f:
            json.dump(state, f, indent=2)
        print(f"✅ System state exported to: {output_path}")
        
    elif args.action == 'forecast':
        forecast = exporter.get_forecast(args.interval)
        output_path = args.output or f"runtime/snapshots/forecast_{args.interval}_{datetime.now().strftime('%H%M%S')}.json"
        
        with open(output_path, 'w') as f:
            json.dump(forecast, f, indent=2)
        print(f"✅ Forecast exported to: {output_path}")
        
    elif args.action == 'symbolic':
        symbolic_path = exporter.export_symbolic_trace()
        print(f"✅ Symbolic trace exported to: {symbolic_path}")
        
    elif args.action == 'full-zip':
        zip_path = exporter.create_full_snapshot_zip()
        print(f"✅ Full snapshot ZIP created: {zip_path}")
    
    print("\n🎯 Export complete!")


if __name__ == "__main__":
    main()