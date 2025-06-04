"""
Enhanced batch test for DAWN visual scripts with comprehensive results saving
Run from Tick_engine directory
"""

import os
import subprocess
import sys
from pathlib import Path
import time
import json
from datetime import datetime

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
    
    # Detailed results for each script
    detailed_results = {}
    
    # Get all python files
    visual_scripts = sorted([f.name for f in visual_dir.glob("*.py") 
                            if f.name not in ["__init__.py", "__int__.py"]])
    
    print(f"🔍 Found {len(visual_scripts)} visual scripts to test")
    print("=" * 60)
    
    # Count output files before
    output_before = len(list(Path("visual_output").rglob("*.*"))) if Path("visual_output").exists() else 0
    
    # Track test metadata
    test_metadata = {
        "timestamp": datetime.now().isoformat(),
        "total_scripts": len(visual_scripts),
        "python_version": sys.version,
        "working_directory": str(Path.cwd()),
        "output_directory": str(Path("visual_output").absolute()) if Path("visual_output").exists() else None
    }
    
    for i, script in enumerate(visual_scripts, 1):
        print(f"\n[{i}/{len(visual_scripts)}] Testing {script}...", flush=True)
        
        script_result = {
            "script": script,
            "index": i,
            "start_time": datetime.now().isoformat()
        }
        
        # Try running with wrapper
        try:
            start_time = time.time()
            result = subprocess.run(
                [sys.executable, "run_visual.py", script],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=Path.cwd()
            )
            execution_time = time.time() - start_time
            
            script_result["execution_time"] = execution_time
            script_result["return_code"] = result.returncode
            script_result["stdout"] = result.stdout
            script_result["stderr"] = result.stderr
            
            # Check output
            if result.returncode == 0:
                # Check if new files were created
                output_after = len(list(Path("visual_output").rglob("*.*"))) if Path("visual_output").exists() else 0
                files_created = output_after - output_before
                
                script_result["files_created"] = files_created
                
                # Get list of new files
                if files_created > 0:
                    all_files = list(Path("visual_output").rglob("*.*"))
                    all_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                    new_files = [str(f.relative_to("visual_output")) for f in all_files[:files_created]]
                    script_result["output_files"] = new_files
                
                if files_created > 0:
                    results["✅ Working"].append(script)
                    script_result["status"] = "working"
                    print(f"  ✅ SUCCESS - Created {files_created} output file(s)")
                else:
                    results["⚠️ Runs but no output"].append(script)
                    script_result["status"] = "runs_no_output"
                    print(f"  ⚠️ Ran successfully but no output created")
                
                output_before = output_after
                
            else:
                # Categorize error
                stderr = result.stderr
                if "FileNotFoundError" in stderr or "No such file" in stderr:
                    results["❌ File not found errors"].append(script)
                    script_result["status"] = "file_not_found"
                    script_result["error_type"] = "FileNotFoundError"
                    # Extract missing file
                    if "No such file" in stderr:
                        lines = stderr.split('\n')
                        for line in lines:
                            if "No such file" in line:
                                script_result["missing_file"] = line
                    print(f"  ❌ Missing data file")
                    
                elif "ModuleNotFoundError" in stderr or "ImportError" in stderr:
                    results["❌ Import errors"].append(script)
                    script_result["status"] = "import_error"
                    script_result["error_type"] = "ImportError"
                    # Extract missing module
                    if "No module named" in stderr:
                        module_match = stderr.split("No module named")[1].split("'")[1]
                        script_result["missing_module"] = module_match
                    print(f"  ❌ Import error")
                    
                else:
                    results["❌ Other errors"].append(script)
                    script_result["status"] = "other_error"
                    error_line = stderr.strip().split('\n')[-1] if stderr else "Unknown error"
                    script_result["error_summary"] = error_line
                    print(f"  ❌ {error_line[:60]}...")
                    
        except subprocess.TimeoutExpired:
            results["⏱️ Timeout"].append(script)
            script_result["status"] = "timeout"
            script_result["execution_time"] = 10.0  # timeout value
            print(f"  ⏱️ Timeout (might be creating animation)")
            
        except Exception as e:
            results["❌ Other errors"].append(script)
            script_result["status"] = "exception"
            script_result["exception"] = str(e)
            print(f"  ❌ Exception: {str(e)[:60]}")
        
        script_result["end_time"] = datetime.now().isoformat()
        detailed_results[script] = script_result
        
        time.sleep(0.1)  # Brief pause
    
    # Save results to JSON
    results_data = {
        "metadata": test_metadata,
        "summary": {
            category: {
                "count": len(scripts),
                "scripts": scripts
            }
            for category, scripts in results.items()
        },
        "detailed_results": detailed_results
    }
    
    # Save to timestamped file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = Path(f"visual_test_results_{timestamp}.json")
    with open(results_file, 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")
    
    # Also save a summary report
    create_summary_report(results, detailed_results, timestamp)
    
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
    create_output_gallery(results["✅ Working"], timestamp)
    
    return results

def create_summary_report(results, detailed_results, timestamp):
    """Create a markdown summary report"""
    report_file = Path(f"visual_test_report_{timestamp}.md")
    
    with open(report_file, 'w') as f:
        f.write("# DAWN Visual Scripts Test Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Overview statistics
        total = sum(len(scripts) for scripts in results.values())
        f.write("## Overview\n\n")
        f.write(f"- **Total Scripts Tested:** {total}\n")
        f.write(f"- **Working Scripts:** {len(results['✅ Working'])}\n")
        f.write(f"- **Scripts Running Without Output:** {len(results['⚠️ Runs but no output'])}\n")
        f.write(f"- **Failed Scripts:** {len(results['❌ File not found errors']) + len(results['❌ Import errors']) + len(results['❌ Other errors'])}\n")
        f.write(f"- **Timeout Scripts:** {len(results['⏱️ Timeout'])}\n\n")
        
        # Success rate
        if total > 0:
            success_rate = (len(results['✅ Working']) / total) * 100
            f.write(f"**Success Rate:** {success_rate:.1f}%\n\n")
        
        # Detailed categories
        f.write("## Detailed Results\n\n")
        
        # Working scripts
        if results['✅ Working']:
            f.write("### ✅ Working Scripts\n\n")
            f.write("These scripts successfully created output files:\n\n")
            for script in sorted(results['✅ Working']):
                detail = detailed_results.get(script, {})
                files = detail.get('output_files', [])
                exec_time = detail.get('execution_time', 0)
                f.write(f"- **{script}** ({exec_time:.2f}s)")
                if files:
                    f.write(f" - Created: {', '.join(files[:3])}")
                    if len(files) > 3:
                        f.write(f" and {len(files)-3} more")
                f.write("\n")
            f.write("\n")
        
        # Scripts that run but don't save
        if results['⚠️ Runs but no output']:
            f.write("### ⚠️ Scripts Running Without Output\n\n")
            f.write("These scripts run successfully but don't save any files (may use plt.show() only):\n\n")
            for script in sorted(results['⚠️ Runs but no output']):
                f.write(f"- {script}\n")
            f.write("\n")
        
        # File not found errors
        if results['❌ File not found errors']:
            f.write("### ❌ File Not Found Errors\n\n")
            f.write("These scripts are missing required data files:\n\n")
            for script in sorted(results['❌ File not found errors']):
                detail = detailed_results.get(script, {})
                missing = detail.get('missing_file', 'Unknown file')
                f.write(f"- **{script}** - Missing: `{missing}`\n")
            f.write("\n")
        
        # Import errors
        if results['❌ Import errors']:
            f.write("### ❌ Import Errors\n\n")
            f.write("These scripts have missing module dependencies:\n\n")
            for script in sorted(results['❌ Import errors']):
                detail = detailed_results.get(script, {})
                module = detail.get('missing_module', 'Unknown module')
                f.write(f"- **{script}** - Missing module: `{module}`\n")
            f.write("\n")
        
        # Other errors
        if results['❌ Other errors']:
            f.write("### ❌ Other Errors\n\n")
            for script in sorted(results['❌ Other errors']):
                detail = detailed_results.get(script, {})
                error = detail.get('error_summary', detail.get('exception', 'Unknown error'))
                f.write(f"- **{script}** - {error[:100]}\n")
            f.write("\n")
        
        # Timeout scripts
        if results['⏱️ Timeout']:
            f.write("### ⏱️ Timeout Scripts\n\n")
            f.write("These scripts exceeded the 10-second timeout (may be creating animations):\n\n")
            for script in sorted(results['⏱️ Timeout']):
                f.write(f"- {script}\n")
            f.write("\n")
        
        # Recommendations
        f.write("## Recommendations\n\n")
        f.write("1. **For scripts without output:** Run `fix_visual_outputs.py` to add save functionality\n")
        f.write("2. **For file not found errors:** Create missing data files or run the main DAWN system first\n")
        f.write("3. **For import errors:** Install missing dependencies or ensure proper Python path\n")
        f.write("4. **For timeout scripts:** These may be creating animations - increase timeout or run individually\n")
    
    print(f"📄 Summary report saved to: {report_file}")

def create_output_gallery(working_scripts, timestamp):
    """Create an enhanced HTML gallery of generated visualizations"""
    output_dir = Path("visual_output")
    if not output_dir.exists():
        return
    
    # Find all image files
    image_files = list(output_dir.rglob("*.png")) + list(output_dir.rglob("*.jpg"))
    
    if not image_files:
        return
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>DAWN Visual Output Gallery - {timestamp}</title>
    <style>
        body {{ font-family: Arial; margin: 20px; background: #f0f0f0; }}
        .header {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .image-card {{ background: white; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        img {{ width: 100%; height: auto; border-radius: 4px; cursor: pointer; }}
        .title {{ font-weight: bold; margin-top: 10px; }}
        h1 {{ color: #333; }}
        .stats {{ color: #666; margin-bottom: 20px; }}
        .modal {{ display: none; position: fixed; z-index: 1; padding-top: 60px; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.9); }}
        .modal-content {{ margin: auto; display: block; width: 80%; max-width: 1200px; }}
        .close {{ position: absolute; top: 15px; right: 35px; color: #f1f1f1; font-size: 40px; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 DAWN Visual Output Gallery</h1>
        <div class="stats">
            <p>✅ Working scripts: {len(working_scripts)}</p>
            <p>🖼️ Images generated: {len(image_files)}</p>
            <p>📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
    
    <div class="gallery">
"""
    
    for img_path in sorted(image_files, key=lambda x: x.stat().st_mtime, reverse=True)[:50]:  # Most recent first
        rel_path = img_path.relative_to(output_dir)
        html_content += f"""
        <div class="image-card">
            <img src="visual_output/{rel_path.as_posix()}" alt="{rel_path.name}" onclick="openModal(this)">
            <div class="title">{rel_path.name}</div>
            <div style="color: #666; font-size: 0.9em;">{rel_path.parent}</div>
        </div>
"""
    
    html_content += """
    </div>
    
    <div id="myModal" class="modal">
        <span class="close" onclick="closeModal()">&times;</span>
        <img class="modal-content" id="modalImg">
    </div>
    
    <script>
    function openModal(img) {
        var modal = document.getElementById("myModal");
        var modalImg = document.getElementById("modalImg");
        modal.style.display = "block";
        modalImg.src = img.src;
    }
    
    function closeModal() {
        document.getElementById("myModal").style.display = "none";
    }
    
    // Close modal on ESC key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModal();
        }
    });
    </script>
</body>
</html>
"""
    
    gallery_path = Path(f"dawn_visual_gallery_{timestamp}.html")
    with open(gallery_path, 'w') as f:
        f.write(html_content)
    
    print(f"\n🖼️ Created output gallery: {gallery_path}")
    print("   Open in your browser to see all generated visualizations")

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
    
    results = []
    for script in quick_scripts:
        if Path(f"visual/{script}").exists():
            print(f"\n▶️ {script}")
            result = os.system(f"python run_visual.py {script}")
            results.append({
                "script": script,
                "success": result == 0
            })
    
    # Save quick test results
    with open("quick_test_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Quick test results saved to: quick_test_results.json")

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
        print("2. Check the timestamped JSON file for detailed results")
        print("3. Read the markdown report for recommendations")
        print("4. Open the HTML gallery to view all generated images")