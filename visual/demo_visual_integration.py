# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#!/usr/bin/env python3
"""
DAWN Visual Integration Demo

Demonstrates the complete visual process integration system working with
real visualizations and tick loop integration.
"""

import os
import sys
import time
import json
import math
from datetime import datetime
from pathlib import Path

# Import our visual integration system
try:
    from visual.visual_trigger import trigger_visual_snapshot, save_tick_visualization
    from runtime.tick_visual_integration import VisualTickIntegration
    VISUAL_INTEGRATION_AVAILABLE = True
except ImportError as e:
    print(f"❌ Visual integration not available: {e}")
    VISUAL_INTEGRATION_AVAILABLE = False

def create_sample_visual_script():
    """Create a sample visualization script that works with our system"""
    
    sample_script = '''#!/usr/bin/env python3
"""
Sample Tick Visualization Script
Demonstrates how to create DAWN-compatible visualizations
"""

import os
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Check for tick data from environment or file
tick_data = {}
if 'TICK_DATA_PATH' in os.environ:
    try:
        with open(os.environ['TICK_DATA_PATH'], 'r') as f:
            tick_data = json.load(f)
    except:
        pass

if 'CURRENT_TICK_DATA' in globals():
    tick_data = CURRENT_TICK_DATA

# Default values if no tick data available
tick = tick_data.get('tick', 0)
scup = tick_data.get('scup', 0.5)
entropy = tick_data.get('entropy', 0.3)
heat = tick_data.get('heat', 0.25)
mood = tick_data.get('mood', 'contemplative')

# Create visualization
plt.style.use('dark_background')
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
fig.patch.set_facecolor('#0a0a0a')

# SCUP visualization
ax1.bar(['SCUP'], [scup], color='#4a9eff', alpha=0.8)
ax1.set_ylim(0, 1)
ax1.set_title(f'SCUP: {scup:.3f}', color='#4a9eff')
ax1.set_facecolor('#0a0a0a')

# Entropy flow
x = np.linspace(0, 10, 100)
y = entropy * np.sin(x + time.time() * 0.1)
ax2.plot(x, y, color='#ff6b4a', linewidth=2)
ax2.set_title(f'Entropy Flow: {entropy:.3f}', color='#ff6b4a')
ax2.set_facecolor('#0a0a0a')

# Heat visualization
theta = np.linspace(0, 2*np.pi, 100)
r = heat * (1 + 0.3 * np.sin(5 * theta))
ax3.polar(theta, r, color='#ffa94a', linewidth=3)
ax3.set_title(f'Heat Pattern: {heat:.3f}', color='#ffa94a')
ax3.set_facecolor('#0a0a0a')

# Tick and mood info
ax4.text(0.5, 0.7, f'Tick: {tick}', ha='center', va='center', 
         color='#e8f4f8', fontsize=16, transform=ax4.transAxes)
ax4.text(0.5, 0.3, f'Mood: {mood}', ha='center', va='center',
         color='#8ba4c7', fontsize=14, transform=ax4.transAxes)
ax4.set_facecolor('#0a0a0a')
ax4.set_xticks([])
ax4.set_yticks([])

plt.tight_layout()

# Save the visualization
output_path = os.environ.get('OUTPUT_PATH', f'runtime/snapshots/demo_visualization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight', 
           facecolor='#0a0a0a', edgecolor='none')
plt.close()

print(f"Demo visualization saved to: {output_path}")
'''
    
    # Write the sample script
    script_path = Path("runtime/demo_visual_script.py")
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(script_path, 'w') as f:
        f.write(sample_script)
    
    return str(script_path)

