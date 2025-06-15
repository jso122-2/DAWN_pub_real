import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, AnimatePresence, useMotionValue, useTransform } from 'framer-motion';
import { 
  Brain, 
  Eye, 
  Activity, 
  Sparkles, 
  Heart, 
  AlertCircle,
  Cpu,
  Waves,
  Zap
} from 'lucide-react';
import { EventEmitter } from '@/lib/EventEmitter';

// Core consciousness data structures
interface ConsciousnessState {
  scup: number; // 0-100
  entropy: number; // 0-1
  mood: 'calm' | 'active' | 'excited' | 'critical';
  tickNumber: number;
  neuralActivity: number; // 0-1
  memoryFragments: MemoryFragment[];
  timestamp: number;
}

interface MemoryFragment {
  id: string;
  content: string;
  age: number;
  importance: number;
  position: { x: number; y: number; z: number };
}

interface NeuralNode {
  id: string;
  x: number;
  y: number;
  active: boolean;
  connections: string[];
}

// Mood color system
const moodColors = {
  calm: {
    primary: '#22d3ee',
    secondary: '#0891b2',
    glow: 'rgba(34, 211, 238, 0.3)'
  },
  active: {
    primary: '#a855f7',
    secondary: '#7c3aed',
    glow: 'rgba(168, 85, 247, 0.3)'
  },
  excited: {
    primary: '#f59e0b',
    secondary: '#d97706',
    glow: 'rgba(245, 158, 11, 0.3)'
  },
  critical: {
    primary: '#ef4444',
    secondary: '#dc2626',
    glow: 'rgba(239, 68, 68, 0.3)'
  }
};

interface ConsciousnessVisualizerProps {
  emitter?: EventEmitter;
  globalEntropy?: number;
}

