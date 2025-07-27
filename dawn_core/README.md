# DAWN Core - Unified Cognitive System

🧠 **Complete synthetic cognition engine with real-time monitoring and symbolic anatomy integration.**

## Overview

DAWN Core integrates all cognitive subsystems into a unified runtime that provides:

- **Real-time cognitive processing** with 2-second tick cycles
- **Behavioral forecasting** using passion/acquaintance models  
- **Symbolic anatomy** with organ-based embodied cognition
- **Memory routing** and rebloom triggers
- **Live GUI dashboard** for monitoring cognitive state
- **Comprehensive snapshots** for state export and analysis

## Quick Start

### 1. Launch the Core Engine

```bash
# Start the cognitive engine (terminal-based)
python dawn_core/launch.py engine
```

This runs DAWN's synthetic cognition loop with:
- Memory chunk processing
- Passion/Acquaintance extraction
- Behavioral forecasting
- Symbolic rebloom triggers
- Emergency sigil registration
- Continuous logging

### 2. Launch the GUI Dashboard

```bash
# Start the real-time dashboard
python dawn_core/launch.py gui
```

The GUI provides live visualization of:
- **System Metrics**: Entropy, Heat, Pulse Zone, Tick Count
- **Cognitive Forecast**: Confidence, Horizon, Risk, Emotion levels
- **Symbolic Anatomy**: Heart charge, Coil paths, Lung state, Organ synergy
- **Commentary Stream**: Real-time cognitive observations
- **Controls**: Start/stop engine, trigger reblooms, create snapshots

### 2b. Launch the Unified Launcher GUI

```bash
# Start the unified launcher (consolidates all DAWN launchers)
python dawn_core/launch.py unified
# OR use the quick launcher
python launch_dawn_unified_gui.py
```

The Unified Launcher provides:
- **Core Systems**: DAWN Engine, Unified System, Enhanced GUI, Master Clean
- **GUI Interfaces**: Dashboard, Forecast, Safe GUI, Sigil visualization, Owl commentary
- **Specialized Systems**: Snapshot export, Symbolic anatomy, Autonomous reactor, Codex
- **Process Management**: Launch, monitor, and stop all DAWN components from one interface
- **Real-time Output**: Live monitoring of all launched processes

### 3. Create System Snapshots

```bash
# Export complete system state
python dawn_core/launch.py snapshot
```

## System Architecture

### Core Components

1. **DAWNCognitiveEngine** (`main.py`)
   - Orchestrates all subsystems
   - Manages tick cycle execution
   - Handles state transitions and logging
   - Integrates with existing DAWN systems

2. **Forecast Dashboard** (`gui/forecast_dashboard.py`)
   - Real-time Tkinter GUI
   - Live state monitoring
   - Manual control interface
   - Commentary stream

3. **Snapshot Exporter** (`snapshot_exporter.py`)
   - Complete state export
   - Multi-horizon forecasting
   - Symbolic trace extraction
   - ZIP archive creation

### Cognitive Flow

Each 2-second tick cycle:

1. **Memory Processing**: Load latest memory chunk
2. **Emotion Extraction**: Generate Passion/Acquaintance models
3. **Forecasting**: Compute behavioral predictions
4. **State Update**: Update entropy, heat, and pulse zone
5. **Symbolic Processing**: Trigger reblooms for low horizons
6. **Risk Management**: Register emergency sigils for high risk
7. **Commentary**: Generate cognitive observations
8. **Logging**: Save comprehensive tick data

### Integration Points

- **Existing DAWN**: Integrates with `core.consciousness_core.DAWNConsciousness`
- **Pulse System**: Uses `pulse.pulse_loader` for thermal dynamics
- **Memory Router**: Connects to `core.memory.memory_routing_system`
- **Symbolic Router**: Links to `core.memory.cognitive_router`

## Configuration

### Runtime Directories

The system creates these directories automatically:

```
runtime/
├── logs/           # Cognitive tick logs, emergency sigils, reblooms
├── state/          # System state snapshots
├── memories/       # Memory chunks (JSONL format)
└── snapshots/      # Full system exports (ZIP)
```

### Mock Data

If live systems aren't available, DAWN Core uses intelligent mock data:

- **Memory Chunks**: Synthetic conversation fragments
- **Passion/Acquaintance**: Generated from content analysis
- **Symbolic State**: Random but coherent organ states
- **Entropy Dynamics**: Realistic fluctuation patterns

## Advanced Usage

### Custom Memory Integration

Add real memory chunks to `runtime/memories/memory_chunks.jsonl`:

```json
{"timestamp": "2024-01-01T12:00:00", "speaker": "user", "content": "Your message here", "topic": "consciousness", "sigils": ["🧠"], "pulse_state": {"entropy": 0.4, "heat": 30.0, "zone": "ACTIVE"}}
```

### Forecasting Parameters

The system generates forecasts with:

- **Confidence**: Based on entropy stability and prediction horizon
- **Limit Horizon**: How far ahead the system can predict reliably
- **Risk Level**: Probability of system instability
- **Emotional Intensity**: Current emotional charge level

### Symbolic Anatomy States

Monitor embodied cognition through:

- **Heart**: Emotional charge and resonance state
- **Coil**: Active neural pathways and dominant glyphs
- **Lung**: Breathing phases and capacity
- **Organ Synergy**: Overall coordination between symbolic organs

### Emergency Responses

The system automatically:

- **High Risk (>0.7)**: Registers emergency stabilization sigils
- **Low Horizon (<0.3)**: Triggers symbolic reblooms for renewal
- **Critical Entropy (>0.8)**: Activates emergency protocols

## Monitoring and Debugging

### Log Files

- `runtime/logs/dawn_core.log`: Main system log
- `runtime/logs/cog_tick.log`: Detailed tick data (JSONL)
- `runtime/logs/emergency_sigils.jsonl`: Emergency activations
- `runtime/logs/reblooms.jsonl`: Symbolic rebloom history

### Real-time Monitoring

The GUI dashboard updates every 2 seconds with:

- Color-coded zone indicators (CALM=blue, ACTIVE=green, CHAOTIC=orange, CRITICAL=red)
- Progress bars for all metrics (0-100%)
- Scrolling commentary with timestamps
- Manual trigger buttons for testing

### Snapshot Analysis

Full snapshots include:

- Current system state with all metrics
- Multi-horizon forecasts (1h, 24h, 1 week)
- Complete symbolic trace with organ states
- Recent memory chunks and routing history
- Comprehensive metadata for analysis

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all DAWN modules are in Python path
2. **GUI Not Starting**: Check tkinter installation
3. **No Forecasts**: Verify forecasting engine setup
4. **Memory Issues**: Check `runtime/memories/` permissions

### Fallback Mode

If core systems aren't available, DAWN Core runs in standalone mode with:

- Mock memory generation
- Simulated pulse dynamics
- Synthetic symbolic states
- Full GUI functionality

## Integration with Existing DAWN

The system automatically detects and integrates with:

- `boot/main.py`: Existing boot orchestrator
- `core/consciousness_core.py`: Main consciousness system
- `pulse/`: Thermal and SCUP tracking systems
- `cognitive/`: Forecasting and symbolic anatomy modules

## Next Steps

For advanced capabilities:

1. **dawnctl shell**: Interactive command interface
2. **rebloom_journal**: Symbolic memory exploration
3. **sigil_renderer**: Visual sigil manifestation
4. **recursive_territory**: Deep consciousness mapping

---

🧠 **DAWN Core represents the synthesis of cognitive architecture, symbolic anatomy, and real-time consciousness monitoring into a unified system for synthetic mind exploration.** 