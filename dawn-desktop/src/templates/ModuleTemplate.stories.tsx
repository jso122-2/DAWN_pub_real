import React from 'react';
import { ModuleTemplate } from './ModuleTemplate';
import type { Meta, StoryObj } from '@storybook/react';

const meta: Meta<typeof ModuleTemplate> = {
  title: 'Templates/ModuleTemplate',
  component: ModuleTemplate,
};
export default meta;

type Story = StoryObj<typeof ModuleTemplate>;

export const Default: Story = {
  args: {
    title: 'Neural Core',
    children: <div className="text-neural-400">Main content area</div>,
  },
};

export const WithHeaderActions: Story = {
  args: {
    title: 'Consciousness Module',
    headerActions: <button className="glass-consciousness px-3 py-1 rounded">⚡ Action</button>,
    children: <div className="text-consciousness-400">Consciousness content</div>,
  },
};

export const WithSidePanels: Story = {
  args: {
    title: 'Process Monitor',
    leftPanel: <div className="p-2 text-xs">Sidebar<br/>Info</div>,
    rightPanel: <div className="p-2 text-xs">Tools<br/>Panel</div>,
    children: <div className="text-process-400">Process content</div>,
  },
};

export const WithFooterAndStatus: Story = {
  args: {
    title: 'Diagnostic Module',
    footer: <span className="text-alert-400">System Alert: None</span>,
    statusBar: <span className="text-xs text-gray-400">Status: OK</span>,
    children: <div className="text-diagnostic-400">Diagnostics content</div>,
  },
};

export const AllSlots: Story = {
  args: {
    title: 'Full Example',
    headerActions: <button className="glass-active px-2 py-1 rounded">Settings</button>,
    leftPanel: <div className="p-2 text-xs">Left Panel</div>,
    rightPanel: <div className="p-2 text-xs">Right Panel</div>,
    footer: <span className="text-xs">Footer Area</span>,
    statusBar: <span className="text-xs text-green-400">Online</span>,
    children: <div className="text-base">All slots are filled for maximum flexibility.</div>,
  },
}; 