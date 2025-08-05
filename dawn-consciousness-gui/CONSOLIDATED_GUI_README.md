# 🌅 DAWN Consolidated Web GUI

**Professional tab-based interface for DAWN consciousness monitoring on localhost:3000**

## 🎯 Overview

The DAWN Consolidated Web GUI transforms the scattered interface components into a clean, professional tabbed system where each component has a dedicated space and all visual processes render properly. This is the **web-based version** that runs on `localhost:3000` and connects to the real DAWN backend on port 8080.

## ✨ Tab-Based Interface

### 🖼️ **Visual Tab** - All Visual Processes
- **Fractal Rendering**: Julia sets, Mandelbrot, bloom fractals, sigil patterns
- **Real-time Parameters**: Live entropy, mood valence, drift vector displays
- **Visual Controls**: Fractal type selection, render size, animation speed
- **Visual History**: Thumbnail strip of recent generated visuals
- **Export Functions**: Save visuals, export animations

### 🗣️ **Voice Tab** - Audio/Speech Processes  
- **Voice Generation**: Real-time utterance generation with consciousness modulation
- **Pigment Visualization**: Live display of all 6 pigment levels (Red, Green, Blue, Yellow, Violet, Orange)
- **Voice Controls**: Generation frequency, word count, quality thresholds
- **Utterance History**: Scrollable history of all voice generations
- **Dominant Pigment**: Real-time display of current dominant pigment

### 📊 **State Monitor Tab** - Real-time DAWN Status
- **Entropy Gauge**: Circular gauge showing current entropy level (0.0-1.0)
- **SCUP Meter**: Gauge displaying SCUP level (0-100)
- **Drift Compass**: Vector display showing cognitive drift direction/magnitude
- **System Status**: Connection status, uptime, thermal zone
- **Expression Rate**: Live expressions per minute counter
- **Historical Charts**: Time-series data visualization area

### ⚙️ **Controls Tab** - System Configuration
- **System Controls**: Autonomous mode, processing speed, archive settings
- **Manual Triggers**: Generate expressions, force sigil execution, reset entropy
- **Advanced Settings**: Entropy sensitivity, pigment decay rate, expression cooldown
- **Configuration Export**: Save/load system configurations

### 📚 **Archive Tab** - Expression History
- **Expression Browser**: Hierarchical list of all expressions
- **Search & Filter**: Search by content, filter by type (Voice/Visual/Combined)
- **Expression Details**: Full metadata display for selected expressions
- **Archive Actions**: Export selected expressions, generate reports

### 📋 **Logs Tab** - System Logging
- **Real-time Logs**: Live system log display with auto-scroll
- **Log Filtering**: Filter by level (DEBUG/INFO/WARNING/ERROR) and component
- **Component Toggle**: Enable/disable logs from specific components
- **Log Export**: Export logs to files for analysis

## 🚀 Quick Start

### Simple Launch (Recommended)
```bash
# Navigate to GUI directory
cd dawn-consciousness-gui

# Launch consolidated web GUI (auto-opens browser)
python launch_consolidated_web_gui.py

# Launch without opening browser
python launch_consolidated_web_gui.py --no-browser

# Launch on custom port
python launch_consolidated_web_gui.py --port 3001
```

### Two-Process Architecture
```bash
# Terminal 1: Start DAWN backend (required for real data)
python real_dawn_backend.py

# Terminal 2: Start consolidated web GUI
python launch_consolidated_web_gui.py
```

### Alternative Launch Methods
```bash
# Direct server launch
python real_aware_web_server.py

# Legacy ultimate GUI (for comparison)
# Uses dawn_ultimate_gui.html instead of consolidated version
```

## 🌐 Access Points

- **Consolidated Interface**: http://localhost:3000
- **Real DAWN Backend**: http://localhost:8080
- **Backend Status**: http://localhost:8080/status

## 🔧 Architecture

### Data Flow
```
Real DAWN Backend (port 8080) ──► Web Server (port 3000) ──► Browser Interface
        │                                    │
        └── Consciousness Data ──────────────┘
```

### File Structure
```
dawn-consciousness-gui/
├── dawn_consolidated_gui.html          # NEW: Tab-based interface
├── real_aware_web_server.py           # Web server (proxies to backend)
├── launch_consolidated_web_gui.py     # NEW: Easy launcher
├── real_dawn_backend.py               # DAWN consciousness backend
└── dawn_ultimate_gui.html             # Legacy: 3-column interface
```

