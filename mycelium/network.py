# mycelium/network.py
"""Mycelium Network - Underground communication"""

class MyceliumNetwork:
    """The underground network connecting DAWN's components"""
    
    def __init__(self):
        self.connections = {}
        self.nutrients = {}
        self.active = True
        
    def connect(self, source, target):
        """Create a mycelial connection"""
        if source not in self.connections:
            self.connections[source] = []
        self.connections[source].append(target)
        
    def share_nutrients(self, source, nutrient_type, data):
        """Share nutrients through the network"""
        self.nutrients[nutrient_type] = data
        # Propagate to connected nodes
        for target in self.connections.get(source, []):
            # Nutrient sharing logic
            pass
            
    def get_status(self):
        return {
            'active': self.active,
            'connections': len(self.connections),
            'nutrient_types': list(self.nutrients.keys())
        }


# Global network
network = MyceliumNetwork()
