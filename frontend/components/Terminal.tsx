import React, { useEffect, useState } from 'react';
import { wsService, WebSocketMessage } from '../services/websocket';

export const Terminal: React.FC = () => {
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Subscribe to WebSocket messages
    const unsubscribe = wsService.subscribe((message) => {
      setMessages(prev => [...prev, message]);
      
      // Update connection status based on message type
      if (message.type === 'system' && message.content?.includes('Connected')) {
        setIsConnected(true);
      }
    });

    // Cleanup subscription on unmount
    return () => {
      unsubscribe();
    };
  }, []);

  return (
    <div className="terminal">
      <div className="terminal-header">
        <span className="status-indicator" style={{ 
          backgroundColor: isConnected ? '#00ff00' : '#ff0000' 
        }} />
        <span className="title">DAWN Terminal</span>
      </div>
      <div className="terminal-content">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            {msg.type === 'system' && <span className="prompt">SYS &gt;</span>}
            {msg.type === 'response' && <span className="prompt">DAWN &gt;</span>}
            <span className="content">{msg.content}</span>
            {msg.metadata && (
              <div className="metadata">
                {msg.metadata.tick && <span>[T:{msg.metadata.tick}]</span>}
                {msg.metadata.scup && <span>[S:{msg.metadata.scup}%]</span>}
                {msg.metadata.mood && <span>[M:{msg.metadata.mood}]</span>}
                {msg.metadata.process && <span>[P:{msg.metadata.process}]</span>}
                {msg.metadata.psl_metrics && (
                  <>
                    <span>[CPU:{msg.metadata.psl_metrics.cpu_usage_mean?.toFixed(1)}%]</span>
                    <span>[MEM:{msg.metadata.psl_metrics.memory_usage_mean?.toFixed(1)}%]</span>
                    <span>[PROC:{msg.metadata.psl_metrics.process_count_mean?.toFixed(0)}]</span>
                  </>
                )}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}; 