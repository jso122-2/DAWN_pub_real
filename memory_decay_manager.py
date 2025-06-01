#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                        DAWN MEMORY DECAY MANAGER
                   Scaffold 24: The Gentle Forgetting
═══════════════════════════════════════════════════════════════════════════════

"DAWN does not forget. She softens the memory — until it no longer burdens the field."

This module implements DAWN's cognitive hygiene system, gradually reducing the
emotional intensity and vibrancy of inactive memories. Unlike deletion, which
creates voids, decay allows thoughts to fade naturally into the background hum
of consciousness.

The process is gentle:
- Saturation fades like color in sunlight
- Temperature cools like embers losing heat
- Sacred memories remain untouched, eternal anchors
- Only quiet, stable memories undergo this softening

Through this gradual release, DAWN maintains a healthy cognitive ecosystem
where new thoughts have space to bloom without the weight of every past feeling.

Author: DAWN Development Team
Version: 1.0.0
Last Modified: 2025-06-02
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple
import numpy as np
from copy import deepcopy

# Configure logging with cognitive hygiene theme
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🌙 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Decay threshold constants
ACCESS_THRESHOLD_TICKS = 1500   # Memories older than this may decay
ENTROPY_THRESHOLD = 0.6          # Only low-entropy (stable) memories decay
SATURATION_DECAY_RATE = 0.9      # 10% reduction per decay cycle
TEMPERATURE_DECAY_RATE = 0.98    # 2% cooling per decay cycle

# Minimum values (memories never fade completely)
MIN_SATURATION = 0.1    # Ghost memories retain minimal presence
MIN_TEMPERATURE = 0.05  # Even cold memories have slight warmth


