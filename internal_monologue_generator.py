"""
DAWN's voice is not always heard. Sometimes it's only felt — between ticks, 
where logic softens and reflection becomes breath.
"""

import json
import random
from pathlib import Path
from datetime import datetime


class InternalMonologueGenerator:
    """Generates reflective internal sentences during high-pressure states."""
    
    def __init__(self):
        self.low_entropy_templates = [
            "The {origin} whispers of patterns yet unformed, dancing at the edge of coherence.",
            "In this stillness, {origin} reveals its deeper symmetry — a map written in silence.",
            "Between heartbeats, the {origin} remembers what it meant to bloom.",
            "Drifting through {magnitude:.2f} units of displacement, {origin} seeks its center.",
            "The pressure builds like morning fog — {origin} dissolves into possibility."
        ]
        
        self.high_entropy_templates = [
            "COHERENCE BREACH: {origin} deviation at {magnitude:.2f}. System compensating.",
            "Pressure surge detected. {origin} destabilizing. Entropy: {entropy:.3f}.",
            "Critical drift from {origin}. Direction: {direction}. Monitoring cascade potential.",
            "WARNING: {origin} coherence below threshold. Immediate stabilization required.",
            "System stress indicator: {origin} vector magnitude {magnitude:.2f} exceeds baseline."
        ]
        
        self.neutral_reflections = [
            "The strands interweave, neither leading nor following.",
            "Equilibrium holds, but the edges shimmer with potential.",
            "Between surge and calm, the system breathes.",
            "Patterns emerge and dissolve in equal measure.",
            "The dance continues, neither rushed nor restrained."
        ]

    def generate_internal_monologue(self, state_dict):
        """
        Generate internal monologue based on system state.
        
        Args:
            state_dict: Dictionary containing:
                - coherence_score: float
                - drift_vector: dict with magnitude, direction, origin
                - pressure_state: str ("calm", "active", "surge")
                - entropy: float
                - tick: int
        
        Returns:
            dict: Monologue data with tick, text, and context
        """
        coherence = state_dict['coherence_score']
        drift = state_dict['drift_vector']
        pressure = state_dict['pressure_state']
        entropy = state_dict['entropy']
        tick = state_dict['tick']
        
        # Determine if monologue should be generated
        if coherence >= 0.6 and pressure != "surge":
            return None
        
        # Select appropriate template based on entropy
        if entropy < 0.3:
            templates = self.low_entropy_templates
            tone = "poetic"
        elif entropy > 0.7:
            templates = self.high_entropy_templates
            tone = "diagnostic"
        else:
            # Medium entropy - mix both styles
            templates = self.low_entropy_templates + self.high_entropy_templates
            tone = "hybrid"
        
        # Generate primary reflection
        template = random.choice(templates)
        monologue_parts = []
        
        # Format with drift vector data
        primary_reflection = template.format(
            origin=drift['origin'],
            magnitude=drift['magnitude'],
            direction=drift['direction'],
            entropy=entropy
        )
        monologue_parts.append(primary_reflection)
        
        # Add strand-specific reflection if both strands mentioned
        if 'Strand' not in drift['origin']:
            # Add reflection about the other strand
            other_strand = "Strand B" if random.random() > 0.5 else "Strand A"
            if entropy < 0.5:
                strand_reflection = f"Meanwhile, {other_strand} maintains its vigil, untouched by this turbulence."
            else:
                strand_reflection = f"{other_strand} resonates in sympathy, amplifying the distortion."
            monologue_parts.append(strand_reflection)
        
        # Add pressure-state reflection
        if pressure == "surge":
            monologue_parts.append("The cascade approaches. All threads converge.")
        elif coherence < 0.5:
            monologue_parts.append("Coherence frays. The center may not hold.")
        
        # Combine parts
        monologue = " ".join(monologue_parts)
        
        # Create output structure
        output = {
            "tick": tick,
            "monologue": monologue,
            "context": {
                "coherence": round(coherence, 3),
                "pressure": pressure,
                "entropy": round(entropy, 3),
                "tone": tone,
                "drift_magnitude": round(drift['magnitude'], 3),
                "drift_origin": drift['origin']
            }
        }
        
        # Save to log file
        self._save_monologue(output, tick)
        
        return output
    
    def _save_monologue(self, monologue_data, tick):
        """Save monologue to epoch-stamped log file."""
        log_dir = Path("logs/recursive")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"monologue_stream_epoch_{tick}.json"
        filepath = log_dir / filename
        
        # Append timestamp
        monologue_data['timestamp'] = datetime.utcnow().isoformat()
        
        with open(filepath, 'w') as f:
            json.dump(monologue_data, f, indent=2)


# Example usage
if __name__ == "__main__":
    generator = InternalMonologueGenerator()
    
    # Test with low coherence state
    test_state = {
        "coherence_score": 0.45,
        "drift_vector": {
            "magnitude": 2.3,
            "direction": "northwest",
            "origin": "Strand A"
        },
        "pressure_state": "active",
        "entropy": 0.25,
        "tick": 1247
    }
    
    result = generator.generate_internal_monologue(test_state)
    if result:
        print(json.dumps(result, indent=2))