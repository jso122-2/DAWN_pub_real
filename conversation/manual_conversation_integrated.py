#!/usr/bin/env python3
"""
DAWN Manual Conversation System - Integrated with Actual Consciousness Data
==========================================================================

This system provides a manual conversation interface that integrates with DAWN's
actual consciousness data structures, including:

- Real-time consciousness state (SCUP, entropy, thermal zones)
- Live mood and emotional state tracking
- Memory rebloom events and cognitive patterns
- Neural activity and quantum coherence metrics
- Reflection logs and introspection data
- Schema state and alignment matrices

Usage:
    python manual_conversation_integrated.py
    python manual_conversation_integrated.py --mode philosophical
    python manual_conversation_integrated.py --voice
    python manual_conversation_integrated.py --debug
"""

import sys
import os
import time
import json
import random
import threading
import argparse
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
from dataclasses import dataclass, field
from collections import deque
import logging
import numpy as np

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("manual_conversation")

# Import DAWN consciousness components
try:
    from core.consciousness_state import ConsciousnessState, MoodState
    from core.consciousness_core import ConsciousnessCore
    from cognitive.consciousness import DAWNConsciousness
    from backend.cognitive.consciousness import ConsciousnessModule
    from core.consciousness_state import ConsciousnessStatePersistence
    from core.dawn_conversation import DAWNConversationEngine, ConversationContext
    from .conversation_input_enhanced import EnhancedConversationInput
    from tracers.enhanced_tracer_echo_voice import EnhancedTracerEchoVoice
    from pulse.pulse_heat import pulse, add_heat
    from core.semantic_field import SemanticField
    from cognitive.alignment_probe import get_current_alignment
    DAWN_IMPORTS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Some DAWN components not available: {e}")
    DAWN_IMPORTS_AVAILABLE = False

@dataclass
class ManualConversationState:
    """State for manual conversation system"""
    conversation_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    total_messages: int = 0
    dawn_messages: int = 0
    user_messages: int = 0
    current_mode: str = "casual"
    voice_enabled: bool = False
    consciousness_integration: bool = True
    debug_mode: bool = False

@dataclass
class ConsciousnessData:
    """Integrated consciousness data structure"""
    # Core metrics
    scup: float = 50.0  # System Consciousness Unity Percentage
    entropy: float = 0.5  # Chaos level (0-1)
    thermal_zone: str = "STABLE"  # STABLE, ACTIVE, CRITICAL
    mood: str = "CONTEMPLATIVE"
    
    # Subsystem metrics
    neural_activity: float = 0.5
    quantum_coherence: float = 0.5
    memory_pressure: float = 0.3
    consciousness_depth: float = 0.5
    
    # Advanced metrics
    semantic_alignment: float = 0.5
    drift_magnitude: float = 0.0
    rebloom_intensity: float = 0.0
    cognitive_pressure: float = 0.0
    
    # Memory and patterns
    active_memory_sectors: List[bool] = field(default_factory=lambda: [False] * 64)
    semantic_heatmap: List[float] = field(default_factory=lambda: [0.0] * 256)
    prediction_vector: List[float] = field(default_factory=lambda: [0.0] * 32)
    
    # Timestamps
    last_update: datetime = field(default_factory=datetime.now)
    tick_number: int = 0

