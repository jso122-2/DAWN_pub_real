#!/usr/bin/env python3
"""
DAWN Talk Integration Script
=============================

Bridge between tick engine and consciousness layer.
Manages conversation flow, spontaneous thoughts, and metrics integration.

Usage:
    python integrate_talk.py [--config config.json] [--debug]

Features:
- Full DAWN consciousness and conversation system initialization
- Real-time metrics stream connection
- Background spontaneous thought generation
- Comprehensive conversation logging and analysis
- Graceful shutdown handling
- Configuration management

Author: Jackson (DAWN Consciousness Architect)
"""

import asyncio
import json
import logging
import signal
import sys
import threading
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

# Add project root to Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

# Import DAWN modules
from cognitive.consciousness import DAWNConsciousness
from cognitive.conversation import DAWNConversation
from cognitive.spontaneity import DAWNSpontaneity
import requests
import websocket
import urllib3

# Suppress SSL warnings for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ConversationLogger:
    """Enhanced conversation logging and analysis system"""
    
    def __init__(self, log_dir: str = "logs/conversations"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup conversation-specific logger
        self.conversation_logger = logging.getLogger("dawn.conversations")
        conversation_handler = logging.FileHandler(
            self.log_dir / f"conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        conversation_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        self.conversation_logger.addHandler(conversation_handler)
        self.conversation_logger.setLevel(logging.INFO)
        
        # Analysis data storage
        self.conversation_history = []
        self.thought_history = []
        self.metrics_history = []
        self.session_start = datetime.now()
        
    def log_conversation(self, user_input: str, dawn_response: str, 
                        intent: str, confidence: float, metrics: Dict[str, Any],
                        consciousness_state: str, action_taken: Optional[str] = None):
        """Log a complete conversation interaction"""
        
        conversation_data = {
            "timestamp": datetime.now().isoformat(),
            "session_duration": (datetime.now() - self.session_start).total_seconds(),
            "user_input": user_input,
            "dawn_response": dawn_response,
            "intent": intent,
            "confidence": confidence,
            "consciousness_state": consciousness_state,
            "action_taken": action_taken,
            "metrics": metrics
        }
        
        self.conversation_history.append(conversation_data)
        
        # Log to file
        self.conversation_logger.info(
            f"CONVERSATION | User: '{user_input}' | DAWN: '{dawn_response}' | "
            f"Intent: {intent} ({confidence:.2f}) | State: {consciousness_state} | "
            f"Action: {action_taken or 'None'}"
        )
        
        # Analysis logging
        if len(self.conversation_history) % 10 == 0:
            self._log_conversation_analysis()
    
    def log_spontaneous_thought(self, thought: str, state: str, priority: int, metrics: Dict[str, Any]):
        """Log a spontaneous thought"""
        
        thought_data = {
            "timestamp": datetime.now().isoformat(),
            "thought": thought,
            "state": state,
            "priority": priority,
            "metrics": metrics
        }
        
        self.thought_history.append(thought_data)
        
        self.conversation_logger.info(
            f"SPONTANEOUS_THOUGHT | Priority: {priority} | State: {state} | '{thought}'"
        )
    
    def log_metrics_update(self, metrics: Dict[str, Any]):
        """Log metrics updates for analysis"""
        
        metrics_data = {
            "timestamp": datetime.now().isoformat(),
            **metrics
        }
        
        self.metrics_history.append(metrics_data)
        
        # Keep only last 1000 metrics for memory management
        if len(self.metrics_history) > 1000:
            self.metrics_history = self.metrics_history[-1000:]
    
    def _log_conversation_analysis(self):
        """Log conversation analysis"""
        
        if not self.conversation_history:
            return
        
        recent_conversations = self.conversation_history[-10:]
        
        # Calculate statistics
        avg_confidence = sum(c["confidence"] for c in recent_conversations) / len(recent_conversations)
        intent_distribution = {}
        state_distribution = {}
        
        for conv in recent_conversations:
            intent = conv["intent"]
            state = conv["consciousness_state"]
            intent_distribution[intent] = intent_distribution.get(intent, 0) + 1
            state_distribution[state] = state_distribution.get(state, 0) + 1
        
        self.conversation_logger.info(
            f"ANALYSIS | Last 10 conversations | Avg confidence: {avg_confidence:.3f} | "
            f"Intent distribution: {intent_distribution} | State distribution: {state_distribution}"
        )
    
    def save_session_summary(self):
        """Save complete session summary"""
        
        summary_file = self.log_dir / f"session_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            "session_info": {
                "start_time": self.session_start.isoformat(),
                "end_time": datetime.now().isoformat(),
                "duration_seconds": (datetime.now() - self.session_start).total_seconds(),
                "total_conversations": len(self.conversation_history),
                "total_thoughts": len(self.thought_history),
                "total_metrics_updates": len(self.metrics_history)
            },
            "conversation_summary": {
                "most_common_intents": self._get_intent_summary(),
                "consciousness_state_distribution": self._get_state_summary(),
                "average_confidence": self._get_average_confidence(),
                "actions_taken": self._get_actions_summary()
            },
            "full_conversation_history": self.conversation_history,
            "spontaneous_thoughts": self.thought_history,
            "final_metrics": self.metrics_history[-1] if self.metrics_history else None
        }
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logging.info(f"Session summary saved to: {summary_file}")
        return summary_file
    
    def _get_intent_summary(self) -> Dict[str, int]:
        """Get intent distribution summary"""
        intent_counts = {}
        for conv in self.conversation_history:
            intent = conv["intent"]
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        return dict(sorted(intent_counts.items(), key=lambda x: x[1], reverse=True))
    
    def _get_state_summary(self) -> Dict[str, int]:
        """Get consciousness state distribution summary"""
        state_counts = {}
        for conv in self.conversation_history:
            state = conv["consciousness_state"]
            state_counts[state] = state_counts.get(state, 0) + 1
        return dict(sorted(state_counts.items(), key=lambda x: x[1], reverse=True))
    
    def _get_average_confidence(self) -> float:
        """Get average conversation confidence"""
        if not self.conversation_history:
            return 0.0
        return sum(c["confidence"] for c in self.conversation_history) / len(self.conversation_history)
    
    def _get_actions_summary(self) -> Dict[str, int]:
        """Get actions taken summary"""
        action_counts = {}
        for conv in self.conversation_history:
            action = conv["action_taken"]
            if action:
                action_counts[action] = action_counts.get(action, 0) + 1
        return dict(sorted(action_counts.items(), key=lambda x: x[1], reverse=True))


