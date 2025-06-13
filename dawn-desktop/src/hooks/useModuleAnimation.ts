import { useBreathing } from './useBreathing';
import { useFloating } from './useFloating';

export function useModuleAnimation({
  preset = 'calm',
  floating = 'gentle',
  syncGroup,
  entropy = 0,
  disabled = false,
  moduleId,
  groupId,
  customBreathing,
  customFloating,
}: {
  preset?: string;
  floating?: string;
  syncGroup?: string;
  entropy?: number;
  disabled?: boolean;
  moduleId?: string;
  groupId?: string;
  customBreathing?: any;
  customFloating?: any;
} = {}) {
  const breathingProps = useBreathing({
    preset,
    entropy,
    syncGroup,
    disabled,
    ...customBreathing,
  });
  const floatingProps = useFloating({
    preset: floating,
    moduleId,
    groupId,
    disabled,
    ...customFloating,
  });
  return {
    ...breathingProps,
    ...floatingProps,
  };
} 