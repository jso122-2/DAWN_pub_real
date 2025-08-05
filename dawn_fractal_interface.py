#!/usr/bin/env python3
"""
DAWN Fractal Interface
=====================

Production interface for connecting DAWN's live consciousness state to the 
fractal generation system with intelligent caching, concurrent processing,
and real-time bloom generation.

This interface sits between DAWN's consciousness core and the visualization
pipeline, providing seamless integration without blocking main consciousness loops.
"""

import asyncio
import threading
import time
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, deque
import sqlite3
import pickle

# Import DAWN consciousness systems
from dawn_state_parser import DAWNStateParser, DAWNConsciousnessConfig
from dawn_shape_complexity import calculate_shape_complexity
from dawn_mood_palette import generate_mood_palette
from dawn_drift_transformation import apply_drift_transformation

@dataclass
class BloomCacheEntry:
    """Cache entry for generated bloom fractals"""
    
    cache_key: str
    config: DAWNConsciousnessConfig
    generated_timestamp: float
    access_count: int
    last_accessed: float
    fractal_data: Optional[Dict[str, Any]]
    file_path: Optional[str]
    
    # Visual characteristics for similarity matching
    visual_signature: Dict[str, float]
    
    def is_expired(self, max_age_seconds: float = 3600) -> bool:
        """Check if cache entry is expired"""
        return (time.time() - self.generated_timestamp) > max_age_seconds
    
    def calculate_similarity(self, other_config: DAWNConsciousnessConfig) -> float:
        """Calculate similarity to another consciousness configuration"""
        
        # Parameter-based similarity
        param_diffs = [
            abs(self.config.bloom_entropy - other_config.bloom_entropy),
            abs(self.config.mood_valence - other_config.mood_valence),
            abs(self.config.drift_vector - other_config.drift_vector),
            abs(self.config.rebloom_depth - other_config.rebloom_depth),
            abs(self.config.sigil_saturation - other_config.sigil_saturation)
        ]
        
        # Pulse zone similarity (categorical)
        pulse_similarity = 1.0 if self.config.pulse_zone == other_config.pulse_zone else 0.5
        
        # Combined similarity score (lower = more similar)
        param_distance = np.mean(param_diffs)
        overall_similarity = 1.0 - (param_distance * 0.8 + (1.0 - pulse_similarity) * 0.2)
        
        return max(0.0, overall_similarity)

@dataclass 
class StateChangeEvent:
    """Event triggered when DAWN's consciousness state changes"""
    
    previous_state: Optional[DAWNConsciousnessConfig]
    current_state: DAWNConsciousnessConfig
    change_magnitude: float
    significant_change: bool
    timestamp: float

