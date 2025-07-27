# codex/codex_core.py
"""Core Codex functionality"""

class CodexCore:
    """The core codex system"""
    
    def __init__(self):
        self.sigils = {}
        self.active = True
        
    def register_sigil(self, sigil):
        """Register a new sigil"""
        self.sigils[sigil.symbol] = sigil
        
    def lookup(self, symbol):
        """Look up a sigil by symbol"""
        return self.sigils.get(symbol)
        
    def get_all_sigils(self):
        """Get all registered sigils"""
        return list(self.sigils.values())
