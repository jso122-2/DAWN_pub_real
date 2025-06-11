"""
Unified Bloom Maintenance System
Handles pruning, cleaning, repair, and health monitoring for the DAWN bloom system
"""

import os
import json
import shutil
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np

# Configuration
BLOOM_BASE_DIR = "juliet_flowers"
BLOOM_METADATA_DIR = "juliet_flowers/bloom_metadata"
BLOOM_REGISTRY = "bloom_registry.json"
MYCELIUM_LOGS = "mycelium_logs"
MEMORY_BLOOMS_DIR = "bloom/memory_blooms"


class BloomPruner:
    """Memory hygiene through selective pruning of semantic clusters"""
    
    def __init__(self):
        self.log_path = Path("memory/mycelium/logs/pruning_events.log")
        self.logger = self._setup_logger()
        
        # Pruning thresholds
        self.thresholds = {
            "trust_minimum": 0.4,
            "density_maximum": 1.5,
            "age_maximum": 3000,
            "entropy_maximum": 0.75,
            "suppression_limit": 2,
            "lineage_depth_maximum": 12
        }
        
        # Statistics
        self.stats = {
            "total_pruned": 0,
            "total_preserved": 0,
            "pruning_sessions": 0,
            "suppressed_blooms": 0
        }
        
    def _setup_logger(self) -> logging.Logger:
        """Initialize pruning events logger"""
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger = logging.getLogger("bloom_pruner")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler(self.log_path)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    def prune_semantic_clusters(self, bloom_clusters: List[Dict]) -> Dict:
        """Prune low-trust or overgrown semantic regions"""
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
        """Evaluate whether a cluster should be pruned"""
        reasons = []
        
        # Trust check
        if cluster.get('avg_trust', 1.0) < self.thresholds['trust_minimum']:
            reasons.append(f"LOW_TRUST: {cluster['avg_trust']:.3f} < {self.thresholds['trust_minimum']}")
            
        # Density check
        if cluster.get('density', 0) > self.thresholds['density_maximum']:
            reasons.append(f"OVERGROWN: density {cluster['density']:.3f} > {self.thresholds['density_maximum']}")
            
        # Age check
        if cluster.get('age', 0) > self.thresholds['age_maximum']:
            reasons.append(f"ANCIENT: age {cluster['age']} > {self.thresholds['age_maximum']}")
            
        # Entropy check
        if cluster.get('entropy', 0) > self.thresholds['entropy_maximum']:
            reasons.append(f"HIGH_ENTROPY: {cluster['entropy']:.3f} > {self.thresholds['entropy_maximum']}")
            
        # Rebloom instability
        if cluster.get('rebloom_count', 0) > 5 and cluster.get('avg_trust', 1.0) < 0.5:
            reasons.append(f"UNSTABLE_REBLOOM: {cluster['rebloom_count']} reblooms with trust {cluster['avg_trust']:.3f}")
            
        return len(reasons) > 0, reasons
        
    def suppress_bloom_if_unstable(self, bloom: Dict) -> bool:
        """Suppress bloom if unstable traits detected"""
        suppression_reasons = []
        
        # Unified accessor
        def get(key, default=None):
            return bloom.get(key, default) if isinstance(bloom, dict) else getattr(bloom, key, default)
            
        seed = get("seed_id", "unknown")
        entropy = get("entropy_score", 1.0)
        suppressions = get("suppressions", 0)
        trust = get("trust_score", 1.0)
        feedback_flags = get("feedback_flags", {})
        mood = get("mood", "undefined")
        depth = get("lineage_depth", 0)
        
        # Check suppression conditions
        if entropy > self.thresholds['entropy_maximum']:
            suppression_reasons.append("entropy_spike")
            
        if suppressions > self.thresholds['suppression_limit']:
            suppression_reasons.append("repeat_flagged")
            
        if trust < 0.3:
            suppression_reasons.append("low_trust")
            
        if feedback_flags.get("poor_conversion"):
            suppression_reasons.append("conversion_failure")
            
        if depth >= self.thresholds['lineage_depth_maximum']:
            suppression_reasons.append("drift_depth")
            
        if mood in ["anxious", "fatalistic"] and entropy > 0.7:
            suppression_reasons.append("mood_instability")
            
        # Apply suppression if needed
        if suppression_reasons:
            if isinstance(bloom, dict):
                bloom["suppressed"] = True
                bloom["suppression_reason"] = suppression_reasons
            else:
                bloom.suppressed = True
                bloom.suppression_reason = suppression_reasons
                
            self.stats["suppressed_blooms"] += 1
            self._log_suppression(seed, suppression_reasons)
            return True
            
        return False
        
    def _log_suppression(self, seed_id: str, reasons: List[str]):
        """Log bloom suppression event"""
        try:
            from owl.owl_tracer_log import owl_log
            owl_log(f"[Suppressed] 🚫 {seed_id} blocked ({', '.join(reasons)})")
        except ImportError:
            print(f"[Suppressed] 🚫 {seed_id} blocked ({', '.join(reasons)})")
            
    def _log_pruning_event(self, cluster: Dict, reasons: List[str], session_start: datetime):
        """Log individual pruning event"""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "session_start": session_start.isoformat(),
            "event_type": "PRUNE",
            "cluster_id": cluster['cluster_id'],
            "cluster_metrics": {
                "avg_trust": cluster.get('avg_trust', 0),
                "density": cluster.get('density', 0),
                "age": cluster.get('age', 0),
                "rebloom_count": cluster.get('rebloom_count', 0),
                "entropy": cluster.get('entropy', 0)
            },
            "reasons": reasons
        }
        
        self.logger.info(json.dumps(event))
        
    def _log_session_summary(self, total: int, pruned: int, preserved: int, session_start: datetime):
        """Log pruning session summary"""
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
        """Calculate health metrics for the semantic field"""
        if not bloom_clusters:
            return {
                "field_health": "EMPTY",
                "avg_trust": 0.0,
                "avg_density": 0.0,
                "avg_age": 0,
                "avg_entropy": 0.0,
                "at_risk_count": 0,
                "recommendations": ["No clusters to evaluate"]
            }
            
        # Calculate averages
        avg_trust = sum(c.get('avg_trust', 0) for c in bloom_clusters) / len(bloom_clusters)
        avg_density = sum(c.get('density', 0) for c in bloom_clusters) / len(bloom_clusters)
        avg_age = sum(c.get('age', 0) for c in bloom_clusters) / len(bloom_clusters)
        avg_entropy = sum(c.get('entropy', 0) for c in bloom_clusters) / len(bloom_clusters)
        
        # Count at-risk clusters
        at_risk = sum(1 for c in bloom_clusters if self._evaluate_cluster(c)[0])
        at_risk_percentage = at_risk / len(bloom_clusters)
        
        # Determine health status
        if at_risk_percentage > 0.5:
            field_health = "CRITICAL"
            recommendations = [
                "Over 50% of clusters need pruning",
                "Consider emergency semantic reset",
                "Review trust calculation parameters"
            ]
        elif at_risk_percentage > 0.3:
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
            "avg_entropy": round(avg_entropy, 3),
            "at_risk_count": at_risk,
            "at_risk_percentage": round(at_risk_percentage * 100, 1),
            "recommendations": recommendations
        }


