#!/usr/bin/env python3
"""
entropy_analyzer.py - Entropy Volatility Analysis for DAWN
Monitors entropy patterns, identifies hot blooms, and predicts chaotic behavior.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from collections import deque, defaultdict
import statistics
import json
from scipy import stats
from scipy.signal import find_peaks


@dataclass
class EntropySample:
    """Single entropy measurement"""
    bloom_id: str
    entropy: float
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            'bloom_id': self.bloom_id,
            'entropy': self.entropy,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class EntropyProfile:
    """Statistical profile of a bloom's entropy behavior"""
    bloom_id: str
    mean: float = 0.0
    variance: float = 0.0
    std_dev: float = 0.0
    min_entropy: float = 1.0
    max_entropy: float = 0.0
    trend: str = 'stable'  # 'increasing', 'decreasing', 'oscillating', 'stable'
    volatility_score: float = 0.0
    last_sample_time: Optional[datetime] = None
    sample_count: int = 0
    
    
class EntropyAnalyzer:
    """
    Analyzes entropy patterns to predict chaotic behavior and identify volatile blooms.
    """
    
    def __init__(self, max_samples_per_bloom: int = 1000, 
                 volatility_window: int = 50,
                 chaos_threshold: float = 0.7):
        """
        Initialize the entropy analyzer.
        
        Args:
            max_samples_per_bloom: Maximum samples to keep per bloom
            volatility_window: Window size for volatility calculations
            chaos_threshold: Threshold for chaos prediction (0-1)
        """
        # Sample storage
        self.samples: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_samples_per_bloom))
        self.profiles: Dict[str, EntropyProfile] = {}
        
        # Configuration
        self.max_samples = max_samples_per_bloom
        self.volatility_window = volatility_window
        self.chaos_threshold = chaos_threshold
        
        # Global statistics
        self.global_entropy_mean = 0.5
        self.global_entropy_std = 0.15
        self.total_samples = 0
        
        # Hot bloom tracking
        self.hot_blooms: Set[str] = set()
        self.cooling_blooms: Set[str] = set()
        
        # Chaos prediction cache
        self.chaos_predictions: Dict[str, float] = {}
        self.last_prediction_update = datetime.now()
        
    def add_entropy_sample(self, bloom_id: str, entropy: float) -> EntropyProfile:
        """
        Add an entropy sample for a bloom.
        
        Args:
            bloom_id: ID of the bloom
            entropy: Entropy value (0.0 - 1.0)
            
        Returns:
            Updated entropy profile for the bloom
        """
        # Validate entropy
        entropy = np.clip(entropy, 0.0, 1.0)
        
        # Create sample
        sample = EntropySample(bloom_id=bloom_id, entropy=entropy)
        self.samples[bloom_id].append(sample)
        
        # Update profile
        profile = self._update_profile(bloom_id)
        
        # Update global statistics
        self.total_samples += 1
        self._update_global_stats()
        
        # Check for hot/cooling status
        self._update_temperature_status(bloom_id, profile)
        
        # Invalidate chaos predictions cache if needed
        if (datetime.now() - self.last_prediction_update).seconds > 60:
            self.chaos_predictions.clear()
            self.last_prediction_update = datetime.now()
        
        return profile
    
    def get_entropy_variance(self, bloom_id: str) -> float:
        """
        Get the entropy variance for a bloom.
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            Variance of entropy samples (0 if insufficient data)
        """
        if bloom_id not in self.profiles:
            return 0.0
        
        return self.profiles[bloom_id].variance
    
    def get_hot_blooms(self, threshold: float = 0.7) -> List[Tuple[str, float]]:
        """
        Get blooms with high entropy above threshold.
        
        Args:
            threshold: Minimum entropy level (0.0 - 1.0)
            
        Returns:
            List of (bloom_id, current_entropy) tuples sorted by entropy
        """
        hot_blooms = []
        
        for bloom_id, profile in self.profiles.items():
            if bloom_id not in self.samples or not self.samples[bloom_id]:
                continue
                
            # Get most recent entropy
            recent_entropy = self.samples[bloom_id][-1].entropy
            
            if recent_entropy >= threshold:
                hot_blooms.append((bloom_id, recent_entropy))
        
        # Sort by entropy (highest first)
        hot_blooms.sort(key=lambda x: x[1], reverse=True)
        
        return hot_blooms
    
    def recommend_stabilization(self) -> List[str]:
        """
        Recommend blooms likely to rebloom chaotically based on entropy patterns.
        
        Returns:
            List of bloom IDs at risk of chaotic reblooming
        """
        at_risk_blooms = []
        
        for bloom_id, profile in self.profiles.items():
            if bloom_id not in self.samples or len(self.samples[bloom_id]) < 10:
                continue
            
            # Calculate chaos score
            chaos_score = self._calculate_chaos_score(bloom_id)
            
            # Cache the prediction
            self.chaos_predictions[bloom_id] = chaos_score
            
            # Add to at-risk list if above threshold
            if chaos_score >= self.chaos_threshold:
                at_risk_blooms.append(bloom_id)
        
        # Sort by chaos score (highest risk first)
        at_risk_blooms.sort(
            key=lambda bid: self.chaos_predictions.get(bid, 0), 
            reverse=True
        )
        
        return at_risk_blooms
    
    def get_entropy_trajectory(self, bloom_id: str, 
                              window_size: Optional[int] = None) -> List[Tuple[datetime, float]]:
        """
        Get entropy trajectory over time.
        
        Args:
            bloom_id: ID of the bloom
            window_size: Number of recent samples (None for all)
            
        Returns:
            List of (timestamp, entropy) tuples
        """
        if bloom_id not in self.samples:
            return []
        
        samples = list(self.samples[bloom_id])
        if window_size:
            samples = samples[-window_size:]
        
        return [(s.timestamp, s.entropy) for s in samples]
    
    def get_entropy_phase_portrait(self, bloom_id: str) -> Dict:
        """
        Generate phase portrait data for entropy dynamics.
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            Phase portrait data including entropy vs rate of change
        """
        if bloom_id not in self.samples or len(self.samples[bloom_id]) < 3:
            return {'error': 'Insufficient data'}
        
        samples = list(self.samples[bloom_id])
        entropies = [s.entropy for s in samples]
        
        # Calculate rate of change
        rates = []
        for i in range(1, len(entropies)):
            time_delta = (samples[i].timestamp - samples[i-1].timestamp).total_seconds()
            if time_delta > 0:
                rate = (entropies[i] - entropies[i-1]) / time_delta
                rates.append(rate)
            else:
                rates.append(0.0)
        
        # Create phase portrait data
        portrait = {
            'entropy': entropies[1:],  # Skip first since no rate
            'rate_of_change': rates,
            'trajectory_length': len(rates),
            'phase_space_area': self._calculate_phase_space_area(entropies[1:], rates)
        }
        
        return portrait
    
    def detect_entropy_anomalies(self, bloom_id: str, 
                                z_score_threshold: float = 2.5) -> List[Dict]:
        """
        Detect anomalous entropy values using statistical methods.
        
        Args:
            bloom_id: ID of the bloom
            z_score_threshold: Z-score threshold for anomaly detection
            
        Returns:
            List of anomaly dictionaries with timestamp and severity
        """
        if bloom_id not in self.samples or len(self.samples[bloom_id]) < 20:
            return []
        
        samples = list(self.samples[bloom_id])
        entropies = [s.entropy for s in samples]
        
        # Calculate z-scores
        mean = np.mean(entropies)
        std = np.std(entropies)
        
        if std == 0:
            return []
        
        anomalies = []
        for i, (sample, entropy) in enumerate(zip(samples, entropies)):
            z_score = abs((entropy - mean) / std)
            
            if z_score > z_score_threshold:
                anomalies.append({
                    'timestamp': sample.timestamp,
                    'entropy': entropy,
                    'z_score': z_score,
                    'severity': 'high' if z_score > 3.5 else 'medium',
                    'type': 'spike' if entropy > mean else 'drop'
                })
        
        return anomalies
    
    def get_entropy_correlations(self, bloom_ids: List[str]) -> Dict[Tuple[str, str], float]:
        """
        Calculate entropy correlations between multiple blooms.
        
        Args:
            bloom_ids: List of bloom IDs to correlate
            
        Returns:
            Dictionary mapping bloom ID pairs to correlation coefficients
        """
        correlations = {}
        
        for i in range(len(bloom_ids)):
            for j in range(i + 1, len(bloom_ids)):
                bloom1, bloom2 = bloom_ids[i], bloom_ids[j]
                
                if bloom1 not in self.samples or bloom2 not in self.samples:
                    continue
                
                # Get overlapping time periods
                samples1 = list(self.samples[bloom1])
                samples2 = list(self.samples[bloom2])
                
                if len(samples1) < 10 or len(samples2) < 10:
                    continue
                
                # Simple correlation using recent samples
                recent_size = min(50, len(samples1), len(samples2))
                entropy1 = [s.entropy for s in samples1[-recent_size:]]
                entropy2 = [s.entropy for s in samples2[-recent_size:]]
                
                if len(entropy1) == len(entropy2):
                    corr = np.corrcoef(entropy1, entropy2)[0, 1]
                    correlations[(bloom1, bloom2)] = corr
        
        return correlations
    
    def predict_entropy_future(self, bloom_id: str, steps: int = 5) -> List[float]:
        """
        Predict future entropy values using simple time series forecasting.
        
        Args:
            bloom_id: ID of the bloom
            steps: Number of future steps to predict
            
        Returns:
            List of predicted entropy values
        """
        if bloom_id not in self.samples or len(self.samples[bloom_id]) < 20:
            return []
        
        samples = list(self.samples[bloom_id])
        entropies = [s.entropy for s in samples]
        
        # Simple linear regression for trend
        x = np.arange(len(entropies))
        slope, intercept, _, _, _ = stats.linregress(x, entropies)
        
        # Add some noise based on historical volatility
        volatility = np.std(entropies)
        
        predictions = []
        last_x = len(entropies) - 1
        
        for i in range(1, steps + 1):
            # Linear prediction with bounded noise
            pred = slope * (last_x + i) + intercept
            noise = np.random.normal(0, volatility * 0.3)
            pred_with_noise = np.clip(pred + noise, 0.0, 1.0)
            predictions.append(pred_with_noise)
        
        return predictions
    
    def get_stability_report(self, bloom_id: str) -> Dict:
        """
        Generate comprehensive stability report for a bloom.
        
        Args:
            bloom_id: ID of the bloom
            
        Returns:
            Detailed stability analysis
        """
        if bloom_id not in self.profiles:
            return {'error': 'No data available'}
        
        profile = self.profiles[bloom_id]
        samples = list(self.samples[bloom_id]) if bloom_id in self.samples else []
        
        report = {
            'bloom_id': bloom_id,
            'profile': {
                'mean_entropy': profile.mean,
                'variance': profile.variance,
                'std_dev': profile.std_dev,
                'range': (profile.min_entropy, profile.max_entropy),
                'trend': profile.trend,
                'volatility_score': profile.volatility_score,
                'sample_count': profile.sample_count
            },
            'stability_assessment': self._assess_stability(profile),
            'risk_factors': self._identify_risk_factors(bloom_id),
            'recommendations': self._generate_recommendations(bloom_id, profile)
        }
        
        # Add recent behavior
        if samples:
            recent_window = min(20, len(samples))
            recent_samples = samples[-recent_window:]
            recent_entropies = [s.entropy for s in recent_samples]
            
            report['recent_behavior'] = {
                'mean': np.mean(recent_entropies),
                'trend': 'increasing' if recent_entropies[-1] > recent_entropies[0] else 'decreasing',
                'volatility': np.std(recent_entropies)
            }
        
        return report
    
    def _update_profile(self, bloom_id: str) -> EntropyProfile:
        """Update entropy profile for a bloom"""
        samples = list(self.samples[bloom_id])
        
        if not samples:
            return EntropyProfile(bloom_id=bloom_id)
        
        entropies = [s.entropy for s in samples]
        
        # Calculate statistics
        profile = EntropyProfile(
            bloom_id=bloom_id,
            mean=np.mean(entropies),
            variance=np.var(entropies),
            std_dev=np.std(entropies),
            min_entropy=min(entropies),
            max_entropy=max(entropies),
            last_sample_time=samples[-1].timestamp,
            sample_count=len(samples)
        )
        
        # Determine trend
        if len(samples) >= 10:
            recent = entropies[-10:]
            x = np.arange(len(recent))
            slope, _, _, _, _ = stats.linregress(x, recent)
            
            if abs(slope) < 0.01:
                profile.trend = 'stable'
            elif slope > 0.01:
                profile.trend = 'increasing'
            else:
                profile.trend = 'decreasing'
            
            # Check for oscillation
            if self._detect_oscillation(recent):
                profile.trend = 'oscillating'
        
        # Calculate volatility score
        if len(samples) >= self.volatility_window:
            window_samples = entropies[-self.volatility_window:]
            profile.volatility_score = self._calculate_volatility_score(window_samples)
        
        self.profiles[bloom_id] = profile
        return profile
    
    def _calculate_chaos_score(self, bloom_id: str) -> float:
        """Calculate chaos prediction score for a bloom"""
        if bloom_id not in self.profiles:
            return 0.0
        
        profile = self.profiles[bloom_id]
        samples = list(self.samples[bloom_id])
        
        if len(samples) < 20:
            return 0.0
        
        # Factors contributing to chaos
        factors = []
        
        # 1. High volatility
        factors.append(profile.volatility_score)
        
        # 2. High mean entropy
        factors.append(profile.mean)
        
        # 3. Oscillating behavior
        if profile.trend == 'oscillating':
            factors.append(0.8)
        else:
            factors.append(0.2)
        
        # 4. Recent acceleration
        recent_entropies = [s.entropy for s in samples[-10:]]
        if len(recent_entropies) >= 3:
            accel = self._calculate_acceleration(recent_entropies)
            factors.append(min(abs(accel) * 5, 1.0))
        
        # 5. Anomaly frequency
        anomalies = self.detect_entropy_anomalies(bloom_id)
        anomaly_rate = len(anomalies) / len(samples)
        factors.append(min(anomaly_rate * 10, 1.0))
        
        # Weighted combination
        weights = [0.3, 0.2, 0.2, 0.15, 0.15]
        chaos_score = sum(f * w for f, w in zip(factors, weights))
        
        return min(chaos_score, 1.0)
    
    def _calculate_volatility_score(self, entropy_values: List[float]) -> float:
        """Calculate volatility score from entropy values"""
        if len(entropy_values) < 2:
            return 0.0
        
        # Calculate returns (changes)
        returns = [entropy_values[i] - entropy_values[i-1] 
                  for i in range(1, len(entropy_values))]
        
        # Volatility is standard deviation of returns
        volatility = np.std(returns)
        
        # Normalize to 0-1 scale (assuming max reasonable volatility is 0.2)
        normalized = min(volatility / 0.2, 1.0)
        
        return normalized
    
    def _detect_oscillation(self, values: List[float]) -> bool:
        """Detect oscillating pattern in values"""
        if len(values) < 5:
            return False
        
        # Count sign changes in differences
        diffs = [values[i] - values[i-1] for i in range(1, len(values))]
        sign_changes = sum(1 for i in range(1, len(diffs)) 
                          if diffs[i] * diffs[i-1] < 0)
        
        # High frequency of sign changes indicates oscillation
        return sign_changes > len(diffs) * 0.6
    
    def _calculate_acceleration(self, values: List[float]) -> float:
        """Calculate acceleration (second derivative) of values"""
        if len(values) < 3:
            return 0.0
        
        # First derivative (velocity)
        velocities = [values[i] - values[i-1] for i in range(1, len(values))]
        
        # Second derivative (acceleration)
        accelerations = [velocities[i] - velocities[i-1] 
                        for i in range(1, len(velocities))]
        
        return np.mean(accelerations) if accelerations else 0.0
    
    def _calculate_phase_space_area(self, entropies: List[float], 
                                   rates: List[float]) -> float:
        """Calculate area covered in phase space"""
        if len(entropies) < 3:
            return 0.0
        
        # Use convex hull area as proxy for phase space coverage
        points = np.column_stack((entropies, rates))
        
        # Simple rectangular area estimation
        e_range = max(entropies) - min(entropies)
        r_range = max(rates) - min(rates) if rates else 0
        
        return e_range * r_range
    
    def _update_temperature_status(self, bloom_id: str, profile: EntropyProfile):
        """Update hot/cooling bloom status"""
        if profile.sample_count < 5:
            return
        
        recent_entropy = self.samples[bloom_id][-1].entropy
        
        # Hot bloom criteria
        if recent_entropy > 0.7 and profile.volatility_score > 0.5:
            self.hot_blooms.add(bloom_id)
            if bloom_id in self.cooling_blooms:
                self.cooling_blooms.remove(bloom_id)
        
        # Cooling bloom criteria
        elif bloom_id in self.hot_blooms and recent_entropy < 0.5:
            self.hot_blooms.remove(bloom_id)
            self.cooling_blooms.add(bloom_id)
        
        # Remove from cooling if stabilized
        elif bloom_id in self.cooling_blooms and profile.volatility_score < 0.2:
            self.cooling_blooms.remove(bloom_id)
    
    def _update_global_stats(self):
        """Update global entropy statistics"""
        all_entropies = []
        for samples in self.samples.values():
            all_entropies.extend([s.entropy for s in samples])
        
        if all_entropies:
            self.global_entropy_mean = np.mean(all_entropies)
            self.global_entropy_std = np.std(all_entropies)
    
    def _assess_stability(self, profile: EntropyProfile) -> str:
        """Assess stability level of a bloom"""
        if profile.volatility_score < 0.2 and profile.std_dev < 0.1:
            return 'highly_stable'
        elif profile.volatility_score < 0.4 and profile.std_dev < 0.2:
            return 'stable'
        elif profile.volatility_score < 0.6:
            return 'moderately_stable'
        elif profile.volatility_score < 0.8:
            return 'unstable'
        else:
            return 'highly_unstable'
    
    def _identify_risk_factors(self, bloom_id: str) -> List[str]:
        """Identify risk factors for a bloom"""
        if bloom_id not in self.profiles:
            return []
        
        profile = self.profiles[bloom_id]
        risks = []
        
        if profile.mean > 0.8:
            risks.append('high_baseline_entropy')
        
        if profile.volatility_score > 0.7:
            risks.append('extreme_volatility')
        
        if profile.trend == 'oscillating':
            risks.append('oscillating_pattern')
        
        if profile.max_entropy > 0.95:
            risks.append('near_maximum_entropy')
        
        if bloom_id in self.hot_blooms:
            risks.append('currently_hot')
        
        # Check for recent anomalies
        anomalies = self.detect_entropy_anomalies(bloom_id)
        if len(anomalies) > 3:
            risks.append('frequent_anomalies')
        
        return risks
    
    def _generate_recommendations(self, bloom_id: str, 
                                 profile: EntropyProfile) -> List[str]:
        """Generate stabilization recommendations"""
        recommendations = []
        
        if profile.volatility_score > 0.7:
            recommendations.append('Apply entropy dampening to reduce volatility')
        
        if profile.mean > 0.8:
            recommendations.append('Reduce baseline entropy through cooling cycles')
        
        if profile.trend == 'increasing':
            recommendations.append('Monitor for entropy cascade - consider early intervention')
        
        if profile.trend == 'oscillating':
            recommendations.append('Stabilize oscillations with phase-locked reblooming')
        
        if bloom_id in self.chaos_predictions and self.chaos_predictions[bloom_id] > 0.8:
            recommendations.append('HIGH PRIORITY: Immediate stabilization recommended')
        
        return recommendations
    
    def save_to_file(self, filepath: str):
        """Save analyzer state to file"""
        data = {
            'samples': {
                bloom_id: [s.to_dict() for s in samples]
                for bloom_id, samples in self.samples.items()
            },
            'config': {
                'max_samples': self.max_samples,
                'volatility_window': self.volatility_window,
                'chaos_threshold': self.chaos_threshold
            },
            'metadata': {
                'total_samples': self.total_samples,
                'saved_at': datetime.now().isoformat()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# Example usage and testing
if __name__ == "__main__":
    # Create analyzer
    analyzer = EntropyAnalyzer(volatility_window=20, chaos_threshold=0.7)
    
    # Simulate entropy samples for different bloom patterns
    import random
    import time
    
    # Stable bloom
    for i in range(50):
        analyzer.add_entropy_sample("bloom_stable", 0.3 + random.uniform(-0.05, 0.05))
        time.sleep(0.01)
    
    # Volatile bloom
    for i in range(50):
        base = 0.5 + 0.3 * np.sin(i * 0.3)
        analyzer.add_entropy_sample("bloom_volatile", base + random.uniform(-0.2, 0.2))
        time.sleep(0.01)
    
    # Hot bloom
    for i in range(50):
        analyzer.add_entropy_sample("bloom_hot", 0.8 + random.uniform(-0.1, 0.15))
        time.sleep(0.01)
    
    # Chaotic bloom
    for i in range(50):
        if i % 10 < 5:
            entropy = 0.2 + random.uniform(0, 0.1)
        else:
            entropy = 0.8 + random.uniform(-0.1, 0.1)
        analyzer.add_entropy_sample("bloom_chaotic", entropy)
        time.sleep(0.01)
    
    print("=== Entropy Analysis Results ===\n")
    
    # Get hot blooms
    print("Hot Blooms (threshold=0.7):")
    for bloom_id, entropy in analyzer.get_hot_blooms(0.7):
        print(f"  {bloom_id}: {entropy:.3f}")
    
    # Get variance
    print("\nEntropy Variance:")
    for bloom_id in ["bloom_stable", "bloom_volatile", "bloom_hot", "bloom_chaotic"]:
        variance = analyzer.get_entropy_variance(bloom_id)
        print(f"  {bloom_id}: {variance:.4f}")
    
    # Chaos predictions
    print("\nChaos Risk Assessment:")
    at_risk = analyzer.recommend_stabilization()
    for bloom_id in at_risk:
        score = analyzer.chaos_predictions.get(bloom_id, 0)
        print(f"  {bloom_id}: chaos score = {score:.3f}")
    
    # Stability reports
    print("\nStability Reports:")
    for bloom_id in ["bloom_stable", "bloom_chaotic"]:
        report = analyzer.get_stability_report(bloom_id)
        print(f"\n{bloom_id}:")
        print(f"  Stability: {report.get('stability_assessment', 'unknown')}")
        print(f"  Risk Factors: {report.get('risk_factors', [])}")
        print(f"  Recommendations: {report.get('recommendations', [])}")
    
    # Entropy correlations
    print("\nEntropy Correlations:")
    correlations = analyzer.get_entropy_correlations(
        ["bloom_stable", "bloom_volatile", "bloom_hot", "bloom_chaotic"]
    )
    for (b1, b2), corr in correlations.items():
        print(f"  {b1} <-> {b2}: {corr:.3f}")