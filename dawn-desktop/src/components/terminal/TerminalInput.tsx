import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';

interface TerminalInputProps {
  onCommand: (command: string) => void;
  prompt?: string;
  disabled?: boolean;
  className?: string;
}

export const TerminalInput: React.FC<TerminalInputProps> = ({
  onCommand,
  prompt = 'DAWN://>',
  disabled = false,
  className = '',
}) => {
  const [input, setInput] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input on mount
  useEffect(() => {
    if (!disabled) {
      inputRef.current?.focus();
    }
  }, [disabled]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onCommand(input.trim());
      setInput('');
    }
  };

  return (
    <motion.form
      onSubmit={handleSubmit}
      className={`terminal-input ${className}`}
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <span className="prompt">{prompt}</span>
      <input
        ref={inputRef}
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="input-field"
        disabled={disabled}
        spellCheck={false}
        autoComplete="off"
        autoCorrect="off"
        autoCapitalize="off"
      />
      <span className="cursor" />
    </motion.form>
  );
}; 