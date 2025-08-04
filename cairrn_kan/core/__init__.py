"""
KAN-Cairrn Core Module

Core components for the KAN-Cairrn interpretable function space navigation system.
"""

from ...spline_neurons import SplineNeuronManager, LearnableSplineFunction
from ...kan_topology import KANTopologyManager
from ...entropy_engine import EntropyEngine
from ...weave_router import WeaveRouter

__all__ = [
    'SplineNeuronManager',
    'LearnableSplineFunction', 
    'KANTopologyManager',
    'EntropyEngine',
    'WeaveRouter'
] 