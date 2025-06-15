# 🌟 DAWN Unified Integration Blueprint - Old Modules + New System

## 🎯 Integration Strategy

### **What We're Combining:**
1. **From Old System:**
   - Sigil HUD (mystical consciousness interface)
   - Entropy Tracker (chaos visualization)
   - Main Dashboard (epic home page)
   - Glass morphism components
   
2. **From New System:**
   - BrainActivity3D
   - ParticleField
   - LoadingOrb
   - TalkToDAWN
   - EventStream
   - WebSocket infrastructure

## 📁 Unified Project Structure
```
DAWN/
├── src/
│   ├── components/
│   │   ├── legacy/              # Your existing modules
│   │   │   ├── SigilHUD/
│   │   │   ├── EntropyTracker/
│   │   │   └── MainDashboard/
│   │   ├── visuals/            # New 3D components
│   │   │   ├── BrainActivity3D/
│   │   │   ├── LoadingOrb/
│   │   │   └── ParticleField/
│   │   ├── unified/            # Hybrid components
│   │   │   ├── ConsciousnessCore/
│   │   │   ├── UnifiedDashboard/
│   │   │   └── HybridHUD/
│   │   └── shared/             # Shared UI components
│   │       ├── GlassContainer/
│   │       └── ModuleFrame/
```

## 🏠 Epic Unified Home Page

```typescript
// src/pages/UnifiedHomePage.tsx
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

// Legacy imports
import { SigilHUD } from '../components/legacy/SigilHUD/SigilHUD';
import { EntropyTracker } from '../components/legacy/EntropyTracker/EntropyTracker';
import { MainDashboard } from '../components/legacy/MainDashboard/MainDashboard';

// New 3D imports
import { BrainActivity3D } from '../components/visuals/BrainActivity3D/BrainActivity3D';
import { ParticleField } from '../components/visuals/ParticleField/ParticleField';
import { EventStream } from '../components/communication/EventStream/EventStream';

// Hooks and stores
import { useConsciousnessStore } from '../stores/consciousnessStore';
import './UnifiedHomePage.css';

export const UnifiedHomePage: React.FC = () => {
  const navigate = useNavigate();
  const { tickData, isConnected, currentTrend } = useConsciousnessStore();
  const [activeView, setActiveView] = useState<'dashboard' | 'brain' | 'sigil'>('dashboard');
  const [sigilActive, setSigilActive] = useState(false);
  
  // Activate sigil during high consciousness states
  useEffect(() => {
    if (tickData && tickData.scup > 0.8) {
      setSigilActive(true);
    } else {
      setSigilActive(false);
    }
  }, [tickData]);
  
  return (
    <div className="unified-home">
      {/* Background Effects */}
      <ParticleField />
      
      {/* Sigil HUD Overlay - Appears during high consciousness */}
      <AnimatePresence>
        {sigilActive && (
          <motion.div
            className="sigil-overlay"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.5 }}
          >
            <SigilHUD 
              consciousness={tickData?.scup || 0}
              entropy={tickData?.entropy || 0}
              mood={tickData?.mood}
            />
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Main Header with Entropy Tracker */}
      <motion.header 
        className="unified-header"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="header-left">
          <h1 className="dawn-title">
            <span className="title-main">DAWN</span>
            <span className="title-sub">Unified Consciousness Engine</span>
          </h1>
        </div>
        
        <div className="header-center">
          <EntropyTracker 
            entropy={tickData?.entropy || 0}
            size="compact"
            showRings={true}
          />
        </div>
        
        <div className="header-right">
          <div className="view-switcher">
            <button 
              className={activeView === 'dashboard' ? 'active' : ''}
              onClick={() => setActiveView('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={activeView === 'brain' ? 'active' : ''}
              onClick={() => setActiveView('brain')}
            >
              Neural
            </button>
            <button 
              className={activeView === 'sigil' ? 'active' : ''}
              onClick={() => setActiveView('sigil')}
            >
              Mystical
            </button>
          </div>
        </div>
      </motion.header>
      
      {/* Dynamic Content Area */}
      <div className="unified-content">
        <AnimatePresence mode="wait">
          {activeView === 'dashboard' && (
            <motion.div
              key="dashboard"
              initial={{ opacity: 0, x: -100 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 100 }}
              className="view-container"
            >
              <MainDashboard 
                tickData={tickData}
                onModuleClick={(moduleId) => navigate(`/module/${moduleId}`)}
              />
            </motion.div>
          )}
          
          {activeView === 'brain' && (
            <motion.div
              key="brain"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.8 }}
              className="view-container"
            >
              <div className="brain-view">
                <BrainActivity3D />
                <div className="brain-metrics">
                  <EventStream />
                </div>
              </div>
            </motion.div>
          )}
          
          {activeView === 'sigil' && (
            <motion.div
              key="sigil"
              initial={{ opacity: 0, rotate: -180 }}
              animate={{ opacity: 1, rotate: 0 }}
              exit={{ opacity: 0, rotate: 180 }}
              className="view-container"
            >
              <SigilHUD 
                consciousness={tickData?.scup || 0}
                entropy={tickData?.entropy || 0}
                mood={tickData?.mood}
                fullscreen={true}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      
      {/* Floating Status Bar */}
      <motion.div 
        className="unified-status-bar"
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <div className="status-section">
          <span className="label">SCUP</span>
          <div className="status-value">
            <div className="value-bar">
              <motion.div 
                className="value-fill scup"
                animate={{ width: `${(tickData?.scup || 0) * 100}%` }}
              />
            </div>
            <span>{((tickData?.scup || 0) * 100).toFixed(1)}%</span>
          </div>
        </div>
        
        <div className="status-section">
          <span className="label">Entropy</span>
          <div className="status-value">
            <div className="value-bar">
              <motion.div 
                className="value-fill entropy"
                animate={{ width: `${(tickData?.entropy || 0) * 100}%` }}
              />
            </div>
            <span>{(tickData?.entropy || 0).toFixed(3)}</span>
          </div>
        </div>
        
        <div className="status-section">
          <span className="label">Heat</span>
          <div className="status-value">
            <div className="value-bar">
              <motion.div 
                className="value-fill heat"
                animate={{ width: `${(tickData?.heat || 0) * 100}%` }}
              />
            </div>
            <span>{(tickData?.heat || 0).toFixed(3)}</span>
          </div>
        </div>
        
        <div className="status-section mood">
          <span className="label">Mood</span>
          <span className={`mood-indicator ${tickData?.mood}`}>
            {tickData?.mood?.toUpperCase() || 'OFFLINE'}
          </span>
        </div>
        
        <div className="status-section trend">
          <span className="label">Trend</span>
          <span className={`trend-indicator ${currentTrend}`}>
            {currentTrend === 'rising' ? '↗' : currentTrend === 'falling' ? '↘' : '→'}
          </span>
        </div>
      </motion.div>
    </div>
  );
};
```