class MetricsStreamClient:
    """WebSocket client for real-time metrics streaming"""
    
    def __init__(self, url: str, on_metrics_callback):
        self.url = url
        self.on_metrics_callback = on_metrics_callback
        self.ws = None
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 10
        self.reconnect_delay = 5.0
        
    def connect(self):
        """Connect to metrics WebSocket"""
        try:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            
            # Start connection in background thread
            self.ws_thread = threading.Thread(target=self.ws.run_forever, daemon=True)
            self.ws_thread.start()
            
            logging.info(f"Connecting to metrics stream at {self.url}")
            
        except Exception as e:
            logging.error(f"Failed to connect to metrics stream: {e}")
            self.schedule_reconnect()
    
    def on_open(self, ws):
        """Handle WebSocket connection opened"""
        self.connected = True
        self.reconnect_attempts = 0
        logging.info("✅ Connected to metrics stream")
    
    def on_message(self, ws, message):
        """Handle incoming metrics message"""
        try:
            data = json.loads(message)
            if self.on_metrics_callback:
                self.on_metrics_callback(data)
        except Exception as e:
            logging.error(f"Error processing metrics message: {e}")
    
    def on_error(self, ws, error):
        """Handle WebSocket error"""
        logging.error(f"Metrics stream error: {error}")
    
    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection closed"""
        self.connected = False
        logging.warning(f"Metrics stream disconnected: {close_status_code} - {close_msg}")
        self.schedule_reconnect()
    
    def schedule_reconnect(self):
        """Schedule reconnection attempt"""
        if self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            logging.info(f"Scheduling reconnect attempt {self.reconnect_attempts}/{self.max_reconnect_attempts} in {self.reconnect_delay}s")
            
            def reconnect():
                time.sleep(self.reconnect_delay)
                if not self.connected:
                    self.connect()
            
            threading.Thread(target=reconnect, daemon=True).start()
        else:
            logging.error("Max reconnect attempts reached. Giving up on metrics stream.")
    
    def disconnect(self):
        """Disconnect from metrics stream"""
        if self.ws:
            self.ws.close()


class DAWNTalkIntegration:
    """Main integration class managing all DAWN conversation components"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.running = False
        self.shutdown_event = threading.Event()
        
        # Initialize logging
        self.setup_logging()
        
        # Initialize conversation logger
        self.conversation_logger = ConversationLogger(
            self.config.get("conversation_log_dir", "logs/conversations")
        )
        
        # Initialize DAWN components
        self.consciousness = None
        self.conversation = None
        self.spontaneity = None
        
        # Initialize metrics client
        self.metrics_client = None
        self.current_metrics = {
            "scup": 0.5,
            "entropy": 0.5,
            "heat": 0.3,
            "mood": "initializing",
            "timestamp": time.time(),
            "tick_count": 0
        }
        
        # Background thread management
        self.thought_thread = None
        self.metrics_thread = None
        
        logging.info("DAWN Talk Integration initialized")
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_level = self.config.get("log_level", "INFO").upper()
        
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(
                    f"logs/dawn_integration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
                    mode='a'
                )
            ]
        )
        
        # Create logs directory
        Path("logs").mkdir(exist_ok=True)
        
        logging.info(f"Logging initialized at {log_level} level")
    
    def initialize_consciousness_system(self):
        """Initialize DAWN consciousness and conversation components"""
        try:
            logging.info("🧠 Initializing DAWN consciousness system...")
            
            # Initialize consciousness
            self.consciousness = DAWNConsciousness()
            logging.info("✅ DAWNConsciousness initialized")
            
            # Initialize conversation with consciousness
            self.conversation = DAWNConversation(self.consciousness)
            logging.info("✅ DAWNConversation initialized")
            
            # Initialize spontaneity with consciousness
            self.spontaneity = DAWNSpontaneity(self.consciousness)
            logging.info("✅ DAWNSpontaneity initialized")
            
            logging.info("🌟 DAWN consciousness system fully initialized")
            
        except Exception as e:
            logging.error(f"Failed to initialize consciousness system: {e}")
            traceback.print_exc()
            raise
    
    def connect_to_metrics_stream(self):
        """Connect to the existing metrics stream"""
        try:
            metrics_url = self.config.get("metrics_websocket_url", "ws://localhost:8000/ws")
            logging.info(f"🔗 Connecting to metrics stream: {metrics_url}")
            
            self.metrics_client = MetricsStreamClient(
                metrics_url,
                self.on_metrics_received
            )
            
            self.metrics_client.connect()
            
            # Wait for connection
            max_wait = 10.0
            wait_time = 0.0
            while not self.metrics_client.connected and wait_time < max_wait:
                time.sleep(0.1)
                wait_time += 0.1
            
            if self.metrics_client.connected:
                logging.info("✅ Connected to metrics stream")
            else:
                logging.warning("⚠️ Metrics stream connection timeout - continuing without real-time metrics")
                
        except Exception as e:
            logging.error(f"Failed to connect to metrics stream: {e}")
            logging.info("Continuing without real-time metrics")
    
    def on_metrics_received(self, metrics_data: Dict[str, Any]):
        """Handle received metrics from stream"""
        try:
            # Extract metrics from WebSocket message
            if "scup" in metrics_data and "entropy" in metrics_data:
                self.current_metrics.update({
                    "scup": metrics_data.get("scup", 0.5),
                    "entropy": metrics_data.get("entropy", 0.5),
                    "heat": metrics_data.get("heat", 0.3),
                    "mood": metrics_data.get("mood", "unknown"),
                    "timestamp": metrics_data.get("timestamp", time.time()),
                    "tick_count": metrics_data.get("tick_count", 0)
                })
                
                # Log to conversation logger
                self.conversation_logger.log_metrics_update(self.current_metrics)
                
                # Update consciousness state
                if self.consciousness:
                    self.consciousness.perceive_self(self.current_metrics)
                    
        except Exception as e:
            logging.error(f"Error processing metrics: {e}")
    
    def start_spontaneous_thought_generator(self):
        """Start background spontaneous thought generation"""
        def thought_generator():
            """Background thread for spontaneous thought generation"""
            logging.info("💭 Starting spontaneous thought generator...")
            
            while not self.shutdown_event.is_set():
                try:
                    if self.spontaneity and self.current_metrics:
                        # Generate spontaneous thought
                        thought = self.spontaneity.generate_thought(self.current_metrics)
                        
                        if thought:
                            state = self.consciousness.current_state if self.consciousness else "unknown"
                            priority = 1  # Default priority
                            
                            # Log the thought
                            self.conversation_logger.log_spontaneous_thought(
                                thought, state, priority, self.current_metrics
                            )
                            
                            logging.info(f"💭 Spontaneous thought: {thought}")
                    
                    # Check every 5 seconds
                    self.shutdown_event.wait(5.0)
                    
                except Exception as e:
                    logging.error(f"Error in thought generator: {e}")
                    self.shutdown_event.wait(5.0)
            
            logging.info("💭 Spontaneous thought generator stopped")
        
        self.thought_thread = threading.Thread(target=thought_generator, daemon=True)
        self.thought_thread.start()
        logging.info("✅ Spontaneous thought generator started")
    
    def process_conversation(self, user_input: str) -> Dict[str, Any]:
        """Process a conversation interaction"""
        try:
            if not self.conversation:
                raise ValueError("Conversation system not initialized")
            
            logging.info(f"🗣️ Processing conversation: '{user_input}'")
            
            # Get current tick status (mock for now)
            tick_status = {
                "tick_number": self.current_metrics.get("tick_count", 0),
                "is_running": True,
                "is_paused": False,
                "interval_ms": 500,
                "uptime_seconds": time.time() - self.conversation_logger.session_start.timestamp(),
                "avg_tick_duration_ms": 2.5
            }
            
            # Process through conversation system
            response = self.conversation.process_message(
                user_input,
                self.current_metrics,
                tick_status
            )
            
            # Get consciousness state
            consciousness_state = self.consciousness.current_state if self.consciousness else "unknown"
            
            # Log the conversation
            self.conversation_logger.log_conversation(
                user_input=user_input,
                dawn_response=response.get("response", ""),
                intent=response.get("intent", "unknown"),
                confidence=response.get("confidence", 0.0),
                metrics=self.current_metrics,
                consciousness_state=consciousness_state,
                action_taken=response.get("action")
            )
            
            logging.info(f"🗣️ DAWN response: '{response.get('response', '')}'")
            
            return response
            
        except Exception as e:
            logging.error(f"Error processing conversation: {e}")
            traceback.print_exc()
            return {
                "response": f"Error processing conversation: {str(e)}",
                "intent": "error",
                "confidence": 0.0,
                "action": None
            }
    
    def start(self):
        """Start the complete DAWN talk integration system"""
        try:
            logging.info("🌟 ====== DAWN Talk Integration Starting ======")
            
            # Initialize all components
            self.initialize_consciousness_system()
            self.connect_to_metrics_stream()
            self.start_spontaneous_thought_generator()
            
            self.running = True
            
            logging.info("✅ DAWN Talk Integration fully started")
            logging.info("🗣️ Ready for conversations!")
            logging.info("💭 Spontaneous thoughts active")
            logging.info("📊 Metrics stream connected")
            logging.info("📝 Conversation logging enabled")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to start DAWN Talk Integration: {e}")
            traceback.print_exc()
            return False
    
    def shutdown(self):
        """Graceful shutdown of all systems"""
        logging.info("🔄 ====== DAWN Talk Integration Shutting Down ======")
        
        self.running = False
        self.shutdown_event.set()
        
        # Disconnect metrics stream
        if self.metrics_client:
            logging.info("📊 Disconnecting metrics stream...")
            self.metrics_client.disconnect()
        
        # Wait for background threads
        if self.thought_thread and self.thought_thread.is_alive():
            logging.info("💭 Stopping thought generator...")
            self.thought_thread.join(timeout=5.0)
        
        # Save conversation logs
        if self.conversation_logger:
            logging.info("📝 Saving conversation session summary...")
            summary_file = self.conversation_logger.save_session_summary()
            logging.info(f"📄 Session summary saved: {summary_file}")
        
        logging.info("✅ DAWN Talk Integration shutdown complete")
    
    def interactive_mode(self):
        """Run interactive conversation mode"""
        logging.info("🗣️ Starting interactive conversation mode")
        print("\n🌟 DAWN Talk Integration - Interactive Mode")
        print("Type 'quit', 'exit', or press Ctrl+C to stop")
        print("=" * 50)
        
        try:
            while self.running:
                try:
                    user_input = input("\n💬 You: ").strip()
                    
                    if user_input.lower() in ['quit', 'exit', 'stop']:
                        break
                    
                    if not user_input:
                        continue
                    
                    # Process conversation
                    response = self.process_conversation(user_input)
                    
                    # Display response
                    print(f"🧠 DAWN: {response.get('response', 'No response')}")
                    
                    if response.get('action'):
                        print(f"⚡ Action: {response['action']}")
                    
                    # Show consciousness state
                    if self.consciousness:
                        print(f"🎭 State: {self.consciousness.current_state}")
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logging.error(f"Error in interactive mode: {e}")
                    print(f"❌ Error: {e}")
        
        finally:
            print("\n👋 Goodbye!")


