import { useEffect, useRef, useState, useCallback } from 'react';
import { useSpring, useMotionValue, useTransform, SpringOptions } from 'framer-motion';
import { useAnimation } from '../../contexts/AnimationContext';

// Module position manager for magnetic repulsion
class ModulePositionManager {
  private static instance: ModulePositionManager;
  private modules: Map<string, { x: number; y: number; z: number }> = new Map();
  private listeners: Set<(positions: Map<string, { x: number; y: number; z: number }>) => void> = new Set();

  static getInstance() {
    if (!ModulePositionManager.instance) {
      ModulePositionManager.instance = new ModulePositionManager();
    }
    return ModulePositionManager.instance;
  }

  updatePosition(moduleId: string, position: { x: number; y: number; z: number }) {
    this.modules.set(moduleId, position);
    this.notifyListeners();
  }

  removeModule(moduleId: string) {
    this.modules.delete(moduleId);
    this.notifyListeners();
  }

  getModules() {
    return new Map(this.modules);
  }

  subscribe(listener: (positions: Map<string, { x: number; y: number; z: number }>) => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  private notifyListeners() {
    this.listeners.forEach(listener => listener(this.getModules()));
  }
}

export interface FloatingConfig {
  hoverHeight?: number;
  rotationRange?: number;
  mouseInfluence?: number;
  magneticStrength?: number;
  orbitalRadius?: number;
  springConfig?: SpringOptions;
  depthRange?: { min: number; max: number };
}

interface UseFloatingOptions {
  moduleId?: string;
  groupId?: string;
  config?: FloatingConfig;
  isActive?: boolean;
  isFocused?: boolean;
}

interface UseFloatingReturn {
  floatingStyle: {
    x: any;
    y: any;
    z: any;
    rotateX: any;
    rotateY: any;
    scale: any;
  };
  updatePosition: (x: number, y: number) => void;
  setFocus: (focused: boolean) => void;
  nearbyModules: number;
}

const DEFAULT_CONFIG: FloatingConfig = {
  hoverHeight: 20,
  rotationRange: 5,
  mouseInfluence: 0.3,
  magneticStrength: 50,
  orbitalRadius: 100,
  springConfig: {
    stiffness: 150,
    damping: 20,
    mass: 1
  },
  depthRange: { min: 0, max: 100 }
};

export function useFloating({
  moduleId = `floating-${Date.now()}`,
  groupId,
  config = {},
  isActive = true,
  isFocused: initialFocused = false
}: UseFloatingOptions = {}): UseFloatingReturn {
  const { isAnimationsEnabled } = useAnimation();
  const positionManager = ModulePositionManager.getInstance();
  const mergedConfig = { ...DEFAULT_CONFIG, ...config };
  
  // Motion values
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);
  const baseX = useMotionValue(0);
  const baseY = useMotionValue(0);
  const baseZ = useMotionValue(0);
  
  // State
  const [isFocused, setIsFocused] = useState(initialFocused);
  const [nearbyModules, setNearbyModules] = useState(0);
  const modulePositionRef = useRef({ x: 0, y: 0, z: 0 });
  const animationFrameRef = useRef<number>();
  const orbitalPhaseRef = useRef(Math.random() * Math.PI * 2);
  
  // Spring physics
  const springConfig = mergedConfig.springConfig!;
  const x = useSpring(baseX, springConfig);
  const y = useSpring(baseY, springConfig);
  const z = useSpring(baseZ, springConfig);
  
  // Rotation based on position
  const rotateX = useTransform(
    y,
    [-100, 100],
    [-mergedConfig.rotationRange!, mergedConfig.rotationRange!]
  );
  const rotateY = useTransform(
    x,
    [-100, 100],
    [mergedConfig.rotationRange!, -mergedConfig.rotationRange!]
  );
  
  // Scale based on depth
  const scale = useTransform(
    z,
    [mergedConfig.depthRange!.min, mergedConfig.depthRange!.max],
    [0.95, 1.05]
  );
  
