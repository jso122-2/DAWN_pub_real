
import types

class PulseHeatHealer:
    @staticmethod
    def heal_pulse(pulse_instance):
        def adjust_urgency(self, delta):
            if not hasattr(self, 'urgency'):
                self.urgency = 0.7
            self.urgency = max(0.0, min(1.0, self.urgency + delta))
            return self.urgency
        
        pulse_instance.adjust_urgency = types.MethodType(adjust_urgency, pulse_instance)
        pulse_instance.urgency = getattr(pulse_instance, 'urgency', 0.7)
        return pulse_instance
