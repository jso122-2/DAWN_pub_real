import { Command, CommandResponse, CommandRegistry, DAWN_COMMANDS } from '../types/commands';
import { webSocketManager } from './WebSocketManager';

export class CommandService {
  private registry: CommandRegistry;

  constructor(registry: CommandRegistry = DAWN_COMMANDS) {
    this.registry = registry;
  }

  async execute(command: string, args: any[] = [], kwargs: Record<string, any> = {}): Promise<CommandResponse> {
    // Validate command exists
    if (!this.registry[command]) {
      return {
        success: false,
        message: `Unknown command: ${command}`,
        error: 'COMMAND_NOT_FOUND'
      };
    }

    // Validate parameters
    const validation = this.validateParameters(command, args, kwargs);
    if (!validation.success) {
      return validation;
    }

    // Prepare command message
    const message: Command = {
      type: 'command',
      data: {
        command,
        args,
        kwargs
      },
      timestamp: Date.now()
    };

    try {
      // Send command via WebSocket
      webSocketManager.send(message);

      // Wait for response
      return new Promise((resolve) => {
        const timeout = setTimeout(() => {
          resolve({
            success: false,
            message: 'Command timed out',
            error: 'TIMEOUT'
          });
        }, 5000);

        const handler = (response: Command) => {
          if (response.type === 'command_response' && response.data.command === command) {
            clearTimeout(timeout);
            webSocketManager.removeListener('message', handler);
            resolve(response.data);
          }
        };

        webSocketManager.on('message', handler);
      });
    } catch (error) {
      return {
        success: false,
        message: 'Failed to execute command',
        error: error instanceof Error ? error.message : 'UNKNOWN_ERROR'
      };
    }
  }

  private validateParameters(command: string, args: any[], kwargs: Record<string, any>): CommandResponse {
    const commandDef = this.registry[command];
    if (!commandDef.parameters) {
      return { success: true, message: 'Command validated' };
    }

    const params = commandDef.parameters;
    const errors: string[] = [];

    // Check required parameters
    for (const [name, def] of Object.entries(params)) {
      if (def.required && !(name in kwargs)) {
        errors.push(`Missing required parameter: ${name}`);
      }
    }

    // Validate parameter types
    for (const [name, value] of Object.entries(kwargs)) {
      const def = params[name];
      if (!def) {
        errors.push(`Unknown parameter: ${name}`);
        continue;
      }

      if (typeof value !== def.type) {
        errors.push(`Invalid type for ${name}: expected ${def.type}, got ${typeof value}`);
      }
    }

    if (errors.length > 0) {
      return {
        success: false,
        message: 'Parameter validation failed',
        error: errors.join(', ')
      };
    }

    return { success: true, message: 'Command validated' };
  }

  getCommandHelp(command?: string): string {
    if (command) {
      const cmd = this.registry[command];
      if (!cmd) {
        return `Unknown command: ${command}`;
      }

      let help = `${command}: ${cmd.description}\n`;
      if (cmd.parameters) {
        help += '\nParameters:\n';
        for (const [name, def] of Object.entries(cmd.parameters)) {
          help += `  ${name} (${def.type})${def.required ? ' [required]' : ''}: ${def.description}\n`;
        }
      }
      return help;
    }

    // List all commands
    return Object.entries(this.registry)
      .map(([name, def]) => `${name}: ${def.description}`)
      .join('\n');
  }
}

// Create singleton instance
export const commandService = new CommandService(); 