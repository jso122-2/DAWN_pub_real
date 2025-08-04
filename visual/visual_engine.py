# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Visual Engine - Central Visual Process Integration System

Discovers, integrates, and triggers all DAWN visualization modules.
Links visualizers with the live tick loop and enables automatic snapshotting.

Usage:
    python visual_engine.py --snapshot-now
    python visual_engine.py --auto-snapshot --interval 10
    python visual_engine.py --list-modules
    python visual_engine.py --run-continuous
"""

import os
import sys
import json
import time
import argparse
import importlib
import traceback
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class VisualModule:
    """Represents a discovered visualization module"""
    name: str
    path: str
    module_type: str  # 'realtime', 'analysis', 'script'
    has_savefig: bool = False
    has_tick_integration: bool = False
    module_obj: Any = None
    render_function: Optional[Callable] = None
    last_render_time: float = 0.0
    render_count: int = 0

class DAWNVisualEngine:
    """Central coordination system for all DAWN visual processes"""
    
    def __init__(self, tick_data_source: str = "/tmp/dawn_tick_data.json"):
        self.tick_data_source = tick_data_source
        self.visual_modules: Dict[str, VisualModule] = {}
        self.snapshot_dir = Path("runtime/snapshots")
        self.current_tick_data: Dict[str, Any] = {}
        self.is_running = False
        self.auto_snapshot_interval = 0  # 0 = disabled
        self.last_snapshot_time = 0.0
        
        # Ensure directories exist
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Discovery patterns for different types of modules
        self.module_discovery_patterns = {
            'realtime': [
                'visual/tick_pulse.py',
                'visual/dawn_mood_state.py', 
                'visual/SCUP_pressure_grid.py',
                'visual/consciousness_constellation.py',
                'visual/entropy_flow.py',
                'visual/recursive_depth_explorer.py',
                'visual/heat_monitor.py',
                'visual/scup_zone_animator.py',
                'visual/sigil_command_stream.py'
            ],
            'analysis': [
                'bloom/bloom_visualization_system.py',
                'network/router/cluster_graph.py',
                'experiments/dawn_unified_visualizer.py',
                'experiments/dawn_unified_visualizer_2.py',
                'backend/visual/bloom_genealogy_network.py',
                'backend/visual/semantic_flow_graph.py',
                'backend/visual/psl_integration.py'
            ],
            'scripts': [
                'visual/scripts/attention_map.py',
                'visual/scripts/loss_landscape.py',
                'visual/scripts/anomaly_timeline.py',
                'visual/scripts/activation_histogram.py',
                'visual/scripts/correlation_matrix.py',
                'visual/scripts/state_transition_graph.py',
                'visual/scripts/latent_space_trajectory.py',
                'visual/scripts/temporal_activity_raster.py'
            ],
            'memory': [
                'memories/personal/joyti_bloom.py',
                'memories/personal/max_birthday.py',
                'memories/personal/shanaz.py'
            ]
        }
        
        self._discover_modules()
    
    def _discover_modules(self):
        """Discover all available visualization modules"""
        logger.info("🔍 Discovering DAWN visualization modules...")
        
        for module_type, patterns in self.module_discovery_patterns.items():
            for pattern in patterns:
                module_path = Path(pattern)
                if module_path.exists():
                    module_name = module_path.stem
                    
                    # Check for matplotlib/savefig usage
                    has_savefig = self._check_savefig_capability(module_path)
                    has_tick_integration = self._check_tick_integration(module_path)
                    
                    visual_module = VisualModule(
                        name=module_name,
                        path=str(module_path),
                        module_type=module_type,
                        has_savefig=has_savefig,
                        has_tick_integration=has_tick_integration
                    )
                    
                    self.visual_modules[module_name] = visual_module
                    logger.info(f"✅ Found {module_type} module: {module_name} (savefig: {has_savefig}, tick: {has_tick_integration})")
        
        logger.info(f"🎯 Discovered {len(self.visual_modules)} visualization modules")
    
    def _check_savefig_capability(self, module_path: Path) -> bool:
        """Check if module has matplotlib savefig capability"""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return 'savefig' in content or 'plt.savefig' in content or 'fig.savefig' in content
        except Exception:
            return False
    
    def _check_tick_integration(self, module_path: Path) -> bool:
        """Check if module can integrate with tick data"""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tick_indicators = [
                    'tick_data', 'dawn_tick_data.json', 'parse_tick_data',
                    'process_tick', 'update_tick', 'tick_integration'
                ]
                return any(indicator in content for indicator in tick_indicators)
        except Exception:
            return False
    
    def load_tick_data(self) -> Dict[str, Any]:
        """Load current tick data from DAWN tick system"""
        try:
            # Try multiple sources for tick data
            sources = [
                self.tick_data_source,
                "state/tick_state.json",
                "runtime/dawn_consciousness.mmap",  # Binary data would need special handling
                "tick_state.json"
            ]
            
            for source in sources:
                if os.path.exists(source) and source.endswith('.json'):
                    with open(source, 'r') as f:
                        data = json.load(f)
                        # Standardize tick data format
                        standardized = self._standardize_tick_data(data)
                        self.current_tick_data = standardized
                        return standardized
            
            # Fallback: generate simulated tick data
            return self._generate_simulated_tick_data()
            
        except Exception as e:
            logger.warning(f"Failed to load tick data: {e}")
            return self._generate_simulated_tick_data()
    
    def _standardize_tick_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Standardize tick data format for consistent module consumption"""
        return {
            'tick': raw_data.get('tick_count', raw_data.get('tick', 0)),
            'timestamp': time.time(),
            'uptime': raw_data.get('uptime', 0.0),
            'scup': raw_data.get('scup', raw_data.get('performance_metrics', {}).get('scup', 0.5)),
            'entropy': raw_data.get('entropy', 0.3),
            'heat': raw_data.get('heat', raw_data.get('thermal_state', {}).get('heat', 0.25)),
            'mood': raw_data.get('mood', 'contemplative'),
            'neural_activity': raw_data.get('neural_activity', 0.4),
            'consciousness_depth': raw_data.get('consciousness_depth', 0.6),
            'pulse_intensity': raw_data.get('pulse_intensity', 0.5),
            'tick_rate': raw_data.get('performance_metrics', {}).get('ticks_per_second', 1.0),
            'memory_usage': raw_data.get('performance_metrics', {}).get('memory_usage', 0.0),
            'cpu_usage': raw_data.get('performance_metrics', {}).get('cpu_usage', 0.0),
            'subsystems': raw_data.get('subsystems', []),
            'raw_data': raw_data
        }
    
    def _generate_simulated_tick_data(self) -> Dict[str, Any]:
        """Generate simulated tick data for testing"""
        current_time = time.time()
        tick_num = int(current_time) % 10000
        
        return {
            'tick': tick_num,
            'timestamp': current_time,
            'uptime': current_time % 3600,
            'scup': 0.3 + 0.4 * abs(sin(current_time * 0.1)),
            'entropy': 0.2 + 0.3 * abs(sin(current_time * 0.15)),
            'heat': 0.1 + 0.4 * abs(sin(current_time * 0.08)),
            'mood': ['contemplative', 'curious', 'analytical', 'reflective'][tick_num % 4],
            'neural_activity': 0.3 + 0.4 * abs(sin(current_time * 0.12)),
            'consciousness_depth': 0.4 + 0.3 * abs(sin(current_time * 0.07)),
            'pulse_intensity': 0.2 + 0.6 * abs(sin(current_time * 0.2)),
            'tick_rate': 1.0 + 0.5 * abs(sin(current_time * 0.05)),
            'memory_usage': 45.0 + 20.0 * abs(sin(current_time * 0.03)),
            'cpu_usage': 15.0 + 25.0 * abs(sin(current_time * 0.06)),
            'subsystems': ['visual_engine', 'tick_emitter', 'consciousness_core'],
            'simulated': True
        }
    
    def render_and_save(self, tick_data: Dict[str, Any], module_names: Optional[List[str]] = None) -> Dict[str, str]:
        """Render visualizations and save snapshots for specified modules"""
        if module_names is None:
            module_names = list(self.visual_modules.keys())
        
        rendered_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        tick_num = tick_data.get('tick', 0)
        
        logger.info(f"🎨 Rendering tick {tick_num} visualizations...")
        
        for module_name in module_names:
            if module_name not in self.visual_modules:
                logger.warning(f"Module {module_name} not found")
                continue
                
            module = self.visual_modules[module_name]
            
            try:
                output_path = self.snapshot_dir / f"{module_name}_tick_{tick_num}_{timestamp}.png"
                
                if module.has_savefig:
                    success = self._render_module_direct(module, tick_data, output_path)
                else:
                    success = self._render_module_wrapper(module, tick_data, output_path)
                
                if success:
                    rendered_files[module_name] = str(output_path)
                    module.render_count += 1
                    module.last_render_time = time.time()
                    logger.info(f"✅ Rendered {module_name} -> {output_path}")
                else:
                    logger.warning(f"⚠️  Failed to render {module_name}")
                    
            except Exception as e:
                logger.error(f"❌ Error rendering {module_name}: {e}")
                
        return rendered_files
    
    def _render_module_direct(self, module: VisualModule, tick_data: Dict[str, Any], output_path: Path) -> bool:
        """Render module that has direct savefig capability"""
        try:
            # Import and execute the module with tick data
            spec = importlib.util.spec_from_file_location(module.name, module.path)
            mod = importlib.util.module_from_spec(spec)
            
            # Inject tick data into module's global namespace
            mod.__dict__['CURRENT_TICK_DATA'] = tick_data
            mod.__dict__['OUTPUT_PATH'] = str(output_path)
            
            # Execute the module
            spec.loader.exec_module(mod)
            
            # Check if file was created
            return output_path.exists()
            
        except Exception as e:
            logger.error(f"Direct render failed for {module.name}: {e}")
            return False
    
    def _render_module_wrapper(self, module: VisualModule, tick_data: Dict[str, Any], output_path: Path) -> bool:
        """Render module using matplotlib wrapper for modules without direct savefig"""
        try:
            import matplotlib.pyplot as plt
            
            # Clear any existing plots
            plt.clf()
            
            # Import and run the module
            spec = importlib.util.spec_from_file_location(module.name, module.path)
            mod = importlib.util.module_from_spec(spec)
            mod.__dict__['CURRENT_TICK_DATA'] = tick_data
            spec.loader.exec_module(mod)
            
            # Save current matplotlib figure
            if plt.get_fignums():  # Check if any figures exist
                plt.savefig(output_path, dpi=150, bbox_inches='tight', 
                           facecolor='#0a0a0a', edgecolor='none')
                plt.close('all')
                return True
            else:
                logger.warning(f"No matplotlib figures found for {module.name}")
                return False
                
        except Exception as e:
            logger.error(f"Wrapper render failed for {module.name}: {e}")
            return False
    
    def snapshot_now(self, module_filter: Optional[str] = None) -> Dict[str, str]:
        """Take immediate snapshot of all or filtered visual modules"""
        tick_data = self.load_tick_data()
        
        if module_filter:
            modules_to_render = [name for name in self.visual_modules.keys() 
                               if module_filter.lower() in name.lower()]
        else:
            modules_to_render = None
            
        rendered_files = self.render_and_save(tick_data, modules_to_render)
        
        # Create snapshot summary
        summary_path = self.snapshot_dir / f"snapshot_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        summary = {
            'timestamp': datetime.now().isoformat(),
            'tick_data': tick_data,
            'rendered_files': rendered_files,
            'module_count': len(rendered_files),
            'total_modules_available': len(self.visual_modules)
        }
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
        logger.info(f"📸 Snapshot complete: {len(rendered_files)} files rendered")
        logger.info(f"📋 Summary saved: {summary_path}")
        
        return rendered_files
    
    def run_continuous(self, snapshot_interval: int = 10):
        """Run continuous visual processing with periodic snapshots"""
        self.is_running = True
        self.auto_snapshot_interval = snapshot_interval
        
        logger.info(f"🚀 Starting continuous visual processing (snapshot every {snapshot_interval} ticks)")
        
        tick_counter = 0
        while self.is_running:
            try:
                # Load current tick data
                tick_data = self.load_tick_data()
                current_tick = tick_data.get('tick', 0)
                
                # Check if we should take a snapshot
                if (tick_counter % snapshot_interval == 0) or (current_tick % snapshot_interval == 0):
                    self.snapshot_now()
                    self.last_snapshot_time = time.time()
                
                tick_counter += 1
                time.sleep(1.0)  # 1 second between checks
                
            except KeyboardInterrupt:
                logger.info("⏹️  Stopping continuous processing...")
                self.is_running = False
                break
            except Exception as e:
                logger.error(f"Error in continuous processing: {e}")
                time.sleep(5.0)  # Wait before retrying
    
    def list_modules(self):
        """List all discovered visualization modules"""
        print("\n🎨 DAWN Visualization Modules")
        print("=" * 60)
        
        for module_type in ['realtime', 'analysis', 'scripts', 'memory']:
            modules_of_type = [m for m in self.visual_modules.values() if m.module_type == module_type]
            if modules_of_type:
                print(f"\n📊 {module_type.upper()} MODULES ({len(modules_of_type)})")
                print("-" * 40)
                for module in modules_of_type:
                    status_icons = []
                    if module.has_savefig:
                        status_icons.append("💾")
                    if module.has_tick_integration:
                        status_icons.append("⏱️")
                    
                    print(f"  {''.join(status_icons)} {module.name:30} | {module.path}")
                    if module.render_count > 0:
                        print(f"    {'':33} | Rendered {module.render_count} times")
        
        print(f"\n📈 SUMMARY")
        print("-" * 40)
        print(f"Total modules: {len(self.visual_modules)}")
        print(f"With savefig:  {sum(1 for m in self.visual_modules.values() if m.has_savefig)}")
        print(f"Tick-enabled:  {sum(1 for m in self.visual_modules.values() if m.has_tick_integration)}")
        print("\nIcons: 💾 = savefig capable, ⏱️ = tick integration")

