"""
KAN-Cairrn Main Integration Script

This script initializes and orchestrates the complete KAN-Cairrn system,
integrating all components for interpretable function space navigation.
"""

import asyncio
import logging
import numpy as np
import networkx as nx
from typing import Dict, List, Any, Optional
from datetime import datetime
import uvicorn
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all KAN-Cairrn components
from models import (
    KANTopology, SplineNeuron, CursorState, FunctionPath, 
    KANConfig, CairrConfig
)
from core.spline_neurons import SplineNeuronManager, LearnableSplineFunction
from cursor.function_navigator import FunctionNavigator
from cursor.interpretability import SplineInterpreter
from adapters.claude_kan import ClaudeKANAdapter
from interfaces.spline_api import spline_api


class KANCairrSystem:
    """Main KAN-Cairrn system orchestrator"""
    
    def __init__(self, kan_config: KANConfig = None, cairr_config: CairrConfig = None):
        self.kan_config = kan_config or KANConfig()
        self.cairr_config = cairr_config or CairrConfig()
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Core components
        self.neuron_manager: Optional[SplineNeuronManager] = None
        self.kan_topology: Optional[KANTopology] = None
        self.function_navigator: Optional[FunctionNavigator] = None
        self.spline_interpreter: Optional[SplineInterpreter] = None
        self.claude_adapter: Optional[ClaudeKANAdapter] = None
        
        # System state
        self.is_initialized = False
        self.startup_time: Optional[datetime] = None
        
        self.logger.info("KAN-Cairrn system created with interpretable function space navigation")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/kan_cairrn.log'),
                logging.StreamHandler()
            ]
        )
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        return logging.getLogger(__name__)
    
    async def initialize(self):
        """Initialize all system components"""
        try:
            self.startup_time = datetime.now()
            self.logger.info("🚀 Initializing KAN-Cairrn system...")
            
            # Step 1: Initialize neuron manager
            self.logger.info("📡 Initializing spline neuron manager...")
            self.neuron_manager = SplineNeuronManager(
                feature_dim=self.cairr_config.feature_vector_dim
            )
            
            # Step 2: Create KAN topology
            self.logger.info("🕸️ Building KAN topology...")
            self.kan_topology = await self._create_kan_topology()
            
            # Step 3: Initialize function navigator
            self.logger.info("🧭 Initializing function navigator...")
            self.function_navigator = FunctionNavigator(self.kan_topology)
            
            # Step 4: Initialize spline interpreter
            self.logger.info("🔍 Initializing spline interpreter...")
            self.spline_interpreter = SplineInterpreter()
            
            # Step 5: Initialize Claude adapter
            self.logger.info("🤖 Initializing Claude-KAN adapter...")
            self.claude_adapter = ClaudeKANAdapter(
                self.kan_topology, 
                self.function_navigator
            )
            
            # Step 6: Create initial spline neurons
            self.logger.info("⚡ Creating initial spline neurons...")
            await self._create_initial_neurons()
            
            # Step 7: Initialize API components
            self.logger.info("🌐 Setting up API components...")
            spline_api.set_components(
                self.kan_topology,
                self.function_navigator,
                self.claude_adapter
            )
            
            self.is_initialized = True
            init_time = (datetime.now() - self.startup_time).total_seconds()
            
            self.logger.info(f"✅ KAN-Cairrn system initialized successfully in {init_time:.2f}s")
            self.logger.info(f"📊 System stats: {await self._get_initialization_stats()}")
            
        except Exception as e:
            self.logger.error(f"❌ KAN-Cairrn initialization failed: {e}")
            raise
    
    async def _create_kan_topology(self) -> KANTopology:
        """Create the KAN network topology"""
        
        # Initialize empty topology
        spline_neurons = {}
        connection_graph = nx.DiGraph()
        
        # Create thread routing matrix (placeholder)
        matrix_size = sum(self.kan_config.neurons_per_layer)
        thread_routing_matrix = np.random.normal(0, 0.1, (matrix_size, matrix_size))
        
        topology = KANTopology(
            spline_neurons=spline_neurons,
            connection_graph=connection_graph,
            thread_routing_matrix=thread_routing_matrix,
            global_entropy=0.5,
            entropy_threshold=self.kan_config.sparse_threshold
        )
        
        return topology
    
    async def _create_initial_neurons(self):
        """Create initial set of spline neurons"""
        
        # Define some example assemblages for testing
        initial_assemblages = [
            {
                "id": "desire_ritual_001",
                "features": ["desire", "ritual", "intensity"],
                "threshold": 0.2
            },
            {
                "id": "grief_sigil_001", 
                "features": ["grief", "sigil", "transformation"],
                "threshold": 0.3
            },
            {
                "id": "identity_mask_001",
                "features": ["identity", "mask", "performance"],
                "threshold": 0.25
            },
            {
                "id": "memory_fragment_001",
                "features": ["memory", "fragment", "nostalgia"],
                "threshold": 0.15
            },
            {
                "id": "quantum_assemblage_001",
                "features": ["quantum", "superposition", "collapse"],
                "threshold": 0.4
            }
        ]
        
        for assemblage in initial_assemblages:
            neuron = self.neuron_manager.create_neuron(
                assemblage_id=assemblage["id"],
                input_features=assemblage["features"],
                activation_threshold=assemblage["threshold"]
            )
            
            # Add to topology
            self.kan_topology.spline_neurons[assemblage["id"]] = neuron
            
            # Add node to connection graph
            self.kan_topology.connection_graph.add_node(assemblage["id"])
        
        # Create some connections between neurons
        neuron_ids = list(self.kan_topology.spline_neurons.keys())
        for i, neuron_id_1 in enumerate(neuron_ids):
            for j, neuron_id_2 in enumerate(neuron_ids[i+1:], i+1):
                # Random connections with 30% probability
                if np.random.random() < 0.3:
                    weight = np.random.uniform(0.1, 0.8)
                    self.kan_topology.connection_graph.add_edge(
                        neuron_id_1, neuron_id_2, weight=weight
                    )
        
        # Update global entropy
        self.kan_topology.update_global_entropy()
        
        self.logger.info(f"Created {len(initial_assemblages)} initial spline neurons")
    
    async def _get_initialization_stats(self) -> Dict[str, Any]:
        """Get system statistics after initialization"""
        
        stats = {
            "initialization_time": (datetime.now() - self.startup_time).total_seconds(),
            "total_neurons": len(self.kan_topology.spline_neurons),
            "total_connections": self.kan_topology.connection_graph.number_of_edges(),
            "global_entropy": self.kan_topology.global_entropy,
            "feature_dimension": self.cairr_config.feature_vector_dim,
            "kan_layers": self.kan_config.num_layers,
            "spline_order": self.kan_config.spline_order
        }
        
        return stats
    
    async def demonstrate_system(self):
        """Run a demonstration of the KAN-Cairrn system"""
        
        if not self.is_initialized:
            await self.initialize()
        
        self.logger.info("🎭 Starting KAN-Cairrn system demonstration...")
        
        try:
            # Demo 1: Spline neuron activation
            self.logger.info("Demo 1: Activating spline neurons...")
            demo_vector = np.random.normal(0, 1, self.cairr_config.feature_vector_dim)
            
            for neuron_id, neuron in self.kan_topology.spline_neurons.items():
                glyph = self.neuron_manager.activate_neuron(neuron_id, demo_vector)
                if glyph:
                    self.logger.info(f"  ✨ {neuron_id}: {glyph.interpretable_explanation}")
            
            # Demo 2: Function navigation
            self.logger.info("Demo 2: Navigating through function space...")
            target_semantics = {
                "desire": 0.8,
                "ritual": 0.6,
                "transformation": 0.9
            }
            
            nav_result = await self.function_navigator.navigate_to_function(target_semantics)
            self.logger.info(f"  🧭 Navigation: {nav_result.interpretation_summary}")
            
            # Demo 3: Claude integration simulation
            self.logger.info("Demo 3: Claude-KAN integration simulation...")
            test_prompt = "Explain the concept of fluid identity through ritualistic transformation"
            
            # This would normally call Claude API
            suggestions = await self.claude_adapter.get_contextual_suggestions(test_prompt)
            self.logger.info(f"  🤖 Suggestions: {suggestions}")
            
            # Demo 4: System visualization data
            self.logger.info("Demo 4: Generating visualization data...")
            viz_data = self.claude_adapter.get_kan_visualization_data()
            self.logger.info(f"  📊 Visualization: {viz_data['activity_level']} activity level")
            
            self.logger.info("✅ Demonstration completed successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Demonstration failed: {e}")
            raise
    
    async def run_api_server(self, host: str = "127.0.0.1", port: int = 8000):
        """Run the KAN-Cairrn API server"""
        
        if not self.is_initialized:
            await self.initialize()
        
        self.logger.info(f"🌐 Starting KAN-Cairrn API server on {host}:{port}")
        
        config = uvicorn.Config(
            app=spline_api.app,
            host=host,
            port=port,
            log_level="info"
        )
        
        server = uvicorn.Server(config)
        await server.serve()
    
    async def shutdown(self):
        """Graceful system shutdown"""
        self.logger.info("🛑 Shutting down KAN-Cairrn system...")
        
        # Save current state if needed
        if self.kan_topology:
            self.kan_topology.last_updated = datetime.now()
        
        # Cleanup resources
        self.is_initialized = False
        
        self.logger.info("✅ KAN-Cairrn system shutdown complete")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        
        status = {
            "initialized": self.is_initialized,
            "startup_time": self.startup_time.isoformat() if self.startup_time else None,
            "uptime_seconds": (datetime.now() - self.startup_time).total_seconds() if self.startup_time else 0,
            "components": {
                "neuron_manager": bool(self.neuron_manager),
                "kan_topology": bool(self.kan_topology),
                "function_navigator": bool(self.function_navigator),
                "spline_interpreter": bool(self.spline_interpreter),
                "claude_adapter": bool(self.claude_adapter)
            }
        }
        
        if self.kan_topology:
            status["topology_stats"] = {
                "total_neurons": len(self.kan_topology.spline_neurons),
                "global_entropy": self.kan_topology.global_entropy,
                "last_updated": self.kan_topology.last_updated.isoformat()
            }
        
        return status


