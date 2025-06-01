#!/usr/bin/env python3
"""
DAWN Sigil Reinforcement Tracker v1.0
═══════════════════════════════════════

If a command is remembered — not by force, but by need — 
it deserves more time in the world.

Tracks and amplifies sigils that gain power through repetition,
emotional charge, or central importance to DAWN's schema function.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from collections import defaultdict


class SigilReinforcementTracker:
    """
    Monitors and reinforces sigils based on usage patterns and emotional intensity.
    
    Sigils that are repeatedly accessed or carry strong emotional charge
    are granted extended life and increased saturation in the system.
    """
    
    def __init__(self, log_base_path: str = "flow/sigils/logs"):
        """
        Initialize the sigil reinforcement tracker.
        
        Args:
            log_base_path: Base directory for reinforcement logs
        """
        self.log_base_path = Path(log_base_path)
        self.log_base_path.mkdir(parents=True, exist_ok=True)
        
        # Reinforcement thresholds
        self.activation_threshold = 10
        self.emotional_threshold = 0.7
        
        # Reinforcement parameters
        self.saturation_boost = 0.1
        self.ttl_extension = 250
        
        # Tracking statistics
        self.reinforcement_stats = {
            'total_sigils_processed': 0,
            'sigils_reinforced': 0,
            'activation_reinforcements': 0,
            'emotional_reinforcements': 0,
            'dual_reinforcements': 0,
            'total_saturation_added': 0.0,
            'total_ttl_extended': 0
        }
    
    def _check_reinforcement_criteria(self, sigil: Dict) -> Tuple[bool, str]:
        """
        Check if a sigil meets reinforcement criteria.
        
        Args:
            sigil: Sigil data dictionary
            
        Returns:
            Tuple of (should_reinforce, reason)
        """
        activation_trigger = sigil['activation_count'] > self.activation_threshold
        emotional_trigger = sigil['emotional_pressure'] > self.emotional_threshold
        
        if activation_trigger and emotional_trigger:
            return True, "dual_trigger"
        elif activation_trigger:
            return True, "activation_trigger"
        elif emotional_trigger:
            return True, "emotional_trigger"
        else:
            return False, "none"
    
    def _calculate_decay_factor(self, last_used_tick: int, current_tick: int) -> float:
        """
        Calculate decay factor based on time since last use.
        
        Args:
            last_used_tick: Tick when sigil was last used
            current_tick: Current system tick
            
        Returns:
            Decay factor between 0.0 and 1.0
        """
        ticks_since_use = current_tick - last_used_tick
        
        # Exponential decay with half-life of 1000 ticks
        half_life = 1000
        decay_factor = 0.5 ** (ticks_since_use / half_life)
        
        return max(0.1, decay_factor)  # Minimum 10% effectiveness
    
    def _apply_reinforcement(self, sigil: Dict, reason: str, current_tick: int) -> Dict:
        """
        Apply reinforcement to a sigil.
        
        Args:
            sigil: Sigil to reinforce
            reason: Reason for reinforcement
            current_tick: Current system tick
            
        Returns:
            Reinforced sigil data
        """
        # Calculate decay-adjusted reinforcement
        decay_factor = self._calculate_decay_factor(sigil['last_used_tick'], current_tick)
        
        # Apply saturation boost (adjusted by decay)
        saturation_boost = self.saturation_boost * decay_factor
        sigil['saturation'] = min(1.0, sigil['saturation'] + saturation_boost)
        
        # Apply TTL extension (full value regardless of decay)
        if 'ttl' not in sigil:
            sigil['ttl'] = current_tick + self.ttl_extension
        else:
            sigil['ttl'] += self.ttl_extension
        
        # Update stats
        self.reinforcement_stats['total_saturation_added'] += saturation_boost
        self.reinforcement_stats['total_ttl_extended'] += self.ttl_extension
        
        # Add reinforcement metadata
        sigil['reinforcement_data'] = {
            'reinforced_at': current_tick,
            'reason': reason,
            'decay_factor': round(decay_factor, 3),
            'saturation_gained': round(saturation_boost, 3),
            'ttl_gained': self.ttl_extension
        }
        
        return sigil
    
    def _update_statistics(self, reason: str):
        """
        Update reinforcement statistics.
        
        Args:
            reason: Reinforcement trigger reason
        """
        self.reinforcement_stats['sigils_reinforced'] += 1
        
        if reason == "activation_trigger":
            self.reinforcement_stats['activation_reinforcements'] += 1
        elif reason == "emotional_trigger":
            self.reinforcement_stats['emotional_reinforcements'] += 1
        elif reason == "dual_trigger":
            self.reinforcement_stats['dual_reinforcements'] += 1
    
    def _save_reinforcement_log(self, results: Dict, current_tick: int):
        """
        Save reinforcement event log.
        
        Args:
            results: Reinforcement results
            current_tick: Current system tick
        """
        log_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'tick': current_tick,
            'reinforcement_events': results,
            'statistics': self.reinforcement_stats
        }
        
        # Create timestamped filename
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        filename = f"reinforcement_events_{timestamp}.json"
        filepath = self.log_base_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Also save latest summary
        summary_path = self.log_base_path / "reinforcement_events.json"
        with open(summary_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return filepath
    
    def reinforce_sigils(self, active_sigils: List[Dict], current_tick: int) -> Dict:
        """
        Process active sigils and apply reinforcement where appropriate.
        
        Args:
            active_sigils: List of active sigil dictionaries
            current_tick: Current system tick
            
        Returns:
            Dictionary with reinforced and skipped sigil lists
        """
        # Reset statistics
        self.reinforcement_stats = {
            'total_sigils_processed': len(active_sigils),
            'sigils_reinforced': 0,
            'activation_reinforcements': 0,
            'emotional_reinforcements': 0,
            'dual_reinforcements': 0,
            'total_saturation_added': 0.0,
            'total_ttl_extended': 0
        }
        
        reinforced_sigils = []
        skipped_sigils = []
        
        # Process each sigil
        for sigil in active_sigils:
            sigil_id = sigil['sigil_id']
            
            # Check reinforcement criteria
            should_reinforce, reason = self._check_reinforcement_criteria(sigil)
            
            if should_reinforce:
                # Apply reinforcement
                reinforced_sigil = self._apply_reinforcement(sigil, reason, current_tick)
                reinforced_sigils.append(sigil_id)
                
                # Update statistics
                self._update_statistics(reason)
            else:
                skipped_sigils.append(sigil_id)
        
        return {
            'reinforced_sigils': reinforced_sigils,
            'skipped': skipped_sigils
        }


def track_and_reinforce_sigils(active_sigils: List[Dict], current_tick: int) -> Dict:
    """
    Track and reinforce sigils based on usage patterns and emotional intensity.
    
    This function identifies sigils that have gained power through repetition
    or emotional charge, granting them extended life and increased saturation.
    
    Args:
        active_sigils: List of sigil dictionaries with:
            - sigil_id: str
            - activation_count: int
            - saturation: float (0.0 to 1.0)
            - emotional_pressure: float (0.0 to 1.0)
            - last_used_tick: int
        current_tick: Current system tick
        
    Returns:
        Dictionary containing:
            - reinforced_sigils: List of sigil_ids that were reinforced
            - skipped: List of sigil_ids that were not reinforced
    """
    # Create tracker instance
    tracker = SigilReinforcementTracker()
    
    # Process sigils for reinforcement
    results = tracker.reinforce_sigils(active_sigils, current_tick)
    
    # Save reinforcement log
    tracker._save_reinforcement_log(results, current_tick)
    
    # Add metadata to results
    results['metadata'] = {
        'tick': current_tick,
        'statistics': tracker.reinforcement_stats,
        'thresholds': {
            'activation': tracker.activation_threshold,
            'emotional': tracker.emotional_threshold
        },
        'reinforcement_values': {
            'saturation_boost': tracker.saturation_boost,
            'ttl_extension': tracker.ttl_extension
        }
    }
    
    return results


# Example usage and testing
if __name__ == "__main__":
    # Create sample sigil data
    sample_sigils = [
        {
            "sigil_id": "sigil_trust_001",
            "activation_count": 15,  # Above threshold
            "saturation": 0.6,
            "emotional_pressure": 0.8,  # Above threshold
            "last_used_tick": 950,
            "ttl": 1200
        },
        {
            "sigil_id": "sigil_emerge_002",
            "activation_count": 5,  # Below threshold
            "saturation": 0.4,
            "emotional_pressure": 0.9,  # Above threshold
            "last_used_tick": 980
        },
        {
            "sigil_id": "sigil_remember_003",
            "activation_count": 12,  # Above threshold
            "saturation": 0.7,
            "emotional_pressure": 0.3,  # Below threshold
            "last_used_tick": 900
        },
        {
            "sigil_id": "sigil_flow_004",
            "activation_count": 3,  # Below both thresholds
            "saturation": 0.2,
            "emotional_pressure": 0.4,
            "last_used_tick": 800
        },
        {
            "sigil_id": "sigil_sacred_005",
            "activation_count": 25,  # Well above threshold
            "saturation": 0.85,
            "emotional_pressure": 0.95,  # Well above threshold
            "last_used_tick": 999  # Recent use
        }
    ]
    
    # Track and reinforce sigils
    current_tick = 1000
    results = track_and_reinforce_sigils(sample_sigils, current_tick)
    
    # Display results
    print("SIGIL REINFORCEMENT RESULTS:")
    print("=" * 50)
    print(f"\nReinforced Sigils ({len(results['reinforced_sigils'])}):")
    for sigil_id in results['reinforced_sigils']:
        # Find the sigil to show its reinforcement data
        sigil = next(s for s in sample_sigils if s['sigil_id'] == sigil_id)
        if 'reinforcement_data' in sigil:
            data = sigil['reinforcement_data']
            print(f"  - {sigil_id}: {data['reason']} "
                  f"(+{data['saturation_gained']} sat, +{data['ttl_gained']} ttl)")
    
    print(f"\nSkipped Sigils ({len(results['skipped'])}):")
    for sigil_id in results['skipped']:
        print(f"  - {sigil_id}")
    
    print(f"\nStatistics: {results['metadata']['statistics']}")