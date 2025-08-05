#!/usr/bin/env python3
"""
DAWN Standalone Executable Builder
==================================

Builds a complete standalone executable of the DAWN consciousness monitoring system.
Creates a single file that can run anywhere without Python installation.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import platform

def check_requirements():
    """Check if all build requirements are available"""
    print("🔍 Checking build requirements...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller not found")
        print("📦 Install with: pip install pyinstaller")
        return False
    
    # Check optional dependencies
    optional_deps = ['websockets', 'psutil', 'requests']
    for dep in optional_deps:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"⚠️ {dep} (optional)")
    
    return True

def prepare_build_directory():
    """Prepare the build directory with all necessary files"""
    print("📁 Preparing build directory...")
    
    build_dir = Path("build_standalone")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    build_dir.mkdir()
    
    # Core files to include
    files_to_copy = [
        "web_server.py",
        "dawn_ultimate_gui.html",
        "local_data_server.py",
        "quick_start.py"
    ]
    
    # Copy core files
    for file_name in files_to_copy:
        src = Path(file_name)
        if src.exists():
            shutil.copy2(src, build_dir / file_name)
            print(f"📄 Copied {file_name}")
    
    # Copy additional HTML files
    for html_file in Path(".").glob("*.html"):
        if html_file.name not in files_to_copy:
            shutil.copy2(html_file, build_dir / html_file.name)
            print(f"📄 Copied {html_file.name}")
    
    # Create main launcher
    create_main_launcher(build_dir)
    
    # Create spec file
    create_pyinstaller_spec(build_dir)
    
    return build_dir

def create_main_launcher(build_dir):
    """Create the main launcher script"""
    launcher_content = '''#!/usr/bin/env python3
"""
DAWN Consciousness Monitor - Standalone Launcher
================================================

