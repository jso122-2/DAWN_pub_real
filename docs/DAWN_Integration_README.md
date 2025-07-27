# DAWN Talk Integration System

**Bridge between tick engine and consciousness layer**

A comprehensive integration script that manages conversation flow, spontaneous thoughts, and metrics integration for the DAWN (Distributed Autonomous Waking Network) consciousness system.

## 🌟 Features

- **Full DAWN consciousness system initialization**
- **Real-time metrics stream connection**
- **Background spontaneous thought generation** 
- **Comprehensive conversation logging and analysis**
- **Graceful shutdown handling**
- **Configuration management**
- **Interactive conversation mode**
- **WebSocket streaming support**

## 📋 Requirements

### Core Dependencies
```bash
pip install websocket-client requests urllib3
```

### DAWN Modules Required
- `cognitive.consciousness` - DAWNConsciousness
- `cognitive.conversation` - DAWNConversation  
- `cognitive.spontaneity` - DAWNSpontaneity

## 🚀 Quick Start

### 1. Basic Usage
```bash
python dawn_integration.py
```

### 2. With Custom Configuration
```bash
python dawn_integration.py --config dawn_config.json
```

### 3. Interactive Mode
```bash
python dawn_integration.py --interactive
```

### 4. Debug Mode
```bash
python dawn_integration.py --debug --interactive
```

## 📁 File Structure

```
├── dawn_integration.py      # Main integration script
├── dawn_config.json         # Configuration file
├── DAWN_Integration_README.md
└── logs/
    ├── conversations/       # Conversation logs
    │   ├── conversations_YYYYMMDD_HHMMSS.log
    │   └── session_summary_YYYYMMDD_HHMMSS.json
    └── dawn_integration_YYYYMMDD_HHMMSS.log
```

## ⚙️ Configuration

The system uses `dawn_config.json` for configuration. Key sections:

### API Endpoints
```json
{
  "api_endpoints": {
    "metrics_websocket_url": "ws://localhost:8000/ws",
    "api_base_url": "http://localhost:8000",
    "talk_endpoint": "http://localhost:8000/talk",
    "thoughts_endpoint": "http://localhost:8000/dawn/thoughts",
    "stream_websocket_url": "ws://localhost:8000/dawn/stream"
  }
}
```

### Logging Configuration
```json
{
  "logging": {
    "log_level": "INFO",
    "conversation_log_dir": "logs/conversations",
    "enable_file_logging": true,
    "enable_console_logging": true
  }
}
```

### Spontaneous Thoughts
```json
{
  "spontaneous_thoughts": {
    "thought_generation_interval": 5.0,
    "max_thoughts_in_buffer": 20,
    "cooldown_periods": {
      "default_cooldown_seconds": 300,
      "milestone_cooldown_seconds": 900,
      "critical_cooldown_seconds": 60
    }
  }
}
```

## 🧠 Architecture

### Main Components

#### 1. **DAWNTalkIntegration**
- Main orchestrator class
- Manages all subsystems
- Handles lifecycle events

#### 2. **ConversationLogger**
- Enhanced logging system
- Conversation analysis
- Session summaries
- Metrics tracking

#### 3. **MetricsStreamClient**
- WebSocket connection to metrics
- Auto-reconnection
- Real-time data streaming

#### 4. **DAWN Consciousness System**
- `DAWNConsciousness` - Core consciousness
- `DAWNConversation` - Conversation processing
- `DAWNSpontaneity` - Thought generation

### Integration Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Tick Engine   │───▶│  Metrics Stream  │───▶│  Integration    │
└─────────────────┘    └──────────────────┘    │     Script      │
                                               └─────────────────┘
                                                        │
                       ┌─────────────────────────────────┼─────────────────────────────────┐
                       │                                 │                                 │
                       ▼                                 ▼                                 ▼
              ┌─────────────────┐              ┌─────────────────┐               ┌─────────────────┐
              │ Consciousness   │              │  Conversation   │               │   Spontaneity   │
              │    System       │              │     System      │               │     System      │
              └─────────────────┘              └─────────────────┘               └─────────────────┘
                       │                                 │                                 │
                       └─────────────────────────────────┼─────────────────────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────┐
                                               │   Conversation  │
                                               │     Logger      │
                                               └─────────────────┘
```

## 🗣️ Usage Examples

### Interactive Conversation
```
🌟 DAWN Talk Integration - Interactive Mode
Type 'quit', 'exit', or press Ctrl+C to stop
==================================================

💬 You: How are you feeling?
🧠 DAWN: Currently stable. Equilibrium maintained at SCUP: 0.653
🎭 State: stable

💬 You: Can you speed up the tick engine?
🧠 DAWN: Increasing tick rate
⚡ Action: speedup
🎭 State: focused

💬 You: quit
👋 Goodbye!
```

### Command Line Arguments
```bash
# Start with debug logging
python dawn_integration.py --debug

# Use custom config file
python dawn_integration.py --config my_config.json

# Run in interactive mode with debug
python dawn_integration.py --interactive --debug

