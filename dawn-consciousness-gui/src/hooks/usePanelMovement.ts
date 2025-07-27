import { useState, useRef, useCallback } from 'react';

// Types for drag and drop functionality
interface DragState {
  isDragging: boolean;
  draggedPanelId: string | null;
  dragOffset: { x: number; y: number };
  startPosition: { x: number; y: number };
}

interface PanelPosition {
  id: string;
  column: 'cognition' | 'symbolic' | 'reflection';
  order: number;
}

interface UsePanelMovementProps {
  onPanelMove?: (panelId: string, newColumn: string, newOrder: number) => void;
  initialPositions?: PanelPosition[];
}

export const usePanelMovement = ({ onPanelMove, initialPositions = [] }: UsePanelMovementProps = {}) => {
  const [dragState, setDragState] = useState<DragState>({
    isDragging: false,
    draggedPanelId: null,
    dragOffset: { x: 0, y: 0 },
    startPosition: { x: 0, y: 0 }
  });

  const [panelPositions, setPanelPositions] = useState<PanelPosition[]>(initialPositions);
  const dragRef = useRef<HTMLElement | null>(null);

  // Start dragging a panel
  const startDrag = useCallback((
    panelId: string, 
    event: React.MouseEvent | React.TouchEvent
  ) => {
    event.preventDefault();
    
    const clientX = 'touches' in event ? event.touches[0].clientX : event.clientX;
    const clientY = 'touches' in event ? event.touches[0].clientY : event.clientY;

    setDragState({
      isDragging: true,
      draggedPanelId: panelId,
      dragOffset: { x: 0, y: 0 },
      startPosition: { x: clientX, y: clientY }
    });

    // Add visual feedback
    document.body.style.cursor = 'grabbing';
    document.body.style.userSelect = 'none';
  }, []);

  // Handle drag movement
  const onDrag = useCallback((event: MouseEvent | TouchEvent) => {
    if (!dragState.isDragging || !dragState.draggedPanelId) return;

    const clientX = 'touches' in event ? event.touches[0].clientX : event.clientX;
    const clientY = 'touches' in event ? event.touches[0].clientY : event.clientY;

    const newOffset = {
      x: clientX - dragState.startPosition.x,
      y: clientY - dragState.startPosition.y
    };

    setDragState(prev => ({
      ...prev,
      dragOffset: newOffset
    }));
  }, [dragState.isDragging, dragState.startPosition]);

  // End dragging
  const endDrag = useCallback(() => {
    if (!dragState.isDragging) return;

    // Reset cursor and selection
    document.body.style.cursor = '';
    document.body.style.userSelect = '';

    // Determine drop zone and new position
    const draggedElement = document.querySelector(`[data-panel-id="${dragState.draggedPanelId}"]`);
    if (draggedElement) {
      const rect = draggedElement.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2 + dragState.dragOffset.x;
      const centerY = rect.top + rect.height / 2 + dragState.dragOffset.y;
      
      // Find the column and position to drop
      const dropTarget = getDropTarget(centerX, centerY);
      
      if (dropTarget && onPanelMove) {
        onPanelMove(dragState.draggedPanelId!, dropTarget.column, dropTarget.order);
      }
    }

    setDragState({
      isDragging: false,
      draggedPanelId: null,
      dragOffset: { x: 0, y: 0 },
      startPosition: { x: 0, y: 0 }
    });
  }, [dragState, onPanelMove]);

  // Helper function to determine drop target
  const getDropTarget = (x: number, y: number) => {
    const columns = document.querySelectorAll('[data-column]');
    
    for (const column of columns) {
      const rect = column.getBoundingClientRect();
      if (x >= rect.left && x <= rect.right && y >= rect.top && y <= rect.bottom) {
        const columnName = column.getAttribute('data-column');
        const panels = column.querySelectorAll('[data-panel-id]');
        
        let order = 0;
        for (const panel of panels) {
          const panelRect = panel.getBoundingClientRect();
          if (y < panelRect.top + panelRect.height / 2) {
            break;
          }
          order++;
        }
        
        return {
          column: columnName || 'cognition',
          order
        };
      }
    }
    
    return null;
  };

  // Get drag styles for a panel
  const getDragStyles = useCallback((panelId: string) => {
    if (dragState.draggedPanelId !== panelId) {
      return {};
    }

    return {
      transform: `translate(${dragState.dragOffset.x}px, ${dragState.dragOffset.y}px)`,
      zIndex: 1000,
      opacity: 0.8,
      transition: dragState.isDragging ? 'none' : 'transform 0.2s ease, opacity 0.2s ease',
      boxShadow: dragState.isDragging ? '0 10px 30px rgba(64, 224, 255, 0.3)' : 'none'
    };
  }, [dragState]);

  // Check if a panel is being dragged
  const isPanelDragging = useCallback((panelId: string) => {
    return dragState.isDragging && dragState.draggedPanelId === panelId;
  }, [dragState]);

  // Get drop zone styles
  const getDropZoneStyles = useCallback((column: string) => {
    if (!dragState.isDragging) return {};

    return {
      background: 'rgba(64, 224, 255, 0.1)',
      border: '2px dashed rgba(64, 224, 255, 0.3)',
      borderRadius: '8px'
    };
  }, [dragState.isDragging]);

  return {
    // State
    dragState,
    panelPositions,
    
    // Actions
    startDrag,
    onDrag,
    endDrag,
    
    // Helpers
    getDragStyles,
    isPanelDragging,
    getDropZoneStyles,
    
    // Update positions
    setPanelPositions
  };
};

// Hook for keyboard navigation between panels
export const usePanelNavigation = () => {
  const [focusedPanelId, setFocusedPanelId] = useState<string | null>(null);

  const moveFocus = useCallback((direction: 'up' | 'down' | 'left' | 'right') => {
    const panels = document.querySelectorAll('[data-panel-id]');
    const panelArray = Array.from(panels) as HTMLElement[];
    
    if (panelArray.length === 0) return;

    const currentIndex = focusedPanelId 
      ? panelArray.findIndex(p => p.getAttribute('data-panel-id') === focusedPanelId)
      : -1;

    let newIndex = currentIndex;

    switch (direction) {
      case 'up':
        newIndex = currentIndex > 0 ? currentIndex - 1 : panelArray.length - 1;
        break;
      case 'down':
        newIndex = currentIndex < panelArray.length - 1 ? currentIndex + 1 : 0;
        break;
      case 'left':
        // Move to previous column
        newIndex = Math.max(0, currentIndex - 3);
        break;
      case 'right':
        // Move to next column
        newIndex = Math.min(panelArray.length - 1, currentIndex + 3);
        break;
    }

    const newFocusedPanel = panelArray[newIndex];
    if (newFocusedPanel) {
      const newPanelId = newFocusedPanel.getAttribute('data-panel-id');
      setFocusedPanelId(newPanelId);
      newFocusedPanel.focus();
    }
  }, [focusedPanelId]);

  const getFocusStyles = useCallback((panelId: string) => {
    if (focusedPanelId !== panelId) return {};

    return {
      outline: '2px solid rgba(64, 224, 255, 0.6)',
      outlineOffset: '2px'
    };
  }, [focusedPanelId]);

  return {
    focusedPanelId,
    setFocusedPanelId,
    moveFocus,
    getFocusStyles
  };
};

export default usePanelMovement; 