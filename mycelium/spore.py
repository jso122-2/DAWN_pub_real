# mycelium/spore.py
"""Spore - Information packets in the mycelium network"""

class Spore:
    """A packet of information traveling through mycelium"""
    
    def __init__(self, content, source=None):
        self.content = content
        self.source = source
        self.hops = []
        
    def travel_to(self, destination):
        """Record travel through network"""
        self.hops.append(destination)
        
    def __repr__(self):
        return f"<Spore from={self.source} hops={len(self.hops)}>"
