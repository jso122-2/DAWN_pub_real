#!/usr/bin/env python3
"""
rebloom_genealogy_widget.py - Tkinter Widget for Rebloom Genealogy Display
Provides visual display of bloom family trees and genealogy information
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import math
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

try:
    from integration.rebloom_tracker_integration import IntegratedRebloomSystem
    INTEGRATION_AVAILABLE = True
except ImportError:
    INTEGRATION_AVAILABLE = False


class RebloomGenealogyWidget(ttk.Frame):
    """
    Widget for displaying rebloom genealogy information in the DAWN GUI
    """
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Integration system
        self.rebloom_system = None
        if INTEGRATION_AVAILABLE:
            try:
                self.rebloom_system = IntegratedRebloomSystem()
                print("[GenealogyWidget] ✅ Connected to RebloomSystem")
            except Exception as e:
                print(f"[GenealogyWidget] ⚠️ Failed to connect: {e}")
        
        # UI state
        self.selected_bloom = None
        self.auto_refresh = tk.BooleanVar(value=True)
        self.refresh_interval = 5000  # 5 seconds
        self.last_update = None
        
        # Data cache
        self.family_stats = {}
        self.genealogy_cache = {}
        self.patterns_cache = {}
        
        # Create UI
        self.create_widgets()
        self.setup_layout()
        
        # Start auto-refresh if enabled
        self.schedule_refresh()
    
    def create_widgets(self):
        """Create the widget components"""
        
        # Header frame
        self.header_frame = ttk.Frame(self)
        
        # Title
        self.title_label = ttk.Label(
            self.header_frame, 
            text="🌸 Rebloom Genealogy", 
            font=('Arial', 14, 'bold')
        )
        
        # Status indicator
        self.status_label = ttk.Label(
            self.header_frame,
            text="●" if self.rebloom_system else "○",
            foreground="green" if self.rebloom_system else "red",
            font=('Arial', 12)
        )
        
        # Refresh controls
        self.refresh_frame = ttk.Frame(self.header_frame)
        
        self.auto_refresh_check = ttk.Checkbutton(
            self.refresh_frame,
            text="Auto-refresh",
            variable=self.auto_refresh,
            command=self.toggle_auto_refresh
        )
        
        self.refresh_button = ttk.Button(
            self.refresh_frame,
            text="Refresh",
            command=self.refresh_data,
            width=8
        )
        
        # Main content notebook
        self.notebook = ttk.Notebook(self)
        
        # Family Tree tab
        self.tree_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tree_frame, text="Family Trees")
        self.create_tree_tab()
        
        # Statistics tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistics")
        self.create_stats_tab()
        
        # Patterns tab
        self.patterns_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.patterns_frame, text="Patterns")
        self.create_patterns_tab()
        
        # Genealogy tab
        self.genealogy_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.genealogy_frame, text="Genealogy")
        self.create_genealogy_tab()
    
    def create_tree_tab(self):
        """Create the family tree visualization tab"""
        
        # Tree selection
        selection_frame = ttk.Frame(self.tree_frame)
        selection_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(selection_frame, text="Root Bloom:").pack(side='left')
        
        self.root_combo = ttk.Combobox(selection_frame, width=20, state='readonly')
        self.root_combo.pack(side='left', padx=(5, 10))
        self.root_combo.bind('<<ComboboxSelected>>', self.on_root_selected)
        
        self.show_all_button = ttk.Button(
            selection_frame,
            text="Show All",
            command=self.show_all_trees,
            width=10
        )
        self.show_all_button.pack(side='left')
        
        # Tree display canvas
        canvas_frame = ttk.Frame(self.tree_frame)
        canvas_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create canvas with scrollbars
        self.tree_canvas = tk.Canvas(
            canvas_frame, 
            bg='white',
            scrollregion=(0, 0, 1000, 1000)
        )
        
        self.tree_h_scroll = ttk.Scrollbar(
            canvas_frame, 
            orient='horizontal', 
            command=self.tree_canvas.xview
        )
        self.tree_v_scroll = ttk.Scrollbar(
            canvas_frame, 
            orient='vertical', 
            command=self.tree_canvas.yview
        )
        
        self.tree_canvas.configure(
            xscrollcommand=self.tree_h_scroll.set,
            yscrollcommand=self.tree_v_scroll.set
        )
        
        # Pack scrollbars and canvas
        self.tree_h_scroll.pack(side='bottom', fill='x')
        self.tree_v_scroll.pack(side='right', fill='y')
        self.tree_canvas.pack(side='left', fill='both', expand=True)
        
        # Bind canvas events
        self.tree_canvas.bind('<Button-1>', self.on_canvas_click)
        self.tree_canvas.bind('<Motion>', self.on_canvas_motion)
    
    def create_stats_tab(self):
        """Create the statistics tab"""
        
        # Global stats frame
        global_frame = ttk.LabelFrame(self.stats_frame, text="Global Statistics", padding=10)
        global_frame.pack(fill='x', padx=5, pady=5)
        
        # Create labels for global stats
        self.global_stats_vars = {
            'total_blooms': tk.StringVar(value="Total Blooms: 0"),
            'total_roots': tk.StringVar(value="Root Families: 0"),
            'max_depth': tk.StringVar(value="Max Depth: 0"),
            'total_reblooms': tk.StringVar(value="Total Reblooms: 0"),
            'average_depth': tk.StringVar(value="Average Depth: 0.0")
        }
        
        for var in self.global_stats_vars.values():
            label = ttk.Label(global_frame, textvariable=var, font=('Arial', 10))
            label.pack(anchor='w', pady=2)
        
        # Entropy stats frame
        entropy_frame = ttk.LabelFrame(self.stats_frame, text="Entropy Statistics", padding=10)
        entropy_frame.pack(fill='x', padx=5, pady=5)
        
        self.entropy_stats_vars = {
            'max_positive': tk.StringVar(value="Max Positive Drift: 0.0"),
            'max_negative': tk.StringVar(value="Max Negative Drift: 0.0"),
            'average_drift': tk.StringVar(value="Average Drift: 0.0")
        }
        
        for var in self.entropy_stats_vars.values():
            label = ttk.Label(entropy_frame, textvariable=var, font=('Arial', 10))
            label.pack(anchor='w', pady=2)
        
        # Depth distribution
        depth_frame = ttk.LabelFrame(self.stats_frame, text="Depth Distribution", padding=10)
        depth_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create treeview for depth distribution
        self.depth_tree = ttk.Treeview(
            depth_frame,
            columns=('Count', 'Percentage'),
            show='tree headings',
            height=8
        )
        
        self.depth_tree.heading('#0', text='Depth')
        self.depth_tree.heading('Count', text='Count')
        self.depth_tree.heading('Percentage', text='%')
        
        self.depth_tree.column('#0', width=80)
        self.depth_tree.column('Count', width=80)
        self.depth_tree.column('Percentage', width=80)
        
        self.depth_tree.pack(fill='both', expand=True)
    
    def create_patterns_tab(self):
        """Create the patterns analysis tab"""
        
        # Recent patterns frame
        recent_frame = ttk.LabelFrame(self.patterns_frame, text="Recent Rebloom Patterns", padding=10)
        recent_frame.pack(fill='x', padx=5, pady=5)
        
        self.pattern_vars = {
            'increasing_entropy': tk.StringVar(value="Increasing Entropy: 0"),
            'decreasing_entropy': tk.StringVar(value="Decreasing Entropy: 0"),
            'stable_entropy': tk.StringVar(value="Stable Entropy: 0"),
            'high_volatility': tk.StringVar(value="High Volatility: 0"),
            'entropy_trend': tk.StringVar(value="Trend: Unknown"),
        }
        
        for var in self.pattern_vars.values():
            label = ttk.Label(recent_frame, textvariable=var, font=('Arial', 10))
            label.pack(anchor='w', pady=2)
        
        # Source distribution frame
        source_frame = ttk.LabelFrame(self.patterns_frame, text="Rebloom Sources", padding=10)
        source_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.source_tree = ttk.Treeview(
            source_frame,
            columns=('Count', 'Percentage'),
            show='tree headings'
        )
        
        self.source_tree.heading('#0', text='Source')
        self.source_tree.heading('Count', text='Count')
        self.source_tree.heading('Percentage', text='%')
        
        self.source_tree.pack(fill='both', expand=True)
    
    def create_genealogy_tab(self):
        """Create the bloom genealogy lookup tab"""
        
        # Bloom selection
        selection_frame = ttk.Frame(self.genealogy_frame)
        selection_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(selection_frame, text="Bloom ID:").pack(side='left')
        
        self.bloom_entry = ttk.Entry(selection_frame, width=20)
        self.bloom_entry.pack(side='left', padx=(5, 10))
        self.bloom_entry.bind('<Return>', self.lookup_bloom)
        
        self.lookup_button = ttk.Button(
            selection_frame,
            text="Lookup",
            command=self.lookup_bloom,
            width=10
        )
        self.lookup_button.pack(side='left')
        
        # Results frame
        results_frame = ttk.Frame(self.genealogy_frame)
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create text widget for genealogy display
        self.genealogy_text = tk.Text(
            results_frame,
            wrap='word',
            font=('Courier', 10),
            height=20
        )
        
        genealogy_scroll = ttk.Scrollbar(
            results_frame,
            orient='vertical',
            command=self.genealogy_text.yview
        )
        
        self.genealogy_text.configure(yscrollcommand=genealogy_scroll.set)
        
        genealogy_scroll.pack(side='right', fill='y')
        self.genealogy_text.pack(side='left', fill='both', expand=True)
    
    def setup_layout(self):
        """Setup the widget layout"""
        
        # Pack header components
        self.title_label.pack(side='left')
        self.status_label.pack(side='left', padx=(10, 0))
        
        self.auto_refresh_check.pack(side='left')
        self.refresh_button.pack(side='left', padx=(5, 0))
        
        self.refresh_frame.pack(side='right')
        
        # Pack main components
        self.header_frame.pack(fill='x', padx=5, pady=5)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
    
    def refresh_data(self):
        """Refresh all data from the rebloom system"""
        if not self.rebloom_system:
            self.show_no_connection_message()
            return
        
        try:
            # Update family stats
            self.family_stats = self.rebloom_system.get_family_statistics()
            
            # Update patterns
            self.patterns_cache = self.rebloom_system.get_rebloom_patterns()
            
            # Update UI components
            self.update_stats_display()
            self.update_patterns_display()
            self.update_tree_roots()
            
            # Update status
            self.last_update = datetime.now()
            self.status_label.configure(foreground="green")
            
            print(f"[GenealogyWidget] 🔄 Data refreshed at {self.last_update.strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"[GenealogyWidget] ⚠️ Refresh error: {e}")
            self.status_label.configure(foreground="red")
            messagebox.showerror("Refresh Error", f"Failed to refresh data: {e}")
    
    def update_stats_display(self):
        """Update the statistics tab display"""
        if not self.family_stats:
            return
        
        # Update global stats
        self.global_stats_vars['total_blooms'].set(f"Total Blooms: {self.family_stats.get('total_blooms', 0)}")
        self.global_stats_vars['total_roots'].set(f"Root Families: {self.family_stats.get('total_roots', 0)}")
        self.global_stats_vars['max_depth'].set(f"Max Depth: {self.family_stats.get('max_depth', 0)}")
        self.global_stats_vars['total_reblooms'].set(f"Total Reblooms: {self.family_stats.get('total_reblooms', 0)}")
        self.global_stats_vars['average_depth'].set(f"Average Depth: {self.family_stats.get('average_depth', 0):.2f}")
        
        # Update entropy stats
        entropy_stats = self.family_stats.get('entropy_stats', {})
        self.entropy_stats_vars['max_positive'].set(f"Max Positive Drift: {entropy_stats.get('max_positive_drift', 0):.3f}")
        self.entropy_stats_vars['max_negative'].set(f"Max Negative Drift: {entropy_stats.get('max_negative_drift', 0):.3f}")
        self.entropy_stats_vars['average_drift'].set(f"Average Drift: {entropy_stats.get('average_drift', 0):.3f}")
        
        # Update depth distribution
        self.depth_tree.delete(*self.depth_tree.get_children())
        
        depth_dist = self.family_stats.get('depth_distribution', {})
        total_blooms = sum(depth_dist.values()) if depth_dist else 1
        
        for depth, count in sorted(depth_dist.items()):
            percentage = (count / total_blooms) * 100
            self.depth_tree.insert('', 'end', text=f'Depth {depth}', 
                                 values=(count, f'{percentage:.1f}%'))
    
    def update_patterns_display(self):
        """Update the patterns tab display"""
        if not self.patterns_cache:
            return
        
        # Update pattern variables
        self.pattern_vars['increasing_entropy'].set(f"Increasing Entropy: {self.patterns_cache.get('increasing_entropy', 0)}")
        self.pattern_vars['decreasing_entropy'].set(f"Decreasing Entropy: {self.patterns_cache.get('decreasing_entropy', 0)}")
        self.pattern_vars['stable_entropy'].set(f"Stable Entropy: {self.patterns_cache.get('stable_entropy', 0)}")
        self.pattern_vars['high_volatility'].set(f"High Volatility: {self.patterns_cache.get('high_volatility', 0)}")
        self.pattern_vars['entropy_trend'].set(f"Trend: {self.patterns_cache.get('entropy_trend', 'Unknown')}")
        
        # Update source distribution
        self.source_tree.delete(*self.source_tree.get_children())
        
        source_dist = self.patterns_cache.get('source_distribution', {})
        total_sources = sum(source_dist.values()) if source_dist else 1
        
        for source, count in sorted(source_dist.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_sources) * 100
            self.source_tree.insert('', 'end', text=source, 
                                  values=(count, f'{percentage:.1f}%'))
    
    def update_tree_roots(self):
        """Update the root bloom selection combo"""
        if not self.rebloom_system:
            return
        
        roots = list(self.rebloom_system.tracker.roots)
        self.root_combo['values'] = roots
        
        if roots and not self.root_combo.get():
            self.root_combo.set(roots[0])
    
    def on_root_selected(self, event):
        """Handle root bloom selection"""
        root_id = self.root_combo.get()
        if root_id:
            self.draw_family_tree(root_id)
    
    def show_all_trees(self):
        """Show all family trees"""
        self.draw_family_tree(None)
    
    def draw_family_tree(self, root_id: Optional[str]):
        """Draw the family tree on canvas"""
        if not self.rebloom_system:
            return
        
        # Clear canvas
        self.tree_canvas.delete("all")
        
        try:
            # Get visualization data
            viz_data = self.rebloom_system.visualize_lineage_network(root_id)
            
            if not viz_data['nodes']:
                self.tree_canvas.create_text(50, 50, text="No blooms to display", 
                                           anchor='nw', font=('Arial', 12))
                return
            
            # Calculate positions for nodes
            positions = self._calculate_tree_positions(viz_data)
            
            # Draw edges first
            for edge in viz_data['edges']:
                source_pos = positions.get(edge['source'])
                target_pos = positions.get(edge['target'])
                
                if source_pos and target_pos:
                    self._draw_edge(source_pos, target_pos, edge['entropy_diff'])
            
            # Draw nodes
            for node in viz_data['nodes']:
                pos = positions.get(node['id'])
                if pos:
                    self._draw_node(pos, node)
            
            # Update scroll region
            self.tree_canvas.configure(scrollregion=self.tree_canvas.bbox("all"))
            
        except Exception as e:
            print(f"[GenealogyWidget] ⚠️ Tree drawing error: {e}")
            self.tree_canvas.create_text(50, 50, text=f"Error: {e}", 
                                       anchor='nw', font=('Arial', 12), fill='red')
    
    def _calculate_tree_positions(self, viz_data: Dict) -> Dict[str, Tuple[int, int]]:
        """Calculate positions for tree nodes"""
        positions = {}
        
        # Group nodes by depth
        depth_groups = {}
        for node in viz_data['nodes']:
            depth = node['depth']
            if depth not in depth_groups:
                depth_groups[depth] = []
            depth_groups[depth].append(node)
        
        # Layout parameters
        level_height = 100
        node_spacing = 120
        start_x = 100
        start_y = 50
        
        # Position nodes level by level
        for depth, nodes in sorted(depth_groups.items()):
            y = start_y + depth * level_height
            total_width = len(nodes) * node_spacing
            start_x_level = max(start_x, (800 - total_width) // 2)
            
            for i, node in enumerate(nodes):
                x = start_x_level + i * node_spacing
                positions[node['id']] = (x, y)
        
        return positions
    
    def _draw_node(self, pos: Tuple[int, int], node: Dict):
        """Draw a node on the canvas"""
        x, y = pos
        
        # Node color based on properties
        if node['is_root']:
            color = '#4CAF50'  # Green for roots
        elif node['entropy_drift'] > 0.3:
            color = '#FF9800'  # Orange for high entropy
        elif node['entropy_drift'] < -0.3:
            color = '#2196F3'  # Blue for low entropy
        else:
            color = '#9E9E9E'  # Gray for neutral
        
        # Draw circle
        radius = 20
        self.tree_canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius,
            fill=color, outline='black', width=2,
            tags=('node', node['id'])
        )
        
        # Draw label
        short_id = node['id'][-8:] if len(node['id']) > 8 else node['id']
        self.tree_canvas.create_text(
            x, y - radius - 15,
            text=short_id,
            font=('Arial', 8),
            tags=('label', node['id'])
        )
        
        # Draw stats
        stats_text = f"D:{node['depth']}\nE:{node['entropy_drift']:.2f}"
        self.tree_canvas.create_text(
            x, y + radius + 15,
            text=stats_text,
            font=('Arial', 7),
            tags=('stats', node['id'])
        )
    
    def _draw_edge(self, source_pos: Tuple[int, int], target_pos: Tuple[int, int], entropy_diff: float):
        """Draw an edge between nodes"""
        x1, y1 = source_pos
        x2, y2 = target_pos
        
        # Edge color based on entropy change
        if entropy_diff > 0.1:
            color = '#FF5722'  # Red for positive entropy
        elif entropy_diff < -0.1:
            color = '#4CAF50'  # Green for negative entropy
        else:
            color = '#757575'  # Gray for neutral
        
        # Draw arrow
        self.tree_canvas.create_line(
            x1, y1 + 20, x2, y2 - 20,
            arrow=tk.LAST, fill=color, width=2,
            tags='edge'
        )
        
        # Draw entropy label
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        self.tree_canvas.create_text(
            mid_x, mid_y,
            text=f"{entropy_diff:+.2f}",
            font=('Arial', 7),
            fill=color,
            tags='entropy_label'
        )
    
    def on_canvas_click(self, event):
        """Handle canvas click events"""
        # Find clicked item
        clicked = self.tree_canvas.find_closest(event.x, event.y)[0]
        tags = self.tree_canvas.gettags(clicked)
        
        # Check if it's a node
        for tag in tags:
            if tag.startswith('bloom_') or (tag != 'node' and tag != 'label' and tag != 'stats' and tag != 'edge'):
                if tag != 'node' and tag != 'label' and tag != 'stats':
                    self.selected_bloom = tag
                    self.bloom_entry.delete(0, tk.END)
                    self.bloom_entry.insert(0, tag)
                    self.lookup_bloom()
                    break
    
    def on_canvas_motion(self, event):
        """Handle canvas mouse motion for tooltips"""
        # Could implement tooltips here
        pass
    
    def lookup_bloom(self, event=None):
        """Lookup genealogy information for a specific bloom"""
        bloom_id = self.bloom_entry.get().strip()
        
        if not bloom_id or not self.rebloom_system:
            return
        
        try:
            genealogy = self.rebloom_system.get_bloom_genealogy(bloom_id)
            
            # Clear text widget
            self.genealogy_text.delete(1.0, tk.END)
            
            if 'error' in genealogy:
                self.genealogy_text.insert(tk.END, f"Error: {genealogy['error']}\n")
                return
            
            # Format genealogy information
            output = f"🌸 Genealogy for: {bloom_id}\n"
            output += "=" * 50 + "\n\n"
            
            output += f"📍 Position:\n"
            output += f"  Depth: {genealogy['depth']}\n"
            output += f"  Children: {genealogy['node_info']['children_count']}\n"
            output += f"  Created: {genealogy['node_info']['creation_time']}\n"
            output += f"  Entropy Drift: {genealogy['node_info']['total_entropy_drift']:.3f}\n\n"
            
            output += f"🌳 Ancestry Chain:\n"
            for i, ancestor in enumerate(genealogy['ancestry_chain']):
                indent = "  " * i
                output += f"{indent}└─ {ancestor}\n"
            output += "\n"
            
            if genealogy['descendants']:
                output += f"👶 Descendants ({len(genealogy['descendants'])}):\n"
                for desc in genealogy['descendants']:
                    output += f"  • {desc}\n"
                output += "\n"
            
            if genealogy['siblings']:
                output += f"👨‍👩‍👧‍👦 Siblings ({len(genealogy['siblings'])}):\n"
                for sibling in genealogy['siblings']:
                    output += f"  • {sibling}\n"
                output += "\n"
            
            output += f"📈 Entropy Evolution:\n"
            for bloom, entropy in genealogy['entropy_evolution']:
                output += f"  {bloom}: {entropy:+.3f}\n"
            
            self.genealogy_text.insert(tk.END, output)
            
        except Exception as e:
            self.genealogy_text.delete(1.0, tk.END)
            self.genealogy_text.insert(tk.END, f"Error looking up bloom: {e}\n")
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh mode"""
        if self.auto_refresh.get():
            self.schedule_refresh()
        else:
            # Cancel scheduled refresh
            if hasattr(self, '_refresh_job'):
                self.after_cancel(self._refresh_job)
    
    def schedule_refresh(self):
        """Schedule next auto-refresh"""
        if self.auto_refresh.get():
            self._refresh_job = self.after(self.refresh_interval, self.auto_refresh_callback)
    
    def auto_refresh_callback(self):
        """Auto-refresh callback"""
        self.refresh_data()
        self.schedule_refresh()
    
    def show_no_connection_message(self):
        """Show message when no rebloom system is connected"""
        messagebox.showwarning(
            "No Connection",
            "Rebloom tracking system is not available.\n\n"
            "This may be due to missing dependencies or "
            "integration system not being initialized."
        )
    
    def update_with_dawn_data(self, dawn_data: Dict[str, Any]):
        """
        Update genealogy display with DAWN data
        
        Args:
            dawn_data: Dictionary containing DAWN state data
        """
        if not self.rebloom_system:
            return
        
        # Extract bloom-related information from DAWN data
        bloom_info = dawn_data.get('bloom', {})
        
        if bloom_info and self.auto_refresh.get():
            # Check if we should trigger a refresh based on new bloom activity
            current_blooms = bloom_info.get('active_blooms', 0)
            if current_blooms != getattr(self, '_last_bloom_count', 0):
                self._last_bloom_count = current_blooms
                self.after_idle(self.refresh_data)


