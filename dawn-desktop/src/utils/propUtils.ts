import React from 'react';
import { filterProps } from '../components/system/SafeMotionDiv';

/**
 * Safely clones a React element and passes custom props only to React components,
 * not DOM elements. This prevents React warnings about unknown DOM properties.
 */
export function safeCloneElement(
  element: React.ReactElement,
  customProps: Record<string, any>
): React.ReactElement {
  if (!React.isValidElement(element)) {
    return element;
  }

  // Check if it's a DOM element (string type) or a React component
  if (typeof element.type === 'string') {
    // It's a DOM element (div, span, etc), don't pass custom props
    return element;
  }

  // It's a React component, safe to pass custom props
  try {
    return React.cloneElement(element, customProps);
  } catch (error) {
    console.warn('Failed to pass custom props to component:', element.type, error);
    return element;
  }
}

/**
 * Safely passes props to children, filtering out custom props from DOM elements
 */
export function safePassPropsToChildren(
  children: React.ReactNode,
  customProps: Record<string, any>
): React.ReactNode {
  return React.Children.map(children, (child) => {
    if (!React.isValidElement(child)) {
      return child;
    }
    
    return safeCloneElement(child, customProps);
  });
}

/**
 * Wraps motion component props to ensure only valid motion props are passed
 */
export function safeMotionProps(props: Record<string, any>) {
  const { motionProps, domProps } = filterProps(props);
  return { motionProps, domProps };
}

/**
 * Higher-order component that filters props before passing to motion components
 */
export function withSafeProps<T extends Record<string, any>>(
  WrappedComponent: React.ComponentType<T>
) {
  return React.forwardRef<any, T>((props, ref) => {
    const { motionProps, domProps } = filterProps(props);
    const safeProps = { ...domProps, ...motionProps } as T;
    
    return React.createElement(WrappedComponent, { ref, ...safeProps });
  });
}

/**
 * Check if a value is a valid React component (not a DOM element)
 */
export function isReactComponent(element: React.ReactElement): boolean {
  return typeof element.type !== 'string';
}

/**
 * Check if a value is a DOM element (string type)
 */
export function isDOMElement(element: React.ReactElement): boolean {
  return typeof element.type === 'string';
} 