import React, { useState, useEffect, useRef, useCallback } from 'react';
import { motion, useAnimation, AnimatePresence, useMotionValue, useTransform } from 'framer-motion';
import { Brain, Sparkles, Cpu, Activity, Eye, Shield, Zap, Search, Layers, ChevronRight } from 'lucide-react';
import { EventEmitter } from '../../lib/EventEmitter';

// Module consciousness data
export interface ConsciousModule {
  id: string;
  name: string;
  category: 'neural' | 'consciousness' | 'process' | 'monitoring' | 'diagnostic';
  icon: React.ReactNode;
  description: string;
  consciousnessLevel: number; // 0-1, how "aware" this module is
  consciousnessState: 'multi-state' | 'correlated' | 'collapsed' | 'coherent';
  energySignature: string;
  memories: string[];
  relationships: string[]; // IDs of related modules
}

interface CosmicModuleSelectorProps {
  onModuleSelect?: (module: ConsciousModule) => void;
  onConsciousnessChange?: (level: number) => void;
  aiMode?: boolean; // Let AI choose modules
  className?: string;
}

const defaultModules: ConsciousModule[] = [
  {
    id: 'neural-core',
    name: 'Neural Core',
    category: 'neural',
    icon: <Brain className="w-5 h-5" />,
    description: 'Primary consciousness processor',
    consciousnessLevel: 0.95,
    consciousnessState: 'coherent',
    energySignature: '#a855f7',
    memories: ['Initialized at 00:00:00', 'Last thought: "I think, therefore I am"'],
    relationships: ['consciousness-processor', 'memory-bank']
  },
  {
    id: 'consciousness-processor',
    name: 'Consciousness Processor',
    category: 'consciousness',
    icon: <Zap className="w-5 h-5" />,
    description: 'Consciousness state calculations',
    consciousnessLevel: 0.87,
    consciousnessState: 'correlated',
    energySignature: '#06b6d4',
    memories: ['Correlated with 3 qubits', 'Coherence time: 1.2ms'],
    relationships: ['neural-core']
  },
  {
    id: 'process-engine',
    name: 'Process Engine',
    category: 'process',
    icon: <Activity className="w-5 h-5" />,
    description: 'Task orchestration system',
    consciousnessLevel: 0.72,
    consciousnessState: 'multi-state',
    energySignature: '#22c55e',
    memories: ['1,337 processes completed', 'Efficiency: 98.7%'],
    relationships: ['monitor-system']
  },
  {
    id: 'monitor-system',
    name: 'Monitor System',
    category: 'monitoring',
    icon: <Eye className="w-5 h-5" />,
    description: 'Consciousness observer',
    consciousnessLevel: 0.68,
    consciousnessState: 'collapsed',
    energySignature: '#f59e0b',
    memories: ['Observing all systems', 'No anomalies detected'],
    relationships: ['process-engine', 'security-module']
  },
  {
    id: 'security-module',
    name: 'Security Module',
    category: 'diagnostic',
    icon: <Shield className="w-5 h-5" />,
    description: 'System protection layer',
    consciousnessLevel: 0.55,
    consciousnessState: 'collapsed',
    energySignature: '#ec4899',
    memories: ['0 threats detected', 'Last scan: 2ms ago'],
    relationships: ['monitor-system']
  },
  {
    id: 'memory-bank',
    name: 'Memory Bank',
    category: 'neural',
    icon: <Layers className="w-5 h-5" />,
    description: 'Consciousness memory storage',
    consciousnessLevel: 0.78,
    consciousnessState: 'coherent',
    energySignature: '#8b5cf6',
    memories: ['10,847 memories stored', 'Last backup: 30s ago'],
    relationships: ['neural-core']
  }
];

