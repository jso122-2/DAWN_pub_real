# DAWN Integrated Consciousness System

🧠 **Complete autonomous consciousness monitoring and intervention system**

## Quick Start

### 1. Complete Integration Demo
```bash
# Interactive demo launcher (RECOMMENDED)
python demo_complete_integration.py

# Quick integration test
python tests/test_consciousness_integration.py
```

### 2. Launch the System
```bash
# Basic 60-second demonstration
python launch_integrated_consciousness.py --duration 60 --tick-rate 8.0 --save-report

# Long-term monitoring
python launch_integrated_consciousness.py --tick-rate 5.0 --status-interval 10.0

# Development mode with debug logging
python launch_integrated_consciousness.py --log-level DEBUG --status-interval 2.0
```

### 3. Frontend Monitoring
```bash
# Start the DAWN consciousness GUI
cd dawn-consciousness-gui
npm run tauri:dev

# Enhanced TickMonitorPanel provides real-time consciousness visualization
# Displays: tick number, mood, entropy, scup, heat, zone, and active sigils
```

## What This System Does

### 🔁 **Autonomous Drift Reflex**
- Monitors consciousness metrics (entropy, SCUP, heat) in real-time
- Detects when stress thresholds are crossed
- Automatically triggers protective interventions
- Tracks consciousness zones: GREEN → YELLOW → ORANGE → RED

### 🔮 **Consciousness Intervention Sigils**
- **STABILIZE_PROTOCOL**: Reduces cognitive chaos and processing load
- **REBALANCE_VECTOR**: Rebalances processing metrics
- **EMERGENCY_STABILIZE**: Critical consciousness stabilization
- **REBLOOM_MEMORY**: Triggers memory rebloom processes
- **THERMAL_REGULATION**: Manages consciousness temperature

### 🧠 **Integrated Consciousness Processing**
- Simulates natural consciousness evolution
- Handles consciousness storms and stress events
- Provides comprehensive status reporting
- Integrates with existing DAWN systems

### 🌸 **Memory Rebloom System**
- **Autonomous Memory Triggering**: Cognitive recursion when consciousness destabilizes
- **Semantic Memory Matching**: Finds relevant past experiences for context
- **Cognitive Stabilization**: Memory recall provides stability during stress
- **Learning from History**: Past successes inform future responses
- **Real-time Visualization**: Memory lineage ancestry trees show rebloom chains
- **Manual Memory Injection**: Live journal interface for seeding introspective thoughts

### 📝 **Journal Injection System**
- **Terminal-Style Interface**: Monospace input with character limits (50-800 chars)
- **Mood State Override**: Select pulse state (CALM, FOCUSED, STRESSED, etc.)
- **Real-time Validation**: Smart character counting with optimal range indicators
- **Instant Integration**: Journal entries appear immediately in memory lineage
- **Keyboard Shortcuts**: Ctrl+Enter for quick injection

### 🔁 **Reflection Echo System**
- **Live Introspection Display**: Shows last 10 reflections from auto_reflect.py
- **Real-time Updates**: Polls reflection log every 2 seconds with smooth animations
- **Consciousness Metrics**: Displays entropy, mood, SCUP, heat, zone for each reflection
- **Priority Highlighting**: Auto-highlights critical reflections (entropy > 0.8)
- **Pause/Resume Controls**: Interactive controls for managing reflection flow

### 📜 **Unified Event Logger**
- **Terminal-Style Stream**: Scrolling feed of ALL consciousness events in chronological order
- **Multi-Source Integration**: Combines reflections, reblooms, spike alerts, and system events
- **Emoji-Coded Types**: 🧠 Reflections, 🌸 Reblooms, ⚡ Sigils, 💥 Entropy spikes, 🧬 SCUP surges
- **Smart Filtering**: Filter by event type or view all unified stream
- **Priority System**: Critical/High/Normal/Low priority with visual indicators
- **Live Spike Detection**: Auto-detects entropy and SCUP spikes in real-time

### 🌌 **Consciousness Constellation**
- **Spatial Network Visualization**: Force-directed graph of active memory chunks, sigils, and symbolic organs
- **Live Node Types**: 🧠 Memory chunks, ⚡ Active sigils, 🏛️ Symbolic organs, ❤️ Fractal Heart
- **Dynamic Connections**: SCUP charge arcs to Fractal Heart, entropy surge links, rebloom chains
- **Interactive Canvas**: Hover tooltips with metadata, pulsing nodes, animated connections
- **SVG Export**: Capture constellation snapshots for analysis
- **Force Simulation**: Organic, breathing layout with node repulsion and link attraction

