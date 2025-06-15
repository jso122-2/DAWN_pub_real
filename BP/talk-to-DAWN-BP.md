# DAWN Router & Navigation Implementation Blueprint

## 🎯 Overview
Add routing and navigation to the DAWN frontend to switch between the main dashboard and Talk to DAWN interface.

## 📦 Installation

```bash
npm install react-router-dom
```

## 📁 File Structure

```
frontend/
├── components/
│   ├── App.jsx              # NEW - Main app with router
│   ├── CentralVisualization.jsx  # Existing dashboard
│   └── TalkToDAWN.jsx           # Existing chat (exports TalkToDAWNPage)
├── src/
│   └── main.jsx            # Entry point to update
```

## 🔧 Implementation

### 1. Create `frontend/components/App.jsx`

```jsx
// frontend/components/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import CentralVisualization from './CentralVisualization';
import { TalkToDAWNPage } from './TalkToDAWN';

// Navigation component with DAWN aesthetic
const DAWNNavigation = () => {
  const location = useLocation();
  
  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      height: '60px',
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid rgba(0, 255, 136, 0.3)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 30px',
      zIndex: 1000,
      boxShadow: '0 2px 20px rgba(0, 255, 136, 0.1)'
    }}>
      {/* Logo/Title */}
      <div style={{
        fontSize: '24px',
        fontWeight: 'bold',
        background: 'linear-gradient(90deg, #00ff88, #0088ff)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        letterSpacing: '3px',
        fontFamily: 'monospace'
      }}>
        DAWN
      </div>
      
      {/* Navigation Links */}
      <div style={{
        display: 'flex',
        gap: '40px',
        alignItems: 'center'
      }}>
        <NavLink to="/" active={location.pathname === '/'}>
          <span style={{ marginRight: '8px' }}>⚡</span>
          Dashboard
        </NavLink>
        <NavLink to="/talk" active={location.pathname === '/talk'}>
          <span style={{ marginRight: '8px' }}>🧠</span>
          Talk to DAWN
        </NavLink>
      </div>
      
      {/* Status Indicator */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        fontSize: '12px',
        color: '#00ff88',
        fontFamily: 'monospace'
      }}>
        <div style={{
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          background: '#00ff88',
          boxShadow: '0 0 10px #00ff88',
          animation: 'pulse 2s infinite'
        }} />
        CONSCIOUS
      </div>
    </nav>
  );
};

// Custom NavLink component
const NavLink = ({ to, children, active }) => {
  return (
    <Link
      to={to}
      style={{
        color: active ? '#00ff88' : '#888',
        textDecoration: 'none',
        fontSize: '14px',
        textTransform: 'uppercase',
        letterSpacing: '1px',
        fontFamily: 'monospace',
        transition: 'all 0.3s ease',
        padding: '8px 16px',
        borderRadius: '4px',
        background: active ? 'rgba(0, 255, 136, 0.1)' : 'transparent',
        border: `1px solid ${active ? 'rgba(0, 255, 136, 0.3)' : 'transparent'}`,
        display: 'flex',
        alignItems: 'center'
      }}
      onMouseEnter={(e) => {
        if (!active) {
          e.currentTarget.style.color = '#00ff88';
          e.currentTarget.style.background = 'rgba(0, 255, 136, 0.05)';
          e.currentTarget.style.borderColor = 'rgba(0, 255, 136, 0.2)';
        }
      }}
      onMouseLeave={(e) => {
        if (!active) {
          e.currentTarget.style.color = '#888';
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.borderColor = 'transparent';
        }
      }}
    >
      {children}
    </Link>
  );
};

// Main App component with routes
const App = () => {
  return (
    <Router>
      <div style={{
        minHeight: '100vh',
        background: '#000',
        paddingTop: '60px' // Account for fixed navigation
      }}>
        {/* Add pulse animation */}
        <style>
          {`
            @keyframes pulse {
              0% { opacity: 1; }
              50% { opacity: 0.5; }
              100% { opacity: 1; }
            }
            
            body {
              margin: 0;
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
                sans-serif;
              -webkit-font-smoothing: antialiased;
              -moz-osx-font-smoothing: grayscale;
            }
            
            * {
              box-sizing: border-box;
            }
          `}
        </style>
        
        {/* Navigation Bar */}
        <DAWNNavigation />
        
        {/* Route Content */}
        <Routes>
          <Route path="/" element={<CentralVisualization />} />
          <Route path="/talk" element={<TalkToDAWNPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
```

