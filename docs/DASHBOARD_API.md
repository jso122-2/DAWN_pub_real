# DAWN Dashboard API Documentation

## Dashboard-Specific Endpoints

These endpoints are designed to provide comprehensive data streaming and control capabilities for the DAWN dashboard interface.

### 1. Dashboard WebSocket Stream

**Endpoint:** `ws://localhost:8000/dashboard/stream`

Provides real-time streaming of all DAWN subsystem data for dashboard visualization.

**Connection Example:**
```javascript
const ws = new WebSocket('ws://localhost:8000/dashboard/stream');

ws.onmessage = (event) => {
  const dashboardData = JSON.parse(event.data);
  // Update dashboard UI with streaming data
};
```

**Data Structure:**
```json
{
  "timestamp": 1234567890.123,
  "metrics": {
    "scup": 0.75,
    "entropy": 0.42,
    "heat": 0.31,
    "mood": "contemplative",
    "subsystems": [...]
  },
  "consciousness": {
    "emotion": "contemplative",
    "intensity": 0.68,
    "state": {...}
  },
  "gradient": {
    "current_mood": "contemplative",
    "history": [...],
    "transitions": []
  },
  "tracer": {
    "recent_events": [],
    "chain_length": 0
  },
  "rebloom": {
    "active": false,
    "progress": 0.0,
    "priority": "normal",
    "last_rebloom": null
  },
  "fractal": {
    "current_depth": 1,
    "emotion_tree": {},
    "complexity": 0.5
  },
  "memory": {
    "total_memories": 42,
    "recent_memories": [...],
    "memory_usage": 0.0,
    "consolidation_status": "idle"
  },
  "spontaneity": {
    "probability": 0.15,
    "last_thought": null,
    "cooldown_remaining": 0,
    "thought_count": 7
  },
  "tick": {
    "tick_count": 12345,
    "tick_rate": 500,
    "rhythm_pattern": "regular",
    "phase": 0.5
  },
  "anomalies": []
}
```

### 2. Get Subprocess Details

**Endpoint:** `GET /dashboard/subprocess/{name}`

Retrieves detailed information about a specific subprocess.

**Available Subprocesses:**
- `tracer` - Event tracing and chain analysis
- `state` - State machine history and transitions
- `rebloom` - Rebloom status and configuration
- `fractal` - Fractal emotion tree structure
- `memory` - Full memory/chat history and statistics
- `spontaneity` - Spontaneous thought generation logs
- `metrics` - Detailed metrics history and statistics

**Example Request:**
```bash
GET http://localhost:8000/dashboard/subprocess/memory
```

**Example Response:**
```json
{
  "name": "memory",
  "total_memories": 42,
  "memories": [...],
  "memory_stats": {
    "user_messages": 20,
    "dawn_messages": 22,
    "average_length": 45.7
  },
  "consolidation_events": []
}
```

### 3. Control Subprocess

**Endpoint:** `POST /dashboard/control/{subprocess}/{action}`

Provides direct control over DAWN subprocesses from the dashboard.

**Available Controls:**

#### Tick Engine
- `/dashboard/control/tick/pause` - Pause tick engine
- `/dashboard/control/tick/resume` - Resume tick engine
- `/dashboard/control/tick/reset` - Reset tick count
- `/dashboard/control/tick/set_rate_250` - Set tick rate to 250ms
- `/dashboard/control/tick/set_rate_1000` - Set tick rate to 1000ms

#### Spontaneity
- `/dashboard/control/spontaneity/enable` - Enable spontaneous thoughts
- `/dashboard/control/spontaneity/disable` - Disable spontaneous thoughts
- `/dashboard/control/spontaneity/force` - Force generate a thought

#### Memory
- `/dashboard/control/memory/clear` - Clear all memories
- `/dashboard/control/memory/consolidate` - Trigger memory consolidation

#### Rebloom
- `/dashboard/control/rebloom/trigger` - Manually trigger rebloom
- `/dashboard/control/rebloom/abort` - Abort active rebloom

#### State Machine
- `/dashboard/control/state/set_mood_contemplative` - Set mood
- `/dashboard/control/state/reset` - Reset to neutral state

**Example Request:**
```bash
POST http://localhost:8000/dashboard/control/spontaneity/force
```

**Example Response:**
```json
{
  "subprocess": "spontaneity",
  "action": "force",
  "success": true,
  "message": "Generated thought: I wonder what patterns emerge...",
  "thought": "I wonder what patterns emerge..."
}
```

### 4. Export Dashboard Data

**Endpoint:** `GET /dashboard/export?format=json`

Export complete dashboard data for external analysis.

**Example Request:**
```bash
GET http://localhost:8000/dashboard/export?format=json
```

**Response Structure:**
```json
{
  "export_timestamp": 1234567890.123,
  "system_info": {
    "uptime": 3600.5,
    "tick_count": 7200,
    "version": "1.0.0"
  },
  "metrics_history": [...],
  "chat_history": [...],
  "anomalies": [...],
  "personality": {...},
  "configuration": {
    "proactive_insights": true,
    "alert_thresholds": {...}
  }
}
```

## Integration Example

Here's how to integrate these endpoints into a dashboard component:

```javascript
class DAWNDashboard {
  constructor() {
    this.ws = null;
    this.data = {};
  }

  connect() {
    this.ws = new WebSocket('ws://localhost:8000/dashboard/stream');
    
    this.ws.onmessage = (event) => {
      this.data = JSON.parse(event.data);
      this.updateUI();
    };
  }

  async getSubprocessDetail(name) {
    const response = await fetch(`http://localhost:8000/dashboard/subprocess/${name}`);
    return await response.json();
  }

  async controlSubprocess(subprocess, action) {
    const response = await fetch(
      `http://localhost:8000/dashboard/control/${subprocess}/${action}`,
      { method: 'POST' }
    );
    return await response.json();
  }

  async exportData() {
    const response = await fetch('http://localhost:8000/dashboard/export?format=json');
    return await response.json();
  }

  updateUI() {
    // Update dashboard visualizations with this.data
    updateMetricsGauges(this.data.metrics);
    updateGradientVisualization(this.data.gradient);
    updateConsciousnessIndicator(this.data.consciousness);
    // ... etc
  }
}
```

## Notes

1. **WebSocket Streaming**: The dashboard stream updates every 500ms with comprehensive system data.

2. **TODO Items**: Several features are marked as TODO in the implementation:
   - Tracer event logging
   - Mood transition tracking
   - Rebloom tracking implementation
   - Fractal emotion depth tracking
   - Memory usage tracking
   - Thought logging
   - Tick rate adjustment

3. **Error Handling**: All endpoints include proper error handling with meaningful error messages.

4. **Authentication**: Currently no authentication is required. Add authentication middleware for production use.

5. **Rate Limiting**: Consider adding rate limiting for control endpoints to prevent abuse. 