def sin(x):
    """Simple sine function for simulation"""
    import math
    return math.sin(x)

def main():
    parser = argparse.ArgumentParser(description='DAWN Visual Engine - Central Visual Process Integration')
    parser.add_argument('--snapshot-now', action='store_true', help='Take immediate snapshot')
    parser.add_argument('--auto-snapshot', action='store_true', help='Enable automatic snapshotting')
    parser.add_argument('--interval', type=int, default=10, help='Snapshot interval in ticks')
    parser.add_argument('--list-modules', action='store_true', help='List all discovered modules')
    parser.add_argument('--run-continuous', action='store_true', help='Run continuous processing')
    parser.add_argument('--filter', type=str, help='Filter modules by name pattern')
    parser.add_argument('--tick-source', type=str, default='/tmp/dawn_tick_data.json', 
                       help='Tick data source file')
    
    args = parser.parse_args()
    
    # Initialize visual engine
    engine = DAWNVisualEngine(tick_data_source=args.tick_source)
    
    if args.list_modules:
        engine.list_modules()
    elif args.snapshot_now:
        rendered = engine.snapshot_now(module_filter=args.filter)
        print(f"\n✅ Snapshot complete: {len(rendered)} visualizations rendered")
        for module, path in rendered.items():
            print(f"  📁 {module}: {path}")
    elif args.run_continuous or args.auto_snapshot:
        engine.run_continuous(snapshot_interval=args.interval)
    else:
        # Default: show help and list modules
        parser.print_help()
        print("\n")
        engine.list_modules()

if __name__ == "__main__":
    main() 