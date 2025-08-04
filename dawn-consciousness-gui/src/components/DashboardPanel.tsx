import React from 'react';
import { Colors, Font, Spacing, PanelStyles, Transitions } from '../theme/theme_tokens';
import './DashboardPanel.css';

// Standardized Panel Wrapper Component
interface DashboardPanelProps {
  title: string;
  children: React.ReactNode;
  icon?: string;
  className?: string;
  isLive?: boolean;
  onToggle?: () => void;
  onExport?: () => void;
  onSnapshot?: () => void;
  variant?: 'default' | 'cognition' | 'symbolic' | 'reflection';
}

export const DashboardPanel: React.FC<DashboardPanelProps> = ({
  title,
  children,
  icon,
  className = '',
  isLive = false,
  onToggle,
  onExport,
  onSnapshot,
  variant = 'default'
}) => {
  const getVariantColor = () => {
    switch (variant) {
      case 'cognition': return Colors.cognitionCore;
      case 'symbolic': return Colors.symbolicLayer;
      case 'reflection': return Colors.reflectionStream;
      default: return Colors.textAccent;
    }
  };

  const variantColor = getVariantColor();

  return (
    <div 
      className={`dashboard-panel ${className}`}
      style={{
        ...PanelStyles.base,
        borderColor: isLive ? variantColor : Colors.backgroundTertiary,
        transition: Transitions.panel,
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = variantColor;
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = isLive ? variantColor : Colors.backgroundTertiary;
      }}
    >
      {/* Panel Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: `${Spacing.sm} ${Spacing.panelPadding}`,
        borderBottom: `1px solid ${Colors.backgroundTertiary}`,
        minHeight: '40px',
      }}>
        {/* Title Section */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: Spacing.xs,
        }}>
          {icon && (
            <span style={{
              fontSize: Font.size.sm,
              color: variantColor,
            }}>
              {icon}
            </span>
          )}
          <h3 style={{
            fontSize: Font.size.sm,
            color: Colors.textPrimary,
            margin: 0,
            textTransform: 'uppercase',
            letterSpacing: Font.letterSpacing.wide,
            fontFamily: Font.mono,
            fontWeight: Font.weight.semibold,
          }}>
            {title}
          </h3>
          {isLive && (
            <div style={{
              width: '6px',
              height: '6px',
              borderRadius: '50%',
              backgroundColor: Colors.connected,
              animation: 'pulse 2s ease-in-out infinite',
            }} />
          )}
        </div>

        {/* Control Buttons */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: Spacing.xs,
        }}>
          {onToggle && (
            <button
              style={{
                background: 'transparent',
                border: 'none',
                color: Colors.textSecondary,
                fontSize: Font.size.xs,
                cursor: 'pointer',
                padding: '2px 4px',
                borderRadius: '2px',
                transition: Transitions.button,
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = variantColor;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = Colors.textSecondary;
              }}
              onClick={onToggle}
              title="Toggle panel"
            >
              ⏸
            </button>
          )}
          {onExport && (
            <button
              style={{
                background: 'transparent',
                border: 'none',
                color: Colors.textSecondary,
                fontSize: Font.size.xs,
                cursor: 'pointer',
                padding: '2px 4px',
                borderRadius: '2px',
                transition: Transitions.button,
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = variantColor;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = Colors.textSecondary;
              }}
              onClick={onExport}
              title="Export data"
            >
              ↗
            </button>
          )}
          {onSnapshot && (
            <button
              style={{
                background: 'transparent',
                border: 'none',
                color: Colors.textSecondary,
                fontSize: Font.size.xs,
                cursor: 'pointer',
                padding: '2px 4px',
                borderRadius: '2px',
                transition: Transitions.button,
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.color = variantColor;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.color = Colors.textSecondary;
              }}
              onClick={onSnapshot}
              title="Take snapshot"
            >
              📸
            </button>
          )}
        </div>
      </div>

      {/* Panel Content */}
      <div style={{
        flex: 1,
        padding: Spacing.panelPadding,
        overflow: 'auto',
        minHeight: 0,
      }}>
        {children}
      </div>

      {/* Inject pulse animation */}
      <style>
        {`
          @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.6; }
          }
        `}
      </style>
    </div>
  );
};

// Legacy Panel Component (for backward compatibility)
interface PanelProps {
  title: string;
  children: React.ReactNode;
  icon?: string;
  className?: string;
}

export const Panel: React.FC<PanelProps> = ({ title, children, icon, className = '' }) => {
  return (
    <DashboardPanel 
      title={title}
      icon={icon}
      className={className}
    >
      {children}
    </DashboardPanel>
  );
};

export default DashboardPanel; 