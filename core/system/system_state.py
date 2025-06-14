from helix_import_architecture import helix_import
from substrate import pulse_heat
from owl.owl_auditor import OwlAuditor
from mycelium.nutrient_utils import get_nutrient_heat

# Get pulse from the imported module or create it
if hasattr(pulse_heat, 'pulse'):
    pulse = pulse_heat.pulse
else:
    # Try to get from UnifiedPulseHeat
    UnifiedPulseHeat = getattr(pulse_heat, 'UnifiedPulseHeat', None)
    if UnifiedPulseHeat:
        pulse = UnifiedPulseHeat()
        print("[SystemState] Created new pulse instance")
    else:
        # Fallback - try to get from global
        import builtins
        pulse = getattr(builtins, 'pulse', None)
        if not pulse:
            print("[SystemState] ⚠️ Warning: No pulse system available")
            # Create a minimal mock pulse for compatibility
            class MockPulse:
                def __init__(self):
                    self.heat = 1.0
                def get_heat(self):
                    return self.heat
                def add_heat(self, source, amount, reason=""):
                    self.heat += amount
                    print(f"[MockPulse] Heat added: {amount}")
            pulse = MockPulse()

# Now we can create the owl with pulse
tick_counter = 0
owl = OwlAuditor(pulse)

def emit_tick():
    global tick_counter
    tick_counter += 1
    print(f"[Tick] ⏱️ Emitting Tick {tick_counter}")
    return tick_counter

def current_tick():
    return tick_counter

# Create system state dictionary
system_state = {
    "pulse": pulse,
    "get_nutrient_heat": get_nutrient_heat,
    "owl": owl,
}

# Make pulse available for import
__all__ = ['pulse', 'owl', 'system_state', 'emit_tick', 'current_tick']

print(f"[SystemState] ✅ System state initialized with pulse: {pulse.__class__.__name__}")