import { useState, useCallback } from 'react';
import { commandService } from '../services/CommandService';
import { CommandResponse } from '../types/commands';

export function useCommand() {
  const [isExecuting, setIsExecuting] = useState(false);
  const [lastResponse, setLastResponse] = useState<CommandResponse | null>(null);
  const [error, setError] = useState<Error | null>(null);

  const execute = useCallback(async (command: string, args: any[] = [], kwargs: Record<string, any> = {}) => {
    setIsExecuting(true);
    setError(null);

    try {
      const response = await commandService.execute(command, args, kwargs);
      setLastResponse(response);
      return response;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Unknown error');
      setError(error);
      return {
        success: false,
        message: 'Command execution failed',
        error: error.message
      };
    } finally {
      setIsExecuting(false);
    }
  }, []);

  const getHelp = useCallback((command?: string) => {
    return commandService.getCommandHelp(command);
  }, []);

  return {
    execute,
    getHelp,
    isExecuting,
    lastResponse,
    error
  };
} 