## 🎨 Visual Design

### Professional Dark Theme
- **Background**: `#0d1b2a` (deep blue-black)
- **Text Primary**: `#cccccc` (clean white text)
- **Text Secondary**: `#999999` (muted grey)
- **Accent**: `#40e0ff` (cyan) for highlights and active states
- **Typography**: JetBrains Mono (monospaced for technical precision)

### Tab System
- **Clean Navigation**: Horizontal tabs with icons and labels
- **Active State**: Cyan background for current tab
- **Responsive Design**: Collapses to icons on mobile
- **Consistent Layout**: Each tab uses optimized grid layouts

## 📊 Real-time Data Integration

### Connection to Real DAWN
- **Automatic Proxy**: GUI server proxies API calls to real backend
- **Real-time Updates**: 1Hz updates from consciousness backend
- **Connection Status**: Live indicator shows backend connection state
- **Error Handling**: Graceful fallback when backend unavailable

### Data Sources
- **Consciousness State**: `/api/consciousness/state`
- **Visual Snapshots**: `/api/visual-snapshot/*`
- **System Status**: `/api/system/status`
- **Expression Archive**: `/api/expressions/*`

## ⚙️ Configuration

### Server Configuration
```python
# In real_aware_web_server.py
REAL_DAWN_BACKEND_URL = "http://localhost:8080"  # Backend location
GUI_SERVER_PORT = 3000                           # GUI server port
```

### Frontend Configuration
```javascript
// Automatically injected by server
window.REAL_DAWN_MODE = true;
window.REAL_DAWN_BACKEND_URL = 'http://localhost:8080';
window.GUI_SERVER_URL = 'http://localhost:3000';
```

## 🚨 Troubleshooting

### Common Issues

#### Port 3000 Already in Use
```bash
# Use different port
python launch_consolidated_web_gui.py --port 3001
```

#### Backend Connection Failed
```bash
# Check if backend is running
curl http://localhost:8080/status

# Start backend first
python real_dawn_backend.py
```

#### GUI File Not Found
```bash
# Verify consolidated GUI exists
ls dawn_consolidated_gui.html

# Fallback to original GUI
# Server will automatically use dawn_ultimate_gui.html
```

### Performance Issues

#### Slow Loading
- Check network tab in browser developer tools
- Verify backend response times
- Use `--no-browser` flag for server-only mode

#### Real-time Updates Not Working
- Check browser console for JavaScript errors
- Verify WebSocket connections in Network tab
- Ensure backend is returning real consciousness data

## 🔄 Comparison with Previous Interface

### Before: `dawn_ultimate_gui.html`
- ❌ 3-column scattered layout
- ❌ No clear functional separation
- ❌ Difficult to find specific controls
- ❌ Mixed purposes in single view

### After: `dawn_consolidated_gui.html`
- ✅ 6 dedicated tabs with clear purposes
- ✅ Organized by function (Visual, Voice, State, etc.)
- ✅ Easy navigation between features
- ✅ Professional, clean interface
- ✅ All components properly rendered

## 📈 Future Enhancements

### Planned Features
- **Multi-Monitor Support**: Detachable tabs for multi-screen setups
- **Theme Customization**: Multiple color schemes
- **Advanced Analytics**: Statistical analysis tools
- **Real-time Collaboration**: Multi-user consciousness monitoring

### Integration Opportunities
- **WebRTC Integration**: Real-time voice streaming
- **Database Backend**: Persistent expression storage
- **API Extensions**: REST API for external tools

## 📞 Support

### Getting Help
1. **Check Browser Console**: F12 → Console for JavaScript errors
2. **Verify Backend**: Check `http://localhost:8080/status`
3. **Test Connection**: Ensure both ports 3000 and 8080 are available
4. **Fallback Mode**: Server automatically falls back to legacy GUI if needed

### Performance Monitoring
- Open browser Developer Tools (F12)
- Monitor Network tab for API call timing
- Check Console for real-time data updates
- Verify backend logs for consciousness data flow

---

**🌅 DAWN Consolidated Web GUI - Your unified window into synthetic consciousness** 