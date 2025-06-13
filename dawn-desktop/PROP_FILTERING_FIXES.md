# DAWN Prop Filtering Fixes

## Problem
React was throwing warnings about custom props like `globalEntropy`, `motionProps`, and other DAWN-specific properties being passed through to DOM elements. This happens when:

1. Custom props are spread onto `motion.div` or other DOM elements
2. Props are passed to children using `React.cloneElement` without checking if the child is a DOM element
3. Higher-order components pass all props through without filtering

## Solutions Implemented

### 1. Enhanced SafeMotionDiv Component (`src/components/system/SafeMotionDiv.tsx`)
- **Function**: `filterProps()` - Separates custom props, motion props, and DOM props
- **Components**: `SafeMotionDiv`, `SafeMotionSpan`, `SafeMotionButton`, etc.
- **Usage**: Automatically filters props before passing to motion components

### 2. New Prop Utilities (`src/utils/propUtils.ts`)
- **`safeCloneElement()`**: Safely clones React elements, only passing custom props to React components
- **`safePassPropsToChildren()`**: Maps over children and safely passes props
- **`safeMotionProps()`**: Wrapper for filtering motion component props
- **`withSafeProps()`**: Higher-order component for prop filtering
- **`isReactComponent()` / `isDOMElement()`**: Type checking utilities

### 3. Fixed Components

#### ModuleOrchestra (`src/components/ModuleOrchestra.tsx`)
**Before**:
```tsx
{React.Children.map(children, (child) => {
  return React.cloneElement(child, { globalEntropy });
})}
```

**After**:
```tsx
{safePassPropsToChildren(children, { globalEntropy })}
```

#### ConsciousModule (`src/components/modules/ConsciousModule.tsx`)
**Before**:
```tsx
<motion.div {...breathingMotionProps}>
```

**After**:
```tsx
const { motionProps: safeBreathingProps } = filterProps(breathingMotionProps || {});
<motion.div {...safeBreathingProps}>
```

#### ApiIntegrationExample (`src/components/modules/ApiIntegrationExample.tsx`)
**Before**:
```tsx
<motion.div {...breathingProps}>
```

**After**:
```tsx
const { motionProps: breathingProps } = filterProps(rawBreathingProps || {});
<motion.div {...breathingProps}>
```

## Best Practices Going Forward

### 1. Use SafeMotionDiv for Motion Components
```tsx
import { SafeMotionDiv } from '../components/system/SafeMotionDiv';

// Instead of:
<motion.div globalEntropy={0.5} customProp="value">

// Use:
<SafeMotionDiv globalEntropy={0.5} customProp="value">
```

### 2. Filter Props When Spreading
```tsx
import { filterProps } from '../components/system/SafeMotionDiv';

const { motionProps, domProps, customProps } = filterProps(allProps);
<motion.div {...motionProps} {...domProps}>
```

### 3. Safe Children Prop Passing
```tsx
import { safePassPropsToChildren } from '../utils/propUtils';

// Instead of:
{React.Children.map(children, child => 
  React.cloneElement(child, { customProp })
)}

// Use:
{safePassPropsToChildren(children, { customProp })}
```

### 4. Component Type Checking
```tsx
import { isReactComponent, isDOMElement } from '../utils/propUtils';

if (isReactComponent(element)) {
  // Safe to pass custom props
} else if (isDOMElement(element)) {
  // Only pass standard DOM props
}
```

## Known Custom Props to Filter
The following props are automatically filtered out from DOM elements:

- `globalEntropy`
- `motionProps`
- `consciousnessLevel`
- `quantumState`
- `neuralActivity`
- `entropyLevel`
- `breathingPreset`
- `floatingPreset`
- `syncGroup`
- `orbitalGroup`
- `moduleId`
- `groupId`
- `isActive`
- `isCritical`
- `enableFloating`
- `enableBreathing`
- `glowIntensity`
- `particleCount`
- `connectionPorts`
- `dataFlow`
- `processingLoad`
- `healthStatus`
- `quantumCoherence`
- `neuralConnections`

## Testing
After implementing these fixes:

1. ✅ No more React warnings about unknown DOM properties
2. ✅ Custom props still work for React components
3. ✅ Motion components receive only valid motion props
4. ✅ DOM elements receive only valid HTML attributes
5. ✅ Backward compatibility maintained

## Future Improvements
1. Add TypeScript definitions for custom prop interfaces
2. Create ESLint rules to catch prop spreading issues
3. Add unit tests for prop filtering utilities
4. Consider using a more robust prop filtering library if needed 