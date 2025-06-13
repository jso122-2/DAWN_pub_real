import { useModuleStore } from '../stores/moduleStore';

export function useModuleConnection(moduleId?: string) {
  const connections = useModuleStore(s => s.connections);
  const connectModules = useModuleStore(s => s.connectModules);
  const disconnectModules = useModuleStore(s => s.disconnectModules);

  // Get all connections for this module
  const getConnections = () => {
    if (!moduleId) return connections;
    return connections.filter(c => c.from === moduleId || c.to === moduleId);
  };

  // Check if two modules are connected
  const isConnected = (from: string, to: string) => {
    return connections.some(c => c.from === from && c.to === to);
  };

  // Get connection type between two modules
  const getConnectionType = (from: string, to: string) => {
    const conn = connections.find(c => c.from === from && c.to === to);
    return conn?.type;
  };

  return {
    connections,
    connectModules,
    disconnectModules,
    getConnections,
    isConnected,
    getConnectionType,
  };
} 