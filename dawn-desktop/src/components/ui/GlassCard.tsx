import { cn } from '../../lib/utils'

export function GlassCard({ 
  children, 
  className,
  glow = false 
}: { 
  children: React.ReactNode
  className?: string
  glow?: boolean
}) {
  return (
    <div className={cn(
      "glass-base rounded-xl p-tissue",
      glow && "pulse-glow",
      className
    )}>
      {children}
    </div>
  )
} 