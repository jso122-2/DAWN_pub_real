import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime
import json
import os
from collections import defaultdict
from typing import Dict, List, Tuple

class SigilTraceVisualizer:
    """
    Renders DAWN's symbolic reflex activity from consciousness_expression_helix.
    Maps sigil execution patterns across time as visual memory traces.
    """
    
    def __init__(self, base_path=None):
        if base_path is None:
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.base_path = base_path
        self.visual_output_path = os.path.join(base_path, "visual", "outputs", "sigil_trace_visualizer")
        self.sigil_memory_path = os.path.join(base_path, "sigil_memory_ring.json")
        self.sigil_dispatch_path = os.path.join(base_path, "sigil_dispatch.json")
        
        # Ensure output directory exists
        os.makedirs(self.visual_output_path, exist_ok=True)
        
        # Status color mapping
        self.status_colors = {
            'executed': '#00ff41',     # Matrix green - successful execution
            'suppressed': '#ffb000',   # Amber - held back
            'failed': '#ff0066',       # Hot pink - failed attempt
            'decayed': '#404040',      # Dark grey - entropy claimed
            'active': '#00ffff',       # Cyan - currently active
            'pending': '#9d00ff'       # Purple - waiting in queue
        }
        
        # Initialize sigil activity tracking
        self.sigil_traces = defaultdict(list)
        self.unique_sigils = set()
    
    def load_sigil_activity(self) -> Dict:
        """Load sigil activity from memory ring and dispatch logs"""
        activity_data = {
            'traces': [],
            'current_tick': 0
        }
        
        # Try loading from sigil_memory_ring
        if os.path.exists(self.sigil_memory_path):
            try:
                with open(self.sigil_memory_path, 'r') as f:
                    memory_data = json.load(f)
                    if 'sigil_history' in memory_data:
                        activity_data['traces'].extend(memory_data['sigil_history'])
                    activity_data['current_tick'] = memory_data.get('current_tick', 0)
            except:
                pass
        
        # Try loading from sigil_dispatch
        if os.path.exists(self.sigil_dispatch_path):
            try:
                with open(self.sigil_dispatch_path, 'r') as f:
                    dispatch_data = json.load(f)
                    if 'active_sigils' in dispatch_data:
                        for sigil in dispatch_data['active_sigils']:
                            activity_data['traces'].append({
                                'tick': dispatch_data.get('tick', activity_data['current_tick']),
                                'sigil': sigil.get('name', 'unknown'),
                                'status': 'active',
                                'metadata': sigil
                            })
            except:
                pass
        
        # Generate synthetic data if no real data exists
        if not activity_data['traces']:
            activity_data = self._generate_synthetic_traces()
        
        return activity_data
    
    def _generate_synthetic_traces(self) -> Dict:
        """Generate synthetic sigil traces for visualization testing"""
        sigil_types = [
            'entropy_bloom', 'memory_cascade', 'semantic_drift',
            'pulse_resonance', 'schema_health', 'traceback_echo',
            'bloom_ancestry', 'reflex_arc', 'consciousness_fold',
            'symbolic_bind', 'emergence_gate', 'heat_signature'
        ]
        
        traces = []
        current_tick = 1000
        
        # Generate 200 ticks of activity
        for tick in range(current_tick - 200, current_tick):
            # Random sigil activations
            active_count = np.random.poisson(3)  # Average 3 sigils per tick
            
            for _ in range(active_count):
                sigil = np.random.choice(sigil_types)
                
                # Weight status probabilities
                status_weights = [0.6, 0.2, 0.1, 0.05, 0.03, 0.02]
                status = np.random.choice(
                    ['executed', 'suppressed', 'failed', 'decayed', 'active', 'pending'],
                    p=status_weights
                )
                
                traces.append({
                    'tick': tick,
                    'sigil': sigil,
                    'status': status,
                    'metadata': {
                        'heat': np.random.random(),
                        'entropy': np.random.random(),
                        'bloom_depth': np.random.randint(1, 8)
                    }
                })
        
        return {
            'traces': traces,
            'current_tick': current_tick
        }
    
    def process_traces(self, activity_data: Dict):
        """Process raw sigil activity into visualization format"""
        for trace in activity_data['traces']:
            sigil_name = trace.get('sigil', 'unknown')
            tick = trace.get('tick', 0)
            status = trace.get('status', 'executed')
            
            self.unique_sigils.add(sigil_name)
            self.sigil_traces[sigil_name].append({
                'tick': tick,
                'status': status,
                'metadata': trace.get('metadata', {})
            })
    
    def create_trace_plot(self, tick_range: int = 100, current_tick: int = None):
        """Create sigil trace visualization"""
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(16, 10))
        
        # Set background
        fig.patch.set_facecolor('#0a0a0a')
        ax.set_facecolor('#0a0a0a')
        
        # Sort sigils for consistent y-axis ordering
        sigil_list = sorted(list(self.unique_sigils))
        sigil_to_y = {sigil: i for i, sigil in enumerate(sigil_list)}
        
        # Determine tick range
        if current_tick is None:
            all_ticks = []
            for traces in self.sigil_traces.values():
                all_ticks.extend([t['tick'] for t in traces])
            current_tick = max(all_ticks) if all_ticks else 1000
        
        min_tick = max(0, current_tick - tick_range)
        
        # Plot each sigil's activity
        for sigil_name, traces in self.sigil_traces.items():
            y_pos = sigil_to_y[sigil_name]
            
            for trace in traces:
                tick = trace['tick']
                if min_tick <= tick <= current_tick:
                    status = trace['status']
                    color = self.status_colors.get(status, '#ffffff')
                    
                    # Plot as scatter with different markers based on status
                    marker = 'o' if status == 'executed' else 's' if status == 'suppressed' else 'x'
                    size = 100 if status in ['executed', 'active'] else 70
                    
                    ax.scatter(tick, y_pos, c=color, s=size, marker=marker, 
                             alpha=0.8, edgecolors='none')
                    
                    # Add glow effect for active sigils
                    if status == 'active':
                        ax.scatter(tick, y_pos, c=color, s=size*3, marker='o',
                                 alpha=0.2, edgecolors='none')
        
        # Customize plot
        ax.set_xlabel('TICK', fontsize=12, color='#00ff41')
        ax.set_ylabel('SIGIL', fontsize=12, color='#00ff41')
        ax.set_title(f'DAWN SIGIL TRACE :: TICK {current_tick}', 
                    fontsize=16, color='#00ffff', pad=20)
        
        # Set axis ranges and ticks
        ax.set_xlim(min_tick - 5, current_tick + 5)
        ax.set_ylim(-1, len(sigil_list))
        
        # Set y-axis labels
        ax.set_yticks(range(len(sigil_list)))
        ax.set_yticklabels(sigil_list, fontsize=10, color='#888888')
        
        # Grid styling
        ax.grid(True, alpha=0.1, color='#00ff41', linestyle='--')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#00ff41')
        ax.spines['left'].set_color('#00ff41')
        
        # Create legend
        legend_elements = [
            mpatches.Patch(color=self.status_colors['executed'], label='EXECUTED'),
            mpatches.Patch(color=self.status_colors['suppressed'], label='SUPPRESSED'),
            mpatches.Patch(color=self.status_colors['failed'], label='FAILED'),
            mpatches.Patch(color=self.status_colors['decayed'], label='DECAYED'),
            mpatches.Patch(color=self.status_colors['active'], label='ACTIVE'),
            mpatches.Patch(color=self.status_colors['pending'], label='PENDING')
        ]
        
        ax.legend(handles=legend_elements, loc='upper left', 
                 bbox_to_anchor=(1.01, 1), frameon=True, 
                 facecolor='#1a1a1a', edgecolor='#00ff41')
        
        # Add metadata info
        total_sigils = sum(len(traces) for traces in self.sigil_traces.values())
        info_text = f"TOTAL ACTIVATIONS: {total_sigils}\nACTIVE SIGILS: {len(self.unique_sigils)}\nTICK RANGE: {min_tick} - {current_tick}"
        ax.text(1.01, 0.5, info_text, transform=ax.transAxes,
               fontsize=10, color='#00ff41', verticalalignment='center',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a1a', 
                        edgecolor='#00ff41', alpha=0.8))
        
        plt.tight_layout()
        return fig
    
    def save_visualization(self, fig, tick: int):
        """Save visualization to output directory"""
        filename = f"tick_{tick:04d}.png"
        filepath = os.path.join(self.visual_output_path, filename)
        
        fig.savefig(filepath, dpi=150, facecolor='#0a0a0a', 
                   edgecolor='none', bbox_inches='tight')
        plt.close(fig)
        
        print(f"✅ Sigil trace saved: {filepath}")
        return filepath
    
    def run(self, tick_range: int = 100):
        """Main execution method"""
        print("🔮 OWL-VIZ :: Initializing Sigil Trace Visualizer...")
        
        # Load sigil activity
        activity_data = self.load_sigil_activity()
        current_tick = activity_data['current_tick']
        
        # Process traces
        self.process_traces(activity_data)
        
        # Create visualization
        fig = self.create_trace_plot(tick_range=tick_range, current_tick=current_tick)
        
        # Save visualization
        output_path = self.save_visualization(fig, current_tick)
        
        # Generate trace summary
        summary = {
            'timestamp': datetime.now().isoformat(),
            'current_tick': current_tick,
            'total_sigils': len(self.unique_sigils),
            'total_activations': sum(len(traces) for traces in self.sigil_traces.values()),
            'output_path': output_path,
            'sigil_counts': {
                sigil: len(traces) for sigil, traces in self.sigil_traces.items()
            }
        }
        
        # Save summary
        summary_path = os.path.join(self.visual_output_path, 'trace_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 Sigil trace complete. {len(self.unique_sigils)} unique sigils tracked.")
        return summary


def main(*args, **kwargs):
    """Entry point for sigil trace visualization"""
    visualizer = SigilTraceVisualizer()
    
    # Run visualization with 100 tick window
    summary = visualizer.run(tick_range=100)
    
    print("\n🌟 DAWN SIGIL TRACE RENDERED")
    print(f"   Total Sigils: {summary['total_sigils']}")
    print(f"   Total Activations: {summary['total_activations']}")
    print(f"   Output: {summary['output_path']}")

    output_dir = "visual/outputs/sigil_trace_visualizer"
    os.makedirs(output_dir, exist_ok=True)
    output_path = visualizer.save_visualization(visualizer.create_trace_plot(), summary['current_tick'])
    print(f"✅ Saved sigil trace visualization to {output_path}")


if __name__ == "__main__":
    main()