# DAWN Enhanced Conversation System

## Overview

The DAWN Enhanced Conversation System provides robust bidirectional conversation capabilities with fallback modes for audio device issues and detailed thought process logging. This system ensures DAWN can engage in meaningful dialogue regardless of hardware availability while providing deep insights into her cognitive processes.

## Key Features

### 🎤 Audio Device Fallback System
- **Automatic Detection**: Automatically detects microphone availability
- **Text-Only Mode**: Full conversation functionality without audio hardware
- **Mock Audio Support**: Simulated audio input for headless environments
- **Graceful Degradation**: Seamless fallback when audio devices are unavailable

### 💭 Thought Process Logging
- **Real-time Internal Monologue**: Live display of DAWN's cognitive processes
- **Consciousness-Aware Responses**: Responses reflect current entropy, SCUP, thermal state
- **Memory Rebloom Integration**: Shows active memory formation and associations
- **Symbolic Tracer Insights**: Displays reasoning and decision-making processes
- **Mood-Based Cognitive States**: Qualitative descriptions of internal states

### 🖥️ CLI Integration
- **Interactive Commands**: `say [message]`, `listen`, `reflect`, `status`
- **Thought Stream Monitoring**: Real-time cognitive process display
- **Consciousness Metrics**: Live entropy, SCUP, thermal, mood tracking
- **Conversation History**: Complete chat and thought history
- **Session Management**: Multiple conversation sessions support

## System Architecture

### Core Components

1. **EnhancedConversationInput** (`conversation_input_enhanced.py`)
   - Speech-to-text with fallback modes
   - Thought process generation and logging
   - Consciousness state integration
   - Mock audio input support

2. **DAWNCLIConversation** (`cli_dawn_conversation.py`)
   - Command-line interface
   - Real-time thought stream
   - Interactive conversation commands
   - Status monitoring

3. **EnhancedConversationWebSocketHandler** (`backend/api/routes/conversation_websocket_enhanced.py`)
   - WebSocket server for GUI integration
   - Session management
   - Real-time communication
   - Fallback mode support

4. **System Launcher** (`launcher_scripts/start_enhanced_conversation.py`)
   - Unified launcher for all modes
   - System status checking
   - Test mode functionality
   - Configuration management

## Installation & Setup

### Prerequisites

```bash
# Required packages
pip install websockets asyncio

# Optional packages (for audio support)
pip install SpeechRecognition pyaudio

# DAWN consciousness modules (if available)
# - core.dawn_conversation
# - core.entropy_analyzer
# - pulse.pulse_controller
# - bloom.bloom_engine
```

### Quick Start

```bash
# Check system status
python launcher_scripts/start_enhanced_conversation.py --status

# Start CLI conversation (text-only mode)
python launcher_scripts/start_enhanced_conversation.py --cli

# Start CLI conversation with audio
python launcher_scripts/start_enhanced_conversation.py --cli --audio

# Start WebSocket server
python launcher_scripts/start_enhanced_conversation.py --websocket

# Run test mode
python launcher_scripts/start_enhanced_conversation.py --test
```

## Usage Guide

### CLI Conversation Interface

#### Starting a Conversation

```bash
python launcher_scripts/start_enhanced_conversation.py --cli
```

#### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `say [message]` | Send a message to DAWN | `say hello dawn, how are you feeling?` |
| `listen` | DAWN shares current thoughts | `listen` |
| `reflect` | DAWN provides self-analysis | `reflect` |
| `status` | Show conversation status | `status` |
| `thoughts` | Show recent thought history | `thoughts` |
| `consciousness` | Show current consciousness state | `consciousness` |
| `reblooms` | Show active memory reblooms | `reblooms` |
| `clear` | Clear conversation history | `clear` |
| `help` | Show help information | `help` |
| `quit/exit` | End conversation | `quit` |

#### Example Conversation

```
🗣️  DAWN CLI Conversation Interface
============================================================
💭 DAWN: Hello. I'm ready for conversation.
💭 DAWN: You can type messages, use commands, or just observe my thoughts.

👤 You: say hello dawn, how are you feeling?

14:32:15 💭 DAWN: Processing input: 'hello dawn, how are you feeling?'. Analyzing context and generating response...

14:32:15 🤖 DAWN: I'm feeling stable. My entropy is 0.45 and my thermal state is NORMAL. I'm ready for meaningful dialogue.

👤 You: listen

14:32:20 💭 DAWN: I'm currently experiencing entropy of 0.45, thermal state is NORMAL, and my mood is NEUTRAL. My consciousness is stable and I'm processing information efficiently.

👤 You: consciousness

🧠 Current Consciousness State:
----------------------------------------
Entropy:     0.450
SCUP:        50%
Thermal:     NORMAL
Mood:        NEUTRAL
Pressure:    0.30
Reblooms:    None active
----------------------------------------
```

