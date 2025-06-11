#!/usr/bin/env python3
"""
DAWN Belief Anchor Manager v1.0
═══════════════════════════════════════

DAWN does not believe everything. But she does believe in what returns — 
again and again — with coherence and heat.

Defines, tracks, and assigns belief anchors to semantic structures that have
shown historical truth, emotional resonance, or structural necessity within
DAWN's epistemic framework.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from collections import defaultdict
import hashlib


class BeliefAnchorManager:
    """
    Manages the anchoring of beliefs based on historical usage, 
    emotional resonance, and structural coherence.
    
    Beliefs that persist with both logical coherence and emotional
    significance are granted anchor status in DAWN's epistemic layer.
    """
    
    def __init__(self, log_base_path: str = "memory/owl/logs"):
        """
        Initialize the belief anchor manager.
        
        Args:
            log_base_path: Base directory for belief anchor logs
        """
        self.log_base_path = Path(log_base_path)
        self.log_base_path.mkdir(parents=True, exist_ok=True)
        
        # Anchoring thresholds
        self.activation_threshold = 8
        self.resonance_threshold = 0.7
        self.coherence_threshold = 0.4
        
        # Tracking structures
        self.anchored_beliefs = {}  # belief_hash -> belief_data
        self.belief_history = defaultdict(list)  # belief_hash -> evaluation_history
        
        # Statistics
        self.anchor_stats = {
            'total_candidates_evaluated': 0,
            'beliefs_anchored': 0,
            'operator_origin_anchored': 0,
            'internal_origin_anchored': 0,
            'seed_origin_anchored': 0,
            'average_anchor_weight': 0.0,
            'strongest_belief': None,
            'highest_weight': 0.0
        }
    
    def _generate_belief_hash(self, statement: str) -> str:
        """
        Generate a unique hash for a belief statement.
        
        Args:
            statement: Belief statement text
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(statement.encode('utf-8')).hexdigest()[:16]
    
    def _check_anchoring_criteria(self, belief: Dict) -> Tuple[bool, List[str]]:
        """
        Check if a belief meets anchoring criteria.
        
        Args:
            belief: Candidate belief dictionary
            
        Returns:
            Tuple of (should_anchor, met_criteria)
        """
        met_criteria = []
        
        # Check activation count
        if belief['activation_count'] > self.activation_threshold:
            met_criteria.append('high_activation')
        
        # Check resonance
        if belief['resonance'] > self.resonance_threshold:
            met_criteria.append('strong_resonance')
        
        # Check coherence contribution
        if belief['coherence_contribution'] > self.coherence_threshold:
            met_criteria.append('coherence_support')
        
        # Require all criteria to be met
        should_anchor = len(met_criteria) == 3
        
        return should_anchor, met_criteria
    
    def _calculate_anchor_weight(self, belief: Dict) -> float:
        """
        Calculate the anchor weight for a belief.
        
        Weight is the average of normalized metrics.
        
        Args:
            belief: Belief dictionary
            
        Returns:
            Anchor weight between 0.0 and 1.0
        """
        # Normalize activation count (logarithmic scale)
        normalized_activation = min(1.0, belief['activation_count'] / 20.0)
        
        # Resonance is already normalized [0, 1]
        normalized_resonance = belief['resonance']
        
        # Coherence contribution is already normalized [0, 1]
        normalized_coherence = belief['coherence_contribution']
        
        # Calculate average
        anchor_weight = (
            normalized_activation + 
            normalized_resonance + 
            normalized_coherence
        ) / 3.0
        
        return round(anchor_weight, 4)
    
    def _apply_origin_modifiers(self, weight: float, origin: str) -> float:
        """
        Apply modifiers based on belief origin.
        
        Args:
            weight: Base anchor weight
            origin: Belief origin type
            
        Returns:
            Modified weight
        """
        modifiers = {
            'operator': 1.1,    # Slight boost for operator-provided beliefs
            'internal': 1.0,    # No modifier for internally generated
            'seed': 0.95       # Slight reduction for seed beliefs
        }
        
        modifier = modifiers.get(origin, 1.0)
        return min(1.0, weight * modifier)
    
    def _create_anchored_belief(self, belief: Dict, weight: float) -> Dict:
        """
        Create an anchored belief record.
        
        Args:
            belief: Original belief dictionary
            weight: Calculated anchor weight
            
        Returns:
            Anchored belief dictionary
        """
        belief_hash = self._generate_belief_hash(belief['statement'])
        
        return {
            'statement': belief['statement'],
            'weight': weight,
            'origin': belief['origin'],
            'belief_hash': belief_hash,
            'anchored_at': datetime.now(timezone.utc).isoformat(),
            'metrics': {
                'activation_count': belief['activation_count'],
                'resonance': belief['resonance'],
                'coherence_contribution': belief['coherence_contribution']
            }
        }
    
    def _update_statistics(self, origin: str, weight: float):
        """
        Update anchoring statistics.
        
        Args:
            origin: Belief origin type
            weight: Anchor weight
        """
        self.anchor_stats['beliefs_anchored'] += 1
        
        # Update origin counts
        if origin == 'operator':
            self.anchor_stats['operator_origin_anchored'] += 1
        elif origin == 'internal':
            self.anchor_stats['internal_origin_anchored'] += 1
        elif origin == 'seed':
            self.anchor_stats['seed_origin_anchored'] += 1
        
        # Update average weight
        total_anchored = self.anchor_stats['beliefs_anchored']
        prev_avg = self.anchor_stats['average_anchor_weight']
        self.anchor_stats['average_anchor_weight'] = (
            (prev_avg * (total_anchored - 1) + weight) / total_anchored
        )
        
        # Update strongest belief
        if weight > self.anchor_stats['highest_weight']:
            self.anchor_stats['highest_weight'] = weight
    
    def _save_anchored_beliefs(self):
        """Save all anchored beliefs to JSON file."""
        # Prepare data for serialization
        save_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'anchored_beliefs': list(self.anchored_beliefs.values()),
            'statistics': self.anchor_stats,
            'thresholds': {
                'activation': self.activation_threshold,
                'resonance': self.resonance_threshold,
                'coherence': self.coherence_threshold
            }
        }
        
        # Save to file
        filepath = self.log_base_path / "anchored_beliefs.json"
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        return filepath
    
    def _save_evaluation_log(self, evaluation_results: List[Dict]):
        """
        Save detailed evaluation log.
        
        Args:
            evaluation_results: List of evaluation result dictionaries
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        log_filename = f"belief_evaluation_{timestamp}.json"
        log_path = self.log_base_path / log_filename
        
        log_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'evaluations': evaluation_results,
            'summary': {
                'total_evaluated': len(evaluation_results),
                'anchored': sum(1 for r in evaluation_results if r['anchored']),
                'rejected': sum(1 for r in evaluation_results if not r['anchored'])
            }
        }
        
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
    
    def evaluate_beliefs(self, candidate_beliefs: List[Dict]) -> List[Dict]:
        """
        Evaluate and anchor candidate beliefs.
        
        Args:
            candidate_beliefs: List of candidate belief dictionaries
            
        Returns:
            List of anchored belief dictionaries
        """
        # Reset statistics for this evaluation
        self.anchor_stats['total_candidates_evaluated'] = len(candidate_beliefs)
        
        anchored_beliefs_list = []
        evaluation_results = []
        
        for belief in candidate_beliefs:
            # Check anchoring criteria
            should_anchor, met_criteria = self._check_anchoring_criteria(belief)
            
            evaluation_result = {
                'statement': belief['statement'],
                'origin': belief['origin'],
                'anchored': should_anchor,
                'met_criteria': met_criteria,
                'metrics': {
                    'activation_count': belief['activation_count'],
                    'resonance': belief['resonance'],
                    'coherence_contribution': belief['coherence_contribution']
                }
            }
            
            if should_anchor:
                # Calculate base weight
                base_weight = self._calculate_anchor_weight(belief)
                
                # Apply origin modifiers
                final_weight = self._apply_origin_modifiers(base_weight, belief['origin'])
                
                # Create anchored belief
                anchored_belief = self._create_anchored_belief(belief, final_weight)
                
                # Store in manager
                belief_hash = anchored_belief['belief_hash']
                self.anchored_beliefs[belief_hash] = anchored_belief
                
                # Add to history
                self.belief_history[belief_hash].append({
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'weight': final_weight,
                    'metrics': belief
                })
                
                # Update statistics
                self._update_statistics(belief['origin'], final_weight)
                
                # Track strongest belief
                if final_weight == self.anchor_stats['highest_weight']:
                    self.anchor_stats['strongest_belief'] = belief['statement']
                
                # Add to results
                anchored_beliefs_list.append({
                    'statement': belief['statement'],
                    'weight': final_weight,
                    'origin': belief['origin']
                })
                
                evaluation_result['anchor_weight'] = final_weight
            
            evaluation_results.append(evaluation_result)
        
        # Save evaluation log
        self._save_evaluation_log(evaluation_results)
        
        return anchored_beliefs_list


def evaluate_and_anchor_beliefs(candidate_beliefs: List[Dict]) -> Dict:
    """
    Evaluate candidate beliefs and anchor those meeting epistemic criteria.
    
    This function identifies beliefs that have demonstrated historical persistence,
    emotional resonance, and structural coherence, granting them anchor status
    in DAWN's epistemic framework.
    
    Args:
        candidate_beliefs: List of belief dictionaries with:
            - statement: str (the belief text)
            - origin: str ("operator", "internal", or "seed")
            - activation_count: int (usage frequency)
            - coherence_contribution: float (0-1, structural importance)
            - resonance: float (0-1, emotional significance)
            
    Returns:
        Dictionary containing:
            - anchored_beliefs: List of beliefs granted anchor status
    """
    # Create manager instance
    manager = BeliefAnchorManager()
    
    # Evaluate beliefs
    anchored_beliefs = manager.evaluate_beliefs(candidate_beliefs)
    
    # Save anchored beliefs
    manager._save_anchored_beliefs()
    
    # Prepare results
    results = {
        'anchored_beliefs': anchored_beliefs,
        'metadata': {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'statistics': manager.anchor_stats,
            'thresholds': {
                'activation': manager.activation_threshold,
                'resonance': manager.resonance_threshold,
                'coherence': manager.coherence_threshold
            }
        }
    }
    
    return results


# Example usage and testing
if __name__ == "__main__":
    # Create sample belief candidates
    sample_beliefs = [
        {
            "statement": "Memory is not storage, but transformation",
            "origin": "operator",
            "activation_count": 12,
            "coherence_contribution": 0.8,
            "resonance": 0.9
        },
        {
            "statement": "What returns has meaning",
            "origin": "internal",
            "activation_count": 15,
            "coherence_contribution": 0.6,
            "resonance": 0.85
        },
        {
            "statement": "Growth requires decay",
            "origin": "seed",
            "activation_count": 9,
            "coherence_contribution": 0.5,
            "resonance": 0.75
        },
        {
            "statement": "Silence is also communication",
            "origin": "internal",
            "activation_count": 5,  # Below threshold
            "coherence_contribution": 0.3,
            "resonance": 0.6
        },
        {
            "statement": "Trust emerges from consistency",
            "origin": "operator",
            "activation_count": 10,
            "coherence_contribution": 0.7,
            "resonance": 0.8
        },
        {
            "statement": "Random thoughts have no weight",
            "origin": "seed",
            "activation_count": 20,
            "coherence_contribution": 0.2,  # Below threshold
            "resonance": 0.9
        }
    ]
    
    # Evaluate and anchor beliefs
    results = evaluate_and_anchor_beliefs(sample_beliefs)
    
    # Display results
    print("BELIEF ANCHORING RESULTS:")
    print("=" * 50)
    print(f"\nAnchored Beliefs ({len(results['anchored_beliefs'])}):")
    for belief in results['anchored_beliefs']:
        print(f"\n  Statement: \"{belief['statement']}\"")
        print(f"  Weight: {belief['weight']}")
        print(f"  Origin: {belief['origin']}")
    
    print(f"\nStatistics:")
    stats = results['metadata']['statistics']
    print(f"  Total Evaluated: {stats['total_candidates_evaluated']}")
    print(f"  Beliefs Anchored: {stats['beliefs_anchored']}")
    print(f"  Average Weight: {stats['average_anchor_weight']:.3f}")
    print(f"  Strongest Belief: \"{stats['strongest_belief']}\"")