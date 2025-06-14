import { useEffect, useRef, useCallback } from 'react';

export function useAnimationFrame(callback: (time: number) => void) {
  const requestRef = useRef<number>();
  const startTimeRef = useRef<number>();
  
  const animate = useCallback((time: number) => {
    if (!startTimeRef.current) {
      startTimeRef.current = time;
    }
    
    callback(time - startTimeRef.current);
    requestRef.current = requestAnimationFrame(animate);
  }, [callback]);
  
  useEffect(() => {
    requestRef.current = requestAnimationFrame(animate);
    
    return () => {
      if (requestRef.current) {
        cancelAnimationFrame(requestRef.current);
      }
    };
  }, [animate]);
} 