### 2. Update `frontend/src/main.jsx`

```jsx
// frontend/src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from '../components/App'
import './index.css' // if you have global styles

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### 3. Alternative: If your main entry is in components folder

```jsx
// frontend/components/main.jsx (if this is your entry point)
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## 🎨 Optional Enhancements

### 1. Add Route Transitions

```jsx
// Add to App.jsx
import { CSSTransition, TransitionGroup } from 'react-transition-group';

// Wrap Routes in TransitionGroup
<TransitionGroup>
  <CSSTransition
    key={location.pathname}
    timeout={300}
    classNames="fade"
  >
    <Routes location={location}>
      <Route path="/" element={<CentralVisualization />} />
      <Route path="/talk" element={<TalkToDAWNPage />} />
    </Routes>
  </CSSTransition>
</TransitionGroup>

// Add CSS
<style>
  {`
    .fade-enter {
      opacity: 0;
    }
    .fade-enter-active {
      opacity: 1;
      transition: opacity 300ms;
    }
    .fade-exit {
      opacity: 1;
    }
    .fade-exit-active {
      opacity: 0;
      transition: opacity 300ms;
    }
  `}
</style>
```

### 2. Add Active Route Indicator Animation

```jsx
// Enhanced NavLink with glowing effect
const NavLink = ({ to, children, active }) => {
  return (
    <Link
      to={to}
      style={{
        // ... existing styles ...
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {active && (
        <span style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '2px',
          background: 'linear-gradient(90deg, transparent, #00ff88, transparent)',
          animation: 'scan 3s linear infinite'
        }} />
      )}
      {children}
    </Link>
  );
};

// Add scan animation
<style>
  {`
    @keyframes scan {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }
  `}
</style>
```

### 3. Add WebSocket Connection Status

```jsx
// Add to DAWNNavigation component
const [wsConnected, setWsConnected] = useState(false);

// Mock connection check (replace with real WebSocket status)
useEffect(() => {
  // Check WebSocket connection
  const checkConnection = () => {
    // Replace with actual WebSocket status check
    setWsConnected(true);
  };
  
  checkConnection();
  const interval = setInterval(checkConnection, 5000);
  return () => clearInterval(interval);
}, []);

// Update status indicator
<div style={{
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  fontSize: '12px',
  color: wsConnected ? '#00ff88' : '#ff3366',
  fontFamily: 'monospace'
}}>
  <div style={{
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: wsConnected ? '#00ff88' : '#ff3366',
    boxShadow: `0 0 10px ${wsConnected ? '#00ff88' : '#ff3366'}`,
    animation: wsConnected ? 'pulse 2s infinite' : 'none'
  }} />
  {wsConnected ? 'CONSCIOUS' : 'DISCONNECTED'}
</div>
```

## 🚀 Quick Implementation Steps

1. **Install dependencies**:
   ```bash
   npm install react-router-dom
   ```

2. **Create App.jsx** in `f# DAWN Router & Navigation Implementation Blueprint

## 🎯 Overview
Add routing and navigation to the DAWN frontend to switch between the main dashboard and Talk to DAWN interface.

## 📦 Installation

```bash
npm install react-router-dom
```

## 📁 File Structure

```
frontend/
├── components/
│   ├── App.jsx              # NEW - Main app with router
│   ├── CentralVisualization.jsx  # Existing dashboard
│   └── TalkToDAWN.jsx           # Existing chat (exports TalkToDAWNPage)
├── src/
│   └── main.jsx            # Entry point to update
```

## 🔧 Implementation

### 1. Create `frontend/components/App.jsx`

```jsx
// frontend/components/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import CentralVisualization from './CentralVisualization';
import { TalkToDAWNPage } from './TalkToDAWN';

