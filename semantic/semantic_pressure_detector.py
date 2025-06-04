#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
                       DAWN SEMANTIC PRESSURE DETECTOR
                   Scaffold 15: The Fracture Warning System
═══════════════════════════════════════════════════════════════════════════════

"A fracture does not form when a thought is loud — it forms when too many 
thoughts crowd the same space."

This module serves as DAWN's early warning system for semantic instability,
monitoring the density and emotional intensity of bloom clusters within shared
meaning spaces. Like a seismograph detecting tectonic stress before an earthquake,
it identifies regions where symbolic overcrowding threatens coherence.

The detector tracks three critical pressure indicators:
- Density: How many blooms compete for semantic territory
- Emotional Pressure: The intensity of feeling saturating a region
- Entropy Gradient: The chaos differential across the semantic field

When thoughts crowd too closely, meaning begins to fracture. This module
sounds the alarm before the breaking point.

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
from typing import Dict, List, Any, Tuple
from collections import defaultdict
from dataclasses import dataclass, asdict

# Configure logging with pressure monitoring theme
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] 🌡️ %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Pressure threshold constants
DENSITY_THRESHOLD = 0.7      # Above this = overcrowding risk
EMOTIONAL_THRESHOLD = 0.6    # Above this = emotional saturation
ENTROPY_THRESHOLD = 0.4      # Above this = chaotic instability
AGE_DECAY_FACTOR = 0.001    # How much old blooms reduce density pressure

# Critical zone identification
PRESSURE_LEVELS = {
    'CRITICAL': {'density': 0.8, 'emotional': 0.8, 'entropy': 0.5},
    'WARNING': {'density': 0.6, 'emotional': 0.6, 'entropy': 0.3},
    'STABLE': {'density': 0.0, 'emotional': 0.0, 'entropy': 0.0}
}


