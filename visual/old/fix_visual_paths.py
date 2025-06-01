"""
Batch test all DAWN visual scripts to see which ones work
Run from Tick_engine directory
"""

import os
import subprocess
import sys
from pathlib import Path
import time

def test_all_visuals():
    """Test all visual scripts and categorize by status"""
    
    visual_dir = Path("visual")
    results = {
        "✅ Working": [],
        "⚠️ Runs but no output": [],
        "❌ File not found errors": [],
        "❌ Import errors": [],
        "❌ Other errors": [],
        "⏱️ Timeout": []
    }
    
    # Get all python files
    visual_scripts = sorted([f.name for f in visual_dir.glob("*.py") 
                            if f.name not in ["__init__.py", "__int__.py"]])
    
    print(f"🔍 Found {len(visual_scripts)} visual scripts to test")
    print("=" * 60)
    
    # Count output files before
    output_before = len(list(Path("visual_output").rglob("*.*"))) if Path("visual_output").exists() else 0
    
    for i, script in enumerate(visual_scripts, 1):
        print(f"\n[{i}/{len(visual_scripts)}] Testing {script}...", flush=True)
        
        # Try running with wrapper
        try:
            result = subprocess.run(
                [sys.executable, "run_visual.py", script],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=Path.cwd()
            )
            
            # Check output
            if result.returncode == 0:
                # Check if new files were created
                output_after = len(list(Path("visual_output").rglob("*.*"))) if Path("visual_output").exists() else 0
                
                if output_after > output_before:
                    results["✅ Working"].append(script)
                    print(f"  ✅ SUCCESS - Created {output_after - output_before} output file(s)")
                else:
                    results["⚠️ Runs but no output"].append(script)
                    print(f"  ⚠️ Ran successfully but no output created")
                
                output_before = output_after
                
            else:
                # Categorize error
                stderr = result.stderr
                if "FileNotFoundError" in stderr or "No such file" in stderr:
                    results["❌ File not found errors"].append(script)
                    print(f"  ❌ Missing data file")
                elif "ModuleNotFoundError" in stderr or "ImportError" in stderr:
                    results["❌ Import errors"].append(script)
                    print(f"  ❌ Import error")
                else:
                    results["❌ Other errors"].append(script)
                    error_line = stderr.strip().split('\n')[-1] if stderr else "Unknown error"
                    print(f"  ❌ {error_line[:60]}...")
                    
        except subprocess.TimeoutExpired:
            results["⏱️ Timeout"].append(script)
            print(f"  ⏱️ Timeout (might be creating animation)")
        except Exception as e:
            results["❌ Other errors"].append(script)
            print(f"  ❌ Exception: {str(e)[:60]}")
        
        time.sleep(0.1)  # Brief pause
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    for category, scripts in results.items():
        if scripts:
            print(f"\n{category} ({len(scripts)} scripts):")
            for script in scripts[:10]:  # Show first 10
                print(f"  - {script}")
            if len(scripts) > 10:
                print(f"  ... and {len(scripts) - 10} more")
    
    # Show created outputs
    print("\n📁 Output files created:")
    if Path("visual_output").exists():
        output_files = list(Path("visual_output").rglob("*.*"))
        recent_files = sorted(output_files, key=lambda x: x.stat().st_mtime, reverse=True)[:10]
        for f in recent_files:
            print(f"  - {f.relative_to('visual_output')}")
    
    # Create a simple HTML gallery of outputs
    create_output_gallery(results["✅ Working"])
    
    return results

def create_output_gallery(working_scripts):
    """Create an HTML gallery of generated visualizations"""
    output_dir = Path("visual_output")
    if not output_dir.exists():
        return
    
    # Find all image files
    image_files = list(output_dir.rglob("*.png")) + list(output_dir.rglob("*.jpg"))
    
    if not image_files:
        return
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>DAWN Visual Output Gallery</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f0f0f0; }
        .gallery { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .image-card { background: white; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        img { width: 100%; height: auto; border-radius: 4px; }
        .title { font-weight: bold; margin-top: 10px; }
        h1 { color: #333; }
        .stats { color: #666; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>🎨 DAWN Visual Output Gallery</h1>
    <div class="stats">
        <p>✅ Working scripts: {working_count}</p>
        <p>🖼️ Images generated: {image_count}</p>
    </div>
    <div class="gallery">
""".format(working_count=len(working_scripts), image_count=len(image_files))
    
    for img_path in image_files[:50]:  # Limit to 50 images
        rel_path = img_path.relative_to(output_dir)
        html_content += f"""
        <div class="image-card">
            <img src="visual_output/{rel_path.as_posix()}" alt="{rel_path.name}">
            <div class="title">{rel_path.name}</div>
            <div>{rel_path.parent}</div>
        </div>
"""
    
    html_content += """
    </div>
</body>
</html>
"""
    
    gallery_path = Path("dawn_visual_gallery.html")
    with open(gallery_path, 'w') as f:
        f.write(html_content)
    
    print(f"\n🖼️ Created output gallery: {gallery_path}")
    print("   Open dawn_visual_gallery.html in your browser to see all outputs")

def quick_test():
    """Quick test of most likely to work scripts"""
    print("🚀 Quick test of likely working scripts...")
    
    quick_scripts = [
        "bloom_lineage_radar.py",  # Known to work
        "entropy_cluster_plot.py",
        "pulse_map_renderer.py",
        "drift_compass.py",
        "memory_clusters.py",
        "mood_heatmap.py",
        "recursive_fieldmap.py",
        "visual_bloom_state.py"
    ]
    
    for script in quick_scripts:
        if Path(f"visual/{script}").exists():
            print(f"\n▶️ {script}")
            os.system(f"python run_visual.py {script}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test DAWN visual scripts')
    parser.add_argument('--quick', action='store_true', help='Quick test of likely working scripts')
    parser.add_argument('--all', action='store_true', help='Test all scripts')
    
    args = parser.parse_args()
    
    if args.quick:
        quick_test()
    else:
        results = test_all_visuals()
        
        print("\n💡 Next steps:")
        if results["✅ Working"]:
            print(f"1. View working visualizations: {', '.join(results['✅ Working'][:3])}")
        print("2. Open dawn_visual_gallery.html to see all generated images")
        print("3. Fix missing data files for scripts with FileNotFoundError")