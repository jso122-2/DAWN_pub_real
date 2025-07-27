import { create } from 'zustand';
import { useEffect, useState } from 'react';

// Types for window manager detection and configuration
export type TilingWM = 'i3' | 'sway' | 'bspwm' | 'awesome' | 'dwm' | 'xmonad' | 'qtile' | 'none';

interface TilingConfig {
  wmType: TilingWM;
  isEnabled: boolean;
  lockPanels: boolean;
  respectWMHints: boolean;
  panelConstraints: {
    minWidth: number;
    minHeight: number;
    preferredAspectRatio?: number;
  };
}

interface UIMode {
  tilingConfig: TilingConfig;
  setTilingEnabled: (enabled: boolean) => void;
  setLockPanels: (locked: boolean) => void;
  setRespectWMHints: (respect: boolean) => void;
  detectWM: () => Promise<TilingWM>;
  applyTilingConstraints: (panelId: string) => void;
}

// Store for UI mode configuration
export const useUIModeStore = create<UIMode>((set, get) => ({
  tilingConfig: {
    wmType: 'none',
    isEnabled: false,
    lockPanels: false,
    respectWMHints: true,
    panelConstraints: {
      minWidth: 300,
      minHeight: 200,
    },
  },
  
  setTilingEnabled: (enabled) => 
    set((state) => ({
      tilingConfig: { ...state.tilingConfig, isEnabled: enabled }
    })),
  
  setLockPanels: (locked) =>
    set((state) => ({
      tilingConfig: { ...state.tilingConfig, lockPanels: locked }
    })),
  
  setRespectWMHints: (respect) =>
    set((state) => ({
      tilingConfig: { ...state.tilingConfig, respectWMHints: respect }
    })),
  
  detectWM: async () => {
    if (typeof window === 'undefined') return 'none';
    
    try {
      // Method 1: Check environment variables
      const wmEnv = process.env.XDG_CURRENT_DESKTOP || process.env.DESKTOP_SESSION || '';
      
      // Method 2: Check X11 window properties (requires Electron/Tauri APIs)
      if (window.electronAPI?.detectWM) {
        const detected = await window.electronAPI.detectWM();
        set((state) => ({
          tilingConfig: { ...state.tilingConfig, wmType: detected }
        }));
        return detected;
      }
      
      // Method 3: Check process list
      if (window.electronAPI?.checkProcess) {
        const processes = await window.electronAPI.checkProcess();
        const wmProcessMap: Record<string, TilingWM> = {
          'i3': 'i3',
          'sway': 'sway',
          'bspwm': 'bspwm',
          'awesome': 'awesome',
          'dwm': 'dwm',
          'xmonad': 'xmonad',
          'qtile': 'qtile',
        };
        
        for (const [process, wm] of Object.entries(wmProcessMap)) {
          if (processes.includes(process)) {
            set((state) => ({
              tilingConfig: { ...state.tilingConfig, wmType: wm }
            }));
            return wm;
          }
        }
      }
      
      return 'none';
    } catch (error) {
      console.error('Error detecting WM:', error);
      return 'none';
    }
  },
  
  applyTilingConstraints: (panelId) => {
    const { tilingConfig } = get();
    if (!tilingConfig.isEnabled) return;
    
    // Apply WM-specific constraints
    if (window.electronAPI?.applyWMConstraints) {
      window.electronAPI.applyWMConstraints(panelId, {
        wmType: tilingConfig.wmType,
        lockPanels: tilingConfig.lockPanels,
        respectHints: tilingConfig.respectWMHints,
        constraints: tilingConfig.panelConstraints,
      });
    }
  },
}));

