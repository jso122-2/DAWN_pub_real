import { useEffect, useRef, useCallback } from 'react';

interface CanvasMetrics {
  renderTime: number;
  frameCount: number;
  memoryUsage: number;
  isHealthy: boolean;
}

interface CanvasGuardConfig {
  maxRenderTime?: number;
  maxFrameCount?: number;
  memoryThreshold?: number;
  cleanupInterval?: number;
}

class CanvasMonitor {
  private canvases = new Map<string, CanvasMetrics>();
  private cleanupInterval: NodeJS.Timeout | null = null;

  startMonitoring(canvasId: string, config: CanvasGuardConfig = {}) {
    const {
      maxRenderTime = 16, // 60fps target
      maxFrameCount = 10000,
      memoryThreshold = 100 * 1024 * 1024, // 100MB
      cleanupInterval = 30000 // 30 seconds
    } = config;

    this.canvases.set(canvasId, {
      renderTime: 0,
      frameCount: 0,
      memoryUsage: 0,
      isHealthy: true
    });

    if (!this.cleanupInterval) {
      this.cleanupInterval = setInterval(() => {
        this.performCleanup();
      }, cleanupInterval);
    }
  }

  stopMonitoring(canvasId: string) {
    this.canvases.delete(canvasId);
    
    if (this.canvases.size === 0 && this.cleanupInterval) {
      clearInterval(this.cleanupInterval);
      this.cleanupInterval = null;
    }
  }

  updateMetrics(canvasId: string, metrics: Partial<CanvasMetrics>) {
    const current = this.canvases.get(canvasId);
    if (current) {
      this.canvases.set(canvasId, { ...current, ...metrics });
    }
  }

  getMetrics(canvasId: string): CanvasMetrics | null {
    return this.canvases.get(canvasId) || null;
  }

  private performCleanup() {
    // Perform memory cleanup for unhealthy canvases
    this.canvases.forEach((metrics, canvasId) => {
      if (!metrics.isHealthy) {
        console.warn(`Canvas ${canvasId} is unhealthy, performing cleanup`);
        // Reset frame count
        this.updateMetrics(canvasId, { frameCount: 0, isHealthy: true });
      }
    });

    // Force garbage collection if available
    if (window.gc) {
      window.gc();
    }
  }

  getAllMetrics(): Map<string, CanvasMetrics> {
    return new Map(this.canvases);
  }
}

export const canvasMonitor = new CanvasMonitor();

export interface UseCanvasGuardReturn {
  canvasRef: React.RefObject<HTMLCanvasElement>;
  isHealthy: boolean;
  metrics: CanvasMetrics | null;
  cleanup: () => void;
  updateMetrics: (metrics: Partial<CanvasMetrics>) => void;
}

export function useCanvasGuard(
  canvasId: string,
  config: CanvasGuardConfig = {}
): UseCanvasGuardReturn {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const metricsRef = useRef<CanvasMetrics | null>(null);

  useEffect(() => {
    canvasMonitor.startMonitoring(canvasId, config);
    
    return () => {
      canvasMonitor.stopMonitoring(canvasId);
    };
  }, [canvasId, config]);

  const cleanup = useCallback(() => {
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      if (ctx) {
        ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      }
      
      // Clear WebGL context if it exists
      const gl = canvasRef.current.getContext('webgl') || canvasRef.current.getContext('webgl2');
      if (gl) {
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      }
    }
    
    canvasMonitor.updateMetrics(canvasId, { frameCount: 0, isHealthy: true });
  }, [canvasId]);

  const updateMetrics = useCallback((metrics: Partial<CanvasMetrics>) => {
    canvasMonitor.updateMetrics(canvasId, metrics);
    metricsRef.current = canvasMonitor.getMetrics(canvasId);
  }, [canvasId]);

  // Get current metrics
  const currentMetrics = canvasMonitor.getMetrics(canvasId);
  const isHealthy = currentMetrics?.isHealthy ?? true;

  return {
    canvasRef,
    isHealthy,
    metrics: currentMetrics,
    cleanup,
    updateMetrics
  };
} 