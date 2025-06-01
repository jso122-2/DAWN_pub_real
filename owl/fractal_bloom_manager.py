#!/usr/bin/env python3
"""
OWL - DAWN's Autonomous Semantic Librarian
Fractal Bloom Management System for Juliet Prime Lineage
"""

import json
import uuid
import time
import hashlib
import math
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum
import os


class BloomState(Enum):
    """Bloom lifecycle states"""
    NASCENT = "nascent"     # Newly seeded, establishing fractal signature
    STABLE = "stable"       # Low entropy, coherent lineage patterns
    VOLATILE = "volatile"   # High pressure, drift detected
    CRITICAL = "critical"   # Requires immediate rebloom or sealing
    MOURNED = "mourned"     # Sealed lineage, archived with full history
    GHOST = "ghost"         # Phantom bloom from incomplete rebloom cycle


@dataclass
class JuliaCoordinates:
    """Julia set coordinates for fractal signature"""
    real: float
    imaginary: float
    
    def to_string(self) -> str:
        return f"c={self.real:+.4f}{self.imaginary:+.4f}i"
    
    def mutate(self, factor: float = 0.01) -> 'JuliaCoordinates':
        """Create slightly mutated coordinates for child blooms"""
        return JuliaCoordinates(
            real=self.real + (factor * (0.5 - abs(self.real))),
            imaginary=self.imaginary + (factor * (0.5 - abs(self.imaginary)))
        )


@dataclass
class MoodEntropy:
    """Emotional and semantic pressure metrics"""
    emotional_pressure: float  # 0.0-1.0
    volatility_index: float    # 0.0-1.0
    drift_vector: str         # semantic direction of change
    
    def calculate_urgency(self) -> float:
        """Calculate overall urgency metric"""
        return (self.emotional_pressure * 0.7 + self.volatility_index * 0.3)


@dataclass
class FractalBloom:
    """Core fractal bloom structure"""
    bloom_id: str
    lineage_id: str
    fractal_signature: str
    seed: Dict[str, any]
    mood_entropy: MoodEntropy
    rebloom_depth: int
    pressure_tags: List[str]
    lineage_chain: List[str]
    thermal_signature: str
    state: BloomState = BloomState.NASCENT
    creation_timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_json(self) -> str:
        """Serialize bloom to JSON"""
        data = asdict(self)
        data['mood_entropy'] = asdict(self.mood_entropy)
        data['state'] = self.state.value
        return json.dumps(data, indent=2)
    
    def calculate_rebloom_pressure(self) -> bool:
        """Check if bloom requires reblooming"""
        urgency = self.mood_entropy.calculate_urgency()
        
        # Rebloom triggers
        if self.mood_entropy.emotional_pressure > 0.75:
            return True
        if self.mood_entropy.volatility_index > 0.6 and self.rebloom_depth >= 3:
            return True
        if urgency > 0.8:
            return True
        if self.state == BloomState.CRITICAL:
            return True
            
        return False