class DAWNStateMonitor:
    """Monitors DAWN's consciousness state for significant changes"""
    
    def __init__(self, change_threshold: float = 0.1):
        self.change_threshold = change_threshold
        self.current_state: Optional[DAWNConsciousnessConfig] = None
        self.state_history: deque = deque(maxlen=100)
        
        # Event callbacks
        self.change_callbacks: List[Callable[[StateChangeEvent], None]] = []
        
        # State monitoring
        self.monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.monitor_interval = 0.5  # 500ms monitoring interval
    
    def add_change_callback(self, callback: Callable[[StateChangeEvent], None]):
        """Add callback for state change events"""
        self.change_callbacks.append(callback)
    
    def calculate_change_magnitude(self, prev_state: DAWNConsciousnessConfig, 
                                 current_state: DAWNConsciousnessConfig) -> float:
        """Calculate magnitude of change between two states"""
        
        changes = [
            abs(prev_state.bloom_entropy - current_state.bloom_entropy),
            abs(prev_state.mood_valence - current_state.mood_valence) / 2.0,  # Normalized to 0-1
            abs(prev_state.drift_vector - current_state.drift_vector) / 2.0,
            abs(prev_state.rebloom_depth - current_state.rebloom_depth) / 20.0,  # Normalized
            abs(prev_state.sigil_saturation - current_state.sigil_saturation)
        ]
        
        # Pulse zone change
        pulse_change = 0.0 if prev_state.pulse_zone == current_state.pulse_zone else 0.2
        
        # Weighted average of changes
        return np.mean(changes) + pulse_change
    
    def update_state(self, new_state: DAWNConsciousnessConfig):
        """Update with new consciousness state and check for significant changes"""
        
        previous_state = self.current_state
        self.current_state = new_state
        
        # Add to history
        self.state_history.append((time.time(), new_state))
        
        # Check for significant change
        if previous_state:
            change_magnitude = self.calculate_change_magnitude(previous_state, new_state)
            significant_change = change_magnitude >= self.change_threshold
            
            # Create change event
            event = StateChangeEvent(
                previous_state=previous_state,
                current_state=new_state,
                change_magnitude=change_magnitude,
                significant_change=significant_change,
                timestamp=time.time()
            )
            
            # Notify callbacks
            for callback in self.change_callbacks:
                try:
                    callback(event)
                except Exception as e:
                    print(f"⚠️  State change callback error: {e}")
    
    def start_monitoring(self, state_source_path: str):
        """Start monitoring DAWN state files for changes"""
        
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(state_source_path,),
            daemon=True
        )
        self.monitor_thread.start()
        print(f"🔍 Started DAWN state monitoring: {state_source_path}")
    
    def stop_monitoring(self):
        """Stop state monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        print("⏹️  Stopped DAWN state monitoring")
    
    def _monitor_loop(self, state_source_path: str):
        """Main monitoring loop"""
        
        parser = DAWNStateParser(strict_validation=False)
        last_modification_times = {}
        
        while self.monitoring:
            try:
                # Check for new or modified state files
                state_dir = Path(state_source_path)
                if state_dir.exists():
                    
                    # Look for recent JSON files
                    json_files = list(state_dir.glob("*.json"))
                    
                    for json_file in json_files:
                        mod_time = json_file.stat().st_mtime
                        
                        # Check if file is new or modified
                        if (json_file not in last_modification_times or 
                            mod_time > last_modification_times[json_file]):
                            
                            try:
                                # Parse state file
                                config = parser.parse_file(json_file)
                                if config and config.validation_passed:
                                    self.update_state(config)
                                    last_modification_times[json_file] = mod_time
                                    
                            except Exception as e:
                                print(f"⚠️  Error parsing state file {json_file}: {e}")
                
                time.sleep(self.monitor_interval)
                
            except Exception as e:
                print(f"⚠️  State monitoring error: {e}")
                time.sleep(1.0)

class BloomArchive:
    """Archive system for storing and retrieving bloom sequences"""
    
    def __init__(self, archive_dir: str = "dawn_bloom_archive"):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)
        
        # SQLite database for bloom metadata
        self.db_path = self.archive_dir / "bloom_metadata.db"
        self._init_database()
        
        print(f"📁 Bloom archive initialized: {self.archive_dir}")
    
    def _init_database(self):
        """Initialize SQLite database for bloom metadata"""
        
        try:
            # Use timeout and WAL mode for better concurrency
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA synchronous=NORMAL")
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS blooms (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cache_key TEXT UNIQUE,
                    memory_id TEXT,
                    timestamp REAL,
                    bloom_entropy REAL,
                    mood_valence REAL,
                    drift_vector REAL,
                    rebloom_depth INTEGER,
                    sigil_saturation REAL,
                    pulse_zone TEXT,
                    archetype TEXT,
                    file_path TEXT,
                    visual_complexity REAL,
                    color_variance REAL,
                    motion_magnitude REAL,
                    fractal_string TEXT
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON blooms(timestamp)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_parameters ON blooms(
                    bloom_entropy, mood_valence, drift_vector, rebloom_depth
                )
            """)
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"⚠️  Database initialization error: {e}")
            # Create a simpler fallback database
            self.db_path = self.archive_dir / f"bloom_metadata_{int(time.time())}.db"
    
    def store_bloom(self, cache_entry: BloomCacheEntry):
        """Store bloom in archive database"""
        
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            conn.execute("PRAGMA journal_mode=WAL")
            
            conn.execute("""
                INSERT OR REPLACE INTO blooms (
                    cache_key, memory_id, timestamp, bloom_entropy, mood_valence,
                    drift_vector, rebloom_depth, sigil_saturation, pulse_zone,
                    archetype, file_path, visual_complexity, color_variance,
                    motion_magnitude, fractal_string
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                cache_entry.cache_key,
                cache_entry.config.memory_id,
                cache_entry.generated_timestamp,
                cache_entry.config.bloom_entropy,
                cache_entry.config.mood_valence,
                cache_entry.config.drift_vector,
                cache_entry.config.rebloom_depth,
                cache_entry.config.sigil_saturation,
                cache_entry.config.pulse_zone,
                cache_entry.config.archetype,
                cache_entry.file_path,
                cache_entry.visual_signature.get('complexity', 0.0),
                cache_entry.visual_signature.get('color_variance', 0.0),
                cache_entry.visual_signature.get('motion_magnitude', 0.0),
                cache_entry.visual_signature.get('fractal_string', '')
            ))
            
            conn.commit()
            conn.close()
                
        except Exception as e:
            print(f"⚠️  Error storing bloom in archive: {e}")
    
    def retrieve_time_range(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Retrieve blooms from a specific time range"""
        
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.execute("""
                SELECT * FROM blooms 
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp ASC
            """, (start_time, end_time))
            
            columns = [desc[0] for desc in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()
            
            return results
                
        except Exception as e:
            print(f"⚠️  Error retrieving blooms from archive: {e}")
            return []
    
    def find_similar_blooms(self, target_config: DAWNConsciousnessConfig, 
                          similarity_threshold: float = 0.7,
                          max_results: int = 10) -> List[Dict[str, Any]]:
        """Find blooms similar to target configuration"""
        
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            
            # Query recent blooms (within reasonable parameter ranges)
            cursor = conn.execute("""
                SELECT * FROM blooms 
                WHERE ABS(bloom_entropy - ?) < 0.3
                AND ABS(mood_valence - ?) < 0.6
                AND ABS(drift_vector - ?) < 0.6
                AND ABS(rebloom_depth - ?) < 5
                ORDER BY timestamp DESC
                LIMIT 50
            """, (
                target_config.bloom_entropy,
                target_config.mood_valence,
                target_config.drift_vector,
                target_config.rebloom_depth
            ))
            
            columns = [desc[0] for desc in cursor.description]
            candidates = [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.close()
                
                # Calculate precise similarity scores
                similar_blooms = []
                for bloom_data in candidates:
                    # Create temporary config for similarity calculation
                    bloom_config = DAWNConsciousnessConfig(
                        memory_id=bloom_data['memory_id'],
                        timestamp=None,
                        bloom_entropy=bloom_data['bloom_entropy'],
                        mood_valence=bloom_data['mood_valence'],
                        drift_vector=bloom_data['drift_vector'],
                        rebloom_depth=bloom_data['rebloom_depth'],
                        sigil_saturation=bloom_data['sigil_saturation'],
                        pulse_zone=bloom_data['pulse_zone']
                    )
                    
                    # Calculate similarity using the same logic as BloomCacheEntry
                    param_diffs = [
                        abs(bloom_config.bloom_entropy - target_config.bloom_entropy),
                        abs(bloom_config.mood_valence - target_config.mood_valence),
                        abs(bloom_config.drift_vector - target_config.drift_vector),
                        abs(bloom_config.rebloom_depth - target_config.rebloom_depth),
                        abs(bloom_config.sigil_saturation - target_config.sigil_saturation)
                    ]
                    
                    pulse_similarity = 1.0 if bloom_config.pulse_zone == target_config.pulse_zone else 0.5
                    param_distance = np.mean(param_diffs)
                    similarity = 1.0 - (param_distance * 0.8 + (1.0 - pulse_similarity) * 0.2)
                    
                    if similarity >= similarity_threshold:
                        bloom_data['similarity_score'] = similarity
                        similar_blooms.append(bloom_data)
                
                # Sort by similarity and return top results
                similar_blooms.sort(key=lambda x: x['similarity_score'], reverse=True)
                return similar_blooms[:max_results]
                
        except Exception as e:
            print(f"⚠️  Error finding similar blooms: {e}")
            return []

class DAWNFractalInterface:
    """
    Production interface for DAWN's consciousness-driven fractal generation system.
    
    Provides real-time, cached, concurrent fractal generation connected to 
    DAWN's live consciousness state without blocking main consciousness loops.
    """
    
    def __init__(self, 
                 output_dir: str = "dawn_live_fractals",
                 cache_size: int = 100,
                 max_concurrent_jobs: int = 3,
                 state_monitor_path: str = "runtime/consciousness"):
        
        # Core configuration
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Cache system
        self.cache_size = cache_size
        self.bloom_cache: Dict[str, BloomCacheEntry] = {}
        self.cache_access_order: deque = deque(maxlen=cache_size)
        
        # Concurrency control
        self.max_concurrent_jobs = max_concurrent_jobs
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent_jobs)
        self.active_jobs: Dict[str, Any] = {}
        
        # State monitoring
        self.state_monitor = DAWNStateMonitor(change_threshold=0.08)
        self.state_monitor.add_change_callback(self._on_state_change)
        
        # Archive system
        self.archive = BloomArchive(self.output_dir / "archive")
        
        # Generation statistics
        self.stats = {
            'total_generations': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'concurrent_generations': 0,
            'average_generation_time': 0.0
        }
        
        # Auto-start state monitoring
        if Path(state_monitor_path).exists():
            self.state_monitor.start_monitoring(state_monitor_path)
        
        print(f"🎨 DAWN Fractal Interface initialized")
        print(f"   Output: {self.output_dir}")
        print(f"   Cache size: {cache_size}")
        print(f"   Max concurrent: {max_concurrent_jobs}")
        print(f"   State monitoring: {state_monitor_path}")
    
    def _create_cache_key(self, config: DAWNConsciousnessConfig) -> str:
        """Create cache key from consciousness configuration"""
        
        # Round parameters to avoid cache misses for tiny differences
        rounded_params = {
            'entropy': round(config.bloom_entropy, 2),
            'valence': round(config.mood_valence, 2),
            'drift': round(config.drift_vector, 2),
            'depth': config.rebloom_depth,
            'saturation': round(config.sigil_saturation, 2),
            'zone': config.pulse_zone
        }
        
        # Create hash-based cache key
        param_string = json.dumps(rounded_params, sort_keys=True)
        return hashlib.md5(param_string.encode()).hexdigest()[:12]
    
    def _calculate_visual_signature(self, config: DAWNConsciousnessConfig) -> Dict[str, float]:
        """Calculate visual signature for a consciousness configuration"""
        
        # Generate components without full rendering
        shape_complexity = calculate_shape_complexity(config.bloom_entropy, config.rebloom_depth)
        mood_palette = generate_mood_palette(config.mood_valence, config.sigil_saturation)
        
        # Create visual signature
        signature = {
            'complexity': shape_complexity.chaos_factor,
            'edge_roughness': shape_complexity.edge_roughness,
            'color_variance': np.std(mood_palette.base_colors) / 255.0,
            'petal_count': float(shape_complexity.petal_count),
            'motion_potential': abs(config.drift_vector) if config.pulse_zone == 'flowing' else 0.0,
            'fractal_string': f"R{shape_complexity.recursion_levels}-E{int(config.bloom_entropy*10)}-V{int((config.mood_valence+1)*5)}"
        }
        
        return signature
    
    def _get_from_cache(self, cache_key: str) -> Optional[BloomCacheEntry]:
        """Retrieve bloom from cache"""
        
        if cache_key in self.bloom_cache:
            entry = self.bloom_cache[cache_key]
            
            # Check if expired
            if entry.is_expired():
                del self.bloom_cache[cache_key]
                return None
            
            # Update access statistics
            entry.access_count += 1
            entry.last_accessed = time.time()
            self.stats['cache_hits'] += 1
            
            # Move to end of access order
            if cache_key in self.cache_access_order:
                self.cache_access_order.remove(cache_key)
            self.cache_access_order.append(cache_key)
            
            return entry
        
        self.stats['cache_misses'] += 1
        return None
    
    def _store_in_cache(self, entry: BloomCacheEntry):
        """Store bloom in cache with LRU eviction"""
        
        # Add to cache
        self.bloom_cache[entry.cache_key] = entry
        self.cache_access_order.append(entry.cache_key)
        
        # Evict oldest entries if cache is full
        while len(self.bloom_cache) > self.cache_size:
            oldest_key = self.cache_access_order.popleft()
            if oldest_key in self.bloom_cache:
                del self.bloom_cache[oldest_key]
        
        # Store in archive
        try:
            self.archive.store_bloom(entry)
        except Exception as e:
            print(f"⚠️  Error archiving bloom: {e}")
    
    def _generate_fractal_data(self, config: DAWNConsciousnessConfig) -> Dict[str, Any]:
        """Generate fractal data from consciousness configuration"""
        
        start_time = time.time()
        
        try:
            # Generate consciousness components
            shape_complexity = calculate_shape_complexity(config.bloom_entropy, config.rebloom_depth)
            mood_palette = generate_mood_palette(config.mood_valence, config.sigil_saturation)
            
            # Create base fractal coordinates
            petal_count = shape_complexity.petal_count
            point_count = petal_count * 12  # Detailed resolution
            
            angles = np.linspace(0, 2*np.pi, point_count, endpoint=False)
            
            # Apply shape complexity
            edge_modulation = 1.0 + shape_complexity.edge_roughness * 0.4 * np.sin(angles * petal_count)
            radius = edge_modulation * (1.0 + 0.3 * np.sin(angles * petal_count / 2))
            
            base_coords = np.column_stack([
                radius * np.cos(angles),
                radius * np.sin(angles)
            ])
            
            # Apply drift transformation
            drift_transformation = apply_drift_transformation(
                base_coords, config.drift_vector, config.pulse_zone
            )
            
            # Package fractal data
            fractal_data = {
                'coordinates': drift_transformation.transformed_coords.tolist(),
                'center_offset': drift_transformation.center_offset,
                'rotation_angle': drift_transformation.rotation_angle,
                'transparency_map': drift_transformation.transparency_map.tolist() if drift_transformation.transparency_map is not None else None,
                'motion_vectors': drift_transformation.motion_vectors.tolist() if drift_transformation.motion_vectors is not None else None,
                'expansion_factor': drift_transformation.expansion_factor.tolist() if drift_transformation.expansion_factor is not None else None,
                'shape_complexity': asdict(shape_complexity),
                'mood_palette': {
                    'base_colors': mood_palette.base_colors,
                    'glow_colors': mood_palette.glow_colors,
                    'palette_name': mood_palette.palette_name,
                    'brightness_multiplier': mood_palette.brightness_multiplier
                },
                'generation_time': time.time() - start_time,
                'timestamp': time.time()
            }
            
            return fractal_data
            
        except Exception as e:
            print(f"⚠️  Error generating fractal data: {e}")
            return {
                'error': str(e),
                'generation_time': time.time() - start_time,
                'timestamp': time.time()
            }
    
    def _on_state_change(self, event: StateChangeEvent):
        """Handle DAWN state change events"""
        
        if event.significant_change:
            print(f"🔄 Significant state change detected (magnitude: {event.change_magnitude:.3f})")
            
            # Trigger automatic fractal generation
            try:
                self.generate_memory_bloom(event.current_state, priority=True)
            except Exception as e:
                print(f"⚠️  Error generating bloom for state change: {e}")
    
    async def generate_memory_bloom(self, 
                                  current_state: DAWNConsciousnessConfig,
                                  priority: bool = False,
                                  force_regenerate: bool = False) -> Optional[BloomCacheEntry]:
        """
        Generate memory bloom fractal for current consciousness state.
        
        Args:
            current_state: Current DAWN consciousness configuration
            priority: If True, prioritize this generation
            force_regenerate: If True, bypass cache and regenerate
            
        Returns:
            BloomCacheEntry with generated fractal data
        """
        
        # Create cache key
        cache_key = self._create_cache_key(current_state)
        
        # Check cache first (unless forced regeneration)
        if not force_regenerate:
            cached_entry = self._get_from_cache(cache_key)
            if cached_entry:
                print(f"💾 Cache hit for bloom: {cache_key}")
                return cached_entry
        
        # Check if already generating
        if cache_key in self.active_jobs:
            print(f"⏳ Bloom already generating: {cache_key}")
            # Wait for existing job (if priority)
            if priority:
                try:
                    return await asyncio.wrap_future(self.active_jobs[cache_key])
                except Exception as e:
                    print(f"⚠️  Error waiting for bloom generation: {e}")
            return None
        
        # Submit generation job
        print(f"🎨 Generating new bloom: {cache_key}")
        
        future = self.executor.submit(self._generate_bloom_job, current_state, cache_key)
        self.active_jobs[cache_key] = future
        
        try:
            # Wait for completion (async)
            result = await asyncio.wrap_future(future)
            
            # Remove from active jobs
            if cache_key in self.active_jobs:
                del self.active_jobs[cache_key]
            
            return result
            
        except Exception as e:
            print(f"⚠️  Error in bloom generation: {e}")
            if cache_key in self.active_jobs:
                del self.active_jobs[cache_key]
            return None
    
    def _generate_bloom_job(self, config: DAWNConsciousnessConfig, cache_key: str) -> BloomCacheEntry:
        """Worker function for bloom generation"""
        
        start_time = time.time()
        
        try:
            # Generate fractal data
            fractal_data = self._generate_fractal_data(config)
            
            # Calculate visual signature
            visual_signature = self._calculate_visual_signature(config)
            
            # Create output file path
            timestamp_str = time.strftime('%Y%m%d_%H%M%S', time.localtime())
            file_path = self.output_dir / f"bloom_{timestamp_str}_{cache_key}.json"
            
            # Save fractal data to file
            with open(file_path, 'w') as f:
                json.dump({
                    'consciousness_config': asdict(config),
                    'fractal_data': fractal_data,
                    'visual_signature': visual_signature,
                    'cache_key': cache_key,
                    'generated_timestamp': start_time
                }, f, indent=2)
            
            # Create cache entry
            cache_entry = BloomCacheEntry(
                cache_key=cache_key,
                config=config,
                generated_timestamp=start_time,
                access_count=1,
                last_accessed=time.time(),
                fractal_data=fractal_data,
                file_path=str(file_path),
                visual_signature=visual_signature
            )
            
            # Store in cache
            self._store_in_cache(cache_entry)
            
            # Update statistics
            generation_time = time.time() - start_time
            self.stats['total_generations'] += 1
            
            # Update average generation time
            total_time = self.stats['average_generation_time'] * (self.stats['total_generations'] - 1)
            self.stats['average_generation_time'] = (total_time + generation_time) / self.stats['total_generations']
            
            print(f"✅ Bloom generated: {cache_key} ({generation_time:.2f}s)")
            
            return cache_entry
            
        except Exception as e:
            print(f"❌ Bloom generation failed: {cache_key} - {e}")
            raise
    
    def archive_bloom_sequence(self, 
                             start_time: float, 
                             end_time: float,
                             sequence_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Archive a sequence of blooms from a specific time range.
        
        Args:
            start_time: Start timestamp
            end_time: End timestamp  
            sequence_name: Optional name for the sequence
            
        Returns:
            Dictionary with archive results
        """
        
        print(f"📦 Archiving bloom sequence: {start_time} to {end_time}")
        
        # Retrieve blooms from time range
        blooms = self.archive.retrieve_time_range(start_time, end_time)
        
        if not blooms:
            print(f"⚠️  No blooms found in time range")
            return {'sequence_name': sequence_name, 'bloom_count': 0, 'blooms': []}
        
        # Create sequence archive
        if not sequence_name:
            sequence_name = f"sequence_{int(start_time)}_{int(end_time)}"
        
        sequence_data = {
            'sequence_name': sequence_name,
            'start_time': start_time,
            'end_time': end_time,
            'bloom_count': len(blooms),
            'blooms': blooms,
            'archived_timestamp': time.time()
        }
        
        # Save sequence archive
        archive_path = self.archive.archive_dir / f"{sequence_name}.json"
        try:
            with open(archive_path, 'w') as f:
                json.dump(sequence_data, f, indent=2)
            
            print(f"✅ Archived {len(blooms)} blooms to: {archive_path}")
            
        except Exception as e:
            print(f"⚠️  Error saving sequence archive: {e}")
        
        return sequence_data
    
    def retrieve_similar_blooms(self, 
                              target_params: DAWNConsciousnessConfig,
                              similarity_threshold: float = 0.7,
                              max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve blooms similar to target consciousness parameters.
        
        Args:
            target_params: Target consciousness configuration
            similarity_threshold: Minimum similarity score (0.0 to 1.0)
            max_results: Maximum number of results to return
            
        Returns:
            List of similar bloom entries with similarity scores
        """
        
        print(f"🔍 Finding blooms similar to: entropy={target_params.bloom_entropy:.2f}, "
              f"valence={target_params.mood_valence:.2f}, depth={target_params.rebloom_depth}")
        
        # Search archive for similar blooms
        similar_blooms = self.archive.find_similar_blooms(
            target_params, similarity_threshold, max_results
        )
        
        print(f"✅ Found {len(similar_blooms)} similar blooms")
        
        return similar_blooms
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """Get cache and generation statistics"""
        
        cache_efficiency = (
            self.stats['cache_hits'] / max(1, self.stats['cache_hits'] + self.stats['cache_misses'])
        )
        
        return {
            'cache_size': len(self.bloom_cache),
            'cache_max_size': self.cache_size,
            'cache_efficiency': cache_efficiency,
            'total_generations': self.stats['total_generations'],
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses'],
            'active_jobs': len(self.active_jobs),
            'average_generation_time': self.stats['average_generation_time']
        }
    
    def shutdown(self):
        """Gracefully shutdown the interface"""
        
        print("🔄 Shutting down DAWN Fractal Interface...")
        
        # Stop state monitoring
        self.state_monitor.stop_monitoring()
        
        # Wait for active jobs to complete
        if self.active_jobs:
            print(f"⏳ Waiting for {len(self.active_jobs)} active jobs to complete...")
            for future in self.active_jobs.values():
                try:
                    future.result(timeout=30.0)
                except Exception as e:
                    print(f"⚠️  Job completion error: {e}")
        
        # Shutdown executor
        self.executor.shutdown(wait=True, timeout=30.0)
        
        print("✅ DAWN Fractal Interface shutdown complete")

# Example integration functions

async def demo_live_fractal_generation():
    """Demonstrate live fractal generation with state changes"""
    
    interface = DAWNFractalInterface()
    
    print("\n🎨 DAWN Live Fractal Generation Demo")
    print("=" * 40)
    
    try:
        # Simulate different consciousness states
        test_states = [
            DAWNConsciousnessConfig(
                memory_id="demo_calm", timestamp=None,
                bloom_entropy=0.2, mood_valence=0.5, drift_vector=0.1,
                rebloom_depth=4, sigil_saturation=0.6, pulse_zone="calm"
            ),
            DAWNConsciousnessConfig(
                memory_id="demo_chaos", timestamp=None,
                bloom_entropy=0.8, mood_valence=-0.3, drift_vector=-0.7,
                rebloom_depth=8, sigil_saturation=0.9, pulse_zone="surge"
            ),
            DAWNConsciousnessConfig(
                memory_id="demo_flow", timestamp=None,
                bloom_entropy=0.4, mood_valence=0.2, drift_vector=0.5,
                rebloom_depth=6, sigil_saturation=0.7, pulse_zone="flowing"
            )
        ]
        
        # Generate blooms for each state
        for i, state in enumerate(test_states):
            print(f"\n🎯 Generating bloom {i+1}/3: {state.memory_id}")
            
            bloom = await interface.generate_memory_bloom(state, priority=True)
            if bloom:
                print(f"   ✅ Generated: {bloom.cache_key}")
                print(f"   📊 Complexity: {bloom.visual_signature.get('complexity', 0):.3f}")
                print(f"   🎨 Color variance: {bloom.visual_signature.get('color_variance', 0):.3f}")
        
        # Test cache efficiency
        print(f"\n💾 Testing cache efficiency...")
        
        # Re-request same states (should hit cache)
        for state in test_states[:2]:
            bloom = await interface.generate_memory_bloom(state)
            print(f"   💾 Cache result: {bloom.cache_key if bloom else 'None'}")
        
        # Test similarity search
        print(f"\n🔍 Testing similarity search...")
        similar = interface.retrieve_similar_blooms(test_states[0], similarity_threshold=0.5)
        print(f"   🎯 Found {len(similar)} similar blooms")
        
        # Display statistics
        stats = interface.get_cache_statistics()
        print(f"\n📊 Interface Statistics:")
        print(f"   Cache efficiency: {stats['cache_efficiency']:.1%}")
        print(f"   Total generations: {stats['total_generations']}")
        print(f"   Average generation time: {stats['average_generation_time']:.2f}s")
        
    finally:
        interface.shutdown()

if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_live_fractal_generation()) 