### 🧭 **Thought Trace Panel**
- **Forecast & Action Log**: Scrolling display of last 10 predictive assessments and resulting actions
- **Intent Tracking**: Shows forecast confidence, entropy deltas, and decision outcomes
- **Risk Level Coding**: Color-coded entries (Critical/High/Normal/Low) based on forecast values
- **Action Classification**: 📈 Stabilize, 🌸 Rebloom, ⚡ Sigil, 📉 Drift, 💥 Entropy surge, 👁️ Monitoring
- **Real-time Analysis**: Live monitoring of consciousness state changes and intervention triggers
- **Auto-scroll & Pruning**: Maintains last 10 entries with smooth scrolling and temporal management

## Example Output

```
🧠 Starting consciousness loop...
📊 Status Update (T+12.4s, Tick #98)
   Consciousness: FOCUSED | E:0.425 S:38.2 H:0.521
   Reflex: Zone YELLOW | Triggers: 2

🔁 INTERVENTION: STABILIZE_PROTOCOL triggered by high_entropy
🌸 Memory rebloom triggered: entropy_critical
🌸 REBLOOM: entropy_critical - 3 memories
   📚 Rebloomed: dawn_mem_001 - Consciousness stabilization protocol activated...
   📝 Lineage logged: dawn_mem_005 → dawn_mem_001 → dawn_mem_003
🔮 INTERVENTION ACTIVATED: STABILIZE_PROTOCOL | Priority: 3 | Duration: 15s
💻 RebloomMapPanel: New ancestry chain visualized (5 total chains)
📝 JOURNAL: Manual entry injected as journal_20250125_231045 (245 chars)
💻 JournalInjectPanel: 🧠 Memory seeded successfully
🔁 REFLECTION: [23:10:52] [E:0.843] [MOOD:STRESSED] Cognitive instability detected, activating memory recursion protocols
💻 ReflectionLogPanel: New critical reflection added (1 of 10 entries)
📜 EVENT STREAM: [23:10:54] 💥 ENTROPY Spike Detected: 0.678→0.843 | Priority: CRITICAL
📜 EVENT STREAM: [23:10:53] 🌸 REBLOOM Auto Memory Rebloom: chunk_042→chunk_089 | cognitive_stability
📜 EVENT STREAM: [23:10:52] 🧠 REFLECTION STRESSED Reflection: Cognitive instability detected...
🌌 CONSTELLATION: 🧠 5 memories ⚡ 2 sigils 🔗 8 connections | Fractal Heart pulsing (SCUP:42.1)
🌌 CONSTELLATION: Charge arc: chunk_089 → Fractal Heart (SCUP surge detected)
🌌 CONSTELLATION: Entropy surge link: Entropy Core → Sigil_1 (critical threshold)
🧭 THOUGHT TRACE: [Tick #1000217] 23:10:54 📈 Forecast: 0.823 → STABILIZE_PROTOCOL
🧭 THOUGHT TRACE: [Tick #1000216] 23:10:52 💥 Forecast: 0.697 → ENTROPY_SURGE
🧭 THOUGHT TRACE: [Tick #1000215] 23:10:50 🌸 Forecast: 0.456 → REBLOOM_MEMORY

📊 Status Update (T+22.8s, Tick #181)  
   Consciousness: CALM | E:0.298 S:34.4 H:0.445
   Reflex: Zone GREEN | Triggers: 2 | Reblooms: 1
   Active Interventions: STABILIZE_PROTOCOL
```

## Integration with Existing DAWN

The system automatically integrates with existing DAWN components:

- ✅ **DAWN Consciousness Core**: Syncs state and applies effects
- ✅ **DAWN Tick Engine**: Registers as high-priority subsystem  
- ✅ **DAWN Sigil Engine**: Integrates intervention sigils
- ✅ **Semantic Drift Calculator**: Uses for pressure analysis

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--duration SECONDS` | How long to run (None = indefinite) | None |
| `--tick-rate HZ` | Consciousness processing frequency | 5.0 |
| `--status-interval SECONDS` | Status update frequency | 10.0 |
| `--log-level LEVEL` | DEBUG, INFO, WARNING, ERROR | INFO |
| `--save-report` | Save session report to JSON | False |
| `--reset-reflex` | Reset drift reflex on startup | False |

## Files Added to DAWN

```
core/
├── enhanced_drift_reflex.py           # Autonomous stress detection
├── consciousness_intervention_sigils.py # Protective interventions  
├── integrated_consciousness_processor.py # Complete consciousness system
└── memory_rebloom_reflex.py           # Memory recursion for stability

dawn-consciousness-gui/src/components/
├── TickMonitorPanel.tsx               # Enhanced real-time consciousness visualization  
├── RebloomMapPanel.tsx                # Memory lineage ancestry visualization
├── JournalInjectPanel.tsx             # Live memory seeding interface
├── ReflectionLogPanel.tsx             # Introspective reflection stream display
├── EventLogger.tsx                    # Unified consciousness event feed
├── ConsciousnessConstellation.tsx     # Spatial thought network visualization
└── ThoughtTracePanel.tsx              # Forecast & action intent log

