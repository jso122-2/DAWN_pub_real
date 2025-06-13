import { useEffect } from 'react';

// Standard DOM props that are safe to pass to DOM elements
const STANDARD_DOM_PROPS = new Set([
  // HTML Global Attributes
  'accessKey', 'autoFocus', 'className', 'contentEditable', 'contextMenu',
  'dir', 'draggable', 'hidden', 'id', 'lang', 'spellCheck', 'style',
  'tabIndex', 'title', 'translate',
  
  // Event Handlers
  'onAbort', 'onBlur', 'onCanPlay', 'onCanPlayThrough', 'onChange', 'onClick',
  'onContextMenu', 'onCopy', 'onCut', 'onDoubleClick', 'onDrag', 'onDragEnd',
  'onDragEnter', 'onDragExit', 'onDragLeave', 'onDragOver', 'onDragStart',
  'onDrop', 'onDurationChange', 'onEmptied', 'onEncrypted', 'onEnded',
  'onError', 'onFocus', 'onInput', 'onInvalid', 'onKeyDown', 'onKeyPress',
  'onKeyUp', 'onLoad', 'onLoadedData', 'onLoadedMetadata', 'onLoadStart',
  'onMouseDown', 'onMouseEnter', 'onMouseLeave', 'onMouseMove', 'onMouseOut',
  'onMouseOver', 'onMouseUp', 'onPaste', 'onPause', 'onPlay', 'onPlaying',
  'onProgress', 'onRateChange', 'onScroll', 'onSeeked', 'onSeeking',
  'onSelect', 'onStalled', 'onSubmit', 'onSuspend', 'onTimeUpdate',
  'onToggle', 'onVolumeChange', 'onWaiting', 'onWheel',
  
  // Form-specific
  'accept', 'acceptCharset', 'action', 'allowFullScreen', 'alt', 'async',
  'autoComplete', 'autoPlay', 'capture', 'cellPadding', 'cellSpacing',
  'challenge', 'charSet', 'checked', 'cite', 'classID', 'cols', 'colSpan',
  'content', 'controls', 'coords', 'crossOrigin', 'data', 'dateTime',
  'default', 'defer', 'disabled', 'download', 'encType', 'form', 'formAction',
  'formEncType', 'formMethod', 'formNoValidate', 'formTarget', 'frameBorder',
  'headers', 'height', 'high', 'href', 'hrefLang', 'htmlFor', 'httpEquiv',
  'icon', 'inputMode', 'integrity', 'is', 'itemID', 'itemProp', 'itemRef',
  'itemScope', 'itemType', 'keyParams', 'keyType', 'kind', 'label', 'list',
  'loop', 'low', 'manifest', 'marginHeight', 'marginWidth', 'max', 'maxLength',
  'media', 'mediaGroup', 'method', 'min', 'minLength', 'multiple', 'muted',
  'name', 'nonce', 'noValidate', 'open', 'optimum', 'pattern', 'placeholder',
  'playsInline', 'poster', 'preload', 'radioGroup', 'readOnly', 'rel',
  'required', 'reversed', 'role', 'rows', 'rowSpan', 'sandbox', 'scope',
  'scoped', 'scrolling', 'security', 'selected', 'shape', 'size', 'sizes',
  'span', 'src', 'srcDoc', 'srcLang', 'srcSet', 'start', 'step', 'summary',
  'target', 'type', 'useMap', 'value', 'width', 'wmode', 'wrap',
  
  // React-specific
  'children', 'key', 'ref', 'dangerouslySetInnerHTML',
  
  // ARIA attributes (common ones)
  'aria-label', 'aria-labelledby', 'aria-describedby', 'aria-hidden',
  'aria-expanded', 'aria-selected', 'aria-checked', 'aria-disabled',
  'aria-required', 'aria-invalid', 'aria-live', 'aria-atomic'
]);

// Custom props that are commonly used in the DAWN ecosystem
const DAWN_CUSTOM_PROPS = new Set([
  'globalEntropy', 'consciousnessLevel', 'quantumState', 'neuralActivity',
  'entropyLevel', 'breathingPreset', 'floatingPreset', 'syncGroup',
  'orbitalGroup', 'moduleId', 'groupId', 'isActive', 'isCritical',
  'enableFloating', 'enableBreathing', 'glowIntensity', 'particleCount',
  'connectionPorts', 'dataFlow', 'processingLoad', 'healthStatus',
  'quantumCoherence', 'memoryFragments', 'tickNumber', 'scup', 'entropy',
  'mood', 'motionProps', 'emitter', 'animationControls', 'allModules'
]);

