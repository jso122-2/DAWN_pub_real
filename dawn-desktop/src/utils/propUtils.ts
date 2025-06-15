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

  // Check if it's a framer-motion component
  if (isMotionComponent(element)) {
    // It's a motion component, filter props appropriately
    const combinedProps = Object.assign({}, element.props, customProps);
    const { motionProps, domProps } = filterProps(combinedProps);
    return React.cloneElement(element, Object.assign({}, domProps, motionProps));
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
    
    // Filter out custom props for motion components and DOM elements to prevent warnings
    const filteredCustomProps = Object.keys(customProps).reduce((acc, key) => {
      // Only pass custom props to React components, not DOM elements or motion components
      if (typeof child.type !== 'string' && !isMotionComponent(child)) {
        acc[key] = customProps[key];
      }
      return acc;
    }, {} as Record<string, any>);
    
    // Apply safe prop passing
    const safeChild = safeCloneElement(child, filteredCustomProps);
    
    // If the child has children, recursively apply safe prop passing
    if (child.props.children) {
      const updatedChild = React.cloneElement(safeChild, {
        children: safePassPropsToChildren(child.props.children, customProps)
      });
      return updatedChild;
    }
    
    return safeChild;
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

/**
 * Check if a component is a framer-motion component
 */
export function isMotionComponent(element: React.ReactElement): boolean {
  if (!element.type) {
    return false;
  }
  
  // Check for motion component display name
  if (typeof element.type === 'object' && 'displayName' in element.type) {
    const displayName = (element.type as any).displayName;
    if (displayName && displayName.includes('motion.')) {
      return true;
    }
  }
  
  // Check for framer-motion component properties
  if (typeof element.type === 'object') {
    const type = element.type as any;
    // Check if it has motion-specific properties
    if (type.$$typeof || type._payload || type.render) {
      // Check the element's props for motion-specific keys
      const motionKeys = ['animate', 'initial', 'exit', 'variants', 'whileHover', 'whileTap'];
      if (element.props && motionKeys.some(key => key in element.props)) {
        return true;
      }
    }
  }
  
  return false;
} 