import { create } from 'zustand';
import { subscribeWithSelector } from 'zustand/middleware';
import { FlowState, PythonProcess, DataFlow } from '../modules/ProcessFlowManager/types';

interface ProcessFlowStore extends FlowState {
  // Process management
  addProcess: (process: PythonProcess) => void;
  removeProcess: (processId: string) => void;
  updateProcess: (processId: string, updates: Partial<PythonProcess>) => void;
  
  // Flow management
  connectProcesses: (sourceId: string, sourcePort: string, targetId: string, targetPort: string) => void;
  disconnectFlow: (flowId: string) => void;
  updateFlow: (flowId: string, updates: Partial<DataFlow>) => void;
  
  // Process control
  startProcess: (processId: string) => Promise<void>;
  stopProcess: (processId: string) => Promise<void>;
  pauseProcess: (processId: string) => Promise<void>;
  restartProcess: (processId: string) => Promise<void>;
  
  // View control
  selectProcess: (processId: string | null) => void;
  setViewMode: (mode: '2d' | '3d') => void;
  toggleAutoArrange: () => void;
  toggleMetrics: () => void;
  setFlowSpeed: (speed: number) => void;
  
  // Batch operations
  startAllProcesses: () => Promise<void>;
  stopAllProcesses: () => Promise<void>;
  clearErrors: (processId?: string) => void;
  
  // Layout
  autoArrangeProcesses: () => void;
  updateProcessPosition: (processId: string, position: { x: number; y: number; z: number }) => void;
}

