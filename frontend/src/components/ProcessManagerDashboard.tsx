import { useEffect, useState, useRef } from 'react';

interface Process {
  name: string;
  is_running: boolean;
  start_time: string | null;
  last_tick: number | null;
  error: string | null;
  output: string[];
  color: string;
}

interface ProcessCardProps {
  process: Process;
  onToggle: (name: string) => Promise<void>;
  onOutput: (name: string, output: string) => void;
}

const ProcessCard: React.FC<ProcessCardProps> = ({ process, onToggle, onOutput }) => {
  const outputRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (outputRef.current) {
      outputRef.current.scrollTop = outputRef.current.scrollHeight;
    }
  }, [process.output]);

  return (
    <div
      style={{
        background: 'rgba(255, 255, 255, 0.1)',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        borderRadius: '1rem',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        padding: '1.5rem',
        margin: '1rem',
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        transition: 'all 0.3s ease',
        borderColor: process.color
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h3 style={{ 
          margin: 0,
          color: process.color,
          fontSize: '1.25rem',
          fontFamily: 'var(--font-mono)'
        }}>
          {process.name}
        </h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.5rem',
            color: process.is_running ? '#10b981' : '#ef4444'
          }}>
            <div style={{
              width: '0.75rem',
              height: '0.75rem',
              borderRadius: '50%',
              backgroundColor: process.is_running ? '#10b981' : '#ef4444',
              boxShadow: `0 0 8px ${process.is_running ? '#10b981' : '#ef4444'}`
            }} />
            {process.is_running ? 'Running' : 'Stopped'}
          </div>
          <button
            onClick={() => onToggle(process.name)}
            style={{
              padding: '0.5rem 1rem',
              background: process.is_running ? '#ef4444' : '#10b981',
              color: '#000',
              border: 'none',
              borderRadius: '0.5rem',
              cursor: 'pointer',
              fontFamily: 'var(--font-mono)',
              transition: 'all 0.2s ease'
            }}
          >
            {process.is_running ? 'Stop' : 'Start'}
          </button>
        </div>
      </div>

      <div style={{ marginBottom: '1rem' }}>
        <div style={{ color: '#9ca3af', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
          Last Tick: {process.last_tick || 'N/A'}
        </div>
        {process.error && (
          <div style={{ 
            color: '#ef4444', 
            fontSize: '0.875rem',
            marginBottom: '0.5rem',
            fontFamily: 'var(--font-mono)'
          }}>
            Error: {process.error}
          </div>
        )}
      </div>

      <div
        ref={outputRef}
        style={{
          background: 'rgba(0, 0, 0, 0.2)',
          padding: '1rem',
          borderRadius: '0.5rem',
          height: '200px',
          overflow: 'auto',
          fontFamily: 'var(--font-mono)',
          fontSize: '0.875rem',
          whiteSpace: 'pre-wrap',
          wordBreak: 'break-all'
        }}
      >
        {process.output.map((line, index) => (
          <div key={index} style={{ color: '#9ca3af' }}>
            {line}
          </div>
        ))}
      </div>
    </div>
  );
};

const ProcessManagerDashboard = () => {
  const [processes, setProcesses] = useState<Process[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  const fetchProcesses = async () => {
    try {
      const response = await fetch('http://localhost:8000/processes/status');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      // Ensure we have a processes array, default to empty array if not
      setProcesses(data?.processes || []);
    } catch (error) {
      console.error('Failed to fetch processes:', error);
      setProcesses([]); // Set empty array on error
    }
  };

  const getProcessColor = (name: string): string => {
    // Generate consistent colors based on process name
    const colors = [
      '#3b82f6', // blue
      '#10b981', // green
      '#f97316', // orange
      '#8b5cf6', // purple
      '#ec4899', // pink
      '#06b6d4', // cyan
    ];
    const index = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[index % colors.length];
  };

  const toggleProcess = async (name: string) => {
    const process = processes.find(p => p.name === name);
    if (!process) return;

    try {
      const endpoint = process.is_running ? 'stop' : 'start';
      const response = await fetch(`http://localhost:8000/processes/${name}/${endpoint}`, {
        method: 'POST'
      });
      const data = await response.json();
      
      if (data.success) {
        setProcesses(prev => prev.map(p => 
          p.name === name ? { ...p, is_running: !p.is_running } : p
        ));
      }
    } catch (error) {
      console.error(`Error toggling process ${name}:`, error);
    }
  };

  const addProcessOutput = (name: string, output: string) => {
    setProcesses(prev => prev.map(p => 
      p.name === name ? { ...p, output: [...p.output, output].slice(-100) } : p
    ));
  };

  useEffect(() => {
    const fetchProcesses = async () => {
      try {
        const response = await fetch('http://localhost:8000/processes/status');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // Ensure we have a processes array, default to empty array if not
        setProcesses(data?.processes || []);
      } catch (error) {
        console.error('Failed to fetch processes:', error);
        setProcesses([]); // Set empty array on error
      }
    };

    fetchProcesses();
    const interval = setInterval(fetchProcesses, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Process Manager</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {processes && processes.length > 0 ? (
          processes.map((process) => (
            <ProcessCard
              key={process.name}
              process={process}
              onToggle={toggleProcess}
              onOutput={addProcessOutput}
            />
          ))
        ) : (
          <div className="col-span-full text-center text-gray-500">
            No processes available
          </div>
        )}
      </div>
    </div>
  );
};

export default ProcessManagerDashboard; 