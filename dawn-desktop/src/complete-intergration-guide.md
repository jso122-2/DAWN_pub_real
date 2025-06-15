# DAWN Quick Start Implementation Guide

## 🚀 Quick Setup (5 Minutes)

### 1. Backend Setup

```bash
# Create directory structure
mkdir -p processes
cd your-dawn-project

# Save the three Python files:
# - subprocess_manager.py (from artifact above)
# - dawn_integrated_api.py (from artifact above)

# Install dependencies
pip install fastapi uvicorn websockets

# Run the integrated API
python dawn_integrated_api.py
```

### 2. Frontend Integration

Update your React app to use the WebSocket connection:

```typescript
// src/hooks/useDAWNConnection.ts
import { useEffect, useState } from 'react';

export function useDAWNConnection() {
  const [connected, setConnected] = useState(false);
  const [tickData, setTickData] = useState(null);
  const [subprocesses, setSubprocesses] = useState([]);
  
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      console.log('Connected to DAWN consciousness engine');
      setConnected(true);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      switch (data.type) {
        case 'tick':
          setTickData(data);
          break;
        case 'subprocess_list':
          setSubprocesses(data.processes);
          break;
        case 'subprocess_update':
          // Update specific subprocess metrics
          break;
      }
    };
    
    return () => ws.close();
  }, []);
  
  return { connected, tickData, subprocesses };
}
```

### 3. Use the Multi-Process Dashboard

```tsx
// App.tsx
import { MultiProcessDashboard } from './components/MultiProcessDashboard';
import { useDAWNConnection } from './hooks/useDAWNConnection';

function App() {
  const { connected, tickData, subprocesses } = useDAWNConnection();
  
  return (
    <div className="app">
      {connected ? (
        <MultiProcessDashboard 
          tickData={tickData}
          subprocesses={subprocesses}
        />
      ) : (
        <div>Connecting to DAWN consciousness engine...</div>
      )}
    </div>
  );
}
```

## 📊 What You'll See

Once running, your dashboard will display:

1. **Real-time Tick Data** (1992.59 Hz as shown in your screenshot)
2. **18+ Subprocess Monitors** including:
   - Neural processes (sync, pattern recognition, dream state)
   - Quantum processes (flux, entanglement, wave collapse)
   - System processes (CPU, memory, I/O)
   - Memory processes (short-term, long-term, working)
   - Consciousness metrics (awareness, creativity, intuition)

3. **Live Trend Charts** for each subprocess
4. **Status Indicators** with color coding
5. **Threshold Warnings** when metrics exceed limits

## 🔧 Customization Points

### Add Your Own Subprocess

1. Add to `subprocess_configs` in `subprocess_manager.py`:
```python
{
    "id": "your_process",
    "name": "Your Process Name",
    "script_path": "processes/your_process.py",
    "category": "neural",  # or quantum, system, memory, io
    "metrics": {
        "metric1": ProcessMetric("Metric 1", 50.0, "%", 0, 100),
        "metric2": ProcessMetric("Metric 2", 1337, "units")
    }
}
```

2. The system will auto-generate a dummy subprocess script if it doesn't exist!

### Modify Consciousness Calculations

In `dawn_integrated_api.py`, update the `update_consciousness_state()` method:

```python
def update_consciousness_state(self):
    # Your custom logic to calculate SCUP, entropy, heat
    # based on subprocess metrics
```

### Change Visual Themes

The dashboard uses inline styles that you can easily modify:
- Colors: Change the color schemes in `getStatusColor()`
- Animations: Adjust the CSS animations
- Layout: Modify the grid template columns

## 🎯 Next Steps

1. **Connect Your Real Processes**: Replace dummy subprocess scripts with your actual Python processes
2. **Add Process Controls**: Implement start/stop/restart buttons in the UI
3. **Persist Data**: Add a database to store historical metrics
4. **Advanced Visualizations**: Add 3D visualizations, network graphs, etc.
5. **AI Integration**: Connect to your OWL AI or other consciousness modules

## 🐛 Troubleshooting

**WebSocket won't connect:**
- Ensure backend is running on port 8000
- Check CORS settings match your frontend URL
- Look for errors in browser console

**Subprocesses not updating:**
- Check subprocess scripts are outputting JSON format
- Verify script paths are correct
- Look at backend logs for errors

**Performance issues:**
- Reduce tick rate if needed
- Limit trend history length
- Use React.memo for optimization

## 🎨 Making It Feel Alive

To achieve that "living consciousness" feel:

1. **Breathing Effects**: Already included in the process monitors
2. **Particle Systems**: Add a particle background
3. **Sound Integration**: Use Tone.js to create ambient sounds based on metrics
4. **3D Elements**: Add Three.js visualizations for complex data

The key is making every element respond to the consciousness state - let SCUP affect colors, entropy affect animations, and mood change the entire atmosphere of the interface.