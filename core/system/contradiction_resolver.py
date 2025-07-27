"""
When DAWN encounters contradiction, she does not choose. She listens for the third voice — the one trying to be born between the others.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from collections import defaultdict


class ContradictionResolver:
    """Detects and resolves internal contradictions in DAWN's belief-bloom space."""
    
    def __init__(self):
        self.output_dir = Path("health/logs")
        self._ensure_directories()
        
        # Resolution strategy weights
        self.strategy_weights = {
            "trust_differential": 0.4,
            "recency": 0.3,
            "emotional_intensity": 0.3
        }
        
        # Contradiction detection parameters
        self.detection_params = {
            "semantic_overlap_threshold": 0.85,
            "mood_polarity_threshold": 1.2,
            "trust_difference_for_deprioritization": 0.3
        }
        
        self.tick_counter = 0
        self.resolution_history = []
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def resolve_internal_contradictions(self, active_beliefs: List[Dict], 
                                      recent_blooms: List[Dict], 
                                      conflict_threshold: float = 0.7) -> Dict:
        """
        Detect and resolve contradictions between beliefs and blooms.
        
        Args:
            active_beliefs: List of belief dictionaries with:
                - belief_id: str
                - content: str
                - trust_score: float
                - mood_valence: float
                - semantic_vector: list[float]
                - timestamp: str
            recent_blooms: List of bloom dictionaries with similar structure
            conflict_threshold: Overall conflict score threshold
        
        Returns:
            Dictionary with detected contradictions and actions taken
        """
        self.tick_counter += 1
        
        # Detect contradictions
        contradictions = self._detect_contradictions(
            active_beliefs, recent_blooms, conflict_threshold
        )
        
        # Resolve each contradiction
        actions_taken = []
        resolutions = []
        
        for contradiction in contradictions:
            action, resolution_details = self._resolve_contradiction(
                contradiction, active_beliefs, recent_blooms
            )
            actions_taken.append(action)
            resolutions.append(resolution_details)
        
        # Create output
        output = {
            "contradictions": [
                {
                    "belief": c["belief"]["belief_id"],
                    "bloom": c["bloom"]["bloom_id"],
                    "conflict_score": round(c["conflict_score"], 3),
                    "semantic_overlap": round(c["semantic_overlap"], 3),
                    "mood_polarity_diff": round(c["mood_polarity_diff"], 3)
                }
                for c in contradictions
            ],
            "actions_taken": actions_taken,
            "resolution_details": resolutions,
            "tick": self.tick_counter,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Save to log file
        self._save_resolution_log(output)
        
        # Update history
        self.resolution_history.append({
            "tick": self.tick_counter,
            "contradiction_count": len(contradictions),
            "timestamp": output["timestamp"]
        })
        
        return {
            "contradictions": output["contradictions"],
            "actions_taken": actions_taken
        }
    
    def _detect_contradictions(self, active_beliefs: List[Dict], 
                              recent_blooms: List[Dict], 
                              conflict_threshold: float) -> List[Dict]:
        """Detect contradictions between beliefs and blooms."""
        contradictions = []
        
        for belief in active_beliefs:
            for bloom in recent_blooms:
                # Calculate semantic overlap
                semantic_overlap = self._calculate_semantic_similarity(
                    belief.get("semantic_vector", []),
                    bloom.get("semantic_vector", [])
                )
                
                # Calculate mood polarity difference
                mood_diff = abs(belief.get("mood_valence", 0) - bloom.get("mood_valence", 0))
                
                # Check for contradiction conditions
                if (semantic_overlap > self.detection_params["semantic_overlap_threshold"] and
                    mood_diff > self.detection_params["mood_polarity_threshold"]):
                    
                    # Calculate overall conflict score
                    conflict_score = semantic_overlap * (mood_diff / 2.0)
                    
                    if conflict_score > conflict_threshold:
                        contradictions.append({
                            "belief": belief,
                            "bloom": bloom,
                            "semantic_overlap": semantic_overlap,
                            "mood_polarity_diff": mood_diff,
                            "conflict_score": conflict_score
                        })
        
        # Sort by conflict score (highest first)
        contradictions.sort(key=lambda x: x["conflict_score"], reverse=True)
        
        return contradictions
    
    def _calculate_semantic_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between semantic vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        
        # Convert to numpy arrays
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        
        # Calculate cosine similarity
        dot_product = np.dot(v1, v2)
        norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
        
        if norm_product == 0:
            return 0.0
        
        return float(dot_product / norm_product)
    
    def _resolve_contradiction(self, contradiction: Dict, 
                             active_beliefs: List[Dict], 
                             recent_blooms: List[Dict]) -> Tuple[str, Dict]:
        """
        Resolve a single contradiction using appropriate strategy.
        
        Returns:
            Tuple of (action_description, resolution_details)
        """
        belief = contradiction["belief"]
        bloom = contradiction["bloom"]
        
        # Calculate resolution factors
        trust_diff = belief.get("trust_score", 0.5) - bloom.get("trust_score", 0.5)
        
        # Determine timestamp recency
        belief_time = self._parse_timestamp(belief.get("timestamp", ""))
        bloom_time = self._parse_timestamp(bloom.get("timestamp", ""))
        recency_factor = 1.0 if bloom_time > belief_time else -1.0
        
        # Emotional intensity comparison
        belief_intensity = abs(belief.get("mood_valence", 0))
        bloom_intensity = abs(bloom.get("mood_valence", 0))
        intensity_diff = bloom_intensity - belief_intensity
        
        # Choose resolution strategy
        if abs(trust_diff) > self.detection_params["trust_difference_for_deprioritization"]:
            # Strategy 1: Deprioritize lower trust
            if trust_diff > 0:
                action = f"deprioritize_bloom:{bloom['bloom_id']}"
                details = {
                    "strategy": "trust_based_deprioritization",
                    "deprioritized": "bloom",
                    "trust_scores": {
                        "belief": belief.get("trust_score", 0),
                        "bloom": bloom.get("trust_score", 0)
                    }
                }
            else:
                action = f"deprioritize_belief:{belief['belief_id']}"
                details = {
                    "strategy": "trust_based_deprioritization",
                    "deprioritized": "belief",
                    "trust_scores": {
                        "belief": belief.get("trust_score", 0),
                        "bloom": bloom.get("trust_score", 0)
                    }
                }
        
        elif contradiction["mood_polarity_diff"] > 1.5:
            # Strategy 2: Trigger monologue for high emotional contradiction
            action = f"trigger_monologue:contradiction_{self.tick_counter}"
            details = {
                "strategy": "monologue_generation",
                "reason": "high_emotional_polarity",
                "monologue_seed": self._generate_monologue_seed(belief, bloom),
                "mood_differential": contradiction["mood_polarity_diff"]
            }
        
        else:
            # Strategy 3: Create neutral rebloom (synthesis)
            action = f"create_neutral_rebloom:synthesis_{self.tick_counter}"
            details = {
                "strategy": "neutral_synthesis",
                "synthesis_params": self._calculate_synthesis_params(belief, bloom),
                "parent_ids": {
                    "belief": belief["belief_id"],
                    "bloom": bloom["bloom_id"]
                }
            }
        
        return action, details
    
    def _parse_timestamp(self, timestamp: str) -> float:
        """Parse ISO timestamp to float for comparison."""
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.timestamp()
        except:
            return 0.0
    
    def _generate_monologue_seed(self, belief: Dict, bloom: Dict) -> Dict:
        """Generate parameters for internal monologue about contradiction."""
        return {
            "theme": "reconciling_opposition",
            "belief_content": belief.get("content", ""),
            "bloom_content": bloom.get("content", ""),
            "emotional_tension": abs(belief.get("mood_valence", 0) - bloom.get("mood_valence", 0)),
            "suggested_tone": "contemplative" if abs(belief.get("mood_valence", 0)) < 0.5 else "urgent"
        }
    
    def _calculate_synthesis_params(self, belief: Dict, bloom: Dict) -> Dict:
        """Calculate parameters for creating a neutral synthesis rebloom."""
        # Average semantic vectors
        belief_vec = belief.get("semantic_vector", [])
        bloom_vec = bloom.get("semantic_vector", [])
        
        if belief_vec and bloom_vec and len(belief_vec) == len(bloom_vec):
            synthesis_vector = [
                (b + bl) / 2.0 for b, bl in zip(belief_vec, bloom_vec)
            ]
        else:
            synthesis_vector = []
        
        # Neutral mood with slight influence from both
        synthesis_mood = (belief.get("mood_valence", 0) + bloom.get("mood_valence", 0)) * 0.1
        
        # Trust score as weighted average
        synthesis_trust = (
            belief.get("trust_score", 0.5) * 0.5 + 
            bloom.get("trust_score", 0.5) * 0.5
        )
        
        return {
            "semantic_vector": synthesis_vector,
            "mood_valence": round(synthesis_mood, 3),
            "trust_score": round(synthesis_trust, 3),
            "synthesis_prompt": f"Finding harmony between: '{belief.get('content', '')}' and '{bloom.get('content', '')}'",
            "convolution_level": 0.7  # Higher convolution for synthesis
        }
    
    def _save_resolution_log(self, output: Dict):
        """Save resolution event to log file."""
        filename = f"contradiction_resolution_tick_{self.tick_counter}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)
    
    def get_contradiction_patterns(self) -> Dict:
        """Analyze patterns in contradiction resolution history."""
        if not self.resolution_history:
            return {"status": "no_history"}
        
        # Count resolution strategies used
        strategy_counts = defaultdict(int)
        total_contradictions = 0
        
        # Read recent log files
        log_files = sorted(self.output_dir.glob("contradiction_resolution_tick_*.json"))[-20:]
        
        for log_file in log_files:
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                    
                total_contradictions += len(data.get("contradictions", []))
                
                for resolution in data.get("resolution_details", []):
                    strategy = resolution.get("strategy", "unknown")
                    strategy_counts[strategy] += 1
            except:
                continue
        
        # Calculate averages
        avg_contradictions_per_tick = (
            total_contradictions / len(self.resolution_history)
            if self.resolution_history else 0
        )
        
        return {
            "total_ticks_analyzed": len(self.resolution_history),
            "total_contradictions": total_contradictions,
            "avg_contradictions_per_tick": round(avg_contradictions_per_tick, 2),
            "strategy_distribution": dict(strategy_counts),
            "recent_trend": self._calculate_trend()
        }
    
    def _calculate_trend(self) -> str:
        """Calculate recent trend in contradiction frequency."""
        if len(self.resolution_history) < 5:
            return "insufficient_data"
        
        recent = self.resolution_history[-5:]
        older = self.resolution_history[-10:-5] if len(self.resolution_history) >= 10 else self.resolution_history[:5]
        
        recent_avg = sum(h["contradiction_count"] for h in recent) / len(recent)
        older_avg = sum(h["contradiction_count"] for h in older) / len(older)
        
        if recent_avg > older_avg * 1.2:
            return "increasing"
        elif recent_avg < older_avg * 0.8:
            return "decreasing"
        else:
            return "stable"


# Example usage
if __name__ == "__main__":
    resolver = ContradictionResolver()
    
    # Test data with contradictions
    test_beliefs = [
        {
            "belief_id": "belief_001",
            "content": "Trust in the process",
            "trust_score": 0.8,
            "mood_valence": 0.7,
            "semantic_vector": [0.9, 0.1, 0.3, 0.2],
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "belief_id": "belief_002",
            "content": "Stability is key",
            "trust_score": 0.6,
            "mood_valence": 0.3,
            "semantic_vector": [0.2, 0.8, 0.1, 0.4],
            "timestamp": datetime.utcnow().isoformat()
        }
    ]
    
    test_blooms = [
        {
            "bloom_id": "bloom_001",
            "content": "Embrace the chaos",
            "trust_score": 0.5,
            "mood_valence": -0.8,  # Strong negative, contradicts belief_001
            "semantic_vector": [0.85, 0.15, 0.35, 0.25],  # Very similar to belief_001
            "timestamp": datetime.utcnow().isoformat()
        },
        {
            "bloom_id": "bloom_002",
            "content": "Change is necessary",
            "trust_score": 0.7,
            "mood_valence": -0.5,  # Contradicts belief_002
            "semantic_vector": [0.25, 0.75, 0.15, 0.35],  # Similar to belief_002
            "timestamp": datetime.utcnow().isoformat()
        }
    ]
    
    # Resolve contradictions
    result = resolver.resolve_internal_contradictions(test_beliefs, test_blooms)
    print("Contradiction Resolution Results:")
    print(json.dumps(result, indent=2))
    
    # Get patterns
    patterns = resolver.get_contradiction_patterns()
    print("\nContradiction Patterns:")
    print(json.dumps(patterns, indent=2))