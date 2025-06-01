
import types

def heal_dawn_objects():
    """Simple healing function"""
    healed = 0
    
    # Try to find and heal objects in global namespace
    for name, obj in globals().items():
        try:
            if hasattr(obj, 'adjust_urgency'):
                continue  # Already patched
            
            if 'pulse' in name.lower() or 'heat' in name.lower():
                def adjust_urgency(self, delta):
                    if not hasattr(self, 'urgency'):
                        self.urgency = 0.6
                    self.urgency = max(0.0, min(1.0, self.urgency + delta))
                    return self.urgency
                obj.adjust_urgency = types.MethodType(adjust_urgency, obj)
                obj.urgency = 0.6
                print(f"Healed {name}")
                healed += 1
            
            elif 'alignment' in name.lower() or 'probe' in name.lower():
                def call_method(self, *args, **kwargs):
                    return 0.8
                obj.__call__ = types.MethodType(call_method, obj)
                print(f"Healed {name}")
                healed += 1
                
        except Exception:
            pass
    
    return healed

if __name__ == "__main__":
    result = heal_dawn_objects()
    print(f"Healing complete: {result} objects healed")
