"""
Semantic Field Initializer
Handles initialization and access to the semantic field instance
"""

import numpy as np
import logging
from typing import Dict, List, Optional
from datetime import datetime

from ...field_types import NodeCharge, RhizomicSemanticField

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global semantic field instance
_semantic_field = None

def initialize_field() -> None:
    """Initialize the semantic field instance"""
    global _semantic_field
    if _semantic_field is None:
        _semantic_field = RhizomicSemanticField()
        logger.info("Initialized semantic field")

def get_current_field() -> RhizomicSemanticField:
    """Get the current semantic field instance"""
    global _semantic_field
    if _semantic_field is None:
        initialize_field()
    return _semantic_field

# Convenience functions
def add_concept(content: str, embedding: np.ndarray, charge_type: NodeCharge = NodeCharge.STATIC_NEUTRAL) -> str:
    """Add semantic concept to the field"""
    field = get_current_field()
    return field.add_semantic_node(content, embedding, charge_type)

def activate_pathway(start: str, end: str) -> Optional[List[str]]:
    """Activate semantic pathway between concepts"""
    field = get_current_field()
    return field.activate_semantic_pathway(start, end)

def get_field_state() -> Dict:
    """Get current field state for visualization"""
    field = get_current_field()
    return field.get_field_visualization_data()

def tick_semantic_field() -> Dict:
    """Perform per-tick field update"""
    field = get_current_field()
    return field.tick_update()

__all__ = ['initialize_field', 'get_current_field', 'add_concept', 'activate_pathway', 'get_field_state', 'tick_semantic_field'] 