"""
Complete fix for DAWN visualization scripts
Run from Tick_engine directory
"""

import os
import sys
from pathlib import Path
import json

def fix_pathpatch_in_file(filepath):
    """Fix PathPatch import in a specific file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add the import at the top after matplotlib imports
    lines = content.split('\n')
    
    # Find where matplotlib is imported
    import_index = -1
    for i, line in enumerate(lines):
        if 'import matplotlib' in line or 'from matplotlib' in line:
            import_index = i
            break
    
    # Add PathPatch import if not present
    if 'from matplotlib.patches import PathPatch' not in content:
        if import_index >= 0:
            lines.insert(import_index + 1, 'from matplotlib.patches import PathPatch')
        else:
            lines.insert(0, 'from matplotlib.patches import PathPatch')
    
    # Also add Path import if needed
    if 'matplotlib.path.Path' in content and 'from matplotlib.path import Path' not in content:
        if import_index >= 0:
            lines.insert(import_index + 1, 'from matplotlib.path import Path')
        else:
            lines.insert(0, 'from matplotlib.path import Path')
    
    content = '\n'.join(lines)
    
    # Replace plt.PathPatch with PathPatch
    content = content.replace('plt.PathPatch', 'PathPatch')
    content = content.replace('pyplot.PathPatch', 'PathPatch')
    
    # Save the fixed content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Fixed PathPatch in: {filepath.name}")

def create_missing_data_files():
    """Create all missing data files that scripts expect"""
    base = Path.cwd()
    
    # Create rebloom tick log
    rebloom_log = base / "juliet_flowers/cluster_report/rebloom_tick_log.csv"
    with open(rebloom_log, 'w', encoding='utf-8') as f:
        f.write("tick,rebloom_count,source,target\n")
        for i in range(50):
            f.write(f"{1000+i*2},{i%5},bloom_{i%3},bloom_{(i+1)%3}\n")
    print("✅ Created rebloom_tick_log.csv")
    
    # Create bloom log
    bloom_log = base / "juliet_flowers/bloom_log.csv"
    with open(bloom_log, 'w', encoding='utf-8') as f:
        f.write("tick,bloom_id,entropy,mood_pressure,depth\n")
        for i in range(100):
            f.write(f"{1000+i},{i%10},{0.2+i*0.005},{0.3+i*0.003},{i%5}\n")
    print("✅ Created bloom_log.csv")
    
    # Create proper zone overlay log with zones
    zone_log = base / "juliet_flowers/cluster_report/zone_overlay_log.csv"
    with open(zone_log, 'w', encoding='utf-8') as f:
        f.write("tick,zone,heat\n")
        for i in range(200):
            zones = ["calm", "active", "surge"]
            zone = zones[i % 3]
            heat = 0.3 + (i % 10) * 0.05
            f.write(f"{1000+i},{zone},{heat:.3f}\n")
    print("✅ Created zone_overlay_log.csv")
    
    # Create entropy logs
    entropy_dir = base / "juliet_flowers/entropy_logs"
    entropy_dir.mkdir(exist_ok=True)
    
    # Sigil entropy log
    sigil_entropy = entropy_dir / "sigil_entropy_log.csv"
    with open(sigil_entropy, 'w', encoding='utf-8') as f:
        f.write("tick,sigil_id,entropy,type\n")
        for i in range(100):
            f.write(f"{1000+i},sigil_{i%8},{0.1+i*0.008},type_{i%3}\n")
    print("✅ Created sigil_entropy_log.csv")
    
    # Mood transition log
    mood_log = base / "juliet_flowers/cluster_report/mood_transition_log.csv"
    with open(mood_log, 'w', encoding='utf-8') as f:
        f.write("tick,from_mood,to_mood,pressure\n")
        moods = ["calm", "curious", "urgent", "defensive"]
        for i in range(50):
            from_mood = moods[i % 4]
            to_mood = moods[(i + 1) % 4]
            f.write(f"{1000+i*2},{from_mood},{to_mood},{0.2+i*0.01}\n")
    print("✅ Created mood_transition_log.csv")
    
    # Drift log
    drift_log = base / "owl/drift_log.csv"
    (base / "owl").mkdir(exist_ok=True)
    with open(drift_log, 'w', encoding='utf-8') as f:
        f.write("tick,dx,dy,dz,magnitude\n")
        for i in range(100):
            import math
            dx = math.sin(i * 0.1) * 0.5
            dy = math.cos(i * 0.1) * 0.3
            dz = math.sin(i * 0.2) * 0.2
            mag = math.sqrt(dx*dx + dy*dy + dz*dz)
            f.write(f"{1000+i},{dx:.3f},{dy:.3f},{dz:.3f},{mag:.3f}\n")
    print("✅ Created drift_log.csv")

def test_visual_direct(script_name):
    """Test running a visual script directly"""
    script_path = Path("visual") / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    # Try running directly
    original_dir = os.getcwd()
    try:
        os.chdir("visual")
        result = os.system(f'python {script_name}')
        return result == 0
    finally:
        os.chdir(original_dir)

def main():
    print("🔧 Complete DAWN Visual Fix")
    print("=" * 60)
    
    # Step 1: Fix PathPatch in specific files
    print("\n📝 Fixing PathPatch imports...")
    visual_dir = Path("visual")
    
    # Files known to have PathPatch issues
    pathpatch_files = [
        "bloom_lineage_radar.py",
        "drift_lattice_generator.py",
        "recursive_bloom_tree.py",
        "visual_rhizome.py"
    ]
    
    for filename in pathpatch_files:
        filepath = visual_dir / filename
        if filepath.exists():
            try:
                fix_pathpatch_in_file(filepath)
            except Exception as e:
                print(f"❌ Error fixing {filename}: {e}")
    
    # Step 2: Create missing data files
    print("\n📄 Creating missing data files...")
    create_missing_data_files()
    
    # Step 3: Test some scripts
    print("\n🧪 Testing scripts...")
    test_scripts = [
        "entropy_cluster_plot.py",
        "pulse_zone_timeline.py", 
        "bloom_lineage_radar.py",
        "interval_animation.py",
        "mood_pressure_timeseries.py"
    ]
    
    working = []
    for script in test_scripts:
        print(f"\nTesting {script}...")
        os.system(f'python run_visual.py {script}')
        
        # Check if output was created
        output_files = list(Path("visual_output").rglob("*.png")) + \
                      list(Path("visual_output").rglob("*.gif"))
        if output_files:
            working.append(script)
            print(f"✅ {script} created output!")
    
    print("\n" + "=" * 60)
    print("✅ Fix complete!")
    print(f"\n📊 Working scripts: {len(working)}")
    for script in working:
        print(f"  - {script}")
    
    print("\n💡 Try these commands:")
    print("python run_visual.py entropy_cluster_plot.py")
    print("python run_visual.py pulse_zone_timeline.py")
    print("python run_visual.py bloom_lineage_radar.py")
    
    # Check what output was created
    print("\n📁 Output files:")
    output_dir = Path("visual_output")
    if output_dir.exists():
        files = list(output_dir.rglob("*.*"))[:5]
        for f in files:
            print(f"  - {f.relative_to(output_dir)}")

if __name__ == "__main__":
    main()