"""
Semantic Field Implementation
Core implementation of the semantic field system
"""

import math
import threading
import numpy as np
from typing import Dict, List, Set, Optional, Tuple, Callable
from dataclasses import dataclass, field
from collections import defaultdict, deque
from datetime import datetime, timedelta
import logging

from backend.cognitive.mood_urgency_probe import get_mood_probe
from backend.cognitive.entropy_fluctuation import get_entropy_fluctuation
from backend.cognitive.qualia_kernel import get_qualia_kernel
from pulse.pulse_heat import pulse, PulseHeat, add_heat
from ...field_types import (
    NodeCharge, SemanticVector, RhizomicConnection, 
    SemanticNode, RhizomicSemanticField
)
from ...field_initializer import (
    get_current_field,
    add_concept,
    activate_pathway,
    get_field_state,
    tick_semantic_field
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Export convenience functions
__all__ = [
    'get_current_field',
    'add_concept',
    'activate_pathway',
    'get_field_state',
    'tick_semantic_field'
]

# Convenience functions
def add_concept(content: str, embedding: np.ndarray, charge_type: NodeCharge = NodeCharge.STATIC_NEUTRAL) -> str:
    """Add semantic concept to the field"""
    return SemanticField.add_semantic_node(content, embedding, charge_type)

def activate_pathway(start: str, end: str) -> Optional[List[str]]:
    """Activate semantic pathway between concepts"""
    return SemanticField.activate_semantic_pathway(start, end)

def get_field_state() -> Dict:
    """Get current field state for visualization"""
    return SemanticField.get_field_visualization_data()

def tick_semantic_field() -> Dict:
    """Perform per-tick field update"""
    return SemanticField.tick_update()
