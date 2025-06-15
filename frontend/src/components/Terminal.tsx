import React, { useEffect, useRef, useState } from 'react';
import { wsService } from '../services/websocket';
import { useCosmicStore } from '../store/cosmic.store';
import { TickData, ModuleStatus } from '../types';
import '../styles/terminal.css';

export const Terminal: React.FC = () => {
    const [tickData, setTickData] = useState<TickData | null>(null);
    const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'connecting'>('disconnected');
    const terminalRef = useRef<HTMLDivElement>(null);
    
    // Use the cosmic store
    const cosmicState = useCosmicStore((state) => ({
        systemUnity: state.systemUnity,
        entropy: state.entropy,
        mood: state.mood,
        neuralActivity: state.neuralActivity,
        systemLoad: state.systemLoad,
        quantumCoherence: state.quantumCoherence
    }));

    useEffect(() => {
        const handleTickData = (data: TickData | ModuleStatus | string) => {
            if (typeof data === 'object' && 'tick_number' in data) {
                const tickData = data as TickData;
                setTickData(tickData);
                // Update cosmic store with new data
                useCosmicStore.getState().updateEntropy(tickData.entropy);
                useCosmicStore.getState().updateMood(tickData.mood);
                useCosmicStore.getState().updateSystemUnity(tickData.scup);
            }
        };

        const handleConnectionStatus = (data: TickData | ModuleStatus | string) => {
            if (typeof data === 'string' && ['connected', 'disconnected', 'connecting'].includes(data)) {
                setConnectionStatus(data as 'connected' | 'disconnected' | 'connecting');
            }
        };

        // Add WebSocket event handlers
        wsService.on('tick_data', handleTickData);
        wsService.on('connection_status', handleConnectionStatus);

        // Connect to WebSocket
        wsService.connect();

        return () => {
            // Cleanup handlers
            wsService.off('tick_data', handleTickData);
            wsService.off('connection_status', handleConnectionStatus);
            wsService.disconnect();
        };
    }, []);

    useEffect(() => {
        if (terminalRef.current) {
            terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
        }
    }, [tickData]);

    const formatTimestamp = () => {
        return new Date().toLocaleTimeString();
    };

    return (
        <div className="terminal-container">
            <div className="terminal-header">
                <div className="terminal-title">DAWN Consciousness Engine</div>
                <div className={`connection-status ${connectionStatus}`}>
                    {connectionStatus.toUpperCase()}
                </div>
            </div>
            <div className="terminal-body" ref={terminalRef}>
                {tickData ? (
                    <div className="tick-data">
                        <div className="tick-header">
                            <span className="tick-number">Tick #{tickData.tick_number}</span>
                            <span className="tick-time">{formatTimestamp()}</span>
                        </div>
                        <div className="metrics">
                            <div className="metric">
                                <span className="label">SCUP:</span>
                                <span className="value">{cosmicState.systemUnity.toFixed(2)}</span>
                            </div>
                            <div className="metric">
                                <span className="label">Entropy:</span>
                                <span className="value">{cosmicState.entropy.toFixed(2)}</span>
                            </div>
                            <div className="metric">
                                <span className="label">Mood:</span>
                                <span className="value">{cosmicState.mood}</span>
                            </div>
                            <div className="metric">
                                <span className="label">Neural Activity:</span>
                                <span className="value">{cosmicState.neuralActivity.toFixed(2)}</span>
                            </div>
                            <div className="metric">
                                <span className="label">System Load:</span>
                                <span className="value">{cosmicState.systemLoad.toFixed(2)}%</span>
                            </div>
                            <div className="metric">
                                <span className="label">Quantum Coherence:</span>
                                <span className="value">{cosmicState.quantumCoherence.toFixed(2)}</span>
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="no-data">
                        Waiting for tick data...
                    </div>
                )}
            </div>
        </div>
    );
}; 