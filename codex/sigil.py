# codex/sigil.py
"""Sigil - Symbolic representations"""

class Sigil:
    """A symbol in DAWN's language"""
    
    def __init__(self, symbol, meaning=None, power=1.0):
        self.symbol = symbol
        self.meaning = meaning
        self.power = power
        self.invocations = 0
        
    def invoke(self):
        """Invoke the sigil's power"""
        self.invocations += 1
        return {
            'symbol': self.symbol,
            'power': self.power,
            'invocation': self.invocations
        }
        
    def __repr__(self):
        return f"<Sigil:{self.symbol}>"
