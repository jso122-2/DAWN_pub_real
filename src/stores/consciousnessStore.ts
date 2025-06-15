import { create } from 'zustand';
import { TickData } from '../services/WebSocketService';

interface ConsciousnessState {
  // Current state
  tickData: TickData | null;
  isConnected: boolean;  
  connectionState: 'connecting' | 'connected' | 'disconnected' | 'error';
  
  // History
  history: TickData[];
  maxHistory: number;
  
  // Derived values
  averageScup: number;
  peakScup: number;
  minScup: number;
  currentTrend: 'rising' | 'falling' | 'stable';
  moodHistory: string[];
  entropyTrend: 'increasing' | 'decreasing' | 'stable';
  
  // Performance metrics
  tickRate: number;
  uptime: number;
  totalTicks: number;
  
  // Actions
  updateTickData: (data: TickData) => void;
  setConnectionState: (state: 'connecting' | 'connected' | 'disconnected' | 'error') => void;
  clearHistory: () => void;
  getRecentHistory: (count: number) => TickData[];
  getScupTrend: () => number[];
  getEntropyTrend: () => number[];
  calculateCorrelation: (metric1: keyof TickData, metric2: keyof TickData) => number;
}

export const useConsciousnessStore = create<ConsciousnessState>((set, get) => ({
  // Initial state
  tickData: null,
  isConnected: false,
  connectionState: 'disconnected',
  history: [],
  maxHistory: 1000,
  averageScup: 0,
  peakScup: 0,
  minScup: 1,
  currentTrend: 'stable',
  moodHistory: [],
  entropyTrend: 'stable',
  tickRate: 0,
  uptime: 0,
  totalTicks: 0,
  
  updateTickData: (data) => set((state) => {
    const newHistory = [...state.history, data].slice(-state.maxHistory);
    const totalTicks = state.totalTicks + 1;
    
    // Calculate SCUP metrics
    const scupValues = newHistory.map(d => d.scup);
    const averageScup = scupValues.reduce((sum, val) => sum + val, 0) / scupValues.length;
    const peakScup = Math.max(...scupValues);
    const minScup = Math.min(...scupValues);
    
    // Calculate SCUP trend
    let currentTrend: 'rising' | 'falling' | 'stable' = 'stable';
    if (newHistory.length > 20) {
      const recent = scupValues.slice(-10);
      const older = scupValues.slice(-20, -10);
      const recentAvg = recent.reduce((sum, val) => sum + val, 0) / recent.length;
      const olderAvg = older.reduce((sum, val) => sum + val, 0) / older.length;
      
      const threshold = 0.02; // 2% change threshold
      if (recentAvg > olderAvg + threshold) currentTrend = 'rising';
      else if (recentAvg < olderAvg - threshold) currentTrend = 'falling';
    }
    
    // Calculate entropy trend
    let entropyTrend: 'increasing' | 'decreasing' | 'stable' = 'stable';
    if (newHistory.length > 10) {
      const entropyValues = newHistory.slice(-10).map(d => d.entropy);
      const entropySlope = entropyValues.reduce((sum, val, idx) => sum + (val * (idx + 1)), 0) - 
                          (entropyValues.reduce((sum, val) => sum + val, 0) * 5.5);
      
      if (entropySlope > 0.1) entropyTrend = 'increasing';
      else if (entropySlope < -0.1) entropyTrend = 'decreasing';
    }
    
    // Update mood history
    const moodHistory = [...state.moodHistory, data.mood].slice(-50);
    
    // Calculate tick rate (ticks per second over last 10 ticks)
    let tickRate = 0;
    if (newHistory.length > 10) {
      const recentTicks = newHistory.slice(-10);
      const timeSpan = recentTicks[recentTicks.length - 1].timestamp - recentTicks[0].timestamp;
      tickRate = timeSpan > 0 ? (recentTicks.length - 1) / (timeSpan / 1000) : 0;
    }
    
    return {
      tickData: data,
      history: newHistory,
      averageScup,
      peakScup,
      minScup,
      currentTrend,
      entropyTrend,
      moodHistory,
      tickRate,
      totalTicks,
      isConnected: true,
      connectionState: 'connected' as const
    };
  }),
  
  setConnectionState: (connectionState) => set((state) => ({
    connectionState,
    isConnected: connectionState === 'connected'
  })),
  
  clearHistory: () => set({ 
    history: [], 
    averageScup: 0, 
    peakScup: 0, 
    minScup: 1, 
    moodHistory: [],
    totalTicks: 0
  }),
  
  getRecentHistory: (count) => {
    const state = get();
    return state.history.slice(-count);
  },
  
  getScupTrend: () => {
    const state = get();
    return state.history.slice(-50).map(d => d.scup);
  },
  
  getEntropyTrend: () => {
    const state = get();
    return state.history.slice(-50).map(d => d.entropy);
  },
  
  calculateCorrelation: (metric1, metric2) => {
    const state = get();
    const data = state.history.slice(-100);
    
    if (data.length < 10) return 0;
    
    const values1 = data.map(d => Number(d[metric1]));
    const values2 = data.map(d => Number(d[metric2]));
    
    const mean1 = values1.reduce((sum, val) => sum + val, 0) / values1.length;
    const mean2 = values2.reduce((sum, val) => sum + val, 0) / values2.length;
    
    let numerator = 0;
    let denominator1 = 0;
    let denominator2 = 0;
    
    for (let i = 0; i < values1.length; i++) {
      const diff1 = values1[i] - mean1;
      const diff2 = values2[i] - mean2;
      
      numerator += diff1 * diff2;
      denominator1 += diff1 * diff1;
      denominator2 += diff2 * diff2;
    }
    
    const correlation = numerator / Math.sqrt(denominator1 * denominator2);
    return isNaN(correlation) ? 0 : correlation;
  }
})); 