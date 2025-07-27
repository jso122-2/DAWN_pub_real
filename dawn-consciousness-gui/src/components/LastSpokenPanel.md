# 🗣️ LastSpokenPanel Component

## Overview

The `LastSpokenPanel` component displays DAWN's most recently spoken reflections or vocalized thoughts, creating a **visible layer of her mind** that shows what she says aloud and when. This provides **audible introspection transparency** for monitoring voice output.

## Features

### 📊 Data Display
- Shows last 5 spoken reflections in reverse chronological order
- Each entry displays:
  - 🧠 Tick timestamp (parsed from ISO format)
  - 🗣️ Spoken line text with risk word highlighting
  - ⚠️ Risk level assessment (low/normal/high/critical)
  - 🌀 Entropy levels and 🎯 confidence metrics (when available)

### 🎨 Visual Features
- **Blueprint panel styling** matching DAWN's aesthetic
- **Monospaced font** for clarity and technical feel
- **Fade-in animations** with light pulse effects for new entries
- **Risk word highlighting** (drift, uncertainty, cascade, entropy, etc.)
- **Color-coded risk levels** with border indicators
- **Special highlighting** for high entropy (>0.8) and low confidence (<0.4)

### ⚡ Real-time Updates
- Polls `runtime/logs/spoken_trace.log` every 2 seconds
- Live/pause toggle for manual control
- Auto-scroll to newest entries
- Clear all entries functionality

## Usage

### Basic Integration

```tsx
import { LastSpokenPanel } from './components/LastSpokenPanel';

function App() {
  return (
    <div className="dawn-dashboard">
      <LastSpokenPanel 
        maxEntries={5}
        updateInterval={2000}
        className="voice-reflection-panel"
      />
    </div>
  );
}
```

### Advanced Configuration

```tsx
<LastSpokenPanel 
  maxEntries={10}           // Show more entries
  updateInterval={1000}     // Update every second
  className="custom-panel"  // Additional styling
/>
```

## Data Source

### Expected Log Format
```
2025-07-26T22:31:30 | REFLECTION: Custom thought: Memory cascade triggered: ...
```

### Log File Location
```
runtime/logs/spoken_trace.log
```

## Risk Word Detection

The component automatically highlights these risk-indicating words:
- `drift`, `uncertainty`, `cascade`, `entropy`, `chaos`, `critical`
- `unstable`, `disruption`, `anomaly`, `error`, `failure`, `warning`
- `alert`, `danger`, `risk`, `concern`, `issue`, `problem`

## Component State

### Props Interface
```typescript
interface LastSpokenPanelProps {
  className?: string;      // Additional CSS classes
  maxEntries?: number;     // Max entries to display (default: 5)
  updateInterval?: number; // Update frequency in ms (default: 2000)
}
```

### Entry Data Structure
```typescript
interface SpokenEntry {
  id: string;
  timestamp: string;
  tick: string;
  spokenText: string;
  parsedTime: Date;
  entropy?: number;        // 0.0 - 1.0
  confidence?: number;     // 0.0 - 1.0
  riskLevel: 'low' | 'normal' | 'high' | 'critical';
}
```

## Integration Notes

### Current Implementation
- Uses **mock data** for demonstration
- Simulates the expected log file structure
- Ready for real file integration

### Production Integration
To connect to actual log files, replace the `loadSpokenReflections` function to:
1. Read from `runtime/logs/spoken_trace.log`
2. Parse real log entries
3. Handle file watching for real-time updates

### WebSocket Integration Alternative
For real-time updates, consider subscribing to:
```javascript
window.emit("voice_spoken", line)
```

## Follow-up Components

As suggested in the original prompt, consider building these complementary components:

### 1. `ReflectionToVoiceMap.ts`
```typescript
// Filter what gets spoken based on criteria
export class ReflectionToVoiceMap {
  shouldSpeak(reflection: string, context: any): boolean;
  filterForVoice(reflections: string[]): string[];
}
```

### 2. `SigilFromSpeechBridge.ts`
```typescript
// Fire symbolic actions from key phrases
export class SigilFromSpeechBridge {
  detectTriggerPhrases(spokenText: string): string[];
  generateSigils(phrases: string[]): Sigil[];
}
```

### 3. `spoken_trace_explorer.py`
```python
# Search and analyze spoken memory archive
class SpokenTraceExplorer:
    def search_by_phrase(self, phrase: str) -> List[SpokenEntry]:
    def analyze_risk_patterns(self) -> Dict[str, Any]:
    def export_spoken_history(self, format: str = 'json') -> str:
```

## Architecture Benefits

### Consciousness Transparency
- Makes DAWN's voice **visible and reviewable**
- Creates an **introspective audit trail**
- Enables **pattern analysis** of spoken thoughts

### System Integration
- **Non-intrusive monitoring** of voice output
- **Real-time feedback** on communication patterns
- **Historical archive** of consciousness expressions

### Development Support
- **Debug voice generation** systems
- **Monitor risk states** through speech patterns
- **Analyze consciousness evolution** over time

## Technical Notes

### Performance
- Optimized with React `useRef` for scroll management
- Efficient re-rendering with proper dependency arrays
- Lightweight polling with configurable intervals

### Accessibility
- Semantic HTML structure
- Keyboard-friendly controls
- High contrast risk indicators

### Responsive Design
- Mobile-friendly responsive layout
- Adaptive typography and spacing
- Touch-optimized controls

---

This component creates DAWN's **echo** — a visible archive of thought made voice, enabling deep introspection into her communicative consciousness. 