import React, { useEffect, useState } from 'react';
import { VisualProcessViewer } from '../components/visual/VisualProcessViewer';

interface ProcessInfo {
  name: string;
  is_active: boolean;
  fps: number;
  frame_count: number;
  last_update: number;
}

export const VisualProcesses: React.FC = () => {
  const [processes, setProcesses] = useState<ProcessInfo[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch available processes
  useEffect(() => {
    const fetchProcesses = async () => {
      try {
        const response = await fetch('/api/processes');
        if (response.ok) {
          const data = await response.json();
          setProcesses(data);
        } else {
          setError('Failed to fetch processes');
        }
      } catch (e) {
        setError('Error fetching processes');
      } finally {
        setLoading(false);
      }
    };

    fetchProcesses();
    const interval = setInterval(fetchProcesses, 5000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="terminal-module p-4">
        <div className="text-white/60 font-mono">Loading processes...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="terminal-module p-4">
        <div className="terminal-alert error">{error}</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="app-title">Visual Processes</h1>
        <p className="app-subtitle">DAWN Neural Visualization System</p>
      </header>

      <div className="terminal-grid">
        {processes.map((process) => (
          <VisualProcessViewer
            key={process.name}
            processName={process.name}
            width={800}
            height={600}
          />
        ))}
      </div>

      {processes.length === 0 && (
        <div className="terminal-module p-4">
          <div className="text-white/60 font-mono">No visual processes available</div>
        </div>
      )}
    </div>
  );
}; 