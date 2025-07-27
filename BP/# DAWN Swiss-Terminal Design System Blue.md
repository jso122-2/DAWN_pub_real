# DAWN Swiss-Terminal Design System Blueprint

## Design Philosophy
Merging Bauhaus mathematical precision with terminal brutalism - where Swiss grid meets CRT glow.

## Core Design System

### Color Palette
```css
:root {
  /* Swiss Base */
  --black: #000000;
  --gray-950: #0a0a0a;
  --gray-900: #111111;
  --gray-800: #1a1a1a;
  --gray-700: #222222;
  --gray-600: #2a2a2a;
  --gray-400: #444444;
  --gray-200: #666666;
  --gray-100: #888888;
  --white: #ffffff;
  --off-white: #f0f0f0;
  
  /* Terminal Accents */
  --terminal-green: #00ff41;
  --terminal-green-dim: #00cc33;
  --terminal-amber: #ffb000;
  --terminal-red: #ff0040;
  
  /* Effects */
  --glow-green: 0 0 10px rgba(0, 255, 65, 0.5);
  --scanline: rgba(0, 255, 65, 0.03);
}
```

### Typography System
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
  /* Swiss Typography */
  --font-ui: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  
  /* Type Scale (Major Third) */
  --text-xs: 0.64rem;    /* 10.24px */
  --text-sm: 0.8rem;     /* 12.8px */
  --text-base: 1rem;     /* 16px */
  --text-lg: 1.25rem;    /* 20px */
  --text-xl: 1.563rem;   /* 25px */
  --text-2xl: 1.953rem;  /* 31.25px */
  --text-3xl: 2.441rem;  /* 39px */
  
  /* Swiss Grid Unit */
  --grid-unit: 8px;
}
```

### Grid System
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: var(--grid-unit);
  padding: calc(var(--grid-unit) * 3);
  max-width: 1440px;
  margin: 0 auto;
}

.grid-lines {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  background-image: 
    linear-gradient(var(--gray-900) 1px, transparent 1px),
    linear-gradient(90deg, var(--gray-900) 1px, transparent 1px);
  background-size: var(--grid-unit) var(--grid-unit);
  opacity: 0.1;
  z-index: 1;
}
```

### Terminal Components

#### ASCII Border Component
```css
.terminal-border {
  border: 1px solid var(--gray-700);
  position: relative;
  padding: calc(var(--grid-unit) * 2);
  background: var(--gray-950);
}

.terminal-border::before {
  content: "┌─────────────────────────────────────┐";
  position: absolute;
  top: -1px;
  left: -1px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--gray-400);
  line-height: 1;
}

.terminal-border::after {
  content: "└─────────────────────────────────────┘";
  position: absolute;
  bottom: -7px;
  left: -1px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--gray-400);
  line-height: 1;
}
```

#### CRT Effect Layer
```css
.crt-effect {
  position: relative;
  overflow: hidden;
}

.crt-effect::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    rgba(0, 255, 65, 0.03) 50%,
    rgba(0, 0, 0, 0.03) 50%
  );
  background-size: 100% 2px;
  pointer-events: none;
  animation: scanlines 8s linear infinite;
}

@keyframes scanlines {
  0% { transform: translateY(0); }
  100% { transform: translateY(10px); }
}

.crt-glow {
  text-shadow: var(--glow-green);
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}
```

### Component Examples

#### Terminal Input Component
```typescript
// TerminalInput.tsx
import React, { useState } from 'react';
import './TerminalInput.css';

export const TerminalInput: React.FC = () => {
  const [input, setInput] = useState('');
  
  return (
    <div className="terminal-input">
      <span className="prompt">DAWN://&gt;</span>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="input-field"
        spellCheck={false}
      />
      <span className="cursor">_</span>
    </div>
  );
};
```

```css
/* TerminalInput.css */
.terminal-input {
  display: flex;
  align-items: center;
  background: var(--black);
  border: 1px solid var(--gray-700);
  padding: calc(var(--grid-unit) * 2);
  font-family: var(--font-mono);
  font-size: var(--text-sm);
}

.prompt {
  color: var(--terminal-green);
  margin-right: var(--grid-unit);
  text-shadow: var(--glow-green);
}

.input-field {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--off-white);
  font-family: inherit;
  font-size: inherit;
  outline: none;
}

.cursor {
  color: var(--terminal-green);
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
```