# Main execution functions
async def main():
    """Main entry point for KAN-Cairrn system"""
    
    # Create system with default configuration
    system = KANCairrSystem()
    
    try:
        # Initialize the system
        await system.initialize()
        
        # Run demonstration
        await system.demonstrate_system()
        
        # Start API server
        await system.run_api_server()
        
    except KeyboardInterrupt:
        print("\n🛑 Received shutdown signal")
    except Exception as e:
        print(f"❌ System error: {e}")
    finally:
        await system.shutdown()


def run_system():
    """Synchronous wrapper for running the system"""
    asyncio.run(main())


def run_demo_only():
    """Run only the system demonstration"""
    async def demo():
        system = KANCairrSystem()
        await system.initialize()
        await system.demonstrate_system()
        await system.shutdown()
    
    asyncio.run(demo())


def run_api_only(host: str = "127.0.0.1", port: int = 8000):
    """Run only the API server"""
    async def api():
        system = KANCairrSystem()
        await system.initialize()
        await system.run_api_server(host, port)
    
    asyncio.run(api())


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="KAN-Cairrn System")
    parser.add_argument("--mode", choices=["full", "demo", "api"], default="full",
                       help="Run mode: full system, demo only, or API only")
    parser.add_argument("--host", default="127.0.0.1", help="API server host")
    parser.add_argument("--port", type=int, default=8000, help="API server port")
    
    args = parser.parse_args()
    
    print("🧠 KAN-Cairrn: Interpretable Function Space Navigation System")
    print("=" * 60)
    
    if args.mode == "demo":
        run_demo_only()
    elif args.mode == "api":
        run_api_only(args.host, args.port)
    else:
        run_system() 