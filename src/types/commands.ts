export interface Command {
  type: string;
  data: any;
  timestamp: number;
}

export interface CommandResponse {
  success: boolean;
  message: string;
  data?: any;
  error?: string;
}

export interface CommandRegistry {
  [key: string]: {
    description: string;
    parameters?: {
      [key: string]: {
        type: 'string' | 'number' | 'boolean';
        description: string;
        required?: boolean;
        default?: any;
      };
    };
  };
}

// Core DAWN commands
export const DAWN_COMMANDS: CommandRegistry = {
  // Status commands
  status: {
    description: 'Display DAWN\'s visual status',
  },
  schema: {
    description: 'Display schema integrity status',
  },

  // Stimulation commands
  emotion: {
    description: 'Stimulate emotional response',
    parameters: {
      type: {
        type: 'string',
        description: 'Emotion type (e.g., joy, sadness)',
        required: true,
      },
      intensity: {
        type: 'number',
        description: 'Emotion intensity (0-1)',
        required: true,
      },
    },
  },
  curiosity: {
    description: 'Stimulate curiosity patterns',
    parameters: {
      intensity: {
        type: 'number',
        description: 'Curiosity intensity (0-1)',
        required: true,
      },
    },
  },
  tension: {
    description: 'Stimulate tension dynamics',
    parameters: {
      amount: {
        type: 'number',
        description: 'Tension amount (0-1)',
        required: true,
      },
    },
  },

  // System commands
  heat: {
    description: 'Add manual heat to system',
    parameters: {
      amount: {
        type: 'number',
        description: 'Heat amount',
        required: true,
      },
      label: {
        type: 'string',
        description: 'Heat source label',
        default: 'manual',
      },
    },
  },
  debug_bloom: {
    description: 'Debug bloom system internals',
  },
  test_bloom: {
    description: 'Force a test bloom creation',
  },
  bloom_stats: {
    description: 'Display bloom activation statistics',
  },

  // Connection commands
  connect: {
    description: 'Connect to DAWN instance',
  },

  // Meta commands
  help: {
    description: 'Show available commands',
  },
  tick_status: {
    description: 'Show tick safety status',
  },
}; 