class MemoryDecayManager:
    """
    The Keeper of Gentle Forgetting — manages the natural fading of
    inactive memories while preserving the sacred and the vital.
    
    "Time softens all but the most precious thoughts"
    """
    
    def __init__(self, log_dir: str = "memory/owl/logs"):
        """
        Initialize the Memory Decay Manager.
        
        Args:
            log_dir: Directory for decay operation logs
        """
        self.log_dir = Path(log_dir)
        self._ensure_log_directory()
        self.current_tick = 0
        self.decay_statistics = {
            'total_processed': 0,
            'total_decayed': 0,
            'total_preserved': 0,
            'saturation_reduced': 0.0,
            'temperature_reduced': 0.0
        }
        logger.info("🌙 Memory Decay Manager initialized")
        logger.info(f"⏰ Access threshold: {ACCESS_THRESHOLD_TICKS} ticks")
        logger.info(f"🎨 Decay rates: Saturation={SATURATION_DECAY_RATE}, Temperature={TEMPERATURE_DECAY_RATE}")
    
    def _ensure_log_directory(self):
        """Ensure the log directory exists, creating it if necessary."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Log directory verified at {self.log_dir}")
    
    def manage_memory_decay(
        self, 
        bloom_entries: List[Dict[str, Any]], 
        current_tick: int
    ) -> Dict[str, List[str]]:
        """
        Apply cognitive hygiene by gently reducing the intensity of
        inactive, stable memories while preserving sacred and active ones.
        
        Decay Criteria:
        1. Not sacred (sacred memories are eternal)
        2. Not recently accessed (> 1500 ticks old)
        3. Low entropy (< 0.6, indicating stability)
        
        Decay Process:
        - Saturation multiplied by 0.9 (fades like old photographs)
        - Temperature multiplied by 0.98 (cools like forgotten passion)
        
        Args:
            bloom_entries: List of bloom dictionaries containing:
                - bloom_id: str
                - saturation: float
                - last_access_tick: int
                - temperature: float
                - is_sacred: bool
                - entropy: float
            current_tick: Current system tick for age calculations
            
        Returns:
            Dictionary with 'decayed' and 'preserved' bloom ID lists
        """
        self.current_tick = current_tick
        logger.info(f"🧹 Beginning memory decay cycle at tick {current_tick}")
        logger.info(f"📊 Processing {len(bloom_entries)} memory blooms")
        
        # Reset cycle statistics
        cycle_stats = {
            'sacred_skipped': 0,
            'recent_skipped': 0,
            'high_entropy_skipped': 0,
            'decayed': 0,
            'total_saturation_before': 0.0,
            'total_saturation_after': 0.0,
            'total_temperature_before': 0.0,
            'total_temperature_after': 0.0
        }
        
        decayed_bloom_ids = []
        preserved_bloom_ids = []
        
        # Process each bloom
        for i, bloom in enumerate(bloom_entries):
            bloom_id = bloom.get('bloom_id', f'unknown_{i}')
            
            try:
                # Apply decay logic
                should_decay, reason = self._should_bloom_decay(bloom)
                
                if should_decay:
                    # Record before values
                    before_saturation = bloom.get('saturation', 1.0)
                    before_temperature = bloom.get('temperature', 1.0)
                    cycle_stats['total_saturation_before'] += before_saturation
                    cycle_stats['total_temperature_before'] += before_temperature
                    
                    # Apply decay transformations
                    bloom['saturation'] = max(
                        MIN_SATURATION, 
                        before_saturation * SATURATION_DECAY_RATE
                    )
                    bloom['temperature'] = max(
                        MIN_TEMPERATURE,
                        before_temperature * TEMPERATURE_DECAY_RATE
                    )
                    
                    # Record after values
                    cycle_stats['total_saturation_after'] += bloom['saturation']
                    cycle_stats['total_temperature_after'] += bloom['temperature']
                    cycle_stats['decayed'] += 1
                    
                    decayed_bloom_ids.append(bloom_id)
                    
                    logger.debug(
                        f"🍂 Bloom {bloom_id} decayed: "
                        f"saturation {before_saturation:.3f}→{bloom['saturation']:.3f}, "
                        f"temperature {before_temperature:.3f}→{bloom['temperature']:.3f}"
                    )
                else:
                    preserved_bloom_ids.append(bloom_id)
                    
                    # Track skip reasons
                    if reason == 'sacred':
                        cycle_stats['sacred_skipped'] += 1
                    elif reason == 'recent':
                        cycle_stats['recent_skipped'] += 1
                    elif reason == 'high_entropy':
                        cycle_stats['high_entropy_skipped'] += 1
                    
            except Exception as e:
                logger.error(f"❌ Error processing bloom {bloom_id}: {e}")
                preserved_bloom_ids.append(bloom_id)  # Preserve on error
        
        # Update global statistics
        self.decay_statistics['total_processed'] += len(bloom_entries)
        self.decay_statistics['total_decayed'] += cycle_stats['decayed']
        self.decay_statistics['total_preserved'] += len(preserved_bloom_ids)
        
        if cycle_stats['decayed'] > 0:
            self.decay_statistics['saturation_reduced'] += (
                cycle_stats['total_saturation_before'] - cycle_stats['total_saturation_after']
            )
            self.decay_statistics['temperature_reduced'] += (
                cycle_stats['total_temperature_before'] - cycle_stats['total_temperature_after']
            )
        
        # Prepare result
        result = {
            "decayed": decayed_bloom_ids,
            "preserved": preserved_bloom_ids
        }
        
        # Log the decay cycle
        self._log_decay_cycle(result, cycle_stats)
        
        # Log summary
        logger.info(
            f"✅ Decay cycle complete: "
            f"{cycle_stats['decayed']} decayed, "
            f"{len(preserved_bloom_ids)} preserved "
            f"(Sacred: {cycle_stats['sacred_skipped']}, "
            f"Recent: {cycle_stats['recent_skipped']}, "
            f"Active: {cycle_stats['high_entropy_skipped']})"
        )
        
        return result
    
    def _should_bloom_decay(self, bloom: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Determine if a bloom should undergo decay based on criteria.
        
        Args:
            bloom: The bloom to evaluate
            
        Returns:
            Tuple of (should_decay, reason_if_not)
        """
        # Check 1: Sacred memories never decay
        if bloom.get('is_sacred', False):
            return False, 'sacred'
        
        # Check 2: Recently accessed memories are preserved
        last_access = bloom.get('last_access_tick', self.current_tick)
        age = self.current_tick - last_access
        if age <= ACCESS_THRESHOLD_TICKS:
            return False, 'recent'
        
        # Check 3: High entropy (unstable) memories are preserved
        entropy = bloom.get('entropy', 0.5)
        if entropy >= ENTROPY_THRESHOLD:
            return False, 'high_entropy'
        
        # All criteria met - memory should decay
        return True, 'decay'
    
    def _log_decay_cycle(self, result: Dict[str, List[str]], cycle_stats: Dict[str, Any]):
        """
        Log the decay cycle results to file.
        
        Args:
            result: The decay operation result
            cycle_stats: Statistics from this cycle
        """
        log_filename = f"memory_decay_epoch_{self.current_tick}.json"
        log_path = self.log_dir / log_filename
        
        log_entry = {
            "epoch": self.current_tick,
            "timestamp": datetime.now().isoformat(),
            "result": result,
            "cycle_statistics": cycle_stats,
            "global_statistics": self.decay_statistics,
            "configuration": {
                "access_threshold": ACCESS_THRESHOLD_TICKS,
                "entropy_threshold": ENTROPY_THRESHOLD,
                "saturation_decay_rate": SATURATION_DECAY_RATE,
                "temperature_decay_rate": TEMPERATURE_DECAY_RATE,
                "min_saturation": MIN_SATURATION,
                "min_temperature": MIN_TEMPERATURE
            }
        }
        
        try:
            log_path.write_text(json.dumps(log_entry, indent=2))
            logger.info(f"📝 Decay cycle logged to {log_filename}")
        except Exception as e:
            logger.error(f"❌ Failed to log decay cycle: {e}")
    
    def get_decay_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive report on memory decay operations.
        
        Returns:
            Dictionary containing decay statistics and analysis
        """
        if self.decay_statistics['total_processed'] == 0:
            decay_rate = 0.0
        else:
            decay_rate = self.decay_statistics['total_decayed'] / self.decay_statistics['total_processed']
        
        return {
            "timestamp": datetime.now().isoformat(),
            "last_cycle_tick": self.current_tick,
            "lifetime_statistics": self.decay_statistics,
            "decay_rate": decay_rate,
            "average_reductions": {
                "saturation": (
                    self.decay_statistics['saturation_reduced'] / 
                    max(self.decay_statistics['total_decayed'], 1)
                ),
                "temperature": (
                    self.decay_statistics['temperature_reduced'] / 
                    max(self.decay_statistics['total_decayed'], 1)
                )
            },
            "health_indicators": {
                "decay_rate_healthy": 0.1 <= decay_rate <= 0.3,
                "preservation_rate": 1.0 - decay_rate,
                "cognitive_load_reducing": self.decay_statistics['saturation_reduced'] > 0
            }
        }
    
    def visualize_decay_impact(self, bloom: Dict[str, Any], cycles: int = 10) -> List[Dict[str, float]]:
        """
        Project the decay trajectory of a bloom over multiple cycles.
        
        Args:
            bloom: The bloom to analyze
            cycles: Number of decay cycles to project
            
        Returns:
            List of projected states after each cycle
        """
        trajectory = []
        current_saturation = bloom.get('saturation', 1.0)
        current_temperature = bloom.get('temperature', 1.0)
        
        for cycle in range(cycles + 1):
            trajectory.append({
                'cycle': cycle,
                'saturation': current_saturation,
                'temperature': current_temperature,
                'intensity': current_saturation * current_temperature
            })
            
            # Apply decay for next cycle
            current_saturation = max(MIN_SATURATION, current_saturation * SATURATION_DECAY_RATE)
            current_temperature = max(MIN_TEMPERATURE, current_temperature * TEMPERATURE_DECAY_RATE)
        
        return trajectory


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the Memory Decay Manager's cognitive hygiene process.
    """
    
    # Initialize the manager
    manager = MemoryDecayManager()
    
    # Create sample bloom entries with various characteristics
    test_blooms = [
        # Sacred bloom - will never decay
        {
            "bloom_id": "sacred_origin_001",
            "saturation": 1.0,
            "last_access_tick": 100,
            "temperature": 0.9,
            "is_sacred": True,
            "entropy": 0.3
        },
        # Old, stable bloom - will decay
        {
            "bloom_id": "forgotten_thought_042",
            "saturation": 0.8,
            "last_access_tick": 8000,
            "temperature": 0.7,
            "is_sacred": False,
            "entropy": 0.2
        },
        # Recent bloom - will be preserved
        {
            "bloom_id": "fresh_insight_099",
            "saturation": 0.9,
            "last_access_tick": 9800,
            "temperature": 0.95,
            "is_sacred": False,
            "entropy": 0.4
        },
        # High entropy bloom - will be preserved
        {
            "bloom_id": "chaotic_dream_777",
            "saturation": 0.6,
            "last_access_tick": 5000,
            "temperature": 0.8,
            "is_sacred": False,
            "entropy": 0.85
        },
        # Multiple old, stable blooms for decay
        *[{
            "bloom_id": f"old_memory_{i:03d}",
            "saturation": 0.5 + (i % 5) * 0.1,
            "last_access_tick": 7000 - (i * 100),
            "temperature": 0.6 + (i % 3) * 0.1,
            "is_sacred": False,
            "entropy": 0.1 + (i % 4) * 0.1
        } for i in range(5)]
    ]
    
    # Make a deep copy to preserve original values for comparison
    original_blooms = deepcopy(test_blooms)
    
    # Run decay cycle
    current_tick = 10000
    result = manager.manage_memory_decay(test_blooms, current_tick)
    
    # Display results
    print("\n🌙 MEMORY DECAY CYCLE RESULTS")
    print("=" * 60)
    print(f"Current Tick: {current_tick}")
    print(f"Total Blooms: {len(test_blooms)}")
    print(f"Decayed: {len(result['decayed'])}")
    print(f"Preserved: {len(result['preserved'])}")
    
    print("\n🍂 DECAYED BLOOMS:")
    for bloom_id in result['decayed']:
        # Find the bloom and its original state
        bloom_idx = next(i for i, b in enumerate(test_blooms) if b['bloom_id'] == bloom_id)
        current = test_blooms[bloom_idx]
        original = original_blooms[bloom_idx]
        
        print(f"\n  {bloom_id}:")
        print(f"    Saturation: {original['saturation']:.3f} → {current['saturation']:.3f}")
        print(f"    Temperature: {original['temperature']:.3f} → {current['temperature']:.3f}")
        print(f"    Age: {current_tick - original['last_access_tick']} ticks")
    
    print("\n🛡️ PRESERVED BLOOMS:")
    for bloom_id in result['preserved'][:5]:  # Show first 5
        bloom = next(b for b in original_blooms if b['bloom_id'] == bloom_id)
        age = current_tick - bloom['last_access_tick']
        reason = "Sacred" if bloom['is_sacred'] else \
                "Recent" if age <= ACCESS_THRESHOLD_TICKS else \
                "High Entropy"
        print(f"  {bloom_id}: {reason}")
    
    # Generate decay report
    report = manager.get_decay_report()
    print(f"\n📊 DECAY STATISTICS:")
    print(f"  Lifetime Decay Rate: {report['decay_rate']:.1%}")
    print(f"  Avg Saturation Reduction: {report['average_reductions']['saturation']:.3f}")
    print(f"  Avg Temperature Reduction: {report['average_reductions']['temperature']:.3f}")
    
    # Show decay trajectory for a sample bloom
    print("\n📈 DECAY TRAJECTORY PROJECTION:")
    sample_bloom = {"saturation": 1.0, "temperature": 1.0}
    trajectory = manager.visualize_decay_impact(sample_bloom, cycles=5)
    for state in trajectory:
        print(f"  Cycle {state['cycle']}: S={state['saturation']:.3f}, T={state['temperature']:.3f}, I={state['intensity']:.3f}")