  // Mouse tracking
  useEffect(() => {
    if (!isAnimationsEnabled || !isActive) return;
    
    const handleMouseMove = (e: MouseEvent) => {
      mouseX.set(e.clientX);
      mouseY.set(e.clientY);
    };
    
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, [mouseX, mouseY, isAnimationsEnabled, isActive]);
  
  // Calculate forces and update position
  const updateFloatingPosition = useCallback(() => {
    if (!isAnimationsEnabled || !isActive) return;
    
    const currentMouseX = mouseX.get();
    const currentMouseY = mouseY.get();
    const modulePos = modulePositionRef.current;
    
    // Base floating animation
    const time = Date.now() * 0.001;
    let targetX = Math.sin(time * 0.5) * 5;
    let targetY = Math.cos(time * 0.7) * mergedConfig.hoverHeight!;
    let targetZ = mergedConfig.depthRange!.min;
    
    // Mouse influence (gentle repulsion)
    const dx = modulePos.x - currentMouseX;
    const dy = modulePos.y - currentMouseY;
    const mouseDistance = Math.sqrt(dx * dx + dy * dy);
    
    if (mouseDistance < 200 && mouseDistance > 0) {
      const force = (1 - mouseDistance / 200) * mergedConfig.mouseInfluence!;
      targetX += (dx / mouseDistance) * force * 30;
      targetY += (dy / mouseDistance) * force * 30;
    }
    
    // Magnetic repulsion from other modules
    const otherModules = positionManager.getModules();
    let repulsionX = 0;
    let repulsionY = 0;
    let nearbyCount = 0;
    
    otherModules.forEach((otherPos, otherId) => {
      if (otherId === moduleId) return;
      
      const dx = modulePos.x - otherPos.x;
      const dy = modulePos.y - otherPos.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < 150 && distance > 0) {
        nearbyCount++;
        const force = (1 - distance / 150) * mergedConfig.magneticStrength!;
        repulsionX += (dx / distance) * force;
        repulsionY += (dy / distance) * force;
      }
    });
    
    targetX += repulsionX;
    targetY += repulsionY;
    setNearbyModules(nearbyCount);
    
    // Orbital motion when grouped
    if (groupId && nearbyCount > 2) {
      orbitalPhaseRef.current += 0.01;
      const orbitalX = Math.cos(orbitalPhaseRef.current) * mergedConfig.orbitalRadius! * 0.3;
      const orbitalY = Math.sin(orbitalPhaseRef.current) * mergedConfig.orbitalRadius! * 0.3;
      targetX += orbitalX;
      targetY += orbitalY;
    }
    
    // Focus state affects depth
    if (isFocused) {
      targetZ = mergedConfig.depthRange!.max;
      targetY -= 10; // Float higher when focused
    } else if (nearbyCount > 3) {
      targetZ = mergedConfig.depthRange!.min - 20; // Push back when crowded
    }
    
    // Apply targets
    baseX.set(targetX);
    baseY.set(targetY);
    baseZ.set(targetZ);
    
    // Update position in manager
    positionManager.updatePosition(moduleId, {
      x: modulePos.x + targetX,
      y: modulePos.y + targetY,
      z: targetZ
    });
    
    animationFrameRef.current = requestAnimationFrame(updateFloatingPosition);
  }, [
    moduleId,
    groupId,
    mouseX,
    mouseY,
    baseX,
    baseY,
    baseZ,
    mergedConfig,
    isFocused,
    isAnimationsEnabled,
    isActive,
    positionManager
  ]);
  
  // Start animation loop
  useEffect(() => {
    if (isAnimationsEnabled && isActive) {
      updateFloatingPosition();
    }
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      positionManager.removeModule(moduleId);
    };
  }, [updateFloatingPosition, moduleId, isAnimationsEnabled, isActive]);
  
  // Update module position
  const updatePosition = useCallback((x: number, y: number) => {
    modulePositionRef.current = { x, y, z: modulePositionRef.current.z };
  }, []);
  
  // Set focus state
  const setFocus = useCallback((focused: boolean) => {
    setIsFocused(focused);
  }, []);
  
  return {
    floatingStyle: {
      x,
      y,
      z,
      rotateX,
      rotateY,
      scale
    },
    updatePosition,
    setFocus,
    nearbyModules
  };
}

// Export position manager for global access
export const modulePositionManager = ModulePositionManager.getInstance();