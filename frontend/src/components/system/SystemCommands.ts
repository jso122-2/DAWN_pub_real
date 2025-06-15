import { Command } from '../../hooks/useCommandHandler';

export const systemCommands: Command[] = [
  {
    name: 'system',
    description: 'Show system status',
    execute: () => {
      console.log('\x1b[36mSystem Status:\x1b[0m');
      console.log('  CPU Usage: 45%');
      console.log('  Memory Usage: 2.3GB');
      console.log('  Active Threads: 12');
      console.log('  Uptime: 3h 45m');
    },
  },
  {
    name: 'modules',
    description: 'List active modules',
    execute: () => {
      console.log('\x1b[36mActive Modules:\x1b[0m');
      console.log('  1. Core Consciousness');
      console.log('  2. Neural Network');
      console.log('  3. Memory Manager');
      console.log('  4. Process Scheduler');
      console.log('  5. Event Handler');
    },
  },
  {
    name: 'logs',
    description: 'Show recent system logs',
    execute: () => {
      console.log('\x1b[36mRecent Logs:\x1b[0m');
      console.log('  [12:34:56] System initialized');
      console.log('  [12:34:57] Neural network loaded');
      console.log('  [12:34:58] Memory system ready');
      console.log('  [12:34:59] Process manager started');
    },
  },
  {
    name: 'config',
    description: 'Show system configuration',
    execute: () => {
      console.log('\x1b[36mSystem Configuration:\x1b[0m');
      console.log('  Mode: Development');
      console.log('  Debug Level: 2');
      console.log('  Logging: Enabled');
      console.log('  Auto-recovery: Enabled');
    },
  },
  {
    name: 'restart',
    description: 'Restart the system',
    execute: () => {
      console.log('\x1b[33mRestarting system...\x1b[0m');
      // TODO: Implement system restart
    },
  },
]; 