#!/usr/bin/env python3
"""
🔍 DAWN Class Finder - Discovers the main DAWN class
"""

import importlib
import inspect
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def find_dawn_classes():
    """Find potential DAWN main classes in various modules"""
    
    print("🔍 Searching for DAWN main class...")
    print("=" * 50)
    
    # Modules to check
    modules_to_check = [
        'main',
        'main_loop',
        'dawn_engine',
        'unified_tick_engine',
        'dawn_consciousness',
        'UnifiedTickEngine'
    ]
    
    found_classes = []
    
    for module_name in modules_to_check:
        try:
            # Import the module
            module = importlib.import_module(module_name)
            print(f"\n✅ Found module: {module_name}")
            
            # Look for classes
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    # Check if it's a DAWN-related class
                    if any(keyword in name.lower() for keyword in ['dawn', 'schema', 'engine', 'tick']):
                        # Check if it has a tick method
                        has_tick = hasattr(obj, 'tick') or hasattr(obj, 'run_tick') or hasattr(obj, 'run')
                        
                        found_classes.append({
                            'module': module_name,
                            'class': name,
                            'has_tick': has_tick,
                            'methods': [m for m in dir(obj) if not m.startswith('_')][:10]  # First 10 public methods
                        })
                        
                        print(f"  📦 Class: {name}")
                        print(f"     Has tick method: {'✅' if has_tick else '❌'}")
                        
        except ImportError as e:
            print(f"\n❌ Could not import {module_name}: {e}")
        except Exception as e:
            print(f"\n⚠️  Error checking {module_name}: {e}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if found_classes:
        print("\nPotential DAWN main classes:")
        for info in found_classes:
            if info['has_tick']:
                print(f"\n⭐ {info['module']}.{info['class']} (HAS TICK METHOD)")
                print(f"   Methods: {', '.join(info['methods'][:5])}...")
    else:
        print("\n❌ No DAWN classes found!")
    
    # Try to find the most likely candidate
    tick_classes = [c for c in found_classes if c['has_tick']]
    if tick_classes:
        best = tick_classes[0]
        print(f"\n🎯 Best candidate: {best['module']}.{best['class']}")
        print(f"\nTo use it, update your import to:")
        print(f"  from {best['module']} import {best['class']}")
    
    return found_classes


def check_main_py_directly():
    """Check what's actually in main.py"""
    print("\n" + "=" * 50)
    print("📄 Checking main.py directly...")
    print("=" * 50)
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
            
        # Look for class definitions
        import re
        classes = re.findall(r'class\s+(\w+)', content)
        functions = re.findall(r'def\s+(\w+)', content)
        
        print(f"\nClasses in main.py: {classes}")
        print(f"Main functions: {[f for f in functions if 'main' in f.lower() or 'run' in f.lower()]}")
        
        # Check if it's importing from elsewhere
        imports = re.findall(r'from\s+(\w+)\s+import', content)
        if imports:
            print(f"\nImports from: {imports}")
            
    except FileNotFoundError:
        print("❌ main.py not found!")
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")


if __name__ == "__main__":
    # Find classes
    classes = find_dawn_classes()
    
    # Check main.py directly
    check_main_py_directly()
    
    print("\n💡 Next steps:")
    print("1. Update your import based on the findings above")
    print("2. Or share the output so we can fix the import together")