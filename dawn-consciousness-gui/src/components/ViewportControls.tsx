import React from 'react';
import './ViewportControls.css';

interface ViewportControlsProps {
  viewportState: {
    x: number;
    y: number;
    zoom: number;
  };
  isDragging: boolean;
  isMiddleClickDragging: boolean;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onReset: () => void;
  onCenter: () => void;
}

export const ViewportControls: React.FC<ViewportControlsProps> = ({
  viewportState,
  isDragging,
  isMiddleClickDragging,
  onZoomIn,
  onZoomOut,
  onReset,
  onCenter
}) => {
  const { x, y, zoom } = viewportState;

  return (
    <div className="viewport-controls">
      {/* Status Display */}
      <div className="viewport-status">
        <div className="status-group">
          <div className="status-label">Position</div>
          <div className="status-value">
            {Math.round(x)}, {Math.round(y)}
          </div>
        </div>
        
        <div className="status-group">
          <div className="status-label">Zoom</div>
          <div className="status-value">
            {Math.round(zoom * 100)}%
          </div>
        </div>
        
        <div className="status-group">
          <div className="status-label">Mode</div>
          <div className={`status-value ${isDragging || isMiddleClickDragging ? 'active' : ''}`}>
            {isDragging && '🖱️ Dragging'}
            {isMiddleClickDragging && '🖲️ Panning'}
            {!isDragging && !isMiddleClickDragging && '🎯 Ready'}
          </div>
        </div>
      </div>

      {/* Navigation Controls */}
      <div className="viewport-buttons">
        <div className="button-group">
          <button 
            className="viewport-btn zoom-btn"
            onClick={onZoomIn}
            title="Zoom In (Ctrl/Cmd + '+' or Ctrl/Cmd + Scroll)"
          >
            🔍+
          </button>
          
          <button 
            className="viewport-btn zoom-btn"
            onClick={onZoomOut}
            title="Zoom Out (Ctrl/Cmd + '-' or Ctrl/Cmd + Scroll)"
          >
            🔍−
          </button>
        </div>

        <div className="button-group">
          <button 
            className="viewport-btn center-btn"
            onClick={onCenter}
            title="Center View (Ctrl/Cmd + C)"
          >
            🎯
          </button>
          
          <button 
            className="viewport-btn reset-btn"
            onClick={onReset}
            title="Reset View (Ctrl/Cmd + 0)"
          >
            ↺
          </button>
        </div>
      </div>

      {/* Help Text */}
      <div className="viewport-help">
        <div className="help-text">
          🖱️ <strong>Left Click + Drag:</strong> Pan view
        </div>
        <div className="help-text">
          🖲️ <strong>Middle Click + Drag:</strong> Pan view
        </div>
        <div className="help-text">
          🔄 <strong>Ctrl/Cmd + Scroll:</strong> Zoom to mouse
        </div>
        <div className="help-text">
          📜 <strong>Scroll:</strong> Pan view
        </div>
        <div className="help-text">
          ⇧ <strong>Shift + Arrows:</strong> Pan by steps
        </div>
      </div>


    </div>
  );
}; 