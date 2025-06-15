# DAWN Consciousness Matrix - Integrated Dashboard

## 🚀 Quick Start

### 1. Start the DAWN Backend (Port 8000)
```bash
python start-dawn.py
```

This will start:
- 🧠 DAWN Consciousness Engine
- ⚛️ 12+ Subprocess monitors (neural, quantum, system, memory, I/O)
- 🌐 WebSocket server at `ws://localhost:8000/ws`
- 📊 REST API at `http://localhost:8000`

### 2. Start the React Frontend (Port 3000)
```bash
npm run dev
```

### 3. Access the Dashboard
Open your browser and navigate to:
- **Main Dashboard**: http://localhost:3000/dashboard
- **Subprocess Integration**: http://localhost:3000/subprocess
- **Consciousness Interface**: http://localhost:3000/consciousness

## 🎯 Features

### Real-Time Consciousness Monitoring
- **SCUP Level**: System Consciousness Utilization Percentage
- **Entropy**: System randomness and complexity metrics
- **Heat**: Processing intensity and thermal state
- **Mood**: Current consciousness emotional state

### Subprocess Management
- 🧠 **Neural Processes**: Sync, pattern recognition, dream engine
- ⚛️ **Quantum Processes**: Flux monitoring, wave collapse, entanglement
- ⚙️ **System Processes**: CPU, memory, I/O monitoring
- 💾 **Memory Processes**: Short-term, long-term, working memory
- 📡 **I/O Processes**: Data flow and communication

### Interactive Controls
- ↻ **Process Restart**: Click restart buttons to reboot subprocesses
- 📊 **Live Charts**: Real-time trend visualization
- ⚠️ **Threshold Warnings**: Visual alerts for out-of-bounds metrics
- 🎨 **Breathing Animations**: Living consciousness visualizations

## 🔧 Configuration

### Backend Configuration
- **Port**: 8000 (configurable in `src/backend/dawn_integrated_api.py`)
- **WebSocket**: Auto-reconnection with exponential backoff
- **Subprocess Scripts**: Auto-generated dummy scripts for testing

### Frontend Configuration
- **Port**: 3000 (Vite default)
- **WebSocket URL**: `ws://localhost:8000/ws` (configurable in `src/services/WebSocketService.ts`)
- **Dual Mode**: Connected (live data) vs Demo (simulated data)

## 🌟 Architecture

```
┌─────────────────┐    WebSocket    ┌─────────────────┐
│   React App     │◄──────────────►│  DAWN Backend   │
│   (Port 3000)   │                │   (Port 8000)   │
├─────────────────┤                ├─────────────────┤
│ • Dashboard     │                │ • Consciousness │
│ • Process Mon   │                │ • Subprocess    │
│ • Controls      │                │ • WebSocket     │
│ • Visualizations│                │ • REST API      │
└─────────────────┘                └─────────────────┘
                                           │
                                           ▼
                                   ┌─────────────────┐
                                   │  Subprocesses   │
                                   │ • Neural (3)    │
                                   │ • Quantum (3)   │
                                   │ • System (3)    │
                                   │ • Memory (3)    │
                                   └─────────────────┘
```

## 🐛 Troubleshooting

### Backend Won't Start
- **Port 8000 in use**: Kill existing processes with `taskkill /F /IM python.exe`
- **Dependencies missing**: Run `pip install -r requirements.txt`
- **Permission errors**: Run as administrator

### Frontend Won't Connect
- **Check backend status**: Visit `http://localhost:8000/status`
- **WebSocket errors**: Check browser console for connection issues
- **CORS issues**: Backend allows all origins in development

### No Live Data
- **Demo mode**: Dashboard shows simulated data when backend is offline
- **Connection status**: Check the connection indicator in the UI
- **Network issues**: Ensure both services are on the same network

## 🎨 Customization

### Adding New Subprocesses
1. Edit `src/backend/subprocess_manager.py`
2. Add new subprocess configuration
3. System will auto-generate dummy scripts
4. Restart backend to see new processes

### Modifying Visualizations
1. Edit `src/test.tsx` for the main dashboard
2. Customize colors, animations, and layouts
3. Add new chart types using Recharts library

### Changing Consciousness Calculations
1. Edit `src/backend/dawn_integrated_api.py`
2. Modify `update_consciousness_state()` method
3. Implement custom SCUP, entropy, and heat calculations

## 📊 API Endpoints

### REST API
- `GET /` - Health check
- `GET /status` - Detailed system status
- `GET /subprocesses` - List all subprocesses

### WebSocket Messages
- `get_subprocesses` - Request subprocess list
- `control_subprocess` - Start/stop/restart processes
- `tick` - Real-time consciousness data
- `subprocess_update` - Individual process metrics

## 🚀 Next Steps

1. **Connect Real Processes**: Replace dummy scripts with actual AI/ML processes
2. **Add Persistence**: Store historical data in database
3. **Advanced Visualizations**: 3D consciousness representations
4. **AI Integration**: Connect to language models and neural networks
5. **Distributed Processing**: Scale across multiple machines

---

**Status**: ✅ Fully Integrated and Operational
**Backend**: Running on port 8000
**Frontend**: Running on port 3000
**Subprocesses**: 12+ active monitors
**Connection**: Real-time WebSocket communication