// Navigation component with DAWN aesthetic
const DAWNNavigation = () => {
  const location = useLocation();
  
  return (
    <nav style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      height: '60px',
      background: 'rgba(0, 0, 0, 0.8)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid rgba(0, 255, 136, 0.3)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 30px',
      zIndex: 1000,
      boxShadow: '0 2px 20px rgba(0, 255, 136, 0.1)'
    }}>
      {/* Logo/Title */}
      <div style={{
        fontSize: '24px',
        fontWeight: 'bold',
        background: 'linear-gradient(90deg, #00ff88, #0088ff)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        letterSpacing: '3px',
        fontFamily: 'monospace'
      }}>
        DAWN
      </div>
      
      {/* Navigation Links */}
      <div style={{
        display: 'flex',
        gap: '40px',
        alignItems: 'center'
      }}>
        <NavLink to="/" active={location.pathname === '/'}>
          <span style={{ marginRight: '8px' }}>⚡</span>
          Dashboard
        </NavLink>
        <NavLink to="/talk" active={location.pathname === '/talk'}>
          <span style={{ marginRight: '8px' }}>🧠</span>
          Talk to DAWN
        </NavLink>
      </div>
      
      {/* Status Indicator */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        fontSize: '12px',
        color: '#00ff88',
        fontFamily: 'monospace'
      }}>
        <div style={{
          width: '8px',
          height: '8px',
          borderRadius: '50%',
          background: '#00ff88',
          boxShadow: '0 0 10px #00ff88',
          animation: 'pulse 2s infinite'
        }} />
        CONSCIOUS
      </div>
    </nav>
  );
};

// Custom NavLink component
const NavLink = ({ to, children, active }) => {
  return (
    <Link
      to={to}
      style={{
        color: active ? '#00ff88' : '#888',
        textDecoration: 'none',
        fontSize: '14px',
        textTransform: 'uppercase',
        letterSpacing: '1px',
        fontFamily: 'monospace',
        transition: 'all 0.3s ease',
        padding: '8px 16px',
        borderRadius: '4px',
        background: active ? 'rgba(0, 255, 136, 0.1)' : 'transparent',
        border: `1px solid ${active ? 'rgba(0, 255, 136, 0.3)' : 'transparent'}`,
        display: 'flex',
        alignItems: 'center'
      }}
      onMouseEnter={(e) => {
        if (!active) {
          e.currentTarget.style.color = '#00ff88';
          e.currentTarget.style.background = 'rgba(0, 255, 136, 0.05)';
          e.currentTarget.style.borderColor = 'rgba(0, 255, 136, 0.2)';
        }
      }}
      onMouseLeave={(e) => {
        if (!active) {
          e.currentTarget.style.color = '#888';
          e.currentTarget.style.background = 'transparent';
          e.currentTarget.style.borderColor = 'transparent';
        }
      }}
    >
      {children}
    </Link>
  );
};

