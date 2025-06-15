import React, { useRef, useState, useCallback } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera, Stars } from '@react-three/drei';
import { motion } from 'framer-motion';
import { css } from '@emotion/css';
import * as THREE from 'three';
import { Memory, MemoryPattern } from '../types/memory.types';
import { useMemoryPalace } from '../hooks/useMemoryPalace';
import { MemoryNode } from '../three/MemoryNode';
import { ModuleContainer } from '../../../components/core/ModuleContainer';

export interface MemoryPalaceViewerProps {
  moduleId: string;
  position?: { x: number; y: number; z: number };
  onClose?: () => void;
  onMemorySelect?: (memory: Memory) => void;
  onPatternSelect?: (pattern: MemoryPattern) => void;
}

type VisualizationMode = 'spatial' | 'temporal' | 'emotional';

export const MemoryPalaceViewer: React.FC<MemoryPalaceViewerProps> = ({
  moduleId,
  position,
  onClose,
  onMemorySelect,
  onPatternSelect
}) => {
  const [selectedMemory, setSelectedMemory] = useState<Memory | null>(null);
  const [viewMode, setViewMode] = useState<VisualizationMode>('spatial');
  
  const { 
    memories, 
    patterns, 
    connections, 
    landmarks,
    statistics,
    isLoading 
  } = useMemoryPalace();
  
  const handleMemoryClick = useCallback((memory: Memory) => {
    setSelectedMemory(memory);
    onMemorySelect?.(memory);
  }, [onMemorySelect]);
  
  return (
    <ModuleContainer
      moduleId={moduleId}
      category="consciousness"
      position={position}
      onClose={onClose}
      className={`memory-palace-viewer ${containerStyles}`}
    >
      <div className={headerStyles}>
        <div className="flex items-center gap-3">
          <h3 className={titleStyles}>🏛️ Memory Palace</h3>
          <div className={statusStyles}>
            <div className={`${statusDotStyles} ${isLoading ? loadingStyles : activeStyles}`} />
            <span>{isLoading ? 'Loading...' : `${memories.length} memories`}</span>
          </div>
        </div>
        
        <div className={modeSelectStyles}>
          {(['spatial', 'temporal', 'emotional'] as VisualizationMode[]).map(mode => (
            <motion.button
              key={mode}
              className={modeButtonStyles(viewMode === mode)}
              onClick={() => setViewMode(mode)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {mode}
            </motion.button>
          ))}
        </div>
      </div>
      
      <div className={canvasContainerStyles}>
        <Canvas
          camera={{ position: [0, 50, 100], fov: 60 }}
          gl={{ antialias: true, alpha: true }}
        >
          <fog attach="fog" args={['#000033', 50, 500]} />
          <ambientLight intensity={0.2} />
          <pointLight position={[0, 100, 0]} intensity={0.5} />
          
          <Stars
            radius={300}
            depth={50}
            count={5000}
            factor={4}
            saturation={0}
            fade
          />
          
          {/* Memory Nodes */}
          {memories.map(memory => (
            <MemoryNode
              key={memory.id}
              memory={memory}
              selected={selectedMemory?.id === memory.id}
              onClick={() => handleMemoryClick(memory)}
              viewMode={viewMode}
            />
          ))}
          
          <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            minDistance={10}
            maxDistance={500}
          />
        </Canvas>
        
        {/* Statistics Panel */}
        <div className={statsStyles}>
          <h4>Palace Statistics</h4>
          <div className={statItemStyles}>
            <span>Memories</span>
            <span className={statValueStyles}>{statistics.totalMemories}</span>
          </div>
          <div className={statItemStyles}>
            <span>Patterns</span>
            <span className={statValueStyles}>{statistics.totalPatterns}</span>
          </div>
          <div className={statItemStyles}>
            <span>Avg Strength</span>
            <span className={statValueStyles}>
              {(statistics.averageStrength * 100).toFixed(0)}%
            </span>
          </div>
        </div>
      </div>
    </ModuleContainer>
  );
};

// Styles
const containerStyles = css`
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 600px;
`;

const headerStyles = css`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.1);
`;

const titleStyles = css`
  font-size: 1.25rem;
  font-weight: 600;
  color: rgba(226, 232, 240, 0.9);
  margin: 0;
`;

const statusStyles = css`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: rgba(148, 163, 184, 0.8);
`;

const statusDotStyles = css`
  width: 8px;
  height: 8px;
  border-radius: 50%;
`;

const loadingStyles = css`
  background: #FFC107;
  animation: pulse 2s infinite;
`;

const activeStyles = css`
  background: #4CAF50;
`;

const modeSelectStyles = css`
  display: flex;
  gap: 0.5rem;
`;

const modeButtonStyles = (isActive: boolean) => css`
  padding: 0.5rem 1rem;
  background: ${isActive 
    ? 'rgba(59, 130, 246, 0.2)' 
    : 'rgba(15, 23, 42, 0.4)'};
  border: 1px solid ${isActive 
    ? 'rgba(59, 130, 246, 0.4)' 
    : 'rgba(148, 163, 184, 0.2)'};
  border-radius: 6px;
  color: ${isActive 
    ? 'rgba(147, 197, 253, 0.9)' 
    : 'rgba(148, 163, 184, 0.8)'};
  font-size: 0.875rem;
  font-weight: 500;
  text-transform: capitalize;
  cursor: pointer;
  transition: all 0.2s ease;
`;

const canvasContainerStyles = css`
  flex: 1;
  position: relative;
  overflow: hidden;
`;

const statsStyles = css`
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: rgba(15, 23, 42, 0.9);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 8px;
  padding: 1rem;
  backdrop-filter: blur(10px);
  min-width: 200px;
  z-index: 10;
  
  h4 {
    margin: 0 0 1rem 0;
    color: rgba(226, 232, 240, 0.9);
    font-size: 0.875rem;
    font-weight: 600;
  }
`;

const statItemStyles = css`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: rgba(148, 163, 184, 0.9);
`;

const statValueStyles = css`
  font-weight: 600;
  color: rgba(59, 130, 246, 0.9);
`; 