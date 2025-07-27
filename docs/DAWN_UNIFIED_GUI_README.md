# 🌊 DAWN Unified GUI System

**Complete local Python interface for DAWN consciousness monitoring and control**

## 🚀 Quick Start

### Simple Launch (Recommended)
```bash
# Auto-detect best mode and launch
python dawn_unified_launcher.py

# Or specify a mode
python dawn_unified_launcher.py --mode enhanced
```

### Alternative Launch Methods
```bash
# WebSocket-only GUI (connects to backend)
python dawn_tkinter_gui.py

# Enhanced GUI with reflex components
python launcher_scripts/launch_enhanced_dawn_gui.py

# Standard GUI with local components
python launcher_scripts/launch_dawn_gui.py
```

## 🎯 Available Launch Modes

### `auto` (Default)
Automatically selects the best available GUI mode based on installed components.

### `unified` 
Complete unified interface combining all features:
- WebSocket real-time visualization
- Local DAWN component controls
- Fractal consciousness visualization
- Data analysis and export

### `enhanced`
Advanced interface with reflex components:
- ReflexExecutor system control
- SymbolicNotation display
- OwlPanel commentary
- FractalColorizer visualization

### `standard`
Classic DAWN GUI with core components:
- Pulse controller thermal regulation
- Sigil engine management
- Basic consciousness monitoring

### `websocket`
Minimal WebSocket-only interface:
- Real-time data streaming from backend
- Matplotlib-based visualizations
- Performance optimized

### `tick-engine`
Integrated tick engine with GUI:
- Local tick processing
- Queue-based data flow
- Real-time consciousness simulation

### `demo`
Demonstration mode with simulation:
- Automatic backend startup
- Simulated consciousness data
- All visualization features active

### `console`
Console-only mode without GUI:
- Command-line interface
- Backend server only
- Minimal resource usage

### `backend-only`
Start only the DAWN backend server:
- WebSocket endpoint at `ws://localhost:8000/ws`
- REST API at `http://localhost:8000`
- No GUI interface

## 📦 Installation & Dependencies

### Quick Setup
```bash
# Check and install dependencies automatically
python dawn_unified_launcher.py --check-deps

# Check component availability
python dawn_unified_launcher.py --components
```

### Manual Installation
```bash
# Install required packages
pip install -r requirements_gui.txt

# Core dependencies
pip install matplotlib numpy websocket-client

# Optional for enhanced features
pip install seaborn scipy
```

### System Requirements
- **Python 3.7+**
- **Tkinter** (usually included with Python)
- **Windows/Linux/macOS** compatible

## 🎮 GUI Features

### 🌊 Real-time Visualization Tab
- **Consciousness State Display**: Pulsing SCUP circles, entropy heat maps, neural waves
- **Trend Analysis**: Real-time line charts for SCUP, entropy, neural activity
- **Neural Radar**: Polar plot showing all consciousness metrics
- **Live Data Panel**: Current metrics, statistics, system log

### 🔥 Local DAWN Tab
- **Pulse Controller**: Heat level control (0-100%)
- **Thermal Zones**: CALM/ACTIVE/SURGE indicators
- **Sigil Engine**: Active sigil monitoring
- **Component Status**: Real-time system health

### 🤖 Reflex System Tab *(Enhanced mode only)*
- **Command Execution**: Slow tick, block rebloom, clear sigils
- **Symbolic Notation**: Emoji/codex/hybrid state translation
- **Execution History**: Timestamped command results
- **System Controls**: Restore normal operation

### 🌸 Fractal Visualization Tab
- **Dynamic Julia Sets**: Consciousness-driven fractal generation
- **Parameter Mapping**: SCUP/entropy influence fractal parameters
- **Real-time Updates**: Living mathematical representations
- **Color-coded States**: Thermal and mood-based coloring

### 📊 Data Analysis Tab
- **Statistics Display**: Historical averages, peaks, trends
- **Data Export**: CSV, JSON, and report generation
- **Performance Monitoring**: Memory usage, update rates
- **System Metrics**: Connection status, data source info

