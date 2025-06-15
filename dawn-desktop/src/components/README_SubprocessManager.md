# 🌊 Unified Visual Subprocess Manager - Port 3000

## 🎯 **Perfect Integration Complete!**

Your **UnifiedVisualSubprocessManager** successfully merges all existing subprocess management logic from:

- ✅ **ProcessViewer** (toggle functionality)
- ✅ **PythonProcessManager** (tick-aware processes)  
- ✅ **ProcessControlPanel** (resource management)
- ✅ **ProcessFlowManager** (3D visualization concepts)
- ✅ **ProcessManagementDashboard** (unified interface)

## 🚀 **Quick Usage**

### 1. **Basic Integration**
```tsx
import UnifiedVisualSubprocessManager from './components/UnifiedVisualSubprocessManager';

function App() {
  return (
    <div className="h-screen w-full">
      <UnifiedVisualSubprocessManager 
        port={3000}
        onProcessToggle={(id, enabled) => console.log(`${id}: ${enabled}`)}
        globalEntropy={0.5}
      />
    </div>
  );
}
```

### 2. **Advanced Integration with Logging**
```tsx
import { SubprocessIntegrationExample } from './components/SubprocessIntegrationExample';

// Use the complete example with system stats and logging
function DawnApp() {
  return <SubprocessIntegrationExample />;
}
```

## 🎛️ **Features Available**

### **Process Management**
- 🔄 **Toggle Enable/Disable** - Full process control
- 👁️ **Toggle Visibility** - Show/hide in visualizations  
- ⚡ **Execute/Kill** - Runtime process control
- 📊 **Real-time Metrics** - CPU, Memory, FPS monitoring

### **View Modes**
- 🗂️ **Grid View** - Card-based visual layout
- 📋 **List View** - Category-organized hierarchical view
- 🔍 **Detail Modal** - Full process configuration

### **Categories**
- 🧠 **Neural** - Neural activity, network flow, cognitive radar
- ⚡ **Consciousness** - Consciousness analyzers, state processors
- 🖥️ **System** - System diagnostics, entropy reducers
- 💾 **Memory** - Memory consolidators, storage management
- 🌌 **Quantum** - Quantum state processors
- ⚙️ **Processing** - General processing modules

### **Smart Features**
- 🔌 **Auto-reconnect WebSocket** to port 3000
- 🎯 **Tick-awareness** - Processes triggered by system states
- 🎨 **Visual Status** - Color-coded status indicators
- 📈 **Live Updates** - Real-time process metrics
- 🔍 **Filtering** - Show only enabled/visible processes

## 🎯 **Port 3000 WebSocket Protocol**

Your component expects these WebSocket message types:

### **Incoming Messages**
```json
// Tick updates
{ "type": "tick", "tick_number": 12345, "scup": 0.75, "entropy": 0.3 }

// Process list
{ "type": "subprocess_list", "processes": [...] }

// Process updates  
{ "type": "subprocess_update", "processId": "neural-processor", "updates": {...} }
```

### **Outgoing Messages**
```json
// Toggle process
{ "action": "toggle_process", "processId": "consciousness-analyzer" }

// Execute process
{ "action": "execute_process", "processId": "memory-consolidator", "parameters": {...} }

// Kill process
{ "action": "kill_process", "processId": "entropy-reducer" }
```

## 🎨 **Default Processes Included**

1. **Neural Activity Visualizer** - Real-time EEG visualization (Running)
2. **Consciousness Analyzer** - Pattern correlation analysis (Idle)
3. **Memory Consolidator** - Memory pattern consolidation (Queued) 
4. **Entropy Reducer** - System entropy management (Stopped)
5. **Quantum State Processor** - Quantum consciousness processing (Hidden)

## ⚙️ **Customization**

### **Add New Process Categories**
```tsx
// Extend the category type
category: 'neural' | 'consciousness' | 'system' | 'memory' | 'quantum' | 'processing' | 'your_new_category'

// Add icon in getCategoryIcon()
case 'your_new_category': return <YourIcon className="w-4 h-4" />;
```

### **Custom Process Triggers**
```tsx
const customProcess: UnifiedProcess = {
  id: 'custom-analyzer',
  name: 'Custom Analyzer',
  category: 'processing',
  triggers: {
    onTick: 50,                               // Every 50 ticks
    onSCUP: { operator: '>', value: 0.8 },    // When SCUP > 0.8
    onEntropy: { operator: '<', value: 0.3 }, // When entropy < 0.3
    onMood: ['excited', 'focused'],           // On specific moods
    onSignal: 'custom_signal'                 // On custom signals
  }
};
```

## 🔧 **Backend Integration**

To connect to a real backend on port 3000:

1. **Start WebSocket Server**
```python
# Your existing DAWN API with WebSocket support
python dawn_integrated_api.py  # Should serve on port 3000
```

2. **Process Management**
```python
# In your Python backend
async def handle_toggle_process(process_id: str):
    # Toggle your actual subprocess
    if process_id in active_processes:
        stop_process(process_id)
    else:
        start_process(process_id)
```

## 🎯 **Ready to Use!**

Your **UnifiedVisualSubprocessManager** is production-ready and combines all your existing subprocess management functionality into one powerful interface for port 3000!

Simply import and use - it handles all the complexity internally while providing a beautiful, functional interface for managing your visual subprocesses.

```tsx
// That's it! 🚀
<UnifiedVisualSubprocessManager port={3000} />
``` 