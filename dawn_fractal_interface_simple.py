#!/usr/bin/env python3
"""
DAWN Fractal Interface - Simplified Version
==========================================

Production interface for DAWN's consciousness-driven fractal generation system.
Simplified version that avoids database complexity and focuses on core functionality.
"""

import time
import json
import hashlib
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict, deque
import threading

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
            abs(prev_state.mood_valence - current_state.mood_valence) / 2.0,
            abs(prev_state.drift_vector - current_state.drift_vector) / 2.0,
            abs(prev_state.rebloom_depth - current_state.rebloom_depth) / 20.0,
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

class SimpleBloomArchive:
    """Simple file-based archive system for storing bloom sequences"""
    
    def __init__(self, archive_dir: str = "dawn_bloom_archive"):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)
        
        # In-memory bloom metadata
        self.bloom_metadata: List[Dict[str, Any]] = []
        
        print(f"📁 Simple bloom archive initialized: {self.archive_dir}")
    
    def store_bloom(self, cache_entry: BloomCacheEntry):
        """Store bloom metadata in memory"""
        
        try:
            bloom_record = {
                'cache_key': cache_entry.cache_key,
                'memory_id': cache_entry.config.memory_id,
                'timestamp': cache_entry.generated_timestamp,
                'bloom_entropy': cache_entry.config.bloom_entropy,
                'mood_valence': cache_entry.config.mood_valence,
                'drift_vector': cache_entry.config.drift_vector,
                'rebloom_depth': cache_entry.config.rebloom_depth,
                'sigil_saturation': cache_entry.config.sigil_saturation,
                'pulse_zone': cache_entry.config.pulse_zone,
                'archetype': cache_entry.config.archetype,
                'file_path': cache_entry.file_path,
                'visual_complexity': cache_entry.visual_signature.get('complexity', 0.0),
                'color_variance': cache_entry.visual_signature.get('color_variance', 0.0),
                'motion_magnitude': cache_entry.visual_signature.get('motion_magnitude', 0.0),
                'fractal_string': cache_entry.visual_signature.get('fractal_string', '')
            }
            
            self.bloom_metadata.append(bloom_record)
            
        except Exception as e:
            print(f"⚠️  Error storing bloom in archive: {e}")
    
    def retrieve_time_range(self, start_time: float, end_time: float) -> List[Dict[str, Any]]:
        """Retrieve blooms from a specific time range"""
        
        try:
            return [
                bloom for bloom in self.bloom_metadata
                if start_time <= bloom['timestamp'] <= end_time
            ]
        except Exception as e:
            print(f"⚠️  Error retrieving blooms from archive: {e}")
            return []
    
    def find_similar_blooms(self, target_config: DAWNConsciousnessConfig, 
                          similarity_threshold: float = 0.7,
                          max_results: int = 10) -> List[Dict[str, Any]]:
        """Find blooms similar to target configuration"""
        
        try:
            similar_blooms = []
            
            for bloom_record in self.bloom_metadata:
                # Calculate similarity
                param_diffs = [
                    abs(bloom_record['bloom_entropy'] - target_config.bloom_entropy),
                    abs(bloom_record['mood_valence'] - target_config.mood_valence),
                    abs(bloom_record['drift_vector'] - target_config.drift_vector),
                    abs(bloom_record['rebloom_depth'] - target_config.rebloom_depth),
                    abs(bloom_record['sigil_saturation'] - target_config.sigil_saturation)
                ]
                
                pulse_similarity = 1.0 if bloom_record['pulse_zone'] == target_config.pulse_zone else 0.5
                param_distance = np.mean(param_diffs)
                similarity = 1.0 - (param_distance * 0.8 + (1.0 - pulse_similarity) * 0.2)
                
                if similarity >= similarity_threshold:
                    bloom_record_copy = bloom_record.copy()
                    bloom_record_copy['similarity_score'] = similarity
                    similar_blooms.append(bloom_record_copy)
            
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
                 max_concurrent_jobs: int = 3):
        
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
        self.archive = SimpleBloomArchive(self.output_dir / "archive")
        
        # Generation statistics
        self.stats = {
            'total_generations': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'concurrent_generations': 0,
            'average_generation_time': 0.0
        }
        
        print(f"🎨 DAWN Fractal Interface initialized")
        print(f"   Output: {self.output_dir}")
        print(f"   Cache size: {cache_size}")
        print(f"   Max concurrent: {max_concurrent_jobs}")
    
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
            
            # Convert shape complexity to JSON-safe format
            shape_complexity_dict = asdict(shape_complexity)
            # Convert enum to string
            if 'complexity_mode' in shape_complexity_dict:
                shape_complexity_dict['complexity_mode'] = shape_complexity_dict['complexity_mode'].value
            
            # Package fractal data
            fractal_data = {
                'coordinates': drift_transformation.transformed_coords.tolist(),
                'center_offset': drift_transformation.center_offset,
                'rotation_angle': drift_transformation.rotation_angle,
                'transparency_map': drift_transformation.transparency_map.tolist() if drift_transformation.transparency_map is not None else None,
                'motion_vectors': drift_transformation.motion_vectors.tolist() if drift_transformation.motion_vectors is not None else None,
                'expansion_factor': drift_transformation.expansion_factor.tolist() if drift_transformation.expansion_factor is not None else None,
                'shape_complexity': shape_complexity_dict,
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
    
    def generate_memory_bloom(self, 
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
            return None
        
        # Generate bloom synchronously for simplicity
        print(f"🎨 Generating new bloom: {cache_key}")
        
        try:
            return self._generate_bloom_job(current_state, cache_key)
        except Exception as e:
            print(f"⚠️  Error in bloom generation: {e}")
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
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        print("✅ DAWN Fractal Interface shutdown complete")

# Example usage
if __name__ == "__main__":
    print("🎨 DAWN Fractal Interface - Simple Version Test")
    print("=" * 48)
    
    # Create interface
    interface = DAWNFractalInterface(
        output_dir="test_simple_fractals",
        cache_size=20,
        max_concurrent_jobs=2
    )
    
    try:
        # Test with sample consciousness state
        test_state = DAWNConsciousnessConfig(
            memory_id="test_simple_interface", timestamp=None,
            bloom_entropy=0.6, mood_valence=0.3, drift_vector=0.2,
            rebloom_depth=5, sigil_saturation=0.7, pulse_zone="flowing"
        )
        
        print(f"\n🎯 Testing bloom generation...")
        bloom = interface.generate_memory_bloom(test_state)
        
        if bloom:
            print(f"✅ Generated bloom: {bloom.cache_key}")
            print(f"📊 Visual signature: {bloom.visual_signature}")
            
            # Test cache hit
            print(f"\n💾 Testing cache...")
            cached_bloom = interface.generate_memory_bloom(test_state)
            print(f"Cache result: {'HIT' if cached_bloom else 'MISS'}")
            
            # Display statistics
            stats = interface.get_cache_statistics()
            print(f"\n📈 Statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        
    finally:
        interface.shutdown() 