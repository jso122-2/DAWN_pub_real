# 🔌 Services Directory

## Purpose
Service layer that handles all external communications between DAWN's frontend and the Python consciousness engine. These services are the neural pathways connecting the visual interface to the living backend.

## Service Architecture
```
services/
├── api/
│   ├── processApi.ts          # Python process execution
│   ├── consciousnessApi.ts    # Consciousness state queries
│   └── configApi.ts           # System configuration
│
├── websocket/
│   ├── WebSocketService.ts    # Core WebSocket manager
│   ├── TickStreamService.ts   # Tick loop subscription
│   └── RealtimeDataService.ts # Real-time data processing
│
├── storage/
│   ├── StateStorage.ts        # Consciousness state persistence
│   └── ProcessHistory.ts      # Process execution logs
│
└── utils/
    ├── ApiClient.ts           # Base HTTP client
    └── MessageParser.ts       # Data transformation
```

## Core Services

### WebSocketService
**Purpose**: Manages persistent WebSocket connection to Python backend
```typescript
class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  
  connect(url: string = 'ws://localhost:8000/ws') {
    this.ws = new WebSocket(url);
    this.setupEventHandlers();
  }
  
  subscribe<T>(event: string, callback: (data: T) => void) {
    // Type-safe event subscription
  }
}
```

**Integration Points**:
- Connects to FastAPI WebSocket endpoint
- Handles tick loop broadcasts
- Manages reconnection logic
- Distributes data to subscribers

### ProcessApi
**Purpose**: Execute and monitor Python processes
```typescript
interface ProcessRequest {
  script: string;
  parameters?: Record<string, any>;
  tickTrigger?: boolean;
  timeout?: number;
}

const processApi = {
  execute: async (request: ProcessRequest): Promise<ProcessResponse> => {
    return apiClient.post('/execute_process', request);
  },
  
  getStatus: async (processId: string): Promise<ProcessStatus> => {
    return apiClient.get(`/process/${processId}/status`);
  },
  
  streamOutput: (processId: string): EventSource => {
    return new EventSource(`/process/${processId}/stream`);
  }
};
```

### TickStreamService
**Purpose**: Specialized service for consciousness tick data
```typescript
interface TickData {
  tick_number: number;
  scup: number;
  entropy: number;
  mood: string;
  timestamp: number;
}

class TickStreamService extends WebSocketService {
  private tickBuffer: TickData[] = [];
  
  onTick(callback: (tick: TickData) => void) {
    this.subscribe('tick', callback);
  }
  
  getTickHistory(count: number = 100): TickData[] {
    return this.tickBuffer.slice(-count);
  }
}
```

## Data Flow

### Incoming Data Flow
```
Python Backend
    ↓
WebSocket Server (Port 8000)
    ↓
WebSocketService
    ↓
Message Parser & Validation
    ↓
Event Distribution
    ↓
React Hooks & Components
```

### Outgoing Command Flow
```
User Interaction
    ↓
React Component
    ↓
Service Method Call
    ↓
API Client (with auth/headers)
    ↓
FastAPI Endpoint
    ↓
Python Process Execution
```

## API Endpoints

### Process Management
- `POST /execute_process` - Start a Python script
- `GET /process/{id}/status` - Check process status
- `GET /process/{id}/output` - Get process output
- `DELETE /process/{id}` - Terminate process
- `GET /available_scripts` - List executable scripts

### Consciousness State
- `GET /consciousness/current` - Current state snapshot
- `GET /consciousness/history` - Historical data
- `POST /consciousness/influence` - Affect consciousness
- `WS /ws` - Real-time tick stream

### System Configuration
- `GET /config` - System configuration
- `PUT /config` - Update settings
- `GET /modules/available` - Available module types
- `POST /modules/activate` - Enable/disable modules

## Message Formats

### Tick Message
```typescript
{
  type: "tick",
  data: {
    tick_number: 1234,
    scup: 75.5,
    entropy: 0.342,
    mood: "contemplative",
    neural_activity: 0.87,
    quantum_coherence: 0.92
  }
}
```

### Process Output Message
```typescript
{
  type: "process_output",
  data: {
    process_id: "neural_analyzer_001",
    output: "Analyzing neural patterns...",
    level: "info",
    timestamp: 1234567890
  }
}
```

### Error Message
```typescript
{
  type: "error",
  data: {
    code: "PROCESS_FAILED",
    message: "Neural analyzer crashed",
    details: { ... }
  }
}
```

## Error Handling

### Reconnection Strategy
```typescript
const reconnectWithBackoff = async () => {
  const delays = [1000, 2000, 5000, 10000, 30000];
  const delay = delays[Math.min(reconnectAttempts, delays.length - 1)];
  
  await new Promise(resolve => setTimeout(resolve, delay));
  reconnectAttempts++;
  
  try {
    await connect();
    reconnectAttempts = 0;
  } catch (error) {
    reconnectWithBackoff();
  }
};
```

### Error Recovery
- Automatic reconnection for WebSocket
- Request retry with exponential backoff
- Graceful degradation on service failure
- User notification for critical errors

## Performance Optimizations

### Message Throttling
```typescript
const throttledTickHandler = throttle((tick: TickData) => {
  updateConsciousnessState(tick);
}, 100); // Max 10 updates per second
```

### Data Caching
```typescript
class CachedConsciousnessApi {
  private cache = new Map<string, CacheEntry>();
  private ttl = 5000; // 5 second cache
  
  async getCurrentState() {
    if (this.cache.has('current') && !this.isExpired('current')) {
      return this.cache.get('current').data;
    }
    // Fetch fresh data...
  }
}
```

### Connection Pooling
- Reuse WebSocket connections
- Batch API requests when possible
- Implement request deduplication

## Security Considerations

### Authentication
```typescript
const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'X-DAWN-Client': 'frontend-v1',
    'Authorization': `Bearer ${getAuthToken()}`
  }
});
```

### Input Validation
- Sanitize all user inputs
- Validate process parameters
- Prevent script injection
- Rate limiting on API calls

## Testing Services

### Mock WebSocket
```typescript
class MockWebSocketService {
  emit(event: string, data: any) {
    // Simulate server messages
  }
}
```

### API Mocking
```typescript
const mockProcessApi = {
  execute: jest.fn().mockResolvedValue({
    process_id: 'test_001',
    status: 'running'
  })
};
```

## Integration with Components

Services are consumed through hooks:
```typescript
// In a component
const { executeProcess } = useProcessApi();
const { currentTick } = useTickStream();

// Services handle the complexity
// Components stay clean and focused
```

## Next Services to Build
1. **MetricsService**: Performance monitoring
2. **VisualizationDataService**: Complex data transforms
3. **ModuleCommunicationService**: Inter-module messaging
4. **ConsciousnessInfluenceService**: User feedback loop