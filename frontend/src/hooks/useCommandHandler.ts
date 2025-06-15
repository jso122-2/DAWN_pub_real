import { useCallback } from 'react';
import { useWebSocket } from './useWebSocket';
import { visualCommands } from '../components/visuals/VisualCommands';
import { dawnCommands } from '../components/consciousness/DAWNCommands';
import { monitorCommands } from '../components/system/MonitorCommands';
import { Command } from '../components/terminal/types';

const baseCommands = new Map<string, Command>();

// Register base commands
baseCommands.set('help', {
  name: 'help',
  description: 'Show available commands',
  execute: async () => {
    return Array.from(baseCommands.values())
      .map(cmd => `${cmd.name}: ${cmd.description}`)
      .join('\n');
  }
});

baseCommands.set('clear', {
  name: 'clear',
  description: 'Clear the terminal',
  execute: async () => {
    return '\x1Bc';
  }
});

// Register WebSocket commands
baseCommands.set('connect', {
  name: 'connect',
  description: 'Connect to WebSocket server',
  execute: async () => {
    return 'Connecting to WebSocket server...';
  }
});

baseCommands.set('disconnect', {
  name: 'disconnect',
  description: 'Disconnect from WebSocket server',
  execute: async () => {
    return 'Disconnecting from WebSocket server...';
  }
});

// Register visual commands
visualCommands.forEach(cmd => baseCommands.set(cmd.name, cmd));

// Register DAWN commands
dawnCommands.forEach(cmd => baseCommands.set(cmd.name, cmd));

// Register monitor commands
monitorCommands.forEach(cmd => baseCommands.set(cmd.name, cmd));

export const useCommandHandler = (commands?: Command[]) => {
  const { send } = useWebSocket();
  const commandMap = new Map(baseCommands);

  // Register provided commands
  if (commands) {
    commands.forEach(cmd => commandMap.set(cmd.name, cmd));
  }

  const handleCommand = useCallback(async (input: string) => {
    const [command, ...args] = input.trim().split(' ');
    const cmd = commandMap.get(command);

    if (cmd) {
      return await cmd.execute(args);
    }

    return `Command not found: ${command}. Type 'help' for available commands.`;
  }, [send]);

  const registerCommand = useCallback((command: Command) => {
    commandMap.set(command.name, command);
  }, []);

  return {
    handleCommand,
    registerCommand
  };
}; 