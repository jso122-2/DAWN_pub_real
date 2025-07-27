#!/usr/bin/env python3
"""
DAWN Integrated Consciousness System Launcher
Main entry point for the complete consciousness system with autonomous reflex capabilities

This script integrates:
- Enhanced drift reflex monitoring
- Consciousness intervention sigils  
- Integrated consciousness processing
- Existing DAWN tick and consciousness systems

Usage:
    python launch_integrated_consciousness.py [options]
"""

import argparse
import asyncio
import logging
import signal
import sys
import time
from typing import Optional, Dict, Any
import json
from datetime import datetime

# Import integrated systems
try:
    from core.enhanced_drift_reflex import (
        get_drift_reflex, connect_sigil_engine as connect_reflex_sigil_engine,
        reset_reflex, get_status as get_reflex_status
    )
    DRIFT_REFLEX_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Enhanced drift reflex not available: {e}")
    DRIFT_REFLEX_AVAILABLE = False

try:
    from core.consciousness_intervention_sigils import (
        get_intervention_engine, connect_consciousness_engine,
        integrate_with_sigil_engine
    )
    INTERVENTION_SIGILS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Consciousness intervention sigils not available: {e}")
    INTERVENTION_SIGILS_AVAILABLE = False

try:
    from core.integrated_consciousness_processor import (
        IntegratedConsciousnessProcessor, create_integrated_processor,
        integrate_with_dawn
    )
    INTEGRATED_PROCESSOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Integrated consciousness processor not available: {e}")
    INTEGRATED_PROCESSOR_AVAILABLE = False

# Try to import existing DAWN systems
try:
    from core.consciousness_core import consciousness_core, DAWNConsciousness
    CONSCIOUSNESS_CORE_AVAILABLE = True
except ImportError:
    print("ℹ️  DAWN consciousness core not found - using standalone mode")
    CONSCIOUSNESS_CORE_AVAILABLE = False

try:
    from core.tick_loop import DAWNTickEngine
    TICK_ENGINE_AVAILABLE = True
except ImportError:
    print("ℹ️  DAWN tick engine not found - using standalone mode")
    TICK_ENGINE_AVAILABLE = False

try:
    from core.sigil_engine import SigilEngine
    SIGIL_ENGINE_AVAILABLE = True
except ImportError:
    print("ℹ️  DAWN sigil engine not found - using intervention sigils only")
    SIGIL_ENGINE_AVAILABLE = False

