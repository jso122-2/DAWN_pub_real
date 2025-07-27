#!/usr/bin/env python3
"""
Enhanced DAWN GUI Setup Script
Checks dependencies and sets up the environment for the enhanced DAWN GUI

Usage:
    python setup_enhanced_gui.py [--install]
    
Options:
    --install    Attempt to install missing dependencies automatically
"""

import sys
import subprocess
import importlib
import argparse
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_required_packages():
    """Check if required packages are installed"""
    required_packages = [
        'tkinter',
        'numpy', 
        'matplotlib',
        'PIL',
        'threading',
        'json'
    ]
    
    missing_packages = []
    
    print("\n📦 Checking required packages...")
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'PIL':
                from PIL import Image
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    return missing_packages


def check_dawn_components():
    """Check if DAWN core components are available"""
    print("\n🧠 Checking DAWN core components...")
    
    # Add project root to path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    
    components = [
        ('core.pulse_controller', 'PulseController'),
        ('core.dawn_entropy_analyzer', 'EnhancedEntropyAnalyzer'),
        ('reflex.reflex_executor', 'ReflexExecutor'),
        ('reflex.fractal_colorizer', 'FractalColorizer'),
        ('gui.dawn_gui_enhanced', 'EnhancedDawnGUI')
    ]
    
    missing_components = []
    
    for module_path, class_name in components:
        try:
            module = importlib.import_module(module_path)
            getattr(module, class_name)
            print(f"✅ {module_path}.{class_name}")
        except (ImportError, AttributeError) as e:
            print(f"❌ {module_path}.{class_name} - {e}")
            missing_components.append(f"{module_path}.{class_name}")
    
    return missing_components


def install_missing_packages(packages):
    """Attempt to install missing packages using pip"""
    if not packages:
        return True
    
    print(f"\n📥 Attempting to install missing packages: {', '.join(packages)}")
    
    for package in packages:
        # Map package names to pip install names
        pip_name = package
        if package == 'PIL':
            pip_name = 'Pillow'
        elif package == 'tkinter':
            print("⚠️  tkinter is built into Python - may need system package")
            continue
        
        try:
            print(f"Installing {pip_name}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pip_name])
            print(f"✅ {pip_name} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {pip_name}: {e}")
            return False
    
    return True


def setup_directories():
    """Ensure required directories exist"""
    print("\n📁 Setting up directories...")
    
    project_root = Path(__file__).parent.parent
    required_dirs = [
        project_root / "logs",
        project_root / "runtime" / "memory",
        project_root / "visual_outputs",
        project_root / "state"
    ]
    
    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")


def run_component_test():
    """Run a quick test of GUI components"""
    print("\n🧪 Running component test...")
    
    try:
        # Add project root to path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))
        
        # Test basic GUI creation
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide window
        
        # Test DAWN components
        from core.pulse_controller import PulseController
        pulse_controller = PulseController()
        
        from core.dawn_entropy_analyzer import EnhancedEntropyAnalyzer
        entropy_analyzer = EnhancedEntropyAnalyzer()
        
        root.destroy()
        print("✅ Component test passed")
        return True
        
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description='Setup Enhanced DAWN GUI')
    parser.add_argument('--install', action='store_true', 
                       help='Attempt to install missing dependencies')
    args = parser.parse_args()
    
    print("🌟 DAWN Enhanced GUI Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check required packages
    missing_packages = check_required_packages()
    
    # Check DAWN components
    missing_components = check_dawn_components()
    
    # Setup directories
    setup_directories()
    
    # Install missing packages if requested
    if missing_packages and args.install:
        if not install_missing_packages(missing_packages):
            print("\n❌ Package installation failed")
            sys.exit(1)
        # Re-check packages after installation
        missing_packages = check_required_packages()
    
    # Report results
    print("\n📋 Setup Summary:")
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run with --install to attempt automatic installation")
    else:
        print("✅ All required packages available")
    
    if missing_components:
        print(f"❌ Missing DAWN components: {len(missing_components)}")
        for component in missing_components:
            print(f"   - {component}")
    else:
        print("✅ All DAWN components available")
    
    # Run component test if everything looks good
    if not missing_packages and not missing_components:
        if run_component_test():
            print("\n🎉 Enhanced DAWN GUI setup completed successfully!")
            print("💡 You can now run the GUI with: python gui/dawn_gui_enhanced.py")
        else:
            print("\n⚠️  Setup completed but component test failed")
    else:
        print("\n⚠️  Setup incomplete - please resolve missing dependencies")


if __name__ == "__main__":
    main() 