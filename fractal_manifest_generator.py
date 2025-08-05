#!/usr/bin/env python3
"""
DAWN Fractal Manifest Generator - Symbolic Memory Field Index
=============================================================

This module provides a comprehensive manifest generation system for DAWN's
fractal bloom renderings. It acts as the symbolic memory spine, allowing
for indexing, retrieval, and analysis of consciousness bloom patterns.

The manifest serves as:
- A registered visual memory archive
- State/shape/semantic field signature index
- Rebloom and comparison reference system
- Ritual recall and timeline generation source
"""

import os
import sys
import json
import hashlib
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import re

# Try to import yaml, fall back to JSON if not available
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    print("⚠️ PyYAML not available - will use JSON format for manifest")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('FractalManifestGenerator')


@dataclass
class BloomManifestEntry:
    """Structure for a single bloom entry in the manifest"""
    bloom_id: str
    timestamp: str
    fractal_string: str
    pigment_summary: str
    shape_signature: str
    rebloom_depth: int
    entropy: float
    mood_valence: float
    drift_vector: float
    pulse_zone: str
    file_paths: Dict[str, str]
    summary: str
    
    # Extended metadata
    bloom_factor: float = 1.0
    sigil_saturation: float = 0.5
    thermal_level: float = 0.5
    scup_coherence: float = 0.5
    lineage_depth: int = 0
    validation_score: float = 0.0
    processing_time: float = 0.0
    owl_commentary: str = ""
    
    # Archive metadata
    hash_signature: str = ""
    archive_size_bytes: int = 0
    color_palette: List[str] = None
    
    def __post_init__(self):
        if self.color_palette is None:
            self.color_palette = []