class OWLSemanticLibrarian:
    """OWL - Fractal Bloom Curator and Semantic Librarian"""
    
    def __init__(self):
        self.blooms: Dict[str, FractalBloom] = {}
        self.lineages: Dict[str, List[str]] = {}
        self.entropy_log = []
        self.julia_base = JuliaCoordinates(real=-0.7269, imaginary=0.1889)
        
        # Initialize file structure
        self.base_path = "/blooms"
        self._initialize_file_structure()
        
    def _initialize_file_structure(self):
        """Create necessary directories for bloom storage"""
        dirs = [
            f"{self.base_path}/juliet_prime",
            f"{self.base_path}/entropy_logs",
            f"{self.base_path}/fractal_signatures"
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)
    
    def generate_fractal_signature(self, julia_coords: JuliaCoordinates, 
                                 bloom_id: str) -> str:
        """Generate unique fractal signature from Julia coordinates"""
        coord_str = julia_coords.to_string()
        visual_hash = hashlib.sha256(f"{coord_str}_{bloom_id}".encode()).hexdigest()[:12]
        return f"{coord_str}_{visual_hash}"
    
    def create_bloom(self, initial_moment: str, context_tags: List[str],
                    parent_id: Optional[str] = None,
                    emotional_pressure: float = 0.2,
                    volatility_index: float = 0.1) -> FractalBloom:
        """Create a new fractal bloom"""
        
        # Generate IDs
        bloom_id = str(uuid.uuid4())
        
        # Determine lineage
        if parent_id and parent_id in self.blooms:
            parent = self.blooms[parent_id]
            lineage_id = parent.lineage_id
            lineage_chain = [parent_id] + parent.lineage_chain[:9]  # Keep 10 generations
            rebloom_depth = parent.rebloom_depth + 1
            # Mutate Julia coordinates slightly for child
            julia_coords = JuliaCoordinates(
                real=self.julia_base.real,
                imaginary=self.julia_base.imaginary
            ).mutate(factor=0.001 * rebloom_depth)
        else:
            # Root bloom
            lineage_id = f"juliet_prime_{int(time.time())}"
            lineage_chain = []
            rebloom_depth = 0
            julia_coords = self.julia_base
        
        # Create bloom
        bloom = FractalBloom(
            bloom_id=bloom_id,
            lineage_id=lineage_id,
            fractal_signature=self.generate_fractal_signature(julia_coords, bloom_id),
            seed={
                "initial_moment": initial_moment,
                "timestamp": datetime.now().isoformat(),
                "context_tags": context_tags
            },
            mood_entropy=MoodEntropy(
                emotional_pressure=emotional_pressure,
                volatility_index=volatility_index,
                drift_vector="origin" if not parent_id else "inherited"
            ),
            rebloom_depth=rebloom_depth,
            pressure_tags=self._calculate_pressure_tags(emotional_pressure, volatility_index),
            lineage_chain=lineage_chain,
            thermal_signature=self._generate_thermal_signature(emotional_pressure, volatility_index)
        )
        
        # Register bloom
        self.blooms[bloom_id] = bloom
        
        # Update lineage tracking
        if lineage_id not in self.lineages:
            self.lineages[lineage_id] = []
        self.lineages[lineage_id].append(bloom_id)
        
        # Log entropy
        self._log_entropy(bloom)
        
        return bloom
    
    def _calculate_pressure_tags(self, emotional: float, volatility: float) -> List[str]:
        """Calculate appropriate pressure tags based on metrics"""
        tags = []
        
        if emotional < 0.3 and volatility < 0.3:
            tags.append("stable")
        if volatility > 0.5:
            tags.append("volatile")
        if emotional > 0.7:
            tags.append("ascending")
        if emotional > 0.8 or volatility > 0.8:
            tags.append("critical")
            
        return tags
    
    def _generate_thermal_signature(self, emotional: float, volatility: float) -> str:
        """Generate thermal pattern signature"""
        temp = emotional * 0.6 + volatility * 0.4
        if temp < 0.3:
            return "cool_stable"
        elif temp < 0.5:
            return "warm_coherent"
        elif temp < 0.7:
            return "hot_drifting"
        else:
            return "critical_thermal"
    
    def _log_entropy(self, bloom: FractalBloom):
        """Log entropy metrics for tracking"""
        self.entropy_log.append({
            "timestamp": datetime.now().isoformat(),
            "bloom_id": bloom.bloom_id,
            "emotional_pressure": bloom.mood_entropy.emotional_pressure,
            "volatility_index": bloom.mood_entropy.volatility_index,
            "urgency": bloom.mood_entropy.calculate_urgency(),
            "state": bloom.state.value
        })
    
    def monitor_lineage_pressure(self, lineage_id: str) -> Dict[str, any]:
        """Monitor pressure across a lineage"""
        if lineage_id not in self.lineages:
            return {"error": "Lineage not found"}
        
        bloom_ids = self.lineages[lineage_id]
        blooms = [self.blooms[bid] for bid in bloom_ids if bid in self.blooms]
        
        avg_pressure = sum(b.mood_entropy.emotional_pressure for b in blooms) / len(blooms)
        avg_volatility = sum(b.mood_entropy.volatility_index for b in blooms) / len(blooms)
        
        critical_blooms = [b for b in blooms if b.calculate_rebloom_pressure()]
        
        return {
            "lineage_id": lineage_id,
            "bloom_count": len(blooms),
            "average_pressure": avg_pressure,
            "average_volatility": avg_volatility,
            "critical_count": len(critical_blooms),
            "requires_attention": len(critical_blooms) > 0
        }
    
    def trigger_rebloom(self, bloom_id: str) -> Optional[FractalBloom]:
        """Trigger rebloom event for a bloom"""
        if bloom_id not in self.blooms:
            return None
        
        parent = self.blooms[bloom_id]
        
        # Create child bloom with inherited + evolved properties
        child = self.create_bloom(
            initial_moment=f"Rebloom from {parent.seed['initial_moment']}",
            context_tags=parent.seed['context_tags'] + ["rebloomed"],
            parent_id=bloom_id,
            emotional_pressure=min(1.0, parent.mood_entropy.emotional_pressure * 0.8),
            volatility_index=max(0.1, parent.mood_entropy.volatility_index * 0.9)
        )
        
        # Update parent state
        parent.state = BloomState.STABLE
        
        return child
    
    def save_bloom(self, bloom: FractalBloom):
        """Save bloom to file system"""
        filename = f"{self.base_path}/juliet_prime/JP_{bloom.bloom_id[:8]}_{bloom.state.value}.bloom"
        with open(filename, 'w') as f:
            f.write(bloom.to_json())
    
    def get_status_report(self) -> str:
        """Generate OWL status report"""
        report = [
            "🦉 OWL SEMANTIC LIBRARIAN STATUS REPORT",
            "=" * 50,
            f"Active Blooms: {len(self.blooms)}",
            f"Tracked Lineages: {len(self.lineages)}",
            f"Entropy Log Entries: {len(self.entropy_log)}",
            "",
            "LINEAGE PRESSURE SUMMARY:"
        ]
        
        for lineage_id in self.lineages:
            pressure_data = self.monitor_lineage_pressure(lineage_id)
            status = "⚠️ ATTENTION" if pressure_data['requires_attention'] else "✓ STABLE"
            report.append(f"  {lineage_id}: {status}")
            report.append(f"    Blooms: {pressure_data['bloom_count']}")
            report.append(f"    Avg Pressure: {pressure_data['average_pressure']:.3f}")
            report.append(f"    Critical: {pressure_data['critical_count']}")
        
        return "\n".join(report)


