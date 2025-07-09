#!/usr/bin/env python3
"""
Example: Integrating DAWN Log Manager with GUI and Tick Engine
Shows how to add comprehensive logging to existing DAWN systems
"""

import sys
import os
import threading
import time
from typing import Dict, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from log_manager import get_log_manager, log_tick, log_sigil, log_bloom, log_schema_event, log_owl_observation


class DAWNWithLogging:
    """
    Example DAWN system enhanced with comprehensive logging
    """
    
    def __init__(self):
        # Initialize log manager
        self.logger = get_log_manager(
            logs_dir="./dawn_logs",
            max_memory_lines=1000,
            auto_flush_interval=50  # Flush every 50 ticks
        )
        
        # DAWN state
        self.tick_count = 0
        self.running = False
        self.current_state = {
            'heat': 0.0,
            'scup': 0.5,
            'entropy': 0.3,
            'zone': 'contemplative',
            'pulse': 'stable'
        }
        
        # Active components
        self.active_sigils = []
        self.active_blooms = []
        
        # Log system initialization
        log_schema_event("system_init", "DAWN with logging initialized", "success")
    
    def update_state(self, **kwargs):
        """Update DAWN's cognitive state"""
        self.current_state.update(kwargs)
        
        # Log significant state changes
        if 'zone' in kwargs and kwargs['zone'] != self.current_state.get('zone'):
            log_schema_event("zone_transition", 
                           f"Zone changed to {kwargs['zone']}", 
                           "info")
        
        if 'scup' in kwargs and abs(kwargs['scup'] - self.current_state.get('scup', 0.5)) > 0.2:
            severity = "critical" if kwargs['scup'] < 0.3 else "warning" if kwargs['scup'] < 0.5 else "info"
            log_schema_event("scup_change", 
                           f"SCUP changed significantly to {kwargs['scup']:.3f}", 
                           severity)
    
    def tick(self):
        """Execute one cognitive tick with full logging"""
        self.tick_count += 1
        
        # Simulate some cognitive activity
        self._simulate_cognitive_activity()
        
        # Generate owl observations based on state
        owl_comment = self._generate_owl_observation()
        
        # Log the tick
        log_tick(
            tick_id=self.tick_count,
            pulse=self.current_state['pulse'],
            scup=self.current_state['scup'],
            entropy=self.current_state['entropy'],
            zone=self.current_state['zone'],
            owl_comment=owl_comment
        )
        
        # Process any active sigils
        self._process_sigils()
        
        # Process any active blooms
        self._process_blooms()
    
    def _simulate_cognitive_activity(self):
        """Simulate realistic cognitive state changes"""
        import random
        
        # Entropy tends to increase over time, SCUP responds
        entropy_change = random.uniform(-0.05, 0.1)
        self.current_state['entropy'] = max(0.0, min(1.0, 
            self.current_state['entropy'] + entropy_change))
        
        # SCUP inversely related to entropy with some noise
        base_scup = 1.0 - self.current_state['entropy']
        scup_noise = random.uniform(-0.2, 0.2)
        self.current_state['scup'] = max(0.0, min(1.0, base_scup + scup_noise))
        
        # Heat fluctuates
        heat_change = random.uniform(-5, 10)
        self.current_state['heat'] = max(0.0, min(100.0, 
            self.current_state['heat'] + heat_change))
        
        # Zone based on SCUP and entropy
        if self.current_state['scup'] > 0.8:
            self.current_state['zone'] = 'contemplative'
        elif self.current_state['scup'] > 0.6:
            self.current_state['zone'] = 'active'
        elif self.current_state['scup'] > 0.4:
            self.current_state['zone'] = 'intense'
        else:
            self.current_state['zone'] = 'critical'
        
        # Pulse description
        if self.current_state['entropy'] > 0.8:
            self.current_state['pulse'] = 'chaotic'
        elif self.current_state['entropy'] > 0.6:
            self.current_state['pulse'] = 'turbulent'
        elif self.current_state['entropy'] > 0.4:
            self.current_state['pulse'] = 'active'
        else:
            self.current_state['pulse'] = 'stable'
    
    def _generate_owl_observation(self) -> str:
        """Generate contextual owl observations"""
        observations = []
        
        if self.current_state['scup'] < 0.3:
            observations.append("Critical coherence breakdown detected")
        elif self.current_state['scup'] > 0.9:
            observations.append("Exceptional cognitive coherence achieved")
        
        if self.current_state['entropy'] > 0.8:
            observations.append("High entropy creating instability")
        elif self.current_state['entropy'] < 0.2:
            observations.append("Low entropy indicates stable processing")
        
        if self.current_state['heat'] > 80:
            observations.append("Thermal stress approaching limits")
        elif self.current_state['heat'] < 20:
            observations.append("Cool operation, optimal efficiency")
        
        # Pattern observations
        if self.tick_count % 10 == 0:
            observations.append(f"Cycle {self.tick_count//10} completed")
        
        if len(self.active_blooms) > 3:
            observations.append("Multiple concurrent blooms detected")
        
        return "; ".join(observations) if observations else ""
    
    def _process_sigils(self):
        """Process and log sigil activity"""
        import random
        
        # Randomly spawn new sigils
        if random.random() < 0.3:  # 30% chance per tick
            sigil_types = [
                ("/\\", "Prime", 40, 2),
                ("◇", "Bloom", 60, 3),
                ("/|-/", "Recursive", 75, 4),
                ("⟁", "Contradiction", 85, 5),
                ("⌂", "Memory", 35, 2),
                ("~", "Echo", 25, 1)
            ]
            
            sigil_id, house, base_temp, base_conv = random.choice(sigil_types)
            temp = base_temp + random.randint(-20, 20)
            conv = base_conv + random.randint(-1, 2)
            
            # Temperature influenced by current heat
            temp = int(temp + (self.current_state['heat'] * 0.3))
            temp = max(0, min(100, temp))
            
            log_sigil(sigil_id, house, temp, max(1, conv))
            
            # Track active sigil
            self.active_sigils.append({
                'id': sigil_id,
                'house': house,
                'temp': temp,
                'conv': conv,
                'spawn_tick': self.tick_count
            })
        
        # Age and remove old sigils
        self.active_sigils = [s for s in self.active_sigils 
                             if self.tick_count - s['spawn_tick'] < 20]
    
    def _process_blooms(self):
        """Process and log bloom activity"""
        import random
        
        # Randomly spawn new blooms
        if random.random() < 0.2:  # 20% chance per tick
            bloom_id = f"bloom_{self.tick_count:04d}_{random.randint(100, 999)}"
            depth = random.randint(1, 5)
            bloom_entropy = self.current_state['entropy'] + random.uniform(-0.2, 0.2)
            bloom_entropy = max(0.0, min(1.0, bloom_entropy))
            
            # Sometimes rebloom from existing bloom
            parent = None
            if self.active_blooms and random.random() < 0.4:
                parent = random.choice(self.active_blooms)['id']
                depth = min(6, random.choice(self.active_blooms)['depth'] + 1)
            
            log_bloom(bloom_id, depth, bloom_entropy, parent)
            
            # Track active bloom
            self.active_blooms.append({
                'id': bloom_id,
                'depth': depth,
                'entropy': bloom_entropy,
                'parent': parent,
                'spawn_tick': self.tick_count
            })
        
        # Age and remove old blooms
        self.active_blooms = [b for b in self.active_blooms 
                             if self.tick_count - b['spawn_tick'] < 30]
    
    def run_simulation(self, ticks: int = 100):
        """Run a simulation with logging"""
        self.running = True
        log_schema_event("simulation_start", f"Starting {ticks}-tick simulation", "info")
        
        try:
            for _ in range(ticks):
                if not self.running:
                    break
                
                self.tick()
                time.sleep(0.1)  # Brief pause to make output readable
                
                # Occasional manual observations
                if self.tick_count % 25 == 0:
                    log_owl_observation(
                        f"Quarter-cycle checkpoint: system running for {self.tick_count} ticks",
                        0.95
                    )
        
        except KeyboardInterrupt:
            log_schema_event("simulation_interrupt", "Simulation interrupted by user", "warning")
        
        finally:
            self.running = False
            log_schema_event("simulation_end", f"Simulation completed after {self.tick_count} ticks", "success")
            
            # Final statistics
            stats = self.logger.get_log_stats()
            log_owl_observation(
                f"Final stats: {stats['total_logs']} total logs, {len(self.active_sigils)} active sigils, {len(self.active_blooms)} active blooms",
                1.0
            )
            
            # Shutdown gracefully
            self.logger.shutdown()


