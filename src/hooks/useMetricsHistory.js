import { useState, useEffect } from 'react';

export function useMetricsHistory(tickData, maxHistory = 100) {
  const [history, setHistory] = useState([]);
  
  useEffect(() => {
    if (tickData) {
      setHistory(prev => {
        const newHistory = [...prev, {
          timestamp: Date.now(),
          scup: tickData.scup,
          entropy: tickData.entropy,
          heat: tickData.heat,
          mood: tickData.mood
        }];
        
        // Keep only last N entries
        return newHistory.slice(-maxHistory);
      });
    }
  }, [tickData, maxHistory]);
  
  // Calculate trends
  const calculateTrend = (metric) => {
    if (history.length < 10) return 'stable';
    
    const recent = history.slice(-10);
    const older = history.slice(-20, -10);
    
    if (older.length === 0) return 'stable';
    
    const recentAvg = recent.reduce((sum, h) => sum + h[metric], 0) / recent.length;
    const olderAvg = older.reduce((sum, h) => sum + h[metric], 0) / older.length;
    
    if (recentAvg > olderAvg + 0.05) return 'rising';
    if (recentAvg < olderAvg - 0.05) return 'falling';
    return 'stable';
  };
  
  // Calculate moving average for smoothing
  const calculateMovingAverage = (metric, windowSize = 10) => {
    if (history.length < windowSize) return [];
    
    const result = [];
    for (let i = windowSize - 1; i < history.length; i++) {
      const window = history.slice(i - windowSize + 1, i + 1);
      const average = window.reduce((sum, h) => sum + h[metric], 0) / windowSize;
      result.push({
        timestamp: history[i].timestamp,
        value: average
      });
    }
    return result;
  };
  
  // Calculate volatility (standard deviation)
  const calculateVolatility = (metric, windowSize = 20) => {
    if (history.length < windowSize) return 0;
    
    const recent = history.slice(-windowSize);
    const values = recent.map(h => h[metric]);
    const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
    const squaredDiffs = values.map(val => Math.pow(val - mean, 2));
    const variance = squaredDiffs.reduce((sum, val) => sum + val, 0) / values.length;
    
    return Math.sqrt(variance);
  };
  
  // Calculate correlation between two metrics
  const calculateCorrelation = (metric1, metric2, windowSize = 50) => {
    if (history.length < windowSize) return 0;
    
    const recent = history.slice(-windowSize);
    const values1 = recent.map(h => h[metric1]);
    const values2 = recent.map(h => h[metric2]);
    
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
  };
  
  // Detect anomalies (values beyond 2 standard deviations)
  const detectAnomalies = (metric, threshold = 2) => {
    if (history.length < 30) return [];
    
    const values = history.map(h => h[metric]);
    const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
    const std = Math.sqrt(
      values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length
    );
    
    return history.filter(h => 
      Math.abs(h[metric] - mean) > threshold * std
    ).map(h => ({
      ...h,
      deviation: Math.abs(h[metric] - mean) / std,
      metric
    }));
  };
  
  // Get peak and valley points
  const findExtremes = (metric, windowSize = 5) => {
    if (history.length < windowSize * 2) return { peaks: [], valleys: [] };
    
    const peaks = [];
    const valleys = [];
    
    for (let i = windowSize; i < history.length - windowSize; i++) {
      const current = history[i][metric];
      const window = history.slice(i - windowSize, i + windowSize + 1);
      const values = window.map(h => h[metric]);
      
      const max = Math.max(...values);
      const min = Math.min(...values);
      
      if (current === max && current > values[0] && current > values[values.length - 1]) {
        peaks.push(history[i]);
      }
      
      if (current === min && current < values[0] && current < values[values.length - 1]) {
        valleys.push(history[i]);
      }
    }
    
    return { peaks, valleys };
  };
  
  // Calculate performance score based on all metrics
  const calculatePerformanceScore = () => {
    if (history.length === 0) return 0;
    
    const latest = history[history.length - 1];
    
    // Normalize metrics (assuming SCUP is 0-100, others 0-1)
    const normalizedScup = latest.scup / 100;
    const normalizedEntropy = 1 - latest.entropy; // Lower entropy is better
    const normalizedHeat = latest.heat; // Heat can be good or bad depending on context
    
    // Weighted performance score
    const score = (
      normalizedScup * 0.4 +
      normalizedEntropy * 0.3 +
      normalizedHeat * 0.3
    ) * 100;
    
    return Math.round(score);
  };
  
  return {
    history,
    trends: {
      scup: calculateTrend('scup'),
      entropy: calculateTrend('entropy'),
      heat: calculateTrend('heat')
    },
    movingAverages: {
      scup: calculateMovingAverage('scup'),
      entropy: calculateMovingAverage('entropy'),
      heat: calculateMovingAverage('heat')
    },
    volatility: {
      scup: calculateVolatility('scup'),
      entropy: calculateVolatility('entropy'),
      heat: calculateVolatility('heat')
    },
    correlations: {
      scupEntropy: calculateCorrelation('scup', 'entropy'),
      scupHeat: calculateCorrelation('scup', 'heat'),
      entropyHeat: calculateCorrelation('entropy', 'heat')
    },
    anomalies: {
      scup: detectAnomalies('scup'),
      entropy: detectAnomalies('entropy'),
      heat: detectAnomalies('heat')
    },
    extremes: {
      scup: findExtremes('scup'),
      entropy: findExtremes('entropy'),
      heat: findExtremes('heat')
    },
    performanceScore: calculatePerformanceScore(),
    
    // Utility functions
    getMetricHistory: (metric, count = 50) => {
      return history.slice(-count).map(h => ({
        timestamp: h.timestamp,
        value: h[metric]
      }));
    },
    
    getTimeRange: () => {
      if (history.length === 0) return { start: 0, end: 0, duration: 0 };
      
      const start = history[0].timestamp;
      const end = history[history.length - 1].timestamp;
      
      return {
        start,
        end,
        duration: end - start
      };
    },
    
    getMoodDistribution: () => {
      const moodCounts = {};
      history.forEach(h => {
        moodCounts[h.mood] = (moodCounts[h.mood] || 0) + 1;
      });
      
      const total = history.length;
      const distribution = {};
      
      Object.keys(moodCounts).forEach(mood => {
        distribution[mood] = {
          count: moodCounts[mood],
          percentage: (moodCounts[mood] / total) * 100
        };
      });
      
      return distribution;
    }
  };
} 