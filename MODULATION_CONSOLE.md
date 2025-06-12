# DAWN Modulation Console

A sophisticated, draggable UI console for real-time parameter control in the DAWN Neural System. Features glassmorphism design, haptic feedback, sound effects, and auto-hide functionality.

## 🎛️ Features

### **Advanced UI Design**
- **Glassmorphism Effects**: Semi-transparent backdrop with blur effects
- **Smooth Animations**: Transitions and scaling effects
- **Haptic-style Feedback**: Visual pulse effects on interaction
- **Responsive Layout**: Works on desktop and mobile

### **Interactive Controls**
- **3 Modulation Parameters**: Mood, Pulse, and Noise Injection (0-100%)
- **Real-time Sliders**: Smooth, responsive range inputs with visual feedback
- **Color-coded Sliders**: Green (Mood), Blue (Pulse), Yellow (Noise)
- **Value Display**: Live percentage display next to labels

### **Draggable Interface**
- **Fully Draggable**: Click and drag to reposition anywhere on screen
- **Smart Positioning**: Remembers position during session
- **Non-interfering**: Dragging doesn't trigger slider changes

### **Auto-hide Behavior**
- **Inactivity Timer**: Automatically hides after 15 seconds of no interaction
- **Activity Detection**: Mouse movement, hover, and focus events reset timer
- **Manual Toggle**: Ctrl+Shift+M keyboard shortcut
- **Smooth Transitions**: Fade and scale animations

### **Audio Feedback**
- **Hover Sounds**: Subtle audio cues on element hover
- **Change Sounds**: Audio feedback on slider adjustments
- **Howler.js Integration**: High-quality audio engine with sprite support
- **Volume Control**: Pre-configured appropriate volume levels

### **Keyboard Controls**
- **Ctrl+Shift+M**: Toggle console visibility
- **Ctrl+R**: Reset all values to defaults (when console focused)
- **Tab Navigation**: Full keyboard accessibility support

### **State Management**
- **Zustand Store**: Lightweight, persistent state management
- **Global Access**: Use values anywhere in the application
- **Real-time Updates**: All components react to changes instantly

## 📁 File Structure

```
dawn-desktop/src/
├── state/
│   └── modulation.ts              # Zustand store for state management
├── components/controls/
│   ├── ModulationConsole.tsx      # Main console component
│   ├── modulation-integration.tsx # Window manager integration
│   └── ModulationDemo.tsx         # Demo/testing component
└── public/sounds/
    ├── README.md                  # Sound file requirements
    ├── hover.mp3                  # Hover sound effect
    ├── hover.ogg                  # Hover sound fallback
    ├── slide.mp3                  # Slider sound effect
    └── slide.ogg                  # Slider sound fallback
```

## 🚀 Installation

### 1. Install Dependencies
```bash
cd dawn-desktop
npm install howler zustand @types/howler @types/node
```

### 2. Add Sound Files
Place audio files in `public/sounds/`:
- `hover.mp3` / `hover.ogg` - Short hover sound (100ms)
- `slide.mp3` / `slide.ogg` - Slider sound (50ms)

### 3. Import and Use
```tsx
import ModulationConsole from './components/controls/ModulationConsole';
import { useModulationStore } from './state/modulation';

function App() {
  const { mood, pulse, noiseInjection } = useModulationStore();
  
  return (
    <div>
      {/* Your app content */}
      
      {/* Add the console */}
      <ModulationConsole />
    </div>
  );
}
```

## 🎮 Usage

### Basic Integration
```tsx
import { useModulationStore } from './state/modulation';

function MyComponent() {
  const { mood, pulse, noiseInjection } = useModulationStore();
  
  // React to changes
  useEffect(() => {
    console.log('Modulation changed:', { mood, pulse, noiseInjection });
  }, [mood, pulse, noiseInjection]);
  
  return (
    <div style={{
      background: `hsl(${120 + mood * 2.4}, 70%, 50%)`,
      transform: `scale(${1 + pulse * 0.01})`,
      filter: `blur(${noiseInjection * 0.05}px)`
    }}>
      Content affected by modulation
    </div>
  );
}
```

### Manual State Control
```tsx
import { useModulationStore } from './state/modulation';

function Controls() {
  const { setMood, setPulse, setNoiseInjection, resetToDefaults } = useModulationStore();
  
  return (
    <div>
      <button onClick={() => setMood(75)}>Set High Mood</button>
      <button onClick={() => setPulse(90)}>Set High Pulse</button>
      <button onClick={resetToDefaults}>Reset All</button>
    </div>
  );
}
```

