"""
DAWN KAN-Cairrn Integration System

Cursor serves as DAWN's neural navigation layer - a contextual pointer system that 
traverses the Kolmogorov-Arnold Network (KAN) where Cairrn caches assemblages as 
learnable spline functions.
"""

"""
DAWN KAN-Cairrn Integration System

Cursor serves as DAWN's neural navigation layer - a contextual pointer system that 
traverses the Kolmogorov-Arnold Network (KAN) where Cairrn caches assemblages as 
learnable spline functions.
"""

from .core.kan_topology import KANTopologyManager
from .core.spline_neurons import SplineNeuronManager
from .core.weave_router import WeaveRouter
from .core.entropy_engine import EntropyEngine
from .cursor.function_navigator import FunctionNavigator
from .cursor.interpretability import SplineInterpreter
from .cursor.trajectory_learner import TrajectoryLearner
from ...models import (
    SplineNeuron, KANTopology, CursorState, FunctionPath, 
    NavigationResult, CachedGlyph, KANConfig, CairrConfig,
    LearnableSplineFunction
)

__version__ = "1.0.0"
__author__ = "DAWN Development Team"

__all__ = [
    'KANTopologyManager',
    'SplineNeuronManager', 
    'WeaveRouter',
    'EntropyEngine',
    'FunctionNavigator',
    'SplineInterpreter',
    'TrajectoryLearner',
    'SplineNeuron',
    'KANTopology',
    'CursorState',
    'FunctionPath',
    'NavigationResult',
    'CachedGlyph',
    'KANConfig',
    'CairrConfig',
    'LearnableSplineFunction'
] 