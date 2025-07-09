#!/usr/bin/env python3
"""
Test script for DAWN GUI with Codex Integration
"""

import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_codex_integration():
    """Test the codex engine integration with the GUI"""
    
    print("=" * 60)
    print("DAWN Codex Integration Test")
    print("=" * 60)
    
    # Test codex engine functions directly
    try:
        from codex.codex_engine import (
            get_pulse_zone, 
            describe_pulse_zone, 
            get_schema_health, 
            summarize_bloom
        )
        
        print("✅ Codex engine imported successfully")
        
        # Test pulse zone functions
        print("\n📊 Testing Pulse Zone Functions:")
        for heat in [15, 35, 55, 75, 95]:
            zone = get_pulse_zone(heat)
            description = describe_pulse_zone(zone)
            print(f"  Heat {heat:2d} → Zone: {zone:12s} | {description[:50]}...")
        
        # Test schema health
        print("\n🏥 Testing Schema Health Function:")
        health = get_schema_health(
            schema_pressure=0.6,
            coherence=0.7,
            entropy=0.4,
            heat=50.0
        )
        print(f"  Status: {health['status']}")
        print(f"  Score: {health['health_score']:.3f}")
        print(f"  Stability: {health['stability']:.3f}")
        if health['indicators']:
            print(f"  Indicators: {', '.join(health['indicators'])}")
        
        # Test bloom summary
        print("\n🌸 Testing Bloom Summary Function:")
        summary = summarize_bloom(
            depth=3,
            heat=45.0,
            coherence=0.8,
            frequency=1.2,
            intensity=0.6
        )
        print(f"  Summary: {summary}")
        
        print("\n✅ All codex functions working correctly!")
        
    except ImportError as e:
        print(f"❌ Failed to import codex engine: {e}")
        return False
    
    except Exception as e:
        print(f"❌ Error testing codex functions: {e}")
        return False
    
    # Test GUI integration
    print("\n" + "=" * 60)
    print("Starting DAWN GUI with Codex Integration...")
    print("=" * 60)
    
    try:
        import tkinter as tk
        from gui.dawn_gui_tk import DAWNGui
        
        # Create GUI
        root = tk.Tk()
        gui = DAWNGui(root)
        
        print("🚀 GUI created successfully with codex integration!")
        print("💡 Close the GUI window to complete the test")
        
        # Start the GUI
        root.mainloop()
        
        print("✅ GUI test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error running GUI: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_codex_integration()
    if success:
        print("\n🎉 Codex integration test completed successfully!")
    else:
        print("\n💥 Codex integration test failed!")
        sys.exit(1) 