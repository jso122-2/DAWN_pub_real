# DAWN Timeline Visual Module

This module provides a neural cognition timeline visualizer for DAWN.

## Files
- `neural_timeline.html`: Interactive timeline visualizer for neural events.
- `timeline_server.py`: WebSocket server to serve the timeline and stream events.
- `event_collector.py`: Collects and formats events from DAWN for visualization.
- `__init__.py`: Makes this directory a Python module.

## Usage
- Run `timeline_server.py` to start the WebSocket server and serve the timeline visualizer.
- Integrate `event_collector.py` with DAWN to feed live events to the timeline.

## Integration
Import the module in DAWN's visual components to enable the timeline visualizer. 