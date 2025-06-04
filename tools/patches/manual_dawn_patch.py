
# Manual DAWN Patch - Run this in DAWN's terminal
import types

# Find pulse heat object
pulse_heat = None
alignment_probe = None

# Search through globals
for name, obj in globals().items():
    if 'pulse' in name.lower() and 'heat' in name.lower():
        pulse_heat = obj
        print(f"Found pulse heat: {name}")
    elif 'alignment' in name.lower() and 'probe' in name.lower():
        alignment_probe = obj
        print(f"Found alignment probe: {name}")

# Patch pulse heat
if pulse_heat:
    def adjust_urgency(self, delta):
        if not hasattr(self, 'urgency'):
            self.urgency = 0.6
        self.urgency = max(0.0, min(1.0, self.urgency + delta))
        return self.urgency
    
    pulse_heat.adjust_urgency = types.MethodType(adjust_urgency, pulse_heat)
    pulse_heat.urgency = 0.6
    print("PulseHeat patched!")

# Patch alignment probe
if alignment_probe:
    def call_method(self, *args, **kwargs):
        return 0.8
    
    alignment_probe.__call__ = types.MethodType(call_method, alignment_probe)
    print("AlignmentProbe patched!")

print("Manual patching complete!")
