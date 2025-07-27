# DAWN Frontend Removal & Clean Setup Blueprint

## Step 1: Remove Old Frontend Files

```bash
# Navigate to your DAWN frontend directory
cd /path/to/DAWN_pub_real/frontend

# Remove old components and styles
rm -rf src/components/*
rm -rf src/styles/*
rm -rf src/assets/*
rm -rf src/contexts/*
rm -rf src/hooks/*
rm -rf src/utils/*

# Keep only essential structure
# Keep: src/main.tsx, src/App.tsx, vite.config.ts, package.json
```

## Step 2: Clean Package Dependencies

Update `package.json` to remove unnecessary dependencies:

```json
{
  "name": "dawn-minimal",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "clsx": "^2.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "@vitejs/plugin-react": "^4.0.0",
    "autoprefixer": "^10.4.14",
    "eslint": "^8.45.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.3",
    "postcss": "^8.4.27",
    "tailwindcss": "^3.3.3",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  }
}
```

## Step 3: Minimal App.tsx Setup

```typescript
// src/App.tsx
import React from 'react';
import './App.css';

function App() {
  return (
    <div className="app">
      <h1>DAWN</h1>
      <p>Consciousness Engine Interface</p>
    </div>
  );
}

export default App;
```

## Step 4: Minimal Global Styles

```css
/* src/App.css */
:root {
  --color-black: #000000;
  --color-white: #ffffff;
  --color-gray-900: #0a0a0a;
  --color-gray-800: #1a1a1a;
  --color-gray-700: #2a2a2a;
  --color-gray-600: #3a3a3a;
  --color-gray-500: #4a4a4a;
  --color-gray-400: #6a6a6a;
  --color-gray-300: #8a8a8a;
  --color-gray-200: #aaaaaa;
  --color-gray-100: #cacaca;
  
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
  --font-sans: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-sans);
  background: var(--color-black);
  color: var(--color-gray-100);
  font-size: 14px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

h1 {
  font-size: 2rem;
  font-weight: 300;
  letter-spacing: 0.2em;
  margin-bottom: 0.5rem;
}

p {
  color: var(--color-gray-400);
  font-size: 0.875rem;
}
```

## Step 5: Clean main.tsx

```typescript
// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## Step 6: Minimal index.css

```css
/* src/index.css */
/* Reset and base styles only */
html, body, #root {
  height: 100%;
  margin: 0;
  padding: 0;
}
```

## Step 7: Update Tailwind Config (if using)

```javascript
// tailwind.config.js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        black: '#000000',
        white: '#ffffff',
        gray: {
          900: '#0a0a0a',
          800: '#1a1a1a',
          700: '#2a2a2a',
          600: '#3a3a3a',
          500: '#4a4a4a',
          400: '#6a6a6a',
          300: '#8a8a8a',
          200: '#aaaaaa',
          100: '#cacaca',
        }
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace'],
        'sans': ['-apple-system', 'BlinkMacSystemFont', 'Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
```

## Step 8: Clean Directory Structure

After removal, your structure should be:

```
frontend/
├── src/
│   ├── App.tsx
│   ├── App.css
│   ├── main.tsx
│   └── index.css
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js (optional)
```

## Step 9: Reinstall Dependencies

```bash
# Remove node_modules and lock file
rm -rf node_modules package-lock.json

# Reinstall clean dependencies
npm install
```

## Step 10: Test Clean Setup

```bash
# Start the dev server
npm run dev

# You should see a minimal black screen with "DAWN" text
```

## Notes for Next Steps

1. **WebSocket Setup**: Ready to add minimal WebSocket connection
2. **Module Structure**: Can now build minimal module system from scratch
3. **Command Line Interface**: Terminal-style input component to be added
4. **Existing Logic**: Backend connections remain unchanged
5. **Design System**: Monochromatic palette established

## Verification Checklist

- [ ] All old component files removed
- [ ] All old style files removed
- [ ] Package.json cleaned of unused dependencies
- [ ] Basic app runs with minimal text
- [ ] Black/grey/white color scheme working
- [ ] No console errors
- [ ] Clean git status (commit removal changes)

## Next Blueprint Suggestions

1. Minimal WebSocket Manager
2. Terminal/CLI Component
3. Module Registry System
4. Data Flow Architecture
5. Minimal Module Container