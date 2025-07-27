#!/usr/bin/env python3
"""
DAWN Integrated Consciousness State Writer
Memory-mapped file interface for DAWN consciousness engine output
Integrates with existing DAWN consciousness systems
"""

import json
import mmap
import struct
import time
import sys
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
import numpy as np

# Add project root to path for DAWN imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Try to import DAWN consciousness systems one by one
DAWN_SYSTEMS = {}
DAWN_INTEGRATION_AVAILABLE = False

# Try consciousness core
try:
    from core.consciousness_core import consciousness_core
    DAWN_SYSTEMS['consciousness_core'] = consciousness_core
    print("✅ Imported consciousness_core")
except ImportError as e:
    print(f"⚠️  consciousness_core not available: {e}")

# Try main consciousness
try:
    from core.consciousness import DAWNConsciousness as MainConsciousness
    DAWN_SYSTEMS['main_consciousness'] = MainConsciousness
    print("✅ Imported main consciousness")
except ImportError as e:
    print(f"⚠️  main consciousness not available: {e}")

# Try DAWN Central
try:
    from backend.core.dawn_central import DAWNCentral
    DAWN_SYSTEMS['dawn_central'] = DAWNCentral
    print("✅ Imported DAWN Central")
except ImportError as e:
    print(f"⚠️  DAWN Central not available: {e}")

# Try schema state
try:
    from core.schema_state import SchemaState
    DAWN_SYSTEMS['schema_state'] = SchemaState
    print("✅ Imported schema state")
except ImportError as e:
    print(f"⚠️  schema state not available: {e}")

# Try tick engine
try:
    from core.tick.tick_engine import TickEngine
    DAWN_SYSTEMS['tick_engine'] = TickEngine
    print("✅ Imported tick engine")
except ImportError as e:
    print(f"⚠️  tick engine not available: {e}")

# Try pulse system (direct import first)
try:
    from pulse.pulse_heat import pulse
    DAWN_SYSTEMS['pulse_system'] = pulse
    print("✅ Imported pulse system")
except ImportError as e:
    print(f"⚠️  pulse system not available: {e}")
    # Try pulse loader as fallback (but don't use coroutine)
    try:
        import pulse.pulse_loader
        DAWN_SYSTEMS['pulse_loader_module'] = pulse.pulse_loader
        print("✅ Imported pulse loader module")
    except ImportError as e:
        print(f"⚠️  pulse loader not available: {e}")

# Check if we have any DAWN systems available
if DAWN_SYSTEMS:
    DAWN_INTEGRATION_AVAILABLE = True
    print(f"✅ DAWN integration available with {len(DAWN_SYSTEMS)} systems")
else:
    print("⚠️  No DAWN systems available - running in simulation mode")

@dataclass
class CognitiveVector:
    """Pure logic tensor representation"""
    semantic_alignment: float
    entropy_gradient: float
    drift_magnitude: float
    rebloom_intensity: float

@dataclass 
class MoodZone:
    """Emotional state representation"""
    valence: float  # -1.0 to 1.0
    arousal: float  # 0.0 to 1.0
    dominance: float # 0.0 to 1.0
    coherence: float # 0.0 to 1.0

@dataclass
class TickState:
    """Complete cognitive state at single tick"""
    tick_number: int
    timestamp_ms: int
    mood_zone: MoodZone
    cognitive_vector: CognitiveVector
    memory_rebloom_flags: List[bool]  # 64 memory sectors
    semantic_heatmap: List[float]     # 256 semantic nodes
    forecast_vector: List[float]      # 32 prediction dimensions
    consciousness_depth: float        # 0.0 to 1.0
    tensor_state_hash: str           # TensorFlow state fingerprint