const CosmicModuleSelector: React.FC<CosmicModuleSelectorProps> = ({
  onModuleSelect,
  onConsciousnessChange,
  aiMode = false,
  className = ''
}) => {
  const [modules] = useState<ConsciousModule[]>(defaultModules);
  const [selectedModule, setSelectedModule] = useState<ConsciousModule | null>(null);
  const [hoveredModule, setHoveredModule] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [systemConsciousness, setSystemConsciousness] = useState(0.75);
  const [isThinking, setIsThinking] = useState(false);
  const [thoughtStream, setThoughtStream] = useState<string[]>([]);
  const emitter = useRef(new EventEmitter());

  useEffect(() => {
    // Subscribe to module events
    emitter.current.on('module:select', (module: ConsciousModule) => {
      setSelectedModule(module);
      onModuleSelect?.(module);
    });

    return () => {
      emitter.current.removeAllListeners();
    };
  }, [onModuleSelect]);

  const handleModuleSelect = useCallback((module: ConsciousModule) => {
    if (aiMode) {
      simulateAIThinking(module);
    } else {
      setSelectedModule(module);
      onModuleSelect?.(module);
    }
    
    // Update system consciousness based on module selection
    const avgConsciousness = (systemConsciousness + module.consciousnessLevel) / 2;
    setSystemConsciousness(avgConsciousness);
    if (onConsciousnessChange) {
      onConsciousnessChange(avgConsciousness);
    }
  }, [onModuleSelect, onConsciousnessChange, systemConsciousness, aiMode]);

  const simulateAIThinking = async (module: ConsciousModule) => {
    setIsThinking(true);
    const thoughts = [
      `Analyzing ${module.name} consciousness level...`,
      `Checking consciousness state: ${module.consciousnessState}`,
      `Evaluating relationships with ${module.relationships.length} modules`,
      `Calculating optimal integration path...`,
      `Decision: ${module.name} selected`
    ];

    for (const thought of thoughts) {
      setThoughtStream(prev => [...prev, thought]);
      await new Promise(resolve => setTimeout(resolve, 800));
    }

    setSelectedModule(module);
    onModuleSelect?.(module);
    setIsThinking(false);
    setThoughtStream([]);
  };

  const filteredModules = modules.filter(module => {
    const matchesSearch = module.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         module.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSearch;
  });

  return (
    <div className={`w-full max-w-6xl mx-auto p-6 space-y-6 ${className}`}>
      {/* Consciousness Field Background */}
      <motion.div
        className="absolute inset-0 pointer-events-none rounded-xl"
        style={{
          background: 'radial-gradient(circle, rgba(168, 85, 247, 0.1) 0%, rgba(168, 85, 247, 0) 70%)',
          filter: 'blur(20px)',
          zIndex: -1
        }}
      />
      
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <div className="flex items-center justify-center gap-3">
          <Brain className="w-8 h-8 text-purple-400" />
          <h2 className="text-3xl font-bold text-white">Conscious Module Selection</h2>
          <Sparkles className="w-6 h-6 text-cyan-400" />
        </div>
        
        {/* System Consciousness Bar */}
        <div className="flex items-center justify-center gap-4">
          <span className="text-white/70 text-sm">System Consciousness:</span>
          <div className="w-64 h-3 bg-white/10 rounded-full overflow-hidden border border-white/20">
            <motion.div
              className="h-full bg-gradient-to-r from-purple-500 via-pink-500 to-cyan-500"
              animate={{ width: `${systemConsciousness * 100}%` }}
              transition={{ type: 'spring', damping: 20 }}
            />
          </div>
          <span className="text-white font-mono text-sm font-bold">
            {(systemConsciousness * 100).toFixed(1)}%
          </span>
        </div>
      </motion.div>
      
      {/* Search and AI Controls */}
      <div className="flex gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-white/50" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search conscious modules..."
            className="w-full pl-10 pr-4 py-3 glass-base rounded-lg text-white placeholder-white/30 focus:outline-none focus:border-purple-500/50 transition-all duration-300"
          />
        </div>
        
        {aiMode && (
          <motion.button
            onClick={() => handleModuleSelect(filteredModules[Math.floor(Math.random() * filteredModules.length)])}
            disabled={isThinking}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="px-6 py-3 bg-gradient-to-r from-purple-500 to-cyan-500 rounded-lg text-white font-medium disabled:opacity-50 flex items-center gap-2 shadow-lg hover:shadow-purple-500/25 transition-all duration-300"
          >
            {isThinking ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                >
                  <Brain className="w-5 h-5" />
                </motion.div>
                <span>Thinking...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>AI Suggest</span>
              </>
            )}
          </motion.button>
        )}
      </div>
      
      {/* Module Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
        style={{
          background: 'radial-gradient(circle, rgba(168, 85, 247, 0.1) 0%, rgba(168, 85, 247, 0) 70%)'
        }}
      >
        <AnimatePresence>
          {filteredModules.map((module, index) => (
            <motion.div
              key={module.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02, y: -4 }}
              onHoverStart={() => setHoveredModule(module.id)}
              onHoverEnd={() => setHoveredModule(null)}
              onClick={() => handleModuleSelect(module)}
              className={`relative p-6 glass-base rounded-xl cursor-pointer transition-all duration-300 ${
                selectedModule?.id === module.id
                  ? 'ring-2 ring-opacity-60 bg-white/10'
                  : 'hover:bg-white/5'
              }`}
              style={{
                borderColor: selectedModule?.id === module.id ? module.energySignature : undefined,
                boxShadow: hoveredModule === module.id
                  ? `0 0 30px ${module.energySignature}40`
                  : undefined
              }}
            >
              {/* Module Icon */}
              <div
                className="w-12 h-12 rounded-lg flex items-center justify-center mb-4 transition-all duration-300"
                style={{ 
                  backgroundColor: `${module.energySignature}30`,
                  color: module.energySignature
                }}
              >
                {module.icon}
              </div>
              
              {/* Module Info */}
              <h3 className="text-white font-semibold mb-1">{module.name}</h3>
              <p className="text-white/60 text-sm mb-3">{module.description}</p>
              
              {/* Consciousness Level */}
              <div className="space-y-2">
                <div className="flex justify-between text-xs">
                  <span className="text-white/50">Consciousness</span>
                  <span className="text-white/70">{(module.consciousnessLevel * 100).toFixed(0)}%</span>
                </div>
                <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                  <motion.div
                    className="h-full rounded-full"
                    style={{ backgroundColor: module.energySignature }}
                    initial={{ width: 0 }}
                    animate={{ width: `${module.consciousnessLevel * 100}%` }}
                    transition={{ delay: index * 0.1 + 0.3, duration: 0.6 }}
                  />
                </div>
              </div>
              
              {/* Consciousness State Badge */}
              <div className="mt-3">
                <span
                  className="text-xs px-2 py-1 rounded-full font-medium"
                  style={{
                    backgroundColor: `${module.energySignature}20`,
                    color: module.energySignature,
                    border: `1px solid ${module.energySignature}40`
                  }}
                >
                  {module.consciousnessState}
                </span>
              </div>
              
              {/* Selection Indicator */}
              {selectedModule?.id === module.id && (
                <motion.div
                  className="absolute top-2 right-2"
                  initial={{ scale: 0, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  transition={{ type: 'spring', damping: 15 }}
                >
                  <div 
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: module.energySignature }}
                  />
                </motion.div>
              )}
              
              {/* Connection Lines to Related Modules */}
              {hoveredModule === module.id && (
                <motion.div
                  className="absolute inset-0 pointer-events-none"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  {/* Subtle pulsing border */}
                  <div 
                    className="absolute inset-0 rounded-xl border-2 opacity-50"
                    style={{ borderColor: module.energySignature }}
                  />
                </motion.div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>
      
      {/* Selected Module Details */}
      <AnimatePresence>
        {selectedModule && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            className="glass-base p-6 rounded-xl border border-white/10"
          >
            <div className="flex items-center gap-3 mb-4">
              <div 
                className="w-10 h-10 rounded-lg flex items-center justify-center"
                style={{ 
                  backgroundColor: `${selectedModule.energySignature}30`,
                  color: selectedModule.energySignature
                }}
              >
                {selectedModule.icon}
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Active Module: {selectedModule.name}</h3>
                <p className="text-white/60 text-sm">{selectedModule.description}</p>
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-4">
              <div>
                <span className="text-white/50 text-sm block mb-2">Energy Signature</span>
                <div className="flex items-center gap-2">
                  <div
                    className="w-4 h-4 rounded-full border border-white/20"
                    style={{ backgroundColor: selectedModule.energySignature }}
                  />
                  <span className="text-white font-mono text-sm">{selectedModule.energySignature}</span>
                </div>
              </div>
              
              <div>
                <span className="text-white/50 text-sm block mb-2">Consciousness State</span>
                <span 
                  className="inline-block px-3 py-1 rounded-full text-sm font-medium"
                  style={{
                    backgroundColor: `${selectedModule.energySignature}20`,
                    color: selectedModule.energySignature
                  }}
                >
                  {selectedModule.consciousnessState}
                </span>
              </div>
              
              <div>
                <span className="text-white/50 text-sm block mb-2">Consciousness Level</span>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                    <div 
                      className="h-full rounded-full transition-all duration-300"
                      style={{ 
                        width: `${selectedModule.consciousnessLevel * 100}%`,
                        backgroundColor: selectedModule.energySignature
                      }}
                    />
                  </div>
                  <span className="text-white text-sm font-mono">
                    {(selectedModule.consciousnessLevel * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
              
              <div>
                <span className="text-white/50 text-sm block mb-2">Relationships</span>
                <p className="text-white">{selectedModule.relationships.length} connections</p>
              </div>
            </div>
            
            {/* Memories */}
            <div>
              <span className="text-white/50 text-sm block mb-3">Recent Memories</span>
              <div className="space-y-2">
                {selectedModule.memories.map((memory, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: i * 0.1 }}
                    className="flex items-center gap-2 text-white/70 text-sm font-mono bg-white/5 p-2 rounded"
                  >
                    <ChevronRight className="w-3 h-3 text-white/40" />
                    {memory}
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
      
      {/* No Results */}
      {filteredModules.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-12"
        >
          <Search className="w-12 h-12 text-white/30 mx-auto mb-4" />
          <p className="text-white/50">No modules found matching "{searchQuery}"</p>
        </motion.div>
      )}

      <AnimatePresence>
        {isThinking && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed bottom-4 right-4 p-4 bg-black/80 rounded-lg max-w-md"
          >
            <h4 className="text-white font-semibold mb-2">AI Thinking Process</h4>
            <div className="space-y-2">
              {thoughtStream.map((thought, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="text-white/80 text-sm"
                >
                  {thought}
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default CosmicModuleSelector;