import { useState, useEffect, useCallback, useRef } from 'react';

interface ViewportState {
  x: number;
  y: number;
  zoom: number;
}

interface ViewportControls {
  viewportState: ViewportState;
  isDragging: boolean;
  isMiddleClickDragging: boolean;
  resetViewport: () => void;
  zoomIn: () => void;
  zoomOut: () => void;
  centerView: () => void;
  getTransformStyle: () => string;
  handleMouseDown: (event: React.MouseEvent) => void;
  handleMouseMove: (event: React.MouseEvent) => void;
  handleMouseUp: (event: React.MouseEvent) => void;
  handleWheel: (event: React.WheelEvent) => void;
  handleMiddleClick: (event: React.MouseEvent) => void;
}

interface UseViewportControlsProps {
  initialZoom?: number;
  minZoom?: number;
  maxZoom?: number;
  zoomStep?: number;
  smoothPanning?: boolean;
  onViewportChange?: (state: ViewportState) => void;
}

export const useViewportControls = ({
  initialZoom = 1,
  minZoom = 0.3,
  maxZoom = 3,
  zoomStep = 0.1,
  smoothPanning = true,
  onViewportChange
}: UseViewportControlsProps = {}): ViewportControls => {
  
  const [viewportState, setViewportState] = useState<ViewportState>({
    x: 0,
    y: 0,
    zoom: initialZoom
  });

  const [isDragging, setIsDragging] = useState(false);
  const [isMiddleClickDragging, setIsMiddleClickDragging] = useState(false);
  const [lastMousePos, setLastMousePos] = useState({ x: 0, y: 0 });
  
  const dragTypeRef = useRef<'normal' | 'middle' | null>(null);
  const viewportRef = useRef<HTMLElement | null>(null);

  // Update viewport state and notify parent
  const updateViewport = useCallback((newState: Partial<ViewportState>) => {
    setViewportState(prev => {
      const updated = { ...prev, ...newState };
      onViewportChange?.(updated);
      return updated;
    });
  }, [onViewportChange]);

  // Reset viewport to center position
  const resetViewport = useCallback(() => {
    updateViewport({ x: 0, y: 0, zoom: initialZoom });
    setIsDragging(false);
    setIsMiddleClickDragging(false);
    dragTypeRef.current = null;
  }, [initialZoom, updateViewport]);

  // Zoom functions
  const zoomIn = useCallback(() => {
    updateViewport({ 
      zoom: Math.min(maxZoom, viewportState.zoom + zoomStep) 
    });
  }, [viewportState.zoom, maxZoom, zoomStep, updateViewport]);

  const zoomOut = useCallback(() => {
    updateViewport({ 
      zoom: Math.max(minZoom, viewportState.zoom - zoomStep) 
    });
  }, [viewportState.zoom, minZoom, zoomStep, updateViewport]);

  // Center view (smooth animation)
  const centerView = useCallback(() => {
    if (smoothPanning) {
      // Smooth animation to center
      const duration = 300;
      const startX = viewportState.x;
      const startY = viewportState.y;
      const startTime = Date.now();

      const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        
        updateViewport({
          x: startX * (1 - easeProgress),
          y: startY * (1 - easeProgress)
        });

        if (progress < 1) {
          requestAnimationFrame(animate);
        }
      };

      animate();
    } else {
      updateViewport({ x: 0, y: 0 });
    }
  }, [viewportState.x, viewportState.y, smoothPanning, updateViewport]);

  // Get CSS transform style
  const getTransformStyle = useCallback(() => {
    return `translate(${viewportState.x}px, ${viewportState.y}px) scale(${viewportState.zoom})`;
  }, [viewportState.x, viewportState.y, viewportState.zoom]);

  // Mouse wheel handling (zoom and pan)
  const handleWheel = useCallback((event: React.WheelEvent) => {
    event.preventDefault();
    
    const rect = event.currentTarget.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    if (event.ctrlKey || event.metaKey) {
      // Zoom with Ctrl/Cmd + wheel
      const delta = -event.deltaY * 0.001;
      const newZoom = Math.max(minZoom, Math.min(maxZoom, viewportState.zoom + delta));
      
      // Zoom towards mouse position
      const zoomFactor = newZoom / viewportState.zoom;
      const newX = viewportState.x - (mouseX - viewportState.x) * (zoomFactor - 1);
      const newY = viewportState.y - (mouseY - viewportState.y) * (zoomFactor - 1);
      
      updateViewport({ x: newX, y: newY, zoom: newZoom });
    } else {
      // Pan with wheel
      const deltaX = event.deltaX;
      const deltaY = event.deltaY;
      
      updateViewport({
        x: viewportState.x - deltaX * 0.5,
        y: viewportState.y - deltaY * 0.5
      });
    }
  }, [viewportState, minZoom, maxZoom, updateViewport]);

  // Mouse down handling
  const handleMouseDown = useCallback((event: React.MouseEvent) => {
    // Ignore if clicking on interactive elements
    const target = event.target as HTMLElement;
    if (target.closest('button') || target.closest('[data-panel-id]') || target.closest('.panel-controls')) {
      return;
    }

    const isMiddleClick = event.button === 1;
    const isLeftClick = event.button === 0;

    if (isMiddleClick || (isLeftClick && event.shiftKey)) {
      // Middle click or Shift+Left click for panning
      event.preventDefault();
      setIsMiddleClickDragging(true);
      dragTypeRef.current = 'middle';
      document.body.style.cursor = 'grab';
    } else if (isLeftClick) {
      // Regular left click drag
      setIsDragging(true);
      dragTypeRef.current = 'normal';
      document.body.style.cursor = 'grabbing';
    }

    setLastMousePos({ x: event.clientX, y: event.clientY });
    
    // Add document-level event listeners
    document.addEventListener('mousemove', handleDocumentMouseMove);
    document.addEventListener('mouseup', handleDocumentMouseUp);
  }, []);

  // Mouse move handling (document level)
  const handleDocumentMouseMove = useCallback((event: MouseEvent) => {
    if (!isDragging && !isMiddleClickDragging) return;

    const deltaX = event.clientX - lastMousePos.x;
    const deltaY = event.clientY - lastMousePos.y;

    updateViewport({
      x: viewportState.x + deltaX,
      y: viewportState.y + deltaY
    });

    setLastMousePos({ x: event.clientX, y: event.clientY });
  }, [isDragging, isMiddleClickDragging, lastMousePos, viewportState, updateViewport]);

  // Mouse up handling (document level)
  const handleDocumentMouseUp = useCallback(() => {
    setIsDragging(false);
    setIsMiddleClickDragging(false);
    dragTypeRef.current = null;
    document.body.style.cursor = 'default';
    
    // Remove document-level event listeners
    document.removeEventListener('mousemove', handleDocumentMouseMove);
    document.removeEventListener('mouseup', handleDocumentMouseUp);
  }, [handleDocumentMouseMove]);

  // Component mouse handlers (for React events)
  const handleMouseMove = useCallback((event: React.MouseEvent) => {
    // This is handled by document-level events for better performance
  }, []);

  const handleMouseUp = useCallback((event: React.MouseEvent) => {
    // This is handled by document-level events
  }, []);

  const handleMiddleClick = useCallback((event: React.MouseEvent) => {
    if (event.button === 1) {
      event.preventDefault();
      // Middle click handling is done in handleMouseDown
    }
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.target !== document.body) return; // Only when not in input fields

      switch (event.code) {
        case 'Equal':
        case 'NumpadAdd':
          if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            zoomIn();
          }
          break;
        case 'Minus':
        case 'NumpadSubtract':
          if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            zoomOut();
          }
          break;
        case 'Digit0':
        case 'Numpad0':
          if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            resetViewport();
          }
          break;
        case 'KeyC':
          if (event.ctrlKey || event.metaKey) {
            event.preventDefault();
            centerView();
          }
          break;
        case 'ArrowUp':
          if (event.shiftKey) {
            event.preventDefault();
            updateViewport({ y: viewportState.y + 50 });
          }
          break;
        case 'ArrowDown':
          if (event.shiftKey) {
            event.preventDefault();
            updateViewport({ y: viewportState.y - 50 });
          }
          break;
        case 'ArrowLeft':
          if (event.shiftKey) {
            event.preventDefault();
            updateViewport({ x: viewportState.x + 50 });
          }
          break;
        case 'ArrowRight':
          if (event.shiftKey) {
            event.preventDefault();
            updateViewport({ x: viewportState.x - 50 });
          }
          break;
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [zoomIn, zoomOut, resetViewport, centerView, viewportState, updateViewport]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      document.removeEventListener('mousemove', handleDocumentMouseMove);
      document.removeEventListener('mouseup', handleDocumentMouseUp);
      document.body.style.cursor = 'default';
    };
  }, [handleDocumentMouseMove, handleDocumentMouseUp]);

  return {
    viewportState,
    isDragging,
    isMiddleClickDragging,
    resetViewport,
    zoomIn,
    zoomOut,
    centerView,
    getTransformStyle,
    handleMouseDown,
    handleMouseMove,
    handleMouseUp,
    handleWheel,
    handleMiddleClick
  };
}; 