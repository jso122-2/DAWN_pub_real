"""
Talk To Handler - Manages conversation and interaction with DAWN
"""

import logging
import time
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect

# Import all DAWN components
from core.unified_tick_engine import UnifiedTickEngine
from core.consciousness_core import DAWNConsciousness
from core.orchestrator import initialize_module, get_module, shutdown_modules
from core.conversation_enhanced import EnhancedConversation
from core.system.event_bus import EventBus, DAWNEvents, event_bus

# Import cognitive components
from cognitive.conversation import DAWNConversation
from cognitive.spontaneity import DAWNSpontaneity
from cognitive.entropy_fluctuation import EntropyFluctuation
from cognitive.mood_urgency_probe import MoodUrgencyProbe
from cognitive.qualia_kernel import QualiaKernel
from cognitive.alignment_probe import AlignmentProbe

# Import processes
from processes.awareness_engine import AwarenessEngine
from processes.creativity_engine import CreativityEngine
from processes.dream_engine import DreamEngine
from processes.intuition_processor import IntuitionProcessor
from processes.memory_palace import MemoryPalace
from processes.neural_sync import NeuralSync
from processes.pattern_recognizer import PatternRecognizer
from processes.quantum_flux import QuantumFlux

# Import visualizers
from core.dawn_visualizer import DAWNVisualizer
from core.alignment_visualizer import AlignmentVisualizer
from core.entropy_visualizer import EntropyVisualizer
from core.thermal_visualizer import ThermalVisualizer
from core.bloom_visualizer import BloomVisualizer

# Import PSL visualizer
try:
    from visual.psl_integration import PSLVisualizer
except (ImportError, IndentationError):
    from backend.visual.psl_integration_bypass import PSLVisualizer

logger = logging.getLogger(__name__)

@dataclass
class TalkState:
    """Current state of the talk system"""
    last_interaction: float = field(default_factory=time.time)
    conversation_history: List[Dict] = field(default_factory=list)
    current_context: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=lambda: {
        'response_time': 0.0,
        'context_relevance': 0.0,
        'emotional_resonance': 0.0
    })

class TalkToHandler:
    """
    Manages conversation and interaction with DAWN.
    Handles input processing, response generation, and context management.
    """
    
    def __init__(self):
        """Initialize talk handler"""
        self.state = TalkState()
        self.consciousness = DAWNConsciousness()
        self.qualia = QualiaKernel()
        self.alignment = AlignmentProbe()
        self.mood = MoodUrgencyProbe()
        self.entropy = EntropyFluctuation()
        self.spontaneity = DAWNSpontaneity()
        self.psl_visualizer = PSLVisualizer()
        
        self.config = {
            'update_interval': 0.5,  # 500ms
            'history_limit': 100,
            'context_window': 10,  # Number of interactions to keep in context
            'metrics': {
                'response_time': 0.0,
                'context_relevance': 0.0,
                'emotional_resonance': 0.0
            }
        }
        logger.info("Initialized TalkToHandler")
    
    async def handle_connection(self, websocket: WebSocket):
        """Handle WebSocket connection for talk interface"""
        await websocket.accept()
        logger.info("New WebSocket connection accepted")
        
        try:
            # Send initial state
            await websocket.send_json({
                "type": "connection",
                "data": {
                    "status": "connected",
                    "state": self.get_talk_state()
                }
            })
            
            # Handle incoming messages
            while True:
                try:
                    # Receive message
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    
                    if message.get("type") == "message":
                        # Process input
                        response = self.process_input(message.get("content", ""))
                        
                        # Send response
                        await websocket.send_json({
                            "type": "response",
                            "data": {
                                "content": response,
                                "metrics": self.state.metrics,
                                "timestamp": time.time()
                            }
                        })
                        
                    elif message.get("type") == "heartbeat":
                        # Send heartbeat response
                        await websocket.send_json({
                            "type": "heartbeat_response",
                            "timestamp": message.get("timestamp")
                        })
                        
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid JSON format"
                    })
                    
        except WebSocketDisconnect:
            logger.info("WebSocket connection closed")
        except Exception as e:
            logger.error(f"Error in WebSocket connection: {e}")
            try:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
            except:
                pass
    
    def process_input(self, input_text: str) -> Optional[str]:
        """
        Process user input and generate response
        
        Args:
            input_text: User input text
            
        Returns:
            Generated response or None
        """
        if not input_text:
            return None
        
        start_time = time.time()
        
        # Process input through cognitive components
        qualia_experience = self.qualia.process_experience(input_text)
        alignment_state = self.alignment.check_alignment(input_text)
        mood_state = self.mood.check_mood(input_text)
        entropy_state = self.entropy.check_entropy(input_text)
        spontaneity = self.spontaneity.check_spontaneity(input_text)
        
        # Generate response
        response = self._generate_response(
            input_text,
            qualia_experience,
            alignment_state,
            mood_state,
            entropy_state,
            spontaneity
        )
        
        # Update metrics
        self._update_metrics(time.time() - start_time)
        
        # Record interaction
        self._record_interaction(input_text, response)
        
        return response
    
    def _generate_response(
        self,
        input_text: str,
        qualia: Dict[str, Any],
        alignment: Dict[str, Any],
        mood: Dict[str, Any],
        entropy: Dict[str, Any],
        spontaneity: Dict[str, Any]
    ) -> str:
        """Generate response based on cognitive states"""
        # Simple response generation for now
        return f"Processed: {input_text}"
    
    def _update_metrics(self, response_time: float) -> None:
        """Update talk metrics"""
        self.state.metrics['response_time'] = response_time
        self.state.metrics['context_relevance'] = self._calculate_context_relevance()
        self.state.metrics['emotional_resonance'] = self._calculate_emotional_resonance()
    
    def _calculate_context_relevance(self) -> float:
        """Calculate context relevance score"""
        return 0.8  # Placeholder
    
    def _calculate_emotional_resonance(self) -> float:
        """Calculate emotional resonance score"""
        return 0.7  # Placeholder
    
    def _record_interaction(self, input_text: str, response: str) -> None:
        """Record interaction in history"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'input': input_text,
            'response': response,
            'metrics': self.state.metrics.copy()
        }
        
        self.state.conversation_history.append(interaction)
        if len(self.state.conversation_history) > self.config['history_limit']:
            self.state.conversation_history = self.state.conversation_history[-self.config['history_limit']:]
        
        self.state.last_interaction = time.time()
    
    def get_talk_state(self) -> Dict:
        """Get current talk state"""
        return {
            'last_interaction': self.state.last_interaction,
            'history_size': len(self.state.conversation_history),
            'metrics': self.state.metrics.copy()
        }
    
    def get_metrics_json(self) -> str:
        """Get current metrics as JSON string"""
        return json.dumps({
            "type": "metrics",
            "subprocess_id": "talk_handler",
            "metrics": self.state.metrics,
            "timestamp": time.time()
        })

# Global instance
_talk_handler = None

def get_talk_handler() -> TalkToHandler:
    """Get or create the global talk handler instance"""
    global _talk_handler
    if _talk_handler is None:
        _talk_handler = TalkToHandler()
    return _talk_handler

__all__ = ['TalkToHandler', 'get_talk_handler'] 