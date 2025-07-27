#!/usr/bin/env python3
"""
DAWN Visual Trigger - Lightweight Tick Loop Integration

Simple interface for triggering visual snapshots from within DAWN's tick loop.
Designed to be imported and called from existing DAWN systems.

Usage in tick loop:
    from visual_trigger import trigger_visual_snapshot
    trigger_visual_snapshot(tick_data, every_n_ticks=5)
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Configure logging
logger = logging.getLogger(__name__)

class VisualTrigger:
    """Lightweight visual trigger for DAWN tick loop integration"""
    
    def __init__(self, snapshot_dir: str = "runtime/snapshots"):
        self.snapshot_dir = Path(snapshot_dir)
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.last_snapshot_tick = 0
        self.render_queue = []
        
        # Quick discovery of visualization scripts
        self.script_modules = self._discover_script_modules()
        
    def _discover_script_modules(self) -> List[str]:
        """Quick discovery of renderable script modules"""
        scripts = []
        
        # Visual scripts directory
        scripts_dir = Path("visual/scripts")
        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                scripts.append(str(script))
        
        # Key standalone visualizers
        standalone = [
            "visual/tick_pulse.py",
            "visual/dawn_mood_state.py",
            "experiments/dawn_unified_visualizer.py"
        ]
        
        for script in standalone:
            if Path(script).exists():
                scripts.append(script)
                
        logger.info(f"✅ Visual trigger found {len(scripts)} renderable modules")
        return scripts
    
    def trigger_snapshot(self, tick_data: Dict[str, Any], force: bool = False) -> List[str]:
        """Trigger visual snapshot with current tick data"""
        rendered_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tick_num = tick_data.get('tick', 0)
        
        # Update last snapshot tick
        self.last_snapshot_tick = tick_num
        
        # Write tick data to temporary file for script consumption
        temp_tick_file = Path("/tmp/dawn_tick_data.json")
        with open(temp_tick_file, 'w') as f:
            json.dump(tick_data, f)
        
        # Render key visualization scripts
        priority_scripts = [
            "visual/scripts/attention_map.py",
            "visual/scripts/correlation_matrix.py", 
            "visual/scripts/state_transition_graph.py"
        ]
        
        for script_path in priority_scripts:
            if Path(script_path).exists():
                try:
                    output_file = self._render_script(script_path, tick_data, timestamp)
                    if output_file:
                        rendered_files.append(output_file)
                except Exception as e:
                    logger.warning(f"Failed to render {script_path}: {e}")
        
        # Create snapshot manifest
        manifest = {
            'tick': tick_num,
            'timestamp': timestamp,
            'rendered_files': rendered_files,
            'tick_data_snapshot': tick_data
        }
        
        manifest_path = self.snapshot_dir / f"snapshot_manifest_{timestamp}.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"📸 Visual snapshot tick {tick_num}: {len(rendered_files)} files")
        return rendered_files
    
    def _render_script(self, script_path: str, tick_data: Dict[str, Any], timestamp: str) -> Optional[str]:
        """Render a single visualization script"""
        try:
            script_name = Path(script_path).stem
            output_path = self.snapshot_dir / f"{script_name}_{timestamp}.png"
            
            # Create a simple execution environment
            import subprocess
            import tempfile
            
            # Create a wrapper script that sets up the environment
            wrapper_content = f'''
import sys
import os
sys.path.append(os.getcwd())

# Import the target script
import importlib.util
spec = importlib.util.spec_from_file_location("target_module", "{script_path}")
module = importlib.util.module_from_spec(spec)

# Set up environment variables
os.environ['OUTPUT_PATH'] = "{output_path}"
os.environ['TICK_DATA_PATH'] = "/tmp/dawn_tick_data.json"

# Execute the module
try:
    spec.loader.exec_module(module)
    print("SUCCESS: Module executed")
except Exception as e:
    print(f"ERROR: {{e}}")
'''
            
            # Execute the wrapper
            result = subprocess.run([sys.executable, "-c", wrapper_content], 
                                  capture_output=True, text=True, timeout=30)
            
            if output_path.exists():
                return str(output_path)
            else:
                logger.warning(f"Script {script_name} did not generate output file")
                return None
                
        except Exception as e:
            logger.error(f"Failed to render script {script_path}: {e}")
            return None
    
    def should_snapshot(self, current_tick: int, every_n_ticks: int = 10) -> bool:
        """Check if we should take a snapshot based on tick interval"""
        return (current_tick - self.last_snapshot_tick) >= every_n_ticks

# Global instance for easy import
_visual_trigger = None

def get_visual_trigger() -> VisualTrigger:
    """Get or create global visual trigger instance"""
    global _visual_trigger
    if _visual_trigger is None:
        _visual_trigger = VisualTrigger()
    return _visual_trigger

def trigger_visual_snapshot(tick_data: Dict[str, Any], every_n_ticks: int = 10, force: bool = False) -> List[str]:
    """
    Main entry point for triggering visual snapshots from DAWN tick loop
    
    Args:
        tick_data: Current tick state data
        every_n_ticks: Snapshot frequency (default: every 10 ticks)
        force: Force snapshot regardless of tick interval
    
    Returns:
        List of rendered file paths
    """
    trigger = get_visual_trigger()
    current_tick = tick_data.get('tick', 0)
    
    if force or trigger.should_snapshot(current_tick, every_n_ticks):
        return trigger.trigger_snapshot(tick_data, force=force)
    else:
        return []

def save_tick_visualization(tick_data: Dict[str, Any], output_path: str) -> bool:
    """
    Save a single tick visualization using matplotlib
    
    Simple function for creating basic tick visualizations
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Create a simple dashboard-style visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('#0a0a0a')
        
        # Extract metrics
        tick = tick_data.get('tick', 0)
        scup = tick_data.get('scup', 0.5)
        entropy = tick_data.get('entropy', 0.3)
        heat = tick_data.get('heat', 0.25)
        mood = tick_data.get('mood', 'unknown')
        
        # SCUP meter
        ax1.barh([0], [scup], color='#4a9eff', alpha=0.8)
        ax1.set_xlim(0, 1)
        ax1.set_title(f'SCUP: {scup:.3f}', color='#4a9eff')
        ax1.set_facecolor('#0a0a0a')
        
        # Entropy visualization
        ax2.barh([0], [entropy], color='#ff6b4a', alpha=0.8)
        ax2.set_xlim(0, 1)
        ax2.set_title(f'Entropy: {entropy:.3f}', color='#ff6b4a')
        ax2.set_facecolor('#0a0a0a')
        
        # Heat visualization  
        ax3.barh([0], [heat], color='#ffa94a', alpha=0.8)
        ax3.set_xlim(0, 1)
        ax3.set_title(f'Heat: {heat:.3f}', color='#ffa94a')
        ax3.set_facecolor('#0a0a0a')
        
        # Mood and tick info
        ax4.text(0.5, 0.7, f'Tick: {tick}', ha='center', va='center', 
                color='#e8f4f8', fontsize=16, transform=ax4.transAxes)
        ax4.text(0.5, 0.3, f'Mood: {mood}', ha='center', va='center',
                color='#8ba4c7', fontsize=14, transform=ax4.transAxes)
        ax4.set_facecolor('#0a0a0a')
        ax4.set_xticks([])
        ax4.set_yticks([])
        
        # Style all axes
        for ax in [ax1, ax2, ax3]:
            ax.set_yticks([])
            ax.tick_params(colors='#8ba4c7')
            for spine in ax.spines.values():
                spine.set_color('#2d5a87')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                   facecolor='#0a0a0a', edgecolor='none')
        plt.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to save tick visualization: {e}")
        return False

