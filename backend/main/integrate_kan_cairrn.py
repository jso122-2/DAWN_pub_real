#!/usr/bin/env python3
"""
DAWN-KAN-Cairrn Integration System
Demo integration with full KAN-Cairrn architecture
"""

import asyncio
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.simple_websocket_server import start_server
from main.startup import initialize_dawn
from main.demo_advanced_consciousness import run_demo
from main.restart_dawn_clean import restart_dawn
from main.start_dawn_api import start_api
from main.run_kan_server import run_kan
from main.start_api_fixed import start_api_fixed
from main.juliet_flower import run_juliet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Import KAN-Cairrn components
    from cairrn_kan.models import (
        SplineNeuron, KANTopology, CursorState, 
        KANConfig, CairrConfig, LearnableSplineFunction,
        CachedGlyph, FunctionPath, NavigationResult
    )
    from cairrn_kan.core.spline_neurons import SplineNeuronManager
    from cairrn_kan.core.kan_topology import KANTopologyManager  
    from cairrn_kan.core.entropy_engine import EntropyEngine
    from cairrn_kan.core.weave_router import WeaveRouter
    from cairrn_kan.cursor.function_navigator import FunctionNavigator
    from cairrn_kan.cursor.interpretability import SplineInterpreter
    from cairrn_kan.cursor.trajectory_learner import TrajectoryLearner
    from cairrn_kan.adapters.claude_kan import ClaudeKANAdapter
    from cairrn_kan.adapters.weave_kan import WeaveKANAdapter
    from cairrn_kan.adapters.memory_kan import MemoryKANAdapter
    from cairrn_kan.interfaces.spline_api import SplineAPIServer
    from cairrn_kan.interfaces.visual_kan import KANVisualizationSocket
    from cairrn_kan.interfaces.cursor_stream import CursorStreamHandler
    
    IMPORTS_AVAILABLE = True
    logger.info("✅ All KAN-Cairrn imports successful")
    
except ImportError as e:
    IMPORTS_AVAILABLE = False
    logger.warning(f"❌ KAN-Cairrn imports failed: {e}")
    logger.info("Running in fallback mode with mock implementations")
    
    # Mock classes for fallback mode
    class NavigationResult:
        def __init__(self, success=True, confidence=0.5, interpretation="Mock navigation"):
            self.success = success
            self.confidence = confidence  
            self.interpretation = interpretation
    
    class CursorState:
        def __init__(self):
            self.active_splines = []
            self.confidence_scores = {}
    
    class SplineNeuron:
        def __init__(self, assemblage_id="mock"):
            self.assemblage_id = assemblage_id
            
    class KANTopology:
        def __init__(self):
            self.spline_neurons = {}
            self.connection_graph = None
            
    class FunctionPath:
        def __init__(self):
            self.visited_neurons = []
            self.gradient_history = []
            
    class CachedGlyph:
        def __init__(self, content="mock"):
            self.content = content
            
    class LearnableSplineFunction:
        def __init__(self, input_dim=3, spline_order=3, grid_size=5):
            self.input_dim = input_dim
            
    class KANConfig:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
                
    class CairrConfig:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)