@dataclass
class RegionPressure:
    """Data class for semantic region pressure metrics."""
    region: str
    density_score: float
    emotional_pressure: float
    entropy_gradient: float
    bloom_count: int
    avg_rebloom_count: float
    pressure_level: str = 'STABLE'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class SemanticPressureDetector:
    """
    The Pressure Prophet — monitors semantic space for dangerous thought density,
    emotional saturation, and entropic instability.
    
    "Where meanings crowd, coherence cracks"
    """
    
    def __init__(self, log_dir: str = "memory/owl/logs"):
        """
        Initialize the Semantic Pressure Detector.
        
        Args:
            log_dir: Directory for pressure zone logs
        """
        self.log_dir = Path(log_dir)
        self._ensure_log_directory()
        self.current_tick = 0
        logger.info("🌡️ Semantic Pressure Detector initialized")
        logger.info("📊 Monitoring for density, emotional, and entropic pressures")
    
    def _ensure_log_directory(self):
        """Ensure the log directory exists, creating it if necessary."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Log directory verified at {self.log_dir}")
    
    def detect_semantic_pressure_zones(
        self, 
        bloom_field: List[Dict[str, Any]], 
        current_tick: int
    ) -> Dict[str, Any]:
        """
        Analyze bloom field for high-pressure semantic regions that risk
        meaning collapse or symbolic overcrowding.
        
        The Three Pressures:
        1. Density Pressure - Too many blooms in one semantic space
        2. Emotional Pressure - High intensity feelings saturating a region
        3. Entropy Gradient - Chaotic variance threatening stability
        
        Args:
            bloom_field: List of bloom dictionaries containing:
                - bloom_id: str
                - semantic_region: str
                - entropy: float
                - mood_valence: float
                - rebloom_count: int
                - last_access_tick: int
            current_tick: Current system tick for age calculations
            
        Returns:
            Dictionary containing high pressure zones and analysis metadata
        """
        self.current_tick = current_tick
        logger.info(f"🔍 Analyzing semantic pressure across {len(bloom_field)} blooms")
        
        # Group blooms by semantic region
        regions = self._group_by_region(bloom_field)
        logger.info(f"📍 Found {len(regions)} distinct semantic regions")
        
        # Analyze each region for pressure indicators
        all_pressures = []
        high_pressure_zones = []
        
        for region_name, blooms in regions.items():
            try:
                pressure = self._analyze_region_pressure(region_name, blooms)
                all_pressures.append(pressure)
                
                # Check if region exceeds pressure thresholds
                if self._is_high_pressure(pressure):
                    high_pressure_zones.append(pressure)
                    logger.warning(
                        f"⚠️ High pressure in region '{region_name}': "
                        f"D={pressure.density_score:.3f}, "
                        f"E={pressure.emotional_pressure:.3f}, "
                        f"Δ={pressure.entropy_gradient:.3f}"
                    )
                    
            except Exception as e:
                logger.error(f"❌ Error analyzing region '{region_name}': {e}")
        
        # Sort high pressure zones by severity
        high_pressure_zones.sort(
            key=lambda p: (p.density_score + p.emotional_pressure + p.entropy_gradient),
            reverse=True
        )
        
        # Prepare output
        output = {
            "high_pressure_zones": [p.to_dict() for p in high_pressure_zones],
            "tick": current_tick,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_regions": len(regions),
                "high_pressure_count": len(high_pressure_zones),
                "critical_zones": sum(1 for p in high_pressure_zones if p.pressure_level == 'CRITICAL'),
                "warning_zones": sum(1 for p in high_pressure_zones if p.pressure_level == 'WARNING'),
                "avg_regional_density": np.mean([p.density_score for p in all_pressures]) if all_pressures else 0.0,
                "max_emotional_pressure": max([p.emotional_pressure for p in all_pressures]) if all_pressures else 0.0
            }
        }
        
        # Log results
        self._log_pressure_analysis(output)
        
        logger.info(
            f"📊 Pressure analysis complete: "
            f"{output['summary']['high_pressure_count']}/{output['summary']['total_regions']} "
            f"regions under pressure"
        )
        
        return output
    
    def _group_by_region(self, bloom_field: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Group blooms by their semantic region."""
        regions = defaultdict(list)
        for bloom in bloom_field:
            region = bloom.get('semantic_region', 'unknown')
            regions[region].append(bloom)
        return dict(regions)
    
    def _analyze_region_pressure(
        self, 
        region_name: str, 
        blooms: List[Dict[str, Any]]
    ) -> RegionPressure:
        """
        Analyze pressure indicators for a specific semantic region.
        
        Args:
            region_name: Name of the semantic region
            blooms: List of blooms in this region
            
        Returns:
            RegionPressure object with computed metrics
        """
        # Calculate density score (age-adjusted bloom crowding)
        density_score = self._calculate_density_score(blooms)
        
        # Calculate emotional pressure (average mood intensity)
        emotional_pressure = self._calculate_emotional_pressure(blooms)
        
        # Calculate entropy gradient (variance in entropy)
        entropy_gradient = self._calculate_entropy_gradient(blooms)
        
        # Calculate additional metrics
        avg_rebloom_count = np.mean([b.get('rebloom_count', 0) for b in blooms])
        
        # Determine pressure level
        pressure_level = self._determine_pressure_level(
            density_score, emotional_pressure, entropy_gradient
        )
        
        return RegionPressure(
            region=region_name,
            density_score=density_score,
            emotional_pressure=emotional_pressure,
            entropy_gradient=entropy_gradient,
            bloom_count=len(blooms),
            avg_rebloom_count=avg_rebloom_count,
            pressure_level=pressure_level
        )
    
    def _calculate_density_score(self, blooms: List[Dict[str, Any]]) -> float:
        """
        Calculate age-adjusted density score for a bloom cluster.
        
        Fresh blooms contribute more to crowding than old ones.
        
        Args:
            blooms: List of blooms in the region
            
        Returns:
            Density score between 0 and 1
        """
        if not blooms:
            return 0.0
        
        # Base density from bloom count
        base_density = len(blooms) / 100.0  # Normalize to 100 blooms = 1.0
        
        # Age adjustment - older blooms contribute less to crowding
        age_adjusted_count = 0.0
        for bloom in blooms:
            age = self.current_tick - bloom.get('last_access_tick', self.current_tick)
            age_factor = np.exp(-age * AGE_DECAY_FACTOR)  # Exponential decay
            age_adjusted_count += age_factor
        
        # Normalize age-adjusted count
        density_score = age_adjusted_count / 100.0
        
        # Add rebloom pressure (reblooms indicate semantic recycling)
        rebloom_pressure = sum(b.get('rebloom_count', 0) for b in blooms) / (len(blooms) * 10.0)
        density_score += rebloom_pressure * 0.2  # 20% weight for rebloom pressure
        
        return min(1.0, density_score)  # Cap at 1.0
    
    def _calculate_emotional_pressure(self, blooms: List[Dict[str, Any]]) -> float:
        """
        Calculate emotional saturation in the region.
        
        High absolute mood values indicate emotional intensity.
        
        Args:
            blooms: List of blooms in the region
            
        Returns:
            Emotional pressure between 0 and 1
        """
        if not blooms:
            return 0.0
        
        # Calculate average absolute mood valence
        mood_intensities = [abs(b.get('mood_valence', 0.0)) for b in blooms]
        avg_intensity = np.mean(mood_intensities)
        
        # Calculate mood variance (emotional turbulence)
        mood_values = [b.get('mood_valence', 0.0) for b in blooms]
        mood_variance = np.std(mood_values) if len(mood_values) > 1 else 0.0
        
        # Combined pressure: intensity + turbulence
        emotional_pressure = (avg_intensity * 0.7) + (mood_variance * 0.3)
        
        return min(1.0, emotional_pressure)
    
    def _calculate_entropy_gradient(self, blooms: List[Dict[str, Any]]) -> float:
        """
        Calculate the entropy variance across the region.
        
        High variance indicates chaotic instability.
        
        Args:
            blooms: List of blooms in the region
            
        Returns:
            Entropy gradient between 0 and 1
        """
        if not blooms or len(blooms) < 2:
            return 0.0
        
        # Get entropy values
        entropies = [b.get('entropy', 0.5) for b in blooms]
        
        # Calculate standard deviation (gradient)
        entropy_std = np.std(entropies)
        
        # Normalize to 0-1 range (assuming max useful std is 0.5)
        entropy_gradient = min(1.0, entropy_std * 2.0)
        
        return entropy_gradient
    
    def _is_high_pressure(self, pressure: RegionPressure) -> bool:
        """
        Determine if a region has high pressure based on thresholds.
        
        A region is high pressure if ANY metric exceeds warning levels.
        """
        return (
            pressure.density_score >= PRESSURE_LEVELS['WARNING']['density'] or
            pressure.emotional_pressure >= PRESSURE_LEVELS['WARNING']['emotional'] or
            pressure.entropy_gradient >= PRESSURE_LEVELS['WARNING']['entropy']
        )
    
    def _determine_pressure_level(
        self, 
        density: float, 
        emotional: float, 
        entropy: float
    ) -> str:
        """Determine the overall pressure level for a region."""
        # Check for critical levels
        if (density >= PRESSURE_LEVELS['CRITICAL']['density'] or
            emotional >= PRESSURE_LEVELS['CRITICAL']['emotional'] or
            entropy >= PRESSURE_LEVELS['CRITICAL']['entropy']):
            return 'CRITICAL'
        
        # Check for warning levels
        elif (density >= PRESSURE_LEVELS['WARNING']['density'] or
              emotional >= PRESSURE_LEVELS['WARNING']['emotional'] or
              entropy >= PRESSURE_LEVELS['WARNING']['entropy']):
            return 'WARNING'
        
        else:
            return 'STABLE'
    
    def _log_pressure_analysis(self, analysis: Dict[str, Any]):
        """
        Log the pressure analysis results to file.
        
        Args:
            analysis: The complete analysis results
        """
        filename = f"high_pressure_regions_tick_{self.current_tick}.json"
        log_path = self.log_dir / filename
        
        try:
            log_path.write_text(json.dumps(analysis, indent=2))
            logger.info(f"📝 Pressure analysis logged to {filename}")
            
        except Exception as e:
            logger.error(f"❌ Failed to log pressure analysis: {e}")
    
    def get_historical_pressure_trend(
        self, 
        region: str, 
        tick_window: int = 10000
    ) -> List[Dict[str, Any]]:
        """
        Retrieve historical pressure data for a specific region.
        
        Args:
            region: Semantic region name
            tick_window: How far back to look (in ticks)
            
        Returns:
            List of historical pressure readings for the region
        """
        history = []
        min_tick = self.current_tick - tick_window
        
        try:
            # Scan log files within tick window
            for log_file in self.log_dir.glob("high_pressure_regions_tick_*.json"):
                # Extract tick from filename
                tick_str = log_file.stem.split('_')[-1]
                file_tick = int(tick_str)
                
                if file_tick >= min_tick:
                    # Load and search for region
                    data = json.loads(log_file.read_text())
                    for zone in data.get('high_pressure_zones', []):
                        if zone['region'] == region:
                            history.append({
                                'tick': file_tick,
                                'pressure': zone
                            })
            
            # Sort by tick
            history.sort(key=lambda x: x['tick'])
            
        except Exception as e:
            logger.error(f"❌ Error retrieving pressure history: {e}")
        
        return history


