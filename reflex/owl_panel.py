"""
Owl Panel - Visual Commentary Side Feed for DAWN System
Provides real-time monitoring commentary with GUI rendering and timestamps
"""

import logging
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
import threading
import queue
import time

logger = logging.getLogger(__name__)


class OwlCommentType(Enum):
    """Types of owl commentary"""
    OBSERVATION = "observation"
    WARNING = "warning"
    ALERT = "alert"
    INSIGHT = "insight"
    DEBUG = "debug"
    SYSTEM = "system"
    BLOOM = "bloom"
    SIGIL = "sigil"
    THERMAL = "thermal"


@dataclass
class OwlEntry:
    """Individual owl commentary entry with metadata"""
    tick_id: int
    timestamp: datetime
    comment: str
    comment_type: OwlCommentType
    source: str = "owl"
    priority: int = 1  # 1=low, 5=critical
    context: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


class OwlPanel:
    """
    Visual commentary side feed with GUI rendering and time-stamped monitoring.
    Provides real-time owl observations with styling and filtering capabilities.
    """
    
    def __init__(self, max_entries: int = 100, auto_scroll: bool = True):
        """
        Initialize owl panel with GUI components.
        
        Args:
            max_entries: Maximum number of entries to keep in memory
            auto_scroll: Whether to auto-scroll to newest entries
        """
        self.entries: List[OwlEntry] = []
        self.max_entries = max_entries
        self.auto_scroll = auto_scroll
        
        # GUI components
        self.root = None
        self.panel_frame = None
        self.text_widget = None
        self.filter_frame = None
        self.status_frame = None
        
        # State management
        self.is_visible = False
        self.current_filter = None
        self.paused = False
        self.update_queue = queue.Queue()
        self.update_thread = None
        
        # Styling configuration
        self.colors = {
            OwlCommentType.OBSERVATION: "#E8F4FD",  # Light blue
            OwlCommentType.WARNING: "#FFF3CD",      # Light yellow
            OwlCommentType.ALERT: "#F8D7DA",        # Light red
            OwlCommentType.INSIGHT: "#D1ECF1",      # Light cyan
            OwlCommentType.DEBUG: "#E2E3E5",        # Light gray
            OwlCommentType.SYSTEM: "#D4EDDA",       # Light green
            OwlCommentType.BLOOM: "#F8E6FF",        # Light purple
            OwlCommentType.SIGIL: "#FFE6CC",        # Light orange
            OwlCommentType.THERMAL: "#FFD6D6"       # Light pink
        }
        
        self.icons = {
            OwlCommentType.OBSERVATION: "👁️",
            OwlCommentType.WARNING: "⚠️",
            OwlCommentType.ALERT: "🚨",
            OwlCommentType.INSIGHT: "💡",
            OwlCommentType.DEBUG: "🐛",
            OwlCommentType.SYSTEM: "⚙️",
            OwlCommentType.BLOOM: "🌸",
            OwlCommentType.SIGIL: "◈",
            OwlCommentType.THERMAL: "🌡️"
        }
        
        logger.info("OwlPanel initialized")
        
    def create_gui(self, parent_window: Optional[tk.Tk] = None) -> tk.Frame:
        """
        Create the GUI panel for owl commentary.
        
        Args:
            parent_window: Parent Tkinter window, creates new if None
            
        Returns:
            Main panel frame
        """
        if parent_window is None:
            self.root = tk.Tk()
            self.root.title("🦉 DAWN Owl Commentary")
            self.root.geometry("400x600")
            parent = self.root
        else:
            parent = parent_window
            
        # Main panel frame
        self.panel_frame = ttk.Frame(parent, padding="5")
        self.panel_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(self.panel_frame)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        title_label = ttk.Label(header_frame, text="🦉 Owl Commentary", 
                               font=("Arial", 12, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Control buttons
        self._create_control_buttons(header_frame)
        
        # Filter frame
        self._create_filter_frame()
        
        # Main text display
        self._create_text_display()
        
        # Status frame
        self._create_status_frame()
        
        # Start update thread
        self._start_update_thread()
        
        self.is_visible = True
        logger.info("Owl panel GUI created")
        
        return self.panel_frame
        
    def _create_control_buttons(self, parent: ttk.Frame) -> None:
        """Create control buttons for the panel"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(side=tk.RIGHT)
        
        # Pause/Resume button
        self.pause_button = ttk.Button(button_frame, text="⏸️", width=3,
                                      command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT, padx=1)
        
        # Clear button
        clear_button = ttk.Button(button_frame, text="🗑️", width=3,
                                 command=self.clear_entries)
        clear_button.pack(side=tk.LEFT, padx=1)
        
        # Settings button
        settings_button = ttk.Button(button_frame, text="⚙️", width=3,
                                   command=self.show_settings)
        settings_button.pack(side=tk.LEFT, padx=1)
        
    def _create_filter_frame(self) -> None:
        """Create filtering controls"""
        self.filter_frame = ttk.LabelFrame(self.panel_frame, text="Filters", padding="3")
        self.filter_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Comment type filter
        type_frame = ttk.Frame(self.filter_frame)
        type_frame.pack(fill=tk.X)
        
        ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT)
        
        self.type_var = tk.StringVar(value="all")
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, width=12)
        type_combo['values'] = ['all'] + [t.value for t in OwlCommentType]
        type_combo.pack(side=tk.LEFT, padx=5)
        type_combo.bind('<<ComboboxSelected>>', self._on_filter_change)
        
        # Priority filter
        ttk.Label(type_frame, text="Min Priority:").pack(side=tk.LEFT, padx=(10, 0))
        
        self.priority_var = tk.StringVar(value="1")
        priority_combo = ttk.Combobox(type_frame, textvariable=self.priority_var, width=3)
        priority_combo['values'] = ['1', '2', '3', '4', '5']
        priority_combo.pack(side=tk.LEFT, padx=5)
        priority_combo.bind('<<ComboboxSelected>>', self._on_filter_change)
        
    def _create_text_display(self) -> None:
        """Create the main text display widget"""
        # Text widget with scrollbar
        text_frame = ttk.Frame(self.panel_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_widget = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED,
            bg="#1a1a1a",
            fg="#e0e0e0",
            insertbackground="#e0e0e0",
            selectbackground="#404040"
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Configure text tags for styling
        self._configure_text_tags()
        
    def _create_status_frame(self) -> None:
        """Create status information frame"""
        self.status_frame = ttk.Frame(self.panel_frame)
        self.status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", 
                                     font=("Arial", 8))
        self.status_label.pack(side=tk.LEFT)
        
        self.entry_count_label = ttk.Label(self.status_frame, text="0 entries",
                                          font=("Arial", 8))
        self.entry_count_label.pack(side=tk.RIGHT)
        
    def _configure_text_tags(self) -> None:
        """Configure text widget tags for styling"""
        for comment_type in OwlCommentType:
            tag_name = f"type_{comment_type.value}"
            bg_color = self.colors.get(comment_type, "#FFFFFF")
            
            self.text_widget.tag_configure(
                tag_name,
                background=bg_color,
                relief=tk.RAISED,
                borderwidth=1,
                lmargin1=5,
                lmargin2=15,
                rmargin=5
            )
            
        # Special tags
        self.text_widget.tag_configure("timestamp", foreground="#888888", font=("Consolas", 8))
        self.text_widget.tag_configure("tick_id", foreground="#4a9eff", font=("Consolas", 8, "bold"))
        self.text_widget.tag_configure("priority_high", foreground="#ff4444", font=("Consolas", 9, "bold"))
        
    def add_comment(self, tick_id: int, comment: str, 
                   comment_type: OwlCommentType = OwlCommentType.OBSERVATION,
                   source: str = "owl", priority: int = 1,
                   context: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a new owl commentary entry with full metadata.
        
        Args:
            tick_id: System tick identifier
            comment: Commentary text
            comment_type: Type of commentary
            source: Source system/component
            priority: Priority level (1-5)
            context: Additional context data
        """
        entry = OwlEntry(
            tick_id=tick_id,
            timestamp=datetime.now(timezone.utc),
            comment=comment,
            comment_type=comment_type,
            source=source,
            priority=priority,
            context=context or {}
        )
        
        # Add to entries list
        self.entries.append(entry)
        
        # Maintain max entries limit
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
            
        # Queue for GUI update
        if self.is_visible and not self.paused:
            self.update_queue.put(entry)
            
        logger.debug(f"Added owl comment: {comment[:50]}...")
        
    def _start_update_thread(self) -> None:
        """Start the GUI update thread"""
        if self.update_thread is None or not self.update_thread.is_alive():
            self.update_thread = threading.Thread(target=self._update_worker, daemon=True)
            self.update_thread.start()
            
    def _update_worker(self) -> None:
        """Worker thread for updating GUI"""
        while True:
            try:
                # Wait for update with timeout
                entry = self.update_queue.get(timeout=1.0)
                
                if self.text_widget and not self.paused:
                    # Schedule GUI update on main thread
                    if self.root:
                        self.root.after(0, self._update_display, entry)
                        
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error in owl panel update worker: {e}")
                
    def _update_display(self, entry: OwlEntry) -> None:
        """Update the text display with new entry"""
        if not self.text_widget:
            return
            
        # Check filter
        if not self._passes_filter(entry):
            return
            
        # Format entry text
        formatted_text = self._format_entry(entry)
        
        # Insert into text widget
        self.text_widget.config(state=tk.NORMAL)
        
        # Insert formatted text with tags
        self._insert_formatted_entry(entry, formatted_text)
        
        # Auto-scroll if enabled
        if self.auto_scroll:
            self.text_widget.see(tk.END)
            
        self.text_widget.config(state=tk.DISABLED)
        
        # Update status
        self._update_status()
        
    def _format_entry(self, entry: OwlEntry) -> str:
        """Format an entry for display"""
        timestamp_str = entry.timestamp.strftime("%H:%M:%S.%f")[:-3]
        icon = self.icons.get(entry.comment_type, "🔍")
        priority_indicator = "!" * entry.priority if entry.priority > 1 else ""
        
        return f"[{timestamp_str}] Tick {entry.tick_id:04d} {icon} {priority_indicator}{entry.comment}\n"
        
    def _insert_formatted_entry(self, entry: OwlEntry, formatted_text: str) -> None:
        """Insert formatted entry with proper tags"""
        lines = formatted_text.split('\n')
        for line in lines:
            if not line.strip():
                continue
                
            # Insert with type-specific tag
            tag_name = f"type_{entry.comment_type.value}"
            if entry.priority >= 4:
                tag_name = "priority_high"
                
            self.text_widget.insert(tk.END, line + '\n', tag_name)
            
    def _passes_filter(self, entry: OwlEntry) -> bool:
        """Check if entry passes current filters"""
        # Type filter
        if self.type_var and self.type_var.get() != "all":
            if entry.comment_type.value != self.type_var.get():
                return False
                
        # Priority filter
        if self.priority_var:
            try:
                min_priority = int(self.priority_var.get())
                if entry.priority < min_priority:
                    return False
            except ValueError:
                pass
                
        return True
        
    def _on_filter_change(self, event=None) -> None:
        """Handle filter changes"""
        self.refresh_display()
        
    def refresh_display(self) -> None:
        """Refresh the entire display based on current filters"""
        if not self.text_widget:
            return
            
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        
        for entry in self.entries:
            if self._passes_filter(entry):
                formatted_text = self._format_entry(entry)
                self._insert_formatted_entry(entry, formatted_text)
                
        if self.auto_scroll:
            self.text_widget.see(tk.END)
            
        self.text_widget.config(state=tk.DISABLED)
        self._update_status()
        
    def _update_status(self) -> None:
        """Update status labels"""
        if self.entry_count_label:
            visible_count = sum(1 for entry in self.entries if self._passes_filter(entry))
            total_count = len(self.entries)
            self.entry_count_label.config(text=f"{visible_count}/{total_count} entries")
            
        if self.status_label:
            status = "Paused" if self.paused else "Active"
            self.status_label.config(text=status)
            
    def toggle_pause(self) -> None:
        """Toggle pause state"""
        self.paused = not self.paused
        if self.pause_button:
            self.pause_button.config(text="▶️" if self.paused else "⏸️")
        self._update_status()
        
    def clear_entries(self) -> None:
        """Clear all entries"""
        self.entries.clear()
        if self.text_widget:
            self.text_widget.config(state=tk.NORMAL)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.config(state=tk.DISABLED)
        self._update_status()
        
    def show_settings(self) -> None:
        """Show settings dialog"""
        # TODO: Implement settings dialog
        logger.info("Settings dialog not yet implemented")
        
    def get_recent(self, count: int = 10) -> List[str]:
        """
        Get recent entries as formatted strings.
        
        Args:
            count: Number of recent entries to return
            
        Returns:
            List of formatted entry strings
        """
        recent_entries = self.entries[-count:] if count > 0 else self.entries
        return [self._format_entry(entry).strip() for entry in recent_entries]
        
    def get_entries_by_type(self, comment_type: OwlCommentType) -> List[OwlEntry]:
        """Get all entries of specific type"""
        return [entry for entry in self.entries if entry.comment_type == comment_type]
        
    def get_entries_by_priority(self, min_priority: int) -> List[OwlEntry]:
        """Get entries with minimum priority level"""
        return [entry for entry in self.entries if entry.priority >= min_priority]
        
    def export_entries(self, filepath: str, format: str = "txt") -> bool:
        """
        Export entries to file.
        
        Args:
            filepath: Output file path
            format: Export format ("txt", "json", "csv")
            
        Returns:
            True if successful
        """
        try:
            if format == "txt":
                with open(filepath, 'w', encoding='utf-8') as f:
                    for entry in self.entries:
                        f.write(self._format_entry(entry))
            elif format == "json":
                import json
                data = [
                    {
                        "tick_id": entry.tick_id,
                        "timestamp": entry.timestamp.isoformat(),
                        "comment": entry.comment,
                        "type": entry.comment_type.value,
                        "source": entry.source,
                        "priority": entry.priority,
                        "context": entry.context
                    }
                    for entry in self.entries
                ]
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            else:
                logger.error(f"Unsupported export format: {format}")
                return False
                
            logger.info(f"Exported {len(self.entries)} entries to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export entries: {e}")
            return False
            
    def destroy(self) -> None:
        """Clean up resources"""
        self.is_visible = False
        if self.root:
            self.root.destroy()
        logger.info("OwlPanel destroyed")


# Convenience functions for quick usage
def create_owl_sidebar(parent_window: tk.Tk = None) -> OwlPanel:
    """Create a styled owl commentary sidebar"""
    panel = OwlPanel(max_entries=150, auto_scroll=True)
    panel.create_gui(parent_window)
    return panel


def add_owl_observation(panel: OwlPanel, tick_id: int, message: str, priority: int = 1):
    """Quick function to add an observation"""
    panel.add_comment(tick_id, message, OwlCommentType.OBSERVATION, priority=priority)


def add_owl_alert(panel: OwlPanel, tick_id: int, message: str, context: Dict[str, Any] = None):
    """Quick function to add an alert"""
    panel.add_comment(tick_id, message, OwlCommentType.ALERT, priority=4, context=context) 