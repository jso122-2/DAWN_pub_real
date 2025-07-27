// DAWN Blueprint Design System - Unified Design Tokens
// Schematic, blueprint-style consistency across all components

export const DesignTokens = {
  // Typography System
  fonts: {
    primary: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
    sizes: {
      title: '16px',
      body: '14px',
      small: '13px',
      label: '12px',
      micro: '11px'
    },
    weights: {
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700
    }
  },

  // Color System
  colors: {
    // Base Blueprint Colors
    background: '#0d1b2a',
    surface: '#0d1b2a',
    border: '#ffffff25',
    borderHover: '#ffffff40',
    borderActive: '#ffffff60',
    
    // Text Colors
    textPrimary: '#ffffffb4',
    textSecondary: '#ffffff99',
    textTertiary: '#ffffff66',
    textMuted: '#ffffff40',
    
    // Status Colors
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
    
    // Cognitive System Colors
    cognition: '#40e0ff',
    symbolic: '#8b5cf6',
    reflection: '#10b981',
    entropy: '#ff6b6b',
    scup: '#ffd93d',
    mood: '#4ecdc4',
    
    // Interaction States
    overlay: 'rgba(255, 255, 255, 0.05)',
    overlayHover: 'rgba(255, 255, 255, 0.08)',
    overlayActive: 'rgba(255, 255, 255, 0.12)',
  },

  // Spacing System
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '12px',
    lg: '16px',
    xl: '20px',
    xxl: '24px'
  },

  // Layout System
  layout: {
    maxWidth: '1400px',
    panelMinHeight: '200px',
    panelSmallHeight: '150px',
    borderRadius: '6px',
    borderWidth: '1px'
  },

  // Animation System
  animations: {
    fast: '0.15s ease',
    normal: '0.2s ease',
    slow: '0.3s ease',
    pulse: '2s ease-in-out infinite'
  }
} as const;

// CSS Custom Properties for runtime theming
export const getCSSVariables = () => ({
  '--color-background': DesignTokens.colors.background,
  '--color-surface': DesignTokens.colors.surface,
  '--color-border': DesignTokens.colors.border,
  '--color-border-hover': DesignTokens.colors.borderHover,
  '--color-text-primary': DesignTokens.colors.textPrimary,
  '--color-text-secondary': DesignTokens.colors.textSecondary,
  '--color-cognition': DesignTokens.colors.cognition,
  '--color-symbolic': DesignTokens.colors.symbolic,
  '--color-reflection': DesignTokens.colors.reflection,
  '--font-primary': DesignTokens.fonts.primary,
  '--font-size-title': DesignTokens.fonts.sizes.title,
  '--font-size-body': DesignTokens.fonts.sizes.body,
  '--spacing-md': DesignTokens.spacing.md,
  '--spacing-lg': DesignTokens.spacing.lg,
  '--border-radius': DesignTokens.layout.borderRadius,
  '--animation-normal': DesignTokens.animations.normal
});

// Panel State Types
export type PanelState = 'active' | 'idle' | 'loading' | 'error';

// Standard Panel Configuration
export interface PanelConfig {
  title: string;
  icon?: string;
  category: 'cognition' | 'symbolic' | 'reflection';
  state?: PanelState;
  tooltip?: string;
}

// Standard panel styling helper
export const getPanelStyles = (category: PanelConfig['category']) => ({
  borderColor: category === 'cognition' ? DesignTokens.colors.cognition :
               category === 'symbolic' ? DesignTokens.colors.symbolic :
               DesignTokens.colors.reflection
}); 