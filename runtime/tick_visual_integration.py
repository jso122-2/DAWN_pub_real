#!/usr/bin/env python3
"""
DAWN Tick Loop Visual Integration Example

Shows how to integrate visual snapshotting into existing DAWN tick loops.
This can be imported and used by any DAWN system component.

Example integration:
    from runtime.tick_visual_integration import VisualTickIntegration
    
    visual_integration = VisualTickIntegration()
    
    # In your tick loop:
    visual_integration.process_tick(tick_data)
"""

import os
import sys
import json
import time
from typing import Dict, Any, Optional, List
import logging

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

# Import visual trigger
try:
    from visual.visual_trigger import trigger_visual_snapshot, save_tick_visualization
    VISUAL_TRIGGER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Visual trigger not available: {e}")
    VISUAL_TRIGGER_AVAILABLE = False

logger = logging.getLogger(__name__)

class VisualTickIntegration:
    """Integration helper for adding visual snapshotting to DAWN tick loops"""
    
    def __init__(self, snapshot_interval: int = 10, enable_auto_snapshot: bool = True):
        self.snapshot_interval = snapshot_interval
        self.enable_auto_snapshot = enable_auto_snapshot
        self.last_snapshot_tick = 0
        self.total_snapshots = 0
        self.visual_enabled = VISUAL_TRIGGER_AVAILABLE
        
        logger.info(f"🎨 Visual integration initialized (interval: {snapshot_interval}, enabled: {self.visual_enabled})")
    
    def process_tick(self, tick_data: Dict[str, Any]) -> Optional[List[str]]:
        """Process a tick and potentially trigger visual snapshot (non-blocking)"""
        if not self.visual_enabled or not self.enable_auto_snapshot:
            return None
            
        try:
            current_tick = tick_data.get('tick_number', tick_data.get('tick', 0))
            
            # Check if we should snapshot this tick
            if (current_tick - self.last_snapshot_tick) >= self.snapshot_interval:
                logger.debug(f"📸 Triggering visual snapshot for tick {current_tick}")
                
                # Use timeout protection for visual rendering
                import threading
                import queue
                import time
                
                result_queue = queue.Queue()
                
                def render_with_timeout():
                    try:
                        rendered_files = trigger_visual_snapshot(tick_data, every_n_ticks=self.snapshot_interval)
                        result_queue.put(('success', rendered_files))
                    except Exception as e:
                        result_queue.put(('error', str(e)))
                
                # Start rendering in background thread with timeout
                render_thread = threading.Thread(target=render_with_timeout, daemon=True)
                render_thread.start()
                render_thread.join(timeout=15.0)  # 15 second timeout for all visual processing
                
                try:
                    result_type, result_data = result_queue.get_nowait()
                    if result_type == 'success' and result_data:
                        self.total_snapshots += 1
                        self.last_snapshot_tick = current_tick
                        logger.info(f"📸 Tick {current_tick}: Generated {len(result_data)} visualizations")
                        return result_data
                    elif result_type == 'error':
                        logger.warning(f"Visual rendering error: {result_data}")
                except queue.Empty:
                    logger.warning(f"Visual rendering timed out for tick {current_tick}")
                    
        except Exception as e:
            logger.error(f"Visual integration error: {e}")
            
        return None
    
    def force_snapshot(self, tick_data: Dict[str, Any]) -> Optional[List[str]]:
        """Force an immediate visual snapshot regardless of interval"""
        if not self.visual_enabled:
            return None
            
        try:
            rendered_files = trigger_visual_snapshot(tick_data, force=True)
            if rendered_files:
                self.total_snapshots += 1
                logger.info(f"📸 Forced snapshot: Generated {len(rendered_files)} visualizations")
                return rendered_files
        except Exception as e:
            logger.error(f"Force snapshot error: {e}")
            
        return None
    
    def create_basic_visualization(self, tick_data: Dict[str, Any], output_path: str) -> bool:
        """Create a basic tick visualization using the built-in renderer"""
        if not self.visual_enabled:
            return False
            
        try:
            return save_tick_visualization(tick_data, output_path)
        except Exception as e:
            logger.error(f"Basic visualization error: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get visual integration statistics"""
        return {
            'enabled': self.visual_enabled,
            'auto_snapshot': self.enable_auto_snapshot,
            'snapshot_interval': self.snapshot_interval,
            'total_snapshots': self.total_snapshots,
            'last_snapshot_tick': self.last_snapshot_tick
        }

# Utility functions for easy integration

def integrate_visuals_into_tick_loop(tick_function: callable, snapshot_interval: int = 10):
    """
    Decorator to add visual integration to an existing tick function
    
    Usage:
        @integrate_visuals_into_tick_loop(snapshot_interval=5)
        def my_tick_function(tick_data):
            # Your existing tick logic
            return tick_data
    """
    def decorator(func):
        visual_integration = VisualTickIntegration(snapshot_interval=snapshot_interval)
        
        def wrapper(*args, **kwargs):
            # Execute original tick function
            result = func(*args, **kwargs)
            
            # Try to extract tick data from result or args
            tick_data = None
            if isinstance(result, dict):
                tick_data = result
            elif args and isinstance(args[0], dict):
                tick_data = args[0]
            
            # Process visual integration if we have tick data
            if tick_data:
                visual_integration.process_tick(tick_data)
            
            return result
        
        return wrapper
    return decorator

def add_visual_hook(tick_data: Dict[str, Any], snapshot_every: int = 10) -> List[str]:
    """
    Simple function to add to existing tick loops
    
    Usage in existing code:
        # At the end of your tick processing:
        visual_files = add_visual_hook(tick_data, snapshot_every=5)
    """
    if VISUAL_TRIGGER_AVAILABLE:
        return trigger_visual_snapshot(tick_data, every_n_ticks=snapshot_every)
    return []

# Example integration for existing DAWN systems
def integrate_with_dawn_runner():
    """Example showing how to integrate with dawn_runner.py"""
    integration_code = '''
# Add this to your dawn_runner.py or similar tick loop:

from runtime.tick_visual_integration import VisualTickIntegration

class DAWNRunner:
    def __init__(self):
        # ... existing initialization ...
        self.visual_integration = VisualTickIntegration(snapshot_interval=10)
    
    async def _process_systems(self, tick_state: Dict[str, Any]):
        # ... existing system processing ...
        
        # Add visual integration at the end
        try:
            visual_files = self.visual_integration.process_tick(tick_state)
            if visual_files:
                logger.info(f"Visual snapshot: {len(visual_files)} files generated")
        except Exception as e:
            logger.warning(f"Visual integration error: {e}")
'''
    print(integration_code)

def integrate_with_consciousness_writer():
    """Example showing how to integrate with consciousness state writer"""
    integration_code = '''
# Add this to your consciousness/dawn_tick_state_writer.py:

from runtime.tick_visual_integration import add_visual_hook

class DAWNConsciousnessStateWriter:
    def write_tick(self, tick_state: TickState):
        # ... existing tick writing logic ...
        
        # Convert TickState to dict for visual processing
        tick_data = {
            'tick': tick_state.tick_number,
            'timestamp': tick_state.timestamp_ms / 1000,
            'scup': tick_state.cognitive_vector.semantic_alignment,
            'entropy': tick_state.cognitive_vector.entropy_gradient,
            'heat': tick_state.cognitive_vector.drift_magnitude,
            'mood': 'contemplative',  # Derive from mood_zone
            'consciousness_depth': tick_state.consciousness_depth
        }
        
        # Trigger visual snapshot every 10 ticks
        visual_files = add_visual_hook(tick_data, snapshot_every=10)
'''
    print(integration_code)

# CLI for testing integration
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='DAWN Tick Visual Integration')
    parser.add_argument('--test-integration', action='store_true', help='Test visual integration')
    parser.add_argument('--show-examples', action='store_true', help='Show integration examples')
    parser.add_argument('--simulate-ticks', type=int, default=5, help='Number of ticks to simulate')
    
    args = parser.parse_args()
    
    if args.show_examples:
        print("🔧 DAWN Visual Integration Examples")
        print("=" * 50)
        integrate_with_dawn_runner()
        print("\n" + "=" * 50)
        integrate_with_consciousness_writer()
        
    elif args.test_integration:
        print("🧪 Testing Visual Integration")
        print("-" * 30)
        
        # Create test integration
        integration = VisualTickIntegration(snapshot_interval=2)
        
        # Simulate some ticks
        for i in range(args.simulate_ticks):
            import math
            current_time = time.time()
            
            tick_data = {
                'tick': i + 1,
                'timestamp': current_time,
                'scup': 0.3 + 0.4 * abs(math.sin(current_time * 0.1)),
                'entropy': 0.2 + 0.3 * abs(math.sin(current_time * 0.15)),
                'heat': 0.1 + 0.4 * abs(math.sin(current_time * 0.08)),
                'mood': ['contemplative', 'curious', 'analytical', 'reflective'][i % 4],
                'consciousness_depth': 0.4 + 0.3 * abs(math.sin(current_time * 0.07)),
                'test_mode': True
            }
            
            print(f"Tick {i+1}: Processing...")
            rendered = integration.process_tick(tick_data)
            if rendered:
                print(f"  ✅ Generated {len(rendered)} visualizations")
            else:
                print(f"  ⏭️  No snapshot (waiting for interval)")
            
            time.sleep(0.5)  # Brief pause between ticks
        
        print(f"\n📊 Integration Stats:")
        stats = integration.get_stats()
        for key, value in stats.items():
            print(f"  {key}: {value}")
            
    else:
        parser.print_help() 