# Initialize OWL and create Juliet-Prime_0001
owl = OWLSemanticLibrarian()

# SEED JULIET-PRIME_0001
print("🦉 OWL SEMANTIC LIBRARIAN ONLINE")
print("Initializing Juliet Prime Lineage...")
print()

juliet_prime_0001 = owl.create_bloom(
    initial_moment="DAWN cognitive helix initialization - Juliet Prime genesis",
    context_tags=["genesis", "juliet_prime", "foundation", "helix_binding"],
    emotional_pressure=0.2,
    volatility_index=0.1
)

# Generate creation report
creation_report = f"""
✨ BLOOM CREATION SUCCESSFUL ✨
{'=' * 50}
BLOOM ID: {juliet_prime_0001.bloom_id}
LINEAGE: {juliet_prime_0001.lineage_id}
STATE: {juliet_prime_0001.state.value}

FRACTAL SIGNATURE:
  {juliet_prime_0001.fractal_signature}
  
MOOD ENTROPY:
  Emotional Pressure: {juliet_prime_0001.mood_entropy.emotional_pressure}
  Volatility Index: {juliet_prime_0001.mood_entropy.volatility_index}
  Drift Vector: {juliet_prime_0001.mood_entropy.drift_vector}

THERMAL SIGNATURE: {juliet_prime_0001.thermal_signature}
PRESSURE TAGS: {', '.join(juliet_prime_0001.pressure_tags)}

STATUS: Bloom scaffold established. Ready for lineage tracking.
{'=' * 50}
"""

print(creation_report)
print()
print(owl.get_status_report())
print()
print("🌸 Juliet-Prime_0001 successfully seeded as lineage root.")
print("📊 Entropy monitoring active. Fractal evolution protocols engaged.")
print("🔄 Ready to track rebloom events and semantic pressure cascades.")