import { TickData, ConversationMessage, VisualizationData } from '../services/WebSocketService';

export interface ConsciousnessState {
  currentTick: TickData | null;
  tickHistory: TickData[];
  conversationHistory: ConversationMessage[];
  visualizations: VisualizationData[];
  isConnected: boolean;
  connectionStatus: string;
  lastUpdate: number;
}

class ConsciousnessStore {
  private state: ConsciousnessState = {
    currentTick: null,
    tickHistory: [],
    conversationHistory: [],
    visualizations: [],
    isConnected: false,
    connectionStatus: 'Disconnected',
    lastUpdate: Date.now()
  };

  private subscribers: Set<(state: ConsciousnessState) => void> = new Set();

  // Getters
  getCurrentTick(): TickData | null {
    return this.state.currentTick;
  }

  getTickHistory(): TickData[] {
    return this.state.tickHistory;
  }

  getConversationHistory(): ConversationMessage[] {
    return this.state.conversationHistory;
  }

  getVisualizations(): VisualizationData[] {
    return this.state.visualizations;
  }

  getConnectionStatus(): { isConnected: boolean; status: string } {
    return {
      isConnected: this.state.isConnected,
      status: this.state.connectionStatus
    };
  }

  getLastUpdate(): number {
    return this.state.lastUpdate;
  }

  // State updates
  updateTickData(tickData: TickData): void {
    this.state.currentTick = tickData;
    this.state.tickHistory.push(tickData);
    
    // Keep only last 1000 ticks
    if (this.state.tickHistory.length > 1000) {
      this.state.tickHistory = this.state.tickHistory.slice(-1000);
    }
    
    this.state.lastUpdate = Date.now();
    this.notifySubscribers();
  }

  addConversationMessage(message: ConversationMessage): void {
    this.state.conversationHistory.push(message);
    
    // Keep only last 100 messages
    if (this.state.conversationHistory.length > 100) {
      this.state.conversationHistory = this.state.conversationHistory.slice(-100);
    }
    
    this.notifySubscribers();
  }

  addVisualization(visualization: VisualizationData): void {
    this.state.visualizations.push(visualization);
    
    // Keep only last 50 visualizations
    if (this.state.visualizations.length > 50) {
      this.state.visualizations = this.state.visualizations.slice(-50);
    }
    
    this.notifySubscribers();
  }

  updateConnectionStatus(isConnected: boolean, status: string): void {
    this.state.isConnected = isConnected;
    this.state.connectionStatus = status;
    this.notifySubscribers();
  }

  // Analytics methods
  getAverageScup(): number {
    if (this.state.tickHistory.length === 0) return 0;
    const sum = this.state.tickHistory.reduce((acc, tick) => acc + tick.scup, 0);
    return sum / this.state.tickHistory.length;
  }

  getAverageEntropy(): number {
    if (this.state.tickHistory.length === 0) return 0;
    const sum = this.state.tickHistory.reduce((acc, tick) => acc + tick.entropy, 0);
    return sum / this.state.tickHistory.length;
  }

  getCurrentTrend(): 'rising' | 'falling' | 'stable' {
    if (this.state.tickHistory.length < 10) return 'stable';
    
    const recent = this.state.tickHistory.slice(-10);
    const firstHalf = recent.slice(0, 5);
    const secondHalf = recent.slice(5);
    
    const firstAvg = firstHalf.reduce((acc, tick) => acc + tick.scup, 0) / firstHalf.length;
    const secondAvg = secondHalf.reduce((acc, tick) => acc + tick.scup, 0) / secondHalf.length;
    
    const diff = secondAvg - firstAvg;
    if (Math.abs(diff) < 0.05) return 'stable';
    return diff > 0 ? 'rising' : 'falling';
  }

  getTotalTicks(): number {
    return this.state.tickHistory.length;
  }

  getTickRate(): number {
    if (this.state.tickHistory.length < 2) return 0;
    const firstTick = this.state.tickHistory[0];
    const lastTick = this.state.tickHistory[this.state.tickHistory.length - 1];
    const timeSpan = (lastTick.timestamp - firstTick.timestamp) / 1000; // seconds
    return this.state.tickHistory.length / timeSpan;
  }

  // Subscription management
  subscribe(callback: (state: ConsciousnessState) => void): () => void {
    this.subscribers.add(callback);
    return () => {
      this.subscribers.delete(callback);
    };
  }

  private notifySubscribers(): void {
    this.subscribers.forEach(callback => {
      try {
        callback({ ...this.state });
      } catch (error) {
        console.error('Error in consciousness store subscriber:', error);
      }
    });
  }

  // Utility methods
  clearHistory(): void {
    this.state.tickHistory = [];
    this.state.conversationHistory = [];
    this.state.visualizations = [];
    this.notifySubscribers();
  }

  getRecentTicks(count: number = 50): TickData[] {
    return this.state.tickHistory.slice(-count);
  }

  getRecentMessages(count: number = 20): ConversationMessage[] {
    return this.state.conversationHistory.slice(-count);
  }
}

export default ConsciousnessStore; 