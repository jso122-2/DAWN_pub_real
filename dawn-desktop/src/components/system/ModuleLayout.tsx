import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ModuleContainer } from './ModuleContainer';
import NeuralProcessor from '../modules/NeuralProcessor';
import QuantumCore from '../modules/QuantumCore';
import SystemDiagnostics from '../modules/SystemDiagnostics';
import ModuleWheel from '../modules/CosmicModuleSelector';
import { cn } from '../../lib/utils';
import { EventEmitter } from '../../lib/EventEmitter';

interface ModuleMeta {
  id: string;
  title: string;
  category: 'neural' | 'quantum' | 'process' | 'monitoring' | 'diagnostic';
  component: React.ComponentType<any>;
  defaultPos: { x: number; y: number };
  color?: string;
  glowIntensity?: number;
}

interface ModuleInstance {
  id: string;
  type: string;
  pos: { x: number; y: number };
  connections: string[];
  isActive?: boolean;
  isCritical?: boolean;
}

interface Connection {
  from: string;
  to: string;
  type?: 'neural' | 'quantum' | 'process';
}

const MODULE_COMPONENTS: ModuleMeta[] = [
  {
    id: 'neural-processor',
    title: 'Neural Processor',
    category: 'neural',
    component: NeuralProcessor,
    defaultPos: { x: 100, y: 100 },
    color: '#a78bfa',
    glowIntensity: 0.8
  },
  {
    id: 'quantum-core',
    title: 'Quantum Core',
    category: 'quantum',
    component: QuantumCore,
    defaultPos: { x: 400, y: 120 },
    color: '#60a5fa',
    glowIntensity: 0.9
  },
  {
    id: 'system-diagnostics',
    title: 'System Diagnostics',
    category: 'diagnostic',
    component: SystemDiagnostics,
    defaultPos: { x: 250, y: 320 },
    color: '#f87171',
    glowIntensity: 0.7
  },
];

const STORAGE_KEY = 'dawn-module-layout';

function getInitialLayout(): ModuleInstance[] {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return JSON.parse(saved);
  } catch {}
  return MODULE_COMPONENTS.map((mod, i) => ({
    id: mod.id + '-' + Date.now() + '-' + i,
    type: mod.id,
    pos: mod.defaultPos,
    connections: [],
    isActive: false,
    isCritical: false
  }));
}

