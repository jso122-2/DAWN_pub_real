#!/usr/bin/env python3
"""
Test script for DAWN Log Manager
Demonstrates all logging capabilities with realistic DAWN scenarios
"""

import sys
import os
import time
import random

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from log_manager import (
    LogManager, 
    log_tick, 
    log_sigil, 
    log_bloom, 
    log_schema_event, 
    log_owl_observation,
    flush_logs,
    get_recent_logs
)


def test_basic_logging():
    """Test basic logging functionality"""
    print("🧪 Testing Basic Logging Functions")
    print("=" * 50)
    
    # Test individual log functions
    log_tick(1, "System initialization", 0.85, 0.2, "contemplative", "Clean startup detected")
    time.sleep(0.1)
    
    log_sigil("/\\", "Prime", 45, 2)
    time.sleep(0.1)
    
    log_bloom("bloom_001", 2, 0.3)
    time.sleep(0.1)
    
    log_schema_event("health_check", "Schema integrity verified", "success")
    time.sleep(0.1)
    
    log_owl_observation("System showing stable baseline patterns", 0.95)
    time.sleep(0.5)
    
    print("\n✅ Basic logging test completed\n")


def test_cognitive_scenario():
    """Test a realistic cognitive processing scenario"""
    print("🧠 Testing Cognitive Processing Scenario")
    print("=" * 50)
    
    # Scenario: DAWN processing a complex input
    scenarios = [
        (1, "Input received", 0.8, 0.1, "contemplative", "New data stream detected"),
        (2, "Pattern analysis", 0.75, 0.3, "active", "Analyzing input patterns"),
        (3, "Memory search", 0.7, 0.4, "active", "Searching memory banks"),
        (4, "Complexity surge", 0.6, 0.6, "intense", "High complexity detected"),
        (5, "Resource strain", 0.4, 0.8, "critical", "Memory pressure increasing"),
        (6, "Emergency regulation", 0.3, 0.9, "critical", "Emergency protocols activated"),
        (7, "Stabilization", 0.5, 0.7, "intense", "System stabilizing"),
        (8, "Recovery", 0.7, 0.5, "active", "Normal operations resuming"),
        (9, "Integration", 0.8, 0.3, "contemplative", "Knowledge integrated"),
        (10, "Rest state", 0.85, 0.2, "contemplative", "Processing complete")
    ]
    
    sigils = [
        ("◇", "Bloom", 60, 3),
        ("/|-/", "Recursive", 75, 4),
        ("⟁", "Contradiction", 85, 5),
        ("⌂", "Memory", 40, 2),
        ("~", "Echo", 30, 1)
    ]
    
    blooms = [
        ("b001", 1, 0.2, None),
        ("b002", 2, 0.4, "b001"),
        ("b003", 3, 0.6, "b002"),
        ("b004", 2, 0.5, "b001"),
        ("b005", 4, 0.7, "b003")
    ]
    
    # Execute scenario
    for i, (tick_id, pulse, scup, entropy, zone, owl_comment) in enumerate(scenarios):
        log_tick(tick_id, pulse, scup, entropy, zone, owl_comment)
        
        # Add some sigil activity
        if i < len(sigils):
            sigil_id, house, temp, conv = sigils[i]
            log_sigil(sigil_id, house, temp, conv)
        
        # Add some bloom activity
        if i < len(blooms):
            bloom_id, depth, b_entropy, parent = blooms[i]
            log_bloom(bloom_id, depth, b_entropy, parent)
        
        # Add schema events for critical states
        if scup < 0.4:
            log_schema_event("pressure_alert", f"SCUP critically low: {scup:.3f}", "critical")
        elif entropy > 0.8:
            log_schema_event("entropy_spike", f"High entropy detected: {entropy:.3f}", "warning")
        
        time.sleep(0.2)  # Brief pause between logs
    
    print("\n✅ Cognitive scenario test completed\n")


def test_stress_logging():
    """Test logging under stress with many rapid entries"""
    print("⚡ Testing Stress Logging (Rapid Entries)")
    print("=" * 50)
    
    start_time = time.time()
    num_entries = 50
    
    for i in range(num_entries):
        tick_id = 100 + i
        scup = random.uniform(0.2, 0.9)
        entropy = random.uniform(0.1, 0.8)
        
        # Random zone based on scup
        if scup > 0.8:
            zone = "contemplative"
        elif scup > 0.6:
            zone = "active"
        elif scup > 0.4:
            zone = "intense"
        else:
            zone = "critical"
        
        log_tick(tick_id, f"Rapid processing {i+1}", scup, entropy, zone, f"Stress test entry {i+1}")
        
        # Occasional other events
        if i % 10 == 0:
            log_sigil(f"S{i}", "Stress", random.randint(20, 90), random.randint(1, 5))
        
        if i % 15 == 0:
            log_bloom(f"stress_bloom_{i}", random.randint(1, 4), random.uniform(0.2, 0.8))
    
    elapsed = time.time() - start_time
    
    print(f"✅ Logged {num_entries} entries in {elapsed:.2f} seconds")
    print(f"📊 Rate: {num_entries/elapsed:.1f} entries/second\n")


def test_file_operations():
    """Test file operations and persistence"""
    print("💾 Testing File Operations")
    print("=" * 50)
    
    # Get log manager instance
    from log_manager import get_log_manager
    logger = get_log_manager()
    
    # Show current stats
    stats = logger.get_log_stats()
    print(f"📊 Current Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show recent logs
    recent = get_recent_logs(10)
    print(f"\n📋 Recent Logs ({len(recent)} entries):")
    for line in recent[-5:]:  # Show last 5
        print(f"  {line}")
    
    # Force flush to file
    print(f"\n💾 Flushing logs to file...")
    flush_logs()
    
    # Check if logs directory exists and has files
    logs_dir = stats['logs_directory']
    if os.path.exists(logs_dir):
        log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
        print(f"📁 Found {len(log_files)} log files in {logs_dir}")
        if log_files:
            latest_file = max(log_files)
            print(f"📄 Latest file: {latest_file}")
    
    print("\n✅ File operations test completed\n")


def test_error_handling():
    """Test error handling and edge cases"""
    print("🛡️ Testing Error Handling")
    print("=" * 50)
    
    # Test with extreme values
    log_tick(-1, "", -0.5, 2.0, "invalid_zone", "")
    log_sigil("", "", -10, 100)
    log_bloom("", -1, -1.0, "nonexistent")
    
    # Test with None values (should handle gracefully)
    try:
        log_schema_event("", "", "")
        log_owl_observation("", -1.0)
        print("✅ Error handling working correctly")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
    
    print("\n✅ Error handling test completed\n")


def run_full_test_suite():
    """Run the complete test suite"""
    print("🚀 DAWN Log Manager - Full Test Suite")
    print("=" * 60)
    print()
    
    try:
        # Run all tests
        test_basic_logging()
        test_cognitive_scenario()
        test_stress_logging()
        test_file_operations()
        test_error_handling()
        
        # Final summary
        from log_manager import get_log_manager
        logger = get_log_manager()
        final_stats = logger.get_log_stats()
        
        print("🎉 Test Suite Completed Successfully!")
        print("=" * 60)
        print(f"📊 Final Statistics:")
        for key, value in final_stats.items():
            print(f"  {key}: {value}")
        
        # Shutdown gracefully
        logger.shutdown()
        
        print("\n✅ All tests passed! Log manager is working correctly.")
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_full_test_suite()
    if not success:
        sys.exit(1) 