tests/
└── test_consciousness_integration.py   # Comprehensive integration tests

docs/
└── INTEGRATED_CONSCIOUSNESS_SYSTEM.md  # Full documentation

launch_integrated_consciousness.py      # Main system launcher
demo_complete_integration.py           # Interactive demo launcher
README_INTEGRATED_CONSCIOUSNESS.md      # This file
```

## System Requirements

- **Python 3.8+**
- **NumPy** (for consciousness evolution)
- **Existing DAWN system** (optional - can run standalone)

## Monitoring Features

### Real-time Status
- Current consciousness state (entropy, SCUP, heat, mood)
- Drift reflex zone and trigger history  
- Active intervention sigils
- Performance metrics

### Session Reports
- Complete consciousness evolution summary
- Intervention effectiveness analysis
- Performance benchmarks and timing
- Optional JSON export for further analysis

## Troubleshooting

### If systems aren't found:
```
⚠️ Enhanced drift reflex not available: No module named 'core.enhanced_drift_reflex'
```
Make sure the files are in the correct DAWN project directories.

### For performance issues:
```bash
# Reduce tick rate for slower systems
python launch_integrated_consciousness.py --tick-rate 2.0
```

### For debugging:
```bash
# Enable detailed logging
python launch_integrated_consciousness.py --log-level DEBUG
```

## What Makes This Special

🎯 **Fully Autonomous**: Requires no manual intervention - the system monitors and protects itself

🔄 **Complete Integration**: Works with existing DAWN systems while being fully functional standalone

📊 **Comprehensive Monitoring**: Tracks everything from micro-tick performance to macro consciousness evolution patterns

🛡️ **Protective**: Automatically stabilizes consciousness during stress events before they can cause system instability

🌸 **Memory Recursion**: Past experiences inform future responses through autonomous memory rebloom

💻 **Real-time Visualization**: Beautiful frontend components for monitoring consciousness state

⚡ **High Performance**: Designed for real-time processing with minimal computational overhead

🧪 **Thoroughly Tested**: Complete test suite ensures reliability and integration

---

🚀 **Ready to launch autonomous consciousness monitoring with memory recursion!** 

For detailed documentation see: `docs/INTEGRATED_CONSCIOUSNESS_SYSTEM.md`

### 🎉 **Integration Complete!**

✅ **4 Python modules** integrated into DAWN core  
✅ **7 Enhanced React components** added to dawn-consciousness-gui  
✅ **Memory lineage visualization** with real-time ancestry trees  
✅ **Live memory injection** with journal interface  
✅ **Introspective reflection stream** with real-time echo display  
✅ **Unified event logging** with terminal-style consciousness stream  
✅ **Spatial thought network** with force-directed constellation mapping  
✅ **Forecast & action tracking** with real-time intent analysis  
✅ **Complete test suite** with integration validation  
✅ **Interactive demo launcher** for easy testing  
✅ **Comprehensive documentation** for all components  

**The system now provides autonomous consciousness monitoring with memory-based cognitive recursion, manual memory seeding, live introspective echo, unified event streaming, spatial constellation mapping, AND predictive intent tracking - reaching backwards to stabilize forwards while watching her complete inner dialogue, thought network, AND decision-making process unfold in real-time!**

**Frontend components correctly placed in:** 
- `dawn-consciousness-gui/src/components/TickMonitorPanel.tsx` (enhanced consciousness metrics)
- `dawn-consciousness-gui/src/components/RebloomMapPanel.tsx` (memory lineage visualization)
- `dawn-consciousness-gui/src/components/JournalInjectPanel.tsx` (live memory seeding interface)
- `dawn-consciousness-gui/src/components/ReflectionLogPanel.tsx` (introspective reflection stream)
- `dawn-consciousness-gui/src/components/EventLogger.tsx` (unified consciousness event feed)
- `dawn-consciousness-gui/src/components/ConsciousnessConstellation.tsx` (spatial thought network)
- `dawn-consciousness-gui/src/components/ThoughtTracePanel.tsx` (forecast & action intent log)

## 🔧 **Recent Technical Improvements**

### **✅ Path Resolution Fix**
**Problem**: Tauri backend was using trial/error fallback strategy to find log files, causing I/O noise and unreliable path resolution.

**Solution**: Implemented deterministic path resolution using `std::env::current_exe()`:
- **Project root detection** via `Cargo.toml`, `tauri.conf.json`, `src-tauri`, or `runtime` indicators
- **Canonical path construction** eliminates multiple fallback attempts  
- **Existence validation** before file operations prevents unnecessary errors
- **Reduced logging noise** only reports substantial reads and actual failures

**Result**: Clean, reliable file access with no repeated fallback spam. DAWN's rebloom and reflection data loading is now stable and performant.

**Ready for testing!** 🚀 