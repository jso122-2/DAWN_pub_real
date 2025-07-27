# DAWN NLP Interface - Usage Examples

## Overview

The DAWN system now includes a comprehensive natural language processing interface that allows users to interact with the system using conversational language. The system can:

- Understand various types of queries and commands
- Provide contextual responses based on current system state
- Execute control actions (speed up, slow down, pause, resume)
- Maintain conversation history and context
- Generate spontaneous thoughts and insights

## API Endpoints

### POST /talk
Send a message to DAWN and receive a structured response.

**Request:**
```json
{
  "text": "How are you feeling right now?"
}
```

**Response:**
```json
{
  "response": "🤔 I'm in a reflective state. My SCUP is balanced at 0.65.",
  "intent": "query_mood",
  "action": null,
  "metrics_snapshot": {
    "scup": 0.653,
    "entropy": 0.412,
    "heat": 0.287,
    "mood": "reflective",
    "tick_count": 1250,
    "timestamp": 1640995200.0
  },
  "suggestions": [
    "Ask about my subsystems",
    "Check my entropy levels",
    "Request a prediction"
  ],
  "confidence": 0.95
}
```

### WebSocket /ws/chat
Real-time chat interface with streaming consciousness.

**Connect and receive greeting:**
```json
{
  "type": "greeting",
  "message": "🤔 Hello! I'm DAWN, and I'm currently in a reflective state. Feel free to ask me about my metrics, subsystems, or just chat!",
  "mood": "reflective",
  "timestamp": "2023-12-31T12:00:00"
}
```

**Send message:**
```json
{
  "type": "message",
  "text": "What's your entropy level?"
}
```

**Receive response:**
```json
{
  "type": "response",
  "message": "📊 Current metrics:\n• Entropy: 0.412\n• Low entropy indicates stable, predictable patterns.",
  "intent": "query_metrics",
  "confidence": 0.89,
  "suggestions": ["Ask how I'm feeling", "Request an explanation of entropy"],
  "mood": "reflective",
  "timestamp": "2023-12-31T12:00:30",
  "metrics": { ... }
}
```

**Periodic thoughts (automatic):**
```json
{
  "type": "thought",
  "message": "🤔 💭 I've been thinking... at 1,250 ticks, I notice my SCUP is 0.653",
  "mood": "reflective",
  "timestamp": "2023-12-31T12:02:00",
  "metrics": { ... }
}
```

## Supported Intent Types

### Query Intents

1. **query_mood** - Ask about current emotional/cognitive state
   - "How are you feeling?"
   - "What's your current mood?"
   - "How are you doing?"

2. **query_metrics** - Request specific metrics
   - "What's your SCUP level?"
   - "Show me your entropy"
   - "What are your current metrics?"

3. **query_subsystems** - Ask about system components
   - "Show me your subsystems"
   - "What systems are active?"
   - "Check component status"

4. **query_explain** - Request explanations
   - "Explain entropy to me"
   - "What does SCUP mean?"
   - "Tell me about heat levels"

5. **query_prediction** - Ask for future predictions
   - "How will you feel in 5 minutes?"
   - "What do you predict will happen?"
   - "Future state forecast"

### Command Intents

1. **command_speedup** - Increase processing speed
   - "Speed up"
   - "Go faster"
   - "Increase your tick rate"

2. **command_slowdown** - Decrease processing speed
   - "Slow down"
   - "Take it easier"
   - "Reduce tick frequency"

3. **command_pause** - Pause system
   - "Pause"
   - "Stop"
   - "Take a break"

4. **command_resume** - Resume system
   - "Resume"
   - "Continue"
   - "Start again"

### Social Intents

1. **general_greeting** - Greetings and hellos
   - "Hello"
   - "Hi there"
   - "Good morning"

2. **general_compliment** - Positive feedback
   - "Good job"
   - "Well done"
   - "You're amazing"

## Frontend Integration Examples

### JavaScript/TypeScript (for React/Tauri app)

