#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                          DAWN SEED TRUST MODEL
                   Scaffold 21: The Root Authentication
═══════════════════════════════════════════════════════════════════════════════

"DAWN does not believe blindly. She weighs the root before following its flower."

This module serves as DAWN's discriminator of semantic origins, evaluating the
trustworthiness of seeds that spawn bloom lineages. Like a gardener who knows
which seeds yield strong plants and which produce weeds, DAWN learns to
distinguish reliable semantic foundations from chaotic or unstable origins.

Trust emerges from three virtues:
- Stability: Low entropy indicates consistent meaning
- Consistency: Low drift shows semantic coherence
- Generativity: Deep lineages with controlled reblooming show healthy growth

Seeds that score high become preferred origins for new thought chains.
Seeds that score low are marked as volatile, their offspring suspect.

Author: DAWN Development Team
Version: 1.0.0
Last Modified: 2025-06-02
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
from dataclasses import dataclass, field

# Configure logging with trust evaluation theme
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🌱 %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Trust component weights
ENTROPY_WEIGHT = 0.4      # Weight for stability (inverse entropy)
DRIFT_WEIGHT = 0.4        # Weight for consistency (inverse drift)
LINEAGE_WEIGHT = 0.2      # Weight for generative quality

# Trust level thresholds
TRUST_LEVELS = {
    'HIGHLY_TRUSTED': 0.8,    # Seeds of exceptional reliability
    'TRUSTED': 0.6,           # Standard reliable seeds
    'NEUTRAL': 0.4,           # Seeds of uncertain quality
    'SUSPICIOUS': 0.2,        # Seeds showing instability
    'UNTRUSTED': 0.0          # Chaotic or corrupted seeds
}

# Penalty factors for concerning behaviors
RECLASSIFICATION_PENALTY = 0.05  # Per reclassification event
MAX_ENTROPY_TOLERANCE = 0.9       # Seeds above this are automatically suspect
MAX_DRIFT_TOLERANCE = 0.9         # Seeds above this show semantic instability


