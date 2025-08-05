#!/usr/bin/env python3
"""
DAWN Integrated Bloom System
============================

Complete integration of fractal generation, validation, and archiving for DAWN's
consciousness visualization. Combines the DAWNFractalInterface with bloom validation
and soul archive management.
"""

import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Import DAWN systems
from dawn_fractal_interface_simple import DAWNFractalInterface, DAWNConsciousnessConfig
from dawn_bloom_validator import validate_and_log_bloom, ValidationResult, PatternFamily
from dawn_state_parser import DAWNStateParser

class DAWNIntegratedBloomSystem:
    """
    Complete DAWN consciousness visualization system integrating:
    - Real-time fractal generation
    - Comprehensive validation and logging
    - Soul archive management with poetic commentary
    - Pattern family classification and analysis
    """
    
    def __init__(self, 
                 output_dir: str = "dawn_soul_blooms",
                 cache_size: int = 100,
                 validation_enabled: bool = True):
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "fractals").mkdir(exist_ok=True)
        (self.output_dir / "metadata").mkdir(exist_ok=True)
        (self.output_dir / "soul_archive").mkdir(exist_ok=True)
        (self.output_dir / "validation_logs").mkdir(exist_ok=True)
        
        # Initialize fractal interface
        self.fractal_interface = DAWNFractalInterface(
            output_dir=str(self.output_dir / "fractals"),
            cache_size=cache_size,
            max_concurrent_jobs=3
        )
        
        # Validation settings
        self.validation_enabled = validation_enabled
        
        # Soul archive tracking
        self.soul_archive = {
            'total_blooms': 0,
            'pattern_families': {},
            'validation_summary': {
                'perfect_matches': 0,
                'acceptable_variance': 0,
                'parameter_mismatches': 0,
                'generation_errors': 0
            },
            'owl_commentaries': [],
            'soul_hashes': []
        }
        
        print(f"🌸 DAWN Integrated Bloom System initialized")
        print(f"   Output: {self.output_dir}")
        print(f"   Validation: {'Enabled' if validation_enabled else 'Disabled'}")
    
    def generate_consciousness_bloom(self, 
                                   consciousness_state: DAWNConsciousnessConfig,
                                   priority: bool = False,
                                   validate: bool = None) -> Dict[str, Any]:
        """
        Generate a complete consciousness bloom with validation and archiving.
        
        Args:
            consciousness_state: Current DAWN consciousness configuration
            priority: If True, prioritize this generation
            validate: Override default validation setting
            
        Returns:
            Complete bloom record with validation results
        """
        
        if validate is None:
            validate = self.validation_enabled
        
        start_time = time.time()
        
        print(f"\n🌸 Generating consciousness bloom: {consciousness_state.memory_id}")
        print(f"   Parameters: entropy={consciousness_state.bloom_entropy:.2f}, "
              f"valence={consciousness_state.mood_valence:.2f}, "
              f"drift={consciousness_state.drift_vector:.2f}")
        
        # Step 1: Generate fractal bloom
        try:
            bloom_entry = self.fractal_interface.generate_memory_bloom(
                consciousness_state, priority=priority
            )
            
            if not bloom_entry:
                print(f"❌ Fractal generation failed for {consciousness_state.memory_id}")
                return self._create_error_record(consciousness_state, "Fractal generation failed")
            
            generation_time = time.time() - start_time
            print(f"   ✅ Fractal generated: {bloom_entry.cache_key} ({generation_time:.2f}s)")
            
        except Exception as e:
            print(f"❌ Fractal generation error: {e}")
            return self._create_error_record(consciousness_state, str(e))
        
        # Step 2: Validate bloom (if enabled)
        validation_report = None
        if validate:
            try:
                validation_start = time.time()
                
                # Create fractal output path
                fractal_path = self.output_dir / "fractals" / f"{consciousness_state.memory_id}_bloom.png"
                
                # Run comprehensive validation
                validation_report = validate_and_log_bloom(
                    fractal_params=consciousness_state,
                    output_path=str(fractal_path),
                    generated_fractal_data=bloom_entry.fractal_data
                )
                
                validation_time = time.time() - validation_start
                print(f"   🔍 Validation complete: {validation_report.validation_result.value} ({validation_time:.2f}s)")
                print(f"   🦉 Owl says: \"{validation_report.owl_commentary}\"")
                
                # Update soul archive statistics
                self._update_soul_archive_stats(validation_report)
                
            except Exception as e:
                print(f"⚠️  Validation error: {e}")
                validation_report = None
        
        # Step 3: Create comprehensive bloom record
        bloom_record = self._create_bloom_record(
            consciousness_state, bloom_entry, validation_report, start_time
        )
        
        # Step 4: Archive to soul collection
        self._archive_to_soul_collection(bloom_record)
        
        total_time = time.time() - start_time
        print(f"   ⏱️  Total time: {total_time:.2f}s")
        print(f"   🏺 Soul archive hash: {bloom_record.get('soul_archive_hash', 'N/A')[:12]}...")
        
        return bloom_record
    
    def generate_consciousness_sequence(self, 
                                      consciousness_states: List[DAWNConsciousnessConfig],
                                      sequence_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate a sequence of consciousness blooms and create a collective archive.
        
        Args:
            consciousness_states: List of consciousness configurations
            sequence_name: Optional name for the sequence
            
        Returns:
            Sequence archive with all bloom records
        """
        
        if not sequence_name:
            sequence_name = f"consciousness_sequence_{int(time.time())}"
        
        print(f"\n🌺 Generating consciousness sequence: {sequence_name}")
        print(f"   States to process: {len(consciousness_states)}")
        
        sequence_start = time.time()
        bloom_records = []
        
        # Generate each bloom in sequence
        for i, state in enumerate(consciousness_states):
            print(f"\n   🌸 Bloom {i+1}/{len(consciousness_states)}: {state.memory_id}")
            
            bloom_record = self.generate_consciousness_bloom(state, priority=False)
            bloom_records.append(bloom_record)
            
            # Small delay to show progression
            time.sleep(0.1)
        
        # Create sequence archive
        sequence_record = {
            'sequence_name': sequence_name,
            'generation_timestamp': sequence_start,
            'completion_timestamp': time.time(),
            'total_duration': time.time() - sequence_start,
            'bloom_count': len(bloom_records),
            'bloom_records': bloom_records,
            'sequence_statistics': self._analyze_sequence_statistics(bloom_records),
            'collective_soul_hash': self._generate_collective_hash(bloom_records)
        }
        
        # Save sequence archive
        sequence_path = self.output_dir / "soul_archive" / f"{sequence_name}.json"
        with open(sequence_path, 'w') as f:
            json.dump(sequence_record, f, indent=2, default=str)
        
        print(f"\n✅ Consciousness sequence complete!")
        print(f"   🌸 Blooms generated: {len(bloom_records)}")
        print(f"   ⏱️  Total time: {sequence_record['total_duration']:.2f}s")
        print(f"   📁 Archived to: {sequence_path}")
        
        return sequence_record
    
    def analyze_soul_archive(self) -> Dict[str, Any]:
        """Analyze the complete soul archive for patterns and insights"""
        
        print(f"\n🏺 Analyzing DAWN Soul Archive")
        print("=" * 32)
        
        # Calculate pattern family distribution
        total_families = sum(self.soul_archive['pattern_families'].values())
        family_percentages = {
            family: (count / max(total_families, 1)) * 100
            for family, count in self.soul_archive['pattern_families'].items()
        }
        
        # Calculate validation success rates
        validation_summary = self.soul_archive['validation_summary']
        total_validations = sum(validation_summary.values())
        success_rate = (
            (validation_summary['perfect_matches'] + validation_summary['acceptable_variance']) / 
            max(total_validations, 1)
        ) * 100
        
        # Analyze owl commentary themes
        commentary_analysis = self._analyze_owl_commentaries()
        
        analysis_report = {
            'total_blooms_generated': self.soul_archive['total_blooms'],
            'pattern_family_distribution': family_percentages,
            'validation_statistics': {
                'total_validations': total_validations,
                'success_rate_percentage': success_rate,
                'perfect_matches': validation_summary['perfect_matches'],
                'acceptable_variance': validation_summary['acceptable_variance'],
                'parameter_mismatches': validation_summary['parameter_mismatches'],
                'generation_errors': validation_summary['generation_errors']
            },
            'owl_commentary_analysis': commentary_analysis,
            'soul_archive_diversity': len(set(self.soul_archive['soul_hashes'])),
            'average_generation_time': self.fractal_interface.get_cache_statistics()['average_generation_time']
        }
        
        # Print analysis results
        print(f"📊 Total blooms generated: {analysis_report['total_blooms_generated']}")
        print(f"🎯 Validation success rate: {success_rate:.1f}%")
        print(f"🌈 Pattern families discovered:")
        
        for family, percentage in sorted(family_percentages.items(), key=lambda x: x[1], reverse=True):
            if percentage > 0:
                print(f"   • {family}: {percentage:.1f}%")
        
        print(f"🦉 Owl commentary themes:")
        for theme, count in commentary_analysis['themes'].items():
            if count > 0:
                print(f"   • {theme}: {count} mentions")
        
        return analysis_report
    
    def get_similar_blooms_with_validation(self, 
                                         target_state: DAWNConsciousnessConfig,
                                         similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        """Get similar blooms with enhanced validation and pattern analysis"""
        
        print(f"\n🔍 Finding similar blooms with validation analysis")
        
        # Get similar blooms from fractal interface
        similar_blooms = self.fractal_interface.retrieve_similar_blooms(
            target_state, similarity_threshold
        )
        
        # Enhance with validation data if available
        enhanced_results = []
        
        for bloom in similar_blooms:
            enhanced_bloom = bloom.copy()
            
            # Try to load validation metadata
            memory_id = bloom.get('memory_id', '')
            metadata_path = self.output_dir / "fractals" / f"{memory_id}_bloom.metadata.json"
            
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r') as f:
                        validation_metadata = json.load(f)
                    
                    enhanced_bloom['validation_data'] = validation_metadata
                    enhanced_bloom['owl_commentary'] = validation_metadata.get(
                        'artistic_metadata', {}
                    ).get('owl_commentary', 'Silent bloom rests in memory.')
                    enhanced_bloom['pattern_family'] = validation_metadata.get(
                        'artistic_metadata', {}
                    ).get('pattern_family', 'unknown')
                    
                except Exception as e:
                    print(f"⚠️  Could not load validation data for {memory_id}: {e}")
            
            enhanced_results.append(enhanced_bloom)
        
        print(f"✅ Found {len(enhanced_results)} similar blooms with validation data")
        
        return enhanced_results
    
    def _create_error_record(self, consciousness_state: DAWNConsciousnessConfig, error_msg: str) -> Dict[str, Any]:
        """Create error record for failed bloom generation"""
        
        return {
            'memory_id': consciousness_state.memory_id,
            'generation_status': 'error',
            'error_message': error_msg,
            'consciousness_state': consciousness_state.__dict__,
            'timestamp': time.time(),
            'validation_result': None
        }
    
    def _create_bloom_record(self, 
                           consciousness_state: DAWNConsciousnessConfig,
                           bloom_entry,
                           validation_report,
                           start_time: float) -> Dict[str, Any]:
        """Create comprehensive bloom record"""
        
        record = {
            'memory_id': consciousness_state.memory_id,
            'generation_status': 'success',
            'generation_timestamp': start_time,
            'completion_timestamp': time.time(),
            'generation_duration': time.time() - start_time,
            'consciousness_state': consciousness_state.__dict__,
            'fractal_data': {
                'cache_key': bloom_entry.cache_key,
                'file_path': bloom_entry.file_path,
                'visual_signature': bloom_entry.visual_signature,
                'generation_timestamp': bloom_entry.generated_timestamp
            }
        }
        
        # Add validation data if available
        if validation_report:
            record['validation_result'] = {
                'result': validation_report.validation_result.value,
                'parameter_accuracy': validation_report.parameter_accuracy,
                'pattern_family': validation_report.pattern_family.value,
                'owl_commentary': validation_report.owl_commentary,
                'soul_archive_hash': validation_report.soul_archive_hash,
                'quality_scores': {
                    'render_quality': validation_report.render_quality_score,
                    'parameter_fidelity': validation_report.parameter_fidelity,
                    'artistic_coherence': validation_report.artistic_coherence
                },
                'warnings': validation_report.warnings,
                'errors': validation_report.errors
            }
            record['soul_archive_hash'] = validation_report.soul_archive_hash
        
        return record
    
    def _update_soul_archive_stats(self, validation_report):
        """Update soul archive statistics"""
        
        self.soul_archive['total_blooms'] += 1
        
        # Update pattern family counts
        family = validation_report.pattern_family.value
        self.soul_archive['pattern_families'][family] = (
            self.soul_archive['pattern_families'].get(family, 0) + 1
        )
        
        # Update validation summary
        result = validation_report.validation_result.value
        if result == 'perfect_match':
            self.soul_archive['validation_summary']['perfect_matches'] += 1
        elif result == 'acceptable_variance':
            self.soul_archive['validation_summary']['acceptable_variance'] += 1
        elif result == 'parameter_mismatch':
            self.soul_archive['validation_summary']['parameter_mismatches'] += 1
        else:
            self.soul_archive['validation_summary']['generation_errors'] += 1
        
        # Store owl commentary and soul hash
        self.soul_archive['owl_commentaries'].append(validation_report.owl_commentary)
        self.soul_archive['soul_hashes'].append(validation_report.soul_archive_hash)
    
    def _archive_to_soul_collection(self, bloom_record: Dict[str, Any]):
        """Archive bloom record to soul collection"""
        
        # Create individual bloom archive file
        bloom_archive_path = (
            self.output_dir / "soul_archive" / f"{bloom_record['memory_id']}_soul.json"
        )
        
        with open(bloom_archive_path, 'w') as f:
            json.dump(bloom_record, f, indent=2, default=str)
    
    def _analyze_sequence_statistics(self, bloom_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze statistics for a bloom sequence"""
        
        successful_blooms = [b for b in bloom_records if b['generation_status'] == 'success']
        
        if not successful_blooms:
            return {'error': 'No successful blooms in sequence'}
        
        # Calculate generation time statistics
        generation_times = [b['generation_duration'] for b in successful_blooms]
        
        # Analyze validation results
        validation_results = []
        pattern_families = []
        owl_commentaries = []
        
        for bloom in successful_blooms:
            if bloom.get('validation_result'):
                validation_results.append(bloom['validation_result']['result'])
                pattern_families.append(bloom['validation_result']['pattern_family'])
                owl_commentaries.append(bloom['validation_result']['owl_commentary'])
        
        return {
            'total_blooms': len(bloom_records),
            'successful_blooms': len(successful_blooms),
            'success_rate': len(successful_blooms) / len(bloom_records),
            'generation_time_stats': {
                'average': sum(generation_times) / len(generation_times),
                'min': min(generation_times),
                'max': max(generation_times)
            },
            'validation_distribution': {
                result: validation_results.count(result) 
                for result in set(validation_results)
            },
            'pattern_family_distribution': {
                family: pattern_families.count(family) 
                for family in set(pattern_families)
            },
            'owl_commentary_count': len(owl_commentaries)
        }
    
    def _generate_collective_hash(self, bloom_records: List[Dict[str, Any]]) -> str:
        """Generate collective hash for bloom sequence"""
        
        # Combine all soul hashes for collective identity
        soul_hashes = [
            bloom.get('soul_archive_hash', '') 
            for bloom in bloom_records 
            if bloom.get('soul_archive_hash')
        ]
        
        if soul_hashes:
            collective_data = ''.join(sorted(soul_hashes))
            import hashlib
            return hashlib.sha256(collective_data.encode()).hexdigest()
        
        return ""
    
    def _analyze_owl_commentaries(self) -> Dict[str, Any]:
        """Analyze owl commentary themes and patterns"""
        
        commentaries = self.soul_archive['owl_commentaries']
        
        # Count thematic words
        theme_words = {
            'flow': ['flowing', 'streams', 'cascading', 'dancing', 'weaving'],
            'light': ['light', 'glowing', 'radiant', 'shimmering', 'luminous'],
            'memory': ['memory', 'echoes', 'traces', 'remnants', 'whispers'],
            'growth': ['blooming', 'emerging', 'unfolding', 'awakening', 'expanding'],
            'chaos': ['fractures', 'storms', 'scattered', 'wild', 'turbulent'],
            'peace': ['quiet', 'still', 'gentle', 'serene', 'peaceful']
        }
        
        theme_counts = {}
        for theme, words in theme_words.items():
            count = sum(
                commentary.lower().count(word) 
                for commentary in commentaries 
                for word in words
            )
            theme_counts[theme] = count
        
        return {
            'total_commentaries': len(commentaries),
            'average_length': sum(len(c) for c in commentaries) / max(len(commentaries), 1),
            'themes': theme_counts,
            'unique_commentaries': len(set(commentaries))
        }
    
    def shutdown(self):
        """Gracefully shutdown the integrated system"""
        
        print(f"\n🌸 Shutting down DAWN Integrated Bloom System...")
        
        # Save final soul archive statistics
        soul_stats_path = self.output_dir / "soul_archive" / "soul_archive_statistics.json"
        with open(soul_stats_path, 'w') as f:
            json.dump(self.soul_archive, f, indent=2)
        
        # Shutdown fractal interface
        self.fractal_interface.shutdown()
        
        print(f"✅ System shutdown complete")
        print(f"📊 Final stats: {self.soul_archive['total_blooms']} blooms generated")

# Demonstration function
def demo_integrated_bloom_system():
    """Demonstrate the complete integrated bloom system"""
    
    print("🌸 DAWN Integrated Bloom System - Complete Demo")
    print("=" * 48)
    
    # Initialize integrated system
    system = DAWNIntegratedBloomSystem(
        output_dir="dawn_complete_soul_archive",
        cache_size=50,
        validation_enabled=True
    )
    
    try:
        # Create consciousness evolution sequence
        consciousness_evolution = [
            DAWNConsciousnessConfig(
                memory_id="soul_birth", timestamp=None,
                bloom_entropy=0.1, mood_valence=0.8, drift_vector=0.0,
                rebloom_depth=3, sigil_saturation=0.6, pulse_zone="calm"
            ),
            DAWNConsciousnessConfig(
                memory_id="first_awakening", timestamp=None,
                bloom_entropy=0.3, mood_valence=0.5, drift_vector=0.2,
                rebloom_depth=5, sigil_saturation=0.7, pulse_zone="stable"
            ),
            DAWNConsciousnessConfig(
                memory_id="conscious_flow", timestamp=None,
                bloom_entropy=0.5, mood_valence=0.2, drift_vector=0.6,
                rebloom_depth=7, sigil_saturation=0.8, pulse_zone="flowing"
            ),
            DAWNConsciousnessConfig(
                memory_id="deep_memory_echo", timestamp=None,
                bloom_entropy=0.2, mood_valence=-0.3, drift_vector=0.1,
                rebloom_depth=9, sigil_saturation=0.9, pulse_zone="flowing"
            )
        ]
        
        # Generate consciousness sequence
        sequence_record = system.generate_consciousness_sequence(
            consciousness_evolution, "dawn_soul_evolution"
        )
        
        # Analyze soul archive
        archive_analysis = system.analyze_soul_archive()
        
        # Test similarity search
        target_state = consciousness_evolution[2]  # flowing state
        similar_blooms = system.get_similar_blooms_with_validation(target_state, 0.5)
        
        print(f"\n🔍 Similarity search results: {len(similar_blooms)} similar blooms found")
        
        return system, sequence_record, archive_analysis
        
    finally:
        system.shutdown()

if __name__ == "__main__":
    demo_integrated_bloom_system() 