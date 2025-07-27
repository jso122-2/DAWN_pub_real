import { EventEmitter } from 'events';

export interface ModuleMessage {
  id: string;
  sourceModuleId: string;
  targetModuleId?: string;
  type: 'consciousness_update' | 'neural_spike' | 'memory_access' | 'process_complete' | 'custom';
  data: any;
  timestamp: number;
  priority: 'low' | 'normal' | 'high' | 'critical';
}

export interface ModuleConnection {
  id: string;
  sourceId: string;
  targetId: string;
  dataType: string;
  strength: number;
  active: boolean;
}

interface ModuleInfo {
  id: string;
  type: string;
  capabilities: string[];
  lastSeen: number;
  messageCount: number;
}

class ModuleCommunicationHub extends EventEmitter {
  private modules = new Map<string, ModuleInfo>();
  private connections = new Map<string, ModuleConnection>();
  private messageHistory: ModuleMessage[] = [];
  private maxHistorySize = 1000;

  registerModule(moduleId: string, moduleType: string, capabilities: string[]) {
    this.modules.set(moduleId, {
      id: moduleId,
      type: moduleType,
      capabilities,
      lastSeen: Date.now(),
      messageCount: 0
    });
    
    this.emit('moduleRegistered', { moduleId, moduleType });
  }

  unregisterModule(moduleId: string) {
    this.modules.delete(moduleId);
    
    // Remove connections involving this module
    for (const [connId, conn] of this.connections) {
      if (conn.sourceId === moduleId || conn.targetId === moduleId) {
        this.connections.delete(connId);
      }
    }
    
    this.emit('moduleUnregistered', { moduleId });
  }

  sendMessage(message: Omit<ModuleMessage, 'id' | 'timestamp'>) {
    const fullMessage: ModuleMessage = {
      ...message,
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    };

    // Add to history
    this.messageHistory.push(fullMessage);
    if (this.messageHistory.length > this.maxHistorySize) {
      this.messageHistory.shift();
    }

    // Update source module stats
    const sourceModule = this.modules.get(message.sourceModuleId);
    if (sourceModule) {
      sourceModule.messageCount++;
      sourceModule.lastSeen = Date.now();
    }

    // Route message
    if (message.targetModuleId) {
      this.emit(`message:${message.targetModuleId}`, fullMessage);
    } else {
      this.emit('broadcast', fullMessage);
    }

    // Emit for visualization
    this.emit('messageFlow', fullMessage);
    return fullMessage.id;
  }

  getConnections(): ModuleConnection[] {
    return Array.from(this.connections.values());
  }

  getModules(): ModuleInfo[] {
    return Array.from(this.modules.values());
  }

  getRecentMessages(limit = 50): ModuleMessage[] {
    return this.messageHistory.slice(-limit);
  }

  getModuleStats(moduleId: string) {
    const module = this.modules.get(moduleId);
    if (!module) return null;

    const recentMessages = this.messageHistory.filter(
      msg => msg.sourceModuleId === moduleId && 
      Date.now() - msg.timestamp < 60000 // Last minute
    );

    return {
      ...module,
      recentMessageCount: recentMessages.length,
      averageMessageRate: recentMessages.length / 60 // per second
    };
  }
}

export const moduleCommunicationHub = new ModuleCommunicationHub(); 