import React, { Component, ErrorInfo } from 'react';
import { AlertCircle } from 'lucide-react';
import * as styles from './ErrorBoundary.styles';

interface Props {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error; resetError: () => void }>;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught error:', error, errorInfo);
    this.props.onError?.(error, errorInfo);
  }

  resetError = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError && this.state.error) {
      if (this.props.fallback) {
        const FallbackComponent = this.props.fallback;
        return <FallbackComponent error={this.state.error} resetError={this.resetError} />;
      }

      return (
        <div className={styles.errorContainer}>
          <div className={styles.errorContent}>
            <AlertCircle size={48} className={styles.errorIcon} />
            <h2 className={styles.errorTitle}>Module Error</h2>
            <p className={styles.errorMessage}>{this.state.error.message}</p>
            <button onClick={this.resetError} className={styles.retryButton}>
              Retry
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

// Module-specific error boundary
export const ModuleErrorBoundary: React.FC<{ children: React.ReactNode; moduleId: string }> = ({ 
  children, 
  moduleId 
}) => {
  return (
    <ErrorBoundary
      onError={(error, errorInfo) => {
        console.error(`Module ${moduleId} crashed:`, error, errorInfo);
        // Could send error to monitoring service
      }}
    >
      {children}
    </ErrorBoundary>
  );
}; 