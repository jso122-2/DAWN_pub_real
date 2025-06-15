import WebSocketManager from './websocketManager';

type Command = {
  name: string;
  description: string;
  execute: (args: string[]) => void;
};

class CommandHandler {
  private commands: Map<string, Command> = new Map();
  private terminal: any; // Will be set to Terminal type when needed
  private wsManager!: WebSocketManager; // Using definite assignment assertion

  constructor(terminal: any) {
    this.terminal = terminal;
    this.wsManager = new WebSocketManager('ws://localhost:8000');
    this.registerDefaultCommands();
    this.setupWebSocketHandlers();
  }

  private setupWebSocketHandlers() {
    this.wsManager.on('status', (payload) => {
      this.terminal.writeln(`\x1b[36mStatus: ${payload.message}\x1b[0m`);
    });

    this.wsManager.on('error', (payload) => {
      this.terminal.writeln(`\x1b[31mError: ${payload.message}\x1b[0m`);
    });

    this.wsManager.setConnectionChangeHandler((connected) => {
      if (connected) {
        this.terminal.writeln('\x1b[32mConnected to DAWN backend\x1b[0m');
      } else {
        this.terminal.writeln('\x1b[31mDisconnected from DAWN backend\x1b[0m');
      }
    });
  }

  private registerDefaultCommands() {
    this.registerCommand({
      name: 'help',
      description: 'Show available commands',
      execute: () => this.showHelp(),
    });

    this.registerCommand({
      name: 'clear',
      description: 'Clear the terminal',
      execute: () => this.terminal.clear(),
    });

    this.registerCommand({
      name: 'echo',
      description: 'Echo the input',
      execute: (args) => this.terminal.writeln(args.join(' ')),
    });

    this.registerCommand({
      name: 'connect',
      description: 'Connect to DAWN backend',
      execute: () => {
        this.terminal.writeln('Connecting to DAWN backend...');
        this.wsManager.connect();
      },
    });

    this.registerCommand({
      name: 'disconnect',
      description: 'Disconnect from DAWN backend',
      execute: () => {
        this.terminal.writeln('Disconnecting from DAWN backend...');
        this.wsManager.disconnect();
      },
    });

    this.registerCommand({
      name: 'send',
      description: 'Send a message to DAWN backend (usage: send <type> <message>)',
      execute: (args) => {
        if (args.length < 2) {
          this.terminal.writeln('\x1b[31mUsage: send <type> <message>\x1b[0m');
          return;
        }
        const [type, ...messageParts] = args;
        const message = messageParts.join(' ');
        this.wsManager.send(type, { message });
        this.terminal.writeln(`\x1b[90mSent: ${type} - ${message}\x1b[0m`);
      },
    });
  }

  registerCommand(command: Command) {
    this.commands.set(command.name, command);
  }

  private showHelp() {
    this.terminal.writeln('\nAvailable commands:');
    this.commands.forEach((cmd) => {
      this.terminal.writeln(`  ${cmd.name.padEnd(10)} - ${cmd.description}`);
    });
    this.terminal.writeln('');
  }

  handleCommand(input: string) {
    const [command, ...args] = input.trim().split(' ');
    
    if (!command) return;

    const cmd = this.commands.get(command);
    if (cmd) {
      cmd.execute(args);
    } else {
      this.terminal.writeln(`\x1b[31mCommand not found: ${command}\x1b[0m`);
      this.terminal.writeln('Type "help" for available commands');
    }
  }
}

export default CommandHandler; 