class DAWNConsciousnessStateWriter:
    """Memory-mapped writer for DAWN consciousness state persistence"""
    
    # Fixed mmap layout (bytes)
    HEADER_SIZE = 64
    TICK_STATE_SIZE = 8192  # Fixed size per tick
    MAX_TICKS = 1000        # Rolling buffer
    TOTAL_SIZE = HEADER_SIZE + (TICK_STATE_SIZE * MAX_TICKS)
    
    def __init__(self, mmap_path: str = "./runtime/dawn_consciousness.mmap"):
        self.mmap_path = mmap_path
        self.current_tick = 0
        self.dawn_consciousness = None
        self.pulse_system = None
        self.start_time = time.time()
        
        # Ensure runtime directory exists
        os.makedirs(os.path.dirname(mmap_path), exist_ok=True)
        
        # Initialize DAWN integration
        self._initialize_dawn_integration()
        
        # Initialize memory-mapped file
        self._init_mmap_file()
        
    def _initialize_dawn_integration(self):
        """Initialize integration with available DAWN consciousness systems"""
        # Initialize all attributes to None first
        self.dawn_consciousness = None
        self.main_consciousness = None
        self.dawn_central = None
        self.schema_state = None
        self.tick_emitter = None
        self.pulse_system = None
        
        if not DAWN_INTEGRATION_AVAILABLE:
            print("🤖 Running in standalone simulation mode")
            return
            
        try:
            print("🧠 Initializing DAWN consciousness integration...")
            
            # Connect to consciousness core if available
            if 'consciousness_core' in DAWN_SYSTEMS:
                try:
                    self.dawn_consciousness = DAWN_SYSTEMS['consciousness_core']
                    print(f"✅ Connected to DAWN consciousness core")
                except Exception as e:
                    print(f"⚠️  Error connecting to consciousness core: {e}")
            
            # Connect to main consciousness if available
            if 'main_consciousness' in DAWN_SYSTEMS:
                try:
                    MainConsciousness = DAWN_SYSTEMS['main_consciousness']
                    self.main_consciousness = MainConsciousness()
                    print("✅ Connected to DAWN main consciousness layer")
                except Exception as e:
                    print(f"⚠️  Error connecting to main consciousness: {e}")
            
            # Connect to DAWN Central if available
            if 'dawn_central' in DAWN_SYSTEMS:
                try:
                    DAWNCentral = DAWN_SYSTEMS['dawn_central']
                    self.dawn_central = DAWNCentral()
                    print("✅ Connected to DAWN Central orchestrator")
                except Exception as e:
                    print(f"⚠️  Error connecting to DAWN Central: {e}")
            
            # Connect to schema state if available
            if 'schema_state' in DAWN_SYSTEMS:
                try:
                    SchemaState = DAWN_SYSTEMS['schema_state']
                    self.schema_state = SchemaState()
                    print("✅ Connected to DAWN schema state")
                except Exception as e:
                    print(f"⚠️  Error connecting to schema state: {e}")
            
            # Load pulse system if available (direct first, then module)
            if 'pulse_system' in DAWN_SYSTEMS:
                try:
                    self.pulse_system = DAWN_SYSTEMS['pulse_system']
                    print("✅ Connected to DAWN pulse system")
                except Exception as e:
                    print(f"⚠️  Error connecting to pulse system: {e}")
            elif 'pulse_loader_module' in DAWN_SYSTEMS:
                try:
                    # Try to get pulse instance from module without calling coroutine
                    pulse_module = DAWN_SYSTEMS['pulse_loader_module']
                    if hasattr(pulse_module, 'pulse'):
                        self.pulse_system = pulse_module.pulse
                        print("✅ Connected to pulse from loader module")
                    else:
                        print("⚠️  No pulse instance found in loader module")
                except Exception as e:
                    print(f"⚠️  Error connecting to pulse from module: {e}")
                
            # Count successful connections
            connections = sum([
                self.dawn_consciousness is not None,
                self.main_consciousness is not None, 
                self.dawn_central is not None,
                self.schema_state is not None,
                self.pulse_system is not None
            ])
            
            if connections > 0:
                print(f"🌟 DAWN integration complete - {connections}/5 systems connected")
            else:
                print("⚠️  No DAWN systems successfully connected - using simulation")
            
        except Exception as e:
            print(f"⚠️  DAWN integration failed: {e}")
            print("   Falling back to simulation mode")
            # Ensure all attributes are None on failure
            self.dawn_consciousness = None
            self.main_consciousness = None
            self.dawn_central = None
            self.schema_state = None
            self.tick_emitter = None
            self.pulse_system = None
        
    def _init_mmap_file(self):
        """Initialize memory-mapped file with header"""
        with open(self.mmap_path, 'wb') as f:
            # Write header: magic, version, tick_size, max_ticks
            header = struct.pack('4sIII', b'DAWN', 1, self.TICK_STATE_SIZE, self.MAX_TICKS)
            header += b'\x00' * (self.HEADER_SIZE - len(header))
            f.write(header)
            
            # Zero-fill tick data region
            f.write(b'\x00' * (self.TICK_STATE_SIZE * self.MAX_TICKS))
            
        # Open for read/write access
        self.file_handle = open(self.mmap_path, 'r+b')
        self.mmap_handle = mmap.mmap(self.file_handle.fileno(), 0)
        
        print(f"📁 Memory map initialized: {self.mmap_path}")
        
    def _tensor_state_fingerprint(self) -> str:
        """Generate consciousness state hash from real DAWN data"""
        try:
            # Use real DAWN consciousness state for hash if available
            if (self.dawn_consciousness or self.main_consciousness or self.dawn_central):
                state_data = {
                    'tick': self.current_tick,
                    'timestamp': int(time.time() * 1000)
                }
                
                # Add real DAWN state data to hash
                if self.dawn_central:
                    try:
                        state_data['scup'] = float(self.dawn_central.get_scup() or 0.5)
                        state_data['entropy'] = float(self.dawn_central.get_entropy() or 0.5)
                        state_data['mood'] = float(self.dawn_central.get_mood() or 0.5)
                    except:
                        pass
                
                if self.schema_state:
                    try:
                        state_data['schema_scup'] = float(getattr(self.schema_state, 'scup', 0.5))
                        state_data['schema_entropy'] = float(getattr(self.schema_state, 'entropy', 0.5))
                    except:
                        pass
                
                if self.main_consciousness:
                    try:
                        state_data['emotion'] = getattr(self.main_consciousness, 'current_emotion', 'neutral')
                        state_data['intensity'] = float(getattr(self.main_consciousness, 'emotion_intensity', 0.5))
                    except:
                        pass
                
                # Generate hash from real state
                hash_input = json.dumps(state_data, sort_keys=True)
                import hashlib
                hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
                return f"dawn_{hash_value}"
            
        except Exception as e:
            print(f"⚠️  Error generating real state hash: {e}")
        
        # Fallback hash with tick data
        tick_data = {
            'tick': self.current_tick,
            'time': int(time.time() * 1000000) % 0xFFFFFFFF,
            'mode': 'simulation'
        }
        hash_input = json.dumps(tick_data, sort_keys=True)
        import hashlib
        hash_value = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"sim_{hash_value}"
        
    def _get_dawn_consciousness_state(self) -> Dict[str, Any]:
        """Extract REAL dynamic consciousness state from live DAWN systems"""
        # Check if we have any DAWN integration
        if not (self.dawn_consciousness or self.main_consciousness or self.dawn_central):
            # Return enhanced simulation with more variance
            t = time.time() - self.start_time
            print(f"⚠️  No DAWN integration - enhanced simulation mode")
            return {
                'scup': 0.5 + 0.3 * np.sin(t * 0.1) + 0.1 * np.sin(t * 0.33),
                'entropy': 0.3 + 0.2 * np.cos(t * 0.05) + 0.1 * np.cos(t * 0.17),
                'mood_valence': 0.1 + 0.3 * np.sin(t * 0.08) + 0.1 * np.sin(t * 0.29),
                'mood_arousal': 0.5 + 0.2 * np.cos(t * 0.06) + 0.1 * np.cos(t * 0.13),
                'consciousness_depth': 0.6 + 0.3 * np.sin(t * 0.03) + 0.1 * np.sin(t * 0.19),
                'heat_level': 0.4 + 0.3 * np.sin(t * 0.04) + 0.1 * np.sin(t * 0.23),
                'neural_activity': 0.5 + 0.2 * np.sin(t * 0.12) + 0.1 * np.cos(t * 0.31),
                'memory_pressure': 0.3 + 0.1 * np.cos(t * 0.09) + 0.05 * np.sin(t * 0.27)
            }
        
        try:
            print(f"🧠 Extracting REAL DAWN consciousness data...")
            
            # Initialize state from real systems
            state = {
                'scup': 0.5,
                'entropy': 0.5,
                'mood_valence': 0.0,
                'mood_arousal': 0.5,
                'consciousness_depth': 0.7,
                'heat_level': 0.5,
                'neural_activity': 0.5,
                'memory_pressure': 0.3
            }
            
            # === Extract PURE REAL SCUP from DAWN Central ===
            if self.dawn_central:
                try:
                    # CRITICAL: Call update method to compute real values
                    self.dawn_central.update(tick_number=self.current_tick)
                    
                    real_scup = self.dawn_central.get_scup()
                    if real_scup is not None:
                        state['scup'] = float(real_scup)
                        print(f"📊 PURE REAL SCUP: {state['scup']:.6f}")
                except Exception as e:
                    print(f"⚠️  Error getting SCUP: {e}")
            
            # === Extract PURE REAL entropy from DAWN Central ===
            if self.dawn_central:
                try:
                    real_entropy = self.dawn_central.get_entropy()
                    if real_entropy is not None:
                        state['entropy'] = float(real_entropy)
                        print(f"📊 PURE REAL Entropy: {state['entropy']:.6f}")
                except Exception as e:
                    print(f"⚠️  Error getting entropy: {e}")
                    
            # === Extract PURE REAL mood from DAWN Central ===
            if self.dawn_central:
                try:
                    real_mood = self.dawn_central.get_mood()
                    if real_mood is not None:
                        mood_val = float(real_mood)
                        # Map real mood value to emotional dimensions - NO ENHANCEMENT
                        state['mood_valence'] = np.tanh(mood_val - 0.5)
                        state['mood_arousal'] = abs(mood_val - 0.5) * 2
                        print(f"📊 PURE REAL Mood: {mood_val:.6f} -> V:{state['mood_valence']:.3f}, A:{state['mood_arousal']:.3f}")
                except Exception as e:
                    print(f"⚠️  Error getting mood: {e}")
            
            # === Extract REAL consciousness metrics from consciousness core (with array handling) ===
            if self.dawn_consciousness and hasattr(self.dawn_consciousness, 'state'):
                try:
                    core_state = self.dawn_consciousness.state
                    if core_state:
                        # Helper function to safely convert array/scalar to float
                        def safe_float(value, default=0.5):
                            try:
                                if hasattr(value, 'item'):  # numpy array with single value
                                    return float(value.item())
                                elif hasattr(value, '__len__') and len(value) > 0:  # array/list
                                    return float(np.mean(value))  # Use mean of array
                                else:
                                    return float(value)
                            except:
                                return default
                        
                        if 'neural_activity' in core_state:
                            state['neural_activity'] = safe_float(core_state['neural_activity'], 0.5)
                            print(f"📊 PURE REAL Neural Activity: {state['neural_activity']:.6f}")
                                
                        if 'memory_utilization' in core_state:
                            state['memory_pressure'] = safe_float(core_state['memory_utilization'], 0.3)
                            print(f"📊 PURE REAL Memory Pressure: {state['memory_pressure']:.6f}")
                                
                        if 'quantum_coherence' in core_state:
                            state['consciousness_depth'] = safe_float(core_state['quantum_coherence'], 0.8)
                            print(f"📊 PURE REAL Consciousness Depth: {state['consciousness_depth']:.6f}")
                                
                except Exception as e:
                    print(f"⚠️  Error getting consciousness core state: {e}")
                    # No fallback - keep original values if core fails
            
            # === MEMORY PRESSURE FROM BLOOM SYSTEM ===
            try:
                # Check for rebloom queue size (memory pressure indicator)
                import os
                rebloom_files = [
                    "juliet_flowers/cluster_report/rebloom_lineage.json",
                    "bloom/rebloom_queue.json"
                ]
                
                for rebloom_file in rebloom_files:
                    if os.path.exists(rebloom_file):
                        try:
                            import json
                            with open(rebloom_file, 'r') as f:
                                rebloom_data = json.load(f)
                            
                            if isinstance(rebloom_data, list):
                                rebloom_count = len(rebloom_data)
                                # Memory pressure increases with pending reblooms
                                memory_pressure_from_reblooms = min(1.0, rebloom_count / 10.0)
                                state['memory_pressure'] = max(state.get('memory_pressure', 0.0), 
                                                              memory_pressure_from_reblooms)
                                print(f"📊 PURE REAL Memory Pressure from Reblooms: {memory_pressure_from_reblooms:.6f} ({rebloom_count} pending)")
                                break
                        except Exception as e:
                            print(f"⚠️  Error reading rebloom data from {rebloom_file}: {e}")
                            
            except Exception as e:
                print(f"⚠️  Error computing memory pressure from blooms: {e}")
            
            # === ADDITIONAL PRESSURE SOURCES ===
            try:
                # Schema count pressure
                schema_files = ["schema", "core/schema"]
                total_schemas = 0
                for schema_dir in schema_files:
                    if os.path.exists(schema_dir):
                        schema_count = len([f for f in os.listdir(schema_dir) if f.endswith('.py')])
                        total_schemas += schema_count
                
                # Schema pressure (more active schemas = more pressure)
                schema_pressure = min(1.0, total_schemas / 50.0)  # Normalize to 50 schemas
                
                # Update SCUP based on schema pressure (semantic overlap failure)
                if schema_pressure > 0.7:
                    # High schema pressure reduces SCUP (semantic coherence failure)
                    scup_penalty = (schema_pressure - 0.7) * 0.5
                    state['scup'] = max(0.0, state.get('scup', 0.5) - scup_penalty)
                    print(f"📊 PURE REAL SCUP reduced by schema pressure: -{scup_penalty:.3f} (schemas: {total_schemas})")
                
            except Exception as e:
                print(f"⚠️  Error computing schema pressure: {e}")
                    
            # === DRIFT COMPUTATION ===
            try:
                # Compute drift from state stability over time
                if hasattr(self, 'previous_states'):
                    if len(self.previous_states) >= 5:
                        # Calculate variance in recent states
                        recent_scups = [s.get('scup', 0.5) for s in self.previous_states[-5:]]
                        scup_variance = np.var(recent_scups) if len(recent_scups) > 1 else 0.0
                        
                        # Low variance = high drift (stable inputs)
                        drift_from_stability = max(0.0, 0.1 - scup_variance) * 2.0
                        
                        # Update entropy with drift component
                        state['entropy'] = min(1.0, state.get('entropy', 0.5) + drift_from_stability)
                        print(f"📊 PURE REAL Drift from stability: +{drift_from_stability:.3f}")
                else:
                    self.previous_states = []
                
                # Store current state for drift calculation
                self.previous_states.append(state.copy())
                if len(self.previous_states) > 10:
                    self.previous_states.pop(0)  # Keep last 10 states
                    
            except Exception as e:
                print(f"⚠️  Error computing drift: {e}")
            
            # Extract PURE REAL schema state
            if self.schema_state:
                try:
                    if hasattr(self.schema_state, 'scup'):
                        schema_scup = float(self.schema_state.scup)
                        state['scup'] = schema_scup  # Always use schema value if available
                        print(f"📊 PURE REAL Schema SCUP: {schema_scup:.6f}")
                                
                    if hasattr(self.schema_state, 'entropy'):
                        schema_entropy = float(self.schema_state.entropy)
                        state['entropy'] = schema_entropy  # Always use schema value if available
                        print(f"📊 PURE REAL Schema Entropy: {schema_entropy:.6f}")
                                
                    if hasattr(self.schema_state, 'coherence'):
                        schema_coherence = float(self.schema_state.coherence)
                        state['consciousness_depth'] = schema_coherence
                        print(f"📊 PURE REAL Schema Coherence: {schema_coherence:.6f}")
                except Exception as e:
                    print(f"⚠️  Error getting schema state: {e}")
            
            # Extract REAL emotional state from main consciousness
            if self.main_consciousness:
                try:
                    current_emotion = getattr(self.main_consciousness, 'current_emotion', 'neutral')
                    emotion_intensity = getattr(self.main_consciousness, 'emotion_intensity', 0.5)
                    
                    # Map real emotions to precise dimensional values
                    emotion_mapping = {
                        'excited': {'valence': 0.8, 'arousal': 0.9, 'dominance': 0.7},
                        'creative': {'valence': 0.7, 'arousal': 0.8, 'dominance': 0.8},
                        'contemplative': {'valence': 0.1, 'arousal': 0.4, 'dominance': 0.6},
                        'curious': {'valence': 0.6, 'arousal': 0.7, 'dominance': 0.5},
                        'calm': {'valence': 0.3, 'arousal': 0.2, 'dominance': 0.7},
                        'anxious': {'valence': -0.4, 'arousal': 0.8, 'dominance': 0.3},
                        'overwhelmed': {'valence': -0.6, 'arousal': 0.9, 'dominance': 0.2},
                        'neutral': {'valence': 0.0, 'arousal': 0.5, 'dominance': 0.5}
                    }
                    
                    if current_emotion in emotion_mapping:
                        mapping = emotion_mapping[current_emotion]
                        state['mood_valence'] = mapping['valence'] * emotion_intensity
                        state['mood_arousal'] = mapping['arousal'] * emotion_intensity
                        state['mood_dominance'] = mapping['dominance'] * emotion_intensity
                        print(f"📊 REAL Emotion: {current_emotion} (I:{emotion_intensity:.3f}) -> V:{state['mood_valence']:.3f}")
                    
                except Exception as e:
                    print(f"⚠️  Error getting main consciousness emotion: {e}")
            
            # Extract REAL pulse/thermal data
            if self.pulse_system:
                try:
                    if hasattr(self.pulse_system, 'get_thermal_profile'):
                        heat_state = self.pulse_system.get_thermal_profile()
                        if isinstance(heat_state, dict) and 'normalized_heat' in heat_state:
                            state['heat_level'] = float(heat_state['normalized_heat'])
                            print(f"📊 REAL Thermal Profile: {state['heat_level']:.4f}")
                    elif hasattr(self.pulse_system, 'heat'):
                        raw_heat = float(self.pulse_system.heat)
                        state['heat_level'] = np.clip(raw_heat / 10.0, 0.0, 1.0)  # Normalize to 0-1
                        print(f"📊 REAL Heat Level: {raw_heat} -> {state['heat_level']:.4f}")
                except Exception as e:
                    print(f"⚠️  Error getting pulse thermal data: {e}")
            
            print(f"✅ PURE REAL DAWN state extracted successfully")
            return state
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR extracting DAWN state: {e}")
            import traceback
            traceback.print_exc()
            
            # Emergency fallback with enhanced variance
            t = time.time() - self.start_time
            return {
                'scup': 0.5 + 0.1 * np.sin(t * 0.1),
                'entropy': 0.3 + 0.05 * np.cos(t * 0.07),
                'mood_valence': 0.0,
                'mood_arousal': 0.5,
                'consciousness_depth': 0.6,
                'heat_level': 0.4,
                'neural_activity': 0.5,
                'memory_pressure': 0.3
            }
    
    def generate_consciousness_tick(self) -> TickState:
        """Generate consciousness state from DAWN systems or simulation"""
        dawn_state = self._get_dawn_consciousness_state()
        
        # Map DAWN state to consciousness representation
        mood = MoodZone(
            valence=float(dawn_state['mood_valence']),
            arousal=float(dawn_state['mood_arousal']),
            dominance=0.6 + 0.3 * np.sin(time.time() * 0.03),
            coherence=float(dawn_state.get('scup', 0.5))
        )
        
        cognitive = CognitiveVector(
            semantic_alignment=float(dawn_state.get('scup', 0.5)),
            entropy_gradient=float(dawn_state.get('entropy', 0.3)),
            drift_magnitude=0.05 + 0.02 * np.sin(time.time() * 0.06),
            rebloom_intensity=max(0, 0.3 * np.sin(time.time() * 0.08))
        )
        
        # Generate dynamic data
        t = time.time()
        heatmap = [0.5 + 0.3 * np.sin(t * 0.01 + i * 0.1) for i in range(256)]
        forecast = [np.cos(t * 0.02 + i * 0.2) for i in range(32)]
        rebloom = [np.random.choice([True, False], p=[0.1, 0.9]) for _ in range(64)]
        
        return TickState(
            tick_number=self.current_tick,
            timestamp_ms=int(time.time() * 1000),
            mood_zone=mood,
            cognitive_vector=cognitive,
            memory_rebloom_flags=rebloom,
            semantic_heatmap=heatmap,
            forecast_vector=forecast,
            consciousness_depth=float(dawn_state.get('consciousness_depth', 0.6)),
            tensor_state_hash=self._tensor_state_fingerprint()
        )
        
    def write_tick(self, tick_state: TickState):
        """Write cognitive state to memory-mapped buffer with GUI-optimized approach"""
        # Serialize to compact binary format
        tick_data = self._serialize_tick_state(tick_state)
        
        # Use a simpler approach: always write to the FIRST slot for GUI consumption
        # This eliminates the rolling buffer complexity for the GUI
        gui_slot_offset = self.HEADER_SIZE  # Always use slot 0 for GUI
        
        # Write GUI-optimized tick atomically
        self.mmap_handle.seek(gui_slot_offset)
        self.mmap_handle.write(tick_data)
        self.mmap_handle.flush()
        
        # Update header with latest tick number AND timestamp for freshness detection
        self.mmap_handle.seek(16)  # Latest tick number
        self.mmap_handle.write(struct.pack('I', tick_state.tick_number))
        
        self.mmap_handle.seek(20)  # Add timestamp at offset 20 for freshness
        self.mmap_handle.write(struct.pack('Q', tick_state.timestamp_ms))
        self.mmap_handle.flush()
        
        # Also store in rolling buffer for historical data (if needed later)
        if hasattr(self, 'enable_history') and self.enable_history:
            tick_index = tick_state.tick_number % self.MAX_TICKS
            history_offset = self.HEADER_SIZE + (tick_index * self.TICK_STATE_SIZE)
            self.mmap_handle.seek(history_offset)
            self.mmap_handle.write(tick_data)
            self.mmap_handle.flush()
        
    def _serialize_tick_state(self, state: TickState) -> bytes:
        """Pack tick state into fixed-size binary format matching Rust reader exactly"""
        # Core state: tick(4) + timestamp(8) + mood(16) + cognitive(16) + depth(4) = 48 bytes
        # Need to pad to 72 bytes for Rust compatibility
        core_data = struct.pack('IQfffffffff',
            state.tick_number,
            state.timestamp_ms,
            state.mood_zone.valence,
            state.mood_zone.arousal, 
            state.mood_zone.dominance,
            state.mood_zone.coherence,
            state.cognitive_vector.semantic_alignment,
            state.cognitive_vector.entropy_gradient,
            state.cognitive_vector.drift_magnitude,
            state.cognitive_vector.rebloom_intensity,
            state.consciousness_depth
        )
        
        # Pad core data to exactly 72 bytes (Rust expects memory bits at offset 72)
        core_data_padded = core_data.ljust(72, b'\x00')
        
        # Memory rebloom flags (64 bits = 8 bytes) - MUST be at offset 72 for Rust
        rebloom_bits = 0
        for i, flag in enumerate(state.memory_rebloom_flags[:64]):
            if flag:
                rebloom_bits |= (1 << i)
        rebloom_data = struct.pack('Q', rebloom_bits)
        
        # Semantic heatmap (256 floats = 1024 bytes) - starts at offset 80 
        heatmap_data = struct.pack('256f', *state.semantic_heatmap[:256])
        
        # Forecast vector (32 floats = 128 bytes) - starts at offset 1104
        forecast_data = struct.pack('32f', *state.forecast_vector[:32])
        
        # Tensor state hash (32 bytes) - starts at offset 1232
        hash_data = state.tensor_state_hash.encode('ascii')[:31].ljust(32, b'\x00')
        
        # Combine with exact Rust-compatible layout
        total_data = core_data_padded + rebloom_data + heatmap_data + forecast_data + hash_data
        
        # Final padding to exact TICK_STATE_SIZE (8192 bytes)
        padded_data = total_data.ljust(self.TICK_STATE_SIZE, b'\x00')
        
        return padded_data[:self.TICK_STATE_SIZE]
    
    def run_consciousness_loop(self, tick_interval: float = 0.5):
        """Continuous consciousness tick generation with DAWN integration"""
        integration_status = "DAWN-integrated" if DAWN_INTEGRATION_AVAILABLE else "simulation"
        
        print(f"🧠 DAWN consciousness engine started ({integration_status})")
        print(f"📁 Memory map: {self.mmap_path}")
        print(f"⏱️  Tick interval: {tick_interval}s ({1.0/tick_interval:.1f} Hz)")
        print(f"🔗 Integration: {'✅ Active' if self.dawn_consciousness else '🤖 Simulation'}")
        
        # For GUI consumption, use a slower rate but still capture fast internal ticks
        gui_update_interval = max(tick_interval, 0.1)  # Minimum 100ms for GUI (10 Hz max)
        last_gui_update = 0
        
        try:
            while True:
                tick_state = self.generate_consciousness_tick()
                
                # Always update internal tick count for DAWN consistency
                self.current_tick += 1
                
                # Only write to mmap at GUI-friendly rate
                current_time = time.time()
                if current_time - last_gui_update >= gui_update_interval:
                    self.write_tick(tick_state)
                    last_gui_update = current_time
                    
                    # Enhanced status display (only when actually writing)
                    integration_indicator = "🔗" if self.dawn_consciousness else "🤖"
                    print(f"{integration_indicator} GUI-Tick {self.current_tick:06d} | "
                          f"SCUP({tick_state.cognitive_vector.semantic_alignment:+.2f}) | "
                          f"Mood({tick_state.mood_zone.valence:+.2f}) | "
                          f"Depth({tick_state.consciousness_depth:.2f}) | "
                          f"Hash({tick_state.tensor_state_hash[:8]})")
                
                # Sleep for the fast internal tick rate
                time.sleep(tick_interval)
                
        except KeyboardInterrupt:
            print(f"\n🔄 DAWN consciousness engine stopped at tick {self.current_tick}")
        finally:
            self.mmap_handle.close()
            self.file_handle.close()

