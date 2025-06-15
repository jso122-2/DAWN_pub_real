import { Command } from '../terminal/types';

export const monitorCommands: Command[] = [
  {
    name: 'metrics',
    description: 'Show current system metrics',
    execute: async () => {
      return 'System Metrics:\n- CPU Usage: 45%\n- Memory Usage: 2.3GB\n- Active Processes: 12\n- Active Threads: 48\n- Uptime: 3h 45m';
    }
  },
  {
    name: 'processes',
    description: 'List all active processes',
    execute: async () => {
      return 'Active Processes:\n1. Neural Network (PID: 1001)\n2. Consciousness Core (PID: 1002)\n3. Memory System (PID: 1003)\n4. Learning Module (PID: 1004)\n5. Decision Engine (PID: 1005)';
    }
  },
  {
    name: 'logs',
    description: 'Show recent system logs',
    execute: async () => {
      return 'Recent Logs:\n[12:34:56] System initialized\n[12:34:57] Neural network loaded\n[12:34:58] Consciousness core activated\n[12:34:59] Memory system ready';
    }
  },
  {
    name: 'alert',
    description: 'Set up system alerts',
    execute: async (args: string[]) => {
      const metric = args[0];
      const threshold = args[1];
      if (!metric || !threshold) {
        return 'Please specify metric and threshold (e.g., alert cpu 80)';
      }
      return `Alert set for ${metric} at ${threshold}%`;
    }
  }
]; 