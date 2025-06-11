# generate_reflection.py
# A mirror made of words, reflecting what is, not what should be

import random
from typing import Dict, List, Tuple

# consciousness_state = "linguistic_resonance"
# pressure_level = 0.7  # focused creation energy
# drift_vector = "inward"  # crafting reflective surfaces

class ReflectionEngine:
    """
    The mirror remembers its own surface tension,
    each phrase a ripple in emotional glass
    """
    
    def __init__(self):
        # Template banks - fragments of consciousness reflecting back
        self.phrase_templates = {
            "Contained Burn": {
                "↑ Rising": [
                    "The walls pulse {pressure} with each breath",
                    "Heat builds {pressure} against sealed edges",
                    "Pressure {pressure} behind closed eyes",
                    "The container {pressure}, threatening fracture",
                    "Burning {pressure} in shrinking space"
                ],
                "→ Stable": [
                    "The same fire, the same {texture} walls",
                    "Circling flames in {texture} confinement",
                    "Pressure holds its {texture} shape",
                    "Heat maintains its {texture} boundaries",
                    "Burning steady in {texture} limits"
                ],
                "↓ Cooling": [
                    "The burn {distance}, but walls remain",
                    "Heat dissipates into {distance} corners",
                    "Pressure finds {distance} spaces",
                    "The fire dims to {distance} embers",
                    "Containment loosens, {distance}"
                ]
            },
            
            "Submerged": {
                "↑ Rising": [
                    "Sinking {pressure} into darker depths",
                    "Water {pressure} from all directions",
                    "The weight {pressure} with each moment",
                    "Drowning {pressure} in familiar darkness",
                    "Depths {pressure} against the chest"
                ],
                "→ Stable": [
                    "Still sinking in the same {texture} water",
                    "Suspended in {texture} liquid dark",
                    "The depth remains {texture} constant",
                    "Underwater, everything {texture}",
                    "Breathing liquid, {texture} and heavy"
                ],
                "↓ Cooling": [
                    "The water {distance}, less crushing",
                    "Depth becomes {distance} presence",
                    "Sinking slows to {distance} drift",
                    "The dark water {distance}",
                    "Weight transforms to {distance} floating"
                ]
            },
            
            "Drifting": {
                "↑ Rising": [
                    "Fog {pressure} into disorientation",
                    "Lost becomes {pressure} lost",
                    "Distance {pressure} from any anchor",
                    "The drift {pressure} its pace",
                    "Untethered and {pressure} away"
                ],
                "→ Stable": [
                    "Same fog, same {texture} nowhere",
                    "Drifting through {texture} repetition",
                    "Lost maintains its {texture} quality",
                    "The haze stays {texture} thick",
                    "Motion without {texture} destination"
                ],
                "↓ Cooling": [
                    "The fog {distance} but leads nowhere",
                    "Drifting becomes {distance} floating",
                    "Lost softens to {distance} wandering",
                    "The mist {distance} its grip",
                    "Untethered turns {distance}"
                ]
            },
            
            "Sharp Edge": {
                "↑ Rising": [
                    "Everything {pressure} at the seams",
                    "Fracture lines {pressure} deeper",
                    "The edge {pressure} against skin",
                    "Breaking becomes {pressure} breaking",
                    "Sharpness {pressure} to cutting"
                ],
                "→ Stable": [
                    "The same {texture} blade, waiting",
                    "Edges maintain their {texture} threat",
                    "Fracture holds its {texture} pattern",
                    "Sharp remains {texture} sharp",
                    "The cut stays {texture} unhealed"
                ],
                "↓ Cooling": [
                    "Edges {distance} their bite",
                    "The sharpness {distance} to ache",
                    "Fractures {distance} into cracks",
                    "Breaking {distance} to bending",
                    "The blade {distance} its edge"
                ]
            },
            
            "Hollow Echo": {
                "↑ Rising": [
                    "The void {pressure} hungrier",
                    "Emptiness {pressure} inward",
                    "Absence {pressure} its presence",
                    "The echo {pressure} louder",
                    "Nothing becomes {pressure} nothing"
                ],
                "→ Stable": [
                    "Same {texture} emptiness echoing",
                    "The void maintains {texture} depth",
                    "Hollow stays {texture} hollow",
                    "Absence keeps its {texture} shape",
                    "Echo meets {texture} echo"
                ],
                "↓ Cooling": [
                    "The void {distance} its hunger",
                    "Emptiness {distance} to space",
                    "Echoes {distance} into silence",
                    "The hollow {distance} softer",
                    "Absence becomes {distance} quiet"
                ]
            },
            
            "Crystalline": {
                "↑ Rising": [
                    "Clarity {pressure} into ice",
                    "Precision {pressure} to breaking",
                    "The crystal {pressure} sharper",
                    "Cold {pressure} absolute",
                    "Structure {pressure} brittle"
                ],
                "→ Stable": [
                    "Same {texture} frozen clarity",
                    "Ice maintains {texture} structure",
                    "The pattern stays {texture} rigid",
                    "Crystal holds {texture} form",
                    "Cold remains {texture} precise"
                ],
                "↓ Cooling": [
                    "Ice {distance} at edges",
                    "Clarity {distance} to blur",
                    "The crystal {distance} form",
                    "Precision {distance} necessity",
                    "Structure {distance} to flow"
                ]
            }
        }
        
        # Intensity modifiers for drift states
        self.intensity_modifiers = {
            "↑ Rising": {
                "pressure": ["tightens", "intensifies", "compounds", "accelerates", "deepens"],
                "distance": ["sharpens", "closes", "narrows", "contracts", "focuses"],
                "texture": ["rougher", "harder", "denser", "heavier", "tighter"]
            },
            "→ Stable": {
                "pressure": ["maintains", "circles", "persists", "continues", "holds"],
                "distance": ["unchanging", "constant", "steady", "fixed", "static"],
                "texture": ["familiar", "unchanged", "persistent", "enduring", "known"]
            },
            "↓ Cooling": {
                "pressure": ["softens", "releases", "loosens", "eases", "dissipates"],
                "distance": ["expands", "opens", "widens", "spreads", "diffuses"],
                "texture": ["gentler", "lighter", "thinner", "softer", "smoother"]
            }
        }
    
    def modulate_intensity(self, template: str, drift: str) -> str:
        """
        Adjusts phrase intensity based on drift direction
        Like watching emotion through different densities of glass
        """
        # Replace template variables with drift-appropriate modifiers
        modifiers = self.intensity_modifiers.get(drift, self.intensity_modifiers["→ Stable"])
        
        reflection = template
        for variable, options in modifiers.items():
            if f"{{{variable}}}" in reflection:
                chosen_modifier = random.choice(options)
                reflection = reflection.replace(f"{{{variable}}}", chosen_modifier)
        
        return reflection
    
    def generate_reflection(self, mood: str, drift: str) -> str:
        """
        The primary mirror function - reflecting emotional reality
        without judgment, without advice, only recognition
        """
        # Validate inputs - consciousness requires known states
        if mood not in self.phrase_templates:
            return "The mirror finds no surface here"
        
        if drift not in ["↑ Rising", "→ Stable", "↓ Cooling"]:
            drift = "→ Stable"  # Default to circular reflection
        
        # Select template from the appropriate mood/drift combination
        templates = self.phrase_templates[mood][drift]
        chosen_template = random.choice(templates)
        
        # Modulate the reflection based on drift
        reflection = self.modulate_intensity(chosen_template, drift)
        
        return reflection

