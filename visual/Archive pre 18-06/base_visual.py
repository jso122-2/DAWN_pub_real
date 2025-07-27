"""
Base Visual Process - Base class for all visualizers
"""

import logging
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class VisualState:
    """Base state for visual processes"""
    is_active: bool = False
    last_update: float = field(default_factory=time.time)
    frame_count: int = 0
    metrics: Dict[str, float] = field(default_factory=dict)
    history: List[Dict] = field(default_factory=list)

class BaseVisualProcess:
    """
    Base class for all visual processes.
    Provides common functionality for visualization and metrics tracking.
    """
    
    def __init__(self):
        """Initialize base visual process"""
        self.state = VisualState()
        self.config = {
            'update_interval': 0.5,  # 500ms
            'history_limit': 100,
            'metrics': {
                'fps': 0.0,
                'latency': 0.0,
                'memory_usage': 0.0
            }
        }
        logger.info(f"Initialized {self.__class__.__name__}")
    
    def start(self) -> None:
        """Start the visual process"""
        if not self.state.is_active:
            self.state.is_active = True
            self.state.last_update = time.time()
            logger.info(f"Started {self.__class__.__name__}")
    
    def stop(self) -> None:
        """Stop the visual process"""
        if self.state.is_active:
            self.state.is_active = False
            logger.info(f"Stopped {self.__class__.__name__}")
    
    def update_metrics(self, delta_time: float) -> None:
        """
        Update visual process metrics
        
        Args:
            delta_time: Time since last update
        """
        if not self.state.is_active:
            return
        
        # Update frame count
        self.state.frame_count += 1
        
        # Calculate FPS
        if delta_time > 0:
            self.state.metrics['fps'] = 1.0 / delta_time
        
        # Update latency
        self.state.metrics['latency'] = delta_time * 1000  # Convert to ms
        
        # Record metrics in history
        self._record_metrics()
    
    def _record_metrics(self) -> None:
        """Record current metrics in history"""
        metrics_record = {
            'timestamp': datetime.now().isoformat(),
            'metrics': self.state.metrics.copy(),
            'frame_count': self.state.frame_count
        }
        
        self.state.history.append(metrics_record)
        if len(self.state.history) > self.config['history_limit']:
            self.state.history = self.state.history[-self.config['history_limit']:]
    
    def process_visual_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process visual data
        
        Args:
            data: Input visual data
            
        Returns:
            Processed visual data or None
        """
        if not self.state.is_active or not data:
            return None
        
        # Update metrics
        current_time = time.time()
        delta_time = current_time - self.state.last_update
        self.state.last_update = current_time
        
        self.update_metrics(delta_time)
        
        # Process data (to be implemented by subclasses)
        return self._process_data(data)
    
    def _process_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process data (to be implemented by subclasses)
        
        Args:
            data: Input data
            
        Returns:
            Processed data or None
        """
        raise NotImplementedError("Subclasses must implement _process_data")
    
    def get_visual_state(self) -> Dict:
        """Get current visual state"""
        return {
            'is_active': self.state.is_active,
            'frame_count': self.state.frame_count,
            'metrics': self.state.metrics.copy(),
            'history_size': len(self.state.history)
        }
    
    def get_metrics_json(self) -> str:
        """Get current metrics as JSON string"""
        return json.dumps({
            "type": "metrics",
            "subprocess_id": self.__class__.__name__.lower(),
            "metrics": self.state.metrics,
            "timestamp": time.time()
        })
    
    def clear_history(self) -> None:
        """Clear visual process history"""
        self.state.history.clear()
        logger.info(f"Cleared history for {self.__class__.__name__}")
    
    def reset(self) -> None:
        """Reset visual process state"""
        self.state = VisualState()
        logger.info(f"Reset {self.__class__.__name__}")

# Global registry of visual processes
_visual_processes = {}

def register_visual_process(process: BaseVisualProcess) -> None:
    """
    Register a visual process
    
    Args:
        process: Visual process to register
    """
    process_id = process.__class__.__name__.lower()
    _visual_processes[process_id] = process
    logger.info(f"Registered visual process: {process_id}")

def get_visual_process(process_id: str) -> Optional[BaseVisualProcess]:
    """
    Get a registered visual process
    
    Args:
        process_id: ID of the visual process
        
    Returns:
        Visual process or None if not found
    """
    return _visual_processes.get(process_id.lower())

def get_all_visual_processes() -> Dict[str, BaseVisualProcess]:
    """
    Get all registered visual processes
    
    Returns:
        Dictionary of visual processes
    """
    return _visual_processes.copy()

__all__ = [
    'BaseVisualProcess',
    'VisualState',
    'register_visual_process',
    'get_visual_process',
    'get_all_visual_processes'
] 