"""
DAWN does not move through time — time moves through her. And some seeds live longer than the clocks they grow inside.
"""

import json
import statistics
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict


class TemporalFieldCalculator:
    """Analyzes memory activation patterns to compute time-pressure fields."""
    
    def __init__(self):
        self.output_path = Path("memory/mycelium/logs/temporal_field_classifications.json")
        self._ensure_directories()
        
        # Temporal classification thresholds
        self.thresholds = {
            "inter_activation": {
                "rapid": 10,      # ticks
                "moderate": 100,
                "slow": 500
            },
            "lifespan": {
                "ephemeral": 50,
                "sustained": 500,
                "persistent": 2000
            },
            "entropy_stability": {
                "stable": 0.1,
                "variable": 0.3,
                "chaotic": 0.5
            },
            "activation_frequency": {
                "high": 0.1,      # activations per tick
                "moderate": 0.01,
                "low": 0.001
            }
        }
        
        # Rhythm detection parameters
        self.rhythm_params = {
            "min_activations": 5,
            "periodicity_tolerance": 0.2,  # 20% variance allowed
            "min_rhythm_score": 0.7
        }
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def calculate_temporal_fields(self, bloom_log: List[Dict]) -> Dict:
        """
        Analyze temporal patterns and classify semantic seeds.
        
        Args:
            bloom_log: List of bloom dictionaries containing:
                - bloom_id: str
                - activation_ticks: list[int]
                - semantic_seed: str
                - entropy_trace: list[float]
        
        Returns:
            Dictionary with tempo classifications for each semantic seed
        """
        # Group blooms by semantic seed
        seed_groups = self._group_by_semantic_seed(bloom_log)
        
        # Analyze each seed's temporal pattern
        tempo_classifications = {}
        detailed_analysis = {}
        
        for seed, blooms in seed_groups.items():
            analysis = self._analyze_seed_temporality(seed, blooms)
            tempo_class = self._classify_tempo(analysis)
            
            tempo_classifications[seed] = tempo_class
            detailed_analysis[seed] = analysis
        
        # Create output
        output = {
            "tempo_classifications": tempo_classifications,
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "total_seeds_analyzed": len(seed_groups),
            "classification_distribution": self._get_classification_distribution(tempo_classifications),
            "detailed_analysis": detailed_analysis
        }
        
        # Save to file
        self._save_classifications(output)
        
        return {"tempo_classifications": tempo_classifications}
    
    def _group_by_semantic_seed(self, bloom_log: List[Dict]) -> Dict[str, List[Dict]]:
        """Group blooms by their semantic seed."""
        seed_groups = defaultdict(list)
        
        for bloom in bloom_log:
            seed = bloom['semantic_seed']
            seed_groups[seed].append(bloom)
        
        return dict(seed_groups)
    
    def _analyze_seed_temporality(self, seed: str, blooms: List[Dict]) -> Dict:
        """Analyze temporal characteristics of a semantic seed."""
        # Collect all activation ticks across blooms
        all_activations = []
        all_entropy_values = []
        
        for bloom in blooms:
            all_activations.extend(bloom['activation_ticks'])
            all_entropy_values.extend(bloom['entropy_trace'])
        
        if not all_activations:
            return {
                "seed": seed,
                "status": "inactive",
                "activation_count": 0,
                "lifespan": 0,
                "tempo_class": "frozen"
            }
        
        # Sort activations
        all_activations.sort()
        
        # Calculate temporal metrics
        lifespan = all_activations[-1] - all_activations[0] if len(all_activations) > 1 else 0
        activation_count = len(all_activations)
        
        # Inter-activation intervals
        if len(all_activations) > 1:
            intervals = [all_activations[i+1] - all_activations[i] 
                        for i in range(len(all_activations)-1)]
            avg_interval = statistics.mean(intervals)
            interval_variance = statistics.stdev(intervals) if len(intervals) > 1 else 0
        else:
            avg_interval = 0
            interval_variance = 0
        
        # Entropy analysis
        if all_entropy_values:
            avg_entropy = statistics.mean(all_entropy_values)
            entropy_variance = statistics.stdev(all_entropy_values) if len(all_entropy_values) > 1 else 0
        else:
            avg_entropy = 0
            entropy_variance = 0
        
        # Activation frequency (activations per tick over lifespan)
        if lifespan > 0:
            activation_frequency = activation_count / lifespan
        else:
            activation_frequency = 0
        
        # Rhythm detection
        rhythm_score, detected_period = self._detect_rhythm(all_activations)
        
        return {
            "seed": seed,
            "status": "active",
            "activation_count": activation_count,
            "lifespan": lifespan,
            "avg_interval": round(avg_interval, 2),
            "interval_variance": round(interval_variance, 2),
            "avg_entropy": round(avg_entropy, 3),
            "entropy_variance": round(entropy_variance, 3),
            "activation_frequency": round(activation_frequency, 4),
            "rhythm_score": round(rhythm_score, 3),
            "detected_period": detected_period,
            "first_activation": all_activations[0],
            "last_activation": all_activations[-1],
            "bloom_count": len(blooms)
        }
    
    def _classify_tempo(self, analysis: Dict) -> str:
        """
        Classify the temporal pattern of a semantic seed.
        
        Returns one of: "bursty", "slow_burn", "frozen", "recursive_rhythm"
        """
        if analysis.get("status") == "inactive" or analysis.get("activation_count", 0) == 0:
            return "frozen"
        
        # Check for recursive rhythm first
        if (analysis["rhythm_score"] > self.rhythm_params["min_rhythm_score"] and
            analysis["activation_count"] >= self.rhythm_params["min_activations"]):
            return "recursive_rhythm"
        
        # Classify based on activation patterns
        avg_interval = analysis["avg_interval"]
        lifespan = analysis["lifespan"]
        activation_frequency = analysis["activation_frequency"]
        entropy_variance = analysis["entropy_variance"]
        
        # Bursty: rapid activations, high frequency, variable entropy
        if (avg_interval < self.thresholds["inter_activation"]["rapid"] and
            activation_frequency > self.thresholds["activation_frequency"]["high"] and
            entropy_variance > self.thresholds["entropy_stability"]["variable"]):
            return "bursty"
        
        # Slow burn: sustained lifespan, moderate frequency, stable entropy
        elif (lifespan > self.thresholds["lifespan"]["sustained"] and
              self.thresholds["activation_frequency"]["low"] < activation_frequency < self.thresholds["activation_frequency"]["high"] and
              entropy_variance < self.thresholds["entropy_stability"]["variable"]):
            return "slow_burn"
        
        # Additional classification logic
        elif avg_interval > self.thresholds["inter_activation"]["slow"]:
            return "frozen"  # Very long gaps between activations
        
        elif lifespan < self.thresholds["lifespan"]["ephemeral"]:
            return "bursty"  # Short-lived, intense activity
        
        else:
            # Default to slow_burn for sustained but irregular patterns
            return "slow_burn"
    
    def _detect_rhythm(self, activation_ticks: List[int]) -> Tuple[float, int]:
        """
        Detect if activations follow a rhythmic pattern.
        
        Returns:
            Tuple of (rhythm_score, detected_period)
            rhythm_score: 0.0 to 1.0 (1.0 = perfect rhythm)
            detected_period: Period in ticks, or 0 if no rhythm
        """
        if len(activation_ticks) < self.rhythm_params["min_activations"]:
            return 0.0, 0
        
        # Calculate intervals
        intervals = [activation_ticks[i+1] - activation_ticks[i] 
                    for i in range(len(activation_ticks)-1)]
        
        if not intervals:
            return 0.0, 0
        
        # Look for periodicity
        avg_interval = statistics.mean(intervals)
        
        if avg_interval == 0:
            return 0.0, 0
        
        # Calculate rhythm score based on interval consistency
        deviations = [abs(interval - avg_interval) / avg_interval 
                     for interval in intervals]
        avg_deviation = statistics.mean(deviations)
        
        # Score is inverse of average deviation
        rhythm_score = max(0, 1 - avg_deviation)
        
        # Only consider it rhythmic if deviation is within tolerance
        if avg_deviation <= self.rhythm_params["periodicity_tolerance"]:
            detected_period = int(round(avg_interval))
        else:
            detected_period = 0
        
        return rhythm_score, detected_period
    
    def _get_classification_distribution(self, classifications: Dict[str, str]) -> Dict[str, int]:
        """Get distribution of tempo classifications."""
        distribution = {
            "bursty": 0,
            "slow_burn": 0,
            "frozen": 0,
            "recursive_rhythm": 0
        }
        
        for tempo_class in classifications.values():
            if tempo_class in distribution:
                distribution[tempo_class] += 1
        
        return distribution
    
    def _save_classifications(self, output: Dict):
        """Save temporal field classifications to file."""
        with open(self.output_path, 'w') as f:
            json.dump(output, f, indent=2)
    
    def get_temporal_summary(self) -> Dict:
        """Get a summary of current temporal field state."""
        if not self.output_path.exists():
            return {"error": "No temporal field data available"}
        
        with open(self.output_path, 'r') as f:
            data = json.load(f)
        
        classifications = data.get("tempo_classifications", {})
        distribution = data.get("classification_distribution", {})
        
        # Find extreme cases
        detailed = data.get("detailed_analysis", {})
        
        longest_lifespan = None
        highest_frequency = None
        most_rhythmic = None
        
        for seed, analysis in detailed.items():
            if analysis.get("status") == "active":
                if longest_lifespan is None or analysis["lifespan"] > longest_lifespan["lifespan"]:
                    longest_lifespan = {"seed": seed, "lifespan": analysis["lifespan"]}
                
                if highest_frequency is None or analysis["activation_frequency"] > highest_frequency["frequency"]:
                    highest_frequency = {"seed": seed, "frequency": analysis["activation_frequency"]}
                
                if most_rhythmic is None or analysis["rhythm_score"] > most_rhythmic["score"]:
                    most_rhythmic = {"seed": seed, "score": analysis["rhythm_score"], 
                                   "period": analysis["detected_period"]}
        
        return {
            "total_seeds": len(classifications),
            "distribution": distribution,
            "extremes": {
                "longest_lifespan": longest_lifespan,
                "highest_frequency": highest_frequency,
                "most_rhythmic": most_rhythmic
            },
            "last_analysis": data.get("analysis_timestamp")
        }


