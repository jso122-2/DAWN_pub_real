#!/usr/bin/env python3
"""
DAWN Rebloom Depth Statistics v1.0
═══════════════════════════════════════

Some thoughts echo once and die. 
Others become forests — with roots deeper than memory.

Calculates and tracks rebloom lineage depth and propagation statistics
per semantic seed, revealing which concepts evolve into deep forests
and which remain surface echoes.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from collections import defaultdict
import math


class RebloomDepthAnalyzer:
    """
    Analyzes rebloom lineage depth and propagation patterns across semantic seeds.
    
    Tracks memory continuity, evolution depth, and stagnation patterns
    to identify which conceptual seeds grow into forests of meaning.
    """
    
    def __init__(self, output_path: str = "memory/blooms/entropy_logs"):
        """
        Initialize the rebloom depth analyzer.
        
        Args:
            output_path: Directory for output files
        """
        self.output_path = Path(output_path)
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Analysis thresholds
        self.high_depth_threshold = 5
        self.low_stagnation_threshold = 1.2
        
        # Statistics tracking
        self.analysis_stats = {
            'total_seeds_analyzed': 0,
            'high_evolution_seeds': 0,
            'stagnant_seeds': 0,
            'deepest_lineage': 0,
            'most_rebloomed_seed': None
        }
    
    def _calculate_stagnation_ratio(self, rebloom_count: int, lineage_depth: int) -> float:
        """
        Calculate stagnation ratio for a bloom set.
        
        Stagnation ratio = rebloom_count / lineage_depth
        Higher ratio means more reblooms relative to depth (healthy evolution)
        Lower ratio means deep lineage with few reblooms (potentially stagnant)
        
        Args:
            rebloom_count: Total number of reblooms
            lineage_depth: Maximum lineage depth
            
        Returns:
            Stagnation ratio (protected against division by zero)
        """
        if lineage_depth == 0:
            return 0.0
        
        return round(rebloom_count / lineage_depth, 3)
    
    def _calculate_evolution_score(self, 
                                 max_depth: int, 
                                 avg_depth: float,
                                 total_reblooms: int,
                                 stagnation_ratio: float) -> float:
        """
        Calculate overall evolution score for a semantic seed.
        
        Combines multiple factors to assess the evolutionary health
        and complexity of a memory branch.
        
        Args:
            max_depth: Maximum lineage depth
            avg_depth: Average lineage depth
            total_reblooms: Total rebloom count
            stagnation_ratio: Calculated stagnation ratio
            
        Returns:
            Evolution score between 0.0 and 1.0
        """
        # Normalize components
        depth_score = min(max_depth / 10.0, 1.0)  # Cap at depth 10
        avg_depth_score = min(avg_depth / 5.0, 1.0)  # Cap at avg 5
        rebloom_score = min(total_reblooms / 20.0, 1.0)  # Cap at 20 reblooms
        
        # Invert stagnation for scoring (lower stagnation = higher score)
        stagnation_score = 1.0 / (1.0 + stagnation_ratio)
        
        # Weighted combination
        evolution_score = (
            0.3 * depth_score +
            0.2 * avg_depth_score +
            0.3 * rebloom_score +
            0.2 * stagnation_score
        )
        
        return round(evolution_score, 4)
    
    def _group_blooms_by_seed(self, all_blooms: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group blooms by their semantic seed.
        
        Args:
            all_blooms: List of all bloom dictionaries
            
        Returns:
            Dictionary mapping semantic seeds to their bloom lists
        """
        seed_groups = defaultdict(list)
        
        for bloom in all_blooms:
            seed = bloom.get('semantic_seed', 'unknown')
            seed_groups[seed].append(bloom)
        
        return dict(seed_groups)
    
    def _analyze_seed_blooms(self, seed_blooms: List[Dict]) -> Dict:
        """
        Analyze blooms for a single semantic seed.
        
        Args:
            seed_blooms: List of blooms for one semantic seed
            
        Returns:
            Dictionary of calculated statistics
        """
        if not seed_blooms:
            return {
                'max_depth': 0,
                'avg_depth': 0.0,
                'total_reblooms': 0,
                'stagnation_ratio': 0.0,
                'evolution_score': 0.0,
                'bloom_count': 0
            }
        
        # Extract metrics
        depths = [bloom.get('lineage_depth', 0) for bloom in seed_blooms]
        rebloom_counts = [bloom.get('rebloom_count', 0) for bloom in seed_blooms]
        
        # Calculate statistics
        max_depth = max(depths)
        avg_depth = sum(depths) / len(depths)
        total_reblooms = sum(rebloom_counts)
        
        # Calculate stagnation ratio
        stagnation_ratio = self._calculate_stagnation_ratio(total_reblooms, max_depth)
        
        # Calculate evolution score
        evolution_score = self._calculate_evolution_score(
            max_depth, avg_depth, total_reblooms, stagnation_ratio
        )
        
        # Track deepest lineage
        if max_depth > self.analysis_stats['deepest_lineage']:
            self.analysis_stats['deepest_lineage'] = max_depth
        
        return {
            'max_depth': max_depth,
            'avg_depth': round(avg_depth, 2),
            'total_reblooms': total_reblooms,
            'stagnation_ratio': stagnation_ratio,
            'evolution_score': evolution_score,
            'bloom_count': len(seed_blooms),
            'unique_parents': len(set(
                parent 
                for bloom in seed_blooms 
                for parent in bloom.get('parent_ids', [])
            ))
        }
    
    def _identify_high_value_evolution(self, seed_stats: Dict) -> bool:
        """
        Identify if a seed represents high-value evolution.
        
        Criteria:
        - max_depth > 5 (deep lineage)
        - stagnation_ratio < 1.2 (not stagnant)
        
        Args:
            seed_stats: Statistics for a semantic seed
            
        Returns:
            True if seed shows high-value evolution
        """
        return (
            seed_stats['max_depth'] > self.high_depth_threshold and
            seed_stats['stagnation_ratio'] < self.low_stagnation_threshold
        )
    
    def _save_lifecycle_data(self, results: Dict):
        """
        Save bloom lifecycle data to JSON file.
        
        Args:
            results: Analysis results dictionary
        """
        filepath = self.output_path / "bloom_lifecycle.json"
        
        # Add metadata
        results['metadata'] = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'analysis_stats': self.analysis_stats,
            'thresholds': {
                'high_depth': self.high_depth_threshold,
                'low_stagnation': self.low_stagnation_threshold
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filepath
    
    def analyze_rebloom_depths(self, all_blooms: List[Dict]) -> Dict:
        """
        Analyze rebloom depth statistics for all blooms.
        
        Args:
            all_blooms: List of all bloom dictionaries
            
        Returns:
            Dictionary with rebloom depth statistics by seed
        """
        # Reset statistics
        self.analysis_stats = {
            'total_seeds_analyzed': 0,
            'high_evolution_seeds': 0,
            'stagnant_seeds': 0,
            'deepest_lineage': 0,
            'most_rebloomed_seed': None,
            'most_reblooms': 0
        }
        
        # Group blooms by seed
        seed_groups = self._group_blooms_by_seed(all_blooms)
        self.analysis_stats['total_seeds_analyzed'] = len(seed_groups)
        
        # Analyze each seed
        rebloom_depth_by_seed = {}
        
        for seed, blooms in seed_groups.items():
            # Calculate statistics
            seed_stats = self._analyze_seed_blooms(blooms)
            
            # Check for high-value evolution
            if self._identify_high_value_evolution(seed_stats):
                seed_stats['high_value_evolution'] = True
                self.analysis_stats['high_evolution_seeds'] += 1
            else:
                seed_stats['high_value_evolution'] = False
            
            # Check for stagnation
            if seed_stats['stagnation_ratio'] > 2.0:
                self.analysis_stats['stagnant_seeds'] += 1
            
            # Track most rebloomed seed
            if seed_stats['total_reblooms'] > self.analysis_stats['most_reblooms']:
                self.analysis_stats['most_reblooms'] = seed_stats['total_reblooms']
                self.analysis_stats['most_rebloomed_seed'] = seed
            
            rebloom_depth_by_seed[seed] = seed_stats
        
        return {'rebloom_depth_by_seed': rebloom_depth_by_seed}


def calculate_rebloom_depth_stats(all_blooms: List[Dict]) -> Dict:
    """
    Calculate and log rebloom lineage depth and propagation statistics.
    
    This function analyzes the evolutionary patterns of semantic seeds,
    identifying which concepts have grown into deep forests of meaning
    and which remain surface-level echoes.
    
    Args:
        all_blooms: List of bloom dictionaries with:
            - bloom_id: str
            - parent_ids: list of str
            - lineage_depth: int
            - rebloom_count: int
            - semantic_seed: str
            
    Returns:
        Dictionary containing:
            - rebloom_depth_by_seed: Statistics for each semantic seed
    """
    # Create analyzer instance
    analyzer = RebloomDepthAnalyzer()
    
    # Perform analysis
    results = analyzer.analyze_rebloom_depths(all_blooms)
    
    # Save to file
    analyzer._save_lifecycle_data(results)
    
    return results


# Example usage and testing
if __name__ == "__main__":
    # Create sample bloom data
    sample_blooms = [
        # Trust seed 42 - deep evolution
        {
            "bloom_id": "bloom_001",
            "parent_ids": [],
            "lineage_depth": 0,
            "rebloom_count": 0,
            "semantic_seed": "trust_seed_42"
        },
        {
            "bloom_id": "bloom_002",
            "parent_ids": ["bloom_001"],
            "lineage_depth": 1,
            "rebloom_count": 1,
            "semantic_seed": "trust_seed_42"
        },
        {
            "bloom_id": "bloom_003",
            "parent_ids": ["bloom_002"],
            "lineage_depth": 2,
            "rebloom_count": 1,
            "semantic_seed": "trust_seed_42"
        },
        {
            "bloom_id": "bloom_004",
            "parent_ids": ["bloom_002", "bloom_003"],
            "lineage_depth": 3,
            "rebloom_count": 2,
            "semantic_seed": "trust_seed_42"
        },
        {
            "bloom_id": "bloom_005",
            "parent_ids": ["bloom_004"],
            "lineage_depth": 4,
            "rebloom_count": 1,
            "semantic_seed": "trust_seed_42"
        },
        {
            "bloom_id": "bloom_006",
            "parent_ids": ["bloom_005"],
            "lineage_depth": 5,
            "rebloom_count": 1,
            "semantic_seed": "trust_seed_42"
        },
        {
            "bloom_id": "bloom_007",
            "parent_ids": ["bloom_006"],
            "lineage_depth": 6,
            "rebloom_count": 1,
            "semantic_seed": "trust_seed_42"
        },
        # Emergence 17 - shallow, high rebloom
        {
            "bloom_id": "bloom_101",
            "parent_ids": [],
            "lineage_depth": 0,
            "rebloom_count": 0,
            "semantic_seed": "emergence_17"
        },
        {
            "bloom_id": "bloom_102",
            "parent_ids": ["bloom_101"],
            "lineage_depth": 1,
            "rebloom_count": 5,
            "semantic_seed": "emergence_17"
        },
        {
            "bloom_id": "bloom_103",
            "parent_ids": ["bloom_101"],
            "lineage_depth": 1,
            "rebloom_count": 3,
            "semantic_seed": "emergence_17"
        },
        # Sacred memory - single bloom
        {
            "bloom_id": "bloom_201",
            "parent_ids": [],
            "lineage_depth": 0,
            "rebloom_count": 0,
            "semantic_seed": "sacred_memory_1"
        }
    ]
    
    # Calculate statistics
    results = calculate_rebloom_depth_stats(sample_blooms)
    
    # Display results
    print("REBLOOM DEPTH STATISTICS:")
    print("=" * 50)
    
    for seed, stats in results['rebloom_depth_by_seed'].items():
        print(f"\n{seed}:")
        print(f"  Max Depth: {stats['max_depth']}")
        print(f"  Avg Depth: {stats['avg_depth']}")
        print(f"  Total Reblooms: {stats['total_reblooms']}")
        print(f"  Stagnation Ratio: {stats['stagnation_ratio']}")
        print(f"  Evolution Score: {stats['evolution_score']}")
        print(f"  High-Value Evolution: {'YES' if stats['high_value_evolution'] else 'NO'}")
    
    if 'metadata' in results:
        print(f"\nAnalysis Summary: {results['metadata']['analysis_stats']}")