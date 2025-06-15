import { cn } from '../../lib/utils'

interface GlassButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'base' | 'consciousness' | 'neural' | 'alert'
  size?: 'sm' | 'md' | 'lg'
}

export function GlassButton({ 
  variant = 'base', 
  size = 'md',
  className,
  children,
  ...props 
}: GlassButtonProps) {
  const sizeClasses = {
    sm: 'px-molecule py-atom text-sm',
    md: 'px-tissue py-molecule',
    lg: 'px-organ py-cell text-lg'
  }

  return (
    <button
      className={cn(
        'glass-base rounded-lg font-medium transition-all',
        'hover:scale-105 active:scale-95',
        variant === 'consciousness' && 'glass-consciousness text-consciousness-300',
        variant === 'neural' && 'glass-neural text-neural-300',
        variant === 'alert' && 'glass-critical text-alert-300',
        sizeClasses[size],
        className
      )}
      {...props}
    >
      {children}
    </button>
  )
} 