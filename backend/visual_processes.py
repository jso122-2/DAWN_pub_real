"""
DAWN Visual Processes Manager
"""

import logging
import asyncio
from typing import Dict, List, Optional
from visual import (
    BaseVisualizer,
    DriftVectorFieldRenderer,
    ConsciousnessWaveVisualizer,
    EntropyHistogramVisualizer,
    MoodHeatmapVisualizer,
    ProcessTimelineVisualizer,
    NeuralHeatmapVisualizer,
    MetricsRadarVisualizer
)

logger = logging.getLogger(__name__)

class VisualProcessManager:
    def __init__(self):
        self.visualizers: Dict[str, BaseVisualizer] = {}
        self.is_running = False
        self.update_interval = 1.0  # seconds
        
    def initialize_visualizers(self):
        """Initialize all visualizers"""
        try:
            # Create visualizer instances
            self.visualizers = {
                'drift': DriftVectorFieldRenderer(),
                'consciousness': ConsciousnessWaveVisualizer(),
                'entropy': EntropyHistogramVisualizer(),
                'mood': MoodHeatmapVisualizer(),
                'process': ProcessTimelineVisualizer(),
                'neural': NeuralHeatmapVisualizer(),
                'metrics': MetricsRadarVisualizer()
            }
            
            logger.info(f"Initialized {len(self.visualizers)} visualizers")
            
        except Exception as e:
            logger.error(f"Error initializing visualizers: {e}")
            raise
    
    async def start(self):
        """Start all visualizers"""
        if self.is_running:
            return
            
        self.is_running = True
        self.initialize_visualizers()
        
        for name, visualizer in self.visualizers.items():
            try:
                visualizer.start()
                logger.info(f"Started {name} visualizer")
            except Exception as e:
                logger.error(f"Error starting {name} visualizer: {e}")
    
    async def stop(self):
        """Stop all visualizers"""
        if not self.is_running:
            return
            
        self.is_running = False
        
        for name, visualizer in self.visualizers.items():
            try:
                visualizer.stop()
                visualizer.cleanup()
                logger.info(f"Stopped {name} visualizer")
            except Exception as e:
                logger.error(f"Error stopping {name} visualizer: {e}")
    
    async def update(self, data: Dict):
        """Update all visualizers with new data"""
        if not self.is_running:
            return
            
        for name, visualizer in self.visualizers.items():
            try:
                visualizer.update(data)
            except Exception as e:
                logger.error(f"Error updating {name} visualizer: {e}")
    
    def get_visualizer(self, name: str) -> Optional[BaseVisualizer]:
        """Get a specific visualizer by name"""
        return self.visualizers.get(name)
    
    def get_all_visualizers(self) -> List[BaseVisualizer]:
        """Get all visualizers"""
        return list(self.visualizers.values())

# Create global instance
visual_manager = VisualProcessManager() 