# core/system/substrate_integration.py
from substrate.registry import SubstrateRegistry


class SubstrateIntegration:
    """Connects substrate layer to core systems"""
    
    def __init__(self):
        self.substrate = SubstrateRegistry()
        
    def boot_substrate(self):
        """Initialize substrate before core systems"""
        print("[SUBSTRATE] Initializing deep architecture layer...")
        self.substrate.initialize_substrate()
        print("[SUBSTRATE] Ready.")
        
    def get_genome_engine(self):
        """Get genesis/genome for bloom evolution"""
        return self.substrate.genesis
        
    def get_helix_bridge(self):
        """Get helix for system connections"""
        return self.substrate.helix
        
    def get_consciousness(self):
        """Get meta-consciousness for owl"""
        return self.substrate.consciousness