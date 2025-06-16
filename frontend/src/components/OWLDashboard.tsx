import { useState, useEffect, useRef } from 'react';
import { useHotkeys } from 'react-hotkeys-hook';

interface SystemMetrics {
  tickRate: number;
  cpuLoad: number;
  memoryUsage: number;
  activeProcesses: number;
  lastUpdate: number;
}

interface Command {
  id: string;
  name: string;
  description: string;
  action: () => void;
  category: string;
}

const OWLDashboard = () => {
  const [metrics, setMetrics] = useState<SystemMetrics>({
    tickRate: 0,
    cpuLoad: 0,
    memoryUsage: 0,
    activeProcesses: 0,
    lastUpdate: Date.now()
  });
  const [showCommandPalette, setShowCommandPalette] = useState(false);
  const [commandQuery, setCommandQuery] = useState('');
  const [selectedCommandIndex, setSelectedCommandIndex] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);
  const commandInputRef = useRef<HTMLInputElement>(null);

  // Command palette hotkey
  useHotkeys('cmd+k, ctrl+k', (e: KeyboardEvent) => {
    e.preventDefault();
    setShowCommandPalette(true);
  });

  // System metrics update
  useEffect(() => {
    wsRef.current = new WebSocket('ws://localhost:8000/ws');

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'system_metrics') {
          setMetrics(data.metrics);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Command palette focus
  useEffect(() => {
    if (showCommandPalette && commandInputRef.current) {
      commandInputRef.current.focus();
    }
  }, [showCommandPalette]);

  const commands: Command[] = [
    {
      id: 'restart',
      name: 'Restart System',
      description: 'Restart all DAWN processes',
      action: () => console.log('Restarting system...'),
      category: 'System'
    },
    {
      id: 'clear-memory',
      name: 'Clear Memory',
      description: 'Clear all memory structures',
      action: () => console.log('Clearing memory...'),
      category: 'Memory'
    },
    {
      id: 'export-logs',
      name: 'Export Logs',
      description: 'Export system logs to file',
      action: () => console.log('Exporting logs...'),
      category: 'System'
    },
    {
      id: 'toggle-debug',
      name: 'Toggle Debug Mode',
      description: 'Enable/disable debug logging',
      action: () => console.log('Toggling debug mode...'),
      category: 'System'
    }
  ];

  const filteredCommands = commands.filter(cmd => 
    cmd.name.toLowerCase().includes(commandQuery.toLowerCase()) ||
    cmd.description.toLowerCase().includes(commandQuery.toLowerCase())
  );

  const handleCommandSelect = (command: Command) => {
    command.action();
    setShowCommandPalette(false);
    setCommandQuery('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setShowCommandPalette(false);
      setCommandQuery('');
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedCommandIndex(prev => 
        Math.min(prev + 1, filteredCommands.length - 1)
      );
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedCommandIndex(prev => Math.max(prev - 1, 0));
    } else if (e.key === 'Enter' && filteredCommands[selectedCommandIndex]) {
      handleCommandSelect(filteredCommands[selectedCommandIndex]);
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      {/* System Health Grid */}
      <div style={{ 
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '2rem'
      }}>
        <div style={{
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(8px)',
          WebkitBackdropFilter: 'blur(8px)',
          padding: '1rem',
          borderRadius: '0.5rem',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Tick Rate</div>
          <div style={{ 
            color: '#00ff88',
            fontSize: '1.5rem',
            fontFamily: 'var(--font-mono)'
          }}>
            {metrics.tickRate.toFixed(1)} Hz
          </div>
        </div>

        <div style={{
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(8px)',
          WebkitBackdropFilter: 'blur(8px)',
          padding: '1rem',
          borderRadius: '0.5rem',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>CPU Load</div>
          <div style={{ 
            color: '#00ff88',
            fontSize: '1.5rem',
            fontFamily: 'var(--font-mono)'
          }}>
            {metrics.cpuLoad.toFixed(1)}%
          </div>
        </div>

        <div style={{
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(8px)',
          WebkitBackdropFilter: 'blur(8px)',
          padding: '1rem',
          borderRadius: '0.5rem',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Memory Usage</div>
          <div style={{ 
            color: '#00ff88',
            fontSize: '1.5rem',
            fontFamily: 'var(--font-mono)'
          }}>
            {metrics.memoryUsage.toFixed(1)}%
          </div>
        </div>

        <div style={{
          background: 'rgba(0, 0, 0, 0.8)',
          backdropFilter: 'blur(8px)',
          WebkitBackdropFilter: 'blur(8px)',
          padding: '1rem',
          borderRadius: '0.5rem',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>Active Processes</div>
          <div style={{ 
            color: '#00ff88',
            fontSize: '1.5rem',
            fontFamily: 'var(--font-mono)'
          }}>
            {metrics.activeProcesses}
          </div>
        </div>
      </div>

      {/* Command Palette */}
      {showCommandPalette && (
        <div
          style={{
            position: 'fixed',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '600px',
            maxWidth: '90vw',
            background: 'rgba(0, 0, 0, 0.95)',
            backdropFilter: 'blur(8px)',
            WebkitBackdropFilter: 'blur(8px)',
            borderRadius: '0.5rem',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            zIndex: 1000
          }}
        >
          <div style={{ padding: '1rem' }}>
            <input
              ref={commandInputRef}
              type="text"
              value={commandQuery}
              onChange={(e) => setCommandQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type a command or search..."
              style={{
                width: '100%',
                background: 'transparent',
                border: 'none',
                color: '#fff',
                fontSize: '1rem',
                fontFamily: 'var(--font-mono)',
                outline: 'none'
              }}
            />
          </div>

          <div style={{ 
            maxHeight: '300px',
            overflowY: 'auto'
          }}>
            {filteredCommands.map((command, index) => (
              <div
                key={command.id}
                onClick={() => handleCommandSelect(command)}
                style={{
                  padding: '0.75rem 1rem',
                  cursor: 'pointer',
                  background: index === selectedCommandIndex ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div>
                  <div style={{ color: '#fff' }}>{command.name}</div>
                  <div style={{ color: '#9ca3af', fontSize: '0.875rem' }}>
                    {command.description}
                  </div>
                </div>
                <div style={{ 
                  color: '#9ca3af',
                  fontSize: '0.875rem',
                  padding: '0.25rem 0.5rem',
                  background: 'rgba(255, 255, 255, 0.1)',
                  borderRadius: '0.25rem'
                }}>
                  {command.category}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Terminal Component */}
      <div style={{
        background: 'rgba(0, 0, 0, 0.8)',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        padding: '1rem',
        borderRadius: '0.5rem',
        border: '1px solid rgba(255, 255, 255, 0.1)',
        height: '300px',
        overflow: 'auto',
        fontFamily: 'var(--font-mono)',
        fontSize: '0.875rem',
        color: '#00ff88'
      }}>
        <div style={{ marginBottom: '0.5rem' }}>
          DAWN Terminal v1.0.0
        </div>
        <div style={{ color: '#9ca3af' }}>
          Type 'help' for available commands
        </div>
      </div>
    </div>
  );
};

export default OWLDashboard; 