# React Three Fiber `_roots` Initialization Fix

## 🎯 **Problem Diagnosis**

Your Dawn Neural Monitor is hitting a **React Three Fiber initialization race condition**. The Canvas component is being unmounted before the Three.js scene fully initializes, causing the `Cannot access '_roots' before initialization` error.

**Root Cause:** React 18's Strict Mode + R3F timing mismatch + improper cleanup patterns.

---

## 🛠 **Immediate Fix Strategy**

### 1. **Canvas Component Stabilization**

```typescript
// src/components/ParticleBackground.tsx
import React, { useRef, useEffect, useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';

export function ParticleBackground() {
  const [isCanvasReady, setIsCanvasReady] = useState(false);
  const mountedRef = useRef(true);

  useEffect(() => {
    // Delay canvas mounting to avoid race condition
    const timer = setTimeout(() => {
      if (mountedRef.current) {
        setIsCanvasReady(true);
      }
    }, 100);

    return () => {
      clearTimeout(timer);
      mountedRef.current = false;
    };
  }, []);

  // Don't render Canvas until component is stable
  if (!isCanvasReady) {
    return (
      <div style={{ width: '100%', height: '100%', background: '#000' }}>
        <div>Loading Neural Interface...</div>
      </div>
    );
  }

  return (
    <Canvas
      // Force software rendering as fallback
      gl={{ 
        antialias: true,
        alpha: true,
        preserveDrawingBuffer: false,
        powerPreference: "high-performance"
      }}
      // Prevent automatic camera updates during mount
      camera={{ position: [0, 0, 5], fov: 75 }}
      // Add error recovery
      onCreated={(state) => {
        console.log('Canvas created successfully', state);
      }}
      onError={(error) => {
        console.error('Canvas creation error:', error);
      }}
    >
      <Suspense fallback={<ParticleLoadingFallback />}>
        <ParticleSystem />
      </Suspense>
    </Canvas>
  );
}

function ParticleLoadingFallback() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshBasicMaterial color="orange" wireframe />
    </mesh>
  );
}
```

### 2. **Safe Component Unmounting Pattern**

```typescript
// src/components/ParticleSystem.tsx
import React, { useRef, useEffect, useCallback } from 'react';
import { useFrame, useThree } from '@react-three/fiber';
import * as THREE from 'three';

export function ParticleSystem() {
  const meshRef = useRef<THREE.Mesh>(null);
  const { scene, gl } = useThree();
  const mountedRef = useRef(true);

  // Safe cleanup pattern
  useEffect(() => {
    return () => {
      mountedRef.current = false;
      
      // Clean up Three.js resources
      if (meshRef.current) {
        if (meshRef.current.geometry) {
          meshRef.current.geometry.dispose();
        }
        if (meshRef.current.material) {
          if (Array.isArray(meshRef.current.material)) {
            meshRef.current.material.forEach(mat => mat.dispose());
          } else {
            meshRef.current.material.dispose();
          }
        }
        scene.remove(meshRef.current);
      }
    };
  }, [scene]);

  // Safe frame updates
  useFrame((state, delta) => {
    if (!mountedRef.current || !meshRef.current) return;
    
    try {
      meshRef.current.rotation.x += delta * 0.5;
      meshRef.current.rotation.y += delta * 0.2;
    } catch (error) {
      console.warn('Frame update error:', error);
    }
  });

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[1, 32, 32]} />
      <meshStandardMaterial color="cyan" wireframe />
    </mesh>
  );
}
```

### 3. **Canvas Container with Error Boundaries**

```typescript
// src/components/SafeCanvas.tsx
import React, { ErrorInfo, ReactNode } from 'react';

interface CanvasErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export class CanvasErrorBoundary extends React.Component<
  { children: ReactNode; fallback?: ReactNode },
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
    console.error('Canvas error details:', { error, errorInfo });
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
            background: '#1a1a1a',
            color: '#fff'
          }}>
            <div>
              <h3>Neural Interface Temporarily Offline</h3>
              <p>Reinitializing...</p>
              <button 
                onClick={() => this.setState({ hasError: false })}
                style={{ padding: '8px 16px', marginTop: '16px' }}
              >
                Retry
              </button>
            </div>
          </div>
        )
      );
    }

    return this.props.children;
  }
}

// Usage in UnifiedHomePage
export function SafeParticleField() {
  return (
    <CanvasErrorBoundary>
      <ParticleField />
    </CanvasErrorBoundary>
  );
}
```

