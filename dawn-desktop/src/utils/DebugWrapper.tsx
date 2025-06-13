import React from 'react';
import { usePropDebugger } from './propDebugger';

interface DebugWrapperProps {
  componentName: string;
  logLevel?: 'none' | 'warn' | 'info' | 'debug';
  logProps?: boolean;
  children: React.ReactNode;
  [key: string]: any;
}

/**
 * Wrapper component for debugging props passed to child components
 * Usage: <DebugWrapper componentName="MyComponent" {...props}>{children}</DebugWrapper>
 */
export function DebugWrapper({
  componentName,
  logLevel = 'warn',
  logProps = false,
  children,
  ...restProps
}: DebugWrapperProps) {
  
  // Debug all props passed to this wrapper
  usePropDebugger(restProps, {
    componentName,
    logLevel,
    logProps,
    highlightDOMIssues: true
  });
  
  return <>{children}</>;
}

/**
 * HOC version for wrapping existing components
 */
export function withDebugWrapper<T extends Record<string, any>>(
  Component: React.ComponentType<T>,
  componentName: string,
  debugOptions: {
    logLevel?: 'none' | 'warn' | 'info' | 'debug';
    logProps?: boolean;
  } = {}
) {
  return function DebugWrappedComponent(props: T) {
    usePropDebugger(props, {
      componentName,
      logLevel: debugOptions.logLevel || 'warn',
      logProps: debugOptions.logProps || false,
      highlightDOMIssues: true
    });
    
    return <Component {...props} />;
  };
}

/**
 * Quick debug function to add to any component
 * Usage: debugComponentProps('ComponentName', props);
 */
export function debugComponentProps(
  componentName: string,
  props: Record<string, any>,
  options: {
    logLevel?: 'warn' | 'info' | 'debug';
    logAll?: boolean;
  } = {}
) {
  const { logLevel = 'warn', logAll = false } = options;
  
  if (process.env.NODE_ENV !== 'development') return;
  
  const customProps = Object.keys(props).filter(key => 
    !key.startsWith('data-') && 
    !key.startsWith('aria-') &&
    !['className', 'style', 'children', 'onClick', 'onChange', 'onSubmit', 'id', 'key', 'ref'].includes(key)
  );
  
  if (logAll || customProps.length > 0) {
    console.group(`🔍 [${componentName}] Prop Debug`);
    
    if (logAll) {
      console.log('All props:', props);
    }
    
    if (customProps.length > 0) {
      console.warn('Custom props detected:', customProps);
      
      // Highlight DAWN-specific props that might cause issues
      const dawnProps = customProps.filter(key => 
        ['globalEntropy', 'consciousnessLevel', 'quantumState', 'entropyLevel', 'motionProps'].includes(key)
      );
      
      if (dawnProps.length > 0) {
        console.warn('⚠️  DAWN props that might cause DOM warnings:', dawnProps);
        console.info('💡 Solution: Use SafeMotionDiv or filter these props');
      }
    }
    
    console.groupEnd();
  }
}

/**
 * Runtime checker for problematic prop patterns
 */
export function checkPropPatterns(
  componentName: string,
  props: Record<string, any>
) {
  if (process.env.NODE_ENV !== 'development') return;
  
  const issues: string[] = [];
  
  // Check for motion props being passed to DOM
  if (props.animate && typeof props.type === 'string') {
    issues.push('Motion props (animate, initial, etc.) passed to DOM element');
  }
  
  // Check for DAWN custom props
  const dawnProps = ['globalEntropy', 'consciousnessLevel', 'quantumState'];
  const foundDawnProps = dawnProps.filter(prop => props.hasOwnProperty(prop));
  if (foundDawnProps.length > 0) {
    issues.push(`DAWN custom props detected: ${foundDawnProps.join(', ')}`);
  }
  
  // Check for function props with non-standard names
  const functionProps = Object.entries(props)
    .filter(([key, value]) => typeof value === 'function' && !key.startsWith('on'))
    .map(([key]) => key);
  
  if (functionProps.length > 0) {
    issues.push(`Non-standard function props: ${functionProps.join(', ')}`);
  }
  
  if (issues.length > 0) {
    console.warn(`[${componentName}] Potential prop issues:`, issues);
  }
}

export default DebugWrapper; 