interface PropDebugOptions {
  componentName: string;
  logLevel?: 'none' | 'warn' | 'info' | 'debug';
  logProps?: boolean;
  logCustomProps?: boolean;
  highlightDOMIssues?: boolean;
}

/**
 * Debug hook to identify problematic prop passing
 */
export function usePropDebugger(
  props: Record<string, any>,
  options: PropDebugOptions
) {
  const {
    componentName,
    logLevel = 'warn',
    logProps = false,
    logCustomProps = true,
    highlightDOMIssues = true
  } = options;

  useEffect(() => {
    if (logLevel === 'none') return;

    const propKeys = Object.keys(props);
    const customProps: string[] = [];
    const potentialDOMIssues: string[] = [];

    // Analyze each prop
    propKeys.forEach(key => {
      // Skip data-* and aria-* attributes as they're always valid
      if (key.startsWith('data-') || key.startsWith('aria-')) {
        return;
      }

      // Check if it's a standard DOM prop
      if (!STANDARD_DOM_PROPS.has(key)) {
        customProps.push(key);
        
        // Check if it's a known DAWN custom prop that might be passed to DOM
        if (DAWN_CUSTOM_PROPS.has(key)) {
          potentialDOMIssues.push(key);
        }
      }
    });

    // Log component props if requested
    if (logProps && (logLevel === 'info' || logLevel === 'debug')) {
      console.log(`[PropDebugger] ${componentName} - All props:`, props);
    }

    // Log custom props
    if (logCustomProps && customProps.length > 0) {
      if (logLevel === 'debug' || logLevel === 'info') {
        console.info(`[PropDebugger] ${componentName} - Custom props:`, customProps);
      } else if (logLevel === 'warn') {
        console.warn(`[PropDebugger] ${componentName} - Custom props detected:`, customProps);
      }
    }

    // Highlight potential DOM issues
    if (highlightDOMIssues && potentialDOMIssues.length > 0) {
      console.warn(
        `[PropDebugger] ${componentName} - POTENTIAL DOM ISSUES! These DAWN props might be passed to DOM elements:`,
        potentialDOMIssues
      );
      console.warn(
        `  💡 Solution: Use SafeMotionDiv or filter these props before passing to DOM elements`
      );
    }

    // Provide suggestions for common issues
    if (potentialDOMIssues.includes('globalEntropy')) {
      console.warn(
        `[PropDebugger] ${componentName} - 🔧 Fix globalEntropy: Use SafeMotionDiv from '@/components/system/SafeMotionDiv'`
      );
    }

    if (potentialDOMIssues.includes('motionProps')) {
      console.warn(
        `[PropDebugger] ${componentName} - 🔧 Fix motionProps: Destructure and pass only motion-specific props to motion components`
      );
    }

  }, [props, componentName, logLevel, logProps, logCustomProps, highlightDOMIssues]);
}

/**
 * Quick debug function for immediate use in components
 */
export function debugProps(
  componentName: string,
  props: Record<string, any>,
  logLevel: 'warn' | 'info' | 'debug' = 'warn'
) {
  const customProps = Object.keys(props).filter(key => 
    !key.startsWith('data-') && 
    !key.startsWith('aria-') &&
    !STANDARD_DOM_PROPS.has(key)
  );
  
  const dawnCustomProps = customProps.filter(key => DAWN_CUSTOM_PROPS.has(key));
  
  if (customProps.length > 0) {
    if (logLevel === 'debug' || logLevel === 'info') {
      console.log(`[${componentName}] Props:`, props);
    }
    
    console.warn(`[${componentName}] Custom props:`, customProps);
    
    if (dawnCustomProps.length > 0) {
      console.warn(
        `[${componentName}] ⚠️  DAWN custom props that might cause DOM warnings:`,
        dawnCustomProps
      );
    }
  }
}

/**
 * Filter props to separate DOM-safe props from custom props
 */
export function filterDOMProps(props: Record<string, any>): {
  domProps: Record<string, any>;
  customProps: Record<string, any>;
} {
  const domProps: Record<string, any> = {};
  const customProps: Record<string, any> = {};
  
  Object.entries(props).forEach(([key, value]) => {
    if (
      key.startsWith('data-') || 
      key.startsWith('aria-') || 
      STANDARD_DOM_PROPS.has(key)
    ) {
      domProps[key] = value;
    } else {
      customProps[key] = value;
    }
  });
  
  return { domProps, customProps };
}

// Export constants for use in other files
export { STANDARD_DOM_PROPS, DAWN_CUSTOM_PROPS }; 