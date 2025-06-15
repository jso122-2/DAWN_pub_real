import { useState, useEffect, useCallback, useRef } from 'react';
import { OwlState, Observation, OwlResponse, StrategicPlan, StrategicRecommendation } from '../types/owl.types';
import { owlConfig } from '../config/owl.config';

interface UseOwlStateOptions {
  autoConnect?: boolean;
  onObservation?: (observation: Observation) => void;
  onRecommendation?: (recommendation: StrategicRecommendation) => void;
  onError?: (error: Error) => void;
}

export function useOwlState(options: UseOwlStateOptions = {}) {
  const {
    autoConnect = true,
    onObservation,
    onRecommendation,
    onError
  } = options;

  // Connection state
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connecting' | 'connected' | 'error'>('disconnected');
  const [lastError, setLastError] = useState<string | null>(null);

  // Owl state
  const [owlState, setOwlState] = useState<Partial<OwlState> | null>(null);
  const [observations, setObservations] = useState<Observation[]>([]);
  const [activePlans, setActivePlans] = useState<StrategicPlan[]>([]);
  const [recommendations, setRecommendations] = useState<StrategicRecommendation[]>([]);
  const [lastResponse, setLastResponse] = useState<OwlResponse | null>(null);

  // Connection management
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const heartbeatIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttempts = useRef(0);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    setConnectionStatus('connecting');
    
    try {
      const ws = new WebSocket(owlConfig.websocket.url);

      ws.onopen = () => {
        console.log('🦉 Owl WebSocket connected');
        setIsConnected(true);
        setConnectionStatus('connected');
        setLastError(null);
        reconnectAttempts.current = 0;

        // Start heartbeat
        if (heartbeatIntervalRef.current) {
          clearInterval(heartbeatIntervalRef.current);
        }
        heartbeatIntervalRef.current = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
              type: 'heartbeat',
              timestamp: Date.now()
            }));
          }
        }, owlConfig.websocket.heartbeatInterval);
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          handleMessage(message);
        } catch (error) {
          console.error('Failed to parse Owl WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('Owl WebSocket error:', error);
        setLastError('WebSocket connection error');
        setConnectionStatus('error');
        onError?.(new Error('WebSocket connection error'));
      };

      ws.onclose = () => {
        console.log('🦉 Owl WebSocket disconnected');
        setIsConnected(false);
        setConnectionStatus('disconnected');
        
        // Clear heartbeat
        if (heartbeatIntervalRef.current) {
          clearInterval(heartbeatIntervalRef.current);
          heartbeatIntervalRef.current = null;
        }

        // Attempt reconnection
        if (reconnectAttempts.current < owlConfig.websocket.maxReconnectAttempts) {
          reconnectAttempts.current++;
          console.log(`🦉 Reconnecting to Owl... (attempt ${reconnectAttempts.current})`);
          
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, owlConfig.websocket.reconnectDelay);
        } else {
          console.error('🦉 Max reconnection attempts reached');
          setLastError('Failed to reconnect after multiple attempts');
          setConnectionStatus('error');
        }
      };

      wsRef.current = ws;

    } catch (error) {
      console.error('Failed to create Owl WebSocket connection:', error);
      setLastError('Failed to create WebSocket connection');
      setConnectionStatus('error');
      onError?.(error as Error);
    }
  }, [onError]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (heartbeatIntervalRef.current) {
      clearInterval(heartbeatIntervalRef.current);
      heartbeatIntervalRef.current = null;
    }

    setIsConnected(false);
    setConnectionStatus('disconnected');
  }, []);

  const handleMessage = useCallback((message: any) => {
    if (owlConfig.debug.enabled && owlConfig.debug.logObservations) {
      console.log('🦉 Owl message received:', message);
    }

    switch (message.type) {
      case 'owl_state':
        setOwlState(message.data);
        break;

      case 'owl_observation':
        const response = message.data as OwlResponse;
        setLastResponse(response);

        // Update observations
        if (response.observations) {
          setObservations(prev => {
            const newObs = [...prev, ...response.observations];
            return newObs.slice(-owlConfig.analysis.maxObservationBuffer);
          });

          // Trigger callbacks
          response.observations.forEach(obs => {
            onObservation?.(obs);
          });
        }

        // Update plans
        if (response.activePlans) {
          setActivePlans(response.activePlans);
        }

        // Update recommendations
        if (response.recommendations) {
          setRecommendations(prev => {
            const newRecs = [...prev, ...response.recommendations];
            // Trigger callbacks
            response.recommendations.forEach(rec => {
              onRecommendation?.(rec);
            });
            return newRecs.slice(-20); // Keep last 20 recommendations
          });
        }
        break;

      case 'observations':
        setObservations(message.data);
        break;

      case 'heartbeat_response':
        // Heartbeat acknowledged
        break;

      case 'error':
        console.error('🦉 Owl server error:', message.message);
        setLastError(message.message);
        onError?.(new Error(message.message));
        break;

      default:
        console.warn('🦉 Unknown Owl message type:', message.type);
    }
  }, [onObservation, onRecommendation, onError]);

  // Request specific data
  const requestObservations = useCallback((count: number = 50) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: 'get_observations',
        count
      }));
    }
  }, []);

  const requestPlans = useCallback(() => {
    // This would be a REST API call since plans are less frequently updated
    fetch('http://localhost:8001/api/owl/plans')
      .then(response => response.json())
      .then(data => {
        if (data.plans) {
          setActivePlans(data.plans);
        }
      })
      .catch(error => {
        console.error('Failed to fetch Owl plans:', error);
        onError?.(error);
      });
  }, [onError]);

  const requestSchemaAlignments = useCallback(() => {
    return fetch('http://localhost:8001/api/owl/schemas')
      .then(response => response.json())
      .catch(error => {
        console.error('Failed to fetch schema alignments:', error);
        onError?.(error);
        return null;
      });
  }, [onError]);

  // Filter and search functions
  const getObservationsByType = useCallback((type: string) => {
    return observations.filter(obs => obs.type === type);
  }, [observations]);

  const getRecentObservations = useCallback((count: number = 10) => {
    return observations.slice(-count);
  }, [observations]);

  const getHighSignificanceObservations = useCallback((threshold: number = 0.7) => {
    return observations.filter(obs => obs.significance >= threshold);
  }, [observations]);

  const getActiveRecommendations = useCallback(() => {
    return recommendations.filter(rec => rec.urgency >= 7); // High urgency
  }, [recommendations]);

  // Effects
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    return () => {
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    // Connection state
    isConnected,
    connectionStatus,
    lastError,
    
    // Owl state
    owlState,
    observations,
    activePlans,
    recommendations,
    lastResponse,
    
    // Actions
    connect,
    disconnect,
    requestObservations,
    requestPlans,
    requestSchemaAlignments,
    
    // Utilities
    getObservationsByType,
    getRecentObservations,
    getHighSignificanceObservations,
    getActiveRecommendations,
    
    // Metrics
    observationCount: observations.length,
    planCount: activePlans.length,
    recommendationCount: recommendations.length
  };
} 