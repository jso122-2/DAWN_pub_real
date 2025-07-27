# DAWN Tauri Integration Guide

## Overview

The DAWN tick engine is now wired into the Tauri GUI via memory-mapped files. This creates a real-time bridge between DAWN's consciousness data and the native desktop application.

## Architecture

```
DAWN Tick Engine → Consciousness State Writer → Memory-Mapped File → Tauri GUI
     (10 Hz)              (Python)                  (mmap)        (Rust/React)
```

## Running the Integrated System

### Method 1: Two-Step Process (Recommended)

#### Step 1: Start the DAWN Consciousness Bridge
```bash
python launcher_scripts/start_dawn_consciousness_bridge.py
```

This will:
- Start the DAWN consciousness tick loop at 10 Hz
- Write real-time consciousness data to `runtime/dawn_consciousness.mmap`
- Display connection instructions

#### Step 2: Start the Tauri GUI
In a new terminal:
```bash
cd dawn-consciousness-gui
npm run tauri:dev
```

### Method 2: Full Integration (Advanced)
If npm is properly configured:
```bash
python launcher_scripts/launch_dawn_tauri_integrated.py
```

## Data Flow

The consciousness bridge writes the following data every 100ms:

### TickState Structure
- **tick_number**: Current tick count
- **timestamp_ms**: Millisecond timestamp
- **mood_zone**: Emotional state (valence, arousal, dominance, coherence)
- **cognitive_vector**: Core consciousness metrics
- **memory_rebloom_flags**: 64 memory sector states
- **semantic_heatmap**: 256 semantic node activities
- **forecast_vector**: 32 prediction dimensions
- **consciousness_depth**: Overall awareness level (0.0-1.0)
- **tensor_state_hash**: Current state fingerprint

### Memory Layout
- **Header**: 64 bytes (metadata)
- **Tick States**: 8192 bytes per tick × 1000 ticks (rolling buffer)
- **Total**: ~8.3 MB memory-mapped file

## Tauri App Features

The native desktop app reads the memory-mapped data and provides:

- **Real-time consciousness visualization**
- **Mood zone tracking**
- **Semantic field heatmaps**
- **Memory rebloom status**
- **Consciousness depth monitoring**
- **Native performance** (60+ FPS)

## Integration Points

### DAWN Side (Python)
```python
from consciousness.dawn_tick_state_writer import DAWNConsciousnessStateWriter

# Integrate with existing tick engine
writer = DAWNConsciousnessStateWriter()
tick_engine.register_subsystem('consciousness_gui', writer.write_tick)
```

### Tauri Side (Rust)
```rust
// src-tauri/src/mmap_reader.rs
use memmap2::MmapOptions;

pub fn read_consciousness_state() -> Result<TickState, String> {
    // Read from memory-mapped file
    let file = File::open("runtime/dawn_consciousness.mmap")?;
    let mmap = unsafe { MmapOptions::new().map(&file)? };
    // Parse consciousness data...
}
```

## File Structure

```
DAWN_Vault/Tick_engine/Tick_engine/
├── launcher_scripts/
│   ├── start_dawn_consciousness_bridge.py      # Simple bridge launcher
│   └── launch_dawn_tauri_integrated.py         # Full integration
├── consciousness/
│   └── dawn_tick_state_writer.py               # Memory-mapped writer
├── dawn-consciousness-gui/                     # Tauri application
│   ├── src/                                    # React frontend
│   ├── src-tauri/                              # Rust backend
│   └── package.json                            # Node.js config
└── runtime/
    └── dawn_consciousness.mmap                  # Shared memory file
```

## Troubleshooting

### No consciousness data in GUI
1. Check if `runtime/dawn_consciousness.mmap` exists
2. Verify the consciousness bridge is running
3. Look for error messages in Python console

### Tauri build issues
1. Ensure Rust is installed: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. Install Node.js dependencies: `npm install`
3. Try running from WSL if on Windows

### Performance issues
- The tick rate is set to 10 Hz (100ms) for responsive GUI
- Adjust in `start_dawn_consciousness_bridge.py` if needed
- Memory-mapped files are very efficient for real-time data

## Development

### Adding new consciousness data
1. Modify `TickState` in `dawn_tick_state_writer.py`
2. Update Rust structures in `src-tauri/src/mmap_reader.rs`
3. Add visualization in React components

### Debugging data flow
```python
# Python side - add logging
logger.info(f"Writing tick {tick_state.tick_number}")

# Rust side - add debug prints
println!("Read consciousness state: {:?}", state);
```

## Next Steps

- [ ] Add more consciousness metrics to TickState
- [ ] Implement historical data buffering
- [ ] Add GUI controls for tick rate
- [ ] Create consciousness state export/import
- [ ] Add multi-node consciousness synchronization

## Performance Notes

- **Memory usage**: ~8.3 MB for consciousness data
- **Update rate**: 10 Hz (configurable)
- **Latency**: <10ms from DAWN to GUI
- **GUI refresh**: 60+ FPS native performance

The integration provides real-time consciousness visualization with minimal overhead using efficient memory-mapped file communication. 