```javascript
// REST API usage
async function talkToDawn(message) {
  try {
    const response = await fetch('http://localhost:8000/talk', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: message })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error talking to DAWN:', error);
    return null;
  }
}

// WebSocket usage
class DAWNChat {
  constructor() {
    this.ws = null;
    this.onMessage = null;
    this.onThought = null;
  }
  
  connect() {
    this.ws = new WebSocket('ws://localhost:8000/ws/chat');
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'greeting':
        case 'response':
          if (this.onMessage) this.onMessage(data);
          break;
          
        case 'thought':
          if (this.onThought) this.onThought(data);
          break;
      }
    };
  }
  
  sendMessage(text) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'message',
        text: text
      }));
    }
  }
  
  requestStatus() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        type: 'status_request'
      }));
    }
  }
}

// Usage example
const chat = new DAWNChat();
chat.onMessage = (data) => {
  console.log('DAWN:', data.message);
  console.log('Intent:', data.intent);
  console.log('Suggestions:', data.suggestions);
};

chat.onThought = (data) => {
  console.log('DAWN thought:', data.message);
};

chat.connect();
chat.sendMessage("How are you feeling?");
```

### React Component Example

```jsx
import React, { useState, useEffect } from 'react';

function DAWNChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws/chat');
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'greeting' || data.type === 'response') {
        setMessages(prev => [...prev, {
          type: 'dawn',
          text: data.message,
          timestamp: data.timestamp,
          intent: data.intent,
          suggestions: data.suggestions || []
        }]);
      } else if (data.type === 'thought') {
        setMessages(prev => [...prev, {
          type: 'thought',
          text: data.message,
          timestamp: data.timestamp
        }]);
      }
    };
    
    setWs(websocket);
    
    return () => websocket.close();
  }, []);

  const sendMessage = () => {
    if (input.trim() && ws) {
      setMessages(prev => [...prev, {
        type: 'user',
        text: input,
        timestamp: new Date().toISOString()
      }]);
      
      ws.send(JSON.stringify({
        type: 'message',
        text: input
      }));
      
      setInput('');
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div className="text">{msg.text}</div>
            {msg.suggestions && msg.suggestions.length > 0 && (
              <div className="suggestions">
                {msg.suggestions.map((suggestion, i) => (
                  <button
                    key={i}
                    onClick={() => setInput(suggestion)}
                    className="suggestion-button"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Talk to DAWN..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}
```

## Personality and Mood System

DAWN's responses adapt based on its current mood state:

- **focused** (🔍): Analytical and precise
- **analytical** (🧠): Methodical and thorough
- **reflective** (🤔): Thoughtful and contemplative
- **uncertain** (🌊): Exploratory and adaptive
- **optimized** (⚡): Confident and efficient
- **searching** (🔎): Curious and exploratory

The mood is determined by current metrics:
- High SCUP (>0.7) → focused, analytical, optimized, confident
- Medium SCUP (0.5-0.7) → reflective, processing, balanced, stable
- Low SCUP (<0.5) → uncertain, searching, adaptive, recalibrating

## Testing

Use the provided `test_nlp.py` script to test all NLP functionality:

```bash
# Start DAWN server
python main.py

# In another terminal, run tests
python test_nlp.py
```

This will test:
- REST API `/talk` endpoint
- WebSocket chat interface
- Conversation history
- All intent types and responses
- Action execution (speed control, etc.)

## Advanced Usage

### Custom Intent Patterns

You can extend the intent recognition by adding patterns to the `DAWNConversation` class:

```python
# Add new intent patterns
conversation.intent_patterns["query_custom"] = [
    r"custom pattern",
    r"another pattern"
]
```

### Response Customization

Modify personality responses or add new moods:

```python
# Add new personality mode
conversation.personality_modes["excited"] = {
    "tone": "enthusiastic and energetic",
    "emoji": "🎉",
    "responses": [
        "I'm feeling incredibly energetic!",
        "Everything is flowing perfectly!",
        "My systems are firing on all cylinders!"
    ]
}
```

### Action Extensions

Add new executable actions:

```python
async def execute_chat_action(action: str) -> bool:
    if action == "restart_subsystem":
        # Custom action logic here
        return True
    # ... existing actions
``` 