export const useProcessFlowStore = create<ProcessFlowStore>()(
  subscribeWithSelector((set, get) => ({
    // Initial state
    processes: new Map(),
    flows: new Map(),
    selectedProcessId: null,
    viewMode: '3d',
    autoArrange: true,
    showMetrics: true,
    flowSpeed: 1.0,
    
    // Process management
    addProcess: (process) => set((state) => {
      const newProcesses = new Map(state.processes);
      newProcesses.set(process.id, process);
      return { processes: newProcesses };
    }),
    
    removeProcess: (processId) => set((state) => {
      const newProcesses = new Map(state.processes);
      const newFlows = new Map(state.flows);
      
      // Remove associated flows
      for (const [flowId, flow] of newFlows) {
        if (flow.sourceProcessId === processId || flow.targetProcessId === processId) {
          newFlows.delete(flowId);
        }
      }
      
      newProcesses.delete(processId);
      return { processes: newProcesses, flows: newFlows };
    }),
    
    updateProcess: (processId, updates) => set((state) => {
      const newProcesses = new Map(state.processes);
      const process = newProcesses.get(processId);
      if (process) {
        newProcesses.set(processId, { ...process, ...updates });
      }
      return { processes: newProcesses };
    }),
    
    // Flow management
    connectProcesses: (sourceId, sourcePort, targetId, targetPort) => set((state) => {
      const flowId = `${sourceId}:${sourcePort}->${targetId}:${targetPort}`;
      const newFlows = new Map(state.flows);
      
      newFlows.set(flowId, {
        id: flowId,
        sourceProcessId: sourceId,
        sourcePortId: sourcePort,
        targetProcessId: targetId,
        targetPortId: targetPort,
        flowRate: 0,
        latency: 0,
        dataType: 'json',
        particles: [],
        color: '#00ff88',
        intensity: 1.0
      });
      
      return { flows: newFlows };
    }),
    
    // Process control
    startProcess: async (processId) => {
      const process = get().processes.get(processId);
      if (!process) return;
      
      set((state) => {
        const newProcesses = new Map(state.processes);
        newProcesses.set(processId, { ...process, status: 'running' });
        return { processes: newProcesses };
      });
      
      // API call to start process
      try {
        const response = await fetch(`/api/processes/${processId}/start`, { method: 'POST' });
        if (!response.ok) throw new Error('Failed to start process');
      } catch (error) {
        set((state) => {
          const newProcesses = new Map(state.processes);
          newProcesses.set(processId, { ...process, status: 'error' });
          return { processes: newProcesses };
        });
      }
    },
    
    stopProcess: async (processId) => {
      const process = get().processes.get(processId);
      if (!process) return;
      
      try {
        const response = await fetch(`/api/processes/${processId}/stop`, { method: 'POST' });
        if (!response.ok) throw new Error('Failed to stop process');
        
        set((state) => {
          const newProcesses = new Map(state.processes);
          newProcesses.set(processId, { ...process, status: 'idle' });
          return { processes: newProcesses };
        });
      } catch (error) {
        console.error('Failed to stop process:', error);
      }
    },
    
    pauseProcess: async (processId) => {
      const process = get().processes.get(processId);
      if (!process) return;
      
      set((state) => {
        const newProcesses = new Map(state.processes);
        newProcesses.set(processId, { ...process, status: 'paused' });
        return { processes: newProcesses };
      });
    },
    
    restartProcess: async (processId) => {
      await get().stopProcess(processId);
      setTimeout(() => get().startProcess(processId), 1000);
    },
    
    // Auto-arrange using force-directed layout
    autoArrangeProcesses: () => set((state) => {
      const newProcesses = new Map(state.processes);
      const processArray = Array.from(newProcesses.values());
      
      // Simple force-directed layout
      const center = { x: 0, y: 0, z: 0 };
      const radius = 300;
      const angleStep = (2 * Math.PI) / processArray.length;
      
      processArray.forEach((process, index) => {
        const angle = index * angleStep;
        const position = {
          x: center.x + radius * Math.cos(angle),
          y: center.y + radius * Math.sin(angle),
          z: center.z + (Math.random() - 0.5) * 100
        };
        
        newProcesses.set(process.id, { ...process, position });
      });
      
      return { processes: newProcesses };
    }),
    
    updateProcessPosition: (processId, position) => set((state) => {
      const newProcesses = new Map(state.processes);
      const process = newProcesses.get(processId);
      if (process) {
        newProcesses.set(processId, { ...process, position });
      }
      return { processes: newProcesses };
    }),
    
    // Other methods implementation
    disconnectFlow: (flowId) => set((state) => {
      const newFlows = new Map(state.flows);
      newFlows.delete(flowId);
      return { flows: newFlows };
    }),
    
    updateFlow: (flowId, updates) => set((state) => {
      const newFlows = new Map(state.flows);
      const flow = newFlows.get(flowId);
      if (flow) {
        newFlows.set(flowId, { ...flow, ...updates });
      }
      return { flows: newFlows };
    }),
    
    selectProcess: (processId) => set({ selectedProcessId: processId }),
    setViewMode: (mode) => set({ viewMode: mode }),
    toggleAutoArrange: () => set((state) => ({ autoArrange: !state.autoArrange })),
    toggleMetrics: () => set((state) => ({ showMetrics: !state.showMetrics })),
    setFlowSpeed: (speed) => set({ flowSpeed: speed }),
    
    startAllProcesses: async () => {
      const processes = get().processes;
      const promises = Array.from(processes.keys()).map(id => get().startProcess(id));
      await Promise.all(promises);
    },
    
    stopAllProcesses: async () => {
      const processes = get().processes;
      const promises = Array.from(processes.keys()).map(id => get().stopProcess(id));
      await Promise.all(promises);
    },
    
    clearErrors: (processId) => set((state) => {
      const newProcesses = new Map(state.processes);
      
      if (processId) {
        const process = newProcesses.get(processId);
        if (process) {
          newProcesses.set(processId, { ...process, errors: [] });
        }
      } else {
        // Clear all errors
        for (const [id, process] of newProcesses) {
          newProcesses.set(id, { ...process, errors: [] });
        }
      }
      
      return { processes: newProcesses };
    })
  }))
); 