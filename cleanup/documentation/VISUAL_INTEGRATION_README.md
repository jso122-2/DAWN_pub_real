# DAWN Visual Integration System

This document describes the integration of the `visual/run_visuals.sh` script with the main DAWN engine in `backend/main.py`.

## Overview

The visual integration system provides a Python interface to manage the DAWN visual system, which runs multiple visualization processes in parallel using the `run_visuals.sh` bash script. This integration allows the main DAWN engine to start, stop, monitor, and configure the visual system programmatically.

## Architecture

### Components

1. **VisualIntegrationManager** (`backend/visual_integration.py`)
   - Core manager class that handles the visual system lifecycle
   - Manages subprocess execution of the bash script
   - Provides monitoring and status reporting
   - Handles configuration management

2. **DAWNVisualIntegration** (`backend/visual_integration.py`)
   - Integration wrapper for use within the main DAWN system
   - Automatically configures the visual system based on DAWN settings
   - Provides simplified interface for the main engine

3. **API Endpoints** (`backend/main.py`)
   - REST API endpoints for controlling the visual system
   - Status monitoring and configuration management
   - Integration with FastAPI server

### Integration Points

- **Startup**: Visual system starts automatically with the main DAWN engine
- **Shutdown**: Visual system stops gracefully when DAWN shuts down
- **Configuration**: Visual system can be configured via API endpoints
- **Monitoring**: Real-time status monitoring through API endpoints

## Usage

### Starting the Visual System

The visual system starts automatically when the main DAWN engine starts:

```python
# In backend/main.py startup_event()
if dawn_central.visual_integration.start():
    logger.info("Visual integration system started successfully")
else:
    logger.warning("Visual integration system failed to start")
```

### Manual Control

You can also control the visual system manually:

```python
from backend.visual_integration import get_visual_manager

# Get the visual manager
manager = get_visual_manager()

# Start the visual system
success = manager.start_visual_system()

# Stop the visual system
success = manager.stop_visual_system()

# Get status
status = manager.get_status()
```

### Configuration

The visual system can be configured with various parameters:

```python
from backend.visual_integration import VisualConfig, VisualMode

config = VisualConfig(
    mode=VisualMode.STDIN,  # or VisualMode.DEMO
    interval_ms=100,        # Animation interval
    buffer_size=100,        # Buffer size for visualizations
    log_dir="visual/logs",  # Log directory
    output_dir="visual/outputs_2024-01-01",  # Output directory
    kill_existing=True,     # Kill existing processes
    max_processes=8         # Maximum concurrent processes
)

manager = VisualIntegrationManager(config)
```

## API Endpoints

The visual integration provides several REST API endpoints:

### Status Endpoints

- `GET /api/visual-system/status` - Get current status
- `GET /api/visual-system/config` - Get current configuration

### Control Endpoints

- `POST /api/visual-system/start` - Start the visual system
- `POST /api/visual-system/stop` - Stop the visual system
- `POST /api/visual-system/restart` - Restart the visual system

### Configuration Endpoints

- `POST /api/visual-system/config` - Update configuration

Example usage:

```bash
# Get status
curl http://localhost:8000/api/visual-system/status

# Start visual system
curl -X POST http://localhost:8000/api/visual-system/start

# Update configuration
curl -X POST "http://localhost:8000/api/visual-system/config?interval_ms=200&buffer_size=150"

# Stop visual system
curl -X POST http://localhost:8000/api/visual-system/stop
```

## Visual Scripts

The integration manages the following visual scripts (defined in `run_visuals.sh`):

1. **scup_zone_animator.py** - SCUP zone animation
2. **tick_pulse.py** - Tick pulse visualization
3. **consciousness_constellation.py** - Consciousness constellation
4. **SCUP_pressure_grid.py** - SCUP pressure grid
5. **heat_monitor.py** - Heat monitoring
6. **entropy_flow.py** - Entropy flow visualization
7. **semantic_flow_graph.py** - Semantic flow graph
8. **recursive_depth_explorer.py** - Recursive depth exploration
9. **bloom_genealogy_network.py** - Bloom genealogy network
10. **sigil_command_stream.py** - Sigil command stream
11. **dawn_mood_state.py** - DAWN mood state

## Configuration Options

### VisualMode

- `STDIN` - Read data from standard input (default)
- `DEMO` - Run in demo mode with simulated data
- `DISABLED` - Disable visual system
- `AUTO` - Automatic mode selection

### Parameters

- `interval_ms` - Animation interval in milliseconds (default: 100)
- `buffer_size` - Buffer size for visualizations (default: 100)
- `log_dir` - Directory for log files (default: "visual/logs")
- `output_dir` - Directory for visual outputs (default: auto-generated)
- `kill_existing` - Kill existing processes on start (default: true)
- `max_processes` - Maximum concurrent processes (default: 8)

## Monitoring and Logging

### Status Information

The visual system provides comprehensive status information:

```python
status = manager.get_status()
# Returns:
{
    "is_running": bool,
    "config": {
        "mode": str,
        "interval_ms": int,
        "buffer_size": int,
        "log_dir": str,
        "output_dir": str
    },
    "process": {
        "pid": int,
        "returncode": int
    },
    "visual_processes": [int]  # List of PIDs
}
```

### Logging

The visual system logs to:
- Console output (via Python logging)
- Log files in the configured log directory
- Individual process logs for each visualization

### Error Handling

The integration includes robust error handling:
- Process monitoring and restart capabilities
- Graceful shutdown on errors
- Configuration validation
- Resource cleanup

## Testing

Run the test suite to verify the integration:

```bash
python test_visual_integration.py
```

This will test:
- Visual manager creation and configuration
- System startup and shutdown
- Configuration updates
- Global convenience functions
- Error handling

## Troubleshooting

### Common Issues

1. **Script not found**: Ensure `visual/run_visuals.sh` exists and is executable
2. **Permission denied**: Make sure the script has execute permissions (`chmod +x visual/run_visuals.sh`)
3. **Process already running**: Use `kill_existing=True` or manually stop existing processes
4. **Port conflicts**: Ensure no other processes are using the same ports

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.getLogger('backend.visual_integration').setLevel(logging.DEBUG)
```

### Manual Cleanup

If processes become stuck, you can manually clean up:

```bash
# Kill all visualization processes
pkill -f "python.*visual.*\.py"

# Remove PID file
rm -f visualization_pids.txt
```

## Integration with DAWN

The visual integration is fully integrated into the DAWN system:

1. **Automatic Startup**: Starts with the main DAWN engine
2. **Automatic Shutdown**: Stops when DAWN shuts down
3. **Configuration**: Uses DAWN session information for output directories
4. **Monitoring**: Integrated with DAWN's health monitoring system
5. **API**: Available through DAWN's REST API

## Future Enhancements

Potential improvements for the visual integration:

1. **Real-time Data Streaming**: Pipe DAWN state data directly to visual processes
2. **Dynamic Process Management**: Start/stop individual visualizations based on system load
3. **Performance Optimization**: Adaptive configuration based on system resources
4. **WebSocket Integration**: Real-time status updates via WebSocket
5. **Plugin System**: Support for custom visualization plugins

## Dependencies

- Python 3.7+
- FastAPI (for API endpoints)
- subprocess (for process management)
- threading (for monitoring)
- pathlib (for path handling)

## License

This integration is part of the DAWN project and follows the same licensing terms. 