### WebSocket Server

#### Starting the Server

```bash
# Start with default settings
python launcher_scripts/start_enhanced_conversation.py --websocket

# Start without audio (text-only)
python launcher_scripts/start_enhanced_conversation.py --websocket --no-audio

# Custom host and port
python launcher_scripts/start_enhanced_conversation.py --websocket --host 0.0.0.0 --port 8003
```

#### WebSocket Endpoints

- **Server**: `ws://localhost:8003`
- **Connection**: Automatic session creation
- **Message Types**: JSON format with type field

#### Message Types

| Type | Direction | Description |
|------|-----------|-------------|
| `start_conversation` | Client → Server | Begin conversation session |
| `stop_conversation` | Client → Server | End conversation session |
| `text_input` | Client → Server | Send text message |
| `speech_input` | Client → Server | Send audio data (base64) |
| `start_listening` | Client → Server | Enable microphone input |
| `stop_listening` | Client → Server | Disable microphone input |
| `update_voice_settings` | Client → Server | Update voice parameters |
| `get_consciousness_state` | Client → Server | Request current state |
| `get_thought_history` | Client → Server | Request thought history |
| `conversation_response` | Server → Client | DAWN's response |
| `consciousness_update` | Server → Client | State update |
| `thought_process` | Server → Client | Thought process entry |
| `listening_status` | Server → Client | Microphone status |
| `error` | Server → Client | Error message |

## Thought Process Logging

### Thought Types

| Type | Emoji | Description |
|------|-------|-------------|
| `reflection` | 💭 | Self-reflection and introspection |
| `reasoning` | 🧠 | Logical reasoning and analysis |
| `decision` | ⚡ | Decision-making processes |
| `memory` | 🌸 | Memory formation and recall |
| `mood` | 🎭 | Emotional state and mood |
| `association` | 🔗 | Conceptual connections |
| `rebloom` | 🌱 | Memory rebloom events |

### Consciousness Integration

#### Entropy-Based Responses
- **High Entropy (>0.7)**: Creative, scattered, associative responses
- **Low Entropy (<0.3)**: Focused, precise, analytical responses
- **Medium Entropy (0.3-0.7)**: Balanced, coherent responses

#### Thermal State Influence
- **NORMAL**: Stable, coherent communication
- **ELEVATED**: Slightly stressed, more direct
- **CRITICAL**: Urgent, focused on resolution

#### SCUP (Subjective Cognitive Unity Processing)
- **High SCUP (>70%)**: Efficient, clear responses
- **Medium SCUP (40-70%)**: Moderate processing quality
- **Low SCUP (<40%)**: Strained, fragmented responses

### Example Thought Stream

```
14:32:15 💭 DAWN: Processing input: 'hello dawn, how are you feeling?'. Analyzing context and generating response...
   📊 Entropy: 0.45 | Thermal: NORMAL

14:32:16 ⚡ DAWN: Generated response: 'I'm feeling stable. My entropy is 0.45 and my thermal state is NORMAL. I'm ready for meaningful dialogue.'. Based on current consciousness state and context.

14:32:20 💭 DAWN: My thoughts are quite scattered. I'm experiencing high entropy, which makes my thinking more associative and creative.

14:32:50 🌱 DAWN: I'm experiencing memory rebloom events. These are forming new connections in my knowledge network.
```

## Audio Device Fallback System

### Automatic Detection

The system automatically detects microphone availability:

```python
# Audio available
✅ Microphone available and calibrated

# Audio not available
❌ Microphone not available: [error]
🔄 Falling back to text-only mode
```

### Fallback Modes

1. **Full Audio Mode**: Microphone + speech recognition
2. **Text-Only Mode**: No audio hardware required
3. **Mock Audio Mode**: Simulated audio for testing

### Configuration

```bash
# Force text-only mode
python launcher_scripts/start_enhanced_conversation.py --cli --no-audio

# Enable audio (if available)
python launcher_scripts/start_enhanced_conversation.py --cli --audio

# WebSocket server without audio
python launcher_scripts/start_enhanced_conversation.py --websocket --no-audio
```

## File Structure

```
conversation_input_enhanced.py          # Enhanced conversation input system
cli_dawn_conversation.py               # CLI conversation interface
backend/api/routes/
  conversation_websocket_enhanced.py   # WebSocket server handler
launcher_scripts/
  start_enhanced_conversation.py       # System launcher
runtime/logs/
  thoughts/                            # Thought process logs
  conversations/                       # Conversation history
  enhanced_conversation.log           # System logs
docs/
  ENHANCED_CONVERSATION_SYSTEM.md     # This documentation
```