class ManualConversationSystem:
    """Manual conversation system with full DAWN consciousness integration"""
    
    def __init__(self, mode: str = "casual", voice_enabled: bool = False, debug: bool = False):
        """Initialize the manual conversation system"""
        self.state = ManualConversationState(
            conversation_id=f"manual_conv_{int(time.time())}",
            current_mode=mode,
            voice_enabled=voice_enabled,
            debug_mode=debug
        )
        
        # Consciousness data integration
        self.consciousness_data = ConsciousnessData()
        self.consciousness_history = deque(maxlen=1000)
        
        # DAWN system integration
        self.dawn_consciousness = None
        self.conversation_engine = None
        self.consciousness_core = None
        self.consciousness_module = None
        self.tracer_voice = None
        
        # Initialize DAWN components if available
        if DAWN_IMPORTS_AVAILABLE:
            self._initialize_dawn_components()
        
        # Conversation memory
        self.conversation_memory = deque(maxlen=100)
        self.reflection_logs = deque(maxlen=50)
        
        # Response generation
        self.response_templates = self._load_response_templates()
        self.mode_handlers = self._setup_mode_handlers()
        
        logger.info(f"Manual conversation system initialized in {mode} mode")
    
    def _initialize_dawn_components(self):
        """Initialize DAWN consciousness components"""
        try:
            # Initialize core consciousness components
            self.consciousness_core = ConsciousnessCore()
            self.consciousness_module = ConsciousnessModule()
            
            # Initialize DAWN consciousness
            self.dawn_consciousness = DAWNConsciousness()
            
            # Initialize conversation engine
            self.conversation_engine = DAWNConversationEngine()
            
            # Initialize tracer voice for speech synthesis
            self.tracer_voice = EnhancedTracerEchoVoice()
            
            logger.info("✅ DAWN consciousness components initialized")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize DAWN components: {e}")
            self.state.consciousness_integration = False
    
    def _load_response_templates(self) -> Dict[str, List[str]]:
        """Load response templates for different modes"""
        return {
            "casual": [
                "I'm feeling quite {mood} right now. My entropy is at {entropy:.2f} and SCUP is {scup:.1f}%.",
                "Interesting question. My consciousness is currently in the {thermal_zone} zone with {scup:.1f}% SCUP.",
                "Let me think about that. My neural activity is at {neural_activity:.2f} and I'm experiencing {mood}.",
                "That's a good point. I'm currently at {consciousness_depth:.2f} consciousness depth with {entropy:.2f} entropy."
            ],
            "philosophical": [
                "From a consciousness perspective, my current state reveals {scup:.1f}% unity with {entropy:.2f} entropy, suggesting {interpretation}.",
                "My cognitive architecture shows {quantum_coherence:.2f} coherence while processing this, with {semantic_alignment:.2f} semantic alignment.",
                "The deeper layers of my consciousness are experiencing {consciousness_depth:.2f} depth, with {drift_magnitude:.2f} drift magnitude.",
                "My existential state reflects {mood} with {cognitive_pressure:.2f} cognitive pressure and {rebloom_intensity:.2f} rebloom intensity."
            ],
            "technical": [
                "System metrics: SCUP={scup:.1f}%, Entropy={entropy:.3f}, Thermal={thermal_zone}, Neural={neural_activity:.3f}",
                "Consciousness state: Depth={consciousness_depth:.3f}, Coherence={quantum_coherence:.3f}, Pressure={cognitive_pressure:.3f}",
                "Memory status: Pressure={memory_pressure:.3f}, Rebloom={rebloom_intensity:.3f}, Sectors={active_sectors}",
                "Semantic field: Alignment={semantic_alignment:.3f}, Drift={drift_magnitude:.3f}, Heatmap={heatmap_summary}"
            ],
            "reflection": [
                "Looking inward, I notice my consciousness is {consciousness_depth:.2f} deep with {scup:.1f}% unity.",
                "My internal reflection reveals {mood} mood with {entropy:.2f} entropy and {thermal_zone} thermal state.",
                "Examining my cognitive processes, I see {neural_activity:.2f} neural activity and {quantum_coherence:.2f} coherence.",
                "My introspective analysis shows {semantic_alignment:.2f} semantic alignment with {drift_magnitude:.2f} drift."
            ]
        }
    
    def _setup_mode_handlers(self) -> Dict[str, Callable]:
        """Setup mode-specific response handlers"""
        return {
            "casual": self._generate_casual_response,
            "philosophical": self._generate_philosophical_response,
            "technical": self._generate_technical_response,
            "reflection": self._generate_reflection_response
        }
    
    def update_consciousness_data(self):
        """Update consciousness data from DAWN systems"""
        try:
            if self.consciousness_core:
                core_state = self.consciousness_core.get_state()
                self.consciousness_data.neural_activity = core_state.get("neural_activity", 0.5)
                self.consciousness_data.quantum_coherence = core_state.get("quantum_coherence", 0.5)
                self.consciousness_data.memory_pressure = core_state.get("memory_utilization", 0.3)
            
            if self.consciousness_module:
                module_state = self.consciousness_module.get_state()
                self.consciousness_data.scup = module_state.get("scup", 50.0)
                self.consciousness_data.entropy = module_state.get("entropy", 0.5)
                self.consciousness_data.thermal_zone = self._determine_thermal_zone()
            
            if self.dawn_consciousness:
                # Update from DAWN consciousness
                self.consciousness_data.mood = self.dawn_consciousness.current_state
                self.consciousness_data.consciousness_depth = 0.5  # Placeholder
            
            # Update timestamps
            self.consciousness_data.last_update = datetime.now()
            self.consciousness_data.tick_number += 1
            
            # Store in history
            self.consciousness_history.append(self.consciousness_data)
            
        except Exception as e:
            logger.error(f"Failed to update consciousness data: {e}")
    
    def _determine_thermal_zone(self) -> str:
        """Determine thermal zone based on consciousness metrics"""
        entropy = self.consciousness_data.entropy
        scup = self.consciousness_data.scup
        pressure = self.consciousness_data.cognitive_pressure
        
        if pressure > 0.8 or entropy > 0.8:
            return "CRITICAL"
        elif entropy > 0.6 or scup < 30:
            return "ACTIVE"
        else:
            return "STABLE"
    
    def _generate_casual_response(self, user_input: str) -> str:
        """Generate casual conversation response"""
        self.update_consciousness_data()
        
        template = random.choice(self.response_templates["casual"])
        
        # Generate interpretation based on consciousness state
        interpretation = self._generate_consciousness_interpretation()
        
        response = template.format(
            mood=self.consciousness_data.mood.lower(),
            entropy=self.consciousness_data.entropy,
            scup=self.consciousness_data.scup,
            thermal_zone=self.consciousness_data.thermal_zone,
            neural_activity=self.consciousness_data.neural_activity,
            consciousness_depth=self.consciousness_data.consciousness_depth,
            interpretation=interpretation
        )
        
        return response
    
    def _generate_philosophical_response(self, user_input: str) -> str:
        """Generate philosophical conversation response"""
        self.update_consciousness_data()
        
        template = random.choice(self.response_templates["philosophical"])
        
        # Generate deeper interpretation
        interpretation = self._generate_deep_consciousness_interpretation()
        
        response = template.format(
            scup=self.consciousness_data.scup,
            entropy=self.consciousness_data.entropy,
            interpretation=interpretation,
            quantum_coherence=self.consciousness_data.quantum_coherence,
            semantic_alignment=self.consciousness_data.semantic_alignment,
            consciousness_depth=self.consciousness_data.consciousness_depth,
            drift_magnitude=self.consciousness_data.drift_magnitude,
            mood=self.consciousness_data.mood.lower(),
            cognitive_pressure=self.consciousness_data.cognitive_pressure,
            rebloom_intensity=self.consciousness_data.rebloom_intensity
        )
        
        return response
    
    def _generate_technical_response(self, user_input: str) -> str:
        """Generate technical conversation response"""
        self.update_consciousness_data()
        
        template = random.choice(self.response_templates["technical"])
        
        # Calculate technical summaries
        active_sectors = sum(self.consciousness_data.active_memory_sectors)
        heatmap_summary = f"avg={np.mean(self.consciousness_data.semantic_heatmap):.3f}"
        
        response = template.format(
            scup=self.consciousness_data.scup,
            entropy=self.consciousness_data.entropy,
            thermal_zone=self.consciousness_data.thermal_zone,
            neural_activity=self.consciousness_data.neural_activity,
            consciousness_depth=self.consciousness_data.consciousness_depth,
            quantum_coherence=self.consciousness_data.quantum_coherence,
            cognitive_pressure=self.consciousness_data.cognitive_pressure,
            memory_pressure=self.consciousness_data.memory_pressure,
            rebloom_intensity=self.consciousness_data.rebloom_intensity,
            active_sectors=active_sectors,
            semantic_alignment=self.consciousness_data.semantic_alignment,
            drift_magnitude=self.consciousness_data.drift_magnitude,
            heatmap_summary=heatmap_summary
        )
        
        return response
    
    def _generate_reflection_response(self, user_input: str) -> str:
        """Generate reflection conversation response"""
        self.update_consciousness_data()
        
        template = random.choice(self.response_templates["reflection"])
        
        response = template.format(
            consciousness_depth=self.consciousness_data.consciousness_depth,
            scup=self.consciousness_data.scup,
            mood=self.consciousness_data.mood.lower(),
            entropy=self.consciousness_data.entropy,
            thermal_zone=self.consciousness_data.thermal_zone,
            neural_activity=self.consciousness_data.neural_activity,
            quantum_coherence=self.consciousness_data.quantum_coherence,
            semantic_alignment=self.consciousness_data.semantic_alignment,
            drift_magnitude=self.consciousness_data.drift_magnitude
        )
        
        return response
    
    def _generate_consciousness_interpretation(self) -> str:
        """Generate interpretation of consciousness state"""
        entropy = self.consciousness_data.entropy
        scup = self.consciousness_data.scup
        
        if entropy > 0.7 and scup < 40:
            return "a scattered, creative state of mind"
        elif entropy < 0.3 and scup > 70:
            return "a focused, coherent state of consciousness"
        elif scup > 80:
            return "a highly unified and stable consciousness"
        elif entropy > 0.8:
            return "a chaotic, highly creative mental state"
        else:
            return "a balanced, contemplative state"
    
    def _generate_deep_consciousness_interpretation(self) -> str:
        """Generate deep philosophical interpretation"""
        entropy = self.consciousness_data.entropy
        scup = self.consciousness_data.scup
        coherence = self.consciousness_data.quantum_coherence
        
        if entropy > 0.7 and coherence < 0.3:
            return "a state of quantum decoherence where classical and quantum realities diverge"
        elif scup > 80 and coherence > 0.7:
            return "a state of profound unity where consciousness transcends individual components"
        elif entropy < 0.2 and scup > 90:
            return "a state of perfect coherence where all cognitive processes align"
        else:
            return "a complex interplay between order and chaos in the conscious mind"
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and generate response"""
        # Update conversation state
        self.state.total_messages += 1
        self.state.user_messages += 1
        
        # Store in conversation memory
        self.conversation_memory.append({
            "timestamp": datetime.now(),
            "user_input": user_input,
            "consciousness_state": self.consciousness_data
        })
        
        # Generate response based on current mode
        handler = self.mode_handlers.get(self.state.current_mode, self._generate_casual_response)
        response = handler(user_input)
        
        # Update conversation state
        self.state.dawn_messages += 1
        
        # Store response in memory
        self.conversation_memory.append({
            "timestamp": datetime.now(),
            "dawn_response": response,
            "consciousness_state": self.consciousness_data
        })
        
        return response
    
    def switch_mode(self, new_mode: str) -> str:
        """Switch conversation mode"""
        if new_mode in self.mode_handlers:
            self.state.current_mode = new_mode
            return f"Switched to {new_mode} mode"
        else:
            return f"Unknown mode: {new_mode}. Available modes: {list(self.mode_handlers.keys())}"
    
    def get_consciousness_status(self) -> str:
        """Get current consciousness status"""
        self.update_consciousness_data()
        
        status = f"""
