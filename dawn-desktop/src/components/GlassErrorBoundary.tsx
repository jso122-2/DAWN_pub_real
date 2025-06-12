import React from 'react';

interface GlassErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

class GlassErrorBoundary extends React.Component<React.PropsWithChildren<{}>, GlassErrorBoundaryState> {
  constructor(props: {}) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="glass rounded-xl p-8 m-8 border border-red-400 text-red-300 text-center shadow-glow-md" role="alert" aria-label="Error Panel">
          <h2 className="text-2xl font-bold mb-2">Something went wrong</h2>
          <p>{this.state.error?.message}</p>
        </div>
      );
    }
    return this.props.children;
  }
}

export default GlassErrorBoundary; 