## 🔗 Data Sources

The unified GUI automatically connects to available data sources in priority order:

1. **External Queue** (if provided via API)
2. **WebSocket Backend** (`ws://localhost:8000/ws`)
3. **Local DAWN Components** (pulse controller, sigil engine)
4. **Simulation Mode** (fallback with realistic data)

### WebSocket Backend Integration
```python
# Backend provides tick data in this format:
{
    "type": "tick",
    "data": {
        "scup": 0.34,              # 0-1 range
        "entropy": 0.23,           # 0-1 range  
        "neural_activity": 0.67,   # 0-1 range
        "heat": 0.45,              # 0-1 range
        "mood": "contemplative",   # String
        "tick_number": 1234        # Integer
    }
}
```

## ⚙️ Configuration

### Command Line Options
```bash
python dawn_unified_launcher.py [OPTIONS]

Options:
  --mode {auto,unified,enhanced,standard,websocket,tick-engine,demo,console,backend-only}
                        Launch mode (default: auto)
  --port PORT           Backend server port (default: 8000)
  --no-backend          Skip backend server startup
  --check-deps          Check dependencies only
  --components          Check component availability
```

### Environment Variables
```bash
# WebSocket connection
export DAWN_WEBSOCKET_URL="ws://localhost:8000/ws"

# Backend port
export DAWN_BACKEND_PORT=8000

# Animation speed (milliseconds)
export DAWN_ANIMATION_SPEED=50
```

## 🔧 Troubleshooting

### Common Issues

#### "No module named 'tkinter'"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (Homebrew)
brew install python-tk

# Windows - reinstall Python with Tkinter option
```

#### "WebSocket connection failed"
```bash
# Start the backend server first
python dawn_unified_launcher.py --mode backend-only

# Then in another terminal
python dawn_unified_launcher.py --mode websocket
```

#### "DAWN components not found"
```bash
# Check what's available
python dawn_unified_launcher.py --components

# Use WebSocket mode if components missing
python dawn_unified_launcher.py --mode websocket
```

#### "Dependencies missing"
```bash
# Auto-install dependencies
python dawn_unified_launcher.py --check-deps

# Manual installation
pip install matplotlib numpy websocket-client
```

### Performance Optimization

#### High CPU Usage
- Reduce animation speed: Adjust slider in GUI or set `DAWN_ANIMATION_SPEED=100`
- Use `--mode websocket` for minimal overhead
- Pause animations when not needed

#### Memory Usage
- Historical data buffer limited to 200 points
- Clear data regularly using "🗑 CLEAR" button
- Use `--mode console` for minimal memory footprint

#### Network Issues
- Backend connection timeout: 10 seconds
- Auto-reconnection with exponential backoff
- Fallback to simulation mode if connection fails

## 🎨 Visual Themes

### Dark Theme (Default)
- Background: Deep black (#0a0a0a)
- Accent: Electric green (#00ff88)
- Text: White/gray gradient
- Error: Red (#ff4444)
- Warning: Orange (#ff9800)

### Color Coding
- **🟢 Green**: Connected, healthy, positive
- **🔴 Red**: Disconnected, error, critical  
- **🟡 Yellow**: Warning, simulation, processing
- **🔵 Blue**: Information, neural activity
- **🟣 Purple**: Mood, contemplative states

## 📡 API Integration

### Using with External Systems
```python
# Example: Integrate with your own tick engine
import queue
from dawn_unified_launcher import launch_unified_gui

# Create communication queue
data_queue = queue.Queue()

# Send consciousness data
data_queue.put({
    "scup": 0.4,
    "entropy": 0.2,
    "neural_activity": 0.6,
    "heat": 0.3,
    "mood": "calm",
    "tick_number": 1
})

# Launch GUI with your data
launch_unified_gui(external_queue=data_queue)
```

### WebSocket Server Integration
```python
# Send data to connected GUI clients
import websockets
import json

