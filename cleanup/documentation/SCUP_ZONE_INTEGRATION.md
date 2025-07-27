# SCUP Zone Animator Integration

This document describes the integration of the SCUP Zone Animator with the DAWN Tick Engine backend.

## Overview

The SCUP Zone Animator has been integrated into the backend system to provide real-time visualization of SCUP (Semantic Coherence Under Pressure) values and their corresponding zones (calm, active, surge). The integration includes:

- **Enhanced Zone Tracker**: Tracks SCUP values and determines zones
- **SCUP Zone Animator Service**: Manages animation generation and auto-animation
- **API Endpoints**: REST endpoints for controlling the animator
- **Backend Integration**: Full integration with the DAWN Central system

## Components

### 1. Enhanced Zone Tracker (`pulse/enhanced_zone_tracker.py`)

Tracks SCUP values and determines zones based on thresholds:
- **Calm Zone**: SCUP < 0.3
- **Active Zone**: 0.3 ≤ SCUP < 0.7  
- **Surge Zone**: SCUP ≥ 0.7

Features:
- Real-time zone determination
- Historical data collection
- Data export for animation
- Integration with SCUP tracker

### 2. SCUP Zone Animator Service (`backend/visual/scup_zone_animator_service.py`)

Service that manages animation generation:
- Automatic animation generation
- Integration with DAWN Central
- Data collection and export
- Status monitoring

### 3. Backend Integration (`backend/main.py`)

The animator is integrated into the DAWN Central system:
- Added as a subsystem
- Included in system state
- Proper shutdown handling
- API endpoints

## API Endpoints

### Status Endpoints

- `GET /api/scup-zone-animator/status` - Get animator service status
- `GET /api/scup-zone-animator/last-animation` - Get last animation path

### Control Endpoints

- `POST /api/scup-zone-animator/generate` - Generate new animation
- `POST /api/scup-zone-animator/auto-start?interval=60` - Start auto-animation
- `POST /api/scup-zone-animator/auto-stop` - Stop auto-animation

### Data Endpoints

- `GET /api/scup-zone-animator/recent-data?count=50` - Get recent zone data

## Usage Examples

### Generate Animation Manually

```bash
curl -X POST http://localhost:8000/api/scup-zone-animator/generate
```

### Start Auto-Animation

```bash
curl -X POST "http://localhost:8000/api/scup-zone-animator/auto-start?interval=30"
```

### Get Status

```bash
curl http://localhost:8000/api/scup-zone-animator/status
```

### Get Recent Data

```bash
curl "http://localhost:8000/api/scup-zone-animator/recent-data?count=100"
```

## System State Integration

The SCUP zone animator status is included in the system state:

```json
{
  "tick": 1234,
  "scup": 0.65,
  "scup_zone_animator": {
    "active": true,
    "auto_animate": false,
    "animation_interval": 60,
    "last_animation_path": "visual/outputs/scup_zone_animator/scup_zone_overlay.gif",
    "zone_tracker_status": {
      "active": true,
      "current_zone": "active",
      "history_size": 150,
      "scup_history_size": 150,
      "last_scup": 0.65
    }
  }
}
```

## File Structure

```
visual/
├── scup_zone_animator.py                    # Original animator
└── outputs/
    └── scup_zone_animator/
        ├── scup_bloom_correlation.csv       # SCUP data
        ├── zone_overlay_log.csv             # Zone data
        └── scup_zone_overlay.gif            # Generated animation

pulse/
└── enhanced_zone_tracker.py                 # Enhanced zone tracker

backend/
├── main.py                                  # Main backend (integrated)
└── visual/
    └── scup_zone_animator_service.py        # Animator service
```

## Testing

Run the integration test:

```bash
python test_scup_zone_integration.py
```

## Configuration

The animator can be configured through the service:

- **Animation Interval**: Default 60 seconds for auto-animation
- **Output Directory**: `visual/outputs/scup_zone_animator/`
- **Zone Thresholds**: Configurable in `EnhancedZoneTracker`
- **History Size**: Limited to 1000 entries for performance

## Dependencies

- `matplotlib` - Animation generation
- `pandas` - Data handling
- `numpy` - Numerical operations
- `fastapi` - API endpoints
- `asyncio` - Async operations

## Troubleshooting

### Common Issues

1. **Missing Dependencies**: Install required packages
2. **Permission Errors**: Ensure write access to output directory
3. **Memory Issues**: Reduce history size for large datasets
4. **Animation Failures**: Check matplotlib backend configuration

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.getLogger('backend.visual.scup_zone_animator_service').setLevel(logging.DEBUG)
```

## Future Enhancements

- Real-time WebSocket streaming of animations
- Custom zone definitions
- Advanced visualization options
- Integration with other visualizers
- Performance optimizations 