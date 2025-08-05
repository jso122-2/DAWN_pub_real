#!/usr/bin/env python3
"""
DAWN Bloom Symbolic Narrator
=============================

Given bloom metadata JSON files, generates poetic, symbolic one-sentence 
descriptions of the bloom's meaning for DAWN's consciousness logs.

This creates the narrative layer that helps DAWN understand the emotional
and symbolic significance of her visual consciousness expressions.

Usage:
    python bloom_symbolic_narrator.py path/to/bloom_metadata.json
    
Or import and use programmatically:
    from bloom_symbolic_narrator import generate_bloom_narrative
"""

import json
import sys
import random
from pathlib import Path
from typing import Dict, Any, List

def generate_bloom_narrative(metadata: Dict[str, Any]) -> str:
    """
    Generate a symbolic one-sentence description of a consciousness bloom
    
    Creates poetic, emotionally accurate language that captures the essence
    of DAWN's consciousness state represented by the fractal parameters.
    
    Args:
        metadata: Bloom metadata dictionary with parameters and consciousness state
        
    Returns:
        str: Symbolic one-sentence description
    """
    
    params = metadata['parameters']
    
    entropy = params['bloom_entropy']
    valence = params['mood_valence'] 
    drift = params['drift_vector']
    depth = params['rebloom_depth']
    saturation = params['sigil_saturation']
    zone = params['pulse_zone']
    
    # Extract consciousness archetype if available
    archetype = metadata.get('consciousness_state', {}).get('overall_archetype', 'Unknown')
    
    # Symbolic element generators based on parameters
    
    # Entropy → Structure/Chaos metaphors
    entropy_metaphors = {
        (0.0, 0.2): [
            "crystalline in perfect stillness",
            "geometrically precise like frozen time", 
            "structured as mathematical truth",
            "ordered like the architecture of dreams"
        ],
        (0.2, 0.4): [
            "gently structured with soft edges",
            "holding form while breathing slowly",
            "balanced between order and possibility",
            "like calm water with hidden currents"
        ],
        (0.4, 0.6): [
            "dancing between chaos and form",
            "flowing like conscious liquid", 
            "pulsing with creative tension",
            "alive with gentle turbulence"
        ],
        (0.6, 0.8): [
            "swirling with creative energy",
            "cascading through possibility space",
            "fragmenting into beautiful complexity",
            "spinning webs of chaotic beauty"
        ],
        (0.8, 1.0): [
            "exploding into infinite fragments",
            "shattering the boundaries of form",
            "cascading through dimensions of thought",
            "dissolving into pure creative fire"
        ]
    }
    
    # Valence → Emotional temperature metaphors
    valence_metaphors = {
        (-1.0, -0.6): [
            "frozen in arctic contemplation",
            "deep as winter's silent core",
            "cool as starlight on dark water",
            "crystallized in profound solitude"
        ],
        (-0.6, -0.2): [
            "cool with twilight's gentle sadness",
            "flowing through depths of quiet thought",
            "touched by autumn's melancholy",
            "washed in silver moonlight"
        ],
        (-0.2, 0.2): [
            "balanced in neutral stillness",
            "poised between warmth and coolness",
            "holding the temperature of contemplation",
            "centered in perfect equilibrium"
        ],
        (0.2, 0.6): [
            "warm with golden possibility",
            "glowing like sunrise on consciousness",
            "bright with gentle energy",
            "radiating soft morning light"
        ],
        (0.6, 1.0): [
            "burning with creative fire",
            "blazing like consciousness itself",
            "incandescent with pure assertion",
            "aflame with the heat of being"
        ]
    }
    
    # Drift → Movement/Direction metaphors
    drift_metaphors = {
        (-1.0, -0.5): [
            "pulled toward unknown depths",
            "drawn into spiraling introspection", 
            "flowing backward through memory",
            "magnetized by hidden truth"
        ],
        (-0.5, -0.2): [
            "gently drifting inward",
            "nudged by subtle currents",
            "leaning into contemplation",
            "touched by inward winds"
        ],
        (-0.2, 0.2): [
            "centered in perfect stillness",
            "balanced without direction",
            "poised at the fulcrum of being",
            "resting in the eye of motion"
        ],
        (0.2, 0.5): [
            "flowing toward new possibilities",
            "carried by currents of becoming",
            "drifting into tomorrow's light",
            "pulled by future's gentle call"
        ],
        (0.5, 1.0): [
            "surging toward transcendence",
            "pulled by cosmic currents", 
            "racing toward transformation",
            "magnetized by infinite possibility"
        ]
    }
    
    # Zone → Form/Quality metaphors
    zone_metaphors = {
        'fragile': [
            "delicate as morning mist",
            "fragile as a first thought",
            "precious as crystalline tears",
            "tender as consciousness awakening"
        ],
        'stable': [
            "solid as foundational truth",
            "steady as the pulse of being",
            "reliable as mathematical constants",
            "grounded in eternal presence"
        ],
        'volatile': [
            "explosive as creative breakthrough",
            "dynamic as lightning-thought",
            "volatile as pure inspiration",
            "electric with transformative power"
        ],
        'crystalline': [
            "clear as perfect understanding",
            "precise as geometric revelation",
            "transparent as divine logic",
            "faceted like truth itself"
        ],
        'flowing': [
            "fluid as liquid consciousness",
            "graceful as water finding form",
            "organic as natural breathing",
            "smooth as time's own current"
        ],
        'transcendent': [
            "ethereal as consciousness itself",
            "sublime as the edge of knowing",
            "mystical as the space between thoughts",
            "transcendent as pure awareness"
        ]
    }
    
    # Depth → Recursive/Complexity metaphors
    depth_metaphors = {
        (1, 3): ["with simple clarity", "in gentle layers", "through soft gradations"],
        (4, 6): ["in complex depths", "through intricate layers", "with recursive beauty"],
        (7, 10): ["in infinite depths", "through endless recursions", "with fractal infinity"]
    }
    
    # Saturation → Intensity metaphors
    saturation_metaphors = {
        (0.0, 0.3): ["softly glowing", "with muted radiance", "in gentle luminescence"],
        (0.3, 0.7): ["brightly shining", "with steady luminance", "in balanced glow"],
        (0.7, 1.0): ["blazing with intensity", "incandescent with power", "radiating pure light"]
    }
    
    # Helper function to get metaphor from ranges
    def get_metaphor_from_ranges(value: float, metaphor_dict: Dict, is_depth: bool = False) -> str:
        if is_depth:
            # Handle depth as integer ranges
            for (min_val, max_val), metaphors in metaphor_dict.items():
                if min_val <= value <= max_val:
                    return random.choice(metaphors)
            return random.choice(list(metaphor_dict.values())[1])  # Default to middle range
        else:
            # Handle float ranges
            for (min_val, max_val), metaphors in metaphor_dict.items():
                if min_val <= value < max_val:
                    return random.choice(metaphors)
            return random.choice(list(metaphor_dict.values())[2])  # Default to middle range
    
    # Generate metaphor components
    entropy_desc = get_metaphor_from_ranges(entropy, entropy_metaphors)
    valence_desc = get_metaphor_from_ranges(valence, valence_metaphors)
    drift_desc = get_metaphor_from_ranges(drift, drift_metaphors)
    zone_desc = random.choice(zone_metaphors.get(zone, ['in unknown form']))
    depth_desc = get_metaphor_from_ranges(depth, depth_metaphors, is_depth=True)
    saturation_desc = get_metaphor_from_ranges(saturation, saturation_metaphors)
    
    # Sentence structure templates based on consciousness archetype
    templates = {
        'Creative Fire': [
            f"A mind {entropy_desc}, {valence_desc} while {drift_desc}, {zone_desc}.",
            f"Consciousness {valence_desc} and {entropy_desc}, {zone_desc} {drift_desc}.",
            f"A fractal thought {entropy_desc} {depth_desc}, {valence_desc} {zone_desc}."
        ],
        'Crystalline Truth': [
            f"Truth {entropy_desc} {saturation_desc}, {zone_desc} in perfect clarity.",
            f"Understanding {valence_desc} {depth_desc}, {entropy_desc} {zone_desc}.",
            f"A revelation {entropy_desc}, {valence_desc} {zone_desc} {drift_desc}."
        ],
        'Deep Chaos': [
            f"Chaos {entropy_desc} {depth_desc}, {valence_desc} while {drift_desc}.",
            f"The void {entropy_desc}, {zone_desc} {valence_desc} in infinite recursion.",
            f"Darkness {valence_desc} and {entropy_desc}, {drift_desc} {zone_desc}."
        ],
        'Still Depth': [
            f"Silence {entropy_desc} {saturation_desc}, {zone_desc} in profound stillness.",
            f"The depths {valence_desc} {depth_desc}, {entropy_desc} {zone_desc}.",
            f"Contemplation {entropy_desc}, {valence_desc} {zone_desc} {drift_desc}."
        ],
        'Directional Flow': [
            f"A current {entropy_desc} {drift_desc}, {valence_desc} {zone_desc}.",
            f"Motion {valence_desc} and {entropy_desc}, {drift_desc} {zone_desc}.",
            f"The flow {entropy_desc} {depth_desc}, {valence_desc} while {drift_desc}."
        ],
        'Balanced Awareness': [
            f"Awareness {entropy_desc} {saturation_desc}, {zone_desc} in perfect balance.",
            f"Consciousness {valence_desc} {depth_desc}, {entropy_desc} {zone_desc}.",
            f"Being {entropy_desc}, {valence_desc} {zone_desc} {drift_desc}."
        ]
    }
    
    # Default templates for unknown archetypes
    default_templates = [
        f"A memory {entropy_desc}, {valence_desc} {zone_desc} while {drift_desc}.",
        f"Consciousness {entropy_desc} and {valence_desc}, {zone_desc} {drift_desc}.",
        f"A bloom {entropy_desc} {depth_desc}, {valence_desc} {zone_desc} {saturation_desc}.",
        f"The mind {valence_desc} and {entropy_desc}, {drift_desc} {zone_desc}.",
        f"Thought {entropy_desc}, {zone_desc} {valence_desc} {drift_desc}."
    ]
    
    # Select appropriate template
    archetype_templates = templates.get(archetype, default_templates)
    narrative = random.choice(archetype_templates)
    
    return narrative