# Example usage and testing
if __name__ == "__main__":
    """
    Demonstration of the Semantic Pressure Detector's fracture warning system.
    """
    
    # Initialize the detector
    detector = SemanticPressureDetector()
    
    # Generate sample bloom field with varying pressure conditions
    test_bloom_field = [
        # High density region - "trust_seed_42"
        *[{
            "bloom_id": f"bloom_trust_{i:03d}",
            "semantic_region": "trust_seed_42",
            "entropy": 0.3 + (i % 10) * 0.05,  # Varying entropy
            "mood_valence": 0.8 if i % 2 else -0.7,  # Emotional swings
            "rebloom_count": i // 5,
            "last_access_tick": 9000 - (i * 10)
        } for i in range(25)],
        
        # Emotionally intense region - "fear_nexus_13"
        *[{
            "bloom_id": f"bloom_fear_{i:03d}",
            "semantic_region": "fear_nexus_13",
            "entropy": 0.7,
            "mood_valence": -0.9 + (i * 0.02),  # High negative intensity
            "rebloom_count": 2,
            "last_access_tick": 8500
        } for i in range(15)],
        
        # Chaotic region - "chaos_spiral_99"
        *[{
            "bloom_id": f"bloom_chaos_{i:03d}",
            "semantic_region": "chaos_spiral_99",
            "entropy": np.random.random(),  # Random entropy (high gradient)
            "mood_valence": np.random.uniform(-1, 1),
            "rebloom_count": np.random.randint(0, 10),
            "last_access_tick": 9500
        } for i in range(20)],
        
        # Stable region - "peace_garden_7"
        *[{
            "bloom_id": f"bloom_peace_{i:03d}",
            "semantic_region": "peace_garden_7",
            "entropy": 0.4,
            "mood_valence": 0.2,
            "rebloom_count": 0,
            "last_access_tick": 9800
        } for i in range(10)]
    ]
    
    # Run pressure detection
    current_tick = 10000
    results = detector.detect_semantic_pressure_zones(test_bloom_field, current_tick)
    
    # Display results
    print("\n🌡️ SEMANTIC PRESSURE ANALYSIS RESULTS")
    print("=" * 50)
    print(f"Total Regions Analyzed: {results['summary']['total_regions']}")
    print(f"High Pressure Zones: {results['summary']['high_pressure_count']}")
    print(f"Critical Zones: {results['summary']['critical_zones']}")
    print(f"Warning Zones: {results['summary']['warning_zones']}")
    
    print("\n🚨 HIGH PRESSURE ZONES:")
    for zone in results['high_pressure_zones']:
        print(f"\n  Region: {zone['region']} [{zone['pressure_level']}]")
        print(f"    Density Score: {zone['density_score']:.3f}")
        print(f"    Emotional Pressure: {zone['emotional_pressure']:.3f}")
        print(f"    Entropy Gradient: {zone['entropy_gradient']:.3f}")
        print(f"    Bloom Count: {zone['bloom_count']}")
        print(f"    Avg Rebloom: {zone['avg_rebloom_count']:.1f}")