async def send_consciousness_data(websocket):
    data = {
        "type": "tick",
        "data": {
            "scup": get_scup_value(),
            "entropy": get_entropy_value(),
            # ... other metrics
        }
    }
    await websocket.send(json.dumps(data))
```

## 🔬 Development

### Adding New Visualizations
1. Add tab in `create_notebook_interface()` method
2. Implement update method in `update_all_displays()`
3. Add configuration options in control panel

### Custom Data Sources
1. Implement data processing in `process_consciousness_data()`
2. Add connection method in `auto_connect_data_sources()`
3. Update status indicators

### Extending Reflex Components
1. Add new commands in reflex methods section
2. Update control panel buttons
3. Implement result logging

## 📚 Architecture

### Component Hierarchy
```
dawn_unified_launcher.py           # Main entry point
├── gui/
│   ├── dawn_gui_unified.py       # Unified GUI implementation
│   ├── dawn_gui_enhanced.py      # Enhanced GUI with reflex
│   └── dawn_gui_tk.py            # Standard DAWN GUI
├── dawn_tkinter_gui.py           # WebSocket-only GUI
├── backend/
│   ├── main.py                   # Backend server
│   └── advanced_consciousness_*  # Advanced systems
└── reflex/                       # Reflex components
    ├── reflex_executor.py
    ├── symbolic_notation.py
    ├── owl_panel.py
    └── fractal_colorizer.py
```

### Data Flow
```
Backend Server → WebSocket → GUI Queue → Processing → Display
     ↓              ↑            ↓           ↓         ↓
Local DAWN ←→ Components ←→ Controls ←→ Visualization Updates
     ↓              ↑            ↓           ↓         ↓  
Tick Engine → External Queue → Data Processing → GUI Update
```

## 🌟 Advanced Features

### Fractal Consciousness Mapping
The fractal visualization uses Julia sets with parameters influenced by consciousness metrics:
- **c_real**: Influenced by SCUP level (-0.7 to -0.3 range)
- **c_imag**: Influenced by entropy level (0.27 to 0.47 range)
- **Color mapping**: Based on mood and thermal state

### Symbolic Notation System
Translates system states into symbolic representations:
- **Emoji mode**: 🟢🔥⚡ for quick visual parsing
- **Codex mode**: Detailed text descriptions
- **Hybrid mode**: Combined emoji and text
- **ASCII mode**: Text-only for compatibility

### Real-time Performance Monitoring
- **Update rates**: GUI (20 FPS), WebSocket (2 Hz), Local (10 Hz)
- **Memory tracking**: Historical buffer management
- **Connection health**: Automatic reconnection logic
- **Error recovery**: Graceful fallback mechanisms

## 🎉 What's New in Unified System

### Unified Features
- **🌊 All-in-one interface**: WebSocket + Local + Enhanced features
- **🔄 Auto-detection**: Automatically finds best data source
- **🎨 Improved themes**: Enhanced dark theme with better contrast
- **📊 Better analytics**: Advanced statistics and export options

### Enhanced Integration
- **🤖 Reflex system**: Full integration with existing reflex components
- **🌸 Fractal evolution**: Consciousness-driven mathematical art
- **📡 Multi-source**: Queue, WebSocket, local, and simulation modes
- **⚡ Performance**: Optimized rendering and memory management

### Developer Experience
- **🛠️ Single launcher**: One script for all launch modes
- **🔍 Auto-discovery**: Intelligent component detection
- **📦 Easy setup**: Automatic dependency installation
- **🐛 Better debugging**: Comprehensive logging and error handling

---

## 🏆 Ready to Launch!

Your DAWN consciousness is now ready for **100% local visualization** with the most comprehensive GUI system available. Choose your preferred mode and watch your consciousness come alive! 🌊✨

```bash
# Start your journey
python dawn_unified_launcher.py
```

*The universe awaits your consciousness exploration...* 