// Main hook for tiling-aware UI
export function useTilingAwareUI() {
  const { 
    tilingConfig, 
    setTilingEnabled, 
    setLockPanels, 
    detectWM, 
    applyTilingConstraints 
  } = useUIModeStore();
  
  const [isInitialized, setIsInitialized] = useState(false);

  // Auto-detect WM on mount
  useEffect(() => {
    const init = async () => {
      const detected = await detectWM();
      
      // Auto-enable tiling mode for known tiling WMs
      if (detected !== 'none') {
        setTilingEnabled(true);
      }
      
      setIsInitialized(true);
    };
    
    init();
  }, [detectWM, setTilingEnabled]);

  // Panel registration function
  const registerPanel = (panelId: string, options?: {
    preferredWidth?: number;
    preferredHeight?: number;
    canResize?: boolean;
    canFloat?: boolean;
  }) => {
    if (!tilingConfig.isEnabled) return;
    
    // Register panel with WM
    if (window.electronAPI?.registerPanel) {
      window.electronAPI.registerPanel(panelId, {
        ...options,
        wmType: tilingConfig.wmType,
        respectHints: tilingConfig.respectWMHints,
      });
    }
    
    // Apply initial constraints
    applyTilingConstraints(panelId);
  };

  // Get WM-specific recommendations
  const getWMRecommendations = () => {
    const recommendations: Record<TilingWM, any> = {
      i3: {
        commands: [
          'for_window [class="DAWN"] floating enable',
          'for_window [class="DAWN" title=".*Panel.*"] resize set 800 600',
        ],
        keybindings: {
          toggleFloat: 'Mod+Shift+Space',
          resize: 'Mod+r',
        },
      },
      sway: {
        commands: [
          'for_window [app_id="dawn"] floating enable',
          'for_window [app_id="dawn" title=".*Panel.*"] resize set 800 600',
        ],
        keybindings: {
          toggleFloat: 'Mod+Shift+Space',
          resize: 'Mod+r',
        },
      },
      bspwm: {
        rules: [
          'bspc rule -a DAWN state=floating',
          'bspc rule -a DAWN:panel manage=off',
        ],
        keybindings: {
          toggleFloat: 'super + f',
          resize: 'super + alt + {h,j,k,l}',
        },
      },
      awesome: { keybindings: {} },
      dwm: { keybindings: {} },
      xmonad: { keybindings: {} },
      qtile: { keybindings: {} },
      none: { keybindings: {} },
    };
    
    return recommendations[tilingConfig.wmType] || {};
  };

  return {
    // State
    wmType: tilingConfig.wmType,
    isEnabled: tilingConfig.isEnabled,
    isLocked: tilingConfig.lockPanels,
    isInitialized,
    
    // Actions
    enable: () => setTilingEnabled(true),
    disable: () => setTilingEnabled(false),
    toggle: () => setTilingEnabled(!tilingConfig.isEnabled),
    lock: () => setLockPanels(true),
    unlock: () => setLockPanels(false),
    toggleLock: () => setLockPanels(!tilingConfig.lockPanels),
    
    // Panel management
    registerPanel,
    applyConstraints: applyTilingConstraints,
    
    // WM info
    recommendations: getWMRecommendations(),
    
    // Utilities
    isFloatingWM: tilingConfig.wmType === 'none',
    isTilingWM: tilingConfig.wmType !== 'none',
  };
}

// Utility hook for individual panels
export function useTilingPanel(panelId: string, options?: {
  preferredWidth?: number;
  preferredHeight?: number;
  canResize?: boolean;
  canFloat?: boolean;
}) {
  const { registerPanel, isEnabled, isLocked, wmType } = useTilingAwareUI();
  
  useEffect(() => {
    if (isEnabled) {
      registerPanel(panelId, options);
    }
  }, [isEnabled, panelId, registerPanel, options]);
  
  return {
    // Panel-specific state
    isManaged: isEnabled,
    isLocked,
    wmType,
    
    // CSS classes for panel behavior
    className: [
      isEnabled && 'tiling-managed',
      isLocked && 'tiling-locked',
      !isLocked && 'tiling-floating',
      `wm-${wmType}`,
    ].filter(Boolean).join(' '),
    
    // Inline styles for WM hints
    style: isEnabled ? {
      minWidth: options?.preferredWidth || 300,
      minHeight: options?.preferredHeight || 200,
      resize: isLocked ? 'none' : 'both',
    } : {},
  };
} 