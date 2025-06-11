# network/router/tracer_core.py
"""Tracer Core - Tracking for DAWN"""

class TracerCore:
    def __init__(self):
        self.traces = []
        
    def trace(self, event):
        self.traces.append(event)
        
    def get_traces(self):
        return self.traces
