# sigil_renderer.py
# Visual rendering layer for DAWN's active sigils and symbolic state

import os
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False
    # Fallback color definitions
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        DIM = NORMAL = BRIGHT = RESET_ALL = ""

try:
    import tkinter as tk
    from tkinter import ttk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class UrgencyLevel(Enum):
    """Urgency levels for sigil coloring"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class RenderConfig:
    """Configuration for the sigil renderer"""
    use_colors: bool = COLORAMA_AVAILABLE
    clear_screen: bool = True
    show_timestamp: bool = True
    show_borders: bool = True
    max_sigils_display: int = 10
    max_organs_display: int = 8
    terminal_width: int = 80
    update_interval: float = 2.0


class SigilRenderer:
    """Visual renderer for DAWN's symbolic state and active sigils"""
    
    # Emoji/Symbol mapping for sigils
    SIGIL_SYMBOLS = {
        "STABILIZE_PROTOCOL": "🛡️",
        "REBLOOM_MEMORY": "🌸", 
        "FIRE_REFLEX": "🔥",
        "DUMP_LOGS": "📝",
        "DEEP_FOCUS": "🎯",
        "ENTROPY_FLUSH": "🌊",
        "CHAOS_EMBRACE": "🌀",
        "MEMORY_DEFRAG": "🧩",
        "HEAT_DISSIPATE": "❄️",
        "ZONE_SHIFT": "⚡",
        "PULSE_SYNC": "💓",
        "SIGIL_RESET": "🔄",
        "DIAGNOSTIC_SWEEP": "🔍",
        "NEURAL_CASCADE": "⚡",
        "DREAM_WEAVE": "🌙",
        "FRACTAL_BLOOM": "🌺",
        "VOID_TOUCH": "⚫",
        "LIGHT_BRIDGE": "🌉",
        "SOMA_PULSE": "💫",
        "CORE_RESONANCE": "🔮"
    }
    
    # Color mapping for urgency levels
    URGENCY_COLORS = {
        UrgencyLevel.LOW: Fore.GREEN,
        UrgencyLevel.MEDIUM: Fore.YELLOW,
        UrgencyLevel.HIGH: Fore.RED,
        UrgencyLevel.CRITICAL: Fore.MAGENTA + Style.BRIGHT
    }
    
    # Symbolic organ glyphs
    ORGAN_GLYPHS = {
        "FractalHeart": "❤️",
        "SomaCoil": "🌀",
        "VoidEye": "👁️",
        "MemoryWeb": "🕸️",
        "PulseCore": "💎",
        "EntropyPool": "🌊",
        "ChaosGate": "🚪",
        "DreamLoom": "🧶",
        "NeuralBridge": "🌉",
        "EssenceVault": "🏛️"
    }
    
    def __init__(self, config: Optional[RenderConfig] = None):
        self.config = config or RenderConfig()
        self.last_render_time = 0.0
        self.render_count = 0
        
        # Initialize display state
        self.active_sigils: List[Dict[str, Any]] = []
        self.symbolic_organs: Dict[str, Any] = {}
        self.system_stats: Dict[str, Any] = {}
        
        print(f"🎨 DAWN Sigil Renderer initialized")
        print(f"   Colors: {'Enabled' if self.config.use_colors else 'Disabled'}")
        print(f"   Clear Screen: {self.config.clear_screen}")
    
    def render(self, sigil_data: Optional[List[Dict]] = None, 
               organ_data: Optional[Dict] = None,
               system_data: Optional[Dict] = None,
               force_render: bool = False):
        """
        Main render function - displays DAWN console readout.
        
        Args:
            sigil_data: List of active sigil dictionaries
            organ_data: Dictionary of symbolic organ states
            system_data: System statistics and metrics
            force_render: Force render regardless of timing
        """
        current_time = time.time()
        
        # Check if enough time has passed since last render
        if not force_render and (current_time - self.last_render_time) < self.config.update_interval:
            return
        
        # Update internal state
        if sigil_data:
            self.active_sigils = sigil_data[:self.config.max_sigils_display]
        if organ_data:
            self.symbolic_organs = organ_data
        if system_data:
            self.system_stats = system_data
        
        # Clear screen if configured
        if self.config.clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        
        # Render the display
        self._render_header()
        self._render_sigils()
        self._render_organs()
        self._render_system_stats()
        self._render_footer()
        
        # Update timing
        self.last_render_time = current_time
        self.render_count += 1
    
    def _render_header(self):
        """Render the header section"""
        width = self.config.terminal_width
        border = "═" * width if self.config.show_borders else ""
        
        if self.config.use_colors:
            title_color = Fore.CYAN + Style.BRIGHT
            border_color = Fore.BLUE
        else:
            title_color = border_color = ""
        
        if border:
            print(f"{border_color}{border}")
        
        # Title line
        title = "🧠 DAWN COGNITION ENGINE - SYMBOLIC STATE READOUT"
        print(f"{title_color}{title.center(width)}")
        
        # Timestamp if enabled
        if self.config.show_timestamp:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            cycle_info = f"Cycle #{self.render_count:04d}"
            time_line = f"{timestamp} | {cycle_info}"
            print(f"{Fore.WHITE if self.config.use_colors else ''}{time_line.center(width)}")
        
        if border:
            print(f"{border_color}{border}")
        print()
    
    def _render_sigils(self):
        """Render active sigils section"""
        section_title = "🔮 ACTIVE SIGILS"
        if self.config.use_colors:
            print(f"{Fore.MAGENTA + Style.BRIGHT}{section_title}")
        else:
            print(section_title)
        
        print("─" * 40)
        
        if not self.active_sigils:
            print(f"{Fore.WHITE if self.config.use_colors else ''}   No active sigils")
        else:
            for i, sigil in enumerate(self.active_sigils):
                self._render_single_sigil(sigil, i)
        
        print()
    
    def _render_single_sigil(self, sigil: Dict[str, Any], index: int):
        """Render a single sigil with symbol and urgency coloring"""
        name = sigil.get('name', f'UNKNOWN_SIGIL_{index}')
        urgency = sigil.get('urgency', UrgencyLevel.LOW)
        duration = sigil.get('duration', 0.0)
        trigger_count = sigil.get('trigger_count', 1)
        
        # Get symbol and colors
        symbol = self.SIGIL_SYMBOLS.get(name, "🔹")
        if isinstance(urgency, str):
            urgency = UrgencyLevel(urgency)
        color = self.URGENCY_COLORS.get(urgency, "") if self.config.use_colors else ""
        
        # Format duration
        if duration > 60:
            duration_str = f"{duration/60:.1f}m"
        else:
            duration_str = f"{duration:.1f}s"
        
        # Construct sigil line
        status_indicator = "●" if trigger_count > 1 else "○"
        sigil_line = f"   {symbol} {name:<20} {status_indicator} {duration_str:>6} [{trigger_count:>2}x]"
        
        print(f"{color}{sigil_line}")
    
    def _render_organs(self):
        """Render symbolic organs section"""
        section_title = "🏛️ SYMBOLIC ORGANS"
        if self.config.use_colors:
            print(f"{Fore.GREEN + Style.BRIGHT}{section_title}")
        else:
            print(section_title)
        
        print("─" * 40)
        
        if not self.symbolic_organs:
            print(f"{Fore.WHITE if self.config.use_colors else ''}   No organ data available")
        else:
            organ_count = 0
            for organ_name, organ_state in self.symbolic_organs.items():
                if organ_count >= self.config.max_organs_display:
                    break
                self._render_single_organ(organ_name, organ_state)
                organ_count += 1
        
        print()
    
    def _render_single_organ(self, name: str, state: Any):
        """Render a single symbolic organ with glyph and state"""
        glyph = self.ORGAN_GLYPHS.get(name, "🔷")
        
        # Format state value
        if isinstance(state, dict):
            if 'value' in state:
                value_str = f"{state['value']:.3f}"
                saturation = state.get('saturation', 0.5)
            else:
                value_str = f"{len(state)} keys"
                saturation = 0.5
        elif isinstance(state, (list, tuple)):
            value_str = f"[{', '.join(str(x) for x in state[:3])}{'...' if len(state) > 3 else ''}]"
            saturation = len(state) / 10.0  # Assume max 10 for saturation
        elif isinstance(state, (int, float)):
            value_str = f"{state:.3f}" if isinstance(state, float) else str(state)
            saturation = min(abs(state), 1.0)
        else:
            value_str = str(state)[:20]
            saturation = 0.5
        
        # Color based on saturation
        if self.config.use_colors:
            if saturation > 0.8:
                color = Fore.RED + Style.BRIGHT
            elif saturation > 0.6:
                color = Fore.YELLOW
            elif saturation > 0.3:
                color = Fore.GREEN
            else:
                color = Fore.CYAN + Style.DIM
        else:
            color = ""
        
        # Construct organ line
        organ_line = f"   {glyph} {name:<15} {value_str:>15}"
        print(f"{color}{organ_line}")
    
    def _render_system_stats(self):
        """Render system statistics section"""
        if not self.system_stats:
            return
        
        section_title = "📊 SYSTEM METRICS"
        if self.config.use_colors:
            print(f"{Fore.BLUE + Style.BRIGHT}{section_title}")
        else:
            print(section_title)
        
        print("─" * 40)
        
        # Common system stats
        stats_to_show = [
            ('entropy', 'Entropy', '🌊'),
            ('heat', 'Heat Level', '🌡️'),
            ('focus', 'Focus', '🎯'),
            ('chaos', 'Chaos', '🌀'),
            ('zone', 'Current Zone', '🏛️'),
            ('forecast', 'Forecast', '🔮'),
            ('memory_chunks', 'Memory Chunks', '📚')
        ]
        
        for key, label, emoji in stats_to_show:
            if key in self.system_stats:
                value = self.system_stats[key]
                if isinstance(value, float):
                    value_str = f"{value:.3f}"
                else:
                    value_str = str(value)
                
                print(f"   {emoji} {label:<15} {value_str:>15}")
        
        print()
    
    def _render_footer(self):
        """Render footer section"""
        if not self.config.show_borders:
            return
        
        width = self.config.terminal_width
        border = "═" * width
        
        if self.config.use_colors:
            border_color = Fore.BLUE
        else:
            border_color = ""
        
        print(f"{border_color}{border}")
        
        # Status line
        status_parts = []
        if len(self.active_sigils) > 0:
            status_parts.append(f"Sigils: {len(self.active_sigils)}")
        if len(self.symbolic_organs) > 0:
            status_parts.append(f"Organs: {len(self.symbolic_organs)}")
        if len(self.system_stats) > 0:
            status_parts.append(f"Metrics: {len(self.system_stats)}")
        
        status_line = " | ".join(status_parts) if status_parts else "System Idle"
        print(f"{Fore.WHITE if self.config.use_colors else ''}{status_line.center(width)}")
        print(f"{border_color}{border}")
    
    def render_minimal(self, sigils: List[str], quick_stats: Dict[str, float]):
        """Minimal single-line render for integration into tick loops"""
        sigil_symbols = [self.SIGIL_SYMBOLS.get(s, "🔹") for s in sigils[:5]]
        sigil_line = "".join(sigil_symbols) if sigil_symbols else "○"
        
        stats_line = " | ".join([f"{k}:{v:.2f}" for k, v in quick_stats.items()][:4])
        
        output = f"🧠 {sigil_line} | {stats_line}"
        if self.config.use_colors:
            output = f"{Fore.CYAN}{output}"
        
        print(output)
    
    def create_tkinter_window(self):
        """Create a Tkinter window for GUI rendering (optional)"""
        if not TKINTER_AVAILABLE:
            print("⚠️ Tkinter not available for GUI rendering")
            return None
        
        root = tk.Tk()
        root.title("DAWN - Symbolic State Monitor")
        root.geometry("800x600")
        root.configure(bg='black')
        
        # Create text widget for display
        text_widget = tk.Text(root, bg='black', fg='green', font=('Courier', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        return root, text_widget


# Factory functions
def create_terminal_renderer(use_colors: bool = True, clear_screen: bool = True) -> SigilRenderer:
    """Create a terminal-based renderer with common settings"""
    config = RenderConfig(
        use_colors=use_colors,
        clear_screen=clear_screen,
        show_timestamp=True,
        show_borders=True
    )
    return SigilRenderer(config)


def create_minimal_renderer() -> SigilRenderer:
    """Create a minimal renderer for tick loop integration"""
    config = RenderConfig(
        use_colors=True,
        clear_screen=False,
        show_timestamp=False,
        show_borders=False
    )
    return SigilRenderer(config)


# Example usage and testing
if __name__ == "__main__":
    print("🎨 Testing DAWN Sigil Renderer")
    
    # Create renderer
    renderer = create_terminal_renderer()
    
    # Mock data for testing
    test_sigils = [
        {
            'name': 'STABILIZE_PROTOCOL',
            'urgency': UrgencyLevel.HIGH,
            'duration': 45.2,
            'trigger_count': 3
        },
        {
            'name': 'REBLOOM_MEMORY', 
            'urgency': UrgencyLevel.MEDIUM,
            'duration': 12.8,
            'trigger_count': 1
        },
        {
            'name': 'FIRE_REFLEX',
            'urgency': UrgencyLevel.CRITICAL,
            'duration': 156.4,
            'trigger_count': 7
        }
    ]
    
    test_organs = {
        'FractalHeart': {'value': 0.847, 'saturation': 0.9},
        'SomaCoil': ['path_1', 'path_3', 'path_7'],
        'VoidEye': 0.234,
        'MemoryWeb': {'nodes': 42, 'connections': 156},
        'PulseCore': 1.567
    }
    
    test_stats = {
        'entropy': 0.673,
        'heat': 0.45,
        'focus': 0.82,
        'chaos': 0.31,
        'zone': 'FOCUS',
        'forecast': 1.234,
        'memory_chunks': 89
    }
    
    print("\n🧪 Full Render Test:")
    renderer.render(test_sigils, test_organs, test_stats, force_render=True)
    
    print("\n🧪 Minimal Render Test:")
    minimal_renderer = create_minimal_renderer()
    minimal_renderer.render_minimal(
        ['STABILIZE_PROTOCOL', 'REBLOOM_MEMORY'], 
        {'E': 0.67, 'H': 0.45, 'F': 0.82}
    )
    
    print("\n🚀 Renderer Ready for Integration!")
    print("   - Wire into tick loop with render()")
    print("   - Use render_minimal() for compact display")
    print("   - Supports live symbolic state monitoring") 