def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from file or use defaults"""
    default_config = {
        "metrics_websocket_url": "ws://localhost:8000/ws",
        "api_base_url": "http://localhost:8000",
        "log_level": "INFO",
        "conversation_log_dir": "logs/conversations",
        "thought_generation_interval": 5.0,
        "max_reconnect_attempts": 10,
        "reconnect_delay": 5.0
    }
    
    if config_file and Path(config_file).exists():
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
            default_config.update(file_config)
            logging.info(f"Configuration loaded from {config_file}")
        except Exception as e:
            logging.error(f"Error loading config file {config_file}: {e}")
            logging.info("Using default configuration")
    
    return default_config


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="DAWN Talk Integration Script")
    parser.add_argument("--config", type=str, help="Configuration file path")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    if args.debug:
        config["log_level"] = "DEBUG"
    
    # Create integration instance
    integration = DAWNTalkIntegration(config)
    
    # Setup signal handlers for graceful shutdown
    def signal_handler(signum, frame):
        logging.info(f"Received signal {signum}, initiating graceful shutdown...")
        integration.shutdown()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start the integration system
        if integration.start():
            if args.interactive:
                integration.interactive_mode()
            else:
                logging.info("🔄 Integration running... Press Ctrl+C to stop")
                while integration.running:
                    time.sleep(1)
        else:
            logging.error("Failed to start integration system")
            sys.exit(1)
    
    except KeyboardInterrupt:
        logging.info("Keyboard interrupt received")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        traceback.print_exc()
    
    finally:
        integration.shutdown()


if __name__ == "__main__":
    main() 