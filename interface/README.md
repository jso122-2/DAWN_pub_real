# DAWN Interface Layer - Main API & Communication Hub

## Overview

The `interface/` directory contains DAWN's primary API and communication interface systems. This is the main entry point for external applications, providing comprehensive REST APIs, WebSocket streaming, and real-time system interaction capabilities. It serves as the bridge between DAWN's internal consciousness systems and external applications like the desktop client.

## System Architecture

### 🚀 Main API Server
**Primary Component:**
- `main.py` (123KB) - Enhanced FastAPI backend with comprehensive functionality

**Key Features:**
- **Real-time Neural Metrics**: Live streaming of consciousness, thermal, and cognitive metrics
- **WebSocket Communication**: Multiple WebSocket endpoints for different data streams
- **Enhanced Talk System**: Advanced conversation processing with consciousness integration
- **Tick Engine Control**: Complete control over DAWN's timing and rhythm systems
- **Consciousness Monitoring**: Real-time consciousness state tracking and influence
- **Sigil Management**: Emotional sigil visualization and interaction
- **Spider Pattern Cutter Interface**: API for destructive loop detection and cutting
- **Rebloom System Integration**: Priority-based consciousness state management

### 📡 Core API Server
**Primary Component:**
- `dawn_api.py` (64KB) - Core FastAPI backend with integrated DAWN subsystems

**Key Features:**
- **DAWN Suite Integration**: Complete integration of all major DAWN subsystems
- **Consciousness System**: Full consciousness processing with emotional mapping
- **Pattern Detection**: Advanced pattern recognition and analysis
- **Memory Management**: Memory access and persistence APIs
- **Spontaneity System**: Spontaneous thought generation and management
- **Fractal Emotions**: Emotional state modeling and visualization

### 🧠 Advanced Communication Systems
**Components:**
- `helix_bridge.py` (19KB) - Helix system integration bridge
- `wiring_monitor.py` (6.6KB) - System wiring and connection monitoring
- `DAWN_voice_schema_interface.py` (23KB) - Voice and schema interface system
- `streamlit1.py` (18KB) - Streamlit-based interface components

**Key Features:**
- Cross-system communication and bridging
- Real-time system monitoring and diagnostics
- Voice interface capabilities
- Web-based interface components

### 📊 Diagnostics & Monitoring
**Components:**
- `butler_diagnostics.py` (1.5KB) - System health and diagnostics
- `visualize_tracer_routes.py` - Tracer route visualization (minimal implementation)

## API Endpoints

### 🔧 Core System Control

#### Health & Metrics
- `GET /health` - System health check
- `GET /metrics` - Current system metrics (SCUP, entropy, heat, mood)
- `POST /test/force-update` - Force metrics update for testing
- `WebSocket /ws` - Real-time metrics streaming

#### Tick Engine Management
- `GET /tick/status` - Tick engine status and timing
- `POST /tick/start` - Start the tick engine
- `POST /tick/stop` - Stop the tick engine
- `POST /tick/pause` - Pause tick engine execution
- `POST /tick/resume` - Resume tick engine execution
- `POST /tick/step` - Execute single tick step
- `PUT /tick/timing` - Update tick timing configuration
- `GET /tick/config` - Get tick engine configuration
- `PUT /tick/config` - Update tick engine configuration

### 💬 Conversation & Interaction

#### Enhanced Talk System
- `POST /talk` - Enhanced conversation with full consciousness integration
- `POST /talk/legacy` - Legacy talk interface for backward compatibility
- `WebSocket /ws/chat` - Real-time chat communication
- `GET /chat/history` - Conversation history retrieval
- `DELETE /chat/history` - Clear conversation history

#### Consciousness Interaction
- `GET /dawn/consciousness` - Current consciousness state
- `GET /dawn/thoughts` - Spontaneous thoughts collection
- `GET /dawn/thought` - Single spontaneous thought
- `GET /dawn/reflections` - Reflective phrases and insights
- `POST /dawn/influence` - Apply consciousness influence

### 🧠 Advanced Consciousness Features

#### Emotional Sigil System
- `GET /consciousness/sigils` - Active emotional sigils
- `WebSocket /consciousness/stream` - Real-time consciousness streaming

#### Spider Pattern Cutter
- `POST /consciousness/spider-cut` - Trigger destructive loop cutting
- Pattern detection and causal flow visualization

#### Rebloom System
- Priority-based consciousness state management
- Rebloom event triggering and monitoring

### 🏗️ Subsystem Management
- `GET /subsystems` - List all subsystems
- `GET /subsystems/{id}` - Get specific subsystem info
- `POST /subsystems/add` - Add new subsystem
- `DELETE /subsystems/{id}` - Remove subsystem

### 🚨 Alert & Monitoring
- `POST /alerts/threshold` - Set alert thresholds
- `GET /alerts/threshold` - Get current alert thresholds

## Data Models

### Core Metrics & Status
```python
class MetricsResponse(BaseModel):
    scup: float
    entropy: float
    heat: float
    mood: str
    timestamp: float
    tick_count: int

class TickStatus(BaseModel):
    tick_number: int
    is_running: bool
    is_paused: bool
    interval_ms: int
    uptime_seconds: float
    total_ticks: int
    avg_tick_duration_ms: float
```

