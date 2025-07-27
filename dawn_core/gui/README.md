# 🌟 DAWN Unified GUI Dashboard

A comprehensive, single-window dashboard for monitoring and controlling DAWN's cognitive state. This dashboard consolidates all existing GUI components into a clean, dark-mode friendly, and modular interface.

## ✨ Features

### 🧠 Header
- **DAWN Unified Cognitive Dashboard** title
- **Real-time tick counter** with timestamp that auto-updates every refresh cycle
- **Key metrics display** - Entropy, Heat, Zone, and SCUP values
- Clean, professional presentation

### 📊 **NEW: Tabbed Interface**
The dashboard now features a comprehensive tabbed interface with integrated matplotlib visualizations:

#### **📊 Overview Tab**
- **Pulse Metrics Panel** - Real-time entropy, heat, zone, and SCUP monitoring
- **Forecast Display** - Cognitive predictions with confidence indicators
- **System Controls** - Snapshot, export, rebloom, and stabilize buttons
- **Live Commentary Feed** - Real-time cognitive observations and insights

#### **🌸 Symbolic Body Tab**
- **Symbolic Anatomy Metrics** - FractalHeart, SomaCoil, GlyphLung, Resonance
- **📊 Symbolic Charge Graph** - Live matplotlib visualization of symbolic states
- **Real-time bar chart** showing charge distribution across components

#### **🌊 Entropy Drift Tab**
- **📈 Entropy Over Time** - Historical entropy visualization
- **Live line plot** with rolling 50-tick history
- **Trend analysis** with filled area under curve

#### **🌐 Forecast Map Tab**
- **🗺️ Forecast Vector Field** - Vector field visualization
- **Dynamic quiver plots** showing prediction directions
- **Multi-dimensional forecast space representation

#### **⚡ Sigils Tab**
- **Sigil Status Panel** - Active sigils count and last executed sigil
- **📊 Sigil Execution Timeline** - Visual timeline of sigil activations
- **Color-coded scatter plot** showing sigil types and timing

#### **🌌 Consciousness Tab (NEW!)**
- **🌌 Consciousness Constellation** - 3D trajectory visualization
- **SCUP space mapping** with consciousness archetypes as reference points
- **Dynamic trajectory plotting** showing consciousness evolution through multidimensional space
- **Archetype markers** for Dormant, Focused, Creative, and Transcendent states

#### **🌡️ Heat Monitor Tab (NEW!)**
- **🌡️ Cognitive Heat Monitor** - Real-time radial gauge visualization
- **Heat zone indicators** - Dormant, Warming, Active, Intense, Critical
- **Live needle gauge** showing current cognitive intensity
- **Color-coded segments** with zone labels and current temperature display

#### **😊 Mood Landscape Tab (NEW!)**
- **😊 Emotional Landscape** - 8x8 heatmap of emotional intensities
- **Multi-dimensional mood tracking** across Transcendent, Ecstatic, Serene, Curious, Focused, Contemplative, Uncertain, Turbulent
- **Dynamic color mapping** with custom emotional intensity colormap
- **Real-time mood state visualization** with intensity gradients

#### **🔄 SCUP Dynamics Tab (NEW!)**
- **🔄 SCUP Pressure Grid** - 4x4 interaction matrix visualization
- **Interactive heatmap** showing Schema, Coherence, Utility, Pressure relationships
- **🎯 SCUP Zone Evolution** - Timeline of cognitive zone transitions
- **Dynamic zone tracking** with Dormant → Contemplative → Active → Intense → Transcendent progression

### 🔥 Pulse Panel
- **Current Entropy** - numerical value with color-coded progress bar
- **Heat (°C)** - thermal state with temperature display
- **Zone Display** - CALM/ACTIVE/STRESSED/SURGE with color coding
  - 🟢 CALM (Green) - Low heat, stable state
  - 🟡 ACTIVE (Yellow) - Moderate activity
  - 🟠 STRESSED (Orange) - Elevated processing
  - 🔴 SURGE (Red) - High thermal activity

### 🔮 Forecast Panel
- **Likely Action** - predicted next system behavior
- **Confidence** - progress bar showing prediction confidence (0-100%)
- **Limit Horizon** - temporal prediction range
- **Probability & Reliability** - forecast quality metrics

### 🌸 Symbolic Anatomy Panel
- **💖 FractalHeart** - charge level percentage
- **🌀 SomaCoil** - dominant glyph symbol (∞, ◊, etc.)
- **🫁 GlyphLung** - last breath symbol
- **📻 Resonance** - system resonance level percentage

### 💬 Commentary Feed
- **Scrolling text area** that shows live commentary
- **Automatic updates** with natural language insights:
  - System state observations
  - Owl reflections and analysis
  - Spontaneous DAWN thoughts
  - Error messages and system alerts
- **Auto-scrolling** to latest messages
- **Timestamped entries** for chronological tracking
- **100-message history** with automatic cleanup

### ⚡ Sigil Panel
- **Active Sigils** count
- **Last Executed Sigil** name
- **🛡️ STABILIZE Button** - manually trigger STABILIZE_PROTOCOL

