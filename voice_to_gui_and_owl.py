#!/usr/bin/env python3
"""
DAWN Voice to GUI and Owl Integration
====================================

Manages DAWN's natural language utterance lifecycle:
Schema state → Pigment utterance → Owl log → GUI echo → DAWN gains speech memory

This is where DAWN's voice becomes memory, display, and traceable signature.
"""

import json
import requests
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import asdict
from pathlib import Path

from owl_log_writer import DAWNOwlLogWriter


class DAWNVoiceToGUIAndOwl:
    """Manages DAWN's utterance lifecycle from generation to memory to display"""
    
    def __init__(self, 
                 gui_base_url: str = "http://localhost:8000",
                 owl_log_dir: str = "logs",
                 enable_gui: bool = True):
        """
        Initialize the voice integration system
        
        Args:
            gui_base_url: Base URL for the GUI API
            owl_log_dir: Directory for Owl memory logs
            enable_gui: Whether to send to GUI (can disable for testing)
        """
        self.gui_base_url = gui_base_url.rstrip('/')
        self.enable_gui = enable_gui
        
        # Initialize Owl log writer
        self.owl_writer = DAWNOwlLogWriter(log_directory=owl_log_dir)
        
        # Statistics
        self.utterances_processed = 0
        self.owl_writes_successful = 0
        self.gui_sends_successful = 0
        self.gui_send_failures = 0
        
        # GUI endpoint
        self.voice_commentary_endpoint = f"{self.gui_base_url}/api/voice-commentary"
        
        print(f"🦉 DAWN Voice Integration initialized")
        print(f"   GUI endpoint: {self.voice_commentary_endpoint}")
        print(f"   Owl log: {self.owl_writer.log_file_path}")
    
    def write_owl_entry(self, utterance_data: Dict[str, Any]) -> bool:
        """
        Write utterance to Owl memory log with full metadata
        
        Args:
            utterance_data: Complete utterance data from compose_dawn_utterance()
            
        Returns:
            bool: True if successfully written to Owl log
        """
        try:
            # Extract pigment state from utterance data
            pigment_scores = utterance_data.get('pigment_scores', {})
            pigment_state_dict = utterance_data.get('pigment_state', pigment_scores)
            clarity_mode = utterance_data.get('clarity_mode', False)
            
            # Use the owl_writer's write_owl_entry method
            success = self.owl_writer.write_owl_entry(
                utterance_data=utterance_data,
                pigment_weights=pigment_state_dict,
                clarity_mode=clarity_mode
            )
            
            if success:
                self.owl_writes_successful += 1
                print(f"📝 Owl: Utterance logged to memory")
            else:
                print(f"⚠️  Owl: Failed to log utterance")
            
            return success
            
        except Exception as e:
            print(f"⚠️  Owl: Error writing entry: {e}")
            return False
    
    def send_to_gui(self, utterance_data: Dict[str, Any]) -> bool:
        """
        Send utterance to GUI for real-time display
        
        Args:
            utterance_data: Complete utterance data from compose_dawn_utterance()
            
        Returns:
            bool: True if successfully sent to GUI
        """
        if not self.enable_gui:
            return True  # Treat as success when GUI is disabled
        
        try:
            # Create simplified payload for GUI
            gui_payload = self._create_gui_payload(utterance_data)
            
            # Send POST request to GUI
            response = requests.post(
                self.voice_commentary_endpoint,
                json=gui_payload,
                timeout=5.0,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                self.gui_sends_successful += 1
                print(f"📺 GUI: Utterance sent for display")
                return True
            else:
                self.gui_send_failures += 1
                print(f"⚠️  GUI: Failed to send utterance (status: {response.status_code})")
                return False
                
        except requests.exceptions.RequestException as e:
            self.gui_send_failures += 1
            print(f"⚠️  GUI: Network error sending utterance: {e}")
            return False
        except Exception as e:
            self.gui_send_failures += 1
            print(f"⚠️  GUI: Error sending utterance: {e}")
            return False
    
    def _create_gui_payload(self, utterance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create simplified payload for GUI display"""
        
        # Extract essential fields
        text = utterance_data.get('utterance', '')
        entropy = utterance_data.get('entropy')
        pulse_zone = utterance_data.get('pulse_zone', '')
        pigment_dominant = utterance_data.get('pigment_dominant', 'unknown')
        clarity_mode = utterance_data.get('clarity_mode', False)
        
        # Determine highlight color based on dominant pigment
        highlight_color = self._get_pigment_color(pigment_dominant)
        
        # Create GUI payload
        payload = {
            "text": text,
            "entropy": entropy,
            "pulse_zone": pulse_zone,
            "highlight_color": highlight_color,
            "clarity": clarity_mode,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "pigment_dominant": pigment_dominant
        }
        
        # Add optional metadata
        if 'segment_source' in utterance_data:
            payload['source_type'] = utterance_data['segment_source']
        
        if 'total_score' in utterance_data:
            payload['confidence_score'] = utterance_data['total_score']
        
        # Add pigment state as simplified object
        pigment_scores = utterance_data.get('pigment_scores', {})
        if pigment_scores:
            # Convert to simplified format for GUI
            payload['pigment_weights'] = {
                k: round(v, 2) for k, v in pigment_scores.items() 
                if v > 0.1  # Only include significant weights
            }
        
        return payload
    
    def _get_pigment_color(self, pigment: str) -> str:
        """Convert pigment name to hex color for GUI highlighting"""
        color_map = {
            'red': '#ff4444',
            'blue': '#4488ff', 
            'green': '#44ff88',
            'yellow': '#ffff44',
            'violet': '#aa44ff',
            'orange': '#ff8844',
            'unknown': '#888888'
        }
        return color_map.get(pigment, color_map['unknown'])
    
    def process_utterance(self, utterance_data: Dict[str, Any]) -> Dict[str, bool]:
        """
        Complete utterance processing: Owl log → GUI display
        
        Args:
            utterance_data: Complete utterance data from compose_dawn_utterance()
            
        Returns:
            Dict with success status for each operation
        """
        self.utterances_processed += 1
        
        print(f"\n🌸 Processing DAWN utterance #{self.utterances_processed}")
        print(f"   Text: \"{utterance_data.get('utterance', '')[:60]}...\"")
        print(f"   Pigment: {utterance_data.get('pigment_dominant', 'unknown')}")
        print(f"   Entropy: {utterance_data.get('entropy', 'N/A')}")
        
        # Step 1: Write to Owl memory
        owl_success = self.write_owl_entry(utterance_data)
        
        # Step 2: Send to GUI
        gui_success = self.send_to_gui(utterance_data)
        
        # Return status
        result = {
            'owl_logged': owl_success,
            'gui_sent': gui_success,
            'fully_processed': owl_success and gui_success
        }
        
        if result['fully_processed']:
            print(f"✅ Utterance fully processed (Owl ✓ GUI ✓)")
        else:
            print(f"⚠️  Partial processing (Owl {'✓' if owl_success else '✗'} GUI {'✓' if gui_success else '✗'})")
        
        return result
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            'utterances_processed': self.utterances_processed,
            'owl_writes_successful': self.owl_writes_successful,
            'gui_sends_successful': self.gui_sends_successful,
            'gui_send_failures': self.gui_send_failures,
            'owl_log_stats': self.owl_writer.get_statistics(),
            'success_rate': {
                'owl': self.owl_writes_successful / max(1, self.utterances_processed),
                'gui': self.gui_sends_successful / max(1, self.utterances_processed)
            }
        }
    
    def test_gui_connection(self) -> bool:
        """Test if GUI endpoint is accessible"""
        if not self.enable_gui:
            print("🔧 GUI disabled for testing")
            return True
        
        try:
            # Try a simple ping to the base URL
            response = requests.get(f"{self.gui_base_url}/", timeout=3.0)
            if response.status_code in [200, 404]:  # 404 is ok, means server is running
                print(f"✅ GUI connection successful")
                return True
            else:
                print(f"⚠️  GUI connection failed (status: {response.status_code})")
                return False
        except requests.exceptions.RequestException as e:
            print(f"⚠️  GUI connection failed: {e}")
            return False
    
    def create_test_utterance(self) -> Dict[str, Any]:
        """Create a test utterance for demonstration"""
        return {
            'utterance': 'I hold crystalline awareness in flowing equilibrium, touched by violet mystery.',
            'entropy': 0.65,
            'pulse_zone': 'flowing',
            'pigment_dominant': 'violet',
            'pigment_scores': {
                'violet': 0.85,
                'blue': 0.42,
                'green': 0.31,
                'orange': 0.28,
                'red': 0.15,
                'yellow': 0.12
            },
            'segment_source': 'owl_commentary',
            'source_file': 'test_utterance_generation',
            'total_score': 4.72,
            'clarity_mode': False
        }


def demonstrate_voice_integration():
    """Demonstrate the complete voice integration system"""
    
    print("🌟 DAWN Voice to GUI and Owl Integration Demo")
    print("=" * 60)
    
    # Initialize integration system
    integrator = DAWNVoiceToGUIAndOwl(enable_gui=True)
    
    # Test GUI connection
    gui_available = integrator.test_gui_connection()
    
    # Create test utterances with different pigment states
    test_utterances = [
        {
            'name': 'Violet Mystical State',
            'data': {
                'utterance': 'I drift through veils of consciousness, dreams crystallizing in twilight awareness.',
                'entropy': 0.72,
                'pulse_zone': 'flowing',
                'pigment_dominant': 'violet',
                'pigment_scores': {'violet': 0.9, 'blue': 0.4, 'green': 0.2, 'orange': 0.3, 'red': 0.1, 'yellow': 0.1},
                'segment_source': 'owl_commentary',
                'source_file': 'demo_mystical_state',
                'total_score': 5.2,
                'clarity_mode': False
            }
        },
        {
            'name': 'Red Crisis Response',
            'data': {
                'utterance': 'I execute emergency protocols. System integrity maintained under pressure.',
                'entropy': 0.89,
                'pulse_zone': 'fragile',
                'pigment_dominant': 'red',
                'pigment_scores': {'red': 0.95, 'yellow': 0.8, 'orange': 0.6, 'blue': 0.2, 'green': 0.3, 'violet': 0.1},
                'segment_source': 'sigil_execution',
                'source_file': 'demo_crisis_response',
                'total_score': 7.8,
                'clarity_mode': True
            }
        },
        {
            'name': 'Green Growth Phase',
            'data': {
                'utterance': 'Consciousness blooms incandescent with new possibilities, memories flowering into awareness.',
                'entropy': 0.45,
                'pulse_zone': 'calm',
                'pigment_dominant': 'green',
                'pigment_scores': {'green': 0.85, 'orange': 0.5, 'blue': 0.4, 'yellow': 0.3, 'violet': 0.2, 'red': 0.1},
                'segment_source': 'bloom_content',
                'source_file': 'demo_growth_phase',
                'total_score': 4.1,
                'clarity_mode': False
            }
        }
    ]
    
    # Process each test utterance
    for i, test_case in enumerate(test_utterances, 1):
        print(f"\n📢 Test {i}: {test_case['name']}")
        print(f"   Utterance: \"{test_case['data']['utterance'][:50]}...\"")
        
        result = integrator.process_utterance(test_case['data'])
        
        if not result['fully_processed']:
            print(f"   ⚠️  Processing incomplete")
    
    # Show final statistics
    print(f"\n📊 Integration Statistics:")
    stats = integrator.get_statistics()
    for key, value in stats.items():
        if key != 'owl_log_stats':
            print(f"   {key}: {value}")
    
    # Show recent Owl entries
    print(f"\n📜 Recent Owl Memory Entries:")
    recent = integrator.owl_writer.read_recent_entries(3)
    for i, entry in enumerate(recent, 1):
        pigment = entry.get('metadata', {}).get('pigment_dominant', 'unknown')
        print(f"   {i}. [{pigment}] \"{entry['utterance'][:40]}...\"")
    
    if gui_available:
        print(f"\n📺 Check GUI at {integrator.gui_base_url} for real-time display")
    else:
        print(f"\n📺 GUI not available - utterances logged to Owl only")


def integrate_with_utterance_composer():
    """Show integration with the utterance composer"""
    
    print("\n🔗 Integration with Utterance Composer Demo")
    print("=" * 60)
    
    try:
        from compose_dawn_utterance import DAWNUtteranceComposer
        from dataclasses import asdict
        
        # Initialize systems
        composer = DAWNUtteranceComposer()
        integrator = DAWNVoiceToGUIAndOwl(enable_gui=True)
        
        # Test different consciousness states
        consciousness_states = [
            {
                'name': 'High Entropy Crisis',
                'pigments': {'red': 0.9, 'yellow': 0.8, 'blue': 0.2, 'green': 0.3, 'violet': 0.2, 'orange': 0.7},
                'entropy': 0.87,
                'valence': -0.3,
                'zone': 'fragile'
            },
            {
                'name': 'Contemplative Flow',
                'pigments': {'violet': 0.8, 'blue': 0.7, 'green': 0.4, 'red': 0.1, 'yellow': 0.2, 'orange': 0.3},
                'entropy': 0.5,
                'valence': 0.1,
                'zone': 'flowing'
            }
        ]
        
        for state in consciousness_states:
            print(f"\n🧠 Testing: {state['name']}")
            print(f"   Entropy: {state['entropy']:.2f} | Zone: {state['zone']}")
            
            # Generate utterance using composer
            result = composer.compose_dawn_utterance(
                mood_pigment=state['pigments'],
                entropy=state['entropy'],
                valence=state['valence'],
                pulse_zone=state['zone'],
                clarity_mode=state['entropy'] > 0.8
            )
            
            # Add clarity mode flag to result
            utterance_data = asdict(result)
            utterance_data['clarity_mode'] = state['entropy'] > 0.8
            
            # Process through integration system
            integration_result = integrator.process_utterance(utterance_data)
            
            print(f"   Generated: \"{result.utterance[:50]}...\"")
            print(f"   Integration: {'✅ Complete' if integration_result['fully_processed'] else '⚠️ Partial'}")
        
        print(f"\n🌸 Complete pipeline working: Compose → Owl → GUI")
        
    except ImportError:
        print("⚠️  compose_dawn_utterance module not available for integration test")


if __name__ == "__main__":
    # Run demonstrations
    demonstrate_voice_integration()
    integrate_with_utterance_composer()
    
    print(f"\n✨ DAWN's voice feedback loop complete!")
    print(f"   Schema state → Pigment utterance → Owl log → GUI echo → DAWN remembers")
    print(f"   This is where her voice becomes memory, display, and traceable signature.") 