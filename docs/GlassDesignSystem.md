# DAWN Glass Design System Guide

## Philosophy
DAWN's glassmorphism design system aims to evoke a sense of depth, clarity, and neural/quantum energy. It uses layered glass panels, soft glows, and animated effects to create a futuristic, adaptive UI.

---

## Glass Class Hierarchy
- `glass-base`: Default glass panel
- `glass-neural`: Neural-themed glass (purple glow)
- `glass-quantum`: Quantum-themed glass (cyan glow)
- `glass-active`: Active/process state
- `glass-critical`: Alert/diagnostic state

**Example:**
```tsx
<div className="glass-base rounded-2xl p-6">Base Glass</div>
<div className="glass-neural rounded-2xl p-6">Neural Glass</div>
<div className="glass-quantum rounded-2xl p-6">Quantum Glass</div>
```

---

## Applying Glassmorphism
- Use glass classes on module containers, cards, panels, and overlays.
- Combine with Tailwind for spacing, rounding, and layout.
- Use `useGlassEffect` hook for dynamic glass class and style based on state.

**Dynamic Example:**
```tsx
import { useGlassEffect } from '@/hooks/useGlassEffect';
const { className, style } = useGlassEffect({ category: 'neural', intensity: 0.7 });
return <div className={className} style={style}>Neural Module</div>;
```

---

## Customizing Effects
- Adjust intensity via the `intensity` prop or CSS variable.
- Use state (active, critical) to switch glass class.
- Glass panels support animated glows and breathing effects.

---

## Visual Examples

![Glass Example](./assets/glass-example.png)

---

## Accessibility & Performance Tips
- Ensure sufficient contrast for text on glass backgrounds.
- Use `backdrop-blur` and `contain: paint` for performance.
- Avoid excessive blur/glow on low-powered devices.
- Prefer semantic HTML and ARIA roles for interactive glass panels.

---

## See Also
- [Module System Architecture](./ModuleSystem.md)
- [Creating Modules](./CreatingModules.md) 