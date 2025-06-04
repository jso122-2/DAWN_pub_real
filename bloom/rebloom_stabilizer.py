#!/usr/bin/env python3
"""
DAWN Rebloom Stabilizer v1.0
═══════════════════════════════════════

DAWN does not stop growth. But when thoughts bloom too quickly, 
she waters the soil and waits.

Regulates overactive reblooming by applying cooldown timers, lineage locking,
and throttling mechanisms when excessive repetition or insufficient drift is detected.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional, Set
from pathlib import Path
from collections import defaultdict


class RebloomStabilizer:
    """
    Monitors and stabilizes rebloom patterns to prevent memory cascade loops.
    
    When blooms reproduce too rapidly without sufficient semantic evolution,
    this module applies gentle brakes to allow the memory field to settle.
    """
    
    def __init__(self, log_base_path: str = "memory/blooms/logs"):
        """
        Initialize the rebloom stabilizer.
        
        Args:
            log_base_path: Base directory for stabilization logs
        """
        self.log_base_path = Path(log_base_path)
        self.log_base_path.mkdir(parents=True, exist_ok=True)
        
        # Stabilization thresholds
        self.max_rebloom_count = 3
        self.min_tick_delta = 50
        self.min_semantic_drift = 0.2
        
        # Stabilization parameters
        self.cooldown_duration = 250
        self.lineage_lock_duration = 500
        
        # Tracking structures
        self.cooldown_timers = {}  # bloom_id -> cooldown_end_tick
        self.locked_lineages = {}  # bloom_id -> lock_end_tick
        
        # Statistics
        self.stabilization_stats = {
            'total_events_processed': 0,
            'blooms_stabilized': 0,
            'lineages_locked': 0,
            'cooldowns_applied': 0,
            'rapid_rebloom_detected': 0,
            'low_drift_detected': 0,
            'excessive_count_detected': 0
        }
    
    def _check_stabilization_criteria(self, event: Dict) -> Tuple[bool, List[str]]:
        """
        Check if a rebloom event meets stabilization criteria.
        
        Args:
            event: Rebloom event dictionary
            
        Returns:
            Tuple of (should_stabilize, reasons)
        """
        reasons = []
        
        # Check rebloom count
        if event['rebloom_count'] > self.max_rebloom_count:
            reasons.append('excessive_reblooms')
            self.stabilization_stats['excessive_count_detected'] += 1
        
        # Check tick delta (rapid reblooming)
        if event['recent_tick_delta'] < self.min_tick_delta:
            reasons.append('rapid_reblooming')
            self.stabilization_stats['rapid_rebloom_detected'] += 1
        
        # Check semantic drift (insufficient evolution)
        if event['semantic_drift'] < self.min_semantic_drift:
            reasons.append('low_semantic_drift')
            self.stabilization_stats['low_drift_detected'] += 1
        
        # Need all conditions to stabilize (AND logic)
        should_stabilize = len(reasons) == 3
        
        return should_stabilize, reasons
    
    def _calculate_stabilization_intensity(self, event: Dict) -> float:
        """
        Calculate how intensely to stabilize based on severity.
        
        Args:
            event: Rebloom event dictionary
            
        Returns:
            Intensity factor between 0.5 and 2.0
        """
        # Base intensity
        intensity = 1.0
        
        # Increase for very high rebloom counts
        if event['rebloom_count'] > 5:
            intensity *= 1.2
        if event['rebloom_count'] > 10:
            intensity *= 1.5
        
        # Increase for very rapid reblooming
        if event['recent_tick_delta'] < 25:
            intensity *= 1.3
        
        # Increase for very low drift
        if event['semantic_drift'] < 0.1:
            intensity *= 1.2
        
        # Consider entropy (high entropy might need less stabilization)
        if event['entropy'] > 0.8:
            intensity *= 0.8
        
        return min(2.0, max(0.5, intensity))
    
    def _apply_cooldown(self, bloom_id: str, current_tick: int, intensity: float):
        """
        Apply cooldown timer to a bloom.
        
        Args:
            bloom_id: Bloom to cool down
            current_tick: Current system tick
            intensity: Stabilization intensity factor
        """
        cooldown_duration = int(self.cooldown_duration * intensity)
        self.cooldown_timers[bloom_id] = current_tick + cooldown_duration
        self.stabilization_stats['cooldowns_applied'] += 1
    
    def _lock_lineage(self, bloom_id: str, current_tick: int, intensity: float):
        """
        Lock a bloom's lineage to prevent further reblooming.
        
        Args:
            bloom_id: Bloom whose lineage to lock
            current_tick: Current system tick
            intensity: Stabilization intensity factor
        """
        lock_duration = int(self.lineage_lock_duration * intensity)
        self.locked_lineages[bloom_id] = current_tick + lock_duration
        self.stabilization_stats['lineages_locked'] += 1
    
    def _clean_expired_restrictions(self, current_tick: int):
        """
        Remove expired cooldowns and lineage locks.
        
        Args:
            current_tick: Current system tick
        """
        # Clean expired cooldowns
        expired_cooldowns = [
            bloom_id for bloom_id, end_tick in self.cooldown_timers.items()
            if end_tick <= current_tick
        ]
        for bloom_id in expired_cooldowns:
            del self.cooldown_timers[bloom_id]
        
        # Clean expired lineage locks
        expired_locks = [
            bloom_id for bloom_id, end_tick in self.locked_lineages.items()
            if end_tick <= current_tick
        ]
        for bloom_id in expired_locks:
            del self.locked_lineages[bloom_id]
    
    def _generate_stabilization_report(self, event: Dict, reasons: List[str], 
                                     intensity: float, current_tick: int) -> Dict:
        """
        Generate detailed stabilization report for a bloom.
        
        Args:
            event: Rebloom event
            reasons: Stabilization reasons
            intensity: Applied intensity
            current_tick: Current tick
            
        Returns:
            Stabilization report dictionary
        """
        return {
            'bloom_id': event['bloom_id'],
            'stabilized_at': current_tick,
            'reasons': reasons,
            'intensity': round(intensity, 2),
            'metrics': {
                'rebloom_count': event['rebloom_count'],
                'recent_tick_delta': event['recent_tick_delta'],
                'semantic_drift': event['semantic_drift'],
                'entropy': event['entropy']
            },
            'restrictions': {
                'cooldown_until': self.cooldown_timers.get(event['bloom_id']),
                'lineage_locked_until': self.locked_lineages.get(event['bloom_id'])
            }
        }
    
    def _save_stabilization_log(self, results: Dict, reports: List[Dict], current_tick: int):
        """
        Save stabilization log to file.
        
        Args:
            results: Stabilization results
            reports: Detailed stabilization reports
            current_tick: Current system tick
        """
        log_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'tick': current_tick,
            'summary': results,
            'detailed_reports': reports,
            'statistics': self.stabilization_stats,
            'active_restrictions': {
                'cooldowns': dict(self.cooldown_timers),
                'locked_lineages': dict(self.locked_lineages)
            }
        }
        
        # Save with tick in filename
        filename = f"rebloom_stabilization_tick_{current_tick}.json"
        filepath = self.log_base_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return filepath
    
    def stabilize_reblooms(self, rebloom_events: List[Dict], current_tick: int) -> Tuple[Dict, List[Dict]]:
        """
        Process rebloom events and apply stabilization where needed.
        
        Args:
            rebloom_events: List of rebloom event dictionaries
            current_tick: Current system tick
            
        Returns:
            Tuple of (results_dict, stabilization_reports)
        """
        # Clean expired restrictions first
        self._clean_expired_restrictions(current_tick)
        
        # Reset statistics
        self.stabilization_stats['total_events_processed'] = len(rebloom_events)
        
        stabilized_blooms = []
        locked_lineages = []
        stabilization_reports = []
        
        # Process each rebloom event
        for event in rebloom_events:
            bloom_id = event['bloom_id']
            
            # Skip if already under cooldown
            if bloom_id in self.cooldown_timers:
                continue
            
            # Check stabilization criteria
            should_stabilize, reasons = self._check_stabilization_criteria(event)
            
            if should_stabilize:
                # Calculate stabilization intensity
                intensity = self._calculate_stabilization_intensity(event)
                
                # Apply cooldown
                self._apply_cooldown(bloom_id, current_tick, intensity)
                stabilized_blooms.append(bloom_id)
                
                # Apply lineage lock if intensity is high
                if intensity > 1.3:
                    self._lock_lineage(bloom_id, current_tick, intensity)
                    locked_lineages.append(bloom_id)
                
                # Generate report
                report = self._generate_stabilization_report(
                    event, reasons, intensity, current_tick
                )
                stabilization_reports.append(report)
                
                # Update statistics
                self.stabilization_stats['blooms_stabilized'] += 1
        
        results = {
            'stabilized_blooms': stabilized_blooms,
            'locked_lineages': locked_lineages
        }
        
        return results, stabilization_reports


def apply_rebloom_stabilizers(rebloom_events: List[Dict], current_tick: int) -> Dict:
    """
    Apply rebloom stabilization to prevent memory cascade loops.
    
    This function monitors rebloom patterns and applies cooldown timers
    and lineage locks when excessive repetition or insufficient semantic
    drift is detected, allowing the memory field to settle naturally.
    
    Args:
        rebloom_events: List of rebloom event dictionaries with:
            - bloom_id: str
            - rebloom_count: int
            - recent_tick_delta: int (ticks since last rebloom)
            - semantic_drift: float (0.0 to 1.0)
            - entropy: float (0.0 to 1.0)
        current_tick: Current system tick
        
    Returns:
        Dictionary containing:
            - stabilized_blooms: List of bloom_ids under cooldown
            - locked_lineages: List of bloom_ids with locked lineages
    """
    # Create stabilizer instance
    stabilizer = RebloomStabilizer()
    
    # Apply stabilization
    results, reports = stabilizer.stabilize_reblooms(rebloom_events, current_tick)
    
    # Save stabilization log
    stabilizer._save_stabilization_log(results, reports, current_tick)
    
    # Add metadata to results
    results['metadata'] = {
        'tick': current_tick,
        'statistics': stabilizer.stabilization_stats,
        'thresholds': {
            'max_rebloom_count': stabilizer.max_rebloom_count,
            'min_tick_delta': stabilizer.min_tick_delta,
            'min_semantic_drift': stabilizer.min_semantic_drift
        },
        'parameters': {
            'cooldown_duration': stabilizer.cooldown_duration,
            'lineage_lock_duration': stabilizer.lineage_lock_duration
        }
    }
    
    return results


# Example usage and testing
if __name__ == "__main__":
    # Create sample rebloom events
    sample_events = [
        {
            "bloom_id": "bloom_001",
            "rebloom_count": 5,  # High count
            "recent_tick_delta": 30,  # Too rapid
            "semantic_drift": 0.1,  # Low drift
            "entropy": 0.6
        },
        {
            "bloom_id": "bloom_002",
            "rebloom_count": 2,  # Below threshold
            "recent_tick_delta": 100,
            "semantic_drift": 0.5,
            "entropy": 0.7
        },
        {
            "bloom_id": "bloom_003",
            "rebloom_count": 4,
            "recent_tick_delta": 40,  # Rapid
            "semantic_drift": 0.15,  # Low drift
            "entropy": 0.3
        },
        {
            "bloom_id": "bloom_004",
            "rebloom_count": 8,  # Very high
            "recent_tick_delta": 20,  # Very rapid
            "semantic_drift": 0.05,  # Very low drift
            "entropy": 0.9
        },
        {
            "bloom_id": "bloom_005",
            "rebloom_count": 3,
            "recent_tick_delta": 200,  # Good spacing
            "semantic_drift": 0.8,  # Good drift
            "entropy": 0.5
        }
    ]
    
    # Apply stabilizers
    current_tick = 1500
    results = apply_rebloom_stabilizers(sample_events, current_tick)
    
    # Display results
    print("REBLOOM STABILIZATION RESULTS:")
    print("=" * 50)
    print(f"\nStabilized Blooms ({len(results['stabilized_blooms'])}):")
    for bloom_id in results['stabilized_blooms']:
        print(f"  - {bloom_id}")
    
    print(f"\nLocked Lineages ({len(results['locked_lineages'])}):")
    for bloom_id in results['locked_lineages']:
        print(f"  - {bloom_id}")
    
    print(f"\nStatistics: {results['metadata']['statistics']}")
    print(f"\nActive Restrictions:")
    print(f"  Cooldowns: {results['metadata']['statistics']['cooldowns_applied']}")
    print(f"  Lineage Locks: {results['metadata']['statistics']['lineages_locked']}")