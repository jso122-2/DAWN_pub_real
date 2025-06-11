#!/usr/bin/env python3
"""
test_pulse_engine.py

Test suite for PulseEngine class
Includes unit tests, integration tests, and benchmarking

Coverage:
- Unit tests: Core functionality, edge cases
- Integration tests: Zone transitions, thermal events
- Benchmarks: Performance under load
"""

import unittest
import time
import json
from pathlib import Path
from datetime import datetime
import statistics
from typing import List, Dict, Any
import tempfile
import shutil

from pulse.pulse_engine import PulseEngine, PulseMetrics, PulseZoneState
from pulse.zone_tracker import PulseEvent
from pulse.overheat_detector import ThermalEvent, ThermalAlert

class TestPulseEngine(unittest.TestCase):
    """Unit tests for PulseEngine"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.config_path = Path(self.test_dir) / 'test_pulse_config.yaml'
        self.metrics_path = Path(self.test_dir) / 'logs' / 'pulse_metrics.json'
        self.metrics_path.parent.mkdir(exist_ok=True)
        
        # Create test config
        self._create_test_config()
        
        # Initialize engine with test config
        self.engine = PulseEngine(config_path=str(self.config_path))
        
    def tearDown(self):
        """Clean up test environment"""
        self.engine.shutdown()
        shutil.rmtree(self.test_dir)
        
    def _create_test_config(self):
        """Create test configuration file"""
        config = {
            'pressure_limit': 0.85,
            'cooldown_ms': 100,
            'zone_alert_level': 0.75,
            'thermal_thresholds': {
                'warning': 0.7,
                'critical': 0.85,
                'emergency': 0.95
            },
            'zone_thresholds': {
                'calm': 0.3,
                'active': 0.7,
                'surge': 0.9
            },
            'monitoring': {
                'interval': 0.1,
                'history_size': 10,
                'log_level': 'DEBUG'
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
            
    def test_initialization(self):
        """Test engine initialization"""
        self.assertFalse(self.engine.active)
        self.assertIsNone(self.engine.current_zone)
        self.assertEqual(self.engine.pulse_count, 0)
        self.assertEqual(len(self.engine.zones), 3)
        
    def test_update_normal(self):
        """Test normal update operation"""
        # Wire engine
        self.engine.wire(None)
        
        # Test normal temperature update
        event = self.engine.update(30.0, 0.5)
        self.assertIsNotNone(event)
        self.assertEqual(self.engine.pulse_count, 1)
        self.assertLess(self.engine.thermal_stats['avg_temp'], 31.0)
        
    def test_update_high_pressure(self):
        """Test update with high system pressure"""
        self.engine.wire(None)
        
        # Simulate high pressure condition
        event = self.engine.update(90.0, 0.9)
        self.assertIsNotNone(event)
        self.assertTrue(event.is_critical)
        
    def test_zone_transitions(self):
        """Test zone transition logic"""
        self.engine.wire(None)
        
        # Test calm -> active transition
        self.engine.update(40.0, 0.4)  # Calm zone
        self.engine.update(60.0, 0.6)  # Active zone
        active_zones = self.engine.get_active_zones()
        self.assertTrue(active_zones['🟡 active']['is_active'])
        
    def test_metrics_logging(self):
        """Test metrics logging functionality"""
        self.engine.wire(None)
        
        # Generate some activity
        for _ in range(20):  # Should trigger metrics logging
            self.engine.update(50.0, 0.5)
            
        # Check metrics file
        self.assertTrue(self.metrics_path.exists())
        with open(self.metrics_path, 'r') as f:
            metrics = json.load(f)
            self.assertGreater(len(metrics), 0)
            
    def test_batch_processing(self):
        """Test batch processing functionality"""
        self.engine.wire(None)
        
        # Fill batch buffer
        for _ in range(self.engine.batch_size):
            self.engine.update(50.0, 0.5)
            
        # Check batch processing
        metrics = self.engine.get_metrics()
        self.assertEqual(metrics.batch_size, 0)  # Buffer should be empty after processing

class TestPulseEngineIntegration(unittest.TestCase):
    """Integration tests for PulseEngine"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.engine = PulseEngine()
        self.engine.wire(None)
        
    def tearDown(self):
        """Clean up integration test environment"""
        self.engine.shutdown()
        
    def test_thermal_spike_recovery(self):
        """Test system recovery from thermal spike"""
        # Simulate thermal spike
        for temp in [30, 40, 50, 60, 70, 80, 90, 80, 70, 60, 50, 40, 30]:
            event = self.engine.update(temp, temp/100)
            time.sleep(0.1)
            
        # Check recovery
        metrics = self.engine.get_metrics()
        self.assertLess(metrics.system_pressure, 0.85)
        self.assertEqual(metrics.active_zones, 1)  # Should be in calm zone
        
    def test_zone_cascade(self):
        """Test cascading zone transitions"""
        # Simulate zone cascade
        temps = [30, 45, 60, 75, 90, 75, 60, 45, 30]
        for temp in temps:
            self.engine.update(temp, temp/100)
            time.sleep(0.1)
            
        # Check zone transitions
        zone_stats = self.engine.get_metrics().zone_stats
        self.assertGreater(zone_stats['🟢 calm']['transition_count'], 0)
        self.assertGreater(zone_stats['🟡 active']['transition_count'], 0)
        self.assertGreater(zone_stats['🔴 surge']['transition_count'], 0)
        
    def test_pressure_wave(self):
        """Test system response to pressure wave"""
        # Generate pressure wave
        for i in range(20):
            temp = 30 + 40 * (i % 2)  # Oscillate between 30 and 70
            burn = 0.3 + 0.4 * (i % 2)  # Oscillate between 0.3 and 0.7
            self.engine.update(temp, burn)
            time.sleep(0.1)
            
        # Check system stability
        metrics = self.engine.get_metrics()
        self.assertLess(metrics.avg_tick_duration, 0.1)  # Should maintain performance
        self.assertLess(metrics.memory_usage_mb, 100)  # Should not leak memory

def run_benchmark():
    """Run performance benchmark"""
    print("\n=== PulseEngine Benchmark ===")
    
    # Initialize engine
    engine = PulseEngine()
    engine.wire(None)
    
    # Benchmark parameters
    num_updates = 1000
    temps = [30 + i % 60 for i in range(num_updates)]  # Cycle through temperatures
    burns = [0.3 + (i % 7) * 0.1 for i in range(num_updates)]  # Vary burn rates
    
    # Run benchmark
    start_time = time.time()
    for temp, burn in zip(temps, burns):
        engine.update(temp, burn)
    end_time = time.time()
    
    # Calculate metrics
    total_time = end_time - start_time
    updates_per_second = num_updates / total_time
    avg_tick = statistics.mean(engine.tick_durations)
    
    # Print results
    print(f"\nBenchmark Results:")
    print(f"Total updates: {num_updates}")
    print(f"Total time: {total_time:.2f}s")
    print(f"Updates per second: {updates_per_second:.1f}")
    print(f"Average tick duration: {avg_tick*1000:.1f}ms")
    print(f"Memory usage: {engine.get_metrics().memory_usage_mb:.1f}MB")
    
    # Cleanup
    engine.shutdown()

if __name__ == '__main__':
    # Run unit tests
    unittest.main(verbosity=2)
    
    # Run benchmark
    run_benchmark() 