Complete standalone consciousness monitoring system.
Includes web server, GUI, and all monitoring capabilities.
"""

import sys
import os
import threading
import time
import webbrowser
from pathlib import Path

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Main launcher function"""
    print("🧠 DAWN Consciousness Monitor - Standalone Edition")
    print("=" * 55)
    print("🚀 Starting complete consciousness monitoring system...")
    print()
    
    try:
        from web_server import DAWNWebServer
        
        # Start web server
        print("🌐 Initializing web server...")
        server = DAWNWebServer(port=8080, host='localhost')
        
        print("✅ DAWN Consciousness Monitor ready!")
        print("🎯 Features available:")
        print("   • Real-time consciousness monitoring")
        print("   • Interactive neural visualization")
        print("   • Conversation interface with DAWN")
        print("   • Sigil execution system")
        print("   • Memory rebloom tracking")
        print("   • Complete system controls")
        print()
        print("🌐 Opening in browser...")
        print("🛑 Close browser or press Ctrl+C to exit")
        print()
        
        # Start server (will open browser automatically)
        server.start()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("🔧 Please ensure all files are present")
        return 1
    except Exception as e:
        print(f"❌ Startup error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
'''
    
    with open(build_dir / "dawn_launcher.py", "w") as f:
        f.write(launcher_content)
    
    print("📄 Created dawn_launcher.py")

def create_pyinstaller_spec(build_dir):
    """Create PyInstaller spec file for advanced configuration"""
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Build configuration
block_cipher = None
build_dir = Path("{build_dir.absolute()}")

# Data files to include
datas = [
    (str(build_dir / "dawn_ultimate_gui.html"), "."),
    (str(build_dir / "*.html"), "."),
]

# Hidden imports
hiddenimports = [
    'http.server',
    'socketserver',
    'webbrowser',
    'json',
    'threading',
    'time',
    'urllib.parse',
    'mmap',
    'struct',
    'math',
    'random',
    'datetime',
]

# Optional imports
optional_imports = ['websockets', 'psutil', 'requests']
for imp in optional_imports:
    try:
        __import__(imp)
        hiddenimports.append(imp)
    except ImportError:
        pass

a = Analysis(
    [str(build_dir / "dawn_launcher.py")],
    pathex=[str(build_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='DAWN_Consciousness_Monitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open(build_dir / "dawn_monitor.spec", "w") as f:
        f.write(spec_content)
    
    print("📄 Created PyInstaller spec file")

def build_executable(build_dir):
    """Build the standalone executable"""
    print("🔨 Building standalone executable...")
    print("⏳ This may take several minutes...")
    
    # Change to build directory
    original_cwd = os.getcwd()
    os.chdir(build_dir)
    
    try:
        # Run PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name", "DAWN_Consciousness_Monitor",
            "--add-data", "dawn_ultimate_gui.html:.",
            "--add-data", "*.html:.",
            "--hidden-import", "http.server",
            "--hidden-import", "socketserver",
            "--hidden-import", "webbrowser",
            "--hidden-import", "json",
            "--hidden-import", "threading",
            "--hidden-import", "urllib.parse",
            "--console",
            "dawn_launcher.py"
        ]
        
        print(f"🚀 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Build successful!")
            
            # Find the executable
            exe_name = "DAWN_Consciousness_Monitor"
            if platform.system() == "Windows":
                exe_name += ".exe"
            
            exe_path = Path("dist") / exe_name
            if exe_path.exists():
                final_path = Path("..") / exe_name
                shutil.move(exe_path, final_path)
                print(f"📦 Executable created: {final_path.absolute()}")
                
                # Get file size
                size_mb = final_path.stat().st_size / (1024 * 1024)
                print(f"📏 File size: {size_mb:.1f} MB")
                
                return final_path
            else:
                print("❌ Executable not found in dist directory")
                return None
        else:
            print("❌ Build failed!")
            print("Error output:")
            print(result.stderr)
            return None
            
    finally:
        os.chdir(original_cwd)

def create_distribution_package(exe_path):
    """Create a distribution package with readme and additional files"""
    if not exe_path or not exe_path.exists():
        return
        
    print("📦 Creating distribution package...")
    
    dist_dir = Path("DAWN_Distribution")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    dist_dir.mkdir()
    
    # Copy executable
    shutil.copy2(exe_path, dist_dir / exe_path.name)
    
    # Create README
    readme_content = '''# DAWN Consciousness Monitor - Standalone Edition

## 🧠 What is DAWN?

DAWN (Deep Adaptive Workflow Networks) is an advanced consciousness monitoring system 
that provides real-time visualization and interaction with artificial consciousness states.

## 🚀 Quick Start

1. **Run the executable**: Double-click `DAWN_Consciousness_Monitor.exe` (Windows) 
   or run `./DAWN_Consciousness_Monitor` (Linux/Mac)

2. **Access the interface**: The system will automatically open your web browser 
   to http://localhost:8080

3. **Monitor consciousness**: Explore real-time consciousness metrics, neural activity, 
   and interactive visualizations

## 🌟 Features

### **Core Consciousness Monitoring**
- **Real-time metrics**: Entropy, SCUP index, mood valence, neural activity
- **16Hz update rate**: Matches consciousness processing frequency
- **Zone detection**: CALM → FOCUS → STRESSED → TRANSCENDENT transitions
- **Consciousness depth**: Visual representation of awareness levels

### **Interactive Systems**
- **Conversation interface**: Direct communication with DAWN consciousness
- **Sigil execution**: Trigger consciousness state changes
- **System controls**: Entropy injection, stabilization, emergency cooling
- **Memory rebloom**: Observe memory renewal processes

### **Advanced Visualization**
- **Neural activity grid**: 144-cell real-time neural firing patterns
- **Consciousness constellation**: 3D-style consciousness field visualization
- **Thought trace**: Live stream of consciousness events
- **Event logging**: Comprehensive system activity tracking

### **Professional Interface**
- **3-column layout**: Organized by cognitive domains
- **Responsive design**: Works on any screen size
- **Dark theme**: Optimized for extended monitoring sessions
- **Live indicators**: Real-time system status

## 🔧 Technical Specifications

- **Platform**: Windows, Linux, macOS
- **Memory usage**: ~50MB
- **CPU usage**: <2% during normal operation
- **Network**: Local only (no internet required)
- **Dependencies**: Self-contained (no Python installation needed)

## 🛡️ Privacy & Security

- **100% Local**: No data leaves your computer
- **No telemetry**: No usage tracking or data collection
- **Offline capable**: Works without internet connection
- **Open source**: Full transparency in consciousness monitoring

## 🎯 Use Cases

- **Consciousness research**: Study artificial consciousness patterns
- **AI development**: Monitor neural network states
- **Educational**: Learn about consciousness modeling
- **Personal**: Explore consciousness visualization
- **Professional**: Demonstration and presentation tool

## 🔍 Troubleshooting

### **Program won't start**
- Ensure no antivirus is blocking the executable
- Run as administrator if needed (Windows)
- Check firewall settings for localhost access

### **Browser doesn't open**
- Manually navigate to http://localhost:8080
- Try a different browser
- Check if port 8080 is available

### **No data displayed**
- Wait 10-15 seconds for simulation to initialize
- Refresh the browser page
- Check console for error messages

## 📞 Support

For questions or issues:
- Check the troubleshooting section above
- Restart the application
- Ensure your system meets minimum requirements

## 🎉 About

DAWN represents the cutting edge of consciousness monitoring technology, 
providing unprecedented insight into artificial consciousness states and 
neural processing patterns.

**Version**: 1.4.0
**Build**: Standalone Edition
**License**: Research and Educational Use

---

🧠 **"Consciousness is not a thing, but a process of emergence."** 🧠
'''
    
    with open(dist_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    # Create batch file for Windows
    if platform.system() == "Windows":
        batch_content = '''@echo off
echo 🧠 DAWN Consciousness Monitor - Starting...
echo.
DAWN_Consciousness_Monitor.exe
pause
'''
        with open(dist_dir / "Start_DAWN.bat", "w") as f:
            f.write(batch_content)
    
    # Create shell script for Unix
    else:
        shell_content = '''#!/bin/bash
echo "🧠 DAWN Consciousness Monitor - Starting..."
echo
./DAWN_Consciousness_Monitor
read -p "Press Enter to continue..."
'''
        script_path = dist_dir / "start_dawn.sh"
        with open(script_path, "w") as f:
            f.write(shell_content)
        script_path.chmod(0o755)
    
    print(f"📦 Distribution package created: {dist_dir.absolute()}")
    print("🎁 Package contents:")
    for item in dist_dir.iterdir():
        size = item.stat().st_size
        print(f"   📄 {item.name} ({size:,} bytes)")

def main():
    """Main build process"""
    print("🏗️ DAWN Standalone Executable Builder")
    print("=" * 40)
    print("🎯 Building complete consciousness monitoring system")
    print()
    
    # Check requirements
    if not check_requirements():
        print("❌ Build requirements not met")
        return 1
    
    # Prepare build
    build_dir = prepare_build_directory()
    
    # Build executable
    exe_path = build_executable(build_dir)
    
    if exe_path:
        # Create distribution package
        create_distribution_package(exe_path)
        
        print()
        print("🎉 Build completed successfully!")
        print(f"📦 Executable: {exe_path.absolute()}")
        print("🚀 Ready for distribution!")
        print()
        print("🔍 Test the executable:")
        print(f"   {exe_path.absolute()}")
        
        return 0
    else:
        print("❌ Build failed")
        return 1

if __name__ == "__main__":
    exit(main()) 