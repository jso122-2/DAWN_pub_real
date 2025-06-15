import React from 'react';
import { motion, MotionProps } from 'framer-motion';

interface SafeMotionDivProps extends MotionProps {
  globalEntropy?: number;
  motionProps?: any;
  children?: React.ReactNode;
  [key: string]: any;
}

// List of known custom props that should be filtered out
const CUSTOM_PROPS = [
  'globalEntropy',
  'motionProps',
  'consciousnessLevel',
  'consciousnessState',
  'neuralActivity',
  'entropyLevel',
  'breathingPreset',
  'floatingPreset',
  'syncGroup',
  'orbitalGroup',
  'moduleId',
  'groupId',
  'isActive',
  'isCritical',
  'enableFloating',
  'enableBreathing',
  'glowIntensity',
  'particleCount',
  'connectionPorts',
  'dataFlow',
  'processingLoad',
  'healthStatus',
  'systemUnity',
  'neuralConnections'
];

// Extract motion-specific props
const MOTION_PROPS = [
  'animate',
  'initial',
  'exit',
  'transition',
  'variants',
  'whileHover',
  'whileTap',
  'whileDrag',
  'whileFocus',
  'whileInView',
  'drag',
  'dragConstraints',
  'dragElastic',
  'dragMomentum',
  'dragTransition',
  'dragPropagation',
  'dragControls',
  'onDrag',
  'onDragStart',
  'onDragEnd',
  'onAnimationStart',
  'onAnimationComplete',
  'onUpdate',
  'transformTemplate',
  'layout',
  'layoutId',
  'layoutDependency',
  'onLayoutAnimationStart',
  'onLayoutAnimationComplete',
  'onViewportEnter',
  'onViewportLeave'
];

/**
 * Filters props to separate custom props, motion props, and DOM props
 */
export function filterProps(props: Record<string, any>) {
  const motionProps: Record<string, any> = {};
  const domProps: Record<string, any> = {};
  const customProps: Record<string, any> = {};

  Object.keys(props).forEach(key => {
    if (CUSTOM_PROPS.includes(key)) {
      customProps[key] = props[key];
    } else if (MOTION_PROPS.includes(key)) {
      motionProps[key] = props[key];
    } else {
      domProps[key] = props[key];
    }
  });

  return { motionProps, domProps, customProps };
}

export const SafeMotionDiv: React.FC<SafeMotionDivProps> = (props) => {
  const { motionProps, domProps } = filterProps(props);
  
  return (
    <motion.div {...domProps} {...motionProps}>
      {props.children}
    </motion.div>
  );
};

// Additional safe motion components for other HTML elements
export const SafeMotionSpan: React.FC<SafeMotionDivProps> = (props) => {
  const { motionProps, domProps } = filterProps(props);
  
  return (
    <motion.span {...domProps} {...motionProps}>
      {props.children}
    </motion.span>
  );
};

export const SafeMotionButton: React.FC<SafeMotionDivProps> = (props) => {
  const { motionProps, domProps } = filterProps(props);
  
  return (
    <motion.button {...domProps} {...motionProps}>
      {props.children}
    </motion.button>
  );
};

export const SafeMotionSection: React.FC<SafeMotionDivProps> = (props) => {
  const { motionProps, domProps } = filterProps(props);
  
  return (
    <motion.section {...domProps} {...motionProps}>
      {props.children}
    </motion.section>
  );
};

export const SafeMotionNav: React.FC<SafeMotionDivProps> = (props) => {
  const { motionProps, domProps } = filterProps(props);
  
  return (
    <motion.nav {...domProps} {...motionProps}>
      {props.children}
    </motion.nav>
  );
};

// Generic safe motion component factory
export function createSafeMotionComponent<T extends keyof JSX.IntrinsicElements>(
  element: T
) {
  return React.forwardRef<HTMLElement, SafeMotionDivProps>((props, ref) => {
    const { motionProps, domProps } = filterProps(props);
    const MotionComponent = (motion as any)[element];
    
    return (
      <MotionComponent ref={ref} {...domProps} {...motionProps}>
        {props.children}
      </MotionComponent>
    );
  });
}

// Export the most commonly used safe motion components
export const SafeMotion = {
  div: SafeMotionDiv,
  span: SafeMotionSpan,
  button: SafeMotionButton,
  section: SafeMotionSection,
  nav: SafeMotionNav,
  // Factory for creating custom safe motion components
  create: createSafeMotionComponent
}; 