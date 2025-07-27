import React from 'react';

/**
 * GlassPanel: A reusable glassmorphic panel with neon glow.
 * Migrated from old DAWN repository - your signature glass effect!
 * @param glow - 'cyan' | 'purple' | 'mixed' (default: 'mixed')
 * @param className - Additional classes to merge
 * @param style - Additional styles
 * @param children - Panel content
 */
interface GlassPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  glow?: 'cyan' | 'purple' | 'mixed';
  style?: React.CSSProperties;
  className?: string;
  children: React.ReactNode;
}

const glowClass = {
  cyan: 'neon-glow-cyan',
  purple: 'neon-glow-purple',
  mixed: 'neon-glow-mixed',
};

const GlassPanel = React.forwardRef<HTMLDivElement, GlassPanelProps>(
  ({ glow = 'mixed', className = '', style, children, ...rest }, ref) => (
    <div
      ref={ref}
      className={`glass-panel fade-in ${glowClass[glow]} ${className}`}
      style={style}
      {...rest}
    >
      {children}
    </div>
  )
);

GlassPanel.displayName = 'GlassPanel';

export default GlassPanel; 