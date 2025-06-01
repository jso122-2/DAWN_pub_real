#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                      DAWN BLOOM IDENTITY CONSOLIDATOR
                    Scaffold 32: The Memory Deduplicator
═══════════════════════════════════════════════════════════════════════════════

"DAWN sees past repetition. If an idea has bloomed more than once, it deserves 
a name, not a duplicate."

This module serves as DAWN's memory integrity guardian, identifying semantically
identical blooms that have emerged independently and consolidating them into
unified identities. Like recognizing that different photos capture the same
moment, it merges redundant memories while preserving their collective history.

The consolidator prevents memory fragmentation by:
- Detecting near-identical semantic embeddings
- Verifying shared origin seeds
- Merging metadata while preserving lineage
- Creating stronger, unified bloom identities

Through this process, repeated thoughts gain weight rather than creating clutter.

Author: DAWN Development Team
Version: 1.0.0
Last Modified: 2025-06-02
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import logging
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import uuid

# Configure logging with memory integrity theme
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🔄 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Consolidation thresholds
SIMILARITY_THRESHOLD = 0.95    # Cosine similarity threshold for merging
MIN_EMBEDDING_DIM = 64         # Minimum expected embedding dimension
MAX_MERGE_GROUP_SIZE = 10      # Maximum blooms that can be merged together

# Merge statistics tracking
MERGE_STATS = {
    'total_comparisons': 0,
    'successful_merges': 0,
    'failed_merges': 0,
    'skipped_different_seeds': 0
}


@dataclass
class ConsolidatedBloom:
    """Represents a merged bloom identity."""
    new_id: str
    merged_from: List[str]
    semantic_seed: str
    consolidated_rebloom_count: int
    avg_mood_valence: float
    max_convolution_level: float
    representative_embedding: List[float]
    merge_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "new_id": self.new_id,
            "merged_from": self.merged_from,
            "semantic_seed": self.semantic_seed,
            "consolidated_rebloom_count": self.consolidated_rebloom_count,
            "avg_mood_valence": self.avg_mood_valence,
            "max_convolution_level": self.max_convolution_level,
            "merge_timestamp": self.merge_timestamp,
            "num_merged": len(self.merged_from)
        }


