#!/usr/bin/env python3
"""
DAWN OWL Entropy Sweeper v1.0
═══════════════════════════════════════

Owl does not act loudly. She brushes memory with a feather — 
and if it does not stir, she lets it sleep.

The OWL tracer walks through memory blooms with low-frequency observation,
determining which memories are ready for transformation through decay or rebloom,
and which should remain untouched in their current state.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple
from pathlib import Path


class OWLEntropySweeper:
    """
    OWL (Observational Wisdom Layer) entropy sweeper for DAWN's memory system.
    
    Performs low-frequency sweeps through bloom memory to identify candidates
    for decay, rebloom, or preservation based on entropy and access patterns.
    """
    
    def __init__(self, log_base_path: str = "memory/owl/logs"):
        """
        Initialize the OWL entropy sweeper.
        
        Args:
            log_base_path: Base directory for sweep logs
        """
        self.log_base_path = Path(log_base_path)
        self.log_base_path.mkdir(parents=True, exist_ok=True)
        
        # Sweep thresholds
        self.entropy_decay_threshold = 0.85
        self.entropy_rebloom_threshold = 0.3
        self.access_decay_threshold = 1500
        self.min_lineage_for_rebloom = 2
        
        # Statistics tracking
        self.sweep_stats = {
            'total_blooms': 0,
            'marked_for_decay': 0,
            'marked_for_rebloom': 0,
            'sacred_preserved': 0,
            'naturally_preserved': 0
        }
    
    def _check_decay_conditions(self, bloom: Dict, current_tick: int) -> bool:
        """
        Check if a bloom meets decay conditions.
        
        Decay if:
        - Entropy > 0.85 AND
        - Last access was more than 1500 ticks ago
        
        Args:
            bloom: Bloom data dictionary
            current_tick: Current system tick
            
        Returns:
            True if bloom should decay, False otherwise
        """
        if bloom.get('is_sacred', False):
            return False
        
        ticks_since_access = current_tick - bloom['last_access_tick']
        
        return (
            bloom['entropy'] > self.entropy_decay_threshold and
            ticks_since_access > self.access_decay_threshold
        )
    
    def _check_rebloom_conditions(self, bloom: Dict) -> bool:
        """
        Check if a bloom meets rebloom conditions.
        
        Rebloom if:
        - Entropy < 0.3 AND
        - Never rebloomed before (rebloom_count == 0) AND
        - Lineage depth > 2
        
        Args:
            bloom: Bloom data dictionary
            
        Returns:
            True if bloom should rebloom, False otherwise
        """
        if bloom.get('is_sacred', False):
            return False
        
        return (
            bloom['entropy'] < self.entropy_rebloom_threshold and
            bloom['rebloom_count'] == 0 and
            bloom['lineage_depth'] > self.min_lineage_for_rebloom
        )
    
    def _log_sweep_results(self, results: Dict, current_tick: int, sweep_duration: float):
        """
        Log sweep results to file.
        
        Args:
            results: Sweep results dictionary
            current_tick: Current system tick
            sweep_duration: Time taken for sweep in seconds
        """
        log_filename = f"entropy_sweep_epoch_{current_tick}.txt"
        log_path = self.log_base_path / log_filename
        
        timestamp = datetime.now(timezone.utc).isoformat()
        
        with open(log_path, 'w') as f:
            f.write(f"OWL ENTROPY SWEEP LOG\n")
            f.write(f"{'=' * 50}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Epoch: {current_tick}\n")
            f.write(f"Duration: {sweep_duration:.3f}s\n")
            f.write(f"\nSTATISTICS:\n")
            f.write(f"Total blooms examined: {self.sweep_stats['total_blooms']}\n")
            f.write(f"Marked for decay: {self.sweep_stats['marked_for_decay']}\n")
            f.write(f"Marked for rebloom: {self.sweep_stats['marked_for_rebloom']}\n")
            f.write(f"Sacred (preserved): {self.sweep_stats['sacred_preserved']}\n")
            f.write(f"Naturally preserved: {self.sweep_stats['naturally_preserved']}\n")
            f.write(f"\nDECAY QUEUE ({len(results['decay_queue'])} items):\n")
            for bloom_id in results['decay_queue']:
                f.write(f"  - {bloom_id}\n")
            f.write(f"\nREBLOOM QUEUE ({len(results['rebloom_queue'])} items):\n")
            for bloom_id in results['rebloom_queue']:
                f.write(f"  - {bloom_id}\n")
            f.write(f"\nSKIPPED ({len(results['skipped'])} items):\n")
            # Only log first 10 skipped to avoid huge logs
            for bloom_id in results['skipped'][:10]:
                f.write(f"  - {bloom_id}\n")
            if len(results['skipped']) > 10:
                f.write(f"  ... and {len(results['skipped']) - 10} more\n")
    
    def sweep_blooms(self, bloom_data: List[Dict], current_tick: int) -> Dict[str, List[str]]:
        """
        Perform entropy sweep on bloom data.
        
        Args:
            bloom_data: List of bloom dictionaries
            current_tick: Current system tick
            
        Returns:
            Dictionary with rebloom_queue, decay_queue, and skipped lists
        """
        # Reset statistics
        self.sweep_stats = {
            'total_blooms': len(bloom_data),
            'marked_for_decay': 0,
            'marked_for_rebloom': 0,
            'sacred_preserved': 0,
            'naturally_preserved': 0
        }
        
        # Initialize result queues
        rebloom_queue = []
        decay_queue = []
        skipped = []
        
        # Process each bloom
        for bloom in bloom_data:
            bloom_id = bloom['bloom_id']
            
            # Check sacred status first
            if bloom.get('is_sacred', False):
                skipped.append(bloom_id)
                self.sweep_stats['sacred_preserved'] += 1
                continue
            
            # Check decay conditions
            if self._check_decay_conditions(bloom, current_tick):
                decay_queue.append(bloom_id)
                self.sweep_stats['marked_for_decay'] += 1
            # Check rebloom conditions
            elif self._check_rebloom_conditions(bloom):
                rebloom_queue.append(bloom_id)
                self.sweep_stats['marked_for_rebloom'] += 1
            # Otherwise skip (preserve naturally)
            else:
                skipped.append(bloom_id)
                self.sweep_stats['naturally_preserved'] += 1
        
        return {
            'rebloom_queue': rebloom_queue,
            'decay_queue': decay_queue,
            'skipped': skipped
        }


def run_entropy_sweep(bloom_data: List[Dict], current_tick: int) -> Dict[str, List[str]]:
    """
    Main callable for running OWL entropy sweep.
    
    This function performs a gentle sweep through all memory blooms,
    determining which are ready for transformation and which should rest.
    
    Args:
        bloom_data: List of bloom dictionaries with required fields:
            - bloom_id: str
            - entropy: float (0.0 to 1.0)
            - lineage_depth: int
            - last_access_tick: int
            - is_sacred: bool
            - rebloom_count: int
        current_tick: Current system tick
        
    Returns:
        Dictionary containing:
            - rebloom_queue: List of bloom_ids marked for rebloom
            - decay_queue: List of bloom_ids marked for decay
            - skipped: List of bloom_ids to leave untouched
    """
    import time
    start_time = time.time()
    
    # Create sweeper instance
    sweeper = OWLEntropySweeper()
    
    # Perform sweep
    results = sweeper.sweep_blooms(bloom_data, current_tick)
    
    # Calculate duration
    sweep_duration = time.time() - start_time
    
    # Log results
    sweeper._log_sweep_results(results, current_tick, sweep_duration)
    
    # Add metadata to results
    results['metadata'] = {
        'tick': current_tick,
        'duration_seconds': sweep_duration,
        'stats': sweeper.sweep_stats
    }
    
    return results


# Example usage and testing
if __name__ == "__main__":
    # Create sample bloom data
    sample_blooms = [
        {
            "bloom_id": "bloom_001",
            "entropy": 0.9,  # High entropy
            "lineage_depth": 3,
            "last_access_tick": 100,  # Old access
            "is_sacred": False,
            "rebloom_count": 1
        },
        {
            "bloom_id": "bloom_002",
            "entropy": 0.2,  # Low entropy
            "lineage_depth": 4,
            "last_access_tick": 1500,
            "is_sacred": False,
            "rebloom_count": 0  # Never rebloomed
        },
        {
            "bloom_id": "bloom_003",
            "entropy": 0.95,
            "lineage_depth": 2,
            "last_access_tick": 50,
            "is_sacred": True,  # Sacred, never touch
            "rebloom_count": 0
        },
        {
            "bloom_id": "bloom_004",
            "entropy": 0.5,  # Medium entropy
            "lineage_depth": 1,
            "last_access_tick": 1000,
            "is_sacred": False,
            "rebloom_count": 2
        },
        {
            "bloom_id": "bloom_005",
            "entropy": 0.1,  # Very low entropy
            "lineage_depth": 1,  # Too shallow for rebloom
            "last_access_tick": 1600,
            "is_sacred": False,
            "rebloom_count": 0
        }
    ]
    
    # Run entropy sweep
    current_tick = 1700
    results = run_entropy_sweep(sample_blooms, current_tick)
    
    # Display results
    print("OWL Entropy Sweep Results:")
    print(f"  Rebloom queue: {results['rebloom_queue']}")
    print(f"  Decay queue: {results['decay_queue']}")
    print(f"  Skipped: {results['skipped']}")
    print(f"\nMetadata:")
    print(f"  Duration: {results['metadata']['duration_seconds']:.3f}s")
    print(f"  Stats: {results['metadata']['stats']}")