---

## 🔧 **Package Version Alignment**

### Check Package Compatibility

```bash
# Check current versions
npm list @react-three/fiber @react-three/drei react react-dom

# Update to compatible versions
npm install @react-three/fiber@^8.15.0 @react-three/drei@^9.88.0
npm install react@^18.2.0 react-dom@^18.2.0

# Clear any version conflicts
npm install --legacy-peer-deps
```

### Package.json Fixes

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@react-three/fiber": "^8.15.0",
    "@react-three/drei": "^9.88.0",
    "three": "^0.157.0"
  },
  "overrides": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}
```

---

## ⚡ **Development Mode Fixes**

### 1. **Disable Strict Mode Temporarily**

```typescript
// src/index.tsx - Temporary fix during development
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root')!);

// Remove StrictMode wrapper temporarily
root.render(<App />);

// Instead of:
// root.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>
// );
```

### 2. **Add Canvas Initialization Guards**

```typescript
// src/hooks/useCanvasGuard.ts
import { useEffect, useState, useRef } from 'react';

export function useCanvasGuard() {
  const [isReady, setIsReady] = useState(false);
  const mountedRef = useRef(true);

  useEffect(() => {
    // Wait for component to be fully mounted
    const initTimer = setTimeout(() => {
      if (mountedRef.current) {
        setIsReady(true);
      }
    }, 150);

    return () => {
      clearTimeout(initTimer);
      mountedRef.current = false;
      setIsReady(false);
    };
  }, []);

  return { isReady, isMounted: mountedRef.current };
}

// Usage in components
export function GuardedCanvas({ children }: { children: React.ReactNode }) {
  const { isReady } = useCanvasGuard();
  
  if (!isReady) {
    return <div>Initializing...</div>;
  }
  
  return (
    <Canvas>
      {children}
    </Canvas>
  );
}
```

---

## 🧪 **Debug and Monitoring**

### 1. **Canvas State Monitoring**

```typescript
// src/utils/canvasDebug.ts
export function createCanvasMonitor() {
  let canvasCount = 0;
  let activeCanvases = new Set();

  return {
    onCanvasCreate: (id: string) => {
      canvasCount++;
      activeCanvases.add(id);
      console.log(`Canvas ${id} created. Total: ${canvasCount}, Active: ${activeCanvases.size}`);
    },
    
    onCanvasDestroy: (id: string) => {
      activeCanvases.delete(id);
      console.log(`Canvas ${id} destroyed. Active: ${activeCanvases.size}`);
    },
    
    getStats: () => ({
      total: canvasCount,
      active: activeCanvases.size,
      activeIds: Array.from(activeCanvases)
    })
  };
}

// Global monitor
export const canvasMonitor = createCanvasMonitor();
```

### 2. **Error Recovery Hook**

```typescript
// src/hooks/useCanvasRecovery.ts
import { useState, useCallback, useRef } from 'react';

export function useCanvasRecovery() {
  const [error, setError] = useState<Error | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 3;

  const handleError = useCallback((err: Error) => {
    console.error('Canvas error:', err);
    setError(err);
  }, []);

  const retry = useCallback(() => {
    if (retryCount < maxRetries) {
      setError(null);
      setRetryCount(prev => prev + 1);
    }
  }, [retryCount, maxRetries]);

  const reset = useCallback(() => {
    setError(null);
    setRetryCount(0);
  }, []);

  return {
    error,
    retry,
    reset,
    canRetry: retryCount < maxRetries,
    retryCount,
    handleError
  };
}
```

---

## 🚀 **Quick Implementation Steps**

1. **Apply Canvas stabilization** to ParticleBackground component
2. **Add error boundaries** around all Canvas components  
3. **Update package versions** to compatible set
4. **Temporarily disable StrictMode** during development
5. **Add monitoring hooks** to track Canvas lifecycle
6. **Test with gradual re-enabling** of strict mode

### Expected Results:
- ✅ No more `_roots` initialization errors
- ✅ Stable Canvas mounting/unmounting
- ✅ Graceful error recovery
- ✅ Better development experience

### Test Commands:
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Start with clean slate  
npm start

# Monitor for errors
npm run build
```

This fix addresses the core R3F initialization race condition while maintaining your Dawn Neural Monitor's visual architecture. The error boundaries provide graceful degradation, and the monitoring helps track Canvas lifecycle issues.