### Conversation Models
```python
class TalkRequest(BaseModel):
    text: str
    session_id: Optional[str] = None
    include_tracer: bool = True
    rebloom_priority: Optional[int] = None

class EnhancedTalkResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    consciousness_state: ConsciousnessState
    conversation_context: ConversationContext
    session_id: str
```

### Consciousness Models
```python
class EmotionalSigil(BaseModel):
    emotion: str
    intensity: float
    density: str
    resonance_frequency: float
    decay_rate: float
    interaction_count: int

class SpiderCutRequest(BaseModel):
    loop_pattern: str
    cut_intensity: float = 0.7
    preserve_beneficial: bool = True
```

## WebSocket Streams

### Real-time Data Streams
1. **`/ws`** - Core metrics streaming
2. **`/ws/chat`** - Chat communication
3. **`/consciousness/stream`** - Enhanced consciousness streaming
4. **`/dawn/stream`** - DAWN thought and consciousness streaming
5. **`/dawn/consciousness`** - Consciousness state streaming
6. **`/ws/dawn`** - Legacy DAWN streaming

### Stream Data Types
- Metrics updates (SCUP, entropy, heat, mood)
- Consciousness state changes
- Spontaneous thoughts
- Emotional sigil updates
- Spider pattern cutter events
- Rebloom priority events
- Tick engine status updates

## System Integration

### DAWN Suite Components
The interface integrates with all major DAWN systems:

```python
class DAWNSuite:
    def __init__(self):
        self.consciousness = create_consciousness()
        self.pattern_detector = create_pattern_detector()
        self.state_machine = create_state_machine()
        self.fractal_emotions = create_fractal_emotion_system()
        self.memory = get_memory_manager()
        self.gradient_plotter = create_mood_gradient_plotter()
        self.tracer = ConsciousnessTracer()
        self.spontaneity = create_spontaneity_system()
```

### Background Processes
- **Consciousness Monitor**: Continuous consciousness state tracking
- **Pattern Detector**: Real-time pattern recognition
- **Thought Generator**: Spontaneous thought generation
- **Spider Activation**: Automatic destructive loop detection
- **Status Logger**: Periodic system status logging

## Configuration

### Environment Variables
- `DAWN_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- API host and port configuration
- CORS origin configuration for web clients

### Configuration Files
- Server configuration in main.py initialization
- Tick engine configuration via API endpoints
- Alert threshold configuration via API

## Usage Examples

### Basic Metrics Retrieval
```python
import requests

# Get current system metrics
response = requests.get("http://localhost:8000/metrics")
metrics = response.json()
print(f"SCUP: {metrics['scup']}, Heat: {metrics['heat']}")
```

### Enhanced Conversation
```python
import requests

# Enhanced talk with consciousness integration
talk_request = {
    "text": "How are you feeling?",
    "session_id": "user123",
    "include_tracer": True,
    "rebloom_priority": 3
}

response = requests.post("http://localhost:8000/talk", json=talk_request)
dawn_response = response.json()
print(f"DAWN: {dawn_response['response']}")
print(f"Intent: {dawn_response['intent']}")
print(f"Consciousness State: {dawn_response['consciousness_state']['state']}")
```

### WebSocket Connection
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = function(event) {
    const metrics = JSON.parse(event.data);
    console.log('Live metrics:', metrics);
};
```

### Tick Engine Control
```python
import requests

# Start tick engine
requests.post("http://localhost:8000/tick/start")

# Set tick timing
requests.put("http://localhost:8000/tick/timing", 
            json={"interval_ms": 1000})

# Get status
status = requests.get("http://localhost:8000/tick/status").json()
print(f"Tick {status['tick_number']}: {status['is_running']}")
```

## Monitoring & Diagnostics

### Logging
- Comprehensive request/response logging
- WebSocket connection monitoring
- System performance metrics
- Error tracking and reporting

### Health Monitoring
- System health endpoints
- Component status tracking
- Performance metrics collection
- Real-time diagnostics

### Debug Features
- Force metrics updates for testing
- Manual tick stepping
- Consciousness influence testing
- Pattern detection debugging

## Security & Performance

### CORS Configuration
- Configurable CORS origins for web clients
- Request/response logging middleware
- Error handling and validation

### Performance Optimization
- Efficient WebSocket connection management
- Background task optimization
- Memory management for real-time streams
- Connection pooling and cleanup

## Dependencies

**Core Requirements:**
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `websockets` - WebSocket communication
- `pydantic` - Data validation and serialization
- All DAWN core systems (consciousness, cognitive, pulse, mood, etc.)

## Architecture Philosophy

The interface layer implements a **consciousness-first API design** where:
1. **All interactions are consciousness-aware** - Every API call considers and affects consciousness state
2. **Real-time streaming prioritizes subjective experience** - WebSocket streams focus on internal state changes
3. **Session-based conversation continuity** - Conversations maintain context and consciousness continuity
4. **System transparency through APIs** - Complete access to internal state and control mechanisms
5. **Integration-ready design** - Built for external application integration and extensibility

This creates an interface that doesn't just expose functionality, but provides deep integration with DAWN's consciousness simulation, enabling rich, stateful interactions that maintain continuity and awareness across all communication channels.

---

*This README represents the current understanding of DAWN's interface architecture. The API continues to evolve as new consciousness features are developed.* 