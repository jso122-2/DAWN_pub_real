import { useState, useEffect } from 'react';

interface Subprocess {
  pid: number;
  name: string;
  status: 'active' | 'idle' | 'processing';
  cpu: number;
  memory: number;
  entropy: number;
}

export const useEntropyState = () => {
  const [systemEntropy, setSystemEntropy] = useState(45);
  const [subprocesses, setSubprocesses] = useState<Subprocess[]>([]);

  useEffect(() => {
    // Simulate entropy changes
    const interval = setInterval(() => {
      setSystemEntropy(prev => {
        const change = (Math.random() - 0.5) * 10;
        return Math.max(0, Math.min(100, prev + change));
      });

      // Generate mock subprocesses
      setSubprocesses([
        {
          pid: 1234,
          name: 'Neural Core',
          status: Math.random() > 0.3 ? 'active' : 'idle',
          cpu: Math.random() * 100,
          memory: Math.random() * 1024,
          entropy: Math.random() * 100
        },
        {
          pid: 5678,
          name: 'Consciousness Engine',
          status: Math.random() > 0.5 ? 'processing' : 'active',
          cpu: Math.random() * 100,
          memory: Math.random() * 2048,
          entropy: Math.random() * 100
        },
        {
          pid: 9012,
          name: 'Memory Cortex',
          status: 'active',
          cpu: Math.random() * 50,
          memory: Math.random() * 512,
          entropy: Math.random() * 100
        }
      ]);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return { systemEntropy, subprocesses };
};