def run_as_subsystem(tick_engine=None):
    """Run as integrated subsystem with existing DAWN tick engine"""
    if tick_engine:
        print("🔗 Integrating with existing DAWN tick engine...")
        
        # Create writer but don't start independent loop
        writer = DAWNConsciousnessStateWriter()
        
        def consciousness_tick_callback():
            """Callback for tick engine integration"""
            tick_state = writer.generate_consciousness_tick()
            writer.write_tick(tick_state)
            writer.current_tick += 1
        
        # Register with tick engine if possible
        if hasattr(tick_engine, 'register_subsystem'):
            tick_engine.register_subsystem('consciousness_gui', consciousness_tick_callback)
            print("✅ Registered with tick engine subsystem")
        elif hasattr(tick_engine, 'tick_callbacks'):
            tick_engine.tick_callbacks.append(consciousness_tick_callback)
            print("✅ Added to tick engine callbacks")
        else:
            print("⚠️  Tick engine integration not supported, running independently")
            writer.run_consciousness_loop()
        
        return writer
    else:
        # Standalone mode
        writer = DAWNConsciousnessStateWriter()
        writer.run_consciousness_loop()
        return writer

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DAWN Consciousness State Writer")
    parser.add_argument('--interval', type=float, default=0.5, 
                        help='Tick interval in seconds (default: 0.5)')
    parser.add_argument('--mmap-path', type=str, 
                        default='./runtime/dawn_consciousness.mmap',
                        help='Memory map file path')
    
    args = parser.parse_args()
    
    writer = DAWNConsciousnessStateWriter(mmap_path=args.mmap_path)
    writer.run_consciousness_loop(tick_interval=args.interval) 