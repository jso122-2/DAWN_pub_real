#!/usr/bin/env python3
"""
PSL Integration Bypass
Temporary bypass to avoid indentation errors in PSL integration
Allows backend to run with fragment speech integration
"""

import logging
import numpy as np
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class PSLVisualizer:
    """Bypass PSL visualizer to avoid import errors"""
    
    def __init__(self):
        self.enabled = False
        logger.info("PSL Visualizer bypass initialized")
    
    def update(self, data: Dict[str, Any]):
        """Bypass update method"""
        pass
    
    def render(self):
        """Bypass render method"""
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """Bypass state method"""
        return {'status': 'bypass_mode'}

# Global instance
_psl_visualizer = None

def get_psl_visualizer() -> PSLVisualizer:
    """Get PSL visualizer instance"""
    global _psl_visualizer
    if _psl_visualizer is None:
        _psl_visualizer = PSLVisualizer()
    return _psl_visualizer

def initialize_psl_visualizer():
    """Initialize PSL visualizer"""
    return get_psl_visualizer()

# Export bypass
__all__ = ['PSLVisualizer', 'get_psl_visualizer', 'initialize_psl_visualizer'] 