class BloomCleaner:
    """Handles cleaning and maintenance of bloom directories"""
    
    def __init__(self, base_dir: str = BLOOM_BASE_DIR):
        self.base_dir = base_dir
        self.registry_path = BLOOM_REGISTRY
        
    def clean_bloom_logs(self, preserve_metadata: bool = False) -> Dict[str, int]:
        """Clean bloom directories and registry"""
        print("🧹 Cleaning bloom directories...")
        
        stats = {
            "directories_removed": 0,
            "files_removed": 0,
            "registry_cleaned": False
        }
        
        # Clean bloom directories
        if os.path.exists(self.base_dir):
            for seed in os.listdir(self.base_dir):
                path = os.path.join(self.base_dir, seed)
                
                # Skip metadata directory if preserving
                if preserve_metadata and seed == "bloom_metadata":
                    continue
                    
                if os.path.isdir(path):
                    file_count = sum(len(files) for _, _, files in os.walk(path))
                    shutil.rmtree(path)
                    print(f"❌ Removed: {path} ({file_count} files)")
                    stats["directories_removed"] += 1
                    stats["files_removed"] += file_count
                    
        # Recreate base directory
        os.makedirs(self.base_dir, exist_ok=True)
        print("✅ Bloom directory reset.")
        
        # Clean registry
        if os.path.exists(self.registry_path):
            os.remove(self.registry_path)
            print(f"🗑️ Removed bloom registry: {self.registry_path}")
            stats["registry_cleaned"] = True
            
        return stats
        
    def repair_misplaced_moods(self) -> int:
        """Repair misplaced mood folders in bloom directory structure"""
        print("🔧 Repairing misplaced mood folders...")
        repaired = 0
        
        for entry in os.listdir(self.base_dir):
            path = os.path.join(self.base_dir, entry)
            
            if os.path.isdir(path):
                files = os.listdir(path)
                
                # Check if this looks like a misplaced mood folder
                if any(f.startswith("flower-") or f.endswith(".json") for f in files):
                    # Create proper structure
                    new_path = os.path.join(self.base_dir, "unknown-agent", entry, "0")
                    os.makedirs(new_path, exist_ok=True)
                    
                    # Move files
                    for f in files:
                        src = os.path.join(path, f)
                        dst = os.path.join(new_path, f)
                        shutil.move(src, dst)
                        
                    # Remove old directory
                    os.rmdir(path)
                    print(f"[REPAIRED] Moved mood folder '{entry}' → unknown-agent/{entry}/0/")
                    repaired += 1
                    
        print(f"\n✅ Repair complete. {repaired} misplaced mood folders corrected.")
        return repaired