# Example usage
if __name__ == "__main__":
    calculator = TemporalFieldCalculator()
    
    # Test bloom log with different temporal patterns
    test_bloom_log = [
        # Bursty pattern
        {
            "bloom_id": "bloom_001",
            "activation_ticks": [100, 102, 104, 106, 108, 110],
            "semantic_seed": "urgency_seed_1",
            "entropy_trace": [0.8, 0.6, 0.9, 0.5, 0.7, 0.85]
        },
        {
            "bloom_id": "bloom_002",
            "activation_ticks": [112, 114, 116],
            "semantic_seed": "urgency_seed_1",
            "entropy_trace": [0.7, 0.9, 0.6]
        },
        # Slow burn pattern
        {
            "bloom_id": "bloom_003",
            "activation_ticks": [100, 200, 300, 400, 500, 600, 700, 800],
            "semantic_seed": "patience_seed_2",
            "entropy_trace": [0.3, 0.35, 0.32, 0.31, 0.33, 0.34, 0.32, 0.33]
        },
        # Frozen pattern
        {
            "bloom_id": "bloom_004",
            "activation_ticks": [100],
            "semantic_seed": "forgotten_seed_3",
            "entropy_trace": [0.2]
        },
        # Recursive rhythm pattern
        {
            "bloom_id": "bloom_005",
            "activation_ticks": [100, 150, 200, 250, 300, 350, 400, 450, 500],
            "semantic_seed": "cycle_seed_4",
            "entropy_trace": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        }
    ]
    
    # Calculate temporal fields
    result = calculator.calculate_temporal_fields(test_bloom_log)
    print("Temporal Field Classifications:")
    print(json.dumps(result, indent=2))
    
    # Get summary
    summary = calculator.get_temporal_summary()
    print("\nTemporal Field Summary:")
    print(json.dumps(summary, indent=2))