export const ModuleLayout: React.FC = () => {
  const [modules, setModules] = useState<ModuleInstance[]>(() => getInitialLayout());
  const [positions, setPositions] = useState<Record<string, { x: number; y: number }>>(() => {
    const layout = getInitialLayout();
    const pos: Record<string, { x: number; y: number }> = {};
    layout.forEach((m: ModuleInstance) => { pos[m.id] = m.pos; });
    return pos;
  });
  const [connections, setConnections] = useState<Connection[]>([]);
  const [menuOpen, setMenuOpen] = useState(false);
  const [showModuleWheel, setShowModuleWheel] = useState(false);
  const [activeModule, setActiveModule] = useState<string | null>(null);
  const emitterRef = useRef<EventEmitter>(new EventEmitter());
  const containerRef = useRef<HTMLDivElement>(null);

  // Persist positions
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(modules.map(m => ({
      ...m,
      pos: positions[m.id] || m.pos,
    }))));
  }, [modules, positions]);

  // Add module with enhanced effects
  const spawnModule = (typeId: string, position?: { x: number; y: number }) => {
    const mod = MODULE_COMPONENTS.find((m) => m.id === typeId);
    if (!mod) return;
    const newId = mod.id + '-' + Date.now() + '-' + Math.floor(Math.random()*10000);
    const newPos = position || { ...mod.defaultPos };
    
    setModules((mods) => [...mods, {
      id: newId,
      type: mod.id,
      pos: newPos,
      connections: [],
      isActive: true,
      isCritical: false
    }]);
    
    setPositions((pos) => ({ ...pos, [newId]: newPos }));
    setActiveModule(newId);
    setMenuOpen(false);
    
    // Emit spawn event
    emitterRef.current.emit('module:spawn', { 
      id: newId, 
      type: mod.id,
      position: newPos,
      category: mod.category
    });
  };

  // Remove module with cleanup
  const removeModule = (id: string) => {
    setModules((mods) => mods.filter((m) => m.id !== id));
    setPositions((pos) => { const p = { ...pos }; delete p[id]; return p; });
    setConnections((conns) => conns.filter((c) => c.from !== id && c.to !== id));
    if (activeModule === id) setActiveModule(null);
    
    // Emit remove event
    emitterRef.current.emit('module:remove', { id });
  };

  // Handle drag/position change with enhanced effects
  const handlePositionChange = (id: string, pos: { x: number; y: number }) => {
    setPositions((prev) => ({ ...prev, [id]: pos }));
    emitterRef.current.emit('module:move', { id, position: pos });
  };

  // Enhanced connection handling
  const [pendingConnect, setPendingConnect] = useState<string | null>(null);
  const handleConnect = (id: string) => {
    if (pendingConnect && pendingConnect !== id) {
      const fromModule = modules.find(m => m.id === pendingConnect);
      const toModule = modules.find(m => m.id === id);
      
      if (fromModule && toModule) {
        const connection: Connection = {
          from: pendingConnect,
          to: id,
          type: fromModule.type.startsWith('neural') ? 'neural' :
                fromModule.type.startsWith('quantum') ? 'quantum' : 'process'
        };
        
        setConnections((conns) => [...conns, connection]);
        emitterRef.current.emit('module:connect', connection);
      }
      setPendingConnect(null);
    } else {
      setPendingConnect(id);
    }
  };

  // Enhanced connection rendering with glass effects
  const renderConnections = () => {
    if (!containerRef.current) return null;
    return (
      <svg className="absolute inset-0 w-full h-full pointer-events-none z-0" style={{overflow: 'visible'}}>
        {connections.map((conn, i) => {
          const from = positions[conn.from];
          const to = positions[conn.to];
          if (!from || !to) return null;
          
          const fromModule = modules.find(m => m.id === conn.from);
          const toModule = modules.find(m => m.id === conn.to);
          const color = fromModule?.type.startsWith('neural') ? '#a78bfa' :
                       fromModule?.type.startsWith('quantum') ? '#60a5fa' :
                       '#34d399';
          
          return (
            <g key={i} className="connection-group">
              <line
                x1={from.x + 180}
                y1={from.y + 40}
                x2={to.x + 40}
                y2={to.y + 40}
                stroke={color}
                strokeWidth={3}
                opacity={0.7}
                markerEnd="url(#arrowhead)"
                className="glass-connection"
              />
              <motion.line
                x1={from.x + 180}
                y1={from.y + 40}
                x2={to.x + 40}
                y2={to.y + 40}
                stroke={color}
                strokeWidth={1}
                opacity={0.3}
                className="glass-connection-glow"
                animate={{
                  opacity: [0.3, 0.6, 0.3],
                  strokeWidth: [1, 2, 1]
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "linear"
                }}
              />
            </g>
          );
        })}
        <defs>
          <marker id="arrowhead" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto" markerUnits="strokeWidth">
            <polygon points="0 0, 8 4, 0 8" fill="currentColor" />
          </marker>
        </defs>
      </svg>
    );
  };

  // Enhanced module rendering with glass effects
  const renderModule = (mod: ModuleInstance) => {
    const meta = MODULE_COMPONENTS.find((m) => m.id === mod.type);
    if (!meta) return null;
    const Comp = meta.component;
    const isActive = activeModule === mod.id;
    
    return (
      <motion.div
        key={mod.id}
        className={cn(
          "absolute z-10",
          "glass-base",
          `glass-${meta.category}`,
          isActive && "glass-active",
          mod.isCritical && "glass-critical"
        )}
        style={{ 
          left: positions[mod.id]?.x ?? 0, 
          top: positions[mod.id]?.y ?? 0,
          backgroundColor: meta.color,
          boxShadow: isActive ? `0 0 20px ${meta.color}` : 'none'
        }}
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.8, opacity: 0 }}
        whileHover={{ scale: 1.02 }}
        drag
        dragMomentum={false}
        onDragEnd={(_, info) => {
          handlePositionChange(mod.id, {
            x: positions[mod.id].x + info.offset.x,
            y: positions[mod.id].y + info.offset.y
          });
        }}
      >
        <Comp
          onEvent={(e: any) => {
            if (e.type === 'neural:spike' && modules.length > 1) {
              const other = modules.find((m) => m.id !== mod.id);
              if (other) {
                const connection: Connection = {
                  from: mod.id,
                  to: other.id,
                  type: 'neural'
                };
                setConnections((conns) => [...conns, connection]);
                emitterRef.current.emit('module:connect', connection);
              }
            }
          }}
          emitter={emitterRef.current}
        />
        <div className="flex gap-2 mt-2 p-2">
          <button
            className={cn(
              "glass px-2 py-1 rounded text-xs text-white/70 hover:bg-white/10",
              pendingConnect === mod.id && "glass-active"
            )}
            onClick={() => handleConnect(mod.id)}
            title={pendingConnect === mod.id ? 'Click another module to connect' : 'Connect'}
          >
            {pendingConnect === mod.id ? 'Select target...' : 'Connect'}
          </button>
          <button
            className="glass px-2 py-1 rounded text-xs text-red-400 hover:bg-red-500/20"
            onClick={() => removeModule(mod.id)}
          >
            Remove
          </button>
        </div>
      </motion.div>
    );
  };

  // Handle module selection from wheel
  const handleModuleSelect = (module: any) => {
    spawnModule(module.id);
  };

  // Handle module spawn from wheel
  const handleModuleSpawn = (module: any, position: { x: number; y: number }) => {
    spawnModule(module.id, position);
  };

  return (
    <div ref={containerRef} className="relative w-full h-full overflow-hidden bg-cosmos">
      {/* Module Wheel Toggle Button */}
      <motion.button
        className={cn(
          "absolute top-4 right-4 z-50 px-4 py-2 rounded-full",
          "glass-base hover:glass-active transition-all",
          showModuleWheel && "glass-active"
        )}
        onClick={() => setShowModuleWheel(!showModuleWheel)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <span className="text-white">🎡</span>
      </motion.button>

      {/* Module Wheel */}
      <AnimatePresence>
        {showModuleWheel && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="absolute top-20 right-4 z-40 w-96 h-96"
          >
            <ModuleWheel
              modules={MODULE_COMPONENTS.map(mod => ({
                id: mod.id,
                name: mod.title,
                category: mod.category,
                description: `Default ${mod.category} module`,
                color: mod.color,
                glowIntensity: mod.glowIntensity
              }))}
              onModuleSelect={handleModuleSelect}
              onModuleSpawn={handleModuleSpawn}
              emitter={emitterRef.current}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Module Layout */}
      {renderConnections()}
      <AnimatePresence>
        {modules.map(renderModule)}
      </AnimatePresence>
    </div>
  );
};

export default ModuleLayout; 