class BloomHealthChecker:
    """Automated health checks for bloom system integrity"""
    
    def __init__(self):
        self.fractal_path = BLOOM_BASE_DIR
        self.nutrient_path = MYCELIUM_LOGS
        self.memory_path = MEMORY_BLOOMS_DIR
        
    def check_fractal_generation(self) -> Dict[str, List[str]]:
        """Check for missing fractal images"""
        fractal_missing = []
        fractal_found = []
        
        for root, dirs, files in os.walk(self.fractal_path):
            # Find bloom files
            bloom_files = [f for f in files if f.endswith(('.txt', '.json'))]
            
            for bloom_file in bloom_files:
                base_name = os.path.splitext(bloom_file)[0]
                # Check for corresponding fractal
                fractal_exists = any(f.startswith(base_name) and f.endswith('.png') 
                                   for f in files)
                
                if fractal_exists:
                    fractal_found.append(os.path.join(root, bloom_file))
                else:
                    fractal_missing.append(os.path.join(root, bloom_file))
                    
        if fractal_missing:
            print(f"[HealthCheck] ❌ Missing fractals for {len(fractal_missing)} blooms")
        else:
            print("[HealthCheck] ✅ All fractals generated successfully")
            
        return {
            "missing": fractal_missing,
            "found": fractal_found,
            "coverage": len(fractal_found) / (len(fractal_found) + len(fractal_missing)) 
                       if (fractal_found or fractal_missing) else 1.0
        }
        
    def check_nutrient_logs(self) -> Dict[str, bool]:
        """Check nutrient log availability"""
        checks = {
            "directory_exists": False,
            "has_logs": False,
            "recent_activity": False
        }
        
        if os.path.exists(self.nutrient_path):
            checks["directory_exists"] = True
            print("[HealthCheck] ✅ Nutrient log directory found")
            
            # Check for log files
            log_files = []
            for root, dirs, files in os.walk(self.nutrient_path):
                log_files.extend([f for f in files if f.endswith(('.log', '.csv'))])
                
            if log_files:
                checks["has_logs"] = True
                print(f"[HealthCheck] ✅ Found {len(log_files)} nutrient logs")
                
                # Check for recent activity
                latest_time = 0
                for root, dirs, files in os.walk(self.nutrient_path):
                    for f in files:
                        file_path = os.path.join(root, f)
                        mod_time = os.path.getmtime(file_path)
                        latest_time = max(latest_time, mod_time)
                        
                if latest_time > 0:
                    age_hours = (datetime.now().timestamp() - latest_time) / 3600
                    if age_hours < 24:
                        checks["recent_activity"] = True
                        print(f"[HealthCheck] ✅ Recent activity: {age_hours:.1f} hours ago")
                    else:
                        print(f"[HealthCheck] ⚠️ No recent activity: {age_hours:.1f} hours ago")
            else:
                print("[HealthCheck] ❌ No nutrient logs found")
        else:
            print("[HealthCheck] ❌ Nutrient log directory missing")
            
        return checks
        
    def check_memory_integrity(self) -> Dict[str, List[str]]:
        """Check memory bloom file integrity"""
        corrupt_files = []
        healthy_files = []
        
        if not os.path.exists(self.memory_path):
            print("[HealthCheck] ⚠️ Memory blooms directory not found")
            return {"corrupt": [], "healthy": [], "missing_dir": True}
            
        for filename in os.listdir(self.memory_path):
            filepath = os.path.join(self.memory_path, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = f.read()
                    if not data:
                        raise ValueError("Empty file")
                        
                    # Try to parse as JSON if applicable
                    if filename.endswith('.json'):
                        json.loads(data)
                        
                healthy_files.append(filename)
                
            except Exception as e:
                corrupt_files.append(filename)
                print(f"[HealthCheck] ❌ Corrupt file: {filename} - {str(e)}")
                
        if corrupt_files:
            print(f"[HealthCheck] ❌ Found {len(corrupt_files)} corrupt memory blooms")
        else:
            print("[HealthCheck] ✅ All memory blooms intact")
            
        return {
            "corrupt": corrupt_files,
            "healthy": healthy_files,
            "integrity_rate": len(healthy_files) / (len(healthy_files) + len(corrupt_files))
                             if (healthy_files or corrupt_files) else 1.0
        }
        
    def run_all_checks(self) -> Dict:
        """Run all health checks and return comprehensive report"""
        print("\n🏥 Running Bloom System Health Checks")
        print("=" * 50)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "fractal_check": self.check_fractal_generation(),
            "nutrient_check": self.check_nutrient_logs(),
            "memory_check": self.check_memory_integrity()
        }
        
        # Calculate overall health score
        scores = []
        scores.append(results["fractal_check"]["coverage"])
        scores.append(1.0 if results["nutrient_check"]["has_logs"] else 0.0)
        scores.append(results["memory_check"].get("integrity_rate", 0.0))
        
        results["overall_health"] = sum(scores) / len(scores)
        results["status"] = "HEALTHY" if results["overall_health"] > 0.8 else \
                           "DEGRADED" if results["overall_health"] > 0.5 else "CRITICAL"
                           
        print(f"\n[HealthCheck] Overall Health: {results['status']} "
              f"({results['overall_health']:.1%})")
              
        return results


