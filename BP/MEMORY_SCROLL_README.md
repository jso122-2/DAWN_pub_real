# LiveMemoryScroll System

A sophisticated real-time memory event streaming component for the DAWN Desktop application. This system provides live visualization of system events, user interactions, and memory state changes with advanced filtering, visual effects, and auto-scroll functionality.

## Features

- **Real-time Event Streaming**: Live display of memory events as they occur
- **Advanced Filtering**: Filter events by type (mood, system, override, error)
- **Auto-scroll with Pause**: Automatically scrolls to new events, pauses on user interaction
- **Severity-based Visual Effects**: Different colors and animations for info, warning, and critical events
- **Emotional Weight Indicators**: Visual representation of event emotional impact
- **Sliding Panel Interface**: Collapsible side panel with smooth animations
- **Event Simulation**: Built-in demo event generator for testing

## File Structure

```
dawn-desktop/src/
├── types/
│   └── memory.ts                    # TypeScript type definitions
├── state/
│   └── memory.ts                    # Zustand store and simulation
└── components/logs/
    ├── LiveMemoryScroll.tsx         # Main component
    └── memory-scroll-integration.tsx # Integration example
```

## Installation

The system uses existing dependencies (React, Zustand) that should already be installed in your DAWN Desktop project.

## Usage

### Basic Integration

```tsx
import React from 'react';
import LiveMemoryScroll from './components/logs/LiveMemoryScroll';

function App() {
  return (
    <div className="App">
      {/* Your app content */}
      <LiveMemoryScroll />
    </div>
  );
}
```

### Manual Event Logging

```tsx
import { useMemoryStore } from './state/memory';

function MyComponent() {
  const { addEvent } = useMemoryStore();

  const handleUserAction = () => {
    addEvent({
      source: 'UserInterface',
      type: 'override',
      severity: 'info',
      message: 'User clicked the neural sync button',
      emotionalWeight: 0.4,
      metadata: { component: 'NeuralSync', action: 'click' }
    });
  };

  return <button onClick={handleUserAction}>Sync Neural State</button>;
}
```

## Event Types

### EventType
- `'mood'`: Emotional state changes and mood-related events
- `'system'`: System operations, memory management, processing updates
- `'override'`: User interventions and manual parameter changes
- `'error'`: Errors, warnings, and critical system issues

### EventSeverity
- `'info'`: Normal operations (blue styling)
- `'warning'`: Attention required (orange styling with pulse effect)
- `'critical'`: Immediate attention needed (red styling with burst animation)

## Visual Features

### Color Coding
- **Info Events**: Blue color scheme with subtle glow
- **Warning Events**: Orange color scheme with pulse animation
- **Critical Events**: Red color scheme with burst ripple effect

### Animations
- **New Event Slide-in**: Events slide up from bottom when added
- **Pulse Effect**: Warning events have a breathing pulse animation
- **Burst Effect**: Critical events have an expanding ripple animation
- **Auto-scroll Pause**: Stream pauses when user hovers over it

### Emotional Weight Indicator
Each event can have an optional `emotionalWeight` value (0-1) that displays as a progress bar, helping visualize the emotional impact of events.

## Component Props

The `LiveMemoryScroll` component currently doesn't accept props but uses global state management through Zustand.

## State Management

### useMemoryStore

```tsx
interface MemoryState {
  events: MemoryEvent[];
  addEvent: (event: Omit<MemoryEvent, 'id' | 'timestamp'>) => void;
  clearEvents: () => void;
  getFilteredEvents: (types: EventType[]) => MemoryEvent[];
}
```

### Auto-Cleanup
The store automatically maintains only the last 1000 events to prevent memory overflow.

## Customization

### Styling
The component uses Tailwind CSS classes. You can customize colors by modifying the `getEventColor` function:

```tsx
const colors = {
  info: {
    bg: 'bg-blue-500/10',      // Background color
    border: 'border-blue-500/30',  // Border color
    text: 'text-blue-400',     // Text color
    glow: 'shadow-blue-500/20', // Glow effect
  },
  // ... other severity levels
};
```

### Event Sources
Customize the simulation sources in `state/memory.ts`:

```tsx
const sources = [
  'CoreProcessor', 
  'EmotionEngine', 
  'SystemMonitor', 
  'UserOverride', 
  'MemoryBank',
  'YourCustomSource'  // Add your own sources
];
```

### Panel Width
Adjust the panel width by modifying the inline style:

```tsx
style={{ width: '400px' }}  // Change to desired width
```

## Keyboard Shortcuts

Currently, the component doesn't implement keyboard shortcuts, but you can add them:

- Consider adding `Ctrl+M` to toggle the panel
- `Ctrl+C` to clear all events
- `Ctrl+F` to focus filter input

## Performance Considerations

- **Event Limit**: Maximum 1000 events stored in memory
- **Auto-scroll Throttling**: Scroll updates are optimized to prevent excessive DOM manipulation
- **Render Optimization**: Uses React.memo and useCallback for performance

## Integration Examples

### With ModulationConsole
```tsx
import LiveMemoryScroll from './components/logs/LiveMemoryScroll';
import ModulationConsole from './components/controls/ModulationConsole';

function NeuralInterface() {
  return (
    <>
      <ModulationConsole />
      <LiveMemoryScroll />
      {/* Your neural interface content */}
    </>
  );
}
```

### With System Monitoring
```tsx
useEffect(() => {
  const monitorSystem = () => {
    addEvent({
      source: 'SystemMonitor',
      type: 'system',
      severity: 'info',
      message: `CPU usage: ${cpuUsage}%`,
      emotionalWeight: cpuUsage > 80 ? 0.8 : 0.2
    });
  };

  const interval = setInterval(monitorSystem, 5000);
  return () => clearInterval(interval);
}, []);
```

## Troubleshooting

### Events Not Appearing
1. Check if `startMemorySimulation()` is called
2. Verify the component is mounted
3. Check browser console for errors

### Performance Issues
1. Clear events periodically: `clearEvents()`
2. Reduce simulation frequency in `state/memory.ts`
3. Limit emotional weight calculations for high-frequency events

### Styling Issues
1. Ensure Tailwind CSS is properly configured
2. Check for CSS conflicts with your existing styles
3. Verify backdrop-blur support in your target browsers

## Future Enhancements

- **Export/Import**: Save and load event logs
- **Search Functionality**: Search through event history
- **Event Grouping**: Collapse similar events
- **Performance Metrics**: Built-in performance monitoring
- **Custom Themes**: Multiple color schemes
- **Sound Notifications**: Audio feedback for critical events

## Dependencies

- React 18+
- Zustand (state management)
- Tailwind CSS (styling)
- TypeScript (type safety)

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

Note: Backdrop blur effects require modern browser support. 