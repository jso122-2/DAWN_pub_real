"""
Fix PathPatch import errors in DAWN visual scripts
Run from Tick_engine directory
"""

from pathlib import Path

visual_dir = Path("visual")

# Fix all Python files with PathPatch issues
for py_file in visual_dir.glob("*.py"):
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Check if file uses PathPatch incorrectly
        if "plt.PathPatch" in content or "pyplot.PathPatch" in content:
            # Add proper import
            if "from matplotlib.patches import PathPatch" not in content:
                # Find where to insert import
                if "import matplotlib.pyplot as plt" in content:
                    content = content.replace(
                        "import matplotlib.pyplot as plt",
                        "import matplotlib.pyplot as plt\nfrom matplotlib.patches import PathPatch"
                    )
                elif "import matplotlib" in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if "import matplotlib" in line:
                            lines.insert(i + 1, "from matplotlib.patches import PathPatch")
                            break
                    content = '\n'.join(lines)
                else:
                    content = "from matplotlib.patches import PathPatch\n" + content
            
            # Replace incorrect usage
            content = content.replace("plt.PathPatch", "PathPatch")
            content = content.replace("pyplot.PathPatch", "PathPatch")
            
            modified = True
        
        # Also fix Path import issues
        if "matplotlib.path.Path" in content and "from matplotlib.path import Path" not in content:
            if "import matplotlib" in content:
                content = content.replace(
                    "import matplotlib",
                    "import matplotlib\nfrom matplotlib.path import Path"
                )
                modified = True
        
        if modified:
            with open(py_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {py_file.name}")
    
    except Exception as e:
        print(f"❌ Error with {py_file.name}: {e}")

print("\n✅ PathPatch fixes complete!")
print("\nNow try running:")
print("python run_visual.py bloom_lineage_radar.py")