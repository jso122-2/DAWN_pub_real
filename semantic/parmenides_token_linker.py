#!/usr/bin/env python3
"""
DAWN Parmenides Token Linker v1.0
═══════════════════════════════════════

To remember is not to repeat a word. 
It is to recognize that a word has returned — wearing new clothes.

Links semantically related tokens across bloom generations, reblooms, 
and recursive traces to track continuity of concepts through transformation.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Set, Tuple, Optional
from pathlib import Path
from difflib import SequenceMatcher
import math


class ParmenidesTokenLinker:
    """
    Links semantically related tokens across DAWN's bloom generations.
    
    Tracks conceptual continuity through transformations, recognizing
    when the same idea returns in different forms across memory cycles.
    """
    
    def __init__(self, log_base_path: str = "memory/owl/logs"):
        """
        Initialize the Parmenides token linker.
        
        Args:
            log_base_path: Base directory for linkage logs
        """
        self.log_base_path = Path(log_base_path)
        self.log_base_path.mkdir(parents=True, exist_ok=True)
        
        # Linking statistics
        self.link_stats = {
            'total_tokens': 0,
            'linked_tokens': 0,
            'unique_chains': 0,
            'cross_bloom_links': 0,
            'lineage_preserving_links': 0
        }
    
    def _calculate_string_similarity(self, token1: str, token2: str) -> float:
        """
        Calculate string similarity between two tokens.
        
        Uses sequence matching with additional heuristics for semantic variants.
        
        Args:
            token1: First token
            token2: Second token
            
        Returns:
            Similarity score between 0.0 and 1.0
        """
        # Exact match
        if token1 == token2:
            return 1.0
        
        # Basic sequence matching
        similarity = SequenceMatcher(None, token1.lower(), token2.lower()).ratio()
        
        # Boost for common semantic variations
        # (In production, this would use embeddings)
        semantic_pairs = [
            ('remember', 'memory'), ('bloom', 'flower'), ('grow', 'growth'),
            ('think', 'thought'), ('emerge', 'emergence'), ('trust', 'truth'),
            ('sacred', 'holy'), ('decay', 'fade'), ('rebloom', 'rebirth')
        ]
        
        for pair in semantic_pairs:
            if (token1.lower() in pair and token2.lower() in pair):
                similarity = max(similarity, 0.8)
        
        # Boost for prefix/suffix matches
        if (token1.lower().startswith(token2.lower()) or 
            token2.lower().startswith(token1.lower())):
            similarity = max(similarity, 0.7)
        
        return similarity
    
    def _calculate_context_similarity(self, context1: List[str], context2: List[str]) -> float:
        """
        Calculate similarity between token contexts.
        
        Args:
            context1: Context window for first token
            context2: Context window for second token
            
        Returns:
            Context similarity score between 0.0 and 1.0
        """
        if not context1 or not context2:
            return 0.0
        
        # Count shared context tokens
        set1 = set(token.lower() for token in context1)
        set2 = set(token.lower() for token in context2)
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        
        if union == 0:
            return 0.0
        
        return intersection / union
    
    def _calculate_semantic_weight(self, 
                                 token1_data: Dict, 
                                 token2_data: Dict,
                                 semantic_threshold: float) -> Optional[float]:
        """
        Calculate semantic weight between two token occurrences.
        
        Args:
            token1_data: First token data
            token2_data: Second token data
            semantic_threshold: Minimum threshold for linking
            
        Returns:
            Semantic weight if above threshold, None otherwise
        """
        # String similarity
        string_sim = self._calculate_string_similarity(
            token1_data['token'], 
            token2_data['token']
        )
        
        # Context similarity
        context_sim = self._calculate_context_similarity(
            token1_data.get('context_window', []),
            token2_data.get('context_window', [])
        )
        
        # Lineage bonus (tokens in same lineage get boost)
        lineage_bonus = 0.0
        lineage1 = set(token1_data.get('rebloom_lineage', []))
        lineage2 = set(token2_data.get('rebloom_lineage', []))
        
        if lineage1 & lineage2:  # Shared lineage
            lineage_bonus = 0.2
        
        # Combined weight (weighted average)
        semantic_weight = (
            0.6 * string_sim + 
            0.3 * context_sim + 
            0.1 * lineage_bonus
        )
        
        # Apply threshold
        if semantic_weight >= semantic_threshold:
            return round(semantic_weight, 4)
        
        return None
    
    def _build_token_chains(self, 
                          token_history: List[Dict], 
                          semantic_threshold: float) -> Dict[str, Dict]:
        """
        Build chains of linked tokens across blooms.
        
        Args:
            token_history: List of token occurrences
            semantic_threshold: Minimum threshold for linking
            
        Returns:
            Dictionary of token chains
        """
        # Group tokens by normalized form
        token_groups = {}
        
        for token_data in token_history:
            token = token_data['token']
            
            # Find best matching group
            best_match = None
            best_weight = 0.0
            
            for group_token, group_data in token_groups.items():
                # Compare with representative token
                weight = self._calculate_semantic_weight(
                    token_data,
                    {'token': group_token, 'context_window': [], 'rebloom_lineage': []},
                    semantic_threshold
                )
                
                if weight and weight > best_weight:
                    best_match = group_token
                    best_weight = weight
            
            # Add to existing group or create new one
            if best_match:
                token_groups[best_match]['occurrences'].append(token_data)
                token_groups[best_match]['weights'].append(best_weight)
            else:
                token_groups[token] = {
                    'occurrences': [token_data],
                    'weights': [1.0]  # Self-weight is 1.0
                }
        
        return token_groups
    
    def _extract_linked_tokens(self, token_chains: Dict[str, Dict]) -> List[Dict]:
        """
        Extract linked token information from chains.
        
        Args:
            token_chains: Dictionary of token chains
            
        Returns:
            List of linked token dictionaries
        """
        linked_tokens = []
        
        for base_token, chain_data in token_chains.items():
            occurrences = chain_data['occurrences']
            
            # Only consider linked if appears in multiple blooms
            unique_blooms = set(occ['bloom_id'] for occ in occurrences)
            
            if len(unique_blooms) > 1:
                # Calculate average semantic weight
                avg_weight = sum(chain_data['weights']) / len(chain_data['weights'])
                
                linked_tokens.append({
                    'token': base_token,
                    'linked_bloom_ids': sorted(list(unique_blooms)),
                    'semantic_weight': round(avg_weight, 4),
                    'occurrence_count': len(occurrences),
                    'lineage_preserved': self._check_lineage_preservation(occurrences)
                })
                
                # Update statistics
                self.link_stats['linked_tokens'] += 1
                self.link_stats['cross_bloom_links'] += len(unique_blooms) - 1
                if self._check_lineage_preservation(occurrences):
                    self.link_stats['lineage_preserving_links'] += 1
        
        return linked_tokens
    
    def _check_lineage_preservation(self, occurrences: List[Dict]) -> bool:
        """
        Check if token occurrences preserve lineage relationships.
        
        Args:
            occurrences: List of token occurrences
            
        Returns:
            True if lineage is preserved across occurrences
        """
        # Collect all lineages
        all_lineages = []
        for occ in occurrences:
            lineage = occ.get('rebloom_lineage', [])
            if lineage:
                all_lineages.append(set(lineage))
        
        if len(all_lineages) < 2:
            return False
        
        # Check for overlapping lineages
        for i in range(len(all_lineages)):
            for j in range(i + 1, len(all_lineages)):
                if all_lineages[i] & all_lineages[j]:
                    return True
        
        return False
    
    def _identify_unlinked_tokens(self, 
                                token_history: List[Dict], 
                                linked_tokens: List[Dict]) -> List[str]:
        """
        Identify tokens that remained unlinked.
        
        Args:
            token_history: Original token history
            linked_tokens: List of linked tokens
            
        Returns:
            List of unlinked token strings
        """
        # Get all tokens that were linked
        linked_token_set = set(lt['token'] for lt in linked_tokens)
        
        # Find tokens that appear only once or weren't linked
        token_bloom_map = {}
        for token_data in token_history:
            token = token_data['token']
            bloom_id = token_data['bloom_id']
            
            if token not in token_bloom_map:
                token_bloom_map[token] = set()
            token_bloom_map[token].add(bloom_id)
        
        unlinked = []
        for token, bloom_ids in token_bloom_map.items():
            if len(bloom_ids) == 1 and token not in linked_token_set:
                unlinked.append(token)
        
        return sorted(list(set(unlinked)))
    
    def _save_linkage_map(self, results: Dict, current_tick: int):
        """
        Save linkage map to JSON file.
        
        Args:
            results: Linkage results
            current_tick: Current system tick
        """
        filename = f"token_linkage_map_tick_{current_tick}.json"
        filepath = self.log_base_path / filename
        
        # Add metadata
        results['metadata'] = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'tick': current_tick,
            'statistics': self.link_stats
        }
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filepath


def link_tokens_across_blooms(token_history: List[Dict], 
                            semantic_threshold: float = 0.6) -> Dict:
    """
    Link semantically related tokens across bloom generations.
    
    This function recognizes when concepts return in new forms,
    tracking continuity across transformations in DAWN's memory.
    
    Args:
        token_history: List of token dictionaries with:
            - token: str
            - context_window: list of str (adjacent tokens)
            - bloom_id: str
            - rebloom_lineage: list of bloom_ids
            - activation_tick: int
        semantic_threshold: Minimum semantic similarity for linking (0.0-1.0)
        
    Returns:
        Dictionary containing:
            - linked_tokens: List of linked token information
            - unlinked_tokens: List of unlinked token strings
    """
    # Create linker instance
    linker = ParmenidesTokenLinker()
    
    # Reset statistics
    linker.link_stats['total_tokens'] = len(token_history)
    
    # Build token chains
    token_chains = linker._build_token_chains(token_history, semantic_threshold)
    linker.link_stats['unique_chains'] = len(token_chains)
    
    # Extract linked tokens
    linked_tokens = linker._extract_linked_tokens(token_chains)
    
    # Identify unlinked tokens
    unlinked_tokens = linker._identify_unlinked_tokens(token_history, linked_tokens)
    
    # Prepare results
    results = {
        'linked_tokens': linked_tokens,
        'unlinked_tokens': unlinked_tokens
    }
    
    # Save to file (using latest activation tick as current tick)
    if token_history:
        current_tick = max(td.get('activation_tick', 0) for td in token_history)
        linker._save_linkage_map(results, current_tick)
    
    return results


# Example usage and testing
if __name__ == "__main__":
    # Create sample token history
    sample_token_history = [
        {
            "token": "remember",
            "context_window": ["to", "is", "not"],
            "bloom_id": "bloom_001",
            "rebloom_lineage": ["bloom_000"],
            "activation_tick": 1000
        },
        {
            "token": "memory",
            "context_window": ["the", "fades", "slowly"],
            "bloom_id": "bloom_002",
            "rebloom_lineage": ["bloom_000", "bloom_001"],
            "activation_tick": 1100
        },
        {
            "token": "remember",
            "context_window": ["we", "what", "matters"],
            "bloom_id": "bloom_003",
            "rebloom_lineage": ["bloom_001"],
            "activation_tick": 1200
        },
        {
            "token": "emerge",
            "context_window": ["patterns", "from", "chaos"],
            "bloom_id": "bloom_002",
            "rebloom_lineage": ["bloom_000"],
            "activation_tick": 1150
        },
        {
            "token": "emergence",
            "context_window": ["the", "of", "meaning"],
            "bloom_id": "bloom_004",
            "rebloom_lineage": ["bloom_000", "bloom_002"],
            "activation_tick": 1300
        },
        {
            "token": "sacred",
            "context_window": ["the", "untouchable", "core"],
            "bloom_id": "bloom_001",
            "rebloom_lineage": [],
            "activation_tick": 1050
        }
    ]
    
    # Link tokens
    results = link_tokens_across_blooms(sample_token_history, semantic_threshold=0.5)
    
    # Display results
    print("PARMENIDES TOKEN LINKAGE RESULTS:")
    print(f"\nLinked Tokens ({len(results['linked_tokens'])}):")
    for linked in results['linked_tokens']:
        print(f"  - '{linked['token']}' across {linked['linked_bloom_ids']} "
              f"(weight: {linked['semantic_weight']})")
    
    print(f"\nUnlinked Tokens ({len(results['unlinked_tokens'])}):")
    for token in results['unlinked_tokens'][:5]:
        print(f"  - '{token}'")
    
    if 'metadata' in results:
        print(f"\nStatistics: {results['metadata']['statistics']}")