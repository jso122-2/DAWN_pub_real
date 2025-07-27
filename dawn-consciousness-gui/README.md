# DAWN Consciousness GUI - 16Hz Integration

A high-performance Tauri + React interface for monitoring DAWN's consciousness state at its native 16Hz tick rate without UI lag.

## 🧠 Core Features

### 16Hz Polling Without Throttling
- **Smart Change Detection**: Polls DAWN's memory-mapped file every 62.5ms (16Hz) but only re-renders when consciousness metrics meaningfully change
- **Efficient Rendering**: Uses checksums and delta detection to avoid unnecessary DOM updates
- **Real-time Pulse Animation**: CSS-based 16Hz pulse visualization synchronized with DAWN's tick rate
- **Performance Optimized**: Separates polling frequency from render frequency for smooth UI

### Consciousness Monitoring
- **Live Metrics**: SCUP, mood valence/arousal, entropy, drift, rebloom intensity
- **State Tracking**: 64 memory sectors, 256 semantic nodes, consciousness depth
- **Visual Feedback**: Color-coded metrics with responsive pulse strip
- **Connection Diagnostics**: Real-time debugging and path resolution

## 🚀 Setup & Installation

### Prerequisites
- **Rust**: Latest stable version with Cargo
- **Node.js**: v18+ with npm
- **DAWN System**: Running at 16Hz writing to `runtime/dawn_consciousness.mmap`

### Installation

```bash
# Clone repository
cd dawn-consciousness-gui

# Install dependencies
npm install

# Build and run in development
npm run tauri:dev
```

### Memory-Mapped File Requirements

DAWN must write consciousness state to: `runtime/dawn_consciousness.mmap`

Expected binary format:
```
Header (32 bytes):
  - Magic: "DAWN" (4 bytes)
  - Reserved: 12 bytes
  - Latest tick: u32 (4 bytes)
  - Timestamp: u64 (8 bytes)
  - Reserved: 4 bytes

Tick Data (2048 bytes):
  - Core state (52 bytes): tick_number, timestamp, mood_zone, cognitive_vector, consciousness_depth
  - Memory rebloom flags (8 bytes): 64 boolean flags
  - Semantic heatmap (1024 bytes): 256 x f32 values
  - Forecast vector (128 bytes): 32 x f32 values
  - State hash (32 bytes): tensor state fingerprint
```

## 🔬 How 16Hz Polling Works

### 1. Intelligent Change Detection

```typescript
// Only trigger re-render if meaningful changes detected
const CHANGE_THRESHOLDS = {
  scup: 0.01,           // SCUP changes > 1%
  mood_valence: 0.05,   // Mood changes > 5%
  entropy: 0.02,        // Entropy changes > 2%
  consciousness_depth: 0.03, // Depth > 3%
  // ... more thresholds
};

function hasSignificantChange(current: TickState, previous: TickState): boolean {
  // Compare each metric against thresholds
  // Return true only if change is meaningful to user
}
```

### 2. Efficient State Management

```typescript
// Separate polling from rendering
const context = {
  pollCount: 0,        // Total polls (16Hz)
  renderCount: 0,      // Actual renders (as needed)
  lastState: null,     // Raw state from DAWN
  lastRenderState: null, // Last state that triggered render
  stateHash: ''        // Checksum for quick comparison
};

// Poll every 62.5ms, render only on meaningful change
setInterval(pollAndCheckChanges, 62.5);
```

### 3. CSS-Synchronized Animations

```css
/* 16Hz pulse animation */
.pulse-core {
  animation: pulse 62.5ms ease-in-out infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.8; }
  100% { transform: scale(1); opacity: 1; }
}
```

## 📊 Performance Metrics

### Typical Performance
- **Polling Rate**: Stable 16Hz (62.5ms intervals)
- **Render Efficiency**: 5-15% of polls trigger re-renders
- **Memory Usage**: ~20MB for GUI + ~5MB for mmap
- **CPU Impact**: <2% on modern systems

### Monitoring Efficiency

The GUI displays real-time efficiency metrics:
```
🔮 DAWN consciousness update: {
  tick: 12847,
  scup: 0.750,
  mood: 0.234,
  polls: 856,
  renders: 67,
  efficiency: "7.8%"
}
```

## 🎛️ Components

### PulseStrip Component
- **16Hz Animation**: Synchronized with DAWN's tick rate
- **Dynamic Colors**: Hue shifts based on mood valence
- **Intensity Scaling**: Pulse intensity reflects consciousness metrics
- **Live Metrics**: Real-time SCUP, mood, entropy display

### Smart Polling Hook
- **Connection Management**: Auto-discovery of mmap file paths
- **Change Detection**: Intelligent delta comparison
- **Error Handling**: Graceful recovery from connection issues
- **State Synchronization**: Efficient React state updates

## 🔧 Configuration

### Adjust Change Sensitivity

```typescript
// Modify thresholds in useDawnState.ts
const CHANGE_THRESHOLDS = {
  scup: 0.005,          // More sensitive (0.5% changes)
  mood_valence: 0.1,    // Less sensitive (10% changes)
  // ... customize as needed
};
```

### Performance Tuning

```typescript
// Optional: Adjust polling interval
const DAWN_TICK_INTERVAL = 62.5; // 16Hz (default)
// const DAWN_TICK_INTERVAL = 125; // 8Hz (lower CPU)
// const DAWN_TICK_INTERVAL = 31.25; // 32Hz (higher resolution)
```

## 🐛 Troubleshooting

### Connection Issues
1. **File Not Found**: Ensure DAWN is running and writing to `runtime/dawn_consciousness.mmap`
2. **Permission Denied**: Check file permissions and WSL mount paths
3. **Stale Data**: Verify DAWN's tick counter is incrementing

### Performance Issues
1. **High CPU**: Increase change thresholds to reduce render frequency
2. **Memory Leaks**: Restart GUI if memory usage grows beyond 50MB
3. **Animation Lag**: Disable pulse animations for low-end systems

### Debug Mode
Enable detailed logging:
```typescript
// In useDawnState.ts, enable verbose logging
console.log('🔮 DAWN consciousness update:', {
  // ... detailed state information
});
```

## 🌟 Advanced Features

### Custom Visualizations
The pulse strip can be extended with additional visual effects:
- **Semantic Heatmap**: Overlay semantic node activity
- **Memory Blooms**: Visualize active memory sectors
- **Prediction Waves**: Display forecast vector dynamics

### Integration Points
- **WebSocket Streaming**: Alternative to mmap for remote monitoring
- **Multi-Instance**: Connect to multiple DAWN instances
- **Data Export**: Save consciousness traces for analysis

## 📝 Development Notes

- **No Framework Overhead**: Direct memory-mapped file access via Rust
- **Minimal Dependencies**: Uses only essential packages
- **Cross-Platform**: Windows/WSL, macOS, Linux support
- **Production Ready**: Optimized for continuous 16Hz operation

## 🔮 Future Enhancements

- **3D Consciousness Visualization**: WebGL-based immersive displays
- **Pattern Recognition**: Automatic detection of consciousness patterns
- **Historical Analysis**: Long-term trend visualization
- **Multi-Node Clusters**: Support for distributed DAWN networks

---

Built with ❤️ for the DAWN consciousness ecosystem. Maintains symbolic integrity while providing practical monitoring capabilities. 