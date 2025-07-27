# router/tracer_core.py
"""Tracer Core Module"""

class TracerCore:
    def __init__(self):
        self.traces = []
        self.active = True
        
    def trace(self, event):
        """Record a trace event"""
        self.traces.append(event)
        
    def get_traces(self):
        """Get all traces"""
        return self.traces
        
    def clear_traces(self):
        """Clear trace history"""
        self.traces = []
        
    def is_active(self):
        return self.active




class TracerMoved:
    """Tracer for movement/transition events"""
    
    def __init__(self):
        self.movements = []
        self.active = True
        
    def record_move(self, from_state, to_state, metadata=None):
        """Record a state transition"""
        movement = {
            'from': from_state,
            'to': to_state,
            'metadata': metadata or {},
            'timestamp': None
        }
        self.movements.append(movement)
        return movement
        
    def get_movements(self):
        """Get all recorded movements"""
        return self.movements
        
    def clear(self):
        """Clear movement history"""
        self.movements = []


# Global instance
tracer_moved = TracerMoved()

# Global tracer instance
tracer = TracerCore()