const ConsciousnessVisualizer: React.FC<ConsciousnessVisualizerProps> = ({ 
  emitter = new EventEmitter(),
  globalEntropy = 0 
}) => {
  const [consciousness, setConsciousness] = useState<ConsciousnessState>({
    scup: 75,
    entropy: 0.3,
    mood: 'active',
    tickNumber: 0,
    neuralActivity: 0.6,
    memoryFragments: [],
    timestamp: Date.now()
  });

  const [neuralNodes, setNeuralNodes] = useState<NeuralNode[]>([]);
  const [historicalStates, setHistoricalStates] = useState<ConsciousnessState[]>([]);
  const [injectionPower, setInjectionPower] = useState(0);
  const [hoveredMetric, setHoveredMetric] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Motion values for smooth animations
  const sphereScale = useMotionValue(1);
  const glowIntensity = useMotionValue(0.5);
  const entropyRotation = useMotionValue(0);

  // Transform sphere scale based on SCUP
  const sphereSize = useTransform(sphereScale, [0, 1], [150, 200]);

  // Initialize neural network
  useEffect(() => {
    const nodes: NeuralNode[] = [];
    const nodeCount = 12;
    const radius = 180;

    for (let i = 0; i < nodeCount; i++) {
      const angle = (i / nodeCount) * Math.PI * 2;
      nodes.push({
        id: `node-${i}`,
        x: Math.cos(angle) * radius,
        y: Math.sin(angle) * radius,
        active: Math.random() > 0.6,
        connections: []
      });
    }

    // Create random connections
    nodes.forEach((node, i) => {
      const connectionCount = Math.floor(Math.random() * 3) + 1;
      for (let j = 0; j < connectionCount; j++) {
        const targetIndex = (i + j + 1) % nodes.length;
        node.connections.push(nodes[targetIndex].id);
      }
    });

    setNeuralNodes(nodes);
  }, []);

  // Generate memory fragments
  useEffect(() => {
    const fragments: MemoryFragment[] = [];
    const fragmentCount = Math.floor(consciousness.scup / 20) + 2;

    for (let i = 0; i < fragmentCount; i++) {
      fragments.push({
        id: `fragment-${i}`,
        content: `Memory ${i + 1}`,
        age: Math.random() * 10000,
        importance: Math.random(),
        position: {
          x: (Math.random() - 0.5) * 300,
          y: (Math.random() - 0.5) * 300,
          z: Math.random() * 100
        }
      });
    }

    setConsciousness(prev => ({ ...prev, memoryFragments: fragments }));
  }, [consciousness.scup]);

  // Listen for tick events
  useEffect(() => {
    const handleTick = (data: any) => {
      const newState: ConsciousnessState = {
        scup: Math.max(0, Math.min(100, data.scup || consciousness.scup + (Math.random() - 0.5) * 5)),
        entropy: Math.max(0, Math.min(1, data.entropy || globalEntropy || consciousness.entropy + (Math.random() - 0.5) * 0.1)),
        mood: data.mood || (consciousness.scup > 80 ? 'excited' : consciousness.scup > 50 ? 'active' : consciousness.scup > 20 ? 'calm' : 'critical'),
        tickNumber: consciousness.tickNumber + 1,
        neuralActivity: Math.max(0, Math.min(1, data.neuralActivity || consciousness.neuralActivity + (Math.random() - 0.5) * 0.2)),
        memoryFragments: consciousness.memoryFragments,
        timestamp: Date.now()
      };

      updateConsciousness(newState);
      setIsConnected(true);
    };

    emitter.on('tick_complete', handleTick);
    emitter.on('consciousness:update', handleTick);

    // Simulate data if no real connection
    const simulationInterval = setInterval(() => {
      if (!isConnected) {
        handleTick({});
      }
    }, 1000);

    return () => {
      emitter.off('tick_complete', handleTick);
      emitter.off('consciousness:update', handleTick);
      clearInterval(simulationInterval);
    };
  }, [emitter, consciousness, globalEntropy, isConnected]);

  const updateConsciousness = (updates: Partial<ConsciousnessState>) => {
    setConsciousness(prev => {
      const newState = { ...prev, ...updates };
      
      // Update historical states
      setHistoricalStates(history => {
        const newHistory = [...history, newState];
        return newHistory.slice(-50); // Keep last 50 states
      });

      // Update motion values
      sphereScale.set(0.8 + (newState.scup / 100) * 0.4);
      glowIntensity.set(0.3 + (newState.scup / 100) * 0.7);

      // Emit events
      emitter.emit('consciousness:update', newState);
      
      // Check for anomalies
      if (newState.entropy > 0.8 || newState.scup < 20) {
        emitter.emit('consciousness:anomaly', {
          type: newState.entropy > 0.8 ? 'high_entropy' : 'low_consciousness',
          value: newState.entropy > 0.8 ? newState.entropy : newState.scup,
          timestamp: newState.timestamp
        });
      }

      return newState;
    });
  };

  // Signal injection effect
  const injectSignal = useCallback(() => {
    setInjectionPower(1);
    
    updateConsciousness({
      scup: Math.min(100, consciousness.scup + 10),
      neuralActivity: Math.min(1, consciousness.neuralActivity + 0.2),
      entropy: Math.max(0, consciousness.entropy - 0.1)
    });

    emitter.emit('consciousness:injection', {
      boost: 10,
      timestamp: Date.now()
    });

    setTimeout(() => setInjectionPower(0), 500);
  }, [consciousness, emitter]);

  // Drag handler for entropy influence
  const handleDrag = useCallback((event: any, info: any) => {
    const dragDistance = Math.sqrt(info.offset.x ** 2 + info.offset.y ** 2);
    const entropyChange = Math.min(0.3, dragDistance / 200);
    
    updateConsciousness({
      entropy: Math.min(1, consciousness.entropy + entropyChange)
    });
  }, [consciousness]);

  // Neural network canvas drawing
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;

      // Draw connections as lightning bolts
      neuralNodes.forEach(node => {
        if (!node.active) return;

        node.connections.forEach(connectionId => {
          const targetNode = neuralNodes.find(n => n.id === connectionId);
          if (!targetNode || !targetNode.active) return;

          ctx.beginPath();
          ctx.strokeStyle = moodColors[consciousness.mood].primary;
          ctx.lineWidth = 2 + consciousness.neuralActivity * 3;
          ctx.shadowColor = moodColors[consciousness.mood].glow;
          ctx.shadowBlur = 10;

          // Create lightning effect
          const startX = centerX + node.x;
          const startY = centerY + node.y;
          const endX = centerX + targetNode.x;
          const endY = centerY + targetNode.y;

          ctx.moveTo(startX, startY);
          
          // Add random jitter for lightning effect
          const midX = (startX + endX) / 2 + (Math.random() - 0.5) * 20;
          const midY = (startY + endY) / 2 + (Math.random() - 0.5) * 20;
          
          ctx.quadraticCurveTo(midX, midY, endX, endY);
          ctx.stroke();
        });
      });

      // Draw neural nodes
      neuralNodes.forEach(node => {
        ctx.beginPath();
        ctx.arc(centerX + node.x, centerY + node.y, node.active ? 6 : 3, 0, Math.PI * 2);
        ctx.fillStyle = node.active ? moodColors[consciousness.mood].primary : 'rgba(255,255,255,0.3)';
        ctx.shadowColor = node.active ? moodColors[consciousness.mood].glow : 'none';
        ctx.shadowBlur = node.active ? 15 : 0;
        ctx.fill();
      });
    };

    const animationFrame = requestAnimationFrame(function animate() {
      draw();
      requestAnimationFrame(animate);
    });

    return () => cancelAnimationFrame(animationFrame);
  }, [neuralNodes, consciousness.mood, consciousness.neuralActivity]);

  // Render entropy particles
  const renderEntropyParticles = () => {
    const particleCount = Math.floor(consciousness.entropy * 20);
    
    return [...Array(particleCount)].map((_, i) => (
      <motion.div
        key={`particle-${i}`}
        className="absolute w-1 h-1 rounded-full"
        style={{
          background: moodColors[consciousness.mood].primary
        }}
        animate={{
          x: Math.cos(i * 0.5 + entropyRotation.get()) * (50 + Math.random() * 100),
          y: Math.sin(i * 0.5 + entropyRotation.get()) * (50 + Math.random() * 100),
          scale: [0, 1, 0],
          opacity: [0, 0.8, 0]
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          delay: i * 0.05,
          ease: 'linear'
        }}
      />
    ));
  };
  
  // Animate entropy rotation
  useEffect(() => {
    const interval = setInterval(() => {
      entropyRotation.set(entropyRotation.get() + consciousness.entropy * 0.1);
    }, 50);
    
    return () => clearInterval(interval);
  }, [consciousness.entropy, entropyRotation]);
  
  return (
    <div 
      ref={containerRef}
      className="w-full h-full flex flex-col p-4 relative overflow-hidden cursor-pointer"
      onClick={injectSignal}
      onDoubleClick={() => emitter.emit('consciousness:event', { type: 'manual_trigger' })}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4 z-10">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-purple-400" />
          <h3 className="text-white font-semibold">Consciousness Visualizer</h3>
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`} />
        </div>
        <div className="text-xs text-white/50">
          Tick #{consciousness.tickNumber}
        </div>
      </div>
      
      {/* Main Visualization Area */}
      <div className="flex-1 relative flex items-center justify-center">
        {/* Neural Network Canvas */}
        <canvas
          ref={canvasRef}
          width={400}
          height={400}
          className="absolute inset-0 w-full h-full"
          style={{ opacity: 0.6 }}
        />
        
        {/* Historical State Trails */}
        <div className="absolute inset-0 pointer-events-none">
          {historicalStates.slice(-10).map((state, i) => (
            <motion.div
              key={`trail-${i}`}
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full"
              style={{
                width: 50 + (state.scup / 100) * 150,
                height: 50 + (state.scup / 100) * 150,
                border: `1px solid ${moodColors[state.mood].primary}`,
                opacity: (i / 10) * 0.3
              }}
              initial={{ scale: 0.8 }}
              animate={{ scale: 1.2 }}
              transition={{ duration: 2 }}
            />
          ))}
        </div>
        
        {/* Central Consciousness Sphere */}
        <motion.div
          className="relative"
          style={{ scale: sphereScale }}
          drag
          dragElastic={0.1}
          onDrag={handleDrag}
          whileHover={{ scale: 1.05 }}
        >
          {/* Outer Glow */}
          <motion.div
            className="absolute -inset-20 rounded-full"
            style={{
              background: `radial-gradient(circle, ${moodColors[consciousness.mood].glow} 0%, transparent 70%)`,
              filter: 'blur(20px)',
              opacity: glowIntensity
            }}
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.3, 0.6, 0.3]
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              ease: 'easeInOut'
            }}
          />
          
          {/* Main Sphere */}
          <motion.div
            className="relative w-48 h-48 rounded-full overflow-hidden"
            style={{
              background: `radial-gradient(circle at 30% 30%, ${moodColors[consciousness.mood].primary}, ${moodColors[consciousness.mood].secondary})`,
              boxShadow: `
                inset 0 0 30px rgba(0,0,0,0.3),
                0 0 60px ${moodColors[consciousness.mood].glow},
                0 0 120px ${moodColors[consciousness.mood].glow}
              `
            }}
            animate={{
              rotateY: consciousness.tickNumber * 2,
              rotateZ: consciousness.entropy * 360
            }}
            transition={{
              rotateY: { duration: 20, ease: 'linear' },
              rotateZ: { duration: 5, ease: 'linear' }
            }}
          >
            {/* Inner Core */}
            <div className="absolute inset-4 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
              <div className="text-center">
                <div className="text-3xl font-bold text-white">
                  {consciousness.scup.toFixed(0)}%
                </div>
                <div className="text-xs text-white/70">SCUP</div>
              </div>
            </div>
            
            {/* Consciousness Flickering */}
            {consciousness.entropy > 0.7 && (
              <motion.div
                className="absolute inset-0 bg-white/10"
                animate={{
                  opacity: [0, 0.5, 0]
                }}
                transition={{
                  duration: 0.1,
                  repeat: Infinity,
                  repeatDelay: Math.random() * 0.5
                }}
              />
            )}
          </motion.div>
          
          {/* Rotating Tick Rings */}
          <motion.div
            className="absolute -inset-8 rounded-full border-2 border-dashed"
            style={{ borderColor: moodColors[consciousness.mood].primary }}
            animate={{ rotate: 360 }}
            transition={{ duration: 10, repeat: Infinity, ease: 'linear' }}
          />
          
          <motion.div
            className="absolute -inset-16 rounded-full border"
            style={{ borderColor: moodColors[consciousness.mood].secondary }}
            animate={{ rotate: -360 }}
            transition={{ duration: 15, repeat: Infinity, ease: 'linear' }}
          />
        </motion.div>
        
        {/* Entropy Particles */}
        <div className="absolute inset-0 pointer-events-none">
          {renderEntropyParticles()}
        </div>
        
        {/* Memory Fragments */}
        {consciousness.memoryFragments.map((fragment, i) => (
          <motion.div
            key={fragment.id}
            className="absolute glass-panel glass-depth-1 rounded px-2 py-1 text-xs text-white/70"
            style={{
              left: '50%',
              top: '50%',
              x: fragment.position.x,
              y: fragment.position.y
            }}
            animate={{
              x: [fragment.position.x, fragment.position.x + 20, fragment.position.x],
              y: [fragment.position.y, fragment.position.y - 10, fragment.position.y],
              opacity: [0.3, 0.8, 0.3]
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              delay: i * 0.5
            }}
            onHoverStart={() => setHoveredMetric(`memory-${i}`)}
            onHoverEnd={() => setHoveredMetric(null)}
          >
            <Cpu className="w-3 h-3 inline mr-1" />
            {fragment.content}
          </motion.div>
        ))}
        
        {/* Signal Injection Effect */}
        <AnimatePresence>
          {injectionPower > 0 && (
            <motion.div
              className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 rounded-full border-2"
              style={{ borderColor: moodColors[consciousness.mood].primary }}
              initial={{ scale: 0, opacity: 1 }}
              animate={{ scale: 3, opacity: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
            />
          )}
        </AnimatePresence>
      </div>
      
      {/* Metrics Panel */}
      <div className="grid grid-cols-4 gap-2 mt-4">
        <motion.div
          className="glass-panel glass-depth-1 rounded-lg p-2 text-center cursor-pointer"
          whileHover={{ scale: 1.05 }}
          onHoverStart={() => setHoveredMetric('scup')}
          onHoverEnd={() => setHoveredMetric(null)}
        >
          <Eye className="w-4 h-4 text-purple-400 mx-auto mb-1" />
          <div className="text-xs text-white/60">Consciousness</div>
          <div className="text-sm font-bold text-purple-400">{consciousness.scup.toFixed(0)}%</div>
        </motion.div>
        
        <motion.div
          className="glass-panel glass-depth-1 rounded-lg p-2 text-center cursor-pointer"
          whileHover={{ scale: 1.05 }}
          onHoverStart={() => setHoveredMetric('entropy')}
          onHoverEnd={() => setHoveredMetric(null)}
        >
          <Sparkles className="w-4 h-4 text-cyan-400 mx-auto mb-1" />
          <div className="text-xs text-white/60">Entropy</div>
          <div className="text-sm font-bold text-cyan-400">{(consciousness.entropy * 100).toFixed(0)}%</div>
        </motion.div>
        
        <motion.div
          className="glass-panel glass-depth-1 rounded-lg p-2 text-center cursor-pointer"
          whileHover={{ scale: 1.05 }}
          onHoverStart={() => setHoveredMetric('neural')}
          onHoverEnd={() => setHoveredMetric(null)}
        >
          <Activity className="w-4 h-4 text-green-400 mx-auto mb-1" />
          <div className="text-xs text-white/60">Neural Activity</div>
          <div className="text-sm font-bold text-green-400">{(consciousness.neuralActivity * 100).toFixed(0)}%</div>
        </motion.div>
        
        <motion.div
          className="glass-panel glass-depth-1 rounded-lg p-2 text-center cursor-pointer"
          whileHover={{ scale: 1.05 }}
          onHoverStart={() => setHoveredMetric('mood')}
          onHoverEnd={() => setHoveredMetric(null)}
        >
          <Heart className="w-4 h-4 mx-auto mb-1" style={{ color: moodColors[consciousness.mood].primary }} />
          <div className="text-xs text-white/60">Mood</div>
          <div className="text-sm font-bold capitalize" style={{ color: moodColors[consciousness.mood].primary }}>
            {consciousness.mood}
          </div>
        </motion.div>
      </div>
      
      {/* Detailed Metrics Tooltip */}
      <AnimatePresence>
        {hoveredMetric && (
          <motion.div
            className="absolute bottom-20 left-1/2 -translate-x-1/2 glass-panel glass-depth-2 rounded-lg p-3 min-w-[200px]"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 10 }}
          >
            <div className="text-xs text-white/60 mb-1">Detailed Analysis</div>
            {hoveredMetric === 'scup' && (
              <div className="text-sm text-white">
                System consciousness is {consciousness.scup < 30 ? 'low' : consciousness.scup < 70 ? 'moderate' : 'high'}.
                Current processing capacity at {consciousness.scup}%.
              </div>
            )}
            {hoveredMetric === 'entropy' && (
              <div className="text-sm text-white">
                Chaos level: {(consciousness.entropy * 100).toFixed(0)}%
                {consciousness.entropy > 0.7 && <AlertCircle className="w-4 h-4 text-yellow-400 inline ml-2" />}
              </div>
            )}
            {hoveredMetric === 'neural' && (
              <div className="text-sm text-white">
                Neural pathways firing at {(consciousness.neuralActivity * 100).toFixed(0)}% capacity.
                {neuralNodes.filter(n => n.active).length} of {neuralNodes.length} nodes active.
              </div>
            )}
            {hoveredMetric === 'mood' && (
              <div className="text-sm text-white">
                Emotional state: {consciousness.mood}
                {consciousness.mood === 'critical' && ' - Immediate attention required'}
              </div>
            )}
            {hoveredMetric.startsWith('memory') && (
              <div className="text-sm text-white">
                Memory fragment age: {consciousness.memoryFragments[parseInt(hoveredMetric.split('-')[1])]?.age.toFixed(0)}ms
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* Instructions */}
      <div className="absolute top-16 right-4 text-xs text-white/30 space-y-1">
        <div>Click: Inject signal</div>
        <div>Drag sphere: Influence entropy</div>
        <div>Double-click: Trigger event</div>
      </div>
    </div>
  );
};

export default ConsciousnessVisualizer; 