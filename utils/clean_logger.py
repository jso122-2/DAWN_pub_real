"""
DAWN Clean Logger - Structured output without emojis
Provides consistent, professional logging throughout the DAWN system
"""
import time
from typing import Dict, Any, Optional


class CleanLogger:
    """Professional logging without emoji distractions"""
    
    # Log level configurations
    LEVELS = {
        'DEBUG': {'prefix': '[DEBUG]', 'indent': '  '},
        'INFO': {'prefix': '[INFO]', 'indent': '  '},
        'SUCCESS': {'prefix': '[SUCCESS]', 'indent': '  '},
        'WARNING': {'prefix': '[WARNING]', 'indent': '  '},
        'ERROR': {'prefix': '[ERROR]', 'indent': '  '},
        'CRITICAL': {'prefix': '[CRITICAL]', 'indent': '  '},
        'SYSTEM': {'prefix': '[SYSTEM]', 'indent': '  '},
        'FRACTAL': {'prefix': '[FRACTAL]', 'indent': '  '},
        'TICK': {'prefix': '[TICK]', 'indent': '  '},
        'SIGIL': {'prefix': '[SIGIL]', 'indent': '  '},
    }
    
    def __init__(self, component_name: str = "DAWN", show_timestamps: bool = True):
        self.component_name = component_name
        self.show_timestamps = show_timestamps
        
    def _format_timestamp(self) -> str:
        """Generate clean timestamp"""
        if not self.show_timestamps:
            return ""
        return f"[{time.strftime('%H:%M:%S')}] "
    
    def _format_message(self, level: str, message: str, details: Optional[Dict[str, Any]] = None) -> str:
        """Format message with consistent structure"""
        config = self.LEVELS.get(level.upper(), self.LEVELS['INFO'])
        timestamp = self._format_timestamp()
        
        # Main message line
        output = f"{timestamp}{config['prefix']} {self.component_name}: {message}"
        
        # Add details if provided
        if details:
            for key, value in details.items():
                output += f"\n{config['indent']}{key}: {value}"
                
        return output
    
    def log(self, level: str, message: str, details: Optional[Dict[str, Any]] = None):
        """Generic log method"""
        print(self._format_message(level, message, details))
    
    def debug(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Debug level logging"""
        self.log('DEBUG', message, details)
    
    def info(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Info level logging"""
        self.log('INFO', message, details)
    
    def success(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Success level logging"""
        self.log('SUCCESS', message, details)
    
    def warning(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Warning level logging"""
        self.log('WARNING', message, details)
    
    def error(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Error level logging"""
        self.log('ERROR', message, details)
    
    def critical(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Critical level logging"""
        self.log('CRITICAL', message, details)
    
    def system(self, message: str, details: Optional[Dict[str, Any]] = None):
        """System level logging"""
        self.log('SYSTEM', message, details)
    
    def fractal(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Fractal rendering logging"""
        self.log('FRACTAL', message, details)
    
    def tick(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Tick engine logging"""
        self.log('TICK', message, details)
    
    def sigil(self, message: str, details: Optional[Dict[str, Any]] = None):
        """Sigil system logging"""
        self.log('SIGIL', message, details)
    
    def section_header(self, title: str, width: int = 80):
        """Print clean section header"""
        print("\n" + "=" * width)
        print(f"{title.upper()}")
        print("=" * width)
    
    def section_footer(self, title: str = None, width: int = 80):
        """Print clean section footer"""
        if title:
            print(f"{title.upper()} COMPLETE")
        print("=" * width + "\n")
    
    def subsection(self, title: str, width: int = 60):
        """Print clean subsection header"""
        print(f"\n{title.upper()}:")
        print("-" * len(title))
    
    def parameter_block(self, title: str, params: Dict[str, Any]):
        """Print clean parameter block"""
        self.subsection(title)
        for key, value in params.items():
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:97] + "..."
            print(f"  {key}: {value_str}")
    
    def status_list(self, items: Dict[str, bool], title: str = "System Status"):
        """Print clean status list"""
        self.subsection(title)
        for item, status in items.items():
            status_text = "ACTIVE" if status else "FAILED"
            print(f"  {item}: {status_text}")
    
    def progress_update(self, step: str, current: int, total: int, details: str = ""):
        """Print clean progress update"""
        percentage = (current / total) * 100 if total > 0 else 0
        progress_bar = "=" * int(percentage / 5) + "-" * (20 - int(percentage / 5))
        progress_text = f"[{progress_bar}] {percentage:.1f}% ({current}/{total})"
        
        if details:
            print(f"{step}: {progress_text} - {details}")
        else:
            print(f"{step}: {progress_text}")


# Global instances for common use
fractal_logger = CleanLogger("FRACTAL")
tick_logger = CleanLogger("TICK")
sigil_logger = CleanLogger("SIGIL")
system_logger = CleanLogger("SYSTEM")

# Utility functions for quick access
def log_fractal_render(message: str, details: Optional[Dict[str, Any]] = None):
    """Quick fractal rendering log"""
    fractal_logger.fractal(message, details)

def log_tick_update(message: str, details: Optional[Dict[str, Any]] = None):
    """Quick tick engine log"""
    tick_logger.tick(message, details)

def log_sigil_event(message: str, details: Optional[Dict[str, Any]] = None):
    """Quick sigil system log"""
    sigil_logger.sigil(message, details)

def log_system_event(message: str, details: Optional[Dict[str, Any]] = None):
    """Quick system event log"""
    system_logger.system(message, details)

def clean_section_header(title: str, width: int = 80):
    """Quick section header"""
    print("\n" + "=" * width)
    print(f"{title.upper()}")
    print("=" * width)

def clean_section_footer(title: str = None, width: int = 80):
    """Quick section footer"""
    if title:
        print(f"{title.upper()} COMPLETE")
    print("=" * width + "\n")


# Example usage and test
if __name__ == "__main__":
    # Test the clean logger
    logger = CleanLogger("TEST")
    
    logger.section_header("Clean Logger Test")
    
    logger.info("System initialization", {
        "version": "1.0.0",
        "mode": "production",
        "components": ["fractal", "tick", "sigil"]
    })
    
    logger.success("Initialization complete")
    
    logger.parameter_block("Configuration", {
        "max_iterations": 100,
        "zoom_level": 250.0,
        "julia_constant": "-0.7269 + 0.1889i",
        "color_palette": ["red", "orange", "yellow"]
    })
    
    logger.status_list({
        "Tick Engine": True,
        "Fractal Renderer": True,
        "Sigil System": True,
        "Debug Mode": False
    })
    
    for i in range(5):
        logger.progress_update("Processing", i+1, 5, f"Step {i+1}")
        time.sleep(0.1)
    
    logger.warning("Test warning message")
    logger.error("Test error message", {"error_code": 404, "component": "test"})
    
    logger.section_footer("Clean Logger Test") 