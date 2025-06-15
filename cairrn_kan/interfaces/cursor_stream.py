"""
Cursor Stream Handler

Handler for streaming cursor navigation through function space.
"""

import json
import asyncio
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from ..models import CursorState, KANTopology
from ..cursor.function_navigator import FunctionNavigator


class CursorStreamHandler:
    """Handler for cursor navigation streaming"""
    
    def __init__(self, function_navigator: FunctionNavigator, kan_topology: KANTopology):
        self.function_navigator = function_navigator
        self.kan_topology = kan_topology
        self.logger = logging.getLogger(__name__)
        
        # Streaming state
        self.active_streams = {}
        self.navigation_history = []
        
    async def start_cursor_stream(self, stream_id: str, 
                                callback_func,
                                update_interval: float = 1.0) -> Dict[str, Any]:
        """Start streaming cursor position updates"""
        
        if stream_id in self.active_streams:
            return {"error": "Stream already active", "stream_id": stream_id}
        
        try:
            # Initialize stream
            stream_info = {
                "stream_id": stream_id,
                "callback": callback_func,
                "update_interval": update_interval,
                "active": True,
                "created_at": datetime.now().isoformat(),
                "update_count": 0
            }
            
            self.active_streams[stream_id] = stream_info
            
            # Start streaming task
            asyncio.create_task(self.cursor_stream_loop(stream_id))
            
            self.logger.info(f"Started cursor stream: {stream_id}")
            
            return {
                "stream_id": stream_id,
                "status": "started",
                "update_interval": update_interval,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to start cursor stream {stream_id}: {e}")
            return {"error": str(e), "stream_id": stream_id}
    
    async def stop_cursor_stream(self, stream_id: str) -> Dict[str, Any]:
        """Stop a cursor stream"""
        
        if stream_id not in self.active_streams:
            return {"error": "Stream not found", "stream_id": stream_id}
        
        try:
            # Mark stream as inactive
            self.active_streams[stream_id]["active"] = False
            
            # Remove from active streams
            del self.active_streams[stream_id]
            
            self.logger.info(f"Stopped cursor stream: {stream_id}")
            
            return {
                "stream_id": stream_id,
                "status": "stopped",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to stop cursor stream {stream_id}: {e}")
            return {"error": str(e), "stream_id": stream_id}
    
    async def cursor_stream_loop(self, stream_id: str):
        """Main loop for cursor position streaming"""
        
        while (stream_id in self.active_streams and 
               self.active_streams[stream_id]["active"]):
            
            try:
                stream_info = self.active_streams[stream_id]
                
                # Get current cursor state
                cursor_state = await self.get_current_cursor_state()
                
                # Generate stream update
                update_data = {
                    "stream_id": stream_id,
                    "update_count": stream_info["update_count"],
                    "cursor_state": cursor_state,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Send update via callback
                callback = stream_info["callback"]
                await callback(update_data)
                
                # Update stream info
                stream_info["update_count"] += 1
                
                # Wait for next update
                await asyncio.sleep(stream_info["update_interval"])
                
            except Exception as e:
                self.logger.error(f"Cursor stream error for {stream_id}: {e}")
                break
        
        # Clean up
        if stream_id in self.active_streams:
            self.active_streams[stream_id]["active"] = False
    
    async def get_current_cursor_state(self) -> Dict[str, Any]:
        """Get current cursor state for streaming"""
        
        try:
            # Get active splines
            active_splines = []
            for spline_id, neuron in self.kan_topology.spline_neurons.items():
                # Consider recently accessed neurons as "active"
                time_since_access = (datetime.now() - neuron.last_accessed).total_seconds()
                if time_since_access < 300:  # Active within 5 minutes
                    active_splines.append(spline_id)
            
            # Generate feature vector (simplified)
            import numpy as np
            feature_vector = np.random.normal(0, 1, 64)  # Mock feature vector
            
            # Compute confidence scores
            confidence_scores = {}
            for spline_id in active_splines:
                neuron = self.kan_topology.spline_neurons[spline_id]
                confidence_scores[spline_id] = 1.0 - neuron.entropy_level
            
            cursor_state = {
                "active_splines": active_splines,
                "feature_vector_norm": float(np.linalg.norm(feature_vector)),
                "confidence_scores": confidence_scores,
                "position_summary": {
                    "active_spline_count": len(active_splines),
                    "avg_confidence": np.mean(list(confidence_scores.values())) if confidence_scores else 0.0,
                    "total_neurons": len(self.kan_topology.spline_neurons)
                }
            }
            
            return cursor_state
            
        except Exception as e:
            self.logger.error(f"Failed to get cursor state: {e}")
            return {
                "error": str(e),
                "active_splines": [],
                "confidence_scores": {},
                "position_summary": {}
            }
    
    async def navigate_cursor_streamed(self, 
                                     stream_id: str,
                                     target_semantics: Dict[str, float],
                                     navigation_strategy: str = "adaptive") -> Dict[str, Any]:
        """Execute cursor navigation with streaming updates"""
        
        navigation_start = datetime.now()
        navigation_id = f"nav_{int(navigation_start.timestamp())}"
        
        try:
            # Create mock cursor state for navigation
            import numpy as np
            
            current_state = CursorState(
                active_splines=list(self.kan_topology.spline_neurons.keys())[:3],
                current_feature_vector=np.random.normal(0, 1, 64),
                navigation_trajectory=None,  # Will be created during navigation
                interpretation_context={},
                confidence_scores={},
                session_id=f"stream_{stream_id}"
            )
            
            # Execute navigation
            navigation_result = await self.function_navigator.navigate_to_function(target_semantics)
            
            # Record navigation
            navigation_record = {
                "navigation_id": navigation_id,
                "stream_id": stream_id,
                "target_semantics": target_semantics,
                "strategy": navigation_strategy,
                "navigation_result": navigation_result.__dict__ if hasattr(navigation_result, '__dict__') else str(navigation_result),
                "execution_time": (datetime.now() - navigation_start).total_seconds(),
                "timestamp": navigation_start.isoformat()
            }
            
            self.navigation_history.append(navigation_record)
            
            # Trim history
            if len(self.navigation_history) > 100:
                self.navigation_history = self.navigation_history[-50:]
            
            return {
                "navigation_id": navigation_id,
                "stream_id": stream_id,
                "status": "completed",
                "target_semantics": target_semantics,
                "execution_time": navigation_record["execution_time"],
                "timestamp": navigation_start.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Streamed navigation failed for {stream_id}: {e}")
            return {
                "navigation_id": navigation_id,
                "stream_id": stream_id,
                "error": str(e),
                "target_semantics": target_semantics,
                "timestamp": datetime.now().isoformat()
            }
    
    def get_stream_stats(self) -> Dict[str, Any]:
        """Get statistics about active streams"""
        
        stats = {
            "active_streams": len(self.active_streams),
            "total_navigations": len(self.navigation_history),
            "timestamp": datetime.now().isoformat()
        }
        
        if self.active_streams:
            # Stream activity
            total_updates = sum(
                stream["update_count"] for stream in self.active_streams.values()
            )
            stats["total_updates"] = total_updates
            
            # Average update rate
            active_durations = []
            current_time = datetime.now()
            
            for stream in self.active_streams.values():
                try:
                    created_time = datetime.fromisoformat(stream["created_at"])
                    duration = (current_time - created_time).total_seconds()
                    if duration > 0:
                        active_durations.append(duration)
                except Exception:
                    pass
            
            if active_durations:
                avg_duration = sum(active_durations) / len(active_durations)
                stats["avg_stream_duration"] = avg_duration
        
        if self.navigation_history:
            # Navigation success rate
            successful_navs = [
                nav for nav in self.navigation_history 
                if "error" not in nav
            ]
            stats["navigation_success_rate"] = len(successful_navs) / len(self.navigation_history)
            
            # Average navigation time
            nav_times = [
                nav["execution_time"] for nav in self.navigation_history 
                if "execution_time" in nav
            ]
            if nav_times:
                stats["avg_navigation_time"] = sum(nav_times) / len(nav_times)
        
        return stats
    
    def get_active_streams(self) -> Dict[str, Any]:
        """Get information about active streams"""
        
        active_info = {}
        
        for stream_id, stream_info in self.active_streams.items():
            active_info[stream_id] = {
                "stream_id": stream_id,
                "created_at": stream_info["created_at"],
                "update_interval": stream_info["update_interval"],
                "update_count": stream_info["update_count"],
                "active": stream_info["active"]
            }
        
        return {
            "active_streams": active_info,
            "stream_count": len(active_info),
            "timestamp": datetime.now().isoformat()
        } 