#### Data Module Component
```typescript
// DataModule.tsx
export const DataModule: React.FC<{title: string, value: string}> = ({title, value}) => {
  return (
    <div className="data-module">
      <div className="module-header">
        <span className="ascii-corner">╔═</span>
        <h3>{title}</h3>
        <span className="ascii-corner">═╗</span>
      </div>
      <div className="module-content">
        <div className="data-value crt-glow">{value}</div>
      </div>
      <div className="module-footer">
        <span className="ascii-corner">╚═</span>
        <span className="status">ACTIVE</span>
        <span className="ascii-corner">═╝</span>
      </div>
    </div>
  );
};
```

```css
/* DataModule.css */
.data-module {
  background: var(--gray-950);
  border: 1px solid var(--gray-700);
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: calc(var(--grid-unit) * 20);
  position: relative;
  transition: all 0.2s ease;
}

.data-module:hover {
  border-color: var(--terminal-green-dim);
  transform: translateY(-1px);
}

.module-header,
.module-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--grid-unit);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--gray-400);
}

.module-header h3 {
  font-family: var(--font-ui);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--off-white);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.module-content {
  padding: calc(var(--grid-unit) * 2);
  display: flex;
  align-items: center;
  justify-content: center;
}

.data-value {
  font-family: var(--font-mono);
  font-size: var(--text-2xl);
  color: var(--terminal-green);
}

.ascii-corner {
  color: var(--gray-600);
}

.status {
  font-size: var(--text-xs);
  color: var(--terminal-green-dim);
}
```

### Main Layout Structure
```css
/* App.css */
.app {
  min-height: 100vh;
  background: var(--black);
  color: var(--off-white);
  position: relative;
}

.app::before {
  content: "";
  position: fixed;
  inset: 0;
  background: 
    radial-gradient(
      ellipse at center,
      transparent 0%,
      rgba(0, 0, 0, 0.4) 100%
    );
  pointer-events: none;
  z-index: 2;
}

.main-grid {
  display: grid;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  position: relative;
  z-index: 3;
}

.header {
  border-bottom: 1px solid var(--gray-700);
  padding: calc(var(--grid-unit) * 2) calc(var(--grid-unit) * 3);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-family: var(--font-ui);
  font-size: var(--text-lg);
  font-weight: 300;
  letter-spacing: 0.2em;
  color: var(--off-white);
}

.content {
  padding: calc(var(--grid-unit) * 3);
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: calc(var(--grid-unit) * 3);
}

.footer {
  border-top: 1px solid var(--gray-700);
  padding: calc(var(--grid-unit) * 2) calc(var(--grid-unit) * 3);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--gray-400);
}
```

### Micro-animations
```css
/* Hover Effects */
.interactive {
  transition: all 0.15s ease;
  cursor: pointer;
}

.interactive:hover {
  transform: translateX(1px);
  color: var(--terminal-green);
}

/* Data Updates */
.data-update {
  animation: flash 0.3s ease;
}

@keyframes flash {
  0% { opacity: 1; }
  50% { opacity: 0.5; background: var(--terminal-green-dim); }
  100% { opacity: 1; }
}

/* Loading State */
.loading-dots::after {
  content: "...";
  animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
  0%, 20% { content: ""; }
  40% { content: "."; }
  60% { content: ".."; }
  80%, 100% { content: "..."; }
}
```

## Implementation Notes

1. **Grid Discipline**: Everything aligns to 8px grid
2. **Typography Hierarchy**: UI text in Inter, data/terminal in JetBrains Mono
3. **Color Restraint**: Primarily grayscale, green only for active/data
4. **ASCII Elements**: Use for borders, not overwhelming
5. **CRT Effects**: Subtle, not distracting from data
6. **Animations**: Micro, purposeful, never decorative

## Next Steps
- Implement WebSocket connection indicator with terminal aesthetic
- Create module grid layout system
- Build command palette with ASCII frame
- Add data visualization components (charts in terminal style)