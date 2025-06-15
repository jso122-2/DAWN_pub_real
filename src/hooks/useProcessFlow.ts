import { useEffect, useCallback } from 'react';
import { useProcessFlowStore } from '../store/processFlowStore';
import { processManager } from '../services/processManager';
import { PythonProcess } from '../modules/ProcessFlowManager/types';

export const useProcessFlow = () => {
  const store = useProcessFlowStore();
  
  // Initialize processes from available scripts
  const initializeProcesses = useCallback(async () => {
    try {
      const scripts = await processManager.listAvailableScripts();
      
      // Create processes for each script if none exist
      if (store.processes.size === 0) {
        const defaultProcesses = scripts.slice(0, 3).map((script, index) => {
          const angle = (index * 2 * Math.PI) / 3;
          const radius = 250;
          
          return {
            id: `process-${Date.now()}-${index}`,
            name: script.replace(/\.py$/, '').replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
            script,
            status: 'idle' as const,
            category: script.includes('neural') ? 'neural' as const :
                     script.includes('consciousness') ? 'consciousness' as const :
                     script.includes('memory') ? 'memory' as const :
                     script.includes('synthesis') ? 'synthesis' as const : 'analysis' as const,
            cpuUsage: 0,
            memoryUsage: 0,
            executionTime: 0,
            lastTick: 0,
            inputs: [{ id: 'in1', name: 'Input', type: 'data' as const, dataType: 'json' as const, connected: false }],
            outputs: [{ id: 'out1', name: 'Output', type: 'data' as const, dataType: 'json' as const, connected: false }],
            description: `Executes ${script}`,
            author: 'DAWN',
            version: '1.0.0',
            dependencies: [],
            logs: [],
            errors: [],
            outputData: null,
            position: {
              x: Math.cos(angle) * radius,
              y: Math.sin(angle) * radius,
              z: (Math.random() - 0.5) * 100
            },
            velocity: { x: 0, y: 0, z: 0 }
          } as PythonProcess;
        });
        
        defaultProcesses.forEach(process => store.addProcess(process));
      }
    } catch (error) {
      console.error('Failed to initialize processes:', error);
    }
  }, [store]);
  
  // Monitor process performance
  const monitorProcess = useCallback((processId: string) => {
    const cleanup = processManager.streamProcessOutput(processId, (data) => {
      store.updateProcess(processId, {
        cpuUsage: data.cpuUsage || 0,
        memoryUsage: data.memoryUsage || 0,
        logs: [...(store.processes.get(processId)?.logs || []), {
          timestamp: data.timestamp,
          level: data.level || 'info',
          message: data.message || 'Process output',
          data: data.data
        }].slice(-50) // Keep only last 50 logs
      });
    });
    
    return cleanup;
  }, [store]);
  
  // Create data flow between processes
  const createFlow = useCallback((sourceId: string, targetId: string) => {
    const sourceProcess = store.processes.get(sourceId);
    const targetProcess = store.processes.get(targetId);
    
    if (!sourceProcess || !targetProcess) return;
    
    // Find compatible ports
    const sourcePort = sourceProcess.outputs.find(port => !port.connected);
    const targetPort = targetProcess.inputs.find(port => !port.connected);
    
    if (sourcePort && targetPort) {
      store.connectProcesses(sourceId, sourcePort.id, targetId, targetPort.id);
      
      // Mark ports as connected
      store.updateProcess(sourceId, {
        outputs: sourceProcess.outputs.map(port => 
          port.id === sourcePort.id ? { ...port, connected: true } : port
        )
      });
      
      store.updateProcess(targetId, {
        inputs: targetProcess.inputs.map(port => 
          port.id === targetPort.id ? { ...port, connected: true } : port
        )
      });
    }
  }, [store]);
  
  // Auto-arrange processes in optimal layout
  const optimizeLayout = useCallback(() => {
    const processes = Array.from(store.processes.values());
    const flows = Array.from(store.flows.values());
    
    // Simple force-directed layout algorithm
    const iterations = 50;
    const attraction = 0.01;
    const repulsion = 1000;
    
    for (let i = 0; i < iterations; i++) {
      processes.forEach(process => {
        let fx = 0, fy = 0;
        
        // Repulsion from other processes
        processes.forEach(other => {
          if (other.id !== process.id) {
            const dx = process.position.x - other.position.x;
            const dy = process.position.y - other.position.y;
            const distance = Math.sqrt(dx * dx + dy * dy) || 1;
            
            if (distance < 300) {
              const force = repulsion / (distance * distance);
              fx += (dx / distance) * force;
              fy += (dy / distance) * force;
            }
          }
        });
        
        // Attraction to connected processes
        flows.forEach(flow => {
          if (flow.sourceProcessId === process.id) {
            const target = processes.find(p => p.id === flow.targetProcessId);
            if (target) {
              const dx = target.position.x - process.position.x;
              const dy = target.position.y - process.position.y;
              fx += dx * attraction;
              fy += dy * attraction;
            }
          }
          if (flow.targetProcessId === process.id) {
            const source = processes.find(p => p.id === flow.sourceProcessId);
            if (source) {
              const dx = source.position.x - process.position.x;
              const dy = source.position.y - process.position.y;
              fx += dx * attraction;
              fy += dy * attraction;
            }
          }
        });
        
        // Update position
        store.updateProcessPosition(process.id, {
          x: process.position.x + fx * 0.1,
          y: process.position.y + fy * 0.1,
          z: process.position.z
        });
      });
    }
  }, [store]);
  
  // Performance metrics aggregation
  const getSystemMetrics = useCallback(() => {
    const processes = Array.from(store.processes.values());
    const runningProcesses = processes.filter(p => p.status === 'running');
    
    return {
      totalProcesses: processes.length,
      runningProcesses: runningProcesses.length,
      averageCpuUsage: runningProcesses.reduce((sum, p) => sum + p.cpuUsage, 0) / runningProcesses.length || 0,
      totalMemoryUsage: runningProcesses.reduce((sum, p) => sum + p.memoryUsage, 0),
      errorCount: processes.reduce((sum, p) => sum + p.errors.length, 0),
      flowCount: store.flows.size
    };
  }, [store]);
  
  return {
    // Store state
    ...store,
    
    // Custom hooks
    initializeProcesses,
    monitorProcess,
    createFlow,
    optimizeLayout,
    getSystemMetrics
  };
}; 