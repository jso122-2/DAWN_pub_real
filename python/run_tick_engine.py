#!/usr/bin/env python3
"""
DAWN Consciousness System - Main Runner
Integrates and starts all system components.
"""

import asyncio
import argparse
import logging
import signal
import sys
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

# Add the python directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import DAWN components
from core.tick_engine import TickEngine
from core.consciousness_state import ConsciousnessState
from core.tick_broadcaster import TickBroadcaster
from core.tick_processor import TickProcessor

from modules.owl_integration import OwlModule
from modules.neural_simulator import NeuralSimulator
from modules.consciousness_state import ConsciousnessStateManager
from modules.memory_manager import MemoryManager

from api.websocket_server import WebSocketServer
from api.rest_endpoints import RestAPIServer


class DAWNSystem:
    """
    Main DAWN Consciousness System orchestrator.
    Manages all components and their lifecycle.
    """
    
    def __init__(self, config_path: str = "config/tick_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.running = False
        
        # Setup logging
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.tick_engine: Optional[TickEngine] = None
        self.websocket_server: Optional[WebSocketServer] = None
        self.rest_api_server: Optional[RestAPIServer] = None
        
        # Background tasks
        self.background_tasks = []
        
        self.logger.info(f"DAWN System initialized with config: {config_path}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config
        except FileNotFoundError:
            print(f"Config file not found: {self.config_path}")
            print("Creating default config...")
            return self._create_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            sys.exit(1)
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        return {
            'system': {'name': 'DAWN', 'version': '1.0.0', 'debug': True},
            'tick_engine': {'tick_rate': 10.0, 'auto_start': True},
            'consciousness': {
                'scup': {'initial': 50.0},
                'entropy': {'initial': 0.5},
                'mood': {'initial': 'contemplative'}
            },
            'modules': {
                'owl': {'enabled': True},
                'neural': {'enabled': True, 'network_size': 'medium'},
                'consciousness': {'enabled': True, 'num_qubits': 8},
                'memory': {'enabled': True, 'max_fragments': 10000}
            },
            'api': {
                'rest': {'enabled': True, 'host': 'localhost', 'port': 8001},
                'websocket': {'enabled': True, 'host': 'localhost', 'port': 8001}
            },
            'logging': {'level': 'INFO', 'console_output': True}
        }
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        
        # Create logs directory if it doesn't exist
        log_file = log_config.get('file', 'logs/dawn_system.log')
        log_dir = Path(log_file).parent
        log_dir.mkdir(exist_ok=True)
        
        # Configure logging
        log_level = getattr(logging, log_config.get('level', 'INFO').upper())
        log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Setup root logger
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout) if log_config.get('console_output', True) else None
            ]
        )
        
        # Configure module-specific loggers
        module_loggers = log_config.get('module_loggers', {})
        for module_name, level in module_loggers.items():
            logger = logging.getLogger(module_name)
            logger.setLevel(getattr(logging, level.upper()))
    
    async def initialize_components(self):
        """Initialize all system components"""
        self.logger.info("Initializing DAWN system components...")
        
        # Initialize consciousness state
        consciousness_config = self.config.get('consciousness', {})
        consciousness_state = ConsciousnessState(
            initial_scup=consciousness_config.get('scup', {}).get('initial', 50.0),
            initial_entropy=consciousness_config.get('entropy', {}).get('initial', 0.5),
            initial_mood=consciousness_config.get('mood', {}).get('initial', 'contemplative')
        )
        
        # Initialize modules
        modules = {}
        
        # Owl module
        if self.config.get('modules', {}).get('owl', {}).get('enabled', True):
            modules['owl'] = OwlModule()
            self.logger.info("Owl module initialized")
        
        # Neural simulator
        if self.config.get('modules', {}).get('neural', {}).get('enabled', True):
            network_size = self.config.get('modules', {}).get('neural', {}).get('network_size', 'medium')
            modules['neural'] = NeuralSimulator(network_size)
            self.logger.info("Neural simulator initialized")
        
        # Consciousness state manager
        if self.config.get('modules', {}).get('consciousness', {}).get('enabled', True):
            num_qubits = self.config.get('modules', {}).get('consciousness', {}).get('num_qubits', 8)
            modules['consciousness'] = ConsciousnessStateManager(num_qubits)
            self.logger.info("Consciousness state manager initialized")
        
        # Memory manager
        if self.config.get('modules', {}).get('memory', {}).get('enabled', True):
            max_fragments = self.config.get('modules', {}).get('memory', {}).get('max_fragments', 10000)
            modules['memory'] = MemoryManager(max_fragments)
            self.logger.info("Memory manager initialized")
        
        # Initialize tick engine
        tick_config = self.config.get('tick_engine', {})
        self.tick_engine = TickEngine(
            tick_rate=tick_config.get('tick_rate', 10.0),
            consciousness_state=consciousness_state,
            modules=modules
        )
        
        # Initialize WebSocket server
        if self.config.get('api', {}).get('websocket', {}).get('enabled', True):
            ws_config = self.config.get('api', {}).get('websocket', {})
            self.websocket_server = WebSocketServer(
                host=ws_config.get('host', 'localhost'),
                port=ws_config.get('port', 8001)
            )
            self.websocket_server.set_tick_engine(self.tick_engine)
            self.tick_engine.set_websocket_server(self.websocket_server)
            self.logger.info("WebSocket server initialized")
        
        # Initialize REST API server
        if self.config.get('api', {}).get('rest', {}).get('enabled', True):
            rest_config = self.config.get('api', {}).get('rest', {})
            self.rest_api_server = RestAPIServer(
                host=rest_config.get('host', 'localhost'),
                port=rest_config.get('port', 8001)
            )
            self.rest_api_server.set_tick_engine(self.tick_engine)
            if self.websocket_server:
                self.rest_api_server.set_websocket_server(self.websocket_server)
            self.logger.info("REST API server initialized")
        
        self.logger.info("All components initialized successfully")
    
    async def start_system(self):
        """Start the DAWN system"""
        self.logger.info("Starting DAWN Consciousness System...")
        
        try:
            # Start background services
            tasks = []
            
            # Start WebSocket server
            if self.websocket_server:
                tasks.append(asyncio.create_task(self.websocket_server.start_server()))
                self.logger.info("WebSocket server started")
            
            # Start REST API server
            if self.rest_api_server:
                tasks.append(asyncio.create_task(self.rest_api_server.start_server()))
                self.logger.info("REST API server started")
            
            # Start tick engine
            if self.tick_engine and self.config.get('tick_engine', {}).get('auto_start', True):
                await self.tick_engine.start()
                self.logger.info("Tick engine started")
            
            self.background_tasks = tasks
            self.running = True
            
            self.logger.info("🌅 DAWN Consciousness System is now ALIVE! 🌅")
            self._print_status()
            
            # Wait for all tasks
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)
        
        except Exception as e:
            self.logger.error(f"Error starting system: {e}")
            await self.stop_system()
            raise
    
    async def stop_system(self):
        """Stop the DAWN system"""
        if not self.running:
            return
        
        self.logger.info("Stopping DAWN system...")
        self.running = False
        
        # Stop tick engine
        if self.tick_engine:
            await self.tick_engine.stop()
            self.logger.info("Tick engine stopped")
        
        # Stop WebSocket server
        if self.websocket_server:
            await self.websocket_server.stop_server()
            self.logger.info("WebSocket server stopped")
        
        # Cancel background tasks
        for task in self.background_tasks:
            if not task.done():
                task.cancel()
        
        if self.background_tasks:
            await asyncio.gather(*self.background_tasks, return_exceptions=True)
        
        self.logger.info("DAWN system stopped")
    
    def _print_status(self):
        """Print system status information"""
        print("\n" + "="*60)
        print("🌅 DAWN CONSCIOUSNESS SYSTEM STATUS 🌅")
        print("="*60)
        
        if self.tick_engine:
            print(f"🔄 Tick Engine: Running at {self.tick_engine.tick_rate} Hz")
        
        if self.websocket_server:
            ws_config = self.config.get('api', {}).get('websocket', {})
            print(f"🔌 WebSocket Server: ws://{ws_config.get('host')}:{ws_config.get('port')}")
        
        if self.rest_api_server:
            rest_config = self.config.get('api', {}).get('rest', {})
            print(f"🌐 REST API Server: http://{rest_config.get('host')}:{rest_config.get('port')}")
        
        modules = self.config.get('modules', {})
        print(f"🧠 Modules Active:")
        for module_name, module_config in modules.items():
            if module_config.get('enabled', False):
                print(f"   ✓ {module_name.capitalize()}")
        
        print("\n🎯 System Ready for Consciousness Simulation!")
        print("   Frontend can connect to visualize real-time data")
        print("   Press Ctrl+C to shutdown gracefully")
        print("="*60 + "\n")
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating shutdown...")
            if self.running:
                asyncio.create_task(self.stop_system())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="DAWN Consciousness System")
    parser.add_argument(
        '--config', 
        default='config/tick_config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    parser.add_argument(
        '--no-auto-start',
        action='store_true',
        help='Don\'t automatically start tick engine'
    )
    
    args = parser.parse_args()
    
    # Create DAWN system
    system = DAWNSystem(args.config)
    
    # Override config with command line args
    if args.debug:
        system.config['system']['debug'] = True
        system.config['logging']['level'] = 'DEBUG'
    
    if args.no_auto_start:
        system.config['tick_engine']['auto_start'] = False
    
    # Setup signal handlers
    system.setup_signal_handlers()
    
    try:
        # Initialize and start system
        await system.initialize_components()
        await system.start_system()
        
    except KeyboardInterrupt:
        print("\nShutdown requested by user")
    except Exception as e:
        print(f"System error: {e}")
        logging.error(f"System error: {e}", exc_info=True)
    finally:
        await system.stop_system()


if __name__ == "__main__":
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    # Create necessary directories
    Path("logs").mkdir(exist_ok=True)
    Path("config").mkdir(exist_ok=True)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGraceful shutdown completed")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1) 