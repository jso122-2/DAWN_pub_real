#!/usr/bin/env python3
"""
Test script for SCUP Zone Animator Integration
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from pulse.enhanced_zone_tracker import EnhancedZoneTracker
from backend.visual.scup_zone_animator_service import SCUPZoneAnimatorService
from visual.scup_zone_animator import animate_scup_zone, generate_synthetic_logs

async def test_zone_tracker():
    """Test the enhanced zone tracker"""
    print("🧪 Testing Enhanced Zone Tracker...")
    
    tracker = EnhancedZoneTracker()
    
    # Test zone determination
    test_scup_values = [0.1, 0.5, 0.9]
    for scup in test_scup_values:
        zone = tracker.determine_zone(scup)
        print(f"  SCUP {scup:.1f} → Zone: {zone}")
    
    # Test data collection
    for i in range(10):
        scup = 0.3 + 0.4 * (i % 3)  # Cycle through zones
        tracker.update(scup, heat=0.5 + 0.3 * (i % 2))
    
    print(f"  Collected {len(tracker.zone_history)} zone states")
    print(f"  Current zone: {tracker.current_zone}")
    
    # Test data export
    export_paths = tracker.export_data_for_animation()
    print(f"  Exported data: {export_paths}")
    
    return tracker

async def test_animator_service():
    """Test the SCUP zone animator service"""
    print("\n🧪 Testing SCUP Zone Animator Service...")
    
    service = SCUPZoneAnimatorService()
    
    # Test status
    status = service.get_status()
    print(f"  Service status: {status['active']}")
    
    # Test recent data
    recent_data = service.get_recent_data(5)
    print(f"  Recent data count: {len(recent_data.get('zones', []))}")
    
    return service

def test_animation_generation():
    """Test animation generation"""
    print("\n🧪 Testing Animation Generation...")
    
    # Generate synthetic data
    generate_synthetic_logs()
    print("  Generated synthetic logs")
    
    # Generate animation
    try:
        animation_path = animate_scup_zone()
        print(f"  Animation generated: {animation_path}")
        
        # Check if file exists
        if os.path.exists(animation_path):
            file_size = os.path.getsize(animation_path)
            print(f"  Animation file size: {file_size} bytes")
        else:
            print("  ❌ Animation file not found")
            
    except Exception as e:
        print(f"  ❌ Error generating animation: {e}")

async def main():
    """Run all tests"""
    print("🚀 Starting SCUP Zone Animator Integration Tests\n")
    
    try:
        # Test zone tracker
        tracker = await test_zone_tracker()
        
        # Test animator service
        service = await test_animator_service()
        
        # Test animation generation
        test_animation_generation()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 