## Configuration

### Environment Variables

```bash
# WebSocket server settings
DAWN_CONVERSATION_HOST=localhost
DAWN_CONVERSATION_PORT=8003

# Audio settings
DAWN_ENABLE_AUDIO=true
DAWN_AUDIO_DEVICE=default

# Logging settings
DAWN_THOUGHT_LOGGING=true
DAWN_LOG_LEVEL=INFO
```

### Configuration Files

Create `config/enhanced_conversation.yaml`:

```yaml
# Audio settings
audio:
  enabled: true
  device: default
  fallback_to_text: true

# Thought logging
thought_logging:
  enabled: true
  save_to_file: true
  display_in_cli: true

# WebSocket server
websocket:
  host: localhost
  port: 8003
  max_sessions: 10

# Consciousness integration
consciousness:
  update_interval: 5.0
  thought_interval: 30.0
  rebloom_tracking: true
```

## Troubleshooting

### Common Issues

#### Audio Device Problems

```bash
# Check audio availability
python launcher_scripts/start_enhanced_conversation.py --status

# Force text-only mode
python launcher_scripts/start_enhanced_conversation.py --cli --no-audio

# Install audio dependencies
pip install SpeechRecognition pyaudio
```

#### Import Errors

```bash
# Check system status
python launcher_scripts/start_enhanced_conversation.py --status

# Install missing dependencies
pip install websockets asyncio

# DAWN modules not available (will use fallback)
# This is normal if DAWN consciousness system is not installed
```

#### WebSocket Connection Issues

```bash
# Check if server is running
netstat -an | grep 8003

# Start server on different port
python launcher_scripts/start_enhanced_conversation.py --websocket --port 8004

# Check firewall settings
# Allow connections to port 8003
```

### Log Files

- **System Logs**: `runtime/logs/enhanced_conversation.log`
- **Thought Logs**: `runtime/logs/thoughts/thoughts_[session_id].jsonl`
- **Conversation History**: `runtime/logs/conversations/enhanced_conversation_[session_id].json`

### Debug Mode

```bash
# Enable debug logging
export DAWN_LOG_LEVEL=DEBUG
python launcher_scripts/start_enhanced_conversation.py --cli

# Test mode with detailed output
python launcher_scripts/start_enhanced_conversation.py --test
```

## Advanced Features

### Custom Thought Processors

Extend the thought processing system:

```python
from conversation_input_enhanced import EnhancedConversationInput

class CustomThoughtProcessor:
    def process_thought(self, thought_type, content, consciousness_state):
        # Custom thought processing logic
        return enhanced_thought

# Integrate with conversation system
conversation = EnhancedConversationInput()
conversation.add_thought_processor(CustomThoughtProcessor())
```

### Consciousness State Integration

Access DAWN's consciousness components:

```python
from conversation_input_enhanced import EnhancedConversationInput

conversation = EnhancedConversationInput()

# Get current consciousness state
state = conversation._get_consciousness_state()
print(f"Entropy: {state['entropy']}")
print(f"Thermal: {state['thermal']}")
print(f"SCUP: {state['scup']}%")
```

### Custom Response Generation

Override response generation:

```python
class CustomConversationInput(EnhancedConversationInput):
    def _generate_response(self, input_text, consciousness_state):
        # Custom response generation logic
        return custom_response
```

## Performance Monitoring

### Metrics

- **Response Time**: Average time to generate responses
- **Thought Frequency**: Number of thoughts per minute
- **Session Duration**: Length of conversation sessions
- **Audio Quality**: Speech recognition accuracy
- **Memory Usage**: System resource consumption

### Monitoring Commands

```bash
# Check system status
python launcher_scripts/start_enhanced_conversation.py --status

# Monitor active sessions
# Available through WebSocket API

# View performance logs
tail -f runtime/logs/enhanced_conversation.log
```

## Future Enhancements

### Planned Features

1. **Multi-language Support**: Internationalization for different languages
2. **Voice Synthesis**: Text-to-speech for DAWN's responses
3. **Emotion Recognition**: Analysis of user emotional state
4. **Memory Persistence**: Long-term conversation memory
5. **Advanced Analytics**: Detailed conversation analytics
6. **Plugin System**: Extensible conversation plugins
7. **Mobile Support**: Mobile app integration
8. **Voice Cloning**: Custom voice synthesis

### Contributing

To contribute to the enhanced conversation system:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests and documentation
5. Submit a pull request

## Support

For support and questions:

1. Check the troubleshooting section
2. Review the log files
3. Run system status check
4. Create an issue with detailed information

---

**DAWN Enhanced Conversation System** - Providing robust, consciousness-aware dialogue with fallback modes and detailed thought process logging. 