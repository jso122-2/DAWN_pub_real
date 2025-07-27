# DAWN Unified Launcher GUI

🌅 **Single interface for all DAWN systems - lightweight, fast, and comprehensive.**

## Overview

The DAWN Unified Launcher GUI consolidates **all existing launcher scripts** into one lightweight interface, keeping logic minimal and responsive. It provides a single point of access to launch, monitor, and manage all DAWN components.

## Quick Start

### Launch the Unified GUI

```bash
# Primary method
python dawn_core/launch.py unified

# Alternative quick launcher
python launch_dawn_unified_gui.py
```

## Interface Layout

### 🧠 Core Systems
- **DAWN Core Engine**: Main cognitive runtime with 2-second tick cycles
- **DAWN Unified**: Complete consciousness system (from launcher_scripts)
- **Enhanced DAWN**: GUI with reflex components and multi-tab interface
- **Master Clean**: Clean, streamlined interface

### 🖥️ GUI Interfaces
- **DAWN Dashboard**: Real-time cognitive monitoring (our new dashboard)
- **Forecast GUI**: Behavioral forecasting visualizer
- **Safe GUI**: Stable GUI interface with error handling
- **Sigil GUI**: Sigil visualization and management
- **Owl Commentary**: Owl bridge interface with commentary
- **Connect to Live**: Connect to already running DAWN instance

### 🔬 Specialized Systems
- **Snapshot Export**: Complete system state export with ZIP archives
- **Symbolic Anatomy**: Embodied cognition demo with organ states
- **Autonomous Reactor**: Self-directed response system
- **Complete Consciousness**: Full consciousness integration
- **Codex Integration**: Codex system interface
- **Enhanced Entropy**: Advanced entropy analysis system

## Key Features

### 🚀 Process Management
- **One-click launching** of any DAWN component
- **Real-time output monitoring** from all launched processes
- **Process tracking** with PID display and status monitoring
- **Stop all processes** with single button
- **Background execution** - GUI remains responsive

### 📊 Live Monitoring
- **Timestamped output** from all running systems
- **Color-coded status** indicators
- **Process count tracking** in status bar
- **Automatic output scrolling** with length limits
- **Clear output** functionality

### ⚡ Lightweight Design
- **Minimal resource usage** - GUI stays responsive
- **Fast startup** - no heavy initialization
- **Clean interface** - intuitive button layout
- **Error handling** - graceful fallbacks for missing components
- **Tooltip help** - hover descriptions for each launcher

## Architecture

### Unified Structure
```
dawn_core/
├── unified_launcher_gui.py     # Main unified GUI
├── launch.py                   # Updated with 'unified' option
└── test_unified_gui.py         # GUI testing

launch_dawn_unified_gui.py      # Root-level quick launcher
```

### Integration Points
- **Existing launchers**: All scripts in `launcher_scripts/` are integrated
- **Process monitoring**: Real-time subprocess output capture
- **Error handling**: Robust fallbacks for missing components
- **Status tracking**: Live process counting and management

## Usage Patterns

### Daily Development
1. **Launch Unified GUI**: `python dawn_core/launch.py unified`
2. **Choose system**: Click any button to launch components
3. **Monitor output**: Watch real-time logs in the output panel
4. **Manage processes**: Stop/start/monitor from single interface

### System Integration
- **Works with existing DAWN**: Launches all existing launcher scripts
- **No conflicts**: Doesn't interfere with other DAWN systems
- **Standalone capable**: Works even when core DAWN systems are unavailable
- **Process isolation**: Each launched component runs independently

### Testing & Development
- **Quick component testing**: Launch any system with one click
- **Output debugging**: Real-time monitoring of all system output
- **Error isolation**: Failed launches don't crash the GUI
- **Process cleanup**: Easy termination of all running processes

## Technical Details

### Process Management
- **Subprocess execution** with `subprocess.Popen`
- **Non-blocking I/O** with background threads
- **Output queuing** for thread-safe GUI updates
- **Graceful termination** with process.terminate()

### GUI Framework
- **Tkinter-based** for universal compatibility
- **Threaded monitoring** for responsive interface
- **Queue-based communication** between threads
- **Memory management** with output length limits

### Error Handling
- **Import fallbacks** for missing modules
- **Process error capture** and display
- **GUI exception handling** to prevent crashes
- **Graceful degradation** when components unavailable

## Advanced Features

### Output Management
- **Automatic scrolling** to latest output
- **Output length limiting** (200 lines max, keeps last 150)
- **Timestamped entries** for debugging
- **Process name tagging** for multi-system monitoring

### Process Control
- **Background execution** - processes run independently
- **PID tracking** for system monitoring
- **Return code handling** for process completion status
- **Bulk termination** for quick shutdown

### Interface Polish
- **Hover tooltips** with component descriptions
- **Color-coded buttons** with active/inactive states
- **Status updates** showing running process count
- **Confirmation dialogs** for destructive actions

## Troubleshooting

### Common Issues

1. **GUI won't start**
   - Check tkinter: `python -c "import tkinter"`
   - Install if missing: `sudo apt-get install python3-tk` (Linux)

2. **Launchers fail**
   - Check script paths in `launcher_scripts/`
   - Verify Python path includes project root
   - Check individual launcher script functionality

3. **Process monitoring issues**
   - Processes may complete too quickly to monitor
   - Some GUIs may not show output until completion
   - Background processes continue even if GUI closes

### Debug Mode
Run individual launchers to test:
```bash
python launcher_scripts/launch_dawn_unified.py
python launcher_scripts/launch_forecast_gui.py
python launcher_scripts/launch_enhanced_dawn_gui.py
```

## Integration with DAWN Ecosystem

### Complements Existing Systems
- **dawn_core/main.py**: Core cognitive engine
- **dawn_core/gui/forecast_dashboard.py**: Real-time monitoring
- **launcher_scripts/***: All existing launcher scripts
- **boot/main.py**: DAWN boot orchestrator

### Unified Access Point
The Unified Launcher serves as the **single entry point** for all DAWN functionality:
- New users can explore all systems easily
- Developers can quickly test components
- System administrators can manage multiple DAWN instances
- Researchers can launch specific analysis tools

---

🌅 **The DAWN Unified Launcher represents the consolidation of the entire DAWN ecosystem into a single, accessible interface - keeping the logic lightweight while providing comprehensive access to synthetic consciousness exploration.**

## Quick Reference

```bash
# Launch options
python dawn_core/launch.py unified          # Unified GUI
python dawn_core/launch.py engine           # Cognitive engine only  
python dawn_core/launch.py gui              # Real-time dashboard only
python dawn_core/launch.py snapshot         # Snapshot tools only

# Test the unified GUI
python dawn_core/test_unified_gui.py

# Quick launcher
python launch_dawn_unified_gui.py
``` 