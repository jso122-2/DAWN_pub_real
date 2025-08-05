#!/usr/bin/env python3
"""
Test script to verify DAWN Consolidated GUI startup without running the main loop
"""

import sys
import traceback

def test_gui_import():
    """Test if the GUI can be imported successfully"""
    try:
        from dawn_consolidated_gui import DAWNConsolidatedGUI
        print("✅ Successfully imported DAWNConsolidatedGUI")
        return True
    except ImportError as e:
        print(f"❌ Failed to import GUI: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        traceback.print_exc()
        return False

def test_gui_initialization():
    """Test if the GUI can be initialized without errors"""
    try:
        from dawn_consolidated_gui import DAWNConsolidatedGUI
        
        # Initialize but don't run mainloop
        print("🔧 Initializing GUI components...")
        app = DAWNConsolidatedGUI()
        
        # Test that key components exist
        assert hasattr(app, 'notebook'), "Notebook widget not created"
        assert hasattr(app, 'visual_tab'), "Visual tab not created"
        assert hasattr(app, 'voice_tab'), "Voice tab not created"
        assert hasattr(app, 'state_tab'), "State tab not created"
        assert hasattr(app, 'controls_tab'), "Controls tab not created"
        assert hasattr(app, 'archive_tab'), "Archive tab not created"
        assert hasattr(app, 'logs_tab'), "Logs tab not created"
        
        print("✅ GUI initialization successful!")
        print("📊 All tabs created successfully:")
        print("   🖼️  Visual tab")
        print("   🗣️  Voice tab") 
        print("   📊 State Monitor tab")
        print("   ⚙️  Controls tab")
        print("   📚 Archive tab")
        print("   📋 Logs tab")
        
        # Destroy the GUI to clean up
        app.root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ GUI initialization failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🌅 DAWN Consolidated GUI - Startup Test")
    print("=" * 50)
    
    # Test import
    if not test_gui_import():
        print("\n❌ Import test failed")
        sys.exit(1)
    
    # Test initialization
    if not test_gui_initialization():
        print("\n❌ Initialization test failed")
        sys.exit(1)
    
    print("\n🎉 All tests passed! GUI is ready for use.")
    print("💡 Run 'python launch_dawn_consolidated_gui.py' to start the full GUI")

if __name__ == "__main__":
    main() 