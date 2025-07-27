#!/usr/bin/env python3
"""
DAWN Integration Orchestrator - Tick Loop + Cognition Runtime Integration
=========================================================================

This script demonstrates how to integrate the new CognitionRuntime with 
the existing tick loop system to create a fully orchestrated meta-cognitive 
consciousness system.

Usage:
    python integration_orchestrator.py --mode live    # Connect to live tick loop
    python integration_orchestrator.py --mode demo    # Run demonstration mode
    python integration_orchestrator.py --mode test    # Run test scenarios
"""

import os
import sys
import asyncio
import argparse
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Add DAWN paths
sys.path.append(os.path.dirname(__file__))

# Import DAWN components
try:
    from backend.cognitive.cognition_runtime import CognitionRuntime, get_cognition_runtime
    from core.tick.tick_loop import TickLoop
    from core.tick.tick_engine import TickEngine
    INTEGRATION_READY = True
except ImportError as e:
    print(f"⚠️ Integration components not available: {e}")
    INTEGRATION_READY = False

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("integration_orchestrator")

class DAWNOrchestrator:
    """
    Master orchestrator that coordinates the tick loop with the cognition runtime
    to create a fully integrated meta-cognitive consciousness system.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the orchestrator with configuration"""
        self.config = config or {}
        
        # Initialize core systems
        self.tick_engine = None
        self.tick_loop = None
        self.cognition_runtime = None
        
        # State tracking
        self.running = False
        self.tick_count = 0
        self.integration_errors = 0
        self.start_time = None
        
        # Performance metrics
        self.avg_processing_time = 0.0
        self.tick_performance = []
        
        logger.info("🧠 DAWN Orchestrator initialized")
    
    async def initialize(self):
        """Initialize all core systems"""
        try:
            if not INTEGRATION_READY:
                raise RuntimeError("Integration components not available")
            
            # Initialize cognition runtime first
            self.cognition_runtime = get_cognition_runtime(self.config)
            
            # Initialize tick engine with our cognition hook
            tick_config = self.config.get('tick', {
                'tick_rate': 1.0,
                'enable_metrics': True
            })
            
            # This would connect to existing tick system - for demo we'll create basic one
            logger.info("🔄 Initializing tick systems...")
            
            # Register cognition runtime as tick handler
            await self._setup_tick_integration()
            
            logger.info("✅ All systems initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize orchestrator: {e}")
            raise
    
    async def _setup_tick_integration(self):
        """Setup integration between tick system and cognition runtime"""
        # This creates the bridge between existing tick loop and new cognition runtime
        
        # Mock tick integration for demonstration
        logger.info("🔗 Setting up tick-cognition integration bridge")
        
        # In a real implementation, this would:
        # 1. Hook into existing TickLoop's tick callback system
        # 2. Register cognition_runtime.process_tick as a handler
        # 3. Ensure proper state data flow between systems
        
        self.tick_integration_ready = True
    
    async def start(self):
        """Start the orchestrated consciousness system"""
        if not INTEGRATION_READY:
            logger.error("Cannot start - integration components missing")
            return
        
        self.running = True
        self.start_time = datetime.now()
        
        logger.info("🚀 Starting DAWN Orchestrated Consciousness System")
        logger.info("   - Tick Loop: Active")
        logger.info("   - Cognition Runtime: Active") 
        logger.info("   - Memory Networks: Active")
        logger.info("   - Tracer Stack: Active")
        logger.info("   - Symbolic Processing: Active")
        
        try:
            # Start the main orchestration loop
            await self._orchestration_loop()
            
        except KeyboardInterrupt:
            logger.info("Shutdown requested by user")
        except Exception as e:
            logger.error(f"Orchestration error: {e}")
        finally:
            await self.shutdown()
    
    async def _orchestration_loop(self):
        """Main orchestration loop integrating all systems"""
        
        while self.running:
            tick_start = datetime.now()
            
            try:
                # 1. GENERATE TICK DATA (normally from TickEngine)
                tick_data = self._generate_mock_tick_data()
                
                # 2. PROCESS THROUGH COGNITION RUNTIME
                cognition_result = await self.cognition_runtime.process_tick(tick_data)
                
                # 3. HANDLE ALERTS AND EVENTS
                await self._handle_cognition_results(cognition_result)
                
                # 4. UPDATE PERFORMANCE METRICS
                self._update_performance_metrics(tick_start)
                
                # 5. LOG ORCHESTRATION STATUS
                await self._log_orchestration_status(cognition_result)
                
                self.tick_count += 1
                
                # Maintain tick rate
                await asyncio.sleep(1.0)  # 1 Hz default
                
            except Exception as e:
                self.integration_errors += 1
                logger.error(f"Orchestration tick error: {e}")
                
                if self.integration_errors > 10:
                    logger.critical("Too many integration errors - shutting down")
                    break
    
    def _generate_mock_tick_data(self) -> Dict[str, Any]:
        """Generate mock tick data for demonstration"""
        import random
        import math
        
        # Simulate realistic consciousness data patterns
        time_factor = self.tick_count * 0.1
        
        # Add some realistic variability
        entropy_base = 0.5 + 0.3 * math.sin(time_factor)
        heat_base = 0.4 + 0.2 * math.cos(time_factor * 0.7)
        scup_base = 0.7 + 0.2 * math.sin(time_factor * 0.5)
        
        # Add noise
        entropy = max(0.0, min(1.0, entropy_base + random.uniform(-0.1, 0.1)))
        heat = max(0.0, min(1.0, heat_base + random.uniform(-0.05, 0.05)))
        scup = max(0.0, min(1.0, scup_base + random.uniform(-0.1, 0.1)))
        
        return {
            'tick_id': self.tick_count,
            'timestamp': datetime.now().timestamp(),
            'entropy': entropy,
            'heat': heat,
            'scup': scup,
            'zone': 'surge' if heat > 0.7 else 'active' if entropy > 0.6 else 'calm',
            'pulse_activity': random.uniform(0.3, 0.8),
            'memory_load': random.uniform(0.2, 0.7),
            'cooling_rate': max(0.0, 0.5 - heat * 0.3)
        }
    
    async def _handle_cognition_results(self, cognition_result: Dict[str, Any]):
        """Handle results from cognition runtime"""
        
        # Handle tracer alerts
        alerts = cognition_result.get('tracer_alerts', [])
        if alerts:
            for alert in alerts:
                severity_icon = "🚨" if alert.severity == 'critical' else "⚠️"
                logger.info(f"{severity_icon} {alert.tracer_type.upper()}: {alert.message}")
        
        # Handle memory network updates
        memory_updates = cognition_result.get('memory_updates', {})
        if memory_updates:
            for update_type, data in memory_updates.items():
                logger.info(f"🌿 Memory Network: {update_type} - {data}")
        
        # Handle symbolic events
        symbolic_events = cognition_result.get('symbolic_events', [])
        if symbolic_events:
            for event in symbolic_events:
                logger.info(f"🧿 Symbolic Event: {event['type']} detected")
        
        # Handle forecast adjustments
        forecast_adjustments = cognition_result.get('forecast_adjustments', [])
        if forecast_adjustments:
            for adjustment in forecast_adjustments:
                logger.info(f"🔮 Forecast Adjustment: {adjustment['type']} - {adjustment['reason']}")
    
    def _update_performance_metrics(self, tick_start: datetime):
        """Update orchestration performance metrics"""
        processing_time = (datetime.now() - tick_start).total_seconds()
        
        self.tick_performance.append(processing_time)
        if len(self.tick_performance) > 100:
            self.tick_performance = self.tick_performance[-50:]
        
        self.avg_processing_time = sum(self.tick_performance) / len(self.tick_performance)
    
    async def _log_orchestration_status(self, cognition_result: Dict[str, Any]):
        """Log periodic orchestration status"""
        if self.tick_count % 10 == 0:  # Every 10 ticks
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            status = {
                'tick_count': self.tick_count,
                'uptime': f"{uptime:.1f}s",
                'avg_processing_time': f"{self.avg_processing_time*1000:.1f}ms",
                'integration_errors': self.integration_errors,
                'alerts_processed': len(cognition_result.get('tracer_alerts', [])),
                'cognition_status': self.cognition_runtime.get_status() if self.cognition_runtime else {}
            }
            
            logger.info(f"📊 Orchestration Status: Tick {self.tick_count}, "
                       f"Uptime {status['uptime']}, "
                       f"Avg Processing {status['avg_processing_time']}, "
                       f"Errors {status['integration_errors']}")
    
    async def run_demo_scenario(self, scenario_name: str = "default"):
        """Run a specific demonstration scenario"""
        logger.info(f"🎭 Running demo scenario: {scenario_name}")
        
        scenarios = {
            'default': self._demo_normal_operation,
            'stress_test': self._demo_stress_conditions,
            'drift_cascade': self._demo_drift_cascade,
            'thermal_emergency': self._demo_thermal_emergency,
            'memory_overload': self._demo_memory_overload
        }
        
        demo_func = scenarios.get(scenario_name, self._demo_normal_operation)
        await demo_func()
    
    async def _demo_normal_operation(self):
        """Demonstrate normal orchestrated operation"""
        logger.info("Running normal operation demo for 20 ticks...")
        
        for i in range(20):
            tick_data = self._generate_mock_tick_data()
            cognition_result = await self.cognition_runtime.process_tick(tick_data)
            await self._handle_cognition_results(cognition_result)
            
            print(f"Tick {i+1}: {len(cognition_result.get('tracer_alerts', []))} alerts, "
                  f"{len(cognition_result.get('memory_updates', {}))} memory updates")
            
            await asyncio.sleep(0.5)
    
    async def _demo_stress_conditions(self):
        """Demonstrate stress condition handling"""
        logger.info("Simulating stress conditions...")
        
        for i in range(15):
            # Force high entropy and heat
            tick_data = {
                'tick_id': i,
                'timestamp': datetime.now().timestamp(),
                'entropy': 0.8 + (i * 0.02),  # Rising entropy
                'heat': 0.7 + (i * 0.03),     # Rising heat  
                'scup': 0.6 - (i * 0.02),     # Falling coherence
                'zone': 'critical',
                'pulse_activity': 0.9,
                'memory_load': 0.8,
                'cooling_rate': 0.1
            }
            
            cognition_result = await self.cognition_runtime.process_tick(tick_data)
            await self._handle_cognition_results(cognition_result)
            
            await asyncio.sleep(0.3)
    
    async def _demo_drift_cascade(self):
        """Demonstrate drift cascade detection"""
        logger.info("Simulating drift cascade scenario...")
        
        for i in range(12):
            # Simulate drift cascade
            drift_factor = i * 0.08
            tick_data = {
                'tick_id': i,
                'timestamp': datetime.now().timestamp(),
                'entropy': 0.5 + drift_factor,
                'heat': 0.4 + (drift_factor * 0.5),
                'scup': 0.7 - drift_factor,
                'zone': 'drift',
                'pulse_activity': 0.6,
                'memory_load': 0.5 + drift_factor,
                'cooling_rate': 0.2
            }
            
            cognition_result = await self.cognition_runtime.process_tick(tick_data)
            await self._handle_cognition_results(cognition_result)
            
            await asyncio.sleep(0.4)
    
    async def _demo_thermal_emergency(self):
        """Demonstrate thermal emergency handling"""
        logger.info("Simulating thermal emergency...")
        
        for i in range(10):
            # Simulate thermal spike
            tick_data = {
                'tick_id': i,
                'timestamp': datetime.now().timestamp(),
                'entropy': 0.6,
                'heat': 0.95 if i > 3 else 0.5 + (i * 0.1),  # Sudden spike
                'scup': 0.5,
                'zone': 'emergency' if i > 3 else 'active',
                'pulse_activity': 0.9,
                'memory_load': 0.7,
                'cooling_rate': 0.3 if i > 5 else 0.1  # Emergency cooling kicks in
            }
            
            cognition_result = await self.cognition_runtime.process_tick(tick_data)
            await self._handle_cognition_results(cognition_result)
            
            await asyncio.sleep(0.5)
    
    async def _demo_memory_overload(self):
        """Demonstrate memory network handling"""
        logger.info("Simulating memory network stress...")
        
        for i in range(8):
            tick_data = {
                'tick_id': i,
                'timestamp': datetime.now().timestamp(),
                'entropy': 0.5,
                'heat': 0.4,
                'scup': 0.7,
                'zone': 'active',
                'pulse_activity': 0.7,
                'memory_load': 0.3 + (i * 0.1),  # Rising memory load
                'cooling_rate': 0.3
            }
            
            cognition_result = await self.cognition_runtime.process_tick(tick_data)
            await self._handle_cognition_results(cognition_result)
            
            await asyncio.sleep(0.6)
    
    def get_orchestration_status(self) -> Dict[str, Any]:
        """Get comprehensive orchestration status"""
        status = {
            'running': self.running,
            'tick_count': self.tick_count,
            'integration_errors': self.integration_errors,
            'avg_processing_time': self.avg_processing_time,
            'uptime': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            'cognition_runtime_status': self.cognition_runtime.get_status() if self.cognition_runtime else {}
        }
        
        return status
    
    async def shutdown(self):
        """Shutdown the orchestrator gracefully"""
        logger.info("🛑 Shutting down DAWN Orchestrator...")
        
        self.running = False
        
        if self.cognition_runtime:
            await self.cognition_runtime.shutdown()
        
        # Final status report
        if self.start_time:
            uptime = (datetime.now() - self.start_time).total_seconds()
            logger.info(f"📊 Final Stats: {self.tick_count} ticks processed, "
                       f"{uptime:.1f}s uptime, "
                       f"{self.integration_errors} errors")
        
        logger.info("✅ DAWN Orchestrator shutdown complete")


