import React, { ReactNode } from 'react';
import { cn } from '../lib/utils';

export interface ModuleTemplateProps {
  title?: ReactNode;
  headerActions?: ReactNode;
  children?: ReactNode; // Main content area
  footer?: ReactNode;
  leftPanel?: ReactNode;
  rightPanel?: ReactNode;
  className?: string;
  style?: React.CSSProperties;
  statusBar?: ReactNode;
  // Any additional props
  [key: string]: any;
}

/**
 * Slot-based, glassmorphic module template for DAWN modules.
 *
 * Usage:
 * <ModuleTemplate
 *   title="Neural Core"
 *   headerActions={<Button>...</Button>}
 *   leftPanel={<Sidebar />}
 *   rightPanel={<Tools />}
 *   footer={<Footer />}
 *   statusBar={<StatusBar />}
 * >
 *   <MainContent />
 * </ModuleTemplate>
 */
export function ModuleTemplate({
  title,
  headerActions,
  children,
  footer,
  leftPanel,
  rightPanel,
  className,
  style,
  statusBar,
  ...props
}: ModuleTemplateProps) {
  return (
    <div
      className={cn(
        'glass-base rounded-2xl shadow-glow-md overflow-hidden flex flex-col relative',
        className
      )}
      style={style}
      {...props}
    >
      {/* Header */}
      {(title || headerActions) && (
        <div className="flex items-center justify-between px-6 py-3 border-b border-white/10 bg-gradient-to-b from-white/5 to-transparent backdrop-blur-md z-10">
          <div className="font-semibold text-lg text-white/80 truncate">{title}</div>
          <div className="flex gap-2">{headerActions}</div>
        </div>
      )}
      <div className="flex flex-1 min-h-0">
        {/* Left Panel */}
        {leftPanel && (
          <aside className="w-48 min-w-[3.5rem] max-w-xs border-r border-white/10 bg-white/5 backdrop-blur-md flex-shrink-0 z-10">
            {leftPanel}
          </aside>
        )}
        {/* Main Content */}
        <main className="flex-1 p-6 overflow-auto relative z-0">
          {children}
        </main>
        {/* Right Panel */}
        {rightPanel && (
          <aside className="w-48 min-w-[3.5rem] max-w-xs border-l border-white/10 bg-white/5 backdrop-blur-md flex-shrink-0 z-10">
            {rightPanel}
          </aside>
        )}
      </div>
      {/* Footer */}
      {(footer || statusBar) && (
        <div className="border-t border-white/10 bg-gradient-to-t from-white/5 to-transparent px-6 py-2 flex items-center justify-between min-h-[2.5rem]">
          <div>{footer}</div>
          <div>{statusBar}</div>
        </div>
      )}
    </div>
  );
} 