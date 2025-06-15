import React from 'react';
import { DataFlowVisualization } from './DataFlowVisualization';

interface ModuleOrchestraProps {
  children: React.ReactNode;
  showDataFlow?: boolean;
}

export const ModuleOrchestra: React.FC<ModuleOrchestraProps> = ({ 
  children, 
  showDataFlow = true 
}) => {
  return (
    <div className="relative min-h-screen">
      <div className="relative z-0">
        {children}
      </div>
      
      {showDataFlow && <DataFlowVisualization />}
      
      <div className="fixed top-4 right-4 z-20 bg-black/70 backdrop-blur-sm rounded-lg p-3">
        <div className="text-xs text-white/60 mb-1">Module Communication</div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span className="text-xs text-green-400 font-mono">ACTIVE</span>
        </div>
      </div>
    </div>
  );
}; 