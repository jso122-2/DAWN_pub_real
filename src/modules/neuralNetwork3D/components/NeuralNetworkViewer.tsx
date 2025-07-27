import React, { useRef, useState, useCallback } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { motion } from 'framer-motion';
import * as THREE from 'three';
import { useConsciousnessStore } from '../../../stores/consciousnessStore';
import { useMetricsHistory } from '../../../hooks/useMetricsHistory';

export interface NeuralNetworkViewerProps {
  moduleId: string;
  position?: { x: number; y: number; z: number };
  onClose?: () => void;
  className?: string;
  onNeuronSelect?: (neuron: any) => void;
  showActivity?: boolean;
  showBrainwaves?: boolean;
}

type VisualizationMode = 'structure' | 'activity' | 'waves';

export const NeuralNetworkViewer: React.FC<NeuralNetworkViewerProps> = ({
  moduleId,
  position,
  onClose,
  className,
  onNeuronSelect,
  showActivity = true,
  showBrainwaves = true
}) => {
  const [selectedNeuron, setSelectedNeuron] = useState<any>(null);
  const [viewMode, setViewMode] = useState<VisualizationMode>('activity');
  const [showRegions, setShowRegions] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(1);
  
  // Get real consciousness data
  const { tickData, isConnected } = useConsciousnessStore();
  const metricsHistory = useMetricsHistory(tickData);
  
  // Generate network stats based on consciousness data
  const [networkStats, setNetworkStats] = useState({
    totalNodes: 2847,
    activeConnections: 15983,
    networkHealth: 31
  });
  
  // Update network based on consciousness data
  React.useEffect(() => {
    if (tickData) {
      setNetworkStats(prev => ({
        ...prev,
        activeConnections: Math.floor(prev.totalNodes * (tickData.scup / 100) * 6),
        networkHealth: Math.floor((tickData.scup / 100) * 100)
      }));
    }
  }, [tickData]);
  
  // Generate neurons based on consciousness state
  const neurons = React.useMemo(() => {
    const nodeCount = 50;
    const radius = 80;
    const nodes = [];
    
    for (let i = 0; i < nodeCount; i++) {
      const angle = (i / nodeCount) * Math.PI * 2;
      const layer = Math.floor(i / 10);
      const layerRadius = radius + layer * 20;
      
      nodes.push({
        id: `node-${i}`,
        x: Math.cos(angle) * layerRadius,
        y: Math.sin(angle) * layerRadius,
        z: (Math.random() - 0.5) * 40,
        active: Math.random() > 0.6,
        activity: tickData ? tickData.scup / 100 : Math.random(),
        connections: []
      });
    }
    
    // Create connections
    nodes.forEach((node, i) => {
      const connectionCount = Math.floor(Math.random() * 3) + 1;
      for (let j = 0; j < connectionCount; j++) {
        const targetIndex = (i + j + 1) % nodes.length;
        node.connections.push(nodes[targetIndex].id);
      }
    });
    
    return nodes;
  }, [tickData]);
  
  const isLoading = false;

  const handleNeuronClick = useCallback((neuron: any) => {
    setSelectedNeuron(neuron);
    onNeuronSelect?.(neuron);
  }, [onNeuronSelect]);
  
  // Add zoom controls
  const handleZoom = (direction: 'in' | 'out') => {
    setZoomLevel(prev => {
      const newLevel = direction === 'in' ? prev * 1.2 : prev / 1.2;
      return Math.max(0.5, Math.min(3, newLevel));
    });
  };

  if (isLoading) {
    return (
      <div className="w-full h-[600px] bg-slate-900/50 rounded-lg border border-slate-700/30 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400 mx-auto mb-4"></div>
          <span className="text-slate-400">Initializing neural network...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full h-[600px] bg-slate-900/50 rounded-lg border border-slate-700/30 relative overflow-hidden">
      {/* Header */}
      <div className="absolute top-0 left-0 right-0 z-10 flex justify-between items-center p-4 bg-slate-900/80 backdrop-blur-sm border-b border-slate-700/30">
        <div className="flex items-center gap-3">
          <h3 className="text-lg font-semibold text-slate-200">Neural Network 3D</h3>
          <div className="flex items-center gap-2 text-xs">
            <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
            <span className="text-green-400">Live Simulation</span>
          </div>
        </div>
        
        <div className="flex gap-2">
          {(['structure', 'activity', 'waves'] as VisualizationMode[]).map(mode => (
            <motion.button
              key={mode}
              className={`px-3 py-1 rounded text-sm font-medium transition-all ${
                viewMode === mode
                  ? 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                  : 'bg-slate-800/40 text-slate-400 border border-slate-600/30 hover:bg-slate-700/40'
              }`}
              onClick={() => setViewMode(mode)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {mode}
            </motion.button>
          ))}
        </div>
      </div>
      
      {/* 3D Canvas */}
      <Canvas
        className="w-full h-full"
        camera={{ position: [0, 0, 150], fov: 60 }}
        gl={{ 
          antialias: true, 
          alpha: true,
          powerPreference: "high-performance"
        }}
        onCreated={({ scene }) => {
          scene.background = new THREE.Color(0x0B1426);
          scene.fog = new THREE.Fog(0x1E293B, 100, 400);
        }}
      >
        {/* Lighting */}
        <ambientLight intensity={0.1} />
        <pointLight position={[0, 50, 0]} intensity={0.3} color="#4FC3F7" />
        <pointLight position={[50, 0, 0]} intensity={0.2} color="#E91E63" />
        <pointLight position={[-50, 0, 0]} intensity={0.2} color="#9C27B0" />
        
        {/* Camera Controls */}
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          autoRotate={viewMode === 'waves'}
          autoRotateSpeed={0.5}
          minDistance={50}
          maxDistance={300}
        />
        
        {/* Simple test mesh */}
        <mesh>
          <boxGeometry args={[2, 2, 2]} />
          <meshStandardMaterial color="#4FC3F7" />
        </mesh>
      </Canvas>
      
      {/* UI Overlays */}
      <div className="absolute top-20 left-4 bg-slate-900/80 backdrop-blur-sm rounded-lg p-3 border border-slate-700/30">
        <h4 className="text-sm font-semibold text-slate-200 mb-2">Network Stats</h4>
        <div className="space-y-1 text-xs">
          <div className="flex justify-between gap-4">
            <span className="text-slate-400">Neurons</span>
            <span className="text-slate-200">{neurons.length.toLocaleString()}</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-slate-400">Active</span>
            <span className="text-green-400">{networkStats.activeConnections}</span>
          </div>
          <div className="flex justify-between gap-4">
            <span className="text-slate-400">Health</span>
            <span className="text-blue-400">{networkStats.networkHealth}%</span>
          </div>
          {isConnected && (
            <div className="flex justify-between gap-4">
              <span className="text-slate-400">SCUP</span>
              <span className="text-purple-400">{tickData?.scup?.toFixed(1) || '0.0'}%</span>
            </div>
          )}
        </div>
      </div>
      
      {/* Network Controls */}
      <div className="absolute top-20 right-4 bg-slate-900/80 backdrop-blur-sm rounded-lg p-3 border border-slate-700/30">
        <h4 className="text-sm font-semibold text-slate-200 mb-2">Controls</h4>
        <div className="space-y-2">
          <div className="flex gap-2">
            <motion.button
              className="px-2 py-1 bg-blue-500/20 text-blue-300 border border-blue-500/30 rounded text-xs"
              onClick={() => handleZoom('in')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Zoom In
            </motion.button>
            <motion.button
              className="px-2 py-1 bg-blue-500/20 text-blue-300 border border-blue-500/30 rounded text-xs"
              onClick={() => handleZoom('out')}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Zoom Out
            </motion.button>
          </div>
          <motion.button
            className="w-full px-2 py-1 bg-slate-600/20 text-slate-300 border border-slate-600/30 rounded text-xs"
            onClick={() => setSelectedNeuron(null)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            Reset View
          </motion.button>
        </div>
      </div>
      
      {/* Node Details Panel */}
      {selectedNeuron && (
        <motion.div
          className="absolute bottom-4 left-4 bg-slate-900/90 backdrop-blur-sm rounded-lg p-4 border border-slate-700/30 min-w-[250px]"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
        >
          <div className="flex justify-between items-start mb-3">
            <h4 className="text-sm font-semibold text-slate-200">Node Details</h4>
            <motion.button
              className="text-slate-400 hover:text-slate-200 text-xs"
              onClick={() => setSelectedNeuron(null)}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
            >
              ✕
            </motion.button>
          </div>
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">ID:</span>
              <span className="text-slate-200">{selectedNeuron.id}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Connections:</span>
              <span className="text-slate-200">{selectedNeuron.connections?.length || 0}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Activity:</span>
              <span className={`${selectedNeuron.active ? 'text-green-400' : 'text-slate-400'}`}>
                {selectedNeuron.active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Level:</span>
              <span className="text-blue-400">{(selectedNeuron.activity * 100).toFixed(1)}%</span>
            </div>
          </div>
        </motion.div>
      )}
      
      {/* Connection Status Indicator */}
      <div className={`absolute bottom-4 right-4 px-3 py-2 rounded-lg text-xs font-medium ${
        isConnected 
          ? 'bg-green-500/20 text-green-300 border border-green-500/30' 
          : 'bg-red-500/20 text-red-300 border border-red-500/30'
      }`}>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${
            isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'
          }`} />
          {isConnected ? 'Live Data' : 'Disconnected'}
        </div>
      </div>
    </div>
  );
}; 