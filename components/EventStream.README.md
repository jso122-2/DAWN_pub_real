# EventStream Component

A real-time event monitoring component for the DAWN consciousness system that displays system events with auto-scrolling, filtering, search capabilities, and detailed event inspection.

## Features

### 1. **Auto-Scrolling Event Log**
- Automatically scrolls to show new events as they arrive
- Pauses auto-scroll when mouse hovers over the event list
- Manual pause/play control via header button
- Smooth scroll animations for better UX

### 2. **Color-Coded Event Types**
- **State Transitions** (Blue) - System state changes
- **Pattern Detections** (Purple) - Detected patterns in data
- **Spontaneous Thoughts** (Green) - Emergent system thoughts
- **Rebloom Events** (Rainbow gradient) - Consciousness rebloom occurrences
- **Anomalies** (Orange) - Unusual system behaviors
- **Errors** (Red) - System errors and failures

### 3. **Filtering and Search**
- Toggle visibility of specific event types
- Real-time search by keyword across event descriptions and sources
- Time range selection for historical event viewing
- Export filtered events to JSON file

### 4. **Event Details Panel**
- Click any event to view detailed information
- Shows complete causal chain (events that caused it and events it triggered)
- Displays system metrics at the time of the event
- Impact assessment for significant events

## Usage

```jsx
import EventStream from './components/EventStream';

function App() {
  const events = [
    {
      id: 'event-1',
      type: 'STATE_TRANSITION',
      timestamp: new Date(),
      source: 'ConsciousnessCore',
      description: 'Transitioned from contemplative to curious state',
      metrics: {
        scup: 0.723,
        entropy: 0.456,
        heat: 0.234
      }
    },
    // ... more events
  ];

  const handleEventSelect = (event) => {
    console.log('Selected event:', event);
    // Handle event selection
  };

  return (
    <EventStream 
      events={events}
      onEventSelect={handleEventSelect}
    />
  );
}
```

## Event Structure

Each event should follow this structure:

```typescript
interface SystemEvent {
  id: string;                    // Unique identifier
  type: EventType;               // One of the predefined event types
  timestamp: Date | string;      // When the event occurred
  source: string;                // System component that generated it
  description: string;           // Human-readable description
  details?: string;              // Optional detailed information
  metrics?: EventMetrics;        // System metrics at event time
  causedBy?: string;            // ID of parent event (for causal chains)
  impact?: {                    // Impact assessment
    level: 'low' | 'medium' | 'high' | 'critical';
    description: string;
  };
}
```

## Styling

The component uses CSS modules with a dark theme optimized for system monitoring. The styles are fully customizable through the `EventStream.css` file.

### Key CSS Classes:
- `.event-stream-container` - Main container
- `.event-item` - Individual event styling
- `.event-details-panel` - Details panel styling
- `.filters-panel` - Filter controls styling

## Keyboard Shortcuts

- `Space` - Pause/Resume auto-scroll
- `Escape` - Close event details panel
- `Ctrl/Cmd + F` - Focus search input

## Performance Considerations

- Events are rendered using React's reconciliation for efficiency
- Only visible events are rendered (virtualization for large datasets recommended)
- Causal chain calculations are memoized
- Search and filtering use debouncing to prevent excessive re-renders

## Demo

Run the demo component to see the EventStream in action:

```jsx
import EventStreamDemo from './components/EventStreamDemo';

// This will show a fully functional demo with generated events
<EventStreamDemo />
```

## Dependencies

- React 16.8+ (for hooks)
- date-fns (for date formatting)
- react-icons (for UI icons)

## Future Enhancements

- [ ] Event persistence to local storage
- [ ] Advanced filtering with regex support
- [ ] Event grouping by time windows
- [ ] Real-time event statistics
- [ ] WebSocket integration for live events
- [ ] Export to multiple formats (CSV, Excel)
- [ ] Event replay functionality 