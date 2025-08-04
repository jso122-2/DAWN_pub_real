#!/usr/bin/env python3
"""
Test Import Chain
================

Test the import chain to find where the relative import error is occurring.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

def test_import_chain():
    """Test the import chain step by step"""
    
    print("🔍 Testing Import Chain")
    print("=" * 40)
    
    # Test 1: Import core.dawn_runner
    print("1. Testing core.dawn_runner import...")
    try:
        from core.dawn_runner import DAWNUnifiedRunner
        print("   ✅ core.dawn_runner import successful")
    except Exception as e:
        print(f"   ❌ core.dawn_runner import failed: {e}")
        return
    
    # Test 2: Test specific imports that might be causing issues
    print("\n2. Testing specific imports...")
    
    # Test conversation imports
    try:
        from .conversation_input import ConversationInput
        print("   ✅ conversation.conversation_input import successful")
    except Exception as e:
        print(f"   ❌ conversation.conversation_input import failed: {e}")
    
    # Test visual imports
    try:
        from visual.visual_trigger import trigger_visual_snapshot
        print("   ✅ visual.visual_trigger import successful")
    except Exception as e:
        print(f"   ❌ visual.visual_trigger import failed: {e}")
    
    # Test runtime imports
    try:
        from runtime.tick_visual_integration import VisualTickIntegration
        print("   ✅ runtime.tick_visual_integration import successful")
    except Exception as e:
        print(f"   ❌ runtime.tick_visual_integration import failed: {e}")
    
    # Test tracers imports
    try:
        from tracers.enhanced_tracer_echo_voice import EnhancedTracerEchoVoice
        print("   ✅ tracers.enhanced_tracer_echo_voice import successful")
    except Exception as e:
        print(f"   ❌ tracers.enhanced_tracer_echo_voice import failed: {e}")
    
    print("\n✅ Import chain test complete")

if __name__ == "__main__":
    test_import_chain() 