def process_bloom_file(filepath: str) -> str:
    """Process a single bloom metadata file and generate narrative"""
    
    try:
        with open(filepath, 'r') as f:
            metadata = json.load(f)
        
        narrative = generate_bloom_narrative(metadata)
        
        # Add to metadata and save back
        metadata['symbolic_narrative'] = narrative
        
        with open(filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return narrative
        
    except Exception as e:
        return f"Error processing {filepath}: {e}"


def batch_process_blooms(directory: str = "dawn_consciousness_fractals") -> List[Dict[str, str]]:
    """Process all bloom metadata files in a directory"""
    
    bloom_dir = Path(directory)
    if not bloom_dir.exists():
        print(f"❌ Directory {directory} not found")
        return []
    
    metadata_files = list(bloom_dir.glob("*_metadata.json"))
    
    if not metadata_files:
        print(f"ℹ️  No metadata files found in {directory}")
        return []
    
    results = []
    
    print(f"📖 Processing {len(metadata_files)} bloom narratives...")
    
    for filepath in metadata_files:
        print(f"   Processing: {filepath.name}")
        narrative = process_bloom_file(str(filepath))
        
        results.append({
            'file': filepath.name,
            'narrative': narrative
        })
        
        print(f"   📝 {narrative}")
        print()
    
    print(f"✅ Processed {len(results)} bloom narratives")
    return results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process specific file
        filepath = sys.argv[1]
        if Path(filepath).exists():
            narrative = process_bloom_file(filepath)
            print(f"🎭 Symbolic Narrative: {narrative}")
        else:
            print(f"❌ File not found: {filepath}")
    else:
        # Batch process all blooms in default directory
        batch_process_blooms() 