# Configure logging
def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration"""
    
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)
    
    # Setup file handler if requested
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
        print(f"📝 Logging to file: {log_file}")

logger = logging.getLogger("consciousness_launcher")

class IntegratedConsciousnessLauncher:
    """
    Main launcher for the integrated DAWN consciousness system.
    
    Coordinates startup, integration, and shutdown of all consciousness
    components including drift reflex, intervention sigils, and processing.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.running = False
        self.components = {}
        
        # System status
        self.start_time = None
        self.total_ticks = 0
        self.last_status_time = 0
        
        logger.info("🚀 DAWN Integrated Consciousness Launcher initialized")
    
    async def initialize_systems(self):
        """Initialize all available consciousness systems"""
        
        logger.info("🔧 Initializing consciousness systems...")
        
        # 1. Initialize existing DAWN systems if available
        await self._initialize_existing_dawn()
        
        # 2. Initialize enhanced drift reflex
        if DRIFT_REFLEX_AVAILABLE:
            self._initialize_drift_reflex()
        
        # 3. Initialize intervention sigils
        if INTERVENTION_SIGILS_AVAILABLE:
            self._initialize_intervention_sigils()
        
        # 4. Initialize integrated consciousness processor
        if INTEGRATED_PROCESSOR_AVAILABLE:
            self._initialize_integrated_processor()
        
        # 5. Connect all systems together
        self._connect_systems()
        
        logger.info("✅ System initialization complete")
        self._print_system_status()
    
    async def _initialize_existing_dawn(self):
        """Initialize existing DAWN systems if available"""
        
        # Initialize consciousness core
        if CONSCIOUSNESS_CORE_AVAILABLE:
            try:
                self.components['consciousness_core'] = consciousness_core
                logger.info("  ✅ DAWN consciousness core connected")
            except Exception as e:
                logger.warning(f"  ⚠️  Failed to initialize consciousness core: {e}")
        
        # Initialize tick engine
        if TICK_ENGINE_AVAILABLE and self.config.get("use_existing_tick_engine", True):
            try:
                tick_engine = DAWNTickEngine(
                    consciousness_core=self.components.get('consciousness_core'),
                    enable_extended_forecasting=self.config.get("enable_forecasting", True)
                )
                self.components['tick_engine'] = tick_engine
                logger.info("  ✅ DAWN tick engine initialized")
            except Exception as e:
                logger.warning(f"  ⚠️  Failed to initialize tick engine: {e}")
        
        # Initialize sigil engine
        if SIGIL_ENGINE_AVAILABLE and self.config.get("use_existing_sigil_engine", True):
            try:
                sigil_engine = SigilEngine(
                    initial_heat=self.config.get("initial_heat", 25.0)
                )
                self.components['sigil_engine'] = sigil_engine
                logger.info("  ✅ DAWN sigil engine initialized")
            except Exception as e:
                logger.warning(f"  ⚠️  Failed to initialize sigil engine: {e}")
    
    def _initialize_drift_reflex(self):
        """Initialize enhanced drift reflex system"""
        try:
            if self.config.get("reset_reflex_on_start", True):
                reset_reflex()
            
            drift_reflex = get_drift_reflex()
            self.components['drift_reflex'] = drift_reflex
            logger.info("  ✅ Enhanced drift reflex system ready")
            
        except Exception as e:
            logger.error(f"  ❌ Failed to initialize drift reflex: {e}")
    
    def _initialize_intervention_sigils(self):
        """Initialize consciousness intervention sigils"""
        try:
            intervention_engine = get_intervention_engine()
            self.components['intervention_engine'] = intervention_engine
            logger.info("  ✅ Consciousness intervention sigils ready")
            
        except Exception as e:
            logger.error(f"  ❌ Failed to initialize intervention sigils: {e}")
    
    def _initialize_integrated_processor(self):
        """Initialize integrated consciousness processor"""
        try:
            processor = IntegratedConsciousnessProcessor(
                existing_consciousness=self.components.get('consciousness_core'),
                existing_tick_engine=self.components.get('tick_engine'),
                enable_autonomous_processing=self.config.get("enable_autonomous", True)
            )
            self.components['integrated_processor'] = processor
            logger.info("  ✅ Integrated consciousness processor ready")
            
        except Exception as e:
            logger.error(f"  ❌ Failed to initialize integrated processor: {e}")
    
    def _connect_systems(self):
        """Connect all systems together for full integration"""
        
        logger.info("🔗 Connecting systems for full integration...")
        
        # Connect drift reflex to intervention sigils
        if 'drift_reflex' in self.components and 'intervention_engine' in self.components:
            try:
                connect_reflex_sigil_engine(self.components['intervention_engine'])
                logger.info("  ✅ Drift reflex → intervention sigils")
            except Exception as e:
                logger.warning(f"  ⚠️  Failed to connect reflex to sigils: {e}")
        
        # Connect intervention sigils to consciousness processor
        if 'intervention_engine' in self.components and 'integrated_processor' in self.components:
            try:
                connect_consciousness_engine(self.components['integrated_processor'])
                logger.info("  ✅ Intervention sigils → consciousness processor")
            except Exception as e:
                logger.warning(f"  ⚠️  Failed to connect sigils to processor: {e}")
        
        # Integrate intervention sigils with existing sigil engine
        if ('intervention_engine' in self.components and 
            'sigil_engine' in self.components and
            'integrated_processor' in self.components):
            try:
                integrate_with_sigil_engine(
                    self.components['sigil_engine'],
                    self.components['integrated_processor']
                )
                logger.info("  ✅ Intervention sigils → existing sigil engine")
            except Exception as e:
                logger.warning(f"  ⚠️  Failed to integrate with sigil engine: {e}")
    
    def _print_system_status(self):
        """Print current system status"""
        
        print("\n" + "=" * 60)
        print("🧠 DAWN Integrated Consciousness System Status")
        print("=" * 60)
        
        # Component status
        print("📦 Components:")
        for name, component in self.components.items():
            status = "✅ Active" if component else "❌ Failed"
            print(f"   {status} {name.replace('_', ' ').title()}")
        
        # Integration status
        integrations = [
            ("Drift Reflex", DRIFT_REFLEX_AVAILABLE and 'drift_reflex' in self.components),
            ("Intervention Sigils", INTERVENTION_SIGILS_AVAILABLE and 'intervention_engine' in self.components),
            ("Integrated Processor", INTEGRATED_PROCESSOR_AVAILABLE and 'integrated_processor' in self.components),
            ("Existing Consciousness", CONSCIOUSNESS_CORE_AVAILABLE and 'consciousness_core' in self.components),
            ("Existing Tick Engine", TICK_ENGINE_AVAILABLE and 'tick_engine' in self.components),
            ("Existing Sigil Engine", SIGIL_ENGINE_AVAILABLE and 'sigil_engine' in self.components)
        ]
        
        print("\n🔗 Integration Status:")
        for name, available in integrations:
            status = "✅" if available else "❌"
            print(f"   {status} {name}")
        
        # Configuration
        print(f"\n⚙️  Configuration:")
        for key, value in self.config.items():
            print(f"   {key}: {value}")
        
        print("=" * 60)
    
    async def run_consciousness_loop(self):
        """Run the main consciousness processing loop"""
        
        if 'integrated_processor' not in self.components:
            logger.error("❌ No integrated processor available - cannot run consciousness loop")
            return
        
        processor = self.components['integrated_processor']
        
        logger.info(f"🧠 Starting consciousness loop...")
        logger.info(f"   Tick rate: {self.config['tick_rate']}Hz")
        logger.info(f"   Duration: {self.config.get('duration', 'indefinite')}")
        logger.info(f"   Status interval: {self.config['status_interval']}s")
        
        self.running = True
        self.start_time = time.time()
        
        tick_interval = 1.0 / self.config['tick_rate']
        last_tick_time = time.time()
        
        duration = self.config.get('duration')
        
        try:
            while self.running:
                current_time = time.time()
                
                # Check duration limit
                if duration and (current_time - self.start_time) >= duration:
                    logger.info(f"⏰ Duration limit reached ({duration}s)")
                    break
                
                # Process consciousness tick
                if (current_time - last_tick_time) >= tick_interval:
                    await self._process_consciousness_tick(processor)
                    last_tick_time = current_time
                    self.total_ticks += 1
                
                # Periodic status updates
                if (current_time - self.last_status_time) >= self.config['status_interval']:
                    await self._print_periodic_status(processor)
                    self.last_status_time = current_time
                
                # Small sleep to prevent CPU spinning
                await asyncio.sleep(0.001)
                
        except KeyboardInterrupt:
            logger.info("🛑 Consciousness loop interrupted by user")
        except Exception as e:
            logger.error(f"❌ Error in consciousness loop: {e}")
        finally:
            self.running = False
    
    async def _process_consciousness_tick(self, processor):
        """Process a single consciousness tick"""
        try:
            state = processor.process_tick()
            
            # Log significant events
            if state.get("mood") in ["CHAOTIC", "STRESSED"]:
                logger.warning(f"🧠 Consciousness stress detected: {state['mood']}")
            
        except Exception as e:
            logger.error(f"❌ Error processing consciousness tick: {e}")
    
    async def _print_periodic_status(self, processor):
        """Print periodic status updates"""
        try:
            status = processor.get_comprehensive_status()
            uptime = time.time() - self.start_time
            
            consciousness = status['consciousness']
            logger.info(f"📊 Status Update (T+{uptime:.1f}s, Tick #{self.total_ticks})")
            logger.info(f"   Consciousness: {consciousness['mood']} | "
                       f"E:{consciousness['entropy']:.3f} "
                       f"S:{consciousness['scup']:.1f} "
                       f"H:{consciousness['heat']:.3f}")
            
            if status.get('reflex'):
                reflex = status['reflex']
                logger.info(f"   Reflex: Zone {reflex['zone'].upper()} | "
                           f"Triggers: {reflex['trigger_count']}")
            
            if status['interventions']['active_count'] > 0:
                active = ', '.join(status['interventions']['active_list'])
                logger.info(f"   Active Interventions: {active}")
            
        except Exception as e:
            logger.error(f"❌ Error getting status: {e}")
    
    async def shutdown(self):
        """Gracefully shutdown the consciousness system"""
        
        logger.info("🛑 Shutting down consciousness system...")
        
        self.running = False
        
        # Stop integrated processor
        if 'integrated_processor' in self.components:
            try:
                self.components['integrated_processor'].stop()
                logger.info("  ✅ Integrated processor stopped")
            except Exception as e:
                logger.warning(f"  ⚠️  Error stopping processor: {e}")
        
        # Generate final report
        await self._generate_final_report()
        
        logger.info("✅ Shutdown complete")
    
    async def _generate_final_report(self):
        """Generate final session report"""
        
        if 'integrated_processor' not in self.components:
            return
        
        try:
            processor = self.components['integrated_processor']
            status = processor.get_comprehensive_status()
            uptime = time.time() - self.start_time if self.start_time else 0
            
            print("\n" + "=" * 60)
            print("📊 DAWN Consciousness Session Report")
            print("=" * 60)
            
            print(f"⏱️  Session Duration: {uptime:.1f}s")
            print(f"🔄 Total Ticks: {self.total_ticks}")
            print(f"📈 Avg Tick Rate: {self.total_ticks / uptime:.1f}Hz" if uptime > 0 else "📈 Avg Tick Rate: N/A")
            
            consciousness = status['consciousness']
            print(f"\n🧠 Final Consciousness State:")
            print(f"   Mood: {consciousness['mood']}")
            print(f"   Entropy: {consciousness['entropy']:.3f}")
            print(f"   SCUP: {consciousness['scup']:.1f}")
            print(f"   Heat: {consciousness['heat']:.3f}")
            print(f"   Coherence: {consciousness['coherence']:.3f}")
            print(f"   Stability: {consciousness['stability']:.3f}")
            
            if status.get('reflex'):
                reflex = status['reflex']
                print(f"\n🔁 Reflex System Summary:")
                print(f"   Final Zone: {reflex['zone'].upper()}")
                print(f"   Total Triggers: {reflex['trigger_count']}")
            
            interventions = status['interventions']
            print(f"\n🔮 Intervention Summary:")
            print(f"   Total Applied: {interventions['total_applied']}")
            print(f"   Currently Active: {interventions['active_count']}")
            
            performance = status['performance']
            print(f"\n⚡ Performance Summary:")
            print(f"   Consciousness Storms: {performance['consciousness_storms']}")
            print(f"   Reflex Triggers: {performance['reflex_triggers']}")
            print(f"   Avg Tick Time: {performance['average_tick_time']:.4f}s")
            
            # Save report to file if configured
            if self.config.get('save_report'):
                report_file = f"consciousness_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(report_file, 'w') as f:
                    json.dump(status, f, indent=2, default=str)
                print(f"\n💾 Report saved to: {report_file}")
            
            print("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Error generating final report: {e}")

