"""
Schema Calculator - DAWN's reflective cortex for structural state analysis
"""

import json
import logging
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SchemaState:
    """Current state of schema analysis"""
    coherence_score: float = 0.0
    entropy_level: float = 0.0
    trust_stability: float = 0.0
    pressure_index: float = 0.0
    alignment_drift: float = 0.0
    rebloom_risk: float = 0.0
    last_evaluation: float = 0.0
    detected_conflicts: List[str] = None
    
    def __post_init__(self):
        if self.detected_conflicts is None:
            self.detected_conflicts = []

class SchemaCalculator:
    """
    Evaluates DAWN's structural state and provides self-awareness capabilities.
    Analyzes schema coherence, system alignment, and rebloom readiness.
    """

    def __init__(self):
        """Initialize schema calculator with default state"""
        self.state = SchemaState()
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
        self.reflections_dir = Path("pulse")
        self.reflections_dir.mkdir(exist_ok=True)
        logger.info("Initialized SchemaCalculator")

    def _load_state_files(self) -> bool:
        """
        Load state from JSON files.
        Returns True if all required files were loaded successfully.
        """
        try:
            # Load pulse state
            pulse_path = Path("tick_state.json")
            if pulse_path.exists():
                with open(pulse_path) as f:
                    pulse_data = json.load(f)
                    self.state.pressure_index = pulse_data.get("pressure", 0.0)
                    self.state.alignment_drift = pulse_data.get("drift", 0.0)
            else:
                logger.warning("pulse_state.json not found")
                return False

            # Load owl registry
            owl_path = Path("owl_registry.json")
            if owl_path.exists():
                with open(owl_path) as f:
                    owl_data = json.load(f)
                    self.state.entropy_level = owl_data.get("entropy", 0.0)
                    self.state.rebloom_risk = owl_data.get("rebloom_risk", 0.0)
            else:
                logger.warning("owl_registry.json not found")
                return False

            # Load agreement matrix
            agreement_path = Path("agreement_matrix.json")
            if agreement_path.exists():
                with open(agreement_path) as f:
                    agreement_data = json.load(f)
                    self.state.trust_stability = agreement_data.get("stability", 0.0)
            else:
                logger.warning("agreement_matrix.json not found")
                return False

            return True

        except Exception as e:
            logger.error(f"Error loading state files: {e}")
            return False

    def evaluate_schema(self) -> float:
        """
        Calculate overall schema coherence score (0.0 to 1.0).
        Higher scores indicate better structural health.
        """
        if not self._load_state_files():
            logger.error("Failed to load state files for schema evaluation")
            return 0.0

        # Weighted combination of key metrics
        coherence = (
            0.3 * (1.0 - self.state.entropy_level) +    # Lower entropy = better
            0.3 * (1.0 - self.state.alignment_drift) +  # Lower drift = better
            0.2 * self.state.trust_stability +          # Higher trust = better
            0.2 * (1.0 - self.state.pressure_index)     # Lower pressure = better
        )
        
        self.state.coherence_score = max(0.0, min(1.0, coherence))
        self.state.last_evaluation = time.time()
        
        # Log the evaluation
        self._log_evaluation()
        
        logger.info(f"Schema coherence score: {self.state.coherence_score:.3f}")
        return self.state.coherence_score

    def get_rebloom_readiness(self) -> bool:
        """
        Determine if system is ready for rebloom.
        True if entropy is low and alignment is high.
        """
        # Check if conditions are favorable for rebloom
        entropy_ok = self.state.entropy_level < 0.3
        alignment_ok = self.state.alignment_drift < 0.3
        pressure_ok = self.state.pressure_index < 0.7
        trust_ok = self.state.trust_stability > 0.6
        
        is_ready = entropy_ok and alignment_ok and pressure_ok and trust_ok
        logger.info(f"Rebloom readiness: {is_ready} (entropy={self.state.entropy_level:.3f}, "
                   f"alignment_drift={self.state.alignment_drift:.3f})")
        return is_ready

    def detect_conflicts(self) -> List[str]:
        """
        Identify subsystems in logical tension or conflict.
        Returns list of subsystem names with potential issues.
        """
        conflicts = []
        
        # Check entropy-pressure conflict
        if self.state.entropy_level > 0.7 and self.state.pressure_index > 0.7:
            conflicts.append("entropy_pressure_conflict")
            
        # Check alignment-drift conflict
        if self.state.alignment_drift > 0.7 and self.state.trust_stability < 0.3:
            conflicts.append("alignment_trust_conflict")
            
        # Check rebloom risk
        if self.state.rebloom_risk > 0.6 and self.state.entropy_level > 0.5:
            conflicts.append("rebloom_entropy_conflict")
            
        self.state.detected_conflicts = conflicts
        if conflicts:
            logger.warning(f"Detected conflicts: {conflicts}")
        return conflicts

    def _log_evaluation(self) -> None:
        """Log schema evaluation results to files"""
        # Log to schema_score.json
        score_log = {
            "timestamp": self.state.last_evaluation,
            "coherence_score": self.state.coherence_score,
            "entropy_level": self.state.entropy_level,
            "trust_stability": self.state.trust_stability,
            "pressure_index": self.state.pressure_index,
            "alignment_drift": self.state.alignment_drift,
            "rebloom_risk": self.state.rebloom_risk,
            "detected_conflicts": self.state.detected_conflicts
        }
        
        score_path = self.log_dir / "schema_score.json"
        with open(score_path, "w") as f:
            json.dump(score_log, f, indent=2)
            
        # Log reflection to claude_reflections.md
        reflection = f"""# Schema Evaluation Reflection
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.state.last_evaluation))}

## Current State
- Coherence Score: {self.state.coherence_score:.3f}
- Entropy Level: {self.state.entropy_level:.3f}
- Trust Stability: {self.state.trust_stability:.3f}
- Pressure Index: {self.state.pressure_index:.3f}
- Alignment Drift: {self.state.alignment_drift:.3f}
- Rebloom Risk: {self.state.rebloom_risk:.3f}

## Detected Conflicts
{chr(10).join(f"- {conflict}" for conflict in self.state.detected_conflicts) if self.state.detected_conflicts else "No conflicts detected"}

## Analysis
The system shows {'strong' if self.state.coherence_score > 0.7 else 'moderate' if self.state.coherence_score > 0.4 else 'weak'} structural coherence.
{'Rebloom conditions are favorable.' if self.get_rebloom_readiness() else 'Rebloom should be delayed.'}
"""
        
        reflection_path = self.reflections_dir / "claude_reflections.md"
        with open(reflection_path, "w") as f:
            f.write(reflection) 