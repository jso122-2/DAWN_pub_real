import { useEffect, useCallback, useState } from 'react';
import { moduleCommunicationHub, ModuleMessage } from '../services/ModuleCommunicationHub';

export function useModuleCommunication(moduleId: string, moduleType: string, capabilities: string[] = []) {
  const [messages, setMessages] = useState<ModuleMessage[]>([]);
  const [connections, setConnections] = useState(moduleCommunicationHub.getConnections());

  useEffect(() => {
    // Register this module
    moduleCommunicationHub.registerModule(moduleId, moduleType, capabilities);

    const handleMessage = (message: ModuleMessage) => {
      setMessages(prev => [...prev.slice(-49), message]);
    };

    const handleBroadcast = (message: ModuleMessage) => {
      if (message.sourceModuleId !== moduleId) {
        setMessages(prev => [...prev.slice(-49), message]);
      }
    };

    const handleConnectionUpdate = () => {
      setConnections(moduleCommunicationHub.getConnections());
    };

    // Subscribe to events
    moduleCommunicationHub.on(`message:${moduleId}`, handleMessage);
    moduleCommunicationHub.on('broadcast', handleBroadcast);
    moduleCommunicationHub.on('connectionCreated', handleConnectionUpdate);
    moduleCommunicationHub.on('connectionRemoved', handleConnectionUpdate);

    return () => {
      // Cleanup
      moduleCommunicationHub.off(`message:${moduleId}`, handleMessage);
      moduleCommunicationHub.off('broadcast', handleBroadcast);
      moduleCommunicationHub.off('connectionCreated', handleConnectionUpdate);
      moduleCommunicationHub.off('connectionRemoved', handleConnectionUpdate);
      moduleCommunicationHub.unregisterModule(moduleId);
    };
  }, [moduleId, moduleType]);

  const sendMessage = useCallback((
    type: ModuleMessage['type'],
    data: any,
    targetModuleId?: string,
    priority: ModuleMessage['priority'] = 'normal'
  ) => {
    return moduleCommunicationHub.sendMessage({
      sourceModuleId: moduleId,
      targetModuleId,
      type,
      data,
      priority
    });
  }, [moduleId]);

  const broadcast = useCallback((type: ModuleMessage['type'], data: any, priority: ModuleMessage['priority'] = 'normal') => {
    return sendMessage(type, data, undefined, priority);
  }, [sendMessage]);

  return {
    messages,
    connections: connections.filter(c => c.sourceId === moduleId || c.targetId === moduleId),
    sendMessage,
    broadcast
  };
} 