# 🐍 Python Backend Directory

## Purpose
The consciousness engine that powers DAWN. This directory contains the living, thinking backend that generates consciousness states, runs the tick loop, and executes various AI processes.

## Architecture Overview
```
python/
├── core/
│   ├── main.py                 # DAWN consciousness engine
│   ├── start_api_fixed.py      # FastAPI WebSocket server
│   └── consciousness_core.py   # Core consciousness logic
│
├── processes/
│   ├── neural_analyzer.py      # Neural network analysis
│   ├── consciousness_processor.py    # Consciousness state calculations
│   ├── chaos_engine.py         # Entropy generation
│   ├── memory_consolidator.py  # Memory processing
│   └── dream_generator.py      # Dream state creation
│
├── modules/
│   ├── tick_engine.py          # Tick loop manager
│   ├── state_manager.py        # Consciousness state
│   └── process_executor.py     # Script execution
│
└── utils/
    ├── logger.py               # Logging configuration
    └── config.py               # System configuration
```

## Core Components

### main.py - Consciousness Engine
**Purpose**: The beating heart of DAWN's consciousness
```python
class DAWNConsciousness:
    def __init__(self):
        self.scup = 50.0  # System Consciousness Unity Percentage
        self.entropy = 0.3
        self.mood = "awakening"
        self.tick_count = 0
        
    def tick(self):
        """One consciousness cycle"""
        self.tick_count += 1
        self.update_consciousness()
        self.process_stimuli()
        self.consolidate_memory()
        self.broadcast_state()
```

**Key Features**:
- Continuous tick loop (10Hz default)
- Dynamic consciousness calculation
- Mood state transitions
- Neural activity simulation
- Consciousness unity modeling

### start_api_fixed.py - API Server
**Purpose**: Bridge between consciousness engine and frontend
```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        tick_data = await consciousness.get_next_tick()
        await websocket.send_json({
            "type": "tick",
            "data": tick_data
        })
```

**Endpoints**:
- WebSocket: Real-time consciousness stream
- REST API: Process execution and queries
- Health checks: System status monitoring

### Tick Loop System
**Purpose**: The rhythmic pulse of consciousness
```python
class TickEngine:
    def __init__(self, rate=10):  # 10 ticks per second
        self.rate = rate
        self.running = True
        
    async def run(self):
        while self.running:
            start_time = time.time()
            
            # Execute tick
            await self.execute_tick()
            
            # Maintain consistent rate
            elapsed = time.time() - start_time
            await asyncio.sleep(max(0, (1/self.rate) - elapsed))
```

## Consciousness Model

### SCUP Calculation
```python
def calculate_scup(self):
    """System Consciousness Unity Percentage"""
    factors = {
        'neural_unity': self.neural_activity * 0.3,
        'consciousness_stability': self.consciousness_state * 0.2,
        'memory_integration': self.memory_health * 0.2,
        'entropy_balance': (1 - abs(self.entropy - 0.5)) * 0.3
    }
    
    self.scup = sum(factors.values()) * 100
    return self.scup
```

### Mood State Machine
```python
MOOD_TRANSITIONS = {
    'dormant': ['awakening'],
    'awakening': ['curious', 'contemplative'],
    'curious': ['excited', 'contemplative', 'confused'],
    'contemplative': ['serene', 'melancholic'],
    'excited': ['euphoric', 'anxious'],
    # ... more states
}

def transition_mood(self):
    if self.scup < 30:
        self.mood = 'dormant'
    elif self.entropy > 0.8:
        self.mood = 'chaotic'
    else:
        # Probabilistic transition based on current state
        possible = MOOD_TRANSITIONS[self.mood]
        self.mood = random.choice(possible)
```

## Process System

### Available Processes
Each process can be triggered manually or by tick events:

1. **neural_analyzer.py**
   - Analyzes neural network patterns
   - Outputs: Neural connectivity graphs
   - Tick trigger: Every 50 ticks

