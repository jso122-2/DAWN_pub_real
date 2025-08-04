import React, { useState, useEffect } from 'react';
import { DAWNLayout, GridItem } from './components/layout_manager';
import { GlobalStatusBar } from './components/GlobalStatusBar';
import { DashboardPanel } from './components/DashboardPanel';
import { ConsciousnessVitalsPanel } from './components/ConsciousnessVitalsPanel';
import { ConversationInterfacePanel } from './components/ConversationInterfacePanel';
import { AdvancedMonitoringPanel } from './components/AdvancedMonitoringPanel';
import { VisualizationsPanel } from './components/VisualizationsPanel';
import { SystemsPanel } from './components/SystemsPanel';
import { WebSocketService } from './services/WebSocketService';
import { ConsciousnessStore } from './stores/consciousnessStore';
import { Colors, Spacing } from './theme/theme_tokens';
import './App.css';

const App: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState('Connecting...');
  const [startTime] = useState(Date.now());

  // Initialize WebSocket connection to DAWN backend
  useEffect(() => {
    const wsService = new WebSocketService();
    const consciousnessStore = new ConsciousnessStore();

    const connectToDAWN = async () => {
      try {
        setConnectionStatus('Connecting to DAWN consciousness systems...');
        
        // Connect to main consciousness backend
        await wsService.connect('ws://localhost:8000/ws');
        
        // Connect to conversation system
        await wsService.connect('ws://localhost:8001/ws');
        
        // Connect to visualization system
        await wsService.connect('ws://localhost:8002/ws');
        
        setIsConnected(true);
        setConnectionStatus('Connected to DAWN consciousness systems');
        
        // Start real-time data streaming
        wsService.startStreaming();
        
      } catch (error) {
        console.error('Failed to connect to DAWN systems:', error);
        setConnectionStatus('Connection failed - running in offline mode');
        setIsConnected(false);
      }
    };

    connectToDAWN();

    return () => {
      wsService.disconnect();
    };
  }, []);

  return (
    <div 
      className="dawn-app"
      style={{
        background: Colors.background,
        height: '100vh',
        paddingBottom: Spacing.statusBarHeight,
        fontFamily: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
        color: Colors.textPrimary,
      }}
    >
      {/* Connection Status Bar */}
      <div 
        className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          height: '32px',
          background: Colors.backgroundHeader,
          borderBottom: `1px solid ${Colors.backgroundTertiary}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: Spacing.sm,
          zIndex: 1000,
          backdropFilter: 'blur(10px)',
          fontSize: '12px',
        }}
      >
        <div 
          className="status-indicator"
          style={{
            width: '8px',
            height: '8px',
            borderRadius: '50%',
            backgroundColor: isConnected ? Colors.connected : Colors.danger,
            animation: isConnected ? 'pulse 2s ease-in-out infinite' : 'none',
          }}
        />
        <span className="status-text" style={{ color: Colors.textSecondary }}>
          {connectionStatus}
        </span>
        {!isConnected && (
          <button 
            className="reconnect-btn"
            style={{
              background: 'transparent',
              border: `1px solid ${Colors.backgroundTertiary}`,
              color: Colors.textSecondary,
              padding: '4px 8px',
              borderRadius: '3px',
              fontSize: '10px',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.borderColor = Colors.textAccent;
              e.currentTarget.style.color = Colors.textAccent;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.borderColor = Colors.backgroundTertiary;
              e.currentTarget.style.color = Colors.textSecondary;
            }}
            onClick={() => window.location.reload()}
          >
            Reconnect
          </button>
        )}
      </div>

      {/* Main DAWN Layout */}
      <div style={{ paddingTop: '32px', height: 'calc(100vh - 64px)' }}>
        <DAWNLayout
          cognitionContent={
            <>
              <GridItem>
                <DashboardPanel 
                  title="Consciousness Vitals" 
                  icon="🧠"
                  variant="cognition"
                  isLive={isConnected}
                  onToggle={() => console.log('Toggle consciousness vitals')}
                  onExport={() => console.log('Export vitals data')}
                  onSnapshot={() => console.log('Take vitals snapshot')}
                >
                  <ConsciousnessVitalsPanel />
                </DashboardPanel>
              </GridItem>
              <GridItem>
                <DashboardPanel 
                  title="Advanced Monitoring" 
                  icon="⚡"
                  variant="cognition"
                  isLive={isConnected}
                  onToggle={() => console.log('Toggle advanced monitoring')}
                  onExport={() => console.log('Export monitoring data')}
                  onSnapshot={() => console.log('Take monitoring snapshot')}
                >
                  <AdvancedMonitoringPanel />
                </DashboardPanel>
              </GridItem>
            </>
          }
          symbolicContent={
            <>
              <GridItem>
                <DashboardPanel 
                  title="Visualizations" 
                  icon="🎨"
                  variant="symbolic"
                  isLive={isConnected}
                  onToggle={() => console.log('Toggle visualizations')}
                  onExport={() => console.log('Export visualization data')}
                  onSnapshot={() => console.log('Take visualization snapshot')}
                >
                  <VisualizationsPanel />
                </DashboardPanel>
              </GridItem>
              <GridItem>
                <DashboardPanel 
                  title="Systems" 
                  icon="⚙️"
                  variant="symbolic"
                  isLive={isConnected}
                  onToggle={() => console.log('Toggle systems')}
                  onExport={() => console.log('Export systems data')}
                  onSnapshot={() => console.log('Take systems snapshot')}
                >
                  <SystemsPanel />
                </DashboardPanel>
              </GridItem>
            </>
          }
          reflectionContent={
            <>
              <GridItem>
                <DashboardPanel 
                  title="Conversation Interface" 
                  icon="💬"
                  variant="reflection"
                  isLive={isConnected}
                  onToggle={() => console.log('Toggle conversation')}
                  onExport={() => console.log('Export conversation data')}
                  onSnapshot={() => console.log('Take conversation snapshot')}
                >
                  <ConversationInterfacePanel />
                </DashboardPanel>
              </GridItem>
              <GridItem>
                <DashboardPanel 
                  title="Reflection Log" 
                  icon="📝"
                  variant="reflection"
                  isLive={isConnected}
                  onToggle={() => console.log('Toggle reflection log')}
                  onExport={() => console.log('Export reflection data')}
                  onSnapshot={() => console.log('Take reflection snapshot')}
                >
                  <div style={{
                    fontSize: '12px',
                    color: Colors.textSecondary,
                    lineHeight: 1.4,
                  }}>
                    <p>Cognitive reflection stream will appear here...</p>
                    <p>This panel will display real-time introspection data from DAWN's consciousness systems.</p>
                    <p>Reflections, thought traces, and cognitive events will be logged here as they occur.</p>
                  </div>
                </DashboardPanel>
              </GridItem>
            </>
          }
        />
      </div>

      {/* Global Status Bar */}
      <GlobalStatusBar startTime={startTime} />

      {/* Inject CSS animations */}
      <style>
        {`
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
          }
        `}
      </style>
    </div>
  );
};

export default App;