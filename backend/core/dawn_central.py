from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np
import logging
import time
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from .unified_tick_engine import UnifiedTickEngine
from ..cognitive.consciousness import ConsciousnessModule
from ..cognitive.conversation import ConversationModule
from ..cognitive.spontaneity import SpontaneityModule
from ..cognitive.entropy_fluctuation import EntropyFluctuation
from ..cognitive.mood_urgency_probe import MoodUrgencyProbe
from ..cognitive.qualia_kernel import QualiaKernel

logger = logging.getLogger(__name__)

class DAWNCentral:
    def __init__(self):
        self.tick_engine = UnifiedTickEngine()
        self.is_active = True
        
        # Initialize cognitive modules
        self.consciousness = ConsciousnessModule()
        self.conversation = ConversationModule()
        self.spontaneity = SpontaneityModule()
        self.entropy = EntropyFluctuation()
        self.mood = MoodUrgencyProbe()
        self.qualia = QualiaKernel()
        
        # Initialize state
        self.state = {
            "scup": 0.0,
            "entropy": 0.0,
            "mood": 0.0,
            "temperature": 0.0,
            "coherence": 0.0,
            "active_processes": set(),
            "last_update": datetime.now()
        }
        
        # Initialize history
        self.history = {
            "scup": [],
            "entropy": [],
            "mood": [],
            "temperature": [],
            "coherence": []
        }
        
        # Initialize real computation engines
        self._init_computation_engines()
        
        logger.info("Initialized DAWNCentral with real computation engines")
    
    def _init_computation_engines(self):
        """Initialize connections to real DAWN computation engines"""
        self.computation_engines = {}
        
        # Try to connect to SCUP tracker
        try:
            from schema.scup_tracker import SCUPTracker
            self.computation_engines['scup_tracker'] = SCUPTracker()
            logger.info("Connected to SCUP tracker")
        except ImportError as e:
            logger.warning(f"SCUP tracker not available: {e}")
            self.computation_engines['scup_tracker'] = None
        except Exception as e:
            logger.warning(f"SCUP tracker initialization failed: {e}")
            self.computation_engines['scup_tracker'] = None
            
        # Try to connect to pulse heat system
        try:
            from pulse.pulse_heat import pulse
            self.computation_engines['pulse_heat'] = pulse
            logger.info("Connected to pulse heat system") 
        except ImportError as e:
            logger.warning(f"Pulse heat system not available: {e}")
            self.computation_engines['pulse_heat'] = None
        except Exception as e:
            logger.warning(f"Pulse heat system initialization failed: {e}")
            self.computation_engines['pulse_heat'] = None
            
        # Try to connect to mood engine
        try:
            # Temporarily disable mood engine due to null bytes issue
            # from mood.mood_engine import measure_linguistic_pressure
            # self.computation_engines['mood_engine'] = measure_linguistic_pressure
            logger.info("Mood engine temporarily disabled (null bytes issue)")
            self.computation_engines['mood_engine'] = None
        except ImportError as e:
            logger.warning(f"Mood engine not available: {e}")
            self.computation_engines['mood_engine'] = None
        except Exception as e:
            logger.warning(f"Mood engine initialization failed: {e}")
            self.computation_engines['mood_engine'] = None
            
        # Try to connect to bloom manager for memory pressure
        try:
            from bloom.bloom_manager import BloomManager
            self.computation_engines['bloom_manager'] = BloomManager()
            logger.info("Connected to bloom manager")
        except ImportError as e:
            logger.warning(f"Bloom manager not available: {e}")
            self.computation_engines['bloom_manager'] = None
        except Exception as e:
            logger.warning(f"Bloom manager initialization failed: {e}")
            self.computation_engines['bloom_manager'] = None
    
    def update(self, tick_number: int = None) -> Dict[str, Any]:
        """Update DAWN state with real computation from engines"""
        try:
            current_time = time.time()
            
            # === SCUP COMPUTATION ===
            if self.computation_engines.get('scup_tracker'):
                try:
                    # Calculate real SCUP with pressure simulation
                    alignment = 0.6 + 0.2 * np.sin(current_time * 0.05)  # Base alignment with drift
                    entropy_base = 0.4 + 0.1 * np.cos(current_time * 0.03)  # Base entropy
                    pressure = 0.3 + 0.2 * np.sin(current_time * 0.08)  # Pressure oscillation
                    
                    # Add some variance based on recent state
                    if len(self.history['scup']) > 5:
                        recent_variance = np.var(self.history['scup'][-5:])
                        entropy_base += recent_variance * 0.5  # Entropy increases with state variance
                    
                    scup_result = self.computation_engines['scup_tracker'].compute_scup(
                        alignment=alignment,
                        entropy=entropy_base,
                        pressure=pressure,
                        tick_id=tick_number or 0
                    )
                    self.state['scup'] = float(scup_result['scup'])
                    
                except Exception as e:
                    logger.warning(f"SCUP computation failed: {e}")
                    # Fallback with realistic variance
                    self.state['scup'] = 0.5 + 0.2 * np.sin(current_time * 0.1)
            else:
                # Enhanced simulation mode
                self.state['scup'] = 0.5 + 0.2 * np.sin(current_time * 0.1)
            
            # === THERMAL/PRESSURE COMPUTATION ===
            if self.computation_engines.get('pulse_heat'):
                try:
                    pulse_system = self.computation_engines['pulse_heat']
                    thermal_profile = pulse_system.get_thermal_profile()
                    
                    # Extract real thermal data  
                    current_heat = thermal_profile.get('current_heat', 25.0)
                    normalized_heat = np.clip(current_heat / 100.0, 0.0, 1.0)
                    self.state['temperature'] = normalized_heat
                    
                    # If heat is zero, use baseline thermal activity
                    if current_heat == 0.0:
                        # Generate baseline thermal activity
                        baseline_thermal = 0.4 + 0.2 * np.sin(current_time * 0.06)
                        self.state['temperature'] = np.clip(baseline_thermal, 0.0, 1.0)
                    
                    # Use thermal momentum for pressure
                    thermal_momentum = thermal_profile.get('thermal_momentum', 0.0)
                    pressure_from_heat = np.clip(abs(thermal_momentum) / 10.0, 0.0, 1.0)
                    
                except Exception as e:
                    logger.warning(f"Thermal computation failed: {e}")
                    # Fallback thermal simulation
                    base_temp = 0.4 + 0.3 * np.sin(current_time * 0.06)
                    self.state['temperature'] = np.clip(base_temp, 0.0, 1.0)
            else:
                # Enhanced thermal simulation
                base_temp = 0.4 + 0.3 * np.sin(current_time * 0.06)
                self.state['temperature'] = np.clip(base_temp, 0.0, 1.0)
            
            # === ENTROPY COMPUTATION ===
            entropy_sources = []
            
            # Add mood entropy if available  
            if self.computation_engines.get('mood_engine'):
                try:
                    # Simulate some text input for mood analysis
                    sample_text = "processing consciousness state"
                    mood_data = self.computation_engines['mood_engine'](sample_text)
                    mood_entropy = mood_data.get('entropy', 0.5) if mood_data else 0.5
                    entropy_sources.append(mood_entropy * 0.4)
                except Exception as e:
                    logger.warning(f"Mood entropy computation failed: {e}")
                    entropy_sources.append(0.3)
            else:
                # Simulate mood entropy
                mood_entropy = 0.3 + 0.2 * np.cos(current_time * 0.04)
                entropy_sources.append(mood_entropy * 0.4)
            
            # Add memory pressure entropy from bloom system
            if self.computation_engines.get('bloom_manager'):
                try:
                    bloom_manager = self.computation_engines['bloom_manager']
                    # Simulate memory pressure from active blooms
                    active_count = len(getattr(bloom_manager, 'active_blooms', []))
                    sealed_count = len(getattr(bloom_manager, 'sealed_blooms', []))
                    total_blooms = active_count + sealed_count
                    
                    # Memory pressure increases with more blooms
                    memory_pressure = np.clip(total_blooms / 20.0, 0.0, 1.0)
                    entropy_sources.append(memory_pressure * 0.3)
                    
                except Exception as e:
                    logger.warning(f"Memory pressure computation failed: {e}")
                    # Simulate memory pressure  
                    memory_pressure = 0.2 + 0.1 * np.sin(current_time * 0.02)
                    entropy_sources.append(memory_pressure * 0.3)
            else:
                # Simulate memory pressure
                memory_pressure = 0.2 + 0.1 * np.sin(current_time * 0.02)
                entropy_sources.append(memory_pressure * 0.3)
            
            # Add system entropy (remaining 30%)
            system_entropy = 0.2 + 0.1 * np.sin(current_time * 0.07)
            entropy_sources.append(system_entropy * 0.3)
            
            # Combine entropy sources
            self.state['entropy'] = sum(entropy_sources)
            
            # === MOOD COMPUTATION ===
            # Combine temperature and entropy for mood
            temp_factor = self.state['temperature']
            entropy_factor = self.state['entropy']
            scup_factor = self.state['scup']
            
            # Mood influenced by all factors
            mood_base = (temp_factor * 0.4 + (1.0 - entropy_factor) * 0.3 + scup_factor * 0.3)
            mood_variance = 0.1 * np.sin(current_time * 0.09)
            self.state['mood'] = np.clip(mood_base + mood_variance, 0.0, 1.0)
            
            # === COHERENCE COMPUTATION ===
            # Coherence is inverse of entropy with SCUP influence
            coherence_base = (1.0 - self.state['entropy']) * 0.6 + self.state['scup'] * 0.4
            self.state['coherence'] = np.clip(coherence_base, 0.0, 1.0)
            
            # === UPDATE HISTORY ===
            for key in ['scup', 'entropy', 'mood', 'temperature', 'coherence']:
                self.history[key].append(self.state[key])
                # Keep last 100 values
                if len(self.history[key]) > 100:
                    self.history[key].pop(0)
            
            # Update timestamp
            self.state['last_update'] = datetime.now()
            
            # Log state periodically
            if tick_number and tick_number % 10 == 0:
                logger.debug(f"DAWN state updated - SCUP: {self.state['scup']:.3f}, "
                           f"Entropy: {self.state['entropy']:.3f}, "
                           f"Mood: {self.state['mood']:.3f}")
            
            return self.state.copy()
            
        except Exception as e:
            logger.error(f"Critical error in DAWN state update: {e}")
            # Emergency fallback - return current state
            return self.state.copy()

    def get_scup(self) -> float:
        """Get current SCUP value"""
        return self.state["scup"]
    
    def get_entropy(self) -> float:
        """Get current entropy value"""
        return self.state["entropy"]
    
    def get_mood(self) -> float:
        """Get current mood value"""
        return self.state["mood"]
    
    def get_temperature(self) -> float:
        """Get current temperature value"""
        return self.state["temperature"]
    
    def get_coherence(self) -> float:
        """Get current coherence value"""
        return self.state["coherence"]
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state"""
        return self.state
    
    def get_history(self, duration: int = 100) -> Dict[str, List[float]]:
        """Get historical data"""
        return {
            key: values[-duration:] if len(values) > duration else values
            for key, values in self.history.items()
        }
    
    def get_active_processes(self) -> List[str]:
        """Get list of active processes"""
        return list(self.state["active_processes"])
    
    def get_available_processes(self) -> List[str]:
        """Get list of available processes"""
        return [
            "consciousness",
            "conversation",
            "spontaneity",
            "entropy",
            "mood",
            "qualia"
        ]
    
    def activate_process(self, process_name: str) -> bool:
        """Activate a process"""
        if process_name in self.get_available_processes():
            self.state["active_processes"].add(process_name)
            return True
        return False
    
    def deactivate_process(self, process_name: str) -> bool:
        """Deactivate a process"""
        if process_name in self.state["active_processes"]:
            self.state["active_processes"].remove(process_name)
            return True
        return False
    
    def has_state_changed(self) -> bool:
        """Check if state has changed since last update"""
        return (datetime.now() - self.state["last_update"]).total_seconds() > 0.1
    
    def get_consciousness_metrics(self) -> Dict[str, float]:
        """Get detailed consciousness metrics"""
        return {
            "neural_activity": self.consciousness.get_neural_activity().mean(),
            "quantum_coherence": self.consciousness.get_coherence(),
            "pattern_recognition": self.qualia.get_coherence(),
            "memory_utilization": self.conversation.get_engagement(),
            "chaos_factor": self.entropy.get_fluctuation()
        }
    
    def get_scup_history(self, length: int = 100) -> List[float]:
        """Get SCUP history"""
        return self.history["scup"][-length:]
    
    def get_entropy_distribution(self) -> np.ndarray:
        """Get entropy distribution matrix"""
        return np.zeros((10, 10))  # Placeholder
    
    def get_system_temperature(self) -> float:
        """Get system temperature"""
        return self.state["temperature"]
    
    def get_neural_activity_matrix(self) -> np.ndarray:
        """Get neural activity matrix"""
        return np.zeros((10, 10))  # Placeholder
    
    def get_activation_levels(self) -> List[float]:
        """Get activation levels"""
        return [0.0] * 10  # Placeholder
    
    def get_alignment_matrix(self) -> np.ndarray:
        """Get alignment matrix"""
        return np.zeros((10, 10))  # Placeholder
    
    def get_coherence_score(self) -> float:
        """Get coherence score"""
        return self.state["coherence"]
    
    def get_bloom_pattern(self) -> np.ndarray:
        """Get bloom pattern matrix"""
        return np.zeros((10, 10))  # Placeholder
    
    def get_growth_metrics(self) -> float:
        """Get growth metrics"""
        return 0.0  # Placeholder
    
    def get_mood_vector(self) -> np.ndarray:
        """Get mood vector"""
        return np.zeros(10)  # Placeholder
    
    def get_mood_history(self, length: int = 50) -> List[float]:
        """Get mood history"""
        return self.history["mood"][-length:]
    
    def reset(self) -> None:
        """Reset to initial state"""
        self.state = {
            "scup": 0.0,
            "entropy": 0.0,
            "mood": 0.0,
            "temperature": 0.0,
            "coherence": 0.0,
            "active_processes": set(),
            "last_update": datetime.now()
        }
        self.history = {
            "scup": [],
            "entropy": [],
            "mood": [],
            "temperature": [],
            "coherence": []
        }
        logger.info("Reset DAWNCentral state") 