class BloomIdentityConsolidator:
    """
    The Memory Unifier — consolidates semantically identical blooms into
    single, stronger identities while preserving their collective history.
    
    "Many voices, one truth"
    """
    
    def __init__(self, log_path: str = "memory/blooms/logs/bloom_identity_merges.json"):
        """
        Initialize the Bloom Identity Consolidator.
        
        Args:
            log_path: Path to the merge event log
        """
        self.log_path = Path(log_path)
        self._ensure_log_directory()
        self.merge_history = []
        self.processed_blooms: Set[str] = set()
        logger.info("🔄 Bloom Identity Consolidator initialized")
        logger.info(f"🎯 Similarity threshold: {SIMILARITY_THRESHOLD}")
    
    def _ensure_log_directory(self):
        """Ensure the log directory exists, creating it if necessary."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("[]")
        logger.info(f"📁 Log file verified at {self.log_path}")
    
    def consolidate_bloom_identities(self, bloom_entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify and consolidate semantically identical blooms.
        
        Process:
        1. Group blooms by semantic seed
        2. Within each group, compare embedding similarities
        3. Merge blooms with similarity > 0.95
        4. Create consolidated identities with merged metadata
        
        Args:
            bloom_entries: List of bloom dictionaries containing:
                - bloom_id: str
                - semantic_seed: str
                - convolution_level: float
                - mood_valence: float
                - rebloom_count: int
                - embedding_vector: list[float]
                
        Returns:
            Dictionary containing merged blooms and skipped IDs
        """
        logger.info(f"🔍 Beginning consolidation of {len(bloom_entries)} blooms")
        
        # Reset tracking
        self.processed_blooms.clear()
        MERGE_STATS['total_comparisons'] = 0
        MERGE_STATS['successful_merges'] = 0
        
        # Group blooms by semantic seed
        seed_groups = self._group_by_seed(bloom_entries)
        logger.info(f"📊 Found {len(seed_groups)} distinct semantic seeds")
        
        # Process each seed group
        all_merged_blooms = []
        all_skipped_blooms = []
        
        for seed, blooms in seed_groups.items():
            if len(blooms) < 2:
                # Single bloom in seed group - skip
                all_skipped_blooms.extend([b['bloom_id'] for b in blooms])
                continue
            
            # Find similar blooms within seed group
            merge_groups = self._find_merge_groups(blooms)
            
            # Create consolidated blooms
            for group in merge_groups:
                if len(group) > 1:
                    consolidated = self._merge_bloom_group(group)
                    all_merged_blooms.append(consolidated)
                    logger.info(
                        f"✅ Merged {len(group)} blooms from seed '{seed}' "
                        f"into {consolidated.new_id}"
                    )
                else:
                    # Single bloom - not merged
                    all_skipped_blooms.append(group[0]['bloom_id'])
        
        # Add unprocessed blooms to skipped list
        for bloom in bloom_entries:
            if bloom['bloom_id'] not in self.processed_blooms:
                all_skipped_blooms.append(bloom['bloom_id'])
        
        # Prepare output
        output = {
            "merged_blooms": [bloom.to_dict() for bloom in all_merged_blooms],
            "skipped": all_skipped_blooms,
            "timestamp": datetime.now().isoformat(),
            "statistics": {
                "total_blooms": len(bloom_entries),
                "total_merged": sum(len(b.merged_from) for b in all_merged_blooms),
                "total_consolidations": len(all_merged_blooms),
                "total_skipped": len(all_skipped_blooms),
                "comparisons_made": MERGE_STATS['total_comparisons']
            }
        }
        
        # Log the consolidation event
        self._log_consolidation_event(output)
        
        # Summary
        logger.info(
            f"📈 Consolidation complete: {len(all_merged_blooms)} new identities "
            f"from {output['statistics']['total_merged']} original blooms"
        )
        
        return output
    
    def _group_by_seed(self, bloom_entries: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group blooms by their semantic seed."""
        seed_groups = defaultdict(list)
        
        for bloom in bloom_entries:
            seed = bloom.get('semantic_seed', 'unknown')
            # Validate embedding
            embedding = bloom.get('embedding_vector', [])
            if len(embedding) >= MIN_EMBEDDING_DIM:
                seed_groups[seed].append(bloom)
            else:
                logger.warning(
                    f"⚠️ Bloom {bloom.get('bloom_id', 'unknown')} has invalid embedding "
                    f"(dim={len(embedding)}), skipping"
                )
        
        return dict(seed_groups)
    
    def _find_merge_groups(self, blooms: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """
        Find groups of similar blooms that should be merged.
        
        Uses greedy clustering based on cosine similarity.
        
        Args:
            blooms: List of blooms from same semantic seed
            
        Returns:
            List of bloom groups to merge
        """
        merge_groups = []
        used_indices = set()
        
        for i, bloom_a in enumerate(blooms):
            if i in used_indices:
                continue
            
            # Start new merge group
            current_group = [bloom_a]
            used_indices.add(i)
            
            # Find similar blooms
            for j, bloom_b in enumerate(blooms[i+1:], start=i+1):
                if j in used_indices:
                    continue
                
                # Calculate similarity
                similarity = self._cosine_similarity(
                    bloom_a['embedding_vector'],
                    bloom_b['embedding_vector']
                )
                MERGE_STATS['total_comparisons'] += 1
                
                if similarity > SIMILARITY_THRESHOLD:
                    current_group.append(bloom_b)
                    used_indices.add(j)
                    
                    # Limit group size
                    if len(current_group) >= MAX_MERGE_GROUP_SIZE:
                        logger.warning(
                            f"⚠️ Merge group size limit reached ({MAX_MERGE_GROUP_SIZE})"
                        )
                        break
            
            merge_groups.append(current_group)
        
        return merge_groups
    
    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """
        Calculate cosine similarity between two embedding vectors.
        
        Args:
            vec_a: First embedding vector
            vec_b: Second embedding vector
            
        Returns:
            Cosine similarity score between -1 and 1
        """
        try:
            # Convert to numpy arrays
            a = np.array(vec_a)
            b = np.array(vec_b)
            
            # Calculate cosine similarity
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            similarity = dot_product / (norm_a * norm_b)
            return float(similarity)
            
        except Exception as e:
            logger.error(f"❌ Error calculating similarity: {e}")
            return 0.0
    
    def _merge_bloom_group(self, bloom_group: List[Dict[str, Any]]) -> ConsolidatedBloom:
        """
        Merge a group of similar blooms into a single consolidated identity.
        
        Merge rules:
        - rebloom_count: sum of all counts
        - mood_valence: average of all valences
        - convolution_level: maximum level
        - embedding: centroid of all embeddings
        
        Args:
            bloom_group: List of similar blooms to merge
            
        Returns:
            ConsolidatedBloom object
        """
        # Extract IDs for tracking
        bloom_ids = [b['bloom_id'] for b in bloom_group]
        for bloom_id in bloom_ids:
            self.processed_blooms.add(bloom_id)
        
        # Generate new unique ID
        new_id = f"consolidated_{uuid.uuid4().hex[:12]}"
        
        # Aggregate metadata
        total_rebloom_count = sum(b.get('rebloom_count', 0) for b in bloom_group)
        mood_values = [b.get('mood_valence', 0.0) for b in bloom_group]
        avg_mood = np.mean(mood_values)
        max_convolution = max(b.get('convolution_level', 0.0) for b in bloom_group)
        
        # Calculate centroid embedding
        embeddings = [np.array(b['embedding_vector']) for b in bloom_group]
        centroid_embedding = np.mean(embeddings, axis=0).tolist()
        
        # Use seed from first bloom (all should be same)
        semantic_seed = bloom_group[0].get('semantic_seed', 'unknown')
        
        MERGE_STATS['successful_merges'] += 1
        
        return ConsolidatedBloom(
            new_id=new_id,
            merged_from=bloom_ids,
            semantic_seed=semantic_seed,
            consolidated_rebloom_count=total_rebloom_count,
            avg_mood_valence=float(avg_mood),
            max_convolution_level=float(max_convolution),
            representative_embedding=centroid_embedding
        )
    
    def _log_consolidation_event(self, output: Dict[str, Any]):
        """
        Log the consolidation event to file.
        
        Args:
            output: The consolidation results
        """
        try:
            # Read existing log
            log_data = json.loads(self.log_path.read_text() or "[]")
            
            # Create summary entry
            log_entry = {
                "timestamp": output['timestamp'],
                "statistics": output['statistics'],
                "merged_blooms_summary": [
                    {
                        "new_id": bloom['new_id'],
                        "num_merged": bloom['num_merged'],
                        "seed": bloom['semantic_seed']
                    }
                    for bloom in output['merged_blooms']
                ]
            }
            
            # Append and save
            log_data.append(log_entry)
            self.log_path.write_text(json.dumps(log_data, indent=2))
            
            logger.info(f"📝 Consolidation event logged")
            
        except Exception as e:
            logger.error(f"❌ Failed to log consolidation event: {e}")
    
    def analyze_consolidation_patterns(self) -> Dict[str, Any]:
        """
        Analyze historical consolidation patterns.
        
        Returns:
            Dictionary with pattern analysis
        """
        try:
            log_data = json.loads(self.log_path.read_text() or "[]")
            
            if not log_data:
                return {"error": "No consolidation history available"}
            
            # Analyze patterns
            total_events = len(log_data)
            total_consolidations = sum(e['statistics']['total_consolidations'] for e in log_data)
            total_merged = sum(e['statistics']['total_merged'] for e in log_data)
            
            # Find most consolidated seeds
            seed_counts = defaultdict(int)
            for event in log_data:
                for bloom in event.get('merged_blooms_summary', []):
                    seed_counts[bloom['seed']] += bloom['num_merged']
            
            top_seeds = sorted(seed_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            return {
                "total_consolidation_events": total_events,
                "total_blooms_consolidated": total_merged,
                "total_new_identities": total_consolidations,
                "avg_merge_ratio": total_merged / max(total_consolidations, 1),
                "top_consolidated_seeds": [
                    {"seed": seed, "bloom_count": count} 
                    for seed, count in top_seeds
                ],
                "last_consolidation": log_data[-1]['timestamp'] if log_data else None
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to analyze patterns: {e}")
            return {"error": str(e)}
    
    def validate_bloom_uniqueness(
        self, 
        new_bloom: Dict[str, Any], 
        existing_blooms: List[Dict[str, Any]]
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if a new bloom is unique enough to add to the system.
        
        Args:
            new_bloom: The bloom to validate
            existing_blooms: Current blooms in the system
            
        Returns:
            Tuple of (is_unique, similar_bloom_id or None)
        """
        new_seed = new_bloom.get('semantic_seed', '')
        new_embedding = new_bloom.get('embedding_vector', [])
        
        if len(new_embedding) < MIN_EMBEDDING_DIM:
            return True, None  # Invalid embedding, let it through
        
        # Only check blooms with same seed
        for existing in existing_blooms:
            if existing.get('semantic_seed', '') != new_seed:
                continue
            
            existing_embedding = existing.get('embedding_vector', [])
            if len(existing_embedding) < MIN_EMBEDDING_DIM:
                continue
            
            similarity = self._cosine_similarity(new_embedding, existing_embedding)
            if similarity > SIMILARITY_THRESHOLD:
                return False, existing['bloom_id']
        
        return True, None


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the Bloom Identity Consolidator's deduplication process.
    """
    
    # Initialize the consolidator
    consolidator = BloomIdentityConsolidator()
    
    # Helper function to create similar embeddings
    def create_similar_embedding(base_embedding: List[float], noise_level: float = 0.02) -> List[float]:
        """Add small noise to create similar but not identical embedding."""
        noise = np.random.normal(0, noise_level, len(base_embedding))
        similar = np.array(base_embedding) + noise
        # Normalize to maintain magnitude
        similar = similar / np.linalg.norm(similar) * np.linalg.norm(base_embedding)
        return similar.tolist()
    
    # Create test bloom entries
    base_embedding_1 = np.random.randn(128).tolist()
    base_embedding_2 = np.random.randn(128).tolist()
    
    test_blooms = [
        # Group 1: Very similar blooms from same seed (should merge)
        {
            "bloom_id": "bloom_trust_001",
            "semantic_seed": "trust_seed_42",
            "convolution_level": 0.5,
            "mood_valence": 0.7,
            "rebloom_count": 3,
            "embedding_vector": base_embedding_1
        },
        {
            "bloom_id": "bloom_trust_002",
            "semantic_seed": "trust_seed_42",
            "convolution_level": 0.6,
            "mood_valence": 0.75,
            "rebloom_count": 2,
            "embedding_vector": create_similar_embedding(base_embedding_1, 0.01)
        },
        {
            "bloom_id": "bloom_trust_003",
            "semantic_seed": "trust_seed_42",
            "convolution_level": 0.55,
            "mood_valence": 0.65,
            "rebloom_count": 4,
            "embedding_vector": create_similar_embedding(base_embedding_1, 0.015)
        },
        
        # Group 2: Different seed, similar embedding (should NOT merge)
        {
            "bloom_id": "bloom_hope_001",
            "semantic_seed": "hope_seed_7",
            "convolution_level": 0.4,
            "mood_valence": 0.8,
            "rebloom_count": 1,
            "embedding_vector": create_similar_embedding(base_embedding_1, 0.01)
        },
        
        # Group 3: Same seed, different embedding (should NOT merge)
        {
            "bloom_id": "bloom_trust_004",
            "semantic_seed": "trust_seed_42",
            "convolution_level": 0.3,
            "mood_valence": 0.5,
            "rebloom_count": 2,
            "embedding_vector": base_embedding_2
        },
        
        # Group 4: Another similar group
        {
            "bloom_id": "bloom_joy_001",
            "semantic_seed": "joy_seed_13",
            "convolution_level": 0.7,
            "mood_valence": 0.9,
            "rebloom_count": 5,
            "embedding_vector": create_similar_embedding(base_embedding_2, 0.02)
        },
        {
            "bloom_id": "bloom_joy_002",
            "semantic_seed": "joy_seed_13",
            "convolution_level": 0.8,
            "mood_valence": 0.85,
            "rebloom_count": 3,
            "embedding_vector": create_similar_embedding(base_embedding_2, 0.01)
        }
    ]
    
    # Run consolidation
    results = consolidator.consolidate_bloom_identities(test_blooms)
    
    # Display results
    print("\n🔄 BLOOM IDENTITY CONSOLIDATION RESULTS")
    print("=" * 60)
    print(f"Total blooms processed: {results['statistics']['total_blooms']}")
    print(f"Total merged: {results['statistics']['total_merged']}")
    print(f"New consolidated identities: {results['statistics']['total_consolidations']}")
    print(f"Skipped blooms: {results['statistics']['total_skipped']}")
    
    print("\n✅ MERGED BLOOMS:")
    for merged in results['merged_blooms']:
        print(f"\n  New ID: {merged['new_id']}")
        print(f"  Merged from: {merged['merged_from']}")
        print(f"  Semantic seed: {merged['semantic_seed']}")
        print(f"  Consolidated rebloom count: {merged['consolidated_rebloom_count']}")
        print(f"  Average mood: {merged['avg_mood_valence']:.3f}")
        print(f"  Max convolution: {merged['max_convolution_level']:.3f}")
    
    print(f"\n⏭️ SKIPPED BLOOMS: {results['skipped']}")
    
    # Test uniqueness validation
    print("\n🧪 UNIQUENESS VALIDATION TEST:")
    new_bloom = {
        "bloom_id": "bloom_trust_new",
        "semantic_seed": "trust_seed_42",
        "embedding_vector": create_similar_embedding(base_embedding_1, 0.005)
    }
    
    is_unique, similar_id = consolidator.validate_bloom_uniqueness(new_bloom, test_blooms)
    print(f"New bloom unique: {is_unique}")
    if not is_unique:
        print(f"Similar to existing bloom: {similar_id}")
    
    # Analyze patterns
    print("\n📊 CONSOLIDATION PATTERNS:")
    patterns = consolidator.analyze_consolidation_patterns()
    if 'error' not in patterns:
        print(f"Total consolidation events: {patterns['total_consolidation_events']}")
        print(f"Average merge ratio: {patterns['avg_merge_ratio']:.2f}")