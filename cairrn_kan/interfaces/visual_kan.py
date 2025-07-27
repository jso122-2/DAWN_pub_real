"""
Visual KAN Interface

WebSocket interface for real-time KAN topology visualization.
"""

import json
import asyncio
import websockets
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from ..models import KANTopology


class KANVisualizationSocket:
    """WebSocket handler for KAN visualization"""
    
    def __init__(self, kan_topology: KANTopology):
        self.kan_topology = kan_topology
        self.logger = logging.getLogger(__name__)
        
        # Active connections
        self.active_connections = {}
        self.session_counter = 0
        
    async def handle_connection(self, websocket, path):
        """Handle new WebSocket connection"""
        
        session_id = await self.initialize_kan_session(websocket)
        
        try:
            async for message in websocket:
                await self.handle_message(session_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            self.logger.info(f"Session {session_id} disconnected")
        except Exception as e:
            self.logger.error(f"Session {session_id} error: {e}")
        finally:
            if session_id in self.active_connections:
                del self.active_connections[session_id]
    
    async def initialize_kan_session(self, websocket) -> str:
        """Initialize a new KAN visualization session"""
        
        self.session_counter += 1
        session_id = f"kan_session_{self.session_counter}"
        
        self.active_connections[session_id] = {
            "websocket": websocket,
            "created_at": datetime.now().isoformat(),
            "message_count": 0,
            "streaming": False
        }
        
        # Send initial topology data
        await self.send_topology_snapshot(session_id)
        
        self.logger.info(f"Initialized KAN visualization session: {session_id}")
        return session_id
    
    async def handle_message(self, session_id: str, message: str):
        """Handle incoming WebSocket message"""
        
        if session_id not in self.active_connections:
            return
        
        connection_info = self.active_connections[session_id]
        connection_info["message_count"] += 1
        
        try:
            command = json.loads(message)
            command_type = command.get("type", "unknown")
            
            if command_type == "get_topology":
                await self.send_topology_snapshot(session_id)
            elif command_type == "start_streaming":
                await self.start_activation_stream(session_id)
            elif command_type == "stop_streaming":
                await self.stop_activation_stream(session_id)
            elif command_type == "get_neuron_details":
                neuron_id = command.get("neuron_id")
                await self.send_neuron_details(session_id, neuron_id)
            else:
                await self.send_error(session_id, f"Unknown command: {command_type}")
                
        except json.JSONDecodeError:
            await self.send_error(session_id, "Invalid JSON message")
        except Exception as e:
            await self.send_error(session_id, f"Message handling error: {e}")
    
    async def send_topology_snapshot(self, session_id: str):
        """Send current topology snapshot"""
        
        if session_id not in self.active_connections:
            return
        
        websocket = self.active_connections[session_id]["websocket"]
        
        try:
            # Generate topology visualization data
            topology_data = self.generate_topology_visualization()
            
            message = {
                "type": "topology_snapshot",
                "data": topology_data,
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(message))
            
        except Exception as e:
            self.logger.error(f"Failed to send topology snapshot to {session_id}: {e}")
    
    async def start_activation_stream(self, session_id: str):
        """Start streaming activation updates"""
        
        if session_id not in self.active_connections:
            return
        
        connection_info = self.active_connections[session_id]
        connection_info["streaming"] = True
        
        websocket = connection_info["websocket"]
        
        try:
            await websocket.send(json.dumps({
                "type": "stream_started",
                "message": "Activation streaming started",
                "timestamp": datetime.now().isoformat()
            }))
            
            # Start streaming loop
            asyncio.create_task(self.activation_stream_loop(session_id))
            
        except Exception as e:
            self.logger.error(f"Failed to start streaming for {session_id}: {e}")
    
    async def stop_activation_stream(self, session_id: str):
        """Stop streaming activation updates"""
        
        if session_id not in self.active_connections:
            return
        
        connection_info = self.active_connections[session_id]
        connection_info["streaming"] = False
        
        websocket = connection_info["websocket"]
        
        try:
            await websocket.send(json.dumps({
                "type": "stream_stopped",
                "message": "Activation streaming stopped",
                "timestamp": datetime.now().isoformat()
            }))
            
        except Exception as e:
            self.logger.error(f"Failed to stop streaming for {session_id}: {e}")
    
    async def activation_stream_loop(self, session_id: str):
        """Main loop for streaming activation updates"""
        
        while (session_id in self.active_connections and 
               self.active_connections[session_id]["streaming"]):
            
            try:
                # Generate activation data
                activation_data = self.generate_activation_data()
                
                message = {
                    "type": "activation_update",
                    "data": activation_data,
                    "timestamp": datetime.now().isoformat()
                }
                
                websocket = self.active_connections[session_id]["websocket"]
                await websocket.send(json.dumps(message))
                
                # Wait before next update
                await asyncio.sleep(0.5)  # 2Hz update rate
                
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                self.logger.error(f"Streaming error for {session_id}: {e}")
                break
        
        # Clean up streaming state
        if session_id in self.active_connections:
            self.active_connections[session_id]["streaming"] = False
    
    async def send_neuron_details(self, session_id: str, neuron_id: str):
        """Send detailed information about a specific neuron"""
        
        if session_id not in self.active_connections:
            return
        
        websocket = self.active_connections[session_id]["websocket"]
        
        try:
            if neuron_id in self.kan_topology.spline_neurons:
                neuron = self.kan_topology.spline_neurons[neuron_id]
                
                details = {
                    "neuron_id": neuron_id,
                    "assemblage_id": neuron.assemblage_id,
                    "input_features": neuron.input_features,
                    "activation_threshold": neuron.activation_threshold,
                    "entropy_level": neuron.entropy_level,
                    "access_count": neuron.access_count,
                    "last_accessed": neuron.last_accessed.isoformat()
                }
                
                message = {
                    "type": "neuron_details",
                    "data": details,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                message = {
                    "type": "error",
                    "message": f"Neuron {neuron_id} not found",
                    "timestamp": datetime.now().isoformat()
                }
            
            await websocket.send(json.dumps(message))
            
        except Exception as e:
            self.logger.error(f"Failed to send neuron details to {session_id}: {e}")
    
    async def send_error(self, session_id: str, error_message: str):
        """Send error message to client"""
        
        if session_id not in self.active_connections:
            return
        
        websocket = self.active_connections[session_id]["websocket"]
        
        try:
            message = {
                "type": "error",
                "message": error_message,
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(message))
            
        except Exception as e:
            self.logger.error(f"Failed to send error to {session_id}: {e}")
    
    def generate_topology_visualization(self) -> Dict[str, Any]:
        """Generate visualization data for the current topology"""
        
        # Node data
        nodes = []
        for neuron_id, neuron in self.kan_topology.spline_neurons.items():
            node = {
                "id": neuron_id,
                "assemblage_id": neuron.assemblage_id,
                "entropy": neuron.entropy_level,
                "access_count": neuron.access_count,
                "features": neuron.input_features[:3],  # First 3 features for display
                "threshold": neuron.activation_threshold,
                "last_accessed": neuron.last_accessed.isoformat()
            }
            nodes.append(node)
        
        # Edge data
        edges = []
        if self.kan_topology.connection_graph:
            for source, target, data in self.kan_topology.connection_graph.edges(data=True):
                edge = {
                    "source": source,
                    "target": target,
                    "weight": data.get("weight", 0.0)
                }
                edges.append(edge)
        
        # Statistics
        stats = {
            "total_neurons": len(self.kan_topology.spline_neurons),
            "total_connections": len(edges),
            "global_entropy": self.kan_topology.global_entropy,
            "avg_entropy": sum(n["entropy"] for n in nodes) / len(nodes) if nodes else 0.0,
            "total_accesses": sum(n["access_count"] for n in nodes)
        }
        
        return {
            "nodes": nodes,
            "edges": edges,
            "stats": stats,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_activation_data(self) -> Dict[str, Any]:
        """Generate current activation state data"""
        
        activations = {}
        
        for neuron_id, neuron in self.kan_topology.spline_neurons.items():
            # Simple activation simulation based on recent access
            time_since_access = (datetime.now() - neuron.last_accessed).total_seconds()
            activation_level = max(0.0, 1.0 - time_since_access / 300.0)  # Decay over 5 minutes
            
            activations[neuron_id] = {
                "activation_level": activation_level,
                "entropy": neuron.entropy_level,
                "confidence": 1.0 - neuron.entropy_level  # Simple confidence estimate
            }
        
        return {
            "activations": activations,
            "global_activity": sum(a["activation_level"] for a in activations.values()),
            "active_neurons": sum(1 for a in activations.values() if a["activation_level"] > 0.1),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get statistics about active connections"""
        
        stats = {
            "active_connections": len(self.active_connections),
            "streaming_connections": sum(
                1 for conn in self.active_connections.values() 
                if conn.get("streaming", False)
            ),
            "total_messages": sum(
                conn.get("message_count", 0) 
                for conn in self.active_connections.values()
            ),
            "session_counter": self.session_counter,
            "timestamp": datetime.now().isoformat()
        }
        
        return stats 