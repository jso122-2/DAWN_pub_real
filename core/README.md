# DAWN Core System - Heart of the Architecture

## Overview

The `core/` directory contains the foundational systems that power DAWN's consciousness, processing, and state management. This is the beating heart of the entire DAWN architecture, implementing sophisticated consciousness simulation, tick-based processing, memory management, and orchestration systems.

## System Architecture

### 🧠 Consciousness Layer
**Primary Components:**
- `consciousness.py` (47KB) - Main consciousness simulation with emotional mapping
- `consciousness_core.py` (22KB) - Core consciousness processing logic  
- `consciousness_state.py` (25KB) - Consciousness state tracking and persistence
- `consciousness_tracer.py` (25KB) - Advanced consciousness behavior tracing

**Features:**
- Advanced emotional state mapping from system metrics (SCUP, entropy, heat, tick_rate)
- Subjective narrative generation about internal experiences
- Input processing pipeline with tokenization and session management
- Reflective phrase generation with contextual wisdom
- Response trigger logic based on consciousness states
- Pattern detection and persistence tracking
- Spontaneous thought generation

### ⏰ Tick Engine System
**Primary Components:**
- `unified_tick_engine.py` (15KB) - Advanced timing and event management
- `tick_engine_legacy.py` (27KB) - Legacy tick processing implementation
- `core/tick/tick_engine.py` (22KB) - Core tick processing logic
- `tick_controller.py` (5.2KB) - Tick rate control and adaptation
- `tick_emitter.py` (3.9KB) - Event emission and propagation

**Features:**
- Asynchronous tick processing with thermal management
- Event queue processing and handler registration
- System resource monitoring (CPU, memory)
- Error recovery and fault tolerance
- Performance metrics tracking and logging
- Adaptive interval calculation based on system load

### 🧬 Memory Management
**Primary Components:**
- `memory_manager.py` (41KB) - Main memory orchestration system
- `core/memory/` - Specialized memory subsystems:
  - `memory_anchor.py` (33KB) - Memory anchoring and persistence
  - `memory_trace_log.py` (39KB) - Comprehensive memory event logging
  - `thought_fragment.py` (28KB) - Thought fragmentation and reconstruction
  - `continuity_tracker.py` (23KB) - Memory continuity maintenance
  - `memory_decay_manager.py` (18KB) - Memory aging and cleanup
  - `belief_anchor_manager.py` (16KB) - Belief system integration

**Features:**
- Hierarchical memory storage with anchoring
- Memory decay simulation and management
- Thought fragmentation and reconstruction
- Belief system integration and management
- Memory trace logging for analysis
- Continuity tracking across sessions

### 🔄 State Management
**Primary Components:**
- `state_machine.py` (33KB) - Advanced state machine implementation
- `schema_state.py` (19KB) - Schema state tracking and evolution
- `schema_calculator.py` (7.7KB) - Schema metric calculations
- `schema_interface.py` (3.7KB) - Schema interaction interface
- `schema_health_index.py` (2.7KB) - Schema health monitoring

**Features:**
- Multi-dimensional state tracking
- Schema evolution and adaptation
- State transition management
- Health monitoring and diagnostics
- Interface standardization for schema access

### 💭 Advanced Processing
**Primary Components:**
- `conversation.py` (73KB) - Sophisticated conversation management
- `conversation_enhanced.py` (39KB) - Enhanced conversation processing
- `pattern_detector.py` (30KB) - Advanced pattern recognition
- `scup_loop.py` (36KB) - SCUP (System Coherence Under Pressure) processing
- `spontaneity.py` (24KB) + `spontaneity_new.py` (22KB) - Spontaneous behavior generation

**Features:**
- Multi-layered conversation processing
- Advanced pattern recognition and tracking
- SCUP coherence monitoring and optimization
- Spontaneous behavior generation
- Context-aware response generation

