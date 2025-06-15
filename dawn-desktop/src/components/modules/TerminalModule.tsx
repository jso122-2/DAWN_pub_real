import { ConsciousModule } from './ConsciousModule'

interface TerminalModuleProps {
  id: string
  [key: string]: any
}

export function TerminalModule({ id, ...props }: TerminalModuleProps) {
  return (
    <ConsciousModule
      moduleId={`terminal-${id}`}
      breathingPreset="consciousness"
      floatingPreset="active"
      entropy={0.5} // Terminal has medium entropy
      syncGroup="consciousness-systems"
    >
      <div className="glass-consciousness rounded-2xl p-tissue min-h-[400px]">
        {/* Terminal content */}
      </div>
    </ConsciousModule>
  )
} 