class MoodField:
    """Tracks and visualizes the mood state of DAWN's consciousness."""
    def __init__(self, tick_window=100):
        self.tick_window = tick_window
        self.mood_history = []

    @property
    def stability_measure(self):
        # Stub: always return 1.0 (fully stable)
        return 1.0

    def update(self, mood, tick):
        self.mood_history.append((tick, mood))
        if len(self.mood_history) > self.tick_window:
            self.mood_history.pop(0)

    def get_field_visualization_data(self):
        return {
            "history": self.mood_history,
            "current_mood": self.mood_history[-1][1] if self.mood_history else "NEUTRAL"
        }

    def infer_mood(self):
        # Simple majority vote over recent moods
        if not self.mood_history:
            return ("NEUTRAL", 1.0, {"NEUTRAL": 1.0})
        moods = [m for _, m in self.mood_history]
        from collections import Counter
        mood_counts = Counter(moods)
        most_common, count = mood_counts.most_common(1)[0]
        confidence = count / len(moods)
        mood_probs = {m: c / len(moods) for m, c in mood_counts.items()}
        return (most_common, confidence, mood_probs)

    def update_field(self, context, response_feedback=None):
        # Stub: just append the mood from context
        mood = context.get('mood', 'NEUTRAL')
        tick = context.get('tick_number', len(self.mood_history))
        self.update(mood, tick) 