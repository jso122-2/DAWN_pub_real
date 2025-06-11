"""
DAWN Visualizer - Provides visualization capabilities for DAWN's state and metrics
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json
from pathlib import Path
from datetime import datetime, timezone

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class VisualizationState:
    """Current state of visualization system"""
    active_views: List[str] = None
    metrics_history: Dict[str, List[float]] = None
    last_update: float = 0.0
    is_recording: bool = False
    
    def __post_init__(self):
        if self.active_views is None:
            self.active_views = []
        if self.metrics_history is None:
            self.metrics_history = {}

class DAWNVisualizer:
    """
    Provides visualization capabilities for DAWN's state and metrics.
    Handles metric recording, state visualization, and export functionality.
    """

    def __init__(self):
        """Initialize visualizer with default state"""
        self.state = VisualizationState()
        self.export_path = Path("visualization")
        self.export_path.mkdir(exist_ok=True)
        logger.info("Initialized DAWNVisualizer")

    def record_metrics(self, metrics: Dict[str, float]) -> None:
        """
        Record current metrics for visualization.
        Maintains history of metric values over time.
        """
        for key, value in metrics.items():
            if key not in self.state.metrics_history:
                self.state.metrics_history[key] = []
            self.state.metrics_history[key].append(value)
        logger.debug(f"Recorded metrics: {metrics}")

    def get_metric_history(self, metric_name: str) -> List[float]:
        """Get historical values for a specific metric"""
        return self.state.metrics_history.get(metric_name, [])

    def export_visualization(self, format: str = "json") -> str:
        """
        Export current visualization state to file.
        Returns path to exported file.
        """
        timestamp = int(self.state.last_update)
        filename = f"dawn_state_{timestamp}.{format}"
        filepath = self.export_path / filename
        
        if format == "json":
            with open(filepath, "w") as f:
                json.dump({
                    "metrics": self.state.metrics_history,
                    "active_views": self.state.active_views,
                    "timestamp": timestamp
                }, f, indent=2)
        
        logger.info(f"Exported visualization to {filepath}")
        return str(filepath)

    def start_recording(self) -> None:
        """Start recording metrics for visualization"""
        self.state.is_recording = True
        logger.info("Started metric recording")

    def stop_recording(self) -> None:
        """Stop recording metrics"""
        self.state.is_recording = False
        logger.info("Stopped metric recording")

    def add_view(self, view_name: str) -> None:
        """Add a new visualization view"""
        if view_name not in self.state.active_views:
            self.state.active_views.append(view_name)
            logger.info(f"Added visualization view: {view_name}")

    def remove_view(self, view_name: str) -> None:
        """Remove a visualization view"""
        if view_name in self.state.active_views:
            self.state.active_views.remove(view_name)
            logger.info(f"Removed visualization view: {view_name}")

    def get_active_views(self) -> List[str]:
        """Get list of currently active visualization views"""
        return self.state.active_views.copy()

    async def update(self, consciousness_state: Dict[str, Any] = None) -> None:
        """Update visualization with current system state
        
        Args:
            consciousness_state: Current state of consciousness system
        """
        try:
            # Update visualization state
            self.state.last_update = datetime.now(timezone.utc).timestamp()
            
            # Record metrics if state provided
            if consciousness_state:
                self.record_metrics({
                    'scup': consciousness_state.get('scup', 0.0),
                    'entropy': consciousness_state.get('entropy', 0.0),
                    'tension': consciousness_state.get('tension', 0.0),
                    'drift': consciousness_state.get('drift', 0.0)
                })
            
            # Export current state if recording
            if self.state.is_recording:
                self.export_visualization()
                
            logger.debug("Updated visualization state")
            
        except Exception as e:
            logger.error(f"Error updating visualization: {e}")

    def clear_history(self) -> None:
        """Clear all recorded metric history"""
        self.state.metrics_history.clear()
        logger.info("Cleared metric history") 