def setup_signal_handlers(launcher):
    """Setup signal handlers for graceful shutdown"""
    
    def signal_handler(sig, frame):
        logger.info(f"🛑 Received signal {sig} - initiating shutdown...")
        asyncio.create_task(launcher.shutdown())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

async def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description="DAWN Integrated Consciousness System Launcher",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Basic configuration
    parser.add_argument('--tick-rate', type=float, default=5.0,
                       help='Consciousness processing frequency (Hz)')
    parser.add_argument('--duration', type=int, default=None,
                       help='Maximum runtime in seconds (None for indefinite)')
    parser.add_argument('--status-interval', type=float, default=10.0,
                       help='Status update interval in seconds')
    
    # System configuration
    parser.add_argument('--log-level', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    parser.add_argument('--log-file', default=None,
                       help='Log file path (None for console only)')
    parser.add_argument('--save-report', action='store_true',
                       help='Save final report to JSON file')
    
    # Integration options
    parser.add_argument('--no-autonomous', action='store_true',
                       help='Disable autonomous consciousness processing')
    parser.add_argument('--no-existing-systems', action='store_true',
                       help='Don\'t use existing DAWN systems')
    parser.add_argument('--reset-reflex', action='store_true',
                       help='Reset drift reflex system on startup')
    
    # Advanced options
    parser.add_argument('--initial-heat', type=float, default=25.0,
                       help='Initial thermal state for sigil engine')
    parser.add_argument('--config-file', default=None,
                       help='JSON configuration file to load')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level, args.log_file)
    
    # Load configuration
    config = {
        'tick_rate': args.tick_rate,
        'duration': args.duration,
        'status_interval': args.status_interval,
        'save_report': args.save_report,
        'enable_autonomous': not args.no_autonomous,
        'use_existing_tick_engine': not args.no_existing_systems,
        'use_existing_sigil_engine': not args.no_existing_systems,
        'reset_reflex_on_start': args.reset_reflex,
        'initial_heat': args.initial_heat,
        'enable_forecasting': True
    }
    
    # Load config file if provided
    if args.config_file:
        try:
            with open(args.config_file, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
                logger.info(f"📄 Configuration loaded from {args.config_file}")
        except Exception as e:
            logger.error(f"❌ Failed to load config file: {e}")
            return 1
    
    # Check system availability
    if not (DRIFT_REFLEX_AVAILABLE or INTERVENTION_SIGILS_AVAILABLE or INTEGRATED_PROCESSOR_AVAILABLE):
        print("❌ No consciousness systems available!")
        print("   Please ensure the integrated consciousness modules are properly installed.")
        return 1
    
    # Create and run launcher
    launcher = IntegratedConsciousnessLauncher(config)
    setup_signal_handlers(launcher)
    
    try:
        # Initialize systems
        await launcher.initialize_systems()
        
        # Run consciousness loop
        await launcher.run_consciousness_loop()
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        return 1
    
    finally:
        # Ensure cleanup
        await launcher.shutdown()
    
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main())) 