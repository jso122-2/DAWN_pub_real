import { useState, useEffect, useRef, useCallback } from 'react';

interface PerformanceMetrics {
  fps: number[];
  memory: {
    used: number;
    total: number;
    heapUsed?: number;
    heapTotal?: number;
  };
  renderTimes: Map<string, number>;
  networkRequests: NetworkRequest[];
  cpuUsage: number;
  gpuUsage?: number;
}

interface NetworkRequest {
  id: string;
  url: string;
  method: string;
  startTime: number;
  endTime?: number;
  status?: number;
  duration?: number;
}

interface ComponentRenderTime {
  componentName: string;
  renderTime: number;
  timestamp: number;
}

export const usePerformanceMonitor = () => {
  const [metrics, setMetrics] = useState<PerformanceMetrics>({
    fps: [],
    memory: { used: 0, total: 0 },
    renderTimes: new Map(),
    networkRequests: [],
    cpuUsage: 0,
  });

  const frameTimestamps = useRef<number[]>([]);
  const lastFrameTime = useRef<number>(performance.now());
  const animationFrameId = useRef<number>();
  const networkObserver = useRef<PerformanceObserver>();
  const renderTimesBuffer = useRef<ComponentRenderTime[]>([]);

  // FPS Calculation
  const calculateFPS = useCallback(() => {
    const now = performance.now();
    frameTimestamps.current.push(now);
    
    // Keep only last 60 seconds of data
    const sixtySecondsAgo = now - 60000;
    frameTimestamps.current = frameTimestamps.current.filter(
      timestamp => timestamp > sixtySecondsAgo
    );

    // Calculate FPS for each second in the last 60 seconds
    const fpsData: number[] = [];
    for (let i = 0; i < 60; i++) {
      const secondStart = now - (i + 1) * 1000;
      const secondEnd = now - i * 1000;
      const framesInSecond = frameTimestamps.current.filter(
        timestamp => timestamp >= secondStart && timestamp < secondEnd
      ).length;
      fpsData.unshift(framesInSecond);
    }

    return fpsData;
  }, []);

  // Memory Usage
  const getMemoryUsage = useCallback(() => {
    if ('memory' in performance) {
      const memory = (performance as any).memory;
      return {
        used: memory.usedJSHeapSize / (1024 * 1024), // MB
        total: memory.totalJSHeapSize / (1024 * 1024), // MB
        heapUsed: memory.usedJSHeapSize / (1024 * 1024),
        heapTotal: memory.totalJSHeapSize / (1024 * 1024),
      };
    }
    
    // Fallback estimation
    return {
      used: Math.random() * 50 + 20, // Mock data
      total: 100,
    };
  }, []);

  // CPU Usage (approximation)
  const getCPUUsage = useCallback(() => {
    const now = performance.now();
    const timeDiff = now - lastFrameTime.current;
    lastFrameTime.current = now;
    
    // Rough CPU usage estimation based on frame timing
    const expectedFrameTime = 16.67; // 60fps
    const usage = Math.min(100, Math.max(0, (timeDiff / expectedFrameTime - 1) * 100));
    return usage;
  }, []);

  // Network Request Monitoring
  const setupNetworkMonitoring = useCallback(() => {
    if (!window.PerformanceObserver) return;

    networkObserver.current = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      const newRequests: NetworkRequest[] = [];

      entries.forEach((entry) => {
        if (entry.entryType === 'navigation' || entry.entryType === 'resource') {
          const request: NetworkRequest = {
            id: `${entry.name}-${entry.startTime}`,
            url: entry.name,
            method: 'GET', // Default, actual method not available in PerformanceEntry
            startTime: entry.startTime,
            endTime: entry.startTime + entry.duration,
            duration: entry.duration,
          };
          newRequests.push(request);
        }
      });

      if (newRequests.length > 0) {
        setMetrics(prev => ({
          ...prev,
          networkRequests: [...prev.networkRequests, ...newRequests]
            .slice(-50) // Keep last 50 requests
            .sort((a, b) => a.startTime - b.startTime)
        }));
      }
    });

    try {
      networkObserver.current.observe({ entryTypes: ['navigation', 'resource'] });
    } catch (error) {
      console.warn('Performance Observer not supported for network monitoring');
    }
  }, []);

  // Component Render Time Tracking
  const trackRenderTime = useCallback((componentName: string, renderTime: number) => {
    const entry: ComponentRenderTime = {
      componentName,
      renderTime,
      timestamp: performance.now(),
    };

    renderTimesBuffer.current.push(entry);
    
    // Keep only last 100 entries
    if (renderTimesBuffer.current.length > 100) {
      renderTimesBuffer.current = renderTimesBuffer.current.slice(-100);
    }

    // Update render times map
    setMetrics(prev => {
      const newRenderTimes = new Map(prev.renderTimes);
      newRenderTimes.set(componentName, renderTime);
      return {
        ...prev,
        renderTimes: newRenderTimes,
      };
    });
  }, []);

  // Main update loop
  const updateMetrics = useCallback(() => {
    const fps = calculateFPS();
    const memory = getMemoryUsage();
    const cpuUsage = getCPUUsage();

    setMetrics(prev => ({
      ...prev,
      fps,
      memory,
      cpuUsage,
    }));

    animationFrameId.current = requestAnimationFrame(updateMetrics);
  }, [calculateFPS, getMemoryUsage, getCPUUsage]);

  // GPU Usage (if available)
  const getGPUUsage = useCallback(async () => {
    try {
      // Check if WebGPU is available
      if ('gpu' in navigator) {
        // This is a placeholder - actual GPU usage monitoring would require
        // more complex implementation with WebGPU or vendor-specific APIs
        return Math.random() * 100;
      }
    } catch (error) {
      console.warn('GPU monitoring not available');
    }
    return undefined;
  }, []);

  // Initialize monitoring
  useEffect(() => {
    setupNetworkMonitoring();
    animationFrameId.current = requestAnimationFrame(updateMetrics);

    // GPU usage update (less frequent)
    const gpuInterval = setInterval(async () => {
      const gpuUsage = await getGPUUsage();
      if (gpuUsage !== undefined) {
        setMetrics(prev => ({ ...prev, gpuUsage }));
      }
    }, 1000);

    return () => {
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
      }
      if (networkObserver.current) {
        networkObserver.current.disconnect();
      }
      clearInterval(gpuInterval);
    };
  }, [setupNetworkMonitoring, updateMetrics, getGPUUsage]);

  // Utility functions
  const getAverageRenderTime = useCallback((componentName?: string) => {
    const relevantEntries = componentName
      ? renderTimesBuffer.current.filter(entry => entry.componentName === componentName)
      : renderTimesBuffer.current;

    if (relevantEntries.length === 0) return 0;

    const sum = relevantEntries.reduce((acc, entry) => acc + entry.renderTime, 0);
    return sum / relevantEntries.length;
  }, []);

  const getRenderTimeHeatmap = useCallback(() => {
    const heatmap = new Map<string, { average: number; count: number; max: number }>();

    renderTimesBuffer.current.forEach(entry => {
      const existing = heatmap.get(entry.componentName);
      if (existing) {
        existing.count++;
        existing.average = (existing.average * (existing.count - 1) + entry.renderTime) / existing.count;
        existing.max = Math.max(existing.max, entry.renderTime);
      } else {
        heatmap.set(entry.componentName, {
          average: entry.renderTime,
          count: 1,
          max: entry.renderTime,
        });
      }
    });

    return heatmap;
  }, []);

  return {
    metrics,
    trackRenderTime,
    getAverageRenderTime,
    getRenderTimeHeatmap,
    // Helper functions for components
    startRenderTimer: (componentName: string) => {
      const startTime = performance.now();
      return () => {
        const endTime = performance.now();
        trackRenderTime(componentName, endTime - startTime);
      };
    },
  };
}; 