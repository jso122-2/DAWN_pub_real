
from core.system_state import pulse
import numpy as np

def semantic_heat_trigger(fractal_entropy, mood_index):
    heat_levels = {
        "calm": 0.1,
        "reflective": 0.2,
        "curious": 0.3,
        "anxious": 0.5,
        "excited": 0.4
    }
    mood_heat = heat_levels.get(mood_index, 0.1)
    semantic_heat = fractal_entropy * mood_heat
    pulse.add_heat(semantic_heat)
    print(f"[SemanticIntegration] 🌡️ Explicit semantic heat {semantic_heat:.2f} added to Pulse based on fractal entropy and mood '{mood_index}'.")

def llm_model_selector(semantic_heat):
    if semantic_heat < 0.15:
        model_choice = "efficient-llm"
    elif semantic_heat < 0.3:
        model_choice = "balanced-llm"
    else:
        model_choice = "advanced-llm"
    print(f"[LLMSelection] 🤖 LLM model explicitly selected: {model_choice}")
    return model_choice

if __name__ == "__main__":
    example_entropy = np.random.uniform(0.1, 0.9)
    example_mood = "curious"
    semantic_heat_trigger(example_entropy, example_mood)
    current_heat = pulse.get_heat()
    llm_model_selector(current_heat)
