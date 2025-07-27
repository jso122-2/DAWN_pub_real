import React from 'react';
import './layout_manager.css';

interface GridItemProps {
  children: React.ReactNode;
  className?: string;
}

interface PanelGroupProps {
  title: string;
  children: React.ReactNode;
  className?: string;
}

// Grid item wrapper for individual panels
export const GridItem: React.FC<GridItemProps> = ({ children, className = '' }) => {
  return (
    <div className={`grid-item ${className}`}>
      {children}
    </div>
  );
};

// Panel group wrapper with section titles
export const PanelGroup: React.FC<PanelGroupProps> = ({ title, children, className = '' }) => {
  return (
    <div className={`panel-group ${className}`}>
      <div className="panel-group-header">
        <h2 className="panel-group-title">{title}</h2>
      </div>
      <div className="panel-group-content">
        {children}
      </div>
    </div>
  );
};

// Main layout container props
interface LayoutManagerProps {
  children: React.ReactNode;
  className?: string;
}

// Core layout manager component
export const LayoutManager: React.FC<LayoutManagerProps> = ({ children, className = '' }) => {
  return (
    <div className={`layout-manager ${className}`}>
      <div className="grid-container">
        {children}
      </div>
    </div>
  );
};

// Pre-configured column wrappers for standard DAWN layout
interface CognitionColumnProps {
  children: React.ReactNode;
}

interface SymbolicColumnProps {
  children: React.ReactNode;
}

interface ReflectionColumnProps {
  children: React.ReactNode;
}

export const CognitionColumn: React.FC<CognitionColumnProps> = ({ children }) => {
  return (
    <div className="cognition-column">
      <PanelGroup title="Cognition Core">
        {children}
      </PanelGroup>
    </div>
  );
};

export const SymbolicColumn: React.FC<SymbolicColumnProps> = ({ children }) => {
  return (
    <div className="symbolic-column">
      <PanelGroup title="Symbolic Layer">
        {children}
      </PanelGroup>
    </div>
  );
};

export const ReflectionColumn: React.FC<ReflectionColumnProps> = ({ children }) => {
  return (
    <div className="reflection-column">
      <PanelGroup title="Reflection Stream">
        {children}
      </PanelGroup>
    </div>
  );
};

// Complete DAWN layout with all three columns
interface DAWNLayoutProps {
  cognitionContent: React.ReactNode;
  symbolicContent: React.ReactNode;
  reflectionContent: React.ReactNode;
}

export const DAWNLayout: React.FC<DAWNLayoutProps> = ({
  cognitionContent,
  symbolicContent,
  reflectionContent
}) => {
  return (
    <LayoutManager className="dawn-layout">
      <CognitionColumn>
        {cognitionContent}
      </CognitionColumn>
      
      <SymbolicColumn>
        {symbolicContent}
      </SymbolicColumn>
      
      <ReflectionColumn>
        {reflectionContent}
      </ReflectionColumn>
    </LayoutManager>
  );
};

export default LayoutManager; 