async def main():
    """Main entry point for the orchestrator"""
    parser = argparse.ArgumentParser(description='DAWN Integration Orchestrator')
    parser.add_argument('--mode', choices=['live', 'demo', 'test'], default='demo',
                       help='Orchestrator mode')
    parser.add_argument('--scenario', default='default',
                       help='Demo scenario to run')
    parser.add_argument('--duration', type=int, default=60,
                       help='Duration in seconds for live mode')
    
    args = parser.parse_args()
    
    print("🧠 DAWN Integration Orchestrator")
    print("=" * 50)
    print(f"Mode: {args.mode}")
    
    orchestrator = DAWNOrchestrator()
    
    try:
        await orchestrator.initialize()
        
        if args.mode == 'demo':
            await orchestrator.run_demo_scenario(args.scenario)
        elif args.mode == 'test':
            # Run all demo scenarios
            scenarios = ['default', 'stress_test', 'drift_cascade', 'thermal_emergency', 'memory_overload']
            for scenario in scenarios:
                print(f"\n--- Testing {scenario} ---")
                await orchestrator.run_demo_scenario(scenario)
                await asyncio.sleep(1)
        elif args.mode == 'live':
            # This would connect to live DAWN tick system
            logger.info(f"Running live mode for {args.duration} seconds...")
            await asyncio.wait_for(orchestrator.start(), timeout=args.duration)
        
    except Exception as e:
        logger.error(f"Orchestrator failed: {e}")
    finally:
        await orchestrator.shutdown()


if __name__ == "__main__":
    asyncio.run(main()) 