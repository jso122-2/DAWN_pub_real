# substrate/registry.py
from substrate.genesis.genetic_evolution import GeneticEvolution
from substrate.genesis.thermal_linguistic_genome import ThermalLinguisticGenome
from substrate.helix.bridge import HelixBridge
from substrate.consciousness.meta_consciousness import MetaConsciousness


class SubstrateRegistry:
    """Deep architecture layer - below core systems"""
    
    def __init__(self):
        self.genesis = None
        self.helix = None
        self.consciousness = None
        self._initialized = False
    
    def initialize_substrate(self):
        """Must run before core systems boot"""
        if self._initialized:
            return
            
        # Initialize in order
        self.genesis = GeneticEvolution()
        self.helix = HelixBridge()
        self.consciousness = MetaConsciousness()
        
        # Load initial patterns
        self.genesis.load_genetic_patterns()
        self.helix.establish_bridges()
        self.consciousness.awaken()
        
        self._initialized = True