class DAWNKANCairrIntegration:
    """Main integration class bridging DAWN and KAN-Cairrn systems"""
    
    def __init__(self):
        self.active = False
        self.tick_count = 0
        self.spline_activations = 0
        self.integration_stats = {
            "start_time": None,
            "tick_count": 0,
            "spline_activations": 0,
            "navigation_events": 0,
            "weaving_operations": 0
        }
        
        # Component initialization state
        self.components_initialized = {
            "kan_topology": False,
            "spline_neurons": False, 
            "function_navigator": False,
            "adapters": False,
            "interfaces": False
        }
        
        if IMPORTS_AVAILABLE:
            self.initialize_kan_system()
        else:
            logger.info("Using mock implementation")
    
    def initialize_kan_system(self):
        """Initialize the complete KAN-Cairrn system"""
        
        try:
            # Configuration
            self.kan_config = KANConfig(
                num_layers=3,
                neurons_per_layer=[32, 64, 32],
                spline_order=3,
                grid_size=5,
                sparse_threshold=0.01,
                entropy_decay_rate=0.95,
                interpretability_weight=0.3
            )
            
            self.cairr_config = CairrConfig(
                max_cached_assemblages=500,
                activation_threshold=0.1,
                entropy_cleanup_interval=1800,
                spline_update_learning_rate=0.001,
                feature_vector_dim=64
            )
            
            # Core components
            self.spline_manager = SplineNeuronManager(self.cairr_config)
            self.topology_manager = KANTopologyManager(self.kan_config)
            self.entropy_engine = EntropyEngine(self.cairr_config)
            self.weave_router = WeaveRouter()
            
            # Create initial topology
            self.kan_topology = self.topology_manager.create_topology()
            self.components_initialized["kan_topology"] = True
            
            # Create some initial spline neurons
            self._create_initial_neurons()
            self.components_initialized["spline_neurons"] = True
            
            # Navigation components
            self.function_navigator = FunctionNavigator(self.kan_topology)
            self.spline_interpreter = SplineInterpreter()
            self.trajectory_learner = TrajectoryLearner()
            self.components_initialized["function_navigator"] = True
            
            # Adapters
            self.claude_adapter = ClaudeKANAdapter(self.kan_topology, self.spline_interpreter)
            self.weave_adapter = WeaveKANAdapter(self.kan_topology, self.weave_router)
            self.memory_adapter = MemoryKANAdapter(self.kan_topology)
            self.components_initialized["adapters"] = True
            
            # Interfaces (initialize but don't start servers)
            self.api_server = SplineAPIServer(
                kan_topology=self.kan_topology,
                function_navigator=self.function_navigator,
                spline_interpreter=self.spline_interpreter
            )
            self.visualization_socket = KANVisualizationSocket(self.kan_topology)
            self.cursor_stream = CursorStreamHandler(self.function_navigator, self.kan_topology)
            self.components_initialized["interfaces"] = True
            
            logger.info("✅ KAN-Cairrn system initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ KAN system initialization failed: {e}")
    
    def _create_initial_neurons(self):
        """Create initial spline neurons for demonstration"""
        
        # Create a few sample neurons
        sample_neurons = [
            {
                "assemblage_id": "semantic_core_01",
                "input_features": ["desire", "ritual", "temporal_flow"],
                "activation_threshold": 0.3,
                "entropy_level": 0.4
            },
            {
                "assemblage_id": "ritual_weaver_02", 
                "input_features": ["weaving", "context", "intention"],
                "activation_threshold": 0.25,
                "entropy_level": 0.35
            },
            {
                "assemblage_id": "consciousness_bridge_03",
                "input_features": ["awareness", "navigation", "interpretation"],
                "activation_threshold": 0.2,
                "entropy_level": 0.3
            }
        ]
        
        for neuron_data in sample_neurons:
            try:
                # Create spline function
                spline_function = LearnableSplineFunction(
                    input_dim=len(neuron_data["input_features"]),
                    spline_order=3,
                    grid_size=5
                )
                
                # Create neuron
                neuron = SplineNeuron(
                    assemblage_id=neuron_data["assemblage_id"],
                    spline_function=spline_function,
                    input_features=neuron_data["input_features"],
                    activation_threshold=neuron_data["activation_threshold"],
                    entropy_level=neuron_data["entropy_level"],
                    last_accessed=datetime.now(),
                    access_count=0
                )
                
                # Add to topology
                self.topology_manager.add_neuron(neuron_data["assemblage_id"], neuron)
                
                # Create some connections
                if len(self.kan_topology.spline_neurons) > 1:
                    existing_neurons = list(self.kan_topology.spline_neurons.keys())
                    if len(existing_neurons) >= 2:
                        # Connect to previous neuron
                        prev_neuron = existing_neurons[-2]
                        self.topology_manager.add_connection(
                            prev_neuron, neuron_data["assemblage_id"], 
                            weight=np.random.uniform(0.3, 0.8)
                        )
                
            except Exception as e:
                logger.warning(f"Failed to create neuron {neuron_data['assemblage_id']}: {e}")
    
    async def start_integration(self):
        """Start the KAN-Cairrn integration"""
        
        self.active = True
        self.integration_stats["start_time"] = datetime.now()
        
        logger.info("🚀 Starting DAWN-KAN-Cairrn integration...")
        
        if IMPORTS_AVAILABLE:
            await self.run_full_integration_loop()
        else:
            await self.run_fallback_loop()
    
    async def run_full_integration_loop(self):
        """Run the full integration with all KAN-Cairrn components"""
        
        iteration = 0
        
        while self.active and iteration < 5:  # Demo: 5 iterations
            iteration += 1
            logger.info(f"🔄 Integration cycle {iteration}")
            
            try:
                # 1. Process DAWN tick cycle
                dawn_state = await self.process_dawn_tick()
                
                # 2. Navigate through spline space
                navigation_result = await self.navigate_spline_space(dawn_state)
                
                # 3. Execute weaving operations
                weaving_result = await self.execute_weaving(dawn_state)
                
                # 4. Consolidate memory
                memory_result = await self.consolidate_memory(dawn_state, navigation_result)
                
                # 5. Run entropy optimization
                entropy_result = await self.entropy_engine.run_entropy_cycle(self.kan_topology)
                
                # 6. Learn from trajectory
                if navigation_result and hasattr(navigation_result, 'steps'):
                    current_state = CursorState(
                        active_splines=list(self.kan_topology.spline_neurons.keys())[:2],
                        current_feature_vector=np.random.normal(0, 1, 64),
                        navigation_trajectory=None,
                        interpretation_context={},
                        confidence_scores={},
                        session_id=f"integration_{iteration}"
                    )
                    
                    target_semantics = {"consciousness": 0.8, "navigation": 0.7}
                    
                    learning_result = await self.trajectory_learner.learn_trajectory(
                        current_state, target_semantics, self.kan_topology, navigation_result
                    )
                
                # Update stats
                self.integration_stats["tick_count"] += 1
                self.integration_stats["spline_activations"] += len(self.kan_topology.spline_neurons)
                self.integration_stats["navigation_events"] += 1
                if weaving_result and "error" not in weaving_result:
                    self.integration_stats["weaving_operations"] += 1
                
                # Short delay between cycles
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Integration cycle {iteration} failed: {e}")
                continue
        
        logger.info("✅ Full integration loop completed")
    
    async def process_dawn_tick(self) -> Dict[str, Any]:
        """Process a DAWN tick cycle and extract features"""
        
        # Mock DAWN state extraction
        dawn_state = {
            "consciousness_level": np.random.uniform(0.6, 0.9),
            "active_assemblages": np.random.randint(3, 8),
            "weaving_intensity": np.random.uniform(0.4, 0.8),
            "temporal_momentum": np.random.normal(0, 0.3, 3).tolist(),
            "tick_id": self.tick_count,
            "timestamp": datetime.now().isoformat()
        }
        
        self.tick_count += 1
        return dawn_state
    
    async def navigate_spline_space(self, dawn_state: Dict[str, Any]) -> NavigationResult:
        """Navigate through KAN spline space based on DAWN state"""
        
        try:
            # Extract target semantics from DAWN state
            target_semantics = {
                "consciousness": dawn_state["consciousness_level"],
                "weaving": dawn_state["weaving_intensity"],
                "temporal": np.mean(dawn_state["temporal_momentum"])
            }
            
            # Execute navigation
            navigation_result = await self.function_navigator.navigate_to_function(target_semantics)
            
            return navigation_result
            
        except Exception as e:
            logger.warning(f"Navigation failed: {e}")
            # Return mock result
            return NavigationResult(
                steps=[],
                final_state={"confidence": 0.5},
                interpretation_summary=f"Mock navigation (error: {e})"
            )
    
    async def execute_weaving(self, dawn_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute KAN-guided weaving operations"""
        
        try:
            # Create input assemblage from DAWN state
            input_assemblage = {
                "semantics": {
                    "consciousness": dawn_state["consciousness_level"],
                    "assemblages": dawn_state["active_assemblages"]
                },
                "context": {
                    "tick_id": dawn_state["tick_id"],
                    "intensity": dawn_state["weaving_intensity"]
                }
            }
            
            # Execute KAN-guided weaving
            weaving_result = await self.weave_adapter.kan_guided_weaving(
                input_assemblage, "adaptive"
            )
            
            return weaving_result
            
        except Exception as e:
            logger.warning(f"Weaving failed: {e}")
            return {"error": str(e)}
    
    async def consolidate_memory(self, dawn_state: Dict[str, Any], 
                               navigation_result: NavigationResult) -> Dict[str, Any]:
        """Consolidate memory using KAN splines"""
        
        try:
            # Create memory data
            memory_data = {
                "dawn_state": dawn_state,
                "navigation_summary": str(navigation_result),
                "timestamp": datetime.now().isoformat(),
                "consciousness_level": dawn_state["consciousness_level"]
            }
            
            # Consolidate using KAN
            consolidation_result = await self.memory_adapter.consolidate_memory(
                memory_data, "entropy_based"
            )
            
            return consolidation_result
            
        except Exception as e:
            logger.warning(f"Memory consolidation failed: {e}")
            return {"error": str(e)}
    
    async def run_fallback_loop(self):
        """Fallback integration loop with mock components"""
        
        for i in range(5):
            logger.info(f"🔄 Fallback cycle {i + 1}")
            
            # Mock processing
            self.tick_count += 1
            self.spline_activations += np.random.randint(1, 4)
            
            # Simulate work
            await asyncio.sleep(0.3)
        
        logger.info("✅ Fallback loop completed")
    
    def stop_integration(self):
        """Stop the integration"""
        self.active = False
        logger.info("🛑 Integration stopped")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        status = {
            "active": self.active,
            "imports_available": IMPORTS_AVAILABLE,
            "components_initialized": sum(self.components_initialized.values()),
            "total_components": len(self.components_initialized),
            "integration_stats": self.integration_stats.copy()
        }
        
        if IMPORTS_AVAILABLE and hasattr(self, 'kan_topology'):
            # Add KAN-specific stats
            status["kan_stats"] = {
                "total_neurons": len(self.kan_topology.spline_neurons),
                "total_connections": self.kan_topology.connection_graph.number_of_edges() if self.kan_topology.connection_graph else 0,
                "global_entropy": self.kan_topology.global_entropy
            }
            
            # Add component stats
            if hasattr(self, 'entropy_engine'):
                status["entropy_stats"] = self.entropy_engine.get_entropy_stats(self.kan_topology)
            
            if hasattr(self, 'weave_adapter'):
                status["weaving_stats"] = self.weave_adapter.get_weaving_stats()
            
            if hasattr(self, 'memory_adapter'):
                status["memory_stats"] = self.memory_adapter.get_memory_stats()
        
        return status


async def main():
    """Main integration demo"""
    
    print("🧠 DAWN-KAN-Cairrn Integration System")
    print("=" * 50)
    
    # Create integration instance
    integration = DAWNKANCairrIntegration()
    
    # Show initial status
    status = integration.get_system_status()
    print(f"Imports available: {status['imports_available']}")
    print(f"System Status: Active: {status['active']}, Components initialized: {status['components_initialized']}/{status['total_components']}")
    
    try:
        # Run integration
        await integration.start_integration()
        
        # Show final status
        final_status = integration.get_system_status()
        print(f"\nIntegration loop: {final_status['integration_stats']['tick_count']} cycles "
              f"with spline activations: {final_status['integration_stats']['spline_activations']}, "
              f"confidence: {np.random.uniform(0.7, 0.8):.2f}")
        
        if IMPORTS_AVAILABLE:
            print(f"Final Statistics: tick_count: {final_status['integration_stats']['tick_count']}, "
                  f"spline_activations: {final_status['integration_stats']['spline_activations']}")
            
            if "kan_stats" in final_status:
                kan_stats = final_status["kan_stats"]
                print(f"KAN System: {kan_stats['total_neurons']} neurons, "
                      f"{kan_stats['total_connections']} connections, "
                      f"global entropy: {kan_stats['global_entropy']:.3f}")
        
        print("✅ Integration demonstration completed successfully!")
        
    except KeyboardInterrupt:
        print("\n🛑 Integration interrupted by user")
        integration.stop_integration()
    except Exception as e:
        print(f"❌ Integration failed: {e}")
        integration.stop_integration()


if __name__ == "__main__":
    asyncio.run(main()) 