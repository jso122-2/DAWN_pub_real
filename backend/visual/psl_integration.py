"""
DAWN PSL (Python Standard Library) Integration
Provides visualization and analysis tools using Python Standard Library components
"""

import os
import sys
import time
import json
import os
import os
import os
import os
import logging
import datetime
import statistics
import collections
import itertools
import functools
import signal
import atexit
import io
import base64
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass
from collections import deque, defaultdict, Counter

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap

# Import GIF saver
import signal
import atexit

    from .gif_saver import setup_gif_saver
    from gif_saver import setup_gif_saver

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class PSLMetrics:
    """Container for PSL-based system metrics"""
    cpu_usage: List[float] = None
    memory_usage: List[float] = None
    process_count: List[int] = None
    file_operations: List[int] = None
    network_io: List[int] = None
    timestamps: List[float] = None
    
    def __post_init__(self):
        if self.cpu_usage is None:
            self.cpu_usage = []
        if self.memory_usage is None:
            self.memory_usage = []
        if self.process_count is None:
            self.process_count = []
        if self.file_operations is None:
            self.file_operations = []
        if self.network_io is None:
            self.network_io = []
        if self.timestamps is None:
            self.timestamps = []

class PSLVisualizer:
    """Visualization and analysis tools using Python Standard Library"""
    
    def __init__(self, 
                 output_dir: str = "visual/outputs/psl",
                 window_size: int = 100,
                 update_interval: float = 1.0):
        """
        Initialize PSL visualizer
        
        Args:
            output_dir: Directory for saving visualizations
            window_size: Number of data points to display
            update_interval: Update frequency in seconds
        """
        self.output_dir = Path(output_dir)
        self.window_size = window_size
        self.update_interval = update_interval
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize metrics
        self.metrics = PSLMetrics()
        
        # Setup matplotlib
        plt.style.use('dark_background')
        self.fig = None
        self.ax = None
        self.animation = None
        
        # Performance tracking
        self.performance_stats = defaultdict(list)
        self.start_time = time.time()
        
        # Setup GIF saver
        self.gif_saver = setup_gif_saver("psl_integration")
        
        # Setup signal handlers for GIF saving
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        atexit.register(self.cleanup)
        
        logger.info("Initialized PSL Visualizer")
    
    def save_animation_gif(self):
        """Save the animation as GIF"""

            if hasattr(self, 'animation') and self.animation is not None:
                gif_path = self.gif_saver.save_animation_as_gif(self.animation, fps=5, dpi=100)
                if gif_path:
                    print(f"\nAnimation GIF saved: {gif_path}", file=sys.stderr)
                else:
                    print("\nFailed to save animation GIF", file=sys.stderr)
            else:
                print("\nNo animation to save", file=sys.stderr)
            print(f"\nError saving animation GIF: {e}", file=sys.stderr)

    def cleanup(self):
        """Cleanup function to save GIF"""
        self.save_animation_gif()

    def signal_handler(self, signum, frame):
        """Signal handler to save GIF on termination"""
        print(f"\nReceived signal {signum}, saving GIF...", file=sys.stderr)
        self.save_animation_gif()
    
    def collect_metrics(self) -> None:
        """Collect system metrics using PSL"""

            # CPU usage (using psutil if available, otherwise estimate)

                import psutil
                cpu_percent = psutil.cpu_percent()
                cpu_percent = 0.0  # Placeholder if psutil not available
            
            # Memory usage

                import psutil
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                memory_percent = 0.0
            
            # Process count
            process_count = len(os.popen('tasklist').readlines()) if os.name == 'nt' else len(os.popen('ps').readlines())
            
            # File operations (placeholder)
            file_ops = 0
            
            # Network I/O (placeholder)
            network_io = 0
            
            # Update metrics
            timestamp = time.time()
            self.metrics.cpu_usage.append(cpu_percent)
            self.metrics.memory_usage.append(memory_percent)
            self.metrics.process_count.append(process_count)
            self.metrics.file_operations.append(file_ops)
            self.metrics.network_io.append(network_io)
            self.metrics.timestamps.append(timestamp)
            
            # Trim to window size
            for attr in self.metrics.__dataclass_fields__:
                values = getattr(self.metrics, attr)
                if len(values) > self.window_size:
                    setattr(self.metrics, attr, values[-self.window_size:])
            
            logger.error(f"Error collecting metrics: {e}")
    
    def generate_visualization(self) -> str:
        """Generate system metrics visualization"""

            if self.fig is None:
                self.fig, self.ax = plt.subplots(figsize=(12, 6))
            
            self.ax.clear()
            
            # Plot metrics
            time_axis = np.array(self.metrics.timestamps) - self.metrics.timestamps[0]
            
            # CPU and Memory
            self.ax.plot(time_axis, self.metrics.cpu_usage, 
                        label='CPU %', color='#00ff41', linewidth=2)
            self.ax.plot(time_axis, self.metrics.memory_usage, 
                        label='Memory %', color='#00cc33', linewidth=2)
            
            # Process count
            ax2 = self.ax.twinx()
            ax2.plot(time_axis, self.metrics.process_count, 
                    label='Processes', color='#ffb000', linewidth=2)
            
            # Styling
            self.ax.set_facecolor('#000000')
            self.fig.patch.set_facecolor('#000000')
            
            # Labels and title
            self.ax.set_xlabel('Time (s)', color='#f0f0f0')
            self.ax.set_ylabel('Usage %', color='#f0f0f0')
            ax2.set_ylabel('Process Count', color='#f0f0f0')
            
            self.ax.set_title('PSL System Metrics', 
                             color='#f0f0f0', 
                             fontfamily='monospace',
                             fontsize=12,
                             pad=20)
            
            # Grid
            self.ax.grid(True, color='#1a1a1a', linestyle='--', alpha=0.3)
            
            # Legends
            lines1, labels1 = self.ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            self.ax.legend(lines1 + lines2, labels1 + labels2, 
                          loc='upper right',
                          framealpha=0.8)
            
            # Current values display
            current_values = (
                f"CPU: {self.metrics.cpu_usage[-1]:.1f}%\n"
                f"Memory: {self.metrics.memory_usage[-1]:.1f}%\n"
                f"Processes: {self.metrics.process_count[-1]}"
            )
            
            self.ax.text(0.02, 0.98, current_values,
                        transform=self.ax.transAxes,
                        verticalalignment='top',
                        fontfamily='monospace',
                        color='#f0f0f0',
                        bbox=dict(boxstyle='round',
                                facecolor='#1a1a1a',
                                alpha=0.8))
            
            plt.tight_layout()
            
            # Save to buffer
            buffer = io.BytesIO()
            self.fig.savefig(buffer, format='png', 
                            facecolor='#000000',
                            edgecolor='none',
                            bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            
            return f"data:image/png;base64,{image_base64}"
            
            logger.error(f"Error generating visualization: {e}")
            return None
    
    def start_monitoring(self) -> None:
        """Start continuous monitoring and visualization"""

            def update(frame):
                self.collect_metrics()
                return self.generate_visualization()
            
            self.animation = animation.FuncAnimation(frames=1000, 
                self.fig, update,
                interval=self.update_interval * 1000,
                blit=False
            )
            
            plt.show()
            
            logger.error(f"Error starting monitoring: {e}")
    
    def save_snapshot(self, filename: str = None) -> Optional[Path]:
        """Save current visualization as image"""

            if filename is None:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"psl_metrics_{timestamp}.png"
            
            output_path = self.output_dir / filename
            self.fig.savefig(output_path,
                            facecolor='#000000',
                            edgecolor='none',
                            bbox_inches='tight',
                            dpi=150)
            
            logger.info(f"Saved snapshot to {output_path}")
            return output_path
            
            logger.error(f"Error saving snapshot: {e}")
            return None
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics"""
        stats = {}
        
        # Calculate statistics using PSL
        for metric, values in self.performance_stats.items():
            if values:
                stats[f"{metric}_mean"] = statistics.mean(values)
                stats[f"{metric}_median"] = statistics.median(values)
                stats[f"{metric}_stdev"] = statistics.stdev(values) if len(values) > 1 else 0
                stats[f"{metric}_min"] = min(values)
                stats[f"{metric}_max"] = max(values)
        
        return stats
    
    def close(self) -> None:
        """Clean up resources"""
        if self.animation:
            self.animation.event_source.stop()
        if self.fig:
            plt.close(self.fig)
        logger.info("Closed PSL Visualizer")

if __name__ == "__main__":
    visualizer = PSLVisualizer()

        visualizer.start_monitoring()
        visualizer.close()