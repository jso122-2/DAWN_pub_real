# /core/mood.py

def calculate_mood_urgency(mood_state):
    """Weighted urgency by mood proportion."""
    weights = {"stressed": 0.9, "reflective": 0.6, "resilient": 0.3}
    return sum(weights.get(m, 0.5) * v for m, v in mood_state.items())


class MoodEngine:
    """Mood Engine - Emotional state management"""
    
    def __init__(self):
        self.active = False
        self.current_mood = 'neutral'
        self.mood_history = []
        
    def initialize(self, event_bus=None):
        self.event_bus = event_bus
        self.active = True
        
    def set_mood(self, mood):
        """Set current mood"""
        self.mood_history.append(self.current_mood)
        self.current_mood = mood
        
        if self.event_bus:
            self.event_bus.publish('mood.changed', {
                'from': self.mood_history[-1] if self.mood_history else None,
                'to': mood
            })
            
    def get_mood(self):
        """Get current mood"""
        return self.current_mood
        
    def get_mood_spectrum(self):
        """Get available moods"""
        return ['neutral', 'curious', 'anxious', 'joyful', 'contemplative', 'excited']
        
    def shutdown(self):
        self.active = False
        
    def get_status(self):
        return {
            'active': self.active,
            'current_mood': self.current_mood,
            'history_length': len(self.mood_history)
        }
