# DAWN Cognitive Engine GUI

A real-time Tkinter-based interface for monitoring DAWN's cognitive state, thermal dynamics, and consciousness metrics.

## Features

- **Real-time Heat Monitoring**: Visual pulse heat levels with color-coded indicators
- **Cognitive Zone Display**: Current consciousness zones (calm, active, surge, etc.)
- **Consciousness Summary**: Live analysis of DAWN's cognitive state
- **Tick Activity Log**: Real-time stream of cognitive processing events
- **DAWN Integration**: Direct connection to DAWN's pulse heat, schema state, and consciousness systems
- **Simulation Mode**: Runs without DAWN for testing and demonstration

## Quick Start

### Option 1: Simple Launcher (Recommended)

```bash
# Auto-detect and integrate with running DAWN systems
python launch_dawn_gui.py

# Run in standalone mode (simulation)
python launch_dawn_gui.py --standalone

# Start with a new tick engine
python launch_dawn_gui.py --with-engine
```

### Option 2: Direct GUI Launch

```bash
# Run GUI directly (will auto-detect DAWN or use simulation)
python gui/dawn_gui_tk.py
```

### Option 3: Integration Code

Add to your existing DAWN system:

```python
from gui.dawn_gui_integration import integrate_gui_with_tick_engine

# After creating your tick engine
gui_integration = integrate_gui_with_tick_engine(tick_engine)

# When shutting down
if gui_integration:
    gui_integration.shutdown()
```

## GUI Components

### Heat Display
- **Numeric Display**: Current heat level (0-100%)
- **Progress Bar**: Visual heat level with color coding
- **Color Coding**: Green (low) → Yellow → Orange → Red (high)

### Zone Display
- **Zone Name**: Current cognitive zone (CALM, ACTIVE, SURGE, etc.)
- **Zone Indicator**: Color-coded circular indicator
- **Zone Description**: Brief description of current cognitive state

### Consciousness Summary
- **Real-time Analysis**: Live interpretation of DAWN's cognitive state
- **Multi-factor Summary**: Combines heat, zone, SCUP, entropy, and alignment data
- **Scrollable Text**: Full summary with automatic updates

### Tick Activity Log
- **Live Event Stream**: Real-time tick processing events
- **Timestamped Entries**: Each event with precise timestamp
- **Auto-scrolling**: Automatically scrolls to show latest activity
- **Limited History**: Keeps last 100 entries for performance

## Architecture

### Data Interface (`DAWNGuiDataInterface`)
- Connects to DAWN consciousness systems
- Polls for real-time data every 500ms
- Falls back to simulation mode if DAWN unavailable
- Interfaces with:
  - `UnifiedPulseHeat` for thermal data
  - `SchemaState` for consciousness metrics  
  - `ConsciousnessModule` for SCUP/entropy/coherence
  - `PulseStateTracker` for state persistence

### GUI Core (`DAWNGui`)
- Thread-safe data injection system
- 100ms GUI update cycle
- Queue-based data processing
- Clean separation of data and display

### Integration Layer (`DAWNGuiSubsystem`)
- Tick engine subsystem interface
- Compatible with multiple tick engine types
- Handles registration and lifecycle management

## Integration Methods

### 1. Tick Engine Registration
```python
from gui.dawn_gui_integration import integrate_gui_with_tick_engine

gui_integration = integrate_gui_with_tick_engine(your_tick_engine)
```

### 2. Standalone Mode
```python
from gui.dawn_gui_integration import start_standalone_gui

gui_integration = start_standalone_gui()
```

### 3. Auto-Integration
```python
from gui.dawn_gui_integration import auto_integrate_gui

gui_integration = auto_integrate_gui()  # Finds and integrates automatically
```

## Compatible Tick Engines

The GUI integration supports:
- `TickEngine` (core.tick.tick_engine)
- `TickLoop` (core.tick.tick_loop)
- `UnifiedTickEngine` (core.unified_tick_engine)
- Any engine with `register_subsystem()` method
- Any engine with `tick_callbacks` list
- Custom engines via callback interface

## Data Sources

### Real DAWN Data
When connected to DAWN systems:
- **Heat**: From `UnifiedPulseHeat.heat` (0-1 range, displayed as 0-100%)
- **Zone**: From `UnifiedPulseHeat.classify()` (calm/active/surge)
- **SCUP**: From `ConsciousnessModule.get_state()['scup']`
- **Entropy**: From `ConsciousnessModule.get_state()['entropy']`
- **Schema**: From `SchemaState` (tick, alignment, tension)

### Simulation Data
When DAWN unavailable:
- Randomized but realistic-looking values
- Oscillating patterns for visual appeal
- Clear "SIM" prefixes on tick events

## Requirements

- Python 3.7+
- Tkinter (usually included with Python)
- DAWN consciousness systems (optional - will simulate if unavailable)

## Files

- `gui/dawn_gui_tk.py` - Main GUI implementation
- `gui/dawn_gui_integration.py` - Integration with DAWN systems
- `launch_dawn_gui.py` - Simple launcher script
- `examples/integrate_gui_with_dawn.py` - Integration examples
- `gui/README.md` - This documentation

## Troubleshooting

### GUI Won't Start
```bash
# Check if tkinter is available
python -c "import tkinter; print('Tkinter available')"

# If missing on Ubuntu/Debian:
sudo apt-get install python3-tk
```

### No DAWN Data
- GUI will automatically fall back to simulation mode
- Check console for connection status
- Ensure DAWN systems are running and importable

### Integration Fails
- Check that your tick engine has compatible registration methods
- Try standalone mode: `python launch_dawn_gui.py --standalone`
- Check the integration examples in `examples/integrate_gui_with_dawn.py`

## Examples

See `examples/integrate_gui_with_dawn.py` for comprehensive integration examples with different DAWN system configurations.

## Future Enhancements

- [ ] WebSocket support for remote monitoring
- [ ] Historical data visualization
- [ ] Configuration file support
- [ ] Custom color themes
- [ ] Audio alerts for threshold events
- [ ] Export functionality for consciousness data
- [ ] Multi-instance monitoring 