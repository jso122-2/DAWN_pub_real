// DAWN GUI Theme Tokens - Central Design System

export const Colors = {
  // Core Background Colors
  background: "#0d1b2a",
  backgroundSecondary: "#1b263b", 
  backgroundTertiary: "#415a77",
  backgroundPanel: "rgba(27, 38, 59, 0.9)",
  backgroundHeader: "rgba(13, 27, 42, 0.95)",
  
  // Text Colors
  textPrimary: "#ffffffb4",
  textSecondary: "#cccccc99", 
  textFaint: "#99999966",
  textAccent: "#40e0ff",
  
  // Cognitive State Colors
  entropy: "#ffda3e",
  scup: "#ae81ff", 
  rebloom: "#9effa1",
  mood: "#42f5c8",
  tick: "#40e0ff",
  drift: "#ec4899",
  depth: "#f59e0b",
  
  // Status Colors
  success: "#10b981",
  warning: "#f59e0b", 
  danger: "#ff5555",
  error: "#ef4444",
  processing: "#8b5cf6",
  connected: "#10b981",
  
  // Cognitive Domain Colors
  cognitionCore: "#40e0ff",
  symbolicLayer: "#8b5cf6", 
  reflectionStream: "#10b981",
  
  // Interactive States
  hover: "rgba(64, 224, 255, 0.1)",
  focus: "#40e0ff",
  active: "rgba(64, 224, 255, 0.2)",
  disabled: "rgba(255, 255, 255, 0.3)",
  
  // Overlays
  overlay: "rgba(0, 0, 0, 0.7)",
  backdropBlur: "rgba(13, 27, 42, 0.8)",
} as const;

export const Spacing = {
  // Core Spacing Units
  padding: "16px",
  margin: "12px", 
  gap: "10px",
  
  // Specific Use Cases
  panelPadding: "16px",
  panelGap: "16px",
  headerPadding: "12px",
  statusBarHeight: "32px",
  
  // Layout Spacing
  containerPadding: "16px",
  columnGap: "16px",
  sectionGap: "24px",
  
  // Component Spacing
  buttonPadding: "8px 16px",
  inputPadding: "8px 12px",
  iconGap: "8px",
  
  // Micro Spacing
  xs: "4px",
  sm: "8px", 
  md: "12px",
  lg: "16px",
  xl: "24px",
  xxl: "32px",
} as const;

export const Font = {
  // Font Families
  mono: "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
  ui: "'Liberation Sans', 'DejaVu Sans', 'Arial', sans-serif",
  
  // Font Sizes
  size: {
    xs: "10px",
    sm: "12px",
    label: "12px",
    body: "14px", 
    base: "14px",
    lg: "16px",
    title: "16px",
    xl: "18px",
    xxl: "24px",
    display: "32px",
  },
  
  // Font Weights
  weight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  
  // Line Heights
  lineHeight: {
    tight: 1.2,
    normal: 1.4,
    relaxed: 1.6,
  },
  
  // Letter Spacing
  letterSpacing: {
    tight: "-0.025em",
    normal: "0",
    wide: "0.025em",
    wider: "0.05em",
    widest: "0.1em",
  },
} as const;

export const BorderRadius = {
  none: "0",
  sm: "4px",
  base: "8px", 
  md: "8px",
  lg: "12px",
  xl: "16px",
  full: "9999px",
} as const;

export const Shadows = {
  none: "none",
  sm: "0 1px 2px rgba(0, 0, 0, 0.1)",
  base: "0 1px 3px rgba(0, 0, 0, 0.15)",
  md: "0 4px 6px rgba(0, 0, 0, 0.1)",
  lg: "0 10px 15px rgba(0, 0, 0, 0.1)",
  xl: "0 20px 25px rgba(0, 0, 0, 0.1)",
  
  // Cognitive Glows
  tickGlow: "0 0 8px rgba(64, 224, 255, 0.4)",
  entropyGlow: "0 0 8px rgba(255, 218, 62, 0.4)", 
  rebloomGlow: "0 0 8px rgba(158, 255, 161, 0.4)",
  dangerGlow: "0 0 8px rgba(255, 85, 85, 0.4)",
} as const;

export const Transitions = {
  fast: "0.1s ease",
  normal: "0.2s ease", 
  slow: "0.3s ease",
  
  // Specific Transitions
  color: "color 0.2s ease",
  background: "background-color 0.2s ease",
  border: "border-color 0.2s ease",
  transform: "transform 0.2s ease", 
  opacity: "opacity 0.2s ease",
  
  // Complex Transitions
  panel: "border-color 0.2s ease, background-color 0.2s ease",
  button: "all 0.2s ease",
} as const;

// Shared Panel Styles Object
export const PanelStyles = {
  // Base Panel
  base: {
    background: Colors.backgroundPanel,
    border: `1px solid ${Colors.backgroundTertiary}`,
    borderRadius: BorderRadius.md,
    backdropFilter: "blur(10px)",
    transition: Transitions.panel,
  },
  
  // Panel States
  hover: {
    borderColor: Colors.textAccent,
  },
  
  active: {
    borderColor: Colors.textAccent,
    background: Colors.active,
  },
  
  critical: {
    borderColor: Colors.danger,
    background: "rgba(239, 68, 68, 0.1)",
  },
  
  processing: {
    borderColor: Colors.processing,
  },
  
  // Panel Shadows
  shadow: {
    boxShadow: Shadows.base,
  },
  
  glowShadow: {
    boxShadow: Shadows.tickGlow,
  },
} as const;

// Animation Keyframes
export const Animations = {
  // Pulse for live indicators
  pulse: {
    keyframes: `
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
      }
    `,
    animation: "pulse 2s ease-in-out infinite",
  },
  
  // Glow for high activity
  glow: {
    keyframes: `
      @keyframes glow {
        0% { opacity: 0.6; }
        100% { opacity: 1; }
      }
    `,
    animation: "glow 1s ease-in-out infinite alternate",
  },
  
  // Spin for loading
  spin: {
    keyframes: `
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `,
    animation: "spin 1s linear infinite",
  },
  
  // Fade in for panels
  fadeIn: {
    keyframes: `
      @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
      }
    `,
    animation: "fadeIn 0.3s ease-out",
  },
} as const;

// Breakpoints for responsive design
export const Breakpoints = {
  mobile: "768px",
  tablet: "1024px", 
  desktop: "1200px",
  wide: "1400px",
} as const;

// Z-Index layers
export const ZIndex = {
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,
  popover: 1060,
  tooltip: 1070,
  notification: 1080,
} as const;

// CSS Custom Properties Generator
export const generateCSSVariables = () => {
  const cssVars: Record<string, string> = {};
  
  // Generate color variables
  Object.entries(Colors).forEach(([key, value]) => {
    cssVars[`--color-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`] = value;
  });
  
  // Generate spacing variables  
  Object.entries(Spacing).forEach(([key, value]) => {
    cssVars[`--spacing-${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`] = value;
  });
  
  // Generate font variables
  Object.entries(Font.size).forEach(([key, value]) => {
    cssVars[`--font-size-${key}`] = value;
  });
  
  return cssVars;
};

// Export everything as default for convenience
export default {
  Colors,
  Spacing, 
  Font,
  BorderRadius,
  Shadows,
  Transitions,
  PanelStyles,
  Animations,
  Breakpoints,
  ZIndex,
  generateCSSVariables,
} as const; 