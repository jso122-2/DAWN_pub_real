"""
Growth is not always good. Sometimes the only mercy is letting a branch fall before it shadows the whole tree.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple


class PruningLogic:
    """Memory hygiene through selective pruning of semantic clusters."""
    
    def __init__(self):
        self.log_path = Path("memory/mycelium/logs/pruning_events.log")
        self.logger = self._setup_logger()
        
        # Pruning thresholds
        self.thresholds = {
            "trust_minimum": 0.4,
            "density_maximum": 1.5,
            "age_maximum": 3000
        }
        
        # Track pruning statistics
        self.stats = {
            "total_pruned": 0,
            "total_preserved": 0,
            "pruning_sessions": 0
        }
    
    def _setup_logger(self):
        """Initialize the pruning events logger."""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger("pruning_logic")
        logger.setLevel(logging.INFO)
        
        # Create file handler
        handler = logging.FileHandler(self.log_path)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def prune_semantic_clusters(self, bloom_clusters: List[Dict]) -> Dict[str, List[str]]:
        """
        Prune low-trust or overgrown semantic regions.
        
        Args:
            bloom_clusters: List of cluster dictionaries containing:
                - cluster_id: str
                - avg_trust: float
                - density: float
                - age: int (average tick age)
                - rebloom_count: int
        
        Returns:
            Dictionary with lists of pruned and preserved cluster_ids
        """
        pruned_clusters = []
        preserved_clusters = []
        pruning_reasons = {}
        
        self.stats["pruning_sessions"] += 1
        session_start = datetime.utcnow()
        
        for cluster in bloom_clusters:
            cluster_id = cluster['cluster_id']
            should_prune, reasons = self._evaluate_cluster(cluster)
            
            if should_prune:
                pruned_clusters.append(cluster_id)
                pruning_reasons[cluster_id] = reasons
                self._log_pruning_event(cluster, reasons, session_start)
            else:
                preserved_clusters.append(cluster_id)
        
        # Update statistics
        self.stats["total_pruned"] += len(pruned_clusters)
        self.stats["total_preserved"] += len(preserved_clusters)
        
        # Log session summary
        self._log_session_summary(
            len(bloom_clusters),
            len(pruned_clusters),
            len(preserved_clusters),
            session_start
        )
        
        return {
            "pruned_clusters": pruned_clusters,
            "preserved_clusters": preserved_clusters,
            "pruning_reasons": pruning_reasons,
            "session_stats": {
                "total_evaluated": len(bloom_clusters),
                "pruned_count": len(pruned_clusters),
                "preserved_count": len(preserved_clusters),
                "prune_rate": len(pruned_clusters) / len(bloom_clusters) if bloom_clusters else 0
            }
        }
    
    def _evaluate_cluster(self, cluster: Dict) -> Tuple[bool, List[str]]:
        """
        Evaluate whether a cluster should be pruned.
        
        Returns:
            Tuple of (should_prune, list_of_reasons)
        """
        reasons = []
        
        # Check trust score
        if cluster['avg_trust'] < self.thresholds['trust_minimum']:
            reasons.append(f"LOW_TRUST: {cluster['avg_trust']:.3f} < {self.thresholds['trust_minimum']}")
        
        # Check density
        if cluster['density'] > self.thresholds['density_maximum']:
            reasons.append(f"OVERGROWN: density {cluster['density']:.3f} > {self.thresholds['density_maximum']}")
        
        # Check age
        if cluster['age'] > self.thresholds['age_maximum']:
            reasons.append(f"ANCIENT: age {cluster['age']} > {self.thresholds['age_maximum']}")
        
        # Special case: High rebloom count with low trust is especially problematic
        if cluster['rebloom_count'] > 5 and cluster['avg_trust'] < 0.5:
            reasons.append(f"UNSTABLE_REBLOOM: {cluster['rebloom_count']} reblooms with trust {cluster['avg_trust']:.3f}")
        
        should_prune = len(reasons) > 0
        
        return should_prune, reasons
    
    def _log_pruning_event(self, cluster: Dict, reasons: List[str], session_start: datetime):
        """Log individual pruning event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_start": session_start.isoformat(),
            "event_type": "PRUNE",
            "cluster_id": cluster['cluster_id'],
            "cluster_metrics": {
                "avg_trust": cluster['avg_trust'],
                "density": cluster['density'],
                "age": cluster['age'],
                "rebloom_count": cluster['rebloom_count']
            },
            "reasons": reasons
        }
        
        self.logger.info(json.dumps(event))
    
    def _log_session_summary(self, total: int, pruned: int, preserved: int, 
                           session_start: datetime):
        """Log pruning session summary."""
        duration = (datetime.utcnow() - session_start).total_seconds()
        
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_start": session_start.isoformat(),
            "event_type": "SESSION_SUMMARY",
            "duration_seconds": duration,
            "clusters_evaluated": total,
            "clusters_pruned": pruned,
            "clusters_preserved": preserved,
            "prune_rate": pruned / total if total > 0 else 0,
            "cumulative_stats": self.stats
        }
        
        self.logger.info(json.dumps(summary))
    
    def get_pruning_health_metrics(self, bloom_clusters: List[Dict]) -> Dict:
        """Calculate health metrics for the semantic field."""
        if not bloom_clusters:
            return {
                "field_health": "EMPTY",
                "avg_trust": 0.0,
                "avg_density": 0.0,
                "avg_age": 0,
                "at_risk_count": 0,
                "recommendations": ["No clusters to evaluate"]
            }
        
        # Calculate averages
        avg_trust = sum(c['avg_trust'] for c in bloom_clusters) / len(bloom_clusters)
        avg_density = sum(c['density'] for c in bloom_clusters) / len(bloom_clusters)
        avg_age = sum(c['age'] for c in bloom_clusters) / len(bloom_clusters)
        
        # Count at-risk clusters
        at_risk = 0
        for cluster in bloom_clusters:
            should_prune, _ = self._evaluate_cluster(cluster)
            if should_prune:
                at_risk += 1
        
        # Determine overall health
        if at_risk / len(bloom_clusters) > 0.5:
            field_health = "CRITICAL"
            recommendations = [
                "Over 50% of clusters need pruning",
                "Consider emergency semantic reset",
                "Review trust calculation parameters"
            ]
        elif at_risk / len(bloom_clusters) > 0.3:
            field_health = "DEGRADED"
            recommendations = [
                "Significant pruning needed",
                "Monitor rebloom patterns",
                "Increase trust reinforcement"
            ]
        elif avg_trust < 0.6:
            field_health = "UNSTABLE"
            recommendations = [
                "Low average trust across field",
                "Focus on high-quality bloom generation",
                "Reduce semantic drift"
            ]
        else:
            field_health = "HEALTHY"
            recommendations = [
                "Field in good condition",
                "Continue regular maintenance"
            ]
        
        return {
            "field_health": field_health,
            "avg_trust": round(avg_trust, 3),
            "avg_density": round(avg_density, 3),
            "avg_age": int(avg_age),
            "at_risk_count": at_risk,
            "at_risk_percentage": round(at_risk / len(bloom_clusters) * 100, 1),
            "recommendations": recommendations
        }
    
    def suggest_adaptive_thresholds(self, historical_metrics: List[Dict]) -> Dict:
        """Suggest threshold adjustments based on pruning history."""
        if len(historical_metrics) < 10:
            return {
                "suggestion": "Insufficient data",
                "current_thresholds": self.thresholds
            }
        
        # Analyze recent pruning rates
        recent_rates = [m.get('prune_rate', 0) for m in historical_metrics[-10:]]
        avg_prune_rate = sum(recent_rates) / len(recent_rates)
        
        suggestions = {}
        
        if avg_prune_rate > 0.4:
            # Too aggressive - relax thresholds
            suggestions = {
                "trust_minimum": self.thresholds["trust_minimum"] * 0.9,
                "density_maximum": self.thresholds["density_maximum"] * 1.1,
                "age_maximum": int(self.thresholds["age_maximum"] * 1.2)
            }
            reason = "High prune rate - relaxing thresholds"
        elif avg_prune_rate < 0.1:
            # Too conservative - tighten thresholds
            suggestions = {
                "trust_minimum": min(0.6, self.thresholds["trust_minimum"] * 1.1),
                "density_maximum": self.thresholds["density_maximum"] * 0.9,
                "age_maximum": int(self.thresholds["age_maximum"] * 0.8)
            }
            reason = "Low prune rate - tightening thresholds"
        else:
            suggestions = self.thresholds.copy()
            reason = "Thresholds balanced"
        
        return {
            "suggestion": reason,
            "current_thresholds": self.thresholds,
            "suggested_thresholds": suggestions,
            "recent_avg_prune_rate": round(avg_prune_rate, 3)
        }


# Example usage
if __name__ == "__main__":
    pruner = PruningLogic()
    
    # Test clusters
    test_clusters = [
        {
            "cluster_id": "cluster_001",
            "avg_trust": 0.3,  # Low trust
            "density": 1.2,
            "age": 2500,
            "rebloom_count": 7
        },
        {
            "cluster_id": "cluster_002",
            "avg_trust": 0.8,
            "density": 1.7,  # Overgrown
            "age": 1000,
            "rebloom_count": 2
        },
        {
            "cluster_id": "cluster_003",
            "avg_trust": 0.6,
            "density": 0.9,
            "age": 3500,  # Ancient
            "rebloom_count": 3
        },
        {
            "cluster_id": "cluster_004",
            "avg_trust": 0.7,
            "density": 1.1,
            "age": 500,
            "rebloom_count": 1
        }
    ]
    
    # Perform pruning
    result = pruner.prune_semantic_clusters(test_clusters)
    print("Pruning Results:")
    print(json.dumps(result, indent=2))
    
    # Get health metrics
    health = pruner.get_pruning_health_metrics(test_clusters)
    print("\nField Health Metrics:")
    print(json.dumps(health, indent=2))