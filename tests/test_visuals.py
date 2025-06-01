"""
Test which DAWN visualization scripts actually work
Run from Tick_engine directory
"""

import subprocess
import sys
from pathlib import Path
import time

# Visual scripts to test
visual_scripts = [
    # Likely to work (simpler plots)
    "interval_animation.py",
    "animate_synthesis_trails.py",
    "pulse_zone_timeline.py",
    "entropy_cluster_plot.py",
    "mood_pressure_timeseries.py",
    "tick_visual.py",
    
    # More complex (might have issues)
    "bloom_lineage_radar.py",
    "drift_compass.py",
    "pulse_map_renderer.py",
    "coherence_field_map.py",
    "memory_clusters.py",
    "scup_zone_animator.py",
    
    # Probably need full system
    "visual_consciousness_manager.py",
    "helix_consciousness_dashboard.py",
    "recursive_bloom_tree.py"
]

def test_script(script_name):
    """Test if a script runs without error"""
    try:
        result = subprocess.run(
            [sys.executable, "run_visual.py", script_name],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=Path.cwd()
        )
        
        if result.returncode == 0:
            # Check if it actually created output
            output_files = list(Path("visual_output").rglob("*.*"))
            if len(output_files) > 0:
                return "✅ SUCCESS (created output)"
            else:
                return "✅ RUNS (no visible output)"
        else:
            # Extract error type
            stderr = result.stderr
            if "PathPatch" in stderr:
                return "❌ PathPatch error"
            elif "ModuleNotFoundError" in stderr:
                module = stderr.split("'")[1] if "'" in stderr else "unknown"
                return f"❌ Missing: {module}"
            elif "FileNotFoundError" in stderr:
                return "❌ Missing data file"
            elif "KeyError" in stderr or "IndexError" in stderr:
                return "❌ Data format issue"
            else:
                error_line = stderr.strip().split('\n')[-1][:50]
                return f"❌ {error_line}"
                
    except subprocess.TimeoutExpired:
        return "⏱️ Timeout (might be working)"
    except Exception as e:
        return f"🚨 {str(e)[:30]}"

def fix_pathpatch_import():
    """Fix the PathPatch import issue in affected files"""
    visual_dir = Path("visual")
    fixed_count = 0
    
    print("\n🔧 Fixing PathPatch imports...")
    
    for py_file in visual_dir.glob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file has the PathPatch issue
            if "plt.PathPatch" in content or "pyplot.PathPatch" in content:
                # Add proper import if not present
                if "from matplotlib.patches import" not in content:
                    # Add import after other matplotlib imports
                    if "import matplotlib.pyplot as plt" in content:
                        content = content.replace(
                            "import matplotlib.pyplot as plt",
                            "import matplotlib.pyplot as plt\nfrom matplotlib.patches import PathPatch"
                        )
                    else:
                        # Add at top
                        content = "from matplotlib.patches import PathPatch\n" + content
                
                # Replace plt.PathPatch with PathPatch
                content = content.replace("plt.PathPatch", "PathPatch")
                content = content.replace("pyplot.PathPatch", "PathPatch")
                
                # Save fixed file
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Fixed: {py_file.name}")
                fixed_count += 1
                
        except Exception as e:
            print(f"  ❌ Error fixing {py_file.name}: {e}")
    
    print(f"\n✅ Fixed {fixed_count} files")
    return fixed_count

def main():
    print("🔍 Testing DAWN Visualization Scripts")
    print("=" * 60)
    
    # First, fix known issues
    fix_pathpatch_import()
    
    print("\n📊 Testing scripts...")
    print("=" * 60)
    
    results = {"success": [], "partial": [], "failed": []}
    
    for i, script in enumerate(visual_scripts, 1):
        print(f"[{i}/{len(visual_scripts)}] {script:<35}", end="", flush=True)
        
        status = test_script(script)
        print(status)
        
        if "SUCCESS" in status:
            results["success"].append(script)
        elif "RUNS" in status or "Timeout" in status:
            results["partial"].append(script)
        else:
            results["failed"].append((script, status))
        
        time.sleep(0.5)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    print(f"\n✅ Working ({len(results['success'])}):")
    for script in results["success"]:
        print(f"  - {script}")
    
    print(f"\n🟡 Partial/Timeout ({len(results['partial'])}):")
    for script in results["partial"]:
        print(f"  - {script}")
    
    print(f"\n❌ Failed ({len(results['failed'])}):")
    for script, error in results["failed"][:10]:  # Show first 10
        print(f"  - {script}: {error}")
    
    # Check what output was created
    print("\n📁 Output files created:")
    output_dir = Path("visual_output")
    if output_dir.exists():
        files = list(output_dir.rglob("*.*"))[:10]  # First 10 files
        for f in files:
            print(f"  - {f.relative_to(output_dir)}")
        if len(files) == 0:
            print("  (none)")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if results["success"]:
        print(f"1. Start with these working scripts: {results['success'][0]}")
    print("2. For PathPatch errors, the fix has been applied - retry those scripts")
    print("3. For missing module errors, those scripts need the full DAWN system")
    print("4. Scripts creating .gif/.mp4 animations may timeout but still be working")

if __name__ == "__main__":
    main()