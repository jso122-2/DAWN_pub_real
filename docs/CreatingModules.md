# Creating DAWN Modules: Step-by-Step

## Prerequisites
- React (18+)
- Zustand (state management)
- Framer Motion (animation)
- Tailwind CSS (utility classes)
- `glass.css` and `tokens.css` imported globally

---

## 1. Scaffold a New Module
You can use either `ModuleTemplate` (slot-based) or `ModuleContainer` (classic) as a base.

**Example with ModuleTemplate:**
```tsx
import { ModuleTemplate } from '@/templates/ModuleTemplate';

export function NeuralPulseModule() {
  return (
    <ModuleTemplate
      title="Neural Pulse"
      headerActions={<button>⚡</button>}
      footer={<span>Status: Active</span>}
      leftPanel={<div>Sidebar</div>}
      rightPanel={<div>Tools</div>}
    >
      <div>Neural pulse content here</div>
    </ModuleTemplate>
  );
}
```

---

## 2. Add Interactivity & Events
- Use a shared EventEmitter or event bus for communication.
- Emit events on user actions or state changes.

**Emit an event:**
```tsx
import { EventEmitter } from 'events';
const emitter = new EventEmitter();
emitter.emit('neural:pulse', { value: 1 });
```

**Listen for events:**
```tsx
useEffect(() => {
  const handler = (data) => { /* ... */ };
  emitter.on('quantum:collapse', handler);
  return () => emitter.off('quantum:collapse', handler);
}, []);
```

---

## 3. Visual Connections
- Use the `ConnectionLayer` or ModuleLayout to visualize links between modules.
- Connections can be animated and color-coded.

---

## 4. Best Practices
- Use `React.memo` for performance on module containers.
- Use `useCallback` for event handlers.
- Throttle drag/resize events if needed.
- Use `useGlassEffect` for dynamic glass styling.

---

## Visual Example

![Neural Pulse Module Example](./assets/neural-pulse-example.png)

---

## See Also
- [Module System Architecture](./ModuleSystem.md)
- [Glass Design System](./GlassDesignSystem.md) 