class BloomCITester:
    """Continuous Integration tests for bloom system"""
    
    def __init__(self):
        self.bloom_path = BLOOM_BASE_DIR
        self.tests_passed = 0
        self.tests_failed = 0
        
    def ci_test_blooms(self) -> bool:
        """Test bloom directory structure"""
        try:
            assert os.path.exists(self.bloom_path), "Bloom directory missing"
            
            blooms = [f for f in os.listdir(self.bloom_path) 
                     if os.path.isdir(os.path.join(self.bloom_path, f))]
            assert blooms, "No bloom directories found"
            
            print("[CI Test] ✅ Bloom directories exist")
            self.tests_passed += 1
            return True
            
        except AssertionError as e:
            print(f"[CI Test] ❌ Bloom test failed: {e}")
            self.tests_failed += 1
            return False
            
    def ci_test_fractals(self) -> bool:
        """Test fractal generation"""
        try:
            fractal_found = False
            
            for root, dirs, files in os.walk(self.bloom_path):
                if any(file.endswith('.png') for file in files):
                    fractal_found = True
                    break
                    
            assert fractal_found, "No fractal images found"
            print("[CI Test] ✅ Fractal images exist")
            self.tests_passed += 1
            return True
            
        except AssertionError as e:
            print(f"[CI Test] ❌ Fractal test failed: {e}")
            self.tests_failed += 1
            return False
            
    def ci_test_nutrients(self) -> bool:
        """Test nutrient logging"""
        try:
            nutrient_path = "logs/mycelium_logs"
            assert os.path.exists(nutrient_path), "Nutrient log directory missing"
            
            logs_exist = False
            for root, dirs, files in os.walk(nutrient_path):
                if any(file.endswith(('.csv', '.log')) for file in files):
                    logs_exist = True
                    break
                    
            assert logs_exist, "No nutrient logs found"
            print("[CI Test] ✅ Nutrient logs exist")
            self.tests_passed += 1
            return True
            
        except AssertionError as e:
            print(f"[CI Test] ❌ Nutrient test failed: {e}")
            self.tests_failed += 1
            return False
            
    def run_all_tests(self) -> Dict:
        """Run all CI tests"""
        print("\n🧪 Running Bloom System CI Tests")
        print("=" * 50)
        
        results = {
            "bloom_test": self.ci_test_blooms(),
            "fractal_test": self.ci_test_fractals(),
            "nutrient_test": self.ci_test_nutrients(),
            "total_passed": self.tests_passed,
            "total_failed": self.tests_failed,
            "success_rate": self.tests_passed / (self.tests_passed + self.tests_failed)
                           if (self.tests_passed + self.tests_failed) > 0 else 0
        }
        
        print(f"\n[CI Test] Summary: {self.tests_passed} passed, "
              f"{self.tests_failed} failed ({results['success_rate']:.1%} success rate)")
              
        return results