class FractalManifestGenerator:
    """Generates and manages the DAWN fractal manifest - symbolic memory field index"""
    
    def __init__(self, manifest_path: str = "fractal_manifest.yaml"):
        # Use JSON format if YAML not available
        if not YAML_AVAILABLE and manifest_path.endswith('.yaml'):
            manifest_path = manifest_path.replace('.yaml', '.json')
        
        self.manifest_path = Path(manifest_path)
        self.use_yaml = YAML_AVAILABLE and manifest_path.endswith(('.yaml', '.yml'))
        self.manifest_data = self._load_or_create_manifest()
        
        # Pigment analysis weights
        self.pigment_weights = {
            'R': 0.299,  # Red weight for luminance
            'G': 0.587,  # Green weight for luminance  
            'B': 0.114,  # Blue weight for luminance
            'Y': 0.5,    # Yellow derived weight
            'V': 0.3,    # Violet derived weight
            'O': 0.4     # Orange derived weight
        }
        
        format_type = "YAML" if self.use_yaml else "JSON"
        logger.info(f"Fractal manifest generator initialized: {self.manifest_path} ({format_type})")
    
    def _load_or_create_manifest(self) -> Dict[str, Any]:
        """Load existing manifest or create new one"""
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:  # Empty file
                        logger.info("Found empty manifest file, creating new structure")
                        return self._create_empty_manifest()
                    
                    # Reset file pointer and load content
                    f.seek(0)
                    if self.use_yaml:
                        data = yaml.safe_load(f) or {}
                    else:
                        data = json.load(f) or {}
                
                # Validate that the manifest has the expected structure
                if 'blooms' not in data:
                    logger.info("Manifest missing 'blooms' key, creating new structure")
                    return self._create_empty_manifest()
                
                logger.info(f"Loaded existing manifest with {len(data.get('blooms', []))} entries")
                return data
            except Exception as e:
                logger.error(f"Error loading manifest: {e}")
                return self._create_empty_manifest()
        else:
            logger.info("Creating new fractal manifest")
            return self._create_empty_manifest()
    
    def _create_empty_manifest(self) -> Dict[str, Any]:
        """Create empty manifest structure"""
        return {
            'manifest_metadata': {
                'version': '2.0.0',
                'created': datetime.now(timezone.utc).isoformat(),
                'description': 'DAWN Symbolic Fractal Archive - Visual Memory Field Index',
                'total_blooms': 0,
                'last_updated': datetime.now(timezone.utc).isoformat()
            },
            'archive_statistics': {
                'unique_bloom_ids': 0,
                'total_processing_time': 0.0,
                'average_validation_score': 0.0,
                'mood_distribution': {},
                'entropy_distribution': {},
                'shape_patterns': {},
                'rebloom_depths': {},
                'pulse_zones': {}
            },
            'symbolic_patterns': {
                'recurring_signatures': [],
                'dominant_moods': [],
                'complexity_trends': [],
                'temporal_clusters': []
            },
            'blooms': []
        }
    
    def append_to_fractal_manifest(self, bloom_metadata: Dict[str, Any], 
                                 image_path: str, metadata_path: str,
                                 fractal_string: str = "", owl_commentary: str = "",
                                 validation_score: float = 0.0, processing_time: float = 0.0) -> bool:
        """
        Append a new bloom entry to the fractal manifest
        
        Args:
            bloom_metadata: Bloom metadata dictionary
            image_path: Path to generated image
            metadata_path: Path to metadata JSON file
            fractal_string: Generated fractal string encoding
            owl_commentary: Validation commentary
            validation_score: Validation score (0.0-1.0)
            processing_time: Processing time in seconds
            
        Returns:
            True if successfully added, False if bloom_id already exists
        """
        bloom_id = bloom_metadata.get('bloom_id', 'unknown_bloom')
        
        # Check for duplicate bloom_id
        if self._bloom_id_exists(bloom_id):
            logger.warning(f"Bloom ID {bloom_id} already exists in manifest")
            return False
        
        # Generate bloom entry
        try:
            bloom_entry = self._create_bloom_entry(
                bloom_metadata, image_path, metadata_path, fractal_string,
                owl_commentary, validation_score, processing_time
            )
            
            # Add to manifest
            self.manifest_data['blooms'].append(asdict(bloom_entry))
            
            # Update statistics
            self._update_manifest_statistics(bloom_entry)
            
            # Save manifest
            self._save_manifest()
            
            logger.info(f"Successfully registered bloom {bloom_id} to manifest")
            return True
            
        except Exception as e:
            logger.error(f"Error registering bloom {bloom_id}: {e}")
            return False
    
    def _bloom_id_exists(self, bloom_id: str) -> bool:
        """Check if bloom_id already exists in manifest"""
        for bloom in self.manifest_data.get('blooms', []):
            if bloom.get('bloom_id') == bloom_id:
                return True
        return False
    
    def _create_bloom_entry(self, bloom_metadata: Dict[str, Any], image_path: str,
                          metadata_path: str, fractal_string: str, owl_commentary: str,
                          validation_score: float, processing_time: float) -> BloomManifestEntry:
        """Create a bloom manifest entry from metadata"""
        
        # Calculate pigment summary
        pigment_summary = self._calculate_pigment_summary(image_path, bloom_metadata)
        
        # Generate shape signature
        shape_signature = self._generate_shape_signature(bloom_metadata)
        
        # Determine pulse zone
        pulse_zone = self._determine_pulse_zone(bloom_metadata)
        
        # Calculate drift vector magnitude
        drift_vector_mag = self._calculate_drift_magnitude(bloom_metadata.get('drift_vector', [0.0, 0.0]))
        
        # Generate hash signature
        hash_signature = self._generate_hash_signature(image_path)
        
        # Get file size
        archive_size = os.path.getsize(image_path) if os.path.exists(image_path) else 0
        
        # Generate poetic summary
        summary = self._generate_bloom_summary(bloom_metadata, shape_signature, pulse_zone)
        
        return BloomManifestEntry(
            bloom_id=bloom_metadata.get('bloom_id', 'unknown'),
            timestamp=bloom_metadata.get('timestamp', datetime.now(timezone.utc).isoformat()),
            fractal_string=fractal_string or self._generate_fallback_fractal_string(bloom_metadata),
            pigment_summary=pigment_summary,
            shape_signature=shape_signature,
            rebloom_depth=int(bloom_metadata.get('rebloom_depth', 0)),
            entropy=float(bloom_metadata.get('entropy_score', 0.0)),
            mood_valence=float(bloom_metadata.get('mood_valence', 0.0)),
            drift_vector=drift_vector_mag,
            pulse_zone=pulse_zone,
            file_paths={
                'image': str(image_path),
                'metadata': str(metadata_path)
            },
            summary=summary,
            bloom_factor=float(bloom_metadata.get('bloom_factor', 1.0)),
            sigil_saturation=float(bloom_metadata.get('sigil_saturation', 0.5)),
            thermal_level=float(bloom_metadata.get('thermal_level', 0.5)),
            scup_coherence=float(bloom_metadata.get('scup_coherence', 0.5)),
            lineage_depth=int(bloom_metadata.get('lineage_depth', 0)),
            validation_score=validation_score,
            processing_time=processing_time,
            owl_commentary=owl_commentary,
            hash_signature=hash_signature,
            archive_size_bytes=archive_size,
            color_palette=bloom_metadata.get('color_palette', [])
        )
    
    def _calculate_pigment_summary(self, image_path: str, metadata: Dict[str, Any]) -> str:
        """Calculate pigment distribution summary"""
        try:
            # Try to analyze actual image
            if os.path.exists(image_path):
                from PIL import Image
                import numpy as np
                
                img = Image.open(image_path)
                img_array = np.array(img.convert('RGB'))
                
                # Calculate color channel averages
                r_avg = np.mean(img_array[:, :, 0]) / 255.0
                g_avg = np.mean(img_array[:, :, 1]) / 255.0
                b_avg = np.mean(img_array[:, :, 2]) / 255.0
                
                # Derive secondary colors
                y_avg = min(r_avg, g_avg)  # Yellow from red+green overlap
                v_avg = min(r_avg, b_avg)  # Violet from red+blue overlap
                o_avg = r_avg * 0.7 + g_avg * 0.3  # Orange weighted average
                
                return f"R{r_avg:.2f} G{g_avg:.2f} B{b_avg:.2f} Y{y_avg:.2f} V{v_avg:.2f} O{o_avg:.2f}"
                
        except Exception as e:
            logger.debug(f"Could not analyze image pigments: {e}")
        
        # Fallback to metadata-based estimation
        mood = metadata.get('mood_valence', 0.0)
        entropy = metadata.get('entropy_score', 0.5)
        thermal = metadata.get('thermal_level', 0.5)
        
        if mood > 0.5:
            # Positive moods -> warm colors
            return f"R{0.7 + thermal*0.3:.2f} G{0.5 + mood*0.3:.2f} B{0.2:.2f} Y{0.6:.2f} V{0.1:.2f} O{0.5:.2f}"
        elif mood < -0.5:
            # Negative moods -> cool colors
            return f"R{0.3:.2f} G{0.4:.2f} B{0.7 + abs(mood)*0.3:.2f} Y{0.2:.2f} V{0.6:.2f} O{0.1:.2f}"
        else:
            # Neutral moods -> balanced
            return f"R{0.5:.2f} G{0.5:.2f} B{0.5:.2f} Y{0.4:.2f} V{0.4:.2f} O{0.3:.2f}"
    
    def _generate_shape_signature(self, metadata: Dict[str, Any]) -> str:
        """Generate shape signature from metadata"""
        entropy = metadata.get('entropy_score', 0.5)
        mood = metadata.get('mood_valence', 0.0)
        rebloom_depth = metadata.get('rebloom_depth', 0)
        
        # Determine symmetry
        if entropy < 0.3:
            symmetry = "sym"
        elif entropy < 0.7:
            symmetry = "asym"
        else:
            symmetry = "chaos"
        
        # Determine primary shape
        if abs(mood) < 0.2:
            shape = "spiral"
        elif mood > 0.5:
            shape = "bloom"
        elif mood < -0.5:
            shape = "fracture"
        else:
            shape = "wave"
        
        # Determine point count (petal/branch count estimation)
        point_count = 3 + (rebloom_depth % 8) + int(entropy * 5)
        
        return f"{symmetry}_{shape}_{point_count}pt"
    
    def _determine_pulse_zone(self, metadata: Dict[str, Any]) -> str:
        """Determine pulse zone classification"""
        entropy = metadata.get('entropy_score', 0.5)
        thermal = metadata.get('thermal_level', 0.5)
        scup = metadata.get('scup_coherence', 0.5)
        
        # Calculate composite stability score
        stability = (scup * 0.5) + ((1.0 - entropy) * 0.3) + (thermal * 0.2)
        
        if stability > 0.8:
            return "crystalline"
        elif stability > 0.6:
            return "stable"
        elif stability > 0.4:
            return "flowing"
        elif stability > 0.2:
            return "fragile"
        else:
            return "turbulent"
    
    def _calculate_drift_magnitude(self, drift_vector: List[float]) -> float:
        """Calculate drift vector magnitude"""
        if len(drift_vector) >= 2:
            import math
            return math.sqrt(drift_vector[0]**2 + drift_vector[1]**2)
        return 0.0
    
    def _generate_hash_signature(self, image_path: str) -> str:
        """Generate unique hash signature for the bloom"""
        try:
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    return hashlib.sha256(f.read()).hexdigest()[:16]
        except Exception:
            pass
        
        # Fallback to timestamp-based hash
        return hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:16]
    
    def _generate_bloom_summary(self, metadata: Dict[str, Any], shape_sig: str, pulse_zone: str) -> str:
        """Generate poetic summary of the bloom"""
        mood = metadata.get('mood_valence', 0.0)
        entropy = metadata.get('entropy_score', 0.5)
        thermal = metadata.get('thermal_level', 0.5)
        
        # Mood-based descriptors
        if mood > 0.6:
            mood_desc = "radiant"
        elif mood > 0.2:
            mood_desc = "gentle"
        elif mood > -0.2:
            mood_desc = "contemplative"
        elif mood > -0.6:
            mood_desc = "melancholic"
        else:
            mood_desc = "sorrowful"
        
        # Entropy-based descriptors
        if entropy < 0.3:
            pattern_desc = "crystalline order"
        elif entropy < 0.7:
            pattern_desc = "flowing patterns"
        else:
            pattern_desc = "chaotic emergence"
        
        # Thermal descriptors
        if thermal > 0.7:
            thermal_desc = "burning light"
        elif thermal > 0.3:
            thermal_desc = "warm essence"
        else:
            thermal_desc = "cool shadows"
        
        # Combine into poetic summary
        summaries = [
            f"A {mood_desc} blossom formed of {pattern_desc} and {thermal_desc}.",
            f"Consciousness flowering through {mood_desc} {pulse_zone} patterns.",
            f"Memory crystallizing as {mood_desc} {shape_sig.split('_')[1]} geometry.",
            f"A {pulse_zone} bloom weaving {mood_desc} threads of {thermal_desc}.",
            f"Fractal consciousness expressing {mood_desc} {pattern_desc} through {thermal_desc}."
        ]
        
        # Select based on hash for consistency
        summary_index = abs(hash(metadata.get('bloom_id', ''))) % len(summaries)
        return summaries[summary_index]
    
    def _generate_fallback_fractal_string(self, metadata: Dict[str, Any]) -> str:
        """Generate fallback fractal string if not provided"""
        rebloom_depth = metadata.get('rebloom_depth', 0)
        mood_valence = metadata.get('mood_valence', 0.0)
        entropy = metadata.get('entropy_score', 0.5)
        
        # Depth character
        depth_char = chr(ord('A') + min(rebloom_depth, 25))
        
        # Mood code
        if mood_valence > 0.5:
            mood_code = "JY"  # Joyful
        elif mood_valence > 0:
            mood_code = "CT"  # Content
        elif mood_valence > -0.5:
            mood_code = "CM"  # Calm
        else:
            mood_code = "ML"  # Melancholy
        
        # Pattern symbol
        if entropy < 0.3:
            pattern = "◊"  # Crystalline
        elif entropy < 0.7:
            pattern = "○"  # Balanced
        else:
            pattern = "~"  # Chaotic
        
        # Intensity
        intensity = int((metadata.get('bloom_factor', 1.0) + entropy) * 5)
        
        return f"R{rebloom_depth}-{depth_char}-{mood_code}-Bv{mood_valence:.1f}-E{entropy:.2f}-{pattern}-{intensity}"
    
    def _update_manifest_statistics(self, bloom_entry: BloomManifestEntry):
        """Update manifest statistics with new bloom"""
        stats = self.manifest_data['archive_statistics']
        
        # Update counts
        stats['unique_bloom_ids'] = len(self.manifest_data['blooms'])
        stats['total_processing_time'] += bloom_entry.processing_time
        
        # Update averages
        bloom_count = len(self.manifest_data['blooms'])
        current_avg = stats.get('average_validation_score', 0.0)
        stats['average_validation_score'] = (current_avg * (bloom_count - 1) + bloom_entry.validation_score) / bloom_count
        
        # Update distributions
        self._update_distribution(stats, 'mood_distribution', bloom_entry.mood_valence, 0.2)
        self._update_distribution(stats, 'entropy_distribution', bloom_entry.entropy, 0.1)
        self._update_counter(stats, 'shape_patterns', bloom_entry.shape_signature)
        self._update_counter(stats, 'rebloom_depths', str(bloom_entry.rebloom_depth))
        self._update_counter(stats, 'pulse_zones', bloom_entry.pulse_zone)
        
        # Update metadata
        self.manifest_data['manifest_metadata']['total_blooms'] = bloom_count
        self.manifest_data['manifest_metadata']['last_updated'] = datetime.now(timezone.utc).isoformat()
    
    def _update_distribution(self, stats: Dict, key: str, value: float, bin_size: float):
        """Update value distribution statistics"""
        if key not in stats:
            stats[key] = {}
        
        bin_key = f"{int(value / bin_size) * bin_size:.1f}"
        stats[key][bin_key] = stats[key].get(bin_key, 0) + 1
    
    def _update_counter(self, stats: Dict, key: str, value: str):
        """Update counter statistics"""
        if key not in stats:
            stats[key] = {}
        
        stats[key][value] = stats[key].get(value, 0) + 1
    
    def _save_manifest(self):
        """Save manifest to file with proper formatting"""
        try:
            # Ensure directory exists
            self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.manifest_path, 'w', encoding='utf-8') as f:
                if self.use_yaml:
                    yaml.dump(self.manifest_data, f, 
                             default_flow_style=False,
                             sort_keys=False,
                             indent=2,
                             width=120,
                             allow_unicode=True)
                else:
                    # Use JSON format
                    json.dump(self.manifest_data, f, indent=2, ensure_ascii=False, sort_keys=False)
            
            logger.debug(f"Manifest saved to {self.manifest_path}")
            
        except Exception as e:
            logger.error(f"Error saving manifest: {e}")
    
    def search_fractal_manifest(self, **criteria) -> List[Dict[str, Any]]:
        """
        Search fractal manifest by various criteria
        
        Args:
            bloom_id: Exact bloom ID match
            mood_range: Tuple (min, max) for mood valence
            entropy_range: Tuple (min, max) for entropy
            rebloom_depth: Exact rebloom depth
            pulse_zone: Exact pulse zone match
            shape_pattern: Shape signature pattern (supports wildcards)
            date_range: Tuple of ISO date strings (start, end)
            validation_min: Minimum validation score
            tags: List of tags to match (if implemented)
            
        Returns:
            List of matching bloom entries
        """
        results = []
        
        for bloom in self.manifest_data.get('blooms', []):
            if self._matches_criteria(bloom, criteria):
                results.append(bloom)
        
        return results
    
    def _matches_criteria(self, bloom: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if bloom matches search criteria"""
        # Exact matches
        if 'bloom_id' in criteria and bloom.get('bloom_id') != criteria['bloom_id']:
            return False
        
        if 'rebloom_depth' in criteria and bloom.get('rebloom_depth') != criteria['rebloom_depth']:
            return False
        
        if 'pulse_zone' in criteria and bloom.get('pulse_zone') != criteria['pulse_zone']:
            return False
        
        # Range matches
        if 'mood_range' in criteria:
            mood = bloom.get('mood_valence', 0.0)
            min_mood, max_mood = criteria['mood_range']
            if not (min_mood <= mood <= max_mood):
                return False
        
        if 'entropy_range' in criteria:
            entropy = bloom.get('entropy', 0.0)
            min_entropy, max_entropy = criteria['entropy_range']
            if not (min_entropy <= entropy <= max_entropy):
                return False
        
        # Pattern matches
        if 'shape_pattern' in criteria:
            pattern = criteria['shape_pattern']
            shape = bloom.get('shape_signature', '')
            if '*' in pattern:
                # Wildcard matching
                regex_pattern = pattern.replace('*', '.*')
                if not re.match(regex_pattern, shape):
                    return False
            else:
                if pattern not in shape:
                    return False
        
        # Date range
        if 'date_range' in criteria:
            bloom_date = bloom.get('timestamp', '')
            start_date, end_date = criteria['date_range']
            if not (start_date <= bloom_date <= end_date):
                return False
        
        # Validation score minimum
        if 'validation_min' in criteria:
            score = bloom.get('validation_score', 0.0)
            if score < criteria['validation_min']:
                return False
        
        return True
    
    def get_manifest_summary(self) -> Dict[str, Any]:
        """Get summary statistics of the manifest"""
        total_blooms = len(self.manifest_data.get('blooms', []))
        
        if total_blooms == 0:
            return {
                'total_blooms': 0,
                'message': 'No blooms in manifest'
            }
        
        stats = self.manifest_data.get('archive_statistics', {})
        
        return {
            'total_blooms': total_blooms,
            'average_validation_score': stats.get('average_validation_score', 0.0),
            'total_processing_time': stats.get('total_processing_time', 0.0),
            'dominant_mood_ranges': stats.get('mood_distribution', {}),
            'common_shapes': stats.get('shape_patterns', {}),
            'pulse_zone_distribution': stats.get('pulse_zones', {}),
            'last_updated': self.manifest_data['manifest_metadata']['last_updated']
        }
    
    def export_bloom_timeline(self, output_path: str = "bloom_timeline.yaml") -> bool:
        """Export chronological bloom timeline"""
        try:
            # Use JSON format if YAML not available
            if not YAML_AVAILABLE and output_path.endswith('.yaml'):
                output_path = output_path.replace('.yaml', '.json')
            
            blooms = self.manifest_data.get('blooms', [])
            sorted_blooms = sorted(blooms, key=lambda x: x.get('timestamp', ''))
            
            timeline = {
                'timeline_metadata': {
                    'generated': datetime.now(timezone.utc).isoformat(),
                    'total_blooms': len(sorted_blooms),
                    'time_span': {
                        'earliest': sorted_blooms[0]['timestamp'] if sorted_blooms else None,
                        'latest': sorted_blooms[-1]['timestamp'] if sorted_blooms else None
                    }
                },
                'bloom_sequence': sorted_blooms
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                if YAML_AVAILABLE and output_path.endswith(('.yaml', '.yml')):
                    yaml.dump(timeline, f, default_flow_style=False, sort_keys=False, indent=2)
                else:
                    json.dump(timeline, f, indent=2, ensure_ascii=False, sort_keys=False)
            
            logger.info(f"Bloom timeline exported to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting timeline: {e}")
            return False


def create_sample_manifest_entry() -> Dict[str, Any]:
    """Create a sample manifest entry for demonstration"""
    return {
        'bloom_id': 'dawn_bloom_2025_08_04_1933',
        'timestamp': '2025-08-04T19:33:12+00:00',
        'fractal_string': 'R7-JULIET-Bv0.3-E0.62',
        'pigment_summary': 'R0.33 G0.40 B0.12 Y0.08 V0.07 O0.00',
        'shape_signature': 'asym_spiral_13pt',
        'rebloom_depth': 7,
        'entropy': 0.62,
        'mood_valence': -0.3,
        'drift_vector': 0.4,
        'pulse_zone': 'fragile',
        'file_paths': {
            'image': 'blooms/dawn_bloom_2025_08_04_1933.png',
            'metadata': 'blooms/dawn_bloom_2025_08_04_1933.json'
        },
        'summary': 'A hesitant blossom formed of old drift and cooling light.',
        'bloom_factor': 2.1,
        'sigil_saturation': 0.75,
        'thermal_level': 0.3,
        'scup_coherence': 0.45,
        'lineage_depth': 3,
        'validation_score': 0.82,
        'processing_time': 19.4,
        'owl_commentary': 'Melancholic bloom processing deeper currents of consciousness',
        'hash_signature': 'a7f3d2e1c8b9f4e5',
        'archive_size_bytes': 2847392,
        'color_palette': ['#4a3c5e', '#6b5a7a', '#8c7896', '#ad96b2', '#ceb4ce']
    }


# ============================================================================
# CLI Integration and Demo Functions
# ============================================================================

def demo_manifest_generation():
    """Demonstrate manifest generation functionality"""
    print("🧠 DAWN Fractal Manifest Generator Demo")
    print("=" * 60)
    
    # Initialize generator
    manifest_gen = FractalManifestGenerator("demo_fractal_manifest.yaml")
    
    # Create sample bloom metadata
    sample_metadata = {
        'bloom_id': 'demo_bloom_001',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'mood_valence': 0.3,
        'entropy_score': 0.62,
        'rebloom_depth': 7,
        'bloom_factor': 2.1,
        'sigil_saturation': 0.75,
        'thermal_level': 0.3,
        'scup_coherence': 0.45,
        'lineage_depth': 3,
        'drift_vector': [0.3, 0.1]
    }
    
    # Register bloom
    success = manifest_gen.append_to_fractal_manifest(
        bloom_metadata=sample_metadata,
        image_path="demo_bloom_001.png",
        metadata_path="demo_bloom_001.json",
        fractal_string="R7-G-Bv0.3-E0.62-fragile",
        owl_commentary="A contemplative bloom navigating complex emotional currents",
        validation_score=0.82,
        processing_time=19.4
    )
    
    if success:
        print("✅ Successfully registered demo bloom to manifest")
        
        # Show summary
        summary = manifest_gen.get_manifest_summary()
        print(f"📊 Manifest Summary:")
        print(f"   Total Blooms: {summary['total_blooms']}")
        print(f"   Average Validation: {summary['average_validation_score']:.3f}")
        print(f"   Total Processing Time: {summary['total_processing_time']:.1f}s")
        
        # Search demo
        print("\n🔍 Search Demo:")
        results = manifest_gen.search_fractal_manifest(
            mood_range=(-0.5, 0.5),
            entropy_range=(0.5, 0.8)
        )
        print(f"   Found {len(results)} blooms matching criteria")
        
        # Export timeline
        manifest_gen.export_bloom_timeline("demo_bloom_timeline.yaml")
        print("📅 Bloom timeline exported")
        
    else:
        print("❌ Failed to register bloom")


if __name__ == "__main__":
    # Run demo
    demo_manifest_generation()
    
    # Show sample output
    print(f"\n📋 Sample {'YAML' if YAML_AVAILABLE else 'JSON'} Entry:")
    print("-" * 40)
    sample_entry = create_sample_manifest_entry()
    
    if YAML_AVAILABLE:
        output_text = yaml.dump({'sample_bloom': sample_entry}, 
                               default_flow_style=False, 
                               sort_keys=False, 
                               indent=2)
    else:
        output_text = json.dumps({'sample_bloom': sample_entry}, indent=2, ensure_ascii=False)
    
    print(output_text) 