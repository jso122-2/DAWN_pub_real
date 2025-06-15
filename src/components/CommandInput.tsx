import React, { useState, useRef, useEffect } from 'react';
import { useCommand } from '../hooks/useCommand';
import { DAWN_COMMANDS } from '../types/commands';

export function CommandInput() {
  const [input, setInput] = useState('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showHelp, setShowHelp] = useState(false);
  const [helpCommand, setHelpCommand] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { execute, getHelp, isExecuting, lastResponse, error } = useCommand();

  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setInput(value);

    // Update suggestions
    if (value) {
      const matches = Object.keys(DAWN_COMMANDS).filter(cmd => 
        cmd.toLowerCase().startsWith(value.toLowerCase())
      );
      setSuggestions(matches);
    } else {
      setSuggestions([]);
    }

    // Update help
    if (value.startsWith('help ')) {
      const cmd = value.slice(5).trim();
      setHelpCommand(cmd || null);
      setShowHelp(true);
    } else {
      setShowHelp(false);
    }
  };

  // Handle command execution
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isExecuting) return;

    // Parse command and arguments
    const parts = input.trim().split(/\s+/);
    const command = parts[0];
    const args: any[] = [];
    const kwargs: Record<string, any> = {};

    // Parse remaining parts as args or kwargs
    for (let i = 1; i < parts.length; i++) {
      const part = parts[i];
      if (part.includes('=')) {
        const [key, value] = part.split('=');
        // Try to parse value as number
        const numValue = parseFloat(value);
        kwargs[key] = isNaN(numValue) ? value : numValue;
      } else {
        // Try to parse as number
        const numValue = parseFloat(part);
        args.push(isNaN(numValue) ? part : numValue);
      }
    }

    // Execute command
    await execute(command, args, kwargs);
    setInput('');
    setSuggestions([]);
  };

  // Handle suggestion selection
  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    setSuggestions([]);
    inputRef.current?.focus();
  };

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Tab' && suggestions.length > 0) {
      e.preventDefault();
      setInput(suggestions[0]);
      setSuggestions([]);
    }
  };

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form onSubmit={handleSubmit} className="relative">
        <div className="flex items-center space-x-2">
          <span className="text-gray-400 font-mono">DAWN{'>'}</span>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Type a command..."
            className="flex-1 bg-gray-900 text-gray-100 font-mono px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-gray-700"
            disabled={isExecuting}
          />
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div className="absolute left-0 right-0 mt-1 bg-gray-800 rounded shadow-lg z-10">
            {suggestions.map(suggestion => (
              <button
                key={suggestion}
                type="button"
                onClick={() => handleSuggestionClick(suggestion)}
                className="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 font-mono"
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}

        {/* Help display */}
        {showHelp && (
          <div className="mt-2 p-4 bg-gray-800 rounded text-sm font-mono">
            <pre className="whitespace-pre-wrap text-gray-300">
              {getHelp(helpCommand || undefined)}
            </pre>
          </div>
        )}

        {/* Response display */}
        {lastResponse && (
          <div className={`mt-2 p-4 rounded text-sm font-mono ${
            lastResponse.success ? 'bg-gray-800 text-gray-300' : 'bg-red-900/50 text-red-200'
          }`}>
            {lastResponse.message}
            {lastResponse.error && (
              <div className="mt-1 text-red-400">{lastResponse.error}</div>
            )}
          </div>
        )}

        {/* Error display */}
        {error && (
          <div className="mt-2 p-4 bg-red-900/50 text-red-200 rounded text-sm font-mono">
            {error.message}
          </div>
        )}
      </form>
    </div>
  );
} 