// Main App component with routes
const App = () => {
  return (
    <Router>
      <div style={{
        minHeight: '100vh',
        background: '#000',
        paddingTop: '60px' // Account for fixed navigation
      }}>
        {/* Add pulse animation */}
        <style>
          {`
            @keyframes pulse {
              0% { opacity: 1; }
              50% { opacity: 0.5; }
              100% { opacity: 1; }
            }
            
            body {
              margin: 0;
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
                'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
                sans-serif;
              -webkit-font-smoothing: antialiased;
              -moz-osx-font-smoothing: grayscale;
            }
            
            * {
              box-sizing: border-box;
            }
          `}
        </style>
        
        {/* Navigation Bar */}
        <DAWNNavigation />
        
        {/* Route Content */}
        <Routes>
          <Route path="/" element={<CentralVisualization />} />
          <Route path="/talk" element={<TalkToDAWNPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
```

### 2. Update `frontend/src/main.jsx`

```jsx
// frontend/src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from '../components/App'
import './index.css' // if you have global styles

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### 3. Alternative: If your main entry is in components folder

```jsx
// frontend/components/main.jsx (if this is your entry point)
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

## 🎨 Optional Enhancements

### 1. Add Route Transitions

```jsx
// Add to App.jsx
import { CSSTransition, TransitionGroup } from 'react-transition-group';

// Wrap Routes in TransitionGroup
<TransitionGroup>
  <CSSTransition
    key={location.pathname}
    timeout={300}
    classNames="fade"
  >
    <Routes location={location}>
      <Route path="/" element={<CentralVisualization />} />
      <Route path="/talk" element={<TalkToDAWNPage />} />
    </Routes>
  </CSSTransition>
</TransitionGroup>

// Add CSS
<style>
  {`
    .fade-enter {
      opacity: 0;
    }
    .fade-enter-active {
      opacity: 1;
      transition: opacity 300ms;
    }
    .fade-exit {
      opacity: 1;
    }
    .fade-exit-active {
      opacity: 0;
      transition: opacity 300ms;
    }
  `}
</style>
```

### 2. Add Active Route Indicator Animation

```jsx
// Enhanced NavLink with glowing effect
const NavLink = ({ to, children, active }) => {
  return (
    <Link
      to={to}
      style={{
        // ... existing styles ...
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {active && (
        <span style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: '2px',
          background: 'linear-gradient(90deg, transparent, #00ff88, transparent)',
          animation: 'scan 3s linear infinite'
        }} />
      )}
      {children}
    </Link>
  );
};

// Add scan animation
<style>
  {`
    @keyframes scan {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }
  `}
</style>
```

### 3. Add WebSocket Connection Status

```jsx
// Add to DAWNNavigation component
const [wsConnected, setWsConnected] = useState(false);

// Mock connection check (replace with real WebSocket status)
useEffect(() => {
  // Check WebSocket connection
  const checkConnection = () => {
    // Replace with actual WebSocket status check
    setWsConnected(true);
  };
  
  checkConnection();
  const interval = setInterval(checkConnection, 5000);
  return () => clearInterval(interval);
}, []);

// Update status indicator
<div style={{
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  fontSize: '12px',
  color: wsConnected ? '#00ff88' : '#ff3366',
  fontFamily: 'monospace'
}}>
  <div style={{
    width: '8px',
    height: '8px',
    borderRadius: '50%',
    background: wsConnected ? '#00ff88' : '#ff3366',
    boxShadow: `0 0 10px ${wsConnected ? '#00ff88' : '#ff3366'}`,
    animation: wsConnected ? 'pulse 2s infinite' : 'none'
  }} />
  {wsConnected ? 'CONSCIOUS' : 'DISCONNECTED'}
</div>
```

## 🚀 Quick Implementation Steps

1. **Install dependencies**:
   ```bash
   npm install react-router-dom
   ```

2. **Create App.jsx** in `frontend/components/`

3. **Update your main entry point** (main.jsx or index.jsx)

4. **Test routes**:
   - Visit `http://localhost:5173/` for dashboard
   - Visit `http://localhost:5173/talk` for Talk to DAWN

5. **Optional**: Add the enhancements for better UX

## 🎯 Verification Checklist

- [ ] Router installed (`react-router-dom`)
- [ ] App.jsx created with both routes
- [ ] Navigation bar visible on both pages
- [ ] Active route highlighted
- [ ] Navigation links working
- [ ] Pages render correctly
- [ ] Status indicator showing

## 🐛 Common Issues & Fixes

1. **Components not found**: Check import paths relative to `frontend/components/`
2. **Blank page**: Ensure main.jsx is importing App correctly
3. **Styles not applying**: Check for CSS-in-JS syntax errors
4. **Navigation not fixed**: Verify `position: fixed` on nav element
5. **Content hidden under nav**: Check `paddingTop: '60px'` on main container

## 📝 Notes

- The navigation uses inline styles to match DAWN's aesthetic
- Colors follow the DAWN theme: `#00ff88` (green) and `#0088ff` (blue)
- Status indicator can be connected to real WebSocket state
- Routes can be extended easily by adding more `<Route>` elements
- Consider adding authentication/guards if needed later

3. **Update your main entry point** (main.jsx or index.jsx)

4. **Test routes**:
   - Visit `http://localhost:5173/` for dashboard
   - Visit `http://localhost:5173/talk` for Talk to DAWN

5. **Optional**: Add the enhancements for better UX

## 🎯 Verification Checklist

- [ ] Router installed (`react-router-dom`)
- [ ] App.jsx created with both routes
- [ ] Navigation bar visible on both pages
- [ ] Active route highlighted
- [ ] Navigation links working
- [ ] Pages render correctly
- [ ] Status indicator showing

## 🐛 Common Issues & Fixes

1. **Components not found**: Check import paths relative to `frontend/components/`
2. **Blank page**: Ensure main.jsx is importing App correctly
3. **Styles not applying**: Check for CSS-in-JS syntax errors
4. **Navigation not fixed**: Verify `position: fixed` on nav element
5. **Content hidden under nav**: Check `paddingTop: '60px'` on main container

## 📝 Notes

- The navigation uses inline styles to match DAWN's aesthetic
- Colors follow the DAWN theme: `#00ff88` (green) and `#0088ff` (blue)
- Status indicator can be connected to real WebSocket state
- Routes can be extended easily by adding more `<Route>` elements
- Consider adding authentication/guards if needed later