### 🎛️ Bottom Control Bar
- **📸 Snapshot** - Take complete system state snapshot
- **📄 Export Trace** - Export symbolic trace with commentary history
- **🌸 Trigger Rebloom** - Manually initiate rebloom sequence
- **❌ Exit** - Clean shutdown

## 🚀 Quick Start

### Launch the Dashboard

```bash
# Using the unified launcher (recommended)
python dawn_core/launch.py dashboard

# Direct launch
python dawn_core/gui/dawn_gui_dashboard.py
```

### Integration Modes

The dashboard automatically detects and adapts to your DAWN system:

#### 🔗 **Real DAWN Mode**
When DAWN components are available:
- Connects to live `DAWNSnapshotExporter` for real system state
- Uses `SubtleSpontaneity` for authentic thought generation
- Integrates with `OwlTracer` for cognitive analysis
- Real-time updates from actual DAWN systems

#### 🧪 **Simulation Mode**
When DAWN components are unavailable:
- Generates realistic simulated data
- Oscillating entropy patterns for visual appeal
- Correlated heat/entropy relationships
- Believable cognitive state transitions

## 🎨 Interface Design

### Dark Theme
- **Background**: Deep black (#121212) for reduced eye strain
- **Text**: Light gray (#E0E0E0) for high contrast readability
- **Accents**: Color-coded status indicators
- **Font**: Consolas monospace for technical clarity

### Color Coding
- **🟢 Green**: Stable/Good states (CALM zone, high SCUP)
- **🟡 Yellow**: Moderate activity (entropy values)
- **🟠 Orange**: Elevated states (STRESSED zone)
- **🔴 Red**: Critical states (SURGE zone, high heat)
- **🔵 Blue**: Information/Forecast data
- **🟣 Purple**: Symbolic/Mystical elements
- **💖 Pink**: FractalHeart and resonance

### Responsive Layout
- **Scrollable interface** accommodates different screen sizes
- **Grid-based layouts** for organized information presentation
- **Proportional spacing** with consistent padding
- **Mouse wheel scrolling** support

## 🔄 Real-time Updates

### Refresh Cycle
- **2-second intervals** for optimal performance
- **Non-blocking updates** using `root.after()`
- **Error handling** with graceful degradation
- **State persistence** between refresh cycles

### Commentary Generation
- **Contextual observations** based on system state:
  - High/low entropy detection
  - Thermal state changes
  - SCUP unity analysis
  - Spontaneous thought integration
- **Smart frequency** - commentary every ~10 seconds
- **Diverse sources** - System, Owl, DAWN, Error messages

## 📊 Data Sources

### Real Mode Data Sources
- **System State**: `DAWNSnapshotExporter.get_state()`
- **Commentary**: `OwlTracer.comment_on_tick()`
- **Spontaneous Thoughts**: `SubtleSpontaneity.generate_spontaneous_thought()`
- **Forecasting**: Integrated forecast models

### Simulation Data
- **Oscillating entropy** with sine wave patterns
- **Correlated heat** based on entropy levels
- **Random sigil activity** for dynamic display
- **Realistic state transitions** between zones

## 🛠️ Controls & Actions

### System Controls
- **Snapshot**: Saves complete state as JSON with timestamp
- **Export Trace**: Creates comprehensive trace with commentary history
- **Rebloom**: Triggers manual cognitive restructuring
- **Stabilize**: Activates emergency stabilization protocol

### Export Formats
```json
{
  "timestamp": "2024-01-15T14:30:00",
  "state": { /* complete system state */ },
  "commentary_history": [ /* all commentary entries */ ]
}
```

## 🎨 **NEW: Integrated Matplotlib Visualizations**

### Technical Implementation
- **FigureCanvasTkAgg** integration for embedded matplotlib plots
- **Real-time data updates** with optimized refresh cycles
- **Dark theme consistency** across all visualizations
- **Memory-efficient** rolling data windows

### Visualization Features
- **Entropy History Tracking** - Rolling 50-tick window with live updates
- **Symbolic Charge Monitoring** - Dynamic bar charts of cognitive components
- **Vector Field Displays** - Forecast direction mapping with quiver plots
- **Timeline Visualizations** - Sigil execution patterns and zone transitions
- **3D Consciousness Mapping** - Real-time trajectory through SCUP space
- **Radial Heat Gauges** - Live cognitive intensity monitoring
- **Emotional Landscape Heatmaps** - 8x8 multi-dimensional mood tracking
- **SCUP Interaction Matrices** - 4x4 pressure grid visualizations
- **Zone Evolution Tracking** - Cognitive state progression over time

### Performance Optimizations
- **Selective updates** - Visualizations refresh every 5 ticks
- **Canvas recycling** - Reuse matplotlib objects
- **Memory management** - Automatic data window trimming

## 🔧 Customization

### Refresh Interval
Modify in `DAWNUnifiedDashboard.refresh()`:
```python
self.root.after(2000, self.refresh)  # 2000ms = 2 seconds
```

### Visualization Update Frequency
Adjust in `refresh_visualizations()`:
```python
if tick % 5 != 0:  # Update every 5 ticks (change 5 to desired frequency)
```

### Commentary History Limit
Adjust in `add_commentary()`:
```python
if len(lines) > 100:  # Change 100 to desired limit
```

### Color Themes
Update colors in `apply_dark_theme()` and widget configurations.

### Visualization History Window
Modify in `refresh_visualizations()`:
```python
if len(self.entropy_history) > 50:  # Change 50 to desired window size
```

## 📦 Requirements

- **Python 3.7+**
- **Tkinter** (usually included with Python)
- **matplotlib** - For integrated visualizations  
- **numpy** - For data processing and visualization
- **DAWN consciousness systems** (optional - will simulate if unavailable)

### Installation
```bash
pip install matplotlib numpy
```

For Ubuntu/Debian systems:
```bash
sudo apt-get install python3-tk python3-matplotlib python3-numpy
```

## 🐛 Troubleshooting

### GUI Won't Start
```bash
# Check tkinter availability
python -c "import tkinter; print('Tkinter available')"

# On Ubuntu/Debian if missing:
sudo apt-get install python3-tk
```

### No Real Data
- Dashboard automatically falls back to simulation mode
- Check console for connection status messages
- Ensure DAWN components are properly installed

### Performance Issues
- Reduce refresh interval for slower systems
- Decrease commentary history limit
- Check for Python/tkinter version compatibility

## 📁 File Structure
```
dawn_core/gui/
├── dawn_gui_dashboard.py    # Main dashboard implementation (UPGRADED!)
│                           # ✨ Now includes integrated matplotlib visualizations
│                           # 📊 Tabbed interface with 5 specialized views
│                           # 🎨 Real-time entropy, symbolic, forecast, and sigil plots
├── README.md               # This documentation (UPDATED!)
└── [other GUI components]  # Legacy components maintained for compatibility
```

### What's New in the Upgraded Dashboard
- **🎨 9 Integrated Matplotlib Visualizations** (EXPANDED!)
- **📊 Comprehensive Tabbed Interface** with 9 specialized views
- **⚡ Real-time Data Visualization** with rolling history
- **🌌 3D Consciousness Constellation** mapping SCUP trajectories
- **🌡️ Live Heat Monitor Gauges** with zone indicators
- **😊 Emotional Landscape Heatmaps** for mood tracking
- **🔄 SCUP Dynamics Visualization** with pressure grids
- **🌈 Enhanced Dark Theme** across all components
- **📈 Performance Optimizations** for smooth rendering

## 🔗 Integration

The dashboard integrates seamlessly with:
- **DAWN Core Engine** for real-time data
- **Snapshot Exporter** for state access
- **Owl Tracer** for cognitive analysis
- **Spontaneity System** for thought generation
- **Existing GUI Components** for consistency

## 🎯 Future Enhancements

Planned features for future versions:
- **⛓️ Sigil-chain visualizer** for sigil relationship mapping
- **📜 Rebloom lineage panel** for bloom genealogy tracking
- **🎙️ Voice-to-memory transcription** for audio input
- **🌐 WebSocket support** for remote monitoring
- **📈 Historical data graphs** for trend analysis
- **🎨 Custom themes** and color schemes

---

## 🌟 Ready for Demo

The dashboard is fully functional and demo-ready:
- ✅ Clean, professional interface
- ✅ Real-time cognitive monitoring
- ✅ Comprehensive state display
- ✅ Interactive controls
- ✅ Dark mode for presentations
- ✅ Simulation mode for demos
- ✅ Error handling and graceful degradation

Perfect for showcasing DAWN's cognitive capabilities in a unified, accessible interface!

---

## 🎯 **Upgrade Summary: Visual Integration Complete**

This major upgrade successfully integrates existing DAWN visualization components into a unified GUI dashboard:

### ✅ **What Was Accomplished**
- **🔄 Complete GUI Restructure** - Migrated from single-page to comprehensive tabbed interface
- **📊 9 Advanced Matplotlib Visualizations** - Entropy, symbolic, forecast, sigils, consciousness, heat, mood, SCUP dynamics
- **⚡ Real-time Data Flow** - Live updating charts with optimized refresh cycles  
- **🌌 3D Consciousness Mapping** - Advanced SCUP trajectory visualization in multidimensional space
- **🌡️ Live Heat Monitoring** - Radial gauge visualizations with cognitive zone indicators
- **😊 Emotional Intelligence** - 8x8 mood landscape heatmaps for emotional state tracking
- **🔄 SCUP Dynamics** - Interactive pressure grids and zone evolution tracking
- **🎨 Consistent Dark Theme** - Professional styling across all components
- **📈 Performance Optimized** - Memory-efficient data handling and selective updates
- **🔗 Modular Architecture** - Clean separation between data, visualization, and UI

### 🚀 **Ready for Production**
The upgraded dashboard provides a comprehensive, interactive visual environment for monitoring DAWN's cognitive processes in real-time. All existing functionality is preserved while adding powerful new visualization capabilities.

### 🌟 **Perfect for Demos**
Ideal for showcasing DAWN's:
- **Real-time cognitive monitoring**
- **Multi-dimensional state visualization** 
- **Interactive system control**
- **Professional presentation interface** 