#!/usr/bin/env python3
"""
DAWN GUI Integration Module
Connects the Tkinter GUI with DAWN's backend visualizers and sigil command stream

File: gui/dawn_gui_integration.py
"""

import threading
import time
import queue
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class DAWNGuiIntegration:
    """Integration layer between DAWN backend and GUI"""
    
    def __init__(self):
        self.gui = None
        self.running = False
        self.data_queue = queue.Queue()
        self.integration_thread = None
        
        # Backend visualizer references
        self.sigil_visualizer = None
        self.dawn_central = None
        
        # Data processing
        self.last_sigil_data = []
        self.last_update_time = time.time()
        
    def initialize(self, gui_instance):
        """Initialize integration with GUI instance"""
        self.gui = gui_instance
        logger.info("DAWN GUI integration initialized")
        
        # Try to connect to backend visualizers
        self.connect_to_backend()
        
    def connect_to_backend(self):
        """Attempt to connect to DAWN backend systems"""
        try:
            # Try to import and connect to backend visualizers
            from backend.visual.sigil_command_stream_visualizer import get_sigil_command_stream_visualizer
            from backend.main import DAWNCentral
            
            # Get global DAWN central instance if available
            try:
                import builtins
                self.dawn_central = getattr(builtins, 'dawn_central', None)
                if self.dawn_central:
                    self.sigil_visualizer = self.dawn_central.visualizers.get('sigil_command_stream')
                    logger.info("Connected to DAWN backend systems")
                else:
                    logger.warning("DAWN central instance not found in globals")
            except Exception as e:
                logger.warning(f"Could not access DAWN central: {e}")
                
        except ImportError as e:
            logger.warning(f"Could not import DAWN backend: {e}")
            
    def start_integration(self):
        """Start the integration thread"""
        if not self.running:
            self.running = True
            self.integration_thread = threading.Thread(target=self._integration_loop, daemon=True)
            self.integration_thread.start()
            logger.info("DAWN GUI integration started")
    
    def stop_integration(self):
        """Stop the integration thread"""
        self.running = False
        if self.integration_thread:
            self.integration_thread.join(timeout=1)
        logger.info("DAWN GUI integration stopped")
    
    def _integration_loop(self):
        """Main integration loop - pulls data from backend and pushes to GUI"""
        while self.running:
            try:
                # Get data from backend
                backend_data = self.get_backend_data()
                
                if backend_data and self.gui:
                    # Inject data into GUI
                    self.gui.inject(backend_data)
                
                # Sleep for update interval
                time.sleep(0.5)  # 2Hz update rate
                
            except Exception as e:
                logger.error(f"Integration loop error: {e}")
                time.sleep(1)
    
    def get_backend_data(self) -> Optional[Dict[str, Any]]:
        """Get current data from DAWN backend systems"""
        data = {}
        
        try:
            if self.dawn_central:
                # Get general DAWN state
                dawn_state = self.dawn_central.get_state() if hasattr(self.dawn_central, 'get_state') else {}
                
                # Extract core metrics
                heat = dawn_state.get('heat', 50)
                zone = self.determine_zone_from_state(dawn_state)
                
                # Get SCUP data
                scup_data = dawn_state.get('scup', {})
                entropy = dawn_state.get('entropy', 0.5)
                
                data.update({
                    'heat': heat,
                    'zone': zone,
                    'entropy': entropy,
                    'scup': scup_data.get('coherence', 0.5) if isinstance(scup_data, dict) else 0.5,
                    'coherence': scup_data.get('coherence', 0.5) if isinstance(scup_data, dict) else 0.5
                })
            
            # Get sigil data
            sigil_data = self.get_sigil_data()
            if sigil_data:
                data['sigils'] = sigil_data
            
            # Generate tick message
            if data:
                tick_count = getattr(self.dawn_central, 'tick_count', 0) if self.dawn_central else 0
                data['tick'] = f"T{tick_count:04d} - Live DAWN data | Heat: {data.get('heat', 0)}%"
                data['summary'] = self.generate_live_summary(data)
            
            return data if data else None
            
        except Exception as e:
            logger.error(f"Error getting backend data: {e}")
            return None
    
    def get_sigil_data(self) -> List[Dict[str, Any]]:
        """Extract sigil data from backend visualizer"""
        sigils = []
        
        try:
            if self.sigil_visualizer and hasattr(self.sigil_visualizer, 'get_visualization_data'):
                viz_data = self.sigil_visualizer.get_visualization_data()
                
                # Extract active sigils from visualizer
                active_sigils = viz_data.get('active_sigils', [])
                
                for sigil in active_sigils:
                    # Map visualizer sigil to GUI format
                    gui_sigil = {
                        'symbol': sigil.get('symbol', '◉'),
                        'name': sigil.get('trigger', 'Unknown').replace('_', ' ').title(),
                        'class': sigil.get('category', 'monitor'),
                        'heat': int(sigil.get('intensity', 0.5) * 100),
                        'decay': sigil.get('age', 0) / 100.0  # Convert age to decay
                    }
                    
                    # Map visualizer categories to GUI classes
                    category_map = {
                        'attention': 'attention',
                        'memory': 'memory',
                        'reasoning': 'reasoning',
                        'creativity': 'creativity',
                        'integration': 'integration',
                        'action': 'action',
                        'meta': 'meta'
                    }
                    
                    gui_sigil['class'] = category_map.get(gui_sigil['class'], 'monitor')
                    sigils.append(gui_sigil)
                
                # Store for comparison
                self.last_sigil_data = sigils
                
        except Exception as e:
            logger.error(f"Error getting sigil data: {e}")
            # Fall back to last known data
            sigils = self.last_sigil_data
        
        return sigils
    
    def determine_zone_from_state(self, state: Dict[str, Any]) -> str:
        """Determine cognitive zone from DAWN state"""
        try:
            heat = state.get('heat', 50)
            entropy = state.get('entropy', 0.5)
            
            if heat > 80:
                return "surge"
            elif heat > 60:
                return "active"
            elif heat < 20:
                return "dormant"
            elif entropy > 0.8:
                return "transcendent"
            else:
                return "calm"
                
        except Exception:
            return "calm"
    
    def generate_live_summary(self, data: Dict[str, Any]) -> str:
        """Generate live summary from DAWN state"""
        try:
            summaries = []
            
            heat = data.get('heat', 0)
            zone = data.get('zone', 'calm')
            entropy = data.get('entropy', 0.5)
            coherence = data.get('coherence', 0.5)
            
            # Heat-based insights
            if heat > 80:
                summaries.append("🔥 High thermal intensity - Peak cognitive engagement.")
            elif heat < 30:
                summaries.append("❄️ Low thermal state - Quiet reflection mode.")
            else:
                summaries.append("🌡️ Thermal regulation balanced.")
            
            # Zone insights
            if zone == "surge":
                summaries.append("⚡ Cognitive surge active - Processing complex information.")
            elif zone == "transcendent":
                summaries.append("✨ Transcendent awareness - Creative breakthroughs possible.")
            elif zone == "active":
                summaries.append("🧠 Active cognition - Engaged processing state.")
            
            # Coherence insights
            if coherence > 0.8:
                summaries.append("🎯 High schema coherence - Clear understanding achieved.")
            elif coherence < 0.3:
                summaries.append("🔄 Schema integration in progress.")
            
            # Entropy insights
            if entropy > 0.7:
                summaries.append("🌀 High creative entropy - Novel patterns emerging.")
            elif entropy < 0.2:
                summaries.append("📐 Low entropy - Focused pattern matching.")
            
            return " ".join(summaries)
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "🔴 Live DAWN connection active - Real-time cognitive monitoring engaged."


# Global integration instance
_gui_integration = None

def get_gui_integration() -> DAWNGuiIntegration:
    """Get the global GUI integration instance"""
    global _gui_integration
    if _gui_integration is None:
        _gui_integration = DAWNGuiIntegration()
    return _gui_integration

def initialize_gui_integration(gui_instance):
    """Initialize GUI integration with a GUI instance"""
    integration = get_gui_integration()
    integration.initialize(gui_instance)
    integration.start_integration()
    return integration

def shutdown_gui_integration():
    """Shutdown GUI integration"""
    global _gui_integration
    if _gui_integration:
        _gui_integration.stop_integration()
        _gui_integration = None 