import React, { useState, useRef, useEffect } from 'react';
import { Colors, Spacing } from '../theme/theme_tokens';

interface DraggablePanelProps {
  id: string;
  title: string;
  isLive?: boolean;
  size?: 'small' | 'medium' | 'large';
  onToggle?: () => void;
  onExport?: () => void;
  onSnapshot?: () => void;
  children: React.ReactNode;
  onMove?: (panelId: string, newX: number, newY: number) => void;
}

export const DraggablePanel: React.FC<DraggablePanelProps> = ({
  id,
  title,
  isLive = false,
  size = 'medium',
  onToggle,
  onExport,
  onSnapshot,
  children,
  onMove
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const panelRef = useRef<HTMLDivElement>(null);
  const startPosRef = useRef({ x: 0, y: 0 });

  const handleMouseDown = (e: React.MouseEvent) => {
    if (!panelRef.current) return;
    
    const rect = panelRef.current.getBoundingClientRect();
    startPosRef.current = {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
    
    setIsDragging(true);
    e.preventDefault();
    e.stopPropagation(); // Prevent viewport dragging when dragging panels
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (!isDragging) return;
    
    const newX = e.clientX - startPosRef.current.x;
    const newY = e.clientY - startPosRef.current.y;
    
    setPosition({ x: newX, y: newY });
    setDragOffset({ x: newX, y: newY });
  };

  const handleMouseUp = () => {
    if (!isDragging) return;
    
    setIsDragging(false);
    
    if (onMove) {
      onMove(id, position.x, position.y);
    }
  };

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = 'grabbing';
      document.body.style.userSelect = 'none';
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
  }, [isDragging]);

  const panelStyle: React.CSSProperties = {
    position: isDragging ? 'fixed' : 'relative',
    left: isDragging ? position.x : 'auto',
    top: isDragging ? position.y : 'auto',
    zIndex: isDragging ? 1000 : 'auto',
    transform: isDragging ? 'none' : 'none',
    opacity: isDragging ? 0.8 : 1,
    cursor: isDragging ? 'grabbing' : 'grab',
    transition: isDragging ? 'none' : 'all 0.2s ease',
    boxShadow: isDragging ? '0 10px 30px rgba(64, 224, 255, 0.4)' : 'none',
    border: isDragging ? `2px solid ${Colors.textAccent}` : `1px solid ${Colors.backgroundTertiary}`,
    background: isDragging ? 'rgba(64, 224, 255, 0.1)' : Colors.backgroundPanel,
    borderRadius: '8px',
    backdropFilter: 'blur(10px)',
    display: 'flex',
    flexDirection: 'column' as const,
    minHeight: 0,
    flex: size === 'large' ? 2 : size === 'medium' ? 1.5 : 1
  };

  const headerStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: `12px ${Spacing.panelPadding}`,
    borderBottom: `1px solid ${Colors.backgroundTertiary}`,
    background: Colors.backgroundHeader,
    borderRadius: '8px 8px 0 0',
    cursor: 'grab',
    userSelect: 'none'
  };

  return (
    <div 
      ref={panelRef}
      style={panelStyle}
      data-panel-id={id}
    >
      <div 
        style={headerStyle}
        onMouseDown={handleMouseDown}
      >
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          fontSize: '12px',
          fontWeight: 600,
          color: Colors.textPrimary,
          textTransform: 'uppercase' as const,
          letterSpacing: '0.5px'
        }}>
                     <span style={{
             color: Colors.textFaint,
             fontSize: '10px',
             opacity: 0.7,
             padding: '2px'
           }}>
             ⋮⋮
           </span>
          {title}
        </div>
        
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px'
        }}>
          <div style={{
            width: '6px',
            height: '6px',
            borderRadius: '50%',
                         background: isLive ? Colors.connected : Colors.textFaint,
            animation: isLive ? 'pulse 2s ease-in-out infinite' : 'none'
          }} />
          
          <div style={{ display: 'flex', gap: '4px' }}>
            {onToggle && (
              <button 
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: Colors.textFaint,
                  padding: '4px',
                  borderRadius: '3px',
                  cursor: 'pointer',
                  fontSize: '10px'
                }}
                onClick={onToggle}
                onMouseDown={(e) => e.stopPropagation()}
              >
                ⏸
              </button>
            )}
            {onExport && (
              <button 
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: Colors.textFaint,
                  padding: '4px',
                  borderRadius: '3px',
                  cursor: 'pointer',
                  fontSize: '10px'
                }}
                onClick={onExport}
                onMouseDown={(e) => e.stopPropagation()}
              >
                ↗
              </button>
            )}
            {onSnapshot && (
              <button 
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: Colors.textFaint,
                  padding: '4px',
                  borderRadius: '3px',
                  cursor: 'pointer',
                  fontSize: '10px'
                }}
                onClick={onSnapshot}
                onMouseDown={(e) => e.stopPropagation()}
              >
                📸
              </button>
            )}
          </div>
        </div>
      </div>
      
      <div style={{
        flex: 1,
        padding: Spacing.panelPadding,
        overflowY: 'auto' as const,
        minHeight: 0
      }}>
        {children}
      </div>
      
      {/* Add pulse animation */}
      <style>
        {`
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
          }
        `}
      </style>
    </div>
  );
};

export default DraggablePanel; 