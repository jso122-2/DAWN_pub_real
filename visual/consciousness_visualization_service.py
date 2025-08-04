# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Consciousness Visualization Service
Integrates GUI visualization bridge with the live DAWN tick system
"""

import os
import sys
import json
import time
import asyncio
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from visual.gui_visualization_bridge import GUIVisualizationManager
    BRIDGE_AVAILABLE = True
except ImportError:
    BRIDGE_AVAILABLE = False
    logger.warning("GUI visualization bridge not available")

class ConsciousnessVisualizationService:
    """
    Service that connects DAWN's tick system to GUI visualizations
    """
    
    def __init__(self, 
                 tick_data_file: str = "/tmp/dawn_tick_data.json",
                 output_dir: str = "runtime/gui_visualizations",
                 update_interval: float = 2.0):
        
        self.tick_data_file = Path(tick_data_file)
        self.output_dir = Path(output_dir)
        self.update_interval = update_interval
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize GUI visualization manager
        if BRIDGE_AVAILABLE:
            self.viz_manager = GUIVisualizationManager()
            logger.info("GUI visualization manager initialized")
        else:
            self.viz_manager = None
            logger.warning("GUI visualization manager not available")
        
        # Service state
        self.running = False
        self.last_tick = 0
        self.last_update = time.time()
        self.update_thread = None
        
        # Statistics
        self.total_updates = 0
        self.successful_updates = 0
        self.failed_updates = 0
        
        logger.info(f"ConsciousnessVisualizationService initialized")
        logger.info(f"  - Tick data source: {self.tick_data_file}")
        logger.info(f"  - Output directory: {self.output_dir}")
        logger.info(f"  - Update interval: {self.update_interval}s")
    
    def read_latest_tick_data(self) -> Optional[Dict[str, Any]]:
        """Read the latest tick data from the DAWN system"""
        try:
            if not self.tick_data_file.exists():
                return None
            
            # Read the most recent tick data
            with open(self.tick_data_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return None
                
                # Get the last non-empty line
                for line in reversed(lines):
                    line = line.strip()
                    if line:
                        return json.loads(line)
                
                return None
                
        except Exception as e:
            logger.error(f"Error reading tick data: {e}")
            return None
    
    def update_visualizations(self, tick_data: Dict[str, Any]) -> bool:
        """Update all GUI visualizations with new tick data"""
        if not self.viz_manager:
            return False
        
        try:
            start_time = time.time()
            
            # Generate visualizations
            results = self.viz_manager.update_all_visualizations(tick_data)
            
            if results:
                # Save base64 images as files for GUI access
                for viz_type, base64_data in results.items():
                    if base64_data:
                        self.save_base64_image(viz_type, base64_data, tick_data.get('tick', 0))
                
                # Save metadata for GUI
                metadata = {
                    'timestamp': datetime.now().isoformat(),
                    'tick': tick_data.get('tick', 0),
                    'visualization_types': list(results.keys()),
                    'update_duration': time.time() - start_time,
                    'tick_data': tick_data
                }
                
                metadata_file = self.output_dir / "latest_metadata.json"
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                logger.info(f"Updated {len(results)} visualizations for tick {tick_data.get('tick', 0)} in {time.time() - start_time:.3f}s")
                return True
            else:
                logger.warning("No visualizations generated")
                return False
                
        except Exception as e:
            logger.error(f"Error updating visualizations: {e}")
            return False
    
    def save_base64_image(self, viz_type: str, base64_data: str, tick: int):
        """Save base64 image data to file for GUI access"""
        try:
            # Extract base64 data (remove data:image/png;base64, prefix)
            if base64_data.startswith('data:image/'):
                base64_data = base64_data.split(',')[1]
            
            import base64
            image_data = base64.b64decode(base64_data)
            
            # Save current image
            current_file = self.output_dir / f"{viz_type}_current.png"
            with open(current_file, 'wb') as f:
                f.write(image_data)
            
            # Save timestamped image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            timestamped_file = self.output_dir / f"{viz_type}_tick_{tick}_{timestamp}.png"
            with open(timestamped_file, 'wb') as f:
                f.write(image_data)
            
            logger.debug(f"Saved {viz_type} visualization: {current_file}")
            
        except Exception as e:
            logger.error(f"Error saving {viz_type} image: {e}")
    
    def service_loop(self):
        """Main service loop for continuous visualization updates"""
        logger.info("Starting consciousness visualization service loop")
        
        while self.running:
            try:
                # Read latest tick data
                tick_data = self.read_latest_tick_data()
                
                if tick_data:
                    current_tick = tick_data.get('tick', 0)
                    
                    # Only update if we have new tick data
                    if current_tick > self.last_tick:
                        self.last_tick = current_tick
                        self.total_updates += 1
                        
                        # Update visualizations
                        success = self.update_visualizations(tick_data)
                        
                        if success:
                            self.successful_updates += 1
                        else:
                            self.failed_updates += 1
                        
                        self.last_update = time.time()
                
                # Sleep until next update
                time.sleep(self.update_interval)
                
            except KeyboardInterrupt:
                logger.info("Service interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in service loop: {e}")
                time.sleep(self.update_interval)
        
        logger.info("Consciousness visualization service stopped")
    
    def start(self):
        """Start the visualization service"""
        if self.running:
            logger.warning("Service is already running")
            return
        
        if not self.viz_manager:
            logger.error("Cannot start service - visualization manager not available")
            return
        
        self.running = True
        self.update_thread = threading.Thread(target=self.service_loop, daemon=True)
        self.update_thread.start()
        
        logger.info("Consciousness visualization service started")
    
    def stop(self):
        """Stop the visualization service"""
        if not self.running:
            return
        
        self.running = False
        
        if self.update_thread:
            self.update_thread.join(timeout=5.0)
        
        logger.info("Consciousness visualization service stopped")
    
    def get_status(self) -> Dict[str, Any]:
        """Get service status and statistics"""
        return {
            'running': self.running,
            'last_tick': self.last_tick,
            'last_update': self.last_update,
            'total_updates': self.total_updates,
            'successful_updates': self.successful_updates,
            'failed_updates': self.failed_updates,
            'success_rate': (self.successful_updates / max(1, self.total_updates)) * 100,
            'viz_manager_available': self.viz_manager is not None,
            'output_directory': str(self.output_dir)
        }
    
    def force_update(self) -> bool:
        """Force an immediate visualization update"""
        tick_data = self.read_latest_tick_data()
        
        if not tick_data:
            logger.warning("No tick data available for forced update")
            return False
        
        logger.info(f"Forcing visualization update for tick {tick_data.get('tick', 0)}")
        return self.update_visualizations(tick_data)

def main():
    """CLI interface for the consciousness visualization service"""
    import argparse
    
    parser = argparse.ArgumentParser(description='DAWN Consciousness Visualization Service')
    parser.add_argument('--start', action='store_true', help='Start the service')
    parser.add_argument('--test', action='store_true', help='Test with simulated data')
    parser.add_argument('--status', action='store_true', help='Show service status')
    parser.add_argument('--force-update', action='store_true', help='Force immediate update')
    parser.add_argument('--interval', type=float, default=2.0, help='Update interval in seconds')
    parser.add_argument('--output-dir', default='runtime/gui_visualizations', help='Output directory')
    
    args = parser.parse_args()
    
    # Initialize service
    service = ConsciousnessVisualizationService(
        update_interval=args.interval,
        output_dir=args.output_dir
    )
    
    if args.test:
        # Test with simulated data
        print("Testing consciousness visualization service...")
        
        test_data = {
            'tick': 100,
            'entropy': 0.65,
            'scup': 0.42,
            'heat': 0.58,
            'mood': 'CONTEMPLATIVE',
            'zone': 'ACTIVE',
            'reblooms': 3,
            'sigils': 2,
            'drift': 0.31
        }
        
        success = service.update_visualizations(test_data)
        if success:
            print(f"✅ Test successful! Visualizations saved to: {service.output_dir}")
        else:
            print("❌ Test failed!")
    
    elif args.status:
        # Show service status
        status = service.get_status()
        print("\n🧠 DAWN Consciousness Visualization Service Status")
        print("=" * 60)
        for key, value in status.items():
            print(f"  {key}: {value}")
        print("=" * 60)
    
    elif args.force_update:
        # Force immediate update
        print("Forcing visualization update...")
        success = service.force_update()
        if success:
            print("✅ Update successful!")
        else:
            print("❌ Update failed!")
    
    elif args.start:
        # Start the service
        print("Starting DAWN Consciousness Visualization Service...")
        print(f"Update interval: {args.interval}s")
        print(f"Output directory: {args.output_dir}")
        print("Press Ctrl+C to stop")
        
        try:
            service.start()
            
            # Keep main thread alive
            while service.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nStopping service...")
            service.stop()
            
        # Show final status
        status = service.get_status()
        print(f"\nFinal Statistics:")
        print(f"  Total updates: {status['total_updates']}")
        print(f"  Successful: {status['successful_updates']}")
        print(f"  Failed: {status['failed_updates']}")
        print(f"  Success rate: {status['success_rate']:.1f}%")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 