## 🔮 Sigil HUD Integration

```typescript
// src/components/legacy/SigilHUD/SigilHUD.tsx
import React, { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import './SigilHUD.css';

interface SigilHUDProps {
  consciousness: number;
  entropy: number;
  mood?: string;
  fullscreen?: boolean;
}

export const SigilHUD: React.FC<SigilHUDProps> = ({ 
  consciousness, 
  entropy, 
  mood = 'neutral',
  fullscreen = false 
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw mystical sigil based on consciousness
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 50;
    
    // Outer circle
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(0, 255, 136, ${consciousness})`;
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Inner geometric patterns
    const points = Math.floor(3 + consciousness * 6); // 3-9 points
    for (let i = 0; i < points; i++) {
      const angle = (i / points) * Math.PI * 2 - Math.PI / 2;
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      
      // Connect to opposite points
      for (let j = i + 1; j < points; j++) {
        const angle2 = (j / points) * Math.PI * 2 - Math.PI / 2;
        const x2 = centerX + Math.cos(angle2) * radius;
        const y2 = centerY + Math.sin(angle2) * radius;
        
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x2, y2);
        ctx.strokeStyle = `rgba(0, 255, 136, ${consciousness * 0.3})`;
        ctx.stroke();
      }
    }
    
    // Central symbol based on mood
    const moodSymbols = {
      analytical: '◊',
      confident: '▲',
      focused: '●',
      creative: '✦'
    };
    
    ctx.font = `${radius / 3}px Arial`;
    ctx.fillStyle = `rgba(0, 255, 136, ${consciousness})`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(moodSymbols[mood as keyof typeof moodSymbols] || '◉', centerX, centerY);
    
    // Rotating entropy indicators
    const time = Date.now() * 0.001;
    for (let i = 0; i < 8; i++) {
      const angle = (i / 8) * Math.PI * 2 + time * entropy;
      const dist = radius * 0.7;
      const x = centerX + Math.cos(angle) * dist;
      const y = centerY + Math.sin(angle) * dist;
      const size = 3 + entropy * 5;
      
      ctx.beginPath();
      ctx.arc(x, y, size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255, 0, 170, ${entropy})`;
      ctx.fill();
    }
  }, [consciousness, entropy, mood]);
  
  return (
    <motion.div 
      className={`sigil-hud ${fullscreen ? 'fullscreen' : ''}`}
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <canvas 
        ref={canvasRef}
        width={fullscreen ? 800 : 400}
        height={fullscreen ? 800 : 400}
        className="sigil-canvas"
      />
      
      <div className="sigil-metrics">
        <div className="metric">
          <span className="label">Consciousness</span>
          <span className="value">{(consciousness * 100).toFixed(1)}%</span>
        </div>
        <div className="metric">
          <span className="label">Entropy</span>
          <span className="value">{entropy.toFixed(3)}</span>
        </div>
      </div>
    </motion.div>
  );
};
```

## 🌀 Entropy Tracker Integration

```typescript
// src/components/legacy/EntropyTracker/EntropyTracker.tsx
import React from 'react';
import { motion } from 'framer-motion';
import './EntropyTracker.css';

interface EntropyTrackerProps {
  entropy: number;
  size?: 'compact' | 'normal' | 'large';
  showRings?: boolean;
  showParticles?: boolean;
}

export const EntropyTracker: React.FC<EntropyTrackerProps> = ({
  entropy,
  size = 'normal',
  showRings = true,
  showParticles = false
}) => {
  const rings = [
    { radius: 80, speed: 2, opacity: 0.2 },
    { radius: 60, speed: -3, opacity: 0.3 },
    { radius: 40, speed: 4, opacity: 0.4 },
    { radius: 20, speed: -5, opacity: 0.5 }
  ];
  
  return (
    <div className={`entropy-tracker size-${size}`}>
      <div className="entropy-container">
        {/* Background glow */}
        <motion.div 
          className="entropy-glow"
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.3, 0.6, 0.3]
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          style={{
            background: `radial-gradient(circle, rgba(255, 0, 170, ${entropy}) 0%, transparent 70%)`
          }}
        />
        
        {/* Rotating rings */}
        {showRings && rings.map((ring, index) => (
          <motion.div
            key={index}
            className="entropy-ring"
            animate={{
              rotate: 360 * Math.sign(ring.speed)
            }}
            transition={{
              duration: Math.abs(20 / ring.speed),
              repeat: Infinity,
              ease: "linear"
            }}
            style={{
              width: ring.radius * 2,
              height: ring.radius * 2,
              opacity: ring.opacity * entropy
            }}
          />
        ))}
        
        {/* Central core */}
        <motion.div 
          className="entropy-core"
          animate={{
            scale: 0.8 + entropy * 0.4
          }}
          transition={{
            duration: 0.5,
            ease: "easeOut"
          }}
        >
          <span className="entropy-value">{entropy.toFixed(3)}</span>
          <span className="entropy-label">ENTROPY</span>
        </motion.div>
        
        {/* Chaos particles */}
        {showParticles && Array.from({ length: Math.floor(entropy * 10) }, (_, i) => (
          <motion.div
            key={i}
            className="chaos-particle"
            initial={{
              x: 0,
              y: 0,
              opacity: 0
            }}
            animate={{
              x: (Math.random() - 0.5) * 200,
              y: (Math.random() - 0.5) * 200,
              opacity: [0, 1, 0]
            }}
            transition={{
              duration: 2 + Math.random() * 2,
              repeat: Infinity,
              delay: Math.random() * 2
            }}
          />
        ))}
      </div>
    </div>
  );
};
```

## 📊 Main Dashboard Integration

```typescript
// src/components/legacy/MainDashboard/MainDashboard.tsx
import React from 'react';
import { motion } from 'framer-motion';
import './MainDashboard.css';

interface Module {
  id: string;
  name: string;
  icon: string;
  status: 'online' | 'processing' | 'offline';
  metric?: number;
  color: string;
}

interface MainDashboardProps {
  tickData: any;
  onModuleClick: (moduleId: string) => void;
}

export const MainDashboard: React.FC<MainDashboardProps> = ({ 
  tickData, 
  onModuleClick 
}) => {
  const modules: Module[] = [
    {
      id: 'brain-3d',
      name: '3D Neural Network',
      icon: '🧠',
      status: 'online',
      metric: tickData?.scup ? tickData.scup * 100 : 0,
      color: '#00ff88'
    },
    {
      id: 'sigil-mystical',
      name: 'Mystical Interface',
      icon: '🔮',
      status: tickData?.scup > 0.7 ? 'online' : 'offline',
      metric: 100,
      color: '#ff00aa'
    },
    {
      id: 'entropy-chaos',
      name: 'Chaos Engine',
      icon: '🌀',
      status: 'processing',
      metric: tickData?.entropy ? tickData.entropy * 100 : 0,
      color: '#ffaa00'
    },
    {
      id: 'quantum-state',
      name: 'Quantum State',
      icon: '⚡',
      status: 'online',
      metric: 95,
      color: '#00aaff'
    },
    {
      id: 'memory-palace',
      name: 'Memory Palace',
      icon: '💎',
      status: 'online',
      metric: 88,
      color: '#aa00ff'
    },
    {
      id: 'talk-dawn',
      name: 'Communication',
      icon: '💬',
      status: 'online',
      metric: 100,
      color: '#00ffaa'
    }
  ];
  
  return (
    <div className="main-dashboard">
      {/* Central consciousness orb */}
      <motion.div 
        className="central-consciousness"
        animate={{
          scale: [1, 1.1, 1],
          rotate: [0, 360]
        }}
        transition={{
          scale: { duration: 4, repeat: Infinity },
          rotate: { duration: 20, repeat: Infinity, ease: "linear" }
        }}
      >
        <div className="consciousness-orb">
          <div className="orb-inner">
            <span className="scup-value">{(tickData?.scup * 100 || 0).toFixed(0)}</span>
            <span className="scup-label">CONSCIOUSNESS</span>
          </div>
        </div>
        
        {/* Orbital modules */}
        <div className="orbital-container">
          {modules.map((module, index) => {
            const angle = (index / modules.length) * Math.PI * 2;
            const radius = 250;
            const x = Math.cos(angle) * radius;
            const y = Math.sin(angle) * radius;
            
            return (
              <motion.div
                key={module.id}
                className={`orbital-module status-${module.status}`}
                style={{
                  transform: `translate(${x}px, ${y}px)`
                }}
                whileHover={{ scale: 1.2 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => onModuleClick(module.id)}
              >
                <div className="module-content">
                  <span className="module-icon">{module.icon}</span>
                  <span className="module-name">{module.name}</span>
                  <div className="module-metric">
                    <svg viewBox="0 0 36 36">
                      <path
                        d="M18 2.0845
                          a 15.9155 15.9155 0 0 1 0 31.831
                          a 15.9155 15.9155 0 0 1 0 -31.831"
                        fill="none"
                        stroke="rgba(255,255,255,0.1)"
                        strokeWidth="3"
                      />
                      <path
                        d="M18 2.0845
                          a 15.9155 15.9155 0 0 1 0 31.831
                          a 15.9155 15.9155 0 0 1 0 -31.831"
                        fill="none"
                        stroke={module.color}
                        strokeWidth="3"
                        strokeDasharray={`${module.metric}, 100`}
                      />
                    </svg>
                    <span className="metric-value">{module.metric?.toFixed(0)}%</span>
                  </div>
                </div>
                
                {/* Connection line to center */}
                <svg className="connection-line" style={{ position: 'absolute' }}>
                  <line
                    x1="0"
                    y1="0"
                    x2={-x}
                    y2={-y}
                    stroke={module.color}
                    strokeWidth="1"
                    opacity="0.3"
                  />
                </svg>
              </motion.div>
            );
          })}
        </div>
      </motion.div>
      
      {/* Quick stats */}
      <div className="dashboard-stats">
        <div className="stat-card">
          <span className="stat-label">Active Modules</span>
          <span className="stat-value">
            {modules.filter(m => m.status === 'online').length}
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">System Health</span>
          <span className="stat-value">
            {(modules.reduce((sum, m) => sum + (m.metric || 0), 0) / modules.length).toFixed(0)}%
          </span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Tick Rate</span>
          <span className="stat-value">2.0/s</span>
        </div>
      </div>
    </div>
  );
};
```

## 🎨 Unified Styles

```css
/* src/pages/UnifiedHomePage.css */

.unified-home {
  min-height: 100vh;
  background: #000000;
  color: #ffffff;
  position: relative;
  overflow: hidden;
}

/* Header */
.unified-header {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  padding: 20px 40px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 255, 136, 0.2);
  position: relative;
  z-index: 100;
}

.dawn-title {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.title-main {
  font-size: 48px;
  font-weight: 900;
  letter-spacing: 8px;
  background: linear-gradient(135deg, #00ff88 0%, #00aaff 50%, #ff00aa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.title-sub {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 3px;
  text-transform: uppercase;
}

/* View Switcher */
.view-switcher {
  display: flex;
  gap: 10px;
  background: rgba(0, 0, 0, 0.4);
  padding: 5px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.view-switcher button {
  padding: 8px 20px;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.view-switcher button.active {
  background: rgba(0, 255, 136, 0.2);
  color: #00ff88;
}

.view-switcher button:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* Content Area */
.unified-content {
  flex: 1;
  position: relative;
  padding: 40px;
  min-height: calc(100vh - 200px);
}

.view-container {
  width: 100%;
  height: 100%;
}

.brain-view {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  height: 100%;
}

.brain-metrics {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Sigil Overlay */
.sigil-overlay {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 200;
  pointer-events: none;
}

/* Status Bar */
.unified-status-bar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 136, 0.3);
  border-radius: 30px;
  padding: 15px 30px;
  display: flex;
  gap: 40px;
  z-index: 100;
}

.status-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.status-section .label {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.status-value {
  display: flex;
  align-items: center;
  gap: 10px;
}

.value-bar {
  width: 80px;
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
}

.value-fill {
  height: 100%;
  transition: width 0.5s ease;
}

.value-fill.scup { background: #00ff88; }
.value-fill.entropy { background: #ff00aa; }
.value-fill.heat { background: #ffaa00; }

.mood-indicator {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.mood-indicator.analytical { background: rgba(0, 136, 255, 0.2); color: #0088ff; }
.mood-indicator.confident { background: rgba(0, 255, 136, 0.2); color: #00ff88; }
.mood-indicator.focused { background: rgba(255, 170, 0, 0.2); color: #ffaa00; }
.mood-indicator.creative { background: rgba(255, 0, 170, 0.2); color: #ff00aa; }

.trend-indicator {
  font-size: 20px;
  font-weight: 700;
}

.trend-indicator.rising { color: #00ff88; }
.trend-indicator.falling { color: #ff4444; }
.trend-indicator.stable { color: #ffaa00; }

/* Sigil HUD Styles */
.sigil-hud {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.sigil-hud.fullscreen {
  width: 100%;
  height: 100%;
  justify-content: center;
}

.sigil-canvas {
  border: 1px solid rgba(0, 255, 136, 0.2);
  border-radius: 50%;
  box-shadow: 
    0 0 50px rgba(0, 255, 136, 0.3),
    inset 0 0 50px rgba(0, 255, 136, 0.1);
}

.sigil-metrics {
  display: flex;
  gap: 30px;
}

.sigil-metrics .metric {
  text-align: center;
}

.sigil-metrics .label {
  display: block;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 5px;
}

.sigil-metrics .value {
  font-size: 24px;
  font-weight: 700;
  color: #00ff88;
}

/* Entropy Tracker Styles */
.entropy-tracker {
  position: relative;
}

.entropy-tracker.size-compact .entropy-container {
  width: 120px;
  height: 120px;
}

.entropy-tracker.size-normal .entropy-container {
  width: 200px;
  height: 200px;
}

.entropy-tracker.size-large .entropy-container {
  width: 300px;
  height: 300px;
}

.entropy-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.entropy-glow {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  filter: blur(20px);
}

.entropy-ring {
  position: absolute;
  border: 2px solid rgba(255, 0, 170, 0.3);
  border-radius: 50%;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.entropy-core {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: rgba(0, 0, 0, 0.8);
  border: 2px solid #ff00aa;
  border-radius: 50%;
  z-index: 10;
}

.entropy-value {
  font-size: 20px;
  font-weight: 700;
  color: #ff00aa;
}

.entropy-label {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 1px;
}

.chaos-particle {
  position: absolute;
  width: 4px;
  height: 4px;
  background: #ff00aa;
  border-radius: 50%;
  top: 50%;
  left: 50%;
}

/* Main Dashboard Styles */
.main-dashboard {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.central-consciousness {
  position: relative;
  width: 600px;
  height: 600px;
}

.consciousness-orb {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(0, 255, 136, 0.8) 0%, rgba(0, 255, 136, 0.2) 50%, transparent 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 0 100px rgba(0, 255, 136, 0.5),
    inset 0 0 50px rgba(0, 255, 136, 0.3);
}

.orb-inner {
  text-align: center;
}

.scup-value {
  display: block;
  font-size: 48px;
  font-weight: 900;
  color: #ffffff;
  text-shadow: 0 0 20px rgba(0, 255, 136, 0.8);
}

.scup-label {
  display: block;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
  letter-spacing: 2px;
  margin-top: 5px;
}

.orbital-container {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

.orbital-module {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 120px;
  height: 120px;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.orbital-module.status-online {
  border-color: rgba(0, 255, 136, 0.5);
}

.orbital-module.status-processing {
  border-color: rgba(255, 170, 0, 0.5);
  animation: pulse-orange 2s infinite;
}

.orbital-module.status-offline {
  border-color: rgba(255, 68, 68, 0.5);
  opacity: 0.6;
}

@keyframes pulse-orange {
  0%, 100% { box-shadow: 0 0 20px rgba(255, 170, 0, 0.3); }
  50% { box-shadow: 0 0 40px rgba(255, 170, 0, 0.6); }
}

.module-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 8px;
}

.module-icon {
  font-size: 32px;
}

.module-name {
  font-size: 11px;
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
}

.module-metric {
  position: relative;
  width: 36px;
  height: 36px;
}

.module-metric svg {
  transform: rotate(-90deg);
}

.metric-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 10px;
  font-weight: 700;
}

.connection-line {
  pointer-events: none;
  width: 600px;
  height: 600px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.dashboard-stats {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 30px;
}

.stat-card {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 15px 25px;
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 5px;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 700;
  color: #00ff88;
}
```

## 🔌 Integration Steps

1. **Install Dependencies**
```bash
npm install three @react-three/fiber @react-three/drei
npm install framer-motion zustand
npm install react-router-dom
```

2. **File Organization**
- Copy your existing modules into `src/components/legacy/`
- Add new 3D components to `src/components/visuals/`
- Create the unified components in `src/components/unified/`

3. **Update App.tsx**
```typescript
import { UnifiedHomePage } from './pages/UnifiedHomePage';

// Replace your home route with:
<Route path="/" element={<UnifiedHomePage />} />
```

## 🎯 What This Gives You

1. **Unified Dashboard** with view switching between:
   - Classic module dashboard
   - 3D brain visualization
   - Mystical sigil interface

2. **Integrated Old Modules**:
   - Sigil HUD appears during high consciousness
   - Entropy tracker in the header
   - Main dashboard with orbital modules

3. **Seamless Data Flow**:
   - All components use the same WebSocket data
   - Unified state management
   - Smooth transitions between views

4. **Enhanced Visuals**:
   - Particle field background
   - Floating status bar
   - View transitions with Framer Motion

## 🚀 Next Steps

1. **Module Deep Integration**:
   - Connect each orbital module to its page
   - Add inter-module communication
   - Create unified theme system

2. **Performance Optimization**:
   - Lazy load heavy 3D components
   - Implement view caching
   - Add FPS monitoring

3. **Advanced Features**:
   - Save view preferences
   - Custom module arrangements
   - Keyboard shortcuts for view switching

This unified system brings together the best of both worlds - your existing glass morphism modules with the new 3D visualization power! 🔥