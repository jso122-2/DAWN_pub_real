# sigils/SigilDecayCurve.py

import math

class SigilDecayCurve:
    def __init__(self, half_life=10.0):
        self.half_life = half_life

    def decay_factor(self, time_elapsed: float) -> float:
        """Exponential decay function for sigil intensity"""
        return math.exp(-time_elapsed / self.half_life)

    def is_expired(self, initial_time: float, current_time: float, threshold: float = 0.01) -> bool:
        return self.decay_factor(current_time - initial_time) < threshold 