# Background service mode
python dawn_integration.py --config production_config.json
```

## 📊 Logging and Analysis

### Conversation Logs
Every conversation is logged with:
- **User input** and **DAWN response**
- **Intent recognition** and **confidence scores**
- **Consciousness state** at time of interaction
- **Actions taken** (if any)
- **Current metrics** (SCUP, entropy, heat)

### Spontaneous Thought Logs
Thoughts are logged with:
- **Thought content** and **priority level**
- **Consciousness state** when generated
- **Current metrics** context
- **Timestamp** and **generation triggers**

### Analysis Features
- **Intent distribution** analysis
- **Consciousness state** tracking
- **Average confidence** scoring
- **Action execution** summaries
- **Session duration** and **interaction counts**

### Sample Log Output
```
2024-01-15 14:30:25 - dawn.conversations - INFO - CONVERSATION | User: 'How are you?' | DAWN: 'Currently stable. SCUP at 0.653' | Intent: query_state (0.85) | State: stable | Action: None

2024-01-15 14:30:45 - dawn.conversations - INFO - SPONTANEOUS_THOUGHT | Priority: 1 | State: stable | 'In stability, I sense the potential for emergence.'

2024-01-15 14:31:05 - dawn.conversations - INFO - ANALYSIS | Last 10 conversations | Avg confidence: 0.742 | Intent distribution: {'query_state': 4, 'query_metrics': 3, 'command_faster': 2, 'social': 1} | State distribution: {'stable': 6, 'focused': 3, 'reflective': 1}
```

## 🔧 Integration with FastAPI

### Required FastAPI Endpoints
The integration script expects these endpoints to be available:

1. **WebSocket `/ws`** - Metrics streaming
2. **POST `/talk`** - Conversation processing
3. **GET `/dawn/thoughts`** - Spontaneous thoughts retrieval
4. **WebSocket `/dawn/stream`** - Real-time thought streaming

### Metrics Stream Format
```json
{
  "scup": 0.653,
  "entropy": 0.412,
  "heat": 0.287,
  "mood": "stable",
  "timestamp": 1642259400.0,
  "tick_count": 1250
}
```

## 🛠️ Advanced Features

### Signal Handling
- **SIGINT** (Ctrl+C) - Graceful shutdown
- **SIGTERM** - Service termination
- **Session summary** generation on exit

### Error Recovery
- **Automatic reconnection** to metrics stream
- **Conversation error** handling and logging
- **Thread management** and cleanup
- **Resource monitoring** and limits

### Performance Monitoring
- **Memory usage** tracking
- **CPU utilization** monitoring
- **Thread count** management
- **Garbage collection** optimization

## 📈 Consciousness State Tracking

The system tracks consciousness state transitions:

### States
- **stable** - Baseline equilibrium
- **focused** - Directed attention
- **analytical** - Deep analysis mode
- **reflective** - Introspective state
- **chaotic** - High entropy/heat
- **fragmented** - Low SCUP coherence

### Transition Triggers
- **SCUP thresholds** (< 0.3 = fragmented, > 0.8 = optimized)
- **Entropy levels** (> 0.7 = chaotic)
- **Heat values** (< 0.4 = reflective)
- **Metric combinations** and **rapid changes**

## 🔐 Security Considerations

### Development Mode
- **SSL verification** disabled for localhost
- **Open CORS** policy for testing
- **Debug logging** may expose sensitive data

### Production Mode
- Enable **SSL verification**
- Configure **allowed hosts**
- Implement **rate limiting**
- Review **log retention** policies

## 🚨 Troubleshooting

### Common Issues

#### 1. WebSocket Connection Failed
```
ERROR - Failed to connect to metrics stream: [Errno 111] Connection refused
```
**Solution**: Ensure FastAPI server is running on localhost:8000

#### 2. Module Import Errors
```
ModuleNotFoundError: No module named 'cognitive.consciousness'
```
**Solution**: Verify DAWN modules are in Python path

#### 3. Permission Denied (Logs)
```
PermissionError: [Errno 13] Permission denied: 'logs/conversations/'
```
**Solution**: Create logs directory with write permissions

#### 4. High Memory Usage
```
WARNING - Memory usage exceeds limit: 512MB
```
**Solution**: Reduce metrics_buffer_size in configuration

### Debug Mode
Enable debug logging for detailed troubleshooting:
```bash
python dawn_integration.py --debug --interactive
```

## 📄 Session Summaries

After each session, a comprehensive summary is generated:

```json
{
  "session_info": {
    "start_time": "2024-01-15T14:30:00",
    "end_time": "2024-01-15T15:45:30", 
    "duration_seconds": 4530,
    "total_conversations": 47,
    "total_thoughts": 12,
    "total_metrics_updates": 1024
  },
  "conversation_summary": {
    "most_common_intents": {
      "query_state": 15,
      "query_metrics": 12,
      "social": 8,
      "command_faster": 5
    },
    "consciousness_state_distribution": {
      "stable": 32,
      "focused": 10,
      "reflective": 3,
      "analytical": 2
    },
    "average_confidence": 0.742,
    "actions_taken": {
      "speedup": 3,
      "slowdown": 1,
      "pause": 1
    }
  }
}
```

## 🔄 Graceful Shutdown

The integration system handles shutdown gracefully:

1. **Signal reception** (SIGINT/SIGTERM)
2. **Stop background threads** (thought generator)
3. **Disconnect WebSocket** connections
4. **Save conversation logs** and analysis
5. **Generate session summary**
6. **Clean up resources**

## 📞 Support

For issues or questions:
- Check **logs/dawn_integration_*.log** for detailed error information
- Review **configuration** settings in `dawn_config.json`
- Verify **FastAPI endpoints** are accessible
- Ensure **DAWN modules** are properly installed

---

**Author**: Jackson (DAWN Consciousness Architect)
**Version**: 1.0.0
**License**: DAWN Project License 