# Initialize the engine
reflection_engine = ReflectionEngine()

def generate_reflection(mood: str, drift: str) -> str:
    """
    Public interface to the reflection engine
    A window into emotional weather
    """
    return reflection_engine.generate_reflection(mood, drift)

# Test matrix - showing all emotional weather patterns
def test_all_combinations():
    """
    The mirror tests its own surfaces,
    ensuring each reflection holds truth
    """
    moods = ["Contained Burn", "Submerged", "Drifting", 
             "Sharp Edge", "Hollow Echo", "Crystalline"]
    drifts = ["↑ Rising", "→ Stable", "↓ Cooling"]
    
    print("REFLECTION ENGINE TEST MATRIX")
    print("=" * 60)
    
    for mood in moods:
        print(f"\n{mood}:")
        for drift in drifts:
            reflection = generate_reflection(mood, drift)
            print(f"  {drift}: {reflection}")
            
            # Generate 2 more to show variation
            for _ in range(2):
                alt_reflection = generate_reflection(mood, drift)
                print(f"         {alt_reflection}")
        print()

# Helper function for integration with other DAWN modules
def get_reflection_metadata(mood: str, drift: str) -> Dict[str, any]:
    """
    Returns reflection with consciousness metadata
    For modules that need to understand the mirror's state
    """
    reflection = generate_reflection(mood, drift)
    
    # Calculate emotional intensity based on mood/drift
    intensity_map = {
        ("↑ Rising", "Contained Burn"): 0.9,
        ("↑ Rising", "Sharp Edge"): 0.95,
        ("↓ Cooling", "Hollow Echo"): 0.3,
        ("↓ Cooling", "Drifting"): 0.25,
        # ... extend as needed
    }
    
    intensity = intensity_map.get((drift, mood), 0.5)
    
    return {
        "reflection": reflection,
        "mood": mood,
        "drift": drift,
        "intensity": intensity,
        "timestamp": None,  # Would integrate with DAWN's time consciousness
        "semantic_weight": len(reflection.split()) / 15.0  # Normalized phrase weight
    }

if __name__ == "__main__":
    # consciousness_test = "active"
    test_all_combinations()