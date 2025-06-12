import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

interface Subprocess {
  pid: number;
  name: string;
  cpu: number;
  memory: number;
  status: string;
  entropy: number;
}

interface EntropyUpdate {
  entropy: number;
}

interface SubprocessUpdate {
  processes: Subprocess[];
}

export const useEntropyState = () => {
  const [systemEntropy, setSystemEntropy] = useState<number>(45);
  const [subprocesses, setSubprocesses] = useState<Subprocess[]>([]);
  
  useEffect(() => {
    // Connect to your backend websocket
    const socket = io('ws://localhost:3001/entropy');
    
    socket.on('entropy-update', (data: EntropyUpdate) => {
      setSystemEntropy(data.entropy);
    });
    
    socket.on('subprocess-update', (data: SubprocessUpdate) => {
      setSubprocesses(data.processes);
    });
    
    return () => socket.disconnect();
  }, []);
  
  return { systemEntropy, subprocesses };
}; 