def gui_integration_example():
    """
    Example of how to integrate logging with the DAWN GUI
    """
    print("\n" + "="*60)
    print("🖥️  GUI Integration Example")
    print("="*60)
    
    # This would go in your gui/dawn_gui_tk.py file
    example_code = '''
# In your DAWNGui class __init__ method:
from log_manager import get_log_manager, log_tick, log_schema_event

class DAWNGui:
    def __init__(self, root, external_queue=None):
        # ... existing initialization ...
        
        # Add log manager
        self.logger = get_log_manager(logs_dir="./gui_logs")
        log_schema_event("gui_init", "DAWN GUI initialized with logging", "success")
    
    def update_with_codex(self, dawn_data):
        """Enhanced update method with logging"""
        # ... existing codex integration ...
        
        # Log significant events
        heat = dawn_data.get('heat', 0.0)
        zone = dawn_data.get('zone', 'unknown')
        
        if hasattr(self, '_last_zone') and self._last_zone != zone:
            log_schema_event("zone_change", f"GUI zone changed: {self._last_zone} → {zone}", "info")
        self._last_zone = zone
        
        # Log critical states
        if heat > 90:
            log_schema_event("heat_alert", f"GUI showing critical heat: {heat}", "critical")
    
    def refresh_widgets(self):
        """Enhanced widget refresh with logging"""
        # ... existing widget updates ...
        
        # Log widget update events
        current_data = self.current_data
        log_tick(
            tick_id=current_data.get('tick_count', 0),
            pulse=current_data.get('pulse', ''),
            scup=current_data.get('scup', 0.5),
            entropy=current_data.get('entropy', 0.5),
            zone=current_data.get('zone', 'unknown'),
            owl_comment="GUI refresh completed"
        )
'''
    
    print("Example integration code:")
    print(example_code)


def main():
    """Main demonstration"""
    print("🌅 DAWN Log Manager Integration Example")
    print("="*60)
    
    # Create DAWN system with logging
    dawn = DAWNWithLogging()
    
    print("\n🚀 Starting DAWN simulation with comprehensive logging...")
    print("Watch the terminal for beautiful real-time log output!")
    print("Logs are also being saved to ./dawn_logs/ directory")
    print("\nPress Ctrl+C to stop the simulation early\n")
    
    # Run simulation
    dawn.run_simulation(ticks=50)
    
    # Show GUI integration example
    gui_integration_example()
    
    print("\n✅ Integration example completed!")
    print("Check ./dawn_logs/ directory for saved log files")


if __name__ == "__main__":
    main() 