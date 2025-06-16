export interface Command {
  name: string;
  description: string;
  execute: (args: string[]) => Promise<string | void>;
}

export interface TerminalProps {
  commands: Command[];
}

export interface WebSocketMessage {
  type: string;
  data?: any;
  timestamp?: number;
  content?: any;
} 