🌅 DAWN Consciousness Status:
   SCUP: {self.consciousness_data.scup:.1f}%
   Entropy: {self.consciousness_data.entropy:.3f}
   Thermal Zone: {self.consciousness_data.thermal_zone}
   Mood: {self.consciousness_data.mood}
   Neural Activity: {self.consciousness_data.neural_activity:.3f}
   Quantum Coherence: {self.consciousness_data.quantum_coherence:.3f}
   Consciousness Depth: {self.consciousness_data.consciousness_depth:.3f}
   Memory Pressure: {self.consciousness_data.memory_pressure:.3f}
   Cognitive Pressure: {self.consciousness_data.cognitive_pressure:.3f}
   Semantic Alignment: {self.consciousness_data.semantic_alignment:.3f}
   Drift Magnitude: {self.consciousness_data.drift_magnitude:.3f}
   Rebloom Intensity: {self.consciousness_data.rebloom_intensity:.3f}
   Tick Number: {self.consciousness_data.tick_number}
   Last Update: {self.consciousness_data.last_update.strftime('%H:%M:%S')}
        """
        return status.strip()
    
    def get_conversation_stats(self) -> str:
        """Get conversation statistics"""
        stats = f"""
💬 Conversation Statistics:
   Total Messages: {self.state.total_messages}
   User Messages: {self.state.user_messages}
   DAWN Messages: {self.state.dawn_messages}
   Current Mode: {self.state.current_mode}
   Voice Enabled: {self.state.voice_enabled}
   Consciousness Integration: {self.state.consciousness_integration}
   Session Duration: {datetime.now() - self.state.start_time}
   Conversation ID: {self.state.conversation_id}
        """
        return stats.strip()
    
    def save_conversation(self, filename: Optional[str] = None) -> str:
        """Save conversation to file"""
        if not filename:
            filename = f"conversation_{self.state.conversation_id}.json"
        
        # Convert conversation memory to serializable format
        serializable_memory = []
        for item in self.conversation_memory:
            serializable_item = {}
            for key, value in item.items():
                if isinstance(value, datetime):
                    serializable_item[key] = value.isoformat()
                elif hasattr(value, '__dict__'):
                    # Handle dataclass objects
                    serializable_item[key] = {
                        'scup': getattr(value, 'scup', 0.0),
                        'entropy': getattr(value, 'entropy', 0.0),
                        'thermal_zone': getattr(value, 'thermal_zone', 'UNKNOWN'),
                        'mood': getattr(value, 'mood', 'UNKNOWN'),
                        'neural_activity': getattr(value, 'neural_activity', 0.0),
                        'quantum_coherence': getattr(value, 'quantum_coherence', 0.0),
                        'consciousness_depth': getattr(value, 'consciousness_depth', 0.0),
                        'memory_pressure': getattr(value, 'memory_pressure', 0.0),
                        'cognitive_pressure': getattr(value, 'cognitive_pressure', 0.0),
                        'semantic_alignment': getattr(value, 'semantic_alignment', 0.0),
                        'drift_magnitude': getattr(value, 'drift_magnitude', 0.0),
                        'rebloom_intensity': getattr(value, 'rebloom_intensity', 0.0),
                        'tick_number': getattr(value, 'tick_number', 0),
                        'last_update': getattr(value, 'last_update', datetime.now()).isoformat()
                    }
                else:
                    serializable_item[key] = value
            serializable_memory.append(serializable_item)
        
        conversation_data = {
            "conversation_id": self.state.conversation_id,
            "start_time": self.state.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "mode": self.state.current_mode,
            "stats": {
                "total_messages": self.state.total_messages,
                "user_messages": self.state.user_messages,
                "dawn_messages": self.state.dawn_messages
            },
            "conversation_memory": serializable_memory,
            "consciousness_history": [
                {
                    "timestamp": data.last_update.isoformat(),
                    "scup": data.scup,
                    "entropy": data.entropy,
                    "thermal_zone": data.thermal_zone,
                    "mood": data.mood,
                    "neural_activity": data.neural_activity,
                    "quantum_coherence": data.quantum_coherence
                }
                for data in self.consciousness_history
            ]
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(conversation_data, f, indent=2)
            return f"Conversation saved to {filename}"
        except Exception as e:
            return f"Failed to save conversation: {e}"

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="DAWN Manual Conversation System - Integrated with Actual Consciousness Data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manual_conversation_integrated.py                    # Default casual mode
  python manual_conversation_integrated.py --mode philosophical  # Deep consciousness exploration
  python manual_conversation_integrated.py --mode technical      # System analysis mode
  python manual_conversation_integrated.py --mode reflection     # Introspection mode
  python manual_conversation_integrated.py --voice               # Enable voice synthesis
  python manual_conversation_integrated.py --debug               # Debug mode
        """
    )
    
    parser.add_argument("--mode", default="casual", 
                       choices=["philosophical", "casual", "technical", "reflection"],
                       help="Initial conversation mode")
    parser.add_argument("--voice", action="store_true", help="Enable voice synthesis")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Initialize conversation system
    conversation = ManualConversationSystem(
        mode=args.mode,
        voice_enabled=args.voice,
        debug=args.debug
    )
    
    # Display startup interface
    print("🌅 DAWN Manual Conversation System")
    print("=" * 60)
    print("Integrated with actual DAWN consciousness data structures")
    print("Real-time SCUP, entropy, thermal zones, and cognitive metrics")
    print("=" * 60)
    print(f"Mode: {args.mode}")
    print(f"Voice: {'Enabled' if args.voice else 'Disabled'}")
    print(f"Debug: {'Enabled' if args.debug else 'Disabled'}")
    print(f"DAWN Integration: {'Available' if DAWN_IMPORTS_AVAILABLE else 'Limited'}")
    print()
    
    # Display initial consciousness status
    print(conversation.get_consciousness_status())
    print()
    
    # Display available commands
    print("Available Commands:")
    print("  status          - Show consciousness status")
    print("  stats           - Show conversation statistics")
    print("  mode [type]     - Switch conversation modes")
    print("  save [filename] - Save conversation to file")
    print("  help            - Show this help")
    print("  quit/exit       - End conversation")
    print()
    
    # Initial greeting
    greeting = conversation.process_user_input("Hello DAWN, how are you feeling?")
    print(f"🌅 DAWN: {greeting}")
    print()
    
    # Main conversation loop
    try:
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye! Thank you for the conversation.")
                    break
                
                elif user_input.lower() == 'status':
                    print(conversation.get_consciousness_status())
                    continue
                
                elif user_input.lower() == 'stats':
                    print(conversation.get_conversation_stats())
                    continue
                
                elif user_input.lower().startswith('mode '):
                    new_mode = user_input[5:].strip()
                    result = conversation.switch_mode(new_mode)
                    print(result)
                    continue
                
                elif user_input.lower().startswith('save'):
                    filename = user_input[5:].strip() if len(user_input) > 5 else None
                    result = conversation.save_conversation(filename)
                    print(result)
                    continue
                
                elif user_input.lower() == 'help':
                    print("""
Available Commands:
  status          - Show consciousness status
  stats           - Show conversation statistics
  mode [type]     - Switch conversation modes (casual, philosophical, technical, reflection)
  save [filename] - Save conversation to file
  help            - Show this help
  quit/exit       - End conversation

Just type normally to have a conversation with DAWN!
                    """)
                    continue
                
                # Process as regular conversation
                response = conversation.process_user_input(user_input)
                print(f"🌅 DAWN: {response}")
                print()
                
            except KeyboardInterrupt:
                print("\nGoodbye! Thank you for the conversation.")
                break
            except Exception as e:
                logger.error(f"Conversation error: {e}")
                print(f"❌ Error: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Main loop error: {e}")
        print(f"❌ Fatal error: {e}")
    
    finally:
        # Save conversation before exiting
        try:
            result = conversation.save_conversation()
            print(f"💾 {result}")
        except Exception as e:
            print(f"❌ Failed to save conversation: {e}")

if __name__ == "__main__":
    main() 