## 🎨 Customization

### Modify Default Values
Edit `src/state/modulation.ts`:
```typescript
export const useModulationStore = create<ModulationState>((set) => ({
  mood: 60,           // Change default mood
  pulse: 40,          // Change default pulse  
  noiseInjection: 5,  // Change default noise
  // ...
}));
```

### Custom Slider Colors
Edit `ModulationConsole.tsx`:
```tsx
<ModulationSlider
  id="mood-slider"
  label="Mood"
  value={mood}
  onChange={setMood}
  color="#your-color"  // Custom color
/>
```

### Modify Auto-hide Timer
Change the timeout in `ModulationConsole.tsx`:
```tsx
inactivityTimerRef.current = setTimeout(() => {
  setIsVisible(false);
}, 30000); // 30 seconds instead of 15
```

## 🔧 Integration Examples

### Neural Visualizer Integration
```tsx
function NeuralVisualizer() {
  const { mood, pulse } = useModulationStore();
  
  return (
    <NeuralActivityVisualizer
      animationSpeed={pulse / 100}
      colorScheme={mood > 50 ? 'warm' : 'cool'}
    />
  );
}
```

### Tick Engine Integration
```tsx
function TickEngine() {
  const { pulse } = useModulationStore();
  
  useEffect(() => {
    const interval = 500 * (2 - pulse / 100); // Faster when pulse is higher
    // Update tick timing
  }, [pulse]);
}
```

### Background Effects
```tsx
function Background() {
  const { mood, noiseInjection } = useModulationStore();
  
  return (
    <div 
      className="fixed inset-0 -z-10"
      style={{
        background: `radial-gradient(circle, 
          hsl(${mood * 3.6}, 40%, 10%) 0%, 
          hsl(${mood * 1.8}, 20%, 5%) 100%)`,
        filter: `blur(${noiseInjection * 0.1}px)`,
      }}
    />
  );
}
```

## 🎵 Sound Configuration

### Audio File Requirements
- **Format**: MP3 (primary) + OGG (fallback)
- **Sample Rate**: 44.1kHz
- **Bit Rate**: 128kbps
- **Duration**: 50-100ms for UI sounds
- **Volume**: Normalized to -12dB

### Disable Audio
```tsx
// In ModulationConsole.tsx, comment out sound calls:
// if (sounds.hover.state() === 'loaded') {
//   sounds.hover.play('hover');
// }
```

## 🖥️ Window Manager Integration

For Linux/Electron apps with window manager control:
```tsx
import ModulationConsoleWithWM from './components/controls/modulation-integration';

// This version includes always-on-top and taskbar skip features
<ModulationConsoleWithWM />
```

## ♿ Accessibility

- **ARIA Labels**: All controls have proper accessibility labels
- **Keyboard Navigation**: Full keyboard support
- **Focus Management**: Visible focus indicators
- **Screen Reader Support**: Semantic HTML structure
- **High Contrast**: Works with system high contrast modes

## 🎯 Use Cases

### DAWN Neural System
- **Mood**: Affects emotional tone in visualizations and responses
- **Pulse**: Controls animation speed and update frequency
- **Noise Injection**: Adds randomness to neural patterns

### General Applications
- **Game Development**: Real-time parameter tuning
- **Audio/Visual Tools**: Live effect control
- **Simulation Software**: Dynamic parameter adjustment
- **Debug Interfaces**: Development-time controls

## 🐛 Troubleshooting

### Console Not Appearing
- Check if `isVisible` state is true
- Verify component is rendered in DOM
- Check z-index conflicts (console uses z-50)

### Sound Not Playing
- Verify audio files exist in `public/sounds/`
- Check browser audio permissions
- Confirm file formats (MP3/OGG)
- Check console for Howler.js errors

### Performance Issues
- Reduce update frequency in state reactions
- Use `useCallback` for expensive operations
- Consider debouncing rapid slider changes

### TypeScript Errors
- Ensure all dependencies are installed
- Check `@types/howler` and `@types/node` versions
- Verify tsconfig.json includes necessary lib options

## 📝 License

This component is part of the DAWN Neural System project. Refer to the main project license for usage terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📚 Related Documentation

- [DAWN Neural System](../README.md)
- [Zustand Documentation](https://zustand-demo.pmnd.rs/)
- [Howler.js Documentation](https://howlerjs.com/)
- [React Accessibility Guide](https://reactjs.org/docs/accessibility.html) 