def simulate_dawn_tick_loop():
    """Simulate a DAWN tick loop with visual integration"""
    print("🎬 Starting DAWN Tick Loop Simulation with Visual Integration")
    print("=" * 60)
    
    if not VISUAL_INTEGRATION_AVAILABLE:
        print("❌ Visual integration not available - install visual_trigger.py")
        return
    
    # Create visual integration
    visual_integration = VisualTickIntegration(snapshot_interval=3)
    
    # Create sample visualization script
    demo_script = create_sample_visual_script()
    print(f"📄 Created demo script: {demo_script}")
    
    print(f"\n🔄 Running tick loop (visual snapshots every 3 ticks)...")
    
    for tick_num in range(1, 11):  # Simulate 10 ticks
        current_time = time.time()
        
        # Generate realistic tick data
        tick_data = {
            'tick': tick_num,
            'timestamp': current_time,
            'uptime': tick_num * 1.2,
            'scup': 0.3 + 0.4 * abs(math.sin(current_time * 0.1 + tick_num * 0.5)),
            'entropy': 0.2 + 0.3 * abs(math.sin(current_time * 0.15 + tick_num * 0.3)),
            'heat': 0.1 + 0.4 * abs(math.sin(current_time * 0.08 + tick_num * 0.7)),
            'mood': ['contemplative', 'curious', 'analytical', 'reflective'][tick_num % 4],
            'neural_activity': 0.3 + 0.4 * abs(math.sin(current_time * 0.12 + tick_num)),
            'consciousness_depth': 0.4 + 0.3 * abs(math.sin(current_time * 0.07 + tick_num * 0.4)),
            'pulse_intensity': 0.2 + 0.6 * abs(math.sin(current_time * 0.2 + tick_num * 0.6)),
            'demo_mode': True
        }
        
        print(f"\n⏰ Tick {tick_num:2d} | SCUP: {tick_data['scup']:.3f} | Entropy: {tick_data['entropy']:.3f} | Heat: {tick_data['heat']:.3f}")
        
        # Process tick with visual integration
        rendered_files = visual_integration.process_tick(tick_data)
        
        if rendered_files:
            print(f"   📸 Visual snapshot taken: {len(rendered_files)} files")
            for file_path in rendered_files:
                print(f"   📁 {file_path}")
        else:
            print(f"   ⏭️  No snapshot (next at tick {visual_integration.last_snapshot_tick + visual_integration.snapshot_interval})")
        
        # Simulate tick processing time
        time.sleep(0.3)
    
    # Show final stats
    print(f"\n📊 Simulation Complete")
    print("-" * 30)
    stats = visual_integration.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Demonstrate manual snapshot
    print(f"\n📸 Taking manual snapshot...")
    final_tick_data = {
        'tick': 999,
        'timestamp': time.time(),
        'scup': 0.7,
        'entropy': 0.4,
        'heat': 0.6,
        'mood': 'triumphant',
        'manual_snapshot': True
    }
    
    manual_files = visual_integration.force_snapshot(final_tick_data)
    if manual_files:
        print(f"   ✅ Manual snapshot: {len(manual_files)} files")
        for file_path in manual_files:
            print(f"   📁 {file_path}")

def demonstrate_basic_visualization():
    """Show the basic built-in visualization functionality"""
    print("\n🎨 Demonstrating Basic Tick Visualization")
    print("-" * 40)
    
    # Create sample tick data
    tick_data = {
        'tick': 42,
        'timestamp': time.time(),
        'scup': 0.65,
        'entropy': 0.35,
        'heat': 0.45,
        'mood': 'focused',
        'consciousness_depth': 0.72
    }
    
    # Create basic visualization
    output_path = f"runtime/snapshots/basic_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    
    if VISUAL_INTEGRATION_AVAILABLE:
        success = save_tick_visualization(tick_data, output_path)
        if success:
            print(f"✅ Basic visualization saved: {output_path}")
        else:
            print("❌ Failed to create basic visualization")
    else:
        print("❌ Visual integration not available")

def show_integration_examples():
    """Show code examples for integrating into DAWN systems"""
    print("\n🔧 Integration Examples")
    print("=" * 40)
    
    print("1. Simple Tick Hook:")
    print("""
from runtime.tick_visual_integration import add_visual_hook

# In your tick processing function:
def process_tick(tick_data):
    # ... your existing tick logic ...
    
    # Add visual hook at the end
    visual_files = add_visual_hook(tick_data, snapshot_every=5)
    if visual_files:
        logger.info(f"Generated {len(visual_files)} visualizations")
""")
    
    print("\n2. Full Integration Class:")
    print("""
from runtime.tick_visual_integration import VisualTickIntegration

class YourDAWNSystem:
    def __init__(self):
        self.visual_integration = VisualTickIntegration(snapshot_interval=10)
    
    def tick_loop(self):
        for tick_data in self.get_tick_stream():
            # Process your tick
            result = self.process_tick(tick_data)
            
            # Add visual processing
            self.visual_integration.process_tick(tick_data)
""")
    
    print("\n3. Decorator Approach:")
    print("""
from runtime.tick_visual_integration import integrate_visuals_into_tick_loop

@integrate_visuals_into_tick_loop(snapshot_interval=5)
def my_tick_function(tick_data):
    # Your existing tick logic here
    return processed_tick_data
""")

def main():
    print("🌅 DAWN Visual Process Integration Demo")
    print("=" * 50)
    
    # Check system availability
    if VISUAL_INTEGRATION_AVAILABLE:
        print("✅ Visual integration system available")
    else:
        print("❌ Visual integration system not available")
        return
    
    # Run demonstrations
    demonstrate_basic_visualization()
    simulate_dawn_tick_loop()
    show_integration_examples()
    
    print(f"\n🎯 Demo Complete!")
    print(f"Check runtime/snapshots/ for generated visualizations")

if __name__ == "__main__":
    main() 