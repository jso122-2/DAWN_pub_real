
from core.system_state import pulse
import numpy as np

def dynamic_pulse_intensity(fractal_entropy, mood):
    mood_heat_factors = {
        "calm": 0.2,
        "reflective": 0.4,
        "curious": 0.6,
        "anxious": 0.8,
        "excited": 1.0
    }
    mood_heat = mood_heat_factors.get(mood, 0.3)
    semantic_intensity = fractal_entropy * mood_heat
    pulse.set_intensity(semantic_intensity)
    print(f"[SemanticIntegration] 🌡️ Explicit Pulse intensity set to {semantic_intensity:.2f} based on entropy={fractal_entropy:.2f}, mood='{mood}'.")

def select_llm_model(semantic_intensity):
    if semantic_intensity < 0.25:
        chosen_model = "efficient-model"
    elif semantic_intensity < 0.5:
        chosen_model = "balanced-model"
    elif semantic_intensity < 0.75:
        chosen_model = "advanced-model"
    else:
        chosen_model = "high-power-model"
    pulse.set_model(chosen_model)
    print(f"[SemanticIntegration] 🤖 LLM explicitly selected: {chosen_model}")

if __name__ == "__main__":
    fractal_entropy_example = np.random.uniform(0.1, 0.9)
    mood_example = "reflective"
    dynamic_pulse_intensity(fractal_entropy_example, mood_example)
    select_llm_model(pulse.get_intensity())
