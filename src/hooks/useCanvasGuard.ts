import { useEffect, useState, useRef } from 'react';

export function useCanvasGuard() {
  const [isReady, setIsReady] = useState(false);
  const mountedRef = useRef(true);

  useEffect(() => {
    // Wait for component to be fully mounted
    const initTimer = setTimeout(() => {
      if (mountedRef.current) {
        setIsReady(true);
      }
    }, 150);

    return () => {
      clearTimeout(initTimer);
      mountedRef.current = false;
      setIsReady(false);
    };
  }, []);

  return { isReady, isMounted: mountedRef.current };
}

// Canvas monitor for debugging
export function createCanvasMonitor() {
  let canvasCount = 0;
  let activeCanvases = new Set<string>();

  return {
    onCanvasCreate: (id: string) => {
      canvasCount++;
      activeCanvases.add(id);
      console.log(`Canvas ${id} created. Total: ${canvasCount}, Active: ${activeCanvases.size}`);
    },
    
    onCanvasDestroy: (id: string) => {
      activeCanvases.delete(id);
      console.log(`Canvas ${id} destroyed. Active: ${activeCanvases.size}`);
    },
    
    getStats: () => ({
      total: canvasCount,
      active: activeCanvases.size,
      activeIds: Array.from(activeCanvases)
    })
  };
}

// Global monitor instance
export const canvasMonitor = createCanvasMonitor(); 