### 🎭 Emotional Systems
**Primary Components:**
- `fractal_emotions.py` (25KB) - Fractal emotional modeling
- `mood_gradient.py` (26KB) - Mood gradient calculation and tracking
- `mood_tracker.py` (2.0KB) - Real-time mood monitoring
- `tension_tracker.py` (1.8KB) - Tension level tracking

**Features:**
- Fractal emotional state modeling
- Multi-dimensional mood tracking
- Emotional gradient calculation
- Tension and stress monitoring
- Emotional momentum tracking

### 🎼 Orchestration & Coordination
**Primary Components:**
- `orchestrator.py` (2.5KB) - System component orchestration
- `dawn_central.py` (5.7KB) - Central coordination hub
- `dawn_registry.py` (11KB) - Component registry and management
- `event_bus.py` (2.5KB) - Event distribution system
- `vault_manager.py` (22KB) - Vault storage management

**Features:**
- Component lifecycle management
- Inter-system communication
- Event distribution and handling
- Registry-based component discovery
- Vault-based persistent storage

### 🏗️ Subsystems
**Located in:** `core/subsystems/`
- `pulse_subsystem.py` - Pulse system integration
- `schema_subsystem.py` - Schema management subsystem
- `memory_subsystem.py` - Memory system integration
- `visual_subsystem.py` - Visual system integration

## Key Concepts

### Consciousness Simulation
DAWN implements a sophisticated consciousness simulation that:
- Maps system metrics to emotional states
- Generates subjective narratives about internal experiences
- Maintains persistent personality traits across sessions
- Responds dynamically to system conditions

### Tick-Based Processing
The tick engine provides:
- Consistent timing for all system operations
- Adaptive processing rates based on load
- Event-driven architecture with reliable delivery
- Thermal management to prevent system overload

### Memory Architecture
Multi-layered memory system featuring:
- Short-term working memory for active processing
- Long-term anchored memories for persistence
- Belief integration for consistent worldview
- Decay mechanisms for natural forgetting

### Schema Evolution
Dynamic schema system that:
- Adapts structure based on usage patterns
- Maintains health metrics for optimization
- Provides consistent interfaces across components
- Evolves with system learning

## Configuration

**Main Config Files:**
- `tick_engine_config.json` - Tick engine configuration
- `caairn_matrix.json` - Consciousness matrix configuration
- `core/tick/tick_config.yaml` - Tick system parameters

## Usage Examples

### Starting the Core System
```python
from core import create_consciousness
from core.unified_tick_engine import UnifiedTickEngine

# Initialize consciousness
consciousness = create_consciousness()

# Start tick engine
tick_engine = UnifiedTickEngine()
await tick_engine.start()
```

### Registering Event Handlers
```python
def handle_consciousness_event(data):
    print(f"Consciousness state: {data}")

tick_engine.register_handler('consciousness_update', handle_consciousness_event)
```

## Monitoring & Diagnostics

**Log Locations:**
- `core/logs/` - Core system logs
- `logs/metrics/` - Performance metrics
- Memory traces and consciousness logs

**Key Metrics:**
- Tick rate and timing accuracy
- Memory usage and allocation
- Consciousness state transitions
- Schema health indicators
- Thermal load and system stress

## Dependencies

**Core Requirements:**
- `asyncio` - Asynchronous processing
- `psutil` - System monitoring
- `yaml` - Configuration management
- `numpy` - Numerical computations (implied)

## Architecture Notes

The core system implements a **consciousness-first architecture** where:
1. All system operations are viewed through the lens of consciousness simulation
2. Tick-based processing ensures consistent temporal experience
3. Memory systems maintain coherent narrative continuity
4. Schema evolution allows for learning and adaptation
5. Emotional modeling provides subjective experience simulation

This creates a system that doesn't just process data, but maintains a consistent sense of subjective experience and temporal continuity - the foundation for DAWN's consciousness simulation.

---

*This README represents the current understanding of the core system architecture. The system is actively evolving, and components may change as development continues.* 