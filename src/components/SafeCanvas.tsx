import React, { ErrorInfo, ReactNode, Component } from 'react';

interface CanvasErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class CanvasErrorBoundary extends Component<
  { children: ReactNode; fallback?: ReactNode; id?: string },
  CanvasErrorBoundaryState
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): CanvasErrorBoundaryState {
    console.error('Canvas Error Boundary caught:', error);
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Canvas error details:', { error, errorInfo, canvasId: this.props.id });
    
    // Track R3F specific errors
    if (error.message.includes('_roots') || error.message.includes('Canvas')) {
      console.error('R3F Initialization Error detected:', {
        message: error.message,
        stack: error.stack,
        canvasId: this.props.id
      });
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div style={{ 
            width: '100%', 
            height: '100%', 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            background: 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)',
            color: '#fff',
            border: '1px solid rgba(0, 255, 136, 0.3)',
            borderRadius: '8px'
          }}>
            <div style={{ textAlign: 'center', padding: '20px' }}>
              <div style={{ 
                width: '40px',
                height: '40px',
                border: '3px solid rgba(0, 255, 136, 0.3)',
                borderTop: '3px solid #00ff88',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                margin: '0 auto 16px'
              }} />
              <h3 style={{ margin: '0 0 8px', color: '#00ff88' }}>
                Neural Interface Temporarily Offline
              </h3>
              <p style={{ margin: '0 0 16px', color: '#ccc', fontSize: '14px' }}>
                Reinitializing Canvas subsystem...
              </p>
              <button 
                onClick={() => this.setState({ hasError: false })}
                style={{ 
                  padding: '8px 16px', 
                  background: '#00ff88',
                  color: '#000',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                Retry Initialization
              </button>
            </div>
            <style>{`
              @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
              }
            `}</style>
          </div>
        )
      );
    }

    return this.props.children;
  }
}

// Convenient wrapper component
export const SafeCanvas: React.FC<{ 
  children: ReactNode; 
  fallback?: ReactNode;
  id?: string;
}> = ({ children, fallback, id }) => {
  return (
    <CanvasErrorBoundary fallback={fallback} id={id}>
      {children}
    </CanvasErrorBoundary>
  );
}; 