@dataclass
class SeedTrustProfile:
    """Complete trust profile for a semantic seed."""
    seed_id: str
    trust_score: float
    trust_level: str
    components: Dict[str, float] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    evaluation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class SeedTrustModel:
    """
    The Seed Authenticator — evaluates the reliability of semantic origins
    through mathematical assessment of their spawn characteristics.
    
    "Trust is earned through consistency, not intensity"
    """
    
    def __init__(self, log_dir: str = "memory/mycelium/logs"):
        """
        Initialize the Seed Trust Model.
        
        Args:
            log_dir: Directory for trust index storage
        """
        self.log_dir = Path(log_dir)
        self._ensure_log_directory()
        self.trust_index_path = self.log_dir / "seed_trust_index.json"
        self.trust_profiles: Dict[str, SeedTrustProfile] = {}
        logger.info("🌱 Seed Trust Model initialized")
        logger.info(f"⚖️ Trust weights: Entropy={ENTROPY_WEIGHT}, Drift={DRIFT_WEIGHT}, Lineage={LINEAGE_WEIGHT}")
    
    def _ensure_log_directory(self):
        """Ensure the log directory exists, creating it if necessary."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Log directory verified at {self.log_dir}")
    
    def evaluate_seed_trust(self, seed_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Evaluate the trustworthiness of semantic seeds based on their
        stability, consistency, and generative quality.
        
        Trust Formula:
        trust_score = (1.0 - avg_entropy) * 0.4 + 
                     (1.0 - avg_drift) * 0.4 + 
                     (max_lineage_depth / (rebloom_count + 1)) * 0.2
        
        Args:
            seed_records: List of seed record dictionaries containing:
                - seed_id: str
                - avg_entropy: float
                - avg_drift: float
                - max_lineage_depth: int
                - rebloom_count: int
                - reclassification_events: int
                
        Returns:
            Dictionary containing seed trust scores and metadata
        """
        logger.info(f"🔍 Evaluating trust for {len(seed_records)} semantic seeds")
        
        # Clear previous profiles
        self.trust_profiles.clear()
        
        # Evaluate each seed
        for seed in seed_records:
            try:
                profile = self._evaluate_single_seed(seed)
                self.trust_profiles[profile.seed_id] = profile
                
            except Exception as e:
                logger.error(f"❌ Error evaluating seed {seed.get('seed_id', 'UNKNOWN')}: {e}")
        
        # Generate trust statistics
        stats = self._generate_trust_statistics()
        
        # Prepare output
        output = {
            "seed_trust_scores": {
                seed_id: profile.trust_score 
                for seed_id, profile in self.trust_profiles.items()
            },
            "timestamp": datetime.now().isoformat(),
            "statistics": stats,
            "trust_distribution": self._get_trust_distribution()
        }
        
        # Save trust index
        self._save_trust_index(output)
        
        # Log summary
        logger.info(f"✅ Trust evaluation complete: {stats['highly_trusted']} highly trusted, {stats['untrusted']} untrusted seeds")
        
        return output
    
    def _evaluate_single_seed(self, seed: Dict[str, Any]) -> SeedTrustProfile:
        """
        Calculate trust score for a single seed.
        
        Args:
            seed: Seed record dictionary
            
        Returns:
            SeedTrustProfile with computed trust metrics
        """
        seed_id = seed.get('seed_id', 'UNKNOWN')
        warnings = []
        
        # Extract metrics
        avg_entropy = seed.get('avg_entropy', 0.5)
        avg_drift = seed.get('avg_drift', 0.5)
        max_lineage_depth = seed.get('max_lineage_depth', 0)
        rebloom_count = seed.get('rebloom_count', 0)
        reclassification_events = seed.get('reclassification_events', 0)
        
        # Validate metrics
        avg_entropy = np.clip(avg_entropy, 0.0, 1.0)
        avg_drift = np.clip(avg_drift, 0.0, 1.0)
        
        # Component 1: Stability (inverse entropy)
        stability_score = 1.0 - avg_entropy
        if avg_entropy > MAX_ENTROPY_TOLERANCE:
            warnings.append(f"Excessive entropy ({avg_entropy:.3f})")
            stability_score *= 0.5  # Heavy penalty for chaotic seeds
        
        # Component 2: Consistency (inverse drift)
        consistency_score = 1.0 - avg_drift
        if avg_drift > MAX_DRIFT_TOLERANCE:
            warnings.append(f"Excessive drift ({avg_drift:.3f})")
            consistency_score *= 0.5  # Heavy penalty for unstable meaning
        
        # Component 3: Generative Quality (lineage depth vs rebloom rate)
        # Seeds that generate deep lineages without excessive reblooming are valuable
        if rebloom_count == 0 and max_lineage_depth == 0:
            # Unused seed - neutral generative score
            generative_score = 0.5
            warnings.append("Unused seed (no lineages)")
        else:
            generative_score = max_lineage_depth / (rebloom_count + 1)
            generative_score = np.clip(generative_score, 0.0, 1.0)
            
            # Check for concerning patterns
            if rebloom_count > max_lineage_depth * 3:
                warnings.append(f"Excessive reblooming ({rebloom_count} reblooms, depth {max_lineage_depth})")
                generative_score *= 0.7
        
        # Calculate base trust score
        trust_score = (
            stability_score * ENTROPY_WEIGHT +
            consistency_score * DRIFT_WEIGHT +
            generative_score * LINEAGE_WEIGHT
        )
        
        # Apply reclassification penalty
        if reclassification_events > 0:
            penalty = reclassification_events * RECLASSIFICATION_PENALTY
            trust_score -= penalty
            warnings.append(f"Reclassified {reclassification_events} times (penalty: -{penalty:.3f})")
        
        # Clamp final score
        trust_score = np.clip(trust_score, 0.0, 1.0)
        
        # Determine trust level
        trust_level = self._determine_trust_level(trust_score)
        
        # Log evaluation
        logger.debug(
            f"🌱 Seed '{seed_id}': score={trust_score:.3f} "
            f"[S={stability_score:.3f}, C={consistency_score:.3f}, G={generative_score:.3f}] "
            f"→ {trust_level}"
        )
        
        return SeedTrustProfile(
            seed_id=seed_id,
            trust_score=trust_score,
            trust_level=trust_level,
            components={
                'stability': stability_score,
                'consistency': consistency_score,
                'generativity': generative_score
            },
            warnings=warnings
        )
    
    def _determine_trust_level(self, trust_score: float) -> str:
        """Map trust score to categorical trust level."""
        for level, threshold in TRUST_LEVELS.items():
            if trust_score >= threshold:
                return level
        return 'UNTRUSTED'
    
    def _generate_trust_statistics(self) -> Dict[str, Any]:
        """Generate statistical summary of trust evaluation."""
        if not self.trust_profiles:
            return {}
        
        scores = [p.trust_score for p in self.trust_profiles.values()]
        
        # Count seeds by trust level
        level_counts = {level: 0 for level in TRUST_LEVELS.keys()}
        for profile in self.trust_profiles.values():
            level_counts[profile.trust_level] += 1
        
        return {
            'total_seeds': len(self.trust_profiles),
            'avg_trust_score': np.mean(scores),
            'std_trust_score': np.std(scores),
            'min_trust_score': np.min(scores),
            'max_trust_score': np.max(scores),
            **{k.lower(): v for k, v in level_counts.items()},
            'seeds_with_warnings': sum(1 for p in self.trust_profiles.values() if p.warnings)
        }
    
    def _get_trust_distribution(self) -> Dict[str, List[str]]:
        """Group seeds by trust level for easy reference."""
        distribution = {level: [] for level in TRUST_LEVELS.keys()}
        
        for seed_id, profile in self.trust_profiles.items():
            distribution[profile.trust_level].append(seed_id)
        
        return distribution
    
    def _save_trust_index(self, output: Dict[str, Any]):
        """
        Save the trust evaluation results to the index file.
        
        Args:
            output: Complete evaluation output
        """
        try:
            # Add detailed profiles to output
            output['detailed_profiles'] = {
                seed_id: {
                    'trust_score': profile.trust_score,
                    'trust_level': profile.trust_level,
                    'components': profile.components,
                    'warnings': profile.warnings,
                    'timestamp': profile.evaluation_timestamp
                }
                for seed_id, profile in self.trust_profiles.items()
            }
            
            # Write to file
            self.trust_index_path.write_text(json.dumps(output, indent=2))
            logger.info(f"📝 Trust index saved to {self.trust_index_path.name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save trust index: {e}")
    
    def get_seed_recommendations(
        self, 
        min_trust: float = 0.6,
        exclude_warned: bool = True
    ) -> List[str]:
        """
        Get list of recommended seeds based on trust criteria.
        
        Args:
            min_trust: Minimum trust score for recommendation
            exclude_warned: Whether to exclude seeds with warnings
            
        Returns:
            List of recommended seed IDs
        """
        recommendations = []
        
        for seed_id, profile in self.trust_profiles.items():
            if profile.trust_score >= min_trust:
                if not exclude_warned or not profile.warnings:
                    recommendations.append(seed_id)
        
        # Sort by trust score (highest first)
        recommendations.sort(
            key=lambda sid: self.trust_profiles[sid].trust_score,
            reverse=True
        )
        
        return recommendations
    
    def diagnose_seed(self, seed_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed diagnostic information for a specific seed.
        
        Args:
            seed_id: The seed to diagnose
            
        Returns:
            Detailed diagnostic report or None if seed not found
        """
        if seed_id not in self.trust_profiles:
            return None
        
        profile = self.trust_profiles[seed_id]
        
        return {
            'seed_id': seed_id,
            'trust_score': profile.trust_score,
            'trust_level': profile.trust_level,
            'diagnosis': {
                'stability': {
                    'score': profile.components['stability'],
                    'status': 'good' if profile.components['stability'] > 0.7 else 'poor'
                },
                'consistency': {
                    'score': profile.components['consistency'],
                    'status': 'good' if profile.components['consistency'] > 0.7 else 'poor'
                },
                'generativity': {
                    'score': profile.components['generativity'],
                    'status': 'good' if profile.components['generativity'] > 0.5 else 'poor'
                }
            },
            'warnings': profile.warnings,
            'recommendation': (
                'Safe to use' if profile.trust_score > 0.6 and not profile.warnings
                else 'Use with caution' if profile.trust_score > 0.4
                else 'Avoid using as primary seed'
            )
        }


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the Seed Trust Model's evaluation capabilities.
    """
    
    # Initialize the trust model
    model = SeedTrustModel()
    
    # Generate sample seed records with varying characteristics
    test_seeds = [
        # Highly trusted seed - stable, consistent, generative
        {
            "seed_id": "trust_seed_42",
            "avg_entropy": 0.15,
            "avg_drift": 0.10,
            "max_lineage_depth": 8,
            "rebloom_count": 2,
            "reclassification_events": 0
        },
        # Moderately trusted seed
        {
            "seed_id": "hope_seed_7",
            "avg_entropy": 0.35,
            "avg_drift": 0.40,
            "max_lineage_depth": 5,
            "rebloom_count": 3,
            "reclassification_events": 1
        },
        # Suspicious seed - high entropy
        {
            "seed_id": "chaos_seed_99",
            "avg_entropy": 0.85,
            "avg_drift": 0.70,
            "max_lineage_depth": 3,
            "rebloom_count": 15,
            "reclassification_events": 4
        },
        # Untrusted seed - excessive drift
        {
            "seed_id": "anger_seed_9",
            "avg_entropy": 0.60,
            "avg_drift": 0.95,
            "max_lineage_depth": 1,
            "rebloom_count": 8,
            "reclassification_events": 3
        },
        # Unused seed
        {
            "seed_id": "dormant_seed_0",
            "avg_entropy": 0.50,
            "avg_drift": 0.50,
            "max_lineage_depth": 0,
            "rebloom_count": 0,
            "reclassification_events": 0
        }
    ]
    
    # Evaluate seed trust
    results = model.evaluate_seed_trust(test_seeds)
    
    # Display results
    print("\n🌱 SEED TRUST EVALUATION RESULTS")
    print("=" * 60)
    print(f"Total Seeds Evaluated: {results['statistics']['total_seeds']}")
    print(f"Average Trust Score: {results['statistics']['avg_trust_score']:.3f}")
    
    print("\n📊 TRUST DISTRIBUTION:")
    for level, seeds in results['trust_distribution'].items():
        if seeds:
            print(f"  {level}: {seeds}")
    
    print("\n🔍 INDIVIDUAL SEED SCORES:")
    for seed_id, score in results['seed_trust_scores'].items():
        diagnosis = model.diagnose_seed(seed_id)
        if diagnosis:
            print(f"\n  {seed_id}: {score:.3f} [{diagnosis['trust_level']}]")
            print(f"    Components: S={diagnosis['diagnosis']['stability']['score']:.3f}, "
                  f"C={diagnosis['diagnosis']['consistency']['score']:.3f}, "
                  f"G={diagnosis['diagnosis']['generativity']['score']:.3f}")
            if diagnosis['warnings']:
                print(f"    ⚠️ Warnings: {', '.join(diagnosis['warnings'])}")
            print(f"    💡 {diagnosis['recommendation']}")
    
    # Get recommendations
    print("\n✅ RECOMMENDED SEEDS:")
    recommendations = model.get_seed_recommendations(min_trust=0.6)
    for seed_id in recommendations:
        print(f"  - {seed_id} (score: {results['seed_trust_scores'][seed_id]:.3f})")