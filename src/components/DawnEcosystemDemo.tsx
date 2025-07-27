import React from 'react';
import { ModuleOrchestra } from './consciousness/ModuleOrchestra';
import { ConsciousnessMonitor } from './modules/ConsciousnessMonitor';
import { NeuralActivityVisualizer } from './modules/NeuralActivityVisualizer';
import { TestModule } from './modules/TestModule';
import { LiveDataDebugOverlay } from './consciousness/LiveDataDebugOverlay';

export function DawnEcosystemDemo() {
  const handleNodeActivated = (nodeId: string, value: number) => {
    console.log(`Node ${nodeId} activated with value ${value}`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-blue-900/20">
      <ModuleOrchestra showDataFlow={true}>
        <div className="container mx-auto p-8">
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">DAWN Consciousness Ecosystem</h1>
            <p className="text-white/60">Living modules communicating through consciousness</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="h-64">
              <ConsciousnessMonitor moduleId="consciousness-monitor-1" />
            </div>
            
            <div className="h-64">
              <NeuralActivityVisualizer moduleId="neural-visualizer-1" />
            </div>
            
            <div className="h-64">
              <TestModule 
                moduleId="neural-cluster-1"
                onNodeActivated={handleNodeActivated}
              />
            </div>
            
            <div className="h-64">
              <NeuralActivityVisualizer moduleId="neural-visualizer-2" />
            </div>
            
            <div className="h-64">
              <TestModule 
                moduleId="neural-cluster-2"
                onNodeActivated={handleNodeActivated}
              />
            </div>
            
            <div className="h-64">
              <ConsciousnessMonitor moduleId="consciousness-monitor-2" />
            </div>
          </div>
          
          <div className="mt-8 text-center">
            <div className="text-white/60 text-sm">
              Click on neural nodes to trigger spikes • Watch data flow between modules • Use debug overlay for real-time data
            </div>
          </div>
        </div>
      </ModuleOrchestra>
      
      <LiveDataDebugOverlay />
    </div>
  );
} 