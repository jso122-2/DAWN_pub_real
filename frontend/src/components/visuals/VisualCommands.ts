import { Command } from '../terminal/types';

export const visualCommands: Command[] = [
  {
    name: 'visualize',
    description: 'Toggle visualization of a specific process',
    execute: async (args: string[]) => {
      const process = args[0];
      if (!process) {
        return 'Please specify a process to visualize';
      }
      return `Visualizing process: ${process}`;
    }
  },
  {
    name: 'list-processes',
    description: 'List all available processes for visualization',
    execute: async () => {
      return 'Available processes:\n- Neural Network\n- Consciousness Core\n- Memory System\n- Learning Module\n- Decision Engine';
    }
  },
  {
    name: 'visual-mode',
    description: 'Set visualization mode (graph, matrix, network)',
    execute: async (args: string[]) => {
      const mode = args[0];
      if (!mode) {
        return 'Please specify a visualization mode (graph, matrix, network)';
      }
      return `Set visualization mode to: ${mode}`;
    }
  },
  {
    name: 'clear-visual',
    description: 'Clear current visualization',
    execute: async () => {
      return 'Visualization cleared';
    }
  }
]; 