# Example integration with main DAWN GUI
def integrate_with_dawn_gui(main_gui_instance):
    """
    Example function showing how to integrate the genealogy widget with the main DAWN GUI
    
    Args:
        main_gui_instance: The main DAWN GUI instance
    """
    
    # Create genealogy widget
    genealogy_widget = RebloomGenealogyWidget(main_gui_instance)
    
    # Add to GUI layout (example)
    genealogy_widget.pack(fill='both', expand=True)
    
    # Connect to main GUI update cycle
    def update_genealogy(dawn_data):
        genealogy_widget.update_with_dawn_data(dawn_data)
    
    # Register update callback with main GUI
    if hasattr(main_gui_instance, 'register_update_callback'):
        main_gui_instance.register_update_callback(update_genealogy)
    
    return genealogy_widget


if __name__ == "__main__":
    # Standalone test
    root = tk.Tk()
    root.title("Rebloom Genealogy Widget Test")
    root.geometry("800x600")
    
    widget = RebloomGenealogyWidget(root)
    widget.pack(fill='both', expand=True)
    
    # Add some test data if system is available
    if widget.rebloom_system:
        # Create test blooms
        widget.rebloom_system.log_bloom_creation("test_root", None, 0.0, {'source': 'test'})
        widget.rebloom_system.log_bloom_creation("test_child1", "test_root", 0.1, {'source': 'test'})
        widget.rebloom_system.log_bloom_creation("test_child2", "test_root", -0.05, {'source': 'test'})
        widget.rebloom_system.log_bloom_creation("test_grand1", "test_child1", 0.15, {'source': 'test'})
        
        # Refresh display
        widget.refresh_data()
    
    root.mainloop() 