# Quick CLI interface
if __name__ == "__main__":
    import argparse
    import math
    
    parser = argparse.ArgumentParser(description='DAWN Visual Trigger')
    parser.add_argument('--snapshot-now', action='store_true', help='Take immediate snapshot')
    parser.add_argument('--simulate-tick', action='store_true', help='Generate simulated tick data')
    
    args = parser.parse_args()
    
    if args.snapshot_now:
        # Load or simulate tick data
        if args.simulate_tick:
            current_time = time.time()
            tick_data = {
                'tick': int(current_time) % 1000,
                'timestamp': current_time,
                'scup': 0.3 + 0.4 * abs(math.sin(current_time * 0.1)),
                'entropy': 0.2 + 0.3 * abs(math.sin(current_time * 0.15)),
                'heat': 0.1 + 0.4 * abs(math.sin(current_time * 0.08)),
                'mood': 'contemplative',
                'simulated': True
            }
        else:
            # Try to load from tick state
            try:
                with open('state/tick_state.json', 'r') as f:
                    tick_data = json.load(f)
            except:
                tick_data = {'tick': 0, 'timestamp': time.time()}
        
        rendered = trigger_visual_snapshot(tick_data, force=True)
        print(f"✅ Rendered {len(rendered)} visualizations:")
        for path in rendered:
            print(f"  📁 {path}")
    else:
        print("Use --snapshot-now to trigger immediate snapshot")
        print("Use --simulate-tick to generate test data") 