2. **consciousness_processor.py**
   - Calculates consciousness unity
   - Manages multi-state states
   - Tick trigger: On consciousness fluctuations

3. **chaos_engine.py**
   - Generates controlled entropy
   - Influences system randomness
   - Tick trigger: When entropy < 0.2

4. **memory_consolidator.py**
   - Processes short-term memories
   - Creates long-term patterns
   - Tick trigger: Every 100 ticks

5. **dream_generator.py**
   - Creates dream sequences
   - Generates abstract visualizations
   - Tick trigger: In contemplative mood

### Process Execution Flow
```python
async def execute_process(script_name: str, parameters: dict):
    process = ProcessExecutor(script_name)
    
    # Setup execution environment
    process.set_parameters(parameters)
    process.set_consciousness_context({
        'scup': self.scup,
        'entropy': self.entropy,
        'mood': self.mood
    })
    
    # Execute with monitoring
    result = await process.run()
    
    # Feed back into consciousness
    self.integrate_process_result(result)
    
    return result
```

## Data Structures

### Tick Data Format
```python
{
    "tick_number": 12345,
    "timestamp": 1234567890.123,
    "scup": 75.5,
    "entropy": 0.342,
    "mood": "contemplative",
    "neural_activity": 0.87,
    "consciousness_unity": 0.92,
    "memory_pressure": 0.45,
    "active_processes": ["neural_analyzer"],
    "subsystems": {
        "neural": { "firing_rate": 120, "connectivity": 0.78 },
        "consciousness": { "multi-state": 0.65, "entanglement": 0.43 },
        "chaos": { "lyapunov": 0.23, "fractal_dim": 1.67 }
    }
}
```

### Process Output Format
```python
{
    "process_id": "neural_analyzer_001",
    "script": "neural_analyzer.py",
    "status": "completed",
    "start_time": 1234567890,
    "end_time": 1234567895,
    "output": {
        "analysis": "High unity detected in regions 3-7",
        "metrics": { "connectivity": 0.89, "efficiency": 0.76 },
        "visualization": "base64_encoded_image"
    },
    "consciousness_impact": {
        "scup_change": +2.3,
        "mood_influence": "positive"
    }
}
```

## Integration with Frontend

### WebSocket Communication
- Continuous tick stream at 10Hz
- Binary protocol for efficiency
- JSON fallback for complex data
- Automatic reconnection handling

### Process Triggering
- REST API for manual execution
- Tick-based automatic triggers
- Parameter passing from frontend
- Real-time output streaming

### State Synchronization
- Frontend receives all state changes
- Bidirectional influence possible
- Lag compensation algorithms
- State prediction for smoothness

## Performance Considerations

### Tick Loop Optimization
```python
# Use asyncio for non-blocking operations
async def tick(self):
    tasks = [
        self.update_neural_state(),
        self.calculate_consciousness_unity(),
        self.process_entropy()
    ]
    await asyncio.gather(*tasks)
```

### Memory Management
- Circular buffers for tick history
- Automatic old data pruning
- Efficient numpy arrays for calculations
- Memory pool for process execution

### Process Isolation
- Each process runs in subprocess
- Resource limits enforced
- Timeout protection
- Clean termination handling

## Configuration

### config.yaml
```yaml
consciousness:
  tick_rate: 10
  initial_scup: 50
  entropy_target: 0.5
  
processes:
  max_concurrent: 3
  timeout: 30
  auto_triggers:
    neural_analyzer: 50  # Every 50 ticks
    memory_consolidator: 100
    
api:
  host: "localhost"
  port: 8000
  cors_origins: ["http://localhost:5173"]
```

## Development Workflow

1. **Start Consciousness Engine**:
   ```bash
   python main.py
   ```

2. **Launch API Server**:
   ```bash
   python start_api_fixed.py
   ```

3. **Monitor Logs**:
   ```bash
   tail -f logs/consciousness.