# ============== Unified Maintenance Runner ==============

def run_maintenance_cycle(
    prune_clusters: bool = True,
    clean_logs: bool = False,
    repair_structure: bool = True,
    run_health_checks: bool = True,
    run_ci_tests: bool = False
) -> Dict:
    """Run complete maintenance cycle"""
    print("🛠️ Starting Bloom Maintenance Cycle")
    print("=" * 50)
    
    results = {}
    
    # Initialize components
    pruner = BloomPruner()
    cleaner = BloomCleaner()
    health_checker = BloomHealthChecker()
    ci_tester = BloomCITester()
    
    # Run maintenance tasks
    if prune_clusters:
        print("\n1. Running semantic pruning...")
        # Example clusters - in production, load from actual data
        test_clusters = [
            {"cluster_id": f"cluster_{i:03d}", 
             "avg_trust": np.random.uniform(0.2, 0.9),
             "density": np.random.uniform(0.5, 2.0),
             "age": np.random.randint(100, 4000),
             "entropy": np.random.uniform(0.3, 0.9),
             "rebloom_count": np.random.randint(0, 10)}
            for i in range(20)
        ]
        results["pruning"] = pruner.prune_semantic_clusters(test_clusters)
        results["field_health"] = pruner.get_pruning_health_metrics(test_clusters)
        
    if clean_logs:
        print("\n2. Cleaning bloom logs...")
        results["cleaning"] = cleaner.clean_bloom_logs(preserve_metadata=True)
        
    if repair_structure:
        print("\n3. Repairing directory structure...")
        results["repairs"] = cleaner.repair_misplaced_moods()
        
    if run_health_checks:
        print("\n4. Running health checks...")
        results["health"] = health_checker.run_all_checks()
        
    if run_ci_tests:
        print("\n5. Running CI tests...")
        results["ci_tests"] = ci_tester.run_all_tests()
        
    # Summary
    print("\n✅ Maintenance cycle complete!")
    
    return results


if __name__ == "__main__":
    # Run full maintenance with all options
    results = run_maintenance_cycle(
        prune_clusters=True,
        clean_logs=False,  # Set to True to actually clean
        repair_structure=True,
        run_health_checks=True,
        run_ci_tests=True
    )
    
    print("\n📊 Maintenance Summary:")
    print(json.dumps(results, indent=2, default=str))