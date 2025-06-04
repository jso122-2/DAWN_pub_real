# /core/pulse_ring_trigger.py

"""
Detects pressure zone transitions and emits trigger events
(e.g. enter surge → release overflow, activate override)
"""

class PulseRing:
    def __init__(self):
        self.last_zone = "🟢 calm"
        self.transition_hooks = {
            "🟡 active": [],
            "🔴 surge": [],
            "🟢 calm": []
        }

    def on_transition(self, zone, callback):
        """Register a function to run when entering a specific zone."""
        if zone in self.transition_hooks:
            self.transition_hooks[zone].append(callback)
            print(f"[PulseRing] ✅ Hook registered for {zone}")
        else:
            print(f"[PulseRing] ⚠️ Unknown zone: {zone}")

    def check_transition(self, current_zone):
        if current_zone != self.last_zone:
            print(f"[PulseRing] ⚠️ Zone shift: {self.last_zone} → {current_zone}")
            self.last_zone = current_zone

            # 🧠 Trigger all registered hooks
            for func in self.transition_hooks.get(current_zone, []):
                try:
                    func()
                except Exception as e:
                    print(f"[PulseRing] ❌ Hook error: {e}")

            return True
        return False
