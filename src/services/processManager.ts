export interface ProcessStatus {
  id: string;
  status: 'idle' | 'running' | 'completed' | 'error' | 'paused';
  cpuUsage: number;
  memoryUsage: number;
  lastOutput?: string;
  startTime?: number;
  endTime?: number;
}

interface ProcessManagerAPI {
  startProcess: (processId: string) => Promise<void>;
  stopProcess: (processId: string) => Promise<void>;
  getProcessStatus: (processId: string) => Promise<ProcessStatus>;
  executeScript: (script: string, params?: any) => Promise<any>;
  streamProcessOutput: (processId: string, callback: (data: any) => void) => () => void;
  listAvailableScripts: () => Promise<string[]>;
}

export const processManager: ProcessManagerAPI = {
  startProcess: async (processId: string) => {
    try {
      const response = await fetch(`/api/processes/${processId}/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to start process: ${response.statusText}`);
      }
      
      const result = await response.json();
      console.log(`Process ${processId} started:`, result);
    } catch (error) {
      console.error('Error starting process:', error);
      throw error;
    }
  },
  
  stopProcess: async (processId: string) => {
    try {
      const response = await fetch(`/api/processes/${processId}/stop`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to stop process: ${response.statusText}`);
      }
      
      const result = await response.json();
      console.log(`Process ${processId} stopped:`, result);
    } catch (error) {
      console.error('Error stopping process:', error);
      throw error;
    }
  },
  
  getProcessStatus: async (processId: string): Promise<ProcessStatus> => {
    try {
      const response = await fetch(`/api/processes/${processId}/status`);
      
      if (!response.ok) {
        throw new Error(`Failed to get process status: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error getting process status:', error);
      // Return mock status for development
      return {
        id: processId,
        status: 'idle',
        cpuUsage: Math.random() * 50,
        memoryUsage: Math.random() * 100,
        lastOutput: 'Process status unavailable',
        startTime: Date.now() - Math.random() * 60000
      };
    }
  },
  
  executeScript: async (script: string, params?: any) => {
    try {
      const response = await fetch('/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ script, params })
      });
      
      if (!response.ok) {
        throw new Error(`Failed to execute script: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error executing script:', error);
      // Return mock response for development
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
        output: 'Script execution failed - API not available'
      };
    }
  },
  
  streamProcessOutput: (processId: string, callback: (data: any) => void): (() => void) => {
    try {
      const eventSource = new EventSource(`/api/processes/${processId}/stream`);
      
      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          callback(data);
        } catch (error) {
          console.error('Error parsing stream data:', error);
        }
      };
      
      eventSource.onerror = (error) => {
        console.error('EventSource error:', error);
        // Provide mock data for development
        const mockData = {
          timestamp: Date.now(),
          level: 'info',
          message: `Mock output for process ${processId}`,
          cpuUsage: Math.random() * 50,
          memoryUsage: Math.random() * 100
        };
        callback(mockData);
      };
      
      // Return cleanup function
      return () => {
        eventSource.close();
      };
    } catch (error) {
      console.error('Error setting up process stream:', error);
      // Return no-op cleanup function
      return () => {};
    }
  },
  
  listAvailableScripts: async (): Promise<string[]> => {
    try {
      const response = await fetch('/api/scripts');
      
      if (!response.ok) {
        throw new Error(`Failed to list scripts: ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error listing scripts:', error);
      // Return mock scripts for development
      return [
        'neural_process.py',
        'consciousness_analysis.py',
        'memory_consolidate.py',
        'pattern_synthesis.py',
        'entropy_monitor.py',
        'consciousness_probe.py',
        'dream_analyzer.py',
        'reality_mapper.py'
      ];
    }
  }
};

// Utility functions for process management
export const ProcessUtils = {
  formatProcessName: (script: string): string => {
    return script
      .replace(/\.py$/, '')
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  },
  
  getCategoryFromScript: (script: string): 'neural' | 'consciousness' | 'analysis' | 'synthesis' | 'memory' => {
    if (script.includes('neural')) return 'neural';
    if (script.includes('consciousness')) return 'consciousness';
    if (script.includes('memory')) return 'memory';
    if (script.includes('synthesis') || script.includes('pattern')) return 'synthesis';
    return 'analysis';
  },
  
  generateProcessId: (): string => {
    return `process-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  },
  
  getStatusColor: (status: string): string => {
    const colors = {
      idle: '#444444',
      running: '#00ff88',
      completed: '#0088ff',
      error: '#ff4444',
      paused: '#ffaa00'
    };
    return colors[status as keyof typeof colors] || '#666666';
  }
}; 