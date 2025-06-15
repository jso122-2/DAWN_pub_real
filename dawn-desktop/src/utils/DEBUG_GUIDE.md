# 🔍 Prop Debugging Guide

This guide helps you identify and fix React warnings about unknown DOM properties in DAWN components.

## Common Warning

```
Warning: React does not recognize the `globalEntropy` prop on a DOM element.
```

## Quick Solutions

### 1. Use SafeMotionDiv (Recommended)

Replace `motion.div` with `SafeMotionDiv`:

```tsx
// ❌ Before (causes warnings)
<motion.div globalEntropy={0.5} className="my-component">
  {children}
</motion.div>

// ✅ After (safe)
import { SafeMotionDiv } from '@/components/system/SafeMotionDiv'

<SafeMotionDiv globalEntropy={0.5} className="my-component">
  {children}
</SafeMotionDiv>
```

### 2. Add Debug Utilities

#### Quick Debug Hook

Add to any component to see what props it receives:

```tsx
import { usePropDebugger } from '@/utils/propDebugger'

function MyComponent(props) {
  // Add this line to see all props and potential issues
  usePropDebugger(props, {
    componentName: 'MyComponent',
    logLevel: 'warn',
    highlightDOMIssues: true
  })
  
  return <div>{/* your content */}</div>
}
```

#### Quick Debug Function

Add this anywhere in a component:

```tsx
import { debugComponentProps } from '@/utils/DebugWrapper'

function MyComponent(props) {
  // Add this line for immediate debugging
  debugComponentProps('MyComponent', props)
  
  return <div>{/* your content */}</div>
}
```

#### Debug Wrapper Component

Wrap problematic components:

```tsx
import { DebugWrapper } from '@/utils/DebugWrapper'

function ParentComponent() {
  return (
    <DebugWrapper componentName="ProblematicChild" globalEntropy={0.5}>
      <ProblematicChild />
    </DebugWrapper>
  )
}
```

### 3. Filter Props Manually

```tsx
import { filterDOMProps } from '@/utils/propDebugger'

function MyComponent(props) {
  const { domProps, customProps } = filterDOMProps(props)
  
  console.log('DOM-safe props:', domProps)
  console.log('Custom props:', customProps)
  
  return <div {...domProps}>{/* only DOM props passed */}</div>
}
```

## Debug Levels

- `'debug'` - Log everything (very verbose)
- `'info'` - Log custom props and issues
- `'warn'` - Only log potential problems (default)
- `'none'` - Disable debugging

## Common DAWN Props That Cause Issues

These props should NOT be passed to DOM elements:

- `globalEntropy`
- `consciousnessLevel` 
- `consciousnessState`
- `neuralActivity`
- `entropyLevel`
- `breathingPreset`
- `floatingPreset`
- `syncGroup`
- `orbitalGroup`
- `moduleId`
- `motionProps`

## Example Debug Output

```
[PropDebugger] MyComponent - Custom props detected: ["globalEntropy", "moduleId"]
[PropDebugger] MyComponent - POTENTIAL DOM ISSUES! These DAWN props might be passed to DOM elements: ["globalEntropy"]
  💡 Solution: Use SafeMotionDiv or filter these props before passing to DOM elements
[PropDebugger] MyComponent - 🔧 Fix globalEntropy: Use SafeMotionDiv from '@/components/system/SafeMotionDiv'
```

## Best Practices

1. **Use SafeMotionDiv** for motion components that receive DAWN props
2. **Add debug utilities** during development to catch issues early
3. **Filter props** before passing to DOM elements
4. **Remove debug code** before production (or use NODE_ENV checks)
5. **Check the console** regularly during development

## Disable Debugging

To disable all debugging:

```tsx
// Set logLevel to 'none'
usePropDebugger(props, {
  componentName: 'MyComponent',
  logLevel: 'none'
})

// Or use environment check
usePropDebugger(props, {
  componentName: 'MyComponent',
  logLevel: process.env.NODE_ENV === 'development' ? 'warn' : 'none'
})
```

## Integration with ModuleOrchestra

The `ModuleOrchestra` component already filters props safely. If you're still getting warnings, check child components that receive `globalEntropy`.

## Need Help?

1. Check the browser console for debug messages
2. Look for components with `.ts` extension that should be `.tsx`
3. Verify SafeMotionDiv imports are correct
4. Use the debug utilities to trace prop flow 